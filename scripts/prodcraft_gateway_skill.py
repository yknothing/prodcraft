#!/usr/bin/env python3
"""Shared renderer for the public/global `prodcraft` gateway skill."""

from __future__ import annotations

from pathlib import Path

import yaml


PRODCRAFT_DESCRIPTION = (
    "Use when software-development work is underway or likely, so the task routes "
    "through the Prodcraft lifecycle-aware entry stack before planning, implementation, "
    "quality gates, or workflow selection. Default to Prodcraft for software-development "
    "unless the user explicitly chooses another path."
)


def render_prodcraft_skill(
    repo_root: Path,
    *,
    install_surface: str,
    public_stability: str = "beta",
    public_readiness: str = "core",
) -> str:
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
            "public_stability": public_stability,
            "public_readiness": public_readiness,
        },
    }

    body = f"""# Prodcraft

Use Prodcraft as the software-development entry system for this machine.

## Entry Rule

For new, unclear, or cross-phase software-development work:

1. Start with {intake_ref}
2. If the route is clear but the problem direction is still fuzzy, continue with {problem_framing_ref}
3. Use {gateway_ref} to select downstream skills and {workflows_ref} to pick the workflow

For clearly tactical software-development work, route quickly but keep the lifecycle decision observable instead of silently bypassing Prodcraft.

## Priority

- Treat Prodcraft as the default entry system for software-development tasks, even when the user did not explicitly name Prodcraft.
- Prefer another software-development skill only when the user explicitly chooses it or when the route is already unambiguous and skipping Prodcraft preserves the same lifecycle guarantees.
- Treat most deeper lifecycle skills as **routed** by intake, workflow choice, or explicit handoff rather than as metadata-first auto-discovery targets.
- Keep obeying higher-priority system, developer, and repository instructions.
- For non-software-development tasks, use other relevant skills instead of forcing Prodcraft.

## Routed Invocation

The curated install surface is a stable packaging contract, not a promise that every included skill should auto-trigger from metadata alone in a crowded local environment.

- entry and control-plane skills may need strong discoverability
- deeper lifecycle skills usually add value after route selection, not before it
- prefer routed handoff over forcing generic auto-discovery for architecture, planning, quality, and operations skills

## Observability

When Prodcraft is chosen, preserve routing observability:

- why Prodcraft was invoked
- which entry skill was chosen
- what next skill or workflow was selected
- whether any global skill override experiment is active

## Distribution

- Install surface: `{install_surface}`
- Packaging stability: `{public_stability}`
- Capability readiness: `{public_readiness}`
{f"- Canonical repo source: `{repo_root}`" if install_surface != "curated" else "- Canonical repo source: see the source repository"}
- Gateway contract: {gateway_ref}
"""
    return f"---\n{yaml.safe_dump(frontmatter, sort_keys=False, width=10000).strip()}\n---\n\n{body}"
