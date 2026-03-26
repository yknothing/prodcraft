# Workflow Schema

This document defines the required format for all workflow files in the `workflows/` directory.

## Frontmatter (YAML)

Every workflow file MUST begin with YAML frontmatter containing these fields:

```yaml
---
name: kebab-case-name           # Unique identifier, matches filename without extension
description: "Short sentence"   # What this workflow does, in quotes
cadence: "description"          # Timing pattern (e.g., "1-2 week sprints", "on-demand")
workflow_kind: "primary"        # "primary" or "overlay"
composes_with:                  # Which other workflows this one can layer with
  - "greenfield"
  - "brownfield"
  - "hotfix"
entry_skill: "intake"           # Mandatory lifecycle entry gate
required_artifacts:             # Artifacts that must exist before the workflow starts
  - "intake-brief"
best_for:                       # List of ideal use cases
  - "use-case-one"
  - "use-case-two"
phases_included:                # Which phases this workflow uses
  - "00-discovery"              # Use "all" shorthand or list specific phases
  - "04-implementation"
---
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Kebab-case identifier matching filename |
| `description` | string | yes | One-line summary of the workflow approach |
| `cadence` | string | yes | How time is structured in this workflow |
| `workflow_kind` | string | yes | `primary` governance workflow or `overlay` modifier |
| `composes_with` | list | yes | Names this workflow can legally layer with |
| `entry_skill` | string | yes | Must be `intake`; workflows begin only after intake approval |
| `required_artifacts` | list | yes | Must include `intake-brief` to enforce the hard gate |
| `best_for` | list | yes | Scenarios where this workflow excels |
| `phases_included` | list | yes | Phases used; `["all"]` means all 9 phases |

## Body Structure

### Entry Gate

Every workflow MUST start with an explicit entry gate section that:

- states that the workflow only begins after `intake` is completed and approved
- names the required artifact (`intake-brief`)
- explains any fast-track rule or phase skip in terms of intake-approved routing

This keeps the intake hard gate as a system rule, not a suggestion.

The `intake-brief` should record `workflow_primary` and `workflow_overlays[]`, not only a single workflow string.

### Overview

A 2-4 paragraph summary of the workflow philosophy, when to use it, and what makes it distinct from other workflows.

### Phase Sequence

For each included phase, describe:

- **Phase name and purpose** within this workflow's context
- **Skills applied** -- reference skills from `skills/` by name (e.g., "use `user-story-writing` and `requirements-gathering`")
- **Expected inputs** -- what artifacts or decisions feed into this phase
- **Expected outputs** -- what this phase produces
- **Typical duration** -- how long this phase takes in this workflow

### Quality Gates

Between each phase transition, define:

- **Gate name** -- a descriptive label for the checkpoint
- **Criteria** -- specific, verifiable conditions that must be met
- **Approvers** -- which personas or roles approve passage through the gate
- **Blocking vs advisory** -- whether the gate blocks progress or is informational

### Adaptation Notes

Guidance for tailoring the workflow to different contexts:

- Team size variations (solo, small team, large team)
- Domain-specific adjustments (B2B, B2C, internal tooling)
- Regulatory or compliance overlays
- Remote vs co-located considerations

## Key Principle: Workflows COMPOSE Skills

Workflows orchestrate existing skills from `skills/` -- they never duplicate skill content. A workflow says *when* and *in what order* to apply skills, not *how* to perform the skill itself.

Referenced skills should also declare methodology tags compatible with the workflow that uses them. If a workflow invokes a skill as a routed exception, that exception should be explicit in the skill's `metadata.methodologies` rather than left as an undocumented assumption.

**Do:** "During the specification phase, apply the `spec-writing` skill to produce the PRD."
**Don't:** Reproduce the full spec-writing process inline in the workflow file.

This keeps workflows lightweight and ensures skill improvements automatically benefit all workflows that reference them.
