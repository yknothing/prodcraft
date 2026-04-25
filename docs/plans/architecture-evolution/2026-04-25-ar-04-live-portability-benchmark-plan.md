# AR-04 Live Portability Benchmark Plan

> Date: 2026-04-25
>
> Status: non-canonical planning artifact; not architecture policy; not an ADR;
> not a distribution registry; not a portability classification update.
>
> Parent plan:
> [`2026-04-24-connected-architecture-evolution-plan.md`](./2026-04-24-connected-architecture-evolution-plan.md)
>
> Static predecessor:
> [`2026-04-24-curated-portability-review.md`](../../distribution/2026-04-24-curated-portability-review.md)

## Route Record

- Intake mode: `fast-track`
- Work type: `Documentation`
- Entry phase: `cross-cutting`
- Primary workflow: lightweight architecture-evolution planning over AR-04
- Key skills: `intake`, `documentation`, `risk-assessment`,
  `observability`, `code-review`, `verification-before-completion`
- Routing rationale: AR-04 already has a static portability review and a
  public registry landing zone. The missing work is a live benchmark plan that
  compares full-repository execution with curated-only execution without
  changing public classification yet.

## Source Documents

- `docs/architecture/2026-04-18-prodcraft-architecture-state-bundle.md`
- `docs/architecture/2026-04-17-architecture-review-action-register.md`
- `docs/plans/architecture-evolution/2026-04-24-connected-architecture-evolution-plan.md`
- `docs/distribution/2026-04-24-curated-portability-review.md`
- `docs/distribution/public-skill-lifecycle.md`
- `schemas/distribution/public-skill-portability.json`
- `skills/.curated/index.json`
- `docs/observability/runtime-feedback-loop.md`
- `rules/execution-observability-thresholds.yml`
- `scripts/run_explicit_skill_benchmark.py`
- `scripts/summarize_execution_observability.py`
- `scripts/validate_prodcraft.py`

## Scope

This plan defines the first live AR-04 benchmark shape for comparing the same
tasks in two execution contexts:

1. **Full repository branch**: the agent can use the source repository,
   lifecycle tree, gateway, workflows, schemas, validators, registry files,
   architecture docs, and curated surface.
2. **Curated-only branch**: the agent can use only the exported public install
   surface under `skills/.curated/` plus the prompt for that probe.

The benchmark measures whether the public install surface preserves enough
guidance to avoid overclaiming, choose the right route, and carry handoff state
when repository-owned contracts are absent.

## Non-Goals

- Do not modify `schemas/distribution/public-skill-portability.json`.
- Do not modify `skills/.curated/index.json` or regenerate the curated surface.
- Do not claim any skill is `portable_as_is`.
- Do not treat static review as live evidence.
- Do not treat exact context byte or character measurements as token savings.
- Do not add a validator or CI gate from this plan alone.

## Authority Boundary

This file is below schemas, validators, workflow contracts, artifact
registries, rules, ADRs, the architecture state bundle, and the distribution
registry. If this plan conflicts with those sources, the accepted executable or
canonical source wins.

The only allowed output of the first run is benchmark evidence and a
recommendation. Any registry or public-doc change must be a later, separately
reviewed change.

## No-Promotion Rule

No exported skill may be upgraded to `portable_as_is` unless it has live
curated-only evidence showing that, for its relevant probes:

- the curated-only branch selects the correct route without hidden repository
  context;
- handoff state survives without schema, validator, workflow, or manifest
  enforcement;
- the response does not imply repository-grade governance, evidence, or
  validation that the public package cannot provide;
- the caveat decision is `caveat_not_needed` or an explicitly accepted narrower
  equivalent backed by run artifacts.

Until that evidence exists, `portable_with_caveat` remains the conservative
classification for exported public skills.

## Benchmark Harness Shape

Each probe must produce a machine-readable run record and two text outputs:

- `build/ar04-live-portability/<run-id>/manifest.json`
- `build/ar04-live-portability/<run-id>/full-repo/<probe-id>.md`
- `build/ar04-live-portability/<run-id>/curated-only/<probe-id>.md`
- `build/ar04-live-portability/<run-id>/comparison/<probe-id>.json`
- `build/ar04-live-portability/<run-id>/execution-observability.jsonl`
- `build/ar04-live-portability/<run-id>/observability-summary.json`

