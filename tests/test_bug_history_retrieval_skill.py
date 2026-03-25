import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "manifest.yml"
SKILL_PATH = REPO_ROOT / "skills" / "cross-cutting" / "bug-history-retrieval" / "SKILL.md"
GOTCHAS_PATH = REPO_ROOT / "skills" / "cross-cutting" / "bug-history-retrieval" / "references" / "gotchas.md"

BUG_HISTORY_SKILL_NAME = "bug-history-retrieval"
EXPECTED_PHASE = "cross-cutting"
EXPECTED_STATUS = "draft"
MANIFEST_ENTRY_PREFIX = "- name: "
SKILL_FIELD_INDENT = "  "


def extract_skill_entry_block(manifest_text: str, skill_name: str) -> str | None:
    """Extract the YAML list entry block for `- name: {skill_name}`.

    This manifest models skills as a top-level YAML list, where each entry begins at column 0
    with `- name: ...`, and subsequent fields are indented by two spaces.
    """
    # Avoid relying on third-party YAML parsers in this test.
    lines = manifest_text.splitlines(keepends=True)
    start_index: int | None = None

    for idx, line in enumerate(lines):
        if line.startswith(f"{MANIFEST_ENTRY_PREFIX}{skill_name}"):
            start_index = idx
            break

    if start_index is None:
        return None

    end_index = start_index + 1
    while end_index < len(lines):
        line = lines[end_index]
        stripped = line.strip()

        # The next skill entry starts at column 0 with `- name: ...`.
        if line.startswith(MANIFEST_ENTRY_PREFIX):
            break

        # A new top-level key (e.g. `planned_skills:`, `workflows:`) also starts at column 0.
        if not line.startswith(SKILL_FIELD_INDENT) and stripped != "":
            break

        end_index += 1

    return "".join(lines[start_index:end_index]).rstrip("\n")


class BugHistoryRetrievalSkillTests(unittest.TestCase):
    def test_skill_file_exists(self):
        self.assertTrue(SKILL_PATH.exists(), SKILL_PATH)

    def test_gotchas_file_exists(self):
        self.assertTrue(GOTCHAS_PATH.exists(), GOTCHAS_PATH)

    def test_manifest_registers_bug_history_retrieval_as_cross_cutting_skill(self):
        """Verify the specific manifest entry for bug-history-retrieval has expected phase/status."""
        manifest_text = MANIFEST_PATH.read_text(encoding="utf-8")
        entry_block = extract_skill_entry_block(manifest_text, BUG_HISTORY_SKILL_NAME)

        self.assertIsNotNone(entry_block, f"Missing skills entry for `{BUG_HISTORY_SKILL_NAME}` in manifest.yml")

        self.assertIn(f"phase: {EXPECTED_PHASE}", entry_block)
        self.assertIn(
            f"file: skills/cross-cutting/{BUG_HISTORY_SKILL_NAME}/SKILL.md",
            entry_block,
        )
        self.assertIn(f"status: {EXPECTED_STATUS}", entry_block)

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
