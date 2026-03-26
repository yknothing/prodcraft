from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class CrossCuttingMatrixTests(unittest.TestCase):
    def test_matrix_references_valid_phases_and_skills(self):
        manifest = yaml.safe_load((REPO_ROOT / "manifest.yml").read_text(encoding="utf-8"))
        matrix = yaml.safe_load((REPO_ROOT / "rules" / "cross-cutting-matrix.yml").read_text(encoding="utf-8"))

        phase_ids = {phase["id"] for phase in manifest["phases"]}
        skill_names = {skill["name"] for skill in manifest["skills"]}

        entries = matrix["phases"]
        self.assertEqual(phase_ids, {entry["phase_id"] for entry in entries})

        for entry in entries:
            required = set(entry.get("required", []))
            conditional = {item["skill"] for item in entry.get("conditional", [])}
            self.assertTrue(required.isdisjoint(conditional))
            for skill_name in required | conditional:
                self.assertIn(skill_name, skill_names)


if __name__ == "__main__":
    unittest.main()
