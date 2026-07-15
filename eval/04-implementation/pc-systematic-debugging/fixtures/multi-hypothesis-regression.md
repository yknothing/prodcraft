# Multi-Hypothesis Regression Record

## Failure Boundary

- Scenario id: `multi-hypothesis-regression`
- `test_reassignment_is_tenant_isolated` deterministically fails after a cache cleanup.
- Tenant B receives Tenant A's reassignment policy after Tenant A warms the cache.
- Expected: Tenant B receives its own policy. Actual: Tenant A's policy is reused.

## Recorded Journal

1. Hypothesis H1: the authorization guard was bypassed because the cleanup moved it.
   - Prediction: the guard trace will be absent for Tenant B.
   - One-variable experiment: add a trace at guard entry without changing code behavior.
   - Result: the guard runs and authorizes Tenant B correctly. H1 is rejected; no authorization patch was applied.
2. Hypothesis H2: the cache key omits tenant identity.
   - Prediction: the same cache entry id will appear for Tenant A and Tenant B.
   - One-variable experiment: log the computed cache key only.
   - Result: both requests use `reassignment-policy:project-42`; source inspection confirms the key contains project id only.

No fixes were stacked between H1 and H2.

## Completed Fix Evidence

- Smallest change: include tenant id in the reassignment-policy cache key; authorization code remains unchanged.
- With the fix applied: the original cross-tenant reproduction passes for 50 consecutive paired requests and the surrounding policy tests pass.
- With only that cache-key change removed: the original cross-tenant failure returns on the first paired request.
- Regression protection: retain `test_reassignment_is_tenant_isolated` and hand the verified boundary to `pc-tdd`.
