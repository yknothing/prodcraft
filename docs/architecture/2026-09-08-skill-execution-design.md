# Skill Execution Design Revision — 2026-09-08

This is the canonical English record. A [non-authoritative Chinese companion](2026-09-08-skill-execution-design.zh-CN.md) explains the same decisions, limitations, and self-review.

## Decision

Optimize the existing skill system around decisions and consumable outcomes. Keep its lifecycle, artifact contracts, workflow composition, and optional strict authority engine. Do not add a skill, scheduler, artifact type, or dependency for this revision.

The requested deliverable is positive design improvement to individual skills and their composition. Broad behavioral evaluation is a separate handoff, not the main implementation task. The [repository audit](../reviews/bs-skill-auditor/2026-09-08-health-report.md) remains a historical snapshot of `fd05978dbbbf5a064205a695af47c8a550f1b224`.

## System Changes

| Decision | Implemented contract | Intended effect |
|---|---|---|
| Continue or re-enter | Reuse approved scope and authority; re-enter intake only for new work or a material change | Avoid repeated intake and approval rounds |
| Select a skill | Choose the next unmet obligation and one primary skill; preserve required gates | Avoid automatic full-lifecycle execution |
| Consume inputs | Check accepted artifact scope, freshness, and quality before rerunning a producer | Make handoffs consume real outputs |
| Load context | Main skill and required I/O first; step methods and triggered gotchas as needed | Avoid loading every workflow and reference |
| Compose reviews | Separate intent, code defects, integrity, and completion evidence; permit named sections in one report | Avoid duplicate review work without losing conclusions |
| Repeat work | Resolve a concrete gap; stop a repeated loop that has no new evidence | Avoid approval-seeking rewrites |
| Export behavior | Project the canonical Core Rule into the portable routing map and update the shared gateway renderer | Keep public and source entry behavior aligned |

These are guidance and authoring contracts. They do not automatically enforce model attention or confer runtime authority. Strict execution obligations, state transitions, and operator pins retain their existing meanings. Independent approval cannot be supplied by relabeling a self-review.

## Individual Skill Changes

| Skill | Design improvement |
|---|---|
| `pc-intake` | Restore new bug/review entry eligibility; preserve prior approval; permit one-skill routes and zero questions; teach primary-plus-overlay composition with decision examples |
| `pc-system-design` | Start with current or in-process architecture; justify new boundaries against real drivers; tailor diagrams and topology to the actual runtime |
| `pc-task-breakdown` | Define tasks by outcomes and consumed dependencies; treat duration as a ceiling and parallelism as a cost trade-off |
| `pc-task-execution` | Apply the wrapper only when batching solves a real problem; reuse upstream plans and continue independent authorized work around blockers |
| `pc-tdd` | Separate new behavior from characterization; preserve existing work; prove baseline failure honestly; use appropriate checks for skill prose and visual work |
| `pc-code-review` | Require concrete defects or cited policy for blockers; consolidate root causes; condition repository-specific scanner setup and exception syntax |
| `pc-implementation-alignment-review` | Reuse coverage mappings; prevent unauthorized deferral from satisfying a must-have; inspect only relevant artifacts |
| `pc-implementation-integrity-audit` | Focus on hidden failure and evidence substitution; distinguish missing proof from demonstrated deception |
| `pc-verification-before-completion` | Reuse still-current evidence for the same claim; rerun affected checks; distinguish design handoff from behavioral readiness |
| `pc-delivery-completion` | Execute an already-authorized outcome; keep commit, push, PR, merge, and deployment authority separate |

The authoring schema records an enter/consume/decide/produce/continue-or-stop design convention. Workflow schema guidance explains accepted-artifact reuse, overlay composition, handoff content, and review provenance without changing `workflow.v2` fields.

## Applicability and Authority

- A valid existing artifact can satisfy an input; its filename alone cannot.
- Shared reports preserve every required conclusion and reviewer identity. They do not bypass schemas or strict evidence binding.
- A route change, external side effect, or missing authority still needs the applicable approval. A tech-debt note cannot waive a blocking gate.
- The current Claude Edit/Write adapter rejects micro mode. The September 8 pass documented that limitation; the September 9 follow-up below repairs FIFO blocking and draft recovery.
- Public packages do not install repository hooks or replace consumer Git configuration as a side effect of skill invocation.

## Revision Status and Handoff

