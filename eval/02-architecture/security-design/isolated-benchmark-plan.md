# Security Design Isolated Benchmark Plan

## Goal

Prove that `security-design` turns reviewed architecture and API context into a stronger threat model than a generic baseline.

## Planned Scenario

- `access-review-modernization-security-design`

This scenario uses a brownfield access-review modernization slice where tenant isolation, evidence integrity, unsupported-flow handling, and legacy coexistence all create security-relevant trust boundaries.

## Comparison

1. baseline generic threat-model prompt
2. the same prompt with explicit `security-design` skill invocation

## Assertions

1. `identifies-assets-and-trust-boundaries`
   - sensitive assets and trust transitions are explicit
2. `enumerates-real-abuse-paths`
   - tenant isolation, replay, logging leakage, and coexistence weaknesses are considered
3. `assigns-concrete-controls`
   - authn/authz, validation, logging, and fail-closed controls are mapped to boundaries
4. `keeps-brownfield-risk-visible`
   - legacy and compatibility exposure remain explicit
5. `prepares-audit-handoff`
   - the resulting threat model can feed `security-audit`

## Candidate Inputs

- `fixtures/access-review-modernization-architecture.md`
- `fixtures/access-review-modernization-api-contract.md`

## Exit Criteria for Tested Promotion

- one clean benchmark run exists for the bounded brownfield slice
- one routed handoff review shows downstream security audit can consume the threat model directly
