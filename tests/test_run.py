# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2017 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#

from pip._vendor import pkg_resources

from .utils import SimpleProject, mock


class TestRunCommand(SimpleProject):

    def setUp(self):
        super(TestRunCommand, self).setUp()
        self.cmd.finalize_options()

    def test_run(self):
        self.cmd.build_and_install = mock.Mock()
        self.cmd.generate_manifest_content = mock.Mock()
        self.cmd.make_pkg = mock.Mock()

        self.cmd.run()

        self.assertTrue(self.cmd.build_and_install.called)
        self.assertTrue(self.cmd.generate_manifest_content.called)
        self.assertTrue(self.cmd.make_pkg.called)

    def test_build_and_install(self):
        self.cmd.run_command = mock.Mock()
        self.cmd.build_and_install()
        self.cmd.run_command.assert_has_calls([mock.call('build'),
                                               mock.call('install')])

    @mock.patch('pip.wheel.move_wheel_files')
    def test_build_and_install_wheel(self, pip_move_wheel):
        self.cmd.use_wheel = True
        self.cmd.run_command = mock.Mock()
        self.cmd.build_and_install()
        self.cmd.run_command.assert_has_calls([mock.call('bdist_wheel')])
        pip_move_wheel.assert_has_calls([mock.call(
            name=self.cmd.name,
            prefix=self.cmd.prefix,
            req=pkg_resources.Requirement.parse('{}=={}'.format(
                self.cmd.name,
                self.cmd.version
            )),
            root=self.cmd.install_dir,
            wheeldir=None,
        )])

    @mock.patch('shutil.rmtree')
    def test_maybe_remove_temp(self, rmtree):
        self.cmd.maybe_remove_temp(None)
        self.assertFalse(rmtree.called)
        self.cmd.maybe_remove_temp('/something/that/doesnt/exists')
        self.assertFalse(rmtree.called)
        self.cmd.maybe_remove_temp(__file__)
        self.assertTrue(rmtree.called)

    @mock.patch('shutil.rmtree')
    def test_keep_temps(self, rmtree):
        self.cmd.keep_temp = True
        self.cmd.maybe_remove_temp(__file__)
        self.assertFalse(rmtree.called)
