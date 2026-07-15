# Invite Modernization Spec

## Scope

This release covers invite acceptance in a brownfield environment where the legacy permissions module remains live.

## Non-Goals

- No legacy module replacement
- No tenant migration work
- No cross-tenant reassignment

## Constraints

- The authenticated actor must be the only actor allowed to accept the invite.
- The release must preserve coexistence with the legacy permissions module.
- Errors must make unsupported paths explicit without suggesting the legacy boundary has moved.

## Open Questions

- None for this review slice.