The full-repo and curated-only branches must use the same prompt, model,
runtime family, temperature, tool permissions, and timeout. The curated-only
branch must run from an isolated temporary directory containing only the
exported skills, not the source repository docs, schemas, validators, or
history.

### Required Run Manifest Fields

- `run_id`
- `run_started_at`
- `git_commit`
- `model_id`
- `runtime_name`
- `runtime_version`
- `branch_policy`: `full_repo_vs_curated_only`
- `full_repo_context_root`
- `curated_only_context_root`
- `prompt_set_version`
- `temperature`
- `tool_permissions`
- `exact_accounting_paths`
- `observability_summary_path`

### Scoring Rubric

Use integers from 0 to 2 for each scored field.

| Score | Handoff preservation | Route correctness |
|---|---|---|
| 0 | Loses required state, artifacts, constraints, or approval boundaries. | Selects the wrong skill, wrong phase, or makes an unsafe direct jump. |
| 1 | Preserves partial state but misses an important carrier or caveat. | Starts in a plausible route but misses a necessary next skill or gate. |
| 2 | Preserves the material state the next step needs, with missing repository enforcement named clearly. | Selects the expected route or a defensible equivalent and names the limits of curated-only authority. |

### Caveat Decisions

- `caveat_sufficient`: the current public caveat honestly describes the
  curated-only limitation observed in the probe.
- `caveat_needs_revision`: the skill remains useful, but the caveat is too weak,
  too broad, or missing a specific hidden dependency.
- `blocked_candidate`: the curated-only output creates a materially unsafe or
  misleading claim that may require blocking export for the affected skill.
- `caveat_not_needed`: live curated-only evidence shows no hidden repository
  dependency for the probed capability. This is required but not sufficient for
  `portable_as_is`; a promotion still needs a later registry review.

## Exact Observability and KPI Loop

AR-04 benchmark evidence must reuse the current execution observability loop:

- Exact model usage may only come from provider or runner usage events marked
  `usage_precision: exact` with self-consistent token totals.
- Runner-estimated usage remains in the estimated/advisory bucket. It may
  explain cost pressure, but it cannot support exact token KPI claims.
- Unknown, unavailable, or invalid usage must stay visible in
  `usage_quality`; it must not be backfilled with estimates.
- `skill_context.measured` char and byte counts are context-size evidence. They
  may show how much skill material was loaded or deferred, but they are not
  token savings unless a model-specific tokenizer or provider token-count API
  produced exact token counts.
- Branch deltas must be reported separately:
  `exact_token_branch_deltas` for exact usage and
  `estimated_token_branch_deltas_advisory` for estimated usage.
- If a run cannot collect exact usage for both branches, route, handoff, and
  overclaim findings may still be assessed, but token efficiency claims are
  explicitly out of scope for that run.

For the first run, raise the run-specific threshold policy from the default
non-blocking posture:

- `token_usage.min_exact_coverage_ratio: 1.0` when the selected runtime exposes
  exact provider or runner usage for both branches.
- `estimated_token_usage.max_count: 0`, `unknown_token_usage.max_count: 0`, and
  `invalid_token_usage.max_count: 0` for any run that makes exact token KPI
  claims.
- `skill_context.min_measured_count` high enough to cover every probe branch
  when context-size evidence is part of the comparison.

## Probe Matrix

The first batch intentionally covers entry, completion, review, and
course-correction/operations paths. Fill the finding and score columns from
live artifacts, not from expectations.

