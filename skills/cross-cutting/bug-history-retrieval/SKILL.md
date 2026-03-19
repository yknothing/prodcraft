---
name: bug-history-retrieval
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

Use it when the current problem may already have a known lineage in:

- an internal bug tracker
- incident or postmortem records
- error monitoring systems
- release notes and deployment records
- git history, including fix, revert, and follow-up commits

This skill does **not** replace debugging. It provides historical context that makes downstream debugging, incident response, or planning more accurate.

Prefer direct access to the canonical system through available tools, MCP integrations, or approved internal APIs. Do not duplicate authoritative bug records into local docs unless another skill explicitly asks for a durable summary.

## Inputs

Bring the strongest current signal you have. Typical starting points:

- error message, exception class, or stack fragment
- incident symptom and affected user flow
- service, component, or subsystem name
- regression window or release identifier
- suspicious commit, rollback, or feature flag

If none of these exist, do not force historical retrieval. Route back to direct debugging or intake instead.

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
- invoke `incident-response` because the symptom matches a previously operationalized incident pattern
- invoke `tech-debt-management` or `retrospective` because the same class of failure keeps recurring

## Outputs

- **historical-defect-context** -- Ranked candidate matches from canonical systems, with evidence and confidence
- **fix-lineage-brief** -- Linked versions, commits, reverts, workarounds, and the most defensible next action

## Quality Gate

- [ ] Search terms are grounded in current failure signals rather than generic labels
- [ ] At least one canonical source was queried when available
- [ ] Candidate matches are separated into probable match, useful analog, or noise
- [ ] Fix lineage includes version or commit history when the source provides it
- [ ] The output ends with an explicit next action instead of "investigate more"

## Anti-Patterns

1. **Local wiki first** -- Starting from copied notes or stale summaries when a live bug system exists.
2. **Keyword cosplay** -- Declaring a match because two tickets share one noun.
3. **Closed means solved** -- Assuming a closed bug is fixed in the currently affected release or branch.
4. **History as authority** -- Letting an old workaround override the current workflow, approval path, or safety boundary.
5. **Corpus hoarding** -- Copying tracker contents into a parallel knowledge base just to make retrieval easier.

## Reference Material

For retrieval edge cases that commonly create false matches or stale conclusions, see [Gotchas](references/gotchas.md).

## Related Skills

- [incident-response](../../07-operations/incident-response/SKILL.md) -- use when the current issue is live and requires containment, coordination, and evidence capture
- [documentation](../documentation/SKILL.md) -- use when the retrieved history needs a durable summary, runbook update, or postmortem addendum
- [retrospective](../../08-evolution/retrospective/SKILL.md) -- uses repeated bug patterns to produce owned improvements
- [tech-debt-management](../../08-evolution/tech-debt-management/SKILL.md) -- turns recurring defect classes into prioritized remediation work
