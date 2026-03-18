---
name: tech-selection
description: Use when the architecture is known and the team must choose concrete languages, frameworks, data stores, or infrastructure tools with explicit trade-offs instead of letting implementation drift into ad hoc stack decisions.
metadata:
  phase: 02-architecture
  inputs:
  - requirements-doc
  - architecture-doc
  outputs:
  - tech-decision-record
  prerequisites:
  - system-design
  quality_gate: Key technology choices are explicit, justified against the architecture drivers, and recorded with adoption consequences
  roles:
  - architect
  - tech-lead
  - devops-engineer
  methodologies:
  - all
  effort: medium
---

# Tech Selection

> Choose technologies by architectural fit and operational consequence, not by habit or trend.

## Context

Tech selection turns a structural design into a concrete stack. The right decision makes implementation straightforward and operations predictable. The wrong decision can hard-code skill gaps, cost surprises, and migration pain into the program.

Use this skill when the architecture is stable enough to evaluate real options. If the team skips explicit selection, those choices get made implicitly under delivery pressure and become harder to revisit.

## Inputs

- **requirements-doc** -- The functional and non-functional requirements that constrain viable technology choices.
- **architecture-doc** -- The architecture drivers, boundaries, deployment model, and quality constraints the technologies must satisfy.

## Process

### Step 1: Define the Decision Surface

List the categories that actually require a choice now:

- language or runtime
- framework or service platform
- datastore or messaging substrate
- infrastructure or deployment platform
- supporting tools that materially affect delivery or operations

Do not pretend every category is open if upstream constraints already settled it.

### Step 2: Compare Against Real Drivers

Evaluate each meaningful option against:

- architecture fit
- team skill and hiring reality
- operational burden
- security and compliance posture
- migration or lock-in cost
- ecosystem maturity and upgrade path

Use a small decision matrix when useful, but prefer clear narrative reasoning over spreadsheet theater.

### Step 3: Choose the Minimum Stack That Works

Favor the simplest stack that satisfies the drivers. Extra tools add integration cost, cognitive load, and future upgrade work. "Because it is popular" is not a valid criterion.

### Step 4: Record Consequences and Triggers

Document why the option won, what trade-offs were accepted, and what future condition would justify revisiting the decision.

## Outputs

- **tech-decision-record** -- The selected technologies, alternatives considered, rationale, trade-offs, and triggers for re-evaluation.

## Quality Gate

- [ ] All material stack choices are explicit
- [ ] Each choice is justified against architecture drivers
- [ ] Team capability and operational cost were considered
- [ ] Rejected alternatives and trade-offs are recorded
- [ ] Revisit triggers are documented for high-consequence choices

## Anti-Patterns

1. **Trend chasing** -- choosing tools for novelty instead of fit.
2. **Implicit stack choice** -- letting the first implementer decide by convenience.
3. **Resume-driven architecture** -- optimizing for engineer preference over product needs.
4. **Tool sprawl** -- adding multiple overlapping platforms where one would do.

## Related Skills

- [system-design](../system-design/SKILL.md) -- provides the drivers that technologies must satisfy
- [ci-cd](../../06-delivery/ci-cd/SKILL.md) -- operationalizes the selected toolchain in delivery
- [feature-development](../../04-implementation/feature-development/SKILL.md) -- builds within the chosen stack constraints
- [feasibility-study](../../00-discovery/feasibility-study/SKILL.md) -- may surface technical feasibility questions before final selection
