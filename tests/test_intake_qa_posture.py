from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class IntakeQaPostureTests(unittest.TestCase):
    def test_intake_manifest_entry_is_critical_routed_and_production(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        entries = {entry["name"]: entry for entry in manifest["skills"]}

        intake = entries["pc-intake"]

        self.assertEqual("00-discovery", intake["phase"])
        self.assertEqual("production", intake["status"])
        self.assertEqual("critical", intake["qa_tier"])
        self.assertEqual("routed", intake["evaluation_mode"])

        qa = intake["qa"]
        self.assertIn("benchmark_results_path", qa)
        self.assertIn("integration_test_path", qa)
        self.assertIn("findings_path", qa)
        self.assertIn("security_review_path", qa)

        self.assertTrue((REPO_ROOT / qa["benchmark_results_path"]).exists())
        self.assertTrue((REPO_ROOT / qa["integration_test_path"]).exists())
        self.assertTrue((REPO_ROOT / qa["findings_path"]).exists())
        self.assertTrue((REPO_ROOT / qa["security_review_path"]).exists())

    def test_intake_findings_record_routed_posture_and_discoverability_blocker(self):
        findings = (
            REPO_ROOT / "eval" / "00-discovery" / "pc-intake" / "current-evidence-status.md"
        ).read_text(encoding="utf-8")

        self.assertIn("`pc-intake` is now `production` under a `routed` QA posture", findings)
        self.assertIn("mandatory gateway enforced by Prodcraft workflow contracts", findings)
        self.assertIn("Anthropic trigger-discoverability remains useful diagnostic evidence", findings)

    def test_intake_requires_runtime_boundary_before_quality_handoff(self):
        source = (REPO_ROOT / "skills" / "00-discovery" / "pc-intake" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        curated = (REPO_ROOT / "skills" / ".curated" / "pc-intake" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        for text in (source, curated):
            self.assertIn("quality_target_context", text)
            self.assertIn("runtime_context", text)
            self.assertIn("exposure_profile", text)
            self.assertIn("agent-internal skill", text)
            self.assertIn("public service", text)
            self.assertIn("must calibrate quality and security handoff", text)


if __name__ == "__main__":
    unittest.main()
