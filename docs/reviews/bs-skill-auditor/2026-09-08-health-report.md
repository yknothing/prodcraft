# Prodcraft Repository and Skill Health Audit — 2026-09-08

> Historical audit snapshot. The [September 9 implementation follow-up](../../architecture/2026-09-08-skill-execution-design.md#september-9--top-five-repairs) records subsequent repairs; the findings below describe the audited commit.

## Verdict

Prodcraft has a substantial engineering-governance core: lifecycle routing, explicit artifact contracts, a generated distribution surface, and an optional execution authority engine. Its strongest asset is the separation of guidance, recorded obligations, mechanical checks, and evidence.

Current evidence supports a developed repository governance system with a narrower, opt-in runtime authority boundary. It does not establish that adopting the complete system consistently improves real engineering outcomes after accounting for interaction, context, and maintenance costs.

The highest-value next work is to close evidence-binding and adapter gaps, then measure complete workflows against credible controls. More skills or a distributed orchestrator would not address those gaps.

## Scope and method

- Audited checkout: `fd05978dbbbf5a064205a695af47c8a550f1b224`.
- Source, skills, configuration, and tracked evidence were not modified. This report is the only repository addition made by the audit.
- The pre-existing untracked `docs/architecture/2026-08-28-agent-skills-evolution-competitive-analysis.md` was left untouched and was not used as authority.
- Reviewed repository instructions, gateway, contracts, engine and validator code, export logic, CI, native loading, evaluation infrastructure, selected raw evidence, and central skill processes.
- Fleet-wide static inspection covers 46 authored packages and 40 curated packages. The latter comprise 39 authored skills plus the generated gateway; these are not 86 independent capabilities.
- Semantic review is a declared sample, identified in the inventory. Long-tail methodology not examined in depth is explicitly unassessed.
- Applied the read-only structure/safety/freshness/pattern perspectives from `bs-skill-auditor`, calibrated to Prodcraft conventions. Lifecycle grouping directories are not orphaned skills; `Use before` and `Use after` are valid local trigger syntax. Another repository's pattern taxonomy is not imposed on this project.
- No audited skill was executed as a model workflow. Native parsing, repository tests, adapter probes, and rescoring stored responses are distinct verification layers.
- No approver identity, trusted time, production deployment, fresh live-model benchmark, or multi-writer reliability is certified.

## Verified snapshot

| Dimension | Result |
|---|---|
| Authored skills | 46: 6 production, 32 tested, 8 review, 0 draft |
| Evaluation mode | All 46 authored skills declare routed |
| Curated packages | 40; packaging stability is beta |
| Workflows / personas / artifact schemas | 6 / 7 advisory personas / 8 registered schemas |
| Frontmatter | All 86 package files parse; names match directories |
| Description length | 79–304 characters; all below the 350-character authoring hard cap |
| Soft description guidance | 9 authored descriptions exceed 280 characters; not a validation failure |
| Body size | 180–1,884 whitespace-delimited words; no body-size failure |
| Local Markdown links | No missing targets in package bodies or their Markdown references |
| Safety screen | No configured secret, destructive-command, remote-execution, or permission-bypass pattern hits in package Markdown |
| Revision recency | All 86 package directories last changed on 2026-07-16 |
| Repository validator | PASS |
| Aggregate context budget | PASS |
| Unit/contract suite | 466 tests, 32.161 seconds, OK on Python 3.11.14 |
| Native loader | Gemini CLI 0.39.1 parsed 46/46 authored and 40/40 curated packages |
| Debugging packet rescore | With-skill 12/12; without-skill 12/12; judge pass; no contradictions |
| Existing tracked diff | None |

The static entry-stack inventory contains 36,720 characters. All authored descriptions total 10,330 characters. These are file measurements, not observed per-turn context or exact token billing. The context meter correctly labels its token conversion as estimated.

The first suite run had one environment error: the sandbox prohibited the Unix socket used by a filesystem-safety test. The entire suite passed after allowing that test environment. This was not counted as a product regression.

Revision recency does not prove recent behavioral exercise. The safety screen is not a prompt-injection proof. The scan found no external HTTP Markdown links in package Markdown; it did not certify every externally named API or tool.

## Architecture assessment

```text
Request -> intake and route -> primary workflow plus overlays
        -> selected skill processes and artifacts -> repository validation
        -> optional pinned execution authority
```

Four decisions are particularly valuable:

1. Primary methodology and overlays are separate. Brownfield and hotfix concerns do not require duplicated methodology workflows.
2. Authored maturity, public allowlisting, and generated installation are separate. A tested skill does not silently become a published skill.
3. Quality-target context preserves the real review boundary. Internal agent skills and local tools do not inherit public-service requirements just because they use HTTP.
4. Strict execution authority is separate from structural validity. The engine replays state and phase records, binds obligations, checks current work/evidence, and requires external route/completion pins. Hashing is not presented as identity authentication.

The strict layer is implemented. Engine and adversarial tests cover coordinated evidence rewrites, stale work, canonical versus historical state, duplicate JSON keys, invalid phase order, blocked/resumed execution, symlinks, special files, and Git configuration effects.

This does not make the complete system an autonomous runtime. Legacy workflows are guidance-led. The current Claude adapter gates only Edit/Write against intake; it does not grant strict execution authority. Public packages provide guidance with portability caveats. A host can ignore the system, but then has no Prodcraft strict authorization.

Personas are useful review lenses. Seven role documents do not prove independent agent judgment. Treating them as advisory is appropriate.

Sources: [gateway](../../../skills/_gateway.md), [engine](../../../tools/execution_state.py), [validation service](../../../tools/execution_validation.py), [architecture](../../architecture/2026-07-10-minimal-execution-loop.md), [threat model](../../architecture/2026-07-10-minimal-execution-loop-threat-model.md), [acceptance record](../../architecture/2026-07-10-minimal-execution-loop-acceptance.md).

## Findings

### F1 — P1: Evidence binding omits loaded reference content

**Confidence: 75. Confirmed implementation property with an assurance gap.**

`compute_skill_contract_digest` hashes frontmatter and selected H2 sections of one `SKILL.md`. It does not hash reference-file content. It explicitly excludes Inputs, Outputs, Context, and Anti-Patterns sections. Current skills delegate required inputs and authority to `references/io-contract.md`; references also contain operational rules.

A read-only probe copied the unchanged intake main file to a temporary directory without references. Its contract digest was identical to the full source package. This binding is a main-file projection, not the identity of the behaviorally loaded package.

The evidence registry checks safe paths and file existence, but does not bind evidence-file bytes or require a structured promotion verdict. Export checks catch missing resources and generated drift; they do not require fresh behavioral review when an existing reference changes and export is regenerated.

**Impact:** Reference content can change behavior while prior maturity/evidence bindings remain current. The strict execution-state evidence closure is stronger than this separate skill-promotion boundary.

**Action:** Bind the explicit normative dependency closure and evidence content. Separate deterministic revalidation from behavioral evidence. Keep informational material separately classified if editorial changes should avoid behavioral reruns.

Evidence: [validator](../../../scripts/validate_prodcraft.py), lines 280–313 and 1589–1623; [intake I/O contract](../../../skills/00-discovery/pc-intake/references/io-contract.md); [binding registry](../../../eval/meta/skill-evidence-bindings.yml).

### F2 — P2: The Claude adapter can block on a FIFO before checking its type

**Confidence: 75. Reproduced against the real adapter.**

The final brief is opened with `O_RDONLY | O_NOFOLLOW | O_CLOEXEC`, then checked with `fstat`. Opening a FIFO for reading can block before that check because `O_NONBLOCK` is absent.

A temporary project containing a FIFO at the current intake path caused the real adapter to exceed a 1.5-second probe deadline without rejecting it. Observed elapsed time was 1.505 seconds. The repository validator was never reached.

**Impact:** Invalid filesystem input can stall the gate until the host timeout. The validator's ten-second timeout does not cover this read. Claude's actual timeout disposition was not exercised; this is not a demonstrated authorization bypass.

**Action:** Use nonblocking descriptor reads followed by regular-file checks, consistent with the strict engine, and add a real adapter FIFO regression.

Evidence: [adapter](../../../.claude/hooks/prodcraft_pretooluse.py), lines 106–120; [adapter tests](../../../tests/test_claude_pretooluse_adapter.py).

### F3 — P2: An existing draft intake cannot be repaired through guarded Edit/Write

**Confidence: 75. Reproduced at the adapter boundary.**

The bootstrap exception only permits Write when the brief is absent. Once a brief exists, the adapter validates its old state and rejects non-approved status before allowing the operation, including an edit to the same brief.

An Edit request targeting the current draft brief returned exit 2: `intake brief status must be approved`. This probe used the real adapter with the repository's existing validator fake, isolating the adapter policy without claiming a full host integration test.

**Impact:** Draft-to-approved and invalid-to-repaired flows lack a supported route through the guarded tool family. Bash is outside the matcher; it is not proof of a universal write gate.

**Action:** Define a narrowly authorized repair/promotion operation, validate candidate state, and test recovery alongside rejection. Do not broadly exempt control files or treat an agent-written approver field as human authorization.

Evidence: [adapter](../../../.claude/hooks/prodcraft_pretooluse.py), lines 199–242; [settings](../../../.claude/settings.json).

### F4 — P2: Current maturity presentation and retained supporting reviews disagree

**Confidence: 75. Confirmed documentary inconsistency, not a rejection of all production labels.**

The manifest and current intake status record declare production. The retained benchmark review says it does not justify advancement beyond tested and requires a deeper downstream drill before secure/production. Its integration review covers generated handoff artifacts rather than a complete downstream execution drill.

July 16 revalidation honestly claims deterministic compatibility only. That boundary should remain, but it does not resolve older promotion language or establish fresh end-to-end behavior.

**Action:** Reconcile the current decision with historical reviews. Record validated scope, subject digest, runtime/model, evaluation class, limitations, and revalidation triggers. Preserve historical evidence with explicit supersession rather than rewriting its findings.

Evidence: [manifest](../../../manifest.yml), [benchmark review](../../../eval/00-discovery/pc-intake/post-redesign-benchmark-review.md), lines 103–121; [integration review](../../../eval/00-discovery/pc-intake/post-redesign-integration-review.md); [contract revalidation](../../../eval/00-discovery/pc-intake/contract-revalidation-2026-07-16.md).

### F5 — Product validation gap: Passing behavior tests does not establish incremental value

**Confidence: 75 for the sampled debugging packet; not generalized to every skill.**

The July debugging packet carefully separates evaluator/judge, preserves response hashes, isolates configuration, and excludes contaminated runs. This audit reran its final deterministic scorer with the packet's own benchmark, manifest, and judge records.

Both arms passed all 12 cases. The repository itself states that incremental efficacy is not demonstrated: fixtures and response requirements reveal enough desired process for baseline success.

This is good evidence discipline. It leaves the central product question unresolved: does the complete workflow reduce defects, scope errors, false completion, or delivery time when the test does not already supply the methodology?

The E2E trigger surrogate is similarly honest: 20/20 classification matches are not represented as the official Claude trigger gate.

**Action:** Retain the tooling. Add hidden acceptance discriminators, real repository work, and three arms: no skill, a short generic checklist, and routed Prodcraft. Measure outcome quality and process cost. Avoid scoring only field presence or self-reported compliance.

Evidence: [debugging review](../../../eval/04-implementation/pc-systematic-debugging/evidence/codex-gpt56sol-2026-07-16/review.md); [scorer](../../../scripts/score_explicit_skill_benchmark.py); [surrogate review](../../../eval/05-quality/pc-e2e-scenario-design/evidence/codex-trigger-surrogate-gpt56sol-2026-07-16/review.md).

### F6 — P2: Some imperative rules conflict with valid engineering paths

**Confidence: 75 for textual conflicts; occurrence frequency is unmeasured.**

- TDD requests characterization tests for existing behavior, then says a test passing immediately requires stopping or deleting implementation. Characterization can legitimately pass against existing code. Preserving behavior needs a distinct branch from implementing new behavior.
- Delivery completion always presents four outcomes, without a local branch for an outcome already authorized by the user.
- Intake micro mode permits notify-and-proceed, while the Claude adapter explicitly rejects micro. The small-change experience therefore depends on the host surface.
- Code-review policy treats some literal/exception violations as blocking, while later guidance suppresses checklist-only issues without independent release risk. Precedence needs to be explicit.

**Action:** Add named applicability conditions and precedence, with examples for existing passing characterization tests, already-authorized delivery, and micro work under adapters. Prefer fewer clear conditions over more blanket prohibitions.

Evidence: [TDD](../../../skills/04-implementation/pc-tdd/SKILL.md), lines 54–66; [delivery](../../../skills/06-delivery/pc-delivery-completion/SKILL.md), lines 60–69; [review](../../../skills/05-quality/pc-code-review/SKILL.md); [adapter](../../../.claude/hooks/prodcraft_pretooluse.py), lines 240–243.

### F7 — P2: Public guidance includes an unconditional repository-local hook setup

**Confidence: 75. Confirmed content boundary issue; no consumer configuration was changed.**

Curated code-review says the repository ships `.githooks/pre-commit` and `scripts/hooks/no_magic_values_scan.py`, then instructs `git config core.hooksPath .githooks`. Those tools are not bundled in the package.

The distribution caveat acknowledges the repository requirement for full governance. It does not condition this setup step on tool presence or preserve the consumer's current hook configuration.

**Impact:** Following the instruction elsewhere can point Git at a nonexistent hook directory or replace its previous hook path. A Markdown-link check does not detect this command dependency.

**Action:** Make setup source-repository-only, or explicitly provision/check the tools and preserve existing hook configuration through an authorized setup flow.

Evidence: [curated code-review](../../../skills/.curated/pc-code-review/SKILL.md), lines 152–162 and its Distribution caveat.

## Engineering and adoption costs

Top-level Python files under `scripts/` and `tools/` total 12,208 lines, excluding tests and nested tooling. The 2,995-line validator and 2,290-line execution engine deserve ordinary software maintenance practices. Size alone is not a defect: much of this logic implements purposeful safety checks.

The project still describes itself as documentation/configuration with structural validation. It also contains executable policy, filesystem security, CLI contracts, model runners, and migration tooling. Runtime provisioning and contributor documentation should reflect that reality.

This host's ordinary `python3` is Python 3.8.10 and lacks PyYAML: the real validator fails at `import yaml`. The documented uv Python 3.11 environment passed all checks. The hook invokes `python3`; a working QA environment does not prove its host interpreter is provisioned. A running Claude session's inherited environment was not inspected.

`examples/` explicitly contains no complete checked-in usage examples. Real pressure tests and handoff records exist elsewhere in `eval/`; those records should not be erased from the assessment. Their scope differs from a newcomer-reproducible complete engineering workflow.

Recommended demonstration set:

1. A bounded bug fix through reproduction, TDD, review, verification, and the already-authorized integration outcome.
2. A brownfield compatibility change with a genuine upstream course correction.
3. A completion claim rejected after evidence/work becomes stale, followed by authorized recovery.

Measure artifact consumption, unnecessary approval rounds, false blocks, accepted defects, false completion claims, elapsed time, and provider-reported usage where available. Keep missing data distinct from zero and estimates distinct from exact accounting.

Do not introduce a scheduler, identity service, database, or multi-writer event store until observed deployment requirements exceed the current local authority boundary.

## Verification and limits

Passed with Python 3.11.14, PyYAML, and jsonschema through uv:

```bash
python scripts/validate_prodcraft.py
python scripts/measure_context_cost.py --check
python -m unittest discover tests
git diff --check
```

The complete environment invocation was `UV_CACHE_DIR=/tmp/uv-cache-prodcraft PYTHONDONTWRITEBYTECODE=1 uv run --offline --python 3.11 --with pyyaml --with jsonschema` followed by the Python command. Dependency provisioning initially required network access; subsequent runs were offline.

The stored debugging rescore returned `acceptance_ready=true`, `judge_status=pass`, and no contradictions. This reran scoring, not model generation or judging.

Native loadability was checked through Gemini CLI 0.39.1's exported `loadSkillFromFile` and `loadSkillsFromDir`. Full CLI listing in a temporary project was separately refused by the host's folder-trust policy; that policy was preserved. An earlier listing with the ordinary home timed out. Successful parsing is not represented as trusted-session activation or correct automatic triggering.

The current official [Claude Code hook reference](https://code.claude.com/docs/en/hooks#command-hook-fields) supports an executable plus an `args` vector and project-path expansion. The checked-in command/args form is therefore not treated as a schema bug. Native Claude dispatch and timeout behavior remain untested.

The suite result is a baseline, not proof that the findings are absent. Bounded probes exposed behavior outside current test coverage. No source repair or production-state authorization was performed.

## Recommended order

1. Close F1 and narrow adapter defects F2/F3; verify both rejection and authorized recovery.
2. Resolve F4 and F6/F7 without inflating maturity or adding broad permission exceptions.
3. Publish complete workflow demonstrations and discriminating comparative evaluations for F5.
4. Remove steps, artifacts, and rules that repeatedly add cost without improving outcomes.
5. Consider larger infrastructure only when actual concurrency, identity, or recovery needs require it.

## Per-package confidence inventory

S = structure; Y = bounded safety screen; F = revision freshness; P = sampled process/pattern coherence. Anchors are discrete. Overall is their minimum; 0 means unassessed, not a detected unsafe skill.

S/Y/F are 75: package checks passed, but do not establish universal safety or current semantic execution. P is 75 for a reviewed coherent sample, 50 for a reviewed sample with stated gaps, and 0 for methodology not independently assessed. Foreign pattern-taxonomy conformance is not claimed.

Every scanned package appears below. Source/export duplicates are retained for inventory completeness. F1 concerns authored evidence binding; F4 concerns intake maturity; F5 concerns sampled debugging efficacy; F6 concerns process conflicts; F7 concerns exported setup instructions. Unassessed methodology routes to focused content review before any health claim, not automatic deletion or repair.


### Authored packages

| Skill | Maturity | Description chars | Body words | S | Y | F | P | Overall | Follow-up |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| [pc-feasibility-study](../../../skills/00-discovery/pc-feasibility-study/SKILL.md) | review | 237 | 326 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-intake](../../../skills/00-discovery/pc-intake/SKILL.md) | production | 304 | 1833 | 75 | 75 | 75 | 50 | 50 | F1, F4, F6 |
| [pc-market-analysis](../../../skills/00-discovery/pc-market-analysis/SKILL.md) | review | 211 | 254 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-problem-framing](../../../skills/00-discovery/pc-problem-framing/SKILL.md) | production | 207 | 550 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-user-research](../../../skills/00-discovery/pc-user-research/SKILL.md) | tested | 203 | 477 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-acceptance-criteria](../../../skills/01-specification/pc-acceptance-criteria/SKILL.md) | tested | 79 | 290 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-domain-modeling](../../../skills/01-specification/pc-domain-modeling/SKILL.md) | tested | 212 | 351 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-requirements-engineering](../../../skills/01-specification/pc-requirements-engineering/SKILL.md) | production | 291 | 459 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-spec-writing](../../../skills/01-specification/pc-spec-writing/SKILL.md) | tested | 237 | 386 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-api-design](../../../skills/02-architecture/pc-api-design/SKILL.md) | tested | 295 | 494 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-data-modeling](../../../skills/02-architecture/pc-data-modeling/SKILL.md) | tested | 215 | 305 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-security-design](../../../skills/02-architecture/pc-security-design/SKILL.md) | tested | 186 | 299 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-system-design](../../../skills/02-architecture/pc-system-design/SKILL.md) | review | 243 | 1121 | 75 | 75 | 75 | 75 | 75 | F1; preserve scoped claims |
| [pc-tech-selection](../../../skills/02-architecture/pc-tech-selection/SKILL.md) | tested | 222 | 282 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-estimation](../../../skills/03-planning/pc-estimation/SKILL.md) | tested | 164 | 259 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-risk-assessment](../../../skills/03-planning/pc-risk-assessment/SKILL.md) | tested | 153 | 293 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-sprint-planning](../../../skills/03-planning/pc-sprint-planning/SKILL.md) | tested | 144 | 251 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-task-breakdown](../../../skills/03-planning/pc-task-breakdown/SKILL.md) | production | 245 | 456 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-feature-development](../../../skills/04-implementation/pc-feature-development/SKILL.md) | tested | 215 | 323 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-refactoring](../../../skills/04-implementation/pc-refactoring/SKILL.md) | tested | 195 | 269 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-systematic-debugging](../../../skills/04-implementation/pc-systematic-debugging/SKILL.md) | tested | 228 | 1318 | 75 | 75 | 75 | 75 | 75 | F1, F5 |
| [pc-task-execution](../../../skills/04-implementation/pc-task-execution/SKILL.md) | tested | 273 | 525 | 75 | 75 | 75 | 75 | 75 | F1; preserve scoped claims |
| [pc-tdd](../../../skills/04-implementation/pc-tdd/SKILL.md) | production | 253 | 973 | 75 | 75 | 75 | 50 | 50 | F1, F6 |
| [pc-code-review](../../../skills/05-quality/pc-code-review/SKILL.md) | tested | 302 | 1427 | 75 | 75 | 75 | 50 | 50 | F1, F6 |
| [pc-e2e-scenario-design](../../../skills/05-quality/pc-e2e-scenario-design/SKILL.md) | tested | 303 | 657 | 75 | 75 | 75 | 75 | 75 | F1; preserve scoped claims |
| [pc-implementation-alignment-review](../../../skills/05-quality/pc-implementation-alignment-review/SKILL.md) | review | 208 | 287 | 75 | 75 | 75 | 75 | 75 | F1; preserve scoped claims |
| [pc-implementation-integrity-audit](../../../skills/05-quality/pc-implementation-integrity-audit/SKILL.md) | review | 196 | 352 | 75 | 75 | 75 | 75 | 75 | F1; preserve scoped claims |
| [pc-receiving-code-review](../../../skills/05-quality/pc-receiving-code-review/SKILL.md) | tested | 240 | 498 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-security-audit](../../../skills/05-quality/pc-security-audit/SKILL.md) | tested | 193 | 427 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-testing-strategy](../../../skills/05-quality/pc-testing-strategy/SKILL.md) | tested | 296 | 744 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-ci-cd](../../../skills/06-delivery/pc-ci-cd/SKILL.md) | tested | 241 | 492 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-delivery-completion](../../../skills/06-delivery/pc-delivery-completion/SKILL.md) | tested | 179 | 593 | 75 | 75 | 75 | 50 | 50 | F1, F6 |
| [pc-deployment-strategy](../../../skills/06-delivery/pc-deployment-strategy/SKILL.md) | tested | 199 | 310 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-release-management](../../../skills/06-delivery/pc-release-management/SKILL.md) | tested | 158 | 288 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-incident-response](../../../skills/07-operations/pc-incident-response/SKILL.md) | tested | 287 | 709 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-monitoring-observability](../../../skills/07-operations/pc-monitoring-observability/SKILL.md) | tested | 303 | 391 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-runbooks](../../../skills/07-operations/pc-runbooks/SKILL.md) | tested | 272 | 338 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-retrospective](../../../skills/08-evolution/pc-retrospective/SKILL.md) | tested | 185 | 498 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-tech-debt-management](../../../skills/08-evolution/pc-tech-debt-management/SKILL.md) | tested | 291 | 552 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-accessibility](../../../skills/cross-cutting/pc-accessibility/SKILL.md) | tested | 189 | 201 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-bug-history-retrieval](../../../skills/cross-cutting/pc-bug-history-retrieval/SKILL.md) | review | 257 | 619 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-compliance](../../../skills/cross-cutting/pc-compliance/SKILL.md) | review | 173 | 183 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-documentation](../../../skills/cross-cutting/pc-documentation/SKILL.md) | tested | 209 | 448 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-internationalization](../../../skills/cross-cutting/pc-internationalization/SKILL.md) | review | 170 | 180 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-observability](../../../skills/cross-cutting/pc-observability/SKILL.md) | tested | 247 | 662 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-verification-before-completion](../../../skills/cross-cutting/pc-verification-before-completion/SKILL.md) | production | 220 | 926 | 75 | 75 | 75 | 75 | 75 | F1; preserve scoped claims |

