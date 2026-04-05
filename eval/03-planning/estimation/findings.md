# Estimation QA Findings

## Status

- Current status: `tested`
- Evidence type: isolated benchmark review + routed handoff review
- Scope covered:
  - one brownfield access-review planning slice
  - one downstream handoff into `sprint-planning`

## What Changed

1. The skill now has a checked-in benchmark plan and a first benchmark-grade comparison run.
2. The skill now has a routed handoff review showing why `sprint-planning` is the correct downstream consumer.
3. The repository now has tested-grade evidence that `estimation` improves planning honesty rather than only formatting task sizes.

## What We Learned

1. A strong baseline model can already produce a serviceable size note for this slice, so the benchmark is not comparing against a weak control.
2. Explicit `estimation` invocation materially improves confidence signaling, blocker visibility, and the distinction between confident work and wide-uncertainty work.
3. The skill adds the most value when brownfield risk and coordination cost need to stay explicit before sprint commitment happens.

## Open Issues

- Evidence is still narrow: one benchmark scenario does not justify `secure` or `production`.
- No execution-calibration loop exists yet comparing estimates with actuals.

## Notes

The current evidence is enough for `tested` because the benchmark and the routed handoff both validate the central contract of the skill.
