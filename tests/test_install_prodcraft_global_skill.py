from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "install_prodcraft_global_skill.py"


def load_module():
    spec = importlib.util.spec_from_file_location("install_prodcraft_global_skill", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class InstallProdcraftGlobalSkillTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.skills_root = self.root / "skills"
        self.skills_root.mkdir(parents=True, exist_ok=True)
        self.state_path = self.root / "state.json"
        self.log_path = self.root / "events.jsonl"

    def read_events(self) -> list[dict]:
        if not self.log_path.exists():
            return []
        return [json.loads(line) for line in self.log_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def test_install_creates_prodcraft_skill_and_logs_event(self):
        result = self.module.install_skill(
            target_root=self.skills_root,
            repo_root=REPO_ROOT,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="enable prodcraft globally",
        )

        skill_dir = self.skills_root / "prodcraft"
        self.assertEqual("installed", result["status"])
        self.assertTrue(skill_dir.exists())
        self.assertTrue((skill_dir / "SKILL.md").exists())
        self.assertEqual("enable prodcraft globally", result["reason"])
        self.assertEqual("install", result["last_action"])

        content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: prodcraft", content)
        self.assertIn("prodcraft-runtime.json", content)
        self.assertIn("Canonical repo source: recorded in `prodcraft-runtime.json`", content)
        self.assertNotIn(str(REPO_ROOT), content)
        self.assertIn(
            "A `prodcraft` directory that contains only this `SKILL.md` is a valid gateway install",
            content,
        )
        self.assertIn("trust the current workspace as the source repository only when", content)
        self.assertIn(
            "do not claim that downstream skills such as `code-review`, `testing-strategy`, or `security-audit` ran",
            content,
        )
        self.assertIn("default entry system for software-development tasks", content)
        self.assertIn("user explicitly chooses it", content)
        self.assertIn("skipping Prodcraft preserves the same lifecycle guarantees", content)

        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertEqual("installed", state["status"])
        self.assertEqual(str(skill_dir / "prodcraft-runtime.json"), state["runtime_locator_path"])

        locator = json.loads((skill_dir / "prodcraft-runtime.json").read_text(encoding="utf-8"))
        self.assertEqual("prodcraft-runtime-locator.v1", locator["schema_version"])
        self.assertEqual(str(REPO_ROOT), locator["canonical_repo_root"])
        self.assertEqual(str(REPO_ROOT / "skills" / "_gateway.md"), locator["gateway_path"])
        self.assertEqual(str(REPO_ROOT / "skills"), locator["source_skills_root"])
        self.assertEqual(str(REPO_ROOT / "workflows"), locator["workflow_root"])
        self.assertTrue(locator["singleton_gateway_directory_is_expected"])

        events = self.read_events()
        self.assertEqual(1, len(events))
        self.assertEqual("install", events[0]["action"])
        self.assertEqual("installed", events[0]["status_after"])

    def test_status_reports_installed_skill(self):
        self.module.install_skill(
            target_root=self.skills_root,
            repo_root=REPO_ROOT,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="enable prodcraft globally",
        )

        result = self.module.get_status(
            target_root=self.skills_root,
            state_path=self.state_path,
        )

        self.assertEqual("installed", result["status"])
        self.assertTrue(result["skill_exists"])
        self.assertEqual(str(self.skills_root / "prodcraft" / "prodcraft-runtime.json"), result["runtime_locator_path"])

    def test_remove_deletes_skill_and_logs_event(self):
        self.module.install_skill(
            target_root=self.skills_root,
            repo_root=REPO_ROOT,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="enable prodcraft globally",
        )

        result = self.module.remove_skill(
            target_root=self.skills_root,
            state_path=self.state_path,
            log_path=self.log_path,
            reason="cleanup after experiment",
        )

        self.assertEqual("removed", result["status"])
        self.assertEqual("cleanup after experiment", result["reason"])
        self.assertEqual("remove", result["last_action"])
        self.assertFalse((self.skills_root / "prodcraft").exists())

        events = self.read_events()
        self.assertEqual(["install", "remove"], [event["action"] for event in events])
        self.assertEqual("removed", events[-1]["status_after"])


if __name__ == "__main__":
    unittest.main()
