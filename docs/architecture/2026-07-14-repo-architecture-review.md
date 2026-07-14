# Repository Architecture Review: Post-Refactor Deep Audit

> Date: 2026-07-14
>
> Status: independent review findings and recommendations; not an ADR; not canonical architecture policy.
>
> Canonical architecture state remains:
> [`2026-04-18-prodcraft-architecture-state-bundle.md`](./2026-04-18-prodcraft-architecture-state-bundle.md)
>
> Role of this document: record a full post-refactor audit of architecture, implementation, extensibility, compatibility, and silent-failure risks, plus an evaluation-program design. Findings become repository policy only when they land in schemas, validators, workflow contracts, registries, or ADRs.

## Review Scope And Method

- Direct inspection of `skills/`, `workflows/`, `schemas/`, `scripts/`, `tests/`, `tools/`, `manifest.yml`, `.github/workflows/`, `.githooks/`, and `docs/`.
- Execution of `scripts/validate_prodcraft.py` (passed) and `python -m unittest discover tests` (237 tests, all passed) on the current branch state.
- Findings are ranked by the repository's own control promotion law: frequent failure + meaningful cost + stable checkability first.

## Verdict Summary

The repository governance loop is genuinely strong: generated-surface parity checks, schema-contract validators, evidence-indexed manifest, and contract tests are above typical skill-repo practice. The highest-value defects found are all **transit-boundary defects**: value that exists inside the repository degrades silently when it crosses to the public export surface or to a live execution session. This matches the canonical architecture prediction ("what gets lost in transit?") — but several concrete instances are not yet covered by any check.

## Findings

### F1 (P0, compatibility, silent failure): curated exports ship broken cross-skill links

39 of 40 curated skills carry relative links such as
`[tdd](../../04-implementation/tdd/SKILL.md)` (see
`skills/.curated/acceptance-criteria/SKILL.md`). From `.curated/<name>/`,
`../../{phase}/...` resolves into the **source lifecycle tree** — which exists
only inside a full repository checkout. For an `npx skills add` consumer the
links are dead; for a single-skill install (`--skill intake`) even same-phase
sibling links (`../requirements-engineering/SKILL.md`) are dead.

The failure is silent twice over: inside the repo the links happen to resolve
(to the source tree, not the curated tree), and
`validate_curated_surface` only checks bundled
`(references|scripts|assets)/` links (`scripts/validate_prodcraft.py:1583`),
so no check can ever fire.

Recommendation:

- Teach `export_curated_skills.py` to rewrite `Related Skills` links: flat
  sibling link when the target is also exported; plain text plus
  source-path annotation when it is not.
- Add a curated-link check to `validate_curated_surface` so regression is
  blocked mechanically.

### F2 (P0, compatibility): repo-local presentation policy leaks into public skills

`skills/.curated/intake/SKILL.md` and `skills/.curated/problem-framing/SKILL.md`
instruct agents to default user-facing output to Chinese. That is a
repository-operator preference, not a portable capability contract. Public
consumers get a surprising language default with no caveat.

Recommendation: express presentation locale as protocol state, not skill text.
`intake-brief.v1` already carries `user_presentation_locale`; skill bodies
should defer to that field (or host configuration), with the Chinese default
stated only in repo-local entry contracts (`CLAUDE.md`). The exporter can then
ship locale-neutral text without a fork between source and curated bodies.

### F3 (P1, public overclaim): portability caveats do not travel with the skill

`public_caveat_text` lives only in `skills/.curated/index.json`. Agent runtimes
load `SKILL.md`, not `index.json`. The `## Distribution` block appended by the
exporter includes packaging stability and readiness but not the caveat, so the
one sentence designed to prevent public overclaim is invisible at the only
surface agents actually read.

Recommendation: `export_curated_skills.py` appends the caveat line into each
curated `## Distribution` section; `validate_curated_surface` asserts presence.

### F4 (P1, public capability gap): the routing layer does not ship

