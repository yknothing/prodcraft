---
name: testing-strategy
description: Use when defining or reviewing the testing approach for a feature, service, or system
metadata:
  phase: 05-quality
  inputs:
  - source-code
  - acceptance-criteria-set
  - architecture-doc
  - api-contract
  outputs:
  - test-report
  - test-strategy-doc
  prerequisites:
  - tdd
  quality_gate: Test strategy documented, critical paths covered by E2E, coverage thresholds met
  roles:
  - qa-engineer
  - developer
  methodologies:
  - all
  effort: medium
---

# Testing Strategy

> Define a layered testing approach that balances confidence, speed, and maintenance cost.

## Context

A testing strategy defines what to test, at what layer, and with what tools. Without it, teams either over-test at the wrong layer (slow, brittle E2E suites) or under-test critical paths (production incidents). The strategy aligns testing effort with risk: high-risk paths get more coverage, low-risk paths get less. It also determines how tests integrate into CI/CD, how test data is managed, and how the team prevents test suite rot.

## Inputs

- **source-code**: The codebase under test, including its module boundaries and dependency graph.
- **acceptance-criteria-set**: Business requirements that define expected behavior.
- **architecture-doc**: System topology that determines integration points and test boundaries.
- **api-contract**: API specifications (OpenAPI, GraphQL schema) that drive contract tests.

## Process

### Step 1: Define the Test Pyramid

Establish the ratio across layers. A healthy default:
- **Unit tests (70%)**: Test individual functions and classes in isolation. Fast, cheap, stable.
- **Integration tests (20%)**: Test interactions between components, database queries, API calls.
- **End-to-end tests (10%)**: Test critical user journeys through the full stack. Expensive, slower, more brittle.

Adjust ratios based on system characteristics. API-heavy services may use a "testing diamond" with more integration tests. UI-heavy applications may need more E2E and visual regression tests.

### Step 2: Identify Critical Paths for E2E

Map the top 5-10 user journeys that must never break: signup, login, core transactions, payment flows. These are E2E candidates. Everything else should be covered at lower layers.

### Step 3: Set Coverage Thresholds

Define per-layer targets:
- Unit: 80% line coverage minimum on business logic.
- Integration: All external service interactions covered.
- E2E: All critical paths covered.

Do not chase 100% coverage -- it produces low-value tests on trivial code. Measure branch coverage in addition to line coverage.

### Step 4: Plan Test Data Management

Define how test data is created, isolated, and cleaned up:
- Unit tests: Use factories and builders, never shared fixtures.
- Integration tests: Use database transactions with rollback, or dedicated test databases.
- E2E tests: Use seed scripts or API-driven setup. Never depend on production data.

### Step 5: Design CI Integration

Define which tests run when:
- **On commit/push**: Unit tests, linting, type checks (must complete in under 5 minutes).
- **On pull request**: Unit + integration tests, security scans (must complete in under 15 minutes).
- **On merge to main**: Full suite including E2E, performance smoke tests.
- **Nightly/scheduled**: Full E2E suite, performance benchmarks, chaos tests.

### Step 6: Plan Contract Testing

For services with API consumers, implement contract tests:
- Consumer-driven contracts (Pact) for internal APIs.
- Schema validation against OpenAPI specs for public APIs.
- Run contract tests on both producer and consumer CI pipelines.

### Step 7: Address Flaky Test Prevention

Establish practices to prevent and manage flaky tests:
- Quarantine flaky tests immediately (do not let them erode trust in the suite).
- Require tests to pass 10 consecutive runs before un-quarantining.
- Track flakiness metrics and set a team SLO (e.g., less than 1% flaky rate).
- Ban sleep-based waits; use polling with timeouts.

## Outputs

- **test-report**: Results from executing the test strategy, including coverage metrics, pass/fail status, and identified gaps.
- **test-strategy-doc**: Written document describing the layers, coverage targets, CI integration plan, and test data approach.

## Quality Gate

- [ ] Test strategy document exists and is reviewed
- [ ] Critical user paths are covered by E2E tests
- [ ] Coverage thresholds are met per layer
- [ ] CI pipeline runs the correct tests at each stage
- [ ] No quarantined tests older than 30 days without a fix plan
- [ ] Contract tests exist for all inter-service APIs

## Anti-Patterns

1. **Ice cream cone**: Inverted pyramid with most tests at the E2E layer. Produces slow, brittle, expensive suites that nobody trusts.
2. **Testing implementation, not behavior**: Tests that break on every refactor because they assert on internal method calls instead of outputs. Test the contract, not the wiring.
3. **Shared mutable test state**: Tests that depend on execution order or shared database rows. Each test must set up and tear down its own state.
4. **Ignoring flaky tests**: Treating intermittent failures as "just flaky" instead of fixing them. Flaky tests erode confidence in the entire suite.
5. **Coverage theater**: Writing tests solely to hit a coverage number without asserting meaningful behavior. Coverage measures execution, not correctness.

## Related Skills

- [tdd](../../04-implementation/tdd/SKILL.md) -- provides the test-first discipline that feeds into strategy
- [code-review](../code-review/SKILL.md) -- reviews test quality alongside code quality
- [security-audit](../security-audit/SKILL.md) -- security testing integrates into the strategy
- [performance-audit](../performance-audit/SKILL.md) -- performance testing as part of the overall approach
- [ci-cd](../../06-delivery/ci-cd/SKILL.md) -- consumes the strategy to configure pipeline test stages
