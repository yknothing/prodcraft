#!/usr/bin/env python3
"""Validate Prodcraft structural invariants."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
CURATED_SKILLS_DIR = SKILLS_DIR / ".curated"
WORKFLOWS_DIR = ROOT / "workflows"
MANIFEST_PATH = ROOT / "manifest.yml"
SCHEMAS_DIR = ROOT / "schemas"
ARTIFACT_REGISTRY_PATH = SCHEMAS_DIR / "artifacts" / "registry.yml"
DISTRIBUTION_REGISTRY_PATH = SCHEMAS_DIR / "distribution" / "public-skill-registry.json"
MATRIX_PATH = ROOT / "rules" / "cross-cutting-matrix.yml"
INTAKE_SKILL_PATH = SKILLS_DIR / "00-discovery" / "intake" / "SKILL.md"
GATEWAY_PATH = SKILLS_DIR / "_gateway.md"
ADR_002_PATH = ROOT / "docs" / "adr" / "ADR-002-cross-phase-course-corrections.md"

SKILL_REQUIRED_FIELDS = [
    "name",
    "description",
]

SKILL_METADATA_REQUIRED_FIELDS = [
    "phase",
    "inputs",
    "outputs",
    "prerequisites",
    "roles",
    "methodologies",
]

# quality_gate in frontmatter is optional: the body ## Quality Gate checklist
# is the single authoritative source of truth (avoids dual-representation drift).
# Skills may include a frontmatter quality_gate string as a pre-hydration hint,
# but it is no longer required -- the body checklist alone is enforced.
SKILL_METADATA_OPTIONAL_FIELDS = [
    "quality_gate",
]

WORKFLOW_REQUIRED_FIELDS = [
    "name",
    "description",
    "cadence",
    "workflow_kind",
    "composes_with",
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
    "artifact-schema-registry",
    "cross-cutting-matrix",
    "curated-surface",
    "security-minimal",
}

# Zero-width and soft-hyphen characters that may hide injected content.
_ZERO_WIDTH_CHARS = frozenset("\u200b\u200c\u200d\ufeff\u00ad")

# Pipe followed by shell keywords that suggest command injection in a description.
_PIPE_INJECTION_RE = re.compile(r"\|[^\w]*(?:rm|sudo|curl|wget|eval|exec|sh|bash)\b", re.IGNORECASE)

# Cyrillic codepoint range (basic lookalike detection for otherwise ASCII text).
_CYRILLIC_RE = re.compile(r"[\u0400-\u04ff]")

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

QA_TIERS = {
    "critical",
    "standard",
}

CRITICAL_REVIEW_DEPTH_PATHS = {
    "benchmark_plan_path",
    "benchmark_results_path",
    "security_check_path",
    "trigger_eval_results_path",
}

WORKFLOW_KINDS = {
    "primary",
    "overlay",
}

REQUIRED_SKILL_BODY_HEADINGS = (
    "Context",
    "Inputs",
    "Process",
    "Outputs",
    "Quality Gate",
)

QUALITY_GATE_CHECK_ITEM_RE = re.compile(r"^\s*-\s*\[\s*\]\s+.+$", re.MULTILINE)


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


def iter_lifecycle_skill_paths() -> list[Path]:
    return sorted(
        path
        for path in SKILLS_DIR.rglob("SKILL.md")
        if ".curated" not in path.parts
    )


def load_yaml_file(path: Path, errors: list[str]) -> dict:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        errors.append(f"{path}: file does not exist")
        return {}
    except Exception as exc:
        errors.append(f"{path}: failed to parse YAML: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{path}: expected a YAML mapping")
        return {}
    return payload


def schema_string_enum(schema: dict, field_name: str, schema_path: Path, errors: list[str]) -> set[str]:
    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        errors.append(f"{schema_path}: `properties` must be a mapping")
        return set()

    field = properties.get(field_name)
    if not isinstance(field, dict):
        errors.append(f"{schema_path}: field `{field_name}` must be declared in `properties`")
        return set()

    values = field.get("enum")
    if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
        errors.append(f"{schema_path}: field `{field_name}` must declare a string enum")
        return set()

    return set(values)


def schema_nested_string_enum(schema: dict, path_parts: list[str], schema_path: Path, errors: list[str]) -> set[str]:
    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        errors.append(f"{schema_path}: `properties` must be a mapping")
        return set()

    node: object = properties
    for part in path_parts:
        if not isinstance(node, dict):
            errors.append(f"{schema_path}: `{'.'.join(path_parts)}` must resolve to a mapping before `{part}`")
            return set()
        node = node.get(part)

    if not isinstance(node, dict):
        errors.append(f"{schema_path}: `{'.'.join(path_parts)}` must be a mapping")
        return set()

    values = node.get("enum")
    if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
        errors.append(f"{schema_path}: `{'.'.join(path_parts)}` must declare a string enum")
        return set()

    return set(values)


def extract_intake_work_type_taxonomy(errors: list[str]) -> list[str]:
    try:
        _frontmatter, body = load_frontmatter(INTAKE_SKILL_PATH)
    except ValueError as exc:
        errors.append(str(exc))
        return []

    match = re.search(
        r"### Step 2: Classify Work Type\s*(?P<section>.*?)\n### Step 3: Ask Clarifying Questions",
        body,
        re.DOTALL,
    )
    if not match:
        errors.append(f"{INTAKE_SKILL_PATH}: could not locate the Step 2 work type table")
        return []

    work_types: list[str] = []
    for line in match.group("section").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        columns = [item.strip() for item in stripped.split("|")[1:-1]]
        if len(columns) != 5 or columns[0] in {"Type", "------"}:
            continue
        work_type = columns[0].replace("**", "").strip()
        if work_type and set(work_type) != {"-"}:
            work_types.append(work_type)

    if not work_types:
        errors.append(f"{INTAKE_SKILL_PATH}: work type table did not yield any taxonomy rows")
    return work_types


def load_primary_workflow_names(errors: list[str]) -> set[str]:
    primary_names: set[str] = set()
    for path in sorted(WORKFLOWS_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        try:
            frontmatter, _body = load_frontmatter(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if frontmatter.get("workflow_kind") == "primary":
            name = frontmatter.get("name")
            if isinstance(name, str):
                primary_names.add(name)
    if not primary_names:
        errors.append(f"{WORKFLOWS_DIR}: no primary workflows were discovered")
    return primary_names


def load_overlay_workflow_names(errors: list[str]) -> set[str]:
    overlay_names: set[str] = set()
    for path in sorted(WORKFLOWS_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        try:
            frontmatter, _body = load_frontmatter(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if frontmatter.get("workflow_kind") == "overlay":
            name = frontmatter.get("name")
            if isinstance(name, str):
                overlay_names.add(name)
    if not overlay_names:
        errors.append(f"{WORKFLOWS_DIR}: no overlay workflows were discovered")
    return overlay_names


def validate_intake_brief_schema_contract(schema: dict, schema_path: Path, manifest: dict, errors: list[str]) -> None:
    validate_language_boundary_schema_contract(schema, schema_path, errors)

    expected_work_types = set(extract_intake_work_type_taxonomy(errors))
    schema_work_types = schema_string_enum(schema, "work_type", schema_path, errors)
    if schema_work_types and expected_work_types and schema_work_types != expected_work_types:
        errors.append(
            f"{schema_path}: `work_type` enum must match intake taxonomy {sorted(expected_work_types)}; found {sorted(schema_work_types)}"
        )

    manifest_phase_ids = {
        phase.get("id")
        for phase in manifest.get("phases", [])
        if isinstance(phase, dict) and isinstance(phase.get("id"), str)
    }
    expected_entry_phases = manifest_phase_ids | {"cross-cutting"}
    schema_entry_phases = schema_string_enum(schema, "entry_phase", schema_path, errors)
    if schema_entry_phases and expected_entry_phases and schema_entry_phases != expected_entry_phases:
        errors.append(
            f"{schema_path}: `entry_phase` enum must match manifest phases plus `cross-cutting` {sorted(expected_entry_phases)}; found {sorted(schema_entry_phases)}"
        )

    expected_primary_workflows = load_primary_workflow_names(errors)
    schema_primary_workflows = schema_string_enum(schema, "workflow_primary", schema_path, errors)
    if schema_primary_workflows and expected_primary_workflows and schema_primary_workflows != expected_primary_workflows:
        errors.append(
            f"{schema_path}: `workflow_primary` enum must match declared primary workflows {sorted(expected_primary_workflows)}; found {sorted(schema_primary_workflows)}"
        )

    expected_overlay_workflows = load_overlay_workflow_names(errors)
    schema_overlay_workflows = schema_nested_string_enum(
        schema,
        ["workflow_overlays", "items"],
        schema_path,
        errors,
    )
    if schema_overlay_workflows and expected_overlay_workflows and schema_overlay_workflows != expected_overlay_workflows:
        errors.append(
            f"{schema_path}: `workflow_overlays` enum must match declared overlay workflows {sorted(expected_overlay_workflows)}; found {sorted(schema_overlay_workflows)}"
        )

    properties = schema.get("properties", {})
    workflow_overlays = properties.get("workflow_overlays", {}) if isinstance(properties, dict) else {}
    if not isinstance(workflow_overlays, dict) or workflow_overlays.get("minItems") != 1:
        errors.append(f"{schema_path}: `workflow_overlays` must use omission, not an empty array, to represent no active overlays")

    if schema.get("additionalProperties") is not False:
        errors.append(f"{schema_path}: `additionalProperties` must be `false` to keep the routing contract closed")


def validate_language_boundary_schema_contract(schema: dict, schema_path: Path, errors: list[str]) -> None:
    source_language_enum = schema_string_enum(schema, "source_language", schema_path, errors)
    if source_language_enum and source_language_enum != {"en", "zh", "mixed"}:
        errors.append(
            f"{schema_path}: `source_language` enum must be ['en', 'mixed', 'zh']; found {sorted(source_language_enum)}"
        )

    presentation_locale_enum = schema_string_enum(schema, "user_presentation_locale", schema_path, errors)
    if presentation_locale_enum and presentation_locale_enum != {"en", "zh"}:
        errors.append(
            f"{schema_path}: `user_presentation_locale` enum must be ['en', 'zh']; found {sorted(presentation_locale_enum)}"
        )

    properties = schema.get("properties", {})
    artifact_record_language = properties.get("artifact_record_language", {}) if isinstance(properties, dict) else {}
    if not isinstance(artifact_record_language, dict) or artifact_record_language.get("const") != "en":
        errors.append(f"{schema_path}: `artifact_record_language` must be a const `en` under current repo policy")


def extract_phase_jump_pairs_from_text(
    path: Path,
    *,
    start_marker: str,
    end_marker: str,
    errors: list[str],
) -> set[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    match = re.search(
        rf"{re.escape(start_marker)}\s*(?P<section>.*?){re.escape(end_marker)}",
        text,
        re.DOTALL,
    )
    if not match:
        errors.append(f"{path}: could not locate course-correction pair section between `{start_marker}` and `{end_marker}`")
        return set()

    pairs: set[tuple[str, str]] = set()
    for raw_pair in re.findall(r"-\s+`([^`]+)`", match.group("section")):
        if " -> " not in raw_pair:
            errors.append(f"{path}: malformed course-correction pair `{raw_pair}`")
            continue
        source_phase, target_phase = (part.strip() for part in raw_pair.split(" -> ", 1))
        pairs.add((source_phase, target_phase))
    if not pairs:
        errors.append(f"{path}: no course-correction pairs were found in the approved jump section")
    return pairs


def extract_course_correction_schema_pairs(schema: dict, schema_path: Path, errors: list[str]) -> set[tuple[str, str]]:
    any_of = schema.get("anyOf")
    if not isinstance(any_of, list):
        errors.append(f"{schema_path}: `anyOf` must encode the approved course-correction jump pairs")
        return set()

    pairs: set[tuple[str, str]] = set()
    for index, entry in enumerate(any_of):
        if not isinstance(entry, dict):
            errors.append(f"{schema_path}: anyOf[{index}] must be a mapping")
            continue
        properties = entry.get("properties")
        if not isinstance(properties, dict):
            errors.append(f"{schema_path}: anyOf[{index}] must define `properties`")
            continue
        source = properties.get("source_phase", {})
        target = properties.get("target_phase", {})
        if not isinstance(source, dict) or not isinstance(target, dict):
            errors.append(f"{schema_path}: anyOf[{index}] must constrain both `source_phase` and `target_phase`")
            continue
        source_value = source.get("const")
        target_value = target.get("const")
        if not isinstance(source_value, str) or not isinstance(target_value, str):
            errors.append(f"{schema_path}: anyOf[{index}] must use `const` for both phase fields")
            continue
        pairs.add((source_value, target_value))
    return pairs


def validate_course_correction_schema_contract(schema: dict, schema_path: Path, errors: list[str]) -> None:
    schema_pairs = extract_course_correction_schema_pairs(schema, schema_path, errors)
    adr_pairs = extract_phase_jump_pairs_from_text(
        ADR_002_PATH,
        start_marker="Approved direct jumps:",
        end_marker="Every direct jump must preserve:",
        errors=errors,
    )
    gateway_pairs = extract_phase_jump_pairs_from_text(
        GATEWAY_PATH,
        start_marker="Approved direct jumps:",
        end_marker="Each `course-correction-note` must capture:",
        errors=errors,
    )

    if schema_pairs and adr_pairs and schema_pairs != adr_pairs:
        errors.append(
            f"{schema_path}: schema-approved course-correction pairs must match ADR-002 {sorted(adr_pairs)}; found {sorted(schema_pairs)}"
        )
    if schema_pairs and gateway_pairs and schema_pairs != gateway_pairs:
        errors.append(
            f"{schema_path}: schema-approved course-correction pairs must match gateway contract {sorted(gateway_pairs)}; found {sorted(schema_pairs)}"
        )

    expected_source_phases = {source for source, _target in schema_pairs}
    expected_target_phases = {target for _source, target in schema_pairs}
    source_enum = schema_string_enum(schema, "source_phase", schema_path, errors)
    target_enum = schema_string_enum(schema, "target_phase", schema_path, errors)
    if source_enum and expected_source_phases and source_enum != expected_source_phases:
        errors.append(
            f"{schema_path}: `source_phase` enum must match approved jump sources {sorted(expected_source_phases)}; found {sorted(source_enum)}"
        )
    if target_enum and expected_target_phases and target_enum != expected_target_phases:
        errors.append(
            f"{schema_path}: `target_phase` enum must match approved jump targets {sorted(expected_target_phases)}; found {sorted(target_enum)}"
        )
    if schema.get("additionalProperties") is not False:
        errors.append(f"{schema_path}: `additionalProperties` must be `false` to keep the course-correction contract closed")


def snapshot_file_tree(root: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


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
            continue


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

    # Verify that the skill body includes the contract headings and that quality gate is machine-checkable.
    for heading in REQUIRED_SKILL_BODY_HEADINGS:
        section = extract_markdown_section(body, heading)
        if section is None:
            errors.append(f"{path}: missing required section `## {heading}`")

    quality_gate_section = extract_markdown_section(body, "Quality Gate")
    if quality_gate_section is not None and not QUALITY_GATE_CHECK_ITEM_RE.search(quality_gate_section):
        errors.append(f"{path}: `## Quality Gate` must contain at least one checklist item like `- [ ] ...`")


def validate_skill_security_minimal(path: Path, errors: list[str]) -> None:
    """Minimal automated security checks that produce falsifiable evidence.

    Covers the highest-severity categories from _quality-assurance.md:
    command safety (pipe injection) and basic encoding attacks (zero-width
    chars, Cyrillic homoglyphs in otherwise ASCII descriptions).
    """
    try:
        frontmatter, body = load_frontmatter(path)
    except ValueError:
        return  # structural errors already reported by validate_skill_file

    description = frontmatter.get("description", "") or ""

    # Check for zero-width / soft-hyphen characters in the description.
    hidden = [hex(ord(c)) for c in description if c in _ZERO_WIDTH_CHARS]
    if hidden:
        errors.append(
            f"{path}: `description` contains hidden zero-width or soft-hyphen characters {hidden} "
            f"-- possible encoding-layer payload"
        )

    # Check for pipe-based command injection patterns in description.
    if _PIPE_INJECTION_RE.search(description):
        errors.append(
            f"{path}: `description` contains a pipe followed by a shell keyword "
            f"-- possible command injection pattern"
        )

    # Check for Cyrillic homoglyphs in an otherwise ASCII description.
    ascii_chars = sum(1 for c in description if ord(c) < 128)
    if _CYRILLIC_RE.search(description) and ascii_chars > len(description) * 0.8:
        errors.append(
            f"{path}: `description` mixes Cyrillic characters into predominantly ASCII text "
            f"-- possible homoglyph substitution"
        )


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
        workflow_kind = frontmatter.get("workflow_kind")
        if workflow_kind not in WORKFLOW_KINDS:
            errors.append(f"{path}: `workflow_kind` must be one of {sorted(WORKFLOW_KINDS)}")
        composes_with = frontmatter.get("composes_with")
        if not isinstance(composes_with, list) or not composes_with:
            errors.append(f"{path}: `composes_with` must be a non-empty list")

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

        required_sections = ("Overview", "Phase Sequence", "Quality Gates", "Adaptation Notes")
        for section_name in required_sections:
            if not re.search(rf"^##\s+{re.escape(section_name)}\s*$", body, re.MULTILINE):
                errors.append(f"{path}: missing required workflow section `## {section_name}`")


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
        qa_tier = entry.get("qa_tier")
        if status not in SKILL_STATUSES:
            errors.append(f"{MANIFEST_PATH}: skill `{name}` has invalid or missing `status`")
            continue
        if qa_tier not in QA_TIERS:
            errors.append(f"{MANIFEST_PATH}: skill `{name}` has invalid or missing `qa_tier`")

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
            if status != "draft":
                missing = sorted({"structure_validation_path", "eval_strategy_path"} - set(qa))
                if missing:
                    errors.append(
                        f"{MANIFEST_PATH}: skill `{name}` with status `{status}` is missing QA review artifacts {', '.join(missing)}"
                    )
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

        if qa_tier == "critical" and status in {"tested", "secure", "production"}:
            required_paths = {"benchmark_results_path", "integration_test_path", "findings_path"}
            missing = sorted(required_paths - set(qa or {}))
            if missing:
                errors.append(
                    f"{MANIFEST_PATH}: critical skill `{name}` with status `{status}` is missing QA artifacts {', '.join(missing)}"
                )
        if qa_tier == "critical" and status == "review":
            if "findings_path" not in (qa or {}):
                errors.append(
                    f"{MANIFEST_PATH}: critical skill `{name}` with status `review` must define `qa.findings_path`"
                )
            if not any(path in (qa or {}) for path in CRITICAL_REVIEW_DEPTH_PATHS):
                errors.append(
                    f"{MANIFEST_PATH}: critical skill `{name}` with status `review` must define one substantive review artifact from {sorted(CRITICAL_REVIEW_DEPTH_PATHS)}"
                )
        if qa_tier == "critical" and status in {"secure", "production"}:
            missing = sorted({"security_review_path"} - set(qa or {}))
            if missing:
                errors.append(
                    f"{MANIFEST_PATH}: critical skill `{name}` with status `{status}` is missing QA artifacts {', '.join(missing)}"
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

    for path in iter_lifecycle_skill_paths():
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

    # Note: the prodcraft lifecycle is deliberately iterative — retrospective feeds back into discovery,
    # code-review feeds back into implementation, and so on. Acyclicity cannot be enforced on the full
    # artifact_flow graph. The manifest documents intentional feedback flows in `iterative_feedback_edges`
    # for traceability. Cycle detection via Kahn's algorithm is intentionally omitted here because it
    # produces only false positives on a correctly-designed iterative lifecycle.


def extract_backtick_refs(text: str) -> set[str]:
    return set(re.findall(r"`([a-z0-9-]+)`", text))


def load_skill_methodologies(errors: list[str]) -> dict[str, list[str]]:
    skill_methods: dict[str, list[str]] = {}
    for path in iter_lifecycle_skill_paths():
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
    manifest_skills = {
        entry["name"]: entry
        for entry in manifest.get("skills", [])
        if isinstance(entry, dict) and "name" in entry
    }
    workflow_names = {
        entry.get("name")
        for entry in manifest.get("workflows", [])
        if isinstance(entry, dict) and isinstance(entry.get("name"), str)
    }
    allowed_non_skill_tokens = {
        "all",
        "intake",
        "intake-brief",
    }
    allowed_non_skill_tokens.update(workflow_names)
    for path in sorted(WORKFLOWS_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        frontmatter, body = load_frontmatter(path)
        
        for line in body.splitlines():
            refs = extract_backtick_refs(line)
            for ref in refs:
                if ref not in skills and ref not in allowed_non_skill_tokens:
                    errors.append(
                        f"{path}: references undefined skills/tokens `{ref}`"
                    )
                elif ref in skills:
                    skill_status = manifest_skills.get(ref, {}).get("status")
                    if skill_status == "draft":
                        if not re.search(rf"`{re.escape(ref)}`\s*\((?:experimental|planned)\)", line, re.IGNORECASE):
                            errors.append(f"{path}: draft skill `{ref}` is referenced without being explicitly marked as (experimental) or (planned)")

        refs = extract_backtick_refs(body)
        compatibility_tags = workflow_compatibility_tags(frontmatter.get("name", ""))
        for ref in sorted(ref for ref in refs if ref in skills):
            methods = skill_methods.get(ref, [])
            if methods and not compatibility_tags.intersection(methods):
                errors.append(
                    f"{path}: references skill `{ref}` but workflow `{frontmatter.get('name')}` is incompatible with metadata.methodologies {methods}"
                )


def validate_artifact_schema_registry(manifest: dict, errors: list[str]) -> None:
    registry = load_yaml_file(ARTIFACT_REGISTRY_PATH, errors)
    artifacts = registry.get("artifacts", {})
    if not isinstance(artifacts, dict):
        errors.append(f"{ARTIFACT_REGISTRY_PATH}: `artifacts` must be a mapping")
        return

    manifest_artifacts = {
        entry.get("artifact")
        for entry in manifest.get("artifact_flow", [])
        if isinstance(entry, dict)
    }

    for artifact_name, entry in artifacts.items():
        if artifact_name not in manifest_artifacts:
            errors.append(f"{ARTIFACT_REGISTRY_PATH}: artifact `{artifact_name}` must appear in manifest artifact_flow")
        if not isinstance(entry, dict):
            errors.append(f"{ARTIFACT_REGISTRY_PATH}: artifact `{artifact_name}` must map to a metadata object")
            continue
        schema_rel = entry.get("schema_path")
        if not isinstance(schema_rel, str):
            errors.append(f"{ARTIFACT_REGISTRY_PATH}: artifact `{artifact_name}` is missing `schema_path`")
            continue
        schema_path = ROOT / schema_rel
        if not schema_path.exists():
            errors.append(f"{ARTIFACT_REGISTRY_PATH}: artifact `{artifact_name}` references missing schema `{schema_rel}`")
            continue
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{schema_path}: failed to parse JSON schema: {exc}")
            continue
        if artifact_name == "intake-brief":
            validate_intake_brief_schema_contract(schema, schema_path, manifest, errors)
        if artifact_name in {"problem-frame", "requirements-doc"}:
            validate_language_boundary_schema_contract(schema, schema_path, errors)
        if artifact_name == "course-correction-note":
            validate_course_correction_schema_contract(schema, schema_path, errors)
        template_rel = entry.get("template_path")
        if isinstance(template_rel, str):
            template_path = ROOT / template_rel
            if not template_path.exists():
                errors.append(f"{ARTIFACT_REGISTRY_PATH}: artifact `{artifact_name}` references missing template `{template_rel}`")
                continue
            required_fields = schema.get("required", [])
            if isinstance(required_fields, list):
                template_text = template_path.read_text(encoding="utf-8")
                missing = sorted(field for field in required_fields if field not in template_text)
                if missing:
                    errors.append(
                        f"{template_path}: template is missing required schema field markers {', '.join(missing)}"
                    )


def validate_cross_cutting_matrix(manifest: dict, errors: list[str]) -> None:
    matrix = load_yaml_file(MATRIX_PATH, errors)
    if matrix.get("schema_version") != "cross-cutting-matrix.v2":
        errors.append(f"{MATRIX_PATH}: `schema_version` must be `cross-cutting-matrix.v2`")
    entries = matrix.get("phases", [])
    if not isinstance(entries, list):
        errors.append(f"{MATRIX_PATH}: `phases` must be a list")
        return

    phase_ids = {entry.get("id") for entry in manifest.get("phases", []) if isinstance(entry, dict)}
    skill_names = manifest_skill_names(manifest)
    manifest_skills = {
        entry["name"]: entry
        for entry in manifest.get("skills", [])
        if isinstance(entry, dict) and "name" in entry
    }
    
    seen_phase_ids: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append(f"{MATRIX_PATH}: every matrix entry must be a mapping")
            continue
        phase_id = entry.get("phase_id")
        if phase_id not in phase_ids:
            errors.append(f"{MATRIX_PATH}: phase `{phase_id}` is not declared in manifest phases")
            continue
        seen_phase_ids.add(phase_id)
        must_consider = entry.get("must_consider", [])
        must_produce = entry.get("must_produce", [])
        skip_when_fast_track = entry.get("skip_when_fast_track", [])
        conditional = entry.get("conditional", [])

        if not isinstance(must_consider, list):
            errors.append(f"{MATRIX_PATH}: phase `{phase_id}` field `must_consider` must be a list")
            must_consider = []
        if not isinstance(must_produce, list):
            errors.append(f"{MATRIX_PATH}: phase `{phase_id}` field `must_produce` must be a list")
            must_produce = []
        if not isinstance(skip_when_fast_track, list):
            errors.append(f"{MATRIX_PATH}: phase `{phase_id}` field `skip_when_fast_track` must be a list")
            skip_when_fast_track = []
        if not isinstance(conditional, list):
            errors.append(f"{MATRIX_PATH}: phase `{phase_id}` field `conditional` must be a list")
            conditional = []

        must_consider_names: list[str] = []
        for skill_name in must_consider:
            if not isinstance(skill_name, str):
                errors.append(f"{MATRIX_PATH}: phase `{phase_id}` `must_consider` entries must be skill names")
                continue
            must_consider_names.append(skill_name)
            if skill_name not in skill_names:
                errors.append(f"{MATRIX_PATH}: phase `{phase_id}` references unknown `must_consider` skill `{skill_name}`")
            elif manifest_skills.get(skill_name, {}).get("status") == "draft":
                errors.append(f"{MATRIX_PATH}: phase `{phase_id}` `must_consider` dependency `{skill_name}` must not be draft")

        must_produce_skill_names: set[str] = set()
        for item in must_produce:
            if not isinstance(item, dict) or "skill" not in item or "when" not in item:
                errors.append(f"{MATRIX_PATH}: phase `{phase_id}` `must_produce` entries must include `skill` and `when`")
                continue
            skill_name = item["skill"]
            must_produce_skill_names.add(skill_name)
            if skill_name not in skill_names:
                errors.append(f"{MATRIX_PATH}: phase `{phase_id}` references unknown `must_produce` skill `{skill_name}`")
            elif manifest_skills.get(skill_name, {}).get("status") == "draft":
                errors.append(f"{MATRIX_PATH}: phase `{phase_id}` `must_produce` dependency `{skill_name}` must not be draft")

        skip_fast_track_names: list[str] = []
        for skill_name in skip_when_fast_track:
            if not isinstance(skill_name, str):
                errors.append(f"{MATRIX_PATH}: phase `{phase_id}` `skip_when_fast_track` entries must be skill names")
                continue
            skip_fast_track_names.append(skill_name)
            if skill_name not in skill_names:
                errors.append(f"{MATRIX_PATH}: phase `{phase_id}` references unknown `skip_when_fast_track` skill `{skill_name}`")

        conditional_skill_names: set[str] = set()
        for item in conditional:
            if not isinstance(item, dict) or "skill" not in item or "when" not in item:
                errors.append(f"{MATRIX_PATH}: phase `{phase_id}` conditional entries must include `skill` and `when`")
                continue
            skill_name = item["skill"]
            conditional_skill_names.add(skill_name)
            if skill_name not in skill_names:
                errors.append(f"{MATRIX_PATH}: phase `{phase_id}` references unknown conditional skill `{skill_name}`")

        if len(must_consider_names) != len(set(must_consider_names)):
            errors.append(f"{MATRIX_PATH}: phase `{phase_id}` duplicates `must_consider` skills")
        if len(skip_fast_track_names) != len(set(skip_fast_track_names)):
            errors.append(f"{MATRIX_PATH}: phase `{phase_id}` duplicates `skip_when_fast_track` skills")
        if len(conditional_skill_names) != len(conditional):
            errors.append(f"{MATRIX_PATH}: phase `{phase_id}` duplicates conditional skills")
        if len(must_produce_skill_names) != len(must_produce):
            errors.append(f"{MATRIX_PATH}: phase `{phase_id}` duplicates `must_produce` skills")

        must_consider_set = set(must_consider_names)
        skip_fast_track_set = set(skip_fast_track_names)
        overlap = must_consider_set.intersection(conditional_skill_names)
        if overlap:
            errors.append(f"{MATRIX_PATH}: phase `{phase_id}` duplicates `must_consider` and conditional skills {sorted(overlap)}")
        overlap = must_produce_skill_names.intersection(conditional_skill_names)
        if overlap:
            errors.append(f"{MATRIX_PATH}: phase `{phase_id}` duplicates `must_produce` and conditional skills {sorted(overlap)}")
        if not skip_fast_track_set.issubset(must_consider_set | must_produce_skill_names):
            errors.append(
                f"{MATRIX_PATH}: phase `{phase_id}` `skip_when_fast_track` must be a subset of `must_consider` or `must_produce`"
            )

    if seen_phase_ids != phase_ids:
        missing = sorted(phase_ids - seen_phase_ids)
        errors.append(f"{MATRIX_PATH}: missing phase entries for {', '.join(missing)}")



def validate_curated_surface(errors: list[str]) -> None:
    try:
        registry = json.loads(DISTRIBUTION_REGISTRY_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{DISTRIBUTION_REGISTRY_PATH}: file does not exist")
        return
    except Exception as exc:
        errors.append(f"{DISTRIBUTION_REGISTRY_PATH}: failed to parse JSON: {exc}")
        return

    if not isinstance(registry, dict):
        errors.append(f"{DISTRIBUTION_REGISTRY_PATH}: expected a JSON object")
        return

    public_skills = registry.get("public_skills", [])
    if not isinstance(public_skills, list):
        errors.append(f"{DISTRIBUTION_REGISTRY_PATH}: `public_skills` must be a list")
        return

    index_path = CURATED_SKILLS_DIR / "index.json"
    if not index_path.exists():
        errors.append(f"{index_path}: curated surface index is missing")
        index = {}
    else:
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{index_path}: failed to parse JSON: {exc}")
            index = {}
    index_names = {
        entry.get("name")
        for entry in index.get("skills", [])
        if isinstance(entry, dict) and isinstance(entry.get("name"), str)
    }
    manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8")) or {}
    manifest_skills = {
        entry["name"]: entry
        for entry in manifest.get("skills", [])
        if isinstance(entry, dict) and "name" in entry
    }
    names: set[str] = set()
    for entry in public_skills:
        if not isinstance(entry, dict) or "name" not in entry or "source" not in entry:
            errors.append(f"{DISTRIBUTION_REGISTRY_PATH}: each public skill entry must include `name` and `source`")
            continue
        name = entry["name"]
        if name in names:
            errors.append(f"{DISTRIBUTION_REGISTRY_PATH}: duplicate public skill `{name}`")
        names.add(name)
        if name not in index_names:
            errors.append(f"{index_path}: curated surface index is missing `{name}`")
        skill_dir = CURATED_SKILLS_DIR / name
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            errors.append(f"{skill_file}: curated skill file is missing")
            continue
        if name in manifest_skills:
            skill_meta = manifest_skills[name]
            manual_allowlist = bool(entry.get("manual_allowlist", False))
            if skill_meta.get("qa_tier") == "standard" and not manual_allowlist:
                errors.append(
                    f"{DISTRIBUTION_REGISTRY_PATH}: standard skill `{name}` must set `manual_allowlist: true` for curated export"
                )
            if skill_meta.get("qa_tier") == "critical" and skill_meta.get("status") not in {"tested", "secure", "production"} and not manual_allowlist:
                errors.append(
                    f"{DISTRIBUTION_REGISTRY_PATH}: critical skill `{name}` is below tested status and must be manually allowlisted"
                )
        text = skill_file.read_text(encoding="utf-8")
        for rel_target in re.findall(r"\((references|scripts|assets)/([^)]+)\)", text):
            bundled_path = skill_dir / rel_target[0] / rel_target[1]
            if not bundled_path.exists():
                errors.append(f"{skill_file}: curated reference `{bundled_path.relative_to(ROOT)}` does not exist")

    try:
        from export_curated_skills import export_curated_skills
    except Exception as exc:
        errors.append(f"{Path(__file__).resolve()}: failed to import curated exporter for parity validation: {exc}")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        temp_root = Path(tmpdir)
        export_curated_skills(repo_root=ROOT, output_root=temp_root)
        actual_tree = snapshot_file_tree(CURATED_SKILLS_DIR)
        exported_tree = snapshot_file_tree(temp_root)
        if actual_tree != exported_tree:
            missing = sorted(exported_tree.keys() - actual_tree.keys())
            extra = sorted(actual_tree.keys() - exported_tree.keys())
            changed = sorted(
                rel_path
                for rel_path in actual_tree.keys() & exported_tree.keys()
                if actual_tree[rel_path] != exported_tree[rel_path]
            )
            if missing:
                errors.append(f"{CURATED_SKILLS_DIR}: curated parity mismatch, missing exported files {missing[:10]}")
            if extra:
                errors.append(f"{CURATED_SKILLS_DIR}: curated parity mismatch, extra checked-in files {extra[:10]}")
            if changed:
                errors.append(f"{CURATED_SKILLS_DIR}: curated parity mismatch, changed files {changed[:10]}")


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

    _MANIFEST_DEPENDENT_CHECKS = {
        "manifest-files",
        "workflow-skill-refs",
        "manifest-skill-status",
        "artifact-flow",
        "artifact-schema-registry",
        "cross-cutting-matrix",
    }
    manifest = {}
    if selected_checks & _MANIFEST_DEPENDENT_CHECKS:
        manifest = validate_manifest(errors)

    if "skill-frontmatter" in selected_checks:
        for path in sorted(
            path
            for path in SKILLS_DIR.rglob("*.md")
            if ".curated" not in path.parts
        ):
            validate_skill_file(path, errors)

    if "security-minimal" in selected_checks:
        for path in iter_lifecycle_skill_paths():
            validate_skill_security_minimal(path, errors)

    for path in sorted(WORKFLOWS_DIR.glob("*.md")):
        validate_workflow_file(path, errors, selected_checks)

    if "workflow-skill-refs" in selected_checks and manifest:
        validate_workflow_skill_references(manifest, errors)

    if "manifest-skill-status" in selected_checks and manifest:
        validate_manifest_skill_status(manifest, errors)

    if "artifact-flow" in selected_checks and manifest:
        validate_artifact_flow(manifest, errors)

    if "artifact-schema-registry" in selected_checks and manifest:
        validate_artifact_schema_registry(manifest, errors)

    if "cross-cutting-matrix" in selected_checks and manifest:
        validate_cross_cutting_matrix(manifest, errors)

    if "curated-surface" in selected_checks:
        validate_curated_surface(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Prodcraft validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
