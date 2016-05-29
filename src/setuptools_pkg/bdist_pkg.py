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
    description = "create FreeBSD pkg distribution"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        pass
