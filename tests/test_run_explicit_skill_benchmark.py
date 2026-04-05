import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "run_explicit_skill_benchmark.py"


def load_module():
    spec = importlib.util.spec_from_file_location("run_explicit_skill_benchmark", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def read_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class FakeProcess:
    def __init__(self, stdout="OK\n", stderr="", returncode=0):
        self._stdout = stdout
        self._stderr = stderr
        self.returncode = returncode
        self.pid = 12345

    def communicate(self, timeout=None):
        return self._stdout, self._stderr

    def wait(self):
        return self.returncode


class RunExplicitSkillBenchmarkTests(unittest.TestCase):
    def test_sanitize_runner_output_strips_gemini_preamble_noise(self):
        module = load_module()
        noisy_output = "\n".join(
            [
                "Loaded cached credentials.",
                "Loading extension: chrome-devtools-mcp",
                "Registering notification handlers for server 'pencil'. Capabilities: { logging: {}, tools: {} }",
                "Server 'pencil' has tools but did not declare 'listChanged' capability. Listening anyway for robustness...",
                "[MCP error] Error during discovery for MCP server 'MCP_DOCKER': MCP error -32000: Connection closed",
                "    at McpError.fromError (file:///tmp/fake.js:1:1)",
                "MCP issues detected. Run /mcp list for status.## Intake Brief",
                "",
                "**Work type**: Migration",
            ]
        )

        self.assertEqual(
            module.sanitize_runner_output("gemini", noisy_output),
            "## Intake Brief\n\n**Work type**: Migration",
        )

    def test_sanitize_runner_output_preserves_clean_text(self):
        module = load_module()
        clean_output = "## Intake Brief\n\n**Work type**: Bug Fix"

        self.assertEqual(module.sanitize_runner_output("gemini", clean_output), clean_output)
        self.assertEqual(module.sanitize_runner_output("claude", clean_output), clean_output)
        self.assertEqual(module.sanitize_runner_output("copilot", clean_output), clean_output)

    def test_sanitize_runner_output_strips_copilot_footer(self):
        module = load_module()
        noisy_output = "\n".join(
            [
                "## TDD Plan",
                "",
                "- Write the failing test first",
                "",
                "Total usage est:       1 Premium request",
                "Total duration (API):  3.6s",
                "Usage by model:",
                "    Claude Sonnet 4.5    7.0k input, 4 output, 0 cache read, 0 cache write (Est. 1 Premium request)",
            ]
        )

        self.assertEqual(
            module.sanitize_runner_output("copilot", noisy_output),
            "## TDD Plan\n\n- Write the failing test first",
        )

    def test_maybe_materialize_local_artifact_reads_temp_plan_file(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            plan_path = temp_root / "plans" / "approval-reminders.md"
            plan_path.parent.mkdir(parents=True)
            plan_path.write_text("# TDD Plan\n\n- Write failing tests first\n", encoding="utf-8")

            output = (
                "I drafted the implementation plan and saved it to "
                f"`{plan_path}`.\nPlease review it."
            )

            self.assertEqual(
                module.maybe_materialize_local_artifact(output),
                "# TDD Plan\n\n- Write failing tests first",
            )

    def test_maybe_materialize_local_artifact_sanitizes_missing_temp_path(self):
        module = load_module()
        output = (
            "I drafted the implementation plan and saved it to "
            "`/Users/whatsup/.gemini/tmp/baseline-16/uuid-123/plans/demo.md`."
        )

        self.assertEqual(
            module.maybe_materialize_local_artifact(output),
            "I drafted the implementation plan and saved it to "
            "`<gemini-temp-workspace>/plans/demo.md`.",
        )

    def test_display_path_prefers_repo_relative_paths(self):
        module = load_module()
        repo_path = REPO_ROOT / "eval" / "01-specification" / "requirements-engineering" / "explicit-benchmark.json"

        self.assertEqual(
            module.display_path(repo_path),
            "eval/01-specification/requirements-engineering/explicit-benchmark.json",
        )

    def test_resolve_context_file_uses_benchmark_parent_for_relative_paths(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            benchmark_dir = temp_root / "bench"
            fixture_dir = benchmark_dir / "fixtures"
            fixture_dir.mkdir(parents=True)
            benchmark_path = benchmark_dir / "benchmark.json"
            fixture_path = fixture_dir / "brief.md"
            fixture_path.write_text("fixture\n", encoding="utf-8")

            resolved = module.resolve_context_file("fixtures/brief.md", benchmark_path)
            self.assertEqual(resolved, fixture_path.resolve())

    def test_run_prompt_uses_gemini_plan_mode_by_default(self):
        module = load_module()
        fake_process = FakeProcess(stdout="Loaded cached credentials.\nMCP issues detected. Run /mcp list for status.OK\n")

        with mock.patch.object(module.subprocess, "Popen", return_value=fake_process) as popen:
            output = module.run_prompt(
                prompt="say only OK",
                runner="gemini",
                model=None,
                cwd=Path("/tmp"),
                timeout_seconds=5,
            )

        self.assertEqual(output, "OK")
        cmd = popen.call_args.args[0]
        self.assertEqual(cmd[0], "gemini")
        self.assertIn("-p", cmd)
        self.assertIn("--output-format", cmd)
        self.assertIn("text", cmd)
        self.assertIn("--approval-mode", cmd)
        self.assertIn("plan", cmd)
        self.assertIn("--extensions", cmd)
        self.assertIn("none", cmd)
        self.assertIn("--allowed-mcp-server-names", cmd)
        self.assertNotIn("claude", cmd)

    def test_run_prompt_uses_copilot_noninteractive_defaults(self):
        module = load_module()
        fake_process = FakeProcess(stdout="● OK\n\nTotal usage est:       1 Premium request\n")

        with mock.patch.object(module.subprocess, "Popen", return_value=fake_process) as popen:
            output = module.run_prompt(
                prompt="say only OK",
                runner="copilot",
                model=None,
                cwd=Path("/tmp"),
                timeout_seconds=5,
            )

        self.assertEqual(output, "● OK")
        cmd = popen.call_args.args[0]
        self.assertEqual(cmd[0], "copilot")
        self.assertIn("-p", cmd)
        self.assertIn("--allow-all-tools", cmd)
        self.assertIn("--allow-all-paths", cmd)
        self.assertIn("--disable-builtin-mcps", cmd)
        self.assertIn("--stream", cmd)
        self.assertIn("off", cmd)
        self.assertIn("--no-custom-instructions", cmd)
        self.assertNotIn("gemini", cmd)

    def test_run_prompt_retries_copilot_connection_error_as_transient(self):
        module = load_module()
        failed = FakeProcess(
            stdout="",
            stderr='Model call failed: "Connection error."\nExecution failed: Connection error.\n',
            returncode=1,
        )
        succeeded = FakeProcess(stdout="● OK\n", stderr="", returncode=0)

        with mock.patch.object(module.subprocess, "Popen", side_effect=[failed, succeeded]) as popen:
            with mock.patch.object(module.time, "sleep") as sleep:
                output = module.run_prompt(
                    prompt="say only OK",
                    runner="copilot",
                    model=None,
                    cwd=Path("/tmp"),
                    timeout_seconds=5,
                )

        self.assertEqual(output, "● OK")
        self.assertEqual(popen.call_count, 2)
        sleep.assert_called_once()

    def test_run_prompt_retries_copilot_fetch_failed_as_transient(self):
        module = load_module()
        failed = FakeProcess(
            stdout="",
            stderr="Execution failed: fetch failed\n",
            returncode=1,
        )
        succeeded = FakeProcess(stdout="● OK\n", stderr="", returncode=0)

        with mock.patch.object(module.subprocess, "Popen", side_effect=[failed, succeeded]) as popen:
            with mock.patch.object(module.time, "sleep") as sleep:
                output = module.run_prompt(
                    prompt="say only OK",
                    runner="copilot",
                    model=None,
                    cwd=Path("/tmp"),
                    timeout_seconds=5,
                )

        self.assertEqual(output, "● OK")
        self.assertEqual(popen.call_count, 2)
        sleep.assert_called_once()

    def test_run_prompt_retries_empty_nonzero_exit_as_transient(self):
        module = load_module()
        failed = FakeProcess(stdout="", stderr="", returncode=1)
        succeeded = FakeProcess(stdout="● OK\n", stderr="", returncode=0)

        with mock.patch.object(module.subprocess, "Popen", side_effect=[failed, succeeded]) as popen:
            with mock.patch.object(module.time, "sleep") as sleep:
                output = module.run_prompt(
                    prompt="say only OK",
                    runner="copilot",
                    model=None,
                    cwd=Path("/tmp"),
                    timeout_seconds=5,
                )

        self.assertEqual(output, "● OK")
        self.assertEqual(popen.call_count, 2)
        sleep.assert_called_once()

    def test_main_records_default_runner_and_writes_outputs(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            benchmark_path = temp_root / "benchmark.json"
            skill_path = temp_root / "skill"
            skill_path.mkdir()
            (skill_path / "SKILL.md").write_text("# placeholder skill\n", encoding="utf-8")

            context_file = temp_root / "brief.md"
            context_file.write_text("brief context\n", encoding="utf-8")
            benchmark_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "demo-scenario",
                            "title": "Demo Scenario",
                            "prompt": "Summarize the copied context.",
                            "context_files": [str(context_file)],
                            "assertions": [],
                        }
                    ]
                ),
                encoding="utf-8",
            )

            output_dir = temp_root / "results"
            argv = [
                "run_explicit_skill_benchmark.py",
                "--benchmark",
                str(benchmark_path),
                "--skill-path",
                str(skill_path),
                "--output-dir",
                str(output_dir),
            ]

            with mock.patch.object(module, "run_prompt", side_effect=["baseline output", "skill output"]):
                with mock.patch.object(sys, "argv", argv):
                    exit_code = module.main()

            self.assertEqual(exit_code, 0)
            run_metadata = json.loads((output_dir / "run_metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(run_metadata["runner"], "gemini")
            events = read_jsonl(output_dir / "execution-observability.jsonl")
            event_types = {event["event_type"] for event in events}
            self.assertIn("runner_execution.started", event_types)
            self.assertIn("runner_execution.completed", event_types)
            self.assertIn("skill_invocation.started", event_types)
            self.assertIn("skill_invocation.completed", event_types)
            self.assertIn("model_usage.unavailable", event_types)

            scenario_dir = output_dir / "eval-1-demo-scenario"
            runtime_context = json.loads((scenario_dir / "runtime_context.json").read_text(encoding="utf-8"))
            self.assertEqual(runtime_context["baseline_workspace"], "baseline")
            self.assertEqual(runtime_context["with_skill_workspace"], "with-skill")
            self.assertEqual(runtime_context["copied_skill_path"], "with-skill/skill-under-test/SKILL.md")
            self.assertEqual(runtime_context["baseline_context_files"], ["baseline/brief.md"])
            self.assertEqual(runtime_context["with_skill_context_files"], ["with-skill/brief.md"])
            self.assertEqual(
                (scenario_dir / "without_skill" / "response.md").read_text(encoding="utf-8").strip(),
                "baseline output",
            )
            self.assertEqual(
                (scenario_dir / "with_skill" / "response.md").read_text(encoding="utf-8").strip(),
                "skill output",
            )

    def test_main_materializes_external_plan_references_into_response_artifacts(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            benchmark_path = temp_root / "benchmark.json"
            skill_path = temp_root / "skill"
            skill_path.mkdir()
            (skill_path / "SKILL.md").write_text("# placeholder skill\n", encoding="utf-8")

            plan_path = temp_root / "plans" / "captured-plan.md"
            plan_path.parent.mkdir(parents=True)
            plan_path.write_text("# Captured Plan\n\n- RED first\n", encoding="utf-8")

            benchmark_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "demo-scenario",
                            "title": "Demo Scenario",
                            "prompt": "Summarize the copied context.",
                            "assertions": [],
                        }
                    ]
                ),
                encoding="utf-8",
            )

            output_dir = temp_root / "results"
            argv = [
                "run_explicit_skill_benchmark.py",
                "--benchmark",
                str(benchmark_path),
                "--skill-path",
                str(skill_path),
                "--output-dir",
                str(output_dir),
            ]
            pointer_output = f"The plan is available for review at:\n`{plan_path}`"

            with mock.patch.object(module, "run_prompt", side_effect=[pointer_output, pointer_output]):
                with mock.patch.object(sys, "argv", argv):
                    exit_code = module.main()

            self.assertEqual(exit_code, 0)
            scenario_dir = output_dir / "eval-1-demo-scenario"
            self.assertEqual(
                (scenario_dir / "without_skill" / "response.md").read_text(encoding="utf-8").strip(),
                "# Captured Plan\n\n- RED first",
            )
            self.assertEqual(
                (scenario_dir / "with_skill" / "response.md").read_text(encoding="utf-8").strip(),
                "# Captured Plan\n\n- RED first",
            )

    def test_script_runs_end_to_end_with_fake_gemini_cli(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            bin_dir = temp_root / "bin"
            bin_dir.mkdir()

            fake_gemini = bin_dir / "gemini"
            fake_gemini.write_text(
                "\n".join(
                    [
                        "#!/bin/sh",
                        "prompt=''",
                        "while [ \"$#\" -gt 0 ]; do",
                        "  case \"$1\" in",
                        "    -p|--prompt)",
                        "      shift",
                        "      prompt=\"$1\"",
                        "      ;;",
                        "    --output-format|--approval-mode|--model)",
                        "      shift",
                        "      ;;",
                        "  esac",
                        "  shift",
                        "done",
                        "case \"$prompt\" in",
                        "  *\"First read ./skill-under-test/SKILL.md\"*) printf 'skill cli output\\n' ;;",
                        "  *) printf 'baseline cli output\\n' ;;",
                        "esac",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            fake_gemini.chmod(0o755)

            benchmark_path = temp_root / "benchmark.json"
            skill_path = temp_root / "skill"
            skill_path.mkdir()
            (skill_path / "SKILL.md").write_text("# placeholder skill\n", encoding="utf-8")

            context_file = temp_root / "brief.md"
            context_file.write_text("brief context\n", encoding="utf-8")
            benchmark_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "demo-scenario",
                            "title": "Demo Scenario",
                            "prompt": "Summarize the copied context.",
                            "context_files": [str(context_file)],
                            "assertions": [],
                        }
                    ]
                ),
                encoding="utf-8",
            )

            output_dir = temp_root / "results"
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--benchmark",
                    str(benchmark_path),
                    "--skill-path",
                    str(skill_path),
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            run_metadata = json.loads((output_dir / "run_metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(run_metadata["runner"], "gemini")
            events = read_jsonl(output_dir / "execution-observability.jsonl")
            model_usage_events = [event for event in events if event["event_type"] == "model_usage.unavailable"]
            self.assertTrue(model_usage_events)
            self.assertTrue(all(event["usage_source"] == "unavailable" for event in model_usage_events))

            scenario_dir = output_dir / "eval-1-demo-scenario"
            runtime_context = json.loads((scenario_dir / "runtime_context.json").read_text(encoding="utf-8"))
            self.assertEqual(runtime_context["baseline_workspace"], "baseline")
            self.assertEqual(runtime_context["with_skill_workspace"], "with-skill")
            self.assertEqual(runtime_context["copied_skill_path"], "with-skill/skill-under-test/SKILL.md")
            self.assertEqual(
                (scenario_dir / "without_skill" / "response.md").read_text(encoding="utf-8").strip(),
                "baseline cli output",
            )
            self.assertEqual(
                (scenario_dir / "with_skill" / "response.md").read_text(encoding="utf-8").strip(),
                "skill cli output",
            )

    def test_script_runs_end_to_end_with_fake_copilot_cli(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            bin_dir = temp_root / "bin"
            bin_dir.mkdir()

            fake_copilot = bin_dir / "copilot"
            fake_copilot.write_text(
                "\n".join(
                    [
                        "#!/bin/sh",
                        "prompt=''",
                        "while [ \"$#\" -gt 0 ]; do",
                        "  case \"$1\" in",
                        "    -p|--prompt)",
                        "      shift",
                        "      prompt=\"$1\"",
                        "      ;;",
                        "    --stream|--model)",
                        "      shift",
                        "      ;;",
                        "  esac",
                        "  shift",
                        "done",
                        "case \"$prompt\" in",
                        "  *\"First read ./skill-under-test/SKILL.md\"*) printf 'skill cli output\\n\\nTotal usage est:       1 Premium request\\n' ;;",
                        "  *) printf 'baseline cli output\\n\\nTotal usage est:       1 Premium request\\n' ;;",
                        "esac",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            fake_copilot.chmod(0o755)

            benchmark_path = temp_root / "benchmark.json"
            skill_path = temp_root / "skill"
            skill_path.mkdir()
            (skill_path / "SKILL.md").write_text("# placeholder skill\n", encoding="utf-8")

            context_file = temp_root / "brief.md"
            context_file.write_text("brief context\n", encoding="utf-8")
            benchmark_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "demo-scenario",
                            "title": "Demo Scenario",
                            "prompt": "Summarize the copied context.",
                            "context_files": [str(context_file)],
                            "assertions": [],
                        }
                    ]
                ),
                encoding="utf-8",
            )

            output_dir = temp_root / "results"
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--benchmark",
                    str(benchmark_path),
                    "--skill-path",
                    str(skill_path),
                    "--output-dir",
                    str(output_dir),
                    "--runner",
                    "copilot",
                ],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            run_metadata = json.loads((output_dir / "run_metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(run_metadata["runner"], "copilot")

            scenario_dir = output_dir / "eval-1-demo-scenario"
            self.assertEqual(
                (scenario_dir / "without_skill" / "response.md").read_text(encoding="utf-8").strip(),
                "baseline cli output",
            )
            self.assertEqual(
                (scenario_dir / "with_skill" / "response.md").read_text(encoding="utf-8").strip(),
                "skill cli output",
            )


if __name__ == "__main__":
    unittest.main()
