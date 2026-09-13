# Input and Output Contract Notes

## Inputs

- **source-code** -- Relevant code paths, configuration boundaries, and recent changes near the failure. Required before claiming or implementing a source-code correction, not before beginning a runtime or environment diagnosis. A failure report, logs, artifact identity, or inspectable configuration can start a bounded investigation. State missing access and its effect on confidence; do not route to feature development merely to manufacture this input.
- **test-suite** -- Reuse existing failing tests or the closest executable safety net when available. It is not a prerequisite for starting diagnosis. A fixed claim needs a matching negative/positive check at the affected boundary; a repeatable runtime or manual check can supply that proof when unit tests do not model the failure. Missing proof limits the outcome to diagnosis or mitigation.
- **historical-defect-context** -- Optional. Prior incidents or regressions that may match the symptom.
- **fix-lineage-brief** -- Optional. Prior fixes, reverts, or workarounds that narrow the search space.

## Outputs

- **bug-fix-report** -- Fixed, mitigated, or diagnosis-limited outcome; broken contract, cause or remaining hypotheses, observed revision/environment, evidence, verification limits, containment, and next action. Link meaningful observations to their commands/procedures and results. For continued investigation retain predictions, useful rejected explanations, the next discriminator, its owner and safe resumption conditions in this report or an existing investigation record; do not create a second mandatory journal. A limited investigation can finish its report without claiming the defect is fixed. Review and verification consume only the supported claim.
- **course-correction-note** -- Only when evidence shows the problem belongs upstream in specification, architecture, or planning.
