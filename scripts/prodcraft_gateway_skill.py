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
        repo_source_line = "- Canonical repo source: see the source repository"
        locator_note = (
            "- No machine-specific locator is bundled with the curated package; if the source repository is not "
            "available, rely only on sibling public skill packages that are actually installed."
        )
    else:
        intake_ref = "`intake` from the canonical repository recorded in `prodcraft-runtime.json`"
        problem_framing_ref = "`problem-framing` from the canonical repository recorded in `prodcraft-runtime.json`"
        gateway_ref = "the `gateway_path` recorded in `prodcraft-runtime.json`"
        workflows_ref = "the `workflow_root` recorded in `prodcraft-runtime.json`"
        repo_source_line = "- Canonical repo source: recorded in `prodcraft-runtime.json` for this global install"
        locator_note = (
            "- Machine locator: read `prodcraft-runtime.json` beside this `SKILL.md` when available; it records "
            "the canonical source repository, gateway file, and source skill root for this global install."
        )

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

## Runtime Resolution

A `prodcraft` directory that contains only this `SKILL.md` is a valid gateway install. It is not evidence that downstream Prodcraft skills are missing. Do not search for downstream skills inside the `prodcraft` directory.

Resolve the actual operating context in this order:

1. For a global install, read `prodcraft-runtime.json` beside this file when it exists, then use its `gateway_path`, `source_skills_root`, `workflow_root`, and `canonical_repo_root` fields.
2. In global mode, trust the current workspace as the source repository only when it is the locator's `canonical_repo_root` or inside that root, and it also contains Prodcraft identity files such as `CLAUDE.md`, `manifest.yml`, `skills/_gateway.md`, `schemas/distribution/public-skill-registry.json`, and `scripts/validate_prodcraft.py`.
3. Without a trusted global locator, treat a source repository as authoritative only when the user or higher-priority runtime context explicitly identifies it as the Prodcraft source repository and the same identity files are present.
4. Look for sibling skill packages beside `prodcraft`, such as `../intake/SKILL.md`, `../code-review/SKILL.md`, `../testing-strategy/SKILL.md`, and `../security-audit/SKILL.md`. Sibling packages provide public skill guidance; they do not provide source-repository authority.
5. If neither a trusted source repository nor sibling public skill packages can be resolved, treat the runtime as a partial entry install.

Use explicit file reads for these checks. Do not recursively search arbitrary parent directories or run shell commands to discover a substitute repository.

In partial-entry mode, keep the boundary explicit:

- say: `This is partial-entry guidance, not a completed Prodcraft workflow or evidence gate.`
- produce only an entry-level route recommendation and name the missing runtime context
- ask for the source repository path or installation of the needed public skill package before deeper execution
- do not claim that downstream skills such as `code-review`, `testing-strategy`, or `security-audit` ran
- do not manually simulate repository validators, workflow approval, QA evidence, or completion gates as if Prodcraft executed them

## Observability

When Prodcraft is chosen, preserve routing observability:

- why Prodcraft was invoked
- which entry skill was chosen
- what next skill or workflow was selected
- which source repository, runtime locator, or sibling skill package was used
- whether any global skill override experiment is active

## Distribution

- Install surface: `{install_surface}`
- Packaging stability: `{public_stability}`
- Capability readiness: `{public_readiness}`
{repo_source_line}
- Gateway contract: {gateway_ref}
{locator_note}
"""
    return f"---\n{yaml.safe_dump(frontmatter, sort_keys=False, width=10000).strip()}\n---\n\n{body}"
