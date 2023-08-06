# -*- coding: utf-8 -*-
"""
@auteurs :  Hugo Caussan et Louis-Philippe Baillargeon
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import savemat
import dm4
import scipy.io as sc
import scipy.stats as st

#import pypng as png

"""Ce script contient des fonctions utiles pour travailler avec des spectres images""" 



# Sert à ouvrir les plots à l'exterieur de la console
try:
    import IPython
    shell = IPython.get_ipython()
    shell.enable_matplotlib(gui='qt')
except:
    pass

# Permet d'ouvrir un fichier dm3 / Mat / spd
def loadFile(filepath):

    if filepath[-4:]==".dm4":
        dm4data = dm4.DM4File.open(filepath)
        tags = dm4data.read_directory()
        image_data_tag = tags.named_subdirs['ImageList'].unnamed_subdirs[1].named_subdirs['ImageData']
        image_tag = image_data_tag.named_tags['Data']
        dim1 = dm4data.read_tag_data(image_data_tag.named_subdirs['Dimensions'].unnamed_tags[0])
        dim2 = dm4data.read_tag_data(image_data_tag.named_subdirs['Dimensions'].unnamed_tags[1])
        nb_level = dm4data.read_tag_data(image_data_tag.named_subdirs['Dimensions'].unnamed_tags[2])
        x = np.array(dm4data.read_tag_data(image_tag), dtype=np.uint16)
        x = np.reshape(x, (dim1,dim2,nb_level), order = 'F')    #shape the matrix like the data is stored
    
    elif filepath[-4:]==".mat":#Load a Mat file 
        Xdict = sc.loadmat(filepath)
        x = Xdict['image_round']
        
    elif filepath[-4:]==".txt":#Load a txt file 
        x = np.loadtxt(filepath, comments="#", delimiter=",", unpack=False).T
    
    elif filepath[-4:]==".spd": # SPD FILE (EDAX)
        h = open(filepath,'rb')
        header = {}
        header['tag'] = np.fromfile(h,'int8',16)
        header['version'] = np.fromfile(h,'int32',1)[0]
        header['nSpectra'] = np.fromfile(h,'int32',1)[0]
        header['nCols'] = np.fromfile(h,'int32',1)[0]
        header['nRows'] = np.fromfile(h,'int32',1)[0]
        header['nChannels'] = np.fromfile(h,'int32',1)[0]
        header['countBytes'] = np.fromfile(h,'int32',1)[0]
        header['dataOffset'] = np.fromfile(h,'int32',1)[0]
        header['nFrames'] = np.fromfile(h,'int32',1)[0]
        header['fName'] = np.fromfile(h,'int8',120)
        header['filler'] = np.fromfile(h,'int8',900)
        x = np.zeros([header['nSpectra'],header['nChannels']],'int16')
        for i in range(0,header['nSpectra']):
            x[i,:] = np.fromfile(h,'int16',header['nChannels'])
        h.close()
        x = np.float64(x)
        x = np.reshape(x,[header['nRows'],header['nCols'],header['nChannels']])
        
    elif filepath[-4:]==".npy": # SPD FILE (EDAX)
        x = np.load(filepath)
        
    else:
        print("Type de fichier "+filepath[-4:]+" non prix en charge")

    return x



# Pour normaliser un jeu de données
def normalize(x):
    
    x_sum = np.array([np.sum(x, axis=1)]).T
    x_norm = x / x_sum
    
    if np.any(x_norm != x_norm):
        
        eq = 1/len(x[0,:])
        x_norm = np.where(x_norm != x_norm, eq, x_norm)
        
    
        
    return x_norm



# Verify if a distribution is indeed poisson
def poissonVerify(X):
# X must be a np.array set of pixels of same specie of form [pix,lev]
    Xvar = np.var(X, axis = 0)
    Xmean = np.mean(X, axis = 0)
    slope, intercept, r_value, p_value, std_err = st.linregress(Xvar,Xmean)
    
    plt.figure()
    plt.xlabel('Variance', fontsize = 25)
    plt.ylabel('Mean', fontsize = 25)
    plt.plot(Xvar, Xmean)
    plt.plot()
    ax = plt.axes()
    x = np.linspace(0, np.max(Xvar), 1000)
    ax.plot(x, intercept + slope*x);
    
    print('slope : ' + str(slope))
    print('r : ' + str(r_value))
    
    return slope, r_value, intercept


    

# Permet de bin une image spectrale
def dataBin(x, n = 2):
    dim = len(x.shape)
    if dim == 2:
        s0 = x.shape[0]
        s0 = s0 - s0%n
        
        xb = np.zeros((int(s0/n), x.shape[1]))
        for i in range(n):
            f = range(i,s0,n)
            xb = xb + x[f,:]
        
    elif dim == 3:
        s0 = x.shape[0]
        s1 = x.shape[1]
        
        s0 = s0 - s0%n
        s1 = s1 - s1%n
        
        x = x[:s0,:s1,:]
        xb = np.zeros((int(s0/n),int(s1/n),x.shape[2]))
        
        for i in range(n):
            f1 = range(i,s0,n)
            for j in range(n):
                f2 = range(j,s1,n)
                xb = xb + x[f1,:,:][:,f2,:]
        
    return xb/(n**(dim-1))


# Generate everything but the data on a plot
def plotSpectraSetup(title, xlabel, ylabel):     
    plt.figure()           
    plt.title(title, fontsize = 25)
    plt.xlabel(xlabel, fontsize = 25)
    plt.ylabel(ylabel, fontsize = 25)
    plt.tick_params(axis='both',length=12,which='both',labelsize='large')
    plt.grid(True)

     
# Plot the spectra for all phases
def plotSpectra(S, Emin = 0, Emax = 20, title = 'Phase spectra', xlabel = 'eV', ylabel = 'Abundance (/1)'):
    x = np.linspace(Emin,Emax, S.shape[1])            
    for i in range (S.shape[0]):
            plotSpectraSetup(str(title)+ ' ' + str(i), str(xlabel), str(ylabel))
            plt.plot(x, S[i])
            
# Plot the spectra of a few phases on the same plot to facilitate comparison, group is a np array that contains the indices of the phases that are meant to be ploted together
def plotSpectraGroup(S, group, Emin = 0, Emax = 20):
    x = np.linspace(Emin,Emax, S.shape[1])       
    plotSpectraSetup("Multiple phase Spectra", "eV", "Abundance (%)")
    
    for i in range(len(group)):
        plt.plot(x, 100*S[group[i],:])
        

            
# Plot les cartes de concentration de toutes les phases only works with 3D
def Cmap(cf):

    for i in range(0, len(cf[0,0,:])):
        plt.figure()
        plt.title('Concentration de la phase '+str(i))
        plt.imshow(np.log(cf[:,:,i]))
        plt.show()

# Plot Cmaps and spectras on one page
# If log is set to true, log concentrations will be shown instead of concentrations. Usefull if contrast is small, but can create false impression of high differences.
def plotCompare(S, Emin, Emax, C, pas = 1, log = False, title  = 'Phase '):
    x = np.linspace(Emin,Emax, S.shape[1])  
    
    for i in range (S.shape[0]):

        plt.figure()
        
        #spectra
        plt.subplot(1,2,1)
        plt.xlabel('loss (eV)', fontsize = 25)
        plt.ylabel('abundance', fontsize = 25)
        plt.tick_params(axis='both',length=12,which='both',labelsize='large') 
        plt.plot(x, S[i,:], '-', lw=2)
        plt.title(title + str(i) + ' Spectra', fontsize = 25)
        plt.grid(True)
        
        
        #conc
        plt.subplot(1,2,2)
        plt.tick_params(axis='both',length=12,which='both',labelsize='large')
        
        if log:
            plt.imshow(np.log(C[:,:,i]), origin = 'lower')
            
        else:
            plt.imshow(C[:,:,i], origin = 'lower')
            
        plt.xlabel('pixels', fontsize = 25)
        plt.ylabel('pixels', fontsize = 25)
        plt.title(title + str(i) + ' concentration map', fontsize = 25)
        plt.grid(True)
        
        plt.show
        



# plot le spectre total (tous les niveaux d'énergie additionnés)          
def spectraMap(X3D):   #X3D sous forme[YDim,XDim,Elevel]
    X2D = np.sum(X3D, axis = 2)
    plt.figure()
    plt.title('Tout le spectre reçu')
    plt.imshow(np.log(X2D.T), origin = 'lower')
    plt.show()
    
    
def importMJdata(path):
#Fonction spécifique au données simulées EDX 10 pyramides, elles sont enregistrées sousla forme X3[nb_level, xdim, ydim]
    X3= loadFile(path)
    X3 = X3.T
    return X3

    
        


                
                
                
                
                
                

    