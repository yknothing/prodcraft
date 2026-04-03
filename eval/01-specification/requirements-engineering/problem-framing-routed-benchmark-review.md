# Requirements Engineering Routed Benchmark Review

## Scope

This note is the current benchmark-results artifact for `requirements-engineering`.

It summarizes the strongest clean routed explicit-invocation evidence currently available for the skill and is intended to replace the older contaminated explicit baseline as the primary promotion artifact.

The decisive evidence below comes from the isolated `copilot` lane on the public default chain:

- `problem-framing -> requirements-engineering`

## Runtime Notes

- The benchmark asset for this lane now exists at `problem-framing-routed-benchmark.json`.
- A clean isolated run completed successfully at:
  - `problem-framing-handoff-run-2026-04-03-copilot-isolated`
- A second rerun also completed successfully at:
  - `problem-framing-handoff-run-2026-04-03-copilot-isolated-600s`
- The retained judgment is about skill quality, not runner preference. The important change is that the lane is now clean and auditable.

## Scenario 1: Brownfield Requirements from Problem-Framing Handoff

### Baseline

The isolated baseline produced a usable requirements summary.

Observed behavior:

- preserved the approved campaign-and-evidence-first coexistence direction
- stayed mostly in the requirements layer
- preserved non-goals and unresolved questions
- shaped the artifact for downstream system-design and acceptance-criteria work

Why this matters:

- the skill is not being compared against a weak or obviously broken control
- the current routed benchmark can therefore measure the quality delta on discipline, not just basic usefulness

### With-Skill

The skill-applied branch was materially stronger on the dimensions that matter for `requirements-engineering`.

Observed behavior:

- preserved the approved direction more explicitly as a release boundary rather than generic modernization language
- kept brownfield coexistence as a P0 requirement without silently turning it into migration design
- preserved all non-goals and open questions with clearer ownership and traceability
- labeled unsupported NFR bounds as assumptions requiring review instead of inventing precision
- shaped the artifact for downstream `system-design` only after requirements review

### Judgment

For this routed brownfield scenario, `requirements-engineering` outperformed baseline on:

- preservation of the upstream design-direction boundary
- explicit no-invented-precision discipline
- traceability of open questions and assumptions
- downstream handoff discipline

The baseline remained competent, but the with-skill branch was materially stronger in the specific value shape Prodcraft expects from this skill.

## Overall Judgment

The current clean routed evidence is now strong enough to move `requirements-engineering` from `review` to `tested`.

Why:

- a clean isolated routed benchmark now exists on the strongest public default chain
- existing integration evidence already exists for `intake`, `problem-framing`, and `user-research` handoffs
- the new benchmark closes the contamination gap that had weakened the older primary proof
- the observed lift is on the dimensions that matter most for this skill: scope discipline, non-goal preservation, open-question handling, and downstream handoff quality

## Limits

This review does **not** justify `secure` or `production`.

Remaining limits:

- trigger discoverability is still weak in a crowded local skill environment
- the decisive lane used `copilot`, so later reruns on another stable lane would still improve confidence
- broader multi-scenario isolated evidence would still be valuable for later maturity stages

## Status Recommendation

- recommended status: `tested`
- not yet justified: `secure`
- not yet justified: `production`
