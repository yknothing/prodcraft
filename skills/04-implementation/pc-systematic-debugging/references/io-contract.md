# Input and Output Contract Notes

## Inputs

- **source-code** -- Relevant code paths, configuration boundaries, and recent changes near the failure. Minimum required input.
- **test-suite** -- Existing failing tests or the closest executable safety net.
- **historical-defect-context** -- Optional. Prior incidents or regressions that may match the symptom.
- **fix-lineage-brief** -- Optional. Prior fixes, reverts, or workarounds that narrow the search space.

## Outputs

- **bug-fix-report** -- Fixed, mitigated, or diagnosis-limited outcome; cause or remaining hypotheses, observed revision/environment, evidence, verification limits, containment, and next action. A limited investigation can finish its report without claiming the defect is fixed. Review and verification consume only the supported claim.
- **course-correction-note** -- Only when evidence shows the problem belongs upstream in specification, architecture, or planning.
