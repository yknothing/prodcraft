"""Parse and validate compact, machine-readable Prodcraft workflow contracts."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml


WORKFLOW_CONTRACT_VERSION = "workflow.v2"
WORKFLOW_KINDS = {"primary", "overlay"}
WORKFLOW_REQUIRED_FIELDS = {
    "name",
    "description",
    "cadence",
    "workflow_kind",
    "composes_with",
    "entry_skill",
    "required_artifacts",
    "best_for",
    "phases_included",
    "contract",
}
PHASE_REQUIRED_FIELDS = {
    "id",
    "name",
    "purpose",
    "skills",
    "inputs",
    "outputs",
    "duration",
}
GATE_REQUIRED_FIELDS = {
    "name",
    "after",
    "criteria",
    "approvers",
    "enforcement",
}
OVERLAY_CHANGE_REQUIRED_FIELDS = {"dimension", "effect"}
SKILL_NAME_RE = re.compile(r"^pc-[a-z0-9]+(?:-[a-z0-9]+)*$")
WORKFLOW_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def load_workflow_document(path: Path) -> tuple[dict[str, Any], str]:
    """Load workflow frontmatter and Markdown body without importing the repo validator."""

    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing opening YAML frontmatter delimiter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError(f"{path}: malformed YAML frontmatter delimiters")
    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        raise ValueError(f"{path}: invalid YAML frontmatter: {exc}") from exc
    if not isinstance(frontmatter, dict):
        raise ValueError(f"{path}: workflow frontmatter must be a mapping")
    return frontmatter, parts[2].lstrip("\n")


def workflow_skill_references(frontmatter: dict[str, Any]) -> list[str]:
    """Return ordered, de-duplicated skill references from structured phase data."""

    contract = frontmatter.get("contract")
    if not isinstance(contract, dict):
        return []
    phases = contract.get("phase_sequence")
    if not isinstance(phases, list):
        return []

    result: list[str] = []
    seen: set[str] = set()
    for phase in phases:
        if not isinstance(phase, dict) or not isinstance(phase.get("skills"), list):
            continue
        for skill in phase["skills"]:
            if isinstance(skill, str) and skill not in seen:
                seen.add(skill)
                result.append(skill)
    return result


def _require_non_empty_string(
    mapping: dict[str, Any], field: str, label: str, errors: list[str]
) -> None:
    value = mapping.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}: `{field}` must be a non-empty string")


def _require_non_empty_string_list(
    mapping: dict[str, Any], field: str, label: str, errors: list[str]
) -> None:
    value = mapping.get(field)
    if not isinstance(value, list) or not value or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        errors.append(f"{label}: `{field}` must be a non-empty list of non-empty strings")


def _validate_phase_sequence(contract: dict[str, Any], label: str, errors: list[str]) -> None:
    phases = contract.get("phase_sequence")
    if not isinstance(phases, list) or not phases:
        errors.append(f"{label}: `phase_sequence` must be a non-empty list")
        return

    seen_ids: set[str] = set()
    for index, phase in enumerate(phases):
        phase_label = f"{label}: `phase_sequence[{index}]`"
        if not isinstance(phase, dict):
            errors.append(f"{phase_label} must be a mapping")
            continue
        missing = sorted(PHASE_REQUIRED_FIELDS - phase.keys())
        if missing:
            errors.append(f"{phase_label} is missing required fields {missing}")
        for field in ("id", "name", "purpose", "duration"):
            _require_non_empty_string(phase, field, phase_label, errors)
        for field in ("skills", "inputs", "outputs"):
            _require_non_empty_string_list(phase, field, phase_label, errors)

        phase_id = phase.get("id")
        if isinstance(phase_id, str) and phase_id.strip():
            if phase_id in seen_ids:
                errors.append(f"{phase_label}: duplicate phase id `{phase_id}`")
            seen_ids.add(phase_id)

        skills = phase.get("skills")
        if isinstance(skills, list):
            for skill in skills:
                if isinstance(skill, str) and not SKILL_NAME_RE.fullmatch(skill):
                    errors.append(f"{phase_label}: invalid skill reference `{skill}`")


def _validate_quality_gates(contract: dict[str, Any], label: str, errors: list[str]) -> None:
    gates = contract.get("quality_gates")
    if not isinstance(gates, list) or not gates:
        errors.append(f"{label}: `quality_gates` must be a non-empty list")
        return

    seen_names: set[str] = set()
    for index, gate in enumerate(gates):
        gate_label = f"{label}: `quality_gates[{index}]`"
        if not isinstance(gate, dict):
            errors.append(f"{gate_label} must be a mapping")
            continue
        missing = sorted(GATE_REQUIRED_FIELDS - gate.keys())
        if missing:
            errors.append(f"{gate_label} is missing required fields {missing}")
        for field in ("name", "after"):
            _require_non_empty_string(gate, field, gate_label, errors)
        for field in ("criteria", "approvers"):
            _require_non_empty_string_list(gate, field, gate_label, errors)
        if gate.get("enforcement") not in {"blocking", "advisory"}:
            errors.append(f"{gate_label}: `enforcement` must be `blocking` or `advisory`")

        name = gate.get("name")
        if isinstance(name, str) and name.strip():
            if name in seen_names:
                errors.append(f"{gate_label}: duplicate gate name `{name}`")
            seen_names.add(name)


def _validate_overlay_delta(
    contract: dict[str, Any], workflow_kind: Any, label: str, errors: list[str]
) -> None:
    overlay_delta = contract.get("overlay_delta")
    if workflow_kind == "primary":
        if overlay_delta is not None:
            errors.append(f"{label}: primary workflows must not declare `overlay_delta`")
        return
    if workflow_kind != "overlay":
        return
    if not isinstance(overlay_delta, dict):
        errors.append(f"{label}: overlay workflows must declare an `overlay_delta` mapping")
        return
    _require_non_empty_string_list(overlay_delta, "applies_to", f"{label}: `overlay_delta`", errors)
    changes = overlay_delta.get("changes")
    if not isinstance(changes, list) or not changes:
        errors.append(f"{label}: `overlay_delta.changes` must be a non-empty list")
        return
    for index, change in enumerate(changes):
        change_label = f"{label}: `overlay_delta.changes[{index}]`"
        if not isinstance(change, dict):
            errors.append(f"{change_label} must be a mapping")
            continue
        missing = sorted(OVERLAY_CHANGE_REQUIRED_FIELDS - change.keys())
        if missing:
            errors.append(f"{change_label} is missing required fields {missing}")
        for field in OVERLAY_CHANGE_REQUIRED_FIELDS:
            _require_non_empty_string(change, field, change_label, errors)


def _validate_body(body: str, label: str, errors: list[str]) -> None:
    headings = H2_RE.findall(body)
    if headings != ["Adaptation Notes"]:
        errors.append(
            f"{label}: Markdown body must contain only one H2 section, `## Adaptation Notes`; "
            "Entry Gate, Overview, Phase Sequence, and Quality Gates belong in `contract`"
        )
        return
    match = re.search(r"^##\s+Adaptation Notes\s*$\n(?P<content>.*)\Z", body, re.MULTILINE | re.DOTALL)
    if match is None or not match.group("content").strip():
        errors.append(f"{label}: `## Adaptation Notes` must contain non-empty guidance")


def validate_workflow_contract(path: Path) -> list[str]:
    """Return deterministic contract errors for one workflow document."""

    try:
        frontmatter, body = load_workflow_document(path)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        return [str(exc)]

    label = str(path)
    errors: list[str] = []
    missing = sorted(WORKFLOW_REQUIRED_FIELDS - frontmatter.keys())
    if missing:
        errors.append(f"{label}: missing required workflow fields {missing}")

    for field in ("name", "description", "cadence"):
        _require_non_empty_string(frontmatter, field, label, errors)
    for field in ("composes_with", "required_artifacts", "best_for", "phases_included"):
        _require_non_empty_string_list(frontmatter, field, label, errors)

    workflow_kind = frontmatter.get("workflow_kind")
    name = frontmatter.get("name")
    if isinstance(name, str) and name.strip():
        if not WORKFLOW_NAME_RE.fullmatch(name):
            errors.append(f"{label}: `name` must use kebab-case")
        if name != path.stem:
            errors.append(f"{label}: `name` must match filename `{path.stem}`")
    if workflow_kind not in WORKFLOW_KINDS:
        errors.append(f"{label}: `workflow_kind` must be `primary` or `overlay`")
    if frontmatter.get("entry_skill") != "pc-intake":
        errors.append(f"{label}: `entry_skill` must be `pc-intake`")
    if "intake-brief" not in (frontmatter.get("required_artifacts") or []):
        errors.append(f"{label}: `required_artifacts` must include `intake-brief`")

    contract = frontmatter.get("contract")
    if not isinstance(contract, dict):
        errors.append(f"{label}: `contract` must be a mapping")
        _validate_body(body, label, errors)
        return errors
    if contract.get("version") != WORKFLOW_CONTRACT_VERSION:
        errors.append(f"{label}: `contract.version` must be `{WORKFLOW_CONTRACT_VERSION}`")

    overview = contract.get("overview")
    if not isinstance(overview, dict):
        errors.append(f"{label}: `contract.overview` must be a mapping")
    else:
        for field in ("summary", "distinctive"):
            _require_non_empty_string(overview, field, f"{label}: `contract.overview`", errors)

    entry_gate = contract.get("entry_gate")
    if not isinstance(entry_gate, dict):
        errors.append(f"{label}: `contract.entry_gate` must be a mapping")
    else:
        for field in ("summary", "artifact", "fast_track_rule"):
            _require_non_empty_string(entry_gate, field, f"{label}: `contract.entry_gate`", errors)
        if entry_gate.get("artifact") != "intake-brief":
            errors.append(f"{label}: `contract.entry_gate.artifact` must be `intake-brief`")
        if entry_gate.get("approval_required") is not True:
            errors.append(f"{label}: `contract.entry_gate.approval_required` must be true")

    _validate_phase_sequence(contract, label, errors)
    _validate_quality_gates(contract, label, errors)
    _validate_overlay_delta(contract, workflow_kind, label, errors)
    _validate_body(body, label, errors)
    return errors
