---
name: pc-implementation-integrity-audit
description: Use after code changes when the reviewer must aggressively audit low-level defects, deceptive implementations, improper mocks, fake evidence, and test shortcuts before a delivery claim is trusted.
metadata:
  phase: 05-quality
  inputs:
  - intake-brief
  - source-code
  - test-suite
  - task-list
  outputs:
  - review-report
  prerequisites:
  - pc-feature-development
  quality_gate: No low-level defect, fake-success path, improper mock, fixture masquerade, or unverified evidence remains unreported
  roles:
  - reviewer
  - qa-engineer
  - tech-lead
  methodologies:
  - all
  effort: medium
---

# Implementation Integrity Audit

## Context

This skill is an adversarial quality audit for implementation honesty.

See [context notes](references/context.md).

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Identify Trust Boundaries

List boundaries where code crosses process, network, tool, model, filesystem, database, approval, tenant, or evidence surfaces. Treat every boundary as suspect until a test or runtime artifact proves the contract.

### Step 2: Hunt Low-Level Defects

Check obvious failure classes first: wrong default, stale env, blocking subprocess pipes, missing timeout, unhandled invalid input, mutable shared state, broad exception swallowing, wrong status mapping, unsafe fallback, and repeated literals that encode policy.

### Step 3: Audit Mock and Fixture Honesty

Find mocks, fakes, fixtures, simulated adapters, local-only tools, and generated audit files. Verify their names, raw refs, docs, and tests make the boundary explicit. Flag any fake that uses production-looking names or gets counted as real evidence.

### Step 4: Challenge Success Claims

Trace each success event, `ok=true`, `validated`, `ready`, or `done` claim back to the source. Confirm failure paths cannot emit success and that external evidence is bound to the current task, request, trace, tenant, nonce, or artifact hash when required.

### Step 5: Check Test Integrity

Look for tests that patch out the only risky component, write audit files by hand, assert implementation details without exercising the contract, depend on stale Docker images, or use fixtures that guarantee the conclusion.

### Step 6: Report Only Evidence-Backed Findings

Prioritize findings by blast radius and deception risk. Include file and line references, the misleading claim or failure mode, and the smallest reliable guard needed.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] No fake, fixture, mock, simulated runtime, or manually written audit artifact can be mistaken for real production evidence.
- [ ] Failure, blocked, rejected, and validation-error paths cannot emit success status or success events.
- [ ] Tests exercise the risky boundary or clearly label themselves as contract-only.
- [ ] Runtime evidence is fresh and bound to the current task/request/trace when used for completion claims.
