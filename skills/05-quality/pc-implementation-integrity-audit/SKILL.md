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

Identify changed boundaries where a completion claim depends on process, network, tool, model, filesystem, database, approval, tenant, or evidence behavior. Prioritize the path capable of hiding a real failure. Missing runtime evidence limits the claim; it is not by itself proof of deception.

### Step 2: Hunt Low-Level Defects

Check obvious failure classes first: wrong default, stale env, blocking subprocess pipes, missing timeout, unhandled invalid input, mutable shared state, broad exception swallowing, wrong status mapping, unsafe fallback, and repeated literals that encode policy.

Reuse concrete defects already reported by `pc-code-review`. Extend a finding only with distinct evidence of false success or hidden failure; do not repeat general correctness review under another role name.

### Step 3: Audit Mock and Fixture Honesty

Find mocks, fakes, fixtures, simulated adapters, local-only tools, and generated audit files. Trace whether the actual system under test runs and whether doubles isolate only external dependencies. Flag substitution that conceals the implementation or evidence represented as stronger than its source; a clearly labeled fixture is not itself a defect.

### Step 4: Challenge Success Claims

Trace each success event, `ok=true`, `validated`, `ready`, or `done` claim back to the source. Confirm failure paths cannot emit success and that external evidence is bound to the current task, request, trace, tenant, nonce, or artifact hash when required.

### Step 5: Check Test Integrity

Look for tests that patch out the only risky component, write audit files by hand, assert implementation details without exercising the contract, depend on stale Docker images, or use fixtures that guarantee the conclusion.

### Step 6: Report Only Evidence-Backed Findings

Prioritize findings by blast radius and deception risk. Include file and line references, the misleading claim or failure mode, and the smallest reliable guard needed.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Findings distinguish real runtime evidence from fixture, mock, simulated, or manually produced substitutes.
- [ ] False-success paths and untested risky boundaries are reported with evidence or marked unverified.
- [ ] The report identifies stale or unbound evidence and the completion claims it cannot support.
- [ ] Each blocker has an actionable handoff; unresolved blockers prevent acceptance of the implementation, not completion of the audit report.
