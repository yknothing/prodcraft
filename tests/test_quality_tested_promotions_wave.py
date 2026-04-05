from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class QualityTestedPromotionsWaveTests(unittest.TestCase):
    def setUp(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        self.entries = {entry["name"]: entry for entry in manifest["skills"]}

    def test_manifest_registers_quality_wave_skills_as_tested(self):
        targets = {
            "code-review": "05-quality",
            "testing-strategy": "05-quality",
            "e2e-scenario-design": "05-quality",
        }

        for name, phase in targets.items():
            with self.subTest(skill=name):
                entry = self.entries[name]
                self.assertEqual(phase, entry["phase"])
                self.assertEqual("tested", entry["status"])
                self.assertEqual("routed", entry["evaluation_mode"])
                self.assertIn("benchmark_results_path", entry["qa"])
                self.assertTrue((REPO_ROOT / entry["qa"]["benchmark_results_path"]).exists())

    def test_tested_quality_findings_exist(self):
        targets = [
            REPO_ROOT / "eval" / "05-quality" / "code-review" / "findings.md",
            REPO_ROOT / "eval" / "05-quality" / "testing-strategy" / "findings.md",
            REPO_ROOT / "eval" / "05-quality" / "testing-strategy" / "isolated-benchmark-review.md",
            REPO_ROOT / "eval" / "05-quality" / "e2e-scenario-design" / "isolated-benchmark-review.md",
        ]

        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_findings_record_narrow_tested_posture(self):
        code_review = (
            REPO_ROOT / "eval" / "05-quality" / "code-review" / "findings.md"
        ).read_text(encoding="utf-8")
        testing = (
            REPO_ROOT / "eval" / "05-quality" / "testing-strategy" / "findings.md"
        ).read_text(encoding="utf-8")
        e2e = (
            REPO_ROOT / "eval" / "05-quality" / "e2e-scenario-design" / "findings.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Current status: `tested`", code_review)
        self.assertIn("Current status: `tested`", testing)
        self.assertIn("Current status: `tested`", e2e)


if __name__ == "__main__":
    unittest.main()
