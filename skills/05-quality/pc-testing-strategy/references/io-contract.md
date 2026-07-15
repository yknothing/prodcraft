# Input and Output Contract Notes

## Inputs

- **source-code**: The codebase under test, including its module boundaries and dependency graph.
- **task-list**: The reviewed implementation slice or change scope that defines what must be verified now.
- **architecture-doc**: System topology that determines integration points and test boundaries.
- **api-contract**: API specifications (OpenAPI, GraphQL schema) that drive contract tests.
- **intake-brief**: Must include `quality_target_context` with `runtime_context`, `exposure_profile`, `production_target`, `non_targets`, and `evidence_refs`.

In a lifecycle-aware system, testing strategy must preserve upstream scope boundaries. Do not hide unsupported release-1 behavior, coexistence risks, or unresolved contract questions under a generic "we have E2E tests" answer.

## Outputs

- **test-report**: Results from executing the test strategy, including coverage metrics, pass/fail status, and identified gaps.
- **test-strategy-doc**: Written document describing the layers, coverage targets, CI integration plan, and test data approach.
