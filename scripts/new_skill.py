#!/usr/bin/env python3
"""Create a validated, draft-only Prodcraft skill authoring package."""

from __future__ import annotations

import argparse
import ctypes
import fcntl
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, NamedTuple

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_REL = Path("manifest.yml")
PUBLIC_REGISTRY_REL = Path("schemas/distribution/public-skill-registry.json")
VALID_PHASES = {
    "00-discovery",
    "01-specification",
    "02-architecture",
    "03-planning",
    "04-implementation",
    "05-quality",
    "06-delivery",
    "07-operations",
    "08-evolution",
    "cross-cutting",
}
SKILL_NAME_RE = re.compile(r"^pc-[a-z0-9]+(?:-[a-z0-9]+)*$")
TOP_LEVEL_KEY_RE = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_-]*):.*$", re.MULTILINE)

Validator = Callable[[Path], None]
Replace = Callable[[str | os.PathLike[str], str | os.PathLike[str]], None]
Exchange = Callable[[str | os.PathLike[str], str | os.PathLike[str]], None]


class ScaffoldError(RuntimeError):
    """Raised when a scaffold cannot be committed safely."""


class ScaffoldResult(NamedTuple):
    skill_path: Path
    eval_strategy_path: Path
    manifest_path: Path


def _load_yaml_mapping(path: Path) -> dict:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        raise ScaffoldError(f"failed to load {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ScaffoldError(f"{path} must contain a YAML mapping")
    return value


def _load_public_names(path: Path) -> set[str]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ScaffoldError(f"failed to load {path}: {exc}") from exc
    entries = payload.get("public_skills") if isinstance(payload, dict) else None
    if not isinstance(entries, list):
        raise ScaffoldError(f"{path} must contain a `public_skills` list")
    return {
        entry["name"]
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("name"), str)
    }


def _lexists(path: Path) -> bool:
    """Return True for regular paths and dangling symlinks."""

    return os.path.lexists(path)


def _native_rename(
    source: str | os.PathLike[str],
    target: str | os.PathLike[str],
    *,
    darwin_flag: int,
    linux_flag: int,
    operation: str,
) -> None:
    source_bytes = os.fsencode(source)
    target_bytes = os.fsencode(target)
    libc = ctypes.CDLL(None, use_errno=True)
    system = platform.system()
    if system == "Darwin" and hasattr(libc, "renamex_np"):
        rename = libc.renamex_np
        rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
        rename.restype = ctypes.c_int
        result = rename(source_bytes, target_bytes, darwin_flag)
    elif system == "Linux" and hasattr(libc, "renameat2"):
        rename = libc.renameat2
        rename.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        ]
        rename.restype = ctypes.c_int
        result = rename(-100, source_bytes, -100, target_bytes, linux_flag)
    else:
        raise ScaffoldError(
            f"atomic {operation} is unavailable on this platform; refusing an unsafe write"
        )
    if result != 0:
        error_number = ctypes.get_errno()
        raise OSError(error_number, os.strerror(error_number), os.fspath(target))


def atomic_exchange(
    source: str | os.PathLike[str], target: str | os.PathLike[str]
) -> None:
    """Atomically swap two paths on the supported local POSIX filesystems."""

    _native_rename(
        source,
        target,
        darwin_flag=0x00000002,  # RENAME_SWAP
        linux_flag=0x00000002,  # RENAME_EXCHANGE
        operation="manifest exchange",
    )


def atomic_move_no_replace(
    source: str | os.PathLike[str], target: str | os.PathLike[str]
) -> None:
    """Atomically move source while refusing to replace any target path."""

    _native_rename(
        source,
        target,
        darwin_flag=0x00000004,  # RENAME_EXCL
        linux_flag=0x00000001,  # RENAME_NOREPLACE
        operation="no-replace move",
    )


@contextmanager
def _repo_transaction_lock(repo_root: Path):
    """Serialize cooperating scaffold transactions without creating a lock file."""

    descriptor = os.open(repo_root, os.O_RDONLY)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
    except OSError as exc:
        os.close(descriptor)
        raise ScaffoldError(f"could not hold repository scaffold lock: {exc}") from exc
    try:
        yield
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


