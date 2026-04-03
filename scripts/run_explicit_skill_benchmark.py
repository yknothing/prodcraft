#!/usr/bin/env python3
"""Run an explicit-invocation benchmark for a skill using isolated CLI sessions."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.execution_observability import ExecutionTrace, infer_skill_identity, new_span_id


SUPPORTED_RUNNERS = {"claude", "copilot", "gemini"}
GEMINI_PREAMBLE_LINE_PREFIXES = (
    "Loaded cached credentials.",
    "Loading extension:",
    "Registering notification handlers for server ",
    "Server '",
    "[MCP error]",
    "[MCP info]",
    "Scheduling MCP context refresh...",
    "Executing MCP context refresh...",
    "MCP context refresh already in progress",
    "MCP context refresh complete.",
    "Coalescing burst refresh requests",
    "Tool with name ",
    "Skill conflict detected:",
)
GEMINI_PREAMBLE_CONTINUATIONS = ("at ", "code:", "data:", "}",)
GEMINI_INLINE_PREAMBLE_PATTERNS = (
    re.compile(r"^Loaded cached credentials\.\s*"),
    re.compile(r"^MCP issues detected\. Run /mcp list for status\.?"),
    re.compile(r'^Tool with name ".*?" is already registered\. Overwriting\.'),
    re.compile(r'^Skill conflict detected: .*?\.md"\.', re.DOTALL),
)
COPILOT_FOOTER_RE = re.compile(r"\n+Total usage est:.*\Z", re.DOTALL)
LOCAL_ARTIFACT_REFERENCE_RE = re.compile(
    r"(?P<path>/(?:Users|tmp|var/folders)[^\s`]+?\.(?:md|txt))"
)
LOCAL_ARTIFACT_POINTER_CUES = (
    "plan has been saved",
    "plan is available",
    "plan saved in",
    "plan saved to",
    "saved it to",
    "find the plan saved in",
    "find the plan saved to",
    "saved to `",
    "saved in `",
)
GEMINI_TEMP_PATH_RE = re.compile(
    r"/Users/[^/\s`]+/.gemini/tmp/[^/\s`]+/[^/\s`]+(?P<tail>/[^\s`]+)"
)
MACOS_TEMP_PATH_RE = re.compile(r"/var/folders/[^\s`]+")
TMP_PATH_RE = re.compile(r"/tmp/[^\s`]+")


def build_prompt_command(runner: str, prompt: str, model: str | None) -> list[str]:
    if runner == "gemini":
        cmd = [
            "gemini",
            "-p",
            prompt,
            "--output-format",
            "text",
            "--approval-mode",
            "plan",
        ]
    elif runner == "claude":
        cmd = [
            "claude",
            "-p",
            prompt,
            "--output-format",
            "text",
            "--permission-mode",
            "bypassPermissions",
            "--tools",
            "Read",
        ]
    elif runner == "copilot":
        cmd = [
            "copilot",
            "-p",
            prompt,
            "--allow-all-tools",
            "--allow-all-paths",
            "--disable-builtin-mcps",
            "--stream",
            "off",
            "--no-custom-instructions",
        ]
    else:
        raise ValueError(f"Unsupported runner: {runner}")

    if model:
        cmd.extend(["--model", model])
    return cmd


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path.resolve())


def resolve_context_file(item: str, benchmark_path: Path) -> Path:
    candidate = Path(item)
    if candidate.is_absolute():
        return candidate.resolve()
    return (benchmark_path.parent / candidate).resolve()


def sanitize_runner_output(runner: str, output: str) -> str:
    text = output.strip()
    if not text:
        return text

    if runner == "copilot":
        text = COPILOT_FOOTER_RE.sub("", text).strip()
        return text

    if runner != "gemini":
        return text

    lines = text.splitlines()
    cleaned: list[str] = []
    skipping_preamble = True

    for line in lines:
        candidate = line
        if skipping_preamble:
            stripped = candidate.lstrip()
            if not stripped:
                continue
            while True:
                updated = candidate
                for pattern in GEMINI_INLINE_PREAMBLE_PATTERNS:
                    updated = pattern.sub("", updated, count=1)
                if updated == candidate:
                    break
                candidate = updated.lstrip()
            stripped = candidate.lstrip()
            if not stripped:
                continue
            if stripped.startswith(GEMINI_PREAMBLE_LINE_PREFIXES) or stripped.startswith(GEMINI_PREAMBLE_CONTINUATIONS):
                continue
            skipping_preamble = False
        cleaned.append(candidate)

    return "\n".join(cleaned).strip()


def sanitize_machine_specific_paths(text: str) -> str:
    text = GEMINI_TEMP_PATH_RE.sub(r"<gemini-temp-workspace>\g<tail>", text)
    text = MACOS_TEMP_PATH_RE.sub("<macos-temp-path>", text)
    text = TMP_PATH_RE.sub("<tmp-path>", text)
    return text


def is_allowed_local_artifact_path(path: Path) -> bool:
    allowed_roots = (
        Path.home() / ".gemini" / "tmp",
        Path("/tmp"),
        Path("/private/tmp"),
        Path("/var/folders"),
        Path("/private/var/folders"),
    )
    for root in allowed_roots:
        try:
            path.relative_to(root)
            return True
        except ValueError:
            continue
    return False


def maybe_materialize_local_artifact(output: str) -> str:
    normalized = output.strip()
    if not normalized:
        return normalized

    lowered = normalized.lower()
    if not any(cue in lowered for cue in LOCAL_ARTIFACT_POINTER_CUES):
        return sanitize_machine_specific_paths(normalized)

    for match in LOCAL_ARTIFACT_REFERENCE_RE.finditer(normalized):
        candidate = Path(match.group("path"))
        if candidate.suffix.lower() not in {".md", ".txt"}:
            continue
        if not candidate.exists() or not candidate.is_file():
            continue
        resolved = candidate.resolve()
        if not is_allowed_local_artifact_path(resolved):
            continue
        materialized = candidate.read_text(encoding="utf-8").strip()
        if materialized:
            return sanitize_machine_specific_paths(materialized)

    return sanitize_machine_specific_paths(normalized)


def run_prompt(prompt: str, runner: str, model: str | None, cwd: Path, timeout_seconds: int) -> str:
    cmd = build_prompt_command(runner, prompt, model)
    env = os.environ.copy()
    if runner == "claude":
        env.pop("CLAUDECODE", None)

    max_attempts = 4
    base_delay = 5.0
    
    for attempt in range(1, max_attempts + 1):
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
            env=env,
        )
        try:
            stdout, stderr = process.communicate(timeout=timeout_seconds)
            if process.returncode == 0:
                return sanitize_runner_output(runner, stdout)
                
            combined_output = stdout + "\n" + stderr
            is_transient = (
                "429" in combined_output or 
                "RESOURCE_EXHAUSTED" in combined_output or 
                "ECONNRESET" in combined_output or
                "Connection error." in combined_output or
                "Connection error" in combined_output or
                "worker_failed" in combined_output or
                "Premature close" in combined_output or
                "socket hang up" in combined_output or
                "ERR_STREAM_PREMATURE_CLOSE" in combined_output
            )
            
            if is_transient and attempt < max_attempts:
                print(f"Attempt {attempt} failed with transient error, retrying in {base_delay}s...", file=sys.stderr)
                time.sleep(base_delay)
                base_delay *= 2
                continue
                
            raise subprocess.CalledProcessError(
                returncode=process.returncode,
                cmd=cmd,
                output=stdout,
                stderr=stderr,
            )
            
        except subprocess.TimeoutExpired as exc:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
            if attempt < max_attempts:
                print(f"Attempt {attempt} timed out, retrying in {base_delay}s...", file=sys.stderr)
                time.sleep(base_delay)
                base_delay *= 2
                continue
            raise subprocess.TimeoutExpired(
                cmd=exc.cmd,
                timeout=timeout_seconds,
                output=exc.output,
                stderr=exc.stderr,
            ) from exc

    # Should not reach here
    raise RuntimeError("Retry loop exhausted without returning or raising.")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n")


def append_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(content.rstrip() + "\n")


def run_case(
    *,
    prompt: str,
    runner: str,
    model: str | None,
    timeout_seconds: int,
    cwd: Path,
    result_dir: Path,
    observability_output: Path,
    branch_label: str,
    scenario_id: str,
    skill_name: str | None = None,
    phase: str | None = None,
) -> None:
    trace = ExecutionTrace(
        output_path=observability_output,
        runner=runner,
        model_name=model,
        skill_name=skill_name,
        phase=phase,
        workflow=None,
    )
    skill_span_id = None
    if skill_name:
        skill_span_id = new_span_id()
        trace.emit(
            event_type="skill_invocation.started",
            status="started",
            span_id=skill_span_id,
            metadata={"branch": branch_label, "scenario_id": scenario_id},
        )

    runner_span_id = new_span_id()
    trace.emit(
        event_type="runner_execution.started",
        status="started",
        span_id=runner_span_id,
        parent_span_id=skill_span_id,
        metadata={"branch": branch_label, "scenario_id": scenario_id, "timeout_ms": timeout_seconds * 1000},
    )
    start_time = time.monotonic()
    try:
        output = run_prompt(
            prompt,
            runner=runner,
            model=model,
            cwd=cwd,
            timeout_seconds=timeout_seconds,
        )
        output = maybe_materialize_local_artifact(output)
        response_path = result_dir / "response.md"
        write_text(response_path, output)
        duration_ms = int((time.monotonic() - start_time) * 1000)
        trace.emit(
            event_type="model_usage.unavailable",
            status="unavailable",
            span_id=new_span_id(),
            parent_span_id=runner_span_id,
            artifact_path=display_path(response_path),
            usage_source="unavailable",
            metadata={
                "branch": branch_label,
                "scenario_id": scenario_id,
                "reason": "runner output did not expose token usage",
            },
        )
        trace.emit(
            event_type="runner_execution.completed",
            status="completed",
            span_id=runner_span_id,
            parent_span_id=skill_span_id,
            duration_ms=duration_ms,
            artifact_path=display_path(response_path),
            metadata={"branch": branch_label, "scenario_id": scenario_id},
        )
        if skill_span_id:
            trace.emit(
                event_type="skill_invocation.completed",
                status="completed",
                span_id=skill_span_id,
                duration_ms=duration_ms,
                artifact_path=display_path(response_path),
                metadata={"branch": branch_label, "scenario_id": scenario_id},
            )
    except subprocess.TimeoutExpired:
        error_path = result_dir / "error.txt"
        write_text(error_path, f"Timed out after {timeout_seconds}s")
        duration_ms = int((time.monotonic() - start_time) * 1000)
        trace.emit(
            event_type="model_usage.unavailable",
            status="unavailable",
            span_id=new_span_id(),
            parent_span_id=runner_span_id,
            artifact_path=display_path(error_path),
            usage_source="unavailable",
            metadata={
                "branch": branch_label,
                "scenario_id": scenario_id,
                "reason": "runner timed out before usage could be recorded",
            },
        )
        trace.emit(
            event_type="runner_execution.failed",
            status="failed",
            span_id=runner_span_id,
            parent_span_id=skill_span_id,
            duration_ms=duration_ms,
            artifact_path=display_path(error_path),
            metadata={
                "branch": branch_label,
                "scenario_id": scenario_id,
                "error_type": "timeout",
                "timeout_ms": timeout_seconds * 1000,
            },
        )
        if skill_span_id:
            trace.emit(
                event_type="skill_invocation.failed",
                status="failed",
                span_id=skill_span_id,
                duration_ms=duration_ms,
                artifact_path=display_path(error_path),
                metadata={"branch": branch_label, "scenario_id": scenario_id, "error_type": "timeout"},
            )
    except subprocess.CalledProcessError as exc:
        error_path = result_dir / "error.txt"
        write_text(
            error_path,
            f"Exit code: {exc.returncode}\nSTDERR:\n{exc.stderr}\nSTDOUT:\n{exc.stdout}",
        )
        duration_ms = int((time.monotonic() - start_time) * 1000)
        trace.emit(
            event_type="model_usage.unavailable",
            status="unavailable",
            span_id=new_span_id(),
            parent_span_id=runner_span_id,
            artifact_path=display_path(error_path),
            usage_source="unavailable",
            metadata={
                "branch": branch_label,
                "scenario_id": scenario_id,
                "reason": "runner exited with non-zero status before usage could be recorded",
            },
        )
        trace.emit(
            event_type="runner_execution.failed",
            status="failed",
            span_id=runner_span_id,
            parent_span_id=skill_span_id,
            duration_ms=duration_ms,
            artifact_path=display_path(error_path),
            metadata={
                "branch": branch_label,
                "scenario_id": scenario_id,
                "error_type": "called_process_error",
                "returncode": exc.returncode,
            },
        )
        if skill_span_id:
            trace.emit(
                event_type="skill_invocation.failed",
                status="failed",
                span_id=skill_span_id,
                duration_ms=duration_ms,
                artifact_path=display_path(error_path),
                metadata={
                    "branch": branch_label,
                    "scenario_id": scenario_id,
                    "error_type": "called_process_error",
                    "returncode": exc.returncode,
                },
            )


def copy_context_files(
    context_files: list[str],
    target_dir: Path,
    benchmark_path: Path,
    workspace_label: str,
) -> list[str]:
    copied = []
    for item in context_files:
        source = resolve_context_file(item, benchmark_path)
        destination = target_dir / source.name
        if not source.exists():
            raise FileNotFoundError(f"context file not found: {source}")
        shutil.copy2(source, destination)
        copied.append(f"{workspace_label}/{source.name}")
    return copied


def main() -> int:
    parser = argparse.ArgumentParser(description="Run an explicit-invocation benchmark for a skill.")
    parser.add_argument("--benchmark", required=True, help="Path to benchmark JSON.")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory containing SKILL.md.")
    parser.add_argument("--output-dir", required=True, help="Directory to write benchmark outputs.")
    parser.add_argument(
        "--runner",
        choices=sorted(SUPPORTED_RUNNERS),
        default="gemini",
        help="CLI runner to invoke for each benchmark prompt. Defaults to gemini.",
    )
    parser.add_argument("--model", default=None, help="Optional model override for the selected runner.")
    parser.add_argument("--timeout-seconds", type=int, default=120, help="Per-prompt timeout for the selected CLI runner.")
    parser.add_argument("--scenario-id", default=None, help="Optional single scenario id to run.")
    args = parser.parse_args()

    benchmark_path = Path(args.benchmark).resolve()
    skill_path = Path(args.skill_path).resolve()
    output_dir = Path(args.output_dir).resolve()

    if not (skill_path / "SKILL.md").exists():
        raise SystemExit(f"No SKILL.md found at {skill_path}")

    scenarios = json.loads(benchmark_path.read_text())
    if args.scenario_id:
        scenarios = [scenario for scenario in scenarios if scenario["id"] == args.scenario_id]
        if not scenarios:
            raise SystemExit(f"No scenario matched --scenario-id={args.scenario_id}")
    timestamp = datetime.now().isoformat(timespec="seconds")

    write_text(
        output_dir / "run_metadata.json",
        json.dumps(
            {
                "benchmark": display_path(benchmark_path),
                "skill_path": display_path(skill_path),
                "runner": args.runner,
                "model": args.model,
                "run_started_at": timestamp,
                "scenario_count": len(scenarios),
            },
            indent=2,
        ),
    )
    progress_log = output_dir / "progress.log"
    observability_output = output_dir / "execution-observability.jsonl"
    skill_name, phase = infer_skill_identity(skill_path)

    for index, scenario in enumerate(scenarios, start=1):
        scenario_dir = output_dir / f"eval-{index}-{scenario['id']}"
        write_text(scenario_dir / "eval_metadata.json", json.dumps(scenario, indent=2, ensure_ascii=False))
        with tempfile.TemporaryDirectory(prefix=f"prodcraft-explicit-benchmark-{scenario['id']}-") as tmpdir:
            temp_root = Path(tmpdir)
            baseline_dir = temp_root / "baseline"
            with_skill_dir = temp_root / "with-skill"
            baseline_dir.mkdir(parents=True, exist_ok=True)
            with_skill_dir.mkdir(parents=True, exist_ok=True)
            isolated_skill_dir = with_skill_dir / "skill-under-test"
            shutil.copytree(skill_path, isolated_skill_dir, dirs_exist_ok=True)
            context_files = scenario.get("context_files", [])
            copied_baseline_context = copy_context_files(
                context_files,
                baseline_dir,
                benchmark_path,
                "baseline",
            )
            copied_with_skill_context = copy_context_files(
                context_files,
                with_skill_dir,
                benchmark_path,
                "with-skill",
            )

            baseline_prompt = (
                "Work only from the request below. Do not read any local files or rely on repository instructions. "
                "If you need assumptions, state them briefly and continue.\n\n"
                f"{scenario['prompt']}"
            )
            with_skill_prompt = (
                "First read ./skill-under-test/SKILL.md, then answer the request below using that skill. "
                "Do not read any other local files or rely on repository instructions beyond the copied skill. "
                "If you need assumptions, state them briefly and continue.\n\n"
                f"{scenario['prompt']}"
            )

            write_text(scenario_dir / "without_skill" / "prompt.txt", baseline_prompt)
            write_text(scenario_dir / "with_skill" / "prompt.txt", with_skill_prompt)
            write_text(
                scenario_dir / "runtime_context.json",
                json.dumps(
                    {
                        "baseline_workspace": "baseline",
                        "with_skill_workspace": "with-skill",
                        "copied_skill_path": "with-skill/skill-under-test/SKILL.md",
                        "baseline_context_files": copied_baseline_context,
                        "with_skill_context_files": copied_with_skill_context,
                        "isolation_mode": "tempdir-outside-repo",
                    },
                    indent=2,
                ),
            )

            append_text(progress_log, f"running {scenario['id']} without_skill")
            run_case(
                prompt=baseline_prompt,
                runner=args.runner,
                model=args.model,
                timeout_seconds=args.timeout_seconds,
                cwd=baseline_dir,
                result_dir=scenario_dir / "without_skill",
                observability_output=observability_output,
                branch_label="without_skill",
                scenario_id=scenario["id"],
            )

            append_text(progress_log, f"running {scenario['id']} with_skill")
            run_case(
                prompt=with_skill_prompt,
                runner=args.runner,
                model=args.model,
                timeout_seconds=args.timeout_seconds,
                cwd=with_skill_dir,
                result_dir=scenario_dir / "with_skill",
                observability_output=observability_output,
                branch_label="with_skill",
                scenario_id=scenario["id"],
                skill_name=skill_name,
                phase=phase,
            )

            append_text(progress_log, f"completed {scenario['id']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
