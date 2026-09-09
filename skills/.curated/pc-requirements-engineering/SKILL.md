---
name: pc-requirements-engineering
description: "Use when the work is still at the \u201Cwhat should we build\u201D stage and approved discovery inputs or entry-stack outputs must become prioritized requirements and scope boundaries before specification, architecture, planning, or coding. Not for acceptance criteria, spec review, or implementation."
metadata:
  phase: 01-specification
  inputs:
  - intake-brief
  - problem-frame
  - design-direction
  - market-research-report
  - user-persona-set
  - feasibility-report
  outputs:
  - requirements-doc
  prerequisites:
  - pc-intake
  quality_gate: Requirements doc reviewed by stakeholders, all P0/P1 requirements have acceptance criteria
  roles:
  - product-manager
  - tech-lead
  methodologies:
  - all
  effort: large
  internal: false
  distribution_surface: curated
  source_path: skills/01-specification/pc-requirements-engineering/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Requirements Engineering

> Transform user needs and business goals into precise, testable requirements.

## Context

Requirements engineering bridges discovery and design.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Gather Functional Requirements

For each affected user/workflow, reuse available personas and journeys to identify what the system must do:
- User actions (login, create, search, purchase, export)
- System responses (validate, calculate, notify, persist)
- Business rules (pricing logic, access control, workflow transitions)

Use a consistent format: "The system shall [action] when [condition] so that [benefit]."

### Step 2: Identify Non-Functional Requirements

Quantify quality attributes **only when the source material supports a bound or when you clearly label an assumption that still needs owner confirmation**:
- **Performance**: Workload, measurement boundary, percentile, and justified target
- **Security**: Actual exposure, data obligations, and required controls
- **Scalability/availability**: Expected demand, tolerated interruption, and recovery needs
- **Accessibility**: Applicable users, platforms, and required conformance scope

When the source gives a direction but not a number:
- Convert it into a bounded requirement only if the bound is explicitly sourced
- Otherwise record it as an **open question** or **assumption requiring review**
- Do **not** invent precise targets just to make the document look complete

### Step 3: Prioritize

Use MoSCoW (Must/Should/Could/Won't) or RICE (Reach x Impact x Confidence / Effort):
- **P0 (Must)**: Product is unusable without these
- **P1 (Should)**: Important but workarounds exist
- **P2 (Could)**: Nice to have, include if time permits
- **P3 (Won't)**: Explicitly out of scope for this iteration

### Step 4: Validate and Resolve Conflicts

- Review with stakeholders for completeness
- Check for contradictions between requirements
- Resolve material feasibility doubts with the responsible engineer
- Ensure traceability (each requirement links to a user need)
- Flag any requirement or NFR whose precision is assumption-driven rather than source-driven
- Preserve upstream non-goals and open questions from `problem-frame`, `design-direction`, or `intake-brief` instead of silently collapsing them into solution commitments

### Step 5: Document with Traceability

Each requirement should have: ID, description, priority, source (which user need), acceptance criteria reference, and status.

If a metric, SLA, or retention bound is not directly supported by the source material, include it only as:
- an explicitly labeled assumption, or
- an open question with a named owner

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] All P0/P1 requirements documented with clear acceptance criteria
- [ ] Non-functional requirements quantified where evidence exists; otherwise converted into explicit open questions or assumptions
- [ ] No unresolved contradictions between requirements
- [ ] Stakeholders have reviewed and signed off
- [ ] Requirements are traceable to user needs

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/01-specification/pc-requirements-engineering/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
