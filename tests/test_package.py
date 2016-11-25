# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#

import json
import os
import shutil
import tempfile

from .utils import SimpleProject, mock


class TestSimplePackage(SimpleProject):

    def setUp(self):
        super(TestSimplePackage, self).setUp()
        self.cmd.finalize_options()
        self.cmd.install_dir = os.path.join(os.path.dirname(__file__),
                                            'simple_project_layout')

    def test_make_package(self):
        manifest = self.cmd.generate_manifest_content()
        try:
            bdist_dir = tempfile.mkdtemp()
            dist_dir = tempfile.mkdtemp()

            self.cmd.bdist_dir = bdist_dir
            self.cmd.dist_dir = dist_dir
            self.cmd.make_pkg(manifest)

            self.check_manifest_exists(bdist_dir)
            self.check_compact_manifest_exists(bdist_dir)
            self.check_txx_exists(self.cmd.dist_dir, self.cmd.format)
        finally:
            shutil.rmtree(bdist_dir)
            shutil.rmtree(dist_dir)

    def test_make_tar_package(self):
        self.cmd.format = 'tar'
        manifest = self.cmd.generate_manifest_content()
        self.cmd.compress_tar = mock.Mock()
        try:
            bdist_dir = tempfile.mkdtemp()
            dist_dir = tempfile.mkdtemp()

            self.cmd.bdist_dir = bdist_dir
            self.cmd.dist_dir = dist_dir
            self.cmd.make_pkg(manifest)

            self.check_manifest_exists(bdist_dir)
            self.check_compact_manifest_exists(bdist_dir)
            self.check_tar_exists(self.cmd.dist_dir)
        finally:
            shutil.rmtree(bdist_dir)
            shutil.rmtree(dist_dir)
        self.assertFalse(self.cmd.compress_tar.called)

    def test_fail_for_unsupported_format(self):
        self.cmd.format = 'txx'
        manifest = self.cmd.generate_manifest_content()
        try:
            bdist_dir = tempfile.mkdtemp()
            dist_dir = tempfile.mkdtemp()

            self.cmd.bdist_dir = bdist_dir
            self.cmd.dist_dir = dist_dir
            with self.assertRaises(RuntimeError):
                self.cmd.make_pkg(manifest)
            self.check_tar_exists(self.cmd.dist_dir)
        finally:
            shutil.rmtree(bdist_dir)
            shutil.rmtree(dist_dir)

    def check_manifest_exists(self, bdist_dir):
        manifest = os.path.join(bdist_dir, '+MANIFEST')
        self.assertTrue(os.path.exists(manifest))
        self.assertTrue(os.path.isfile(manifest))

    def check_compact_manifest_exists(self, bdist_dir):
        manifest = os.path.join(bdist_dir, '+COMPACT_MANIFEST')
        self.assertTrue(os.path.exists(manifest))
        self.assertTrue(os.path.isfile(manifest))
        with open(manifest) as f:
            content = json.load(f)
        for key in {'dirs', 'directories', 'files', 'scripts'}:
            self.assertNotIn(key, content)

    def check_tar_exists(self, dist_dir):
        self.check_txx_exists(dist_dir, 'tar')

    def check_txx_exists(self, dist_dir, format):
        txxname = '{}-{}.{}'.format(self.cmd.name, self.cmd.version, format)
        txxpath = os.path.join(dist_dir, txxname)
        self.assertTrue(os.path.exists(txxpath))
        self.assertTrue(os.path.isfile(txxpath))
