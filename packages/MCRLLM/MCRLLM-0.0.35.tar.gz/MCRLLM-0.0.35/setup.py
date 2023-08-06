import setuptools


setuptools.setup(
    name="MCRLLM",
    version="0.0.35",
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
    \nAlgorithm is designed to treat 2D data X(nxk) matrices where n spectra acquired over k energy levels.\
    \n3D spectral image X(n1,n2,k) can be unfolded to 2D matrix X(n1xn2,k) prior to MCRLLM analysis. Composition maps can then be obtained by folding C(n1xn2,a) matrices into 2D chemical maps C(n1,n2,a).\
    \n# Input and output arguments\
    \nMCRLLM requires 3 inputs : X dat, number of components to compute (nb) and use of phi exponent.\
    \n Refer to paper above for use of phi. To optimize phi: 'phi' or to set phi to 1: 'standard'\
    \ndecomposition = mcr.mcrllm(X,nb,'phi')\
    \n# Results\
    \nShow S and C for each iteration (all) or only for final results (final).\
    \nS_all = decomposition.allS\
    \nS_final = decomposition.S\
    \nC_all = decomposition.allC\
    \nC_final = decomposition.C\
    \n# Example\
    \nCompute MCRLLM using 7 components and optimizing phi exponent.\
    \nimport MCRLLM as mcr\
    \ndecomposition = mcr.mcrllm(X,7,'phi')\
    \n#Iterate each component 20 times\
    \ndecomposition.iterate(20)\
    \nS_final = decomposition.S\
    \nC_final = decomposition.C\
    \nplt.figure()\
    \nplt.plot(S_final.T)\
    \nplt.title('S',fontsize=16)\
    \nplt.figure()\
    \nplt.plot(C_final)\
    \nplt.title('C',fontsize=16)",
    long_description_content_type="text/markdown",
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)