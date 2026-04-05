from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class CiCdReviewStatusTests(unittest.TestCase):
    def setUp(self):
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))

    def test_manifest_registers_ci_cd_as_tested_routed(self):
        entries = {entry["name"]: entry for entry in self.manifest["skills"]}
        entry = entries["ci-cd"]

        self.assertEqual("06-delivery", entry["phase"])
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

    def test_tested_artifacts_exist(self):
        targets = [
            REPO_ROOT / "eval" / "06-delivery" / "ci-cd" / "findings.md",
            REPO_ROOT / "eval" / "06-delivery" / "ci-cd" / "evals" / "eval-strategy.md",
            REPO_ROOT / "eval" / "06-delivery" / "ci-cd" / "isolated-benchmark-plan.md",
            REPO_ROOT / "eval" / "06-delivery" / "ci-cd" / "isolated-benchmark-review.md",
            REPO_ROOT / "eval" / "06-delivery" / "ci-cd" / "pipeline-review.md",
        ]

        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_artifact_flow_phase_docs_and_findings_reference_ci_cd(self):
        artifact_flow = {entry["artifact"]: entry for entry in self.manifest["artifact_flow"]}
        phase_text = (REPO_ROOT / "skills" / "06-delivery" / "_phase.md").read_text(encoding="utf-8")
        gateway = (REPO_ROOT / "skills" / "_gateway.md").read_text(encoding="utf-8")
        findings = (REPO_ROOT / "eval" / "06-delivery" / "ci-cd" / "findings.md").read_text(
            encoding="utf-8"
        )

        self.assertEqual("ci-cd", artifact_flow["ci-cd-pipeline"]["produced_by"])
        self.assertIn("release-management", artifact_flow["ci-cd-pipeline"]["consumed_by"])
        self.assertIn("ci-cd", phase_text)
        self.assertIn("ci-cd", gateway)
        self.assertIn("Current status: `tested`", findings)
        self.assertIn("isolated benchmark", findings)


if __name__ == "__main__":
    unittest.main()
