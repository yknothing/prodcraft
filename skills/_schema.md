# Skill Schema

This document defines the format and conventions for all Prodcraft skills.

## Frontmatter Specification

Every skill package must live at `skills/{phase}/{skill-name}/SKILL.md` and begin with YAML frontmatter:

```yaml
---
name: string           # kebab-case identifier, unique across all phases
description: string    # concise what + when guidance for Anthropic discovery
metadata:
  phase: string        # Phase directory name: "00-discovery" through "08-evolution" or "cross-cutting"
  inputs:              # Artifacts this skill requires (produced by upstream skills)
    - artifact-name    # Reference to an output from another skill
  outputs:             # Artifacts this skill produces (consumed by downstream skills)
    - artifact-name    # Becomes available to downstream skills
  prerequisites:       # Skills that should complete before this one
    - skill-name       # Reference to another skill's `name` field
  quality_gate: string # Measurable exit criterion -- must be verifiable
  roles:               # Personas best suited to execute this skill
    - persona-name     # Advisory perspective / collaboration lens, not a default runtime guarantee
  methodologies:       # Which workflow families or explicit workflows include this skill
    - all              # Options: "all", family tags like "spec-driven"/"agile"/"waterfall", or workflow names like "greenfield"
  effort: string       # Relative effort: "small" (<1h), "medium" (1-4h), "large" (4h-2d), "xlarge" (2d+)
---
```

Keep frontmatter limited to discovery metadata. Do not pack edge cases, troubleshooting rules, or workflow caveats into `description` or `metadata`; use a `## Gotchas` section or `references/gotchas.md` instead so the runtime-discovery surface stays concise.

Follow the runtime guidance shared across Anthropic, OpenAI, Cursor, and Trae:

- keep `description` focused on **when to use** the skill
- keep the main skill concise and move heavy material into supporting files
- preserve explicit approval points for risky or side-effectful actions
- add new guardrails only when they map to a real observed failure mode

## Required Frontmatter Fields

| Field | Required | Notes |
|-------|----------|-------|
| name | Yes | Must be unique, kebab-case |
| description | Yes | Must start with trigger condition |
| metadata.phase | Yes | Must match parent phase directory |
| metadata.inputs | Yes | Empty array `[]` for phase-entry skills |
| metadata.outputs | Yes | At least one output |
| metadata.quality_gate | Yes | Must be verifiable |
| metadata.roles | Yes | At least one role |
| metadata.methodologies | Yes | Default to `["all"]` |
| metadata.prerequisites | Yes | Use empty array `[]` if no dependencies |
| metadata.effort | No | Default to "medium" |

## Body Structure

After frontmatter, the skill body follows this structure:

```markdown
# Skill Name

> One-line purpose statement.

## Context

When and why this skill matters. What problems it solves. How it fits in the lifecycle.

## Inputs

Describe what this skill expects to receive and the quality bar for each input.

## Process

Step-by-step instructions. Use numbered lists for sequential steps, bullet lists for parallel activities.

### Step 1: [Action]
Detailed instructions...

### Step 2: [Action]
...

## Outputs

Describe what this skill produces, with quality criteria for each output.

## Quality Gate

Explicit, measurable criteria that must be met before this skill is considered complete.
Checklist format preferred:
- [ ] Criterion 1
- [ ] Criterion 2

## Anti-Patterns

Common mistakes and how to avoid them.

## Gotchas

Short, structured edge cases that commonly break the workflow despite the main process being correct.
Each `###` gotcha entry should include:
- `Trigger`
- `Failure mode`
- `What to do`
- `Escalate when`

## Examples

Concrete examples demonstrating the skill in practice.

## Related Skills

- [prerequisite-skill](../phase/prerequisite-skill/SKILL.md) -- what it provides
- [downstream-skill](../phase/downstream-skill/SKILL.md) -- what it consumes from this skill
```

For larger skills, move the `## Gotchas` content into `references/gotchas.md` and link to it from `SKILL.md`. This keeps the core skill concise while still giving the model an explicit place to load edge-case handling.

## User-Facing Output Style

- User-facing outputs default to Chinese unless the user explicitly asks for another language.
- Use plain language. Keep sentences short. Explain the point directly.
- When framing work, proposing a path, or reviewing direction, keep checking current system shape and collaboration quality if they affect scope, risk, sequencing, or handoff quality.

## Naming Conventions

- Directory names match the `name` field: `api-design/SKILL.md` has `name: api-design`
- Use verb-noun patterns when possible: `spec-writing`, `code-review`, `risk-assessment`
- Avoid generic names: prefer `data-modeling` over `database`

## Artifact Naming

Artifacts (inputs/outputs) use a consistent naming scheme:

| Category | Examples |
|----------|----------|
| Framing | `intake-brief`, `problem-frame`, `options-brief`, `design-direction` |
| Documents | `requirements-doc`, `spec-doc`, `architecture-doc` |
| Diagrams | `component-diagram`, `sequence-diagram`, `er-diagram` |
| Code artifacts | `source-code`, `test-suite`, `migration-script` |
| Configurations | `ci-config`, `deploy-config`, `monitoring-config` |
| Decisions | `tech-decision-record`, `architecture-decision-record` |
| Reports | `review-report`, `audit-report`, `test-report` |
| Plans | `research-plan`, `sprint-plan`, `release-plan`, `capacity-plan` |

## Methodology Tagging

- `all` -- Included in every workflow
- `spec-driven` -- Only in specification-driven workflows (heavier documentation)
- `agile` -- Only in agile workflows (lighter, iterative)
- `waterfall` -- Only in waterfall-style workflows (phase-gated)
- Explicit workflow names such as `greenfield`, `brownfield`, or `hotfix` -- Use when a skill belongs only to that routed workflow and not to the full methodology family

Skills tagged `all` are the core skills that every methodology needs. Skills tagged with methodology-family values provide additional rigor appropriate to that family. Explicit workflow tags are for routed exceptions that should be validated against workflow references.

Workflow routing now records:

- one `workflow_primary`
- zero or more `workflow_overlays`

Do not collapse that composition back into a single workflow string in new artifacts or templates.

## Quality Gate Guidelines

Good quality gates are:
- **Measurable**: "All tests pass" not "Code is well tested"
- **Verifiable**: Can be checked by automation or a reviewer
- **Binary**: Pass or fail, no ambiguity
- **Scoped**: Relevant to this skill's outputs only

Bad quality gates:
- "Code is clean" (subjective)
- "Everything works" (unmeasurable)
- "No bugs" (unverifiable)

## Gotchas vs Anti-Patterns

- **Anti-Patterns** capture broad bad habits or poor discipline.
- **Gotchas** capture narrow but recurring failure modes triggered by ambiguous inputs, authority conflicts, missing artifacts, or operational edge cases.

Use `Gotchas` when the model needs a recovery rule for a realistic trap, not just a warning that a general practice is bad.
