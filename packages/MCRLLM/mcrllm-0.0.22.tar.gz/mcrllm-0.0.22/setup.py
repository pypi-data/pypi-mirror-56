import setuptools


setuptools.setup(
    name="mcrllm",
    version="0.0.22",
    author="Ryan Gosselin",
    author_email="ryan.gosselin@usherbrooke.ca",
    packages=["mcrllm"],
    description="MCRLLM: Multivariate Curve Resolution by Log-Likelihood Maximization",
    long_description="MCRLLM: Multivariate Curve Resolution by Log-Likelihood Maximization.\
    \n\n#Method first presented in:\
    \nLavoie F.B., Braidy N. and Gosselin R. (2016) Including Noise Characteristics in MCR to improve Mapping and Component Extraction from Spectral Images, Chemometrics and Intelligent Laboratory Systems, 153, 40-50.\
    \n\n#Input variable\
    \nX(nxk): 2D spectral matrix : n spectra acquired over k energy levels\
    \nNote: 3D spectral image can be unfold to 2D matrix prior to analysis.\
    \n\n#Input and output arguments\
    \nMCRLLM requires 3 inputs : X dat, number of components to compute (nb) and use of phi exponent.\
    \n Refer to paper above for use of phi. To use it: 'phi', if not: 'standard'\
    \ndecomposition = mcr.mcrllm(X,nb,'phi')\
    \ndecomposition.iterate(20)\
    \n# Results\
    \nallS = decomposition.allS\
    \nS_final = decomposition.S\
    \nallC = decomposition.allC\
    \nC_final = decomposition.C\
    \nSini = decomposition.Sini\
    \nallphi = decomposition.allphi",
    long_description_content_type="text/markdown",
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)