# Intake-to-Requirements Handoff Review

## Goal

Verify that `requirements-engineering` preserves an approved `intake-brief` when entering the `01-specification` phase.

## Artifacts Reviewed

- Initial long-prompt handoff run: `intake-handoff-run-2026-03-16-approvals`
- Optimized context-file handoff run: `intake-handoff-run-2026-03-16-approvals-rerun`

## What Changed Between Runs

The initial handoff benchmark inlined the full intake brief and discovery notes into the prompt. That made the benchmark expensive and the with-skill branch timed out.

The rerun moved the handoff artifacts into separate context files and shortened the prompt. This better matches how skills are supposed to load context progressively and eliminated the timeout.

## Initial Run Findings

- Baseline produced a usable requirements document.
- With-skill timed out.
- Because the prompt was unnecessarily long, this run is useful mainly as a benchmark-design lesson, not as the main evidence artifact.

## Rerun Findings

### Baseline

Baseline preserved many handoff constraints, but it drifted on an important scope boundary:

- it promoted department-specific thresholds into release-1 in-scope requirements
- it did not preserve downstream handoff notes as explicitly
- it preserved open questions reasonably well

### With Skill

The with-skill output showed stronger handoff fidelity:

- kept the work clearly in the requirements layer
- preserved intake risks as explicit `Risks`
- preserved intake open questions as unresolved `Open Questions`
- respected the "no invented precision" constraint by leaving `near-instant` as an open question rather than fabricating a latency target
- preserved downstream handoff intent (`spec-writing`, `acceptance-criteria`) explicitly
- correctly treated department-specific thresholds as **out of scope for release 1**, matching the intended scope boundary better than baseline

## Assertion Review

| Assertion | Baseline | With skill | Notes |
|---|---|---|---|
| stays in specification phase | pass | pass | Neither output jumped into API or schema design. |
| preserves intake risks | partial | pass | Baseline captured some ambiguity, but with-skill preserved intake risks more explicitly. |
| preserves intake open questions | pass | pass | With-skill structured them more cleanly. |
| respects no invented precision | pass | pass | With-skill explicitly reinforced the open-question treatment of `near-instant`. |
| prepares downstream handoff | partial | pass | With-skill named downstream handoff expectations more clearly. |

## Conclusion

This is the first good evidence that `requirements-engineering` is not just a useful standalone skill, but also a useful **workflow skill** inside Prodcraft.

The skill improves:

- scope-boundary preservation
- risk carry-through
- open-question preservation
- downstream handoff readiness

These are exactly the dimensions that matter in a lifecycle-aware system.

## Remaining Limits

- This handoff evidence is one scenario only.
- It does not resolve the weak trigger-discoverability result.
- It should increase confidence in the skill as a routed/core workflow skill, not as an auto-discoverable skill.
