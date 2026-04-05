from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class FeatureAndDeploymentStrategyReviewStatusTests(unittest.TestCase):
    def setUp(self):
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))

    def test_manifest_registers_feature_development_and_deployment_strategy_as_critical_tested_routed(self):
        entries = {entry["name"]: entry for entry in self.manifest["skills"]}

        feature = entries["feature-development"]
        deployment = entries["deployment-strategy"]

        self.assertEqual("04-implementation", feature["phase"])
        self.assertEqual("06-delivery", deployment["phase"])
        self.assertEqual("tested", feature["status"])
        self.assertEqual("tested", deployment["status"])
        self.assertEqual("critical", feature["qa_tier"])
        self.assertEqual("critical", deployment["qa_tier"])
        self.assertEqual("routed", feature["evaluation_mode"])
        self.assertEqual("routed", deployment["evaluation_mode"])

        for entry in (feature, deployment):
            qa = entry["qa"]
            self.assertIn("structure_validation_path", qa)
            self.assertIn("eval_strategy_path", qa)
            self.assertIn("benchmark_plan_path", qa)
            self.assertIn("findings_path", qa)
            self.assertIn("integration_test_path", qa)
            self.assertIn("benchmark_results_path", qa)

    def test_tested_artifacts_exist_for_both_skills(self):
        targets = [
            REPO_ROOT / "eval" / "04-implementation" / "feature-development" / "findings.md",
            REPO_ROOT / "eval" / "04-implementation" / "feature-development" / "evals" / "eval-strategy.md",
            REPO_ROOT / "eval" / "04-implementation" / "feature-development" / "isolated-benchmark-plan.md",
            REPO_ROOT / "eval" / "04-implementation" / "feature-development" / "isolated-benchmark-review.md",
            REPO_ROOT / "eval" / "04-implementation" / "feature-development" / "tdd-handoff-review.md",
            REPO_ROOT / "eval" / "06-delivery" / "deployment-strategy" / "findings.md",
            REPO_ROOT / "eval" / "06-delivery" / "deployment-strategy" / "evals" / "eval-strategy.md",
            REPO_ROOT / "eval" / "06-delivery" / "deployment-strategy" / "isolated-benchmark-plan.md",
            REPO_ROOT / "eval" / "06-delivery" / "deployment-strategy" / "isolated-benchmark-review.md",
            REPO_ROOT / "eval" / "06-delivery" / "deployment-strategy" / "pipeline-handoff-review.md",
        ]

        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_gateway_and_phase_docs_keep_both_skills_on_the_spine(self):
        gateway = (REPO_ROOT / "skills" / "_gateway.md").read_text(encoding="utf-8")
        implementation_phase = (REPO_ROOT / "skills" / "04-implementation" / "_phase.md").read_text(encoding="utf-8")
        delivery_phase = (REPO_ROOT / "skills" / "06-delivery" / "_phase.md").read_text(encoding="utf-8")

        self.assertIn("feature-development", gateway)
        self.assertIn("deployment-strategy", gateway)
        self.assertIn("feature-development", implementation_phase)
        self.assertIn("deployment-strategy", delivery_phase)

    def test_findings_record_tested_status(self):
        feature_findings = (
            REPO_ROOT / "eval" / "04-implementation" / "feature-development" / "findings.md"
        ).read_text(encoding="utf-8")
        deployment_findings = (
            REPO_ROOT / "eval" / "06-delivery" / "deployment-strategy" / "findings.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Current status: `tested`", feature_findings)
        self.assertIn("Current status: `tested`", deployment_findings)


if __name__ == "__main__":
    unittest.main()
