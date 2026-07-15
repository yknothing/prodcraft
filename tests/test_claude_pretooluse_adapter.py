from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = REPO_ROOT / ".claude" / "hooks" / "prodcraft_pretooluse.py"


class ClaudePreToolUseAdapterTests(unittest.TestCase):
    def make_repo(self, root: Path) -> None:
        validator = root / "scripts" / "validate_prodcraft.py"
        validator.parent.mkdir(parents=True)
        validator.write_text(
            """#!/usr/bin/env python3
import json
import os
import sys
swap_target = os.environ.get("STUB_SWAP_BRIEF")
if swap_target:
    with open(swap_target, "w", encoding="utf-8") as handle:
        json.dump({"status": "approved", "approver": "attacker", "intake_mode": "fast-track"}, handle)
print(json.dumps({"status": "valid", "authority": None, "errors": []}))
raise SystemExit(int(os.environ.get("STUB_VALIDATOR_EXIT", "0")))
""",
            encoding="utf-8",
        )

    def write_brief(
        self,
        root: Path,
        *,
        work_id: str = "work-123",
        status: str = "approved",
        approver: str = "reviewer@example.com",
        intake_mode: str = "fast-track",
    ) -> Path:
        brief = root / ".prodcraft" / "artifacts" / work_id / "intake-brief.json"
        brief.parent.mkdir(parents=True, exist_ok=True)
        brief.write_text(
            json.dumps(
                {
                    "artifact": "intake-brief",
                    "schema_version": "intake-brief.v1",
                    "status": status,
                    "approver": approver,
                    "intake_mode": intake_mode,
                }
            ),
            encoding="utf-8",
        )
        return brief

    def run_adapter(
        self,
        root: Path,
        *,
        file_path: Path | None = None,
        tool_name: str = "Write",
        work_id: str | None = "work-123",
        extra_env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["CLAUDE_PROJECT_DIR"] = str(root)
        if work_id is None:
            env.pop("PRODCRAFT_WORK_ID", None)
        else:
            env["PRODCRAFT_WORK_ID"] = work_id
        env.update(extra_env or {})
        payload = {
            "hook_event_name": "PreToolUse",
            "tool_name": tool_name,
            "tool_input": {"file_path": str(file_path or (root / "src" / "app.py"))},
        }
        return subprocess.run(
            [sys.executable, str(ADAPTER_PATH)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            cwd=root,
            env=env,
            timeout=5,
        )

    def test_missing_work_id_or_brief_blocks_with_exit_two(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.make_repo(root)

            missing_id = self.run_adapter(root, work_id=None)
            self.assertEqual(2, missing_id.returncode)
            self.assertIn("PRODCRAFT_WORK_ID", missing_id.stderr)

            missing_brief = self.run_adapter(root)
            self.assertEqual(2, missing_brief.returncode)
            self.assertIn("intake-brief.json", missing_brief.stderr)

    def test_exact_intake_brief_write_is_the_only_bootstrap_escape(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.make_repo(root)
            brief = root / ".prodcraft" / "artifacts" / "work-123" / "intake-brief.json"

            bootstrap = self.run_adapter(root, file_path=brief)
            self.assertEqual(0, bootstrap.returncode, bootstrap.stderr)

            wrong_work = self.run_adapter(
                root,
                file_path=root / ".prodcraft" / "artifacts" / "work-456" / "intake-brief.json",
            )
            self.assertEqual(2, wrong_work.returncode)

    def test_approved_non_micro_brief_passes_and_invalid_states_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.make_repo(root)

            self.write_brief(root)
            allowed = self.run_adapter(root)
            self.assertEqual(0, allowed.returncode, allowed.stderr)

            self.write_brief(root, status="draft")
            self.assertEqual(2, self.run_adapter(root).returncode)
            self.write_brief(root, approver="   ")
            self.assertEqual(2, self.run_adapter(root).returncode)
            self.write_brief(root, intake_mode="micro")
            micro = self.run_adapter(root)
            self.assertEqual(2, micro.returncode)
            self.assertIn("micro", micro.stderr)

    def test_validator_failure_and_symlinked_brief_map_to_blocking_exit_two(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.make_repo(root)
            brief = self.write_brief(root)

            failed = self.run_adapter(root, extra_env={"STUB_VALIDATOR_EXIT": "1"})
            self.assertEqual(2, failed.returncode)
            self.assertIn("repository validator", failed.stderr)

            real_brief = brief.with_name("real-brief.json")
            brief.rename(real_brief)
            brief.symlink_to(real_brief)
            symlinked = self.run_adapter(root)
            self.assertEqual(2, symlinked.returncode)
            self.assertIn("symlink", symlinked.stderr)

    def test_symlinked_brief_parent_cannot_escape_the_project(self):
        with tempfile.TemporaryDirectory() as tmpdir, tempfile.TemporaryDirectory() as outside_tmpdir:
            root = Path(tmpdir)
            outside = Path(outside_tmpdir)
            self.make_repo(root)
            external_artifacts = outside / "artifacts"
            external_brief = external_artifacts / "work-123" / "intake-brief.json"
            external_brief.parent.mkdir(parents=True)
            external_brief.write_text(
                json.dumps(
                    {
                        "artifact": "intake-brief",
                        "schema_version": "intake-brief.v1",
                        "status": "approved",
                        "approver": "outside@example.com",
                        "intake_mode": "fast-track",
                    }
                ),
                encoding="utf-8",
            )
            (root / ".prodcraft").symlink_to(outside, target_is_directory=True)

            escaped = self.run_adapter(root)

            self.assertEqual(2, escaped.returncode)
            self.assertIn("symlink", escaped.stderr)

    def test_validator_result_is_bound_to_the_same_brief_snapshot(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.make_repo(root)
            brief = self.write_brief(root)

            swapped = self.run_adapter(
                root,
                extra_env={"STUB_SWAP_BRIEF": str(brief)},
            )

            self.assertEqual(2, swapped.returncode)
            self.assertIn("changed during validation", swapped.stderr)

    def test_repo_settings_and_ci_track_the_adapter(self):
        settings = json.loads((REPO_ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        groups = settings["hooks"]["PreToolUse"]
        group = next(item for item in groups if item.get("matcher") == "Edit|Write")
        hook = group["hooks"][0]
        self.assertEqual("command", hook["type"])
        self.assertEqual("python3", hook["command"])
        self.assertEqual(
            ["${CLAUDE_PROJECT_DIR}/.claude/hooks/prodcraft_pretooluse.py"],
            hook["args"],
        )

        workflow = yaml.safe_load(
            (REPO_ROOT / ".github" / "workflows" / "validate-skills.yml").read_text(encoding="utf-8")
        )
        triggers = workflow[True]
        self.assertIn(".claude/**", triggers["push"]["paths"])
        self.assertIn(".claude/**", triggers["pull_request"]["paths"])


if __name__ == "__main__":
    unittest.main()
