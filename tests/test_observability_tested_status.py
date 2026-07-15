from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class ObservabilityTestedStatusTests(unittest.TestCase):
    def setUp(self):
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        self.entries = {entry["name"]: entry for entry in self.manifest["skills"]}

    def test_manifest_registers_observability_as_tested(self):
        entry = self.entries["pc-observability"]

        self.assertEqual("cross-cutting", entry["phase"])
        self.assertEqual("tested", entry["status"])
        self.assertEqual("critical", entry["qa_tier"])
        self.assertEqual("routed", entry["evaluation_mode"])

        qa = entry["qa"]
        self.assertIn("structure_validation_path", qa)
        self.assertIn("eval_strategy_path", qa)
        self.assertIn("benchmark_plan_path", qa)
        self.assertIn("benchmark_results_path", qa)
        self.assertIn("findings_path", qa)
        self.assertIn("integration_test_path", qa)
        self.assertIn("manual_review_path", qa)

    def test_tested_artifacts_exist(self):
        targets = [
            REPO_ROOT / "eval" / "cross-cutting" / "pc-observability" / "findings.md",
            REPO_ROOT / "eval" / "cross-cutting" / "pc-observability" / "evals" / "eval-strategy.md",
            REPO_ROOT
            / "eval"
            / "cross-cutting"
            / "pc-observability"
            / "isolated-benchmark-plan.md",
            REPO_ROOT
            / "eval"
            / "cross-cutting"
            / "pc-observability"
            / "isolated-benchmark-review.md",
            REPO_ROOT
            / "eval"
            / "cross-cutting"
            / "pc-observability"
            / "runtime-contract-review.md",
        ]

        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_findings_and_artifact_flow_record_tested_promotion(self):
        findings = (
            REPO_ROOT / "eval" / "cross-cutting" / "pc-observability" / "findings.md"
        ).read_text(encoding="utf-8")
        artifact_flow = {entry["artifact"]: entry for entry in self.manifest["artifact_flow"]}

        self.assertIn("Current status: `tested`", findings)
        self.assertIn("isolated benchmark review", findings)
        self.assertEqual("pc-observability", artifact_flow["observability-spec"]["produced_by"])
        self.assertIn("pc-monitoring-observability", artifact_flow["observability-spec"]["consumed_by"])


if __name__ == "__main__":
    unittest.main()
