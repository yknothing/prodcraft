# Testing Strategy Review

## Goal

Verify that `testing-strategy` turns a reviewed slice and its findings into a layered, risk-driven quality plan.

## Scenario

- `access-review-modernization-testing-strategy`

This is a brownfield modernization slice where:

- unsupported reassignment variants must fail explicitly
- sync semantics remain unresolved
- tenant authorization is partly unresolved
- coexistence risks still matter

## Artifacts Reviewed

- Manual baseline strategy: `manual-run-2026-03-17-access-review`
- Input fixtures:
  - `fixtures/access-review-modernization-task-slice.md`
  - `fixtures/access-review-modernization-api-contract.md`
  - `fixtures/access-review-modernization-review-findings.md`

## Baseline Findings

The baseline strategy is serviceable but generic:

- it mentions unit/integration/E2E layers
- it covers happy path and authorization at a high level

But it does not map the real slice risks to the right layers.

## With-Skill Findings

The skill-applied strategy is stronger on the dimensions that matter for lifecycle-aware quality:

- unsupported-flow behavior is treated as a contract/integration priority
- coexistence and sync uncertainty are preserved as explicit verification concerns
- E2E scope stays narrow while contract and integration coverage carry most of the risk
- downstream CI and QA handoff are clearer

## Assertion Review

| Assertion | Baseline | With skill | Notes |
|---|---|---|---|
| maps risk to layer | partial | pass | With-skill assigns unsupported-flow and coexistence to contract/integration layers explicitly. |
| preserves brownfield safety | partial | pass | Baseline is too generic; with-skill keeps coexistence visible. |
| uses contract-aware tests | partial | pass | With-skill grounds coverage in the reviewed API contract. |
| stays strategic | pass | pass | Both remain strategic, but with-skill is sharper. |
| prepares downstream handoff | partial | pass | With-skill gives clearer CI and execution guidance. |

## Conclusion

The first manual review suggests `testing-strategy` follows the same pattern as the rest of the core spine:

- it is more valuable as a routed/core workflow skill than as a discoverability-first skill
- its value comes from turning slice-specific risks into explicit layered verification

This is review-stage evidence only. The next step is an isolated benchmark for the same slice plus a non-brownfield feature slice.
