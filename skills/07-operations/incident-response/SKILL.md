---
name: incident-response
description: Use when a production incident occurs or when establishing incident management procedures
metadata:
  phase: 07-operations
  inputs:
  - monitoring-config
  - deployment-runbook
  - architecture-doc
  outputs:
  - incident-playbook
  - postmortem-report
  prerequisites:
  - monitoring-observability
  quality_gate: Incident playbook covers top 5 failure modes, postmortem template ready, on-call rotation defined
  roles:
  - devops-engineer
  - tech-lead
  methodologies:
  - all
  effort: medium
---

# Incident Response

> When production breaks, speed and clarity matter more than perfection. Mitigate first, root-cause later.

## Context

Incident response is the skill of managing production failures under pressure. It combines technical diagnosis with communication discipline. The goal is not to find the perfect fix immediately -- it's to stop the bleeding, then investigate properly.

## Process

### Step 1: Detect

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

### Step 3: Assemble Response Team

- **Incident Commander**: Owns coordination, not debugging
- **Technical Responder(s)**: Debug and fix
- **Communications Lead**: Updates stakeholders and users

### Step 4: Mitigate

Stop the bleeding. Acceptable mitigations:
- Rollback to last known good deployment
- Disable feature flag for broken feature
- Scale up to handle load
- Switch to backup/failover system
- Apply rate limiting to protect remaining capacity

Mitigation does NOT need to fix the root cause. It needs to reduce impact.

### Step 5: Resolve

Once mitigated, investigate root cause with less time pressure:
- Gather evidence (logs, metrics, traces from the incident window)
- Build timeline (what happened, in what order)
- Identify root cause (not just the symptom)
- Implement proper fix
- Deploy fix with extra monitoring

### Step 6: Postmortem (within 48 hours)

Blameless postmortem -- focus on systems, not people:
- Timeline of events
- Root cause analysis (5 Whys)
- What went well in the response
- What went poorly
- Action items with owners and deadlines

## Quality Gate

- [ ] Severity classification matrix documented
- [ ] Incident playbook covers top 5 known failure modes
- [ ] Postmortem template ready
- [ ] On-call rotation defined and tested
- [ ] Communication templates for stakeholder updates ready

## Anti-Patterns

1. **Blame culture** -- "Who broke it?" kills incident reporting. Focus on "what broke and why."
2. **Hero culture** -- One person always fixes everything. This is a single point of failure.
3. **Postmortem without action items** -- A postmortem that identifies problems but assigns no fixes will see the same incident again.
4. **Skipping postmortem for "small" incidents** -- Small incidents reveal systemic issues. Review them.

## Related Skills

- [monitoring-observability](../monitoring-observability/SKILL.md) -- provides the alerting that triggers response
- [runbooks](../runbooks/SKILL.md) -- provides step-by-step response procedures
- [retrospective](../../08-evolution/retrospective/SKILL.md) -- broader process improvement from incident patterns
