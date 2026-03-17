---
name: spec-writing
description: Use when writing a detailed technical specification or product requirements document
metadata:
  phase: 01-specification
  inputs:
  - requirements-doc
  - domain-model
  outputs:
  - spec-doc
  prerequisites:
  - requirements-engineering
  quality_gate: Spec reviewed by engineering team, all open questions resolved
  roles:
  - product-manager
  - architect
  methodologies:
  - spec-driven
  - waterfall
  effort: large
---

# Spec Writing

> A good spec eliminates ambiguity. Engineers should be able to build from it without guessing.

## Context

Spec writing is the heaviest specification skill, used primarily in spec-driven and waterfall workflows. In agile workflows, this is replaced by lightweight user stories with acceptance criteria. The spec is the contract between product and engineering.

## Process

### Step 1: Structure the Document

Use a consistent template (see `templates/tdd-doc.md`):
1. **Overview** -- One paragraph explaining what this is and why it matters
2. **Goals** -- What success looks like (measurable)
3. **Non-Goals** -- Explicitly what this does NOT cover (prevents scope creep)
4. **Detailed Design** -- The meat: user flows, data models, API interfaces, edge cases
5. **Security Considerations** -- Threat vectors and mitigations
6. **Testing Strategy** -- How to verify this works
7. **Rollout Plan** -- How to ship safely
8. **Open Questions** -- Unresolved items (must be empty before implementation)

### Step 2: Write for Your Audience

Engineers are the primary readers. Be precise:
- Include data types and validation rules
- Specify error handling for each operation
- Define state transitions explicitly
- Use diagrams for complex flows (sequence diagrams, state machines)

### Step 3: Define Scope Boundaries

For every feature, explicitly state:
- What IS included in this spec
- What is NOT included (and where it will be addressed)
- What assumptions you're making (and how to validate them)

### Step 4: Review Cycle

- **Self-review**: Re-read after 24 hours with fresh eyes
- **Peer review**: Have another PM or architect review for completeness
- **Engineering review**: Have the implementing team review for feasibility and questions
- **Resolve all open questions** before approving for implementation

## Quality Gate

- [ ] All sections of the template completed
- [ ] Open Questions section is empty (all resolved)
- [ ] Engineering team has reviewed and has no blocking concerns
- [ ] Spec is versioned and accessible to all team members

## Anti-Patterns

1. **Spec that's actually a novel** -- If it's over 15 pages, split into smaller specs. No one reads a 50-page spec.
2. **Spec without non-goals** -- Without explicit non-goals, scope will expand invisibly.
3. **Spec as waterfall artifact** -- A spec should be a living document, updated as understanding evolves.
4. **Implementation details in spec** -- Spec defines WHAT, not HOW. Leave implementation decisions to the developer.

## Related Skills

- [requirements-engineering](../requirements-engineering/SKILL.md) -- provides the requirements to specify
- [domain-modeling](../domain-modeling/SKILL.md) -- provides domain model referenced in spec
- [system-design](../../02-architecture/system-design/SKILL.md) -- consumes spec for architecture decisions
- [task-breakdown](../../03-planning/task-breakdown/SKILL.md) -- breaks spec into implementable tasks