def _require_real_repo_path(repo_root: Path, path: Path, *, kind: str) -> None:
    if path.is_symlink():
        raise ScaffoldError(f"{kind} must not be a symlink: {path}")
    try:
        path.resolve().relative_to(repo_root)
    except ValueError as exc:
        raise ScaffoldError(f"{kind} escapes the repository root: {path}") from exc


def _validate_request(repo_root: Path, phase: str, name: str, manifest: dict) -> bool:
    if phase not in VALID_PHASES:
        raise ScaffoldError(f"invalid phase `{phase}`; expected one of {sorted(VALID_PHASES)}")
    if not SKILL_NAME_RE.fullmatch(name):
        raise ScaffoldError(
            f"invalid skill name `{name}`; expected a canonical `pc-` kebab-case name"
        )

    skills = manifest.get("skills")
    if not isinstance(skills, list):
        raise ScaffoldError(f"{repo_root / MANIFEST_REL}: `skills` must be a list")
    implemented = {
        entry.get("name")
        for entry in skills
        if isinstance(entry, dict) and isinstance(entry.get("name"), str)
    }
    if name in implemented:
        raise ScaffoldError(f"skill `{name}` is already implemented")

    planned = manifest.get("planned_skills", [])
    if planned is None:
        planned = []
    if not isinstance(planned, list):
        raise ScaffoldError(f"{repo_root / MANIFEST_REL}: `planned_skills` must be a list")
    matches = [entry for entry in planned if isinstance(entry, dict) and entry.get("name") == name]
    if len(matches) > 1:
        raise ScaffoldError(f"planned skill `{name}` appears more than once")
    if matches and matches[0].get("phase") != phase:
        raise ScaffoldError(
            f"planned skill `{name}` belongs to phase `{matches[0].get('phase')}`, not `{phase}`"
        )
    expected_target = f"skills/{phase}/{name}/SKILL.md"
    if matches and matches[0].get("target_file") != expected_target:
        raise ScaffoldError(
            f"planned skill `{name}` has non-canonical target_file "
            f"`{matches[0].get('target_file')}`; expected `{expected_target}`"
        )

    public_names = _load_public_names(repo_root / PUBLIC_REGISTRY_REL)
    if name in public_names:
        raise ScaffoldError(
            f"skill `{name}` is already reserved by the public distribution registry; "
            "draft scaffolding must not mutate promotion surfaces"
        )

    skill_dir = repo_root / "skills" / phase / name
    eval_dir = repo_root / "eval" / phase / name
    if _lexists(skill_dir) or _lexists(eval_dir):
        collisions = [str(path) for path in (skill_dir, eval_dir) if _lexists(path)]
        raise ScaffoldError(f"scaffold destination already exists: {', '.join(collisions)}")
    for surface_root, parent in (
        (repo_root / "skills", skill_dir.parent),
        (repo_root / "eval", eval_dir.parent),
    ):
        _require_real_repo_path(repo_root, surface_root, kind="authoring root")
        _require_real_repo_path(repo_root, parent, kind="lifecycle phase directory")
        if not parent.is_dir():
            raise ScaffoldError(f"expected lifecycle parent directory does not exist: {parent}")

    return bool(matches)


def _title_for(name: str) -> str:
    return " ".join(part.capitalize() for part in name.removeprefix("pc-").split("-"))


