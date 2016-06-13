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

try:
    import unittest.mock as mock
except ImportError:
    import mock


class BdistPkgInit(unittest.TestCase):

    def setUp(self):
        self._orig_warn = bdist_pkg.warn
        bdist_pkg.warn = lambda self, msg: None

    def tearDown(self):
        bdist_pkg.warn = self._orig_warn

    def test_bdist_base(self):
        cmd = bdist_pkg(Distribution({}))
        self.assertIsNone(cmd.bdist_base)
        cmd.finalize_options()
        self.assertEqual(cmd.bdist_base,
                         os.path.join('build', 'bdist.' + get_platform()))

    def test_dist_dir(self):
        cmd = bdist_pkg(Distribution({}))
        self.assertIsNone(cmd.dist_dir)
        cmd.finalize_options()
        self.assertEqual(cmd.dist_dir, 'dist')

    @mock.patch('platform.machine')
    @mock.patch('platform.release')
    @mock.patch('platform.system')
    def test_abi_on_freebsd(self, system, release, machine):
        system.return_value = 'freebsd'
        release.return_value = '10.1-STABLE-r273058'
        machine.return_value = 'amd64'

        cmd = bdist_pkg(Distribution({}))
        self.assertIsNone(cmd.abi)
        cmd.finalize_options()
        self.assertEqual(cmd.abi, 'freebsd:10:amd64')

    @mock.patch('platform.system')
    def test_abi_on_else(self, system):
        system.return_value = 'linux'

        cmd = bdist_pkg(Distribution({}))
        self.assertIsNone(cmd.abi)
        cmd.finalize_options()
        self.assertEqual(cmd.abi, '*')

    @mock.patch('platform.machine')
    @mock.patch('platform.release')
    @mock.patch('platform.system')
    def test_arch_on_freebsd(self, system, release, machine):
        system.return_value = 'freebsd'
        release.return_value = '10.1-STABLE-r273058'
        machine.return_value = 'amd64'

        cmd = bdist_pkg(Distribution({}))
        self.assertIsNone(cmd.arch)
        cmd.finalize_options()
        self.assertEqual(cmd.arch, 'freebsd:10:x86:64')

    @mock.patch('platform.system')
    def test_arch_on_else(self, system):
        system.return_value = 'linux'

        cmd = bdist_pkg(Distribution({}))
        self.assertIsNone(cmd.arch)
        cmd.finalize_options()
        self.assertEqual(cmd.arch, '*')

    def test_categories(self):
        cmd = bdist_pkg(Distribution({'keywords': ['foo', 'bar', 'baz']}))
        self.assertIsNone(cmd.categories)
        cmd.finalize_options()
        self.assertEqual(cmd.categories, ['foo', 'bar', 'baz'])

    def test_categories_not_set(self):
        cmd = bdist_pkg(Distribution({}))
        self.assertIsNone(cmd.categories)
        cmd.finalize_options()
        self.assertEqual(cmd.categories, [])

    def test_comment(self):
        cmd = bdist_pkg(Distribution({'description': 'hello, world!'}))
        cmd.finalize_options()
        self.assertEqual(cmd.comment, 'hello, world!')

    def test_comment_not_set(self):
        cmd = bdist_pkg(Distribution({}))
        self.assertIsNone(cmd.comment)
        cmd.finalize_options()
        self.assertEqual(cmd.comment, 'UNKNOWN')

    def test_desc(self):
        cmd = bdist_pkg(Distribution({'long_description': 'hello, world!'}))
        cmd.finalize_options()
        self.assertEqual(cmd.desc, 'hello, world!')

    def test_desc_not_set(self):
        cmd = bdist_pkg(Distribution({}))
        self.assertIsNone(cmd.desc)
        cmd.finalize_options()
        self.assertEqual(cmd.desc, 'UNKNOWN')

    def test_license_known(self):
        cmd = bdist_pkg(Distribution({'license': 'BSD-2-clause'}))
        cmd.finalize_options()
        self.assertEqual(cmd.license, 'BSD2CLAUSE')

    def test_license_unknown(self):
        cmd = bdist_pkg(Distribution({'license': 'EULA'}))
        cmd.finalize_options()
        self.assertEqual(cmd.license, 'EULA')

    def test_license_not_set(self):
        cmd = bdist_pkg(Distribution({}))
        cmd.finalize_options()
        self.assertEqual(cmd.license, None)

    def test_maintainer_is_maintainer(self):
        cmd = bdist_pkg(Distribution({
            'maintainer': 'maintainer',
            'maintainer_email': 'maintainer@work',
            'author': 'author',
            'author_email': 'author@home'
        }))
        cmd.finalize_options()
        self.assertEqual(cmd.maintainer, 'maintainer <maintainer@work>')

    def test_maintainer_is_author(self):
        cmd = bdist_pkg(Distribution({
            'author': 'author',
            'author_email': 'author@home'
        }))
        cmd.finalize_options()
        self.assertEqual(cmd.maintainer, 'author <author@home>')

    def test_maintainer_not_set(self):
        cmd = bdist_pkg(Distribution({}))
        cmd.finalize_options()
        self.assertEqual(cmd.maintainer, 'UNKNOWN <UNKNOWN>')

    def test_name(self):
        cmd = bdist_pkg(Distribution({'name': 'mylittleproject'}))
        cmd.finalize_options()
        self.assertEqual(cmd.name, 'mylittleproject')

    def test_name_not_set(self):
        cmd = bdist_pkg(Distribution({}))
        self.assertIsNone(cmd.name)
        cmd.finalize_options()
        self.assertEqual(cmd.name, 'UNKNOWN')

    def test_origin(self):
        cmd = bdist_pkg(Distribution({}))
        cmd.origin = 'misc/python'
        cmd.finalize_options()
        self.assertEqual(cmd.origin, 'misc/python')

    def test_origin_not_set(self):
        cmd = bdist_pkg(Distribution({}))
        self.assertIsNone(cmd.origin)
        cmd.finalize_options()
        self.assertEqual(cmd.origin, 'lang/python')

    def test_prefix(self):
        cmd = bdist_pkg(Distribution({}))
        cmd.prefix = '/tmp'
        cmd.finalize_options()
        self.assertEqual(cmd.prefix, '/tmp')

    def test_prefix_not_set(self):
        cmd = bdist_pkg(Distribution({}))
        self.assertIsNone(cmd.prefix)
        cmd.finalize_options()
        self.assertEqual(cmd.prefix, '/usr/local')

    def test_prefix_strip_trailing_slash(self):
        cmd = bdist_pkg(Distribution({}))
        cmd.prefix = '/tmp/foo/bar/'
        cmd.finalize_options()
        self.assertEqual(cmd.prefix, '/tmp/foo/bar')

    def test_version(self):
        cmd = bdist_pkg(Distribution({'version': '1.0.1'}))
        cmd.finalize_options()
        self.assertEqual(cmd.version, '1.0.1')

    def test_version_not_set(self):
        cmd = bdist_pkg(Distribution({}))
        self.assertIsNone(cmd.version)
        cmd.finalize_options()
        self.assertEqual(cmd.version, '0.0.0')

    def test_www(self):
        cmd = bdist_pkg(Distribution({'url': 'example.com'}))
        cmd.finalize_options()
        self.assertEqual(cmd.www, 'example.com')

    def test_www_not_set(self):
        cmd = bdist_pkg(Distribution({}))
        self.assertIsNone(cmd.www)
        cmd.finalize_options()
        self.assertEqual(cmd.www, 'UNKNOWN')