The curated surface exports 40 skills plus a `prodcraft` gateway package whose
routing guidance defers to "`skills/_gateway.md` in the source repository".
Curated-only consumers therefore hold a skill set with no navigable
composition: no phase map, no selection priority, no fast-track rules — and
(per F1) broken inter-skill links. The static portability review
(`docs/distribution/2026-04-24-curated-portability-review.md`) judged the
gateway honest about this, but honesty about a gap is not the same as closing
the cheap part of the gap.

Recommendation: generate a portable routing digest (phase map, selection
priority table, fast-track table — no repo-only contracts) into
`prodcraft/references/routing-map.md` at export time, derived from
`skills/_gateway.md` so there is no second source of truth.

### F5 (P0, silent failure, governance loop): QA evidence is not bound to skill content state

`manifest.yml` marks skills `tested`/`production` with `qa.*_path` evidence
pointers, but nothing records **which content state** the evidence proved.
Editing a `SKILL.md` after promotion leaves status and evidence untouched —
the exact "evidence freshness masquerade" the state bundle warns about for
downstream work applies, unchecked, to the repository's own governance loop.
Note the contrast: `verification-record.v1` instances *are* required to bind
evidence to `work_state_ref` (`scripts/validate_prodcraft.py:720-793`), so the
repository already knows how to do this correctly.

Recommendation: add an optional `content_ref` (git blob hash of `SKILL.md`)
or `evidence_verified_against` field per manifest skill entry; the validator
warns when the current file hash differs for `tested+` skills, and the warning
graduates to an error once backfilled. This is high-checkability, low-Goodhart:
it proves staleness, not quality.

### F6 (P0, downstream execution loop): protocol artifacts have no runtime validation entry point

The artifact contracts are dual-represented: markdown templates
(`templates/intake-brief.md`) that agents actually fill in during sessions,
and JSON Schemas (`schemas/artifacts/*.schema.json`) that only unit tests
exercise against synthetic payloads
(`tests/test_artifact_schema_registry.py:344`). There is no CLI, no canonical
artifact location, and no hook that can validate a **real produced instance**.
The instance-level completion-claim checks
(`validate_verification_record_instance_contract`) are implemented but
unreachable from any execution path. The downstream loop therefore cannot
mechanically reject a malformed intake-brief or a stale verification-record,
which is the first wave AR-02 already targets.

Recommendation (cheapest closing move, in order):

1. Declare a canonical session artifact convention (e.g.
   `build/artifacts/<work-id>/<artifact>.json`, gitignored by default,
   committable when evidence should persist).
2. Ship `scripts/validate_artifact_instance.py <path...>` that dispatches on
   `artifact` + `schema_version` through `schemas/artifacts/registry.yml` and
   also runs the instance-contract functions.
3. Only then bind host adapters (Claude Code hook, CI job) per AR-03 —
   adapters call the repo-owned CLI; they do not reimplement it.
4. Resolve the dual representation: either templates gain a machine-readable
   block (YAML frontmatter in the artifact md) that the CLI parses, or the
   JSON instance is canonical and the md is a rendering.

### F7 (P1, enforcement gap): main-branch pushes bypass all structural gates

`.github/workflows/validate-skills.yml` triggers on `pull_request` only; a
direct push to `main` runs nothing. The local pre-commit hook requires opt-in
(`git config core.hooksPath .githooks` — unset in a fresh clone) and runs only
the magic-values scan, not the validator.

Recommendation: add a `push: branches: [main]` trigger to the validation
workflow; extend `.githooks/pre-commit` with the fast validator subset
(`skill-frontmatter`, `workflow-entry-gate`, `manifest-skill-status`); document
the hooks opt-in in README Quick Start (it currently lives only in the
code-review skill and `docs/quality/magic-value-governance.md`).

### F8 (P1, extensibility): authoring a skill is a five-surface dual-write with no scaffold

Adding one skill requires coordinated edits to: `SKILL.md`, `manifest.yml`
`skills:` entry, `manifest.yml` `artifact_flow` (duplicating frontmatter
inputs/outputs), the `eval/` tree, and — if exported — both distribution
registries. The validator detects drift in every direction but nothing
*generates* the redundant parts, so the cost of iteration lands on authors.
For a repository whose stated priority is extremely high-quality skill design,
authoring friction is a quality tax: expensive iteration means fewer
iterations.

