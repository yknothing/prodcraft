---
name: data-modeling
description: Use when the system structure is known and the team must turn domain concepts and architectural boundaries into durable storage schemas, ownership rules, and migration-safe data flow decisions before implementation.
metadata:
  phase: 02-architecture
  inputs:
  - architecture-doc
  - domain-model
  - spec-doc
  outputs:
  - data-schema
  prerequisites:
  - system-design
  quality_gate: Data schema matches domain and architecture boundaries, lifecycle rules are explicit, and migration-sensitive decisions are documented
  roles:
  - architect
  - developer
  methodologies:
  - all
  effort: medium
---

# Data Modeling

> Turn concepts and boundaries into durable data structures the system can evolve safely.

## Context

Data modeling decides what the system remembers, how it relates, and how change propagates through storage over time. In Prodcraft, it bridges domain language and implementation reality: the model must reflect real ownership boundaries, consistency needs, and migration cost.

Use this skill after system design clarifies component boundaries. If storage design is left implicit, implementation invents schema rules piecemeal and migration risk surfaces late.

## Inputs

- **architecture-doc** -- Defines component boundaries, data ownership, and integration seams.
- **domain-model** -- Provides entities, value objects, and relationships that should survive into persistence.
- **spec-doc** -- Captures workflow rules, constraints, and edge cases that shape state transitions.

## Process

### Step 1: Define Data Ownership

For each major entity or aggregate, decide:

- which component owns the canonical record
- which components may cache or project it
- which fields are authoritative versus derived
- what must stay transactionally consistent versus eventually consistent

### Step 2: Shape the Storage Model

Translate the domain into tables, collections, events, or documents based on access patterns and consistency needs. Keep read models and write models separate when the workload or boundary requires it.

Avoid schemas that blur service boundaries just because a join would be convenient.

### Step 3: Model Lifecycle and Mutation Rules

Document:

- identifiers and uniqueness rules
- state transitions and retention rules
- soft delete, archival, and backfill expectations
- migration hazards for legacy or brownfield coexistence paths

### Step 4: Test the Schema Against Real Change

Before finalizing, challenge the model with likely future operations:

- adding a field without downtime
- replaying or backfilling data
- migrating legacy records
- supporting partial rollout or coexistence during modernization

If the data model makes routine change unsafe, revise it now.

## Outputs

- **data-schema** -- The persistence model, ownership rules, and migration-sensitive notes required for implementation and future evolution.

## Quality Gate

- [ ] Data ownership is explicit for every core entity
- [ ] Schema aligns with architecture boundaries and domain language
- [ ] Consistency and lifecycle rules are documented
- [ ] Brownfield or migration-sensitive paths are called out explicitly
- [ ] The model can evolve without avoidable downtime or unsafe backfills

## Anti-Patterns

1. **Schema-first architecture** -- letting database convenience redraw service boundaries.
2. **One model for every concern** -- forcing write, read, analytics, and migration needs into the same shape.
3. **Implicit ownership** -- multiple components update the same record without a canonical owner.
4. **Migration amnesia** -- designing a clean schema that ignores how real data will get there.

## Related Skills

- [system-design](../system-design/SKILL.md) -- provides the component and ownership boundaries
- [domain-modeling](../../01-specification/domain-modeling/SKILL.md) -- provides the conceptual model
- [feature-development](../../04-implementation/feature-development/SKILL.md) -- implements against the resulting schema
- `migration-strategy` (planned) -- handles larger migration programs that depend on the model
