import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUN_EVAL_PATH = REPO_ROOT / "tools" / "anthropic_trigger_eval" / "run_eval.py"
RERUN_SCRIPT_PATH = REPO_ROOT / "eval" / "00-discovery" / "intake" / "scripts" / "rerun_iter2_trigger_eval.sh"


class AnthropicTriggerEvalToolingTests(unittest.TestCase):
    def test_project_owned_run_eval_exists(self):
        self.assertTrue(RUN_EVAL_PATH.exists(), RUN_EVAL_PATH)

    def test_intake_rerun_script_uses_project_owned_harness_and_current_paths(self):
        content = RERUN_SCRIPT_PATH.read_text(encoding="utf-8")
        self.assertNotIn("intake-workspace", content)
        self.assertNotIn(".claude/plugins/cache/claude-plugins-official/skill-creator", content)
        self.assertIn("tools/anthropic_trigger_eval/run_eval.py", content)
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

            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"

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


if __name__ == "__main__":
    unittest.main()
