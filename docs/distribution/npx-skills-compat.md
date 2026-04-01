# `npx skills` Compatibility

Prodcraft supports the de facto Agent Skills installation flow:

- `npx skills add <repo>`
- `npx skills add <repo> --skill <name>`
- `npx skills update`

## Public Install Surface

- Canonical public install surface: `skills/.curated/`
- Canonical authoring source: lifecycle directories under `skills/00-discovery/` through `skills/cross-cutting/`

## Why `.curated` Exists

The lifecycle source tree is optimized for authoring, review, and repository-local validation.
The `.curated` tree is optimized for stable installation and upgrade contracts across agent runtimes.

This separation lets Prodcraft preserve rich lifecycle structure internally without forcing that structure onto installers. **Note that the curated surface currently represents a beta capability set.** Inclusion in the curated tree means a skill's installation boundary is stable, not necessarily that the skill itself has reached production maturity.

## Export Contract

- `.curated/<skill>/SKILL.md` must be directly installable
- packaged `references/`, `scripts/`, and `assets/` must resolve locally
- public skill names must remain stable across `update`
- deprecations require a migration path and at least one full release cycle of overlap

## Tooling

- Source registry: `schemas/distribution/public-skill-registry.json`
- Exporter: `scripts/export_curated_skills.py`
- Repo index: `skills/.curated/index.json`
