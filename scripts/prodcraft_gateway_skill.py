#!/usr/bin/env python3
"""Shared renderer for the public/global `prodcraft` gateway skill."""

from __future__ import annotations

from pathlib import Path

import yaml


PRODCRAFT_DESCRIPTION = (
    "Use when software-development work should follow the Prodcraft lifecycle-aware "
    "skills system, or when the user explicitly asks to use Prodcraft for routing, "
    "planning, implementation, quality gates, or workflow selection."
)


def render_prodcraft_skill(repo_root: Path, *, install_surface: str) -> str:
    if install_surface == "curated":
        intake_ref = "`intake`"
        problem_framing_ref = "`problem-framing`"
        gateway_ref = "`skills/_gateway.md` in the source repository"
        workflows_ref = "`workflows/` in the source repository"
    else:
        intake_ref = f"`{repo_root / 'skills' / '00-discovery' / 'intake' / 'SKILL.md'}`"
        problem_framing_ref = f"`{repo_root / 'skills' / '00-discovery' / 'problem-framing' / 'SKILL.md'}`"
        gateway_ref = f"`{repo_root / 'skills' / '_gateway.md'}`"
        workflows_ref = f"`{repo_root / 'workflows'}`"

    frontmatter = {
        "name": "prodcraft",
        "description": PRODCRAFT_DESCRIPTION,
        "metadata": {
            "internal": False,
            "distribution_surface": install_surface,
            "source_path": "skills/_gateway.md",
        },
    }

    body = f"""# Prodcraft

Use Prodcraft as the software-development entry system for this machine.

## Entry Rule

For new or unclear software-development work:

1. Start with {intake_ref}
2. If the route is clear but the problem direction is still fuzzy, continue with {problem_framing_ref}
3. Use {gateway_ref} to select downstream skills and {workflows_ref} to pick the workflow

## Priority

- Prefer Prodcraft over generic brainstorming for software-development tasks when the user explicitly asks for Prodcraft or lifecycle-aware routing.
- Keep obeying higher-priority system, developer, and repository instructions.
- For non-software-development tasks, use other relevant skills instead of forcing Prodcraft.

## Observability

When Prodcraft is chosen, preserve routing observability:

- why Prodcraft was invoked
- which entry skill was chosen
- what next skill or workflow was selected
- whether any global skill override experiment is active

## Distribution

- Install surface: `{install_surface}`
{f"- Canonical repo source: `{repo_root}`" if install_surface != "curated" else "- Canonical repo source: see the source repository"}
- Gateway contract: {gateway_ref}
"""
    return f"---\n{yaml.safe_dump(frontmatter, sort_keys=False, width=10000).strip()}\n---\n\n{body}"
