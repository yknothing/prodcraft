# Input and Output Contract Notes

## Inputs

- **review-report** -- Required findings or comments with their reviewed revision and scope. It may come from code review, alignment review, integrity audit, or the current human review; do not invoke another reviewer only to satisfy a prerequisite label.
- **source-code** -- Required when judging or applying implementation feedback. Review the current revision and affected boundaries, not only the quoted diff.
- **test-suite** -- Conditional on the accepted change. Use relevant behavioral checks for code and appropriate structural/manual checks for other artifacts; clarification-only work does not require fabricated test runs.

## Outputs

- **review-response-record** -- Reuse a record with stable finding identifiers. Each item needs disposition, evidence/revision, affected dependency group, verification or explicit gaps, and the next reviewer/decision. `pc-code-review` consumes it for re-review; `pc-verification-before-completion` uses it to identify unresolved claims. A disputed blocker is not resolved by the author's disagreement.

If one comment questions an API decision and another identifies an independent typo, the API group waits for that decision while an already-authorized typo correction can proceed. If both touch the same behavior, clarify their interaction first.
