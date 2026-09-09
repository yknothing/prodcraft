---
name: pc-testing-strategy
description: Use when a change needs a risk-based verification strategy or an existing suite leaves important behavior, compatibility, or dependency boundaries unprotected.
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
  prerequisites: []
  quality_gate: Relevant risks map to meaningful checks and acceptance conditions; planned verification is distinguished from executed results
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

A testing strategy defines what to test, at what layer, and with what tools.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 0: Establish the Target and Claim

Read `quality_target_context`, scope, and the claim that needs evidence. Distinguish an agent-internal skill, host tool, local harness, internal service, and public HTTP service. HTTP-shaped code alone does not establish public exposure. Resolve only unknowns that change the checking strategy.

For an agent-internal skill, consider invocation behavior, actual outputs/actions, artifact privacy, tool boundaries, schemas, export parity, and runtime loading. Static parsing does not prove useful behavior. Public HTTP service checks require the corresponding exposed interfaces and risks.

### Step 1: Map Risks to the Lowest Sufficient Layer

For each material failure, name the observable contract, useful input or trigger, expected result, and the boundary that must remain real. Reuse adequate current tests. Choose unit, integration, contract, E2E, visual, or manual checks according to that risk, not a fixed ratio or journey count. A layered strategy need not use every layer.

Use characterization for preserved legacy behavior and targeted integration for coexistence, failure handling, data migration, and dependency boundaries. Add E2E only where lower layers cannot establish the required interaction. A mock may isolate an external dependency; it must not replace the behavior being verified.

### Step 2: Set Acceptance and Data Rules

Keep explicit project coverage and release gates. Otherwise choose targets from actual risk and missing branches; line coverage alone is not correctness. Record unsupported/deferred behavior and its expected rejection or failure path.

Choose isolated reproducible data. Shared immutable fixtures are valid; shared mutable state and order-dependent tests are not. Use authorized test data and define cleanup. Do not assume production-data access or add a test framework merely because a technique names one.

### Step 3: Fit Checks to the Delivery Path

Assign required checks to the stage where failure must block progress, accounting for measured runtime and environment availability. Use existing CI/tools when sufficient. Contract checks should exercise relevant producer/consumer boundaries; OpenAPI or a consumer-contract framework applies only where that contract exists.

Diagnose flaky behavior. Quarantine requires an owner, expiry/re-entry condition, and explicit visibility of the lost coverage. It cannot silently remove a required gate. Confirm stability against the observed failure conditions; arbitrary rerun counts are not proof. Prefer condition-based waits with bounded timeouts.

### Step 4: Deliver Strategy or Results Honestly

Produce `test-strategy-doc` for strategy work; produce `test-report` only for actual authorized execution, following the I/O contract. Mark unexecuted work planned. A strategy cannot satisfy a workflow or strict-mode obligation for execution evidence.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Material risks and changed contracts map to appropriate checks without arbitrary layer quotas
- [ ] Required policy gates, data boundaries, and unverified scope are explicit
- [ ] The strategy is actionable by its named consumer; unavailable environments have a clear handoff
- [ ] Any reported execution result has actual evidence; strategy-only work makes no passing claim
- [ ] Flaky or missing coverage remains visible and cannot silently satisfy a blocking gate
