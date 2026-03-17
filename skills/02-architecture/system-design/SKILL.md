---
name: system-design
description: Use when designing or redesigning a system's high-level architecture, component boundaries, and interaction patterns
metadata:
  phase: 02-architecture
  inputs:
  - requirements-doc
  - spec-doc
  - domain-model
  outputs:
  - architecture-doc
  - component-diagram
  prerequisites:
  - spec-writing
  - domain-modeling
  quality_gate: Architecture review passed, all ADRs documented, component boundaries validated
  roles:
  - architect
  - tech-lead
  methodologies:
  - all
  effort: large
---

# System Design

> Define the high-level structure of a system: its components, their responsibilities, how they communicate, and where they run.

## Context

System design translates requirements and domain knowledge into a technical blueprint. A well-designed architecture absorbs change gracefully -- poor design decisions compound over time and become exponentially expensive to reverse. Invest here before writing code. Every subsequent skill in the architecture and implementation phases depends on the decisions made here.

## Inputs

- **requirements-doc** -- Functional and non-functional requirements with priority rankings. Pay special attention to quality attributes (latency, throughput, availability, consistency).
- **spec-doc** -- Detailed feature specifications that reveal integration points and complexity hotspots.
- **domain-model** -- Bounded contexts and entity relationships that inform component boundaries.

## Process

### Step 1: Identify Architectural Drivers

Extract the top 5-7 quality attributes that will shape the architecture. Rank them by importance. Common drivers include:
- Performance (latency, throughput)
- Scalability (horizontal, vertical)
- Availability (uptime targets, failover)
- Security (data sensitivity, compliance)
- Maintainability (team size, release cadence)
- Cost (infrastructure budget, operational overhead)

### Step 2: Choose Architectural Style

Select the primary style based on drivers. Map each driver to the style that best supports it:
- **Monolith** -- Small team, simple deployment, strong consistency needs
- **Microservices** -- Independent scaling, team autonomy, polyglot requirements
- **Serverless** -- Event-driven workloads, unpredictable traffic, minimal ops budget
- **Event-driven** -- Loose coupling, eventual consistency acceptable, complex workflows
- **Hybrid** -- Most real systems combine styles; document where each applies and why

### Step 3: Define Component Boundaries

Use the C4 model to work top-down:
1. **Context level** -- Draw the system boundary. Identify all external actors (users, systems, services). Document what crosses the boundary.
2. **Container level** -- Break the system into deployable units (web app, API, database, message queue). Assign responsibilities to each.
3. **Component level** -- Within each container, identify major structural components (modules, services, repositories). Define interfaces between them.
4. **Code level** -- Defer to implementation phase. Only sketch here if a component has unusual complexity.

### Step 4: Design Communication Patterns

For each component-to-component interaction, decide:
- Synchronous (REST, gRPC) vs asynchronous (message queue, event bus)
- Request/response vs publish/subscribe vs command/query
- Data format and contract (JSON, Protobuf, Avro)
- Failure handling (retries, circuit breakers, dead-letter queues)

### Step 5: Document Deployment Topology

Define where each container runs:
- Cloud provider and region strategy
- Container orchestration (Kubernetes, ECS) or serverless platform
- Network boundaries (VPC, subnets, load balancers)
- Data residency and compliance constraints

### Step 6: Create Architecture Decision Records

For every significant decision, write an ADR:
- **Title** -- Short noun phrase (e.g., "Use PostgreSQL for primary data store")
- **Status** -- Proposed, Accepted, Deprecated, Superseded
- **Context** -- What forces are at play
- **Decision** -- What was decided
- **Consequences** -- What becomes easier, what becomes harder

### Step 7: Conduct Trade-Off Analysis

For each major decision, document:
- What you gain (the primary benefit)
- What you sacrifice (the cost or risk)
- What would trigger reconsidering this decision (the trigger)

## Outputs

- **architecture-doc** -- Written document covering architectural style, component boundaries, communication patterns, deployment topology, and all ADRs. Must be understandable by any developer joining the team.
- **component-diagram** -- C4 diagrams at context, container, and component levels. Use a tool that supports version control (Structurizr DSL, Mermaid, PlantUML).

## Quality Gate

- [ ] Architecture review completed with at least two reviewers
- [ ] All significant decisions captured as ADRs
- [ ] Component boundaries align with domain bounded contexts
- [ ] Quality attribute trade-offs explicitly documented
- [ ] Deployment topology accounts for failure modes
- [ ] C4 diagrams at context, container, and component levels exist
- [ ] No circular dependencies between components

## Anti-Patterns

1. **Resume-Driven Architecture** -- Choosing technologies because they look impressive rather than because they solve the problem. Always start from drivers, not from tools.
2. **Big Design Up Front** -- Trying to nail every detail before writing code. Design to the level of certainty you have; mark unknowns as spikes for validation during implementation.
3. **Distributed Monolith** -- Splitting into microservices without achieving independent deployability. If services must deploy together, they are not separate services.
4. **Ignoring the "-ilities"** -- Focusing only on functional requirements. Non-functional requirements (scalability, observability, security) are architectural concerns -- they rarely emerge from good intentions alone.
5. **Architecture Astronautics** -- Over-abstracting and over-generalizing for hypothetical future needs. Design for today's known requirements with extension points for likely changes.

## Examples

**Choosing between monolith and microservices:**
- Team of 4 developers, single product, 1-2 releases per week --> modular monolith. Low coordination overhead, simple deployment, easy debugging.
- Team of 30 across 6 squads, each owning a business domain, independent release schedules --> microservices. Team autonomy justifies the operational complexity.

**ADR example:**
```
# ADR-003: Use event sourcing for order processing

Status: Accepted

Context: Orders go through complex state transitions. Audit requirements demand
full history. Multiple services react to order state changes.

Decision: Implement event sourcing for the Order aggregate. Store events in
an append-only event store. Project read models for query needs.

Consequences:
+ Full audit trail without additional logging
+ Natural integration with event-driven architecture
- Increased complexity in read model projection
- Team needs training on event sourcing patterns
- Eventually consistent read models require UX consideration
```

## Related Skills

- [spec-writing](../../01-specification/spec-writing/SKILL.md) -- Provides the spec-doc input
- [domain-modeling](../../01-specification/domain-modeling/SKILL.md) -- Provides bounded contexts that inform component boundaries
- [api-design](../api-design/SKILL.md) -- Designs the interfaces between components defined here
- [data-modeling](../data-modeling/SKILL.md) -- Translates the domain model into storage schemas within this architecture
- [security-design](../security-design/SKILL.md) -- Layers security controls onto the architecture
- [tech-selection](../tech-selection/SKILL.md) -- Evaluates concrete technologies for the components defined here
- [task-breakdown](../../03-planning/task-breakdown/SKILL.md) -- Decomposes the architecture into implementable tasks
