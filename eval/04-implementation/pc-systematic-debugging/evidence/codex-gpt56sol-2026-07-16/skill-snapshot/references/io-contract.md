# Input and Output Contract Notes

## Inputs

- **source-code** -- Relevant code paths, configuration boundaries, and recent changes near the failure. Minimum required input.
- **test-suite** -- Existing failing tests or the closest executable safety net.
- **historical-defect-context** -- Optional. Prior incidents or regressions that may match the symptom.
- **fix-lineage-brief** -- Optional. Prior fixes, reverts, or workarounds that narrow the search space.

## Outputs

- **bug-fix-report** -- Root cause, supporting evidence, fix boundary, regression protection, and follow-up notes.
- **course-correction-note** -- Only when evidence shows the problem belongs upstream in specification, architecture, or planning.
