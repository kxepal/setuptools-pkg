# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#

import os
from distutils.errors import DistutilsOptionError

from .utils import EmptyProject, SimpleProject


class TestEmptyProjectManifest(EmptyProject):

    def test_manifest(self):
        self.cmd.finalize_options()
        with self.assertRaises(DistutilsOptionError):
            self.cmd.generate_manifest_content()


class TestSimpleProjectManifest(SimpleProject):

    def test_manifest(self):
        self.cmd.finalize_options()
        manifest = self.cmd.generate_manifest_content()

        metadata_map = {
            'name': 'name',
            'version': 'version',
            'long_description': 'desc',
            'description': 'comment',
            'keywords': 'categories',
            'url': 'www',
        }
        for attr, key in metadata_map.items():
            self.assertEqual(manifest[key], getattr(self.dist.metadata, attr),
                             (key, attr))

        cmd_map = {
            'abi': 'abi',
            'arch': 'arch',
            'maintainer': 'maintainer',
            'options': 'options',
            'origin': 'origin',
            'prefix': 'prefix',
            'provides': 'provides',
            'requires': 'requires',
        }
        for attr, key in cmd_map.items():
            self.assertEqual(manifest[key], getattr(self.cmd, attr),
                             (key, attr))

        self.assertEqual(manifest['licenselogic'], 'single')
        self.assertEqual(manifest['licenses'], [self.dist.metadata.license])

    def test_dirs_and_files(self):
        self.cmd.finalize_options()
        self.cmd.install_dir = os.path.join(os.path.dirname(__file__),
                                            'simple_project_layout')
        manifest = self.cmd.generate_manifest_content()

        for key, value in manifest['directories'].items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, dict)

            self.assertEqual(value['gname'], 'wheel')
            self.assertEqual(value['perm'], '0755')
            self.assertEqual(value['uname'], 'root')

        for key, value in manifest['files'].items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, dict)

            self.assertEqual(value['gname'], 'wheel')
            self.assertEqual(value['perm'], '0644')
            self.assertEqual(value['uname'], 'root')
            self.assertIn('sum', value)

    def test_require_project_name(self):
        self.cmd.finalize_options()
        self.cmd.name = None
        with self.assertRaises(DistutilsOptionError):
            self.cmd.generate_manifest_content()

    def test_require_project_version(self):
        self.cmd.finalize_options()
        self.cmd.version = None
        with self.assertRaises(DistutilsOptionError):
            self.cmd.generate_manifest_content()

    def test_require_project_description(self):
        self.cmd.finalize_options()
        self.cmd.comment = None
        with self.assertRaises(DistutilsOptionError):
            self.cmd.generate_manifest_content()

    def test_require_project_long_description(self):
        self.cmd.finalize_options()
        self.cmd.desc = None
        with self.assertRaises(DistutilsOptionError):
            self.cmd.generate_manifest_content()

    def test_require_project_maintainer(self):
        self.cmd.finalize_options()
        self.cmd.maintainer = None
        with self.assertRaises(DistutilsOptionError):
            self.cmd.generate_manifest_content()
