# Input and Output Contract Notes

## Inputs

- **Accepted slice** -- Required outcome, acceptance conditions, and scope. Consume `task-list` or the existing approved task section; do not create a separate plan merely for its filename.
- **test-suite** -- Required where executable behavior is changed. Check which behavior it protects and whether the evidence matches the current revision. Reuse accepted TDD output; passing legacy characterization alone does not cover new behavior. Follow the explicit TDD applicability rules for non-executable changes.
- **architecture-doc** -- Conditional on a relevant architecture decision or workflow obligation. Existing source and accepted boundary references suffice for a local change with no new architecture decision.
- **api-contract** -- Required when an affected public or inter-service contract needs preserving or changing. Do not invent an API artifact for an internal implementation detail.

## Outputs

- **source-code** -- The accepted slice's implementation. Hand its diff/revision, verification, contract changes, and unverified scope to the next required consumer. Use one brief note in the existing task/PR, or the completion response when no durable handoff is required. Link unchanged scope and decisions; do not repeat the intake JSON or create a section for every review dimension unless the accepted route requires those records.

A local bug fix with an accepted task and existing tests can continue from that evidence. A proposed new public API still needs its approved contract before dependent implementation. Required workflow obligations remain binding in both cases.

Check accepted work's revision, scope, and acceptance condition before reuse. Return changed facts to their owner and recheck dependent implementation and evidence; preserve unaffected decisions and approval. Never replace a missing contract with a guess or restart unrelated work.
