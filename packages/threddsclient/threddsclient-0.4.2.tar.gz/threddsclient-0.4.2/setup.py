#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup
import re

version = re.search(r'__version__ = [\'"](.+)[\'"]\n?', open('threddsclient/__init__.py').read()).group(1)
long_description = (
    open('README.rst').read() + '\n' + open('AUTHORS.rst').read() + '\n' + open('CHANGES.rst').read()
)

reqs = [line.strip() for line in open('requirements.txt')]

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering :: Atmospheric Science',
]

setup(
    name='threddsclient',
    version=version,
    description='Thredds catalog client',
    long_description=long_description,
    classifiers=classifiers,
    author='Birdhouse',
    email='',
    license='Apache 2.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=reqs,
)
