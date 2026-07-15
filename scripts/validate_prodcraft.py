#!/usr/bin/env python3
"""Validate Prodcraft structural invariants."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import tempfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.execution_validation import (  # noqa: E402
    ValidationDisposition,
    authorize_execution_state,
    validate_artifact_instance,
    validate_registered_artifact_payload as validate_registered_artifact_payload,
    validate_verification_record_instance_contract as validate_verification_record_instance_contract,
)
from tools.execution_state import (  # noqa: E402
    STRICT_JSON_MAX_BYTES,
    StrictJSONError,
    parse_strict_json_bytes,
)

SKILLS_DIR = ROOT / "skills"
CURATED_SKILLS_DIR = SKILLS_DIR / ".curated"
WORKFLOWS_DIR = ROOT / "workflows"
MANIFEST_PATH = ROOT / "manifest.yml"
SCHEMAS_DIR = ROOT / "schemas"
ARTIFACT_REGISTRY_PATH = SCHEMAS_DIR / "artifacts" / "registry.yml"
PROTOCOL_RESULT_REGISTRY_PATH = SCHEMAS_DIR / "protocol" / "registry.yml"
DISTRIBUTION_REGISTRY_PATH = SCHEMAS_DIR / "distribution" / "public-skill-registry.json"
PUBLIC_SKILL_PORTABILITY_PATH = SCHEMAS_DIR / "distribution" / "public-skill-portability.json"
MATRIX_PATH = ROOT / "rules" / "cross-cutting-matrix.yml"
INTAKE_SKILL_PATH = SKILLS_DIR / "00-discovery" / "pc-intake" / "SKILL.md"
GATEWAY_PATH = SKILLS_DIR / "_gateway.md"
ADR_002_PATH = ROOT / "docs" / "adr" / "ADR-002-cross-phase-course-corrections.md"

SKILL_NAME_PREFIX = "pc-"
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_SKILL_LINK_RE = re.compile(
    r"\[[^\]]+\]\((?P<target>[^)\s]*SKILL\.md(?:#[^)\s]+)?)\)"
)
LOCAL_EVAL_FILE_RE = re.compile(
    r"`(?P<path>eval/[^`\s]+)`"
)


def _is_gitignored_local_artifact(rel_path: str) -> bool:
    """True when a referenced eval path matches a declared local-artifact pattern.

    Raw benchmark run directories (e.g. `eval/**/run-*/`) are deliberately
    gitignored; review documents may still cite them as provenance for evidence
    that lives only on the operator's machine. A gitignored reference is a
    declared local artifact, not a broken link.
    """
    import subprocess

    # Directory ignore patterns (`run-*/`) only match paths with a trailing
    # slash, and the referenced path may be a file or a directory -- probe both.
    for candidate in (rel_path, rel_path.rstrip("/") + "/"):
        result = subprocess.run(
            ["git", "check-ignore", "-q", candidate],
            cwd=ROOT,
            capture_output=True,
        )
        if result.returncode == 0:
            return True
    return False

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
    "protocol-result-registry",
    "cross-cutting-matrix",
    "curated-surface",
    "security-minimal",
    "doc-script-refs",
    "gateway-refs",
}

# Repository-root script references in prose, e.g. `scripts/validate_prodcraft.py`.
# The lookbehind stops the regex from matching the tail of a longer nested path
# such as `tools/anthropic_trigger_eval/scripts/run_eval.py`.
_SCRIPT_REF_RE = re.compile(r"(?<![\w/])scripts/[A-Za-z0-9_\-/]+\.py\b")

# Discovery descriptions share one context budget across every installed skill.
# Soft guidance is 280 characters; this is the enforced hard cap.
DESCRIPTION_HARD_CAP = 350


class _CheckChoices(tuple[str, ...]):
    """Preserve the legacy argparse listing while accepting additive checks."""

    def __contains__(self, value: object) -> bool:
        return value in CHECKS


LEGACY_CHECK_CHOICES = _CheckChoices(sorted(CHECKS - {"protocol-result-registry"}))

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

PUBLIC_SURFACE_STABILITIES = {
    "beta",
    "stable",
}

PUBLIC_SURFACE_READINESS = {
    "core",
    "beta",
    "experimental",
}

PUBLIC_SURFACE_PORTABILITY = {
    "portable_as_is",
    "portable_with_caveat",
    "blocked",
}

BCP_47_LOCALE_PATTERN = r"^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*$"

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


def validate_skill_name(name: object, source: Path, errors: list[str]) -> None:
    if not isinstance(name, str) or not name:
        errors.append(f"{source}: skill name must be a non-empty string")
        return
    if len(name) > 64:
        errors.append(f"{source}: skill name `{name}` must be 64 characters or fewer")
    if not SKILL_NAME_RE.fullmatch(name):
        errors.append(
            f"{source}: skill name `{name}` must contain only lowercase letters, numbers, and single hyphens"
        )
    if not name.startswith(SKILL_NAME_PREFIX):
        errors.append(f"{source}: skill name `{name}` must start with `pc-`")


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


class _UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects mapping-key replacement."""


