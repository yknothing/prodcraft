# Input and Output Contract Notes

## Inputs

- **source-code**: The diff or changeset under review, with sufficient context to understand the change.
- **test-suite**: Accompanying tests that validate the change. Verify they exist and are meaningful.
- **task-list**: The reviewed implementation slice or task context that defines what was actually supposed to land now.
- **api-contract**: The contract or externally visible behavior that the changeset must preserve or implement.
- **architecture-doc**: System design context to verify the change aligns with architectural decisions.
- **intake-brief**: Must include `quality_target_context` with `runtime_context`, `exposure_profile`, `production_target`, `non_targets`, and `evidence_refs`.

In a lifecycle-aware system, review should not silently approve code that closes unresolved upstream questions by accident. Brownfield coexistence, unsupported release-1 flows, and contract boundaries are review concerns, not "later" concerns.

## Outputs

- **review-report**: Written feedback on the changeset with classified issues and any follow-up actions. Unless explicitly requested, the default output is a concise findings list rather than an approval verdict.

Default review-report shape when approval state is not requested:

1. prioritized findings only
2. brief assumptions or open questions only if they materially affect the review
3. no remediation appendix, no patch sketch, and no approval footer
