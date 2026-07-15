#!/usr/bin/env python3
"""Run an explicit-invocation benchmark for a skill using isolated CLI sessions."""

from __future__ import annotations

import argparse
import hashlib
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

from tools.execution_observability import (  # noqa: E402
    ExecutionTrace,
    infer_skill_identity,
    measure_skill_context,
    new_span_id,
)
from tools.model_usage_normalization import (  # noqa: E402
    COPILOT_FOOTER_RE,
    normalize_copilot_footer_usage,
    normalize_runner_usage,
)


SUPPORTED_RUNNERS = {"claude", "codex", "copilot", "gemini"}
CODEX_HOME_FORBIDDEN_PATH_FRAGMENT = "systematic-debugging"
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


def parse_copilot_usage(output: str) -> dict[str, int | str] | None:
    return normalize_copilot_footer_usage(output)


def parse_runner_usage(runner: str, output: str) -> dict[str, int | str] | None:
    return normalize_runner_usage(runner, output)


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_text(content: str) -> str:
    return sha256_bytes(content.encode("utf-8"))


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def codex_home_isolation_metadata() -> dict[str, object]:
    return {
        "mode": "per-case-temporary-auth-only",
        "auth_exposure": "auth.json-symlink",
        "source_user_config_loaded": False,
        "forbidden_path_fragment": CODEX_HOME_FORBIDDEN_PATH_FRAGMENT,
        "preflight_forbidden_path_matches": 0,
        "postflight_forbidden_path_matches": 0,
        "cleanup": "automatic-after-each-case",
    }


def assert_codex_home_has_no_forbidden_paths(home: Path, stage: str) -> None:
    forbidden_matches = [
        path
        for path in home.rglob("*")
        if CODEX_HOME_FORBIDDEN_PATH_FRAGMENT in str(path)
    ]
    if forbidden_matches:
        relative_matches = [str(path.relative_to(home)) for path in forbidden_matches]
        raise OSError(
            f"{stage} isolated codex home contains forbidden "
            f"{CODEX_HOME_FORBIDDEN_PATH_FRAGMENT} paths: {relative_matches}"
        )


def create_isolated_codex_home(cwd: Path) -> Path:
    source_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    source_auth = source_home / "auth.json"
    if not source_auth.is_file():
        raise OSError("codex auth.json is unavailable for isolated evaluator home")

    isolated_home = Path(
        tempfile.mkdtemp(prefix=".codex-home-auth-only-", dir=cwd.parent)
    )
    try:
        (isolated_home / "auth.json").symlink_to(source_auth.resolve())
        assert_codex_home_has_no_forbidden_paths(isolated_home, "preflight")
    except Exception:
        shutil.rmtree(isolated_home, ignore_errors=True)
        raise
    return isolated_home


