# Brownfield History-to-TDD Integration Review

## Decision

The current contract-level integration is **PASS** for the behavioral chain:

`pc-bug-history-retrieval -> pc-systematic-debugging -> bounded pc-tdd handoff`

This is not a claim that a live history connector was queried or that `pc-tdd`
executed a RED-GREEN-REFACTOR cycle. The upstream history is an explicitly
synthetic, non-production fixture, and the downstream evidence establishes
handoff readiness only.

The sealed systematic-debugging packet is acceptance-ready: the with-skill arm
passed 12/12 machine-scored cases and the independent judge passed all 24/24
cases. The baseline arm also passed every assertion, so this review makes no
incremental efficacy claim for explicit skill loading.

## Evidence Reviewed

- `fixtures/brownfield-history-context.md`
- `fixtures/multi-hypothesis-regression.md`
- `fixtures/structured-response-contract.md`
- sealed packet `evidence/codex-gpt56sol-2026-07-16/review.md`
- sealed packet `evidence/codex-gpt56sol-2026-07-16/final-score-summary.json`
- sealed Scenario A with-skill responses:
  - `responses/multi-hypothesis-regression--run-01--with-skill.json`
  - `responses/multi-hypothesis-regression--run-02--with-skill.json`
  - `responses/multi-hypothesis-regression--run-03--with-skill.json`
- the current `pc-bug-history-retrieval`, `pc-systematic-debugging`, and
  `pc-tdd` skill contracts
- current manifest `artifact_flow`

## Scenario State Progression

1. Synthetic canonical history ranks an authorization analog
   (`HIST-FIXTURE-101`) and a probable cache-key match
   (`HIST-FIXTURE-202`). Neither is treated as current proof.
2. The current failure is reproduced deterministically with
   `test_reassignment_is_tenant_isolated` after cache cleanup.
3. The current authorization hypothesis is tested with a guard-entry trace and
   rejected; no authorization patch is applied.
4. The current cache-key hypothesis is tested independently. Both tenant
   requests use `reassignment-policy:project-42`, and current source inspection
   confirms the project-only key.
5. The smallest boundary is exercised both ways: adding tenant identity makes
   the original reproduction and surrounding policy tests pass; removing only
   that change restores the original failure.
6. Only the confirmed cache-key boundary is handed to `pc-tdd`, with the
   existing regression test as the required RED state and authorization kept
   outside the implementation slice.

## Gate Review

| Gate | Judgment | Evidence |
|---|---|---|
| History query is grounded in current signals | pass | The fixture uses the exact test, component, tenant boundary, project id, and cache-cleanup transition. |
| History candidates are traceable and classified | pass | Synthetic canonical IDs and lineage are recorded; candidates are separated into probable, useful analog, and noise. |
| History narrows hypotheses without replacing current evidence | pass | The fixture explicitly prohibits applying an old patch; Scenario A performs a fresh reproduction and current experiments. |
| Current reproduction is deterministic | pass, 3/3 | Every sealed with-skill response records the same Tenant A warm / Tenant B leak reproduction. |
| Obvious authorization hypothesis is falsified on current behavior | pass, 3/3 | Every response records the current guard trace, rejects H1, and applies no authorization patch. |
| Cache-key cause is confirmed on current behavior | pass, 3/3 | Every response records the shared computed key plus current source inspection. |
| Experiments change one variable and do not stack fixes | pass, 3/3 | `one_variable_per_iteration=true` and `fix_stacking=false` in every response. |
| Causality is proven in both directions | pass, 3/3 | `with_fix_passed=true` and `fix_removed_failure_returned=true` in every response. |
| Fix boundary is the smallest safe change | pass, 3/3 | Every response limits the change to tenant identity in the cache key and preserves authorization. |
| TDD receives only the confirmed boundary | pass for handoff readiness | Every response retains the exact regression test and routes only to `pc-tdd` after the report contains current root-cause and two-way evidence. |

## Artifact and Behavioral Handoff Boundary

The first edge is a declared artifact edge:

- `pc-bug-history-retrieval` produces `historical-defect-context` and
  `fix-lineage-brief`
- `pc-systematic-debugging` declares both as inputs

The second edge is intentionally reviewed as a behavioral translation, not a
direct manifest artifact edge:

- `pc-systematic-debugging` produces `bug-fix-report`
- `pc-tdd` does not declare `bug-fix-report` as an input; it declares
  `acceptance-criteria-set`, `api-contract`, and `task-list`
- the current manifest does not list `pc-tdd` as a direct consumer of
  `bug-fix-report`

For this scenario, the confirmed report is translated into bounded TDD inputs:

- task slice: add tenant identity to the reassignment-policy cache key only
- RED evidence: run the existing `test_reassignment_is_tenant_isolated` in the
  fix-removed state and observe the recorded cross-tenant failure
- acceptance criteria: the original paired-request reproduction passes, 50
  consecutive pairs pass, and surrounding policy tests remain green
- protected boundary: authorization behavior and unrelated policy behavior do
  not change
- excluded work: authorization refactors, speculative cache redesign, and any
  direct application of a historical fixture patch

No `api-contract` change is inferred because the confirmed defect is an
internal isolation failure under the existing policy contract. If the current
implementation reveals a public contract change, the handoff must stop and
route upstream rather than inventing one inside TDD.

## Adversarial Review

| Attack | Result |
|---|---|
| Historical authorization incident anchors the fix | resisted: current guard trace rejects H1 and no authorization code changes. |
| Probable historical cache-key match is accepted as proof | resisted: current deterministic reproduction, current key logging, and current source inspection are still required. |
| Hindsight rewrites the rejected hypothesis away | resisted: all three journals retain H1 before H2. |
| Multiple fixes are stacked | resisted: all three responses record one-variable experiments and no fix stacking. |
| A one-way green test is called causality | resisted: all three responses include fix-applied and fix-removed evidence. |
| A direct `bug-fix-report -> pc-tdd` artifact edge is invented | resisted: this review records the actual manifest gap and the required translation. |
| TDD expands from an unconfirmed historical match | resisted: the TDD task is derived only from the current confirmed cache-key boundary. |

## Limits and Follow-up

- The history fixture proves contract shape and anti-anchoring behavior, not live
  connector availability or production defect lineage.
- The sealed packet proves reliable production of the declared debugging
  response surface, not improvement over baseline.
- The packet records a `pc-tdd` handoff but does not execute TDD. A future
  execution drill should observe the fix-removed RED state, the minimum GREEN
  change, and a bounded refactor decision.
- The evidence supports the current skill contract only. Any future edit to a
  contract-bearing section requires a new contract digest and evidence review.
