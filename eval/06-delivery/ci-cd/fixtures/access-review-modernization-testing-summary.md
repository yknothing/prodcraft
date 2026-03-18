# Testing Strategy Summary

- Contract/integration tests must verify unsupported reassignment variants return `UNSUPPORTED_RELEASE1_FLOW`.
- Integration tests should protect coexistence boundaries.
- E2E scope should stay narrow: one critical happy-path reassignment journey.
- Sync semantics remain unresolved and should not be turned into assumed release guarantees.