def _render_skill(phase: str, name: str) -> str:
    title = _title_for(name)
    return f"""---
name: {name}
description: Use when a reviewed capability needs a dedicated Prodcraft skill before its implementation, routing, and evidence contract are finalized.
metadata:
  phase: {phase}
  inputs: []
  outputs: []
  prerequisites: []
  quality_gate: Draft contract reviewed with measurable acceptance criteria
  roles:
  - developer
  methodologies:
  - all
  effort: medium
---

# {title}

> Define the capability contract before promoting this draft into routed work.

## Context

This draft reserves a focused Prodcraft capability. Refine its boundary from reviewed requirements before adding it to workflows or public distribution.

## Inputs

No lifecycle artifacts are declared while the skill is in draft.

## Process

1. Confirm the capability boundary and the problem that requires a dedicated skill.
2. Define concrete inputs, outputs, stop conditions, and failure handling.
3. Add evaluation scenarios that can distinguish useful behavior from plausible prose.
4. Request review before changing maturity, routing, or distribution surfaces.

## Outputs

No lifecycle artifacts are declared while the skill is in draft.

## Quality Gate

- [ ] The capability boundary is specific and does not duplicate an existing skill.
- [ ] Inputs, outputs, and acceptance criteria are backed by reviewed requirements.
- [ ] Evaluation scenarios include at least one failure or unsupported-flow case.

## Anti-Patterns

1. **Premature routing** -- Do not reference a draft skill from workflows before review.
2. **Premature publication** -- Do not add a draft to distribution registries or curated packages.
3. **Invented artifact flow** -- Keep inputs and outputs empty until their contracts are reviewed.
"""


def _render_eval_strategy(name: str) -> str:
    title = _title_for(name)
    return f"""# {title} Eval Strategy

## Goal

Determine whether `{name}` provides a distinct, useful capability with a reviewable contract.

## Scenarios

1. A representative task that should invoke the skill after its contract is complete.
2. A neighboring task that should remain with an existing skill.
3. A failure or unsupported-flow case that should stop or escalate.

## Assertions

1. The skill stays within its declared capability boundary.
2. Outputs satisfy explicit acceptance criteria rather than prose-only quality claims.
3. Failure handling and escalation behavior are observable.

## Method

Define the baseline, runner and model versions, scenario-set version, rubric, and evidence paths before running the evaluation.

## Exit Criteria

Keep the skill in `draft` until its contract, scenarios, and review evidence justify promotion.
"""


def _manifest_entry(phase: str, name: str) -> str:
    return (
        f"- name: {name}\n"
        f"  phase: {phase}\n"
        f"  file: skills/{phase}/{name}/SKILL.md\n"
        "  status: draft\n"
        "  qa_tier: standard\n"
        "  evaluation_mode: routed\n"
        "  qa:\n"
        "    structure_validation_path: scripts/validate_prodcraft.py\n"
        f"    eval_strategy_path: eval/{phase}/{name}/evals/eval-strategy.md\n"
    )


def _section_bounds(text: str, key: str) -> tuple[int, int, int]:
    match = re.search(rf"^{re.escape(key)}:(?P<value>[^\n]*)\n", text, re.MULTILINE)
    if not match:
        raise ScaffoldError(f"manifest is missing top-level `{key}` section")
    next_key = TOP_LEVEL_KEY_RE.search(text, match.end())
    end = next_key.start() if next_key else len(text)
    return match.start(), match.end(), end


def _remove_planned_entry(text: str, name: str) -> str:
    section_start, content_start, section_end = _section_bounds(text, "planned_skills")
    section = text[content_start:section_end]
    item_matches = list(re.finditer(r"^- name: (?P<name>[^\n]+)\n", section, re.MULTILINE))
    target_indexes = [index for index, match in enumerate(item_matches) if match.group("name") == name]
    if len(target_indexes) != 1:
        raise ScaffoldError(f"could not locate exactly one planned manifest block for `{name}`")
    target_index = target_indexes[0]
    start = item_matches[target_index].start()
    end = item_matches[target_index + 1].start() if target_index + 1 < len(item_matches) else len(section)
    updated_section = section[:start] + section[end:]
    if not list(re.finditer(r"^- name: ", updated_section, re.MULTILINE)):
        return text[:section_start] + "planned_skills: []\n" + text[section_end:]
    return text[:content_start] + updated_section + text[section_end:]


def _insert_skill_entry(text: str, phase: str, name: str) -> str:
    _section_start, content_start, section_end = _section_bounds(text, "skills")
    header = text[_section_start:content_start]
    if header.strip() == "skills: []":
        return text[:_section_start] + "skills:\n" + _manifest_entry(phase, name) + text[section_end:]
    insertion = _manifest_entry(phase, name)
    return text[:section_end] + insertion + text[section_end:]


