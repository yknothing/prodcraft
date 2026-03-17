# CI/CD Pipeline Outline: Release-1 Reassignment Slice

## PR / Pre-Merge Gates

1. **Lint and static validation**
2. **Build**
3. **Unit tests for validation and authorization branches**
4. **Contract/integration tests for supported vs unsupported reassignment behavior**
5. **Integration check that release-1 code does not assume unsupported immediate legacy-sync guarantees**

If any of steps 3-5 fail, the pipeline stops before merge.

## Merge-to-Main / Staging Gates

6. **Package release candidate artifact**
7. **Deploy to staging**
8. **Run narrow happy-path E2E reassignment flow**
9. **Run coexistence-focused integration verification against staging adapters**

If staging E2E or coexistence verification fails, production deployment is blocked.

## Production Release Gate

10. **Manual or controlled approval gate**
    - Reviewer confirms that unsupported-flow, contract, and coexistence checks all passed.
11. **Deploy to production using a staged or fail-closed pattern**
12. **Run immediate smoke checks for reassignment endpoint contract and error behavior**

## Rollback / Safety

- Rollback must be scripted and ready before production deployment.
- Any signal that unsupported variants are being accepted or sync semantics are misrepresented should trigger rollback.

## Notifications

- Notify on PR gate failures and staging/production deployment failures.
- Include links to failing contract or coexistence stages to speed diagnosis.

## Downstream Handoff

- `deployment-strategy` should decide the exact rollout pattern using this gate structure as the baseline.
- `release-management` should coordinate approval timing and stakeholder communication around the production gate.
