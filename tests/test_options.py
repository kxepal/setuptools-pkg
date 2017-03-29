# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#

import os
import sys
from distutils.errors import DistutilsOptionError
from distutils.util import get_platform

from setuptools_pkg import bdist_pkg

from .utils import EmptyProject, SimpleProject, mock


class TestCommandOptions(EmptyProject):

    def test_bdist_base(self):
        self.assertIsNone(self.cmd.bdist_base)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.bdist_base,
                         os.path.join('build', 'bdist.' + get_platform()))

    def test_dist_dir(self):
        self.assertIsNone(self.cmd.dist_dir)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.dist_dir, 'dist')

    def test_format(self):
        self.cmd.warn = mock.Mock()
        for format in {'txz', 'tbz', 'tgz', 'tar'}:
            self.cmd.format = format
            self.cmd.finalize_options()
            self.assertFalse(self.cmd.warn.called)
            self.assertEqual(self.cmd.format, format)

    def test_unknown_format(self):
        self.cmd.warn = mock.Mock()
        self.cmd.format = 'zip'
        self.cmd.finalize_options()
        self.assertTrue(self.cmd.warn.called)
        self.assertEqual(self.cmd.format, 'tgz')


class TestEmptyProjectOptions(EmptyProject):

    def test_abi_on_freebsd(self):
        self.assertIsNone(self.cmd.abi)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.abi, 'freebsd:10:amd64')

    def test_abi_for_pure_dist_on_linux(self):
        self.system_fn.return_value = 'linux'
        self.dist.is_pure = mock.Mock(return_value=True)
        self.assertIsNone(self.cmd.abi)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.abi, '*')

    def test_abi_on_else(self):
        self.system_fn.return_value = 'linux'
        with self.assertRaises(DistutilsOptionError):
            self.cmd.get_abi()

    def test_arch_on_freebsd(self):
        self.assertIsNone(self.cmd.arch)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.arch, 'freebsd:10:x86:64')

    def test_arch_for_pure_dist_on_linux(self):
        self.system_fn.return_value = 'linux'
        self.dist.is_pure = mock.Mock(return_value=True)
        self.assertIsNone(self.cmd.arch)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.arch, '*')

    def test_arch_on_else(self):
        self.system_fn.return_value = 'linux'
        with self.assertRaises(DistutilsOptionError):
            self.cmd.get_arch()

    def test_categories(self):
        self.assertIsNone(self.cmd.categories)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.categories, [])

    def test_comment(self):
        self.assertIsNone(self.cmd.comment)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.comment, 'UNKNOWN')

    def test_deps(self):
        self.assertIsNone(self.cmd.deps)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.deps, {})

    def test_desc(self):
        self.assertIsNone(self.cmd.desc)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.desc, 'UNKNOWN')

    def test_groups(self):
        self.assertIsNone(self.cmd.groups)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.groups, None)

    def test_groups_set(self):
        self.cmd.groups = ['test']
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.groups, ['test'])

    def test_groups_set_str(self):
        self.cmd.groups = 'test,passed'
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.groups, ['test', 'passed'])

    def test_groups_bad(self):
        self.cmd.groups = 42
        with self.assertRaises(DistutilsOptionError):
            self.cmd.finalize_options()

    def test_license(self):
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.license, None)

    def test_maintainer(self):
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.maintainer, 'UNKNOWN <UNKNOWN>')

    def test_name(self):
        self.assertIsNone(self.cmd.name)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.name, 'UNKNOWN')

    def test_origin(self):
        pyver = ''.join(map(str, sys.version_info[:2]))
        self.assertIsNone(self.cmd.origin)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.origin,
                         'devel/py{}-{}'.format(pyver, self.cmd.name))

    def test_prefix(self):
        self.cmd.prefix = '/tmp'
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.prefix, '/tmp')

    def test_prefix_not_set(self):
        self.assertIsNone(self.cmd.prefix)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.prefix, '/usr/local')

    def test_prefix_strip_trailing_slash(self):
        self.cmd.prefix = '/tmp/foo/bar/'
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.prefix, '/tmp/foo/bar')

    def test_provides(self):
        self.assertIsNone(self.cmd.provides)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.provides, None)

    def test_provides_set(self):
        self.cmd.provides = ['test']
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.provides, ['test'])

    def test_provides_set_str(self):
        self.cmd.provides = 'test,passed'
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.provides, ['test', 'passed'])

    def test_provides_bad(self):
        self.cmd.provides = 42
        with self.assertRaises(DistutilsOptionError):
            self.cmd.finalize_options()

    def test_requires(self):
        self.assertIsNone(self.cmd.requires)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.requires, None)

    def test_requires_set(self):
        self.cmd.requires = ['test']
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.requires, ['test'])

    def test_requires_set_str(self):
        self.cmd.requires = 'test,passed'
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.requires, ['test', 'passed'])

    def test_requires_bad(self):
        self.cmd.requires = 42
        with self.assertRaises(DistutilsOptionError):
            self.cmd.finalize_options()

    def test_users(self):
        self.assertIsNone(self.cmd.users)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.users, None)

    def test_users_set(self):
        self.cmd.users = ['test']
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.users, ['test'])

    def test_users_set_str(self):
        self.cmd.users = 'test,passed'
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.users, ['test', 'passed'])

    def test_users_bad(self):
        self.cmd.users = 42
        with self.assertRaises(DistutilsOptionError):
            self.cmd.finalize_options()

    def test_version(self):
        self.assertIsNone(self.cmd.version)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.version, '0.0.0')

    def test_www(self):
        self.assertIsNone(self.cmd.www)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.www, 'UNKNOWN')

    def test_manifest_requires_project_name(self):
        self.dist.metadata.name = None
        self.cmd.finalize_options()
        with self.assertRaises(DistutilsOptionError):
            self.cmd.generate_manifest_content()

    def test_manifest_requires_project_version(self):
        self.dist.metadata.name = 'test'
        self.cmd.finalize_options()
        self.cmd.version = None
        with self.assertRaises(DistutilsOptionError):
            self.cmd.generate_manifest_content()


