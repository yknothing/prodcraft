# Observability Isolated Benchmark Plan

## Goal

Prove that the cross-cutting `observability` contract remains analyzable across completed, incomplete, and usage-limited execution traces without relying on manual guesswork.

## Why This Matters

`observability` is a critical cross-cutting skill. Review-stage evidence shows the contract exists and is already emitted, but `tested` should require stronger proof that the contract survives real execution variance instead of only looking coherent on paper.

## Planned Benchmark Coverage

1. **Completed execution trace**
   - use a clean completed `execution-observability.jsonl` artifact
   - verify start/completed spans, artifact paths, and usage-unavailable handling
2. **Incomplete execution trace**
   - use an interrupted or partially completed trace
   - verify the artifact still explains what started and where the chain stopped
3. **Cross-path consistency**
   - compare at least one benchmark artifact with one non-benchmark runtime artifact once such a path exists
   - verify shared fields and event naming stay stable across paths

## Assertions

1. `completed-traces-are-self-describing`
   - a reviewer can identify the skill, runner, branch, and output artifact without external reconstruction
2. `incomplete-traces-remain-actionable`
   - partial traces still expose the last meaningful step instead of silently disappearing
3. `missing-usage-stays-explicit`
   - unavailable token data uses `model_usage.unavailable` and canonical null fields
4. `feedback-loop-consumes-the-artifacts`
   - `scripts/summarize_execution_observability.py` can summarize the artifacts without schema-specific patching

## Candidate Inputs

- `eval/05-quality/code-review/run-2026-04-03-copilot-brownfield-only-clean/execution-observability.jsonl`
- `eval/02-architecture/system-design/run-2026-04-03-copilot-brownfield-only-v1-1-rerun/execution-observability.jsonl`
- a future non-benchmark runtime artifact once available

## Exit Criteria for Tested Promotion

- at least one completed trace and one incomplete trace are reviewed against the assertion list
- summarizer output is recorded for the reviewed artifacts
- the reviewed artifacts demonstrate stable field naming and explicit missing-usage behavior
