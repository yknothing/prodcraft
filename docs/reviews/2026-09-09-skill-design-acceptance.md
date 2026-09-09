# Whole-Library Skill Design Acceptance — 2026-09-09

## Scope and Acceptance Boundary

The user approved whole-library design acceptance after sixteen earlier skill revisions. This pass reviews the remaining thirty main files and all their 91 supporting reference files, then checks the interfaces of the earlier sixteen through bug repair, brownfield change, and delivery closeout. Source is the current uncommitted worktree based on `fd05978dbbbf5a064205a695af47c8a550f1b224`.

This is semantic design acceptance, not a new model benchmark, all-host certification, security certification, or production promotion. The [September 8 audit](bs-skill-auditor/2026-09-08-health-report.md) remains historical. The [design record](../architecture/2026-09-08-skill-execution-design.md) holds the approved scope; [candidate identities and evaluation handoff](../../eval/meta/2026-09-08-skill-design-handoff.md) define the exact revised packages.

Acceptance criteria:

1. Every authored skill has a design disposition based on its main instructions, reference contracts, or explicitly retained earlier review.
2. Entry, decisions, output consumers, missing-information behavior, and approval boundaries are coherent for the skill's actual scope.
3. The three complete task chains identify useful handoffs without invented artifacts, repeated producers, or silent gate waivers.
4. Substantive findings raised in this pass are closed by source changes and independent follow-up review.
5. Metadata, evidence disposition, public generation, loading, references, and existing context budgets agree with the final source.

## Coverage and Disposition

`Repaired` means the identified design issue was corrected and independently reread, not that changed model behavior has been measured. `No new issue` is a bounded semantic-review conclusion, not a universal absence-of-defects claim. `Retained review` reuses the earlier exact package review and checks its current handoff; these sixteen packages were not rewritten in this pass.