class TestSimpleProjectOptions(SimpleProject):

    def test_categories(self):
        self.assertIsNone(self.cmd.categories)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.categories, ['foo', 'bar', 'baz'])

    def test_comment(self):
        self.assertIsNone(self.cmd.comment)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.comment, 'long story short')

    def test_deps(self):
        self.assertIsNone(self.cmd.deps)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.deps,
                         {'py-test': {
                             'origin': 'devel/py-test',
                             'version': '1.2.3'
                         }})

    def test_deps_custom_stacks_together(self):
        self.cmd.deps = {
            'py-something': {
                'origin': 'devel/py-something',
                'version': '42',
            },
        }
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.deps,
                         {'py-test': {'origin': 'devel/py-test',
                                      'version': '1.2.3'},
                          'py-something': {'origin': 'devel/py-something',
                                           'version': '42'},
                          })

    def test_desc(self):
        self.assertIsNone(self.cmd.desc)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.desc, 'long story long')

    def test_license(self):
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.license, 'BSD')

    def test_maintainer_as_author(self):
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.maintainer,
                         'John Doe <john.doe@example.com>')

    def test_maintainer_as_maintainer(self):
        self.dist.metadata.maintainer = 'Jane Doe'
        self.dist.metadata.maintainer_email = 'jane.doe@example.com'
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.maintainer,
                         'Jane Doe <jane.doe@example.com>')

    def test_name(self):
        self.assertIsNone(self.cmd.name)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.name, 'simple')

    def test_options(self):
        self.assertIsNone(self.cmd.options)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.options,
                         {'foo': False, 'bar': False, 'zoo': False})

    def test_selected_options(self):
        self.assertIsNone(self.cmd.selected_options)
        self.cmd.selected_options = {'foo', 'zoo'}
        self.cmd.requirements_mapping.update({
            'foo==1.0': {
                'name': 'foo',
                'version': '1.0',
                'origin': 'devel/foo',
            },
            'zoo<=3.0': {
                'name': 'zoo',
                'version': '2.5',
                'origin': 'devel/zoo',
            },
        })
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.options,
                         {'foo': True, 'bar': False, 'zoo': True})

    def test_select_options_without_requirements(self):
        self.cmd.selected_options = {'foo', 'zoo'}
        with self.assertRaises(DistutilsOptionError):
            self.cmd.finalize_options()

    def test_select_unknown_options(self):
        self.cmd.selected_options = {'ololo'}
        with self.assertRaises(DistutilsOptionError):
            self.cmd.finalize_options()

    def test_version(self):
        self.assertIsNone(self.cmd.version)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.version, '1.2.3')

    def test_www(self):
        self.assertIsNone(self.cmd.www)
        self.cmd.finalize_options()
        self.assertEqual(self.cmd.www, 'https://example.com')
