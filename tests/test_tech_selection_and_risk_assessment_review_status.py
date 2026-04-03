from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class TechSelectionAndRiskAssessmentReviewStatusTests(unittest.TestCase):
    def setUp(self):
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))

    def test_manifest_registers_both_skills_as_review_routed(self):
        entries = {entry["name"]: entry for entry in self.manifest["skills"]}

        tech = entries["tech-selection"]
        risk = entries["risk-assessment"]

        self.assertEqual("02-architecture", tech["phase"])
        self.assertEqual("03-planning", risk["phase"])
        self.assertEqual("review", tech["status"])
        self.assertEqual("review", risk["status"])
        self.assertEqual("standard", tech["qa_tier"])
        self.assertEqual("standard", risk["qa_tier"])
        self.assertEqual("routed", tech["evaluation_mode"])
        self.assertEqual("routed", risk["evaluation_mode"])

        for entry in (tech, risk):
            qa = entry["qa"]
            self.assertIn("structure_validation_path", qa)
            self.assertIn("eval_strategy_path", qa)
            self.assertIn("benchmark_plan_path", qa)
            self.assertIn("findings_path", qa)
            self.assertIn("integration_test_path", qa)

    def test_review_artifacts_exist(self):
        targets = [
            REPO_ROOT / "eval" / "02-architecture" / "tech-selection" / "findings.md",
            REPO_ROOT / "eval" / "02-architecture" / "tech-selection" / "evals" / "eval-strategy.md",
            REPO_ROOT / "eval" / "02-architecture" / "tech-selection" / "isolated-benchmark-plan.md",
            REPO_ROOT / "eval" / "02-architecture" / "tech-selection" / "system-design-handoff-review.md",
            REPO_ROOT / "eval" / "03-planning" / "risk-assessment" / "findings.md",
            REPO_ROOT / "eval" / "03-planning" / "risk-assessment" / "evals" / "eval-strategy.md",
            REPO_ROOT / "eval" / "03-planning" / "risk-assessment" / "isolated-benchmark-plan.md",
            REPO_ROOT / "eval" / "03-planning" / "risk-assessment" / "task-breakdown-handoff-review.md",
        ]

        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_gateway_phase_docs_and_artifact_flow_reference_both_skills(self):
        artifact_flow = {entry["artifact"]: entry for entry in self.manifest["artifact_flow"]}
        architecture_phase = (REPO_ROOT / "skills" / "02-architecture" / "_phase.md").read_text(encoding="utf-8")
        planning_phase = (REPO_ROOT / "skills" / "03-planning" / "_phase.md").read_text(encoding="utf-8")
        gateway = (REPO_ROOT / "skills" / "_gateway.md").read_text(encoding="utf-8")

        self.assertEqual("tech-selection", artifact_flow["tech-decision-record"]["produced_by"])
        self.assertEqual("risk-assessment", artifact_flow["risk-register"]["produced_by"])
        self.assertIn("tech-selection", architecture_phase)
        self.assertIn("risk-assessment", planning_phase)
        self.assertIn("tech-selection", gateway)
        self.assertIn("risk-assessment", gateway)


if __name__ == "__main__":
    unittest.main()
