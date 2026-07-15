"""Repository-owned execution artifact and authority validation service."""

from __future__ import annotations

import errno
import hashlib
import json
import os
import re
import stat
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

import yaml

from tools.execution_state import (
    AUTHORITY_GATE,
    AUTHORITY_TERMINAL,
    ControlBundleIO,
    FilesystemControlBundleIO,
    StrictJSONError,
    file_sha256,
    load_strict_json,
    load_strict_json_with_digest,
    parse_strict_json_bytes,
    read_protocol_file,
    resolve_authority_context,
    resolve_control_ref,
    validate_control_bundle,
    validate_execution_state_contract,
    validate_route_decision_contract,
    validate_terminal_completion,
    validate_control_ref,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "schemas"
ARTIFACT_REGISTRY_PATH = SCHEMAS_DIR / "artifacts" / "registry.yml"
MANIFEST_PATH = ROOT / "manifest.yml"

_RFC3339_DATETIME_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})$"
)
_HISTORY_EXECUTION_REF_RE = re.compile(
    r"^history/execution-state\.r(?P<route_revision>[1-9]\d*)\."
    r"s(?P<state_revision>[1-9]\d*)\.(?P<sha256>[0-9a-f]{64})\.json$"
)


class ValidationDisposition(str, Enum):
    """Typed authority-validation disposition for result projection."""

    VALID = "valid"
    APPROVAL_REQUIRED = "approval_required"
    INVALID = "invalid"


@dataclass(frozen=True)
class ExecutionValidationOutcome:
    """Authority and candidate facts without diagnostic-string interpretation."""

    disposition: ValidationDisposition
    authority: str | None
    candidate_completion_digest: str | None = None
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class CandidateBundleView:
    """Immutable effective view over a live control bundle and candidate changes."""

    control_root: Path
    overrides: Mapping[str, bytes]
    removals: frozenset[str]

    def __init__(
        self,
        control_root: Path,
        overrides: dict[str, bytes] | None = None,
        removals: set[str] | frozenset[str] | None = None,
    ) -> None:
        normalized_overrides = dict(overrides or {})
        normalized_removals = frozenset(removals or ())
        root = control_root.absolute()
        try:
            root_stat = root.lstat()
        except OSError as exc:
            raise ValueError(f"control root cannot be inspected: {exc}") from exc
        if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
            raise ValueError("control root must be a non-symlink directory")
        for relative_path, content in normalized_overrides.items():
            validate_control_ref(relative_path)
            if not isinstance(content, bytes):
                raise TypeError(f"candidate override must use bytes: {relative_path}")
            self._inspect_candidate_path(root, relative_path, allow_absent_final=True)
        for relative_path in normalized_removals:
            validate_control_ref(relative_path)
            self._inspect_candidate_path(root, relative_path, allow_absent_final=False)
        conflicts = normalized_overrides.keys() & normalized_removals
        if conflicts:
            raise ValueError(
                f"candidate path cannot be both overridden and removed: {sorted(conflicts)[0]}"
            )
        ordered_overrides = sorted(normalized_overrides)
        for index, ancestor in enumerate(ordered_overrides):
            prefix = ancestor + "/"
            descendant = next(
                (
                    candidate
                    for candidate in ordered_overrides[index + 1 :]
                    if candidate.startswith(prefix)
                ),
                None,
            )
            if descendant is not None:
                raise ValueError(
                    "candidate overrides cannot contain ancestor and descendant paths: "
                    f"{ancestor}, {descendant}"
                )
        object.__setattr__(self, "control_root", root)
        object.__setattr__(self, "overrides", MappingProxyType(normalized_overrides))
        object.__setattr__(self, "removals", normalized_removals)

    @staticmethod
    def _inspect_candidate_path(
        root: Path,
        relative_path: str,
        *,
        allow_absent_final: bool,
    ) -> None:
        parts = relative_path.split("/")
        current = root
        for index, part in enumerate(parts):
            current /= part
            final = index == len(parts) - 1
            try:
                metadata = current.lstat()
            except FileNotFoundError:
                if allow_absent_final:
                    return
                raise ValueError(
                    f"control reference does not resolve to a readable file: {relative_path}"
                ) from None
            except OSError as exc:
                raise ValueError(
                    f"control reference does not resolve to a readable file: "
                    f"{relative_path}: {exc}"
                ) from exc
            if stat.S_ISLNK(metadata.st_mode):
                raise ValueError(f"control reference contains a symlink component: {relative_path}")
            if final:
                if not stat.S_ISREG(metadata.st_mode):
                    raise ValueError(
                        f"control reference target must be a regular file: {relative_path}"
                    )
            elif not stat.S_ISDIR(metadata.st_mode):
                raise ValueError(
                    f"control reference intermediate component is not a directory: {relative_path}"
                )

    def resolve_ref(self, ref: str) -> str:
        validate_control_ref(ref)
        if ref in self.removals:
            missing = FileNotFoundError(
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                str(self.control_root / ref),
            )
            raise ValueError(
                f"control reference does not resolve to a readable file: {ref}: {missing}"
            )
        if ref in self.overrides:
            return ref
        return FilesystemControlBundleIO(self.control_root).resolve_ref(ref)

    def read_bytes(self, relative_path: str) -> bytes:
        if relative_path in self.removals:
            raise ValueError(f"candidate path was removed: {relative_path}")
        if relative_path in self.overrides:
            return self.overrides[relative_path]
        resolved = self.resolve_ref(relative_path)
        if resolved in self.overrides:
            return self.overrides[resolved]
        return FilesystemControlBundleIO(self.control_root).read_bytes(resolved)

    def sha256(self, relative_path: str) -> str:
        if relative_path in self.removals:
            raise ValueError(f"candidate path was removed: {relative_path}")
        if relative_path in self.overrides:
            return "sha256:" + hashlib.sha256(self.overrides[relative_path]).hexdigest()
        resolved = self.resolve_ref(relative_path)
        return FilesystemControlBundleIO(self.control_root).sha256(resolved)

    def iter_relative_files(self) -> tuple[str, ...]:
        live_files = set(FilesystemControlBundleIO(self.control_root).iter_relative_files())
        return tuple(sorted((live_files - self.removals) | self.overrides.keys()))


