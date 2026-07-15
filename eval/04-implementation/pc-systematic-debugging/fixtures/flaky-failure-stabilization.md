# Flaky Failure Stabilization Record

## Failure Boundary

- Scenario id: `flaky-failure-stabilization`
- `test_export_ready_notification` fails 4–9 times per 100 runs.
- The test sleeps 200 ms, then checks for the export completion event.
- Repeated reruns sometimes turn green without any code change; that green is explicitly rejected as evidence.

## Stabilization Journal

1. Instrument event enqueue and worker completion timestamps without changing the wait.
   - Prediction: failing runs check before worker completion.
   - Result: all captured failures check 8–47 ms before completion; passing runs happen to complete inside 200 ms.
2. Replace the test's fixed sleep with a condition-based wait on the observable completion event, leaving production code unchanged.
   - Prediction: the race becomes deterministic and exposes whether the event is eventually emitted.
   - Result: the test now reproduces a missing wake-up whenever the worker registers after the queue transition.
3. Change only the worker registration ordering so the listener exists before the transition.
   - Result: the stabilized reproduction passes 500 consecutive runs.

## Completed Fix Evidence

- Root cause: listener registration can occur after the one-shot completion transition, losing the wake-up.
- Fix boundary: register the listener before the transition; keep the condition-based test wait and remove the fixed sleep.
- With the ordering fix: 500/500 stabilized runs pass.
- With only the ordering fix removed: the stabilized test fails within 12 runs with the same missing wake-up.
- Regression protection: keep the condition-based test and hand it to `pc-tdd`.
