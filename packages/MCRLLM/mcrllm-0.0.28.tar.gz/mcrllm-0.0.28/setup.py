import setuptools


setuptools.setup(
    name="mcrllm",
    version="0.0.28",
    author="Ryan Gosselin",
    author_email="ryan.gosselin@usherbrooke.ca",
    packages=["mcrllm"],
    description="MCRLLM: Multivariate Curve Resolution by Log-Likelihood Maximization",
    long_description="MCRLLM: Multivariate Curve Resolution by Log-Likelihood Maximization.\
    \n\n# Method first presented in:\
    \nLavoie F.B., Braidy N. and Gosselin R. (2016) Including Noise Characteristics in MCR to improve Mapping and Component Extraction from Spectral Images, Chemometrics and Intelligent Laboratory Systems, 153, 40-50.\
    \n\n# Input variables\
    \nX(nxk): 2D spectral matrix : n spectra acquired over k energy levels\
    \nNote: 3D spectral image can be unfold to 2D matrix prior to analysis.\
    \n# Input and output arguments\
    \nMCRLLM requires 3 inputs : X dat, number of components to compute (nb) and use of phi exponent.\
    \n Refer to paper above for use of phi. To optimize phi: 'phi' or to set phi to 1: 'standard'\
    \ndecomposition = mcr.mcrllm(X,nb,'phi')\
    \n# Results\
    \nShow S and C for each iteration (all) for only final results (final).\
    \nallS = decomposition.allS\
    \nS_final = decomposition.S\
    \nallC = decomposition.allC\
    \nC_final = decomposition.C\
    \n# Example:\
    \nCompute MCRLLM using 7 components and optimizing phi exponent.\
    \nimport mcrllm as mcr\
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