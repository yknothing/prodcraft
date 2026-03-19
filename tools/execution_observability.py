from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path


SCHEMA_VERSION = "execution-event.v1"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def new_trace_id() -> str:
    return f"trc_{uuid.uuid4().hex}"


def new_span_id() -> str:
    return f"spn_{uuid.uuid4().hex}"


def append_jsonl(path: Path | None, payload: dict) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8")
    fd = os.open(path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o644)
    try:
        os.write(fd, data)
    finally:
        os.close(fd)


def infer_skill_identity(skill_path: Path) -> tuple[str | None, str | None]:
    skill_file = skill_path / "SKILL.md"
    fallback_name = skill_path.name or None
    fallback_phase = None

    parts = skill_path.parts
    if "skills" in parts:
        idx = parts.index("skills")
        if idx + 1 < len(parts):
            fallback_phase = parts[idx + 1]

    if not skill_file.exists():
        return fallback_name, fallback_phase

    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return fallback_name, fallback_phase

    frontmatter = text.split("---", 2)[1]
    name = fallback_name
    phase = fallback_phase
    for line in frontmatter.splitlines():
        stripped = line.strip()
        if stripped.startswith("name:") and name is None:
            name = stripped.split(":", 1)[1].strip().strip("'\"") or None
        elif stripped.startswith("name:") and name == fallback_name:
            name = stripped.split(":", 1)[1].strip().strip("'\"") or fallback_name
        elif stripped.startswith("phase:") and phase is None:
            phase = stripped.split(":", 1)[1].strip().strip("'\"") or None
        elif stripped.startswith("phase:") and phase == fallback_phase:
            phase = stripped.split(":", 1)[1].strip().strip("'\"") or fallback_phase
    return name, phase


class ExecutionTrace:
    def __init__(
        self,
        *,
        output_path: Path | None,
        runner: str | None,
        model_name: str | None,
        skill_name: str | None,
        phase: str | None,
        workflow: str | None,
        trace_id: str | None = None,
    ) -> None:
        self.output_path = output_path
        self.runner = runner
        self.model_name = model_name
        self.skill_name = skill_name
        self.phase = phase
        self.workflow = workflow
        self.trace_id = trace_id or new_trace_id()

    def emit(
        self,
        *,
        event_type: str,
        status: str,
        span_id: str,
        parent_span_id: str | None = None,
        duration_ms: int | None = None,
        artifact_path: str | None = None,
        metadata: dict | None = None,
        skill_name: str | None = None,
        phase: str | None = None,
        workflow: str | None = None,
        model_name: str | None = None,
        token_input: int | None = None,
        token_output: int | None = None,
        token_total: int | None = None,
        usage_source: str | None = None,
    ) -> None:
        append_jsonl(
            self.output_path,
            {
                "schema_version": SCHEMA_VERSION,
                "timestamp": utc_now_iso(),
                "trace_id": self.trace_id,
                "span_id": span_id,
                "parent_span_id": parent_span_id,
                "event_type": event_type,
                "status": status,
                "runner": self.runner,
                "model_name": model_name if model_name is not None else self.model_name,
                "skill_name": skill_name if skill_name is not None else self.skill_name,
                "phase": phase if phase is not None else self.phase,
                "workflow": workflow if workflow is not None else self.workflow,
                "duration_ms": duration_ms,
                "artifact_path": artifact_path,
                "token_input": token_input,
                "token_output": token_output,
                "token_total": token_total,
                "usage_source": usage_source,
                "metadata": metadata or {},
            },
        )
