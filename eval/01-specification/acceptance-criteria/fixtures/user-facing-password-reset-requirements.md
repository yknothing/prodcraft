# Password Reset Requirements

## Goal

Users must be able to reset their password through a verified email link without exposing account data or allowing expired links to succeed.

## Reviewed Requirements

- A user can request a password reset using an email address.
- The system sends a reset link to the address only when the account exists.
- Reset links expire after 24 hours.
- A reset link can be used only once.
- The user sees a clear error when the link is expired, invalid, or already used.
- The flow must not reveal whether an account exists for an arbitrary email address.
- The flow must work on mobile and desktop browsers.
