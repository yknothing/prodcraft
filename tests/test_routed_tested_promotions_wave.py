from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class RoutedTestedPromotionsWaveTests(unittest.TestCase):
    def setUp(self):
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        self.entries = {entry["name"]: entry for entry in self.manifest["skills"]}

    def test_manifest_registers_wave_skills_as_tested_with_benchmark_results(self):
        targets = {
            "user-research": "00-discovery",
            "incident-response": "07-operations",
            "runbooks": "07-operations",
            "tech-debt-management": "08-evolution",
            "retrospective": "08-evolution",
        }

        for name, phase in targets.items():
            with self.subTest(skill=name):
                entry = self.entries[name]
                self.assertEqual(phase, entry["phase"])
                self.assertEqual("tested", entry["status"])
                self.assertEqual("routed", entry["evaluation_mode"])
                qa = entry["qa"]
                self.assertIn("benchmark_results_path", qa)
                self.assertTrue((REPO_ROOT / qa["benchmark_results_path"]).exists())
                self.assertTrue((REPO_ROOT / qa["findings_path"]).exists())
                self.assertTrue((REPO_ROOT / qa["integration_test_path"]).exists())

    def test_findings_record_tested_status_for_wave_skills(self):
        targets = [
            REPO_ROOT / "eval" / "00-discovery" / "user-research" / "findings.md",
            REPO_ROOT / "eval" / "07-operations" / "incident-response" / "findings.md",
            REPO_ROOT / "eval" / "07-operations" / "runbooks" / "findings.md",
            REPO_ROOT / "eval" / "08-evolution" / "tech-debt-management" / "findings.md",
            REPO_ROOT / "eval" / "08-evolution" / "retrospective" / "findings.md",
        ]

        for path in targets:
            with self.subTest(path=path):
                content = path.read_text(encoding="utf-8")
                self.assertIn("`tested`", content)


if __name__ == "__main__":
    unittest.main()
