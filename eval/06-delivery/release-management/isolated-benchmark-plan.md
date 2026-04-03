# Release Management Isolated Benchmark Plan

## Goal

Prove that `release-management` turns a verified release candidate into a concrete go/no-go coordination plan instead of generic shipping advice.

## Planned Scenarios

1. `access-review-modernization-release-plan`
   - brownfield release with unsupported-flow, coexistence, and rollback constraints
2. `team-invite-release-plan`
   - lower-risk release with normal stakeholder coordination but no legacy coexistence burden

## Comparison

1. baseline generic release coordination prompt
2. explicit `release-management` skill invocation

## Assertions

1. `scope-is-bounded`
   - the plan states what is in, what is out, and what findings remain accepted or blocking
2. `go-no-go-is-explicit`
   - release conditions are named instead of inferred from green checks
3. `ownership-and-comms-exist`
   - owners, approvers, escalation path, and communication moments are concrete
4. `missing-evidence-stays-visible`
   - absent security or performance evidence is recorded as a constraint, not silently cleared
5. `does-not-swallow-rollout-design`
   - rollout shape and rollback mechanics remain downstream deployment concerns

## Candidate Inputs

- `fixtures/access-review-modernization-delivery-decision-record.md`
- `fixtures/access-review-modernization-pipeline-summary.md`
- `fixtures/access-review-modernization-test-report.md`
- `fixtures/access-review-modernization-security-report.md`
- `fixtures/access-review-modernization-performance-report.md`

## Exit Criteria for Tested Promotion

- one clean benchmark run exists for the brownfield release slice
- one lower-coordination scenario exists to prove the skill is not modernization-only
- findings show the with-skill path creates clearer coordination discipline than baseline
