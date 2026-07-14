# `pc-` Skill Identity Migration Design

## Status

Approved for implementation on 2026-07-14.

## Problem

Prodcraft skill names such as `intake`, `system-design`, and `tdd` are easy to
confuse with similarly named skills installed from other repositories. The
public and runtime identity needs a stable Prodcraft-owned marker.

The Agent Skills specification allows lowercase letters, numbers, and hyphens
in `name`; it does not allow `:`. Prodcraft will therefore use `pc-` as part of
the canonical skill name rather than relying on a host-specific namespace.

## Decision

Every implemented, planned, generated, and publicly exported Prodcraft skill
identity MUST start with `pc-`.

Examples:

| Before | After |
|---|---|
| `prodcraft` | `pc-prodcraft` |
| `intake` | `pc-intake` |
| `system-design` | `pc-system-design` |
| `verification-before-completion` | `pc-verification-before-completion` |

The prefix is canonical, not a display-only alias. Directory names, SKILL.md
frontmatter, manifest entries, workflow references, lifecycle matrices, QA
evidence paths, public registries, generated curated packages, and gateway
runtime locator metadata all use the same name.

## Compatibility Policy

This is an intentional breaking identity migration.

- Do not export duplicate unprefixed alias skills.
- Do not accept unprefixed names in canonical skill registries after migration.
- Existing flat installations may retain stale unprefixed directories; upgrade
  documentation must require their removal before reinstalling the curated
  surface.
- The global gateway installer automatically removes the legacy `prodcraft`
  directory only when its runtime locator proves that the same canonical
  repository owns it.
- If an existing legacy `prodcraft` directory cannot be proven safe to migrate,
  installation stops with a clear conflict instead of deleting or ignoring it.

Repository artifact identifiers such as `intake-brief`, schema versions such as
`prodcraft-runtime-locator.v1`, product names, script names, and historical
commit identifiers are not skill identities and are not renamed.

## Architecture Boundaries

### Canonical authoring surface

The lifecycle tree under `skills/` remains the source of truth. Each skill
directory and its frontmatter `name` must match and start with `pc-`.

### Governance surface

`manifest.yml` and repository-owned validators enforce the prefix. Planned
skill identifiers also use `pc-` so future skills cannot reintroduce an
unprefixed identity.

### Public distribution surface

`schemas/distribution/public-skill-registry.json` owns exported package names.
The exporter materializes only `pc-*` directories and frontmatter. The checked
in `skills/.curated/` tree is regenerated, never edited manually.

### Runtime gateway surface

The generated gateway is named `pc-prodcraft`. Its references to downstream
skills use `pc-*`, and its global locator records `skill_name: pc-prodcraft`.
The locator filename and schema version remain stable because they identify the
Prodcraft runtime protocol, not a skill package.

## Failure Semantics

Validation fails when:

- an implemented or planned skill name lacks `pc-`;
- a source or curated package directory does not match frontmatter `name`;
- a public registry or portability registry contains an unprefixed skill;
- generated curated output differs from the checked-in surface;
- a global gateway install encounters an unowned legacy `prodcraft` directory;
- a required relative resource or cross-skill link becomes dangling.

No migration check may silently rewrite an unproven external installation.

## Acceptance Criteria

1. All 46 authored skills have matching `pc-*` directories and frontmatter.
2. All planned skill identifiers in `manifest.yml` start with `pc-`.
3. All public registry, portability registry, and curated index entries start
   with `pc-`; no unprefixed curated skill directory remains.
4. Workflow, gateway, manifest, lifecycle matrix, example, and test references
   resolve to the renamed identities.
5. Eval directories that mirror authored skills use the same `pc-*` name.
6. The global installer writes `pc-prodcraft`, safely migrates a locator-owned
   legacy gateway, and rejects an unowned legacy conflict.
7. Repository validation, the full unit suite, curated export parity, dangling
   reference checks, frontmatter constraints, and runtime-load probes pass.
8. A repository scan finds no unprefixed skill identity in active governance or
   distribution contracts; allowed non-skill protocol and product terms remain
   unchanged.

## Rollback

Revert the migration commits as a unit, regenerate `skills/.curated/`, and run
the full validator. External installations that already adopted `pc-*` would
need a clean reinstall of the reverted unprefixed packages.
