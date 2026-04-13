# Data Modeling Isolated Benchmark Plan

## Goal

Prove that `data-modeling` turns reviewed architecture, domain language, and spec constraints into a stronger persistence design than a generic baseline.

## Planned Scenario

- `access-review-modernization-data-model`

This scenario uses a brownfield access-review modernization slice where evidence retention, compatibility boundaries, and tenant-policy ownership all matter.

## Comparison

1. baseline generic persistence-design prompt
2. the same prompt with explicit `data-modeling` skill invocation

## Assertions

1. `authoritative-ownership-is-explicit`
   - canonical records, derived views, and compatibility-only references are distinguished
2. `lifecycle-rules-are-documented`
   - retention, archival, mutation, and uniqueness rules are visible
3. `brownfield-change-safety-is-preserved`
   - coexistence and historical-read boundaries remain explicit
4. `stays-at-schema-and-ownership-layer`
   - the output does not collapse into implementation or API design
5. `prepares-implementation-handoff`
   - the resulting schema guidance can feed `feature-development`

## Candidate Inputs

- `fixtures/access-review-modernization-architecture.md`
- `fixtures/access-review-modernization-domain-model.md`
- `fixtures/access-review-modernization-spec.md`

## Exit Criteria for Tested Promotion

- one clean benchmark run exists for the bounded brownfield slice
- one routed handoff review shows downstream implementation can consume the schema and ownership guidance directly
