# Assertion Patterns — What to Assert Inside E2E Scenarios

Structural test design (suite layers, scenario shape, state accumulation) is necessary but not sufficient. A well-structured test that asserts only UI visibility can still miss every production bug. This reference covers what to assert at the content level.

---

## The Assertion Gap

A test that adds an item to a cart and asserts the badge shows "1" has verified UI state. If the cart is backed by a server, the badge could show "1" while the server never persisted the item, the quantity was stored as zero, or the wrong product ID was saved. These bugs pass UI assertions.

The right assertion target depends on what the system contract actually is. Identify the source of truth for each piece of state: is it in-memory, in localStorage, in a server database? Assert at that level.

---

## Business State Consistency

For operations that span multiple system boundaries, verify consistency across all of them — not just the last one.

**Price / value consistency across a flow:**
Assert that the value displayed at each stage matches. A price shown on a product page must match the cart, the checkout summary, and the stored order record. Discrepancies between stages are a common production bug that single-step tests never catch.

```
product page price → cart line item → checkout total → order confirmation → order record in DB
```

**Inventory / quota consistency:**
When an item is reserved or consumed, verify that the reservation is reflected system-wide. Adding an item to a cart should reduce available stock. Completing a purchase should finalize the reduction. Race conditions (two users purchasing the last unit) are common and only detectable with concurrency tests.

**Ownership and permissions:**
When a resource is created, verify the creator has the correct role. When a role is changed, verify the change propagates to all UI surfaces that depend on it — not just the page where the change was made.

---

## Concurrency Assertions

Single-user sequential tests cannot find concurrency bugs. Add targeted concurrency checks to the edge case layer.

**Rapid repeated submission:**
Submit the same form twice in quick succession. The system should create one record, not two. Optimistic UI should show a single pending state, not two.

**Concurrent resource access:**
Simulate two sessions acting on the same resource simultaneously. Verify that the conflict is detected and resolved predictably — not silently corrupted. A lost-update (the last write wins without notifying the loser) is a common production bug.

**Inventory oversell:**
For any resource with a finite quantity, test what happens when two users attempt to claim the last unit at the same time. One should succeed; the other should receive a clear error.

---

## Failure Recovery Assertions

Optimistic updates are a common source of silent data loss. When an action shows immediate feedback before server confirmation, assert that the rollback is correct when the server rejects it.

**Optimistic update rollback:**
Intercept the network request for a mutation and force a failure. The UI should revert to the pre-action state. The user should see a clear error. The underlying data should be unchanged.

**Partial failure:**
For multi-step server operations (create + associate + notify), assert the system's behaviour when a mid-chain step fails. Is the prior step rolled back? Is the user informed? Is the partial state visible or hidden?

**Session expiry mid-action:**
Expire the auth token while the user is mid-flow (between form fill and submit). Assert that the user is prompted to re-authenticate, and that their in-progress data is preserved or clearly lost — not silently discarded.

---

## Persistence Assertions

Distinguish what should and should not survive different re-entry paths:

| Re-entry type | What persists | What resets |
|---|---|---|
| Tab / page switch (SPA) | React state, localStorage | Network request cache (may) |
| Soft reload (same session) | localStorage, sessionStorage | In-memory React state |
| Hard reload / new tab | Server-persisted data, localStorage | sessionStorage, React state |
| App background + foreground (mobile) | Server-persisted data, local DB | In-memory state |
| App killed + relaunch | Server-persisted data, local DB | All in-memory state |

For each re-entry type that matters to the product, write one test that explicitly takes that path and asserts the correct persistence boundary.

---

## Assertion Quality Checklist

Before committing a test, verify each assertion:

- [ ] **Asserts the right source of truth** — UI label, API response, database record, or local storage — whichever is the actual contract
- [ ] **Asserts both new state and preserved prior state** — accumulation, not just the latest action
- [ ] **Includes a failure message** that identifies what invariant was violated and where
- [ ] **Does not assert implementation details** — the DOM structure or internal component state, not the user-visible contract
- [ ] **Is not duplicated at a lower layer** — if the unit test already verifies a calculation, the E2E test should verify the result is surfaced correctly, not re-verify the calculation