| Skill | Coverage / disposition | Decision or handoff checked |
|---|---|---|
| [pc-intake](../../skills/00-discovery/pc-intake/SKILL.md) | Retained earlier review; handoff checked | Accepted scope, applicable inputs, current evidence, and distinct downstream responsibility. |
| [pc-problem-framing](../../skills/00-discovery/pc-problem-framing/SKILL.md) | Main + all references; repaired F01 | Compare real choices; preserve a single approved direction when constraints exclude alternatives. |
| [pc-market-analysis](../../skills/00-discovery/pc-market-analysis/SKILL.md) | Main + all references; repaired F02 | Cover relevant alternatives and allow a supported no-opportunity conclusion. |
| [pc-user-research](../../skills/00-discovery/pc-user-research/SKILL.md) | Main + all references; repaired F03 | Accept sufficient intake/system context; separate study planning from synthesis of existing evidence. |
| [pc-feasibility-study](../../skills/00-discovery/pc-feasibility-study/SKILL.md) | Main + all references; repaired F04 | Assess actual internal/commercial value and uncertainty without mandatory market work or POC. |
| [pc-requirements-engineering](../../skills/01-specification/pc-requirements-engineering/SKILL.md) | Main + all references; repaired F05 | Accept an approved concrete request and keep unsourced numerical targets unresolved. |
| [pc-spec-writing](../../skills/01-specification/pc-spec-writing/SKILL.md) | Main + all references; repaired F06 | Approve the next stage while preserving owned downstream questions; align PRD/RFC templates. |
| [pc-domain-modeling](../../skills/01-specification/pc-domain-modeling/SKILL.md) | Main + all references; no new issue | Business vocabulary and invariants remain separate from database and API design. |
| [pc-acceptance-criteria](../../skills/01-specification/pc-acceptance-criteria/SKILL.md) | Main + all references; no new issue | Observable, negative, and boundary criteria feed TDD and quality work. |
| [pc-system-design](../../skills/02-architecture/pc-system-design/SKILL.md) | Retained earlier review; handoff checked | Accepted scope, applicable inputs, current evidence, and distinct downstream responsibility. |
| [pc-data-modeling](../../skills/02-architecture/pc-data-modeling/SKILL.md) | Main + all references; no new issue | Authority, transactions, lifecycle, and migration constraints shape the data design. |
| [pc-security-design](../../skills/02-architecture/pc-security-design/SKILL.md) | Main + all references; no new issue | Actual trust boundaries, misuse paths, controls, and residual risks drive decisions. |
| [pc-tech-selection](../../skills/02-architecture/pc-tech-selection/SKILL.md) | Main + all references; no new issue | Only unresolved categories are compared; operational and migration costs justify choices. |
| [pc-api-design](../../skills/02-architecture/pc-api-design/SKILL.md) | Main + all references; repaired F07 | Specify the existing REST, GraphQL, gRPC, event, or in-process contract on its own terms. |
| [pc-task-breakdown](../../skills/03-planning/pc-task-breakdown/SKILL.md) | Retained earlier review; handoff checked | Accepted scope, applicable inputs, current evidence, and distinct downstream responsibility. |
| [pc-estimation](../../skills/03-planning/pc-estimation/SKILL.md) | Retained earlier review; handoff checked | Accepted scope, applicable inputs, current evidence, and distinct downstream responsibility. |
| [pc-risk-assessment](../../skills/03-planning/pc-risk-assessment/SKILL.md) | Main + all references; no new issue | Material risks change scope, sequencing, estimation, or acceptance. |
| [pc-sprint-planning](../../skills/03-planning/pc-sprint-planning/SKILL.md) | Retained earlier review; handoff checked | Accepted scope, applicable inputs, current evidence, and distinct downstream responsibility. |
| [pc-tdd](../../skills/04-implementation/pc-tdd/SKILL.md) | Retained earlier review; handoff checked | Accepted scope, applicable inputs, current evidence, and distinct downstream responsibility. |
| [pc-systematic-debugging](../../skills/04-implementation/pc-systematic-debugging/SKILL.md) | Main + all references; repaired F08 | Separate identity from reachability, count failed hypotheses, and permit safe limited diagnoses. |
| [pc-task-execution](../../skills/04-implementation/pc-task-execution/SKILL.md) | Retained earlier review; handoff checked | Accepted scope, applicable inputs, current evidence, and distinct downstream responsibility. |
| [pc-feature-development](../../skills/04-implementation/pc-feature-development/SKILL.md) | Retained earlier review; handoff checked | Accepted scope, applicable inputs, current evidence, and distinct downstream responsibility. |
| [pc-refactoring](../../skills/04-implementation/pc-refactoring/SKILL.md) | Retained earlier review; handoff checked | Accepted scope, applicable inputs, current evidence, and distinct downstream responsibility. |
| [pc-code-review](../../skills/05-quality/pc-code-review/SKILL.md) | Retained earlier review; handoff checked | Accepted scope, applicable inputs, current evidence, and distinct downstream responsibility. |
| [pc-implementation-alignment-review](../../skills/05-quality/pc-implementation-alignment-review/SKILL.md) | Retained earlier review; handoff checked | Accepted scope, applicable inputs, current evidence, and distinct downstream responsibility. |
| [pc-implementation-integrity-audit](../../skills/05-quality/pc-implementation-integrity-audit/SKILL.md) | Retained earlier review; handoff checked | Accepted scope, applicable inputs, current evidence, and distinct downstream responsibility. |
| [pc-receiving-code-review](../../skills/05-quality/pc-receiving-code-review/SKILL.md) | Retained earlier review; handoff checked | Accepted scope, applicable inputs, current evidence, and distinct downstream responsibility. |
| [pc-testing-strategy](../../skills/05-quality/pc-testing-strategy/SKILL.md) | Retained earlier review; handoff checked | Accepted scope, applicable inputs, current evidence, and distinct downstream responsibility. |
| [pc-e2e-scenario-design](../../skills/05-quality/pc-e2e-scenario-design/SKILL.md) | Main + all references; repaired F09 | Verify the actual state source, lifecycle, allocation, and failure-recovery contract. |
| [pc-security-audit](../../skills/05-quality/pc-security-audit/SKILL.md) | Main + all references; no new issue | Evidence and exploit paths are calibrated to the actual target and exposure. |
| [pc-ci-cd](../../skills/06-delivery/pc-ci-cd/SKILL.md) | Main + all references; repaired F10 | Select validation/build/deployment stages for the actual artifact and authority. |
| [pc-delivery-completion](../../skills/06-delivery/pc-delivery-completion/SKILL.md) | Retained earlier review; handoff checked | Accepted scope, applicable inputs, current evidence, and distinct downstream responsibility. |
| [pc-deployment-strategy](../../skills/06-delivery/pc-deployment-strategy/SKILL.md) | Main + all references; no new issue | Risk selects rollout, stop/continue signals, and the recovery runbook. |
| [pc-release-management](../../skills/06-delivery/pc-release-management/SKILL.md) | Main + all references; no new issue | Delivery decisions feed scoped go/no-go, ownership, and release coordination. |
| [pc-incident-response](../../skills/07-operations/pc-incident-response/SKILL.md) | Main + all references; no new issue | Containment, impact, preserved evidence, and observed recovery are distinguished. |
| [pc-monitoring-observability](../../skills/07-operations/pc-monitoring-observability/SKILL.md) | Main + all references; no new issue | User-impact signals lead to actionable alerts and responsible owners. |
| [pc-runbooks](../../skills/07-operations/pc-runbooks/SKILL.md) | Main + all references; no new issue | Preconditions, branches, expected observations, and escalation are actionable. |
| [pc-tech-debt-management](../../skills/08-evolution/pc-tech-debt-management/SKILL.md) | Main + all references; repaired F11 | Accept initial evidence and distinguish proposed remediation from committed capacity. |
| [pc-retrospective](../../skills/08-evolution/pc-retrospective/SKILL.md) | Main + all references; repaired F12 | Choose only useful owned actions, including zero, and accept ordinary delivery evidence. |
| [pc-documentation](../../skills/cross-cutting/pc-documentation/SKILL.md) | Main + all references; repaired F13 | Follow current conditional obligations and allow a justified no-update outcome. |
| [pc-observability](../../skills/cross-cutting/pc-observability/SKILL.md) | Main + all references; repaired F14 | Separate application and AI telemetry, reusable signal contracts, and runtime claims. |
| [pc-bug-history-retrieval](../../skills/cross-cutting/pc-bug-history-retrieval/SKILL.md) | Main + all references; no new issue | Canonical versions and fix lineage narrow hypotheses without supplying authority. |
| [pc-verification-before-completion](../../skills/cross-cutting/pc-verification-before-completion/SKILL.md) | Retained earlier review; handoff checked | Accepted scope, applicable inputs, current evidence, and distinct downstream responsibility. |
| [pc-accessibility](../../skills/cross-cutting/pc-accessibility/SKILL.md) | Main + all references; no new issue | Affected user behavior determines checks and minimal remediation. |
| [pc-internationalization](../../skills/cross-cutting/pc-internationalization/SKILL.md) | Main + all references; no new issue | Affected strings, formats, fallback, and locale behavior have scoped verification. |
| [pc-compliance](../../skills/cross-cutting/pc-compliance/SKILL.md) | Main + all references; no new issue | Sourced obligations map to engineering controls, evidence, and explicit gaps. |

