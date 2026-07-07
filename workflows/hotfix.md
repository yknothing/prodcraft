---
name: hotfix
description: "Emergency path for critical production issues"
cadence: "on-demand, hours to 1 day"
workflow_kind: "overlay"
composes_with: ["*"]
entry_skill: "intake"
required_artifacts: ["intake-brief"]
best_for: ["production-incidents", "security-vulnerabilities", "data-corruption"]
phases_included: ["07-operations", "04-implementation", "05-quality", "06-delivery"]
---

# Hotfix Workflow

## Overview

The hotfix workflow is a compressed, emergency path for resolving critical production issues. It intentionally skips discovery, specification, architecture, and planning phases -- relying on the existing system's documentation and the team's domain knowledge to move directly to fix, verify, and deploy.

Speed is the priority, but not at the expense of safety. Every hotfix still requires code review, testing, and a deliberate deployment. The difference is that these steps are accelerated, not eliminated.

This workflow activates when production is degraded or at risk: service outages, security vulnerabilities being actively exploited, data corruption, or critical business process failures. If it can wait until the next sprint, it is not a hotfix.

Hotfix is an overlay. It compresses the normal route around urgency while preserving a primary governance workflow and any relevant system-state overlay such as `brownfield`.

## Entry Gate

Even emergency work must start with `intake`. In hotfix cases, intake is intentionally short, but it still must produce and approve an `intake-brief` that records severity, workflow choice, owner, and fast-track rationale before the team enters the compressed implementation path.

## Entry Criteria

Before entering the hotfix workflow, confirm at least one of:

- **Service outage:** Users cannot complete a core workflow.
- **Security vulnerability:** Active exploitation or imminent risk of exploitation.
- **Data corruption:** Data integrity is compromised or at risk.
- **Regulatory breach:** The system is violating a compliance requirement.
- **Revenue impact:** Quantifiable financial loss per hour of inaction.

If none of these apply, use the standard workflow. Not everything urgent is a hotfix.

## Phase Sequence

### Triage (15-30 minutes)

**Purpose:** Understand the impact, confirm the hotfix path, assign ownership.

**Skills:** Apply `incident-response`, `bug-history-retrieval` when the failure may have lineage, and `documentation`.

**Actions:**
1. Assess severity: who is affected, how many, what is the business impact.
2. Determine if a hotfix is appropriate (vs. rollback, feature flag toggle, or config change).
3. Assign a hotfix owner -- one person who drives the fix to completion.
4. Communicate status to stakeholders: "We are aware, investigating, ETA to follow."

**Output:** Severity classification, hotfix owner assigned, stakeholder notification sent.

### Diagnosis (15 minutes - 2 hours)

**Purpose:** Identify the root cause with enough precision to fix it safely.

**Skills:** Apply `incident-response`, `bug-history-retrieval` when historical lineage may matter, `systematic-debugging` after containment, and `documentation`.

**Actions:**
1. Confirm the current containment path and whether user impact is still active.
2. Reproduce the issue or confirm it from production data.
3. Check for historical incident or regression lineage before inventing a new theory.
4. Identify the code path and root cause with enough evidence to justify the fix path.
5. Assess blast radius: what else could this change affect?

**Output:** Root cause identified, bug-fix-report drafted, proposed fix scoped, blast radius assessed.

**Key principle:** Contain user impact first. Once impact is contained, identify root cause before writing the code fix. If the permanent fix is too large for the hotfix window, ship the smallest safe workaround and log the follow-up debt explicitly.

### Phase 4: Implementation (30 minutes - 4 hours)

**Purpose:** Write the minimal, surgical fix.

**Skills:** Apply `systematic-debugging`, `tdd`, and `feature-development`.

**Actions:**
1. Create a hotfix branch from the production release tag or branch.
2. Confirm the bug-fix-report still matches the change being made.
3. Write the fix -- minimal code change only. No refactoring, no cleanup, no "while I'm here" changes.
4. Write a test that reproduces the original issue and verifies the fix.
5. Self-review the change: is it the smallest possible fix? Could it introduce new issues?

**Output:** Hotfix branch with fix and test.

**Rules for hotfix code:**
- Change as few lines as possible.
- Do not combine the fix with unrelated changes.
- If the fix is a workaround, add a clear comment explaining why and reference the follow-up ticket.
- If the proper fix would take more than 4 hours, apply the workaround now and create a follow-up ticket.

### Phase 5: Quality (30 minutes - 2 hours)

**Purpose:** Verify the fix resolves the issue without introducing regressions.

