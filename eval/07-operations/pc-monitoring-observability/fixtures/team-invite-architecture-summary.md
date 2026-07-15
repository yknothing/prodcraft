# Team Invite Service Architecture Summary

- A new invite service creates invitation records, dispatches email through a provider queue, and validates invite tokens on acceptance.
- There is no legacy coexistence layer or migration seam.
- Main user-critical boundaries are invite creation, email dispatch, and invite acceptance.
- Queue backlog or provider failures can delay invitation delivery without affecting the rest of the product.
