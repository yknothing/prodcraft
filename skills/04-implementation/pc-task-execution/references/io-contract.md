# Input and Output Contract Notes

## Inputs

- **task-list** -- The approved implementation slice and done criteria.
- **dependency-graph** -- Optional but strongly preferred when the task depends on other slices or sequencing constraints.
- **architecture-doc** -- Needed when execution must preserve component boundaries or brownfield seams.
- **api-contract** -- Needed when the current batch could change externally visible behavior.

## Outputs

- **execution-batch-plan** -- The next bounded step sequence, with affected files or behaviors, verification points, and stop conditions; no fixed step duration is required.
- **execution-checkpoint** -- What the batch completed, how it was verified, what remains open, and the next recommended action.
- **execution-state** -- Optional strict-mode checkpoint with replayable lifecycle, phase, and artifact-binding history.
