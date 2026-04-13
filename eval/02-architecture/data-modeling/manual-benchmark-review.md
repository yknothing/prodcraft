# Data Modeling Manual Benchmark Review

## Scope

This note reviews the checked-in manual branch-pair evidence for
`data-modeling`.

Evidence directory:
`eval/02-architecture/data-modeling/manual-run-2026-04-10-access-review`

The comparison uses one brownfield access-review modernization slice and keeps
the same architecture + domain-model + spec fixture trio across both branches:

1. `without_skill`
2. `with_skill`

## Scenario: Access Review Modernization Data Schema

### Baseline

The baseline data model is already strong. It is not a weak control.

It defines a real schema, retention notes, and coexistence boundaries, but it
still leaves more downstream drift available than the skill-applied branch:

- ownership is described table-by-table rather than starting from a clear
  cross-service ownership map
- policy snapshot and reassignment-variant constraints are weaker as first-class
  schema invariants
- audit-chain coexistence behavior is present, but less sharply turned into a
  brownfield integrity contract

### With-Skill

The with-skill branch is materially stronger on the dimensions that matter for
implementation safety:

- it starts with an explicit ownership map across services
- it separates workflow, compliance, and compatibility durability tiers
- it turns policy snapshotting and supported reassignment variants into clear
  schema-level invariants
- it documents `LEGACY_ORIGIN` as an intentional audit-chain boundary for
  backfilled legacy history
- it gives a cleaner additive-change / prohibited-change model for future
  implementation work

## Judgment

This is manual evidence, not a runner-backed isolated benchmark, and it should
stay labeled that way.

Even so, the comparison is strong enough for a narrow `tested` decision because
the baseline is already competent and the with-skill branch still produces a
meaningful improvement in ownership clarity, change safety, and brownfield
integrity rules.

## Status Recommendation

- Recommended status: `tested`
