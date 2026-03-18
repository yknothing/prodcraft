# Test Strategy: Release-1 Reassignment Slice

## Risk-to-Layer Mapping

### Contract / Integration Priority

1. **Unsupported release-1 reassignment variants**
   - Contract/integration tests must verify the endpoint returns `UNSUPPORTED_RELEASE1_FLOW` with the documented error envelope.
2. **Authorized supported reassignment path**
   - Contract/integration tests verify the supported release-1 variant succeeds for allowed actors.
3. **Unauthorized or tenant-incompatible reassignment attempts**
   - Integration tests verify failure behavior for disallowed actors and fail-closed handling for unresolved tenant-policy cases.

### Brownfield / Coexistence Priority

4. **Legacy sync behavior remains non-committal at the public contract layer**
   - Tests should verify the public API does not promise unsupported immediate-sync semantics.
   - Any legacy adapter behavior should be covered with bounded integration tests, not assumed in public E2E.
5. **Regression protection for unsupported/deferred behavior**
   - Add a regression test so unsupported reassignment variants cannot silently fall back to a supported path.

### Unit Layer

6. **Validation and error-envelope shaping**
   - Unit tests cover reassignment-type validation and error construction.
7. **Authorization branch coverage**
   - Unit tests cover allowed vs forbidden actors and fail-closed policy handling.

### E2E Layer

8. **One critical happy-path release-1 reassignment journey**
   - Keep E2E scope narrow: one supported reassignment flow from request to visible success state.
   - Do not rely on E2E to carry unsupported-flow or contract-boundary coverage by itself.

## Execution Order

1. Add/repair contract tests for unsupported-flow and supported-flow behavior.
2. Add authorization and fail-closed integration coverage.
3. Add targeted unit coverage for validation/error shaping.
4. Keep a single high-value E2E flow for confidence.

## CI Placement

- **Push / PR gate**
  - unit tests for validation and authorization branches
  - integration/contract tests for supported and unsupported reassignment behavior
- **Nightly / broader quality gate**
  - critical happy-path E2E reassignment flow
  - any coexistence-focused integration suite that touches legacy adapters

## Explicit Gaps to Track

- If sync semantics are later decided, add tests for the agreed visibility behavior rather than assuming it now.
- When tenant-policy scope is closed, replace fail-closed placeholders with explicit compatibility-case tests.

## Downstream Handoff

- `ci-cd` should gate merge on the unit and integration/contract layers above.
- `code-review` should continue treating missing unsupported-flow coverage as review-relevant, not optional.
