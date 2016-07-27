# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#

import bz2
import gzip
import hashlib
import json
import os
import platform
import shutil
import sys
import tarfile
from distutils.errors import DistutilsOptionError
from itertools import chain

from setuptools import Command

try:
    import lzma
except ImportError:  # pragma: no cover
    try:
        import backports.lzma as lzma
    except ImportError:
        lzma = None


__all__ = (
    'bdist_pkg',
)


def before_make_pkg_callback(install_dir):  # pragma: no cover
    pass


class bdist_pkg(Command):
    description = 'create FreeBSD pkg distribution'

    user_options = [
        ('bdist-base=', 'b',
         'base directory for creating built distributions'),
        ('dist-dir=', 'd',
         'directory to put distribute files in'),
        ('format=', 'f',
         'Set format as the package output format.  It can be one'
         ' of txz, tbz, tgz or tar.  If an invalid or no format is specified'
         ' tgz is assumed.'),
        ('keep-temp', None,
         'keep intermediate build directories and files')
    ]
    boolean_options = ('keep-intermediate-files',)

    compressor_for_format = {
        'txz': lzma,
        'tgz': gzip,
        'tbz': bz2,
    }

    def initialize_options(self):
        self.bdist_base = None
        self.before_make_pkg_callback = before_make_pkg_callback
        self.dist_dir = None
        self.format = None
        self.keep_temp = False
        self.requirements_mapping = None
        self.selected_options = None
        self.initialize_manifest_options()

    def initialize_manifest_options(self):
        # TODO: What is it and how to use it?
        # self.annotations = None
        self.abi = None
        self.arch = None
        self.categories = None
        # TODO: Could conflicts be useful for us?
        # self.conflicts = None
        self.comment = None
        # TODO: What is it and how to use it?
        # self.dep_formula = None
        self.deps = None
        self.desc = None
        # These fields are autogenerated:
        # self.directories = None
        # self.dirs = None
        # self.files = None
        # self.flatsize = None
        self.groups = None
        self.license = None
        self.maintainer = None
        # TODO: should that be single message or multiple ones?
        # self.messages = None
        self.name = None
        self.options = None
        self.selected_options = None
        # Since we use extras, which don't have either defaults or descriptions
        # these fields are not supported so far:
        # self.options_defaults = None
        # self.options_descriptions = None
        self.origin = None
        # TODO: What is the path?
        # self.path = None
        self.prefix = None
        self.provides = None
        self.requires = None
        # TODO: Add scripts support.
        # self.scripts = None
        # TODO: Do we need shared libs support?
        # self.shlibs = None
        # self.shlibs_provides = None
        # self.shlibs_requires = None
        # TODO: Support checksum.
        # self.sum = None
        self.users = None
        self.version = None
        # TODO: Can Python packages be vital?
        # self.vital = None
        self.www = None

    def finalize_options(self):
        self.set_undefined_options('bdist', ('bdist_base', 'bdist_base'))
        self.set_undefined_options('bdist', ('dist_dir', 'dist_dir'))
        self.ensure_format('tgz')
        self.bdist_dir = os.path.join(self.bdist_base, 'pkg')
        self.install_dir = os.path.join(self.bdist_dir, 'root')
        self.finalize_manifest_options()

    def finalize_manifest_options(self):
        project = self.distribution
        self.ensure_string('abi', self.get_abi())
        self.ensure_string('arch', self.get_arch())
        self.ensure_categories(project)
        self.ensure_string('comment', project.get_description())
        self.ensure_string('desc', project.get_long_description())
        self.ensure_string_list('groups')
        self.ensure_string('license', self.resolve_license(project))
        self.ensure_string('maintainer', self.get_maintainer(project))
        self.ensure_string('name', project.get_name())
        self.ensure_string('origin', self.get_default_origin(project))
        self.ensure_prefix('/usr/local')
        self.ensure_string_list('provides')
        self.ensure_string_list('requires')
        self.ensure_string('version', project.get_version())
        self.ensure_string_list('users')
        self.ensure_string('www', project.get_url())
        self.ensure_options()
        self.ensure_deps()
        self.ensure_before_make_pkg_callback()

    def run(self):
        self.build_and_install()
        self.before_make_pkg_callback(self.install_dir)
        self.make_pkg(self.generate_manifest_content())
        self.maybe_remove_temp(self.bdist_base)

    def build_and_install(self):
        # Basically, we need the intermediate results of bdist_dumb,
        # but since it's too monolithic and does the stuff that we would like
        # to avoid, here short copy-paste happens /:
        build = self.reinitialize_command('build', reinit_subcommands=1)
        self.run_command('build')
        install = self.reinitialize_command('install', reinit_subcommands=1)
        install.prefix = self.prefix
        install.root = self.install_dir
        install.warn_dir = 0
        self.run_command('install')
        for path in {build.build_lib, build.build_scripts, build.build_temp}:
            self.maybe_remove_temp(path)

    def generate_manifest_content(self):
        manifest = {
            'abi': self.abi,
            'arch': self.arch,
            'categories': self.categories,
            'comment': self.comment,
            'deps': self.deps,
            'desc': self.desc,
            'directories': {},
            'files': {},
            'flatsize': 0,
            'groups': self.groups,
            'licenselogic': 'single',
            'licenses': [self.license] if self.license else [],
            'maintainer': self.maintainer,
            'name': self.name,
            'options': self.options,
            'origin': self.origin,
            'prefix': self.prefix,
            'provides': self.provides,
            'requires': self.requires,
            'users': self.users,
            'version': self.version,
            'www': self.www,
        }

        mdirs = manifest['directories']
        mfiles = manifest['files']
        for real_file_path, install_path in self.iter_install_files():
            with open(real_file_path, 'rb') as fh:
                data = fh.read()
                manifest['flatsize'] += len(data)
                mdirs[os.path.dirname(install_path)] = {
                    'gname': 'wheel',
                    'perm': '0755',
                    'uname': 'root',
                }
                mfiles[install_path] = {
                    'gname': 'wheel',
                    'perm': '0644',
                    'sum': hashlib.sha256(data).hexdigest(),
                    'uname': 'root',
                }

        # TODO: Should we keep UNKNOWN values?
        manifest = {key: value for key, value in manifest.items()
                    if value and value != 'UNKNOWN'}

        if 'name' not in manifest:
            raise DistutilsOptionError('Project must have name defined')

        if 'version' not in manifest:
            raise DistutilsOptionError('Project must have version defined')

        return manifest

    def make_pkg(self, manifest):
        manifest_path = self.make_manifest(manifest)
        compact_manifest_path = self.make_compact_manifest(manifest)
        files_paths = chain([
            (manifest_path, os.path.basename(manifest_path)),
            (compact_manifest_path, os.path.basename(compact_manifest_path))
        ], self.iter_install_files())

        self.mkpath(self.dist_dir)
        tar_path = self.make_tar(files_paths)

        ext = self.format
        if ext != 'tar':
            compressor = self.get_compressor(ext)
            if compressor is None:
                raise RuntimeError('Format {} is not supported'.format(ext))
            self.compress_tar(tar_path, ext, compressor)
            os.remove(tar_path)

    def make_manifest(self, content):
        path = os.path.join(self.bdist_dir, '+MANIFEST')
        with open(path, 'w') as fobj:
            json.dump(content, fobj, sort_keys=True, indent=4)
        return path

    def make_compact_manifest(self, content):
        path = os.path.join(self.bdist_dir, '+COMPACT_MANIFEST')
        compact_content = content.copy()
        compact_content.pop('directories')
        compact_content.pop('files')
        with open(path, 'w') as fobj:
            json.dump(compact_content, fobj, sort_keys=True, indent=4)
        return path

    def make_tar(self, files_paths):
        basename = '{}-{}.tar'.format(self.name, self.version)
        path = os.path.join(self.dist_dir, basename)
        seen = set()
        with tarfile.open(path, 'w') as tar:
            for file_path, tar_path in files_paths:
                tar_dir_path = os.path.dirname(tar_path)
                if tar_dir_path and tar_dir_path not in seen:
                    tarinfo = tar.gettarinfo(os.path.dirname(file_path),
                                             tar_dir_path)
                    tarinfo.name = tar_dir_path
                    tar.addfile(tarinfo)
                    seen.add(tar_dir_path)
                tarinfo = tar.gettarinfo(file_path, tar_path)
                tarinfo.name = tar_path
                with open(file_path, 'rb') as f:
                    tar.addfile(tarinfo, f)
        return path

    def compress_tar(self, tar_path, ext, compressor):
        txx_path = tar_path.rsplit('.tar', 1)[0] + '.' + ext
        with compressor.open(txx_path, 'w') as txx:
            with open(tar_path, 'rb') as tar:
                txx.write(tar.read())
        return txx_path

    def get_compressor(self, format):
        return self.compressor_for_format.get(format)

    def get_abi(self):
        if platform.system().lower() != 'freebsd':
            if not self.distribution.is_pure():
                raise DistutilsOptionError(
                    'Unable to determine default ABI value'
                    ' since bdist_pkg call happens not on FreeBSD system.'
                    ' Please specify this value according the target system'
                    ' for which you build this package.'
                )
            return '*'
        return ':'.join((
            platform.system(),
            # 10.1-STABLE-r273058 -> 10
            platform.release().split('-', 1)[0].split('.')[0],
            # TODO: ensure that platform.machine() gives correct values
            platform.machine()
        ))

    def get_arch(self):
        if platform.system().lower() != 'freebsd':
            if not self.distribution.is_pure():
                raise DistutilsOptionError(
                    'Unable to determine default ARCH value'
                    ' since bdist_pkg call happens not on FreeBSD system.'
                    ' Please specify this value according the target system'
                    ' for which you build this package.'
                )
            return '*'
        return ':'.join((
            platform.system(),
            # 10.1-STABLE-r273058 -> 10
            platform.release().split('-', 1)[0].split('.')[0],
            # TODO: shouldn't there be a better way?
            'x86:64' if platform.machine() == 'amd64' else 'x86:32'
        ))

    def get_default_origin(self, project):
        return 'devel/py{}{}-{}'.format(sys.version_info[0],
                                        sys.version_info[1],
                                        project.get_name())

    def get_maintainer(self, project):
        maintainer = '{} <{}>'.format(project.get_maintainer(),
                                      project.get_maintainer_email())
        if maintainer == 'UNKNOWN <UNKNOWN>':
            # No explicit maintainer specified, use author contact instead
            maintainer = '{} <{}>'.format(project.get_author(),
                                          project.get_author_email())
        return maintainer

    def resolve_license(self, project):
        # Thanks for this mapping goes to pytoport project
        py2freebsd_mapping = {
            'agpl-3.0': 'AGPLv3',
            'apache-2.0': 'APACHE20',
            'artistic-2.0': 'ART20',
            'bsd-2-clause': 'BSD2CLAUSE',
            'bsd-3-clause-clear': 'BSD3CLAUSE',
            'bsd-3-clause': 'BSD3CLAUSE',
            'cc0-1.0': 'CC0-1.0',
            'epl-1.0': 'EPL',
            'gpl-2.0': 'GPLv2',
            'gpl-3.0': 'GPLv3',
            'isc': 'ISCL',
            'lgpl-2.1': 'LGPL21',
            'lgpl-3.0': 'LGPL3',
            'mit': 'MIT',
            'mpl-2.0': 'MPL',
            'ofl-1.1': 'OFL11',
        }
        license = project.get_license()
        pkg_license = py2freebsd_mapping.get(license.lower())
        if license != 'UNKNOWN' and pkg_license is None:
            self.warn('Unable to convert license %s to PKG naming' % license)
            return license
        return pkg_license

    def ensure_format(self, default):
        self.ensure_string('format', default)
        if self.format not in {'txz', 'tbz', 'tgz', 'tar'}:
            self.warn('Unknown format {!r}, falling back to {}'
                      ''.format(self.format, default))
            self.format = default

    def ensure_prefix(self, default=None):
        self.ensure_string('prefix', default)
        self.prefix = self.prefix.rstrip('/')

    def ensure_categories(self, project):
        self.categories = self.categories or project.get_keywords()
        self.ensure_string_list('categories')

    def ensure_deps(self):
        install_requires = set(self.distribution.install_requires or [])
        for option in self.selected_options:
            install_requires |= set(self.distribution.extras_require[option])
        mapping = self.requirements_mapping or {}
        self.deps = self.deps or {}

        seen_deps = set([])
        for python_dep, spec in mapping.items():
            if not isinstance(python_dep, str):
                raise DistutilsOptionError('Invalid Python dependency: {}'
                                           ''.format(python_dep))

            if python_dep not in install_requires:
                raise DistutilsOptionError('{} is not in install requires list'
                                           ''.format(python_dep))

            if not isinstance(spec, dict):
                raise DistutilsOptionError('requirements_mapping items must be'
                                           ' dict, got {}'.format(repr(spec)))
            if set(spec) != {'origin', 'version', 'name'}:
                raise DistutilsOptionError('requirements_mapping items must'
                                           ' have "origin" and "version" keys,'
                                           ' got {}'.format(set(spec)))
            for key in {'origin', 'version', 'name'}:
                if not isinstance(spec[key], str):
                    raise DistutilsOptionError('"{}" value must be string, got'
                                               ' {}'.format(key, spec[key]))

            self.deps[spec['name']] = {'origin': spec['origin'],
                                       'version': spec['version']}
            seen_deps.add(python_dep)

        missing = seen_deps ^ install_requires
        if missing:
            raise DistutilsOptionError('These packages are listed in install'
                                       ' requirements, but not in bdist_pkg'
                                       ' requirements mapping: {}'
                                       ''.format(', '.join(missing)))

    def ensure_options(self):
        provided_options = set(self.distribution.extras_require or {})
        self.selected_options = set(self.selected_options or [])
        unknown_options = self.selected_options - provided_options
        if not unknown_options:
            self.options = {option: option in self.selected_options
                            for option in provided_options}
        else:
            raise DistutilsOptionError('Unknown extras selected: {}'
                                       ''.format(', '.join(unknown_options)))

    def ensure_before_make_pkg_callback(self):
        if hasattr(self.before_make_pkg_callback, '__call__'):
            return
        raise DistutilsOptionError('before_make_pkg_callback must be callable')

    def iter_install_files(self):
        for root, dirs, files in os.walk(self.install_dir):
            for file in files:
                reldir = os.path.relpath(root, self.install_dir)
                install_path = '/' + os.path.join(reldir, file)
                install_path = install_path.replace(self.prefix + '/lib64/',
                                                    self.prefix + '/lib/')
                yield os.path.join(root, file), install_path

    def maybe_remove_temp(self, path):
        if self.keep_temp:
            return
        if path is None:
            return
        if os.path.exists(path):
            shutil.rmtree(path)
