# Input and Output Contract Notes

## Inputs

- **requirements-doc** -- the accepted requirements or story slice, including its source/version and relevant priority; reuse a current slice instead of recreating the full document
- **spec-doc** -- existing detailed behavior when the accepted route requires it; optional for a sufficiently defined agile story or bounded task

Return missing behavior to its requirements owner. Do not invent scope, approvals, or a specification-writing step just to fill an input slot.

## Outputs

- **acceptance-criteria-set** -- criteria linked to the accepted requirements, with observable outcomes, relevant edge/error cases, and review evidence; downstream tests consume this version and reopen only criteria affected by changed inputs
