---
name: hotfix
description: Emergency production repair with compressed phases and uncompromised verification
cadence: immediate, hours
workflow_kind: overlay
composes_with: ["*"]
entry_skill: pc-intake
required_artifacts: [intake-brief]
best_for: [production-outage, active-security-incident, data-corruption, critical-regression]
phases_included: [04-implementation, 05-quality, 06-delivery, 07-operations, 08-evolution]
contract:
  version: workflow.v2
  overview:
    summary: Restore production safely through rapid intake, containment, focused diagnosis, a minimal fix, targeted verification, controlled deployment, and mandatory follow-up.
    distinctive: Hotfix compresses elapsed time and active phases, but keeps primary governance, independent review, rollback, and completion evidence.
  entry_gate:
    summary: Begin only after pc-intake records severity, impact, owner, primary workflow, fast-track rationale, and explicit approval.
    artifact: intake-brief
    approval_required: true
    fast_track_rule: Discovery and planning may be compressed only for an outage, active exploit, corruption, or critical business-flow failure; verification and rollback are never waived.
  phase_sequence:
    - id: triage-and-contain
      name: Triage and contain
      purpose: Confirm hotfix eligibility, assign ownership, reduce impact, preserve evidence, and choose rollback or forward-fix.
      skills: [pc-incident-response, pc-bug-history-retrieval, pc-documentation]
      inputs: [production symptoms, alerts, recent changes, affected-user reports]
      outputs: [severity decision, owner, containment state, evidence snapshot, rollback decision]
      duration: 15-30 minutes
    - id: diagnose
      name: Focused diagnosis
      purpose: Establish a falsifiable root cause and the narrowest safe correction after containment.
      skills: [pc-incident-response, pc-bug-history-retrieval, pc-systematic-debugging, pc-documentation]
      inputs: [preserved evidence, history, reproduction, logs and metrics]
      outputs: [root-cause statement, reproducer, fix boundary, identified risks]
      duration: 15 minutes to 2 hours
    - id: 04-implementation
      name: Surgical implementation
      purpose: Write the minimal correction and a regression test without unrelated refactoring or feature work.
      skills: [pc-systematic-debugging, pc-tdd, pc-feature-development]
      inputs: [root cause, reproducer, fix boundary, rollback path]
      outputs: [minimal patch, failing-then-passing regression test, implementation diff]
      duration: 30 minutes to 4 hours
    - id: 05-quality
      name: Targeted verification
      purpose: Verify the original failure, adjacent critical paths, security implications, and candidate completion claim.
      skills: [pc-testing-strategy, pc-code-review, pc-verification-before-completion, pc-security-audit]
      inputs: [patch, regression test, affected-path map, staging environment]
      outputs: [review decision, focused test evidence, staging verification, residual-risk record]
      duration: 30 minutes to 2 hours
    - id: 06-delivery
      name: Controlled production delivery
      purpose: Deploy progressively, observe defined health signals, and roll back immediately when abort thresholds trigger.
      skills: [pc-ci-cd, pc-deployment-strategy, pc-verification-before-completion, pc-documentation]
      inputs: [approved patch, deployment and rollback plan, health thresholds]
      outputs: [production deployment, health evidence, stakeholder update, completion decision]
      duration: 15-30 minutes plus stability window
    - id: 08-evolution
      name: Post-hotfix closure
      purpose: Complete postmortem, merge the correction to all affected lines, and schedule durable remediation.
      skills: [pc-retrospective, pc-tech-debt-management, pc-documentation]
      inputs: [incident timeline, deployment evidence, residual risks, temporary mitigations]
      outputs: [postmortem, follow-up owner and due date, merged branches, prevention actions]
      duration: within 24-48 hours
  quality_gates:
    - name: Fix approval
      after: 04-implementation
      criteria: [root cause identified, patch limited to fix boundary, regression test passes, relevant existing tests pass]
      approvers: [peer engineer]
      enforcement: blocking
    - name: Staging verification
      after: 05-quality
      criteria: [candidate deployed to production-like staging, original failure resolved, targeted adjacent checks show no unacceptable regression]
      approvers: [hotfix owner, reviewer]
      enforcement: blocking
    - name: Production stability
      after: 06-delivery
      criteria: [deployment verified, error and health signals within threshold, affected workflow checked, stakeholders notified]
      approvers: [hotfix owner, on-call engineer]
      enforcement: blocking
  overlay_delta:
    applies_to: [agile-sprint, spec-driven, iterative-waterfall, brownfield, greenfield]
    changes:
      - dimension: cadence
        effect: Compress routing and review targets to minutes or hours while retaining named owners and blocking evidence gates.
      - dimension: scope
        effect: Permit only the minimal production restoration patch; defer refactoring, optimization, and unrelated cleanup to follow-up work.
      - dimension: lifecycle
        effect: Focus active execution on containment, implementation, quality, delivery, and closure while preserving the approved primary workflow.
---

# Hotfix Workflow

## Adaptation Notes

- Active security incidents add evidence-preservation, disclosure, and trust-boundary review requirements.
- Data corruption requires backups, reconciliation, and a tested recovery path before destructive repair.
- If staging is unavailable, record that exception and use the safest canary or shadow verification available; do not silently omit the gate.
- Repeated hotfixes for one area trigger a separate root-cause and debt-remediation route.
