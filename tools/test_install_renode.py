#!/usr/bin/env python3
"""Unit tests for Renode installer script contracts."""

import unittest
from pathlib import Path
import tools.install_renode as installer


class TestInstallRenode(unittest.TestCase):
    def test_installer_file_exists(self):
        root = Path(__file__).resolve().parents[1]
        self.assertTrue((root / "tools" / "install_renode.py").exists())
        self.assertTrue((root / "install_renode.ps1").exists())
        self.assertTrue((root / "install_renode.sh").exists())

    def test_os_installer_functions_exist(self):
        self.assertTrue(callable(installer.install_windows))
        self.assertTrue(callable(installer.install_linux))
        self.assertTrue(callable(installer.install_macos))
        self.assertTrue(callable(installer.is_renode_installed))


if __name__ == "__main__":
    unittest.main()
