# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 13:35:05 2019

@auteur : Louis-Philippe Baillargeon
"""
#%% User input

# User input is set in Run h_MCR_LLM, just make sure that you don't delete your variables automatically when you run the script 
# in Run/Configuration per file/General Settings/Remove all variales before execution ; must be unchecked



#%% PCA of h_MCR results - choose spectrum

#loads
import numpy as np
import pcaselect


S_hier = np.load('S_hier.npy')

Sselect = pcaselect.computeSelect(S_hier, nb_c)


