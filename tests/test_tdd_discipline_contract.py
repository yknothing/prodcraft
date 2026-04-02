from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
TDD_SKILL = REPO_ROOT / "skills" / "04-implementation" / "tdd" / "SKILL.md"


class TddDisciplineContractTests(unittest.TestCase):
    def test_tdd_skill_declares_iron_law_and_delete_means_delete(self):
        content = TDD_SKILL.read_text(encoding="utf-8")

        self.assertIn("## The Iron Law", content)
        self.assertIn("NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST", content)
        self.assertIn("delete it and start over from RED", content)
        self.assertIn("do not keep it as a \"reference\"", content)

    def test_tdd_skill_includes_rationalization_prevention_and_red_flags(self):
        content = TDD_SKILL.read_text(encoding="utf-8")

        self.assertIn("## Rationalization Prevention", content)
        self.assertIn("## Red Flags -- Stop and Start Over", content)
        self.assertIn("\"I'll write the tests after\"", content)
        self.assertIn("the next test will need it anyway", content)

    def test_tdd_manifest_entry_is_critical_routed_and_tested_with_benchmark_results(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        entries = {entry["name"]: entry for entry in manifest["skills"]}

        tdd = entries["tdd"]

        self.assertEqual("04-implementation", tdd["phase"])
        self.assertEqual("tested", tdd["status"])
        self.assertEqual("critical", tdd["qa_tier"])
        self.assertEqual("routed", tdd["evaluation_mode"])

        qa = tdd["qa"]
        self.assertIn("benchmark_results_path", qa)
        self.assertIn("integration_test_path", qa)
        self.assertIn("findings_path", qa)

        self.assertTrue((REPO_ROOT / qa["benchmark_results_path"]).exists())
        self.assertTrue((REPO_ROOT / qa["integration_test_path"]).exists())
        self.assertTrue((REPO_ROOT / qa["findings_path"]).exists())


if __name__ == "__main__":
    unittest.main()
