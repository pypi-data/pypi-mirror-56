# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 15:28:17 2018

@author: cauh2701
"""

import numpy as np
from sklearn.decomposition import NMF
from SI_File_Toolbox import normalize


class HyperspectralSegmentation_NMF:
    def nmf(xraw, nb_c, init, nb_iter = 25):
        
        x = normalize(xraw)
        model = NMF(n_components=nb_c, max_iter=nb_iter, init='random', random_state=0)
        s = model.fit_transform(x.T)
        
        x_sum = np.asarray([np.sum(x, axis=1)]).T
        x_norm = x / x_sum
        
        s = s.T
        c = x_norm @ s.T @ np.linalg.inv(s @ s.T)
        return c, s