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
from setuptools.command.sdist import sdist as sdist_orig


# Python project version is a well known place where wheels get reinvented
# again and again. This one is not an exception.
if os.path.exists('VERSION'):
    # The VERSION file contains full project version to use.
    with open('VERSION') as verfile:
        __version__ = verfile.read().strip()
else:
    # For every else cases we use git for the version info.
    __version__ = os.popen('git describe --tags --always').read().strip()
if not __version__:
    # However, things can go wrong, so we'll cry for help here.
    raise RuntimeError('cannot detect project version')


class sdist(sdist_orig):

    def run(self):
        with open('VERSION', 'w') as fobj:
            fobj.write(__version__)
        super(sdist, self).run()


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
    command_options={
        'bdist_pkg': {
            'requirements_mapping': (__file__, {
                ('setuptools>=21', 'py-setuptools'): {
                    'origin': 'devel/py-setuptools',
                    'version': '21.0'
                },
            })
        }
    },
    cmdclass={
        'sdist': sdist
    },
)
