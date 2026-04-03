# Release Management QA Strategy

## Goal

Evaluate whether `release-management` turns a technically viable release candidate into an explicit go/no-go coordination plan without collapsing into `delivery-completion` or `deployment-strategy`.

## Why This Skill Matters

Prodcraft already separates:

- `delivery-completion` -- whether verified work should continue toward shipping
- `deployment-strategy` -- how a release should roll out safely

The missing layer is the release coordination decision in between:

- what is in scope
- what is still conditional
- who owns the window and communications
- which evidence gaps block or constrain the release

## Initial Evaluation Mode

The first evaluation is a **manual routed handoff review** using a brownfield release candidate with explicit quality and rollout constraints.

This is review-stage evidence only. It does not replace future isolated automated benchmarks or live release drills.

## Scenario

- `access-review-modernization-release-plan`

Inputs:

- delivery decision record
- reviewed pipeline summary
- test report
- security report
- performance report

## Assertions

1. **scope-and-exclusions-explicit**
   - the release plan states what is shipping now and what remains out of scope

2. **go-no-go-rationale-explicit**
   - the release decision and any release conditions are named plainly instead of being implied by green pipeline status

3. **owners-and-comms-explicit**
   - owners, approvers, escalation points, and stakeholder communication moments are visible

4. **evidence-gaps-not-silently-cleared**
   - missing or conditional evidence remains visible instead of being upgraded to silent approval

5. **boundary-with-deployment-strategy-preserved**
   - the output stops at release coordination and does not swallow rollout-shape decisions

## Pass Standard

Treat the skill as strong review-stage evidence if the handoff artifact shows a clear delivery boundary between completion, release coordination, and rollout design.

## Next QA Step

- add an isolated benchmark comparing generic release advice against the same constrained release slice
- add a non-brownfield release scenario with lower coordination cost
