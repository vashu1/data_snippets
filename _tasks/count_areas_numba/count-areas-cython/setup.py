import os
from setuptools import setup,Extension
from Cython.Build import cythonize

# https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html

import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(packages=['images'],
    scripts=['count-areas'],
    ext_modules = cythonize(Extension(
           "images.components_v3_cython",                                # the extension name
           sources=["images/components_v3_cython.pyx"], # can take glob *.pyx
           language="c++",                        # generate and compile C++ code
      )))

'''
docker run -v `pwd`:/count-areas -it count-areas /bin/bash
CPPFLAGS=-I/usr/local/lib/python3.7/site-packages/numpy/core/include python3 setup.py build_ext --inplace

./test

python3 performance.py
'''