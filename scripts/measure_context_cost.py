#!/usr/bin/env python3
"""Measure the static runtime context cost of the Prodcraft surface.

Every installed skill description is always-on context; the gateway, intake,
and workflow files are per-route context. This script makes those costs
visible and machine-comparable so context regressions can be reviewed like
quality regressions.

Token counts are estimates (chars / CHARS_PER_TOKEN); they are for comparing
revisions of this repository against each other, not for billing.

Usage:

    python scripts/measure_context_cost.py           # human-readable table
    python scripts/measure_context_cost.py --json    # machine-readable
    python scripts/measure_context_cost.py --top 10  # N largest skill bodies
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"
WORKFLOWS_DIR = REPO_ROOT / "workflows"

# Rough chars-per-token for mixed English/Markdown prose.
CHARS_PER_TOKEN = 3.8

ENTRY_STACK_FILES = (
    "skills/_gateway.md",
    "skills/00-discovery/intake/SKILL.md",
    "skills/00-discovery/intake/references/routing-signals-and-examples.md",
    "skills/00-discovery/intake/references/gotchas.md",
    "templates/intake-brief.md",
)


def est_tokens(chars: int) -> int:
    return round(chars / CHARS_PER_TOKEN)


def split_skill(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text
    return (yaml.safe_load(parts[1]) or {}), parts[2]


def lifecycle_skill_paths() -> list[Path]:
    return sorted(
        path for path in SKILLS_DIR.rglob("SKILL.md") if ".curated" not in path.parts
    )


def measure() -> dict:
    skills = []
    for path in lifecycle_skill_paths():
        frontmatter, body = split_skill(path)
        description = frontmatter.get("description", "") or ""
        references = sorted(path.parent.glob("references/*.md"))
        references_chars = sum(len(ref.read_text(encoding="utf-8")) for ref in references)
        skills.append(
            {
                "name": frontmatter.get("name", path.parent.name),
                "phase": path.parents[1].name,
                "description_chars": len(description),
                "body_chars": len(body),
                "body_tokens_est": est_tokens(len(body)),
                "references_chars": references_chars,
            }
        )

    always_on_description_chars = sum(item["description_chars"] for item in skills)

    entry_stack = []
    for rel in ENTRY_STACK_FILES:
        path = REPO_ROOT / rel
        chars = len(path.read_text(encoding="utf-8")) if path.exists() else 0
        entry_stack.append({"file": rel, "chars": chars, "tokens_est": est_tokens(chars)})
    entry_stack_chars = sum(item["chars"] for item in entry_stack)

    workflows = []
    for path in sorted(WORKFLOWS_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        chars = len(path.read_text(encoding="utf-8"))
        workflows.append(
            {"file": f"workflows/{path.name}", "chars": chars, "tokens_est": est_tokens(chars)}
        )

    phases: dict[str, dict[str, int]] = {}
    for item in skills:
        bucket = phases.setdefault(item["phase"], {"skills": 0, "body_chars": 0})
        bucket["skills"] += 1
        bucket["body_chars"] += item["body_chars"]

    return {
        "chars_per_token_estimate": CHARS_PER_TOKEN,
        "always_on": {
            "skill_count": len(skills),
            "description_chars": always_on_description_chars,
            "description_tokens_est": est_tokens(always_on_description_chars),
        },
        "entry_stack": {
            "files": entry_stack,
            "total_chars": entry_stack_chars,
            "total_tokens_est": est_tokens(entry_stack_chars),
        },
        "workflows": workflows,
        "phases": {
            phase: {**data, "body_tokens_est": est_tokens(data["body_chars"])}
            for phase, data in sorted(phases.items())
        },
        "skills": sorted(skills, key=lambda item: -item["body_chars"]),
    }


def print_human(report: dict, top: int) -> None:
    always_on = report["always_on"]
    print(
        f"Always-on descriptions: {always_on['skill_count']} skills, "
        f"{always_on['description_chars']} chars (~{always_on['description_tokens_est']} tokens)"
    )
    entry = report["entry_stack"]
    print(
        f"Entry stack (gateway + intake + refs + brief template): "
        f"{entry['total_chars']} chars (~{entry['total_tokens_est']} tokens)"
    )
    print("\nWorkflows:")
    for item in report["workflows"]:
        print(f"  {item['file']:40s} {item['chars']:7d} chars ~{item['tokens_est']:5d} tokens")
    print("\nPer-phase skill bodies:")
    for phase, data in report["phases"].items():
        print(
            f"  {phase:18s} {data['skills']:3d} skills {data['body_chars']:8d} chars "
            f"~{data['body_tokens_est']:6d} tokens"
        )
    print(f"\nTop {top} largest skill bodies:")
    for item in report["skills"][:top]:
        print(
            f"  {item['phase']}/{item['name']:32s} body {item['body_chars']:7d} chars "
            f"~{item['body_tokens_est']:5d} tokens, refs {item['references_chars']:6d} chars, "
            f"desc {item['description_chars']:4d} chars"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Measure static Prodcraft context cost.")
    parser.add_argument("--json", action="store_true", help="Emit the full report as JSON.")
    parser.add_argument("--top", type=int, default=8, help="How many largest skill bodies to list.")
    args = parser.parse_args()

    report = measure()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_human(report, args.top)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
