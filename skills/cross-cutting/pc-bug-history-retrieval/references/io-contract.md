# Input and Output Contract Notes

## Inputs

Bring the strongest current signal you have. Typical starting points:

- error message, exception class, or stack fragment
- incident symptom and affected user flow
- service, component, or subsystem name
- regression window or release identifier
- suspicious commit, rollback, or feature flag

If none of these exist, do not force historical retrieval. Route back to direct debugging or intake instead.

## Outputs

- **historical-defect-context** -- Ranked candidate matches from canonical systems, with evidence and confidence
- **fix-lineage-brief** -- Linked versions, commits, reverts, workarounds, and the most defensible next action
