from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class ExternalSkillIntegrationBoundaryTests(unittest.TestCase):
    def test_claude_declares_external_skill_boundary(self):
        content = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")

        self.assertIn("external skill systems", content)
        self.assertIn("plugin, wrapper, adapter, or delegation boundaries", content)
        self.assertIn("Do not directly reference external skills at the source-code level", content)
        self.assertIn("implicit runtime dependencies", content)

    def test_readme_declares_public_external_skill_boundary(self):
        content = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("External Skill Integration Boundary", content)
        self.assertIn("plugin-like or delegation-style boundaries", content)
        self.assertIn("do not directly reference external skills at the source-code level", content)
        self.assertIn("do not make external skills an implicit runtime dependency", content)
        self.assertIn("validation and QA remain owned here", content)


if __name__ == "__main__":
    unittest.main()