### Curated packages

| Skill | Maturity | Description chars | Body words | S | Y | F | P | Overall | Follow-up |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| [pc-acceptance-criteria](../../../skills/.curated/pc-acceptance-criteria/SKILL.md) | tested | 79 | 341 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-accessibility](../../../skills/.curated/pc-accessibility/SKILL.md) | tested | 189 | 252 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-api-design](../../../skills/.curated/pc-api-design/SKILL.md) | tested | 295 | 545 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-ci-cd](../../../skills/.curated/pc-ci-cd/SKILL.md) | tested | 241 | 543 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-code-review](../../../skills/.curated/pc-code-review/SKILL.md) | tested | 302 | 1478 | 75 | 75 | 75 | 50 | 50 | F6, F7 |
| [pc-data-modeling](../../../skills/.curated/pc-data-modeling/SKILL.md) | tested | 215 | 356 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-delivery-completion](../../../skills/.curated/pc-delivery-completion/SKILL.md) | tested | 179 | 644 | 75 | 75 | 75 | 50 | 50 | F1, F6 |
| [pc-deployment-strategy](../../../skills/.curated/pc-deployment-strategy/SKILL.md) | tested | 199 | 361 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-documentation](../../../skills/.curated/pc-documentation/SKILL.md) | tested | 209 | 499 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-domain-modeling](../../../skills/.curated/pc-domain-modeling/SKILL.md) | tested | 212 | 402 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-e2e-scenario-design](../../../skills/.curated/pc-e2e-scenario-design/SKILL.md) | tested | 303 | 708 | 75 | 75 | 75 | 75 | 75 | Preserve portability boundary |
| [pc-estimation](../../../skills/.curated/pc-estimation/SKILL.md) | tested | 164 | 310 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-feature-development](../../../skills/.curated/pc-feature-development/SKILL.md) | tested | 215 | 374 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-incident-response](../../../skills/.curated/pc-incident-response/SKILL.md) | tested | 287 | 760 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-intake](../../../skills/.curated/pc-intake/SKILL.md) | production | 304 | 1884 | 75 | 75 | 75 | 50 | 50 | F1, F4, F6 |
| [pc-monitoring-observability](../../../skills/.curated/pc-monitoring-observability/SKILL.md) | tested | 303 | 442 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-observability](../../../skills/.curated/pc-observability/SKILL.md) | tested | 247 | 713 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-problem-framing](../../../skills/.curated/pc-problem-framing/SKILL.md) | production | 207 | 601 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-prodcraft](../../../skills/.curated/pc-prodcraft/SKILL.md) | gateway | 292 | 696 | 75 | 75 | 75 | 50 | 50 | Host authority boundary |
| [pc-receiving-code-review](../../../skills/.curated/pc-receiving-code-review/SKILL.md) | tested | 240 | 549 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-refactoring](../../../skills/.curated/pc-refactoring/SKILL.md) | tested | 195 | 320 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-release-management](../../../skills/.curated/pc-release-management/SKILL.md) | tested | 158 | 339 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-requirements-engineering](../../../skills/.curated/pc-requirements-engineering/SKILL.md) | production | 291 | 510 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-retrospective](../../../skills/.curated/pc-retrospective/SKILL.md) | tested | 185 | 549 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-risk-assessment](../../../skills/.curated/pc-risk-assessment/SKILL.md) | tested | 153 | 344 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-runbooks](../../../skills/.curated/pc-runbooks/SKILL.md) | tested | 272 | 389 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-security-audit](../../../skills/.curated/pc-security-audit/SKILL.md) | tested | 193 | 478 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-security-design](../../../skills/.curated/pc-security-design/SKILL.md) | tested | 186 | 350 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-spec-writing](../../../skills/.curated/pc-spec-writing/SKILL.md) | tested | 237 | 437 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-sprint-planning](../../../skills/.curated/pc-sprint-planning/SKILL.md) | tested | 144 | 302 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-system-design](../../../skills/.curated/pc-system-design/SKILL.md) | review | 243 | 1172 | 75 | 75 | 75 | 75 | 75 | Preserve portability boundary |
| [pc-systematic-debugging](../../../skills/.curated/pc-systematic-debugging/SKILL.md) | tested | 228 | 1369 | 75 | 75 | 75 | 75 | 75 | F1, F5 |
| [pc-task-breakdown](../../../skills/.curated/pc-task-breakdown/SKILL.md) | production | 245 | 507 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-task-execution](../../../skills/.curated/pc-task-execution/SKILL.md) | tested | 273 | 576 | 75 | 75 | 75 | 75 | 75 | Preserve portability boundary |
| [pc-tdd](../../../skills/.curated/pc-tdd/SKILL.md) | production | 253 | 1024 | 75 | 75 | 75 | 50 | 50 | F1, F6 |
| [pc-tech-debt-management](../../../skills/.curated/pc-tech-debt-management/SKILL.md) | tested | 291 | 603 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-tech-selection](../../../skills/.curated/pc-tech-selection/SKILL.md) | tested | 222 | 333 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-testing-strategy](../../../skills/.curated/pc-testing-strategy/SKILL.md) | tested | 296 | 795 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-user-research](../../../skills/.curated/pc-user-research/SKILL.md) | tested | 203 | 528 | 75 | 75 | 75 | 0 | 0 | Methodology unassessed |
| [pc-verification-before-completion](../../../skills/.curated/pc-verification-before-completion/SKILL.md) | production | 220 | 977 | 75 | 75 | 75 | 75 | 75 | Preserve portability boundary |

## Auditor self-review and limits

SELF-AUDIT: bs-skill-auditor cannot fully audit itself — an auditor shares its own blind spots. Independent review recommended.

The external auditor skill was read. Its own upstream freshness, foreign pattern references, and complete runtime behavior were not audited. Self-audit anchors are S=75, Y=75, F=0, P=0, Overall=0. This is a declared assessment limit, not a conclusion that the auditor is broken. No auditor or target skill was modified.

All 86 scanned packages appear in the inventory. Findings have follow-up actions; unassessed methodology remains explicit. There is no blanket assertion that every skill is healthy. Report-level checks cover inventory completeness, local links, source-reference existence, and absence of unresolved drafting markers.
