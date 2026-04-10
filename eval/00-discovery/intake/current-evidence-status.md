# Intake Current Evidence Status

## Current Status

`intake` is now `production` under a `routed` QA posture.

That posture change is intentional. `intake` is a mandatory gateway enforced by Prodcraft workflow contracts and the `intake-brief` artifact, so its primary QA question is whether explicit invocation improves routing discipline and downstream handoff quality. Anthropic trigger-discoverability remains useful diagnostic evidence, but it is no longer the maturity gate for this skill.

The current production decision is backed by:

- routed benchmark evidence in `post-redesign-benchmark-review.md`
- routed integration evidence in `post-redesign-integration-review.md`
- this findings record
- package security review in `security-review.md`

## What Still Counts

- the historical trigger eval remains useful for understanding earlier discoverability behavior
- the historical benchmark remains useful for understanding the kind of routing discipline `intake` can add versus baseline
- the redesign notes remain valid context for why the skill returned to `review`
- the 2026-03-18 bucketed rerun in `optimization/iter-2/results-{core,overlap,non-trigger,mixed}.json` is current evidence for the tightened routing-only description that began `Route engineering work before execution.`
- the 2026-03-19 isolated Gemini benchmark in `post-redesign-benchmark-run-2026-03-19-gemini-naming-rerun` is current evidence for the redesigned body contract under explicit invocation
- the 2026-03-19 integration review in `post-redesign-integration-review.md` is current evidence that the generated `intake-brief` usually preserves enough routing context for downstream use

## New Evidence From 2026-03-18

A valid bucketed rerun was completed after Claude CLI preflight passed.

Results for the tightened routing-only description:

- core recall: `0/5`
- overlap recall: `0/5`
- non-trigger precision: `10/10`
- mixed continuity accuracy: `10/20`

Interpretation:

- false-positive control is strong
- the tightened metadata became too narrow to surface `intake` for its own highest-signal entry prompts
- this is now a valid product signal, not a quota artifact

After reviewing those results, the description was revised again to restore high-signal user language.

## New Evidence From 2026-03-19

A clean isolated Gemini benchmark was completed after fixing runner-side Gemini startup-noise contamination.

Reviewed artifacts:

- `post-redesign-benchmark-run-2026-03-19-gemini-clean`
- `post-redesign-benchmark-run-2026-03-19-gemini-naming-rerun`

Current benchmark conclusion:

- baseline still drifts strongly into implementation plans or direct research execution
- with-skill output consistently restores routing discipline, approval gating, and observable handoff shape
- the redesign split with `problem-framing` is visible in current evidence, especially on fuzzy discovery requests
- a follow-up rerun after tightening downstream naming improved first-hop handoff specificity on the brownfield migration path

The same run also supported a manual integration review:

- `post-redesign-integration-review.md`

Current integration conclusion:

- the generated `intake-brief` now usually preserves enough context for downstream use
- the remaining quality gap is mostly later-stage route specificity, not missing routing context or first-hop handoff ambiguity

## New Evidence From 2026-03-31

A new post-reset rerun was completed for the description revision that restored high-signal keywords.

Fresh bucket artifacts:

- `optimization/iter-2/results-core-2026-03-31.json`
- `optimization/iter-2/results-non-trigger-2026-03-31.json`

Current results for the description at that time:

- core recall: `0/5`
- non-trigger precision: `10/10`

Initial Interpretation (March 31):

- the same high-precision, low-recall pattern still holds on the strongest entry prompts
- the apparent blocker was thought to be description discoverability and skill-ecosystem competition, as keywords alone did not restore recall

## New Evidence From 2026-04-02

A follow-up investigation into the persistent `0/5` core recall was completed.

Fresh runtime checks:
- Reproducing the trigger failure confirmed that the current harness consistently returns `0/5` recall for core prompts, even with highly optimized descriptions.
- Manual testing revealed a deeper root cause: **Claude CLI is not automatically invoking the temporary commands created in `.claude/commands/` based on their metadata descriptions**, regardless of how the description is phrased. The harness-runner interaction is failing to surface local command metadata for routing.

