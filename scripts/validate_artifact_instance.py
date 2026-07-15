#!/usr/bin/env python3
"""Validate protocol-artifact instances against their registered schemas.

This is the operational counterpart to `validate_prodcraft.py`: that script
validates the contract *definitions* (schema shape, registry integrity), while
this one validates the *records produced during real work* -- intake briefs,
verification records, course-correction notes, and any other artifact
registered in `schemas/artifacts/registry.yml`.

Usage:

    python scripts/validate_artifact_instance.py path/to/record.json [...]
    python scripts/validate_artifact_instance.py --artifact-type intake-brief record.yml

Instances must be JSON or YAML documents. The artifact type is read from the
instance's `artifact` field unless `--artifact-type` overrides it. For
`verification-record` instances the completion-claim bindings that JSON Schema
cannot express (evidence/work-state freshness and identity) are also checked.

Exit codes: 0 all instances valid, 1 validation errors (including instances
that fail to parse or name an unknown artifact type), 2 environment or usage
errors (missing jsonschema dependency, missing file, unreadable registry).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from validate_prodcraft import (
    ARTIFACT_REGISTRY_PATH as REGISTRY_PATH,
    ROOT as REPO_ROOT,
    validate_verification_record_instance_contract,
)

try:
    import jsonschema
except ImportError:  # pragma: no cover - environment-dependent
    jsonschema = None


def load_registry() -> dict[str, dict]:
    registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8")) or {}
    artifacts = registry.get("artifacts")
    if not isinstance(artifacts, dict):
        raise ValueError(f"{REGISTRY_PATH}: `artifacts` must be a mapping")
    return artifacts


def load_instance(path: Path) -> object:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    if path.suffix.lower() in {".yml", ".yaml"}:
        return yaml.safe_load(text)
    raise ValueError(
        f"{path}: unsupported extension `{path.suffix}`; instances must be .json, .yml, or .yaml"
    )


def validate_instance(
    instance_path: Path,
    artifacts: dict[str, dict],
    artifact_type_override: str | None,
) -> list[str]:
    errors: list[str] = []
    source = str(instance_path)

    try:
        instance = load_instance(instance_path)
    except Exception as exc:
        return [f"{source}: failed to load instance: {exc}"]

    if not isinstance(instance, dict):
        return [f"{source}: instance must be a JSON/YAML object"]

    artifact_type = artifact_type_override or instance.get("artifact")
    if not isinstance(artifact_type, str) or not artifact_type:
        return [
            f"{source}: cannot determine artifact type; the instance has no `artifact` field "
            f"and no --artifact-type was given"
        ]

    entry = artifacts.get(artifact_type)
    if entry is None:
        return [
            f"{source}: unknown artifact type `{artifact_type}`; registered types: "
            f"{', '.join(sorted(artifacts))}"
        ]

    schema_rel = entry.get("schema_path")
    if not isinstance(schema_rel, str):
        return [f"{REGISTRY_PATH}: artifact `{artifact_type}` has no `schema_path`"]

    schema_path = REPO_ROOT / schema_rel
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{schema_path}: failed to load schema: {exc}"]

    validator_cls = jsonschema.validators.validator_for(schema)
    validator = validator_cls(schema, format_checker=jsonschema.FormatChecker())
    for error in sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path)):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"{source}: {location}: {error.message}")

    if artifact_type == "verification-record":
        validate_verification_record_instance_contract(instance, source, errors)

    # Overlapping subschemas (e.g. allOf branches) can report the same defect
    # twice; keep first occurrences in order.
    return list(dict.fromkeys(errors))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate protocol-artifact instances against registered schemas."
    )
    parser.add_argument("instances", nargs="+", type=Path, help="Instance files (.json/.yml/.yaml)")
    parser.add_argument(
        "--artifact-type",
        help="Override the artifact type instead of reading the instance's `artifact` field.",
    )
    args = parser.parse_args()

    if jsonschema is None:
        print(
            "ERROR: the `jsonschema` package is required "
            "(install with `pip install jsonschema` or run under `uv run --with jsonschema`)",
            file=sys.stderr,
        )
        return 2

    try:
        artifacts = load_registry()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    failed = False
    for instance_path in args.instances:
        if not instance_path.exists():
            print(f"ERROR: {instance_path}: file does not exist", file=sys.stderr)
            return 2
        errors = validate_instance(instance_path, artifacts, args.artifact_type)
        if errors:
            failed = True
            for error in errors:
                print(f"INVALID: {error}")
        else:
            print(f"OK: {instance_path}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
