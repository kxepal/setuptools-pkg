# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#

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
        }
        for attr, key in cmd_map.items():
            self.assertEqual(manifest[key], getattr(self.cmd, attr),
                             (key, attr))

        self.assertEqual(manifest['licenselogic'], 'single')
        self.assertEqual(manifest['licenses'], [self.dist.metadata.license])
