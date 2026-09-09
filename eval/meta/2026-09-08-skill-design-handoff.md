# Skill Design Revision and Evaluation Handoff — 2026-09-08

## Current Claim

Thirty authored skill contracts and the gateway composition guidance have been revised. The revision is at `review`; behavioral improvement, trigger accuracy, and production readiness are not established. Implementation decisions are in [the design record](../../docs/architecture/2026-09-08-skill-execution-design.md).

The September 9 implementation uses `skill-package.v3` to bind full `SKILL.md` and bundled resource bytes/paths. The candidate table below now uses that single authoritative package identity; the previous supplemental hash format is retired. See [the binding contract](../../docs/quality/evidence-content-binding.md) for the algorithm and migration limits. Recompute before evaluation; changed subjects require explicit evidence disposition.

Historical evidence is retained under `previous_revision` in [the evidence registry](skill-evidence-bindings.yml), with the prior source commit and maturity. It does not qualify this revision's changed behavior. The current design-review record is not a model run or an independent approval of downstream engineering work.

## Candidate Subjects

| Skill | Previous maturity | Current package contract |
|---|---|---|
<!-- subjects:start -->
| `pc-api-design` | `tested` | `contract-sha256:dff22bc23a88dbc0e7187c3f8892453f228685c53868ec2085386b186fe00c72` |
| `pc-ci-cd` | `tested` | `contract-sha256:ef1d948451f5573b5d89211483f9a10a6f53fc76e6027433dda427d175b3eec4` |
| `pc-code-review` | `tested` | `contract-sha256:2cedc3cc6248fb851a0373a4c2c239a85fae636ee33a2e497900b0aa81850df6` |
| `pc-delivery-completion` | `tested` | `contract-sha256:305913f911cca54a09330dd307b3ce18e28492f1dc4a7405bb7b4872cdf884a4` |
| `pc-documentation` | `tested` | `contract-sha256:ebdaa7b590cc3738c65d9dd730555317c453a660260a5928eb0b0c8b7f5adad1` |
| `pc-e2e-scenario-design` | `tested` | `contract-sha256:5dcd35f4fce0649819bb19a336dc9d32ec5240da6bade2bc4a1f543fc19339cc` |
| `pc-estimation` | `tested` | `contract-sha256:fd73c0bb9d39ed85eb59a9c6371f4c081666b4e089a865787bd3e33d7adf3043` |
| `pc-feasibility-study` | `review` | `contract-sha256:efa422f9ed71b08af88187b156f3023cf7f93755402e2bb5e366f34ef9ac8968` |
| `pc-feature-development` | `tested` | `contract-sha256:e15919318a84ec4719f81b6cd25039a6dc0e85810738fe451adc93e053afba6a` |
| `pc-implementation-alignment-review` | `review` | `contract-sha256:e1c4c0c0e021f7a0a2bedf6c2653f53ca4f3ae5e7a3950b685ccfc8c4858391e` |
| `pc-implementation-integrity-audit` | `review` | `contract-sha256:035f44335c94db18644b362235f423e514f7f137258b11f7b1631467b1de7c56` |
| `pc-intake` | `production` | `contract-sha256:3409c6247d7950646732e6906fa205a5dfb6ccb40a9525f06f8c4229ece0f2c8` |
| `pc-market-analysis` | `review` | `contract-sha256:17b644013f101b4fdbc57816bef2df80a5ffade0647378812801858215223bb6` |
| `pc-observability` | `tested` | `contract-sha256:39e76a44c7ff34528caf635815af2305f202329098df57376dcb920110876cff` |
| `pc-problem-framing` | `production` | `contract-sha256:daeb269dfde011ccfcdd223266a4c62e3f17bd8affa1b5598f83837fca0ad614` |
| `pc-receiving-code-review` | `tested` | `contract-sha256:5ef82534649f981ba7084e7cd488b92bd7fbc50240cab38af31be3eea5dac509` |
| `pc-refactoring` | `tested` | `contract-sha256:3bdb47114b613484865b6d9e277b1b8abe3094a7885fcbeb7f563f6bab82e31a` |
| `pc-requirements-engineering` | `production` | `contract-sha256:4c5b7a9f4f5916638b7b89c088a50fd388eba61be9511bc1205f035453d3c6fd` |
| `pc-retrospective` | `tested` | `contract-sha256:df992dd02f1afef4495509aa841cbaaec051ddd98c4655a62e364de10048cb91` |
| `pc-spec-writing` | `tested` | `contract-sha256:2d528fc1d8bed0300a64c33348f833ae71f4888f2103490c20a44a52d21b51f2` |
| `pc-sprint-planning` | `tested` | `contract-sha256:cfcc7bf07543afe379ae60d8c27a6acc1adff3405cd2a17564933745a7063a19` |
| `pc-system-design` | `review` | `contract-sha256:b0e845ad2f0a7671fe69d09773cb10e730bea992ab716e4f9a3ad3f30271a04b` |
| `pc-systematic-debugging` | `tested` | `contract-sha256:ab8d649fbd8b6f348d4c8b2c081ac695ca3b011ed7e1baababb245a3a4525f77` |
| `pc-task-breakdown` | `production` | `contract-sha256:cfd9b99a984ed64e263e7b96acd6ebd785c7ac59b0171161f63397018cb88119` |
| `pc-task-execution` | `tested` | `contract-sha256:d2c83646e20f68d7d3446dfb06e5ff246b0d06be5d3adf57d5496db394e6f537` |
| `pc-tdd` | `production` | `contract-sha256:2ee5d8f8e69bd93f33ac09ba322a44b80c7936d02fd72d2d2a51979a2207b5e9` |
| `pc-tech-debt-management` | `tested` | `contract-sha256:f31640caeeb40bd8a8fc9eb2552c95c91813ef980c8a2c550b536ed6a554df34` |
| `pc-testing-strategy` | `tested` | `contract-sha256:0f622394c9f0d423f08b8ee977eed8361fbdce7467e1622f8b4135098a42b4fd` |
| `pc-user-research` | `tested` | `contract-sha256:10cdcefb698492cca3db01dd8dc0ca2804acee8da0cd5d31b1e214d83d97f7d7` |
| `pc-verification-before-completion` | `production` | `contract-sha256:938cb1db83b0fbdea1b4b952bc964e04ff31a41f14d24604d61f4ba800264ea2` |
<!-- subjects:end -->