def _updated_manifest(original: bytes, phase: str, name: str, remove_planned: bool) -> bytes:
    try:
        text = original.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ScaffoldError("manifest.yml must be UTF-8") from exc
    if remove_planned:
        text = _remove_planned_entry(text, name)
    text = _insert_skill_entry(text, phase, name)
    parsed = yaml.safe_load(text)
    if not isinstance(parsed, dict):
        raise ScaffoldError("generated manifest candidate is not a mapping")
    names = [entry.get("name") for entry in parsed.get("skills", []) if isinstance(entry, dict)]
    if names.count(name) != 1:
        raise ScaffoldError(f"generated manifest must contain exactly one `{name}` skill entry")
    planned_names = [
        entry.get("name")
        for entry in parsed.get("planned_skills", []) or []
        if isinstance(entry, dict)
    ]
    if name in planned_names:
        raise ScaffoldError(f"generated manifest still contains planned skill `{name}`")
    return text.encode("utf-8")


def _copy_candidate(repo_root: Path, candidate_root: Path) -> None:
    ignored_names = {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "node_modules",
    }

    def ignore(_directory: str, names: list[str]) -> set[str]:
        return {
            name
            for name in names
            if name in ignored_names or name == ".DS_Store" or name.startswith(".new-skill-stage-")
        }

    shutil.copytree(repo_root, candidate_root, symlinks=True, ignore=ignore)


def _write_candidate(candidate_root: Path, phase: str, name: str, manifest_bytes: bytes) -> None:
    skill_path = candidate_root / "skills" / phase / name / "SKILL.md"
    strategy_path = candidate_root / "eval" / phase / name / "evals" / "eval-strategy.md"
    skill_path.parent.mkdir(parents=True)
    strategy_path.parent.mkdir(parents=True)
    skill_path.write_text(_render_skill(phase, name), encoding="utf-8")
    strategy_path.write_text(_render_eval_strategy(name), encoding="utf-8")
    (candidate_root / MANIFEST_REL).write_bytes(manifest_bytes)


