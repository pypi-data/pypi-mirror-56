# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 11:32:50 2019

@author: Louis-Philippe Baillargeon
"""

import numpy as np
from sklearn import decomposition
from PointSelector import SelectFromCollection
from SI_File_Toolbox import plotSpectra


def computeShow(S_hier, nb_c, Emin = 0, Emax = 20):
#Computes the PCA and opens the windows to select wanted spectra
    
    #substract mean for pca
    Smoy = np.mean(S_hier, axis = 1)
    S_centered = S_hier.T-Smoy
    S_centered = S_centered.T
    
    #pca transformation
    pca = decomposition.PCA(n_components=nb_c)
    pca.fit(S_centered)
    
    components = pca.components_
    plotSpectra(components, Emin = Emin, Emax = Emax, title = 'Principal Component', ylabel = 'score')
    
    return 


def computeSelect(S_hier, nb_c):
#Computes the PCA and opens the windows to select wanted spectra
    
    #substract mean for pca
    Smoy = np.mean(S_hier, axis = 1)
    S_centered = S_hier.T-Smoy
    S_centered = S_centered.T
    
    #pca transformation
    pca = decomposition.PCA(n_components=nb_c)
    pca.fit(S_centered)
    
    Spca = pca.transform(S_centered)  # spectra expressed in principal components
    
    Sselect = [SelectFromCollection(Spca, S_hier)   for i in range(nb_c)]
    
    return Sselect
    

