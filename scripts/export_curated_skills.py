#!/usr/bin/env python3
"""Export the public `skills/.curated` distribution surface."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from prodcraft_gateway_skill import render_prodcraft_skill  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "schemas" / "distribution" / "public-skill-registry.json"
PORTABILITY_REGISTRY_PATH = REPO_ROOT / "schemas" / "distribution" / "public-skill-portability.json"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "skills" / ".curated"
RESOURCE_DIRS = ("references", "scripts", "assets")
PORTABILITY_VALUES = {"portable_as_is", "portable_with_caveat", "blocked"}
PUBLIC_STABILITIES = {"beta", "stable"}
PUBLIC_READINESS = {"core", "beta", "experimental"}
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_NAME_PREFIX = "pc-"
MARKDOWN_REFERENCE_RE = re.compile(r"!?\[[^\]]*\]\((?P<target>[^)\s]+)\)")
MARKDOWN_SKILL_LINK_RE = re.compile(
    r"(?<!!)\[(?P<label>[^\]]+)\]\((?P<target>[^)\s]*SKILL\.md(?:#[^)\s]+)?)\)"
)


def load_frontmatter(path: Path) -> tuple[dict, str]:
    flags = os.O_RDONLY | os.O_NONBLOCK | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise ValueError(f"{path} must be a readable, non-symlink regular file") from exc
    with os.fdopen(descriptor, "r", encoding="utf-8") as handle:
        if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):
            raise ValueError(f"{path} must be a regular file")
        text = handle.read()
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        raise ValueError(f"{path} is missing valid YAML frontmatter")
    return yaml.safe_load(parts[1]) or {}, parts[2]


def write_skill(destination_dir: Path, frontmatter: dict, body: str) -> None:
    destination_dir.mkdir(parents=True, exist_ok=True)
    payload = f"---\n{yaml.safe_dump(frontmatter, sort_keys=False, width=10000).strip()}\n---\n\n{body.strip()}\n"
    (destination_dir / "SKILL.md").write_text(payload, encoding="utf-8")


def copy_resources(source_dir: Path, destination_dir: Path) -> None:
    for resource_dir in RESOURCE_DIRS:
        source_path = source_dir / resource_dir
        target_path = destination_dir / resource_dir
        if target_path.exists():
            shutil.rmtree(target_path)
        if source_path.exists():
            shutil.copytree(source_path, target_path, symlinks=True)


def rewrite_lifecycle_skill_links(
    body: str,
    *,
    source_dir: Path,
    canonical_skill_paths: set[Path],
    exported_skill_names: dict[Path, str],
) -> str:
    def replace(match: re.Match[str]) -> str:
        target = match.group("target")
        target_path_text, separator, fragment = target.partition("#")
        canonical_target = (source_dir / target_path_text).resolve()
        if canonical_target not in canonical_skill_paths:
            return match.group(0)

        label = match.group("label")
        exported_name = exported_skill_names.get(canonical_target)
        if exported_name is None:
            return f"`{label}`"

        anchor = f"#{fragment}" if separator else ""
        return f"[{label}](../{exported_name}/SKILL.md{anchor})"

    return MARKDOWN_SKILL_LINK_RE.sub(replace, body)


def validate_exported_surface(output_root: Path) -> None:
    for current_root, dirnames, filenames in os.walk(output_root, followlinks=False):
        current = Path(current_root)
        for dirname in dirnames:
            path = current / dirname
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
                raise ValueError(f"curated surface contains a symlink or non-directory: {path}")
        for filename in filenames:
            path = current / filename
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
                raise ValueError(f"curated surface contains a symlink or non-regular file: {path}")

    packaged_root = output_root.resolve()
    for skill_path in sorted(output_root.glob("*/SKILL.md")):
        frontmatter, body = load_frontmatter(skill_path)
        if not isinstance(frontmatter, dict):
            raise ValueError(f"{skill_path} frontmatter must load as a mapping")
        if frontmatter.get("name") != skill_path.parent.name:
            raise ValueError(f"{skill_path} frontmatter name must match its package directory")

        description = frontmatter.get("description")
        if not isinstance(description, str) or not description:
            raise ValueError(f"{skill_path} frontmatter description must be a non-empty string")
        if len(description) > 1024:
            raise ValueError(f"{skill_path} frontmatter description must be 1024 characters or fewer")

        for match in MARKDOWN_REFERENCE_RE.finditer(body):
            target = match.group("target")
            if target.startswith(("#", "/", "http://", "https://", "mailto:")):
                continue

            target_path = (skill_path.parent / target.split("#", 1)[0]).resolve()
            try:
                target_path.relative_to(packaged_root)
            except ValueError as exc:
                raise ValueError(f"{skill_path} relative reference escapes the packaged surface: {target}") from exc
            if not target_path.exists():
                raise ValueError(f"{skill_path} has dangling packaged relative reference: {target}")


def curated_note(source_path: str) -> str:
    return (
        "## Distribution\n\n"
        f"- Public install surface: `skills/.curated`\n"
        f"- Canonical authoring source: `{source_path}`\n"
        "- This package is exported for `npx skills add/update` compatibility.\n"
    )


def portability_note(portability_entry: dict) -> str:
    """Ship the portability class and caveat inside the package body.

    Agent runtimes read SKILL.md, not index.json, so the caveat must travel
    with the skill to prevent public overclaim.
    """
    lines = [f"- Portability: `{portability_entry['portability']}`\n"]
    caveat = portability_entry.get("public_caveat_text", "")
    if caveat:
        lines.append(f"- Public caveat: {caveat}\n")
    return "".join(lines)


def validate_public_skill_name(name: object, *, source: Path) -> str:
    if not isinstance(name, str) or not name:
        raise ValueError(f"{source}: public skill name must be a non-empty string")
    if len(name) > 64 or not SKILL_NAME_RE.fullmatch(name):
        raise ValueError(f"{source}: public skill name {name!r} must follow Agent Skills name syntax")
    if not name.startswith(SKILL_NAME_PREFIX):
        raise ValueError(f"{source}: public skill name {name!r} must start with pc-")
    return name


def validate_public_source_tree(*, repo_root: Path, source: str, registry_path: Path) -> Path:
    relative = Path(source)
    if (
        relative.is_absolute()
        or "\\" in source
        or ":" in source
        or any(part in {"", ".", ".."} for part in relative.parts)
    ):
        raise ValueError(f"{registry_path}: public skill source is unsafe: {source}")

    source_dir = repo_root
    for part in relative.parts:
        source_dir /= part
        try:
            mode = source_dir.lstat().st_mode
        except FileNotFoundError as exc:
            raise ValueError(f"{registry_path}: public skill source is missing: {source}") from exc
        if stat.S_ISLNK(mode):
            raise ValueError(f"{registry_path}: public skill source contains a symlink: {source}")
    if not stat.S_ISDIR(source_dir.lstat().st_mode):
        raise ValueError(f"{registry_path}: public skill source must be a directory: {source}")

    skill_path = source_dir / "SKILL.md"
    try:
        skill_mode = skill_path.lstat().st_mode
    except FileNotFoundError as exc:
        raise ValueError(f"public skill source is missing {skill_path}") from exc
    if stat.S_ISLNK(skill_mode) or not stat.S_ISREG(skill_mode):
        raise ValueError(f"public skill source must contain a regular, non-symlink SKILL.md: {skill_path}")

    for resource_name in RESOURCE_DIRS:
        resource_root = source_dir / resource_name
        if not resource_root.exists() and not resource_root.is_symlink():
            continue
        resource_mode = resource_root.lstat().st_mode
        if stat.S_ISLNK(resource_mode) or not stat.S_ISDIR(resource_mode):
            raise ValueError(f"public skill resource root must be a regular directory: {resource_root}")
        for current_root, dirnames, filenames in os.walk(resource_root, followlinks=False):
            current = Path(current_root)
            for dirname in dirnames:
                path = current / dirname
                mode = path.lstat().st_mode
                if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
                    raise ValueError(f"public skill resource tree contains a symlink or non-directory: {path}")
            for filename in filenames:
                path = current / filename
                mode = path.lstat().st_mode
                if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
                    raise ValueError(f"public skill resource tree contains a symlink or non-regular file: {path}")

    try:
        source_dir.resolve(strict=True).relative_to(repo_root.resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise ValueError(f"public skill source escapes the repository: {source}") from exc
    return source_dir


def load_public_registry(repo_root: Path) -> dict:
    registry_path = repo_root / REGISTRY_PATH.relative_to(REPO_ROOT)
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    if registry.get("schema_version") != "public-skill-registry.v1":
        raise ValueError("public skill registry must use schema_version public-skill-registry.v1")
    entries = registry.get("public_skills")
    if not isinstance(entries, list):
        raise ValueError("public skill registry must include a public_skills list")

    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("each public skill entry must be an object")
        missing = {"name", "source", "stability", "readiness"} - set(entry)
        if missing:
            raise ValueError(f"public skill entry is missing fields {sorted(missing)}")
        name = validate_public_skill_name(entry.get("name"), source=registry_path)
        if name in seen:
            raise ValueError(f"duplicate public skill entry {name}")
        seen.add(name)
        if entry.get("stability") not in PUBLIC_STABILITIES:
            raise ValueError(f"public skill {name} has invalid stability {entry.get('stability')}")
        if entry.get("readiness") not in PUBLIC_READINESS:
            raise ValueError(f"public skill {name} has invalid readiness {entry.get('readiness')}")

        source = entry.get("source")
        if not isinstance(source, str) or not source:
            raise ValueError(f"public skill {name} must include a non-empty source")
        if source == "generated:prodcraft":
            if name != "pc-prodcraft":
                raise ValueError("generated:prodcraft must be exported as pc-prodcraft")
            continue

        source_dir = validate_public_source_tree(
            repo_root=repo_root,
            source=source,
            registry_path=registry_path,
        )
        skill_path = source_dir / "SKILL.md"
        frontmatter, _body = load_frontmatter(skill_path)
        if frontmatter.get("name") != name:
            raise ValueError(
                f"public skill {name} does not match source frontmatter name {frontmatter.get('name')!r}"
            )

    return registry


def load_portability_metadata(repo_root: Path, public_skill_names: set[str]) -> dict[str, dict]:
    registry_path = repo_root / PORTABILITY_REGISTRY_PATH.relative_to(REPO_ROOT)
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    if registry.get("schema_version") != "public-skill-portability.v1":
        raise ValueError("public portability registry must use schema_version public-skill-portability.v1")
    skills = registry.get("skills")
    if not isinstance(skills, list):
        raise ValueError("public portability registry must include a skills list")

    entries: dict[str, dict] = {}
    for entry in skills:
        if not isinstance(entry, dict):
            raise ValueError("each public portability entry must be an object")
        name = entry.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError("each public portability entry must include a non-empty name")
        validate_public_skill_name(name, source=registry_path)
        if name in entries:
            raise ValueError(f"duplicate public portability entry {name}")

        portability = entry.get("portability")
        hidden_dependencies = entry.get("hidden_dependencies")
        required_context = entry.get("required_context")
        public_caveat = entry.get("public_caveat_text")
        if portability not in PORTABILITY_VALUES:
            raise ValueError(f"public portability entry {name} has invalid portability {portability}")
        if not isinstance(hidden_dependencies, list) or any(
            not isinstance(item, str) or not item for item in hidden_dependencies
        ):
            raise ValueError(f"public portability entry {name} must include a string hidden_dependencies list")
        if not isinstance(required_context, str):
            raise ValueError(f"public portability entry {name} must include string required_context")
        if not isinstance(public_caveat, str):
            raise ValueError(f"public portability entry {name} must include string public_caveat_text")
        if portability == "portable_as_is" and (hidden_dependencies or public_caveat):
            raise ValueError(f"portable_as_is entry {name} must not declare hidden dependencies or public caveat text")
        if portability == "portable_with_caveat" and (not required_context or not public_caveat):
            raise ValueError(f"portable_with_caveat entry {name} must include required_context and public_caveat_text")
        if portability == "blocked":
            raise ValueError(f"blocked skill {name} cannot be exported to the curated public surface")
        entries[name] = entry

    metadata_names = set(entries)
    missing = sorted(public_skill_names - metadata_names)
    extra = sorted(metadata_names - public_skill_names)
    if missing:
        raise ValueError(f"missing public portability metadata for {missing}")
    if extra:
        raise ValueError(f"public portability metadata contains non-exported skills {extra}")

    return entries


def export_entry(
    entry: dict,
    *,
    repo_root: Path,
    output_root: Path,
    canonical_skill_paths: set[Path],
    exported_skill_names: dict[Path, str],
    portability_entry: dict,
) -> None:
    destination_dir = output_root / entry["name"]
    if destination_dir.exists():
        shutil.rmtree(destination_dir)

    if entry["source"] == "generated:prodcraft":
        destination_dir.mkdir(parents=True, exist_ok=True)
        rendered = render_prodcraft_skill(
            repo_root,
            install_surface="curated",
            public_stability=entry["stability"],
            public_readiness=entry["readiness"],
        )
        # The rendered body ends inside its Distribution list; the portability
        # note continues that list.
        (destination_dir / "SKILL.md").write_text(
            f"{rendered.rstrip()}\n{portability_note(portability_entry)}",
            encoding="utf-8",
        )
        return

    source_dir = repo_root / entry["source"]
    frontmatter, body = load_frontmatter(source_dir / "SKILL.md")
    metadata = frontmatter.setdefault("metadata", {})
    metadata["internal"] = bool(entry.get("internal", False))
    metadata["distribution_surface"] = "curated"
    metadata["source_path"] = str((source_dir / "SKILL.md").relative_to(repo_root))
    metadata["public_stability"] = entry["stability"]
    metadata["public_readiness"] = entry["readiness"]
    body = rewrite_lifecycle_skill_links(
        body,
        source_dir=source_dir,
        canonical_skill_paths=canonical_skill_paths,
        exported_skill_names=exported_skill_names,
    )

    write_skill(
        destination_dir,
        frontmatter,
        (
            f"{body.strip()}\n\n"
            f"{curated_note(metadata['source_path'])}"
            f"- Packaging stability: `{entry['stability']}`\n"
            f"- Capability readiness: `{entry['readiness']}`\n"
            f"{portability_note(portability_entry)}"
        ),
    )
    copy_resources(source_dir, destination_dir)


def materialize_curated_skills(
    *,
    registry: dict,
    portability: dict[str, dict],
    repo_root: Path,
    output_root: Path,
    canonical_skill_paths: set[Path],
    exported_skill_names: dict[Path, str],
) -> list[str]:
    output_root.mkdir(parents=True, exist_ok=False)
    exported_names: list[str] = []
    index_entries: list[dict[str, object]] = []
    for entry in registry["public_skills"]:
        portability_entry = portability[entry["name"]]
        export_entry(
            entry,
            repo_root=repo_root,
            output_root=output_root,
            canonical_skill_paths=canonical_skill_paths,
            exported_skill_names=exported_skill_names,
            portability_entry=portability_entry,
        )
        exported_names.append(entry["name"])
        index_entry = {
            "name": entry["name"],
            "source": entry["source"],
            "stability": entry["stability"],
            "readiness": entry["readiness"],
            "manual_allowlist": bool(entry.get("manual_allowlist", False)),
            "portability": portability_entry["portability"],
        }
        public_caveat = portability_entry.get("public_caveat_text", "")
        if public_caveat:
            index_entry["public_caveat_text"] = public_caveat
        index_entries.append(index_entry)

    (output_root / "index.json").write_text(
        json.dumps({"schema_version": "curated-surface.v1", "skills": index_entries}, indent=2) + "\n",
        encoding="utf-8",
    )
    validate_exported_surface(output_root)
    return exported_names


def export_curated_skills(*, repo_root: Path = REPO_ROOT, output_root: Path = DEFAULT_OUTPUT_ROOT) -> dict[str, list[str]]:
    registry = load_public_registry(repo_root)
    public_skill_names = {
        entry["name"]
        for entry in registry["public_skills"]
    }
    canonical_skill_paths = {
        path.resolve()
        for path in (repo_root / "skills").glob("*/*/SKILL.md")
        if ".curated" not in path.parts
    }
    exported_skill_names = {
        (repo_root / entry["source"] / "SKILL.md").resolve(): entry["name"]
        for entry in registry["public_skills"]
        if entry["source"] != "generated:prodcraft"
    }
    portability = load_portability_metadata(repo_root, public_skill_names)
    output_root.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix=f".{output_root.name}.staging-", dir=output_root.parent) as tmpdir:
        transaction_root = Path(tmpdir)
        staged_root = transaction_root / "surface"
        exported_names = materialize_curated_skills(
            registry=registry,
            portability=portability,
            repo_root=repo_root,
            output_root=staged_root,
            canonical_skill_paths=canonical_skill_paths,
            exported_skill_names=exported_skill_names,
        )

        backup_root = transaction_root / "previous"
        had_previous = output_root.exists()
        try:
            if had_previous:
                output_root.rename(backup_root)
            staged_root.rename(output_root)
        except BaseException:
            if had_previous and backup_root.exists() and not output_root.exists():
                backup_root.rename(output_root)
            raise

    return {"skills": exported_names}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export the curated Prodcraft skill distribution surface.")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = export_curated_skills(repo_root=args.repo_root, output_root=args.output_root)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