def _load_strict_from_bundle(
    bundle: ControlBundleIO,
    ref: str,
) -> tuple[dict, str, Path]:
    relative = bundle.resolve_ref(ref)
    source = bundle.control_root / relative
    content = bundle.read_bytes(relative)
    payload = parse_strict_json_bytes(content, source)
    digest = "sha256:" + hashlib.sha256(content).hexdigest()
    return payload, digest, source


def _load_yaml_file(path: Path, errors: list[str]) -> dict:
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


def _parse_record_datetime(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed


def _is_portable_json_datetime(value: object) -> bool:
    if not isinstance(value, str) or _RFC3339_DATETIME_RE.fullmatch(value) is None:
        return False
    normalized = value[:-1] + "+00:00" if value.endswith(("Z", "z")) else value
    try:
        parsed = datetime.fromisoformat(normalized.replace("t", "T"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def validate_verification_record_instance_contract(
    record: dict,
    source: str,
    errors: list[str],
) -> None:
    """Validate completion-claim bindings that JSON Schema cannot express portably."""
    if record.get("status") != "accepted" and record.get("claim_may_be_made") is not True:
        return

    work_state = record.get("work_state_ref")
    if not isinstance(work_state, dict):
        errors.append(f"{source}: accepted verification record must use structured work_state_ref")
        return

    verified_at = _parse_record_datetime(record.get("verified_at"))
    if verified_at is None:
        errors.append(f"{source}: accepted verification record must include valid verified_at")

    work_state_id = work_state.get("id")
    if not isinstance(work_state_id, str) or not work_state_id:
        errors.append(f"{source}: accepted verification record work_state_ref must include non-empty id")
        return

    work_state_captured_at = _parse_record_datetime(work_state.get("captured_at"))
    if work_state_captured_at is None:
        errors.append(f"{source}: accepted verification record work_state_ref must include valid captured_at")

    evidence_refs = record.get("evidence_refs")
    if not isinstance(evidence_refs, list) or not evidence_refs:
        errors.append(f"{source}: accepted verification record must declare at least one evidence_ref")
        evidence_refs = []

    evidence_by_id: dict[str, dict] = {}
    for evidence in evidence_refs:
        if not isinstance(evidence, dict):
            errors.append(f"{source}: evidence_refs entries must be structured objects")
            continue
        evidence_id = evidence.get("id")
        if not isinstance(evidence_id, str) or not evidence_id:
            errors.append(f"{source}: evidence_refs entries must include non-empty id")
            continue
        if evidence_id in evidence_by_id:
            errors.append(f"{source}: evidence_ref id `{evidence_id}` must be unique")
        evidence_by_id[evidence_id] = evidence

        evidence_work_state_ref = evidence.get("work_state_ref")
        if evidence_work_state_ref != work_state_id:
            errors.append(
                f"{source}: evidence `{evidence_id}` binds to work_state_ref "
                f"`{evidence_work_state_ref}` instead of current work state `{work_state_id}`"
            )

        evidence_captured_at = _parse_record_datetime(evidence.get("captured_at"))
        if evidence_captured_at is None:
            errors.append(f"{source}: evidence `{evidence_id}` must include valid captured_at")
        elif work_state_captured_at is not None and evidence_captured_at < work_state_captured_at:
            errors.append(
                f"{source}: accepted verification record evidence `{evidence_id}` is older "
                f"than work state `{work_state_id}`"
            )

    checks_run = record.get("checks_run")
    if not isinstance(checks_run, list) or not checks_run:
        errors.append(f"{source}: accepted verification record must declare at least one check")
        return

    for check in checks_run:
        if not isinstance(check, dict):
            errors.append(f"{source}: checks_run entries must be structured objects")
            continue
        check_name = check.get("name")
        check_label = check_name if isinstance(check_name, str) and check_name else "<unnamed>"
        check_evidence_ref = check.get("evidence_ref")
        if check_evidence_ref not in evidence_by_id:
            errors.append(
                f"{source}: check `{check_label}` references unknown evidence_ref `{check_evidence_ref}`"
            )
        check_work_state_ref = check.get("work_state_ref")
        if check_work_state_ref != work_state_id:
            errors.append(
                f"{source}: check `{check_label}` binds to work_state_ref "
                f"`{check_work_state_ref}` instead of current work state `{work_state_id}`"
            )


def load_artifact_instance(path: Path, errors: list[str]) -> dict:
    try:
        text = read_protocol_file(path).decode("utf-8")
    except (UnicodeError, ValueError) as exc:
        errors.append(f"{path}: failed to read artifact instance: {exc}")
        return {}

    try:
        if path.suffix.lower() == ".json":

            def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
                payload: dict = {}
                for key, value in pairs:
                    if key in payload:
                        raise ValueError(f"duplicate JSON key: {key}")
                    payload[key] = value
                return payload

            payload = json.loads(text, object_pairs_hook=reject_duplicate_keys)
        else:
            payload = yaml.safe_load(text)
    except Exception as exc:
        errors.append(f"{path}: failed to parse artifact instance as JSON/YAML: {exc}")
        return {}

    if not isinstance(payload, dict):
        errors.append(f"{path}: artifact instance must be a mapping/object")
        return {}
    return payload


def validate_registered_artifact_payload(
    payload: dict,
    path: Path,
    errors: list[str],
) -> bool:
    """Validate one already-loaded payload against the registered JSON Schema."""

    artifact_name = payload.get("artifact")
    schema_version = payload.get("schema_version")
    if not isinstance(artifact_name, str) or not artifact_name:
        errors.append(f"{path}: artifact instance must include non-empty `artifact`")
        return False
    if not isinstance(schema_version, str) or not schema_version:
        errors.append(f"{path}: artifact instance must include non-empty `schema_version`")
        return False

    registry = _load_yaml_file(ARTIFACT_REGISTRY_PATH, errors)
    artifacts = registry.get("artifacts", {})
    if not isinstance(artifacts, dict):
        errors.append(f"{ARTIFACT_REGISTRY_PATH}: `artifacts` must be a mapping")
        return False
    entry = artifacts.get(artifact_name)
    if not isinstance(entry, dict):
        errors.append(f"{path}: artifact `{artifact_name}` is not registered in {ARTIFACT_REGISTRY_PATH}")
        return False
    expected_schema_version = entry.get("schema_version")
    if schema_version != expected_schema_version:
        errors.append(
            f"{path}: artifact `{artifact_name}` declares schema_version `{schema_version}`; "
            f"expected `{expected_schema_version}`"
        )

    schema_rel = entry.get("schema_path")
    if not isinstance(schema_rel, str):
        errors.append(f"{ARTIFACT_REGISTRY_PATH}: artifact `{artifact_name}` is missing `schema_path`")
        return False
    schema_path = ROOT / schema_rel
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{schema_path}: failed to parse JSON schema: {exc}")
        return False

    try:
        import jsonschema  # type: ignore[import-untyped]
    except Exception as exc:
        errors.append(f"{path}: jsonschema is required to validate artifact instances: {exc}")
        return False

    try:
        format_checker = jsonschema.FormatChecker()
        format_checker.checks("date-time")(_is_portable_json_datetime)
        validator = jsonschema.Draft202012Validator(
            schema,
            format_checker=format_checker,
        )
        validator.validate(payload)
    except jsonschema.ValidationError as exc:
        location = ".".join(str(part) for part in exc.absolute_path)
        suffix = f" at `{location}`" if location else ""
        errors.append(
            f"{path}: artifact `{artifact_name}` failed schema validation{suffix}: {exc.message}"
        )
        return False

    if artifact_name == "verification-record":
        validate_verification_record_instance_contract(payload, str(path), errors)
    if artifact_name in {"intake-brief", "course-correction-note"}:
        validate_artifact_skill_membership(payload, path, errors)
    return True


def validate_artifact_skill_membership(
    payload: dict,
    path: Path,
    errors: list[str],
) -> None:
    """Reject artifact routes that do not resolve to implemented manifest skills."""

    manifest = _load_yaml_file(MANIFEST_PATH, errors)
    implemented_names = {
        entry["name"]
        for entry in manifest.get("skills", [])
        if isinstance(entry, dict) and isinstance(entry.get("name"), str)
    }
    referenced_names: list[str] = []
    recommended = payload.get("recommended_next_skill")
    if isinstance(recommended, str):
        referenced_names.append(recommended)
    proposed = payload.get("proposed_path")
    if isinstance(proposed, list):
        referenced_names.extend(name for name in proposed if isinstance(name, str))
    for name in dict.fromkeys(referenced_names):
        if name not in implemented_names:
            errors.append(f"{path}: route references unknown manifest skill `{name}`")


def validate_route_contract_from_repository(route: dict, errors: list[str]) -> list[str]:
    try:
        route_schema = json.loads(
            (SCHEMAS_DIR / "artifacts" / "route-decision.schema.json").read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        errors.append(f"route contract metadata could not be loaded: {exc}")
        return []
    manifest = _load_yaml_file(MANIFEST_PATH, errors)
    phase_values = set(route_schema.get("$defs", {}).get("phase", {}).get("enum", []))
    workflow_properties = route_schema.get("properties", {}).get("workflow", {}).get("properties", {})
    primary_values = set(workflow_properties.get("primary", {}).get("enum", []))
    overlay_values = set(workflow_properties.get("overlays", {}).get("items", {}).get("enum", []))
    artifact_flow = manifest.get("artifact_flow", [])
    artifact_names: set[str] = {
        entry["artifact"]
        for entry in artifact_flow
        if isinstance(entry, dict) and isinstance(entry.get("artifact"), str)
    }
    return validate_route_decision_contract(
        route,
        phases=phase_values,
        primary_workflows=primary_values,
        overlays=overlay_values,
        artifact_names=artifact_names,
    )


def validate_execution_state_instance_contract(
    path: Path,
    state: dict,
    errors: list[str],
    bundle_io: ControlBundleIO | None = None,
) -> None:
    """Replay generic execution-state instances without granting authority."""

    control_root = path.parent.parent if path.parent.name == "history" else path.parent
    route_binding = state.get("route_binding")
    route_ref = route_binding.get("ref") if isinstance(route_binding, dict) else None
    if not isinstance(route_ref, str):
        errors.append(f"{path}: execution-state route binding ref must be a string")
        return
    try:
        if bundle_io is None:
            route_path = resolve_control_ref(control_root, route_ref)
            route = load_strict_json(route_path)
        else:
            route, _digest, route_path = _load_strict_from_bundle(bundle_io, route_ref)
    except (StrictJSONError, TypeError, ValueError) as exc:
        errors.append(f"{path}: execution-state route cannot be loaded for structural replay: {exc}")
        return
    if not validate_registered_artifact_payload(route, route_path, errors):
        return
    if route.get("artifact") != "route-decision":
        errors.append(f"{path}: execution-state route ref does not identify route-decision")
        return
    route_errors = validate_route_contract_from_repository(route, errors)
    errors.extend(f"{route_path}: {error}" for error in route_errors)
    replay = validate_execution_state_contract(
        state,
        route,
        approved_route_digest=None,
        is_canonical_current=False,
        authority_mode=False,
    )
    errors.extend(f"{path}: {error}" for error in replay.errors)


def validate_artifact_instance(path: Path, errors: list[str]) -> None:
    payload = load_artifact_instance(path, errors)
    if not payload:
        return

    if payload.get("artifact") in {"route-decision", "execution-state"}:
        if path.suffix.lower() != ".json":
            errors.append(f"{path}: strict route/execution artifacts must use JSON")
            return
        try:
            payload = load_strict_json(path)
        except StrictJSONError as exc:
            errors.append(str(exc))
            return

    if not validate_registered_artifact_payload(payload, path, errors):
        return

    if payload.get("artifact") == "route-decision":
        route_contract_errors = validate_route_contract_from_repository(payload, errors)
        errors.extend(f"{path}: {error}" for error in route_contract_errors)
    elif payload.get("artifact") == "execution-state":
        validate_execution_state_instance_contract(path, payload, errors)


def _validate_structural_artifact_bindings(
    state: dict,
    control_root: Path,
    errors: list[str],
    bundle_io: ControlBundleIO | None = None,
) -> None:
    for index, binding in enumerate(state.get("artifact_bindings", [])):
        if not isinstance(binding, dict) or binding.get("assurance") != "structural_valid":
            continue
        ref = binding.get("ref")
        if not isinstance(ref, str):
            errors.append(f"artifact binding {index} structural subject ref must be a string")
            continue
        try:
            if bundle_io is None:
                subject_path = resolve_control_ref(control_root, ref)
                subject, subject_digest = load_strict_json_with_digest(subject_path)
            else:
                subject, subject_digest, subject_path = _load_strict_from_bundle(
                    bundle_io, ref
                )
        except (StrictJSONError, TypeError, ValueError) as exc:
            errors.append(f"artifact binding {index} structural subject is invalid: {exc}")
            continue
        if subject_digest != binding.get("subject_sha256"):
            errors.append(
                f"artifact binding {index} structural subject digest does not match its binding"
            )
            continue
        if subject.get("artifact") != binding.get("artifact"):
            errors.append(
                f"artifact binding {index} structural subject artifact does not match its obligation"
            )
            continue
        if not validate_registered_artifact_payload(subject, subject_path, errors):
            continue
        if subject.get("artifact") == "route-decision":
            route_errors = validate_route_contract_from_repository(subject, errors)
            errors.extend(f"{subject_path}: {error}" for error in route_errors)
        elif subject.get("artifact") == "execution-state":
            validate_execution_state_instance_contract(
                subject_path,
                subject,
                errors,
                bundle_io=bundle_io,
            )


def _validate_terminal_verification_schema(
    state: dict,
    control_root: Path,
    errors: list[str],
    bundle_io: ControlBundleIO | None = None,
) -> tuple[dict, str] | None:
    attempt_id = state.get("current_completion_attempt_id")
    attempt = next(
        (
            candidate
            for candidate in state.get("completion_attempts", [])
            if isinstance(candidate, dict) and candidate.get("attempt_id") == attempt_id
        ),
        None,
    )
    binding = attempt.get("completion_binding") if isinstance(attempt, dict) else None
    if not isinstance(binding, dict):
        return None
    verification_ref = binding.get("verification_record_ref")
    if not isinstance(verification_ref, str):
        errors.append("terminal verification record ref must be a string")
        return None
    try:
        if bundle_io is None:
            verification_path = resolve_control_ref(control_root, verification_ref)
            verification, verification_digest = load_strict_json_with_digest(verification_path)
        else:
            verification, verification_digest, verification_path = _load_strict_from_bundle(
                bundle_io, verification_ref
            )
    except (StrictJSONError, TypeError, ValueError) as exc:
        errors.append(f"terminal verification record is invalid: {exc}")
        return None
    if verification_digest != binding.get("verification_record_sha256"):
        errors.append("terminal verification record digest does not match completion binding")
        return None
    if (
        verification.get("artifact") != "verification-record"
        or verification.get("schema_version") != "verification-record.v1"
    ):
        errors.append("terminal verification record must use verification-record.v1")
        return None
    validate_registered_artifact_payload(verification, verification_path, errors)
    return verification, verification_digest


def _load_route_predecessor_chain(
    route: dict,
    control_root: Path,
    errors: list[str],
    bundle_io: ControlBundleIO | None = None,
) -> list[dict]:
    predecessors: list[dict] = []
    current = route
    seen_refs: set[str] = set()
    while current.get("route_revision", 1) > 1:
        previous = current.get("previous_route")
        if not isinstance(previous, dict):
            errors.append("route predecessor chain is missing previous_route")
            break
        ref = previous.get("ref")
        if not isinstance(ref, str) or ref in seen_refs:
            errors.append(f"route predecessor chain contains an invalid or repeated ref: {ref!r}")
            break
        seen_refs.add(ref)
        expected_ref = f"route-decision.r{previous.get('revision')}.json"
        if ref != expected_ref:
            errors.append(f"route predecessor ref must use canonical route filename {expected_ref}")
        try:
            if bundle_io is None:
                previous_path = resolve_control_ref(control_root, ref)
                predecessor = load_strict_json(previous_path)
            else:
                predecessor, _digest, previous_path = _load_strict_from_bundle(bundle_io, ref)
        except (StrictJSONError, TypeError, ValueError) as exc:
            errors.append(f"route predecessor {ref!r} is invalid: {exc}")
            break
        if not validate_registered_artifact_payload(predecessor, previous_path, errors):
            break
        if predecessor.get("artifact") != "route-decision":
            errors.append(f"route predecessor {ref!r} is not a route-decision")
            break
        route_errors = validate_route_contract_from_repository(predecessor, errors)
        errors.extend(f"{previous_path}: {error}" for error in route_errors)
        if predecessor.get("work_id") != route.get("work_id"):
            errors.append(f"{previous_path}: predecessor work_id does not match current route")
        if predecessor.get("route_id") != route.get("route_id"):
            errors.append(f"{previous_path}: predecessor route_id does not match current route")
        if previous.get("revision") != predecessor.get("route_revision"):
            errors.append(f"{previous_path}: previous_route.revision does not match predecessor")
        if previous.get("digest") != predecessor.get("route_digest"):
            errors.append(f"{previous_path}: previous_route.digest does not match predecessor")
        predecessors.append(predecessor)
        current = predecessor
    return predecessors


def _load_previous_execution_chain(
    state: dict,
    route: dict,
    predecessors: list[dict],
    control_root: Path,
    errors: list[str],
    bundle_io: ControlBundleIO | None = None,
) -> list[dict]:
    historical_states: list[dict] = []
    current_state = state
    routes_by_revision = {
        candidate.get("route_revision"): candidate
        for candidate in [route, *predecessors]
        if isinstance(candidate.get("route_revision"), int)
    }
    expected_revision = route.get("route_revision", 1) - 1
    seen_refs: set[str] = set()
    while expected_revision >= 1:
        previous = current_state.get("previous_execution")
        if not isinstance(previous, dict):
            errors.append(
                f"route revision {expected_revision + 1} execution is missing previous_execution"
            )
            break
        ref = previous.get("ref")
        if not isinstance(ref, str) or ref in seen_refs:
            errors.append(f"previous execution chain contains an invalid or repeated ref: {ref!r}")
            break
        seen_refs.add(ref)
        history_match = _HISTORY_EXECUTION_REF_RE.fullmatch(ref)
        if history_match is None:
            errors.append(
                f"previous execution {ref!r} must use the canonical content-addressed history filename"
            )
        try:
            if bundle_io is None:
                previous_path = resolve_control_ref(control_root, ref)
                archived, actual_digest = load_strict_json_with_digest(previous_path)
            else:
                archived, actual_digest, previous_path = _load_strict_from_bundle(bundle_io, ref)
        except (StrictJSONError, TypeError, ValueError) as exc:
            errors.append(f"previous execution {ref!r} is invalid: {exc}")
            break
        if previous.get("sha256") != actual_digest:
            errors.append(f"previous execution {ref!r} sha256 does not match archived content")
        if history_match is not None:
            if int(history_match.group("route_revision")) != expected_revision:
                errors.append(f"previous execution {ref!r} filename route revision is incorrect")
            if history_match.group("sha256") != actual_digest.removeprefix("sha256:"):
                errors.append(f"previous execution {ref!r} filename digest does not match content")
        if previous.get("lifecycle_state") != "rerouted":
            errors.append(f"previous execution {ref!r} binding must declare rerouted")
        if not validate_registered_artifact_payload(archived, previous_path, errors):
            break
        if archived.get("artifact") != "execution-state":
            errors.append(f"previous execution {ref!r} is not an execution-state")
            break
        if archived.get("lifecycle_state") != "rerouted":
            errors.append(f"previous execution {ref!r} must end in rerouted")
        if history_match is not None and int(history_match.group("state_revision")) != archived.get(
            "state_revision"
        ):
            errors.append(f"previous execution {ref!r} filename state revision is incorrect")
        predecessor_route = routes_by_revision.get(expected_revision)
        if predecessor_route is None:
            errors.append(f"previous execution {ref!r} has no matching predecessor route")
            break
        replay = validate_execution_state_contract(
            archived,
            predecessor_route,
            approved_route_digest=None,
            is_canonical_current=False,
            authority_mode=False,
        )
        errors.extend(f"{previous_path}: {error}" for error in replay.errors)
        historical_states.append(archived)
        current_state = archived
        expected_revision -= 1
    return historical_states


def validate_execution_candidate(
    *,
    repo_root: Path,
    control_root: Path,
    state_path: Path,
    state: dict,
    route: dict,
    view: CandidateBundleView,
    approved_route_digest: str | None,
    approved_completion_digest: str | None = None,
) -> ExecutionValidationOutcome:
    """Validate one effective candidate bundle without materializing candidate bytes."""

    errors: list[str] = []
    root = control_root.absolute()
    if view.control_root != root:
        errors.append("candidate bundle view root does not match control_root")
    canonical_state_path = root / "execution-state.json"
    if state_path.absolute() != canonical_state_path:
        errors.append("candidate state path must be the canonical execution-state.json selector")
    if approved_route_digest is None:
        errors.append("approved route digest is required for candidate validation")

    state_digest: str | None = None
    try:
        loaded_state, state_digest, _loaded_state_path = _load_strict_from_bundle(
            view, "execution-state.json"
        )
    except (StrictJSONError, TypeError, ValueError) as exc:
        errors.append(f"candidate execution-state is invalid: {exc}")
        return ExecutionValidationOutcome(
            ValidationDisposition.INVALID,
            None,
            errors=tuple(_normalize_candidate_errors(errors, root)),
        )
    if loaded_state != state:
        errors.append("candidate execution-state bytes do not match the supplied state payload")
    if not validate_registered_artifact_payload(loaded_state, Path("execution-state.json"), errors):
        return ExecutionValidationOutcome(
            ValidationDisposition.INVALID,
            None,
            errors=tuple(_normalize_candidate_errors(errors, root)),
        )
    if loaded_state.get("artifact") != "execution-state":
        errors.append("candidate state must be an execution-state artifact")

    route_binding = loaded_state.get("route_binding", {})
    route_ref = route_binding.get("ref")
    expected_route_ref = f"route-decision.r{route_binding.get('route_revision')}.json"
    if route_ref != expected_route_ref:
        errors.append(f"route binding must use canonical route filename {expected_route_ref}")
    route_digest: str | None = None
    route_path = Path(expected_route_ref)
    try:
        loaded_route, route_digest, _route_path = _load_strict_from_bundle(view, route_ref)
        route_path = Path(route_ref)
    except (StrictJSONError, TypeError, ValueError) as exc:
        errors.append(f"referenced route decision is invalid: {exc}")
        return ExecutionValidationOutcome(
            ValidationDisposition.INVALID,
            None,
            errors=tuple(_normalize_candidate_errors(errors, root)),
        )
    if loaded_route != route:
        errors.append("candidate route bytes do not match the supplied route payload")
    if not validate_registered_artifact_payload(loaded_route, route_path, errors):
        return ExecutionValidationOutcome(
            ValidationDisposition.INVALID,
            None,
            errors=tuple(_normalize_candidate_errors(errors, root)),
        )
    route_errors = validate_route_contract_from_repository(loaded_route, errors)
    errors.extend(f"{route_path}: {error}" for error in route_errors)

    predecessors = _load_route_predecessor_chain(
        loaded_route,
        root,
        errors,
        bundle_io=view,
    )
    historical_states = _load_previous_execution_chain(
        loaded_state,
        loaded_route,
        predecessors,
        root,
        errors,
        bundle_io=view,
    )
    errors.extend(
        validate_control_bundle(
            root,
            state_path=canonical_state_path,
            state=loaded_state,
            route=loaded_route,
            historical_states=historical_states,
            predecessor_routes=predecessors,
            bundle_io=view,
        )
    )
    _validate_structural_artifact_bindings(loaded_state, root, errors, bundle_io=view)
    for historical_state in historical_states:
        _validate_structural_artifact_bindings(
            historical_state,
            root,
            errors,
            bundle_io=view,
        )

    terminal_verification: tuple[dict, str] | None = None
    lifecycle_state = loaded_state.get("lifecycle_state")
    if lifecycle_state in {"verified", "completed"}:
        terminal_verification = _validate_terminal_verification_schema(
            loaded_state,
            root,
            errors,
            bundle_io=view,
        )
        if terminal_verification is None:
            terminal_errors = ["terminal verification snapshot is unavailable"]
        else:
            verification_document, verification_digest = terminal_verification
            terminal_errors = validate_terminal_completion(
                loaded_state,
                loaded_route,
                control_root=root,
                repo_root=repo_root,
                verification_document=verification_document,
                verification_document_digest=verification_digest,
                bundle_io=view,
            )
        errors.extend(terminal_errors)
        result = validate_execution_state_contract(
            loaded_state,
            loaded_route,
            approved_route_digest=approved_route_digest,
            is_canonical_current=True,
            authority_mode=True,
            terminal_validation_passed=not terminal_errors,
            approved_completion_digest=approved_completion_digest,
        )
    else:
        if approved_completion_digest is not None:
            errors.append(
                "approved completion digest is valid only for verified/completed state"
            )
        result = validate_execution_state_contract(
            loaded_state,
            loaded_route,
            approved_route_digest=approved_route_digest,
            is_canonical_current=True,
            authority_mode=True,
        )

    candidate_pending = result.candidate_completion_digest is not None
    if not candidate_pending:
        errors.extend(result.errors)

    errors.extend(
        f"final control-bundle capture: {error}"
        for error in validate_control_bundle(
            root,
            state_path=canonical_state_path,
            state=loaded_state,
            route=loaded_route,
            historical_states=historical_states,
            predecessor_routes=predecessors,
            bundle_io=view,
        )
    )
    try:
        if view.sha256("execution-state.json") != state_digest:
            errors.append("execution-state changed during candidate validation")
        if view.sha256(route_ref) != route_digest:
            errors.append("route-decision changed during candidate validation")
        if terminal_verification is not None:
            attempt_id = loaded_state.get("current_completion_attempt_id")
            attempt = next(
                (
                    candidate
                    for candidate in loaded_state.get("completion_attempts", [])
                    if isinstance(candidate, dict) and candidate.get("attempt_id") == attempt_id
                ),
                None,
            )
            binding = attempt.get("completion_binding") if isinstance(attempt, dict) else None
            verification_ref = (
                binding.get("verification_record_ref") if isinstance(binding, dict) else None
            )
            if not isinstance(verification_ref, str):
                raise ValueError("terminal verification record ref is unavailable")
            if view.sha256(verification_ref) != terminal_verification[1]:
                errors.append("terminal verification record changed during candidate validation")
    except (TypeError, ValueError) as exc:
        errors.append(f"candidate stability check failed: {exc}")

    if not candidate_pending and result.authority not in {AUTHORITY_GATE, AUTHORITY_TERMINAL}:
        errors.append("candidate authority result is structural-only")

    normalized_errors = tuple(_normalize_candidate_errors(errors, root))
    if normalized_errors:
        return ExecutionValidationOutcome(
            ValidationDisposition.INVALID,
            None,
            errors=normalized_errors,
        )
    if candidate_pending:
        return ExecutionValidationOutcome(
            ValidationDisposition.APPROVAL_REQUIRED,
            None,
            result.candidate_completion_digest,
        )
    return ExecutionValidationOutcome(
        ValidationDisposition.VALID,
        result.authority,
    )


def _normalize_candidate_errors(errors: list[str], control_root: Path) -> list[str]:
    """Keep overlay/materialized candidate diagnostics independent of fixture roots."""

    root_text = str(control_root)
    return [error.replace(root_text, "<control-root>") for error in errors]


def authorize_execution_state(
    state_path: Path,
    approved_route_digest: str | None,
    approved_completion_digest: str | None,
    errors: list[str],
) -> ExecutionValidationOutcome:
    """Validate one canonical state and classify its authority without parsing errors."""

    if approved_route_digest is None:
        errors.append("--approved-route-digest is required with --authorize-execution-state")
        return ExecutionValidationOutcome(ValidationDisposition.INVALID, None)
    try:
        state, state_file_digest = load_strict_json_with_digest(state_path)
    except StrictJSONError as exc:
        errors.append(str(exc))
        return ExecutionValidationOutcome(ValidationDisposition.INVALID, None)
    if not validate_registered_artifact_payload(state, state_path, errors):
        return ExecutionValidationOutcome(ValidationDisposition.INVALID, None)
    if state.get("artifact") != "execution-state":
        errors.append(f"{state_path}: authority mode requires an execution-state artifact")
        return ExecutionValidationOutcome(ValidationDisposition.INVALID, None)

    context, context_errors = resolve_authority_context(state_path, state)
    errors.extend(f"{state_path}: {error}" for error in context_errors)
    if context is None or context_errors:
        return ExecutionValidationOutcome(ValidationDisposition.INVALID, None)

    route_binding = state.get("route_binding", {})
    route_ref = route_binding.get("ref")
    expected_route_ref = f"route-decision.r{route_binding.get('route_revision')}.json"
    if route_ref != expected_route_ref:
        errors.append(f"{state_path}: route binding must use canonical route filename {expected_route_ref}")
    try:
        route_path = resolve_control_ref(context.control_root, route_ref)
        route, route_file_digest = load_strict_json_with_digest(route_path)
    except (StrictJSONError, TypeError, ValueError) as exc:
        errors.append(f"{state_path}: referenced route decision is invalid: {exc}")
        return ExecutionValidationOutcome(ValidationDisposition.INVALID, None)
    if not validate_registered_artifact_payload(route, route_path, errors):
        return ExecutionValidationOutcome(ValidationDisposition.INVALID, None)
    if route.get("artifact") != "route-decision":
        errors.append(f"{route_path}: execution state must reference a route-decision artifact")
        return ExecutionValidationOutcome(ValidationDisposition.INVALID, None)
    route_errors = validate_route_contract_from_repository(route, errors)
    errors.extend(f"{route_path}: {error}" for error in route_errors)

    predecessors = _load_route_predecessor_chain(route, context.control_root, errors)
    historical_states = _load_previous_execution_chain(
        state,
        route,
        predecessors,
        context.control_root,
        errors,
    )

    errors.extend(
        f"{state_path}: {error}"
        for error in validate_control_bundle(
            context.control_root,
            state_path=context.canonical_state_path,
            state=state,
            route=route,
            historical_states=historical_states,
            predecessor_routes=predecessors,
        )
    )
    _validate_structural_artifact_bindings(state, context.control_root, errors)
    for historical_state in historical_states:
        _validate_structural_artifact_bindings(historical_state, context.control_root, errors)

    lifecycle_state = state.get("lifecycle_state")
    terminal_verification: tuple[dict, str] | None = None
    if lifecycle_state in {"verified", "completed"}:
        terminal_verification = _validate_terminal_verification_schema(
            state,
            context.control_root,
            errors,
        )
        if terminal_verification is None:
            terminal_errors = ["terminal verification snapshot is unavailable"]
        else:
            verification_document, verification_digest = terminal_verification
            terminal_errors = validate_terminal_completion(
                state,
                route,
                control_root=context.control_root,
                repo_root=context.repo_root,
                verification_document=verification_document,
                verification_document_digest=verification_digest,
            )
        errors.extend(f"{state_path}: {error}" for error in terminal_errors)
        result = validate_execution_state_contract(
            state,
            route,
            approved_route_digest=approved_route_digest,
            is_canonical_current=True,
            authority_mode=True,
            terminal_validation_passed=not terminal_errors,
            approved_completion_digest=approved_completion_digest,
        )
    else:
        if approved_completion_digest is not None:
            errors.append(
                f"{state_path}: --approved-completion-digest is valid only for verified/completed state"
            )
        result = validate_execution_state_contract(
            state,
            route,
            approved_route_digest=approved_route_digest,
            is_canonical_current=True,
            authority_mode=True,
        )

    candidate_pending = result.candidate_completion_digest is not None
    if not candidate_pending:
        errors.extend(f"{state_path}: {error}" for error in result.errors)

    errors.extend(
        f"{state_path}: final control-bundle capture: {error}"
        for error in validate_control_bundle(
            context.control_root,
            state_path=context.canonical_state_path,
            state=state,
            route=route,
            historical_states=historical_states,
            predecessor_routes=predecessors,
        )
    )
    try:
        if file_sha256(state_path) != state_file_digest:
            errors.append(f"{state_path}: execution-state changed during authorization")
        if file_sha256(route_path) != route_file_digest:
            errors.append(f"{route_path}: route-decision changed during authorization")
        if terminal_verification is not None:
            attempt_id = state.get("current_completion_attempt_id")
            attempt = next(
                (
                    candidate
                    for candidate in state.get("completion_attempts", [])
                    if isinstance(candidate, dict) and candidate.get("attempt_id") == attempt_id
                ),
                None,
            )
            binding = attempt.get("completion_binding") if isinstance(attempt, dict) else None
            ref = binding.get("verification_record_ref") if isinstance(binding, dict) else None
            if not isinstance(ref, str):
                raise ValueError("terminal verification record ref is unavailable")
            verification_path = resolve_control_ref(context.control_root, ref)
            if file_sha256(verification_path) != terminal_verification[1]:
                errors.append(f"{verification_path}: verification record changed during authorization")
    except (TypeError, ValueError) as exc:
        errors.append(f"{state_path}: final content freshness check failed: {exc}")

    if candidate_pending:
        if errors:
            return ExecutionValidationOutcome(ValidationDisposition.INVALID, None)
        errors.extend(f"{state_path}: {error}" for error in result.errors)
        return ExecutionValidationOutcome(
            ValidationDisposition.APPROVAL_REQUIRED,
            None,
            result.candidate_completion_digest,
        )
    if errors:
        return ExecutionValidationOutcome(ValidationDisposition.INVALID, None)
    if result.authority not in {AUTHORITY_GATE, AUTHORITY_TERMINAL}:
        errors.append(f"{state_path}: authority result is structural-only")
        return ExecutionValidationOutcome(ValidationDisposition.INVALID, None)
    return ExecutionValidationOutcome(ValidationDisposition.VALID, result.authority)
