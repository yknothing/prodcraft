# CI/CD QA Strategy

## Goal

Evaluate whether `ci-cd` translates reviewed test and release constraints into a delivery pipeline that protects release boundaries instead of just automating a generic deploy flow.

## Why Start with Routed Handoff

`ci-cd` is the first delivery skill on the core spine.

The first QA question is whether the skill:

- reflects upstream testing and review findings in pipeline gates
- preserves rollback and brownfield release-boundary requirements
- sequences validation and deployment stages coherently
- prepares handoff for rollout and release coordination

## Initial Evaluation Mode

The first evaluation is a **manual release-slice pipeline review** using the brownfield access-review modernization scenario.

This is review-stage evidence only. It does not replace future isolated automated benchmarks or live pipeline tests.

## Scenario

- `access-review-modernization-pipeline`

Inputs:

- task slice
- testing strategy summary
- review findings summary

## Assertions

1. **maps-gates-to-risk**
   - pipeline stages reflect the reviewed test strategy and known blockers

2. **preserves-brownfield-safety**
   - rollback, coexistence, and unsupported-flow checks remain explicit delivery gates

3. **stays-delivery-focused**
   - output remains a pipeline/release automation plan, not a new testing or architecture document

4. **fails-closed**
   - unsafe releases are blocked before deployment rather than left to production discovery

5. **prepares-downstream-handoff**
   - output is usable by deployment-strategy and release-management follow-on work

## Pass Standard

Treat a run as strong review-stage evidence if it clearly outperforms a generic baseline on:

- risk-aware gating
- rollback/coexistence protection
- fail-closed behavior
- delivery readiness

## Next QA Step

After this manual review:

- add an isolated benchmark for the same brownfield slice
- add a non-brownfield service or feature delivery scenario to verify the skill does not overfit to migration-heavy releases
