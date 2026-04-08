from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class ReviewWavePromotionTests(unittest.TestCase):
    def setUp(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        self.entries = {entry["name"]: entry for entry in manifest["skills"]}

    def test_manifest_registers_review_wave_skills_with_review_stage_qa(self):
        targets = {
            "market-analysis": "00-discovery",
            "feasibility-study": "00-discovery",
            "spec-writing": "01-specification",
            "domain-modeling": "01-specification",
            "data-modeling": "02-architecture",
            "security-design": "02-architecture",
            "bug-history-retrieval": "cross-cutting",
            "internationalization": "cross-cutting",
            "compliance": "cross-cutting",
        }

        for name, phase in targets.items():
            with self.subTest(skill=name):
                entry = self.entries[name]
                self.assertEqual(phase, entry["phase"])
                self.assertEqual("review", entry["status"])
                self.assertEqual("standard", entry["qa_tier"])
                self.assertEqual("routed", entry["evaluation_mode"])
                qa = entry["qa"]
                self.assertIn("structure_validation_path", qa)
                self.assertIn("eval_strategy_path", qa)
                self.assertTrue((REPO_ROOT / qa["structure_validation_path"]).exists())
                self.assertTrue((REPO_ROOT / qa["eval_strategy_path"]).exists())

    def test_status_snapshot_records_zero_draft_state(self):
        snapshot = (
            REPO_ROOT / "docs" / "plans" / "2026-04-05-skill-status-snapshot.md"
        ).read_text(encoding="utf-8")

        self.assertIn("`tested`: `33`", snapshot)
        self.assertIn("`review`: `11`", snapshot)
        self.assertIn("`draft`: `0`", snapshot)
        self.assertIn("This wave moved `12` skills from `draft` to `review`", snapshot)


if __name__ == "__main__":
    unittest.main()
