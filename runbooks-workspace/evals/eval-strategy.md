# Runbooks Evaluation Strategy

## Objective

Evaluate whether `runbooks` converts incident and observability context into a step-by-step operational procedure another responder can execute safely.

At review stage, use manual side-by-side evaluation rather than trigger scoring. This skill is expected to be used through routed operations workflows.

## Review Scope

Review the skill on:

1. `access-review-modernization-runbook`
   - brownfield modernization incident
   - fail-closed and fallback decisions matter
   - responders need a reusable procedure, not an ad hoc incident note

## Assertions

1. `provides executable ordered steps`
2. `preserves rollback and fail-closed safety`
3. `includes communication and escalation`
4. `includes verification and evidence capture`
5. `can be followed by another responder`

## Inputs

- `fixtures/access-review-modernization-incident-summary.md`
- `fixtures/access-review-modernization-observability-summary.md`

## Method

1. Produce a baseline runbook without the skill.
2. Produce a second output while explicitly using `runbooks`.
3. Compare against the assertion list.
4. Record findings in `runbook-review.md` and summarize status in `findings.md`.

## Exit Criteria for Review Stage

- At least one routed brownfield runbook scenario reviewed
- Clear manual evidence that the skill improves operational executability
- No claim of tested or production status until broader benchmark coverage exists
