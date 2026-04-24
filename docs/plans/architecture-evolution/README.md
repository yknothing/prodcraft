# Architecture Evolution Planning Buffer

> Status: tracked planning buffer, not canonical architecture policy.

This directory holds temporary but reviewable planning artifacts for architecture
evolution work that must be preserved in the repository while it is active.

Use this directory when a document is more durable than a local `build/` handoff
log, but not authoritative enough for `docs/architecture/`, `docs/adr/`, a
schema, a validator, or a workflow contract.

## Why This Directory Exists

Architecture evolution work now has three durable sources:

- current canonical state in `docs/architecture/2026-04-18-prodcraft-architecture-state-bundle.md`
- historical synthesis in `docs/architecture/2026-04-17-prodcraft-architecture-evolution-basis.md`
- execution support in `docs/architecture/2026-04-17-architecture-review-action-register.md`

Those files should not become a scratchpad for active planning. They are the
inputs and governance references. This directory is the temporary workspace that
connects them to concrete implementation slices.

## Authority Order

If documents disagree, use this order:

1. Accepted schemas, validators, workflow contracts, artifact registries, and
   ADRs.
2. The canonical architecture state bundle.
3. The architecture action register and provisional design notes.
4. Active plans in this directory.
5. Local handoff logs under `build/`.

Plans in this directory may recommend a future contract. They do not make that
contract executable or authoritative.

## Placement Rules

Put a document here when all of these are true:

- it connects architecture state to a concrete next workstream
- it may need review, staging, or a commit while the work is active
- it is not yet an ADR, validator rule, schema, workflow contract, or canonical
  architecture state
- it has a clear graduation or retirement path

Do not put these documents here:

- accepted architecture decisions, which belong in `docs/adr/`
- canonical architecture state, which belongs in `docs/architecture/`
- generated evidence or local handoff logs, which belong under `build/`
- public distribution policy, which belongs in `docs/distribution/`
- executable rule sources, which belong under `rules/`, `schemas/`, scripts,
  tests, workflows, or manifest artifact flow

## Naming

Use dated, kebab-case names:

- `YYYY-MM-DD-<topic>-plan.md`
- `YYYY-MM-DD-<topic>-matrix.md`
- `YYYY-MM-DD-<topic>-review.md`

Each file should declare:

- status
- source documents
- scope and non-goals
- graduation path
- validation expectations

## Graduation

A plan should leave this directory only when it becomes one of these:

- an accepted ADR
- a canonical architecture-state update
- a validator, schema, registry, rule, workflow, or test contract
- a historical plan marked complete or superseded

If the work is abandoned, mark the plan as superseded or rejected instead of
silently deleting the context.
