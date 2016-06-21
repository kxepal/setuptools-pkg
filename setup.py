# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#
import os
from setuptools import find_packages, setup


# Python project version is a well known place where wheels get reinvented
# again and again. This one is not an exception.

# We'll use git for picking package version. It can generate pretty nice
# versino numbers based on tags and distance to them.
__version__ = os.popen('git describe --tags --always').read().strip()
if not __version__:
    # However, things can go wrong, so we'll cry for help here.
    raise RuntimeError('cannot detect project version')


setup(
    name='setuptools-pkg',
    version=__version__,
    description='Plugin for setuptools to build FreeBSD pkg',
    license='BSD',

    author='Alexander Shorin',
    author_email='kxepal@gmail.com',
    url='https://github.com/kxepal/setuptools-pkg',

    package_dir={'': 'src'},
    packages=find_packages('src'),

    test_suite='tests',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],

    install_requires=[
        'setuptools>=21',
    ],
    tests_require=[
        'mock==2.0.0; python_version<"3.3"',
    ],
    entry_points={
        "distutils.commands": [
            "bdist_pkg = setuptools_pkg.bdist_pkg:bdist_pkg",
        ],
    },
    extras_require={
        'lzma': [
            'backports.lzma==0.0.6; python_version<"3.3"',
        ],
    },
)
