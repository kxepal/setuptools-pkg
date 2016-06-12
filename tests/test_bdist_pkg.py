# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#

import os
import unittest
from distutils.util import get_platform

from setuptools import Distribution

from setuptools_pkg.bdist_pkg import bdist_pkg


class BdistPkgInit(unittest.TestCase):

    def test_bdist_base(self):
        cmd = bdist_pkg(Distribution({}))
        self.assertEqual(cmd.bdist_base, None)
        cmd.finalize_options()
        self.assertEqual(cmd.bdist_base,
                         os.path.join('build', 'bdist.' + get_platform()))

    def test_dist_dir(self):
        cmd = bdist_pkg(Distribution({}))
        self.assertEqual(cmd.dist_dir, None)
        cmd.finalize_options()
        self.assertEqual(cmd.dist_dir, 'dist')
