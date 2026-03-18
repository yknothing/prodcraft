# API Contract Summary

- `POST /v1/campaigns/{campaignId}/reassignments`
  - supported release-1 reassignment variants should succeed
  - unsupported variants must return `UNSUPPORTED_RELEASE1_FLOW`
- No public contract guarantees immediate legacy synchronization.
