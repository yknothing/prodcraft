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
  prerequisites:
  - pc-system-design
  quality_gate: API contract reviewed, backward compatibility verified, documentation complete
  roles:
  - architect
  - developer
  methodologies:
  - all
  effort: medium
---

# API Design

> APIs are contracts. Design them as carefully as you would a legal agreement -- they're hard to change once published.

## Context

API design defines how system components communicate.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Choose API Style

| Style | Best For | Trade-offs |
|-------|----------|------------|
| REST | CRUD resources, public APIs | Simple, cacheable, but over/under-fetching |
| GraphQL | Complex data graphs, mobile clients | Flexible queries, but complex caching |
| gRPC | Service-to-service, high performance | Fast, typed, but not browser-native |
| Event-driven | Async workflows, decoupling | Loose coupling, but eventual consistency |

Choose style from the architecture and consumer boundary, not from fashion. If the architecture leaves a timing or consistency question unresolved, preserve that uncertainty in the contract assumptions instead of collapsing it into a premature transport decision.

### Step 2: Design Resource Model

Map domain entities to API resources. Use nouns, not verbs:
- `GET /orders` not `GET /getOrders`
- `POST /orders/{id}/cancel` for actions on resources
- Use consistent naming: plural nouns, kebab-case for multi-word

For brownfield work, explicitly separate:
- externally visible contract resources
- legacy compatibility or adapter surfaces
- internal implementation details that must not leak into the published contract

### Step 3: Define Operations

For each resource: which CRUD operations? What request/response schemas? What status codes?

Document contract boundaries explicitly:
- what the API guarantees in release 1
- what remains unsupported or out of scope
- which fields or behaviors are conditional on unresolved upstream decisions

### Step 4: Plan Versioning

Choose a strategy before the first release:
- **URL versioning**: `/v1/orders` (simple, explicit)
- **Header versioning**: `Accept: application/vnd.api+json;version=1` (clean URLs)
- **No versioning + evolution**: Additive changes only, never remove fields

For brownfield modernization, include backward-compatibility rules between legacy and new surfaces. If coexistence exists, define what callers can rely on during the coexistence window without committing to migration choreography.

### Step 5: Design Error Handling

Consistent error responses across all endpoints:
```json
{
  "error": { "code": "VALIDATION_ERROR", "message": "Human-readable message", "details": [...] }
}
```

### Step 6: Document with OpenAPI/Protobuf

Write the contract specification before implementation. Use OpenAPI for REST, protobuf for gRPC. This enables contract testing and client code generation.

### Step 7: Preserve Open Questions and Assumptions

If architecture or requirements still leave uncertainty around:
- synchronization timing
- legacy-read behavior
- tenant-specific compatibility rules
- authorization edge cases

record those as explicit contract assumptions, deferred fields, or open questions. Do not silently hard-code them into endpoint behavior.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] API contract specified in OpenAPI/protobuf/GraphQL schema
- [ ] Consistent naming, error handling, and pagination across all endpoints
- [ ] Versioning strategy documented
- [ ] Authentication and authorization specified per endpoint
- [ ] Backward compatibility policy defined
