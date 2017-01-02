# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2017 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#
import os

from setuptools import find_packages, setup
from setuptools.command.sdist import sdist as sdist_orig


ROOT_DIR = os.path.dirname(__file__)
README_PATH = os.path.join(ROOT_DIR, 'README.rst')
VERSION_PATH = os.path.join(ROOT_DIR, 'VERSION')


# Python project version is a well known place where wheels get reinvented
# again and again. This one is not an exception.
if os.path.exists(VERSION_PATH):
    # The VERSION file contains full project version to use.
    with open(VERSION_PATH) as verfile:
        __version__ = verfile.read().strip()
else:
    # For every else cases we use git for the version info.
    __version__ = os.popen('git describe --tags --always').read().strip()
    try:
        base, distance, hash = __version__.split('-')
    except ValueError:
        # We're on release teg.
        pass
    else:
        # Reformat git describe for PEP-440
        __version__ = '{}.{}+{}'.format(base, distance, hash)
if not __version__:
    # However, things can go wrong, so we'll cry for help here.
    raise RuntimeError('cannot detect project version')


class sdist(sdist_orig):

    def run(self):
        with open(VERSION_PATH, 'w') as fobj:
            fobj.write(__version__)
        sdist_orig.run(self)


with open(README_PATH) as fobj:
    long_description = fobj.read()


setup(
    name='setuptools-pkg',
    version=__version__,
    description='Plugin for setuptools to build FreeBSD pkg',
    long_description=long_description,
    license='BSD',

    author='Alexander Shorin',
    author_email='kxepal@gmail.com',
    url='https://github.com/kxepal/setuptools-pkg',

    package_dir={'': 'src'},
    packages=find_packages('src'),

    test_suite='tests',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],

    install_requires=[
        'setuptools>=18.2',
    ],
    tests_require=[
        'mock==2.0.0',
    ],
    entry_points={
        "distutils.commands": [
            "bdist_pkg = setuptools_pkg.bdist_pkg:bdist_pkg",
        ],
    },
    extras_require={
        'develop': [
            'flake8==2.6.2',
            'mock==2.0.0',
            'pylint==1.6.1',
            'pytest-cov==2.2.1',
            'pytest-cov==2.2.1',
            'pytest==2.9.2',
        ],
        'lzma-2.7': [
            'backports.lzma==0.0.6',
        ],
        'wheel': [
            'pip>=8.0.0',
            'wheel>=0.25.0',
        ],
    },
    command_options={
        'bdist_pkg': {
            'requirements_mapping': (__file__, {
                'setuptools>=18.2': {
                    'name': 'py27-setuptools',
                    'origin': 'devel/py-setuptools',
                    'version': '23.1.0'
                },
            })
        }
    },
    cmdclass={
        'sdist': sdist
    },
)
