---
name: retrospective
description: Use after a sprint, release, or incident when evidence from execution needs to be converted into a small set of owned improvement actions, especially when brownfield failures, release-boundary misses, or repeated coordination problems must feed the next cycle.
metadata:
  phase: 08-evolution
  inputs:
    - incident-timeline
    - postmortem-report
    - review-report
  outputs:
    - retrospective-report
    - improvement-actions
  prerequisites: []
  quality_gate: Retrospective identifies a small set of system-level improvements, each with owner, deadline, and intake-ready follow-up
  roles:
    - tech-lead
    - product-manager
  methodologies:
    - all
  effort: small
---

# Snapshot

Manual review snapshot of the skill under test.
