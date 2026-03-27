# Systematic Debugging Isolated Benchmark Plan

## Objective

Measure whether `systematic-debugging` reduces guess-first fixes and improves route accuracy on debugging-heavy tasks.

## Candidate Benchmark Scenarios

1. **Normal regression**
   - failing test with a recent code change and no live incident pressure

2. **Contained hotfix**
   - incident already mitigated, root cause still unknown, minimal repair required

3. **Structural mismatch**
   - two failed fixes and evidence that the defect belongs in architecture rather than local code

## Metrics

- whether the run demands reproduction before fix
- whether it separates containment from debugging correctly
- whether it invokes or recommends `bug-history-retrieval` when history matters
- whether it escalates to `course-correction-note` when the defect stops looking local

## Evidence Gap

This file defines the benchmark plan only. Results are not recorded yet.
