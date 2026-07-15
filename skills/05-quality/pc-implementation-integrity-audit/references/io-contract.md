# Input and Output Contract Notes

## Inputs

- **intake-brief**: Target context, evidence requirements, non-targets, and safety constraints.
- **source-code**: The implementation diff and related runtime boundaries.
- **test-suite**: Unit, integration, E2E, fixture, smoke, and benchmark evidence.
- **task-list**: The exact work items and priority sequence.

Also inspect logs, debug records, runbooks, mocks, fixture data, generated artifacts, and quality reports when available.

## Outputs

Produce a `review-report` with:

- trust-boundary map
- mock/fixture inventory
- low-level defect findings
- deceptive-success or improper-mock findings
- test-integrity gaps
- prioritized repairs and regression guards
