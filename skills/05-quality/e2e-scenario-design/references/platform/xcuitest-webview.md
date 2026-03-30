# XCUITest + WKWebView — Platform Reference

Deep reference for iOS apps that embed web content via WKWebView and test with XCUITest. Load this when debugging WKWebView-specific test failures or designing a test suite for this architecture.

---

## How WKWebView Exposes Web Content

Everything is accessed through `app.webViews.firstMatch`. HTML element types map to XCUITest element types:

```swift
let webView = app.webViews.firstMatch
XCTAssertTrue(webView.waitForExistence(timeout: 15))

// HTML <button>   → webView.buttons
// HTML <a href>   → webView.links
// HTML <input>    → webView.textFields
// HTML <textarea> → webView.textViews
// Text node       → webView.staticTexts
```

Use `NSPredicate` for all queries — label matching is the only reliable bridge between the web accessibility tree and XCUITest:

```swift
// Partial match (most flexible)
webView.buttons.matching(NSPredicate(format: "label CONTAINS[c] 'Expenses'")).firstMatch

// Exact match (use when partial match could hit wrong element)
webView.buttons.matching(NSPredicate(format: "label == 'Add Info'")).firstMatch
```

Prefer exact `==` for FABs, confirm buttons, and tab labels — anything where a sibling could match the same substring.

---

## Tapping Web Inputs

`element.tap()` checks `isHittable` before firing. WKWebView doesn't always synchronously update the accessibility first-responder, so direct `.tap()` on text inputs often misfires. Use coordinate-based tap instead, then type via `app.typeText()`:

```swift
private func focusAndType(_ element: XCUIElement, text: String, in app: XCUIApplication) {
    element.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5)).tap()
    XCTAssertTrue(app.keyboards.firstMatch.waitForExistence(timeout: 5))
    app.typeText(text)  // typeText on app, not element
}
```

`app.typeText()` only requires any descendant to hold keyboard focus — which WKWebView satisfies once the OS first-responder is set.

For multi-field forms, navigate between fields using the keyboard accessory toolbar:

```swift
if app.toolbars.buttons["Next"].waitForExistence(timeout: 2) {
    app.toolbars.buttons["Next"].tap()
}
app.typeText("description text")
if app.toolbars.buttons["Done"].waitForExistence(timeout: 2) {
    app.toolbars.buttons["Done"].tap()
}
```

This is more reliable than coordinate-tapping the next field when the keyboard covers part of the form.

---

## Gotchas

### 1. Fixed-position elements report document-coordinate frames

**Symptom**: FAB or sticky header is visually on screen but tapping it does nothing.

**Root cause**: WKWebView reports `position: fixed` element accessibility frames in document coordinates, not viewport coordinates. When the page is scrolled, the element's accessibility frame is at `document_top + element_position` — off-screen relative to the viewport. `coordinate().tap()` dispatches to the visible position, but the DOM hit-test fires at the document coordinate — landing in empty space.

**Fix**: Reset scroll before tapping any fixed-position element:

```swift
// After extended interactions, document scroll offset may be non-zero.
// WKWebView reports fixed-position frames in document coordinates.
webView.swipeDown()

let fab = webView.buttons.matching(NSPredicate(format: "label == 'Add Info'")).firstMatch
XCTAssertTrue(fab.waitForExistence(timeout: 10))
fab.tap()
```

**Diagnosis**: Capture a screenshot to `/tmp` to see exactly what was on screen at the moment of tap:

```swift
let screenshot = XCUIScreen.main.screenshot()
try? screenshot.pngRepresentation.write(to: URL(fileURLWithPath: "/tmp/debug_tap.png"))
```

---

### 2. `aria-modal` hides the accessibility tree while a sheet is open

**Symptom**: After confirming a mutation, test times out finding the tab bar or any element outside the sheet.

**Root cause**: A modal sheet with `aria-modal="true"` removes all sibling elements from the iOS accessibility tree. The mutation may take several seconds. During that window, the tab bar, home button, and everything outside the sheet is inaccessible.

**Fix**: Wait for the sheet element to disappear before querying anything outside it:

```swift
let addToTripBtn = webView.buttons.matching(
    NSPredicate(format: "label CONTAINS[c] 'add to trip'")
).firstMatch
XCTAssertTrue(addToTripBtn.waitForExistence(timeout: 10))
addToTripBtn.tap()

// Sheet is open: aria-modal=true hides everything outside it.
// Wait for the sheet to close before querying the tab bar.
_ = addToTripBtn.waitForNonExistence(timeout: 20)

let expensesTab = webView.buttons.matching(
    NSPredicate(format: "label CONTAINS[c] 'Expenses'")
).firstMatch
XCTAssertTrue(expensesTab.waitForExistence(timeout: 15))
```

