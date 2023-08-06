# -*- coding: utf-8 -*-
"""
@author: Hugo Caussan
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
import pysptools.eea.eea
import math
from tqdm import tqdm
        


"""All intitialisation methods to extract the endmembers"""
################################################################################################################################

class KmeansInit: #Kmeans initialisation
    @classmethod
    def initialisation(cls, x, nb_c, n_init=10):

        s = KMeans(n_clusters=nb_c, n_init = n_init).fit(x).cluster_centers_

        return s

################################################################################################################################

class MBKmeansInit: #Mini Batch Kmeans (plus rapide mais moins robuste)
    @classmethod
    def initialisation(cls, x, nb_c):
        
        ctr_k = MiniBatchKMeans(n_clusters = nb_c).fit(x)
        s = ctr_k.cluster_centers_
        
        return s
################################################################################################################################

class NFindrInit:
    @classmethod
    def initialisation(cls, x, nb_c):
        size0 = x.shape[0]
        size1 = x.shape[1]
        xr = np.reshape(x, (1, size0, size1) ) # NFindr travaille avec des jeux de données 3D...
        s = pysptools.eea.NFINDR.extract(cls, xr, nb_c)
        
        return s

################################################################################################################################
   
class RobustNFindrInit:
    @classmethod
    def initialisation(cls, x, nb_c, fraction = 0.1, min_spectra = 50, nb_i = 50): # Initialisaiton KMeans + NMF / Voir avec Ryan Gosselin pour les explications et évolutions
        """
        fraction : Fraction du jeu de données par échantillon
        min_spectra : minimum de spectre pour garder un échantillong
        nb_i : nombre d'échantillons à créer
        """
        
        
        def km(x, nb_c):
            k = KMeans(n_clusters=nb_c).fit(x)
            IDX = k.labels_
            C = k.cluster_centers_
            return IDX, C
        
        
        s1 = x.shape[0]
        
        fX = math.ceil(s1*fraction)

        
        BESTC = np.array(())
       
        DETC = 0
        for i in tqdm(range(nb_i)):
            
            randomVector = np.random.choice(s1, fX, replace = False)# Create random vector with unique values
            sampX = x[randomVector,:]#Pick a sample in x according to the randomVector
            
            #Run Kmeans
            IDX, C = km(sampX, nb_c)
            
            #Check Number of pixels in each kmeans centroid
            U, nbU = np.unique(IDX, return_counts=True);
            
            
            if min(nbU) > min_spectra: #Do not keep this bootstrap if too few pixels fall in a category
                a = np.zeros((nb_c,1)) + 1 #Start NMF
                C1 = np.column_stack((a, C))
                CC = C1@C1.T
                detc = np.linalg.det(CC)
                if detc > DETC:
                    DETC = detc
                    BESTC = np.copy(C)
                    #print(nbU)
                                           
        return BESTC
    
################################################################################################################################

class RobustNFindrV2Init:
    @classmethod
    def initialisation(cls, x, nb_c, fraction = 0.1, min_spectra = 50, nb_i = 50):
        """
        fraction : Fraction du jeu de données par échantillon
        min_spectra : minimum de spectre pour garder un échantillong
        nb_i : nombre d'échantillons à créer
        """
        
        def km(x, nb_c):
            k = KMeans(n_clusters=nb_c).fit(x)
            IDX = k.labels_
            C = k.cluster_centers_
            return IDX, C
        
        s1 = x.shape[0]
        f = fraction # Fraction to keep in each bootstrap
        fX = math.ceil(s1*f)

        allS = np.array(())


        for i in tqdm(range(nb_i)):
            randomVector = np.random.choice(s1, fX, replace = False)# Create random vector with unique values
            sampX = x[randomVector,:]#Pick a sample in x according to the randomVector
    
        #Run Kmeans
            IDX, C = km(sampX, nb_c)
        
            #Check Number of pixels in each kmeans centroid
            U, nbU = np.unique(IDX, return_counts=True);

            #print(nbU)
            if min(nbU) > min_spectra: #Do not keep this bootstrap if too few pixels fall in a category
                try:
                    allS = np.vstack((allS, C));
                except ValueError:
                    allS = np.copy(C)
        
        size0 = allS.shape[0]
        size1 = allS.shape[1]
        allS = np.reshape(allS, (1, size0, size1) ) # NFindr travaille avec des jeux de données 3D...
        s = pysptools.eea.NFINDR.extract(cls, allS, nb_c)
                    
        return s
    
################################################################################################################################

class AtgpInit: # Automatic Target Generation Process
    @classmethod
    def initialisation(cls, x, nb_c):
        
        s = pysptools.eea.eea.ATGP(x, nb_c)
        
        return s[0]
    
################################################################################################################################
    
class FippiInit: # Fast Iterative Pixel Purity Index
    @classmethod
    def initialisation(cls, x, nb_c):
        
        t = pysptools.eea.eea.FIPPI(x, q = nb_c)
        
        s = t[0]
        s = s[:nb_c, :]
        
        return s
  
################################################################################################################################
    
class PpiInit: # Pixel Purity Index
    @classmethod
    def initialisation(cls, x, nb_c):
        numSkewers = 10000
        s = pysptools.eea.eea.PPI(x, nb_c, numSkewers)
        
        return s[0]   
 
    
################################################################################################################################
class nKmeansInit:    
    @classmethod
    def initialisation(cls, x, nb_c, n = 15): 
        
        """Sometimes it's necessary to run Kmeans for more component than we want, to get the expected spectras, this version runs
        the initialisation for nb_c + n components, and keep the nb_c centroids containing the most pixels"""

        
        nb_ci = nb_c + n 
        
        init = KMeans(nb_ci).fit(x)
        s = init.cluster_centers_
        lab = init.labels_
        
        U, nbU = np.unique(lab, return_counts=True);# nbU is the number of pixels in each centroid
        
        ind = nbU.argsort()[-nb_c:] # Get the indices of the nb_c centroids containing the most pixels
        
        s = s[ind,:] # Keep only the nb_c spectra
        
        
        return s



    
    
    
    
    
    