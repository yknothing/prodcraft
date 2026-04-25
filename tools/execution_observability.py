from __future__ import annotations

import json
import os
import uuid
import hashlib
from datetime import datetime, timezone
from pathlib import Path


SCHEMA_VERSION = "execution-event.v1"
SKILL_SUPPORTING_CONTEXT_SUFFIXES = {
    ".md",
    ".mdx",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def new_trace_id() -> str:
    return f"trc_{uuid.uuid4().hex}"


def new_span_id() -> str:
    return f"spn_{uuid.uuid4().hex}"


def measure_text_size(text: str) -> dict[str, int]:
    return {
        "char_count": len(text),
        "byte_count": len(text.encode("utf-8")),
    }


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return "", text
    return parts[1].strip(), parts[2].strip()


def frontmatter_scalar(frontmatter: str, key: str) -> str | None:
    prefix = f"{key}:"
    for line in frontmatter.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            value = stripped.split(":", 1)[1].strip().strip("'\"")
            return value or None
    return None


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


def iter_supporting_context_files(skill_path: Path) -> list[Path]:
    if not skill_path.exists():
        return []

    files: list[Path] = []
    for path in sorted(skill_path.rglob("*")):
        if not path.is_file() or path.name == "SKILL.md":
            continue
        if path.suffix.lower() in SKILL_SUPPORTING_CONTEXT_SUFFIXES:
            files.append(path)
    return files


def measure_skill_context(skill_path: Path) -> dict[str, object]:
    skill_file = skill_path / "SKILL.md"
    skill_name, phase = infer_skill_identity(skill_path)

    if not skill_file.exists():
        return {
            "skill_name": skill_name,
            "phase": phase,
            "skill_path": str(skill_path),
            "skill_file_path": str(skill_file),
            "skill_file_exists": False,
            "token_count_status": "unavailable",
            "token_count_reason": "skill file does not exist",
            "skill_metadata_char_count": None,
            "skill_frontmatter_char_count": None,
            "skill_body_char_count": None,
            "skill_file_char_count": None,
            "supporting_context_char_count": None,
            "total_available_context_char_count": None,
            "skill_metadata_byte_count": None,
            "skill_frontmatter_byte_count": None,
            "skill_body_byte_count": None,
            "skill_file_byte_count": None,
            "supporting_context_byte_count": None,
            "total_available_context_byte_count": None,
            "supporting_context_file_count": 0,
        }

    text = skill_file.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)
    description = frontmatter_scalar(frontmatter, "description")
    metadata_text = "\n".join(
        item
        for item in (
            f"name: {skill_name}" if skill_name else None,
            f"description: {description}" if description else None,
            f"skill_path: {skill_file}",
        )
        if item
    )

    supporting_files = iter_supporting_context_files(skill_path)
    supporting_char_count = 0
    supporting_byte_count = 0
    supporting_details: list[dict[str, object]] = []
    for path in supporting_files:
        content = path.read_text(encoding="utf-8")
        size = measure_text_size(content)
        supporting_char_count += size["char_count"]
        supporting_byte_count += size["byte_count"]
        supporting_details.append(
            {
                "path": str(path),
                "char_count": size["char_count"],
                "byte_count": size["byte_count"],
                "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            }
        )

    metadata_size = measure_text_size(metadata_text)
    frontmatter_size = measure_text_size(frontmatter)
    body_size = measure_text_size(body)
    skill_file_size = measure_text_size(text)
    return {
        "skill_name": skill_name,
        "phase": phase,
        "skill_path": str(skill_path),
        "skill_file_path": str(skill_file),
        "skill_file_exists": True,
        "skill_file_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "token_count_status": "unavailable",
        "token_count_reason": "no model-specific tokenizer or provider token-count API was used",
        "skill_metadata_char_count": metadata_size["char_count"],
        "skill_frontmatter_char_count": frontmatter_size["char_count"],
        "skill_body_char_count": body_size["char_count"],
        "skill_file_char_count": skill_file_size["char_count"],
        "supporting_context_char_count": supporting_char_count,
        "total_available_context_char_count": skill_file_size["char_count"] + supporting_char_count,
        "skill_metadata_byte_count": metadata_size["byte_count"],
        "skill_frontmatter_byte_count": frontmatter_size["byte_count"],
        "skill_body_byte_count": body_size["byte_count"],
        "skill_file_byte_count": skill_file_size["byte_count"],
        "supporting_context_byte_count": supporting_byte_count,
        "total_available_context_byte_count": skill_file_size["byte_count"] + supporting_byte_count,
        "supporting_context_file_count": len(supporting_files),
        "supporting_context_files": supporting_details,
        "line_count": len(text.splitlines()),
        "byte_count": skill_file_size["byte_count"],
    }


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
        token_cache_read_input: int | None = None,
        token_cache_write_input: int | None = None,
        usage_source: str | None = None,
        usage_precision: str | None = None,
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
                "token_cache_read_input": token_cache_read_input,
                "token_cache_write_input": token_cache_write_input,
                "usage_source": usage_source,
                "usage_precision": usage_precision,
                "metadata": metadata or {},
            },
        )
