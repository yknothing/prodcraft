# Requirements Engineering Explicit Benchmark: Clean Smoke Review

## Context

This review evaluates the first **valid isolated** explicit-invocation benchmark run for `requirements-engineering`.

- Run artifact: `explicit-benchmark-run-2026-03-16-clean-smoke`
- Model: `claude-sonnet-4-6`
- Scenario count: `1`
- Isolation mode: `tempdir-outside-repo`

Prior artifact `explicit-benchmark-run-1` remains useful as exploratory output, but its baseline is **not valid benchmark evidence** because it was run from inside the Prodcraft repo and showed signs of local-skill contamination.

## Scenario Reviewed

- `approvals-feature-en`

## Manual Review

| Assertion | Baseline | With skill | Notes |
|---|---|---|---|
| structured requirements artifact | pass | pass | Both outputs are structured documents, not loose notes. |
| separates functional and non-functional requirements | pass | pass | Both outputs separate FRs and NFRs. |
| includes priorities | pass | pass | Both outputs assign P0/P1/P2-style priorities. |
| includes traceability | pass | pass | Both outputs trace back to interview findings; with-skill is more systematic via indexed source notes and tighter DN mapping. |
| defines non-goals | pass | pass | Both outputs define explicit out-of-scope items; with-skill frames them more cleanly as release-scope boundaries. |

## Observed Lift From the Skill

Although the baseline already clears the binary assertions, the with-skill output shows a **meaningful quality lift** in requirements discipline:

1. It uses more explicit requirement-language framing (`The system shall...`) instead of drifting toward mixed narrative + requirement prose.
2. It separates requirement statements from conflict notes and open questions more cleanly.
3. It carries stronger specification hygiene:
   - indexed discovery sources
   - clearer scope statement
   - explicit quality-gate checklist
   - more deliberate treatment of ambiguity before architecture
4. It stays more obviously in the requirements layer, with less tendency to smuggle design choices into the main requirement statements.

## What This Does Not Prove

- It does **not** prove broad benchmark success; this is one scenario only.
- It does **not** prove the skill should become strongly auto-discoverable.
- It does **not** justify promotion beyond `review` status on its own.

## Interim Conclusion

`requirements-engineering` now has early evidence that:

- trigger discoverability is weak in a crowded skill ecosystem
- explicit invocation still adds value once the skill is deliberately loaded

That combination supports keeping it as a **workflow-driven / manually-invoked core skill**, pending a fuller isolated benchmark set and `intake -> requirements-engineering` handoff evaluation.

## Next Required Evidence

1. Run the remaining isolated benchmark scenarios from `explicit-benchmark.json`.
2. Add one compliance-sensitive scenario to test whether the skill consistently surfaces retention, authorization, and audit obligations.
3. Evaluate `intake -> requirements-engineering` handoff quality using an approved intake brief as input.
