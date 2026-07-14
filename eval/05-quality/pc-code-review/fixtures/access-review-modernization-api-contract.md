# API Contract Summary

- `POST /v1/campaigns/{campaignId}/reassignments`
  - supported release-1 reassignment variants should succeed
  - unsupported variants must return `UNSUPPORTED_RELEASE1_FLOW`
- Authorization remains tenant-sensitive and partly unresolved
- No public contract guarantees immediate legacy synchronization
