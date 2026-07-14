# Password Reset Spec

## Scope

This release covers the password reset request and password reset completion flow for existing accounts.

## Non-Goals

- No social login changes
- No admin reset tooling
- No password policy redesign

## Constraints

- Reset links must be time-limited and single-use.
- The user experience must remain anonymous for unknown email addresses.
- Security errors must be visible enough for QA to verify but must not leak account existence.

## Open Questions

- None for this review slice.
