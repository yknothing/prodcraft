from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class EstimationTestedStatusTests(unittest.TestCase):
    def setUp(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        self.entries = {entry["name"]: entry for entry in manifest["skills"]}

    def test_manifest_registers_estimation_as_tested_routed(self):
        entry = self.entries["estimation"]

        self.assertEqual("03-planning", entry["phase"])
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

    def test_tested_artifacts_exist(self):
        targets = [
            REPO_ROOT / "eval" / "03-planning" / "estimation" / "findings.md",
            REPO_ROOT / "eval" / "03-planning" / "estimation" / "evals" / "eval-strategy.md",
            REPO_ROOT / "eval" / "03-planning" / "estimation" / "isolated-benchmark-plan.md",
            REPO_ROOT / "eval" / "03-planning" / "estimation" / "isolated-benchmark-review.md",
            REPO_ROOT / "eval" / "03-planning" / "estimation" / "sprint-planning-handoff-review.md",
            REPO_ROOT / "eval" / "03-planning" / "estimation" / "fixtures" / "access-review-modernization-task-list.md",
            REPO_ROOT / "eval" / "03-planning" / "estimation" / "fixtures" / "access-review-modernization-risk-register.md",
        ]

        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_findings_record_tested_status(self):
        findings = (
            REPO_ROOT / "eval" / "03-planning" / "estimation" / "findings.md"
        ).read_text(encoding="utf-8")
        artifact_flow = {
            entry["artifact"]: entry
            for entry in yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))["artifact_flow"]
        }

        self.assertIn("Current status: `tested`", findings)
        self.assertIn("isolated benchmark", findings)
        self.assertEqual("estimation", artifact_flow["estimate-set"]["produced_by"])
        self.assertIn("sprint-planning", artifact_flow["estimate-set"]["consumed_by"])


if __name__ == "__main__":
    unittest.main()
