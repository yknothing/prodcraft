# Input and Output Contract Notes

## Inputs

- **intake-brief**: The original intent, target context, non-targets, and evidence expectations.
- **task-list**: The approved implementation slice and any priority ordering.
- **acceptance-criteria-set**: The explicit pass/fail contract, including negative criteria.
- **source-code**: The diff or implementation surface.
- **test-suite**: Tests, fixtures, snapshots, smoke logs, and validation output.

Also read requirements docs, specs, architecture notes, runbooks, or quality snapshots when they are referenced by the task.

## Outputs

Produce a `review-report` with:

- intent contract summary
- coverage matrix
- implementation status by priority
- claim/evidence mismatches
- unresolved scope or consistency questions
- recommended next skill or repair path
