# Input and Output Contract Notes

## Inputs

- **source-code**: Required. The concrete diff or changeset, including skill/document changes when they are the reviewed implementation, with enough surrounding context to trace consequences.
- **intake-brief**: Required approved scope and `quality_target_context` with runtime, exposure, target, exclusions, and evidence. For eligible compact micro work, consume target, exclusions, and check basis from `request_summary` and `routing_rationale`; do not request duplicate fields. If those facts cannot support risk assessment, reassess the route.
- **task-list**: Required task or acceptance context; a small approved slice can be embedded in an existing artifact instead of a separate planning document.
- **test-suite**: Required when changed executable behavior needs regression protection or project policy requires it. For skill prose or documents, consume the relevant contract, reference, export, or loader evidence and state any deferred behavioral evaluation.
- **api-contract**: Conditional on an affected public or inter-service contract. Inspect the authoritative specification or source boundary; report a relevant missing contract rather than inventing an unrelated API document.
- **architecture-doc**: Conditional on an affected architectural decision or compatibility seam. Reuse current accepted context; do not require a new architecture document for every diff.

In a lifecycle-aware system, review should not silently approve code that closes unresolved upstream questions by accident. Brownfield coexistence, unsupported release-1 flows, and contract boundaries are review concerns, not "later" concerns.

## Outputs

- **review-report**: Written feedback on the changeset with classified issues and any follow-up actions. Unless explicitly requested, the default output is a concise findings list rather than an approval verdict.

Default review-report shape when approval state is not requested:

1. prioritized findings only
2. brief assumptions or open questions only if they materially affect the review
3. no remediation appendix, no patch sketch, and no approval footer
