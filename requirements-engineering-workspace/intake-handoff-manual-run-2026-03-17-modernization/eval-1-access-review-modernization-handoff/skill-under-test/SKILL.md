---
name: requirements-engineering
description: Use when the work is still at the “what should we build” stage rather than design or implementation. Apply before spec-writing, architecture, API design, planning, or coding when interviews, personas, stakeholder notes, or discovery artifacts must be turned into prioritized functional requirements, non-functional requirements, scope boundaries, traceable sources, and explicit “the system shall” statements; not for acceptance criteria, PRD drafting from an approved requirements doc, spec review, or implementation.
metadata:
  phase: 01-specification
  inputs:
  - market-research-report
  - user-persona-set
  - feasibility-report
  outputs:
  - requirements-doc
  prerequisites:
  - feasibility-study
  quality_gate: Requirements doc reviewed by stakeholders, all P0/P1 requirements have acceptance criteria
  roles:
  - product-manager
  - tech-lead
  methodologies:
  - all
  effort: large
---

# Requirements Engineering

> Transform user needs and business goals into precise, testable requirements.

## Context

Requirements engineering bridges discovery and design. It takes the "what users need" from discovery and turns it into "what the system must do" for architecture. Poor requirements are the #1 cause of project failure -- not because requirements are missing, but because they're ambiguous, contradictory, or incomplete.

## Process

### Step 1: Gather Functional Requirements

For each user persona and journey, identify what the system must do:
- User actions (login, create, search, purchase, export)
- System responses (validate, calculate, notify, persist)
- Business rules (pricing logic, access control, workflow transitions)

Use a consistent format: "The system shall [action] when [condition] so that [benefit]."

### Step 2: Identify Non-Functional Requirements

Quantify quality attributes **only when the source material supports a bound or when you clearly label an assumption that still needs owner confirmation**:
- **Performance**: Response time < 200ms p95, support 1000 concurrent users
- **Security**: OWASP Top 10 compliance, SOC2 Type II, data encryption at rest
- **Scalability**: Handle 10x growth without architecture changes
- **Availability**: 99.9% uptime (8.7 hours downtime/year)
- **Accessibility**: WCAG 2.1 AA compliance

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
- Verify technical feasibility with architect
- Ensure traceability (each requirement links to a user need)
- Flag any requirement or NFR whose precision is assumption-driven rather than source-driven

### Step 5: Document with Traceability

Each requirement should have: ID, description, priority, source (which user need), acceptance criteria reference, and status.

If a metric, SLA, or retention bound is not directly supported by the source material, include it only as:
- an explicitly labeled assumption, or
- an open question with a named owner

## Quality Gate

- [ ] All P0/P1 requirements documented with clear acceptance criteria
- [ ] Non-functional requirements quantified where evidence exists; otherwise converted into explicit open questions or assumptions
- [ ] No unresolved contradictions between requirements
- [ ] Stakeholders have reviewed and signed off
- [ ] Requirements are traceable to user needs

## Anti-Patterns

1. **Solution masquerading as requirement** -- "Use Redis for caching" is a solution, not a requirement. The requirement is "cache frequently accessed data to achieve < 50ms read latency."
2. **Vague requirements** -- "The system should be fast" is untestable. Quantify everything.
3. **Invented precision** -- Turning "must remain responsive" into "p99 < 800ms" without a source or approved assumption creates false certainty. Mark unknown bounds as open questions.
4. **Requirements by committee** -- Too many stakeholders without a single owner leads to bloat. One person owns the requirements doc.
5. **Scope creep via "just one more"** -- Each new requirement has a cost. Evaluate against the backlog, don't just add.

## Related Skills

- [spec-writing](../spec-writing/SKILL.md) -- transforms requirements into detailed specification
- [domain-modeling](../domain-modeling/SKILL.md) -- runs in parallel to model the domain
- [acceptance-criteria](../acceptance-criteria/SKILL.md) -- creates testable criteria from requirements
