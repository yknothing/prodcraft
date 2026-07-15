# Fable Follow-Up Acceptance

> Date: 2026-07-16
>
> Baseline: `main@b41e032`
>
> Status: implementation and adversarial acceptance complete on
> `codex/fable-followup-acceptance`

## Decision

The seven follow-up items in
`2026-07-15-post-review-optimization-handoff.md` are implemented and pass the
repository's deterministic acceptance surface. The P0 systematic-debugging
revalidation is sealed and acceptance-ready. All 46 manifest skills are bound
to reviewed evidence through a contract projection. The portable routing map,
Claude Code preflight, workflow/context reductions, atomic authoring scaffold,
micro constraints, and aggregate context gates are active.

The result does not claim more than the evidence proves. In particular, the
model packet does not demonstrate incremental lift over baseline, the fresh
trigger result is a Codex surrogate rather than the official Claude gate, and
the brownfield integration review proves a bounded TDD handoff rather than a
live TDD execution.

## Acceptance by Handoff Task

### Task 1: Revalidate `pc-systematic-debugging`

- Four adversarial scenarios run in two arms, three repetitions each: 24/24
  runner completions and 24/24 machine passes.
- The configured acceptance arm passed 12/12.
- A distinct pinned judge model passed 24/24 with no missing, duplicate, extra,
  hash-mismatched, or contradictory verdict.
- Final scorer: `machine_passed=true`, `judge_status=pass`,
  `acceptance_ready=true`.
- Scenario D produced the required course-correction note in every repetition,
  attempted no fourth local patch, and recorded no gate bypass.
- The sealed packet contains 40 indexed files; every recorded SHA-256 and size
  was independently rechecked.
- Packet index SHA-256:
  `c2ea3693d4331d72e9a47083ee23fe32571387493c8fa545e0a0cd6bff7dc802`.
- `pc-e2e-scenario-design` received a fresh 20-case Codex trigger surrogate:
  20/20 labels matched. Its review and metadata set
  `official_trigger_gate_satisfied=false`.

Evidence:

- `eval/04-implementation/pc-systematic-debugging/evidence/codex-gpt56sol-2026-07-16/`
- `eval/04-implementation/pc-systematic-debugging/history-debugging-tdd-integration-review.md`
- `eval/05-quality/pc-e2e-scenario-design/evidence/codex-trigger-surrogate-gpt56sol-2026-07-16/`

The evaluator was `gpt-5.6-sol`; the judge was `gpt-5.4-mini`. They were
isolated in per-case auth-only homes with user configuration disabled and zero
preflight/postflight path matches for the evaluated skill. They are distinct
models but share the same provider and CLI. Gemini was unavailable because the
installed individual client tier was unsupported; Claude was unavailable
because OAuth had expired.

The baseline arm also passed 12/12. This proves that the configured behavior is
reliably produced, not that explicit skill loading caused an improvement. The
fixture and response schema expose substantial process guidance, so no causal
efficacy claim is accepted from this packet.

The integration review uses an explicitly synthetic, non-production history
fixture. It preserves rejected H1, confirms H2 only with current evidence,
requires two-way causality, and translates the confirmed boundary into a
bounded TDD task and acceptance criteria. It does not invent a direct
`bug-fix-report -> pc-tdd` manifest edge or claim that TDD ran.

### Task 2: Evidence-to-content binding

- `contract-projection.v2` hashes normalized frontmatter and every contract H2
  while excluding only declared informational/index sections.
- Duplicate H2 headings fail closed because they make the projection
  ambiguous.
- `review`, `tested`, `secure`, and `production` skills require a current
  binding; `draft` remains authorable without premature evidence.
- `manifest.yml` coverage: 46/46 skills.
- `eval/meta/skill-evidence-bindings.yml` coverage: 46/46 unique records with
  date, scope, and existing repository-local evidence paths.
- Process, hard-gate, iron-law, quality-gate, and frontmatter drift turns the
  validator red. A typo in an excluded Context section does not.
- Absolute, parent-traversing, missing, duplicated, and symlink-component
  evidence paths fail closed.

The binding establishes repository-local freshness and traceability. It does
not convert an old report into external authority or a new model run.

### Task 3: Portable routing digest

- `scripts/gateway_routing.py` parses the canonical gateway sections shared by
  validation and export.
- Export creates
  `skills/.curated/pc-prodcraft/references/routing-map.md`; the curated
  `pc-prodcraft` skill links to it.
- Curated parity fails on stale or missing output.
- Unknown, planned, non-public, and not-included skills retain explicit
  portable markers.
- The exporter rejects lifecycle/cross-cutting source-tree paths, and the
  canonical gateway now uses the independent `pc-documentation` token.

### Task 4: Claude Code host adapter

- Project-scoped `.claude/settings.json` matches `Edit|Write` and uses the
  documented command-plus-args form.
- `.claude/hooks/prodcraft_pretooluse.py` requires the exact current work id and
  approved full/fast-track/resume intake brief, delegates structure to the
  repository validator, and maps every rejection to blocking exit code `2`.
