from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class ReceivingCodeReviewSkillTests(unittest.TestCase):
    def setUp(self):
        self.manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))

    def test_skill_files_exist(self):
        targets = [
            REPO_ROOT / "skills" / "05-quality" / "receiving-code-review" / "SKILL.md",
            REPO_ROOT / "skills" / "05-quality" / "receiving-code-review" / "references" / "gotchas.md",
        ]
        for path in targets:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)

    def test_manifest_registers_receiving_code_review_as_quality_skill(self):
        entries = {entry["name"]: entry for entry in self.manifest["skills"]}
        entry = entries["receiving-code-review"]

        self.assertEqual("05-quality", entry["phase"])
        self.assertEqual("review", entry["status"])
        self.assertEqual("standard", entry["qa_tier"])
        self.assertEqual("routed", entry["evaluation_mode"])
        self.assertIn("eval_strategy_path", entry["qa"])

    def test_artifact_flow_and_phase_docs_reference_author_side_review_followup(self):
        artifact_flow = {entry["artifact"]: entry for entry in self.manifest["artifact_flow"]}
        quality_phase = (REPO_ROOT / "skills" / "05-quality" / "_phase.md").read_text(encoding="utf-8")
        gateway = (REPO_ROOT / "skills" / "_gateway.md").read_text(encoding="utf-8")

        self.assertIn("receiving-code-review", artifact_flow["review-report"]["consumed_by"])
        self.assertEqual("receiving-code-review", artifact_flow["review-response-record"]["produced_by"])
        self.assertIn("receiving-code-review", artifact_flow["source-code"]["consumed_by"])
        self.assertIn("receiving-code-review", artifact_flow["test-suite"]["consumed_by"])

        self.assertIn("receiving-code-review", quality_phase)
        self.assertIn("receiving-code-review", gateway)


if __name__ == "__main__":
    unittest.main()
