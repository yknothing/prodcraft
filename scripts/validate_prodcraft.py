#!/usr/bin/env python3
"""Validate Prodcraft structural invariants."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
WORKFLOWS_DIR = ROOT / "workflows"
MANIFEST_PATH = ROOT / "manifest.yml"

SKILL_REQUIRED_FIELDS = [
    "name",
    "description",
]

SKILL_METADATA_REQUIRED_FIELDS = [
    "phase",
    "inputs",
    "outputs",
    "prerequisites",
    "quality_gate",
    "roles",
    "methodologies",
]

WORKFLOW_REQUIRED_FIELDS = [
    "name",
    "description",
    "cadence",
    "entry_skill",
    "required_artifacts",
    "best_for",
    "phases_included",
]


CHECKS = {
    "skill-frontmatter",
    "workflow-frontmatter",
    "workflow-entry-gate",
    "manifest-files",
    "manifest-skill-status",
    "workflow-skill-refs",
}

SKILL_STATUSES = {
    "draft",
    "review",
    "tested",
    "secure",
    "production",
    "deprecated",
}


def load_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter start delimiter")

    parts = text.split("---\n", 2)
    if len(parts) < 3:
        raise ValueError(f"{path}: malformed YAML frontmatter")

    frontmatter = yaml.safe_load(parts[1]) or {}
    body = parts[2]
    if not isinstance(frontmatter, dict):
        raise ValueError(f"{path}: frontmatter must parse to a mapping")
    return frontmatter, body


def raw_frontmatter(path: Path) -> str:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter start delimiter")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        raise ValueError(f"{path}: malformed YAML frontmatter")
    return parts[1]


def validate_skill_file(path: Path, errors: list[str]) -> None:
    if path.name != "SKILL.md":
        return

    try:
        frontmatter, _body = load_frontmatter(path)
    except ValueError as exc:
        errors.append(str(exc))
        return

    for field in SKILL_REQUIRED_FIELDS:
        if field not in frontmatter:
            errors.append(f"{path}: missing required skill field `{field}`")

    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        errors.append(f"{path}: missing required skill field `metadata`")
        return

    for field in SKILL_METADATA_REQUIRED_FIELDS:
        if field not in metadata:
            errors.append(f"{path}: missing required skill metadata field `metadata.{field}`")

    expected_phase = path.parents[1].name
    actual_phase = metadata.get("phase")
    if actual_phase != expected_phase:
        errors.append(f"{path}: `metadata.phase` must match parent phase directory `{expected_phase}`")

    try:
        frontmatter_raw = raw_frontmatter(path)
    except ValueError as exc:
        errors.append(str(exc))
        return

    lines = frontmatter_raw.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith("description:"):
            continue
        if index + 1 < len(lines) and lines[index + 1].startswith("  "):
            errors.append(f"{path}: `description` must remain on a single line for Anthropic skill discovery")
        break


def validate_workflow_file(path: Path, errors: list[str], selected_checks: set[str]) -> None:
    if path.name.startswith("_"):
        return

    try:
        frontmatter, body = load_frontmatter(path)
    except ValueError as exc:
        errors.append(str(exc))
        return

    if "workflow-frontmatter" in selected_checks:
        for field in WORKFLOW_REQUIRED_FIELDS:
            if field not in frontmatter:
                errors.append(f"{path}: missing required workflow field `{field}`")

    if "workflow-entry-gate" in selected_checks:
        if frontmatter.get("entry_skill") != "intake":
            errors.append(f"{path}: `entry_skill` must be `intake`")

        required_artifacts = frontmatter.get("required_artifacts", [])
        if not isinstance(required_artifacts, list) or "intake-brief" not in required_artifacts:
            errors.append(f"{path}: `required_artifacts` must include `intake-brief`")

        if "## Entry Gate" not in body:
            errors.append(f"{path}: missing `## Entry Gate` section")

        body_lower = body.lower()
        if "intake" not in body_lower or "intake-brief" not in body_lower:
            errors.append(f"{path}: entry gate must mention both `intake` and `intake-brief`")


def manifest_skill_names(manifest: dict) -> set[str]:
    return {item["name"] for item in manifest.get("skills", []) if isinstance(item, dict) and "name" in item}


def validate_manifest(errors: list[str]) -> dict:
    try:
        manifest = yaml.safe_load(MANIFEST_PATH.read_text()) or {}
    except Exception as exc:  # pragma: no cover - parse failure
        errors.append(f"{MANIFEST_PATH}: failed to parse YAML: {exc}")
        return {}

    for entry in manifest.get("skills", []):
        path = ROOT / entry["file"]
        if not path.exists():
            errors.append(f"{MANIFEST_PATH}: missing referenced skill file `{entry['file']}`")

    for entry in manifest.get("workflows", []):
        path = ROOT / entry["file"]
        if not path.exists():
            errors.append(f"{MANIFEST_PATH}: missing referenced workflow file `{entry['file']}`")

    return manifest


def validate_manifest_skill_status(manifest: dict, errors: list[str]) -> None:
    for entry in manifest.get("skills", []):
        name = entry.get("name", "<unknown>")
        status = entry.get("status")
        if status not in SKILL_STATUSES:
            errors.append(f"{MANIFEST_PATH}: skill `{name}` has invalid or missing `status`")
            continue

        qa = entry.get("qa")
        if status != "draft" and not isinstance(qa, dict):
            errors.append(f"{MANIFEST_PATH}: skill `{name}` with status `{status}` must define a `qa` mapping")
            continue

        if isinstance(qa, dict):
            for key, rel_path in qa.items():
                if not key.endswith("_path"):
                    continue
                target = ROOT / rel_path
                if not target.exists():
                    errors.append(
                        f"{MANIFEST_PATH}: skill `{name}` references missing QA artifact `{rel_path}` via `{key}`"
                    )

        if status in {"tested", "secure", "production"}:
            if not isinstance(qa, dict) or "trigger_eval_results_path" not in qa:
                errors.append(
                    f"{MANIFEST_PATH}: skill `{name}` with status `{status}` must define `qa.trigger_eval_results_path`"
                )

        if status == "production":
            required_paths = {"security_review_path", "integration_test_path"}
            missing = sorted(required_paths - set(qa or {}))
            if missing:
                errors.append(
                    f"{MANIFEST_PATH}: skill `{name}` with status `production` is missing QA artifacts {', '.join(missing)}"
                )


def extract_backtick_refs(text: str) -> set[str]:
    return set(re.findall(r"`([a-z0-9-]+)`", text))


def validate_workflow_skill_references(manifest: dict, errors: list[str]) -> None:
    skills = manifest_skill_names(manifest)
    allowed_non_skill_tokens = {
        "all",
        "intake",
        "intake-brief",
    }
    for path in sorted(WORKFLOWS_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        _frontmatter, body = load_frontmatter(path)
        refs = extract_backtick_refs(body)
        missing = sorted(ref for ref in refs if ref not in skills and ref not in allowed_non_skill_tokens)
        if missing:
            errors.append(
                f"{path}: references undefined skills/tokens {', '.join('`' + item + '`' for item in missing)}"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Prodcraft structure.")
    parser.add_argument(
        "--check",
        action="append",
        choices=sorted(CHECKS),
        help="Run only the named check. May be repeated. Defaults to all checks.",
    )
    args = parser.parse_args()

    selected_checks = set(args.check or CHECKS)
    errors: list[str] = []

    manifest = {}
    if "manifest-files" in selected_checks or "workflow-skill-refs" in selected_checks:
        manifest = validate_manifest(errors)

    if "skill-frontmatter" in selected_checks:
        for path in sorted(SKILLS_DIR.rglob("*.md")):
            validate_skill_file(path, errors)

    for path in sorted(WORKFLOWS_DIR.glob("*.md")):
        validate_workflow_file(path, errors, selected_checks)

    if "workflow-skill-refs" in selected_checks and manifest:
        validate_workflow_skill_references(manifest, errors)

    if "manifest-skill-status" in selected_checks and manifest:
        validate_manifest_skill_status(manifest, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Prodcraft validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
