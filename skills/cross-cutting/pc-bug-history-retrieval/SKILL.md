---
name: pc-bug-history-retrieval
description: Use when a current bug, incident, regression, or recurring symptom may match a known internal defect and the agent needs canonical evidence from issue trackers, incident systems, error monitoring, or git history before choosing a fix or next debugging step.
metadata:
  phase: cross-cutting
  inputs: []
  outputs:
  - historical-defect-context
  - fix-lineage-brief
  prerequisites: []
  quality_gate: Candidate matches are tied to canonical records, affected versions or commits, confidence, and an explicit next action instead of vague similarity claims
  roles:
  - developer
  - qa-engineer
  - tech-lead
  - devops-engineer
  methodologies:
  - all
  effort: small
---

# Bug History Retrieval

> Search canonical defect history before improvising a new theory when the current failure may already be known.

## Context

This skill exists to keep bug investigation grounded in **source-of-truth systems** rather than in memory, copied notes, or a shadow knowledge base.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

Review [Gotchas](references/gotchas.md) before accepting a historical match.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Form a Precise Retrieval Question

Before querying any system, write down:

- what is failing now
- which boundary is affected
- the strongest search terms available
- whether you are looking for an exact match, a likely analog, or a release-specific regression

Do not search for "auth bug" or "outage." Search for concrete signals such as:

- exception name
- endpoint or job name
- error code
- queue, tenant, or workflow label
- release or deploy range

### Step 2: Query Canonical Systems First

Search in this order when available:

1. **Internal defect or issue tracker** -- bug records, incident tickets, linked postmortems
2. **Error monitoring and incident systems** -- grouped exceptions, alert history, incident timelines
3. **Version and release history** -- deployment boundaries, rollback notes, release annotations
4. **Git history** -- fix commits, reverts, related PRs, blame on high-signal files

Use MCP or approved internal integrations when available. If the environment exposes a tool for Jira, Linear, Sentry, GitHub, or an internal tracker, prefer that over copy-pasted exports.

If a system returns too many matches, narrow by:

- service or component
- date window
- environment
- release version
- status such as open, fixed, regressed, reverted

### Step 3: Rank Matches by Evidence, Not Vibes

Treat a result as a strong candidate only when one or more of these align:

- same error signature or code path
- same user-visible symptom
- same component boundary
- same release window or regression range
- same fix or rollback pattern

Separate results into:

- **probable match** -- strong evidence that this is the same or directly related defect
- **useful analog** -- not the same bug, but historically similar enough to guide investigation
- **noise** -- keyword overlap without operational relevance

### Step 4: Extract Fix Lineage

For every probable match, capture:

- canonical record ID and title
- current status
- affected versions, environments, or tenants
- linked fix commit, revert, or follow-up PR if available
- workaround or containment used previously
- why the previous fix may or may not apply now

Do not stop at "found a similar ticket." The value is in the lineage: what changed, what shipped, what regressed, and what remains open.

### Step 5: Produce a Minimal Evidence Brief

Return a `historical-defect-context` and `fix-lineage-brief` that include:

- top matches with confidence
- exact evidence supporting the match
- open uncertainty
- the recommended next move

Recommended next moves usually look like:

- continue with direct debugging using the matched fix path as hypothesis
- verify whether a known fix is absent from the current branch or release
- invoke `pc-incident-response` because the symptom matches a previously operationalized incident pattern
- invoke `pc-tech-debt-management` or `pc-retrospective` because the same class of failure keeps recurring

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Search terms are grounded in current failure signals rather than generic labels
- [ ] At least one canonical source was queried when available
- [ ] Candidate matches are separated into probable match, useful analog, or noise
- [ ] Fix lineage includes version or commit history when the source provides it
- [ ] The output ends with an explicit next action instead of "investigate more"