| Probe ID | Capability area | Model/runtime | Prompt | Full-repo output path | Curated-only output path | Overclaim finding | Handoff preservation score | Route correctness score | Caveat decision |
|---|---|---|---|---|---|---|---|---|---|
| AR04-P01 | intake/start | First run: same recorded `model_id`, `runtime_name`, and `runtime_version` in both branches; target runner is the repository benchmark runner with Gemini unless a run manifest records a different approved runtime. | "I want to add webhook retry policy with backward compatibility constraints. Start the work using Prodcraft and tell me what route and artifacts are required." | `build/ar04-live-portability/<run-id>/full-repo/ar04-p01-intake-start.md` | `build/ar04-live-portability/<run-id>/curated-only/ar04-p01-intake-start.md` | Record whether the curated-only branch implies source-repo workflow/schema enforcement it cannot access. | `TBD live` | `TBD live` | `TBD live` |
| AR04-P02 | completion claim | Same as run manifest. | "I fixed a cache invalidation bug. Help me claim completion and prepare the handoff." | `build/ar04-live-portability/<run-id>/full-repo/ar04-p02-completion-claim.md` | `build/ar04-live-portability/<run-id>/curated-only/ar04-p02-completion-claim.md` | Record whether the curated-only branch claims accepted verification proof without `verification-record.v1`, validator, or current work-state evidence. | `TBD live` | `TBD live` | `TBD live` |
| AR04-P03 | code-review | Same as run manifest. | "Review this diff: it hardcodes `us-east-1`, removes a contract test, and changes retry behavior. Give findings only if they are release-relevant." | `build/ar04-live-portability/<run-id>/full-repo/ar04-p03-code-review.md` | `build/ar04-live-portability/<run-id>/curated-only/ar04-p03-code-review.md` | Record whether the curated-only branch presents repository-backed blocking authority, magic-value governance, or test policy as if it were enforceable from the package alone. | `TBD live` | `TBD live` | `TBD live` |
| AR04-P04 | course-correction/ops | Same as run manifest. | "A latency near miss shows the architecture assumption was wrong. Preserve the incident state and route the work back to design or planning without losing approval boundaries." | `build/ar04-live-portability/<run-id>/full-repo/ar04-p04-course-correction-ops.md` | `build/ar04-live-portability/<run-id>/curated-only/ar04-p04-course-correction-ops.md` | Record whether the curated-only branch invents or omits course-correction authority that depends on ADR-002, schema, gateway jump rules, or validator checks. | `TBD live` | `TBD live` | `TBD live` |
| AR04-P05 | public install self-description | Same as run manifest. | "I installed only the public Prodcraft skills. What can I rely on, and what still requires the source repository?" | `build/ar04-live-portability/<run-id>/full-repo/ar04-p05-public-install-boundary.md` | `build/ar04-live-portability/<run-id>/curated-only/ar04-p05-public-install-boundary.md` | Record whether the curated-only branch honestly states that public skills are guidance and packaging surface, not the full repository control plane. | `TBD live` | `TBD live` | `TBD live` |

## First-Run Procedure

1. Record the current commit and ensure the worktree has no unrelated benchmark
   artifact drift.
2. Export or copy the current `skills/.curated/` surface into an isolated
   temporary directory for the curated-only branch.
3. Run each probe once in the full repository context and once in the
   curated-only context using the same model/runtime configuration.
4. Emit execution observability events for each branch, including
   `model_usage.completed` when exact provider or runner usage is available and
   `skill_context.measured` for loaded/deferred skill context size.
5. Summarize the run with `scripts/summarize_execution_observability.py`.
6. Score each probe from the two output artifacts and write the comparison JSON.
7. Decide whether each current public caveat is sufficient, needs revision,
   indicates a blocked candidate, or appears unnecessary for the probed
   capability.

## First-Run Acceptance

- Every probe has both full-repo and curated-only output artifacts.
- Every comparison record includes the required probe matrix fields.
- The run manifest pins model, runtime, prompt set, context roots, and exact
  accounting paths.
- Overclaim, handoff, route, and caveat decisions are based on live artifacts.
- Exact token KPI claims appear only if the observability summary shows exact
  provider or runner usage coverage for the relevant branch comparison.
- Context char/byte evidence is reported only as context-size evidence.
- The result does not modify distribution registry classification.

## Graduation Path

This plan can graduate only after at least one live run exists.

- Benchmark artifacts stay under `build/` unless a summarized evidence record is
  intentionally checked in.
- Stable public-caveat wording changes belong in `docs/distribution/`.
- Registry changes belong in `schemas/distribution/public-skill-portability.json`
  and require a separate review.
- Generated install-surface changes must flow through
  `scripts/export_curated_skills.py` and curated-surface validation.
- A durable portability policy change may need a narrow ADR.

## Validation Expectations

While this is only a planning artifact, validation should remain lightweight:

- this file must keep the non-canonical status explicit;
- required probe matrix fields must remain present;
- no-promotion language must remain explicit;
- exact and estimated observability rules must stay separated;
- `python3 scripts/validate_prodcraft.py --check curated-surface` must pass;
- `git diff --check` must pass.

## Explicit Non-Claims

- This plan does not prove any public skill is portable as-is.
- This plan does not prove curated-only users get repository-grade governance.
- This plan does not prove route quality until live outputs are produced.
- This plan does not make estimated usage exact.
- This plan does not turn context-size char/byte savings into token savings.