## Findings and Repairs

| Finding | Concrete rejected or misleading path before repair | Repair and final boundary |
|---|---|---|
| F01 Framing choices | Fixed approved constraints leave only one viable direction, but two or three are required | Explain exclusions and remaining decisions; genuinely new scope/direction still needs approval |
| F02 Market evidence | A narrow market has fewer than five relevant alternatives, or evidence supports no entry | Cover relevant alternatives and source limits; a negative conclusion is a valid result |
| F03 Research entry and outcome | Existing-system evidence has no market document; completed interviews need synthesis without a new plan | Accept sufficient context and approved direction; plan and evidence-backed findings have separate applicability |
| F04 Feasibility | An internal migration has costs and operational benefits but no revenue model | Assess actual value, cost, constraints, and unknowns; missing decisive evidence blocks commitment |
| F05 Requirements | A concrete approved intake cannot start requirements, while a reference demands universal quantification | Accept the supplied outcome and scope; source numbers or record owned questions |
| F06 Specification | Product contract is clear but architecture must resolve synchronization; all questions must nevertheless be closed | State approval stage and dependent work; carry owned questions forward without authorizing dependent implementation |
| F07 API contracts | Event or local function contracts cannot satisfy REST-centric methods and schema gates | Preserve transport and specify its real semantics, compatibility, and caller expectations |
| F08 Debugging | Probe/add-fix/remove-probe triggers a third-edit stop; missing marker erases valid evidence; production harm must be replayed | Count real failed hypotheses, separate identity/reachability, use safe negative controls, and report limited diagnosis without a fixed claim |
| F09 E2E truth | SPA navigation is treated as server persistence; reload/backgrounding and business rules are assumed universally | Match state source, lifecycle, reservation, retry, and recovery policy; unknown commit outcome requires reconciliation |
| F10 CI/CD | A documentation or native/CLI repository must have service staging, containers, every test type, and a fixed time limit | Select applicable stages/platform and evidence; retain actual release/rollback obligations |
| F11 Debt planning | First debt registration or non-sprint work must invent capacity commitment and historical trends | Start with evidence and a baseline; separate a proposed plan from authorized resources |
| F12 Retrospective | One useful action is expanded to three; ordinary delivery needs incident inputs | Permit zero/one justified actions, ordinary delivery evidence, and explicit scheduling decisions |
| F13 Documentation | Conditional/no-update path still requires generated-doc CI and publication | Resolve actual matrix obligations; update the smallest authoritative page or record why none is needed |
| F14 Observability | A normal request handler must emit skill/model/token data | Scope fields to the real boundary; preserve exact-versus-estimated accounting and design/runtime evidence |