def _run_repo_validator(candidate_root: Path) -> None:
    validator_path = candidate_root / "scripts" / "validate_prodcraft.py"
    if not validator_path.is_file():
        raise ScaffoldError(f"candidate validator does not exist: {validator_path}")
    completed = subprocess.run(
        [sys.executable, str(validator_path)],
        cwd=candidate_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = "\n".join(part.strip() for part in (completed.stdout, completed.stderr) if part.strip())
        suffix = f":\n{detail}" if detail else ""
        raise ScaffoldError(
            f"candidate repository validator failed with exit code {completed.returncode}{suffix}"
        )


def _remove_empty_directory(path: Path, rollback_errors: list[str]) -> None:
    if not _lexists(path):
        return
    if path.is_symlink() or not path.is_dir():
        rollback_errors.append(f"preserved non-directory concurrent path {path}")
        return
    try:
        path.rmdir()
    except OSError:
        rollback_errors.append(f"preserved concurrent content under {path}")


def _rollback_owned_file(
    path: Path,
    expected: bytes,
    quarantine: Path,
    rollback_errors: list[str],
) -> bool:
    """Quarantine a rollback target before inspecting or deleting owned bytes.

    Return False only when non-owned bytes could not be restored and the private
    quarantine must be retained for recovery.
    """

    if not _lexists(path):
        return True
    quarantine.parent.mkdir(parents=True, exist_ok=True)
    try:
        atomic_move_no_replace(path, quarantine)
    except FileNotFoundError:
        return True
    except OSError as exc:
        rollback_errors.append(f"could not quarantine rollback target {path}: {exc}")
        return True

    def restore_non_owned(reason: str) -> bool:
        try:
            atomic_move_no_replace(quarantine, path)
        except OSError as exc:
            rollback_errors.append(
                f"rollback conflict for {path}: {reason}; preserved displaced bytes at "
                f"{quarantine}: {exc}"
            )
            return False
        rollback_errors.append(f"preserved concurrent replacement at {path}: {reason}")
        return True

    if quarantine.is_symlink() or not quarantine.is_file():
        return restore_non_owned("quarantined path is not a regular file")
    try:
        current = quarantine.read_bytes()
    except OSError as exc:
        return restore_non_owned(f"could not inspect quarantined bytes: {exc}")
    if current != expected:
        return restore_non_owned("bytes are not transaction-owned")
    try:
        quarantine.unlink()
    except OSError as exc:
        rollback_errors.append(
            f"failed to remove quarantined transaction-owned file {quarantine}: {exc}"
        )
        return False
    return True


def _commit_candidate(
    repo_root: Path,
    candidate_root: Path,
    phase: str,
    name: str,
    original_manifest: bytes,
    new_manifest: bytes,
    replace_fn: Replace,
    exchange_fn: Exchange,
) -> ScaffoldResult:
    manifest_path = repo_root / MANIFEST_REL
    skill_dir = repo_root / "skills" / phase / name
    eval_dir = repo_root / "eval" / phase / name
    if manifest_path.read_bytes() != original_manifest:
        raise ScaffoldError("manifest.yml changed during candidate validation; refusing to overwrite it")
    if _lexists(skill_dir) or _lexists(eval_dir):
        raise ScaffoldError("scaffold destination appeared during candidate validation")

    stage_root = Path(tempfile.mkdtemp(prefix=".new-skill-stage-", dir=repo_root))
    committed_skill = False
    committed_eval = False
    manifest_exchanged = False
    preserve_stage_root = False
    expected_skill = (candidate_root / "skills" / phase / name / "SKILL.md").read_bytes()
    expected_strategy = (
        candidate_root / "eval" / phase / name / "evals" / "eval-strategy.md"
    ).read_bytes()
    try:
        staged_skill = stage_root / "skill"
        staged_eval = stage_root / "eval"
        staged_manifest = stage_root / "manifest.yml"
        shutil.copytree(candidate_root / "skills" / phase / name, staged_skill)
        shutil.copytree(candidate_root / "eval" / phase / name, staged_eval)
        staged_manifest.write_bytes(new_manifest)
        os.chmod(staged_manifest, manifest_path.stat().st_mode)

        replace_fn(staged_skill, skill_dir)
        committed_skill = True
        replace_fn(staged_eval, eval_dir)
        committed_eval = True
        if manifest_path.read_bytes() != original_manifest:
            raise ScaffoldError(
                "manifest.yml changed during scaffold commit; preserving the concurrent write"
            )
        exchange_fn(staged_manifest, manifest_path)
        manifest_exchanged = True
        displaced_manifest = staged_manifest.read_bytes()
        current_manifest = manifest_path.read_bytes()
        if displaced_manifest != original_manifest:
            if current_manifest != new_manifest:
                manifest_exchanged = False
                preserve_stage_root = True
                raise ScaffoldError(
                    "manifest.yml changed both before and after the atomic exchange; "
                    f"the current writer was preserved and displaced bytes remain at {staged_manifest}"
                )
            exchange_fn(staged_manifest, manifest_path)
            manifest_exchanged = False
            raise ScaffoldError(
                "manifest.yml changed at the atomic exchange boundary; concurrent bytes were restored"
            )
        if current_manifest != new_manifest:
            manifest_exchanged = False
            raise ScaffoldError(
                "manifest.yml was overwritten after the atomic exchange; preserving the concurrent write"
            )
    except Exception as exc:
        rollback_errors: list[str] = []
        if manifest_exchanged:
            try:
                if manifest_path.read_bytes() != new_manifest:
                    rollback_errors.append(
                        "preserved concurrent manifest write instead of exchanging it back"
                    )
                    manifest_exchanged = False
                else:
                    exchange_fn(staged_manifest, manifest_path)
                    manifest_exchanged = False
            except Exception as rollback_exc:  # pragma: no cover - catastrophic local FS failure
                rollback_errors.append(f"manifest exchange-back failed: {rollback_exc}")
                preserve_stage_root = True
        rollback_quarantine = stage_root / "rollback-quarantine"
        if committed_eval:
            preserve_stage_root = not _rollback_owned_file(
                eval_dir / "evals" / "eval-strategy.md",
                expected_strategy,
                rollback_quarantine / "eval-strategy.md",
                rollback_errors,
            ) or preserve_stage_root
            _remove_empty_directory(eval_dir / "evals", rollback_errors)
            _remove_empty_directory(eval_dir, rollback_errors)
        if committed_skill:
            preserve_stage_root = not _rollback_owned_file(
                skill_dir / "SKILL.md",
                expected_skill,
                rollback_quarantine / "SKILL.md",
                rollback_errors,
            ) or preserve_stage_root
            _remove_empty_directory(skill_dir, rollback_errors)
        detail = f"; rollback errors: {'; '.join(rollback_errors)}" if rollback_errors else ""
        raise ScaffoldError(f"failed to commit validated scaffold: {exc}{detail}") from exc
    finally:
        if not preserve_stage_root:
            shutil.rmtree(stage_root, ignore_errors=True)

    return ScaffoldResult(
        skill_path=skill_dir / "SKILL.md",
        eval_strategy_path=eval_dir / "evals" / "eval-strategy.md",
        manifest_path=manifest_path,
    )


def scaffold_skill(
    repo_root: Path,
    phase: str,
    name: str,
    *,
    validator: Validator | None = None,
    replace_fn: Replace = atomic_move_no_replace,
    exchange_fn: Exchange = atomic_exchange,
) -> ScaffoldResult:
    """Create and validate a draft skill, committing only after candidate validation."""

    repo_root = repo_root.resolve()
    with _repo_transaction_lock(repo_root):
        return _scaffold_skill_locked(
            repo_root,
            phase,
            name,
            validator=validator,
            replace_fn=replace_fn,
            exchange_fn=exchange_fn,
        )


def _scaffold_skill_locked(
    repo_root: Path,
    phase: str,
    name: str,
    *,
    validator: Validator | None,
    replace_fn: Replace,
    exchange_fn: Exchange,
) -> ScaffoldResult:
    manifest_path = repo_root / MANIFEST_REL
    registry_path = repo_root / PUBLIC_REGISTRY_REL
    _require_real_repo_path(repo_root, manifest_path, kind="manifest")
    _require_real_repo_path(repo_root, registry_path, kind="public registry")
    original_manifest = manifest_path.read_bytes()
    original_registry = registry_path.read_bytes()
    manifest = _load_yaml_mapping(manifest_path)
    remove_planned = _validate_request(repo_root, phase, name, manifest)
    candidate_manifest = _updated_manifest(original_manifest, phase, name, remove_planned)

    with tempfile.TemporaryDirectory(prefix="prodcraft-new-skill-", dir=repo_root.parent) as tmpdir:
        candidate_root = Path(tmpdir) / "repo"
        _copy_candidate(repo_root, candidate_root)
        _write_candidate(candidate_root, phase, name, candidate_manifest)
        try:
            (validator or _run_repo_validator)(candidate_root)
        except Exception as exc:
            if isinstance(exc, ScaffoldError):
                raise
            raise ScaffoldError(f"candidate repository validation failed: {exc}") from exc

        if registry_path.read_bytes() != original_registry:
            raise ScaffoldError(
                "public skill registry changed during candidate validation; refusing stale collision checks"
            )
        return _commit_candidate(
            repo_root,
            candidate_root,
            phase,
            name,
            original_manifest,
            candidate_manifest,
            replace_fn,
            exchange_fn,
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create a validated draft Prodcraft skill without changing promotion surfaces."
    )
    parser.add_argument("phase", help="Lifecycle phase directory, for example 04-implementation")
    parser.add_argument("name", help="Canonical pc- skill name")
    args = parser.parse_args(argv)
    try:
        result = scaffold_skill(REPO_ROOT, args.phase, args.name)
    except (OSError, ScaffoldError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Created draft skill: {result.skill_path.relative_to(REPO_ROOT)}")
    print(f"Created eval strategy: {result.eval_strategy_path.relative_to(REPO_ROOT)}")
    print("Promotion surfaces were not modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
