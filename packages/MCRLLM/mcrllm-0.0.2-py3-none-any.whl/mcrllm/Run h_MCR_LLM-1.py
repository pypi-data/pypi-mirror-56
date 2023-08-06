# -*- coding: utf-8 -*-
'''
@auteurs : Louis-Philippe Baillargeon et Hugo Caussan
'''
#%% User Input


# SET THE PARAMETERS

#paramètres d'affichage
Emin = 490.234                  # énergie du niveau 0 eV
Emax = 591.885                  # énergie du niveau max eV
Ppas = 1                        # distance entre les pixels (nm)

#file parameters
path = 'data_2.txt'             # choose your file
dim = 2                         # 2D or 3D file
nb_c = 3                       # Number of components

#analysis parameters - general
Bin = False                     # Bin the data
correctPix = False              # Enable the cosmic Xray filter, only works with sufficient dwell time
nb_etype = 3                    # Criteria for cosmic Xray


#analysis parameters - hiearchical init
nb_imcr = 1                     # Number of itteration of mcrllm in hierarchical
min_pixels = 1                  # Minimum of pixel in a division (should be about one percent of total pixels)
max_pixels = 10                 # Maximum of pixels in a division (should be 3 to 10 times bigger than min pixels)
Max_level = 40                  # Maximum of subdivision



#%% Code

# imports
import numpy as np
from h_MCR_LLM_Python import h_MCR_LLM
from SI_File_Toolbox import loadFile, dataBin, normalize
from cosmicRays import findWeirdPixels, estimateWeirdPixelsList
import pcaselect

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

        

# Bin the data set
        
if Bin:
    print("\nbin data :")     
    X = dataBin(X3, Bin)





# Deal with weird pixels
# Finds the corrputed by Xray energy levels of a pixel by comparing it to the same levels of other pixels. If its too large, it is approximated by an average of its neigbours
# Only works with high count data
    
if correctPix:
    print("\nDeal with weird pixels:")     
    Xtrash = np.copy(X)
    
    print("\nfind weird pixels:")    
    weirdlev, weirdmap = findWeirdPixels(np.copy(X), nb_etype)

    
    print("\nestimate weird pixels:")    #partie un peu longue, pourrait améliorer   
    X = estimateWeirdPixelsList(np.copy(X), weirdlev, weirdmap, neighbours = 5)

Xraw = np.copy(X)


#avoid errors, if a energy level has 0 counts on all pixels, it causes log(0) and the level is meaningless, so we take it out
deletedLevels = []
nb_deleted = 0

for lev in range(nb_level):
    
    if np.sum(Xraw[:,lev-nb_deleted]) <= 0:
        
        deletedLevels.append(lev)
        Xraw = np.delete(Xraw, lev-nb_deleted, axis = 1)
        nb_deleted = nb_deleted + 1







# START THE RUN


# Run h_MCR_LLM (might take alot of time)
print("MCR hiérachique jusqu'à " + str(Max_level) + " niveaux - min_pixels = " + str(min_pixels) + " :\n")
S_hier = h_MCR_LLM.h_mcr_llm(nb_imcr, min_pixels, max_pixels, Max_level, Xraw)

np.save('S_hier.npy', S_hier)




print("\nPCA :")                    

Sselect = pcaselect.computeShow(S_hier, nb_c, Emin = Emin, Emax = Emax)







