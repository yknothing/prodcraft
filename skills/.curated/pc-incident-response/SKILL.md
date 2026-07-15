---
name: pc-incident-response
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
  - pc-ci-cd
  quality_gate: Incident plan defines severity, containment path, stakeholder communication cadence, evidence capture, and post-incident follow-up
  roles:
  - devops-engineer
  - tech-lead
  - developer
  methodologies:
  - all
  effort: medium
  internal: false
  distribution_surface: curated
  source_path: skills/07-operations/pc-incident-response/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Incident Response

> When production breaks, speed and clarity matter more than perfection. Mitigate first, root-cause later.

## Context

Incident response is the skill of managing production failures under pressure.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Confirm the Incident and Current Boundary

Capture the minimum facts needed to respond:
- which user-facing behavior is failing
- when the issue started relative to the last deploy
- whether the incident involves a known unsupported flow, coexistence seam, or rollout boundary
- which mitigation levers exist right now (rollback, route disable, traffic shaping, read-only mode, failover)

Automated alerting should catch most incidents before users report them. Key signals:
- Error rate spike (5xx responses > threshold)
- Latency increase (p95 > SLO)
- Resource exhaustion (CPU, memory, disk, connections)
- Business metric anomaly (orders dropping, signups stopping)

### Step 2: Triage -- Classify Severity

| Severity | Impact | Response Time | Example |
|----------|--------|---------------|---------|
| SEV1 | Service down, data loss, security breach | Immediate, all hands | Database corruption, complete outage |
| SEV2 | Major feature broken, significant user impact | < 30 min | Payment processing failing |
| SEV3 | Minor feature broken, workaround exists | < 4 hours | Search results incorrect |
| SEV4 | Cosmetic, no user impact | Next business day | UI misalignment |

Pick a severity based on current user impact, not on how scary the suspected root cause sounds.

### Step 3: Assemble Response Team and Communication Cadence

- **Incident Commander**: Owns coordination, not debugging
- **Technical Responder(s)**: Debug and fix
- **Communications Lead**: Updates stakeholders and users

Define:
- response channel and decision owner
- internal update cadence
- external/customer update trigger if needed

### Step 4: Mitigate First, Prefer Fail-Closed Containment

Stop the bleeding. Acceptable mitigations:
- Rollback to last known good deployment
- Disable feature flag for broken feature
- Scale up to handle load
- Switch to backup/failover system
- Apply rate limiting to protect remaining capacity
- Temporarily reject the unsafe or unsupported path explicitly instead of guessing at partial support
- Shift the affected flow to a safe fallback or read-only coexistence path

Mitigation does NOT need to fix the root cause. It needs to reduce impact.

For brownfield incidents, favor mitigations that preserve coexistence and data integrity over "keep everything available at any cost."

### Step 5: Investigate with Evidence, Not Guesses

Once mitigated, investigate root cause with less time pressure:
- Gather evidence (logs, metrics, traces from the incident window)
- Capture deploy ID, config deltas, and rollback decisions
- Build timeline (what happened, in what order)
- Identify root cause (not just the symptom)
- Compare observed behavior against the reviewed contract or release boundary
- Hand off code-level root-cause work to `pc-systematic-debugging` when the next step is a real code fix rather than an operational mitigation
- Implement the proper fix only after the root-cause path is evidenced
- Deploy fix with extra monitoring

Do not invent precision under pressure. If sync semantics, tenancy rules, or rollout intent remain uncertain, record them as open incident questions and keep the system in the safer mode.

### Step 6: Verify Recovery and Handoff Cleanly

Before declaring the incident resolved:
- confirm alerts and customer-visible symptoms have cleared
- confirm rollback, fail-closed behavior, or fallback path is still active as intended
- document any temporary guardrails that must remain until a permanent fix ships
- hand off the follow-up work to the right downstream skills (`pc-runbooks`, `pc-retrospective`, `pc-tech-debt-management`)

### Step 7: Postmortem (within 48 hours)

Blameless postmortem -- focus on systems, not people:
- Timeline of events
- Root cause analysis (5 Whys)
- What went well in the response
- What went poorly
- Action items with owners and deadlines

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Severity and current user impact are explicit
- [ ] Containment path and rollback or fail-closed decision are explicit
- [ ] Incident timeline and evidence sources are captured
- [ ] Stakeholder communication cadence and owner are explicit
- [ ] Post-incident follow-up actions and owners are defined

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/07-operations/pc-incident-response/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
