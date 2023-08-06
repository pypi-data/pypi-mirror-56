import setuptools


setuptools.setup(
    name="MCRLLM",
    version="0.0.42",
    author="Ryan Gosselin",
    author_email="ryan.gosselin@usherbrooke.ca",
    packages=["MCRLLM"],
    description="MCRLLM: Multivariate Curve Resolution by Log-Likelihood Maximization",
    long_description="MCRLLM: Multivariate Curve Resolution by Log-Likelihood Maximization.\
    \n\nX = CS\
    \nwhere\
    \nX(nxk): Spectroscopic data where n spectra acquired over k energy levels\
    \nC(nxa): Composition map based on a MCRLLM components\
    \nS(axk): Spectra of the a components as computed by MCRLLM\
    \n\n# Method first presented in\
    \nLavoie F.B., Braidy N. and Gosselin R. (2016) Including Noise Characteristics in MCR to improve Mapping and Component Extraction from Spectral Images, Chemometrics and Intelligent Laboratory Systems, 153, 40-50.\
    \n\n# Input data\
    \nAlgorithm is designed to treat 2D data X(nxk) where n spectra acquired over k energy levels.\
    \nA 3D spectral image X(n1,n2,k) can be unfolded to a 2D matrix X(n1xn2,k) prior to MCRLLM analysis. Composition maps can then be obtained by folding C(n1xn2,a) into 2D chemical maps C(n1,n2,a).\
    \n# Input and output arguments\
    \nMCRLLM requires 2 inputs : X data and number of MCRLLM components to compute (nb).\
    \ndecomposition = mcr.mcrllm(X,nb)\
    \n# Results\
    \nShow S and C for each iteration (all) or only for final results (final).\
    \nS_all = decomposition.allS\
    \nS_final = decomposition.S\
    \nC_all = decomposition.allC\
    \nC_final = decomposition.C\
    \n# Example\
    \n#Compute MCRLLM on X using 7 components.\
    \nimport MCRLLM as mcr\
    \nimport matplotlib.pyplot as plt\
    \ndecomposition = mcr.mcrllm(X,7)\
    \n#Iterate each component 10 times\
    \ndecomposition.iterate(10)\
    \nS_final = decomposition.S\
    \nC_final = decomposition.C\
    \nplt.figure();plt.plot(S_final.T)\
    \nplt.figure();plt.plot(C_final)\
    \n# Compatibility\
    \nMCRLLM tested on Python 3.7 using the following modules:\
    \nNumpy 1.17.2\
    \nScipy 1.3.1\
    \nSklearn 0.21.3\
    \nPysptools 0.15.0\
    \nTqdm 4.36.1",
    long_description_content_type="text/markdown",
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)