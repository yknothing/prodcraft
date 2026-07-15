# Post-Review Optimization Handoff

> Date: 2026-07-15
>
> Status: handoff document for follow-up work after the architecture-review
> optimization branch (PR #5) merged to main.
>
> Audience: the next engineer/agent continuing this workstream. Read
> [2026-07-14-repo-architecture-review.md](../architecture/2026-07-14-repo-architecture-review.md)
> first; this document tells you what of it is now DONE, what is IN FLIGHT,
> and what is NEXT, with acceptance criteria per task.

## What PR #5 Shipped (context, do not redo)

Eight batches, each green on `scripts/validate_prodcraft.py` plus the full
`tests/` suite (238 tests):

1. Reference-drift fixes (gateway ghost skills, dangling script refs, intake
   table, examples index) and CI now validating pushes to `main`.
2. Validator hardening: bidirectional maturity labels, gateway reference
   honesty (`gateway-refs` check), artifact-flow graph closure, doc script-ref
   existence (`doc-script-refs` check), 350-char description hard cap.
3. `systematic-debugging` rewritten to a root-cause-first top standard
   (iron law, hypothesis loop, two-way fix causality, `references/techniques.md`,
   six gotchas). Prior benchmark evidence is stale by design -- see
   "Revalidate systematic-debugging" below.
4. Locale-leak fix: curated packages no longer export the operator's Chinese
   default; language fields are open BCP-47 patterns
   (`artifact_record_language` stays const `en`).
5. `micro` intake tier: compact one-block brief, notify-and-proceed, strict
   conjunctive eligibility; schema, gateway, template, and CLAUDE.md aligned.
6. Operational tools: `scripts/validate_artifact_instance.py` (validates real
   artifact records incl. verification-record claim bindings) and
   `scripts/measure_context_cost.py` (context budget accounting).
7. Adversarial-review fix round (schema allOf vs micro contradiction, regex
   boundary defects, helper reuse, prose ownership dedup).
8. Curated self-containment: cross-skill links rewritten at export, portability
   caveats travel inside each package body, mechanical guards in
   `validate_curated_surface`.

Review-doc findings F1, F2, F6, F7, F9 (partially), F10 (partially), F12
(partially), F13 (caveat surfacing) are addressed by the above.

## Standing Rules For All Follow-Up Work

- Enter through `intake` (use `micro`/`fast-track` tiers appropriately).
- After editing any lifecycle skill: `python scripts/export_curated_skills.py`
  then `python scripts/validate_prodcraft.py`; never hand-edit `skills/.curated/`.
- Full local QA:
  `UV_CACHE_DIR=/tmp/uv-cache-prodcraft uv run --python 3.11 --with pyyaml --with jsonschema python -m unittest discover tests`
- Prefer the `gemini` CLI for model-backed evals; the vendored
  `tools/anthropic_trigger_eval/` harness only for official Claude trigger
  semantics.
- Skill-body content discipline (delta-only): contracts, stop signals /
  anti-rationalization, observed-failure gotchas, repo-specific procedure.
  Generic engineering knowledge goes to `references/` or is deleted.

## Task 1 (P0): Revalidate systematic-debugging

The rewrite invalidated prior benchmark/integration evidence. The full plan,
scenario set (multi-hypothesis regression, flaky failure, stale-artifact trap,
structural-mismatch escalation), and acceptance bar are already written:
`eval/04-implementation/systematic-debugging/post-rewrite-revalidation-plan.md`.

- Runner: `scripts/run_explicit_skill_benchmark.py` with gemini, isolated
  workspaces, N>=3 per scenario per arm.
- Acceptance: all machine-checkable assertions pass in every run; zero
  gate-bypass in the escalation scenario; judge verdicts must not contradict
  machine checks. Downstream skill names in outputs must resolve against
  `manifest.yml` (this rubric rule is mandatory -- prior intake evidence
  accepted non-existent skill names).
- Also re-run the trigger eval for `e2e-scenario-design` (description was
  shortened 581 -> ~310 chars in PR #5).

## Task 2 (P1): Evidence-to-content binding (review-doc F5)

`manifest.yml` marks skills `tested`/`production` but nothing records which
content state the evidence proved; PR #5 worked around this with a manual
revalidation-plan note. Implement the mechanical version:

- Add optional `evidence_verified_against` (git blob hash of `SKILL.md`) per
  manifest skill entry.
- Validator: warn when the current hash differs for `tested+` skills; graduate
  to error once all entries are backfilled.
- Hash scope decision (recorded during review): hash the contract-relevant
  sections (frontmatter + Process + Quality Gate) rather than the whole file,
  so wording tweaks do not force full re-benchmarks. If section-scoped hashing
  is too fiddly for v1, whole-file hashing is an acceptable start.
- Acceptance: editing a tested skill's Process section without updating
  evidence turns the validator red; a pure typo fix outside contract sections
  does not (if section-scoped), and the backfill covers all 44 skills.

## Task 3 (P1): Portable routing digest (review-doc F4)

Curated-only consumers hold 40 skills with no navigable composition. Generate
`prodcraft/references/routing-map.md` at export time from `skills/_gateway.md`
(phase map, selection priority tables, fast-track/micro table -- no repo-only
contracts), so there is no second source of truth.

- Acceptance: digest is generated (never hand-written), curated parity check
  covers it, and the generated `prodcraft` SKILL.md references it; a gateway
  routing-table edit shows up in the digest after re-export, and
  `validate_curated_surface` fails if the digest is stale or missing.

## Task 4 (P1): Host adapter first foothold (AR-03, review-doc F6 step 3)

`scripts/validate_artifact_instance.py` exists; bind it to a host:

- A Claude Code `PreToolUse` hook (repo-local `.claude/` config) that blocks
  Edit/Write when no approved intake-brief instance exists for the session's
  work, plus a documented artifact location convention
  (recommendation from review: `build/artifacts/<work-id>/<artifact>.json`,
  gitignored, committable when evidence should persist).
- Keep the adapter thin: it calls the repo-owned CLI; it must not reimplement
  validation.
- Acceptance: in a scratch repo, an edit attempt without a brief is blocked
  with an actionable message; with a valid brief it passes; non-Claude hosts
  are explicitly documented as prose-gated (no silent overclaim).

## Task 5 (P2): Workflow data-ification + delta-only pruning

The biggest unstarted item from the review. Two coupled moves:

- Convert the six `workflows/*.md` narrative files (~18K tokens total) into
  ~30-line structured data (gates, required artifacts, skill sequence,
  overlay deltas) plus short adaptation notes; keep validator sections
  (`Entry Gate`, `Overview`, `Phase Sequence`, `Quality Gates`,
  `Adaptation Notes`) satisfied or update the workflow contract deliberately.
- Prune generic-knowledge restatement from skill bodies (Context/Anti-Patterns
  overlap; ~26% of body words are in low-density sections).
  `systematic-debugging` is the pattern exemplar: tight core + `references/`.
- Measure before/after with `scripts/measure_context_cost.py`; target roughly
  40-50% reduction in workflow tokens and 30%+ in total body tokens with no
  contract loss.
- Acceptance: validator + tests green; per-skill diffs show only knowledge-
  class content removed (contracts, gotchas, stop signals untouched); cost
  meter deltas recorded in the PR description.

## Task 6 (P2): Authoring scaffold (review-doc F8)

Creating a skill is currently a five-surface dual-write (SKILL.md, manifest,
eval tree, distribution registries, cross-cutting matrix). Ship
`scripts/new_skill.py <phase> <name>` that scaffolds all surfaces with
draft-status defaults, so the validator immediately owns consistency.

- Acceptance: scaffold output passes `validate_prodcraft.py` with zero manual
  edits; a follow-up `--promote review` flag is optional scope.

## Task 7 (P2): Known accepted risks to keep an eye on

- Gateway planned-name check can false-positive on ordinary English use of a
  planned skill name (e.g. the word "deprecation" in prose). It fails loudly
  with a clear message; rephrase prose or mark the skill. If it recurs
  often, scope the check to backticked tokens and table rows.
- `micro` notify-and-proceed weakens the blocking-approval invariant by
  design; watch the first real usages for scope creep (anything beyond
  single-revert trivia must fall back to `fast-track`).
- Description budget (350 hard / 280 soft) and the cost meter are not yet
  connected: the meter measures, the validator caps individual descriptions,
  but no check fails on total-budget regressions. Wire a threshold once a
  baseline history exists.

## Suggested Order

1 (unblocks status integrity) -> 2 (makes 1 mechanical forever) -> 4 (turns
prose gates into real gates) -> 3 (cheap public win) -> 5 (largest token/quality
payoff, schedule as its own wave) -> 6 -> 7 (ongoing).
