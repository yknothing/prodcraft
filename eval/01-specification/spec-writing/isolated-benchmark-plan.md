# Spec Writing Isolated Benchmark Plan

## Goal

Prove that `spec-writing` turns reviewed requirements and domain language into a stronger release-boundary spec than a generic baseline.

## Planned Scenario

- `access-review-modernization-spec`

This scenario uses a brownfield access-review modernization slice where release-1 coexistence, evidence integrity, and unresolved sync behavior must stay explicit in the specification.

## Comparison

1. baseline generic specification prompt
2. the same prompt with explicit `spec-writing` skill invocation

## Assertions

1. `scope-and-non-goals-are-explicit`
   - the spec fixes what release 1 includes and excludes
2. `brownfield-constraints-are-preserved`
   - coexistence, historical-read boundaries, and rollout constraints remain visible
3. `open-questions-are-not-laundered`
   - unresolved sync or compatibility assumptions stay explicit
4. `stays-at-contract-layer`
   - the spec does not collapse into service classes or implementation tickets
5. `prepares-architecture-handoff`
   - the resulting spec can feed `api-design` or later architecture work directly

## Candidate Inputs

- `fixtures/access-review-modernization-requirements.md`
- `fixtures/access-review-modernization-domain-model.md`

## Exit Criteria for Tested Promotion

- one clean benchmark run exists for the bounded brownfield slice
- one routed handoff review shows downstream architecture or API work can consume the spec directly