Current status:
- The description was updated to: `'The mandatory gateway for all new engineering work. Triage and route new products, apps, features, migrations, tech-debt, or any ''not sure where to start'' request to the correct lifecycle path. Use before starting design or implementation. Do not use for ongoing tasks, specific debugging, or PR reviews.'`
- This revision provides the strongest possible "gateway" signal while remaining concise.
- **Unified Conclusion**: The 2026-03-31 observation of "low recall despite keywords" is now confirmed as a symptom of the **evaluation harness/runner interaction blocker** discovered on 2026-04-02. The harness is currently unable to produce valid discoverability metrics for local skills.

## QA Posture Decision From 2026-04-03

Prodcraft now treats `intake` as a `routed` gateway skill rather than a `discoverability`-gated skill.

Why this is the stronger contract:

1. `intake` is already enforced as the mandatory entry gate by repository rules, workflows, and the required `intake-brief` artifact.
2. The current explicit benchmark shows clear lift over baseline on routing discipline, approval gating, and the split with `problem-framing`.
3. The current integration review shows the resulting `intake-brief` is usually usable downstream without reconstructing routing context.
4. The Anthropic trigger lane is currently blocked by the harness/CLI interaction, so using it as the primary maturity gate would mis-measure the skill's real operational value.

## Current Recommendation

`intake` should now hold at `production` under the routed posture.

The trigger-discoverability lane should remain as supplemental monitoring only until one of the following occurs:
1. the `anthropic_trigger_eval` harness is repaired to ensure Claude CLI actually respects command metadata for automatic routing
2. a different trigger-eval runner is introduced that accurately reflects the production environment

The skill body itself remains strong. The current benchmark plus integration evidence are now sufficient for `tested`; the remaining blocker applies only to future discoverability experiments, not to the routed maturity claim.

## What No Longer Counts as Current Proof

The following artifacts are now treated as **historical evidence**, not current primary proof:

- `optimization/iter-2/results-mixed.json`
- `iteration-1/benchmark.md`

Why:

1. the redesigned `intake` is narrower and more explicitly routing-only
2. the redesigned skill now hands fuzzy routed cases to `problem-framing`
3. current QA needs to verify lower question load, stronger observability, and cleaner handoff behavior, not just the old trigger/benchmark shape

The following artifact is also treated as **superseded exploratory evidence**, not current primary proof:

- `post-redesign-benchmark-run-2026-03-19-gemini`
- `post-redesign-benchmark-run-2026-03-19-gemini-clean`

Why:

1. `post-redesign-benchmark-run-2026-03-19-gemini` was generated before the benchmark runner stripped Gemini MCP startup noise from stored responses
2. `post-redesign-benchmark-run-2026-03-19-gemini-clean` was generated before the skill body was tightened again to improve downstream handoff naming
3. `post-redesign-benchmark-run-2026-03-19-gemini-naming-rerun` now reflects the current body contract

## What Must Be Re-Generated

Before `intake` can move beyond `tested`, regenerate:

1. a deeper downstream execution drill if we want stronger proof than the current review of benchmark-produced handoff artifacts
2. a tighter follow-up benchmark if the skill body changes again after the 2026-03-19 naming rerun
3. a fresh trigger eval only if the harness is repaired and discoverability monitoring becomes decision-relevant again

The trigger-eval evidence now splits into two sub-parts:

1. keep the valid 2026-03-18 rerun as evidence that one tightened description regressed on core discoverability
2. treat the 2026-03-31 core/non-trigger rerun as current evidence for the latest description revision
3. rerun overlap and mixed continuity only if we need a fuller routing-competition picture before another description rewrite or after a harness fix

## Repository Convention

`manifest.yml` now records the old artifacts under `historical_*_path` so the audit trail is preserved without overstating current evidence quality.
