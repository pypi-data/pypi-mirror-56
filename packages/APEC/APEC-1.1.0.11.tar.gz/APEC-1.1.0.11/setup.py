#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='APEC',
    version='1.1.0.11',
    description='Single cell epigenomic clustering based on accessibility pattern',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Bin Li',
    author_email='libinsnet@gmail.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/QuKunLab/APEC',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
    install_requires=[
        'numpy==1.16.2',
        'scipy==1.0.0',
        'pandas==0.24.2',
        'matplotlib==3.0.3',
        'seaborn==0.9.0',
        'numba==0.43.1',
        'networkx==2.2',
        'python-louvain==0.11',
        'scikit-learn==0.20.0',
        'MulticoreTsne==0.1',
        'umap-learn==0.3.8',
        'rpy2==2.8.5',
        'setuptools'
    ]
)
