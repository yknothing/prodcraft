# Problem Framing Isolated Benchmark Review

## Scope

This note is the current benchmark-results artifact for `problem-framing`.

It summarizes the strongest isolated explicit-invocation evidence currently available for the skill and is intended to replace the older semi-isolated benchmark review as the primary promotion artifact.

The repository attempted a primary Gemini lane first on `2026-04-03`, but repeated transient runner failures prevented a clean completion. The decisive evidence below comes from an isolated `copilot` fallback lane while retaining the partial Gemini run artifacts for auditability.

## Runtime Notes

- Gemini hit repeated transient runner failures on the baseline branch before the scenario completed.
- The retained quality judgment below comes from `eval/00-discovery/problem-framing/run-2026-04-03-copilot-brownfield-only`.
- The runner choice affects lane reliability, not the skill contract being evaluated.

## Scenario 1: Brownfield Access Review Direction

### Baseline

The isolated baseline produced a usable direction summary, but it was weaker on the exact dimensions that justify `problem-framing`.

Observed behavior:

- framed the modernization choice quickly and named three viable options
- preserved some non-goals and open questions
- pointed to `requirements-engineering` next
- returned a terse "created file" style summary instead of a clearly auditable framing artifact

Why this matters:

- the response was directionally competent, so the benchmark is not comparing against a strawman
- the main weakness was not basic usefulness, but weaker observability and weaker artifact quality
- those are the dimensions that matter most for an entry-stack routed skill

### With-Skill

The skill-applied branch produced the artifact shape the skill is supposed to enforce.

Observed behavior:

- made the invocation reason explicit instead of assuming the handoff context
- stayed clearly after intake and before requirements or architecture work
- preserved brownfield coexistence, anti-goals, and unresolved questions as explicit framing elements
- compared three release-1 directions with sharper trade-off and rejection logic
- handed off cleanly to `requirements-engineering` and explained why architecture should wait

### Judgment

For this brownfield scenario, `problem-framing` outperformed baseline on:

- observability of why the skill ran
- clarity of release-1 direction framing
- preservation of non-goals and unresolved questions
- downstream handoff discipline

The baseline remained useful, but the with-skill branch was materially stronger in the specific value shape Prodcraft expects from `problem-framing`.

## Overall Judgment

The current isolated evidence is now strong enough to move `problem-framing` from `review` to `tested`.

Why:

- a clean isolated explicit-invocation benchmark now exists
- integration evidence already exists in `intake-handoff-review.md`
- downstream consumption evidence already exists in both `requirements-engineering` and `user-research`
- the isolated lift is on the dimensions that matter most for this skill: low-burden direction shaping, observability, anti-goal preservation, and clean handoff

## Limits

This review does **not** justify `secure` or `production`.

Remaining limits:

- the decisive lane used a `copilot` fallback because Gemini was unstable on the same date
- only the strongest brownfield scenario has isolated rerun evidence so far
- broader non-brownfield variance evidence would still improve confidence later

## Status Recommendation

- recommended status: `tested`
- not yet justified: `secure`
- not yet justified: `production`
