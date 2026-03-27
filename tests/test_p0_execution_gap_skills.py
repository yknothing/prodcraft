from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class P0ExecutionGapSkillTests(unittest.TestCase):
    def setUp(self):
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        self.matrix = yaml.safe_load((REPO_ROOT / "rules" / "cross-cutting-matrix.yml").read_text(encoding="utf-8"))

    def test_systematic_debugging_and_verification_skill_files_exist_with_gotchas(self):
        targets = [
            REPO_ROOT / "skills" / "04-implementation" / "systematic-debugging" / "SKILL.md",
            REPO_ROOT / "skills" / "04-implementation" / "systematic-debugging" / "references" / "gotchas.md",
            REPO_ROOT / "skills" / "cross-cutting" / "verification-before-completion" / "SKILL.md",
            REPO_ROOT / "skills" / "cross-cutting" / "verification-before-completion" / "references" / "gotchas.md",
        ]
        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_manifest_registers_both_p0_skills_as_critical_review_routed(self):
        entries = {entry["name"]: entry for entry in self.manifest["skills"]}

        systematic = entries["systematic-debugging"]
        verification = entries["verification-before-completion"]

        self.assertEqual("04-implementation", systematic["phase"])
        self.assertEqual("cross-cutting", verification["phase"])
        self.assertEqual("review", systematic["status"])
        self.assertEqual("review", verification["status"])
        self.assertEqual("critical", systematic["qa_tier"])
        self.assertEqual("critical", verification["qa_tier"])
        self.assertEqual("routed", systematic["evaluation_mode"])
        self.assertEqual("routed", verification["evaluation_mode"])

        for entry in (systematic, verification):
            qa = entry["qa"]
            self.assertIn("structure_validation_path", qa)
            self.assertIn("eval_strategy_path", qa)
            self.assertIn("benchmark_plan_path", qa)
            self.assertIn("findings_path", qa)

    def test_artifact_flow_tracks_debugging_and_verification_outputs(self):
        artifact_flow = {entry["artifact"]: entry for entry in self.manifest["artifact_flow"]}

        self.assertIn("bug-fix-report", artifact_flow)
        self.assertIn("verification-record", artifact_flow)
        self.assertIn("systematic-debugging", artifact_flow["course-correction-note"]["produced_by"])
        self.assertEqual("systematic-debugging", artifact_flow["bug-fix-report"]["produced_by"])
        self.assertEqual("verification-before-completion", artifact_flow["verification-record"]["produced_by"])

        self.assertIn("systematic-debugging", artifact_flow["source-code"]["consumed_by"])
        self.assertIn("systematic-debugging", artifact_flow["test-suite"]["consumed_by"])
        self.assertIn("systematic-debugging", artifact_flow["historical-defect-context"]["consumed_by"])
        self.assertIn("systematic-debugging", artifact_flow["fix-lineage-brief"]["consumed_by"])

    def test_gateway_phase_docs_and_hotfix_docs_reference_new_execution_skills(self):
        gateway = (REPO_ROOT / "skills" / "_gateway.md").read_text(encoding="utf-8")
        implementation_phase = (REPO_ROOT / "skills" / "04-implementation" / "_phase.md").read_text(encoding="utf-8")
        incident_response = (REPO_ROOT / "skills" / "07-operations" / "incident-response" / "SKILL.md").read_text(encoding="utf-8")
        hotfix = (REPO_ROOT / "workflows" / "hotfix.md").read_text(encoding="utf-8")

        self.assertIn("systematic-debugging", gateway)
        self.assertIn("verification-before-completion", gateway)
        self.assertIn("systematic-debugging", implementation_phase)
        self.assertIn("systematic-debugging", incident_response)
        self.assertIn("verification-before-completion", hotfix)
        self.assertIn("systematic-debugging", hotfix)

    def test_cross_cutting_matrix_injects_verification_for_execution_heavy_phases(self):
        expected_phases = {"04-implementation", "05-quality", "06-delivery", "07-operations", "08-evolution"}
        entries = {entry["phase_id"]: entry for entry in self.matrix["phases"]}

        for phase_id in expected_phases:
            with self.subTest(phase=phase_id):
                conditional_skills = {item["skill"] for item in entries[phase_id]["conditional"]}
                self.assertIn("verification-before-completion", conditional_skills)


if __name__ == "__main__":
    unittest.main()
