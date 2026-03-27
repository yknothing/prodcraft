from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class SystemDesignContractTests(unittest.TestCase):
    def setUp(self):
        self.skill_text = (
            REPO_ROOT / "skills" / "02-architecture" / "system-design" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.findings_text = (
            REPO_ROOT / "eval" / "02-architecture" / "system-design" / "findings.md"
        ).read_text(encoding="utf-8")
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))

    def test_system_design_keeps_review_contract(self):
        entries = {entry["name"]: entry for entry in self.manifest["skills"]}
        entry = entries["system-design"]

        self.assertEqual("02-architecture", entry["phase"])
        self.assertEqual("review", entry["status"])
        self.assertEqual("critical", entry["qa_tier"])
        self.assertEqual("routed", entry["evaluation_mode"])

    def test_system_design_requires_measurable_quality_attribute_table(self):
        self.assertIn("| Attribute | Stimulus | Response | Measure | Rank | Source / Assumption |", self.skill_text)
        self.assertIn("A missing bound is better recorded as `TBD`", self.skill_text)
        self.assertIn("Ranked quality attribute table exists with stimulus, response, measure, and source/assumption fields", self.skill_text)

    def test_system_design_explicitly_covers_reversibility_exit_cost_and_fitness_functions(self):
        self.assertIn("prefer reversibility over perfection", self.skill_text)
        self.assertIn("exit cost", self.skill_text)
        self.assertIn("### Step 8: Define Architecture Fitness Functions", self.skill_text)
        self.assertIn("Fitness functions exist for the top drivers", self.skill_text)
        self.assertIn("fitness functions", self.findings_text)


if __name__ == "__main__":
    unittest.main()
