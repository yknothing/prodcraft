# Review Report

## Blocking

1. **Unsupported release-1 variants are being accepted instead of rejected**
   - In `reassignments.py`, unsupported reassignment types are coerced into `manager_delegate` and return `200`. The reviewed contract says unsupported variants must return `UNSUPPORTED_RELEASE1_FLOW`. This is a correctness and scope-boundary violation, not a follow-up cleanup item.
2. **The changeset hard-codes immediate legacy synchronization without contract support**
   - `sync_to_legacy_now(...)` is called unconditionally for both supported and unsupported paths, even though the current contract and architecture leave sync semantics unresolved. This silently closes an upstream open question in implementation.

## Should-Fix

3. **Test coverage is missing the highest-risk release-boundary case**
   - The tests cover a supported happy path and a forbidden actor, but they do not cover unsupported reassignment variants returning the required structured error.
4. **Tenant-sensitive authorization behavior is under-specified in code and unprotected in tests**
   - The `TODO` comment around tenant-specific policy checks suggests unresolved policy behavior is being deferred into implementation. At minimum, tests should pin the currently supported/unsupported tenant cases or the code should fail closed.

## Question

5. **Is there an explicit release-1 decision for when legacy sync is user-visible?**
   - If not, this code should not commit the public behavior to immediate sync semantics yet.

## Summary

Do not merge as-is. The changeset currently violates the release-1 unsupported-flow contract and hard-codes an unresolved coexistence decision.
