# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#


from .utils import SimpleProject, mock


class TestRunCommand(SimpleProject):

    def setUp(self):
        super(TestRunCommand, self).setUp()
        self.cmd.finalize_options()

    def test_run(self):
        self.cmd.build_and_install = mock.Mock()
        self.cmd.before_make_pkg_callback = mock.Mock()
        self.cmd.generate_manifest_content = mock.Mock()
        self.cmd.make_pkg = mock.Mock()

        self.cmd.run()

        self.assertTrue(self.cmd.build_and_install.called)
        self.cmd.before_make_pkg_callback.assert_called_with(
            self.cmd.install_dir
        )
        self.assertTrue(self.cmd.generate_manifest_content.called)
        self.assertTrue(self.cmd.make_pkg.called)

    def test_build_and_install(self):
        self.cmd.run_command = mock.Mock()
        self.cmd.build_and_install()
        self.cmd.run_command.assert_has_calls([mock.call('build'),
                                               mock.call('install')])