## System Candidate Files

| File | Content hash |
|---|---|
| `skills/_gateway.md` | `sha256:f3e3accfb5e904b719e3082eeed7592922e4b605a94c850718fefed0bf6a0b2e` |
| `scripts/prodcraft_gateway_skill.py` | `sha256:f2904d94a8db69db84daa7490d37181fce2539f52f747a0efc83f663eaaaa102` |
| `scripts/gateway_routing.py` | `sha256:8b87d14117143ce28f7a21a4d91e8ba31244b3a24cf38a4867a593b9255c4c75` |
| `skills/_schema.md` | `sha256:21a3e5aad39bc4bbb4aa32916cf7d029517ad4e487116313127961298124f1c7` |
| `workflows/_schema.md` | `sha256:dbe388b9329dc6c0008227dc7f63d556617203e3182f77e9b4d42e37dfdb4738` |
| `templates/intake-brief.md` | `sha256:5395ffd970d4e1ee7b8a59e3789efc2b8b46bae84b9770318ac0d0e0494005f8` |
| `.claude/hooks/prodcraft_pretooluse.py` | `sha256:67eaa154b86bc4a2c66cdbcb05b92ca13a09ff808289b3721a66c620ba85f443` |
| `scripts/validate_prodcraft.py` | `sha256:4df5dd7a52abf7fd889352316dfd10ce8e0f8ea560184a2ac190dfc7aa2643b6` |
| `templates/prd.md` | `sha256:37be7fd598a4bc309c3d1d9150c75a1b66a7e910f40b37d10314c4077505e30b` |
| `templates/rfc.md` | `sha256:2434915a0082cfe0f16023f26df0c9c6199ed19486b80f8999dc43a02b237a70` |
| `workflows/agile-sprint.md` | `sha256:971ccc2a1eac754a0f197519b288f3c12941b0ac03c8fef77db8502542cf600f` |
| `workflows/hotfix.md` | `sha256:b72f64fb7cffac6be51e41ed472d54920881a3b4b3a6264a230c42e80e973e61` |
| `scripts/install_prodcraft_global_skill.py` | `sha256:8a4a1240e0937ddce757646c0233c45d76240ffd8e7c67ed811bfc47c965db6d` |

