---
name: pc-data-modeling
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
  - pc-system-design
  quality_gate: Data schema matches domain and architecture boundaries, lifecycle rules are explicit, and migration-sensitive decisions are documented
  roles:
  - architect
  - developer
  methodologies:
  - all
  effort: medium
  internal: false
  distribution_surface: curated
  source_path: skills/02-architecture/pc-data-modeling/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Data Modeling

> Turn concepts and boundaries into durable data structures the system can evolve safely.

## Context

Data modeling decides what the system remembers, how it relates, and how change propagates through storage over time.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

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

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Data ownership is explicit for every core entity
- [ ] Schema aligns with architecture boundaries and domain language
- [ ] Consistency and lifecycle rules are documented
- [ ] Brownfield or migration-sensitive paths are called out explicitly
- [ ] The model can evolve without avoidable downtime or unsafe backfills

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/02-architecture/pc-data-modeling/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
