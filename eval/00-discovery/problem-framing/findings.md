# Problem Framing QA Findings

## Summary

`problem-framing` has moved from `draft` to `review`.

## Why This Skill Exists

The entry-stack redesign split the old overloaded entry expectation into two layers:

1. `intake` handles classification, routing, and approval
2. `problem-framing` handles concept shaping only when routing is already clear

This preserves the hard gate while giving Prodcraft a stronger answer to brainstorming-style exploration.

## What Must Be Proven

`problem-framing` is only worth keeping if it can do all of the following at once:

- add clarity without repeating intake
- compare 2-3 plausible directions without drifting into architecture or implementation
- keep the extra user burden low
- produce artifacts that make the direction choice observable and auditable

## Current Interpretation

At this stage, `problem-framing` should be treated as:

- a discovery-phase routed skill
- part of the entry stack, not a replacement for intake
- a candidate to absorb the strongest brainstorming-like behavior in a lifecycle-aware way

## First Manual Review Signals

Manual handoff reviews now exist at:

- `manual-run-2026-03-17-team-invite`
- `manual-run-2026-03-17-access-review`
- summarized in `intake-handoff-review.md`

Initial signal:

- the skill improves observability by making invocation reason, non-goals, and next destination explicit
- the skill improves usability discipline by recording that zero additional questions were needed for a sufficient intake brief
- the skill appears to add more value as a routed handoff layer than as a discoverability-first skill
- the same pattern now appears in both a non-brownfield and a brownfield scenario

## Semi-Isolated Benchmark Signal

A first benchmark-style review now exists at:

- `explicit-benchmark-review.md`

Interpretation:

- baseline can already produce plausible direction notes
- the with-skill delta is strongest on observability, anti-goal preservation, and handoff discipline
- that is the right value shape for an entry-stack routed skill

## Downstream Consumption Signal

Downstream-consumer reviews now exist at:

- `eval/01-specification/requirements-engineering/problem-framing-handoff-review.md`
- `eval/00-discovery/user-research/problem-framing-handoff-review.md`

Interpretation:

- `problem-framing` outputs are no longer only internally coherent
- both a specification skill and a discovery skill can now consume the artifact as a real upstream input
- the strongest observed lift is still preservation of non-goals, scope boundaries, unresolved questions, and auditable next-step discipline

## Next QA Step

Run one true isolated benchmark or cross-reviewer execution drill on one of the reviewed downstream scenarios so the current semi-isolated and downstream-consumption signals can be checked against cleaner evidence.
