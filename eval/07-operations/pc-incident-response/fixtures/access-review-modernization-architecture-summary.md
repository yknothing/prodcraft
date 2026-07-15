# Access Review Modernization Architecture Summary

- Release 1 supports direct owner reassignment for internal staff only.
- Partner-managed and bulk reassignment variants are out of scope for release 1 and should fail with `UNSUPPORTED_RELEASE1_FLOW`.
- The legacy access-review service still exists for read-only coexistence and operator fallback.
- A sync worker propagates supported reassignment events into the legacy estate asynchronously.
- Sync timing is not contractually guaranteed to be immediate.
