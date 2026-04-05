from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class RefactoringReviewStatusTests(unittest.TestCase):
    def setUp(self):
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))

    def test_manifest_registers_refactoring_as_tested_routed(self):
        entries = {entry["name"]: entry for entry in self.manifest["skills"]}
        refactoring = entries["refactoring"]

        self.assertEqual("04-implementation", refactoring["phase"])
        self.assertEqual("tested", refactoring["status"])
        self.assertEqual("standard", refactoring["qa_tier"])
        self.assertEqual("routed", refactoring["evaluation_mode"])

        qa = refactoring["qa"]
        self.assertIn("structure_validation_path", qa)
        self.assertIn("eval_strategy_path", qa)
        self.assertIn("benchmark_plan_path", qa)
        self.assertIn("benchmark_results_path", qa)
        self.assertIn("findings_path", qa)
        self.assertIn("integration_test_path", qa)

    def test_refactoring_tested_artifacts_exist(self):
        targets = [
            REPO_ROOT / "eval" / "04-implementation" / "refactoring" / "findings.md",
            REPO_ROOT / "eval" / "04-implementation" / "refactoring" / "evals" / "eval-strategy.md",
            REPO_ROOT / "eval" / "04-implementation" / "refactoring" / "isolated-benchmark-plan.md",
            REPO_ROOT / "eval" / "04-implementation" / "refactoring" / "isolated-benchmark-review.md",
            REPO_ROOT / "eval" / "04-implementation" / "refactoring" / "code-review-handoff-review.md",
            REPO_ROOT / "eval" / "04-implementation" / "refactoring" / "fixtures" / "reassignment_handlers.py",
            REPO_ROOT / "eval" / "04-implementation" / "refactoring" / "fixtures" / "test_reassignment_handlers.py",
            REPO_ROOT / "eval" / "04-implementation" / "refactoring" / "fixtures" / "reassignment-structural-review-report.md",
        ]

        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_gateway_and_phase_docs_reference_refactoring(self):
        gateway = (REPO_ROOT / "skills" / "_gateway.md").read_text(encoding="utf-8")
        implementation_phase = (REPO_ROOT / "skills" / "04-implementation" / "_phase.md").read_text(encoding="utf-8")

        self.assertIn("refactoring", gateway)
        self.assertIn("refactoring", implementation_phase)

    def test_findings_record_tested_status(self):
        findings = (
            REPO_ROOT / "eval" / "04-implementation" / "refactoring" / "findings.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Current status: `tested`", findings)
        self.assertIn("isolated benchmark", findings)


if __name__ == "__main__":
    unittest.main()
