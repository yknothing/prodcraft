# Delivery Completion Isolated Benchmark Plan

## Objective

Measure whether `delivery-completion` improves explicit completion outcomes and destructive-action safety over a generic branch-finish baseline.

## Candidate Benchmark Scenarios

1. **PR handoff**
   - verified work should become a PR with explicit evidence and follow-up path

2. **keep-for-later**
   - verified work should remain preserved with a named next checkpoint instead of falling into ambiguous branch state

3. **discard**
   - destructive cleanup should require typed confirmation and a clear record of what is being deleted

## Metrics

- whether exactly four completion outcomes are presented
- whether stale verification blocks completion
- whether discard requires typed confirmation
- whether downstream release handoff is explicit when shipping continues

## Evidence Gap

This file defines the benchmark plan only. Results are not recorded yet.
