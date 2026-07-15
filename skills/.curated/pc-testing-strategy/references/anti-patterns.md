# Anti-Pattern Notes

1. **Ice cream cone**: Inverted pyramid with most tests at the E2E layer. Produces slow, brittle, expensive suites that nobody trusts.
2. **Testing implementation, not behavior**: Tests that break on every refactor because they assert on internal method calls instead of outputs. Test the contract, not the wiring.
3. **Shared mutable test state**: Tests that depend on execution order or shared database rows. Each test must set up and tear down its own state.
4. **Ignoring flaky tests**: Treating intermittent failures as "just flaky" instead of fixing them. Flaky tests erode confidence in the entire suite.
5. **Coverage theater**: Writing tests solely to hit a coverage number without asserting meaningful behavior. Coverage measures execution, not correctness.
6. **Happy-path-only strategy**: Claiming confidence while unsupported flows, coexistence boundaries, or contract failures have no explicit coverage.
