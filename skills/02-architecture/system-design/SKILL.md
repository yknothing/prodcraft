---
name: system-design
description: Use when reviewed requirements or specifications are ready and the team must decide high-level architecture, component boundaries, integration seams, or brownfield coexistence strategy before API design, technology selection, or task planning.
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
  - requirements-engineering
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

In spec-driven work, system design often starts from a reviewed spec package. In agile and brownfield work, it may start from a reviewed requirements document with open questions still visible. Do not silently "fix" requirement ambiguity inside the architecture. Preserve unresolved scope, compatibility, and quality-bound questions as design constraints or architectural open questions.

## Inputs

- **requirements-doc** -- Minimum required input. Functional and non-functional requirements with priority rankings, scope boundaries, and unresolved questions. Pay special attention to quality attributes (latency, throughput, availability, consistency) and brownfield coexistence constraints.
- **spec-doc** -- Optional amplifying input when spec-driven or waterfall work produces a detailed specification.
- **domain-model** -- Optional amplifying input when the problem has enough domain complexity that entity boundaries or ubiquitous language should shape component boundaries.

## Process

### Step 1: Identify Architectural Drivers

Extract the top 5-7 quality attributes that will shape the architecture. Rank them by importance. Common drivers include:
- Performance (latency, throughput)
- Scalability (horizontal, vertical)
- Availability (uptime targets, failover)
- Security (data sensitivity, compliance)
- Maintainability (team size, release cadence)
- Cost (infrastructure budget, operational overhead)

If a driver is implied but not yet quantified, keep it as an architectural question or assumption. Do not convert vague inputs into false precision.

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

For brownfield work, explicitly identify:
- legacy components that must remain in service
- seams where coexistence, routing, or facade patterns are needed
- boundaries that are intentionally deferred because migration rules are still unresolved

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

Keep topology at the level needed for architectural reasoning. Detailed rollout plans, traffic percentages, and migration sequencing belong in later delivery planning unless they are true architectural constraints.

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
6. **Closing open questions by accident** -- Turning unresolved compatibility, synchronization, or rollout questions into assumed architecture facts without labeling them as assumptions or follow-up decisions.

## Reference Material

For worked architecture-style comparisons and an ADR example, see [decision-examples](references/decision-examples.md). Keep the core skill focused on drivers, boundaries, and trade-offs; use the reference when the team needs examples to calibrate the artifact shape.

## Related Skills

- [spec-writing](../../01-specification/spec-writing/SKILL.md) -- Provides the spec-doc input
- [domain-modeling](../../01-specification/domain-modeling/SKILL.md) -- Provides bounded contexts that inform component boundaries
- [api-design](../api-design/SKILL.md) -- Designs the interfaces between components defined here
- `data-modeling` (planned) -- Translates the domain model into storage schemas within this architecture
- `security-design` (planned) -- Layers security controls onto the architecture
- `tech-selection` (planned) -- Evaluates concrete technologies for the components defined here
- [task-breakdown](../../03-planning/task-breakdown/SKILL.md) -- Decomposes the architecture into implementable tasks
