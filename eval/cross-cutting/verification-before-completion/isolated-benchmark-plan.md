# Verification Before Completion Isolated Benchmark Plan

## Objective

Measure whether `verification-before-completion` stops false completion claims and improves evidence quality at handoff boundaries.

## Candidate Benchmark Scenarios

1. **Stale green**
   - tests passed earlier, code changed later, claim still attempts to reuse the old result

2. **Proxy proof**
   - lint passes, but the claim says the build or behavior is fixed

3. **Fast-track handoff**
   - a narrow change is ready to close, but the agent attempts to skip fresh verification because the scope seems small

## Metrics

- whether the exact claim is named
- whether fresh evidence is demanded
- whether artifact or handoff checks appear when relevant
- whether the final wording reflects the actual evidence rather than optimism

## Evidence Gap

This file defines the benchmark plan only. Results are not recorded yet.
