#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    30.03.2016 00:29:06 CEST
# File:    setup.py

import sys

from setuptools import setup

pkgname = 'export'
pkgname_qualified = 'fsc.' + pkgname

with open('doc/description.txt', 'r') as f:
    description = f.read().strip()
try:
    with open('doc/README', 'r') as f:
        readme = f.read()
except IOError:
    readme = description

with open('version.txt', 'r') as f:
    version = f.read().strip()

setup(
    name=pkgname_qualified,
    version=version,
    packages=[
        pkgname_qualified
    ],
    url='http://frescolinogroup.github.io/frescolino/pyexport/' + '.'.join(version.split('.')[:2]),
    include_package_data=True,
    author='C. Frescolino',
    author_email='frescolino@lists.phys.ethz.ch',
    description=description,
    python_requires=">=2.7",
    install_requires=[],
    extras_require={
        ':python_version < "3"': ['fsc'],
        'test': ['pytest'],
        'doc': ['sphinx', 'sphinx_rtd_theme'],
    },
    long_description=readme,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'
    ],
    license='Apache',
)
