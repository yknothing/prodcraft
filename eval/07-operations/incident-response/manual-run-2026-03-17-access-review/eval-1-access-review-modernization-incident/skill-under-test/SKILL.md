---
name: incident-response
description: Use when a live production issue needs coordinated containment, severity triage, stakeholder communication, and evidence capture, especially when a recent release, brownfield coexistence rules, rollback decisions, or unresolved contract boundaries must be handled before root-cause work.
metadata:
  phase: 07-operations
  inputs:
    - ci-cd-pipeline
    - architecture-doc
    - service-alerts
  outputs:
    - incident-playbook
    - incident-timeline
    - postmortem-report
  prerequisites:
    - ci-cd
  quality_gate: Incident plan defines severity, containment path, stakeholder communication cadence, evidence capture, and post-incident follow-up
  roles:
    - devops-engineer
    - tech-lead
    - developer
  methodologies:
    - all
  effort: medium
---

# Snapshot

Manual review snapshot of the skill under test.
