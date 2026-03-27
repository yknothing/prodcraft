from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "archive_superpowers_skills.py"


def load_module():
    spec = importlib.util.spec_from_file_location("archive_superpowers_skills", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ArchiveSuperpowersSkillsTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.skills_root = self.root / "skills"
        self.archive_root = self.root / "skills-archive"
        self.skills_root.mkdir(parents=True, exist_ok=True)
        self.state_path = self.root / "state.json"
        self.log_path = self.root / "events.jsonl"

    def create_skill_dir(self, dirname: str) -> Path:
        skill_dir = self.skills_root / dirname
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(f"# {dirname}\n", encoding="utf-8")
        return skill_dir

    def read_events(self) -> list[dict]:
        if not self.log_path.exists():
            return []
        return [json.loads(line) for line in self.log_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def test_archive_moves_present_dirs_and_logs_event(self):
        self.create_skill_dir("using-superpowers")
        self.create_skill_dir(".disabled-prodcraft-brainstorming")

        result = self.module.archive_skills(
            skills_root=self.skills_root,
            archive_root=self.archive_root,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="prodcraft production cutover",
        )

        self.assertEqual("archived", result["status"])
        self.assertFalse((self.skills_root / "using-superpowers").exists())
        self.assertFalse((self.skills_root / ".disabled-prodcraft-brainstorming").exists())
        self.assertTrue((self.archive_root / "using-superpowers").exists())
        self.assertTrue((self.archive_root / ".disabled-prodcraft-brainstorming").exists())

        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertEqual("archive", state["last_action"])
        self.assertEqual("prodcraft production cutover", state["reason"])
        self.assertIn("using-superpowers", state["archived"])

        events = self.read_events()
        self.assertEqual(1, len(events))
        self.assertEqual("archive", events[0]["action"])
        self.assertEqual("archived", events[0]["status_after"])
        self.assertEqual(
            [".disabled-prodcraft-brainstorming", "using-superpowers"],
            sorted(events[0]["moved_dirnames"]),
        )

    def test_restore_moves_archived_dirs_back(self):
        self.create_skill_dir("verification-before-completion")
        self.module.archive_skills(
            skills_root=self.skills_root,
            archive_root=self.archive_root,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="prodcraft production cutover",
        )

        result = self.module.restore_skills(
            skills_root=self.skills_root,
            archive_root=self.archive_root,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="rollback prodcraft cutover",
        )

        self.assertEqual("source-present", result["status"])
        self.assertTrue((self.skills_root / "verification-before-completion").exists())
        self.assertFalse((self.archive_root / "verification-before-completion").exists())

        events = self.read_events()
        self.assertEqual(["archive", "restore"], [event["action"] for event in events])
        self.assertEqual("source-present", events[-1]["status_after"])

    def test_status_reports_mixed_state(self):
        self.create_skill_dir("systematic-debugging")
        self.archive_root.mkdir(parents=True, exist_ok=True)
        (self.archive_root / "writing-plans").mkdir(parents=True, exist_ok=True)

        result = self.module.get_status(
            skills_root=self.skills_root,
            archive_root=self.archive_root,
            state_path=self.state_path,
        )

        self.assertEqual("mixed", result["status"])
        self.assertIn("systematic-debugging", result["present"])
        self.assertIn("writing-plans", result["archived"])


if __name__ == "__main__":
    unittest.main()
