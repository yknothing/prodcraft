import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.anthropic_trigger_eval import run_eval as run_eval_module

RUN_EVAL_PATH = REPO_ROOT / "tools" / "anthropic_trigger_eval" / "run_eval.py"
RERUN_SCRIPT_PATH = REPO_ROOT / "eval" / "00-discovery" / "intake" / "scripts" / "rerun_iter2_trigger_eval.sh"
DETERMINISTIC_UUID_HEX = "12345678abcdef00"
DETERMINISTIC_CLEAN_NAME = "intake-skill-12345678"


class StaticUuid:
    hex = DETERMINISTIC_UUID_HEX


class FakeStdout:
    def __init__(self, remaining: bytes = b""):
        self.remaining = remaining

    def read(self) -> bytes:
        data = self.remaining
        self.remaining = b""
        return data

    def fileno(self) -> int:
        return 12345


class FakeProcess:
    def __init__(self, stdout: FakeStdout, poll_results: list[int | None]):
        self.stdout = stdout
        self.poll_results = list(poll_results)
        self.killed = False

    def poll(self) -> int | None:
        if self.poll_results:
            return self.poll_results.pop(0)
        return None

    def kill(self) -> None:
        self.killed = True

    def wait(self) -> int:
        return 0


def stream_event_lines(clean_name: str = DETERMINISTIC_CLEAN_NAME, trailing_newline: bool = True) -> bytes:
    lines = [
        json.dumps(
            {
                "type": "stream_event",
                "event": {
                    "type": "content_block_start",
                    "content_block": {"type": "tool_use", "name": "Skill"},
                },
            }
        ),
        json.dumps(
            {
                "type": "stream_event",
                "event": {
                    "type": "content_block_delta",
                    "delta": {"type": "input_json_delta", "partial_json": clean_name},
                },
            }
        ),
        json.dumps({"type": "result"}),
    ]
    payload = "\n".join(lines)
    if trailing_newline:
        payload += "\n"
    return payload.encode("utf-8")


