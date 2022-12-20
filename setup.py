#!/usr/bin/python3

# https://scikit-build.readthedocs.io/en/latest/usage.html

# pip install . && ./test/test.py
# ./clean.sh && ./setup.py bdist_wheel
# ./clean.sh && ./setup.py sdist
# python3 -m twine upload -r testpypi dist/*
# python3 -m twine upload dist/*

from __future__ import print_function

import os
# from setuptools import setup
from skbuild import setup

def readConfig(fname):
    cfg = {}
    with open(fname) as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().replace("\t", " ").split(" ")
            k = parts.pop(0).strip()
            if '#' != k[0]:
                cfg[k] = " ".join(parts).strip()
    return cfg

# Read in the config
here = os.path.abspath(os.path.dirname(__file__))
cfg = readConfig(os.path.join(here, 'PROJECT.txt'))

# Read in the README
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
if not long_description:
    long_description = cfg['description']

setup(
    name=cfg['name'],
    version=cfg['version'],
    description=cfg['description'],
    url=cfg['url'],
    author=cfg['author'],
    author_email=cfg['email'],
    license=cfg['license'],
    include_package_data = True,
    long_description=long_description,
    long_description_content_type='text/markdown'
    # packages=[],
    # install_requires=[],
    # cmake_args=['-DPYVER==%s' % platform.python_version()],
)