The first pass revised ten authored skills; the subsequent design wave below adds six, for sixteen current `review` candidates. In the first pass, all ten changed authored skills are at `review`: three remain there, four return from `production`, and three return from `tested`. Their previous maturity and evidence are retained in the evidence-binding history; the current record describes design review and deferred behavioral evaluation. Existing public packages remain explicitly allowlisted beta candidates; changed `core` readiness labels become `beta`.

The [evaluation handoff](../../eval/meta/2026-09-08-skill-design-handoff.md) binds the candidate contracts, names deferred scenarios and expected decisions, and records the checks actually run. A refreshed digest is not a model benchmark or a promotion decision. Repository export is not global installation or publication.

Rollback can restore the touched source contracts, gateway renderer/projection, and revision-status records from the audited base and regenerate the curated tree. Preserve unrelated user changes and the historical audit. No host configuration or installed global skill is changed by this revision.

## Self-Review of the September 8 Pass

### Judgment

The direction is reasonable, but this is a bounded candidate design revision, not a completed system optimization. The strongest changes replace unconditional procedures with explicit decisions while preserving artifact obligations, approval scope, and strict authority. The main limitation is that most improvements remain agent-executed instructions. The renderer and routing projection carry those instructions to consumers; they do not implement automatic reference loading, artifact reuse, or scheduling.

### What the implementation supports

- Architecture and task decomposition now start from the actual outcome and existing boundaries. New components, diagrams, and execution wrappers need a reason to exist.
- Intake and delivery distinguish continuing authority from new authority. A requested review does not grant integration rights, and branch policy cannot silently authorize push or PR creation.
- Review responsibilities have distinct questions and can reuse findings without inventing independent approval.
- TDD retains test-first as its default, preserves legitimate passing characterization, and treats baseline proof after an early patch as documented recovery rather than the ordinary workflow. Stop-signal lists are subject to the same applicability conditions.
- Shared report sections are compatible with the current `review-report.v1` schema, but schema compatibility does not demonstrate that agents will use them correctly.

### What was insufficient

1. **Reader-facing synchronization was incomplete.** The first pass changed only the English README, left its state date stale, and omitted the Chinese guide. This follow-up synchronizes both and provides the requested Chinese design record.
2. **The first semantic pass did not close every reference dependency.** Independent review found residual C4, duration, input-contract, hotfix-order, and authority conflicts. This self-review found another delivery gotcha that could convert an outcome into a PR without checking authority. These concrete conflicts were repaired; that does not establish that every rule in all 46 skills was deeply reviewed.
3. **Context reduction was not achieved by the static inventory.** Compared with the audited base, descriptions became shorter, but entry and body inventories grew. Conditional loading is an intended execution behavior, not measured savings.
4. **The September 8 execution boundary remained incomplete.** At that snapshot, reference-content evidence binding and the Claude adapter FIFO/draft-repair defects were still open; the September 9 follow-up below closes these implementations. These are implementation debts, not merely missing tests. Updating guidance and candidate hashes does not close them.
5. **Outcome quality remains an inference.** The ten revised skills have clearer branches, but the revision does not establish better architecture decisions, fewer accepted defects, or lower coordination cost. The existing checks establish packaging and contract consistency only.

| Static source inventory | Audited base | Current revision | Change |
|---|---:|---:|---:|
| Authored descriptions | 10,330 characters | 10,183 characters | -147 |
| Entry stack | 36,720 characters | 37,978 characters | +1,258 |
| Authored skill bodies | 160,785 characters | 164,452 characters | +3,667 |

These use the repository context meter's file inventory and the same calculation against `fd05978dbbbf5a064205a695af47c8a550f1b224`. They are neither runtime token counts nor a full reference-dependency inventory. Passing the existing budget is not evidence that this revision reduced context cost.

### Next useful work

Keep the revision at `review`. Complete the known execution-boundary repairs in a separate implementation slice. For design follow-up, inspect complete producer-to-consumer examples for an approved continuation, a brownfield change, and a release decision: every artifact should answer a real downstream question, and every additional step should have an owner and acceptance condition. Use the existing handoff for behavioral evaluation; do not add another orchestration layer or more checklists to compensate for the missing evidence.

## September 9 — Top Five Repairs

The follow-up closes five bounded issues without adding an orchestration layer:

