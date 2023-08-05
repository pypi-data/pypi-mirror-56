"""
Created on Mon Oct 21 23:54:20 2019

@author: groupe_mickjagger
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hapdcensae",
    version="1.0",
    author="groupe_mickjagger",
    author_email="afanboj1@gmail.com",
    description="A package for times series evolution graphics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gabsens/Python-for-Data-Scientists-ENSAE",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)