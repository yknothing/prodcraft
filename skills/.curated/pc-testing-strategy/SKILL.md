---
name: pc-testing-strategy
description: Use when a reviewed implementation slice or feature needs a deliberate test plan across unit, integration, contract, and end-to-end layers, especially when brownfield regressions, unsupported flows, coexistence boundaries, or API contracts require explicit coverage beyond the default happy path.
metadata:
  phase: 05-quality
  inputs:
  - intake-brief
  - source-code
  - task-list
  - architecture-doc
  - api-contract
  outputs:
  - test-report
  - test-strategy-doc
  prerequisites:
  - pc-tdd
  quality_gate: Test strategy documented, critical paths covered by E2E, coverage thresholds met
  roles:
  - qa-engineer
  - developer
  methodologies:
  - all
  effort: medium
  internal: false
  distribution_surface: curated
  source_path: skills/05-quality/pc-testing-strategy/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Testing Strategy

> Define a layered testing approach that balances confidence, speed, and maintenance cost.

## Context

A testing strategy defines what to test, at what layer, and with what tools.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 0: Calibrate the Test Target

Read `quality_target_context` before choosing layers. Confirm whether the reviewed target is an agent-internal skill, host runtime tool, local harness, internal service, or public HTTP service.

For an agent-internal skill, bias toward trigger evals, fixture and golden-output checks, schema or validator coverage, command/tool boundary tests, artifact privacy checks, curated export parity, and runtime portability probes. Do not default to browser E2E, OpenAPI contract, or public web-auth flows unless the target actually exposes that surface.

For a public HTTP service or internet-exposed target, keep API contract, integration, browser/E2E, auth, rate-limit, and abuse-path coverage where risk supports it. If the target context is unknown, document the blind spot and ask for the smallest clarification that can change the test layer decision.

### Step 1: Define the Test Pyramid

Establish the ratio across layers. A healthy default:
- **Unit tests (70%)**: Test individual functions and classes in isolation. Fast, cheap, stable.
- **Integration tests (20%)**: Test interactions between components, database queries, API calls.
- **End-to-end tests (10%)**: Test critical user journeys through the full stack. Expensive, slower, more brittle.

Adjust ratios based on system characteristics. API-heavy services may use a "testing diamond" with more integration tests. UI-heavy applications may need more E2E and visual regression tests.

For brownfield or compatibility-sensitive work, bias toward:
- contract tests for externally visible release-1 behavior
- integration tests for coexistence and adapter boundaries
- targeted characterization/regression tests for legacy behavior that must remain safe
- fewer but sharper E2E flows

### Step 2: Identify Critical Paths for E2E

Map the top 5-10 user journeys that must never break: signup, login, core transactions, payment flows. These are E2E candidates. Everything else should be covered at lower layers.

Treat unsupported or deferred release-boundary behavior as critical verification targets too. They often belong in contract or integration layers rather than only in E2E.

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

If contract behavior is still partly unresolved, define tests that fail closed for unsupported or unknown cases rather than inventing permissive behavior.

### Step 7: Address Flaky Test Prevention

Establish practices to prevent and manage flaky tests:
- Quarantine flaky tests immediately (do not let them erode trust in the suite).
- Require tests to pass 10 consecutive runs before un-quarantining.
- Track flakiness metrics and set a team SLO (e.g., less than 1% flaky rate).
- Ban sleep-based waits; use polling with timeouts.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Test strategy document exists and is reviewed
- [ ] Critical user paths are covered by E2E tests
- [ ] Coverage thresholds are met per layer
- [ ] CI pipeline runs the correct tests at each stage
- [ ] No quarantined tests older than 30 days without a fix plan
- [ ] Contract tests exist for all inter-service APIs
- [ ] Brownfield coexistence and unsupported release-boundary behavior have explicit coverage where applicable

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/05-quality/pc-testing-strategy/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
