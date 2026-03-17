# Runbook Independent Execution Drill

## Purpose

Perform a stricter single-author replay of the runbooks as if the responder had only the scenario fixtures and the runbook text, not the author's hidden context.

This is weaker than an external execution drill, but stronger than author impression alone.

## Scenarios Replayed

1. `access-review-modernization-runbook`
2. `team-invite-email-backlog-runbook`

## Findings

### Access Review Modernization

- The runbook was structurally executable.
- Two points still depended on implicit context:
  - "if route-level guard is available" needed a clearer indication of where that availability is determined
  - "according to operational policy" assumed the responder already knew the retry-damping policy reference

### Team Invite Email Backlog

- The runbook was structurally executable.
- Two points still depended on implicit context:
  - "communication threshold" needed a more explicit source or value
  - "expected window" for recovery needed a named policy or dashboard threshold

## Result

- No fatal structural gaps were found.
- The runbooks are close to executable by another responder.
- They still need threshold and policy references to avoid tribal-knowledge leakage.

## Action Taken

The `runbooks` skill was updated so future runbooks must:

- name the source of any threshold, policy, or guard decision
- avoid magic references like "expected window" without a concrete source

## Status

This drill improves confidence, but it does **not** replace a real external execution drill.
