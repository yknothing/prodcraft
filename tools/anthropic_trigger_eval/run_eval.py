#!/usr/bin/env python3
"""Vendored Anthropic trigger evaluation harness for skill descriptions.

This file is intentionally project-owned but upstream-derived: it preserves
Claude-specific trigger-discoverability semantics while keeping execution
reproducible inside the repository.
"""

from __future__ import annotations

import argparse
import json
import os
import select
import subprocess
import sys
import time
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.execution_observability import ExecutionTrace, measure_text_size, new_span_id

try:
    from .utils import parse_skill_md
except ImportError:  # pragma: no cover - direct script execution
    from utils import parse_skill_md


def find_project_root() -> Path:
    """Find the project root by walking up from cwd looking for .claude/."""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / ".claude").is_dir():
            return parent
    return current


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
    observability_output: str | None = None,
) -> bool:
    """Run a single query and return whether the skill was triggered."""
    unique_id = uuid.uuid4().hex[:8]
    clean_name = f"{skill_name}-skill-{unique_id}"
    project_commands_dir = Path(project_root) / ".claude" / "commands"
    command_file = project_commands_dir / f"{clean_name}.md"
    trace = ExecutionTrace(
        output_path=Path(observability_output) if observability_output else None,
        runner="claude",
        model_name=model,
        skill_name=skill_name,
        phase=None,
        workflow="discoverability-eval",
    )
    skill_span_id = new_span_id()
    runner_span_id = new_span_id()
    trace.emit(
        event_type="skill_invocation.started",
        status="started",
        span_id=skill_span_id,
        metadata={"query": query},
    )
    trace.emit(
        event_type="runner_execution.started",
        status="started",
        span_id=runner_span_id,
        parent_span_id=skill_span_id,
        metadata={"query": query, "timeout_ms": timeout * 1000},
    )
    start_time = time.monotonic()

    try:
        project_commands_dir.mkdir(parents=True, exist_ok=True)
        indented_desc = "\n  ".join(skill_description.split("\n"))
        command_content = (
            f"---\n"
            f"description: |\n"
            f"  {indented_desc}\n"
            f"---\n\n"
            f"# {skill_name}\n\n"
            f"This skill handles: {skill_description}\n"
        )
        command_file.write_text(command_content, encoding="utf-8")
        command_size = measure_text_size(command_content)
        trace.emit(
            event_type="skill_context.measured",
            status="completed",
            span_id=new_span_id(),
            parent_span_id=skill_span_id,
            usage_source="unavailable",
            usage_precision="unavailable",
            metadata={
                "query": query,
                "load_stage": "skill_description_command_stub",
                "loaded_file_count": 1,
                "loaded_context_char_count": command_size["char_count"],
                "deferred_context_char_count": 0,
                "available_context_char_count": command_size["char_count"],
                "loaded_context_byte_count": command_size["byte_count"],
                "deferred_context_byte_count": 0,
                "available_context_byte_count": command_size["byte_count"],
                "token_count_status": "unavailable",
                "token_count_reason": "no model-specific tokenizer or provider token-count API was used",
            },
        )

        cmd = [
            "claude",
            "-p",
            query,
            "--output-format",
            "stream-json",
            "--verbose",
            "--include-partial-messages",
        ]
        if model:
            cmd.extend(["--model", model])

        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            cwd=project_root,
            env=env,
        )

        triggered = False
        wall_start = time.time()
        buffer = ""
        pending_tool_name = None
        accumulated_json = ""

        def finalize(result: bool) -> bool:
            duration_ms = int((time.monotonic() - start_time) * 1000)
            trace.emit(
                event_type="model_usage.unavailable",
                status="unavailable",
                span_id=new_span_id(),
                parent_span_id=runner_span_id,
                usage_source="unavailable",
                usage_precision="unavailable",
                metadata={
                    "query": query,
                    "reason": "runner stream did not expose token usage",
                },
            )
            trace.emit(
                event_type="runner_execution.completed",
                status="completed",
                span_id=runner_span_id,
                parent_span_id=skill_span_id,
                duration_ms=duration_ms,
                metadata={"query": query, "triggered": result},
            )
            trace.emit(
                event_type="skill_invocation.completed",
                status="completed",
                span_id=skill_span_id,
                duration_ms=duration_ms,
                metadata={"query": query, "triggered": result},
            )
            return result

        try:
            while time.time() - wall_start < timeout:
                if process.poll() is not None:
                    remaining = process.stdout.read()
                    if remaining:
                        buffer += remaining.decode("utf-8", errors="replace")
                    break

                ready, _, _ = select.select([process.stdout], [], [], 1.0)
                if not ready:
                    continue

                chunk = os.read(process.stdout.fileno(), 8192)
                if not chunk:
                    break
                buffer += chunk.decode("utf-8", errors="replace")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    if event.get("type") == "stream_event":
                        se = event.get("event", {})
                        se_type = se.get("type", "")

                        if se_type == "content_block_start":
                            cb = se.get("content_block", {})
                            if cb.get("type") == "tool_use":
                                tool_name = cb.get("name", "")
                                if tool_name in ("Skill", "Read"):
                                    pending_tool_name = tool_name
                                    accumulated_json = ""
                                else:
                                    return finalize(False)

                        elif se_type == "content_block_delta" and pending_tool_name:
                            delta = se.get("delta", {})
                            if delta.get("type") == "input_json_delta":
                                accumulated_json += delta.get("partial_json", "")
                                if clean_name in accumulated_json:
                                    return finalize(True)

                        elif se_type in ("content_block_stop", "message_stop"):
                            if pending_tool_name:
                                return finalize(clean_name in accumulated_json)
                            if se_type == "message_stop":
                                return finalize(False)

                    elif event.get("type") == "assistant":
                        message = event.get("message", {})
                        for content_item in message.get("content", []):
                            if content_item.get("type") != "tool_use":
                                continue
                            tool_name = content_item.get("name", "")
                            tool_input = content_item.get("input", {})
                            if tool_name == "Skill" and clean_name in tool_input.get("skill", ""):
                                triggered = True
                            elif tool_name == "Read" and clean_name in tool_input.get("file_path", ""):
                                triggered = True
                            return finalize(triggered)

                    elif event.get("type") == "result":
                        return finalize(triggered)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()

        return finalize(triggered)
    finally:
        if command_file.exists():
            command_file.unlink()


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
    observability_output: str | None = None,
) -> dict:
    """Run the full eval set and return results."""
    results = []
    query_triggers: dict[str, list[bool]] = {}
    query_items: dict[str, dict] = {}

    def record_result(item: dict, triggered: bool) -> None:
        query = item["query"]
        query_items[query] = item
        query_triggers.setdefault(query, []).append(triggered)

    if num_workers <= 1:
        for item in eval_set:
            for _run_idx in range(runs_per_query):
                try:
                    triggered = run_single_query(
                        item["query"],
                        skill_name,
                        description,
                        timeout,
                        str(project_root),
                        model,
                        observability_output,
                    )
                except Exception as exc:
                    print(f"Warning: query failed: {exc}", file=sys.stderr)
                    triggered = False
                record_result(item, triggered)
    else:
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            future_to_info = {}
            for item in eval_set:
                for run_idx in range(runs_per_query):
                    future = executor.submit(
                        run_single_query,
                        item["query"],
                        skill_name,
                        description,
                        timeout,
                        str(project_root),
                        model,
                        observability_output,
                    )
                    future_to_info[future] = (item, run_idx)

            for future in as_completed(future_to_info):
                item, _ = future_to_info[future]
                try:
                    triggered = future.result()
                except Exception as exc:
                    print(f"Warning: query failed: {exc}", file=sys.stderr)
                    triggered = False
                record_result(item, triggered)

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        if should_trigger:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        results.append(
            {
                "query": query,
                "should_trigger": should_trigger,
                "trigger_rate": trigger_rate,
                "triggers": sum(triggers),
                "runs": len(triggers),
                "pass": did_pass,
            }
        )

    passed = sum(1 for result in results if result["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Anthropic trigger evaluation for a skill description")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override description to test")
    parser.add_argument("--num-workers", type=int, default=10, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query in seconds")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument("--model", default=None, help="Claude model override for the vendored Anthropic harness")
    parser.add_argument("--observability-output", default=None, help="Optional JSONL path for execution observability events")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text(encoding="utf-8"))
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        return 1

    name, original_description, _content = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root()

    if args.verbose:
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
        observability_output=args.observability_output,
    )

    if args.verbose:
        summary = output["summary"]
        print(f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr)
        for result in output["results"]:
            status = "PASS" if result["pass"] else "FAIL"
            rate_str = f"{result['triggers']}/{result['runs']}"
            print(
                f"  [{status}] rate={rate_str} expected={result['should_trigger']}: {result['query'][:70]}",
                file=sys.stderr,
            )

    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
