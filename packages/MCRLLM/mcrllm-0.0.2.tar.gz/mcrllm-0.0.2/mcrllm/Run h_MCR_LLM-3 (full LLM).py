# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 13:41:53 2019

@auteur : Louis-Philippe Baillargeon
"""
#%% User Input

#analysis parameters - mcrllm 
nb_i = 10                        # Number of iterations in mcr_llm


#%% code
from SI_File_Toolbox import plotCompare, plotSpectraGroup
import matplotlib.pyplot as plt
import numpy as np
from fct_MCRLLM import HyperspectralSegmentation_MCR_LLM    # Import the algorithm to use

#Load spectrum
Si = np.zeros((nb_c,nb_level))

for i in range(nb_c): 
    Si[i,:] = np.copy(Sselect[i].selectedSpectra)
    

# MCR_LLM
print('MCR-LLM')
C, S = HyperspectralSegmentation_MCR_LLM.mcr_llm(Xraw, nb_c, Si, nb_iter = nb_i)


for i in range(nb_deleted):
    S = np.insert(S,deletedLevels[i], np.zeros(nb_c), axis = 1)

# Show the results

#rearrange data
if dim == 3:
    C3 = np.reshape(C, (dim1,dim2, nb_c))
    C = np.copy(C3)
    plotCompare(S, Emin, Emax, C, pas = 1, log = False)
    
else:
    plt.figure()
    plt.plot(C)
    
plotSpectraGroup(S, [1,2], Emin = Emin, Emax = Emax)