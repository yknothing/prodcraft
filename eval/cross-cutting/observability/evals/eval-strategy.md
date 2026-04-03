# Observability Evaluation Strategy

## Goal

Evaluate whether the cross-cutting `observability` skill has moved beyond design intent and now provides a repository-backed execution telemetry contract that is:

- explicit about the boundaries it instruments
- versioned and stable enough for downstream consumers
- exercised by real repository artifacts instead of only aspirational documentation
- clear about what remains unproven before `tested`

## Review-Stage Evaluation Mode

At review stage, use a **manual contract review plus live artifact spot checks** rather than trigger scoring or prompt-only side-by-side evaluation.

This skill does not primarily win by discoverability. Its value comes from establishing a reusable telemetry contract that other execution paths actually emit and consume.

## Review Scope

Review the skill against four evidence layers:

1. **Skill contract**
   - `skills/cross-cutting/observability/SKILL.md`
2. **Repository-owned design artifacts**
   - `docs/adr/ADR-001-execution-observability-envelope.md`
   - `docs/observability/execution-event-schema-v1.md`
   - `docs/observability/runtime-feedback-loop.md`
3. **Execution consumers**
   - `scripts/summarize_execution_observability.py`
   - `.github/workflows/runtime-feedback-loop.yml`
4. **Live emitted artifacts**
   - `eval/05-quality/code-review/run-2026-04-03-copilot-brownfield-only-clean/execution-observability.jsonl`
   - `eval/02-architecture/system-design/run-2026-04-03-copilot-brownfield-only-v1-1-rerun/execution-observability.jsonl`

## Assertions

1. `boundary-is-explicit`
   - the skill stays scoped to execution telemetry contracts, not production dashboards or alerts
2. `schema-is-versioned-and-canonical`
   - emitted artifacts use the declared schema version and canonical usage fields
3. `shared-execution-events-exist`
   - the repository emits structured events for runner execution, skill invocation, and usage availability
4. `missing-usage-is-honest`
   - unavailable token usage is represented as `null` plus an explicit unavailable reason
5. `feedback-loop-exists`
   - emitted artifacts can be summarized and reviewed through repository-owned automation

## Pass Standard

Treat the skill as strong review-stage evidence if:

- the contract boundary is clear and distinct from `monitoring-observability`
- at least two real execution artifacts follow the declared schema
- missing usage is recorded explicitly instead of fabricated
- the repository already contains a maintained review loop for those artifacts

## Exit Criteria for Review Stage

- one manual contract review is recorded
- live emitted JSONL artifacts are spot-checked against the schema
- findings explain why the skill is `review`, not `tested`

## Next QA Step

- run the isolated benchmark plan in `eval/cross-cutting/observability/isolated-benchmark-plan.md`
- add at least one non-benchmark runtime artifact to prove the contract is not benchmark-only
- verify incomplete and failed traces remain analyzable without manual reconstruction