The independent reread found three additional edge cases within F02/F03/F09: negative market results, synthesis-only research, and waitlist/offline/unknown-commit behavior. Those were corrected and rechecked. Workflow adaptation now permits an evidenced no-new-action retrospective and explicitly prevents self-review from supplying required independent approval. A missing hotfix staging environment requires an approved alternative route; a canary does not silently pass the existing gate.

The browser lifecycle correction uses [MDN sessionStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage) and [Chrome Page Lifecycle guidance](https://developer.chrome.com/docs/web-platform/page-lifecycle-api), checked September 9. The remaining business assertions derive from the declared product contract, not a universal shopping-cart policy.

## Complete Task Chains

The [repository-grounded walkthroughs](../../examples/README.md) show each entry, consumed input, decision, output, and terminal boundary. They use real source changes and retained evidence from this work. They are retrospective/design traces, not newly executed end-to-end model sessions or proof that every historical step invoked the named skill.

- **Bug repair:** FIFO reproducer and adapter correction. Debugging hands causal evidence to TDD/review; a passing local check does not establish installed-host behavior.
- **Brownfield change:** package-identity migration. Existing public shape and historical evidence are preserved; a new identity does not inherit a new benchmark result.
- **Delivery closeout:** this approved design pass. Current checks and source identities feed a scoped design-completion record; local preservation does not imply merge, global installation, or release.

Cost inspection removes no required gate: existing approved scope replaces duplicate plans, preserved negative evidence avoids destructive replay, explicit no-op outcomes avoid filler artifacts, and one canonical record can serve multiple consumers. Whether agents execute these choices efficiently remains a behavioral-evaluation question.

## Verification

- Repository validator: PASS, including frontmatter name/description, description limits, local references, artifact flow, evidence bindings, and curated parity.
- Native Gemini CLI 0.39.1 loading: 46 authored and 40 curated packages parsed; maximum authored description length 303 characters. Parsing does not establish activation or installed-host behavior.
- All 474 repository tests: PASS in 33.950 seconds. Earlier failures pinned superseded maturity/wording or a canonical-document language mismatch; the assertions now distinguish candidate status from preserved historical evidence. Existing safety regressions remain enabled.
- Static inventory: 9,916 description characters, 35,721 entry-stack characters, and 162,062 authored body characters. Both existing body budgets and the context budget remain unchanged and pass. These are source counts, not measured runtime-token savings.
- Candidate preservation: 30 current package identities and 12 system-file hashes checked; the 32 packages not edited in this pass retain their prior source/manifest/bindings, and all fourteen replaced binding records are preserved exactly in history.
- Local file/heading links in the acceptance record, walkthroughs, both design records, and handoff: PASS. `git diff --check`: PASS.

Overall authored maturity is 0 production, 13 tested, and 33 review. Thirty changed design candidates await behavioral revalidation; unchanged candidates retain their existing disposition. No model benchmark, global installation, merge, or release was performed by this pass.

## Remaining Work Outside This Acceptance

- Fresh behavior and incremental-value evaluation of revised candidates, using the existing handoff and exact subjects.
- Installed-host interaction, including Claude confirmation and environment provisioning.
- Comparative process cost and user outcomes on real project tasks.

Do not treat these deferred classes as resolved or as evidence of a current defect. Do not create additional infrastructure to replace the missing measurements.
