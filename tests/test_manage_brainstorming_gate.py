from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "manage_brainstorming_gate.py"


def load_module():
    spec = importlib.util.spec_from_file_location("manage_brainstorming_gate", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ManageBrainstormingGateTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.skills_root = self.root / "skills"
        self.skills_root.mkdir(parents=True, exist_ok=True)
        self.state_path = self.root / "state.json"
        self.log_path = self.root / "events.jsonl"

    def create_brainstorming_skill(self) -> Path:
        skill_dir = self.skills_root / "brainstorming"
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text("# Brainstorming\n", encoding="utf-8")
        return skill_dir

    def read_events(self) -> list[dict]:
        if not self.log_path.exists():
            return []
        return [json.loads(line) for line in self.log_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def test_disable_renames_brainstorming_and_logs_event(self):
        original_dir = self.create_brainstorming_skill()

        result = self.module.disable_brainstorming(
            skills_root=self.skills_root,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="prodcraft experiment",
        )

        self.assertEqual("disabled", result["status"])
        self.assertFalse(original_dir.exists())
        self.assertTrue((self.skills_root / self.module.DISABLED_DIRNAME).exists())

        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertEqual("disabled", state["status"])
        self.assertEqual("brainstorming", state["skill_name"])

        events = self.read_events()
        self.assertEqual(1, len(events))
        self.assertEqual("disable", events[0]["action"])
        self.assertEqual("disabled", events[0]["status_after"])

    def test_enable_restores_brainstorming_and_logs_event(self):
        self.create_brainstorming_skill()
        self.module.disable_brainstorming(
            skills_root=self.skills_root,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="prodcraft experiment",
        )

        result = self.module.enable_brainstorming(
            skills_root=self.skills_root,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="restore after experiment",
        )

        self.assertEqual("enabled", result["status"])
        self.assertTrue((self.skills_root / "brainstorming").exists())
        self.assertFalse((self.skills_root / self.module.DISABLED_DIRNAME).exists())

        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertEqual("enabled", state["status"])

        events = self.read_events()
        self.assertEqual(["disable", "enable"], [event["action"] for event in events])
        self.assertEqual("enabled", events[-1]["status_after"])

    def test_status_reports_enabled_without_state_file(self):
        self.create_brainstorming_skill()

        result = self.module.get_status(
            skills_root=self.skills_root,
            state_path=self.state_path,
        )

        self.assertEqual("enabled", result["status"])
        self.assertTrue(result["brainstorming_exists"])
        self.assertFalse(result["disabled_dir_exists"])


if __name__ == "__main__":
    unittest.main()