def _construct_unique_mapping(loader: _UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict:
    mapping: dict = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key `{key}`")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def load_unique_yaml_mapping(path: Path, errors: list[str]) -> dict:
    try:
        payload = yaml.load(path.read_text(encoding="utf-8"), Loader=_UniqueKeyLoader) or {}
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


def resolve_protocol_schema_path(
    root: Path,
    schema_rel: object,
    registry_path: Path,
    errors: list[str],
) -> Path | None:
    if (
        not isinstance(schema_rel, str)
        or not schema_rel.startswith("schemas/protocol/")
        or schema_rel.startswith("/")
        or "\\" in schema_rel
        or ":" in schema_rel
        or "//" in schema_rel
        or schema_rel.endswith("/")
        or any(part in {"", ".", ".."} for part in schema_rel.split("/"))
    ):
        errors.append(f"{registry_path}: unsafe `schema_path` `{schema_rel}`")
        return None

    candidate = root
    parts = schema_rel.split("/")
    for index, part in enumerate(parts):
        candidate /= part
        try:
            mode = candidate.lstat().st_mode
        except FileNotFoundError:
            errors.append(f"{registry_path}: references missing schema `{schema_rel}`")
            return None
        except OSError as exc:
            errors.append(f"{registry_path}: cannot inspect schema path `{schema_rel}`: {exc}")
            return None
        if stat.S_ISLNK(mode):
            errors.append(f"{registry_path}: schema path `{schema_rel}` contains a symlink")
            return None
        if index < len(parts) - 1 and not stat.S_ISDIR(mode):
            errors.append(f"{registry_path}: schema path `{schema_rel}` has a non-directory parent")
            return None
        if index == len(parts) - 1 and not stat.S_ISREG(mode):
            errors.append(f"{registry_path}: schema path `{schema_rel}` must be a regular file")
            return None

    try:
        candidate.resolve(strict=True).relative_to(root.resolve(strict=True))
    except (OSError, ValueError):
        errors.append(f"{registry_path}: unsafe `schema_path` `{schema_rel}` escapes repository root")
        return None
    return candidate


def load_protocol_schema_snapshot(root: Path, schema_rel: str, schema_path: Path) -> dict:
    """Read one schema without following a swapped path component."""

    directory_fd = -1
    file_fd = -1
    try:
        directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
        directory_fd = os.open(root, directory_flags)
        parts = schema_rel.split("/")
        for part in parts[:-1]:
            next_fd = os.open(part, directory_flags, dir_fd=directory_fd)
            os.close(directory_fd)
            directory_fd = next_fd

        file_flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        file_fd = os.open(parts[-1], file_flags, dir_fd=directory_fd)
        opened_stat = os.fstat(file_fd)
        if not stat.S_ISREG(opened_stat.st_mode):
            raise StrictJSONError(f"schema path must be a regular file: {schema_path}")
        with os.fdopen(file_fd, "rb", closefd=True) as handle:
            file_fd = -1
            content = handle.read(STRICT_JSON_MAX_BYTES + 1)
            final_stat = os.fstat(handle.fileno())
        if len(content) > STRICT_JSON_MAX_BYTES:
            raise StrictJSONError(
                f"schema exceeds {STRICT_JSON_MAX_BYTES} bytes: {schema_path}"
            )
        opened_identity = (
            opened_stat.st_dev,
            opened_stat.st_ino,
            opened_stat.st_mode,
            opened_stat.st_size,
            opened_stat.st_mtime_ns,
            opened_stat.st_ctime_ns,
        )
        final_identity = (
            final_stat.st_dev,
            final_stat.st_ino,
            final_stat.st_mode,
            final_stat.st_size,
            final_stat.st_mtime_ns,
            final_stat.st_ctime_ns,
        )
        if opened_identity != final_identity or len(content) != opened_stat.st_size:
            raise StrictJSONError(f"schema changed while being read: {schema_path}")
        return parse_strict_json_bytes(content, schema_path)
    except StrictJSONError:
        raise
    except OSError as exc:
        raise StrictJSONError(
            f"schema path changed or contains a symlink: {schema_path}: {exc}"
        ) from exc
    finally:
        if file_fd >= 0:
            os.close(file_fd)
        if directory_fd >= 0:
            os.close(directory_fd)


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


def schema_locale_field(field: object, field_name: str, schema_path: Path, errors: list[str]) -> None:
    if not isinstance(field, dict):
        errors.append(f"{schema_path}: field `{field_name}` must be declared in `properties`")
        return
    if field.get("type") != "string" or field.get("pattern") != BCP_47_LOCALE_PATTERN:
        errors.append(
            f"{schema_path}: field `{field_name}` must be a BCP-47-style locale string using pattern {BCP_47_LOCALE_PATTERN}"
        )


def schema_source_language_field(field: object, field_name: str, schema_path: Path, errors: list[str]) -> None:
    if not isinstance(field, dict):
        errors.append(f"{schema_path}: field `{field_name}` must be declared in `properties`")
        return
    one_of = field.get("oneOf")
    expected_locale_branch = {"type": "string", "pattern": BCP_47_LOCALE_PATTERN}
    expected_mixed_branch = {"const": "mixed"}
    if not isinstance(one_of, list) or expected_locale_branch not in one_of or expected_mixed_branch not in one_of:
        errors.append(
            f"{schema_path}: field `{field_name}` must allow BCP-47-style locale strings and the explicit `mixed` sentinel"
        )


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

    expected_runtime_contexts = {
        "agent_internal_skill",
        "host_runtime_tool",
        "local_dev_harness",
        "internal_service",
        "public_service",
        "unknown",
    }
    schema_runtime_contexts = schema_nested_string_enum(
        schema,
        ["quality_target_context", "properties", "runtime_context"],
        schema_path,
        errors,
    )
    if schema_runtime_contexts and schema_runtime_contexts != expected_runtime_contexts:
        errors.append(
            f"{schema_path}: `quality_target_context.runtime_context` enum must be {sorted(expected_runtime_contexts)}; found {sorted(schema_runtime_contexts)}"
        )

    expected_exposure_profiles = {
        "no_network_listener",
        "localhost_only",
        "private_network",
        "public_internet",
        "unknown",
    }
    schema_exposure_profiles = schema_nested_string_enum(
        schema,
        ["quality_target_context", "properties", "exposure_profile"],
        schema_path,
        errors,
    )
    if schema_exposure_profiles and schema_exposure_profiles != expected_exposure_profiles:
        errors.append(
            f"{schema_path}: `quality_target_context.exposure_profile` enum must be {sorted(expected_exposure_profiles)}; found {sorted(schema_exposure_profiles)}"
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


# Language fields are open BCP-47 tags, not a closed operator-specific list.
# `source_language` additionally accepts the literal `mixed` for multilingual requests.


def validate_language_boundary_schema_contract(schema: dict, schema_path: Path, errors: list[str]) -> None:
    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        errors.append(f"{schema_path}: `properties` must be a mapping")
        return

    schema_source_language_field(properties.get("source_language"), "source_language", schema_path, errors)
    schema_locale_field(properties.get("user_presentation_locale"), "user_presentation_locale", schema_path, errors)

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


def validate_verification_record_schema_contract(schema: dict, schema_path: Path, errors: list[str]) -> None:
    required = schema.get("required", [])
    expected_required = {
        "artifact",
        "schema_version",
        "status",
        "claim",
        "claim_scope",
        "verified_at",
        "work_state_ref",
        "evidence_refs",
        "checks_run",
        "passed",
        "failed",
        "remaining_unverified",
        "claim_may_be_made",
    }
    if set(required) != expected_required:
        errors.append(
            f"{schema_path}: required fields must be exactly {sorted(expected_required)}; found {required}"
        )

    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        errors.append(f"{schema_path}: `properties` must be a mapping")
        return

    artifact = properties.get("artifact", {})
    if not isinstance(artifact, dict) or artifact.get("const") != "verification-record":
        errors.append(f"{schema_path}: artifact const must be `verification-record`")

    schema_version = properties.get("schema_version", {})
    if not isinstance(schema_version, dict) or schema_version.get("const") != "verification-record.v1":
        errors.append(f"{schema_path}: schema_version const must be `verification-record.v1`")

    status = properties.get("status", {})
    if not isinstance(status, dict) or set(status.get("enum", [])) != {"draft", "accepted", "rejected"}:
        errors.append(f"{schema_path}: status enum must be draft/accepted/rejected")

    verified_at = properties.get("verified_at", {})
    if not isinstance(verified_at, dict) or verified_at.get("format") != "date-time":
        errors.append(f"{schema_path}: verified_at must use JSON Schema date-time format")

    for field_name in ("claim", "claim_scope"):
        field = properties.get(field_name, {})
        if not isinstance(field, dict) or field.get("minLength") != 1:
            errors.append(f"{schema_path}: `{field_name}` must require non-empty strings with minLength 1")

    work_state_ref = properties.get("work_state_ref", {})
    if not isinstance(work_state_ref, dict) or work_state_ref.get("type") != "object":
        errors.append(f"{schema_path}: work_state_ref must be a structured object")
    else:
        expected_work_state_required = {"id", "kind", "ref", "captured_at", "status"}
        if set(work_state_ref.get("required", [])) != expected_work_state_required:
            errors.append(
                f"{schema_path}: work_state_ref must require {sorted(expected_work_state_required)}"
            )
        work_state_properties = work_state_ref.get("properties", {})
        if not isinstance(work_state_properties, dict):
            errors.append(f"{schema_path}: work_state_ref properties must be a mapping")
        else:
            for field_name in ("id", "ref", "diff_ref"):
                field = work_state_properties.get(field_name, {})
                if not isinstance(field, dict) or field.get("minLength") != 1:
                    errors.append(f"{schema_path}: work_state_ref `{field_name}` must require minLength 1")
            kind = work_state_properties.get("kind", {})
            if not isinstance(kind, dict) or set(kind.get("enum", [])) != {"git"}:
                errors.append(f"{schema_path}: work_state_ref kind enum must be git")
            captured_at = work_state_properties.get("captured_at", {})
            if not isinstance(captured_at, dict) or captured_at.get("format") != "date-time":
                errors.append(f"{schema_path}: work_state_ref captured_at must use JSON Schema date-time format")
            status_field = work_state_properties.get("status", {})
            if not isinstance(status_field, dict) or set(status_field.get("enum", [])) != {"clean", "dirty"}:
                errors.append(f"{schema_path}: work_state_ref status enum must be clean/dirty")
        if work_state_ref.get("additionalProperties") is not False:
            errors.append(f"{schema_path}: work_state_ref must be a closed object")
        dirty_rule = {
            "if": {
                "properties": {"status": {"const": "dirty"}},
                "required": ["status"],
            },
            "then": {"required": ["diff_ref"]},
        }
        if dirty_rule not in work_state_ref.get("allOf", []):
            errors.append(f"{schema_path}: work_state_ref must require diff_ref when status is dirty")

    evidence_refs = properties.get("evidence_refs", {})
    if not isinstance(evidence_refs, dict) or evidence_refs.get("minItems") != 1:
        errors.append(f"{schema_path}: evidence_refs must require at least one item")
    else:
        evidence_ref_item = evidence_refs.get("items", {})
        if not isinstance(evidence_ref_item, dict) or evidence_ref_item.get("type") != "object":
            errors.append(f"{schema_path}: evidence_refs items must be structured objects")
        else:
            expected_evidence_required = {"id", "kind", "ref", "captured_at", "work_state_ref"}
            if set(evidence_ref_item.get("required", [])) != expected_evidence_required:
                errors.append(
                    f"{schema_path}: evidence_refs items must require {sorted(expected_evidence_required)}"
                )
            evidence_properties = evidence_ref_item.get("properties", {})
            if not isinstance(evidence_properties, dict):
                errors.append(f"{schema_path}: evidence_refs item properties must be a mapping")
            else:
                for field_name in ("id", "ref", "work_state_ref"):
                    field = evidence_properties.get(field_name, {})
                    if not isinstance(field, dict) or field.get("minLength") != 1:
                        errors.append(f"{schema_path}: evidence_refs item `{field_name}` must require minLength 1")
                kind = evidence_properties.get("kind", {})
                expected_kinds = {"command", "file", "diff", "test", "review", "other"}
                if not isinstance(kind, dict) or set(kind.get("enum", [])) != expected_kinds:
                    errors.append(f"{schema_path}: evidence_refs item kind enum must be {sorted(expected_kinds)}")
                captured_at = evidence_properties.get("captured_at", {})
                if not isinstance(captured_at, dict) or captured_at.get("format") != "date-time":
                    errors.append(f"{schema_path}: evidence_refs item captured_at must use JSON Schema date-time format")
            if evidence_ref_item.get("additionalProperties") is not False:
                errors.append(f"{schema_path}: evidence_refs items must be closed objects")

    checks_run = properties.get("checks_run", {})
    if not isinstance(checks_run, dict) or checks_run.get("minItems") != 1:
        errors.append(f"{schema_path}: checks_run must require at least one item")
    else:
        check_item = checks_run.get("items", {})
        if not isinstance(check_item, dict) or check_item.get("additionalProperties") is not False:
            errors.append(f"{schema_path}: checks_run items must be closed objects")
        elif set(check_item.get("required", [])) != {"name", "result", "evidence_ref", "work_state_ref"}:
            errors.append(f"{schema_path}: checks_run items must require name/result/evidence_ref/work_state_ref")
        else:
            check_properties = check_item.get("properties", {})
            if not isinstance(check_properties, dict):
                errors.append(f"{schema_path}: checks_run item properties must be a mapping")
            else:
                for field_name in ("name", "evidence_ref", "work_state_ref"):
                    field = check_properties.get(field_name, {})
                    if not isinstance(field, dict) or field.get("minLength") != 1:
                        errors.append(f"{schema_path}: checks_run item `{field_name}` must require minLength 1")
                result = check_properties.get("result", {})
                if not isinstance(result, dict) or set(result.get("enum", [])) != {"passed", "failed", "skipped"}:
                    errors.append(f"{schema_path}: checks_run item result enum must be passed/failed/skipped")

    expected_all_of = [
        {
            "if": {"properties": {"status": {"const": "accepted"}}, "required": ["status"]},
            "then": {"properties": {"claim_may_be_made": {"const": True}}},
        },
        {
            "if": {"properties": {"status": {"const": "rejected"}}, "required": ["status"]},
            "then": {"properties": {"claim_may_be_made": {"const": False}}},
        },
        {
            "if": {
                "properties": {"claim_may_be_made": {"const": True}},
                "required": ["claim_may_be_made"],
            },
            "then": {
                "properties": {
                    "status": {"const": "accepted"},
                    "failed": {"maxItems": 0},
                    "remaining_unverified": {"maxItems": 0},
                    "checks_run": {
                        "items": {
                            "properties": {"result": {"const": "passed"}},
                            "required": ["result"],
                        }
                    },
                }
            },
        },
    ]
    all_of = schema.get("allOf")
    if not isinstance(all_of, list) or all(expected_rule in all_of for expected_rule in expected_all_of) is False:
        errors.append(
            f"{schema_path}: allOf must bind accepted/rejected status to claim_may_be_made and require passed-only proof when claims may be made"
        )

    if schema.get("additionalProperties") is not False:
        errors.append(f"{schema_path}: `additionalProperties` must be `false` to keep the verification contract closed")


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

    name = frontmatter.get("name")
    validate_skill_name(name, path, errors)
    if isinstance(name, str) and name != path.parent.name:
        errors.append(f"{path}: skill name `{name}` must match parent directory `{path.parent.name}`")

    description = frontmatter.get("description")
    if not isinstance(description, str):
        errors.append(f"{path}: `description` must be a string")
    else:
        if len(description) > DESCRIPTION_HARD_CAP:
            errors.append(
                f"{path}: `description` is {len(description)} characters; the hard cap is {DESCRIPTION_HARD_CAP} "
                f"to protect the shared discovery context budget (soft guidance: 280)"
            )
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

    prerequisites = metadata.get("prerequisites")
    if not isinstance(prerequisites, list):
        errors.append(f"{path}: `metadata.prerequisites` must be a list")
    else:
        for prerequisite in prerequisites:
            if not isinstance(prerequisite, str) or not prerequisite.startswith(SKILL_NAME_PREFIX):
                errors.append(
                    f"{path}: prerequisite `{prerequisite}` must be a canonical `pc-` skill name"
                )
            if isinstance(name, str) and prerequisite == name:
                errors.append(f"{path}: skill `{name}` must not list itself as a prerequisite")

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

    for match in MARKDOWN_SKILL_LINK_RE.finditer(body):
        target = match.group("target").split("#", 1)[0]
        if target.startswith(("http://", "https://")):
            continue
        linked_path = (skill_dir / target).resolve()
        if not linked_path.is_file():
            errors.append(f"{path}: referenced skill link `{target}` does not exist")

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
        if frontmatter.get("entry_skill") != "pc-intake":
            errors.append(f"{path}: `entry_skill` must be `pc-intake`")

        required_artifacts = frontmatter.get("required_artifacts", [])
        if not isinstance(required_artifacts, list) or "intake-brief" not in required_artifacts:
            errors.append(f"{path}: `required_artifacts` must include `intake-brief`")

        if "## Entry Gate" not in body:
            errors.append(f"{path}: missing `## Entry Gate` section")

        body_lower = body.lower()
        if "pc-intake" not in body_lower or "intake-brief" not in body_lower:
            errors.append(f"{path}: entry gate must mention both `pc-intake` and `intake-brief`")

        required_sections = ("Overview", "Phase Sequence", "Quality Gates", "Adaptation Notes")
        for section_name in required_sections:
            if not re.search(rf"^##\s+{re.escape(section_name)}\s*$", body, re.MULTILINE):
                errors.append(f"{path}: missing required workflow section `## {section_name}`")


def manifest_skill_names(manifest: dict) -> set[str]:
    return {item["name"] for item in manifest.get("skills", []) if isinstance(item, dict) and "name" in item}


def manifest_planned_skill_names(manifest: dict) -> set[str]:
    return {
        entry.get("name")
        for entry in manifest.get("planned_skills", [])
        if isinstance(entry, dict) and isinstance(entry.get("name"), str)
    }


def maturity_marker_violation(status: object, marker_present: bool) -> str | None:
    """Shared policy: how a skill's manifest status constrains prose maturity markers.

    Aligned with the workflow-reference rule on main: only draft skills carry
    an (experimental)/(planned) marker; any non-draft marker is stale.
    """
    if status == "draft" and not marker_present:
        return "is referenced without being explicitly marked as (experimental) or (planned)"
    if isinstance(status, str) and status != "draft" and marker_present:
        return f"is marked experimental/planned; sync the label with manifest status `{status}`"
    return None


def validate_manifest(errors: list[str]) -> dict:
    try:
        manifest = yaml.safe_load(MANIFEST_PATH.read_text()) or {}
    except Exception as exc:  # pragma: no cover - parse failure
        errors.append(f"{MANIFEST_PATH}: failed to parse YAML: {exc}")
        return {}

    skill_entries = manifest.get("skills", [])
    for entry in skill_entries:
        validate_skill_name(entry.get("name"), MANIFEST_PATH, errors)
        path = ROOT / entry["file"]
        if not path.exists():
            errors.append(f"{MANIFEST_PATH}: missing referenced skill file `{entry['file']}`")
            continue
        try:
            frontmatter, _body = load_frontmatter(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if frontmatter.get("name") != entry.get("name"):
            errors.append(
                f"{MANIFEST_PATH}: skill `{entry.get('name')}` does not match frontmatter name "
                f"`{frontmatter.get('name')}` in `{entry['file']}`"
            )

    for entry in manifest.get("workflows", []):
        path = ROOT / entry["file"]
        if not path.exists():
            errors.append(f"{MANIFEST_PATH}: missing referenced workflow file `{entry['file']}`")

    phase_ids = {
        entry.get("id")
        for entry in manifest.get("phases", [])
        if isinstance(entry, dict) and isinstance(entry.get("id"), str)
    }
    skill_names = manifest_skill_names(manifest)
    source_skill_names: set[str] = set()
    for path in iter_lifecycle_skill_paths():
        try:
            frontmatter, _body = load_frontmatter(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        name = frontmatter.get("name")
        if isinstance(name, str):
            source_skill_names.add(name)
    if source_skill_names != skill_names:
        missing_from_manifest = sorted(source_skill_names - skill_names)
        missing_from_source = sorted(skill_names - source_skill_names)
        if missing_from_manifest:
            errors.append(f"{MANIFEST_PATH}: source skills missing from manifest {missing_from_manifest}")
        if missing_from_source:
            errors.append(f"{MANIFEST_PATH}: manifest skills missing from source tree {missing_from_source}")

    for entry in skill_entries:
        name = entry.get("name")
        phase = entry.get("phase")
        expected_file = f"skills/{phase}/{name}/SKILL.md"
        if entry.get("file") != expected_file:
            errors.append(
                f"{MANIFEST_PATH}: skill `{name}` file must be `{expected_file}`"
            )

    planned_names: set[str] = set()
    planned_skills = manifest.get("planned_skills", [])
    if planned_skills is not None and not isinstance(planned_skills, list):
        errors.append(f"{MANIFEST_PATH}: `planned_skills` must be a list when present")
    for entry in planned_skills if isinstance(planned_skills, list) else []:
        if not isinstance(entry, dict):
            errors.append(f"{MANIFEST_PATH}: planned skill entries must be mappings")
            continue
        name = entry.get("name")
        phase = entry.get("phase")
        rationale = entry.get("rationale")
        if not isinstance(name, str) or not name:
            errors.append(f"{MANIFEST_PATH}: planned skill entries must include non-empty `name`")
            continue
        validate_skill_name(name, MANIFEST_PATH, errors)
        if name in planned_names:
            errors.append(f"{MANIFEST_PATH}: duplicate planned skill `{name}`")
        planned_names.add(name)
        if name in skill_names:
            errors.append(f"{MANIFEST_PATH}: planned skill `{name}` already exists in `skills`")
        if phase not in phase_ids and phase != "cross-cutting":
            errors.append(f"{MANIFEST_PATH}: planned skill `{name}` has invalid phase `{phase}`")
        if not isinstance(rationale, str) or not rationale:
            errors.append(f"{MANIFEST_PATH}: planned skill `{name}` must include rationale")

        target_file = entry.get("target_file")
        expected_target_file = f"skills/{phase}/{name}/SKILL.md"
        if target_file != expected_target_file:
            errors.append(
                f"{MANIFEST_PATH}: planned skill `{name}` target_file must be `{expected_target_file}`"
            )

    for entry in skill_entries:
        name = entry.get("name")
        path = ROOT / entry.get("file", "")
        if not isinstance(name, str) or not path.is_file():
            continue
        try:
            frontmatter, _body = load_frontmatter(path)
        except ValueError:
            continue
        prerequisites = frontmatter.get("metadata", {}).get("prerequisites", [])
        if not isinstance(prerequisites, list):
            errors.append(f"{path}: `metadata.prerequisites` must be a list")
            continue
        for prerequisite in prerequisites:
            if prerequisite not in skill_names:
                errors.append(
                    f"{path}: prerequisite `{prerequisite}` is not an implemented manifest skill"
                )

    for edge in manifest.get("iterative_feedback_edges", []):
        if not isinstance(edge, dict):
            errors.append(f"{MANIFEST_PATH}: iterative feedback edges must be mappings")
            continue
        for field in ("from", "to"):
            skill_name = edge.get(field)
            if skill_name not in skill_names:
                errors.append(
                    f"{MANIFEST_PATH}: iterative feedback edge `{field}` value `{skill_name}` "
                    "is not an implemented skill"
                )

    root_eval_configs = set((ROOT / "eval").glob("*/*/evals.json"))
    nested_eval_configs = set((ROOT / "eval").glob("*/*/evals/*.json"))
    for config_path in sorted(root_eval_configs | nested_eval_configs):
        try:
            payload = json.loads(config_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"{config_path}: active eval config is not valid JSON: {exc}")
            continue
        if config_path in root_eval_configs and (
            not isinstance(payload, dict) or not isinstance(payload.get("skill_name"), str)
        ):
            errors.append(f"{config_path}: active root eval config must declare string `skill_name`")
            continue
        if not isinstance(payload, dict) or "skill_name" not in payload:
            continue
        expected_skill_name = config_path.relative_to(ROOT / "eval").parts[1]
        if payload["skill_name"] != expected_skill_name:
            errors.append(
                f"{config_path}: active eval `skill_name` must be `{expected_skill_name}`, "
                f"got `{payload['skill_name']}`"
            )

    active_benchmarks = set((ROOT / "eval").glob("*/*/*benchmark*.json"))
    active_benchmarks.update((ROOT / "eval").glob("*/*/evals/*benchmark*.json"))
    for benchmark_path in sorted(active_benchmarks):
        try:
            benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"{benchmark_path}: active benchmark config is not valid JSON: {exc}")
            continue
        if not isinstance(benchmark, list):
            errors.append(f"{benchmark_path}: active benchmark config must be a list")
            continue
        for case in benchmark:
            if not isinstance(case, dict):
                errors.append(f"{benchmark_path}: benchmark cases must be objects")
                continue
            context_files = case.get("context_files", [])
            if not isinstance(context_files, list):
                errors.append(f"{benchmark_path}: `context_files` must be a list")
                continue
            for context_file in context_files:
                if not isinstance(context_file, str):
                    errors.append(f"{benchmark_path}: context file paths must be strings")
                    continue
                candidate = (benchmark_path.parent / context_file).resolve()
                try:
                    candidate.relative_to((ROOT / "eval").resolve())
                except ValueError:
                    errors.append(f"{benchmark_path}: context file escapes eval root: `{context_file}`")
                    continue
                if not candidate.is_file():
                    errors.append(f"{benchmark_path}: missing context file `{context_file}`")

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
                    continue
                if target.suffix == ".md":
                    text = target.read_text(encoding="utf-8")
                    for match in LOCAL_EVAL_FILE_RE.finditer(text):
                        local_path = match.group("path")
                        if any(marker in local_path for marker in ("*", "<", ">", "{", "}")):
                            continue
                        if not (ROOT / local_path).exists() and not _is_gitignored_local_artifact(local_path):
                            errors.append(
                                f"{target}: references missing local eval artifact `{local_path}`"
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

    skills = manifest_skill_names(manifest)
    planned_skills = manifest_planned_skill_names(manifest)
    allowed_skill_tokens = skills | planned_skills

    artifact_flow = {
        entry["artifact"]: {
            "produced_by": producer_set(entry.get("produced_by")),
            "consumed_by": set(entry.get("consumed_by", []) or []),
        }
        for entry in manifest.get("artifact_flow", [])
        if isinstance(entry, dict) and "artifact" in entry
    }

    for entry in manifest.get("artifact_flow", []):
        if not isinstance(entry, dict) or "artifact" not in entry:
            continue
        artifact = entry["artifact"]
        producers = producer_set(entry.get("produced_by"))
        if not producers:
            errors.append(f"{MANIFEST_PATH}: artifact_flow `{artifact}` must declare at least one produced_by skill")
        for producer in sorted(producers):
            if producer not in allowed_skill_tokens:
                errors.append(
                    f"{MANIFEST_PATH}: artifact_flow `{artifact}` produced_by references unknown skill `{producer}`"
                )
        consumers = entry.get("consumed_by", [])
        if not isinstance(consumers, list):
            errors.append(f"{MANIFEST_PATH}: artifact_flow `{artifact}` consumed_by must be a list")
            consumers = []
        for consumer in sorted(item for item in consumers if isinstance(item, str)):
            if consumer not in allowed_skill_tokens:
                errors.append(
                    f"{MANIFEST_PATH}: artifact_flow `{artifact}` consumed_by references unknown skill `{consumer}`"
                )

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
    planned_skills = manifest_planned_skill_names(manifest)
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
                    elif re.search(rf"`{re.escape(ref)}`\s*\((?:experimental|planned)\)", line, re.IGNORECASE):
                        errors.append(
                            f"{path}: non-draft skill `{ref}` is marked experimental/planned; sync the label with manifest status `{skill_status}`"
                        )

        refs = extract_backtick_refs(body)
        compatibility_tags = workflow_compatibility_tags(frontmatter.get("name", ""))
        for ref in sorted(ref for ref in refs if ref in skills):
            methods = skill_methods.get(ref, [])
            if methods and not compatibility_tags.intersection(methods):
                errors.append(
                    f"{path}: references skill `{ref}` but workflow `{frontmatter.get('name')}` is incompatible with metadata.methodologies {methods}"
                )

    validate_gateway_phase_skill_references(skills, planned_skills, manifest_skills, errors)


def validate_gateway_phase_skill_references(
    skills: set[str],
    planned_skills: set[str],
    manifest_skills: dict[str, dict],
    errors: list[str],
) -> None:
    text = GATEWAY_PATH.read_text(encoding="utf-8")
    match = re.search(
        r"### Priority 2: Phase-Specific Skills \(contextual\)\s*(?P<section>.*?)\n### ",
        text,
        re.DOTALL,
    )
    if not match:
        errors.append(f"{GATEWAY_PATH}: could not locate the phase-specific skill routing table")
        return

    for line in match.group("section").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "Likely Skills" in stripped or set(stripped.replace("|", "").strip()) == {"-"}:
            continue
        columns = [item.strip() for item in stripped.split("|")[1:-1]]
        if len(columns) != 3:
            continue
        for raw_token in columns[2].split(","):
            token_text = raw_token.strip()
            if not token_text or token_text.lower() == "none":
                continue
            is_marked_planned = bool(re.search(r"\((?:experimental|planned)\)", token_text, re.IGNORECASE))
            token = re.sub(r"\s*\((?:experimental|planned)\)\s*", "", token_text, flags=re.IGNORECASE).strip("` ")
            if token in skills:
                status = manifest_skills.get(token, {}).get("status")
                if status == "draft" and not is_marked_planned:
                    errors.append(f"{GATEWAY_PATH}: draft skill `{token}` in routing table must be marked experimental/planned")
                if status != "draft" and is_marked_planned:
                    errors.append(
                        f"{GATEWAY_PATH}: non-draft skill `{token}` in routing table is marked experimental/planned; manifest status is `{status}`"
                    )
            elif token in planned_skills:
                if not is_marked_planned:
                    errors.append(f"{GATEWAY_PATH}: planned skill `{token}` in routing table must be marked planned")
            else:
                errors.append(f"{GATEWAY_PATH}: routing table references undefined skill `{token}`")


PROTOCOL_RESULT_CONTRACTS = {
    "execution-authority-result": {
        "version": "execution-authority-result.v1",
        "statuses": ("valid", "approval-required", "invalid"),
        "required": {
            "schema_version",
            "status",
            "authority",
            "candidate_completion_digest",
            "errors",
        },
    },
    "execution-authoring-result": {
        "version": "execution-authoring-result.v1",
        "statuses": ("written", "candidate", "recovery-required", "invalid"),
        "required": {
            "schema_version",
            "status",
            "operation",
            "mutations",
            "state_revision",
            "candidate_route_digest",
            "candidate_completion_digest",
            "capacities",
            "warnings",
            "errors",
        },
    },
}

PROTOCOL_AUTHORING_OPERATIONS = (
    "route-draft",
    "state-init",
    "transition",
    "phase-event",
    "artifact-bind",
    "claim-completion",
    "record-outcome",
    "reroute",
)

PROTOCOL_AUTHORITY_VALUES = ("gate-authorized", "terminal-authorized")
PROTOCOL_MUTATION_ACTIONS = ("create", "replace", "remove")


def validate_closed_schema_objects(schema: object, schema_path: Path, errors: list[str], location: str = "$") -> None:
    if isinstance(schema, dict):
        if schema.get("type") == "object" and schema.get("additionalProperties") is not False:
            errors.append(f"{schema_path}: schema object `{location}` must be a closed object")
        for key, value in schema.items():
            validate_closed_schema_objects(value, schema_path, errors, f"{location}/{key}")
    elif isinstance(schema, list):
        for index, value in enumerate(schema):
            validate_closed_schema_objects(value, schema_path, errors, f"{location}/{index}")


def validate_protocol_schema_contract(
    result_name: str,
    entry: dict,
    schema: dict,
    schema_path: Path,
    errors: list[str],
) -> None:
    contract = PROTOCOL_RESULT_CONTRACTS[result_name]
    version = contract["version"]
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        errors.append(f"{schema_path}: properties must be an object")
        return
    schema_version_contract = properties.get("schema_version")
    schema_version = (
        schema_version_contract.get("const")
        if isinstance(schema_version_contract, dict)
        else None
    )
    if entry.get("schema_version") != schema_version:
        errors.append(
            f"{PROTOCOL_RESULT_REGISTRY_PATH}: result `{result_name}` registry version "
            f"`{entry.get('schema_version')}` does not match schema const `{schema_version}`"
        )
    if schema_version != version:
        errors.append(f"{schema_path}: schema_version const must be `{version}`")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append(f"{schema_path}: must declare JSON Schema draft 2020-12")
    if set(schema.get("required", [])) != contract["required"]:
        errors.append(f"{schema_path}: required result fields must be {sorted(contract['required'])}")
    if set(properties) != contract["required"]:
        errors.append(f"{schema_path}: declared result fields must be exactly {sorted(contract['required'])}")
    status_contract = properties.get("status")
    status_values = status_contract.get("enum") if isinstance(status_contract, dict) else None
    if status_values != list(contract["statuses"]):
        errors.append(f"{schema_path}: status enum must be {sorted(contract['statuses'])}")
    definitions = schema.get("$defs")
    if not isinstance(definitions, dict):
        definitions = {}
    sha256 = definitions.get("sha256")
    if sha256 != {"type": "string", "pattern": r"^sha256:[0-9a-f]{64}$"}:
        errors.append(f"{schema_path}: sha256 must require lowercase prefixed 64-hex digests")
    validate_closed_schema_objects(schema, schema_path, errors)

    if result_name != "execution-authoring-result":
        authority_contract = properties.get("authority")
        authority_branches = (
            authority_contract.get("oneOf") if isinstance(authority_contract, dict) else None
        )
        authority_values = None
        if (
            isinstance(authority_branches, list)
            and authority_branches
            and isinstance(authority_branches[0], dict)
        ):
            authority_values = authority_branches[0].get("enum")
        if authority_values != list(PROTOCOL_AUTHORITY_VALUES):
            errors.append(f"{schema_path}: authority enum must be gate-authorized/terminal-authorized")
        validate_protocol_status_contract(result_name, schema, schema_path, errors)
        return
    operation_contract = properties.get("operation")
    operations = operation_contract.get("enum") if isinstance(operation_contract, dict) else None
    if operations != list(PROTOCOL_AUTHORING_OPERATIONS):
        errors.append(f"{schema_path}: operation enum must be {sorted(PROTOCOL_AUTHORING_OPERATIONS)}")
    revision_contract = properties.get("state_revision")
    revision_branches = (
        revision_contract.get("oneOf") if isinstance(revision_contract, dict) else None
    )
    if not isinstance(revision_branches, list):
        revision_branches = []
    if {"type": "integer", "minimum": 1} not in revision_branches or {"type": "null"} not in revision_branches:
        errors.append(f"{schema_path}: state_revision must be null or an integer with minimum 1")

    mutation = definitions.get("mutation", {})
    if not isinstance(mutation, dict):
        mutation = {}
    if set(mutation.get("required", [])) != {"action", "path"}:
        errors.append(f"{schema_path}: mutation must require exactly action and path")
    mutation_properties = mutation.get("properties")
    if not isinstance(mutation_properties, dict):
        mutation_properties = {}
    if set(mutation_properties) != {"action", "path"}:
        errors.append(f"{schema_path}: mutation fields must be exactly action and path")
    action_contract = mutation_properties.get("action")
    actions = action_contract.get("enum") if isinstance(action_contract, dict) else None
    if actions != list(PROTOCOL_MUTATION_ACTIONS):
        errors.append(f"{schema_path}: mutation action enum must be create/replace/remove")
    capacity = definitions.get("capacity", {})
    if not isinstance(capacity, dict):
        capacity = {}
    expected_capacity_fields = {
        "path",
        "used_bytes",
        "warning_bytes",
        "limit_bytes",
        "remaining_bytes",
    }
    if set(capacity.get("required", [])) != expected_capacity_fields:
        errors.append(f"{schema_path}: capacity must require {sorted(expected_capacity_fields)}")
    capacity_properties = capacity.get("properties")
    if not isinstance(capacity_properties, dict):
        capacity_properties = {}
    if set(capacity_properties) != expected_capacity_fields:
        errors.append(f"{schema_path}: capacity fields must be exactly {sorted(expected_capacity_fields)}")
    warning_contract = capacity_properties.get("warning_bytes")
    warning_bytes = warning_contract.get("const") if isinstance(warning_contract, dict) else None
    if warning_bytes != 12 * 1024 * 1024:
        errors.append(f"{schema_path}: capacity warning_bytes must be exactly 12582912")
    limit_contract = capacity_properties.get("limit_bytes")
    limit_bytes = limit_contract.get("const") if isinstance(limit_contract, dict) else None
    if limit_bytes != 16 * 1024 * 1024:
        errors.append(f"{schema_path}: capacity limit_bytes must be exactly 16777216")
    validate_protocol_status_contract(result_name, schema, schema_path, errors)


def _protocol_status_fixtures(result_name: str) -> tuple[list[dict], list[dict]]:
    digest = "sha256:" + ("a" * 64)
    if result_name == "execution-authority-result":
        valid: list[dict] = [
            {
                "schema_version": "execution-authority-result.v1",
                "status": "valid",
                "authority": "gate-authorized",
                "candidate_completion_digest": None,
                "errors": [],
            },
            {
                "schema_version": "execution-authority-result.v1",
                "status": "approval-required",
                "authority": None,
                "candidate_completion_digest": digest,
                "errors": ["pin required"],
            },
            {
                "schema_version": "execution-authority-result.v1",
                "status": "invalid",
                "authority": None,
                "candidate_completion_digest": None,
                "errors": ["invalid"],
            },
        ]
        invalid_fixtures: list[dict] = [
            {**valid[0], "errors": ["unexpected"]},
            {**valid[1], "candidate_completion_digest": None},
            {**valid[1], "authority": "gate-authorized"},
            {**valid[2], "authority": "gate-authorized"},
            {**valid[2], "candidate_completion_digest": digest},
            {**valid[2], "errors": []},
        ]
        return valid, invalid_fixtures

    mutation: dict = {
        "action": "replace",
        "path": ".prodcraft/artifacts/work-1/execution-state.json",
    }
    base: dict = {
        "schema_version": "execution-authoring-result.v1",
        "operation": "transition",
        "state_revision": 2,
        "candidate_route_digest": None,
        "candidate_completion_digest": None,
        "capacities": [],
        "warnings": [],
        "errors": [],
    }
    written: dict = {**base, "status": "written", "mutations": [mutation]}
    candidate: dict = {
        **base,
        "status": "candidate",
        "mutations": [mutation],
        "candidate_route_digest": digest,
    }
    completion_candidate: dict = {
        **base,
        "status": "candidate",
        "mutations": [mutation],
        "candidate_completion_digest": digest,
    }
    recovery: dict = {
        **base,
        "status": "recovery-required",
        "mutations": [],
        "errors": ["manual recovery required"],
    }
    invalid_result: dict = {
        **base,
        "status": "invalid",
        "mutations": [],
        "errors": ["invalid"],
    }
    invalid_fixtures = [
        {**written, "errors": ["unexpected"]},
        {**written, "candidate_route_digest": digest},
        {**written, "mutations": []},
        {**candidate, "candidate_route_digest": None},
        {**candidate, "errors": ["unexpected"]},
        {**candidate, "mutations": []},
        {
            **candidate,
            "candidate_route_digest": None,
            "candidate_completion_digest": digest,
            "mutations": [],
        },
        {**recovery, "candidate_completion_digest": digest},
        {**recovery, "candidate_route_digest": digest},
        {**recovery, "errors": []},
        {**invalid_result, "mutations": [mutation]},
        {**invalid_result, "candidate_route_digest": digest},
        {**invalid_result, "candidate_completion_digest": digest},
        {**invalid_result, "errors": []},
        {
            **written,
            "mutations": [{"action": "replace", "path": "bad\x00path"}],
        },
    ]
    return [written, candidate, completion_candidate, recovery, invalid_result], invalid_fixtures


def validate_protocol_status_contract(
    result_name: str,
    schema: dict,
    schema_path: Path,
    errors: list[str],
) -> None:
    import jsonschema  # type: ignore[import-untyped]

    validator = jsonschema.Draft202012Validator(schema)
    valid_fixtures, invalid_fixtures = _protocol_status_fixtures(result_name)
    if any(not validator.is_valid(payload) for payload in valid_fixtures):
        errors.append(f"{schema_path}: status contract rejects a representative valid result")
    if any(validator.is_valid(payload) for payload in invalid_fixtures):
        errors.append(f"{schema_path}: status contract accepts a contradictory result")


def _load_protocol_result_schema(
    result_name: str,
    errors: list[str],
    *,
    root: Path,
    registry_path: Path,
) -> dict | None:
    registry = load_unique_yaml_mapping(registry_path, errors)
    results = registry.get("results", {})
    if not isinstance(results, dict):
        errors.append(f"{registry_path}: `results` must be a mapping")
        return None
    entry = results.get(result_name)
    if not isinstance(entry, dict):
        errors.append(f"{registry_path}: result `{result_name}` is not registered")
        return None
    schema_rel = entry.get("schema_path")
    schema_path = resolve_protocol_schema_path(root, schema_rel, registry_path, errors)
    if schema_path is None:
        return None
    if not isinstance(schema_rel, str):
        return None
    try:
        schema = load_protocol_schema_snapshot(root, schema_rel, schema_path)
    except StrictJSONError as exc:
        errors.append(f"{schema_path}: failed to parse JSON schema: {exc}")
        return None
    return schema


def validate_protocol_result_registry(
    errors: list[str],
    *,
    root: Path = ROOT,
    registry_path: Path | None = None,
) -> None:
    registry_path = registry_path or root / "schemas" / "protocol" / "registry.yml"
    registry = load_unique_yaml_mapping(registry_path, errors)
    if not registry:
        return
    if set(registry) != {"schema_version", "results"}:
        errors.append(f"{registry_path}: registry must contain exactly schema_version and results")
    if registry.get("schema_version") != "protocol-result-registry.v1":
        errors.append(f"{registry_path}: `schema_version` must be `protocol-result-registry.v1`")
    results = registry.get("results", {})
    if not isinstance(results, dict):
        errors.append(f"{registry_path}: `results` must be a mapping")
        return
    if set(results) != set(PROTOCOL_RESULT_CONTRACTS):
        errors.append(f"{registry_path}: results must be {sorted(PROTOCOL_RESULT_CONTRACTS)}")
    try:
        import jsonschema  # type: ignore[import-untyped]
    except ImportError as exc:
        errors.append(f"{registry_path}: jsonschema is required to validate protocol schemas: {exc}")
        return

    for result_name in sorted(PROTOCOL_RESULT_CONTRACTS):
        entry = results.get(result_name)
        if not isinstance(entry, dict):
            errors.append(f"{registry_path}: result `{result_name}` must map to a metadata object")
            continue
        if set(entry) != {"schema_version", "schema_path"}:
            errors.append(f"{registry_path}: result `{result_name}` must contain exactly schema_version and schema_path")
        expected_path = f"schemas/protocol/{result_name}.v1.schema.json"
        if entry.get("schema_path") != expected_path:
            if isinstance(entry.get("schema_path"), str):
                errors.append(f"{registry_path}: result `{result_name}` must use schema_path `{expected_path}`")
        schema_rel = entry.get("schema_path")
        schema_path = resolve_protocol_schema_path(root, schema_rel, registry_path, errors)
        if schema_path is None:
            continue
        if not isinstance(schema_rel, str):
            continue
        try:
            schema = load_protocol_schema_snapshot(root, schema_rel, schema_path)
        except StrictJSONError as exc:
            errors.append(f"{schema_path}: failed to parse JSON schema: {exc}")
            continue
        try:
            jsonschema.Draft202012Validator.check_schema(schema)
        except jsonschema.SchemaError as exc:
            errors.append(f"{schema_path}: invalid JSON schema: {exc.message}")
            continue
        validate_protocol_schema_contract(result_name, entry, schema, schema_path, errors)


def validate_protocol_result_status_semantics(
    result_name: str,
    payload: dict,
    errors: list[str],
) -> None:
    status = payload.get("status")
    result_errors = payload.get("errors")
    has_errors = isinstance(result_errors, list) and bool(result_errors)
    if result_name == "execution-authority-result":
        authority = payload.get("authority")
        candidate = payload.get("candidate_completion_digest")
        if status == "valid" and (candidate is not None or has_errors):
            errors.append(f"{result_name}: valid status forbids candidates and errors")
        elif status == "approval-required" and (
            authority is not None or candidate is None or not has_errors
        ):
            errors.append(
                f"{result_name}: approval-required status requires only a completion candidate"
            )
        elif status == "invalid" and (
            authority is not None or candidate is not None or not has_errors
        ):
            errors.append(f"{result_name}: invalid status forbids authority and candidates")
        return

    mutations = payload.get("mutations")
    has_mutations = isinstance(mutations, list) and bool(mutations)
    route_candidate = payload.get("candidate_route_digest")
    completion_candidate = payload.get("candidate_completion_digest")
    has_candidate = route_candidate is not None or completion_candidate is not None
    if status == "written" and (not has_mutations or has_candidate or has_errors):
        errors.append(
            f"{result_name}: written status requires mutations and forbids candidates and errors"
        )
    elif status == "candidate" and (not has_mutations or not has_candidate or has_errors):
        errors.append(
            f"{result_name}: candidate status requires mutations and a candidate without errors"
        )
    elif status == "recovery-required" and (has_candidate or not has_errors):
        errors.append(
            f"{result_name}: recovery-required status forbids candidates and requires errors"
        )
    elif status == "invalid" and (has_mutations or has_candidate or not has_errors):
        errors.append(
            f"{result_name}: invalid status requires empty mutations, no candidates, and errors"
        )


def validate_protocol_result_instance(
    result_name: str,
    payload: object,
    errors: list[str],
    *,
    root: Path = ROOT,
    registry_path: Path | None = None,
) -> None:
    registry_path = registry_path or root / "schemas" / "protocol" / "registry.yml"
    schema = _load_protocol_result_schema(
        result_name,
        errors,
        root=root,
        registry_path=registry_path,
    )
    if schema is None:
        return
    try:
        import jsonschema  # type: ignore[import-untyped]
    except ImportError as exc:
        errors.append(f"{registry_path}: jsonschema is required to validate protocol results: {exc}")
        return
    try:
        jsonschema.Draft202012Validator(schema).validate(payload)
    except jsonschema.ValidationError as exc:
        location = "/".join(str(part) for part in exc.absolute_path) or "<root>"
        errors.append(f"{result_name}: invalid result at `{location}`: {exc.message}")

    if not isinstance(payload, dict):
        return
    validate_protocol_result_status_semantics(result_name, payload, errors)
    if result_name != "execution-authoring-result":
        return
    for field_name in ("mutations", "capacities"):
        entries = payload.get(field_name)
        if not isinstance(entries, list):
            continue
        seen_paths: set[str] = set()
        for entry in entries:
            if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
                continue
            path = entry["path"]
            if "\x00" in path:
                errors.append(f"{result_name}: {field_name} path contains a NUL byte")
            if path in seen_paths:
                errors.append(f"{result_name}: duplicate {field_name} path `{path}`")
            seen_paths.add(path)
    capacities = payload.get("capacities")
    if isinstance(capacities, list):
        for index, capacity in enumerate(capacities):
            if not isinstance(capacity, dict):
                continue
            used = capacity.get("used_bytes")
            limit = capacity.get("limit_bytes")
            remaining = capacity.get("remaining_bytes")
            if (
                not isinstance(used, int)
                or isinstance(used, bool)
                or not isinstance(limit, int)
                or isinstance(limit, bool)
                or not isinstance(remaining, int)
                or isinstance(remaining, bool)
            ):
                continue
            if used > limit:
                errors.append(f"{result_name}: capacities[{index}] used_bytes exceeds limit_bytes")
            if remaining != limit - used:
                errors.append(f"{result_name}: capacities[{index}] remaining_bytes must equal limit_bytes - used_bytes")


def _skill_name_occurrences(name: str, line: str) -> list[re.Match]:
    """Occurrences of a skill name as a standalone token.

    Lookarounds treat `-` as part of the token, so `migration-strategy` does
    not match inside `data-migration-strategy`. Ordinary-English collisions
    with a planned skill name (e.g. prose using the word `deprecation`) can
    still fire; that is an accepted loud false positive -- rephrase the prose
    or mark the skill.
    """
    pattern = rf"(?<![\w-])`?{re.escape(name)}`?(?![\w-])"
    return list(re.finditer(pattern, line))


def _occurrence_has_marker(line: str, match: re.Match) -> bool:
    return bool(re.match(r"\s*\((?:experimental|planned)\)", line[match.end():], re.IGNORECASE))


def validate_gateway_references(manifest: dict, errors: list[str]) -> None:
    """Keep gateway routing honest about skill maturity.

    The gateway is the highest-frequency routing document, so a skill name that
    does not resolve (or resolves to an unshipped skill without a marker) sends
    agents to a dead end. Prose uses many non-skill tokens, so this check only
    asserts on names that are known manifest or planned skills, and each
    occurrence must carry its own marker (a marker elsewhere on the line does
    not exempt it).
    """
    text = GATEWAY_PATH.read_text(encoding="utf-8")
    manifest_skills = {
        entry["name"]: entry
        for entry in manifest.get("skills", [])
        if isinstance(entry, dict) and "name" in entry
    }
    planned_names = manifest_planned_skill_names(manifest)
    for line_number, line in enumerate(text.splitlines(), start=1):
        for name in sorted(planned_names):
            for match in _skill_name_occurrences(name, line):
                if not _occurrence_has_marker(line, match):
                    errors.append(
                        f"{GATEWAY_PATH}:{line_number}: planned skill `{name}` must be marked (planned) where the gateway mentions it"
                    )
        for name, entry in manifest_skills.items():
            status = entry.get("status")
            for match in _skill_name_occurrences(name, line):
                violation = maturity_marker_violation(status, _occurrence_has_marker(line, match))
                if violation:
                    errors.append(f"{GATEWAY_PATH}:{line_number}: skill `{name}` {violation}")


def validate_doc_script_refs(errors: list[str]) -> None:
    """Every `scripts/*.py` mentioned in operative docs must exist.

    A dangling script reference turns a documented procedure into an
    unexecutable one without any signal. Historical documents under docs/ and
    eval/ are excluded; they may legitimately cite superseded paths.
    """
    doc_paths = [
        ROOT / "README.md",
        ROOT / "README.zh-CN.md",
        ROOT / "CLAUDE.md",
        ROOT / "AGENTS.md",
    ]
    doc_paths.extend(sorted(WORKFLOWS_DIR.glob("*.md")))
    doc_paths.extend(
        sorted(
            path
            for path in SKILLS_DIR.rglob("*.md")
            if ".curated" not in path.parts
        )
    )
    for path in doc_paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for script_ref in sorted(set(_SCRIPT_REF_RE.findall(text))):
            if not (ROOT / script_ref).exists() and not (path.parent / script_ref).exists():
                errors.append(f"{path}: references missing script `{script_ref}`")


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
        if artifact_name == "verification-record":
            validate_verification_record_schema_contract(schema, schema_path, errors)
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


def validate_markdown_script_references(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in {".git", "build", "__pycache__"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"(?<![\w/-])(scripts/[A-Za-z0-9_./-]+\.py)", text):
            rel_path = match.group(1)
            if not (ROOT / rel_path).exists():
                errors.append(f"{path}: references missing script `{rel_path}`")


def validate_examples_reference_contract(manifest: dict, errors: list[str]) -> None:
    examples_path = ROOT / "examples" / "README.md"
    if not examples_path.exists():
        return

    allowed = manifest_skill_names(manifest) | manifest_planned_skill_names(manifest)
    text = examples_path.read_text(encoding="utf-8")
    for line_number, line in enumerate(text.splitlines(), start=1):
        if "Key skills:" not in line:
            continue
        _, raw_skills = line.split("Key skills:", 1)
        for raw_token in raw_skills.split(","):
            token = raw_token.strip().strip(".")
            if not token:
                continue
            skill_name = re.sub(r"\s*\([^)]*\)\s*", "", token).strip("` ")
            if skill_name and skill_name not in allowed:
                errors.append(
                    f"{examples_path}:{line_number}: Key skills references unknown skill `{skill_name}`"
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

    try:
        portability_registry = json.loads(PUBLIC_SKILL_PORTABILITY_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{PUBLIC_SKILL_PORTABILITY_PATH}: file does not exist")
        return
    except Exception as exc:
        errors.append(f"{PUBLIC_SKILL_PORTABILITY_PATH}: failed to parse JSON: {exc}")
        return

    if not isinstance(portability_registry, dict):
        errors.append(f"{PUBLIC_SKILL_PORTABILITY_PATH}: expected a JSON object")
        return
    if portability_registry.get("schema_version") != "public-skill-portability.v1":
        errors.append(f"{PUBLIC_SKILL_PORTABILITY_PATH}: `schema_version` must be `public-skill-portability.v1`")
    portability_entries_raw = portability_registry.get("skills", [])
    if not isinstance(portability_entries_raw, list):
        errors.append(f"{PUBLIC_SKILL_PORTABILITY_PATH}: `skills` must be a list")
        return

    portability_entries: dict[str, dict] = {}
    portability_names: set[str] = set()
    for entry in portability_entries_raw:
        if not isinstance(entry, dict):
            errors.append(f"{PUBLIC_SKILL_PORTABILITY_PATH}: each portability entry must be an object")
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not name:
            errors.append(f"{PUBLIC_SKILL_PORTABILITY_PATH}: each portability entry must include non-empty `name`")
            continue
        validate_skill_name(name, PUBLIC_SKILL_PORTABILITY_PATH, errors)
        if name in portability_names:
            errors.append(f"{PUBLIC_SKILL_PORTABILITY_PATH}: duplicate portability entry `{name}`")
        portability_names.add(name)
        portability_entries[name] = entry

        portability = entry.get("portability")
        hidden_dependencies = entry.get("hidden_dependencies")
        required_context = entry.get("required_context")
        public_caveat_text = entry.get("public_caveat_text")
        if portability not in PUBLIC_SURFACE_PORTABILITY:
            errors.append(
                f"{PUBLIC_SKILL_PORTABILITY_PATH}: portability entry `{name}` has invalid portability `{portability}`; expected one of {sorted(PUBLIC_SURFACE_PORTABILITY)}"
            )
        if not isinstance(hidden_dependencies, list) or any(not isinstance(item, str) or not item for item in hidden_dependencies):
            errors.append(f"{PUBLIC_SKILL_PORTABILITY_PATH}: portability entry `{name}` must include a string `hidden_dependencies` list")
        if not isinstance(required_context, str):
            errors.append(f"{PUBLIC_SKILL_PORTABILITY_PATH}: portability entry `{name}` must include string `required_context`")
        if not isinstance(public_caveat_text, str):
            errors.append(f"{PUBLIC_SKILL_PORTABILITY_PATH}: portability entry `{name}` must include string `public_caveat_text`")
        if portability == "portable_as_is":
            if hidden_dependencies != []:
                errors.append(f"{PUBLIC_SKILL_PORTABILITY_PATH}: portable_as_is entry `{name}` must not declare hidden dependencies")
            if public_caveat_text != "":
                errors.append(f"{PUBLIC_SKILL_PORTABILITY_PATH}: portable_as_is entry `{name}` must not declare public caveat text")
        if portability == "portable_with_caveat":
            if not isinstance(required_context, str) or not required_context:
                errors.append(f"{PUBLIC_SKILL_PORTABILITY_PATH}: portable_with_caveat entry `{name}` must include required_context")
            if not isinstance(public_caveat_text, str) or not public_caveat_text:
                errors.append(f"{PUBLIC_SKILL_PORTABILITY_PATH}: portable_with_caveat entry `{name}` must include public_caveat_text")

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
    index_entries = {
        entry.get("name"): entry
        for entry in index.get("skills", [])
        if isinstance(entry, dict) and isinstance(entry.get("name"), str)
    }
    index_names = set(index_entries)
    manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8")) or {}
    manifest_skills = {
        entry["name"]: entry
        for entry in manifest.get("skills", [])
        if isinstance(entry, dict) and "name" in entry
    }
    all_public_names = {
        entry["name"]
        for entry in public_skills
        if isinstance(entry, dict) and "name" in entry
    }
    names: set[str] = set()
    for entry in public_skills:
        if not isinstance(entry, dict) or "name" not in entry or "source" not in entry or "stability" not in entry or "readiness" not in entry:
            errors.append(f"{DISTRIBUTION_REGISTRY_PATH}: each public skill entry must include `name`, `source`, `stability`, and `readiness`")
            continue
        name = entry["name"]
        validate_skill_name(name, DISTRIBUTION_REGISTRY_PATH, errors)
        stability = entry["stability"]
        readiness = entry["readiness"]
        if name in names:
            errors.append(f"{DISTRIBUTION_REGISTRY_PATH}: duplicate public skill `{name}`")
        names.add(name)
        if stability not in PUBLIC_SURFACE_STABILITIES:
            errors.append(
                f"{DISTRIBUTION_REGISTRY_PATH}: public skill `{name}` has invalid `stability` `{stability}`; expected one of {sorted(PUBLIC_SURFACE_STABILITIES)}"
            )
        if readiness not in PUBLIC_SURFACE_READINESS:
            errors.append(
                f"{DISTRIBUTION_REGISTRY_PATH}: public skill `{name}` has invalid `readiness` `{readiness}`; expected one of {sorted(PUBLIC_SURFACE_READINESS)}"
            )
        portability_entry = portability_entries.get(name)
        if portability_entry is None:
            errors.append(f"{PUBLIC_SKILL_PORTABILITY_PATH}: missing portability metadata for exported public skill `{name}`")
        elif portability_entry.get("portability") == "blocked":
            errors.append(f"{PUBLIC_SKILL_PORTABILITY_PATH}: exported public skill `{name}` must not be classified as blocked")
        if name not in index_names:
            errors.append(f"{index_path}: curated surface index is missing `{name}`")
        else:
            index_entry = index_entries[name]
            if index_entry.get("stability") != stability:
                errors.append(f"{index_path}: curated surface index entry `{name}` has mismatched `stability`")
            if index_entry.get("readiness") != readiness:
                errors.append(f"{index_path}: curated surface index entry `{name}` has mismatched `readiness`")
            if portability_entry is not None:
                portability = portability_entry.get("portability")
                public_caveat = portability_entry.get("public_caveat_text", "")
                if index_entry.get("portability") != portability:
                    errors.append(f"{index_path}: curated surface index entry `{name}` has mismatched `portability`")
                if public_caveat and index_entry.get("public_caveat_text") != public_caveat:
                    errors.append(f"{index_path}: curated surface index entry `{name}` has mismatched `public_caveat_text`")
                if not public_caveat and "public_caveat_text" in index_entry:
                    errors.append(f"{index_path}: curated surface index entry `{name}` must not include empty public caveat text")
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
            status = skill_meta.get("status")
            if readiness == "core" and status not in {"tested", "secure", "production"}:
                errors.append(
                    f"{DISTRIBUTION_REGISTRY_PATH}: public skill `{name}` is marked `core` but manifest status is `{status}`"
                )
            if readiness == "beta" and status == "draft":
                errors.append(
                    f"{DISTRIBUTION_REGISTRY_PATH}: public skill `{name}` is marked `beta` but manifest status is still `draft`; use `experimental` or graduate the skill first"
                )
            if readiness == "experimental" and not manual_allowlist:
                errors.append(
                    f"{DISTRIBUTION_REGISTRY_PATH}: experimental public skill `{name}` must set `manual_allowlist: true`"
                )
        text = skill_file.read_text(encoding="utf-8")
        for rel_target in re.findall(r"\((references|scripts|assets)/([^)]+)\)", text):
            bundled_path = skill_dir / rel_target[0] / rel_target[1]
            if not bundled_path.exists():
                errors.append(f"{skill_file}: curated reference `{bundled_path.relative_to(ROOT)}` does not exist")

        # Cross-skill links must stay installable: no links escaping into the
        # lifecycle source tree, and sibling links must target exported packages.
        if re.search(r"\]\((?:\.\./){2,}", text):
            errors.append(
                f"{skill_file}: curated body links into the lifecycle source tree (`../../...`); "
                f"the exporter must rewrite cross-skill links"
            )
        for sibling_name in re.findall(r"\]\(\.\./([a-z0-9-]+)/SKILL\.md\)", text):
            if sibling_name not in all_public_names:
                errors.append(
                    f"{skill_file}: curated sibling link targets `{sibling_name}`, which is not an exported public skill"
                )
        if portability_entry is not None:
            expected_caveat = portability_entry.get("public_caveat_text", "")
            if expected_caveat and expected_caveat not in text:
                errors.append(
                    f"{skill_file}: curated body must carry its public caveat text so the caveat travels with the skill"
                )

    extra_portability_names = sorted(portability_names - names)
    if extra_portability_names:
        errors.append(
            f"{PUBLIC_SKILL_PORTABILITY_PATH}: portability metadata includes non-exported public skills {extra_portability_names[:10]}"
        )

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
        choices=LEGACY_CHECK_CHOICES,
        help="Run only the named check. May be repeated. Defaults to all checks.",
    )
    parser.add_argument(
        "--artifact-instance",
        action="append",
        type=Path,
        default=[],
        help="Validate a JSON or YAML protocol artifact instance against the artifact registry and schema.",
    )
    parser.add_argument(
        "--authorize-execution-state",
        type=Path,
        help="Authorize the canonical current execution-state against its bound route and live Git worktree.",
    )
    parser.add_argument(
        "--approved-route-digest",
        help="Operator-supplied sha256 pin for --authorize-execution-state.",
    )
    parser.add_argument(
        "--approved-completion-digest",
        help="Operator-supplied terminal-authority digest pin for verified/completed state.",
    )
    parser.add_argument(
        "--output-format",
        choices=("text", "json"),
        default="text",
        help="Render the validation result as human-readable text or stable JSON.",
    )
    args = parser.parse_args()

    if args.approved_route_digest and args.authorize_execution_state is None:
        parser.error("--approved-route-digest requires --authorize-execution-state")
    if args.approved_completion_digest and args.authorize_execution_state is None:
        parser.error("--approved-completion-digest requires --authorize-execution-state")

    selected_checks = set(
        args.check
        or ([] if args.authorize_execution_state is not None and not args.artifact_instance else CHECKS)
    )
    errors: list[str] = []

    _MANIFEST_DEPENDENT_CHECKS = {
        "manifest-files",
        "workflow-skill-refs",
        "gateway-refs",
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

    if "gateway-refs" in selected_checks and manifest:
        validate_gateway_references(manifest, errors)

    if "doc-script-refs" in selected_checks:
        validate_doc_script_refs(errors)

    if "manifest-skill-status" in selected_checks and manifest:
        validate_manifest_skill_status(manifest, errors)

    if "artifact-flow" in selected_checks and manifest:
        validate_artifact_flow(manifest, errors)

    if "artifact-schema-registry" in selected_checks and manifest:
        validate_artifact_schema_registry(manifest, errors)

    if "protocol-result-registry" in selected_checks:
        validate_protocol_result_registry(errors)

    if "manifest-files" in selected_checks:
        validate_markdown_script_references(errors)
        if manifest:
            validate_examples_reference_contract(manifest, errors)

    if "cross-cutting-matrix" in selected_checks and manifest:
        validate_cross_cutting_matrix(manifest, errors)

    if "curated-surface" in selected_checks:
        validate_curated_surface(errors)

    for artifact_instance in args.artifact_instance:
        validate_artifact_instance(artifact_instance, errors)

    authority_result = None
    if args.authorize_execution_state is not None:
        authority_result = authorize_execution_state(
            args.authorize_execution_state,
            args.approved_route_digest,
            args.approved_completion_digest,
            errors,
        )

    if args.output_format == "json":
        authority = None
        candidate_completion_digest = None
        if (
            authority_result is not None
            and authority_result.disposition is ValidationDisposition.VALID
        ):
            authority = authority_result.authority
        if (
            authority_result is not None
            and authority_result.disposition is ValidationDisposition.APPROVAL_REQUIRED
        ):
            candidate_completion_digest = authority_result.candidate_completion_digest
        print(
            json.dumps(
                {
                    "status": "invalid" if errors else "valid",
                    "authority": authority,
                    "candidate_completion_digest": candidate_completion_digest,
                    "errors": errors,
                },
                sort_keys=True,
            )
        )
        return 1 if errors else 0

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    if authority_result is not None:
        print(authority_result.authority)
    else:
        print("Prodcraft validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
