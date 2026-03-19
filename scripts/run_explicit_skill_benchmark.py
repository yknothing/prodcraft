#!/usr/bin/env python3
"""Run an explicit-invocation benchmark for a skill using isolated CLI sessions."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path


SUPPORTED_RUNNERS = {"claude", "gemini"}


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
    else:
        raise ValueError(f"Unsupported runner: {runner}")

    if model:
        cmd.extend(["--model", model])
    return cmd


def run_prompt(prompt: str, runner: str, model: str | None, cwd: Path, timeout_seconds: int) -> str:
    cmd = build_prompt_command(runner, prompt, model)
    env = os.environ.copy()
    if runner == "claude":
        env.pop("CLAUDECODE", None)

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
    except subprocess.TimeoutExpired as exc:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait()
        raise subprocess.TimeoutExpired(
            cmd=exc.cmd,
            timeout=timeout_seconds,
            output=exc.output,
            stderr=exc.stderr,
        ) from exc

    if process.returncode != 0:
        raise subprocess.CalledProcessError(
            returncode=process.returncode,
            cmd=cmd,
            output=stdout,
            stderr=stderr,
        )

    return stdout.strip()


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
) -> None:
    try:
        output = run_prompt(
            prompt,
            runner=runner,
            model=model,
            cwd=cwd,
            timeout_seconds=timeout_seconds,
        )
        write_text(result_dir / "response.md", output)
    except subprocess.TimeoutExpired:
        write_text(result_dir / "error.txt", f"Timed out after {timeout_seconds}s")
    except subprocess.CalledProcessError as exc:
        write_text(
            result_dir / "error.txt",
            f"Exit code: {exc.returncode}\nSTDERR:\n{exc.stderr}\nSTDOUT:\n{exc.stdout}",
        )


def copy_context_files(context_files: list[str], target_dir: Path) -> list[str]:
    copied = []
    for item in context_files:
        source = Path(item).resolve()
        destination = target_dir / source.name
        if not source.exists():
            raise FileNotFoundError(f"context file not found: {source}")
        shutil.copy2(source, destination)
        copied.append(str(destination))
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
                "benchmark": str(benchmark_path),
                "skill_path": str(skill_path),
                "runner": args.runner,
                "model": args.model,
                "run_started_at": timestamp,
                "scenario_count": len(scenarios),
            },
            indent=2,
        ),
    )
    progress_log = output_dir / "progress.log"

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
            copied_baseline_context = copy_context_files(context_files, baseline_dir)
            copied_with_skill_context = copy_context_files(context_files, with_skill_dir)

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
                        "baseline_cwd": str(baseline_dir),
                        "with_skill_cwd": str(with_skill_dir),
                        "copied_skill_path": str(isolated_skill_dir / "SKILL.md"),
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
            )

            append_text(progress_log, f"running {scenario['id']} with_skill")
            run_case(
                prompt=with_skill_prompt,
                runner=args.runner,
                model=args.model,
                timeout_seconds=args.timeout_seconds,
                cwd=with_skill_dir,
                result_dir=scenario_dir / "with_skill",
            )

            append_text(progress_log, f"completed {scenario['id']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