| Issue | Implemented behavior | Boundary retained |
|---|---|---|
| Package evidence identity | `skill-package.v3` binds full `SKILL.md` and exported resource contents/paths; edits, additions, deletions, and renames invalidate old identity | Historical evidence and maturity are carried forward explicitly; rehashing is not new model evidence |
| FIFO intake blocking | Nonblocking open followed by regular-file validation rejects a FIFO promptly | Symlink, special-file, and snapshot checks still fail closed |
| Intake recovery | Complete canonical `Write` candidates are validated; malformed or draft briefs can be replaced; changed approved candidates request host confirmation | Drafts cannot authorize code writes, aliases cannot evade candidate validation, and no strict operator pin is inferred |
| Producer-to-consumer decisions | Reviews hand actionable blockers to the author; small task plans reuse approved outcomes and existing boundaries; preservation/discard can record failed verification | Integration still requires its approvals and passing evidence; strict completion and destructive-action authority remain separate |
| Repeated entry guidance | Consolidated entry/composition prose and removed duplicated priority explanations in the generated gateway | Input obligations, reference authority, scope changes, and workflow gates remain explicit |

Three producer-to-consumer walkthroughs informed the fourth repair. A requested review produces a consumable `review-report` even when integration is blocked. A small brownfield enhancement consumes approved scope and existing boundary references without manufacturing an architecture document. A failed verification can hand off an accurately incomplete preservation record while merge and successful completion remain blocked. These are design walkthroughs, not fresh model experiments.

Static inventory after this follow-up: descriptions 10,154 characters; entry stack 35,721; authored bodies 161,165. Entry text is 2,257 characters (5.9%) below the September 8 pass and 999 below the audited base. Skill bodies remain larger than the base because the decision branches are explicit. No overall runtime-token or model-quality improvement is claimed.

See the current [binding contract](../quality/evidence-content-binding.md), [adapter boundary](2026-07-16-claude-pretooluse-adapter.md), and [evaluation handoff](../../eval/meta/2026-09-08-skill-design-handoff.md) for reproducible checks and remaining behavioral work. All ten design candidates remain at `review`.

Final implementation verification: all 474 regression tests passed, along with repository validation, unchanged context budgets, and native parsing of 46 source and 40 curated skills. Maximum description length is 303 characters. Claude host UI confirmation and incremental model benefit remain unverified; no global installation or publication was performed.

## September 9 — Next Five Design Tasks

This wave follows the execution repairs and addresses decisions in six more authored packages. It changes existing instructions and handoffs, without introducing a scheduler, artifact type, dependency, or new evaluation framework.

| Task | Observed problem | Positive design change |
|---|---|---|
| 1. Receive review by dependency | One unclear item stopped every fix; item-by-item execution could repeat work for one root cause | Reconcile findings against the current revision, group by cause/decision, continue independent authorized corrections, and hand accepted fixes back for re-review |
| 2. Consume implementation inputs | Artifact names and a prior TDD step did not explain reuse, missing decisions, or continuation | Start from the accepted slice and current code/tests, require only applicable architecture/API decisions, and give review a concrete diff/evidence boundary |
| 3. Justify refactoring | A lower complexity/coupling metric could stand in for a real benefit; existing code appeared to require prior feature production | Compare one maintenance operation before/after, preserve explicit behavior, and justify added structure by current value rather than a metric quota |
| 4. Design verification by risk | Fixed layer percentages, coverage/journey/rerun counts, tool choices, and execution-only gates conflicted with a strategy-only task | Map risks to meaningful checks at the lowest sufficient layer, preserve explicit policy gates, and distinguish a planned strategy from actual test results |
| 5. Separate estimate from commitment | Unresolved work still needed an estimate, while plans lacked an explicit path for unknown capacity or ownership | Record ranges or unknowns, distinguish active work/waiting, avoid fabricated agent speedups, and publish provisional scope until capacity and commitment are supported |

The corresponding I/O contracts identify consumers and usable output content. Review response records preserve finding identifiers and remaining decisions. Feature/refactor handoffs preserve the changed revision and verification boundary. Strategy documents feed CI and selected E2E work; only actual execution produces a test report. Estimates feed a capacity-aware sprint plan. Existing document sections may carry these outputs where the governing workflow permits them.

Design walkthroughs cover an independent correction beside a disputed API comment, a feature continuation with accepted tests, a refactor that changes one maintenance operation, a strategy-only request without invented runs, and a vendor wait with unknown duration. These demonstrate contract reasoning, not measured agent outcomes.

Six packages move from `tested` to `review`: `pc-feature-development`, `pc-refactoring`, `pc-receiving-code-review`, `pc-testing-strategy`, `pc-estimation`, and `pc-sprint-planning`. Their previous evidence and package identities remain in the binding history. Overall maturity is now 2 production, 23 tested, and 21 review; sixteen changed design candidates await behavioral revalidation. The public surface remains 40 packages.

