---
name: pc-runbooks
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
    - pc-incident-response
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

Runbooks convert operational knowledge into executable procedures.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

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

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Trigger and intended owner are explicit
- [ ] Decision points and branch conditions are explicit
- [ ] Rollback or fail-closed path is included where applicable
- [ ] Recovery verification and communication steps are included
- [ ] Another responder could execute the procedure without improvising major steps
