#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 08:51:47 2019

@author: fblavoie
"""




from init import KmeansInit as ini
import numpy as np
from scipy.optimize import minimize
from functools import partial
from mcrllm import init





def pcanipals(Xh,A,it=1000,tol=1e-4):
   
    
    obsCount,varCount = np.shape(Xh);
    T = np.zeros([obsCount,A]);
    P = np.zeros([varCount,A]);
    nr = 0;
    
    for a in range(A):
        
        th = np.array([Xh[:,0]]).T;
        ende = False;
    
        while(ende==False):
            
            nr+=1
            ph=Xh.T@th/np.linalg.inv(th.T@th)
            ph=ph/np.linalg.norm(ph)
            thnew=Xh@ph
            prec = (thnew-th).T@(thnew-th)
            th=thnew
            
            if(prec<=tol**2):
                ende=True
            elif(it<=nr):
                ende=True
    
        Xh = Xh - th@ph.T
        T[:,a] = th[:,0]
        P[:,a] = ph[:,0]
    
    return T,P
    
    





class mcrllm:
    
    
    def __init__(self,X,nb_c,method="standard",fact_ini=.5):
        
        # Save Xraw and normalize data
        self.Xraw = X.copy()
        self.Xsum = np.sum(X,axis=1)
        self.X = X/np.array([np.sum(X,axis=1)]).T
        
        self.pix,self.var = np.shape(self.X)
        self.nb_c = nb_c
        self.method = method
        self.expvar = np.inf
        self.fact_ini = .5
        
        # History initialization
        self.allC = []
        self.allS = []
        self.allphi = []
        
        
        self.C = np.ones([self.pix,self.nb_c])/nb_c
        
        # PCA reconstruction
        X_m = np.array([np.mean(self.X,axis=0)])
        X_s = np.array([np.std(self.X,axis=0)])
        Xpca = (self.X - X_m)/X_s
        T,P = pcanipals(Xpca,nb_c-1)
        self.Xrec = (T@P.T)*X_s+X_m
            
        # Initialization
        self.Sini = ini.initialisation(self.X, nb_c)
        #if(np.sum(self.Sini <= 0)>0):
        #    raise("Bas initialization")
        self.S = self.Sini.copy()
        
        
    
    def iterate(self,nb_iter=1):
        
        for iteration in range(nb_iter):
            #print("Iteration {:.0f}".format(len(self.allS)+1))
            self.C_plm()
            self.S_plm()
            
            
            
    
    def C_plm(self):
        
        c_new = np.zeros((self.pix,self.nb_c))
        

        # on calcule les concentrations optimales pour chaque pixel par maximum likelihood 
        for pix in range(self.pix):
            sraw = self.S*self.Xsum[pix]
            c_new[pix,:] = self.pyPLM(sraw, self.Xraw[pix,:], self.C[pix,:])
                
                
        # avoid errors (this part should not be necessary)
        c_new[np.isnan(c_new)] = 1/self.nb_c
        c_new[np.isinf(c_new)] = 1/self.nb_c
        c_new[c_new<0] = 0
        c_sum1 = np.array([np.sum(c_new,axis=1)]).T
        c_new = c_new/c_sum1

        self.C = c_new.copy()
        self.allC.append( c_new.copy() )
    
            
        
        
    
    def Sphi(self,phi,h):
    
        C_m = self.C**phi
            
        S = np.linalg.inv(C_m[h,:].T@C_m[h,:])@C_m[h,:].T@self.X[h,:]
        S[S<1e-15] = 1e-15
        S = S/np.array([np.sum(S,axis=1)]).T
        
        return S
    
    
    
    
    def S_plm(self):
        
        
        h = np.random.permutation(len(self.X))
        phi_optimal = 1
        
        if self.method == "phi":
            allMSE = []
            all_phis = np.arange(.1,10.1,.1)
            
            for phi in all_phis:
                S = self.Sphi(phi,h)
                allMSE.append(np.sum( (S-self.S)**2 ))
                
            phi_optimal = all_phis[np.argmin(allMSE)]
            self.S = self.Sphi(phi_optimal,h)
            
            
        elif( (self.method=="heuristic") | (self.method=="sg") ):
            
            if(self.method=="heuristic"):
                h = h[:int(len(self.X)/20)]
            newS = self.Sphi(phi_optimal,h)
            delta = newS-self.S
            fact = self.fact_ini
        
            cont = True
            while( cont ):
                St = newS*fact + self.S*(1-fact)
                expvar_t = np.mean( (self.Xrec - self.C@St)**2 )
                print(expvar_t)
                if( expvar_t < self.expvar ):
                    cont = False
                    self.expvar = expvar_t
                else:
                    fact = fact - .1
                
                if(fact<1e-15):
                    cont=False
                
        
            print(fact)
            self.S = self.S + fact*delta
            
        else: # Standard
            
            self.S =  self.Sphi(phi_optimal,h)
            
            
        self.allS.append( self.S.copy() )
        self.allphi.append(phi_optimal)
        
        
        
    
    
    def pyPLM(self, sraw, xrawPix, c_old):
        

        # sum of every value is equal to 1
        def con_one(c_old):
            return 1-sum(c_old) 
        
        
        
        def regressLLPoisson(sraw,  xrawPix, c_pred):
            
            #compute prediction of counts
            yPred = c_pred @ sraw
            nb_lev = len(yPred) #?
            # avoid errors, should (may?) not be necessary
            yPred[yPred < 1/1000000] = 1/1000000
            logLik = -np.sum(xrawPix*np.log(yPred)-yPred)
            return (logLik)
        
        
        
        def jacobians(nb_c, xrawPix, sraw, c_pred):

            #compute prediction of counts
            yPred = c_pred @ sraw
            
            #compute jacobians
            jacC = np.zeros(nb_c)
            
            for phase in range(nb_c):    
                jacC[phase] = -np.sum(((xrawPix*sraw[phase,:])/yPred)-sraw[phase,:])    
            return(jacC) 
        
        
        
        # all values are positive
        bnds = ((0.0, 1.0),) * self.nb_c
        cons = [{'type': 'eq', 'fun': con_one}]
   
                
        # Run the minimizer    
        results = minimize(partial(regressLLPoisson, sraw,  xrawPix), c_old,\
                           method='SLSQP', bounds=bnds, constraints=cons, \
                           jac = partial(jacobians, self.nb_c, xrawPix, sraw))
        results = np.asarray(results.x)
        

        c_new = results.reshape(int(len(results) / self.nb_c), self.nb_c)
        
        
        return c_new
        
        
    
    

        