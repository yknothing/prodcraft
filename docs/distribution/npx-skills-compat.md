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

This separation lets Prodcraft preserve rich lifecycle structure internally without forcing that structure onto installers. Inclusion in the curated tree means a skill's installation boundary is stable, not necessarily that the skill itself has reached full public maturity.

Common confusion:

- the repository may contain many more authored skills than the installer shows
- `manifest.yml` may mark many more skills as `tested` than the installer shows
- `npx skills` should count only the generated curated surface, not the full `skills/` tree and not every manifest entry

Promotion to `tested` is a repository maturity decision. Promotion into `skills/.curated/` is a separate public packaging decision.

Current publication rule:

- the registry should normally include every manifest skill at `tested`, `secure`, or `production`
- lower-maturity public entries must remain explicit exceptions with a documented reason
- `npx skills` therefore tracks the checked-in public beta surface, not the raw authoring count and not the unpublished review backlog

Public registry entries expose two different release signals:

- `stability`: install/update contract stability for the packaged skill
- `readiness`: current public capability maturity (`core`, `beta`, or `experimental`)

Portability is tracked separately in `schemas/distribution/public-skill-portability.json`.
That companion registry prevents the export allowlist from becoming a mixed decision table.
It classifies each public skill as `portable_as_is`, `portable_with_caveat`, or `blocked`, and records hidden dependencies, required context, and public caveat text.
The generated curated index publishes only `portability` and public caveats; internal hidden-dependency notes stay in the repository contract.

## Export Contract

- `.curated/<skill>/SKILL.md` must be directly installable
- packaged `references/`, `scripts/`, and `assets/` must resolve locally
- public skill names must remain stable across `update`
- deprecations require a migration path and at least one full release cycle of overlap
- exported skills must not be classified as `blocked` in the portability registry

## Tooling

- Source registry: `schemas/distribution/public-skill-registry.json`
- Portability registry: `schemas/distribution/public-skill-portability.json`
- Exporter: `scripts/export_curated_skills.py`
- Repo index: `skills/.curated/index.json`
