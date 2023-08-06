# -*- coding: utf-8 -*-
"""
@auteurs : Louis-Philippe Baillargeon et Hugo Caussan
"""
#%% User Input
from init import KmeansInit as ini                                  # Choose the initialization to use1
from fct_MCRLLM import HyperspectralSegmentation_MCR_LLM             # Import the algorithm to use


# SET THE PARAMETERS

#paramètres d'affichage
Emin = 490.234                  # énergie du niveau 0 eV
Emax = 591.885                  # énergie du niveau max eV
pas = 1                         # distance entre les pixels (nm)

#file parameters
path = 'data_2.txt'             # choose your file
dim = 2                         # 2D or 3D file
nb_c = 7                       # Number of components(phases)

#analysis parameters - general
Bin = False                     # Bin the data
correctPix = False              # Enable the cosmic Xray filter, only works with sufficient dwell time
nb_etype = 3                    # Criteria for cosmic Xray

#analysis parameters - mcrllm 
nb_i = 5                        # Number of iterations in mcr_llm



#%% Code
import numpy as np
from SI_File_Toolbox import loadFile, normalize, dataBin, plotCompare, plotSpectraGroup
from cosmicRays import findWeirdPixels, estimateWeirdPixelsList
import matplotlib.pyplot as plt


# LOAD THE DATA

print("load data")  

X3 = loadFile(path)
if dim == 3:
    dim1 = X3.shape[0]
    dim2 = X3.shape[1]
    nb_level = X3.shape[2]
    nb_pix = dim1*dim2
    
    
elif dim == 2:
    nb_level = X3.shape[1]
    nb_pix = X3.shape[0]




X = np.reshape(X3, (nb_pix, nb_level))
        

# Bin the data set
        
if Bin:
    print("\nbin data :")     
    X = dataBin(X, 2)


# Deal with weird pixels

# Finds the corrputed by Xray energy levels of a pixel by comparing it to the same levels of other pixels. If its too large, it is approximated by an average of its neigbours
# Only works with high count data
    
if correctPix:
    print("\nDeal with weird pixels:")     
    Xtrash = np.copy(X)
    
    print("\nfind weird pixels:")    
    weirdlev, weirdmap = findWeirdPixels(np.copy(X), nb_etype)

    
    print("\nestimate weird pixels:")    #partie un peu longue, pourrait améliorer   
    X = estimateWeirdPixelsList(np.copy(X), weirdlev, weirdmap, neighbours = 3)
    

#avoid errors, if a energy level has 0 counts on all pixels, it causes log(0) and the level is meaningless, so we take it out
deletedLevels = []
nb_deleted = 0

for lev in range(nb_level):
    
    if np.sum(X[:,lev-nb_deleted]) <= 0:
        
        deletedLevels.append(lev)
        X= np.delete(X, lev-nb_deleted, axis = 1)
        nb_deleted = nb_deleted + 1


# normalize data
Xraw = np.copy(X)
X = normalize(X)


#%% START THE RUN

print("Initialisation :")
Si = ini.initialisation(X, nb_c) # Initialisation



print("MCR LLM : " + str(nb_c) + " composantes - " + str(nb_i) +" itérations\n")
C, S = HyperspectralSegmentation_MCR_LLM.mcr_llm(Xraw, nb_c, Si, nb_i) # Algorithm


#%% Show the results
#Insert deleted spectra back (the spectra was 0 that's why we took it out)
for i in range(nb_deleted):
    S = np.insert(S,deletedLevels[i], np.zeros(nb_c), axis = 1)
    


#rearrange data
if dim == 3:
    C3 = np.reshape(C, (dim1,dim2, nb_c))
    C = np.copy(C3)
    plotCompare(S, Emin, Emax, C, pas = 1, log = False)
    
else:
    plt.figure()
    plt.plot(C)
    
plotSpectraGroup(S, np.arange(nb_c), Emin = Emin, Emax = Emax)
