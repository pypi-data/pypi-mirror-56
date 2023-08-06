# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 11:10:43 2019

@auteur : Louis-Philippe Baillargeon
"""

import numpy as np

#%%deal with weird pixels
def findWeirdPixels(X, nb_etype = 6):
    
    medians = np.median(X, axis = 0)    # median for each energy level
    stds = np.std(X, axis = 0)          # standart deviation for each energy level
    maxval = medians + stds*nb_etype
    
    weirdmap = np.where(X>maxval, 1,0)
    
    weirdlevint = np.where(weirdmap == 1)
    weirdlev = np.array([weirdlevint[0],weirdlevint[1]]).T

    
    return weirdlev, weirdmap



#estimate weird pixels
def estimateWeirdPixelsList(X, weirdlev, weirdmap, neighbours = 3):
# X : spectra in form [pix,lev]
# weirlev : list of weird levels in form [#pix,#lev]
# neighbours : number of pixels used on each side to estimate the value of the weird level
    
    
    
    nb_level = len(X[0,:]) 

    for i in range(len(weirdlev[:,0])):
        
        
            pix = weirdlev[i,0]
            lev = weirdlev[i,1]
            
            xestime = 0                    # initialisation du xestimé
            k = 1                          # compteur
            nb_neighbours = 0              # total valid neigbours
            
            
            while(k < np.amin([nb_level-lev, neighbours+1])):              # onfait la moyenne des 3 niveaux suivants sauf si on est au bout 
                
                if(weirdmap[pix, lev+k] == 0):                            # ou qu'ils sont fautifs
                           
                    xestime = xestime + X[pix, lev+k]
                    
                    nb_neighbours = nb_neighbours+1
                k = k+1
    
        
    
             
            k = 1                          # compteur
            while k < np.amin([lev,neighbours+1]):                        # et des 3 niveaux précedents sauf si on est au début
               
                xestime = xestime + X[pix, lev-k]
                nb_neighbours = nb_neighbours+1
                k = k+1
            

            if nb_neighbours > 0:
                X[pix,lev] = xestime/nb_neighbours
                
            else:
                print('warning, estimation might be less precised due to too corrupted data')
                X[pix,lev] = estimateWeirdPixel(X, pix, lev, weirdmap, nb_neighbours, nb_neighbours*5)


    return X



def estimateWeirdPixel(X, pix, lev, weirdmap, prev_neighbours, next_neighbours):
    
    xestime = 0                    # initialisation du xestimé
    k = prev_neighbours+1          # compteur
    nb_neighbours = 0              # total valid neigbours
    nb_level = len(X[0,:]) 
    nb_pix = len(X[:,0])
    
    
    while(k < np.amin([nb_level-lev, next_neighbours+1])):              # on fait la moyenne des 3*5 niveaux suivants sauf si on est au bout 
        
        if(weirdmap[pix, lev+k] == 0):                                  # ou qu'ils sont fautifs
                   
            xestime = xestime + X[pix, lev+k]
            
            nb_neighbours = nb_neighbours+1
        k = k+1



     
    k = prev_neighbours+1                          # compteur
    while k < np.amin([lev,next_neighbours+1]):                        # et des 3 niveaux précedents sauf si on est au début
       
        xestime = xestime + X[pix, lev-k]
        nb_neighbours = nb_neighbours+1
        k = k+1
        
        
        
    if nb_neighbours > 0:
        x = xestime/nb_neighbours
        
    else:
        
        x = 1/nb_pix
        print('warning : one pixel is really corrupted, some levels could not be guessed and have been flatened')
        
    return x
  
    
    




                 