**Skills:** Apply `testing-strategy`, `code-review`, `verification-before-completion`, and `security-audit` when the hotfix addresses a vulnerability or trust-boundary failure.

**Actions:**
1. Run the automated test suite. All existing tests must pass.
2. Run the new test that verifies the fix.
3. Perform targeted exploratory testing around the affected area.
4. Deploy to staging and verify the fix in a production-like environment.
5. Peer review the code change -- this is required even for hotfixes. The review is fast-tracked but not skipped.

**Output:** Test results, staging verification, code review approval.

**Fast-track review process:**
- Reviewer is notified with "HOTFIX" priority.
- Review focuses on: correctness, blast radius, test coverage. Style and optimization concerns are deferred.
- Review target: 30 minutes from request to approval.
- If the primary reviewer is unavailable, any senior engineer can approve.

### Phase 6: Delivery (15-30 minutes)

**Purpose:** Deploy the fix to production with verification.

**Skills:** Apply `ci-cd`, `deployment-strategy`, `verification-before-completion`, and `documentation`.

**Actions:**
1. Deploy to production using the standard deployment pipeline (do not bypass it).
2. Verify the fix in production: check the specific issue, monitor error rates, check related functionality.
3. Communicate resolution to stakeholders: "Issue resolved, monitoring for stability."
4. Monitor closely for 1-2 hours after deployment.

**Output:** Production deployment verified, stakeholder notification sent, monitoring active.

**Rollback plan:** If the fix causes new issues, roll back immediately to the previous version. The rollback procedure should be determined before deployment begins.

## Post-Hotfix Requirements

The hotfix is not done when production is stable. The following must happen within 48 hours:

### Postmortem (within 48 hours)

**Skills:** Apply `retrospective` and `tech-debt-management`.

Conduct a blameless postmortem covering:
- Timeline: when detected, when triaged, when fixed, when deployed.
- Root cause: why did this happen? Use the 5 Whys technique.
- Detection: how was it found? Could we have found it sooner?
- Response: what went well? What was slow or confusing?
- Prevention: what changes would prevent this class of issue?

**Output:** Postmortem document (use the [postmortem template](../templates/postmortem.md)).

### Follow-Up Ticket (within 24 hours)

If the hotfix was a workaround or band-aid:
1. Create a ticket for the proper fix.
2. Include the root cause analysis.
3. Reference the hotfix commit and postmortem.
4. Prioritize in the next sprint.

### Merge Back (within 24 hours)

Ensure the hotfix is merged into the main development branch:
1. Cherry-pick or merge the hotfix into the main branch.
2. Resolve any conflicts.
3. Ensure CI passes on the main branch with the hotfix included.

## Quality Gates

### Fix Approval Gate

- **Criteria:** Root cause identified. Fix is minimal and surgical (no unrelated changes). Test reproducing the original issue is written and passing. All existing automated tests pass.
- **Approvers:** Peer engineer (fast-track review, 30-minute target).
- **Type:** BLOCKING -- no production deployment without code review approval.

### Staging Verification Gate

- **Criteria:** Fix deployed to staging. Issue verified resolved in production-like environment. No regressions observed in targeted exploratory testing.
- **Approvers:** Hotfix owner.
- **Type:** BLOCKING -- do not deploy to production without staging verification.

### Production Stability Gate

- **Criteria:** Production deployment verified. Error rates normal. Related functionality checked. Stakeholders notified of resolution.
- **Approvers:** Hotfix owner and on-call engineer.
- **Type:** BLOCKING -- incident is not closed until production stability is confirmed.

## Communication Protocol

| Time | Communication |
|------|--------------|
| Issue detected | Alert on-call engineer via paging system |
| Triage complete | Stakeholder update: impact, ETA, owner |
| Fix deployed | Stakeholder update: resolved, monitoring |
| +2 hours stable | All clear: incident closed |
| +48 hours | Postmortem shared with team |

## Adaptation Notes

- **Solo developer:** Skip the peer review only if the fix is a single-line change and you verify it in staging. For anything larger, find a reviewer even if they are not on your team.
- **Off-hours:** The hotfix owner has authority to deploy without waiting for business hours if the issue is severity 1. For severity 2, deploy during business hours unless impact is escalating.
- **Multiple hotfixes:** If a second hotfix is needed before the first postmortem is complete, that is a signal of a systemic issue. Escalate to the tech lead and schedule a deeper investigation.
- **Security vulnerabilities:** Follow the same process but restrict communication to the security team until the fix is deployed. Do not disclose the vulnerability in public channels until patched.
