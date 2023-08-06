#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `git_code_counter` package."""


import unittest
from click.testing import CliRunner

from git_code_counter import git_code_counter
from git_code_counter import cli


class TestGit_code_counter(unittest.TestCase):
    """Tests for `git_code_counter` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'git_code_counter.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
