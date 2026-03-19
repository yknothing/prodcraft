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
    "artifact-flow",
}

SKILL_STATUSES = {
    "draft",
    "review",
    "tested",
    "secure",
    "production",
    "deprecated",
}

EVALUATION_MODES = {
    "discoverability",
    "routed",
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


def extract_markdown_section(text: str, heading: str) -> str | None:
    pattern = rf"^## {re.escape(heading)}\s*$"
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        return None

    start = match.end()
    remainder = text[start:]
    next_heading = re.search(r"^##\s+", remainder, re.MULTILINE)
    if next_heading:
        return remainder[: next_heading.start()].strip()
    return remainder.strip()


def validate_gotchas_block(source: Path, text: str, errors: list[str], *, source_label: str) -> None:
    gotchas_block = extract_markdown_section(text, "Gotchas")
    if gotchas_block is None:
        errors.append(f"{source}: {source_label} must include a `## Gotchas` section")
        return

    entries = list(re.finditer(r"^###\s+.+$", gotchas_block, re.MULTILINE))
    if not entries:
        errors.append(f"{source}: {source_label} must contain at least one `###` gotcha entry")
        return

    required_bullets = ("Trigger", "Failure mode", "What to do", "Escalate when")
    for index, entry in enumerate(entries):
        start = entry.end()
        end = entries[index + 1].start() if index + 1 < len(entries) else len(gotchas_block)
        entry_body = gotchas_block[start:end]
        missing = [
            bullet
            for bullet in required_bullets
            if not re.search(rf"^\s*-\s+{re.escape(bullet)}:", entry_body, re.MULTILINE)
        ]
        if missing:
            entry_title = entry.group(0).removeprefix("###").strip()
            errors.append(
                f"{source}: gotcha entry `{entry_title}` is missing gotcha bullets {', '.join(missing)}"
            )


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

    description = frontmatter.get("description")
    if not isinstance(description, str):
        errors.append(f"{path}: `description` must be a string")
    else:
        if len(description) > 1024:
            errors.append(f"{path}: `description` must be 1024 characters or fewer for Anthropic discovery")
        if "<" in description or ">" in description:
            errors.append(f"{path}: `description` must not contain XML angle brackets")
        if not re.search(r"\bUse (when|after|before)\b", description):
            errors.append(f"{path}: `description` must include an explicit trigger such as `Use when`, `Use after`, or `Use before`")

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

    skill_dir = path.parent
    if (skill_dir / "README.md").exists():
        errors.append(f"{path}: skill packages must not contain README.md; keep agent-facing guidance in SKILL.md or references/")

    _frontmatter, body = load_frontmatter(path)
    for rel_target in re.findall(r"\((references|scripts|assets)/([^)]+)\)", body):
        bundled_path = skill_dir / rel_target[0] / rel_target[1]
        if not bundled_path.exists():
            errors.append(f"{path}: referenced bundled resource `{bundled_path.relative_to(ROOT)}` does not exist")

    if "## Gotchas" in body:
        validate_gotchas_block(path, body, errors, source_label="inline gotchas section")

    if "references/gotchas.md" in body:
        gotchas_path = skill_dir / "references" / "gotchas.md"
        if gotchas_path.exists():
            validate_gotchas_block(path, gotchas_path.read_text(encoding="utf-8"), errors, source_label="gotchas reference")


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

        evaluation_mode = entry.get("evaluation_mode")
        if status != "draft" and evaluation_mode not in EVALUATION_MODES:
            errors.append(
                f"{MANIFEST_PATH}: skill `{name}` with status `{status}` must define `evaluation_mode` as one of {sorted(EVALUATION_MODES)}"
            )
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
            if evaluation_mode == "discoverability":
                if not isinstance(qa, dict) or "trigger_eval_results_path" not in qa:
                    errors.append(
                        f"{MANIFEST_PATH}: discoverability skill `{name}` with status `{status}` must define `qa.trigger_eval_results_path`"
                    )
            elif evaluation_mode == "routed":
                required_paths = {"benchmark_results_path", "integration_test_path"}
                missing = sorted(required_paths - set(qa or {}))
                if missing:
                    errors.append(
                        f"{MANIFEST_PATH}: routed skill `{name}` with status `{status}` is missing QA artifacts {', '.join(missing)}"
                    )

        if status == "production":
            required_paths = {"security_review_path", "integration_test_path"}
            missing = sorted(required_paths - set(qa or {}))
            if missing:
                errors.append(
                    f"{MANIFEST_PATH}: skill `{name}` with status `production` is missing QA artifacts {', '.join(missing)}"
                )


def validate_artifact_flow(manifest: dict, errors: list[str]) -> None:
    # Most artifacts have a single canonical producer, but implementation artifacts like
    # `source-code` may legitimately come from more than one skill.
    def producer_set(value: object) -> set[str]:
        if isinstance(value, str):
            return {value}
        if isinstance(value, list):
            return {item for item in value if isinstance(item, str)}
        return set()

    artifact_flow = {
        entry["artifact"]: {
            "produced_by": producer_set(entry.get("produced_by")),
            "consumed_by": set(entry.get("consumed_by", []) or []),
        }
        for entry in manifest.get("artifact_flow", [])
        if isinstance(entry, dict) and "artifact" in entry
    }

    for path in sorted(SKILLS_DIR.rglob("SKILL.md")):
        try:
            frontmatter, _body = load_frontmatter(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        skill_name = frontmatter.get("name")
        metadata = frontmatter.get("metadata", {})
        outputs = metadata.get("outputs", [])
        inputs = metadata.get("inputs", [])

        if isinstance(outputs, list):
            for artifact in outputs:
                flow_entry = artifact_flow.get(artifact)
                if not flow_entry or skill_name not in flow_entry.get("produced_by", set()):
                    errors.append(
                        f"{path}: output artifact `{artifact}` must appear in manifest artifact_flow with produced_by `{skill_name}`"
                    )

        if isinstance(inputs, list):
            for artifact in inputs:
                flow_entry = artifact_flow.get(artifact)
                if flow_entry and skill_name not in flow_entry.get("consumed_by", set()):
                    errors.append(
                        f"{path}: input artifact `{artifact}` appears in manifest artifact_flow and must list `{skill_name}` in consumed_by"
                    )


def extract_backtick_refs(text: str) -> set[str]:
    return set(re.findall(r"`([a-z0-9-]+)`", text))


def load_skill_methodologies(errors: list[str]) -> dict[str, list[str]]:
    skill_methods: dict[str, list[str]] = {}
    for path in sorted(SKILLS_DIR.rglob("SKILL.md")):
        try:
            frontmatter, _body = load_frontmatter(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        name = frontmatter.get("name")
        metadata = frontmatter.get("metadata", {})
        methods = metadata.get("methodologies", [])
        if isinstance(name, str) and isinstance(methods, list):
            skill_methods[name] = methods
    return skill_methods


def workflow_compatibility_tags(workflow_name: str) -> set[str]:
    tags = {"all", workflow_name}
    family_aliases = {
        "agile-sprint": {"agile"},
        "iterative-waterfall": {"waterfall"},
        "spec-driven": {"spec-driven"},
        "greenfield": {"greenfield"},
        "brownfield": {"brownfield"},
        "hotfix": {"hotfix"},
    }
    tags.update(family_aliases.get(workflow_name, set()))
    return tags


def validate_workflow_skill_references(manifest: dict, errors: list[str]) -> None:
    skills = manifest_skill_names(manifest)
    skill_methods = load_skill_methodologies(errors)
    allowed_non_skill_tokens = {
        "all",
        "intake",
        "intake-brief",
    }
    for path in sorted(WORKFLOWS_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        frontmatter, body = load_frontmatter(path)
        refs = extract_backtick_refs(body)
        missing = sorted(ref for ref in refs if ref not in skills and ref not in allowed_non_skill_tokens)
        if missing:
            errors.append(
                f"{path}: references undefined skills/tokens {', '.join('`' + item + '`' for item in missing)}"
            )

        compatibility_tags = workflow_compatibility_tags(frontmatter.get("name", ""))
        for ref in sorted(ref for ref in refs if ref in skills):
            methods = skill_methods.get(ref, [])
            if methods and not compatibility_tags.intersection(methods):
                errors.append(
                    f"{path}: references skill `{ref}` but workflow `{frontmatter.get('name')}` is incompatible with metadata.methodologies {methods}"
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

    if "artifact-flow" in selected_checks and manifest:
        validate_artifact_flow(manifest, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Prodcraft validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
