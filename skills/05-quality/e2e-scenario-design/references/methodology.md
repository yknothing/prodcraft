# E2E Scenario Design — Methodology Reference

Deep content for the `e2e-scenario-design` skill. Load this when designing or reviewing a full test suite, not for quick single-question answers.

---

## What "Deep" Means

**State accumulation**: Each step builds on the last. Adding a second item must verify the first is still there. Editing a record must verify original fields were preserved. Accumulation exposes mutation bugs single-step tests cannot.

**Cross-boundary verification**: State must survive navigation — tab switches, modal dismissals, screen transitions, app backgrounding. Test state *after* the navigation event, not just before it.

**Genuine persistence**: A tab switch tests in-memory state. Only a full navigate-away-and-back tests server-side persistence. Simulate the full re-entry path using the product's own navigation, not a test shortcut.

---

## Suite Architecture

### Fixture / stub layer

Must never depend on live infrastructure. Runs in CI without setup. Verifies the application's own loading, routing, navigation chrome, and deep link handling — not business behavior.

### Live flow layer

Verifies each major surface works against a real backend. Keep shallow — value is breadth, not depth. If a live flow test exceeds 5 steps, it probably belongs in the scenario layer.

### Scenario layer

The most valuable layer. Each test simulates what a real user does over an extended interaction. Write from persona journeys, not feature lists.

*Example:* The organizer on travel day: checks current meet-up → adds two expenses as receipts arrive → gets a delay notification → updates the meet-up point → verifies the team's expense state is intact.

This spans 4 features, takes 10+ steps, accumulates state throughout. No single-feature test covers it.

### Edge case layer

Write last, after the happy path is stable. Covers: empty state, partial input, server unavailability, rapid navigation, and lifecycle events (background/foreground, process restart).

---

## Scenario Design Process

### Step 1: Journey extraction

For each primary persona, write the extended session in plain language. Every clause that contains an action + an object is a test step. Every clause that contains a state check is an assertion.

### Step 2: State machine mapping

For each step, record:
- What was added / modified / deleted?
- Which prior state must still be visible after this step?
- Which cross-boundary navigations happen — and what must survive each?

The mapping tells you exactly what to assert. Every checkpoint must assert both the new state and the preserved prior state.

### Step 3: Re-entry point

Find the point in the scenario where the user leaves the context (closes the app, navigates home, returns via notification). Design one test that exercises this transition. This is the only test that verifies server-side persistence.

### Step 4: Edge case taxonomy

**Input boundaries**
- Empty / blank — confirm/submit should be disabled
- Partial — only some required fields filled
- Maximum length — no crash, no layout break
- Invalid format — rejected with clear feedback

**Navigation boundaries**
- Unknown route / invalid ID — graceful degradation, no crash
- Rapid / sequential navigation — state must not corrupt
- Deep link to mid-session state — lands correctly without prior setup

**Lifecycle events**
- Interrupt and resume (mobile: background/foreground; desktop: window minimize; web: tab switch)
- Dependency unavailable at startup vs. mid-session
- Process restart — state that should persist vs. state that should not

**Concurrency and timing**
- Rapid repeated taps on a submit button
- Slow network / delayed UI feedback
- Optimistic update rollback on failure

---

## Implementation Principles

**Wait for state, not time.** Never use `sleep(N)`. Every wait must be conditional: wait for an element, wait for a network completion, wait for a state propagation. Fixed sleeps cause both slowness and intermittent failures.

**Verify side-effects, not just action success.** After tapping "Confirm", assert the resulting state — the new item is in the list, the previous items are still there, the count is updated — not just that the button was tappable.

**Understand environment constraints before writing inputs.** Mock parsers, fixture servers, and stub responses have specific constraints. Read the implementation before writing test inputs. A test that taps "Confirm" on a silently disabled button is not a passing test — it is an unexecuted assertion.

**Anchor before querying.** After any navigation event, wait for an element unique to the new context before broad queries. The transition animation may leave stale elements from the previous context in the accessibility tree.

**Name assertions for failure messages.** Every assertion that could plausibly fail needs a message that reads without looking at the code:

```
// Bad
assert element.exists

// Good
assert element.exists, "First expense must still be visible after adding second — state accumulation broken"
```

**Isolate test data.** Each test runs independently, in any order. Create seed data programmatically at test start. Never depend on data from a prior test.

---

## Debugging Methodology

1. **Capture what the system actually showed.** Enable screenshot or video capture at failure. Looking at what was on screen eliminates guesswork.

2. **Check the precondition, not the assertion.** If `waitForElement` times out, trace backward — the submit button was probably disabled, or the previous action was a no-op.

3. **Classify the failure:**
   - *Timing* — element present but query too early → use conditional wait
   - *State* — element absent because prior action didn't produce expected state → assert on the prior step
   - *Interaction* — action fired at wrong location or intercepted → fix interaction method or reset scroll
   - *Environment* — mock/stub returned unexpected response → read the constraint and fix the input

4. **Reproduce reliably before fixing.** Run the failing test 5 times unchanged. Consistent failure → fix. Intermittent → the root cause is timing or order dependency.

---

## Platform Gotcha Classes

Every platform has a class of non-obvious E2E gotchas. Know which class you are in before writing tests.

**Embedded web content (WKWebView, WebView, Electron)**
The accessibility tree may not match the visual layout. Fixed-position elements report document-coordinate frames, not viewport frames. Modal overlays with `aria-modal` hide sibling elements from the accessibility layer. Disabled buttons are silent no-ops at the gesture level.
→ See [`platform/xcuitest-webview.md`](platform/xcuitest-webview.md) for the XCUITest/WKWebView playbook.

**Single-page applications (React, Vue, Angular)**
Route transitions produce no network requests — "wait for navigation" does not apply, wait for component state instead. Stale closure bugs cause actions to read outdated state. React Strict Mode double-invokes effects, causing test-environment-only state bugs.

**Mobile native (iOS, Android)**
Keyboard presence changes element hit-testability. System permission dialogs interrupt test flow. Background/foreground lifecycle may trigger re-authentication or session expiry. Animations may delay accessibility tree updates.

**Desktop GUI (Electron, Qt, WinForms)**
Window focus is a shared resource — parallel test runs may steal focus. File dialog interactions require OS-level automation. Clipboard state persists across tests.

**API / backend E2E**
Response ordering is non-deterministic for concurrent requests. Pagination and cursor state is easy to corrupt across steps. Token expiry mid-test requires explicit handling. Database constraint errors surface differently across environments.

---

## Anti-Patterns

- **Single-action tests as E2E.** A test that opens a screen and checks one element is a smoke test. Rename it.
- **Fixed sleeps.** `sleep(2)` is a bug. Replace with conditional waits.
- **Trusting that a tap succeeded.** Verify the side-effect. A gesture on a disabled button produces no error.
- **Testing in-memory state and calling it persistence.** A tab switch tests React state. Navigate away and back to test server persistence.
- **Broad queries after navigation.** Wait for a context anchor before querying; stale elements from the departing context may match first.
- **Test data depending on production or prior test runs.** Fix the setup — every test must pass on a clean database.
