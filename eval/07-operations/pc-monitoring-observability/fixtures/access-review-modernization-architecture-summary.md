# Access Review Modernization Architecture Summary

- Release 1 supports direct owner reassignment for internal staff only.
- Partner-managed and bulk reassignment variants are unsupported and should fail with `UNSUPPORTED_RELEASE1_FLOW`.
- The legacy access-review service remains available for read-only coexistence and operator fallback.
- A sync worker propagates supported reassignment events to the legacy estate asynchronously.
- Immediate sync is not part of the public contract.