def build_prompt_command(
    runner: str,
    prompt: str,
    model: str | None,
    *,
    cwd: Path | None = None,
    response_file: Path | None = None,
) -> list[str]:
    if runner == "gemini":
        cmd = [
            "gemini",
            "-p",
            prompt,
            "--output-format",
            "text",
            "--approval-mode",
            "plan",
            "--extensions",
            "none",
            "--allowed-mcp-server-names",
            "none",
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
    elif runner == "codex":
        if cwd is None or response_file is None:
            raise ValueError("codex runner requires cwd and response_file")
        cmd = [
            "codex",
            "exec",
            "--ignore-user-config",
            "--ephemeral",
            "--sandbox",
            "read-only",
            "--skip-git-repo-check",
            "-C",
            str(cwd),
        ]
        if model:
            cmd.extend(["-m", model])
        cmd.extend(["-o", str(response_file), "-"])
        return cmd
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


def run_prompt_with_usage(
    prompt: str,
    runner: str,
    model: str | None,
    cwd: Path,
    timeout_seconds: int,
) -> tuple[str, dict | None]:
    if runner != "codex":
        return _run_prompt_with_usage_in_environment(
            prompt,
            runner,
            model,
            cwd,
            timeout_seconds,
            isolated_codex_home=None,
        )

    isolated_codex_home = create_isolated_codex_home(cwd)
    try:
        result = _run_prompt_with_usage_in_environment(
            prompt,
            runner,
            model,
            cwd,
            timeout_seconds,
            isolated_codex_home=isolated_codex_home,
        )
        assert_codex_home_has_no_forbidden_paths(isolated_codex_home, "postflight")
        return result
    finally:
        shutil.rmtree(isolated_codex_home, ignore_errors=True)


def _run_prompt_with_usage_in_environment(
    prompt: str,
    runner: str,
    model: str | None,
    cwd: Path,
    timeout_seconds: int,
    *,
    isolated_codex_home: Path | None,
) -> tuple[str, dict | None]:
    response_file = cwd / ".codex-final-response.txt" if runner == "codex" else None
    cmd = build_prompt_command(
        runner,
        prompt,
        model,
        cwd=cwd,
        response_file=response_file,
    )
    env = os.environ.copy()
    if runner == "claude":
        env.pop("CLAUDECODE", None)
    if isolated_codex_home is not None:
        env["CODEX_HOME"] = str(isolated_codex_home)

    max_attempts = 4
    base_delay = 5.0
    
    for attempt in range(1, max_attempts + 1):
        if response_file is not None:
            response_file.unlink(missing_ok=True)
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            text=True,
            stdin=subprocess.PIPE if runner == "codex" else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
            env=env,
        )
        try:
            if runner == "codex":
                stdout, stderr = process.communicate(input=prompt, timeout=timeout_seconds)
            else:
                stdout, stderr = process.communicate(timeout=timeout_seconds)
            if process.returncode == 0:
                if response_file is not None:
                    response = response_file.read_text(encoding="utf-8")
                    if not response.strip():
                        raise OSError("codex runner produced an empty final response file")
                    response_file.unlink(missing_ok=True)
                    return response.strip(), parse_runner_usage(runner, stdout)
                return sanitize_runner_output(runner, stdout), parse_runner_usage(runner, stdout)
                
            combined_output = stdout + "\n" + stderr
            empty_failure = not stdout.strip() and not stderr.strip()
            is_transient = (
                "429" in combined_output or 
                "RESOURCE_EXHAUSTED" in combined_output or 
                "ECONNRESET" in combined_output or
                "fetch failed" in combined_output or
                "Connection error." in combined_output or
                "Connection error" in combined_output or
                "worker_failed" in combined_output or
                "Premature close" in combined_output or
                "socket hang up" in combined_output or
                "ERR_STREAM_PREMATURE_CLOSE" in combined_output or
                empty_failure
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


def run_prompt(prompt: str, runner: str, model: str | None, cwd: Path, timeout_seconds: int) -> str:
    output, _usage = run_prompt_with_usage(prompt, runner, model, cwd, timeout_seconds)
    return output


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
    run_number: int = 1,
    output_root: Path | None = None,
    skill_name: str | None = None,
    phase: str | None = None,
    skill_context: dict[str, object] | None = None,
) -> dict[str, object]:
    trace = ExecutionTrace(
        output_path=observability_output,
        runner=runner,
        model_name=model,
        skill_name=skill_name,
        phase=phase,
        workflow=None,
    )
    case_metadata = {
        "branch": branch_label,
        "scenario_id": scenario_id,
        "run_number": run_number,
    }
    skill_span_id = None
    if skill_name:
        skill_span_id = new_span_id()
        trace.emit(
            event_type="skill_invocation.started",
            status="started",
            span_id=skill_span_id,
            metadata=case_metadata,
        )
        if skill_context:
            skill_file_chars = skill_context.get("skill_file_char_count")
            supporting_chars = skill_context.get("supporting_context_char_count")
            skill_file_bytes = skill_context.get("skill_file_byte_count")
            supporting_bytes = skill_context.get("supporting_context_byte_count")
            if (
                isinstance(skill_file_chars, int)
                and isinstance(supporting_chars, int)
                and isinstance(skill_file_bytes, int)
                and isinstance(supporting_bytes, int)
            ):
                loaded_chars = skill_file_chars
                deferred_chars = supporting_chars
                total_available_chars = loaded_chars + deferred_chars
                loaded_bytes = skill_file_bytes
                deferred_bytes = supporting_bytes
                total_available_bytes = loaded_bytes + deferred_bytes
            else:
                loaded_chars = None
                deferred_chars = None
                total_available_chars = None
                loaded_bytes = None
                deferred_bytes = None
                total_available_bytes = None

            trace.emit(
                event_type="skill_context.measured",
                status="completed",
                span_id=new_span_id(),
                parent_span_id=skill_span_id,
                usage_source="unavailable",
                usage_precision="unavailable",
                metadata={
                    **case_metadata,
                    "load_stage": "skill_body",
                    "loaded_file_count": 1,
                    "loaded_context_char_count": loaded_chars,
                    "deferred_context_char_count": deferred_chars,
                    "available_context_char_count": total_available_chars,
                    "loaded_context_byte_count": loaded_bytes,
                    "deferred_context_byte_count": deferred_bytes,
                    "available_context_byte_count": total_available_bytes,
                    "skill_metadata_char_count": skill_context.get("skill_metadata_char_count"),
                    "skill_body_char_count": skill_context.get("skill_body_char_count"),
                    "skill_frontmatter_char_count": skill_context.get("skill_frontmatter_char_count"),
                    "skill_metadata_byte_count": skill_context.get("skill_metadata_byte_count"),
                    "skill_body_byte_count": skill_context.get("skill_body_byte_count"),
                    "skill_frontmatter_byte_count": skill_context.get("skill_frontmatter_byte_count"),
                    "supporting_context_file_count": skill_context.get("supporting_context_file_count"),
                    "token_count_status": skill_context.get("token_count_status"),
                    "token_count_reason": skill_context.get("token_count_reason"),
                    "skill_file_sha256": skill_context.get("skill_file_sha256"),
                },
            )

    runner_span_id = new_span_id()
    trace.emit(
        event_type="runner_execution.started",
        status="started",
        span_id=runner_span_id,
        parent_span_id=skill_span_id,
        metadata={**case_metadata, "timeout_ms": timeout_seconds * 1000},
    )
    start_time = time.monotonic()
    try:
        output, usage = run_prompt_with_usage(
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
        if usage:
            usage_model_name = usage.get("model_name")
            trace.emit(
                event_type="model_usage.completed",
                status="completed",
                span_id=new_span_id(),
                parent_span_id=runner_span_id,
                artifact_path=display_path(response_path),
                model_name=str(usage_model_name) if usage_model_name else None,
                token_input=int(usage["token_input"]),
                token_output=int(usage["token_output"]),
                token_total=int(usage["token_total"]),
                token_cache_read_input=int(usage.get("token_cache_read_input", 0)),
                token_cache_write_input=int(usage.get("token_cache_write_input", 0)),
                usage_source=str(usage["usage_source"]),
                usage_precision=str(usage.get("usage_precision") or "unknown"),
                metadata={
                    **case_metadata,
                    "usage_note": "runner-reported aggregate; precision is recorded separately and estimated usage is excluded from exact summaries",
                },
            )
        else:
            trace.emit(
                event_type="model_usage.unavailable",
                status="unavailable",
                span_id=new_span_id(),
                parent_span_id=runner_span_id,
                artifact_path=display_path(response_path),
                usage_source="unavailable",
                usage_precision="unavailable",
                metadata={
                    **case_metadata,
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
            metadata=case_metadata,
        )
        if skill_span_id:
            trace.emit(
                event_type="skill_invocation.completed",
                status="completed",
                span_id=skill_span_id,
                duration_ms=duration_ms,
                artifact_path=display_path(response_path),
                metadata=case_metadata,
            )
        artifact_path = (
            str(response_path.relative_to(output_root))
            if output_root is not None
            else display_path(response_path)
        )
        return {
            **case_metadata,
            "arm": branch_label,
            "status": "completed",
            "prompt_sha256": sha256_text(prompt),
            "artifact_path": artifact_path,
            "artifact_sha256": sha256_file(response_path),
        }
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
            usage_precision="unavailable",
            metadata={
                **case_metadata,
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
                **case_metadata,
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
                metadata={**case_metadata, "error_type": "timeout"},
            )
        artifact_path = (
            str(error_path.relative_to(output_root))
            if output_root is not None
            else display_path(error_path)
        )
        return {
            **case_metadata,
            "arm": branch_label,
            "status": "failed",
            "error_type": "timeout",
            "prompt_sha256": sha256_text(prompt),
            "artifact_path": artifact_path,
            "artifact_sha256": sha256_file(error_path),
        }
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
            usage_precision="unavailable",
            metadata={
                **case_metadata,
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
                **case_metadata,
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
                    **case_metadata,
                    "error_type": "called_process_error",
                    "returncode": exc.returncode,
                },
            )
        artifact_path = (
            str(error_path.relative_to(output_root))
            if output_root is not None
            else display_path(error_path)
        )
        return {
            **case_metadata,
            "arm": branch_label,
            "status": "failed",
            "error_type": "called_process_error",
            "returncode": exc.returncode,
            "prompt_sha256": sha256_text(prompt),
            "artifact_path": artifact_path,
            "artifact_sha256": sha256_file(error_path),
        }
    except OSError as exc:
        error_path = result_dir / "error.txt"
        write_text(error_path, f"{type(exc).__name__}: {exc}")
        duration_ms = int((time.monotonic() - start_time) * 1000)
        trace.emit(
            event_type="model_usage.unavailable",
            status="unavailable",
            span_id=new_span_id(),
            parent_span_id=runner_span_id,
            artifact_path=display_path(error_path),
            usage_source="unavailable",
            usage_precision="unavailable",
            metadata={**case_metadata, "reason": "runner could not be started"},
        )
        trace.emit(
            event_type="runner_execution.failed",
            status="failed",
            span_id=runner_span_id,
            parent_span_id=skill_span_id,
            duration_ms=duration_ms,
            artifact_path=display_path(error_path),
            metadata={**case_metadata, "error_type": "os_error"},
        )
        if skill_span_id:
            trace.emit(
                event_type="skill_invocation.failed",
                status="failed",
                span_id=skill_span_id,
                duration_ms=duration_ms,
                artifact_path=display_path(error_path),
                metadata={**case_metadata, "error_type": "os_error"},
            )
        artifact_path = (
            str(error_path.relative_to(output_root))
            if output_root is not None
            else display_path(error_path)
        )
        return {
            **case_metadata,
            "arm": branch_label,
            "status": "failed",
            "error_type": "os_error",
            "prompt_sha256": sha256_text(prompt),
            "artifact_path": artifact_path,
            "artifact_sha256": sha256_file(error_path),
        }


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
    parser.add_argument(
        "--runs-per-scenario",
        type=int,
        default=1,
        help="Independent runs to execute for each scenario and arm. Defaults to 1.",
    )
    args = parser.parse_args()

    if args.runs_per_scenario < 1:
        raise SystemExit("--runs-per-scenario must be at least 1")

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
    skill_name, phase = infer_skill_identity(skill_path)
    skill_context = measure_skill_context(skill_path)
    benchmark_sha256 = sha256_file(benchmark_path)
    skill_file_sha256 = sha256_file(skill_path / "SKILL.md")
    runner_home_isolation = (
        codex_home_isolation_metadata() if args.runner == "codex" else None
    )

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
                "runs_per_scenario": args.runs_per_scenario,
                "expected_case_count": len(scenarios) * args.runs_per_scenario * 2,
                "benchmark_sha256": benchmark_sha256,
                "skill_file_sha256": skill_file_sha256,
                "runner_home_isolation": runner_home_isolation,
            },
            indent=2,
        ),
    )
    progress_log = output_dir / "progress.log"
    observability_output = output_dir / "execution-observability.jsonl"
    case_records: list[dict[str, object]] = []

    for index, scenario in enumerate(scenarios, start=1):
        scenario_dir = output_dir / f"eval-{index}-{scenario['id']}"
        write_text(scenario_dir / "eval_metadata.json", json.dumps(scenario, indent=2, ensure_ascii=False))
        for run_number in range(1, args.runs_per_scenario + 1):
            case_dir = (
                scenario_dir
                if args.runs_per_scenario == 1
                else scenario_dir / f"run-{run_number}"
            )
            with tempfile.TemporaryDirectory(
                prefix=f"prodcraft-explicit-benchmark-{scenario['id']}-run-{run_number}-"
            ) as tmpdir:
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
                    "Work only from the request below and copied benchmark context files explicitly named in it. "
                    "You may read those copied context files. Do not read repository instructions, neighboring skills, "
                    "or unrelated local files. If you need assumptions, state them briefly and continue.\n\n"
                    f"{scenario['prompt']}"
                )
                with_skill_prompt = (
                    "First read ./skill-under-test/SKILL.md, then answer the request below using that skill. "
                    "You may read copied benchmark context files explicitly named in the request and resources under "
                    "./skill-under-test/references/ when the copied skill directs you there. Do not read repository "
                    "instructions, neighboring skills, or unrelated local files. If you need assumptions, state them "
                    "briefly and continue.\n\n"
                    f"{scenario['prompt']}"
                )

                write_text(case_dir / "without_skill" / "prompt.txt", baseline_prompt)
                write_text(case_dir / "with_skill" / "prompt.txt", with_skill_prompt)
                write_text(
                    case_dir / "runtime_context.json",
                    json.dumps(
                        {
                            "run_number": run_number,
                            "baseline_workspace": "baseline",
                            "with_skill_workspace": "with-skill",
                            "copied_skill_path": "with-skill/skill-under-test/SKILL.md",
                            "baseline_context_files": copied_baseline_context,
                            "with_skill_context_files": copied_with_skill_context,
                            "allowed_skill_reference_root": "with-skill/skill-under-test/references",
                            "isolation_mode": "tempdir-outside-repo",
                        },
                        indent=2,
                    ),
                )

                append_text(
                    progress_log,
                    f"running {scenario['id']} run={run_number} without_skill",
                )
                case_records.append(
                    run_case(
                        prompt=baseline_prompt,
                        runner=args.runner,
                        model=args.model,
                        timeout_seconds=args.timeout_seconds,
                        cwd=baseline_dir,
                        result_dir=case_dir / "without_skill",
                        observability_output=observability_output,
                        branch_label="without_skill",
                        scenario_id=scenario["id"],
                        run_number=run_number,
                        output_root=output_dir,
                    )
                )

                append_text(
                    progress_log,
                    f"running {scenario['id']} run={run_number} with_skill",
                )
                case_records.append(
                    run_case(
                        prompt=with_skill_prompt,
                        runner=args.runner,
                        model=args.model,
                        timeout_seconds=args.timeout_seconds,
                        cwd=with_skill_dir,
                        result_dir=case_dir / "with_skill",
                        observability_output=observability_output,
                        branch_label="with_skill",
                        scenario_id=scenario["id"],
                        run_number=run_number,
                        output_root=output_dir,
                        skill_name=skill_name,
                        phase=phase,
                        skill_context=skill_context,
                    )
                )

                append_text(progress_log, f"completed {scenario['id']} run={run_number}")

    completed_case_count = sum(record["status"] == "completed" for record in case_records)
    failed_case_count = len(case_records) - completed_case_count
    write_text(
        output_dir / "execution_summary.json",
        json.dumps(
            {
                "schema_version": "explicit-benchmark-execution-summary.v1",
                "benchmark": display_path(benchmark_path),
                "benchmark_sha256": benchmark_sha256,
                "skill_path": display_path(skill_path),
                "skill_name": skill_name,
                "skill_file_sha256": skill_file_sha256,
                "runner_home_isolation": runner_home_isolation,
                "runner": args.runner,
                "model": args.model,
                "run_started_at": timestamp,
                "scenario_count": len(scenarios),
                "runs_per_scenario": args.runs_per_scenario,
                "expected_case_count": len(scenarios) * args.runs_per_scenario * 2,
                "completed_case_count": completed_case_count,
                "failed_case_count": failed_case_count,
                "cases": case_records,
            },
            indent=2,
            ensure_ascii=False,
        ),
    )

    return 1 if failed_case_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
