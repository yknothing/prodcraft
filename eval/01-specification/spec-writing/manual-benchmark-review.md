# Spec Writing Manual Benchmark Review

## Scope

This note reviews the checked-in manual branch-pair evidence for
`spec-writing`.

Evidence directory:
`eval/01-specification/spec-writing/manual-run-2026-04-10-access-review`

The comparison uses one brownfield access-review modernization slice and keeps
the same requirement + domain-model fixture pair across both branches:

1. `without_skill`
2. `with_skill`

## Scenario: Access Review Modernization Release 1

### Baseline

The baseline spec draft is workable, but it fails on the main boundary the
skill exists to protect:

- it frames release 1 as a legacy replacement rather than a coexistence slice
- it pulls migration-only concerns such as historical import and same-day sync
  into in-scope work
- it drifts into implementation shape by prescribing specific services and a
  sync worker
- it launders unresolved reassignment behavior into assumed support

### With-Skill

The with-skill branch is materially stronger:

- release-1 scope and non-goals are explicit
- public contract boundary stays separate from migration and cutover work
- coexistence and historical-read constraints remain visible
- unsupported flows stay explicit instead of silently becoming supported
- open questions remain open, especially around sync semantics and tenant
  variants

## Judgment

This is manual evidence, not a runner-backed isolated benchmark, and it should
stay labeled that way.

Even so, the quality lift is direct and meaningful on the skill's central job:

- it keeps the spec at the contract layer
- it protects downstream architecture and API work from migration leakage
- it preserves the real release boundary rather than replacing it with hopeful
  implementation assumptions

## Status Recommendation

- Recommended status: `tested`
