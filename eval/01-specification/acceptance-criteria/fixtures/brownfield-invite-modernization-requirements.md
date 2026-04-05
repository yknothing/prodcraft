# Invite Modernization Requirements

## Goal

Modernize invite acceptance while preserving legacy coexistence and keeping unsupported paths visible.

## Reviewed Requirements

- Invite acceptance must work for the authenticated user only.
- The release 1 flow must coexist with the legacy permissions module.
- Unsupported tenant and legacy reassignment variants must stay out of scope for release 1.
- The flow must reject forged tenant identifiers.
- SQL injection attempts and malformed identifiers must be rejected.
- The user must see a clear failure when the invite is expired, already used, or not allowed for the current tenant.
