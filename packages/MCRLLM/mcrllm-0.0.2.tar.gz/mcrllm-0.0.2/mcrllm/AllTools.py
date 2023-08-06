# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 10:10:16 2018
@author: cauh2701
"""
#from fct_MCRLLM import HyperspectralSegmentation_MCR_LLM
#from fct_MCRALS import HyperspectralSegmentation_MCR_ALS

#from init import *
#from tkinter import *
from tkinter.messagebox import showerror
from SI_File_Toolbox import loadFile, dataBin, normalize
import matplotlib.pyplot as plt
import numpy as np
from skimage.transform import resize
import dm4
import scipy.io as sc

def run(initList, fctList, nb_c, nb_iter, filepath, nb_dim, hier):
    for i in range(50):
        print("\n")
    
        
    x = loadFile(filepath)
        
   
    try:
        if nb_dim == 3:
        
            # resize image
            print(x.shape)  
            s0 = x.shape[0]
            s1 = x.shape[1]
            s2 = x.shape[2]
                
            nb_pix = s0*s1
        
            x = np.reshape(x, (nb_pix, s2))
            print('Image has been resized.')
            print(x.shape)
            
        elif nb_dim == 2:
            
            # resize image
            print(x.shape)  
            s0 = x.shape[0]
            s2 = x.shape[1]
            
        
            x = np.reshape(x, (s0, s2))
            print('Image has been resized.')
            print(x.shape)
        else:
            raise ValueError

    except ValueError:
        showerror('Erreur', 'Veuillez choisir un nombre de dimensions valide')
        return



    
    xraw = np.copy(x)
    
    #avoid errors, if a energy level has 0 counts on all pixels, it causes log(0) and the level is meaningless, so we take it out
    deletedLevels = []
    nb_deleted = 0
    
    for lev in range(s2):
        
        if np.sum(xraw[:,lev-nb_deleted]) <= 0:
            
            deletedLevels.append(lev)
            xraw = np.delete(xraw, lev-nb_deleted, axis = 1)
            nb_deleted = nb_deleted + 1
    
    
    # normalize data
    x = normalize(xraw)

    for i in initList:
        if i.trigger:
            su = i.do(x, nb_c)#Appel de l'initialisation
            
            for f in fctList:
                if f.trigger:
                    print("{} - {}".format(f.nom, i.nom))
                    try:                    
                        [c, s] = f.do(xraw, nb_c, su, nb_iter = nb_iter)   #Appel de la fonction
                        C = np.array(c)
                        S = np.array(s)
                        
                        for ii in range(nb_deleted):  #Insert deleted spectra back (the spectra was 0 that's why we took it out)
                            S = np.insert(S,deletedLevels[ii], np.zeros(nb_c), axis = 1)
                    except ValueError:
                        print("Non compatibles...")
                        break
                    plt.figure("Spectre {} + {} / {} comp".format(f.nom, i.nom, nb_c))
                    leg = list()
                    

                    for iz in range(nb_c):
                        leg.append("Elem {}".format(iz+1))
                    
                    for n in range (nb_c):
                        plt.plot(S[n,:], linewidth = 0.7)
                    
                    plt.xlabel('Wavelength')
                    plt.ylabel('Spectra')
                    plt.title("{} - {}".format(f.nom, i.nom), fontsize=12)
                    plt.legend(leg)
                    
                    if not isinstance(c, int): # Si c'est n'est pas un int => C'est un array
                        
                        plt.figure("{} + {} / {} comp".format(f.nom, i.nom, nb_c))
                        
                        
                        if  nb_dim == 3:
                            
                            C = np.reshape(C, (s0, s1, nb_c))
                            for ic in range(nb_c):                        
                                a = 331+ic
                                plt.subplot(a); plt.imshow(C[:,:,ic])
                                plt.title("Elem {}".format(ic+1))
                                plt.colorbar()
                                
                                
                        elif nb_dim==2:
                            C = np.reshape(C, (s0, nb_c))
                            plt.title("Concentrations")
                            plt.xlabel('pixels')
                            plt.ylabel('abondance')
                            
                            for ic in range(nb_c):                        
                                plt.plot(C[:,ic])
                                
                    
                    
    if hier:      
    #Je ne savais pas comment appeler les fonctions d'initialisation et je n'avais pas le temps de l'apprendre, alors,
    #j'ai duck tapé ça un peu. Ça mériterait un clean up. On pourrait l'appeler comme les autres au lieu de la faire ici. Faut juste loader Sselect dans le fond
        su = np.load('Sselect.npy')
            
        for f in fctList:
            if f.trigger:
                print("{} - {}".format(f.nom, i.nom))
                try:                    
                    [c, s] = f.do(xraw, nb_c, su, nb_iter = nb_iter)   #Appel de la fonction
                    C = np.array(c)
                    S = np.array(s)
                    
                    for ii in range(nb_deleted):  #Insert deleted spectra back (the spectra was 0 that's why we took it out)
                        S = np.insert(S,deletedLevels[ii], np.zeros(nb_c), axis = 1)
                except ValueError:
                    print("Non compatibles...")
                    break
                plt.figure("Spectre {} + {} / {} comp".format(f.nom, i.nom, nb_c))
                leg = list()
                

                for iz in range(nb_c):
                    leg.append("Elem {}".format(iz+1))
                
                for n in range (nb_c):
                    plt.plot(S[n,:], linewidth = 0.7)
                
                plt.xlabel('Wavelength')
                plt.ylabel('Spectra')
                plt.title("{} - {}".format(f.nom, i.nom), fontsize=12)
                plt.legend(leg)
                
                if not isinstance(c, int): # Si c'est n'est pas un int => C'est un array
                    
                    plt.figure("{} + {} / {} comp".format(f.nom, i.nom, nb_c))
                    
                    
                    if  nb_dim == 3:
                        
                        C = np.reshape(C, (s0, s1, nb_c))
                        for ic in range(nb_c):                        
                            a = 331+ic
                            plt.subplot(a); plt.imshow(C[:,:,ic])
                            plt.title("Elem {}".format(ic+1))
                            plt.colorbar()
                            
                            
                    elif nb_dim==2:
                        C = np.reshape(C, (s0, nb_c))
                        plt.title("Concentrations")
                        plt.xlabel('pixels')
                        plt.ylabel('abondance')
                        
                        for ic in range(nb_c):                        
                            plt.plot(C[:,ic])
                                
                            
                    

