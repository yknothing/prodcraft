# Input and Output Contract Notes

## Inputs

- **source-code** -- The product surface and implementation seams that the scenarios must exercise realistically.
- **task-list** -- The current slice, risk boundary, or release scope that the scenarios must protect.
- **test-strategy-doc** -- The upstream decision on which layers matter now, which risks are critical, and which flows belong in E2E versus lower layers.

## Outputs

- **test-suite** -- Scenario and edge-case tests that cover at least one extended stateful journey for each critical persona or release boundary in scope.
- **test-report** -- What scenarios were added or exercised, which risk boundaries they protect, and any remaining blind spots or deferred coverage.
