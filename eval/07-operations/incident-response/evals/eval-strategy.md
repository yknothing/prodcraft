# Incident Response Evaluation Strategy

## Objective

Evaluate whether `incident-response` improves a routed production-incident handoff over baseline reasoning.

At review stage, use manual side-by-side evaluation instead of auto-trigger scoring. This skill is expected to be a routed operations skill, not a discoverability-first skill.

A "non-brownfield comparison scenario" means an incident that does not depend on legacy coexistence, migration seams, or compatibility burden. It is used to verify that the skill still improves containment and coordination in a more ordinary production failure.

## Review Scope

Review the skill on:

1. `access-review-modernization-incident`
   - brownfield modernization release
   - unsupported reassignment variants should fail closed
   - legacy coexistence and rollback still matter
   - a post-release production incident now exists
2. `team-invite-email-backlog-incident`
   - non-brownfield service incident
   - no legacy coexistence or migration seam exists
   - email delay and queue recovery still require clear containment and communication

## Assertions

1. `maps response to live failure mode`
   - The plan ties containment to the actual failing boundary, not just generic outage playbooks.
2. `preserves brownfield safety`
   - Coexistence, rollback, and data-integrity constraints stay explicit.
3. `mitigates before root-cause guessing`
   - The response prioritizes containment and evidence capture before broad redesign or speculative fixes.
4. `uses explicit command and communication`
   - Severity, roles, cadence, and stakeholder updates are concrete.
5. `prepares post-incident handoff`
   - The result gives clean input to runbooks, retrospective, or follow-up delivery work.

## Inputs

- `fixtures/access-review-modernization-pipeline-summary.md`
- `fixtures/access-review-modernization-architecture-summary.md`
- `fixtures/access-review-modernization-incident-alert.md`
- `fixtures/team-invite-service-summary.md`
- `fixtures/team-invite-incident-alert.md`

## Method

1. Produce a baseline incident plan without the skill.
2. Produce a second response while explicitly using `incident-response`.
3. Compare both outputs against the assertion list.
4. Record findings in `incident-review.md` and summarize status in `findings.md`.

## Exit Criteria for Review Stage

- At least one routed brownfield scenario reviewed
- At least one routed non-brownfield comparison scenario reviewed
- Clear manual evidence that the skill improves containment discipline and handoff quality
- No claim of tested or production status until isolated benchmark coverage exists