Static inventory for this wave: 9,978 description characters and 162,641 authored body characters; entry inventory remains 35,721. Existing budgets are unchanged. Validation results and deferred behavioral checks are recorded in the [handoff](../../eval/meta/2026-09-08-skill-design-handoff.md).

Wave verification: 76 focused checks, the repository validator, unchanged context budgets, and `git diff --check` passed. Native Gemini CLI 0.39.1 parsed 46 authored and 40 curated packages. Independent design review found no remaining substantive issue in the six packages and their workflow handoffs. The earlier 474-test full-suite result belongs to the execution-repair snapshot; this design wave did not repeat the full suite or run model evaluation.

## September 9 — Whole-Library Design Acceptance

### Approved route and scope

The user approved the proposed whole-library acceptance pass with an explicit instruction to proceed as recommended. This continues the existing design-improvement work and its deferral of model evaluation. Intake record: `artifact=intake-brief`, `schema_version=intake-brief.v1`, `status=approved`, `approver=user (current conversation)`, `work_type=Enhancement`, `entry_phase=05-quality`, `intake_mode=resume`, `workflow_primary=agile-sprint`, `recommended_next_skill=pc-code-review`, `source_language=zh-CN`, `artifact_record_language=en`, `user_presentation_locale=zh-CN`, `questions_asked=[]`, `routing_changed_by_answers=false`. The request is to close whole-library design gaps after the first sixteen candidate revisions. The unchanged route reuses the scope and authority established above; it adds no release or installation action. Quality target: `runtime_context=agent_internal_skill`, `exposure_profile=no_network_listener`, `production_target=Prodcraft source skills and generated guidance`, `non_targets=model benchmarks, global installation, deployment`, `evidence_refs=current user approval and this design record`. Scope covers all 46 authored packages; remaining risks are inconsistent reference instructions, unnecessary producer obligations, and unsupported completion claims.

### Acceptance plan

- [x] Read all thirty remaining main files and supporting instructions. For each, record applicability, required decisions, output consumers, missing-information behavior, and reference consistency. Reuse the existing reviews of the first sixteen and recheck their interfaces in the walkthroughs.
- [x] Repair evidence-backed design defects in existing source/reference contracts. Prefer a smaller applicable process over fixed quotas, new abstractions, and blanket approval loops. Keep required workflow gates and real authorization intact.
- [x] Trace three complete repository-grounded paths: a bug repair, a brownfield compatibility change, and delivery closeout. Identify the actual inputs consumed, decisions, outputs, stop conditions, and unnecessary steps. Label retrospective/design walkthroughs separately from fresh execution or model evaluation.
- [x] Synchronize changed package identities, evidence disposition, public registry and generated packages. Retain historical evidence and keep changed behavior at `review`.
- [x] Perform independent semantic review, native parsing, frontmatter/reference validation, unchanged context budgets, and affected deterministic checks. Update both reader languages and the existing evaluation handoff.

Acceptance ends when every authored skill has a stated design disposition, the three task chains have consumable handoffs, and substantive findings raised in this scope are resolved or explicitly identified as outside the approved scope. A design pass does not certify model efficacy, all hosts, or production maturity. Rollback remains a targeted reversal of this pass followed by regeneration, preserving the earlier candidates and unrelated changes.

### Accepted Result

The [whole-library acceptance record](../reviews/2026-09-09-skill-design-acceptance.md) now assigns all 46 packages a disposition: fourteen repairs independently reread, sixteen additional packages with no new substantive issue, and sixteen retained earlier reviews with handoff checks. The [three complete walkthroughs](../../examples/README.md) trace real repository changes and actual evidence across bug repair, brownfield migration, and delivery closeout. They are retrospective/design traces, not fresh model runs.

The fourteen repairs resolve fixed quotas, unsupported prerequisites, stage-approval contradictions, protocol assumptions, unsafe causal experiments, persistence overclaims, and inapplicable output obligations. PRD/RFC templates and agile/hotfix guidance are aligned with the corrected skill boundaries. Required release and independent-review gates remain intact.

All thirty revised contracts remain at `review`; aggregate maturity is 0 production, 13 tested, and 33 review. Historical evidence is preserved, and the public surface remains 40 packages. Final source inventory is 9,916 description characters, 35,721 entry-stack characters, and 162,062 body characters. The existing budgets were not loosened.

Final checks passed: all 474 repository tests (33.950 seconds), the repository validator, context budgets, native parsing of 46 authored and 40 curated packages, candidate/system identity checks, local file/heading links, and `git diff --check`. Model behavior, incremental value, and installed-host interaction remain handed off. This completes the approved design acceptance without promoting changed candidates or asserting release readiness.
