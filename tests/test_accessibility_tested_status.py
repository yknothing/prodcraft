from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class AccessibilityTestedStatusTests(unittest.TestCase):
    def setUp(self):
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        self.entries = {entry["name"]: entry for entry in self.manifest["skills"]}

    def test_manifest_registers_accessibility_as_tested_routed(self):
        entry = self.entries["accessibility"]

        self.assertEqual("cross-cutting", entry["phase"])
        self.assertEqual("tested", entry["status"])
        self.assertEqual("standard", entry["qa_tier"])
        self.assertEqual("routed", entry["evaluation_mode"])

        qa = entry["qa"]
        self.assertIn("structure_validation_path", qa)
        self.assertIn("eval_strategy_path", qa)
        self.assertIn("benchmark_plan_path", qa)
        self.assertIn("benchmark_results_path", qa)
        self.assertIn("findings_path", qa)
        self.assertIn("integration_test_path", qa)

    def test_tested_packet_files_exist(self):
        targets = [
            REPO_ROOT / "eval" / "cross-cutting" / "accessibility" / "evals" / "eval-strategy.md",
            REPO_ROOT / "eval" / "cross-cutting" / "accessibility" / "findings.md",
            REPO_ROOT / "eval" / "cross-cutting" / "accessibility" / "isolated-benchmark-plan.md",
            REPO_ROOT / "eval" / "cross-cutting" / "accessibility" / "isolated-benchmark-review.md",
            REPO_ROOT / "eval" / "cross-cutting" / "accessibility" / "isolated-benchmark.json",
            REPO_ROOT
            / "eval"
            / "cross-cutting"
            / "accessibility"
            / "acceptance-criteria-handoff-review.md",
            REPO_ROOT
            / "eval"
            / "cross-cutting"
            / "accessibility"
            / "fixtures"
            / "invite-modal-ui-summary.md",
            REPO_ROOT
            / "eval"
            / "cross-cutting"
            / "accessibility"
            / "fixtures"
            / "invite-modal-product-constraints.md",
        ]

        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_findings_and_artifact_flow_record_tested_promotion(self):
        findings = (
            REPO_ROOT / "eval" / "cross-cutting" / "accessibility" / "findings.md"
        ).read_text(encoding="utf-8")
        artifact_flow = {entry["artifact"]: entry for entry in self.manifest["artifact_flow"]}

        self.assertIn("Current status: `tested`", findings)
        self.assertIn("isolated benchmark", findings)
        self.assertEqual("accessibility", artifact_flow["accessibility-guidance"]["produced_by"])
        self.assertIn("acceptance-criteria", artifact_flow["accessibility-guidance"]["consumed_by"])


if __name__ == "__main__":
    unittest.main()
