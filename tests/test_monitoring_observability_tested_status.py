from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class MonitoringObservabilityTestedStatusTests(unittest.TestCase):
    def setUp(self):
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        self.entries = {entry["name"]: entry for entry in self.manifest["skills"]}

    def test_manifest_registers_monitoring_observability_as_tested(self):
        entry = self.entries["monitoring-observability"]

        self.assertEqual("07-operations", entry["phase"])
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

    def test_tested_packet_files_exist(self):
        targets = [
            REPO_ROOT / "eval" / "07-operations" / "monitoring-observability" / "evals" / "eval-strategy.md",
            REPO_ROOT / "eval" / "07-operations" / "monitoring-observability" / "findings.md",
            REPO_ROOT
            / "eval"
            / "07-operations"
            / "monitoring-observability"
            / "isolated-benchmark-plan.md",
            REPO_ROOT
            / "eval"
            / "07-operations"
            / "monitoring-observability"
            / "manual-benchmark-review.md",
            REPO_ROOT
            / "eval"
            / "07-operations"
            / "monitoring-observability"
            / "observability-review.md",
        ]

        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_findings_record_narrow_tested_posture(self):
        findings = (
            REPO_ROOT / "eval" / "07-operations" / "monitoring-observability" / "findings.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Current status: `tested`", findings)
        self.assertIn("manual branch-pair benchmark", findings)
        self.assertIn("No true isolated runner-backed benchmark yet", findings)


if __name__ == "__main__":
    unittest.main()
