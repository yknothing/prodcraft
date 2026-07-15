---
name: pc-spec-writing
description: Use when reviewed requirements need a shared product or technical specification that fixes scope, non-goals, interfaces, rollout concerns, and open questions before architecture or implementation. Skip for routine agile story refinement.
metadata:
  phase: 01-specification
  inputs:
  - requirements-doc
  - domain-model
  outputs:
  - spec-doc
  prerequisites:
  - pc-requirements-engineering
  quality_gate: Spec reviewed by engineering team, all open questions resolved
  roles:
  - product-manager
  - architect
  methodologies:
  - spec-driven
  - waterfall
  - greenfield
  - brownfield
  effort: large
  internal: false
  distribution_surface: curated
  source_path: skills/01-specification/pc-spec-writing/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Spec Writing

> A good spec eliminates ambiguity. Engineers should be able to build from it without guessing.

## Context

Spec writing is the heaviest specification skill, used primarily in spec-driven and waterfall workflows.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Structure the Document

Use a consistent template:
- product / feature scope documents: `templates/prd.md`
- technical design proposals: `templates/rfc.md`
1. **Overview** -- One paragraph explaining what this is and why it matters
2. **Goals** -- What success looks like (measurable)
3. **Non-Goals** -- Explicitly what this does NOT cover (prevents scope creep)
4. **Product and system contract** -- the user flows, domain rules, interfaces, rollout boundaries, and edge cases that downstream work must preserve
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

Precision does not mean implementation detail. Keep the spec at the contract layer:

- required behavior
- supported and unsupported flows
- release boundaries
- rollout and coexistence constraints
- unresolved questions that architecture must preserve

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

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] All sections of the template completed
- [ ] Open Questions section is empty (all resolved)
- [ ] Engineering team has reviewed and has no blocking concerns
- [ ] Spec is versioned and accessible to all team members

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/01-specification/pc-spec-writing/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
