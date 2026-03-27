# Public Skill Lifecycle

Prodcraft separates lifecycle authoring from public installation.

## Contracts

- Lifecycle authoring source lives under `skills/00-discovery/...` through `skills/cross-cutting/...`.
- Public installation for `npx skills add/update` lives under `skills/.curated/`.
- Public skill names are governed by `schemas/distribution/public-skill-registry.json`.

## Stability Rules

- A public skill keeps a stable canonical `name`.
- A rename must use `deprecated alias -> new canonical name -> old alias removal`.
- Removal requires at least one full release cycle of overlap or an explicit migration note.
- `manual_allowlist: true` is the escape hatch for curated export while a skill is still below the default maturity bar.

## Export Rules

- `skills/.curated/` is generated, not edited manually.
- `python3 scripts/validate_prodcraft.py --check curated-surface` re-exports the surface into a temporary directory and fails if the checked-in tree drifts from the exporter output.
- Exported skills must keep valid frontmatter and bundle any referenced `references/`, `scripts/`, or `assets/` paths.
- Generated gateway skills such as `prodcraft` must still point back to the canonical repository contract.
