#!/usr/bin/env python3
"""Source-contract tests for Renode emulation integration.
"""

from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RENODE_DIR = ROOT / "emulation"
RESC_FILE = RENODE_DIR / "easyiot_esp32.resc"
REPL_FILE = RENODE_DIR / "platforms" / "easyiot_esp32.repl"
ROBOT_FILE = RENODE_DIR / "tests" / "easyiot_boot.robot"
RUNNER_SCRIPT = ROOT / "tools" / "run_renode.py"
CI_FILE = ROOT / ".github" / "workflows" / "ci.yml"


class TestRenodeIntegration(unittest.TestCase):
    def test_renode_script_exists_and_configured(self) -> None:
        self.assertTrue(RESC_FILE.exists(), "easyiot_esp32.resc must exist")
        content = RESC_FILE.read_text(encoding="utf-8")
        self.assertIn("mach create", content)
        self.assertIn("easyiot_esp32.repl", content)
        self.assertIn("sysbus LoadELF", content)

    def test_renode_platform_description_exists(self) -> None:
        self.assertTrue(REPL_FILE.exists(), "easyiot_esp32.repl must exist")
        content = REPL_FILE.read_text(encoding="utf-8")
        self.assertIn("CPU.Xtensa", content)
        self.assertIn("valve_ring_", content)

    def test_renode_robot_test_exists(self) -> None:
        self.assertTrue(ROBOT_FILE.exists(), "easyiot_boot.robot must exist")
        content = ROBOT_FILE.read_text(encoding="utf-8")
        self.assertIn("Start Emulation", content)

    def test_runner_script_exists(self) -> None:
        self.assertTrue(RUNNER_SCRIPT.exists(), "tools/run_renode.py must exist")

    def test_ci_includes_renode(self) -> None:
        content = CI_FILE.read_text(encoding="utf-8")
        self.assertIn("antmicro/renode-test-action", content)


if __name__ == "__main__":
    unittest.main()
