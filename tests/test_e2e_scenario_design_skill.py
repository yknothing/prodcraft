from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class E2EScenarioDesignSkillTests(unittest.TestCase):
    def setUp(self):
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))

    def test_skill_files_exist(self):
        skill_path = REPO_ROOT / "skills" / "05-quality" / "e2e-scenario-design" / "SKILL.md"
        findings_path = REPO_ROOT / "eval" / "05-quality" / "e2e-scenario-design" / "findings.md"
        eval_strategy_path = REPO_ROOT / "eval" / "05-quality" / "e2e-scenario-design" / "evals" / "eval-strategy.md"

        self.assertTrue(skill_path.exists(), skill_path)
        self.assertTrue(findings_path.exists(), findings_path)
        self.assertTrue(eval_strategy_path.exists(), eval_strategy_path)

    def test_manifest_registers_skill_as_tested_routed(self):
        entries = {entry["name"]: entry for entry in self.manifest["skills"]}
        entry = entries["e2e-scenario-design"]

        self.assertEqual("05-quality", entry["phase"])
        self.assertEqual("tested", entry["status"])
        self.assertEqual("standard", entry["qa_tier"])
        self.assertEqual("routed", entry["evaluation_mode"])
        self.assertIn("benchmark_results_path", entry["qa"])
        self.assertIn("integration_test_path", entry["qa"])

    def test_artifact_flow_covers_inputs_and_outputs(self):
        artifact_flow = {entry["artifact"]: entry for entry in self.manifest["artifact_flow"]}

        self.assertIn("e2e-scenario-design", artifact_flow["source-code"]["consumed_by"])
        self.assertIn("e2e-scenario-design", artifact_flow["task-list"]["consumed_by"])
        self.assertIn("e2e-scenario-design", artifact_flow["test-strategy-doc"]["consumed_by"])
        self.assertIn("e2e-scenario-design", artifact_flow["test-suite"]["produced_by"])
        self.assertIn("e2e-scenario-design", artifact_flow["test-report"]["produced_by"])

    def test_tested_packet_files_exist(self):
        targets = [
            REPO_ROOT / "eval" / "05-quality" / "e2e-scenario-design" / "isolated-benchmark-review.md",
            REPO_ROOT / "eval" / "05-quality" / "e2e-scenario-design" / "testing-strategy-handoff-review.md",
            REPO_ROOT / "eval" / "05-quality" / "e2e-scenario-design" / "consumer-review.md",
        ]

        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_findings_record_tested_status(self):
        findings = (
            REPO_ROOT / "eval" / "05-quality" / "e2e-scenario-design" / "findings.md"
        ).read_text(encoding="utf-8")
        benchmark_review = (
            REPO_ROOT / "eval" / "05-quality" / "e2e-scenario-design" / "isolated-benchmark-review.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Current status: `tested`", findings)
        self.assertIn("Recommended status: `tested`", benchmark_review)


if __name__ == "__main__":
    unittest.main()