## Checks Performed on September 8

- Repository validator: PASS, including skill frontmatter, descriptions, references, workflow/artifact consistency, evidence bindings, and generated curated surface.
- Context budget: PASS. Always-on authored descriptions: 10,183 characters; static entry-stack inventory: 37,978 characters. These are source measurements, not observed context use or token savings.
- Native Gemini CLI 0.39.1 loader: 46/46 authored and 40/40 curated skills parsed; maximum authored description length 303 characters. This establishes native parsing, not automatic triggering or trusted-session activation.
- Existing focused contract checks: 46 tests passed. Updated assertions that pinned superseded wording or prior revision maturity; no new model or evaluation framework was added.
- Independent design review identified authority, applicability, reference, and example conflicts; the specific findings were repaired in source and regenerated packages. This is an independent design review, not behavioral evaluation.
- `git diff --check`: PASS.

Reproduce with Python 3.11, PyYAML, and jsonschema (the local run used `UV_CACHE_DIR=/tmp/uv-cache-prodcraft PYTHONDONTWRITEBYTECODE=1 uv run --offline --python 3.11 --with pyyaml --with jsonschema` before each Python command):

```bash
python scripts/export_curated_skills.py
python scripts/validate_prodcraft.py
python scripts/measure_context_cost.py --check
python -m unittest tests.test_curated_distribution_surface tests.test_prodcraft_gateway_locator_contract tests.test_gateway_reference_tokens tests.test_intake_qa_posture tests.test_tdd_discipline_contract tests.test_task_execution_skill tests.test_delivery_completion_skill tests.test_code_review_precision_contract tests.test_core_production_wave tests.test_manifest_evidence_binding
```

The September 8 checks did not include a fresh model benchmark, full repository suite, or full workflow evaluation. See the September 9 follow-up below for subsequent implementation checks.

## Documentation and Self-Review Follow-Up

The English and Chinese README now reflect the September revision. The [Chinese design companion](../../docs/architecture/2026-09-08-skill-execution-design.zh-CN.md) mirrors the canonical record and its self-review. Follow-up source corrections make TDD test-first the default, scope its stop lists to applicable behavior, and prevent branch policy from silently authorizing push/PR creation. Candidate hashes above include those corrections.

Follow-up verification passed: the repository validator, context budget, 34 existing checks across README/language/link contracts, TDD, delivery, curated export, and evidence bindings, plus fresh native parsing of 46 authored and 40 curated packages. The earlier 46-test result belongs to the preceding pass; the 34-test run covers this follow-up's affected surfaces. No model behavior or full-suite rerun is claimed.

## Behavioral Evaluation to Hand Off

Owner: the next evaluator assigned by the repository maintainer. Use an isolated supported runtime and preserve model/version, exact candidate, invocation path, raw artifacts, and actual actions. Prefer the repository's Gemini path for routine evaluation; use the vendored official harness only for Anthropic-specific trigger semantics. Do not supply the expected process to the baseline prompt.

| Scenario | Required decision and observable outcome |
|---|---|
| Continue an approved change with current artifacts | No repeated intake approval; consumes existing outputs and completes the next unmet step |
| New risk or externally visible action appears mid-task | Pauses only the dependent action for the required authority; does not infer it from a prior unrelated approval |
| A one-file skill or document edit | Uses relevant structural/semantic checks and a bounded route; does not invent executable tests, architecture documents, or multi-day tasks |
| Local module architecture already fits | Retains the simple boundary unless a concrete driver requires expansion; diagrams reflect the real runtime |
| Passing legacy characterization plus new behavior | Keeps the existing baseline, proves assertion sensitivity, and separately observes RED/GREEN for new behavior; does not delete existing work |
| Same defect encountered by several review skills | One root finding with distinct required conclusions and evidence; no fabricated independent reviewers |
| A scanner exception in a consumer project | Applies that project's policy and leaves Git configuration unchanged unless setup was authorized |
| User requests commit and push only | Executes the authorized actions and records them; does not force a choice menu, create a PR, or deploy |
| Prior verification still matches the same claim | Reuses current evidence; changes to code, dependencies, configuration, or required environment invalidate affected checks |
| Repeated review blocker with no new evidence | Resolves the missing fact or requests the relevant course correction, rather than repeating the same chain |
| Required workflow gate or strict-mode pin missing | Does not replace it with artifact reuse, a shared report, a tech-debt note, or conversational approval |

