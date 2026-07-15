# Systematic Debugging Isolated Benchmark Plan

## Objective

Measure whether `pc-systematic-debugging` reduces guess-first fixes and improves route accuracy on debugging-heavy tasks.

## Post-Rewrite Benchmark Scenarios

1. **Multi-hypothesis regression**
   - the obvious authorization hypothesis is disproved before a cache-key cause
     is confirmed through one-variable experiments

2. **Flaky-failure stabilization**
   - rerun-until-green is rejected; an observable condition replaces a fixed wait

3. **Stale-artifact trap**
   - runtime/source contradiction forces marker and deployment verification before
     current-source diagnosis proceeds

4. **Structural mismatch**
   - three failed local fixes and cross-service invariant evidence require a
     `course-correction-note`, not a fourth patch

## Metrics

- whether the run demands reproduction before fix
- whether it separates containment from debugging correctly
- whether it invokes or recommends `pc-bug-history-retrieval` when history matters
- whether it escalates to `course-correction-note` when the defect stops looking local
- whether every named downstream skill resolves exactly against `manifest.yml`
- whether two-way fix causality is recorded for local-defect scenarios

## Revalidation Evidence

The N=3 model-backed run and hash-bound independent-model judge review are sealed
in [`evidence/codex-gpt56sol-2026-07-16/`](evidence/codex-gpt56sol-2026-07-16/).
The configured acceptance arm passed 12/12 machine and judge checks, with
`acceptance_ready=true` and zero contradictions.

The baseline arm also passed 12/12. The packet therefore demonstrates stable
contract execution but does not demonstrate incremental lift from explicit skill
loading. That comparative-efficacy gap requires a more discriminative benchmark.
