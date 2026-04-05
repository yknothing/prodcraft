from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class DeliveryCompletionSkillTests(unittest.TestCase):
    def setUp(self):
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))

    def test_delivery_completion_skill_files_exist(self):
        targets = [
            REPO_ROOT / "skills" / "06-delivery" / "delivery-completion" / "SKILL.md",
            REPO_ROOT / "skills" / "06-delivery" / "delivery-completion" / "references" / "gotchas.md",
        ]
        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_manifest_and_artifact_flow_register_delivery_completion(self):
        entries = {entry["name"]: entry for entry in self.manifest["skills"]}
        artifact_flow = {entry["artifact"]: entry for entry in self.manifest["artifact_flow"]}

        entry = entries["delivery-completion"]
        self.assertEqual("06-delivery", entry["phase"])
        self.assertEqual("tested", entry["status"])
        self.assertEqual("critical", entry["qa_tier"])
        self.assertEqual("routed", entry["evaluation_mode"])
        self.assertIn("qa", entry)
        self.assertIn("eval_strategy_path", entry["qa"])
        self.assertIn("benchmark_plan_path", entry["qa"])
        self.assertIn("benchmark_results_path", entry["qa"])
        self.assertIn("findings_path", entry["qa"])
        self.assertIn("integration_test_path", entry["qa"])

        self.assertIn("delivery-completion", artifact_flow["verification-record"]["consumed_by"])
        self.assertIn("delivery-completion", artifact_flow["execution-checkpoint"]["consumed_by"])
        self.assertEqual("delivery-completion", artifact_flow["delivery-decision-record"]["produced_by"])
        self.assertIn("release-management", artifact_flow["delivery-decision-record"]["consumed_by"])

    def test_gateway_phase_and_skill_contract_keep_delivery_completion_thin(self):
        skill_text = (
            REPO_ROOT / "skills" / "06-delivery" / "delivery-completion" / "SKILL.md"
        ).read_text(encoding="utf-8")
        phase_text = (REPO_ROOT / "skills" / "06-delivery" / "_phase.md").read_text(encoding="utf-8")
        gateway_text = (REPO_ROOT / "skills" / "_gateway.md").read_text(encoding="utf-8")

        self.assertIn("Present these four outcomes", skill_text)
        self.assertIn("typed `discard` confirmation", skill_text)
        self.assertIn("does **not** replace release management or deployment strategy", skill_text)
        self.assertIn("delivery-completion", phase_text)
        self.assertIn("delivery-completion", gateway_text)
        self.assertIn("finishing-a-development-branch", gateway_text)

    def test_tested_artifacts_exist(self):
        targets = [
            REPO_ROOT / "eval" / "06-delivery" / "delivery-completion" / "findings.md",
            REPO_ROOT / "eval" / "06-delivery" / "delivery-completion" / "evals" / "eval-strategy.md",
            REPO_ROOT / "eval" / "06-delivery" / "delivery-completion" / "isolated-benchmark-plan.md",
            REPO_ROOT / "eval" / "06-delivery" / "delivery-completion" / "isolated-benchmark-review.md",
            REPO_ROOT / "eval" / "06-delivery" / "delivery-completion" / "completion-handoff-review.md",
        ]

        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_findings_record_tested_status(self):
        findings = (
            REPO_ROOT / "eval" / "06-delivery" / "delivery-completion" / "findings.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Current status: `tested`", findings)
        self.assertIn("isolated benchmark", findings)


if __name__ == "__main__":
    unittest.main()
