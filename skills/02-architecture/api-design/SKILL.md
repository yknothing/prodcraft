---
name: api-design
description: Use when designing REST, GraphQL, gRPC, or other API interfaces between services or for external consumers
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
  - system-design
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

API design defines how system components communicate. A well-designed API is intuitive, consistent, and evolvable. A poorly designed API creates coupling, breaks clients, and generates support burden for years.

## Process

### Step 1: Choose API Style

| Style | Best For | Trade-offs |
|-------|----------|------------|
| REST | CRUD resources, public APIs | Simple, cacheable, but over/under-fetching |
| GraphQL | Complex data graphs, mobile clients | Flexible queries, but complex caching |
| gRPC | Service-to-service, high performance | Fast, typed, but not browser-native |
| Event-driven | Async workflows, decoupling | Loose coupling, but eventual consistency |

### Step 2: Design Resource Model

Map domain entities to API resources. Use nouns, not verbs:
- `GET /orders` not `GET /getOrders`
- `POST /orders/{id}/cancel` for actions on resources
- Use consistent naming: plural nouns, kebab-case for multi-word

### Step 3: Define Operations

For each resource: which CRUD operations? What request/response schemas? What status codes?

### Step 4: Plan Versioning

Choose a strategy before the first release:
- **URL versioning**: `/v1/orders` (simple, explicit)
- **Header versioning**: `Accept: application/vnd.api+json;version=1` (clean URLs)
- **No versioning + evolution**: Additive changes only, never remove fields

### Step 5: Design Error Handling

Consistent error responses across all endpoints:
```json
{
  "error": { "code": "VALIDATION_ERROR", "message": "Human-readable message", "details": [...] }
}
```

### Step 6: Document with OpenAPI/Protobuf

Write the contract specification before implementation. Use OpenAPI for REST, protobuf for gRPC. This enables contract testing and client code generation.

## Quality Gate

- [ ] API contract specified in OpenAPI/protobuf/GraphQL schema
- [ ] Consistent naming, error handling, and pagination across all endpoints
- [ ] Versioning strategy documented
- [ ] Authentication and authorization specified per endpoint
- [ ] Backward compatibility policy defined

## Anti-Patterns

1. **Chatty APIs** -- Requiring 10 calls to render one page. Design for client use cases.
2. **Leaking implementation** -- Exposing internal IDs, database column names, or internal service structure.
3. **Ignoring pagination** -- Every list endpoint must paginate. No unbounded responses.
4. **Breaking changes without versioning** -- Renaming a field breaks every client. Plan for evolution.

## Related Skills

- [system-design](../system-design/SKILL.md) -- defines the components that need APIs
- [domain-modeling](../../01-specification/domain-modeling/SKILL.md) -- provides the resource model
- [feature-development](../../04-implementation/feature-development/SKILL.md) -- implements the API
- [testing-strategy](../../05-quality/testing-strategy/SKILL.md) -- contract testing for APIs
