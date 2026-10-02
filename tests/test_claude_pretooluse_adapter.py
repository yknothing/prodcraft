from __future__ import annotations

import json
import os
import subprocess
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = REPO_ROOT / ".claude" / "hooks" / "prodcraft_pretooluse.py"
RUNTIME_PATH = REPO_ROOT / "scripts" / "prodcraft_runtime.py"


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
        tool_input: dict | None = None,
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
        payload["tool_input"].update(tool_input or {})
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

            bootstrap = self.run_adapter(root, file_path=brief, tool_input={"content": json.dumps({"status": "draft"})})
            self.assertEqual(0, bootstrap.returncode, bootstrap.stderr)

            wrong_work = self.run_adapter(
                root,
                file_path=root / ".prodcraft" / "artifacts" / "work-456" / "intake-brief.json",
            )
            self.assertEqual(2, wrong_work.returncode)

    def test_fifo_brief_is_rejected_without_waiting_for_a_writer(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.make_repo(root)
            brief = self.write_brief(root)
            brief.unlink()
            os.mkfifo(brief)
            result = self.run_adapter(root)
            self.assertEqual(2, result.returncode)
            self.assertIn("regular file", result.stderr)

    def test_draft_and_malformed_briefs_can_be_replaced_but_do_not_authorize_work(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.make_repo(root)
            brief = self.write_brief(root, status="draft")
            for old in (brief.read_text(), "broken JSON"):
                brief.write_text(old)
                result = self.run_adapter(root, file_path=brief, tool_input={"content": json.dumps({"status": "draft"})})
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual("", result.stdout)
                self.assertEqual(2, self.run_adapter(root).returncode)

    def test_approved_candidate_requires_host_confirmation_even_for_bootstrap(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.make_repo(root)
            brief = self.write_brief(root, status="draft")
            candidate = json.dumps({"status": "approved", "approver": "reviewer", "intake_mode": "fast-track"})
            for existing in (True, False):
                if not existing:
                    brief.unlink()
                result = self.run_adapter(root, file_path=brief, tool_input={"content": candidate})
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual("ask", json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"])

    def test_control_file_edit_or_invalid_candidate_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.make_repo(root)
            brief = self.write_brief(root)
            self.assertEqual(2, self.run_adapter(root, file_path=brief, tool_name="Edit").returncode)
            for content in (None, "{", "[]", json.dumps({"status": "unknown"})):
                with self.subTest(content=content):
                    result = self.run_adapter(root, file_path=brief, tool_input={"content": content})
                    self.assertEqual(2, result.returncode)
            rejected = self.run_adapter(root, file_path=brief, tool_input={"content": json.dumps({"status": "draft"})}, extra_env={"STUB_VALIDATOR_EXIT": "1"})
            self.assertEqual(2, rejected.returncode)

    def test_control_write_preserves_snapshot_and_path_guards(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.make_repo(root)
            brief = self.write_brief(root)
            candidate = {"content": brief.read_text()}
            unchanged = self.run_adapter(root, file_path=brief, tool_input=candidate)
            self.assertEqual(0, unchanged.returncode, unchanged.stderr)
            self.assertEqual("", unchanged.stdout)
            raced = self.run_adapter(root, file_path=brief, tool_input=candidate, extra_env={"STUB_SWAP_BRIEF": str(brief)})
            self.assertEqual(2, raced.returncode)
            self.assertIn("changed during validation", raced.stderr)
            alias = root / "alias.json"
            alias.symlink_to(brief)
            self.assertEqual(2, self.run_adapter(root, file_path=alias, tool_input=candidate).returncode)
            hardlink = root / "hardlink.json"
            os.link(brief, hardlink)
            self.assertEqual(2, self.run_adapter(root, file_path=hardlink, tool_input=candidate).returncode)
            case_alias = brief.with_name("INTAKE-BRIEF.JSON")
            if case_alias.exists() and case_alias.samefile(brief):
                self.assertEqual(2, self.run_adapter(root, file_path=case_alias, tool_input=candidate).returncode)
            brief.unlink()
            os.mkfifo(brief)
            self.assertEqual(2, self.run_adapter(root, file_path=brief, tool_input=candidate).returncode)

    def test_repair_uses_real_repository_schema_and_route_validation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.make_repo(root)
            (root / "scripts" / "validate_prodcraft.py").write_text(
                "import runpy\nrunpy.run_path(" + repr(str(REPO_ROOT / "scripts" / "validate_prodcraft.py")) + ", run_name='__main__')\n"
            )
            brief = self.write_brief(root, status="draft")
            candidate = {
                "artifact": "intake-brief", "schema_version": "intake-brief.v1",
                "status": "draft", "approver": "pending",
                "request_summary": "Repair the approved adapter defects.",
                "source_language": "en", "artifact_record_language": "en", "user_presentation_locale": "en",
                "intake_mode": "fast-track", "work_type": "Bug Fix", "entry_phase": "04-implementation",
                "quality_target_context": {"runtime_context": "host_runtime_tool", "exposure_profile": "no_network_listener", "production_target": "Local hook", "non_targets": [], "evidence_refs": []},
                "scope_assessment": "small", "recommended_next_skill": "pc-debug-expert",
                "routing_rationale": "Known adapter defect", "key_risks": [], "questions_asked": [],
                "routing_changed_by_answers": False,
            }
            result = self.run_adapter(root, file_path=brief, tool_input={"content": json.dumps(candidate)})
            self.assertEqual(0, result.returncode, result.stderr)
            brief.write_text(json.dumps(candidate))
            self.assertEqual(2, self.run_adapter(root).returncode)
            candidate.update(status="approved", approver="reviewer")
            result = self.run_adapter(root, file_path=brief, tool_input={"content": json.dumps(candidate)})
            self.assertEqual("ask", json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"])
            brief.write_text(json.dumps(candidate))  # Simulate the host-approved tool result.
            self.assertEqual(0, self.run_adapter(root).returncode)
            candidate["recommended_next_skill"] = "pc-does-not-exist"
            rejected = self.run_adapter(root, file_path=brief, tool_input={"content": json.dumps(candidate)})
            self.assertEqual(2, rejected.returncode)

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

    def test_real_compact_micro_records_never_grant_write_authority(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.make_repo(root)
            (root / "scripts" / "validate_prodcraft.py").write_text(
                "import runpy\nrunpy.run_path(" + repr(str(REPO_ROOT / "scripts" / "validate_prodcraft.py")) + ", run_name='__main__')\n"
            )
            brief = root / ".prodcraft" / "artifacts" / "work-123" / "intake-brief.json"
            brief.parent.mkdir(parents=True)
            candidate = {
                "artifact": "intake-brief", "schema_version": "intake-brief.v1",
                "status": "approved", "intake_mode": "micro", "approver": "auto (micro policy)",
                "request_summary": "Fix one documentation typo.", "recommended_next_skill": "pc-documentation",
                "routing_rationale": "One reversible line, no behavior or contract change.",
                "quality_target_context": {"runtime_context": "local_dev_harness", "exposure_profile": "no_network_listener"},
                "micro_eligibility": {key: True for key in (
                    "single_revert", "zero_questions", "no_external_effect", "no_security_impact", "no_irreversible_action")},
            }
            # Storing a micro record is bookkeeping; it supplies no native permission override.
            bootstrap = self.run_adapter(root, file_path=brief, tool_input={"content": json.dumps(candidate)})
            self.assertEqual(0, bootstrap.returncode, bootstrap.stderr)
            self.assertEqual("", bootstrap.stdout)
            brief.write_text(json.dumps(candidate))
            for tool in ("Write", "Edit"):
                for target in (root / "README.md", root / "src" / "app.py"):
                    with self.subTest(tool=tool, target=target):
                        result = self.run_adapter(root, file_path=target, tool_name=tool)
                        self.assertEqual(0, result.returncode, result.stderr)
                        self.assertEqual("ask", json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"])
            for patch in (
                {"status": "draft"}, {"approver": "reviewer"}, {"micro_eligibility": {}},
                {"recommended_next_skill": "pc-does-not-exist"},
                {"quality_target_context": {"runtime_context": "public_service", "exposure_profile": "public_internet"}},
            ):
                with self.subTest(patch=patch):
                    invalid = json.dumps({**candidate, **patch})
                    self.assertEqual(2, self.run_adapter(root, file_path=brief, tool_input={"content": invalid}).returncode)
                    brief.write_text(invalid)
                    self.assertEqual(2, self.run_adapter(root).returncode)
            brief.write_text(json.dumps(candidate))
            alias = root / "alias.json"
            alias.symlink_to(brief)
            self.assertEqual(2, self.run_adapter(root, file_path=alias).returncode)
            hardlink = root / "hardlink.json"
            os.link(brief, hardlink)
            self.assertEqual(2, self.run_adapter(root, file_path=hardlink).returncode)
            # A canonical-path write also must not mutate an aliased inode.
            self.assertEqual(2, self.run_adapter(root, file_path=brief, tool_input={"content": json.dumps(candidate)}).returncode)
            hardlink.unlink()
            alias.unlink()
            # The real validator runs, then a concurrent actor aliases the target.
            target = root / "README.md"
            target.write_text("local documentation")
            (root / "scripts" / "validate_prodcraft.py").write_text(
                "import runpy\nfrom pathlib import Path\ntry:\n    runpy.run_path("
                + repr(str(REPO_ROOT / "scripts" / "validate_prodcraft.py")) + ", run_name='__main__')\n"
                + "finally:\n    target = Path(" + repr(str(target)) + ")\n    target.unlink()\n    target.symlink_to(" + repr(str(brief)) + ")\n"
            )
            raced = self.run_adapter(root, file_path=target)
            self.assertEqual(2, raced.returncode, raced.stdout)

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
            ["${CLAUDE_PROJECT_DIR}/scripts/prodcraft_runtime.py", "run", "pretooluse"],
            hook["args"],
        )

        workflow = yaml.safe_load(
            (REPO_ROOT / ".github" / "workflows" / "validate-skills.yml").read_text(encoding="utf-8")
        )
        triggers = workflow[True]
        self.assertIn(".claude/**", triggers["push"]["paths"])
        self.assertIn(".claude/**", triggers["pull_request"]["paths"])

    def test_configured_hook_uses_explicit_runtime_with_missing_bootstrap_dependencies(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root)
            (root / ".claude" / "hooks").mkdir(parents=True)
            shutil.copyfile(ADAPTER_PATH, root / ".claude" / "hooks" / ADAPTER_PATH.name)
            shutil.copyfile(RUNTIME_PATH, root / "scripts" / RUNTIME_PATH.name)
            # -S models a bootstrap Python without site-installed validator dependencies.
            bootstrap = [sys.executable, "-S", str(root / "scripts" / RUNTIME_PATH.name)]
            setup = subprocess.run(
                [*bootstrap, "setup", "--python", sys.executable],
                capture_output=True, text=True, cwd=root,
            )
            self.assertEqual(0, setup.returncode, setup.stderr)
            self.write_brief(root)
            result = subprocess.run(
                [*bootstrap, "run", "pretooluse"],
                input=json.dumps({"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": str(root / "app.py")}}),
                capture_output=True, text=True, cwd=root,
                env={**os.environ, "CLAUDE_PROJECT_DIR": str(root), "PRODCRAFT_WORK_ID": "work-123"},
            )
            self.assertEqual(0, result.returncode, result.stderr)
            config = root / "build" / "prodcraft-runtime.json"
            config.unlink()
            missing = subprocess.run([*bootstrap, "run", "pretooluse"], input="{}", capture_output=True, text=True)
            self.assertEqual(2, missing.returncode)
            self.assertIn("setup --python", missing.stderr)


if __name__ == "__main__":
    unittest.main()
