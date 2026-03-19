import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "manifest.yml"
SKILL_PATH = REPO_ROOT / "skills" / "cross-cutting" / "bug-history-retrieval" / "SKILL.md"
GOTCHAS_PATH = REPO_ROOT / "skills" / "cross-cutting" / "bug-history-retrieval" / "references" / "gotchas.md"


class BugHistoryRetrievalSkillTests(unittest.TestCase):
    def test_skill_file_exists(self):
        self.assertTrue(SKILL_PATH.exists(), SKILL_PATH)

    def test_gotchas_file_exists(self):
        self.assertTrue(GOTCHAS_PATH.exists(), GOTCHAS_PATH)

    def test_manifest_registers_bug_history_retrieval_as_cross_cutting_skill(self):
        manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
        entries = [entry for entry in manifest.get("skills", []) if entry.get("name") == "bug-history-retrieval"]

        self.assertEqual(1, len(entries))
        entry = entries[0]
        self.assertEqual("cross-cutting", entry.get("phase"))
        self.assertEqual("skills/cross-cutting/bug-history-retrieval/SKILL.md", entry.get("file"))
        self.assertEqual("draft", entry.get("status"))

    def test_skill_references_single_file_gotchas(self):
        content = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("references/gotchas.md", content)
        self.assertNotIn("references/gotchas/", content)

    def test_gotchas_file_uses_structured_entries(self):
        content = GOTCHAS_PATH.read_text(encoding="utf-8")
        self.assertIn("## Gotchas", content)
        self.assertIn("- Trigger:", content)
        self.assertIn("- Failure mode:", content)
        self.assertIn("- What to do:", content)
        self.assertIn("- Escalate when:", content)


if __name__ == "__main__":
    unittest.main()
