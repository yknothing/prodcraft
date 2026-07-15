# TDD Execution Plan: Release-1 Reassignment Flow

## RED

1. **Write a failing contract test for unsupported reassignment variants**
   - Assert `POST /v1/campaigns/{campaignId}/reassignments` returns `UNSUPPORTED_RELEASE1_FLOW` with the documented error envelope when the request uses a non-release-1 reassignment type.
2. **Write a failing authorization test for unsupported actor/tenant combinations**
   - Assert unauthorized reassignment attempts fail without leaking unsupported-path behavior.
3. **Write a failing happy-path contract test for one confirmed release-1 reassignment variant**
   - Use only the confirmed supported reassignment subset.
4. **If legacy behavior already exists, add a characterization test around coexistence-sensitive reassignment behavior**
   - Protect the brownfield boundary before implementation expands.

## GREEN

5. Implement the minimal routing/controller logic needed to satisfy the unsupported-flow contract test.
6. Implement the minimal authorization guard needed to satisfy the security/tenant boundary test.
7. Implement only the supported reassignment path needed to satisfy the happy-path test.

## REFACTOR

8. Refactor shared reassignment validation and unsupported-flow response shaping while keeping all tests green.
9. Consolidate test fixtures so supported and unsupported variants remain easy to extend without hiding release-1 boundaries.

## Explicit Constraints

- Do not implement reassignment variants that are still outside the confirmed release-1 subset.
- Do not fill tenant-specific policy gaps with guessed behavior; keep unsupported or unresolved cases explicit in tests.
- Keep the structured error contract stable while implementation evolves.

## Downstream Handoff

- `feature-development` should execute the slice in the RED -> GREEN -> REFACTOR order above.
- `testing-strategy` should incorporate the unsupported-flow and authorization tests into the broader contract/coexistence suite.
