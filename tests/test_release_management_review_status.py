from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class ReleaseManagementReviewStatusTests(unittest.TestCase):
    def setUp(self):
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))

    def test_manifest_registers_release_management_as_tested_routed(self):
        entries = {entry["name"]: entry for entry in self.manifest["skills"]}
        entry = entries["release-management"]

        self.assertEqual("06-delivery", entry["phase"])
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
            REPO_ROOT / "eval" / "06-delivery" / "release-management" / "findings.md",
            REPO_ROOT / "eval" / "06-delivery" / "release-management" / "evals" / "eval-strategy.md",
            REPO_ROOT / "eval" / "06-delivery" / "release-management" / "isolated-benchmark-plan.md",
            REPO_ROOT / "eval" / "06-delivery" / "release-management" / "isolated-benchmark-review.md",
            REPO_ROOT / "eval" / "06-delivery" / "release-management" / "delivery-completion-handoff-review.md",
            REPO_ROOT / "eval" / "06-delivery" / "release-management" / "fixtures" / "access-review-modernization-delivery-decision-record.md",
            REPO_ROOT / "eval" / "06-delivery" / "release-management" / "fixtures" / "access-review-modernization-test-report.md",
            REPO_ROOT / "eval" / "06-delivery" / "release-management" / "fixtures" / "access-review-modernization-security-report.md",
        ]

        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_delivery_artifact_flow_and_phase_docs_reference_release_management(self):
        artifact_flow = {entry["artifact"]: entry for entry in self.manifest["artifact_flow"]}
        phase_text = (REPO_ROOT / "skills" / "06-delivery" / "_phase.md").read_text(encoding="utf-8")
        gateway = (REPO_ROOT / "skills" / "_gateway.md").read_text(encoding="utf-8")

        self.assertIn("release-management", artifact_flow["delivery-decision-record"]["consumed_by"])
        self.assertIn("release-management", artifact_flow["ci-cd-pipeline"]["consumed_by"])
        self.assertEqual("release-management", artifact_flow["release-plan"]["produced_by"])
        self.assertIn("release-management", phase_text)
        self.assertIn("release-management", gateway)

    def test_findings_record_tested_status(self):
        findings = (
            REPO_ROOT / "eval" / "06-delivery" / "release-management" / "findings.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Current status: `tested`", findings)
        self.assertIn("isolated benchmark", findings)


if __name__ == "__main__":
    unittest.main()
