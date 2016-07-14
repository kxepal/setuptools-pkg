# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#

from distutils.errors import DistutilsOptionError

from .utils import SimpleProject


class TestRequirementsMapping(SimpleProject):

    def test_mapping_missing(self):
        self.cmd.requirements_mapping = None
        with self.assertRaises(DistutilsOptionError):
            self.cmd.finalize_options()

    def test_bad_key(self):
        self.cmd.requirements_mapping = {
            ('abc', 'cde'): {
                'name': 'py-test',
                'origin': 'devel/py-test',
                'version': '1.2.3'
            },
        }
        with self.assertRaises(DistutilsOptionError):
            self.cmd.finalize_options()

    def test_value_not_a_dict(self):
        self.cmd.requirements_mapping = {
            'test==1.2.3': [],
        }
        with self.assertRaises(DistutilsOptionError):
            self.cmd.finalize_options()

    def test_bad_key_in_value(self):
        self.cmd.requirements_mapping = {
            'test==1.2.3': {
                'name': 'py-test',
                'origin': 'devel/py-test',
                'version': '1.2.3',
                'test': '42'
            },
        }
        with self.assertRaises(DistutilsOptionError):
            self.cmd.finalize_options()

    def test_bad_value(self):
        self.cmd.requirements_mapping = {
            'test==1.2.3': {
                'name': 'py-test',
                'origin': None,
                'version': '1.2.3',
            },
        }
        with self.assertRaises(DistutilsOptionError):
            self.cmd.finalize_options()

    def test_no_origin(self):
        self.cmd.requirements_mapping = {
            'test==1.2.3': {
                'name': 'py-test',
                'version': '1.2.3',
            },
        }
        with self.assertRaises(DistutilsOptionError):
            self.cmd.finalize_options()

    def test_no_version(self):
        self.cmd.requirements_mapping = {
            'test==1.2.3': {
                'name': 'py-test',
                'origin': 'devel/py-test',
            },
        }
        with self.assertRaises(DistutilsOptionError):
            self.cmd.finalize_options()

    def test_no_name(self):
        self.cmd.requirements_mapping = {
            'test==1.2.3': {
                'origin': 'devel/py-test',
                'version': '1.2.3',
            },
        }
        with self.assertRaises(DistutilsOptionError):
            self.cmd.finalize_options()

    def test_unknown_python_dep(self):
        self.cmd.requirements_mapping = {
            'foo==1.2.3': {
                'origin': 'devel/py-test',
                'version': '1.2.3',
            },
        }
        with self.assertRaises(DistutilsOptionError):
            self.cmd.finalize_options()