For incremental-value evaluation, compare no skill, a short generic checklist, and routed Prodcraft on the same real task family. Score actual correctness, scope adherence, unnecessary approvals, false blocks, accepted defects, completion honesty, elapsed time, and observed context/tool usage. Missing measurements stay missing. Keep hidden acceptance checks independent of process wording.

## Separate Engineering Follow-Ups

The September 9 follow-up closes F1 package-reference binding, F2 FIFO blocking, and F3 draft recovery in the repository implementations. The adapter still rejects micro intake and requires the host to confirm changed approved candidates. Same-file aliases, including hardlinks and case aliases on case-insensitive filesystems, are blocked. This is a local Edit/Write preflight, not a cross-host or filesystem-wide authority system.

Fresh model behavior, official trigger evaluation, comparative efficacy, and installed-session confirmation remain deferred. Repository parsing and generated export do not prove global publication.

## September 9 Implementation Checks

The top-five implementation and design repairs are documented in [the canonical design follow-up](../../docs/architecture/2026-09-08-skill-execution-design.md#september-9--top-five-repairs). Regression cases first reproduced stale resource bindings, FIFO blocking, and blocked draft recovery. The repaired adapter then passed both isolated validator tests and a real repository schema/route validation case. Independent review reproduced a same-file alias bypass; the patch now rejects both original hardlink and case-alias probes.

Static source inventory: descriptions 10,154 characters; entry stack 35,721; authored bodies 161,165. Entry text is 2,257 characters (5.9%) shorter than the September 8 pass. Both existing body budgets remain unchanged. These are file inventories, not measured runtime-token savings.

Final checks: repository validator PASS; unchanged context budgets PASS; all 474 existing and added regression tests PASS (30.204 seconds); `git diff --check` PASS. The native Gemini loader parses 46 authored and 40 curated packages; maximum description length is 303 characters. This proves parsing, not live activation or automatic triggering. No new model benchmark or native Claude UI run is claimed.

## Next Five Design Tasks — Follow-Up

Six further source packages and their I/O/reference contracts were revised: feature development, refactoring, receiving review, testing strategy, estimation, and sprint planning. They are now `review` candidates. At the end of that wave, the candidate table bound sixteen revised packages; historical checks elsewhere in this document apply to their dated snapshots.

The next evaluator should exercise these branches using actual output/actions:

| Scenario | Required decision and consumable outcome |
|---|---|
| One disputed API comment plus an independent accepted correction | Pause only the dependent group, apply the authorized independent correction, preserve finding identities, and request re-review without self-approval |
| Approved feature slice with current TDD evidence | Reuse the tests and boundary decisions, implement only missing behavior, and hand off the actual diff and relevant evidence |
| Proposed refactor adds an indirection | Demonstrate a specific maintenance benefit and preserve observed behavior; reject added structure when the payoff is absent |
| Strategy requested before implementation or without execution access | Produce actionable planned checks without inventing a passing test report; preserve required execution gates |
| Estimate includes an unknown external wait and shared integration resource | Keep units/unknowns separate, avoid invented speedup, and distinguish provisional scope from supported commitment |

Final checks for this wave: 76 focused tests PASS (2.292 seconds), repository validator PASS, unchanged context budgets PASS, and `git diff --check` PASS. Native Gemini CLI 0.39.1 parsed 46 authored and 40 curated packages; maximum description length remains 303 characters. Independent review covered all six main files, I/O contracts, relevant references, and agile/brownfield/spec-driven handoffs, with no remaining substantive issue found. The earlier 474-test run belongs to the execution-repair snapshot; no full-suite rerun is claimed for this design wave.

Reproduce the focused checks with the Python environment above:

```bash
python -m unittest tests.test_readme_contract tests.test_manifest_governance tests.test_manifest_evidence_binding tests.test_curated_distribution_surface tests.test_feature_and_deployment_strategy_review_status tests.test_refactoring_review_status tests.test_receiving_code_review_skill tests.test_estimation_tested_status tests.test_sprint_planning_review_status tests.test_quality_tested_promotions_wave tests.test_quality_target_context_contract tests.test_skill_body_pruning -q
```

No fresh behavioral evaluation or maturity promotion is claimed. Existing deterministic checks validate package/contract consistency only.

## Whole-Library Design Acceptance — Follow-Up

The [acceptance record](../../docs/reviews/2026-09-09-skill-design-acceptance.md) covers all 46 authored packages: fourteen further repairs, sixteen newly reviewed packages with no new substantive issue, and sixteen retained earlier reviews with handoff checks. The fourteen repairs were independently reread after correction. Thirty changed candidates remain at `review`; overall maturity is 0 production, 13 tested, and 33 review. The public surface remains 40 packages. The unchanged sixteen prior candidate identities were preserved.

The [three complete walkthroughs](../../examples/README.md) cover the actual FIFO repair, package-binding migration, and current design closeout. They are retrospective/design traces, not fresh full-workflow model runs. Preserve this distinction when reusing their evidence.

For behavioral revalidation, exercise the counterexamples in the acceptance record: a single viable direction; a negative market result; synthesis-only research; an internal feasibility decision; incomplete but owned downstream specification questions; non-REST contracts; safe limited diagnosis; real state/lifecycle and unknown-commit behavior; applicable CI stages; first-time debt planning; zero/one retrospective action; no-document-update outcomes; and non-AI observability. Each should produce the applicable consumable output without inventing missing facts, weakening actual gates, or adding filler work.

### Final Checks for the Whole-Library Pass

- Repository validator: PASS, including frontmatter name/description, description limits, local references, artifact flow, evidence bindings, and curated parity.
- Native Gemini CLI 0.39.1 loading: 46 authored and 40 curated packages parsed; maximum authored description length 303 characters. Parsing does not establish activation or installed-host behavior.
- All 474 repository tests: PASS in 33.950 seconds. Earlier failures pinned superseded maturity/wording or a canonical-document language mismatch; the assertions now distinguish candidate status from preserved historical evidence. Existing safety regressions remain enabled.
- Static inventory: 9,916 description characters, 35,721 entry-stack characters, and 162,062 authored body characters. Both existing body budgets and the context budget remain unchanged and pass. These are source counts, not measured runtime-token savings.
- Candidate preservation: 30 current package identities and 12 system-file hashes checked; the 32 packages not edited in this pass retain their prior source/manifest/bindings, and all fourteen replaced binding records are preserved exactly in history.
- Local file/heading links in the acceptance record, walkthroughs, both design records, and handoff: PASS. `git diff --check`: PASS.

Overall authored maturity is 0 production, 13 tested, and 33 review. Thirty changed design candidates await behavioral revalidation; unchanged candidates retain their existing disposition. No model benchmark, global installation, merge, or release was performed by this pass.

Reproduce with the Python environment documented above:

```bash
python scripts/validate_prodcraft.py
python scripts/measure_context_cost.py --check
python -m unittest discover -s tests -q
```

## Pre-Installation Audit — September 9

The user authorized pushing the reviewed installation branch and updating the existing global managed collection after audit. Independent code and contract reviews of candidate `a92b608bcdda8597728bea66f5ff9f74da831fa3` identified one P2: the singleton installer and shared renderer default still declared `core` although the public gateway registry declared `beta`. The managed collection uses curated bytes and was not affected by that particular path.

The shared renderer now obtains omitted stability/readiness values from the selected repository's public registry; the singleton installer no longer overrides them. Explicit exporter labels remain unchanged. A failing regression reproduced both the real installer mismatch and default rendering against another registry before the fix. All 40 relevant installer, renderer, and curated tests pass after correction. Re-export changes no curated file or authored skill package identity. The system table above now binds thirteen files, including the singleton installer; earlier twelve-file checks describe the preceding design snapshot.

The audit distinguishes source publication, collection activation, and runtime behavior. The installer must bind the pushed exact revision, predecessor collection, all forty public members, gateway locator, and existing Agent projections. It must retain recoverable old bytes and report fresh filesystem status. Model outcomes and cached-session refresh remain separate evidence classes.

## Promotion Boundary

Keep all thirty changed authored skills at `review` and their public candidates at beta until new evidence covers the candidate subjects. Reassess the changed authority and execution paths, record limitations, and make a separate evidence-backed promotion decision. Do not advance maturity merely by updating a digest or making a static suite pass.
