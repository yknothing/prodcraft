---
name: pc-api-design
description: Use when architecture boundaries are already defined and the team must specify stable API contracts between components or for external consumers, especially when backward compatibility, brownfield coexistence, authorization rules, and error semantics must be made explicit before implementation.
metadata:
  phase: 02-architecture
  inputs:
  - architecture-doc
  - domain-model
  - requirements-doc
  outputs:
  - api-contract
  - api-documentation
  prerequisites: []
  quality_gate: API contract reviewed, backward compatibility verified, documentation complete
  roles:
  - architect
  - developer
  methodologies:
  - all
  effort: medium
---

# API Design

> Define what callers can rely on before changing either side of an interface.

## Context

API design specifies communication across an existing component or consumer boundary.
See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Establish the Boundary

Identify callers, providers, use cases, trust, timing, and compatibility obligations. Reuse the current transport unless a concrete requirement justifies changing it. Preserve unresolved architecture decisions; do not choose transport to hide a consistency question.

### Step 2: Specify the Actual Interface

Choose the relevant contract form:

| Interface | Specify |
|---|---|
| REST | Resources, methods, request/response schemas, status codes, and bounded list behavior |
| GraphQL | Types, queries/mutations/subscriptions, nullability, errors, and query limits |
| gRPC | Services, messages, status, deadlines, and streaming behavior |
| Events | Producer/consumer, payload/version, delivery and ordering guarantees, duplicate handling, and failure/replay behavior |
| In-process | Signatures/types, preconditions, return/error behavior, ownership, and side effects |

Keep names consistent with the domain. Separate caller-visible behavior, legacy adapters, and internal implementation. For example, REST resource routes use `GET /orders`, not `GET /getOrders`; do not impose that naming rule on events or functions.

### Step 3: Define Observable Semantics

For each operation or message, specify valid input, success, errors, and access rules at its actual trust boundary. Include timeouts, cancellation, retries, idempotency, pagination, or backpressure where callers depend on them. State bounds for collections; a small fixed enumeration need not invent pagination.

Mark supported release behavior and non-goals. Assign an owner to any unresolved decision and identify the operation it blocks; a draft assumption does not authorize dependent implementation.

### Step 4: Plan Compatibility

Compare old and new caller behavior. Define additive/breaking changes, schema or API version handling, and deprecation obligations for this interface. In brownfield work, state guarantees during coexistence. Keep migration choreography in the deployment/design owner unless it is part of the caller contract.

### Step 5: Produce and Review the Contract

Use a checkable format already suited to the project: OpenAPI, GraphQL SDL, protobuf, event payload schemas, or typed function interfaces. Include representative valid/error examples and consumer expectations. Review with affected owners; implementation and contract tests consume the same version.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Contract format matches the actual interface and its consumers
- [ ] Operations/messages define data, success, failure, and applicable access/collection rules
- [ ] Compatibility obligations and version evolution are explicit
- [ ] Required reviewers approve the defined scope; unresolved decisions block only dependent work
- [ ] Documentation and examples are sufficient for implementation and consumer verification
