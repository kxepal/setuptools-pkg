# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#

from setuptools import Command

__all__ = (
    'bdist_pkg',
)


class bdist_pkg(Command):
    description = 'create FreeBSD pkg distribution'

    user_options = [
        ('bdist-base=', 'b',
         'base directory for creating built distributions'),
        ('dist-dir=', 'd',
         'directory to put distribute files in'),
    ]

    def initialize_options(self):
        self.bdist_base = None
        self.dist_dir = None

    def finalize_options(self):
        self.set_undefined_options('bdist', ('bdist_base', 'bdist_base'))
        self.set_undefined_options('bdist', ('dist_dir', 'dist_dir'))

    def run(self):
        pass
