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
Assert the documented value relationship at each stage, including legitimate discounts, tax, shipping, and rounding. Verify that the displayed final total matches the authoritative order result; do not require raw product and checkout prices to be identical when the contract transforms them.

```
product page price → cart line item → checkout total → order confirmation → order record in DB
```

**Inventory / quota consistency:**
Identify when the product reserves or consumes capacity: cart addition, checkout, or another documented transition. Verify the corresponding authoritative state and release behavior. Use targeted concurrency checks when two users can claim the same remaining capacity.

**Ownership and permissions:**
When a resource is created, verify the creator has the correct role. When a role is changed, verify the change propagates to all UI surfaces that depend on it — not just the page where the change was made.

---

## Concurrency Assertions

Single-user sequential tests cannot find concurrency bugs. Add targeted concurrency checks to the edge case layer.

**Rapid repeated submission:**
Where one user intent must be idempotent, submit it twice in quick succession and verify one authoritative effect. Distinguish retries from two valid independent intents; assert the product's pending-state behavior.

**Concurrent resource access:**
Simulate two sessions acting on one resource. Verify the declared conflict policy: rejection, merge, serialization, or intentional last-write-wins. Check that no required update is silently lost under that policy.

**Inventory oversell:**
Test competing claims for the last available unit. Verify the declared allocation policy and capacity invariant: a rejected, waitlisted, or backordered request must be represented accurately, not silently treated as an allocated unit.

---

## Failure Recovery Assertions

When UI feedback precedes authoritative confirmation, distinguish confirmed rejection, an unsent operation, and an unknown commit outcome. Verify the product's rollback, pending/retry, or reconciliation policy for each state.

**Optimistic update rollback:**
For a confirmed rejection before commit, verify the declared UI rollback or failed/pending state and that no unauthorized effect occurred. For a lost response, read authoritative state or reconcile using the operation identity; do not assume the server did not commit. An offline-first queue may retain pending work when that is the documented policy.

**Partial failure:**
For multi-step server operations (create + associate + notify), assert the system's behaviour when a mid-chain step fails. Is the prior step rolled back? Is the user informed? Is the partial state visible or hidden?

**Session expiry mid-action:**
Expire the auth token while the user is mid-flow (between form fill and submit). Assert that the user is prompted to re-authenticate, and that their in-progress data is preserved or clearly lost — not silently discarded.

---

## Persistence Assertions

Distinguish what should and should not survive different re-entry paths:

| Re-entry type | What to establish | What the transition does not prove |
|---|---|---|
| SPA route or tab switch | Which components, stores, and query caches survive | Server persistence or process restart |
| Page reload, including hard reload | New document/JS state; same-tab sessionStorage normally survives | Clearing sessionStorage, local storage, or server data |
| New tab or isolated browser context | Actual storage/session setup; opener cloning or shared origin storage may apply | A clean session merely because a new tab exists |
| App background then foreground | Whether the process actually survived, froze, or terminated | Automatic loss of in-memory state |
| Confirmed process termination and relaunch | Persisted source, restore behavior, and session policy | Server persistence if restoration came from a local store |

For each re-entry type that matters to the product, write one test that explicitly takes that path and asserts the correct persistence boundary.

Browser facts: same-tab `sessionStorage` survives reloads and can be copied from an opener ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage)); hidden, frozen, and discarded pages are distinct lifecycle states ([Chrome lifecycle guidance](https://developer.chrome.com/docs/web-platform/page-lifecycle-api)). Derive expected application state from its storage contract, not a generic navigation label.

---

## Assertion Quality Checklist

Before committing a test, verify each assertion:

- [ ] **Asserts the right source of truth** — UI label, API response, database record, or local storage — whichever is the actual contract
- [ ] **Asserts both new state and preserved prior state** — accumulation, not just the latest action
- [ ] **Includes a failure message** that identifies what invariant was violated and where
- [ ] **Does not assert implementation details** — the DOM structure or internal component state, not the user-visible contract
- [ ] **Is not duplicated at a lower layer** — if the unit test already verifies a calculation, the E2E test should verify the result is surfaced correctly, not re-verify the calculation
