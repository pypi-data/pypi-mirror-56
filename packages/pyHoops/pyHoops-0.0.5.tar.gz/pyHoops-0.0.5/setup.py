#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 11:26:33 2019

@author: alessandro
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyHoops", # Replace with your own username
    #packages=["pyHoops"],
    version= "0.0.5",
    license="MIT",
    author="Alessandro Bombelli",
    author_email="alessandro.bombelli.87@gmail.com",
    description="A python package to web-parse basketball play-by-play boxscores and compute data analytics",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    url="https://github.com/alessandroBombelli/pyHoops",
    download_url = "https://github.com/alessandroBombelli/pyHoops/archive/0.0.5.tar.gz",
    #packages=setuptools.find_packages(),
    install_requires =["numpy","beautifulsoup4"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)