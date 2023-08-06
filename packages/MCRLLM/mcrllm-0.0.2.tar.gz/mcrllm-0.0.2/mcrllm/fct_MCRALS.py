# MCR ALS

"""
Coded by Jeffrey Byrns
Adapted by Ryan Gosselin
"""

# import packages
import numpy as np
from scipy import linalg
from SI_File_Toolbox import normalize

class HyperspectralSegmentation_MCR_ALS:
    
    @classmethod
    def mcr_als(cls,xraw, nb_c, init, nb_iter=50):  #I added xraw to facilitates call from GUI
        
        x = normalize(xraw)

        max_iter = nb_iter
        x_n = np.sum(x, 1)
        x_n[x_n < 0.025*np.max(x_n)] = np.max(x_n)
        x = x.T / x_n
        x = x.T
        x.astype('float64')

        '''
        
        
        Updates: 
        1 - The issue was that it the spectral images contained many pixels with low or no signal (except random 
        noise), therefore when normalizing, the amplitude of those pixels would overcome the amplitude of the pixels 
        that had a true signal. So to keep the shape of the data, the normalization is now done in relation with the 
        maximum area under the curve. That way, the area of the most intense pixel will be 1 and the other ones will 
        simply be less than 1.
        
        2- I cannot only use the maximum of the sum because normalizing does allow to amplify features of low signal
        pixels. So line 48 serve as a filter to apply standard normalisation on pixel having sum > 0.05*max(sum(x,1) and 
        divide by max(sum(x,1)) for the pixels that are just random noise.
        
        3- Turns out, the reason the matrix became singular, was because one of the spectra was all negative (and was 
        then contrained to 0). The result was that the sum of that spectrum was 0 and thus making the matrix singular. 
        Adding a break allows to stop the iteration before it happens.
        '''

        s = init

        cnt = 0
        flag = True

        while flag:
            s_mem = s

            # Concentrations by linear regression between X and S
            c1 = s @ s.T
            c2 = linalg.inv(c1)
            c3 = x @ s.T
            c = c3 @ c2

            c[c < 0] = 0
            c_sum = np.sum(c, 1) # Modification to C - Closure
            c_sum[c_sum == 0] = 1  # This line prevent any division by 0
            c = c.T / c_sum
            c = c.T


            # Spectra by linear regression between X and C
            s1 = c.T @ c
            s2 = linalg.inv(s1)
            s3 = c.T @ x
            s = s2 @ s3
            s[s < 0] = 0
            c_mem = c
            cnt = cnt + 1

            if cnt == max_iter or np.min(np.sum(s, 1)) == 0:
                if np.min(np.sum(s, 1)) == 0:
                    s = s_mem
                    c = c_mem
                flag = False


        c = c.astype('float32')
        s = s.astype('float32')

        return c, s