# Spec Summary

- `POST /v1/campaigns/{campaignId}/reassignments`
  - supported release-1 reassignment variants should succeed
  - unsupported variants must return `UNSUPPORTED_RELEASE1_FLOW`
- Exported evidence packages must remain available throughout brownfield coexistence.
- No public contract guarantees immediate legacy synchronization.
- Legacy-only historical campaigns may remain read-only if export and audit evidence remain intact.
- Reviewer hierarchy behavior for confirmed release-1 tenants must stay behaviorally compatible even if the implementation changes underneath.
