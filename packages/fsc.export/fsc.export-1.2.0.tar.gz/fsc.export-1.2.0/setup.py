#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    30.03.2016 00:29:06 CEST
# File:    setup.py

from os.path import abspath, join, dirname
import sys

from setuptools import setup

pkgname = 'export'
pkgname_qualified = 'fsc.' + pkgname

with open(join(dirname(abspath(__file__)), 'doc/description.txt')) as f:
    description = f.read().strip()
with open(join(dirname(abspath(__file__)), 'README.md')) as f:
    long_description = f.read()

with open(join(dirname(abspath(__file__)), 'version.txt')) as f:
    version = f.read().strip()

setup(
    packages=[pkgname_qualified],
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    name=pkgname_qualified,
    version=version,
    url=(
        'http://frescolinogroup.github.io/frescolino/pyexport/' + '.'.join(version.split('.')[:2])
    ),
    include_package_data=True,
    author='C. Frescolino',
    author_email='frescolino@lists.phys.ethz.ch',
    python_requires=">=3.6",
    install_requires=[],
    extras_require={
        'test': ['pytest'],
        'doc': ['sphinx', 'sphinx_rtd_theme'],
        'precommit': ['pre-commit==1.20.0'],
    },
    classifiers=[ # yapf: disable
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities'
    ],
    license='Apache',
)