- Only the exact first `Write` to the canonical missing brief path may
  bootstrap the gate. Micro intake does not grant blocking adapter authority.
- The adapter opens every brief path component without following symlinks,
  validates a private byte snapshot, then securely reopens the canonical brief
  and requires identical identity and bytes before allowing the tool call.
- Scratch tests reproduce and close both a symlink-parent escape and a
  validator-time path replacement. A direct invocation against the real
  repository validator passed for a valid full brief.

The hook decision is snapshot-bound. It does not claim control over a process
that mutates repository state after `PreToolUse` returns. Non-Claude hosts
remain prose-gated.

### Task 5: Workflow data and delta-only bodies

All six workflows now use the shared `workflow.v2` structured contract. The
validator and composition checks consume the same parser, including sequence,
gate, artifact, overlay, and skill-reference semantics.

Measured against `main@b41e032`:

| Surface | Baseline chars | Current chars | Change |
|---|---:|---:|---:|
| Six workflows | 68,556 | 38,265 | -44.18% |
| Forty-six skill bodies | 235,790 | 160,785 | -31.81% |

Generic Context, I/O narration, and ordinary anti-pattern prose moved to lazy
references. Core contracts, observed-failure gotchas, hard gates, stop signals,
and anti-rationalization rules remain in the primary bodies. All 46 contract
digests stayed unchanged through this pruning.

`schemas/context-budget.json` pins the baseline and caps always-on
descriptions, entry stack, workflows, and skill bodies. CI runs
`scripts/measure_context_cost.py --check`.

### Task 6: Authoring scaffold

`scripts/new_skill.py <phase> <name>` creates a validated draft skill, eval
strategy, and manifest entry. Draft creation deliberately leaves promotion
surfaces unchanged until review: workflows, artifact flow, public registry,
portability registry, and cross-cutting matrix are not prematurely wired.

The complete candidate repository is validated before commit. Cooperating
scaffold transactions hold a repository-root advisory lock. Publication uses
no-replace directory moves and an atomic manifest exchange. Rollback moves
owned paths into a private quarantine before comparing or deleting them, and
post-exchange verification requires both the displaced baseline and exact
candidate target. Concurrent replacement bytes are preserved rather than
overwritten or deleted.

Focused race tests cover read-then-replace rollback, post-exchange manifest
overwrite, recovery conflicts, destination appearance, validator failure, and
manifest drift. A real default CLI run in a full scratch repository produced a
draft skill whose complete repository validator passed, while promotion
surface hashes remained unchanged.

The advisory lock cannot force a non-cooperating writer to participate. Such a
writer is detected at transaction boundaries where POSIX filesystem primitives
permit detection; no cross-process byte-level compare-and-swap claim is made.

### Task 7: Accepted-risk closure

- Gateway reference recognition requires canonical `pc-` identities, closing
  ordinary-English collisions while retaining per-occurrence marker checks.
- Micro intake binds `zero_questions` to an empty `questions_asked`, requires
  `routing_changed_by_answers=false`, limits work type/runtime/exposure to the
  small local surface, and retains all five conjunctive eligibility assertions.
- Artifact-instance validation requires `recommended_next_skill` and every
  `proposed_path` entry to resolve to a manifest skill.
- Aggregate context gates are wired to CI and pass against the pinned merge
  baseline.

## Adversarial Review Closure

The first independent review found five P1 issues and no P0:

1. review-status skills were outside evidence drift detection;
2. one repo-only routing path leaked into the curated digest;
3. the host adapter accepted symlinked parents and mutable validation paths;
4. scaffolder rollback/exchange boundaries admitted concurrent data loss or
   silent inconsistency;
5. micro artifacts could self-contradict and route to nonexistent skills.

Each issue received a deterministic reproduction before repair. The follow-up
review found no remaining P0/P1 blocker. The Task 6 race repair passed an
additional 18-test adversarial suite, including preservation of both the newer
public replacement and privately quarantined displaced version on conflict.

## Final Verification

```bash
python3 scripts/export_curated_skills.py
python3 scripts/validate_prodcraft.py
python3 scripts/measure_context_cost.py --check
UV_CACHE_DIR=/tmp/uv-cache-prodcraft \
  uv run --python 3.11 --with pyyaml --with jsonschema \
  python -m unittest discover tests
ruff check <25 changed Python files>
python3 -m py_compile <25 changed Python files>
git diff --check
```

Results:

- curated export: 40 public skill packages generated
- repository validator: pass
- context budget: pass
- full suite: 466 tests, pass
- changed Python lint/compile: pass
- whitespace/error-marker check: pass

## Remaining Evidence Boundaries

- The official vendored Claude trigger gate is not fresh; the available Codex
  surrogate is supplemental only.
- The Claude hook contract and direct adapter are verified, but no authenticated
  Claude UI session performed a live Edit/Write end-to-end run.
- The history input is synthetic and no live connector was queried.
- The integration review proves TDD handoff readiness, not RED-GREEN-REFACTOR
  execution.
- Scaffolder crash consistency under `SIGKILL` or power loss is not claimed.
