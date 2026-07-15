# Input and Output Contract Notes

## Inputs

- **task-list** -- The approved implementation slice and done criteria.
- **dependency-graph** -- Optional but strongly preferred when the task depends on other slices or sequencing constraints.
- **architecture-doc** -- Needed when execution must preserve component boundaries or brownfield seams.
- **api-contract** -- Needed when the current batch could change externally visible behavior.

## Outputs

- **execution-batch-plan** -- The next 2-5 minute step sequence, with files, commands, verification points, and stop conditions.
- **execution-checkpoint** -- What the batch completed, how it was verified, what remains open, and the next recommended action.
- **execution-state** -- Optional strict-mode checkpoint with replayable lifecycle, phase, and artifact-binding history.
