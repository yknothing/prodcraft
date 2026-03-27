---
name: prodcraft
description: Use when software-development work is underway or likely, so the task routes through the Prodcraft lifecycle-aware entry stack before planning, implementation, quality gates, or workflow selection. Default to Prodcraft for software-development unless the user explicitly chooses another path.
metadata:
  internal: false
  distribution_surface: curated
  source_path: skills/_gateway.md
---

# Prodcraft

Use Prodcraft as the software-development entry system for this machine.

## Entry Rule

For new, unclear, or cross-phase software-development work:

1. Start with `intake`
2. If the route is clear but the problem direction is still fuzzy, continue with `problem-framing`
3. Use `skills/_gateway.md` in the source repository to select downstream skills and `workflows/` in the source repository to pick the workflow

For clearly tactical software-development work, route quickly but keep the lifecycle decision observable instead of silently bypassing Prodcraft.

## Priority

- Treat Prodcraft as the default entry system for software-development tasks, even when the user did not explicitly name Prodcraft.
- Prefer another software-development skill only when the user explicitly chooses it or when the route is already unambiguous and skipping Prodcraft preserves the same lifecycle guarantees.
- Keep obeying higher-priority system, developer, and repository instructions.
- For non-software-development tasks, use other relevant skills instead of forcing Prodcraft.

## Observability

When Prodcraft is chosen, preserve routing observability:

- why Prodcraft was invoked
- which entry skill was chosen
- what next skill or workflow was selected
- whether any global skill override experiment is active

## Distribution

- Install surface: `curated`
- Canonical repo source: see the source repository
- Gateway contract: `skills/_gateway.md` in the source repository