---

### 3. Tab transition timing causes broad predicates to match stale elements

**Symptom**: Test taps the right element on the wrong tab — "Add Expense" matched instead of "Add Info" after navigating to Overview.

**Root cause**: SPA tab transitions animate over ~200–300ms. During the animation, both old and new tab content are in the accessibility tree simultaneously. A broad predicate fires against the first match — which may be from the departing tab.

**Fix**: After a tab switch, wait for an element unique to the new context before any broad query:

```swift
webView.buttons.matching(NSPredicate(format: "label CONTAINS[c] 'Overview'")).firstMatch.tap()

// Wait for a tab-specific anchor before broad queries
let meetup = webView.buttons.matching(
    NSPredicate(format: "label CONTAINS[c] 'Shibuya'")
).firstMatch
XCTAssertTrue(meetup.waitForExistence(timeout: 15), "Overview must fully load before tapping Add")

webView.swipeDown()  // also reset scroll before FAB tap
let addInfo = webView.buttons.matching(NSPredicate(format: "label == 'Add Info'")).firstMatch
```

---

### 4. Disabled buttons are silent no-ops

**Symptom**: Test taps "Confirm" or "Add to trip", nothing happens, subsequent `waitForExistence` times out.

**Root cause**: XCUITest's `tap()` on a disabled HTML button fires the gesture successfully — the coordinate lands, the touch event is dispatched — but React's `onClick` is blocked. No error is raised.

**Fix**: Verify prerequisite state before tapping submit buttons. Know what makes the button enabled (required fields, input keyword requirements, server state) and confirm those conditions are met:

```swift
focusAndType(inputField, text: "bo arrives 3pm shibuya", in: app)

if app.toolbars.buttons["Done"].waitForExistence(timeout: 2) {
    app.toolbars.buttons["Done"].tap()
}

let confirm = webView.buttons.matching(NSPredicate(format: "label == 'Confirm'")).firstMatch
XCTAssertTrue(confirm.waitForExistence(timeout: 5))
confirm.tap()
```

Read the implementation before writing test inputs when the button's enabled state depends on a mock parser or local validation rule.

---

## Scenario Test Patterns

**State accumulation with cross-tab verification:**

```swift
// After adding two expenses, both must be visible
XCTAssertTrue(
    webView.buttons.matching(NSPredicate(format: "label CONTAINS[c] 'Bullet train'")).firstMatch.exists,
    "First expense must still be visible after adding second"
)
```

**Genuine persistence via re-entry:**

```swift
// Navigate completely away
app.buttons["rallo-home-button"].tap()

// Re-enter via the product's own navigation (not a test shortcut)
let tripLink = webView.links.matching(
    NSPredicate(format: "label CONTAINS[c] 'Tokyo convergence'")
).firstMatch
XCTAssertTrue(tripLink.waitForExistence(timeout: 15))
tripLink.tap()

// Verify server-persisted state survived
let expensesTab = webView.buttons.matching(NSPredicate(format: "label CONTAINS[c] 'Expenses'")).firstMatch
XCTAssertTrue(expensesTab.waitForExistence(timeout: 15))
expensesTab.tap()
XCTAssertTrue(
    webView.buttons.matching(NSPredicate(format: "label CONTAINS[c] 'Hotel'")).firstMatch
        .waitForExistence(timeout: 15),
    "Expense must persist across full navigate-away and re-entry"
)
```

---

## Server Availability Guard

Live tests require the dev server. Skip gracefully without infrastructure:

```swift
override func setUpWithError() throws {
    continueAfterFailure = false
    try XCTSkipUnless(isServerAvailable(), "Skipping: server not available at \(serverBase)")
}

private func isServerAvailable() -> Bool {
    guard let url = URL(string: "\(serverBase)/en") else { return false }
    var isAvailable = false
    let semaphore = DispatchSemaphore(value: 0)
    URLSession.shared.dataTask(with: url) { _, response, _ in
        isAvailable = (response as? HTTPURLResponse)?.statusCode == 200
        semaphore.signal()
    }.resume()
    semaphore.wait(timeout: .now() + 5)
    return isAvailable
}
```

Fixture and shell lifecycle tests that don't need the server must not call `XCTSkipUnless` — they must pass in offline CI.

---

## XcodeGen Integration

Directory-based source scanning auto-includes all Swift files under the test target path:

```yaml
targets:
  RalloShellUITests:
    type: bundle.ui-testing
    sources:
      - path: RalloShell/UITests   # scans all *.swift recursively
```

Add new test files to the directory and re-run `xcodegen generate`.
