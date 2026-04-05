# Runbooks Manual Benchmark Review

## Scope

This note summarizes the current manual branch-pair benchmark evidence for
`runbooks`.

It is not a true isolated runner-backed benchmark. It does preserve the minimum
comparison structure needed for a narrow `tested` decision:

- a baseline branch
- a with-skill branch
- fixed fixtures
- raw outputs checked into the repo

Reviewed manual branch pairs:

1. `access-review-modernization-runbook`
2. `team-invite-email-backlog-runbook`

## Cross-Branch Judgment

### Scenario 1: Brownfield fallback procedure

The baseline runbook is generic and not safely executable under pressure. It
acknowledges the alert and mentions rollback, but it does not define trigger,
containment branch, verification criteria, evidence capture, or communication
cadence precisely enough for another responder to follow without improvisation.

The with-skill runbook is materially stronger:

- trigger, severity range, and owner are explicit
- the safer containment branch is defined before generic investigation
- verification, evidence capture, and escalation conditions are concrete
- fallback and fail-closed behavior remain visible

### Scenario 2: Non-brownfield operational procedure

The second branch pair shows the same pattern in a lower-coexistence context:

- baseline drifts toward generic procedural prose
- with-skill preserves step-by-step execution shape, verification, and rollback

## Supporting Evidence

`runbooks` also has stronger-than-normal downstream evidence for this maturity
level:

- routed handoff review in `runbook-review.md`
- an independent execution drill artifact

The external execution protocol still needs a cleaner recorded pass, so this
should be treated as a narrow `tested` posture rather than a final operations
gold standard.

## Status Recommendation

- Recommended status: `tested`

Keep the tested posture narrow until:

1. one responder other than the author executes the runbook cleanly with only
   minor clarification edits
2. a true isolated runner-backed benchmark replaces this manual branch-pair
   evidence
