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

# Snapshot

Manual review snapshot of the skill under test.
