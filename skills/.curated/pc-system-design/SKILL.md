---
name: pc-system-design
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
  - pc-requirements-engineering
  quality_gate: Architecture review passed, all ADRs documented, component boundaries validated
  roles:
  - architect
  - tech-lead
  methodologies:
  - all
  effort: large
  internal: false
  distribution_surface: curated
  source_path: skills/02-architecture/pc-system-design/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# System Design

> Define the high-level structure of a system: its components, their responsibilities, how they communicate, and where they run.

## Context

System design translates requirements and domain knowledge into a technical blueprint.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Identify Architectural Drivers

Extract the top 5-7 quality attributes that will shape the architecture. Rank them by importance. Common drivers include:
- Performance (latency, throughput)
- Scalability (horizontal, vertical)
- Availability (uptime targets, failover)
- Security (data sensitivity, compliance)
- Maintainability (team size, release cadence)
- Cost (infrastructure budget, operational overhead)

Document drivers in a table that makes the trade-offs measurable:

| Attribute | Stimulus | Response | Measure | Rank | Source / Assumption |
|-----------|----------|----------|---------|------|---------------------|
| Availability | Primary region loses database connectivity | Service fails over to replica | RTO < 5 minutes | 1 | Requirement REQ-NFR-03 |
| Performance | Peak-hour search traffic doubles | Search responses remain within budget | p95 < 250 ms | 2 | Assumption, owner confirmation needed |

- **Stimulus** -- The event or condition that tests the architecture
- **Response** -- What the system must do when that event occurs
- **Measure** -- The bound, threshold, or decision rule that says "good enough"
- **Source / Assumption** -- Cite the input requirement, or explicitly label the assumption that still needs confirmation

If a driver is implied but not yet quantified, keep it as an architectural question or assumption. Do not convert vague inputs into false precision. A missing bound is better recorded as `TBD` with an owner than fabricated as fake certainty.

### Step 2: Choose Architectural Style

Select the primary style based on drivers. Map each driver to the style that best supports it:
- **Monolith** -- Small team, simple deployment, strong consistency needs
- **Microservices** -- Independent scaling, team autonomy, polyglot requirements
- **Serverless** -- Event-driven workloads, unpredictable traffic, minimal ops budget
- **Event-driven** -- Loose coupling, eventual consistency acceptable, complex workflows
- **Hybrid** -- Most real systems combine styles; document where each applies and why

When multiple styles satisfy the top-ranked drivers, prefer reversibility over perfection. Call out the exit cost of each candidate style: data migration burden, operational retraining, contract churn, and how expensive the architecture would be to unwind if the assumptions prove false.

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
- **Options considered** -- At least two plausible approaches when the choice is material. For technology-heavy decisions, compare fit, team capability, ecosystem maturity, operational cost, and exit cost.
- **Decision** -- What was decided
- **Consequences** -- What becomes easier, what becomes harder
- **Fitness functions** -- How the team will verify the decision is working in reality

If a decision is intentionally hard to reverse, say so directly and record why that irreversibility is acceptable.

### Step 7: Conduct Trade-Off Analysis

For each major decision, document:
- What you gain (the primary benefit)
- What you sacrifice (the cost or risk)
- What the team must be capable of operating successfully
- What ecosystem or integration risk you are accepting
- What the exit cost is if the decision proves wrong
- What would trigger reconsidering this decision (the trigger)

Use this lens when a concrete technology or platform choice is involved:
- **Fit for purpose** -- Does it solve the actual problem?
- **Team capability** -- Can the team run it without heroics?
- **Ecosystem maturity** -- Are dependencies, docs, and hiring reality acceptable?
- **Operational cost** -- What will it cost to run, monitor, and support?
- **Exit cost** -- How painful is it to migrate away later?

When two options are close, prefer the one that is easier to reverse or partition behind a seam.

### Step 8: Define Architecture Fitness Functions

For each top-ranked quality attribute and each hard-to-reverse decision, define at least one measurable fitness function:
- load or latency threshold
- failover rehearsal
- contract or compatibility test
- deployment or rollback drill
- migration dry run

Each fitness function should name:
- the check to run
- the expected threshold or pass/fail rule
- when it will be run
- who owns the evidence

If the team cannot define a real fitness function yet, record the missing information as a follow-up decision with an owner instead of hand-waving it away.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Architecture review completed with at least two reviewers
- [ ] Ranked quality attribute table exists with stimulus, response, measure, and source/assumption fields
- [ ] All significant decisions captured as ADRs
- [ ] Component boundaries align with domain bounded contexts
- [ ] Quality attribute trade-offs explicitly documented
- [ ] Hard-to-reverse decisions include reversibility or exit-cost discussion
- [ ] Fitness functions exist for the top drivers, or missing evidence is assigned to an owner
- [ ] Deployment topology accounts for failure modes
- [ ] C4 diagrams at context, container, and component levels exist
- [ ] No circular dependencies between components

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/02-architecture/pc-system-design/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
