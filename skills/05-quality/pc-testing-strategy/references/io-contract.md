# Input and Output Contract Notes

## Inputs

- **intake-brief** -- Required approved scope and `quality_target_context`, including runtime, exposure, production target, non-targets, and evidence references.
- **task-list** -- Required change/acceptance context from an existing reviewed task or equivalent accepted section. A separate task-list file is unnecessary unless the workflow requires it.
- **source-code** -- Required for claims about an existing implementation. Before implementation, use accepted behavior/contracts and mark implementation-dependent checks as planned.
- **architecture-doc**, **api-contract** -- Conditional on affected architecture or interface boundaries. Current accepted references can satisfy them; no public API artifact is needed for a target with no such surface.

Preserve upstream scope, coexistence constraints, unsupported behavior, and explicit policy gates. Missing context blocks only the dependent test-design or execution decision.

## Outputs

- **test-strategy-doc** -- Required for strategy work. Map each material risk to a check/layer, meaningful assertion, real versus isolated dependency, data/environment, acceptance condition, and owner or consumer. `pc-ci-cd` consumes the scheduling/gate decisions; `pc-e2e-scenario-design` consumes only the selected E2E risks. A compact table in an existing document can suffice.
- **test-report** -- Conditional on actual execution. Record the source revision, environment, commands/checks, observed results, and unverified scope for `pc-release-management`. Do not manufacture a report of passing runs during strategy-only work. If a workflow requires execution evidence, the strategy alone cannot satisfy that obligation.
