#!/usr/bin/env python3
"""Export the public `skills/.curated` distribution surface."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from prodcraft_gateway_skill import render_prodcraft_skill


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "schemas" / "distribution" / "public-skill-registry.json"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "skills" / ".curated"
RESOURCE_DIRS = ("references", "scripts", "assets")


def load_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
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
            shutil.copytree(source_path, target_path)


def curated_note(source_path: str) -> str:
    return (
        "## Distribution\n\n"
        f"- Public install surface: `skills/.curated`\n"
        f"- Canonical authoring source: `{source_path}`\n"
        "- This package is exported for `npx skills add/update` compatibility.\n"
    )


def export_entry(entry: dict, *, repo_root: Path, output_root: Path) -> None:
    destination_dir = output_root / entry["name"]
    if destination_dir.exists():
        shutil.rmtree(destination_dir)

    if entry["source"] == "generated:prodcraft":
        destination_dir.mkdir(parents=True, exist_ok=True)
        (destination_dir / "SKILL.md").write_text(
            render_prodcraft_skill(
                repo_root,
                install_surface="curated",
                public_stability=entry["stability"],
                public_readiness=entry["readiness"],
            ),
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

    write_skill(
        destination_dir,
        frontmatter,
        (
            f"{body.strip()}\n\n"
            f"{curated_note(metadata['source_path'])}"
            f"- Packaging stability: `{entry['stability']}`\n"
            f"- Capability readiness: `{entry['readiness']}`\n"
        ),
    )
    copy_resources(source_dir, destination_dir)


def export_curated_skills(*, repo_root: Path = REPO_ROOT, output_root: Path = DEFAULT_OUTPUT_ROOT) -> dict[str, list[str]]:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    output_root.mkdir(parents=True, exist_ok=True)

    for existing in output_root.iterdir():
        if existing.is_dir():
            shutil.rmtree(existing)
        else:
            existing.unlink()

    exported_names: list[str] = []
    index_entries: list[dict[str, object]] = []
    for entry in registry["public_skills"]:
        export_entry(entry, repo_root=repo_root, output_root=output_root)
        exported_names.append(entry["name"])
        index_entries.append(
            {
                "name": entry["name"],
                "source": entry["source"],
                "stability": entry["stability"],
                "readiness": entry["readiness"],
                "manual_allowlist": bool(entry.get("manual_allowlist", False)),
            }
        )

    (output_root / "index.json").write_text(
        json.dumps({"schema_version": "curated-surface.v1", "skills": index_entries}, indent=2) + "\n",
        encoding="utf-8",
    )
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
