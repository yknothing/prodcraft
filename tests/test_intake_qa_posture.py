from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class IntakeQaPostureTests(unittest.TestCase):
    def test_intake_manifest_entry_is_critical_routed_and_tested(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        entries = {entry["name"]: entry for entry in manifest["skills"]}

        intake = entries["intake"]

        self.assertEqual("00-discovery", intake["phase"])
        self.assertEqual("tested", intake["status"])
        self.assertEqual("critical", intake["qa_tier"])
        self.assertEqual("routed", intake["evaluation_mode"])

        qa = intake["qa"]
        self.assertIn("benchmark_results_path", qa)
        self.assertIn("integration_test_path", qa)
        self.assertIn("findings_path", qa)

        self.assertTrue((REPO_ROOT / qa["benchmark_results_path"]).exists())
        self.assertTrue((REPO_ROOT / qa["integration_test_path"]).exists())
        self.assertTrue((REPO_ROOT / qa["findings_path"]).exists())

    def test_intake_findings_record_routed_posture_and_discoverability_blocker(self):
        findings = (
            REPO_ROOT / "eval" / "00-discovery" / "intake" / "current-evidence-status.md"
        ).read_text(encoding="utf-8")

        self.assertIn("`intake` is now `tested` under a `routed` QA posture", findings)
        self.assertIn("mandatory gateway enforced by Prodcraft workflow contracts", findings)
        self.assertIn("Anthropic trigger-discoverability remains useful diagnostic evidence", findings)


if __name__ == "__main__":
    unittest.main()
