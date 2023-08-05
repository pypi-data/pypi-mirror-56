#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 16:39:38 2018

@author: stephan
"""
from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_descriptions = f.read()

setup(name="EPRsim",
      version="0.0.2dev",
      author="Stephan Rein",
      author_email="stephan.rein@physchem.uni-freiburg.de",
      url="https://www.radicals.uni-freiburg.de/de/software",
      packages=["EPRsim"],
      package_data={'EPRsim': []},
      include_package_data=True,
      long_description=long_descriptions,
      long_description_content_type='text/x-rst',
      license="GPLv3",
      keywords=[
        'EPR simulations'
        'Isotropic limit'
        'Fast-motion regime'
        'solid-state simulations'
      ],
      classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
       ],
      install_requires=[
        'cycler>=0.10.0',
        'kiwisolver>=1.0.1',
        'numpy>=1.15.4',
        'numpydoc>=0.9.1',
        'pyparsing>=2.3.0',
        'python-dateutil',
        'scipy>=1.2.0',
        'six>=1.11.0',
        'matplotlib',
        'sphinx-rtd-theme>=0.4.3',
        'llvmlite>=0.26.0',
        'numba>=0.41.0'
      ],
      extras_require={
        'LowLevelVirtualMaschine': 'llvmlite==0.26.0',
        'JIT':'numba==0.41.0',
        'mysterious_feature_x3':'numb==0.41.0',
      },
      python_requires='>=3.5',
    )