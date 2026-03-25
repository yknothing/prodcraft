---
name: runbooks
description: Use when an operational task or incident needs a concrete step-by-step procedure that another responder can execute safely, especially when rollback, fail-closed containment, coexistence fallback, communication cadence, or evidence capture must be explicit under pressure.
metadata:
  phase: 07-operations
  inputs:
    - incident-playbook
    - monitoring-config
    - ci-cd-pipeline
  outputs:
    - operational-runbook
    - escalation-checklist
  prerequisites:
    - incident-response
  quality_gate: Runbook contains trigger, decision points, execution steps, verification checks, rollback or fail-closed path, and communication guidance
  roles:
    - devops-engineer
    - tech-lead
  methodologies:
    - all
  effort: medium
---

# Runbooks

> A good runbook lets a competent responder do the right thing without improvising under stress.

## Context

Runbooks convert operational knowledge into executable procedures. They are not long theory documents. They are concise operational guides for situations where time, clarity, and safety matter more than perfect prose.

In a lifecycle-aware system, runbooks should encode the same release boundaries the team reviewed earlier. For brownfield systems, that often means explicit rollback, fail-closed behavior, and coexistence-safe fallback steps.

## Inputs

- **incident-playbook** -- produced by the preceding skill in the lifecycle
- **monitoring-config** -- produced by the preceding skill in the lifecycle
- **ci-cd-pipeline** -- produced by the preceding skill in the lifecycle
## Process

### Step 1: Define the Trigger and Owner

Specify:
- what alert or symptom activates the runbook
- who is expected to start it
- what severity range it applies to
- when to escalate instead of continuing solo

### Step 2: Capture Preconditions and Safety Boundaries

Before the first action, state:
- what must be true before executing the procedure
- which paths must be preserved
- what should fail closed if the system is unsafe
- whether rollback or fallback is preferred over partial manual repair
- where any referenced threshold, policy, or guard decision comes from

### Step 3: Write the Response Steps

Use numbered steps with:
- exact decision points
- commands, dashboards, or checks to use
- expected observations
- branch conditions for rollback, fallback, or escalation
- explicit source or value for any threshold like "communication threshold" or "expected recovery window"

Avoid prose that forces the reader to infer the next move.

### Step 4: Add Verification and Communication

A runbook must say:
- how to confirm the mitigation worked
- which metrics or logs prove recovery
- who gets updated and how often
- what evidence should be captured for post-incident follow-up

### Step 5: Keep the Runbook Executable

Validate that someone other than the author can follow it. Update the runbook after incidents, failed drills, or major release changes.

## Outputs

- **operational-runbook** -- produced by this skill
- **escalation-checklist** -- produced by this skill
## Quality Gate

- [ ] Trigger and intended owner are explicit
- [ ] Decision points and branch conditions are explicit
- [ ] Rollback or fail-closed path is included where applicable
- [ ] Recovery verification and communication steps are included
- [ ] Another responder could execute the procedure without improvising major steps

## Anti-Patterns

1. **Narrative instead of procedure** -- If every step has to be inferred, it is not a runbook.
2. **Author-only knowledge** -- A runbook that depends on tribal memory is already failing.
3. **No rollback or safe-stop branch** -- Procedures that assume the happy path are dangerous under pressure.
4. **Outdated environment details** -- Old commands and links are silent operational hazards.
5. **Missing communication checkpoints** -- Recovery can still fail if stakeholders do not know the current state.
6. **Magic thresholds** -- Saying "if the threshold is exceeded" without naming the threshold or policy source forces responders to guess.

## Related Skills

- [monitoring-observability](../monitoring-observability/SKILL.md) -- provides the signals that trigger runbooks
- [incident-response](../incident-response/SKILL.md) -- defines containment and command structure
- [retrospective](../../08-evolution/retrospective/SKILL.md) -- improves runbooks after incidents
