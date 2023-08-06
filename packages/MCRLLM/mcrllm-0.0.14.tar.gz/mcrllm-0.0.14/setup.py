import setuptools


setuptools.setup(
    name="mcrllm",
    version="0.0.14",
    author="Ryan Gosselin",
    author_email="ryan.gosselin@usherbrooke.ca",
    packages=["mcrllm"],
    description="MCRLLM: Multivariate Curve Resolution by Log-Likelihood Maximization",
    long_description="MCRLLM: Multivariate Curve Resolution by Log-Likelihood Maximization. \
Lavoie F.B., Braidy N. and Gosselin R. (2016) Including Noise Characteristics in MCR to improve Mapping and Component Extraction from Spectral Images, Chemometrics and Intelligent Laboratory Systems, 153, 40-50.",
    long_description_content_type="text/markdown",
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)