---
name: pc-documentation
description: Use when a feature, architecture decision, incident, or workflow change needs durable technical documentation such as tutorials, reference docs, ADRs, runbooks, or maintenance guidance instead of ad hoc notes.
metadata:
  phase: cross-cutting
  inputs: []
  outputs:
  - documentation-artifact
  prerequisites: []
  quality_gate: Applicable documentation is current and discoverable at the authorized destination, or a justified no-update decision is recorded
  roles:
  - developer
  - tech-lead
  methodologies:
  - all
  effort: small
---

# Documentation

> Documentation is a product. Treat it with the same care as code: version it, review it, test it, maintain it.

## Context

Documentation is a cross-cutting concern that applies at every lifecycle phase.

See [context notes](references/context.md).

## Diataxis Framework

Organize documentation into four types:

| Type | Purpose | Oriented to |
|------|---------|-------------|
| **Tutorial** | Learning-oriented | Getting started, step-by-step |
| **How-to Guide** | Task-oriented | Solving specific problems |
| **Reference** | Information-oriented | Technical descriptions (API docs) |
| **Explanation** | Understanding-oriented | Background, context, decisions |

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Identify the Need

What documentation is needed? Common triggers:
- New feature shipped (how-to guide for users)
- Architecture decision made (ADR for future developers)
- Incident resolved (runbook to prevent recurrence)
- New team member joining (onboarding tutorial)

Read the current phase matrix and approved route. Evaluate conditional documentation triggers against the actual change. `must_consider` requires a decision; `must_produce` requires its output unless an authorized exception applies. Use `skip_when_fast_track` only when the route actually grants it.

When no durable knowledge changes and no output obligation remains, record why existing documentation suffices in the handoff and finish. Otherwise update the smallest authoritative page that its audience needs.

### Step 2: Write for Your Audience

- **Developers**: Code examples, API reference, architecture docs
- **Operators**: Runbooks, deployment guides, monitoring dashboards
- **Users**: Tutorials, how-to guides, FAQs
- **Stakeholders**: Architecture Decision Records, design docs

### Step 3: Keep Docs Close to Code

- Use the project's canonical documentation location and versioning conventions
- Generate reference material when an existing source of truth supports it; avoid duplicate hand-maintained copies
- Add entry links or directory guidance only where they help readers find required information
- Record architecture decisions in the established decision log

### Step 4: Review and Maintain

- Documentation reviews as part of PR process (if docs were changed)
- Recheck affected instructions when their source changes; choose periodic audits according to drift risk
- Track documentation debt alongside tech debt

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Need and route obligation are resolved; a no-update outcome has a reason
- [ ] Changed guidance supports the intended reader task, with prerequisites and limits explicit
- [ ] Updated documentation has a discoverable canonical location and current source references
- [ ] Relevant examples/links are checked; generated docs are checked in CI when generation is used
- [ ] Required review and publication authority match the delivery; local edits are not claimed as published

## Anti-Patterns

1. **Write once, abandon forever** -- Outdated docs are worse than no docs. They mislead.
2. **Documentation dump** -- A 200-page doc no one reads. Keep it focused and findable.
3. **Divergent copies** -- Keep one authoritative source and an update path, even when documentation lives in a separate system.
4. **No documentation at all** -- "The code is self-documenting" is only true for WHAT, never for WHY.