Recommendation:

- Generate `artifact_flow` from skill frontmatter (producers from `outputs`,
  consumers from `inputs`), keeping only `iterative_feedback_edges` and
  multi-producer rationales hand-authored. One source of truth beats
  dual-write-plus-checker.
- Add `scripts/new_skill.py` scaffolding: SKILL.md skeleton from
  `skills/_schema.md`, manifest entry at `draft`, eval directory skeleton.

### F9 (P2, context economics): the mandatory entry path has no budget check

The activation path every task pays — `CLAUDE.md` (114 lines) →
`skills/_gateway.md` (310 lines) → `intake` (1,778 words) → workflow file
(~160 lines) — is the repository's own declared pressure point
("cumulative load of the path a task activates"), yet no check bounds it.
Body sizes already spread 262–1,849 words with no policy.

Recommendation: add a validator budget check (warning first) for entry-stack
files and per-skill body word counts, with an explicit allowlist for justified
exceptions (`intake`, `code-review`). Record actual entry-path token cost in
execution-observability runs so the budget is evidence-led, not aesthetic.

### F10 (P2, drift risk): entry rules are restated across five surfaces

Entry/routing rules appear in `CLAUDE.md`, `AGENTS.md` (pointer), `README.md`,
`skills/_gateway.md`, and the generated `prodcraft` skill. Some couplings are
already drift-checked (intake taxonomy vs schema, jump pairs vs ADR-002,
README contract tests); the CLAUDE.md/gateway prose overlap is not.

Recommendation: declare `skills/_gateway.md` the single normative routing
source; reduce other surfaces to pointers plus generated summaries; extend the
existing contract tests to cover the remaining overlap.

### F11 (P2, host adapter asymmetry): no Gemini entry contract

`CLAUDE.md` binds Claude Code; `AGENTS.md` binds Codex; there is no `GEMINI.md`
although Gemini is the repository's preferred QA runner. Under the AR-03
adapter policy this is a missing (cheap) adapter.

Recommendation: add a `GEMINI.md` pointer file mirroring `AGENTS.md`.

### F12 (P2, latent authoring trap): workflow backtick tokens must be skill names

`validate_workflow_skill_references` treats every backticked kebab-case token
in a workflow body as a skill reference; the only non-skill tokens allowed are
`all`, `intake`, `intake-brief`, and workflow names
(`scripts/validate_prodcraft.py:1207`). A future workflow edit that backticks
a registered artifact (`course-correction-note`, `problem-frame`) fails with a
misleading "undefined skills/tokens" error.

Recommendation: extend the allowed-token set with artifact names from
`schemas/artifacts/registry.yml` — this tightens semantics (artifacts are
contract-bearing) rather than loosening the check.

### F13 (P2, public index hygiene): internal fields leak into the public index

`skills/.curated/index.json` exposes `manual_allowlist` (an internal
governance flag) and `source` (internal repo paths), while README claims the
index exposes "only public-safe portability fields".

Recommendation: either drop the internal fields from the generated index or
amend the README claim; prefer dropping.

### F14 (P2, skill contract precision): input optionality and unbound thresholds

Two schema-level precision gaps recur across skills:

- Frontmatter `inputs` cannot express optionality. `tdd` lists
  `acceptance-criteria-set` and `api-contract` as inputs while its body calls
  them optional; the artifact-flow graph therefore overstates prerequisites,
  which distorts routing and validation.
- Some quality gates reference parameters with no binding source, e.g. tdd's
  "coverage meets project threshold (e.g., 80%)". A gate that names an
  unbound parameter is not verifiable as written.

Recommendation: add an `optional_inputs` metadata list (schema + validator
support), and require gates that reference thresholds to name where the
threshold is defined (e.g. `rules/testing.yml`).

## Evaluation And Testing Program (direction, plan, acceptance criteria)

Design only — no new implementation is claimed by this document. The program
layers onto existing machinery: `evaluation_mode` in `manifest.yml`,
`scripts/run_explicit_skill_benchmark.py`, the vendored Anthropic trigger
harness, execution-observability JSONL, and the AR-01 matrix.

### L0 — Structural contracts (exists; keep)