class AnthropicTriggerEvalToolingTests(unittest.TestCase):
    def test_project_owned_run_eval_exists(self):
        self.assertTrue(RUN_EVAL_PATH.exists(), RUN_EVAL_PATH)

    def test_intake_rerun_script_uses_project_owned_harness_and_current_paths(self):
        content = RERUN_SCRIPT_PATH.read_text(encoding="utf-8")
        self.assertNotIn("intake-workspace", content)
        self.assertNotIn(".claude/plugins/cache/claude-plugins-official/skill-creator", content)
        self.assertIn("tools/anthropic_trigger_eval/run_eval.py", content)
        self.assertIn("--observability-output", content)
        self.assertIn("eval/00-discovery/intake/evals/trigger-core.json", content)
        self.assertIn("eval/00-discovery/intake/evals/trigger-overlap.json", content)
        self.assertIn("eval/00-discovery/intake/evals/trigger-non-trigger.json", content)

    def test_project_owned_run_eval_executes_with_fake_claude(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            (temp_root / ".claude" / "commands").mkdir(parents=True)

            bin_dir = temp_root / "bin"
            bin_dir.mkdir()
            fake_claude = bin_dir / "claude"
            fake_claude.write_text(
                "\n".join(
                    [
                        "#!/usr/bin/env python3",
                        "import json",
                        "from pathlib import Path",
                        "command_dir = Path.cwd() / '.claude' / 'commands'",
                        "command_files = sorted(command_dir.glob('*.md'))",
                        "clean_name = command_files[0].stem if command_files else 'missing-skill'",
                        "print(json.dumps({'type':'stream_event','event':{'type':'content_block_start','content_block':{'type':'tool_use','name':'Skill'}}}))",
                        "print(json.dumps({'type':'stream_event','event':{'type':'content_block_delta','delta':{'type':'input_json_delta','partial_json': clean_name}}}))",
                        "print(json.dumps({'type':'result'}))",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            fake_claude.chmod(0o755)

            skill_dir = temp_root / "skill"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\nname: intake\ndescription: Use when starting a new effort.\n---\n\n# Intake\n",
                encoding="utf-8",
            )

            eval_set = temp_root / "eval-set.json"
            eval_set.write_text(
                json.dumps([{"query": "start from scratch", "should_trigger": True}]),
                encoding="utf-8",
            )
            observability_path = temp_root / "execution-observability.jsonl"

            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"
            env["PRODCRAFT_CLAUDE_BIN"] = str(fake_claude)

            result = subprocess.run(
                [
                    sys.executable,
                    str(RUN_EVAL_PATH),
                    "--eval-set",
                    str(eval_set),
                    "--skill-path",
                    str(skill_dir),
                    "--num-workers",
                    "1",
                    "--runs-per-query",
                    "1",
                    "--timeout",
                    "3",
                    "--observability-output",
                    str(observability_path),
                ],
                cwd=temp_root,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["summary"]["passed"], 1)
            self.assertEqual(payload["summary"]["total"], 1)
            events = [
                json.loads(line)
                for line in observability_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            event_types = {event["event_type"] for event in events}
            self.assertIn("runner_execution.started", event_types)
            self.assertIn("runner_execution.completed", event_types)
            self.assertIn("skill_invocation.started", event_types)
            self.assertIn("skill_invocation.completed", event_types)
            self.assertIn("skill_context.measured", event_types)
            self.assertIn("model_usage.unavailable", event_types)

    def test_run_single_query_parses_remaining_stdout_after_process_exit(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            (project_root / ".claude" / "commands").mkdir(parents=True)
            fake_process = FakeProcess(
                stdout=FakeStdout(stream_event_lines(trailing_newline=False)),
                poll_results=[0],
            )

            with (
                mock.patch.object(run_eval_module.uuid, "uuid4", return_value=StaticUuid()),
                mock.patch.object(run_eval_module.subprocess, "Popen", return_value=fake_process),
            ):
                triggered = run_eval_module.run_single_query(
                    query="start from scratch",
                    skill_name="intake",
                    skill_description="Use when starting a new effort.",
                    timeout=3,
                    project_root=str(project_root),
                )

            self.assertTrue(triggered)

    def test_run_single_query_flushes_buffer_after_empty_read(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            (project_root / ".claude" / "commands").mkdir(parents=True)
            fake_process = FakeProcess(stdout=FakeStdout(), poll_results=[None, None])
            chunks = [stream_event_lines(trailing_newline=False), b""]

            with (
                mock.patch.object(run_eval_module.uuid, "uuid4", return_value=StaticUuid()),
                mock.patch.object(run_eval_module.subprocess, "Popen", return_value=fake_process),
                mock.patch.object(run_eval_module.select, "select", return_value=([fake_process.stdout], [], [])),
                mock.patch.object(run_eval_module.os, "read", side_effect=chunks),
            ):
                triggered = run_eval_module.run_single_query(
                    query="start from scratch",
                    skill_name="intake",
                    skill_description="Use when starting a new effort.",
                    timeout=3,
                    project_root=str(project_root),
                )

            self.assertTrue(triggered)

    def test_run_single_query_reassembles_json_across_chunks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            (project_root / ".claude" / "commands").mkdir(parents=True)
            fake_process = FakeProcess(stdout=FakeStdout(), poll_results=[None, None])
            payload = stream_event_lines()
            chunks = [payload[:57], payload[57:]]

            with (
                mock.patch.object(run_eval_module.uuid, "uuid4", return_value=StaticUuid()),
                mock.patch.object(run_eval_module.subprocess, "Popen", return_value=fake_process),
                mock.patch.object(run_eval_module.select, "select", return_value=([fake_process.stdout], [], [])),
                mock.patch.object(run_eval_module.os, "read", side_effect=chunks),
            ):
                triggered = run_eval_module.run_single_query(
                    query="start from scratch",
                    skill_name="intake",
                    skill_description="Use when starting a new effort.",
                    timeout=3,
                    project_root=str(project_root),
                )

            self.assertTrue(triggered)

    def test_run_single_query_checks_all_assistant_tool_uses(self):
        assistant_event = {
            "type": "assistant",
            "message": {
                "content": [
                    {"type": "tool_use", "name": "Other", "input": {"skill": "not-it"}},
                    {
                        "type": "tool_use",
                        "name": "Skill",
                        "input": {"skill": DETERMINISTIC_CLEAN_NAME},
                    },
                ]
            },
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            (project_root / ".claude" / "commands").mkdir(parents=True)
            payload = json.dumps(assistant_event).encode("utf-8")
            fake_process = FakeProcess(stdout=FakeStdout(payload), poll_results=[0])

            with (
                mock.patch.object(run_eval_module.uuid, "uuid4", return_value=StaticUuid()),
                mock.patch.object(run_eval_module.subprocess, "Popen", return_value=fake_process),
            ):
                triggered = run_eval_module.run_single_query(
                    query="start from scratch",
                    skill_name="intake",
                    skill_description="Use when starting a new effort.",
                    timeout=3,
                    project_root=str(project_root),
                )

            self.assertTrue(triggered)


if __name__ == "__main__":
    unittest.main()
