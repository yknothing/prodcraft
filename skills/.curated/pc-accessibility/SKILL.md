---
name: pc-accessibility
description: Use when a user interface, user-facing flow, or acceptance criteria need accessibility requirements, audits, or remediation guidance so the system stays usable for people with disabilities.
metadata:
  phase: cross-cutting
  inputs: []
  outputs:
  - accessibility-guidance
  prerequisites: []
  quality_gate: Accessibility requirements, checks, and remediation guidance are explicit enough for implementation and review
  roles:
  - developer
  - qa-engineer
  - tech-lead
  methodologies:
  - all
  effort: medium
  internal: false
  distribution_surface: curated
  source_path: skills/cross-cutting/pc-accessibility/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Accessibility

> Accessibility is not a polish pass. It is a product requirement that must survive design, implementation, and QA.

## Context

Use this skill when UI work, interaction design, content structure, or acceptance criteria need explicit accessibility treatment.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Identify the user-facing surface

List the screens, controls, content blocks, and interaction states affected by the change.

### Step 2: Define the accessibility contract

Specify the expected behavior for:

- keyboard access
- focus order and visible focus
- semantic structure and labels
- contrast and status communication
- error handling and announcements

### Step 3: Turn requirements into checks

Translate the contract into reviewable checks that implementation and QA can execute without guesswork.

### Step 4: Record the remediation path

If gaps already exist, document the minimum remediation sequence and who owns each part.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Affected UI surfaces are named explicitly
- [ ] Keyboard, semantics, feedback, and contrast expectations are documented
- [ ] Reviewers can verify the result without inventing extra rules

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/cross-cutting/pc-accessibility/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
