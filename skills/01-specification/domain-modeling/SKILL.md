---
name: domain-modeling
description: Use when identifying core domain entities, relationships, and ubiquitous language for a system
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
---

# Domain Modeling

> Model the problem domain before modeling the solution. The domain model is the shared language between business and engineering.

## Context

Domain modeling creates a shared understanding of the core concepts in your system. It establishes a ubiquitous language -- terms that mean the same thing to everyone on the team. This prevents the #1 communication failure: using the same word to mean different things.

## Process

### Step 1: Identify Core Entities

From the requirements, extract the nouns that represent real things in the domain:
- User, Account, Order, Product, Payment, Subscription
- Focus on business concepts, not technical ones (no "Table" or "Queue")

### Step 2: Define Relationships

Map how entities relate: one-to-one, one-to-many, many-to-many. Document cardinality and optionality.

### Step 3: Establish Ubiquitous Language

Create a glossary of domain terms with precise definitions. Resolve synonyms:
- Is "Customer" the same as "User"? If not, what's the difference?
- Is an "Order" created when the user clicks "Buy" or when payment succeeds?

### Step 4: Identify Bounded Contexts

Group related entities into bounded contexts (DDD). Each context has its own model and language:
- **Order Context**: Order, LineItem, Discount
- **Payment Context**: Payment, Refund, Invoice
- **User Context**: Account, Profile, Preferences

### Step 5: Validate with Domain Experts

Walk through the model with stakeholders using real scenarios. The model should make business conversations easier, not harder.

## Quality Gate

- [ ] Core entities and relationships documented visually (ER diagram or similar)
- [ ] Ubiquitous language glossary created with team agreement
- [ ] Bounded contexts identified (if system is complex enough to warrant them)
- [ ] Model validated against at least 3 real business scenarios

## Anti-Patterns

1. **Database-first modeling** -- Design the domain model, then derive the database schema. Not the reverse.
2. **One model to rule them all** -- Different contexts need different models. A "Product" in catalog is different from "Product" in shipping.
3. **Premature optimization** -- Don't model for query performance. Model for clarity. Performance comes later.

## Related Skills

- [requirements-engineering](../requirements-engineering/SKILL.md) -- provides requirements to model
- [data-modeling](../../02-architecture/data-modeling/SKILL.md) -- translates domain model to data schema
- [api-design](../../02-architecture/api-design/SKILL.md) -- uses domain language for API resources
