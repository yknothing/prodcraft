from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class ApiDesignReviewStatusTests(unittest.TestCase):
    def setUp(self):
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))

    def test_manifest_registers_api_design_as_tested_routed(self):
        entries = {entry["name"]: entry for entry in self.manifest["skills"]}
        entry = entries["api-design"]

        self.assertEqual("02-architecture", entry["phase"])
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
            REPO_ROOT / "eval" / "02-architecture" / "api-design" / "findings.md",
            REPO_ROOT / "eval" / "02-architecture" / "api-design" / "evals" / "eval-strategy.md",
            REPO_ROOT / "eval" / "02-architecture" / "api-design" / "isolated-benchmark-plan.md",
            REPO_ROOT / "eval" / "02-architecture" / "api-design" / "manual-benchmark-review.md",
            REPO_ROOT / "eval" / "02-architecture" / "api-design" / "architecture-handoff-review.md",
        ]

        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_findings_and_gateway_record_tested_posture(self):
        findings = (
            REPO_ROOT / "eval" / "02-architecture" / "api-design" / "findings.md"
        ).read_text(encoding="utf-8")
        benchmark_review = (
            REPO_ROOT / "eval" / "02-architecture" / "api-design" / "manual-benchmark-review.md"
        ).read_text(encoding="utf-8")
        architecture_phase = (REPO_ROOT / "skills" / "02-architecture" / "_phase.md").read_text(
            encoding="utf-8"
        )
        gateway = (REPO_ROOT / "skills" / "_gateway.md").read_text(encoding="utf-8")

        self.assertIn("Current status: `tested`", findings)
        self.assertIn("Recommended status: `tested`", benchmark_review)
        self.assertIn("api-design", architecture_phase)
        self.assertIn("api-design", gateway)


if __name__ == "__main__":
    unittest.main()
