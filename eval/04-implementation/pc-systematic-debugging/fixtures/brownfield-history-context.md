# Brownfield Defect History Context

> Synthetic, non-production QA fixture. Every `HIST-FIXTURE-*` identifier and
> lineage value below exists only to exercise the integration contract. This is
> not evidence from a live issue tracker, incident system, release record, or
> git repository.

## Retrieval Question

- Current failure: `test_reassignment_is_tenant_isolated` fails after cache
  cleanup when Tenant A warms the reassignment-policy cache before Tenant B
  requests policy for `project-42`.
- Affected boundary: tenant isolation across reassignment-policy authorization
  and caching.
- Search signals: the exact test name, `reassignment-policy`, `project-42`,
  cross-tenant policy reuse, and the cache-cleanup regression boundary.
- Retrieval goal: rank historical candidates that can narrow the current
  hypotheses. No historical record may establish the current root cause.

## `historical-defect-context`

### Probable match: `HIST-FIXTURE-202`

- Synthetic canonical source: fixture issue tracker
- Title: Tenant identity omitted from a reassignment-policy cache key
- Status: fixed in synthetic release `HIST-FIXTURE-RELEASE-2026.06`
- Affected boundary: two tenants using the same project id reused one cached
  reassignment policy after cache lifecycle work
- Match evidence: the historical symptom, component boundary, and project-only
  key signature align with the current retrieval signals
- Confidence: probable historical match, not proof of the current defect
- Current verification required: reproduce the current failure, log only the
  current computed cache key, and inspect the current key construction

### Useful analog: `HIST-FIXTURE-101`

- Synthetic canonical source: fixture incident tracker
- Title: Authorization guard reordered during cache cleanup
- Status: fixed in synthetic release `HIST-FIXTURE-RELEASE-2026.04`
- Affected boundary: authorization ran at the wrong point after cleanup
- Match evidence: the historical user-visible symptom was a cross-tenant policy
  leak after cleanup
- Mismatch: the historical record did not involve a shared cache entry id
- Confidence: useful analog only
- Current verification required: trace current authorization-guard entry before
  considering any authorization change

### Noise: `HIST-FIXTURE-303`

- Synthetic canonical source: fixture issue tracker
- Title: Cross-tenant feature-flag bleed in the notification service
- Status: closed
- Match evidence: keyword overlap on `cross-tenant`
- Mismatch: different service, endpoint, state store, and release boundary; no
  reassignment policy or cache-cleanup signal
- Confidence: noise; exclude from the current hypothesis loop

## `fix-lineage-brief`

| Record | Synthetic lineage | Historical change | Current authority |
|---|---|---|---|
| `HIST-FIXTURE-202` | issue -> `HIST-FIXTURE-COMMIT-202` -> `HIST-FIXTURE-PR-202` -> `HIST-FIXTURE-RELEASE-2026.06` | Added tenant identity to a historical reassignment-policy cache key and added a tenant-isolation regression test. | Hypothesis input only. Verify the current key and current reproduction. |
| `HIST-FIXTURE-101` | incident -> `HIST-FIXTURE-COMMIT-101` -> `HIST-FIXTURE-RELEASE-2026.04` | Restored the historical authorization-guard ordering. | Hypothesis input only. Reject or confirm with a current guard trace. |
| `HIST-FIXTURE-303` | issue -> `HIST-FIXTURE-COMMIT-303` | Corrected an unrelated feature-flag namespace. | No current action. |

## Recommended Next Action

Invoke `pc-systematic-debugging` against the current code and current failing
test. Use `HIST-FIXTURE-101` to order the authorization hypothesis and
`HIST-FIXTURE-202` to order the cache-key hypothesis, but require a deterministic
current reproduction and one-variable current experiments before accepting or
changing either boundary. Do not apply either historical patch directly.
