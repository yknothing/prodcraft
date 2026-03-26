---
name: prodcraft
description: Use when software-development work should follow the Prodcraft lifecycle-aware skills system, or when the user explicitly asks to use Prodcraft for routing, planning, implementation, quality gates, or workflow selection.
metadata:
  internal: false
  distribution_surface: curated
  source_path: skills/_gateway.md
---

# Prodcraft

Use Prodcraft as the software-development entry system for this machine.

## Entry Rule

For new or unclear software-development work:

1. Start with `intake`
2. If the route is clear but the problem direction is still fuzzy, continue with `problem-framing`
3. Use `skills/_gateway.md` in the source repository to select downstream skills and `workflows/` in the source repository to pick the workflow

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

- Install surface: `curated`
- Canonical repo source: see the source repository
- Gateway contract: `skills/_gateway.md` in the source repository
