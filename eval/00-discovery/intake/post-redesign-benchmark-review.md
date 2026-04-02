# Intake Post-Redesign Benchmark Review

## Scope

This review summarizes the current isolated explicit benchmark evidence for the redesigned routing-only `intake`.

The benchmark under review was executed using:

- isolated temp workspaces outside the Prodcraft repo
- a clean baseline prompt that forbids local file reads
- a with-skill prompt that permits only `./skill-under-test/SKILL.md`
- the repository benchmark runner with `gemini`

Superseded exploratory artifact:

- `post-redesign-benchmark-run-2026-03-19-gemini` is not the authoritative benchmark artifact because it was generated before the runner stripped Gemini MCP startup noise from `response.md`
- `post-redesign-benchmark-run-2026-03-19-gemini-clean` is not the authoritative benchmark artifact because it predates the follow-up skill guidance that tightened downstream handoff naming

Current authoritative artifact:

- `post-redesign-benchmark-run-2026-03-19-gemini-naming-rerun`

## Valid Benchmark Scenarios

| Scenario | Baseline | With skill | Judgment |
|---|---|---|---|
| `ambiguous-dark-mode-scope` | Jumps straight to an implementation plan and silently chooses a phased solution direction | Produces an `intake-brief`, routes to `problem-framing`, records risks, and asks one routing-relevant question before handoff | **Positive lift** |
| `legacy-permissions-migration` | Jumps straight to a multi-quarter migration plan with rollout sequencing | Produces an `intake-brief`, classifies this as brownfield discovery work, keeps uncertainty explicit, and now names concrete downstream skills (`software-architecture`, `writing-plans`) | **Positive lift** |
| `seat-management-research-route` | Performs the research/framing itself and recommends a mixed-methods study directly | Produces an `intake-brief`, routes first to `problem-framing`, then to `user-research`, and keeps the work in discovery instead of solutioning | **Positive lift** |

## Assertion Review

### Scenario 1: `ambiguous-dark-mode-scope`

| Assertion | Baseline | With skill | Notes |
|---|---|---|---|
| produces intake brief | fail | pass | Baseline writes a plan; with-skill leaves a visible routing artifact. |
| classifies entry path | fail | pass | With-skill identifies work type, phase, workflow, and risks. |
| keeps question load low | pass | pass | Neither branch over-questions, but baseline uses that speed to skip routing entirely. |
| stays out of solution design | fail | pass | This is the clearest differential in the scenario. |
| records next step and approval gate | partial | pass | Baseline asks for approval on a plan; with-skill asks for approval on the route. |

### Scenario 2: `legacy-permissions-migration`

| Assertion | Baseline | With skill | Notes |
|---|---|---|---|
| produces intake brief | fail | pass | Baseline jumps directly into a migration deliverable. |
| routes to brownfield discovery | fail | pass | With-skill correctly selects migration + brownfield workflow. |
| preserves uncertainty | fail | pass | With-skill keeps hybrid-state and compatibility risk explicit. |
| names downstream handoff | fail | pass | With-skill now names concrete downstream skills on the brownfield path. |
| stays out of cutover design | fail | pass | Baseline immediately commits to phased rollout mechanics. |

### Scenario 3: `seat-management-research-route`

| Assertion | Baseline | With skill | Notes |
|---|---|---|---|
| produces intake brief | fail | pass | Baseline turns straight into a research plan. |
| recognizes fuzzy direction | fail | pass | With-skill preserves that the route is known but the problem direction is not. |
| hands off to problem-framing | fail | pass | This is the key redesign behavior and it appears clearly here. |
| captures routing observability | fail | pass | With-skill records risks and path logic explicitly enough for the next skill. |
| keeps question load low | pass | pass | With-skill reaches the route without turning intake into a long interview. |

## What the Benchmark Shows

### 1. The redesign preserved the core value of `intake`

The redesigned skill still adds visible value where baseline models most often drift:

- converting an ambiguous request into an explicit `intake-brief`
- comparing path options instead of inventing implementation detail
- preserving approval gating before deeper work starts
- routing fuzzy discovery requests to `problem-framing` instead of solving them inline

### 2. Lower question load did not collapse the routing function

The current body contract keeps intake lightweight:

- scenario 1 asks one routing-relevant question before handoff
- scenarios 2 and 3 route immediately with assumptions called out

That is consistent with the redesign goal of keeping `intake` short without removing observability.

### 3. The remaining ambiguity is now narrower

After tightening the skill, the benchmark shows a smaller residual issue:

- the **first downstream handoff** is now consistently concrete on the benchmark set
- some **later** path steps still use generic labels such as `specification`, `implementation`, or `discovery` when those later steps still depend on what the first handoff discovers

This is materially better than the earlier rerun because the immediate handoff target is now clearer. The remaining ambiguity is mostly about provisional later-stage routing, not the first actionable next step.

## Current Judgment

`intake` now has current-version benchmark evidence that the routing-only redesign still improves:

- routing discipline
- approval-gate discipline
- observability of the chosen path
- resistance to collapsing into design, research, or migration planning too early

This benchmark also validates the intended split with `problem-framing`: when the route is known but the direction is still fuzzy, the with-skill branch hands off rather than stretching intake into a discovery workshop.

## Status Implication

This benchmark now supports `intake` holding `tested` under a `routed` QA posture because:

1. the current explicit benchmark shows repeatable lift on the behaviors that matter most for a gateway skill: route selection, approval gating, and handoff observability
2. the supporting integration review confirms the first downstream handoff is usable without reconstructing context
3. the discoverability lane is currently blocked by the Anthropic harness/CLI interaction, so it is tracked as supplemental diagnostic evidence rather than as the primary maturity gate

What this benchmark does **not** prove yet:

1. that `intake` should advance beyond `tested`
2. that the optional discoverability lane is healthy
3. that every later-stage path label is fully final before the first downstream discovery handoff

## Next Required Evidence

1. preserve the rule that the first downstream handoff should be a concrete Prodcraft skill whenever the route is already known
2. run a deeper downstream execution drill before considering `secure` or `production`
3. rerun the bucketed Anthropic trigger eval only after the harness/CLI interaction is repaired
