# MCRLLM

import numpy as np
import matplotlib.pyplot as plt
from mcrllm import mcrllm

plt.close('all')

#X = np.loadtxt('data_2.txt', delimiter=',')
X = np.loadtxt('data_EELS.txt', delimiter=',')

#X = np.loadtxt('data_EDX.txt', delimiter=',')
X = X.T


#%% MCR

# standard
# phi
# heuristic
# sd
decomposition = mcrllm(X,7,'phi')
decomposition.iterate(20)

# Get results
allS = decomposition.allS
S_final = decomposition.S
allC = decomposition.allC
C_final = decomposition.C
Sini = decomposition.Sini
allphi = decomposition.allphi

#np.savetxt('data_S.txt',S_final)
#np.savetxt('data_C.txt',C_final)

#%% Plot results

plt.figure()
plt.plot(S_final.T)
plt.title('S',fontsize=16)

plt.figure()
plt.plot(C_final)
plt.title('C',fontsize=16)

print('That\'s all folks!')