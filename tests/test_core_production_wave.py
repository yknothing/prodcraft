from __future__ import annotations

import unittest
from pathlib import Path
import json

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class CoreProductionWaveTests(unittest.TestCase):
    def setUp(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        self.entries = {entry["name"]: entry for entry in manifest["skills"]}

    def test_core_spine_skills_are_now_production_with_security_reviews(self):
        targets = {
            "intake": "00-discovery",
            "problem-framing": "00-discovery",
            "requirements-engineering": "01-specification",
            "task-breakdown": "03-planning",
            "tdd": "04-implementation",
            "verification-before-completion": "cross-cutting",
        }

        for name, phase in targets.items():
            with self.subTest(skill=name):
                entry = self.entries[name]
                self.assertEqual(phase, entry["phase"])
                self.assertEqual("production", entry["status"])
                self.assertEqual("critical", entry["qa_tier"])
                self.assertEqual("routed", entry["evaluation_mode"])

                qa = entry["qa"]
                for key in (
                    "benchmark_results_path",
                    "integration_test_path",
                    "findings_path",
                    "security_review_path",
                ):
                    self.assertIn(key, qa)
                    self.assertTrue((REPO_ROOT / qa[key]).exists(), f"{name} -> {key}")

    def test_production_wave_doc_records_the_narrow_batch(self):
        content = (
            REPO_ROOT / "docs" / "plans" / "2026-04-10-core-production-wave.md"
        ).read_text(encoding="utf-8")

        self.assertIn("production`: `6`", content)
        self.assertIn("do not mass-promote the entire `tested` set", content)
        self.assertIn("public core spine", content)

    def test_verification_before_completion_is_now_public_core(self):
        index = json.loads((REPO_ROOT / "skills" / ".curated" / "index.json").read_text(encoding="utf-8"))
        entries = {entry["name"]: entry for entry in index["skills"]}

        self.assertEqual("core", entries["verification-before-completion"]["readiness"])


if __name__ == "__main__":
    unittest.main()
