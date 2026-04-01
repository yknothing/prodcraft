from __future__ import annotations

import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]

class CrossCuttingMatrixTests(unittest.TestCase):
    def test_matrix_references_valid_phases_and_skills(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        matrix = yaml.safe_load((REPO_ROOT / "rules" / "cross-cutting-matrix.yml").read_text(encoding="utf-8"))

        self.assertEqual("cross-cutting-matrix.v2", matrix["schema_version"])

        phase_ids = {phase["id"] for phase in manifest["phases"]}
        skill_names = {skill["name"] for skill in manifest["skills"]}
        non_draft_skills = {skill["name"] for skill in manifest["skills"] if skill.get("status") != "draft"}

        entries = matrix["phases"]
        self.assertEqual(phase_ids, {entry["phase_id"] for entry in entries})

        for entry in entries:
            must_consider = set(entry.get("must_consider", []))
            must_produce = {item["skill"] for item in entry.get("must_produce", [])}
            skip_when_fast_track = set(entry.get("skip_when_fast_track", []))
            conditional = {item["skill"] for item in entry.get("conditional", [])}
            # self.assertIn("documentation", must_consider) # documentation might be draft
            self.assertTrue(must_consider.isdisjoint(conditional))
            self.assertTrue(must_produce.isdisjoint(conditional))
            self.assertTrue(skip_when_fast_track.issubset(must_consider | must_produce))
            
            for skill_name in must_consider | must_produce:
                self.assertIn(skill_name, non_draft_skills, f"must_consider/must_produce skill {skill_name} cannot be draft")

            for skill_name in must_consider | must_produce | skip_when_fast_track | conditional:
                self.assertIn(skill_name, skill_names)

if __name__ == "__main__":
    unittest.main()
