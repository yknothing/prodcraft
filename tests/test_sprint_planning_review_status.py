from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class SprintPlanningReviewStatusTests(unittest.TestCase):
    def setUp(self):
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))

    def test_manifest_registers_sprint_planning_as_tested_routed(self):
        entries = {entry["name"]: entry for entry in self.manifest["skills"]}
        entry = entries["sprint-planning"]

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
            REPO_ROOT / "eval" / "03-planning" / "sprint-planning" / "findings.md",
            REPO_ROOT / "eval" / "03-planning" / "sprint-planning" / "evals" / "eval-strategy.md",
            REPO_ROOT / "eval" / "03-planning" / "sprint-planning" / "isolated-benchmark-plan.md",
            REPO_ROOT / "eval" / "03-planning" / "sprint-planning" / "isolated-benchmark-review.md",
            REPO_ROOT / "eval" / "03-planning" / "sprint-planning" / "estimation-handoff-review.md",
            REPO_ROOT / "eval" / "03-planning" / "sprint-planning" / "fixtures" / "access-review-modernization-estimate-set.md",
            REPO_ROOT / "eval" / "03-planning" / "sprint-planning" / "fixtures" / "access-review-modernization-risk-register.md",
        ]

        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_gateway_phase_docs_and_artifact_flow_reference_sprint_planning(self):
        artifact_flow = {entry["artifact"]: entry for entry in self.manifest["artifact_flow"]}
        planning_phase = (REPO_ROOT / "skills" / "03-planning" / "_phase.md").read_text(encoding="utf-8")
        gateway = (REPO_ROOT / "skills" / "_gateway.md").read_text(encoding="utf-8")

        self.assertEqual("sprint-planning", artifact_flow["sprint-plan"]["produced_by"])
        self.assertIn("sprint-planning", artifact_flow["estimate-set"]["consumed_by"])
        self.assertIn("sprint-planning", artifact_flow["risk-register"]["consumed_by"])
        self.assertIn("sprint-planning", planning_phase)
        self.assertIn("sprint-planning", gateway)

    def test_findings_record_tested_status(self):
        findings = (
            REPO_ROOT / "eval" / "03-planning" / "sprint-planning" / "findings.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Current status: `tested`", findings)
        self.assertIn("isolated benchmark", findings)


if __name__ == "__main__":
    unittest.main()
