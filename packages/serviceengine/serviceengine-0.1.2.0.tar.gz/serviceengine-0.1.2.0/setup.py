#!/usr/bin/python3
from setuptools import setuptools, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='serviceengine',
     version='0.1.2.0',
     author="Yuval Feldman",
     author_email="feldmanyuval@gmail.com",
     description="A Quickbuild Python Service Engine package",
     long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YuvalFeldman/PyServEn",
    packages=find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
 )
