# Sprint Planning QA Findings

## Status

- Current status: `tested`
- Evidence type: routed handoff review plus isolated benchmark
- Scope covered:
  - one brownfield estimation-and-risk to sprint-plan scenario
  - explicit handoff from sized tasks into a bounded sprint commitment
  - one isolated benchmark run comparing baseline vs explicit skill invocation

## What Improved

- `sprint-planning` is no longer only a declared planning skill. It now has manifest-backed tested evidence.
- The repository now has a concrete example of when planning should become a capacity-constrained sprint commitment instead of continuing as a generic task list.
- The review packet makes the boundary explicit: estimation sizes the work, risk assessment challenges the plan, and sprint planning decides what actually fits now.
- The isolated benchmark shows the skill improves the core planning behavior that matters most here: keeping committed scope inside real capacity instead of rationalizing slight overcommitment.

## Current Limits

- Only one isolated benchmark scenario exists
- No second scenario yet with a different capacity or lower-risk context
- No execution evidence yet that the resulting sprint plan survives real sprint pressure

## Recommendation

Promote `sprint-planning` from `review` to `tested`.

Keep the tested posture narrow until:

1. at least one second scenario shows the skill is not overfit to one modernization plan
2. the resulting sprint plan is exercised against real execution or replanning evidence
3. later coverage checks whether the skill still holds under replanning pressure, not only first-pass commitment
