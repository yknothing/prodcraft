# Public Skill Lifecycle

Prodcraft separates lifecycle authoring from public installation.

## Contracts

- Lifecycle authoring source lives under `skills/00-discovery/...` through `skills/cross-cutting/...`.
- Public installation for `npx skills add/update` lives under `skills/.curated/`.
- Public skill names are governed by `schemas/distribution/public-skill-registry.json`.
- Public portability claims are governed by `schemas/distribution/public-skill-portability.json`.

## Internal Status vs Public Export

- `manifest.yml` status is the repository's internal maturity signal for the full authoring tree.
- Curated export is the public packaging signal for agent installers.
- A skill reaching `tested` does not automatically enter the curated/public surface.
- Public export still happens by explicit registry edit and curated re-export, not by automatically mirroring `manifest.yml`.
- Current policy is to keep the public beta surface aligned with the manifest `tested` / `secure` / `production` set unless the repository records a deliberate exception.
- Below-tested public skills remain rare continuity exceptions and should stay explicitly documented.

## Stability Rules

- A public skill keeps a stable canonical `name`.
- A rename must use `deprecated alias -> new canonical name -> old alias removal`.
- Removal requires at least one full release cycle of overlap or an explicit migration note.
- `stability` describes the packaging contract for `npx skills add/update` (`beta` or `stable`).
- `readiness` describes capability maturity for public users:
  - `core`: part of the public path we can actively stand behind today
  - `beta`: installable and reviewable, but not yet part of the hardened public promise
  - `experimental`: intentionally exposed for evaluation while still below the normal public maturity bar
- `manual_allowlist: true` is the escape hatch for curated export while a skill is still below the default maturity bar. It signals that a skill is part of the public beta surface even if its repository evidence does not yet support a full production status.

## Portability Rules

The public registry is an export allowlist. It answers which skills are packaged.

The portability registry is the public-claim safety contract. It answers what value survives outside the full repository control plane:

- `portable_as_is`: the exported skill does not depend on hidden repository protocol, validation, or evidence context.
- `portable_with_caveat`: the skill is useful as portable guidance, but its strongest governance claims require named repository context.
- `blocked`: the skill must not be exported in its current form.

Every exported public skill must have portability metadata. Exported skills classified as `blocked` fail curated-surface validation.
`skills/.curated/index.json` exposes only public-safe portability fields: `portability` and, when needed, `public_caveat_text`.
Hidden dependencies stay in the repository registry unless the team intentionally decides to publish them.

## Export Rules

- `skills/.curated/` is generated, not edited manually.
- `python3 scripts/validate_prodcraft.py --check curated-surface` re-exports the surface into a temporary directory and fails if the checked-in tree drifts from the exporter output.
- Exported skills must keep valid frontmatter and bundle any referenced `references/`, `scripts/`, or `assets/` paths.
- Generated gateway skills such as `prodcraft` must still point back to the canonical repository contract.
