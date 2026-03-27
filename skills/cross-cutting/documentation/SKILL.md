---
name: documentation
description: Use when a feature, architecture decision, incident, or workflow change needs durable technical documentation such as tutorials, reference docs, ADRs, runbooks, or maintenance guidance instead of ad hoc notes.
metadata:
  phase: cross-cutting
  inputs: []
  outputs:
  - documentation-artifact
  prerequisites: []
  quality_gate: Documentation reviewed by target audience, published and discoverable
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

Documentation is a cross-cutting concern that applies at every lifecycle phase. Good documentation reduces onboarding time, prevents knowledge loss, and enables async collaboration. The Diataxis framework provides a useful structure.

In the phase matrix, `documentation` is always a `must_consider` concern. It only becomes a `must_produce` obligation when the change creates durable knowledge another person or later phase must rely on. Approved `intake_mode=fast-track` work may waive routine documentation updates, but it does not waive durable docs when the change would otherwise leave important knowledge implicit.

## Diataxis Framework

Organize documentation into four types:

| Type | Purpose | Oriented to |
|------|---------|-------------|
| **Tutorial** | Learning-oriented | Getting started, step-by-step |
| **How-to Guide** | Task-oriented | Solving specific problems |
| **Reference** | Information-oriented | Technical descriptions (API docs) |
| **Explanation** | Understanding-oriented | Background, context, decisions |

## Inputs

None required. This skill can begin from the project context alone.
## Process

### Step 1: Identify the Need

What documentation is needed? Common triggers:
- New feature shipped (how-to guide for users)
- Architecture decision made (ADR for future developers)
- Incident resolved (runbook to prevent recurrence)
- New team member joining (onboarding tutorial)

Before writing, classify the need explicitly:
- `must_consider` only: verify that no durable doc update is needed and record that decision in the surrounding artifact or handoff
- `must_produce`: create or update the durable doc because downstream work, operators, or users would otherwise lose context
- `skip_when_fast_track`: only use the waiver when the route is explicitly fast-tracked and the change does not create durable knowledge debt

### Step 2: Write for Your Audience

- **Developers**: Code examples, API reference, architecture docs
- **Operators**: Runbooks, deployment guides, monitoring dashboards
- **Users**: Tutorials, how-to guides, FAQs
- **Stakeholders**: Architecture Decision Records, design docs

### Step 3: Keep Docs Close to Code

- Use docs-as-code: Markdown in the repository, versioned alongside code
- Auto-generate API docs from code annotations (OpenAPI, JSDoc, docstrings)
- README.md in every significant directory explaining its purpose
- Architecture Decision Records in `docs/adr/`

### Step 4: Review and Maintain

- Documentation reviews as part of PR process (if docs were changed)
- Quarterly documentation audit: remove outdated content
- Track documentation debt alongside tech debt

## Outputs

- **documentation-artifact** -- produced by this skill
## Quality Gate

- [ ] Target audience can complete their task using only the documentation
- [ ] Documentation is discoverable (linked from README, searchable)
- [ ] Auto-generated docs are integrated into CI pipeline
- [ ] No outdated information (verified within last quarter)

## Anti-Patterns

1. **Write once, abandon forever** -- Outdated docs are worse than no docs. They mislead.
2. **Documentation dump** -- A 200-page doc no one reads. Keep it focused and findable.
3. **Separate documentation system** -- If docs aren't next to code, they won't be updated with code.
4. **No documentation at all** -- "The code is self-documenting" is only true for WHAT, never for WHY.

## Related Skills

This skill applies at every phase. Key integration points:
- [spec-writing](../../01-specification/spec-writing/SKILL.md) -- specification is documentation
- [system-design](../../02-architecture/system-design/SKILL.md) -- architecture docs
- [runbooks](../../07-operations/runbooks/SKILL.md) -- operational documentation
- [retrospective](../../08-evolution/retrospective/SKILL.md) -- process documentation
