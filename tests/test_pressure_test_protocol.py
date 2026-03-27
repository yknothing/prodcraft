from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PRESSURE_TEST_ROOT = REPO_ROOT / "eval" / "meta" / "prodcraft-pressure-tests"


class PressureTestProtocolTests(unittest.TestCase):
    def test_protocol_package_has_required_entrypoints(self):
        self.assertTrue((REPO_ROOT / "docs" / "plans" / "2026-03-26-prodcraft-pressure-test-protocol.md").exists())
        self.assertTrue((PRESSURE_TEST_ROOT / "README.md").exists())
        self.assertTrue((PRESSURE_TEST_ROOT / "scenario-matrix.md").exists())
        self.assertTrue((PRESSURE_TEST_ROOT / "templates" / "live-run-record.md").exists())
        self.assertTrue((PRESSURE_TEST_ROOT / "runs").exists())
        self.assertTrue((PRESSURE_TEST_ROOT / "2026-03-26-live-cycle-1-summary.md").exists())
        self.assertTrue((PRESSURE_TEST_ROOT / "2026-03-27-live-cycle-2-summary.md").exists())

    def test_every_scenario_has_a_prompt_pack(self):
        matrix_text = (PRESSURE_TEST_ROOT / "scenario-matrix.md").read_text(encoding="utf-8")
        scenario_ids = set(re.findall(r"`(PT-\d{2}-[a-z0-9-]+)`", matrix_text))

        for scenario_id in sorted(scenario_ids):
            prompt_path = PRESSURE_TEST_ROOT / "prompts" / f"{scenario_id}.md"
            self.assertTrue(prompt_path.exists(), prompt_path)

    def test_live_run_template_matches_optional_workflow_metadata_contract(self):
        template_text = (PRESSURE_TEST_ROOT / "templates" / "live-run-record.md").read_text(encoding="utf-8")

        self.assertIn("workflow_primary", template_text)
        self.assertIn("or omit if the approved fast-track route keeps it implicit", template_text)
        self.assertIn("workflow_overlays", template_text)
        self.assertIn("or omit if no overlay is active", template_text)


if __name__ == "__main__":
    unittest.main()
