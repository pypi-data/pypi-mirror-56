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
from Demi_LLM_Python import HyperspectralSegmentation_Demi_LLM    # Import the algorithm to use

#Load spectrum
Si = np.zeros((nb_c,nb_level))

for i in range(nb_c): 
    Si[i,:] = np.copy(Sselect[i].selectedSpectra)
    
S = Si    

# MCR_LLM
print('MCR-LLM')
C = HyperspectralSegmentation_Demi_LLM.mcr_llm(S, Xraw)




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