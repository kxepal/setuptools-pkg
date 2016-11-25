# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#

import unittest

from setuptools import Distribution

from setuptools_pkg.bdist_pkg import bdist_pkg

try:
    import unittest.mock as mock
except ImportError:  # pragma: no cover
    import mock


class TestProject(unittest.TestCase):

    def new_distribution(self):
        raise NotImplementedError

    def new_bdist_pkg_cmd(self, dist):
        raise NotImplementedError

    def setUp(self):
        self.machine = mock.patch('platform.machine')
        self.machine.start().return_value = 'amd64'
        self.release = mock.patch('platform.release')
        self.release.start().return_value = '10.1-STABLE-r273058'
        self.system = mock.patch('platform.system')
        self.system_fn = self.system.start()
        self.system_fn.return_value = 'freebsd'
        self.dist = self.new_distribution()
        self.cmd = self.new_bdist_pkg_cmd(self.dist)

    def tearDown(self):
        self.machine.stop()
        self.release.stop()
        self.system.stop()


class EmptyProject(TestProject):

    def new_distribution(self):
        return Distribution({})

    def new_bdist_pkg_cmd(self, dist):
        return bdist_pkg(dist)


class SimpleProject(TestProject):
    def new_distribution(self):
        return Distribution({
            'author': 'John Doe',
            'author_email': 'john.doe@example.com',
            'description': 'long story short',
            'install_requires': ['test==1.2.3'],
            'keywords': ['foo', 'bar', 'baz'],
            'license': 'BSD',
            'long_description': 'long story long',
            'name': 'simple',
            'url': 'https://example.com',
            'version': '1.2.3',
            'extras_require': {
                'foo': ['foo==1.0'],
                'bar': ['bar==2.0'],
                'zoo': ['zoo<=3.0'],
            }
        })

    def new_bdist_pkg_cmd(self, dist):
        cmd = bdist_pkg(dist)
        cmd.requirements_mapping = {
            'test==1.2.3': {
                'name': 'py-test',
                'origin': 'devel/py-test',
                'version': '1.2.3',
            },
        }
        cmd.provides = ['features']
        cmd.requires = ['database']
        return cmd
