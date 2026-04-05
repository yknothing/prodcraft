# Acceptance Criteria to Testing Strategy Handoff Review

## Goal

Verify that `acceptance-criteria` produces a behavior-level criteria set that is genuinely useful for downstream `testing-strategy`.

## Scenario

- `access-review-modernization-acceptance-criteria`

This is a brownfield release-1 slice where:

- unsupported reassignment variants must fail explicitly
- sync semantics remain unresolved and must not be silently converted into guarantees
- evidence export and audit integrity remain part of the release boundary

## Artifacts Reviewed

- reviewed input context:
  - `fixtures/access-review-modernization-requirements.md`
  - `fixtures/access-review-modernization-spec-summary.md`

## Review Findings

## 1. The handoff is real and distinct from specification writing

The reviewed inputs already say what release 1 should do. What they do not yet provide is a testable contract that downstream verification can use directly.

That missing layer is exactly what `acceptance-criteria` should fill.

## 2. The downstream boundary is `testing-strategy`, not implementation detail

A correct criteria set should give `testing-strategy` enough clarity to decide:

- which behaviors belong in contract coverage
- which negative paths belong in integration or end-to-end checks
- which unresolved behaviors must remain explicit as test constraints rather than hidden assumptions

The criteria should not choose libraries, schemas, or rollout mechanics.

## 3. Brownfield constraints must stay behaviorally visible

For this slice, a useful criteria handoff must keep these boundaries explicit:

- unsupported release-1 reassignment variants fail with the documented error
- coexistence does not imply immediate legacy synchronization
- evidence export remains available for legacy-held historical campaigns

If those boundaries disappear, downstream testing becomes generic and misses the real release risk.

## Assertion Review

| Assertion | Review result | Notes |
|---|---|---|
| behavior-is-testable | pass | The downstream consumer needs concrete observable behavior, not prose. |
| unsupported-and-error-paths-explicit | pass | This slice is unsafe if unsupported flows are left vague. |
| unresolved-behavior-stays-visible | pass | Sync semantics must remain a constraint, not a silent pass. |
| boundary-with-implementation-preserved | pass | The handoff should stay at behavior level. |
| testing-strategy-can-consume-directly | pass | The criteria set should translate cleanly into layer decisions and test cases. |

## Conclusion

This routed handoff review is enough to support a narrow `tested` posture once a clean isolated benchmark result also exists.
