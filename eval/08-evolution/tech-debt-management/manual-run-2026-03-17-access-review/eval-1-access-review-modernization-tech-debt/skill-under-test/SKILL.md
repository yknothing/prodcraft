---
name: tech-debt-management
description: Use when repeated findings from reviews, incidents, retrospectives, or delivery friction need to be turned into a prioritized technical-debt registry and remediation plan, especially when brownfield seams, release-boundary gaps, or operational workarounds are accruing real engineering cost.
metadata:
  phase: 08-evolution
  inputs:
    - review-report
    - retrospective-report
    - postmortem-report
  outputs:
    - tech-debt-registry
    - remediation-plan
  prerequisites:
    - retrospective
  quality_gate: Debt registry is prioritized by impact and recurrence risk, top items have owners and routes, and capacity is allocated for remediation
  roles:
    - tech-lead
    - developer
    - architect
  methodologies:
    - all
  effort: medium
---

# Snapshot

Manual review snapshot of the skill under test.
