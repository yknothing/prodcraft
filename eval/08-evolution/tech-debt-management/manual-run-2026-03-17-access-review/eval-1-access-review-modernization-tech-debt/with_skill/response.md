# Technical Debt Registry

## Prioritized Debt Items

| Priority | Debt item | Why it is debt | Owner | Target | Success signal | Next lifecycle destination |
|---|---|---|---|---|---|---|
| 1 | Missing fail-closed enforcement for unsupported reassignment variants across contract, runtime guard, and delivery verification | The same boundary gap appeared in review, testing, delivery, and incident response. It creates recurring reliability risk every release. | Backend lead | Next sprint | Unsupported partner-managed requests are rejected consistently in contract tests, runtime guardrails, and release verification. | intake -> planning -> implementation |
| 2 | Weak rollback and fail-closed operational procedure for this modernization seam | Containment depended on improvised operational decisions instead of a prepared repeatable path. | DevOps lead | Next sprint | Runbook and delivery checklist cover rollback and route-level guard activation for this slice. | intake -> delivery / operations |
| 3 | Unresolved sync semantics between modernized flow and legacy estate | The system keeps leaking "immediate sync" assumptions because the boundary is not explicit. This will keep generating bugs and review churn. | Tech lead + architect | Before next scope expansion | Requirements and architecture define the sync contract explicitly, and downstream code no longer guesses. | intake -> specification / architecture |

## Not Treated as Technical Debt

- "Improve incident communication" is operational process work, not core structural debt by itself. It should still be handled, but outside the top debt registry.
- "Refactor the whole access-review service" is too broad to prioritize without evidence of specific leverage.

## Capacity Guidance

- Reserve a defined slice of the next sprint for the top two debt items.
- Re-evaluate the third item at the next scope-planning boundary, because it blocks safe expansion of the modernization effort.
