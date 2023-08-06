
# -*- coding: utf-8 -*-
'''
@auteurs : Louis-Philippe Baillargeon 
'''

# imports
import numpy as np
from SI_File_Toolbox import loadFile
import matplotlib.pyplot as plt
from math import factorial



def pureSpecies4carres1Cercle(path):
        
        
    X3D = loadFile(path, dim = 3)


    # Select data
    group1 = np.arange(0,100)
    group2 = np.arange(150,250)
    group3 = np.arange(110,140)
    
    allPix = np.arange(0,256)
    
    
    X1 = np.delete(X3D, np.delete(allPix, group1), axis = 0)
    X1 = np.delete(X1, np.delete(allPix, group1), axis = 1)
    
    X2 = np.delete(X3D, np.delete(allPix, group2), axis = 0)
    X2 = np.delete(X2, np.delete(allPix, group1), axis = 1)
    
    X3 = np.delete(X3D, np.delete(allPix, group3), axis = 0)
    X3 = np.delete(X3, np.delete(allPix, group3), axis = 1)
    
    return X1,X2,X3


def pureSpectra(X, dim = 3):
#sum of spectra on all pixels. Pixels must be of same specie to obtain pure spectra
    
    if dim ==3:
        S = np.sum(np.sum(X, axis = 0), axis = 0)
        S = S/(X.shape[0]*X.shape[1])
        
    elif dim==2:
        S = np.sum(X,axis = 0)
        
    plt.figure()
    plt.plot(S)
    return(S)
    
    
    
    
def findModeX(X, mode):
    
    lev = np.array([])
    
    for level in range(len(X[0,0,:])):
        dis1 = np.reshape(X[:,:,level], X.shape[0]*X.shape[1])
        
        count = np.zeros(max(dis1))
        
        for cnt in range(max(dis1)):
            for pix in range(len(dis1)):
                if dis1[pix] == cnt:
                    count[cnt] = count[cnt] + 1
        
        count = count/sum(count)
        countMode = np.argmax(count)
        if countMode == mode:
            lev = np.append(lev, level)
            
    return lev
    
    
    
    
    
class distribution:
#compute the distribution of counts on given energy level for multiple pixels of same specie
    @classmethod
    def __init__(self, X, level, dim = 3, maxl = 0):
        
        
        self.maxl = np.max([np.max(X),maxl])
        
        if dim ==3:
            self.dis = np.reshape(X[:,:,level], X.shape[0]*X.shape[1])
            
        elif dim ==2:
            self.dis = X[:,level]
            
        elif dim ==1:
            self.dis = X
        
        self.count = np.zeros(self.maxl)
        self.xraw = np.arange(self.maxl)
        
        
        if np.max(self.dis) == 0:
            self.count[0] =len(self.dis)
            self.countMode = 0
            self.countMean = 0
            self.countNorm =np.zeros(self.maxl)
            
        else:
            
            for cnt in range(np.max(self.dis)):
                for pix in range(len(self.dis)):
                    if self.dis[pix] == cnt:
                        self.count[cnt] = self.count[cnt] + 1
                        
            
            
            self.countSum = np.sum(self.count)
            self.countNorm = np.zeros(self.maxl)
            self.countNorm[:np.max(self.dis)] = self.count[:np.max(self.dis)]/self.countSum
            self.countMode = np.argmax(self.count) 
            self.abundance = self.xraw/self.countSum
            self.x = np.linspace(0,np.max(self.abundance), len(self.xraw))
            countMean = 0
            for cnt in range(len(self.count)):
                countMean = countMean + self.count[cnt]*cnt
                
            self.countMean = countMean/self.countSum
            

def lookDist(espece, level):
    dis = distribution(espece, level, dim = 2)
    yPred = dis.countMean
    
    
    
    plt.figure()
    plt.title('distribution of level ' + str(level) + ', espèce pure 3 , 4 carrés un cercle, \n real mean = ' + str(dis.countMean) + ', yPred = ' + str(yPred),fontsize = 30)
    
    # poisson
    fact = np.array([factorial(dis.xraw[i]) for i in range(len(dis.xraw))])
    lik = np.divide(np.multiply(np.power(yPred, dis.xraw), np.exp(-yPred)), fact)
    plt.plot(dis.xraw, lik , 'b-', lw=5, alpha=0.6, label='poisson')
    

    # mean 
    plt.axvline(x=dis.countMean, label='real mean')
    
    # ypred
    plt.axvline(x=yPred, color = 'm', label='yPred')
    
    
    #dots
    plt.plot(dis.countNorm, 'ro',  label='sum of counts of each pixel of same specie on level ' + str(level))
    
    #legend
    plt.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=0., fontsize = 30)
    plt.xlabel('counts', fontsize = 35)
    plt.ylabel('nb pixels', fontsize = 35)
        

        
        
        