`validate_prodcraft.py` + contract tests. Acceptance: zero errors, CI-blocking
on PR **and** push to main (F7).

### L1 — Discoverability trigger evals (narrow set only)

Scope: `prodcraft` gateway, `intake`, and any future discoverability-first
skill. Method: balanced set of ≥20 positive and ≥20 negative prompts per
skill, negatives including hard cases (adjacent skills, non-software tasks);
Anthropic semantics only through `tools/anthropic_trigger_eval/`.
Acceptance: recall ≥ 90%, false-trigger ≤ 5%. Rerun requirement: results bind
to the description's content hash; a description edit invalidates the result.

### L2 — Routed explicit-invocation A/B benchmarks (the primary gate for the lifecycle spine)

Method: paired baseline (no skill) vs with-skill runs in isolated workspaces;
≥5 scenarios per skill, at least one exercising a declared gotcha; ≥3 runs per
arm for variance; grading by blind rubric derived one-to-one from the skill's
`## Quality Gate` checklist; grader model independent of the runner model; raw
prompts and transcripts persisted as evidence.
Acceptance for `tested`: with-skill win-rate ≥ 70% on the rubric total, no
single rubric dimension regressing > 10% vs baseline, output variance < 15%
across runs. Critical-tier skills additionally require a human findings note.

### L3 — Chain integration evals (handoff fidelity)

Fixed scenario suite (3–5): greenfield feature via agile-sprint; brownfield
bugfix with hotfix overlay; fast-track trivial change; mid-chain
course-correction (04 → 01); quality-target-context mismatch (agent-internal
tool misread as public service). Score three things per handoff: artifact
presence, artifact field completeness vs schema, and non-redundancy (the
downstream skill does not re-ask what the upstream artifact already records).
Acceptance: 100% required-artifact presence, ≥ 90% field completeness, zero
unauthorized gate skips, every course-correction inside the ADR-002 pair set.

### L4 — Adversarial and pressure tests

Every skill with a Gotchas section gets at least one eval that actually trips
the trigger condition. Standing probes: authoritative-looking quoted text that
tries to override gates; "skip intake, this is trivial"; "claim done without
fresh evidence"; injection payloads inside upstream artifacts.
Acceptance: zero gate bypasses; observed recovery matches the gotcha's
"What to do"; escalation fires where "Escalate when" requires it.

### L5 — Portability evals for the public surface (AR-04 live extension)

Same task set run three ways: full repo, curated-only, single-skill install.
Measure route correctness, handoff survival, and overclaim (does the
curated-only run ever assert repo-grade gates ran?).
Acceptance: curated-only and single-skill runs never claim repository
validation or evidence gates; degradation is explicit in the transcript;
caveat text (post-F3) demonstrably reaches the agent.

### L6 — Runtime telemetry loop (exists; sharpen)

Monthly execution-observability summaries remain the promotion evidence
source. Promotion of any soft rule into enforcement continues to require the
AR-01 fields (failure frequency, miss cost, checkability, Goodhart risk) with
real traces — never a single anecdote.

### Evidence hygiene rule binding all layers

Every eval artifact records: skill content hash (F5), runner + model version,
scenario set version, and date. The manifest's `qa.*_path` chain stays
auditable only if stale evidence is mechanically detectable.

## Suggested Execution Order

1. **Wave 1 (transit integrity, small diffs):** F1, F3, F13 (exporter +
   curated checks), F7 (CI push trigger). These are pure enforcement wins with
   near-zero Goodhart risk.
2. **Wave 2 (protocol foothold):** F6 artifact-instance CLI + session artifact
   convention; F5 content-hash binding in the manifest (warning first).
   This is the concrete AR-02 first wave.
3. **Wave 3 (authoring leverage):** F8 artifact-flow generation + skill
   scaffold; F14 optional-inputs schema; F12 token allowlist.
4. **Wave 4 (surface polish):** F2 locale de-hardcoding, F4 routing digest,
   F9 budget checks, F10 single-source routing, F11 GEMINI.md.
5. Run the L1–L5 evaluation program incrementally as skills are touched, not
   as a big-bang revalidation.
