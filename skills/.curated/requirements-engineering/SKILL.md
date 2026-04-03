---
name: requirements-engineering
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
  - intake
  quality_gate: Requirements doc reviewed by stakeholders, all P0/P1 requirements have acceptance criteria
  roles:
  - product-manager
  - tech-lead
  methodologies:
  - all
  effort: large
  internal: false
  distribution_surface: curated
  source_path: skills/01-specification/requirements-engineering/SKILL.md
  public_stability: beta
  public_readiness: core
---

# Requirements Engineering

> Transform user needs and business goals into precise, testable requirements.

## Context

Requirements engineering bridges discovery and design. It takes the "what users need" from discovery and turns it into "what the system must do" for architecture. Poor requirements are the #1 cause of project failure -- not because requirements are missing, but because they're ambiguous, contradictory, or incomplete.

This skill may start from more than one upstream shape:

- a discovery evidence set such as market research, personas, and feasibility findings
- a routed entry-stack handoff such as `problem-frame` and `design-direction`
- an `intake-brief` that records constraints, open questions, and the intended next step

Do not force every route through the same upstream artifact bundle. Start from the approved upstream direction that actually exists, then preserve its constraints faithfully.

## Inputs

- **design-direction** -- Preferred directional input when [problem-framing](../../00-discovery/problem-framing/SKILL.md) has already compared options and selected a path. Treat this as the strongest signal for what release or iteration direction should be converted into requirements.
- **problem-frame** -- Clarifies the problem statement, non-goals, assumptions, open questions, and language-boundary context that requirements must preserve rather than silently resolve.
- **intake-brief** -- Supplemental routing and scope context. Useful for preserving work type, urgency, methodology choice, handoff risks, and the upstream language boundary.
- **market-research-report** -- Market context, competitor gaps, or opportunity framing when the work is still anchored in discovery evidence.
- **user-persona-set** -- User goals, pain points, and behavior patterns that requirements should trace back to.
- **feasibility-report** -- Go/no-go and risk context. Use especially when viability, operational constraints, or timeline limits shape what can become a requirement.

Minimum expectation:

- either an approved `design-direction`, or
- a reviewed discovery evidence set that makes the problem and target user clear enough to write requirements without guessing

If neither exists, stop and route back upstream instead of inventing requirements from vague intent.

When upstream artifacts declare `source_language`, `artifact_record_language`, and `user_presentation_locale`, copy those fields forward instead of re-deciding them implicitly.

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
- Preserve upstream non-goals and open questions from `problem-frame`, `design-direction`, or `intake-brief` instead of silently collapsing them into solution commitments

### Step 5: Document with Traceability

Each requirement should have: ID, description, priority, source (which user need), acceptance criteria reference, and status.

If a metric, SLA, or retention bound is not directly supported by the source material, include it only as:
- an explicitly labeled assumption, or
- an open question with a named owner

## Outputs

- **requirements-doc** -- produced by this skill
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

- [problem-framing](../../00-discovery/problem-framing/SKILL.md) -- provides approved direction, non-goals, and open questions when the route is known but the solution direction was fuzzy
- [spec-writing](../spec-writing/SKILL.md) -- transforms requirements into detailed specification
- [domain-modeling](../domain-modeling/SKILL.md) -- runs in parallel to model the domain
- [acceptance-criteria](../acceptance-criteria/SKILL.md) -- creates testable criteria from requirements

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/01-specification/requirements-engineering/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `core`
