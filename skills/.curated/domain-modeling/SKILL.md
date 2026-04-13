---
name: domain-modeling
description: Use when reviewed requirements still carry ambiguous business nouns, overlapping concepts, or possible bounded contexts, and the team needs a shared domain model before spec writing, API design, or data modeling.
metadata:
  phase: 01-specification
  inputs:
  - requirements-doc
  outputs:
  - domain-model
  prerequisites:
  - requirements-engineering
  quality_gate: Domain model reviewed, ubiquitous language documented and agreed upon by team
  roles:
  - architect
  - developer
  methodologies:
  - all
  effort: medium
  internal: false
  distribution_surface: curated
  source_path: skills/01-specification/domain-modeling/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Domain Modeling

> Model the business language before modeling storage, APIs, or implementation.

## Context

Domain modeling turns reviewed requirements into a stable business-language contract. Its job is to reduce ambiguity before later phases lock in schema, API, or implementation decisions.

In Prodcraft, this skill is most valuable when:

- the same noun may mean different things to product, operations, and engineering
- brownfield work must preserve legacy terms without letting them silently define the new model
- downstream skills need to know which concepts are authoritative, derived, transitional, or still unresolved

This is not database design, API design, or task planning. Stay at the domain layer.

## Inputs

- **requirements-doc** -- produced by the preceding skill in the lifecycle

## Process

### Step 1: Identify Core Entities

Extract the nouns and verb phrases that represent real business concepts:

- campaign
- reviewer assignment
- evidence package
- policy exception

Prefer concepts from the problem space, not solution-space placeholders like table, queue, endpoint, or job.

### Step 2: Define Relationships

Map how entities relate and where the relationship is authoritative:

- one-to-one / one-to-many / many-to-many
- optional vs required
- source-of-truth vs derived view
- transitional or compatibility-only relationship when brownfield coexistence is in play

### Step 3: Establish Ubiquitous Language

Create a glossary of domain terms with precise definitions. Resolve synonyms:
- Is "Customer" the same as "User"? If not, what's the difference?
- Is an "Order" created when the user clicks "Buy" or when payment succeeds?

Record legacy or tenant-specific terms separately when they must remain visible but should not silently dominate the new model.

### Step 4: Identify Bounded Contexts

Introduce bounded contexts only when the requirements justify a real language or responsibility split:
- **Order Context**: Order, LineItem, Discount
- **Payment Context**: Payment, Refund, Invoice
- **User Context**: Account, Profile, Preferences

Do not force DDD vocabulary onto a simple slice that only needs one coherent domain model.

### Step 5: Validate with Domain Experts

Walk the model against real scenarios from the requirements:

- happy path
- error or exception path
- brownfield or compatibility boundary

The model should make those scenarios easier to explain without leaking into schema or endpoint design.

## Outputs

- **domain-model** -- shared glossary, core entities, relationships, authoritative boundaries, and any justified bounded contexts

## Quality Gate

- [ ] Core entities and relationships documented visually (ER diagram or similar)
- [ ] Ubiquitous language glossary created with team agreement
- [ ] Bounded contexts identified (if system is complex enough to warrant them)
- [ ] Model validated against at least 3 real business scenarios

## Anti-Patterns

1. **Database-first modeling** -- Design the domain model, then derive the database schema. Not the reverse.
2. **Bounded contexts by reflex** -- Splitting the model into contexts before the requirements prove the split.
3. **Premature optimization** -- Don't model for query performance. Model for clarity. Performance comes later.
4. **Legacy term capture** -- Letting transitional brownfield vocabulary silently become the canonical future model.

## Related Skills

- [requirements-engineering](../requirements-engineering/SKILL.md) -- provides requirements to model
- [data-modeling](../../02-architecture/data-modeling/SKILL.md) -- translates domain model to data schema
- [api-design](../../02-architecture/api-design/SKILL.md) -- uses domain language for API resources

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/01-specification/domain-modeling/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
