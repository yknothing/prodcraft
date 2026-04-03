from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class PublicSkillPositioningTests(unittest.TestCase):
    def test_readme_distinguishes_routed_skills_from_discoverability(self):
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("## Routed vs Discoverability", readme)
        self.assertIn("discoverability-first", readme)
        self.assertIn("routed", readme)
        self.assertIn("not a promise that every skill should auto-trigger", readme)
        self.assertIn("packaging stability", readme)
        self.assertIn("capability readiness", readme)

    def test_curated_prodcraft_skill_sets_routed_expectation(self):
        prodcraft_skill = (REPO_ROOT / "skills" / ".curated" / "prodcraft" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("## Routed Invocation", prodcraft_skill)
        self.assertIn("stable packaging contract", prodcraft_skill)
        self.assertIn("deeper lifecycle skills", prodcraft_skill)
        self.assertIn("Packaging stability", prodcraft_skill)
        self.assertIn("Capability readiness", prodcraft_skill)


if __name__ == "__main__":
    unittest.main()
