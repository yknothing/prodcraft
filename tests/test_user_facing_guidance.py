from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class UserFacingGuidanceTests(unittest.TestCase):
    def test_claude_mentions_default_chinese_and_plain_language(self):
        content = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("User-facing responses default to Chinese", content)
        self.assertIn("Use plain language", content)
        self.assertIn("system shape and collaboration quality", content)

    def test_schema_mentions_user_facing_language_and_system_collaboration_checks(self):
        content = (REPO_ROOT / "skills" / "_schema.md").read_text(encoding="utf-8")
        self.assertIn("Present user-facing outputs in the user's language", content)
        self.assertIn("must never be hard-coded into exported skill bodies", content)
        self.assertIn("Use plain language", content)
        self.assertIn("system shape and collaboration quality", content)

    def test_exported_skill_bodies_carry_no_operator_locale_default(self):
        # Operator locale policy lives in CLAUDE.md; exported skill prose must
        # stay locale-neutral so public installs do not inherit it.
        curated_root = REPO_ROOT / "skills" / ".curated"
        for skill_file in sorted(curated_root.rglob("SKILL.md")):
            content = skill_file.read_text(encoding="utf-8")
            self.assertNotIn("Default to Chinese", content, skill_file.name)
            self.assertNotIn("default to Chinese", content, skill_file.name)

    def test_entry_skills_call_out_plain_language_and_system_collaboration_signals(self):
        intake = (REPO_ROOT / "skills" / "00-discovery" / "pc-intake" / "SKILL.md").read_text(encoding="utf-8")
        framing = (REPO_ROOT / "skills" / "00-discovery" / "pc-problem-framing" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("plain language", intake)
        self.assertIn("system shape", intake)
        self.assertIn("collaboration quality", intake)

        self.assertIn("plain language", framing)
        self.assertIn("system shape", framing)
        self.assertIn("collaboration quality", framing)


if __name__ == "__main__":
    unittest.main()
