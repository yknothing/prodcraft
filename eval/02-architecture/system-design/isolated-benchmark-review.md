# System Design Isolated Benchmark Review

## Scope

This note records the current isolated benchmark state for `system-design`.

It does **not** yet count as a tested-grade benchmark result artifact because the with-skill branch did not complete cleanly.

The purpose of this note is to make the current blocker auditable and specific so the next rerun starts from a sharper failure mode instead of repeating discovery.

## Runtime Notes

- The benchmark asset now exists at `isolated-benchmark.json`.
- The first `copilot` fallback run at `300s` completed the baseline branch, but the with-skill branch timed out.
- A second `copilot` rerun at `600s` again completed the baseline branch, but the with-skill branch failed with `Connection error.` after reading both the fixture and `skill-under-test/SKILL.md`.
- This means the current blocker is runner-lane instability on the with-skill branch, not a missing benchmark design.

## Scenario 1: Brownfield Access Review Architecture

### Baseline

The isolated baseline completed successfully.

Observed behavior:

- preserved brownfield coexistence as an explicit architectural concern
- kept open questions visible
- stayed mostly at the architecture layer
- produced a serviceable architecture summary with subsystem boundaries

Why this matters:

- the benchmark now has a real clean baseline artifact
- any future with-skill comparison will be against a non-trivial baseline, not a weak control

### With-Skill

The with-skill branch did not produce a usable response artifact in either attempted lane.

Observed behavior:

- `300s` run: timed out
- `600s` rerun: failed with `Connection error.` after reading the skill and the reviewed requirements fixture

Why this matters:

- the current evidence is still insufficient for a promote-or-hold judgment based on benchmark quality delta
- the failure mode is now specific enough to guide the next rerun

## Current Judgment

`system-design` should remain in `review`.

Why:

- the manual routed handoff review remains valid and useful
- the isolated benchmark design is now in place
- the missing piece is a clean with-skill completion for the same brownfield scenario

## Status Recommendation

- recommended status now: `hold at review`
- not yet justified: `tested`

## Next Smallest Honest Step

- rerun the same isolated brownfield scenario once the runner lane is stable
- do not broaden to the second spec-driven scenario yet
- do not rewrite the skill body before a clean with-skill completion exists
