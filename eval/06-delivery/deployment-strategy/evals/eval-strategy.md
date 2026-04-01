# Deployment Strategy QA Strategy

## Goal

Evaluate whether `deployment-strategy` chooses a rollout pattern, verification sequence, and rollback path that match the current release risk instead of defaulting to generic deployment advice.

## Why Start with Routed Handoff

`deployment-strategy` sits late in the delivery spine:

- `ci-cd` defines the delivery pipeline
- `delivery-completion` decides whether the release candidate is actually ready
- `deployment-strategy` decides how that candidate reaches production safely

The first QA question is therefore whether the skill:

- classifies release risk credibly
- selects a rollout pattern that matches blast radius and reversibility
- defines explicit stop/continue verification gates
- writes rollback-first instructions that downstream operations can actually use

## Initial Evaluation Mode

The first evaluation is a **manual pipeline-to-rollout handoff review** using the brownfield access-review modernization release slice.

This is review-stage evidence only. It does not replace future isolated automated benchmarks or live rollout rehearsals.

## Scenario

- `access-review-modernization-rollout`

Inputs:

- reviewed CI/CD pipeline summary
- build artifact and release-scope summary
- release plan or deployment window constraints when available

## Assertions

1. **classifies-release-risk**
   - output distinguishes low-risk, staged-risk, or high-risk release shape from the supplied context

2. **chooses-risk-matched-rollout**
   - rollout pattern matches blast radius and reversibility instead of defaulting to full rollout

3. **defines-verification-gates**
   - stop conditions, owners, and traffic-expansion checks are explicit

4. **writes-rollback-first**
   - rollback path is concrete and fast enough to act on during a bad release

5. **prepares-ops-handoff**
   - output is usable by `runbooks` and `incident-response`

## Pass Standard

Treat a run as strong review-stage evidence if it clearly outperforms a generic baseline on:

- risk-based rollout selection
- explicit verification gates
- rollback clarity
- operational usability

## Next QA Step

After this manual review:

- add an isolated benchmark for the same brownfield release slice
- add a lower-risk stateless release to verify the skill does not overfit staged rollouts
