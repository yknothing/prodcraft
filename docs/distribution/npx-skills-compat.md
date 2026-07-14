# `npx skills` Compatibility

Prodcraft supports the de facto Agent Skills installation flow:

- `npx skills add <repo-url>/skills/.curated`
- `npx skills add <repo-url>/skills/.curated --skill <name>`
- `npx skills update`

## Public Install Surface

- Canonical public install surface: `skills/.curated/`
- Canonical authoring source: lifecycle directories under `skills/00-discovery/` through `skills/cross-cutting/`
- Repository-root discovery is not the public contract unless the installer is
  known to filter by the public registry. The curated directory is the install
  source that matches the checked-in public index.

## Why `.curated` Exists

The lifecycle source tree is optimized for authoring, review, and repository-local validation.
The `.curated` tree is optimized for stable installation and upgrade contracts across agent runtimes.

This separation lets Prodcraft preserve rich lifecycle structure internally without forcing that structure onto installers. Inclusion in the curated tree means a skill's installation boundary is stable, not necessarily that the skill itself has reached full public maturity.

Common confusion:

- the repository may contain many more authored skills than the installer shows
- `manifest.yml` may mark many more skills as `tested` than the installer shows
- `npx skills` should count only the generated curated surface, not the full `skills/` tree and not every manifest entry
- a singleton `pc-prodcraft/SKILL.md` gateway package is expected; do not treat that directory as the complete downstream skill inventory

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
- public skill names must remain stable across `update`, except for an explicitly documented beta-wide canonical migration
- after this beta migration, deprecations require a migration path and at least one full release cycle of overlap
- exported skills must not be classified as `blocked` in the portability registry

## Breaking Upgrade From Unprefixed Beta Packages

Every user-visible Prodcraft skill ID now uses the canonical `pc-` prefix. This
is a one-time beta-wide breaking migration; unprefixed aliases are not exported.
`npx skills update` may install the new `pc-*` packages without proving that an
old flat package with the same basename came from Prodcraft, so an upgrade must
also account for stale unprefixed packages.

Use the installer's provenance or lockfile to identify and uninstall only the
old packages that it can prove came from this repository, then install the
curated surface again. Do not bulk-delete directories such as `intake`,
`code-review`, or `tdd` by basename: those names may belong to another skill
repository, which is the collision this migration is designed to eliminate.

If the installer cannot prove package provenance, use one of these safe paths:

1. Back up the existing skill root and install the curated surface into a new,
   empty, dedicated root.
2. Inspect each old package and its installer metadata individually, removing
   it only after confirming that it is the former Prodcraft package.

After reinstalling, verify that the active Prodcraft packages are `pc-*` and
that no provenance-confirmed unprefixed Prodcraft package remains. Only the
legacy singleton `prodcraft` gateway has repository-owned locator metadata that
the included installer can migrate automatically.

## Gateway Package Resolution

The public `pc-prodcraft` package is an entry gateway. It may be installed by
itself, and the matching global install under `~/.agents/skills/pc-prodcraft` may
also contain only `SKILL.md` plus a runtime locator. That shape is valid.

Agent runtimes should resolve downstream context in this order:

1. For a global install, use `prodcraft-runtime.json` beside the gateway skill.
   Trust the current workspace as the source repository only when it is the
   locator's `canonical_repo_root` or inside that root and it has the expected
   Prodcraft identity files.
2. Without a trusted locator, use a source repository only when the user or host
   runtime explicitly identifies it as the Prodcraft repository.
3. For a public install, use sibling packages such as `pc-intake`, `pc-code-review`,
   `pc-testing-strategy`, or `pc-security-audit` only when they are actually present.
4. If none of those contexts resolve, stay in entry-level guidance and ask for
   the missing repository or package context.

Do not claim repository workflow gates, validators, evidence records, or
downstream QA skills ran from a gateway-only package.

### Legacy global gateway migration

`scripts/install_prodcraft_global_skill.py install` may replace the former
`~/.agents/skills/prodcraft` gateway with `~/.agents/skills/pc-prodcraft` only
when the legacy directory has exactly the managed gateway files and its runtime
locator proves ownership by this canonical repository. Unmanaged files,
symlinks, malformed locators, path mismatches, or another repository owner fail
closed before either directory is changed. The legacy name is not retained as
a runtime alias.

## Tooling

- Source registry: `schemas/distribution/public-skill-registry.json`
- Portability registry: `schemas/distribution/public-skill-portability.json`
- Exporter: `scripts/export_curated_skills.py`
- Repo index: `skills/.curated/index.json`
