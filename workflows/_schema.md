# Workflow Schema

This document defines the canonical `workflow.v2` format for files in `workflows/`.

Workflow semantics live in structured YAML frontmatter. The Markdown body contains only short adaptation guidance. This removes prose-parser ambiguity while keeping the lifecycle route, skills, artifacts, gates, approvals, and overlay effects independently verifiable.

## Canonical Shape

```yaml
---
name: example-workflow
description: Short one-line purpose
cadence: on demand
workflow_kind: primary
composes_with: [greenfield, brownfield]
entry_skill: pc-intake
required_artifacts: [intake-brief]
best_for: [example-context]
phases_included: [04-implementation]
contract:
  version: workflow.v2
  overview:
    summary: What the workflow accomplishes.
    distinctive: How its governance differs from other workflows.
  entry_gate:
    summary: Start only after intake approval.
    artifact: intake-brief
    approval_required: true
    fast_track_rule: Only the approved intake route may shorten the sequence.
  phase_sequence:
    - id: 04-implementation
      name: Implementation
      purpose: Build the approved slice.
      skills: [pc-tdd, pc-feature-development]
      inputs: [approved task slice]
      outputs: [tested implementation]
      duration: one iteration
  quality_gates:
    - name: Implementation complete
      after: 04-implementation
      criteria: [focused tests pass, peer review approved]
      approvers: [tech lead]
      enforcement: blocking
---

# Example Workflow

## Adaptation Notes

- Keep only context-specific tailoring here.
```

## Top-Level Fields

| Field | Type | Contract |
|-------|------|----------|
| `name` | string | Kebab-case identifier; matches the workflow filename. |
| `description` | string | One-line statement of when and why to use the workflow. |
| `cadence` | string | Timing pattern. |
| `workflow_kind` | string | `primary` or `overlay`. |
| `composes_with` | list | Workflows this route may layer with. |
| `entry_skill` | string | Must be `pc-intake`. |
| `required_artifacts` | list | Must include `intake-brief`. |
| `best_for` | list | Contexts where the workflow is appropriate. |
| `phases_included` | list | Lifecycle phases used, or `[all]`. |
| `contract` | mapping | Required machine-readable `workflow.v2` semantics. |

## Structured Semantics

### Overview

`contract.overview` replaces the narrative `## Overview` section:

- `summary` states the workflow outcome and philosophy.
- `distinctive` states how the workflow differs from nearby choices.

### Entry Gate

`contract.entry_gate` replaces the narrative `## Entry Gate` section:

- `artifact` must be `intake-brief` and must also appear in `required_artifacts`.
- `approval_required` must be `true`.
- `summary` states the approval boundary.
- `fast_track_rule` explains how intake may shorten the route without silently waiving governance.

### Phase Sequence

`contract.phase_sequence` replaces the narrative `## Phase Sequence` section. It must contain at least one phase. Every phase requires:

- unique `id` and non-empty `name`;
- `purpose` and `duration`;
- one or more canonical `pc-*` skill names;
- one or more explicit `inputs` and `outputs`.

The sequence composes skills; it must not reproduce skill instructions. Structured skill references are the only workflow dependency surface checked against the manifest and skill methodology tags.

### Quality Gates

`contract.quality_gates` replaces the narrative `## Quality Gates` section. It must contain at least one gate. Every gate requires:

- unique `name`;
- `after`, naming the transition or event being governed;
- one or more falsifiable `criteria`;
- one or more accountable `approvers`;
- `enforcement`, either `blocking` or `advisory`.

### Overlay Delta

Every overlay must define `contract.overlay_delta`; primary workflows must not define it.

```yaml
overlay_delta:
  applies_to: [agile-sprint, spec-driven, iterative-waterfall]
  changes:
    - dimension: delivery
      effect: Describe the exact change to primary governance.
```

Each change requires a non-empty `dimension` and `effect`. An overlay changes assumptions, phase emphasis, cadence, or evidence requirements; it does not replace the selected primary workflow.

## Markdown Body

The body must contain exactly one H2 section: `## Adaptation Notes`. It must include non-empty guidance for team size, domain, regulatory, operating-model, or other context-specific tailoring.

Do not retain empty `Entry Gate`, `Overview`, `Phase Sequence`, or `Quality Gates` headings. Those headings are not compatibility placeholders; their semantics moved to `contract`.

## Validation

`tools/workflow_contract.py` is the shared loader and semantic validator. `scripts/validate_prodcraft.py` uses it for repository checks and reads skill dependencies from `contract.phase_sequence[].skills`.

Validation fails independently when any required phase, skill list, gate, artifact binding, approver list, or overlay delta is missing. Run:

```bash
python3 -m unittest tests.test_workflow_composability
python3 scripts/validate_prodcraft.py \
  --check workflow-frontmatter \
  --check workflow-entry-gate \
  --check workflow-skill-refs
```

## Key Principle

Workflows compose existing skills. They define when skills run, which artifacts cross boundaries, and what evidence authorizes progression. Skill files remain the source of truth for how to perform the work.
