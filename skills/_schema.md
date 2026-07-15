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
- keep `description` at or under 280 characters where possible; 350 is the hard cap enforced by `scripts/validate_prodcraft.py`, because every installed skill's description shares one always-loaded discovery context budget
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
| metadata.outputs | Yes | Empty array `[]` for a new draft; define reviewed outputs before promotion |
| metadata.quality_gate | Yes | Must be verifiable |
| metadata.roles | Yes | At least one role |
| metadata.methodologies | Yes | Default to `["all"]` |
| metadata.prerequisites | Yes | Use empty array `[]` if no dependencies |
| metadata.effort | No | Default to "medium" |

## Draft Scaffolding

Create a new draft package with:

```bash
python scripts/new_skill.py <phase> <pc-skill-name>
```

The command is draft-only. It builds a candidate repository containing the new
`SKILL.md`, a `draft` manifest entry, and `eval/<phase>/<name>/evals/eval-strategy.md`.
The candidate repository must pass `scripts/validate_prodcraft.py` before the
command commits any source-repository change. A matching same-phase entry in
`planned_skills` is converted into the draft entry in the same transaction.
Validation failures, name collisions, concurrent manifest changes, and commit
failures leave the command-owned repository state byte-for-byte unchanged.
Cooperating scaffolder invocations are serialized with an advisory lock on the
repository root. Directory commits use atomic no-replace moves, and exception
rollback first moves each target into a transaction-private quarantine before
inspecting or deleting owned bytes. A replacement installed at the public path
during rollback is never unlinked. The manifest commit uses an atomic exchange
followed by checks of both the displaced bytes and the installed candidate. A
write displaced at the exchange boundary is restored; a write that replaces the
candidate after exchange is preserved and causes the transaction-owned
directories to roll back. The command fails closed when these primitives are
unavailable; supported hosts are local macOS and Linux filesystems that provide
the required locking and rename operations.

This is a local authoring transaction, not distributed locking. A process that
keeps an old manifest inode open and ignores path replacement can operate
outside this boundary. Do not run non-cooperating manifest writers concurrently
with the scaffolder. Exception rollback is tested; power loss, kernel failure,
and uncatchable process termination are not claimed as crash-durable rollback.

The scaffold deliberately starts with empty `inputs` and `outputs`. Do not
invent `artifact_flow` entries before those contracts are reviewed. The
following remain promotion-time review surfaces and are never modified by the
draft scaffolder:

- `manifest.yml` `artifact_flow`
- `schemas/distribution/public-skill-registry.json`
- `schemas/distribution/public-skill-portability.json`
- `rules/cross-cutting-matrix.yml`
- workflows and generated `skills/.curated` packages

Promotion requires explicit review of every applicable surface. The command
does not imply review, routing readiness, portability, or public distribution.

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

- Present user-facing outputs in the user's language, and record the choice as `user_presentation_locale` when the artifact carries language fields. Operator-level locale defaults belong in the host or repository instruction layer (for this repository: CLAUDE.md) and must never be hard-coded into exported skill bodies.
- Use plain language. Keep sentences short. Explain the point directly.
- When framing work, proposing a path, or reviewing direction, keep checking current system shape and collaboration quality if they affect scope, risk, sequencing, or handoff quality.

## Naming Conventions

- Directory names match the `name` field: `pc-api-design/SKILL.md` has `name: pc-api-design`
- Use the `pc-` prefix and verb-noun patterns when possible: `pc-spec-writing`, `pc-code-review`, `pc-risk-assessment`
- Avoid generic names: prefer `pc-data-modeling` over `pc-database`

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

- zero or one explicit `workflow_primary` in the `intake-brief`
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
