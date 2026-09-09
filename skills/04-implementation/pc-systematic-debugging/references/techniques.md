# Debugging Techniques

Deep recipes for the systematic-debugging loop. Load this file when the core process needs a concrete technique, not before.

Run active experiments in an authorized, safe environment. Preserve incident evidence and containment; do not replay harmful production effects. Without a safe experiment, record the missing proof and resumption condition in the diagnosis report.

## Bisection

Use when a regression has any known-good reference point.

- **History bisection**: `git bisect start; git bisect bad HEAD; git bisect good <last-known-good>` and let the repro script drive `git bisect run <cmd>`. If the repro is manual, still bisect -- log(n) manual checks beat rereading n diffs.
- **Input bisection**: halve the failing input (file, payload, dataset) until removing anything makes the failure disappear. The surviving fragment usually names the cause.
- **Config bisection**: start from a config that works, apply half the differences at a time toward the failing config (or the reverse).
- **Code-path bisection**: insert a probe mid-path (log, assertion, early return). Determine which half of the path corrupts the state, then recurse into that half.

Bisection requires a deterministic verdict per probe. If the failure is intermittent, stabilize it first (see Flaky Failures) or bisect on failure *rate* with enough repetitions per probe to be statistically meaningful.

## Differential Debugging

Use when the same code works in one context and fails in another.

1. Enumerate the axes that differ: version, environment variables, dependency versions, data, timing, locale/encoding, user/permissions, hardware, concurrency level.
2. Reduce the differences one axis at a time until the working context fails (or the failing context works).
3. The last difference standing is your hypothesis input for the core loop -- verify it explains the mechanism; correlation across contexts is not yet a cause.

## Instrumentation Patterns

Instrument to observe **actual values at boundaries**, not to narrate execution.

- Log entry/exit values at the component boundary nearest the failure, not everywhere. Include identity (request id, thread, pid) when concurrency is plausible.
- Prefer assertions over logs for invariants: an assertion converts a silent corruption into a loud early failure at the corruption site.
- Capture state *before* the failing call, not just the exception after it -- the exception often reports the victim, not the culprit.
- When output volume gets large, you are instrumenting too wide: narrow to the half of the path bisection implicated.
- Remove or gate instrumentation before the fix lands; leftover debug logging is workaround debt and must be recorded as such in the bug-fix-report.

## Stale-Artifact Checklist

Check identity separately from reachability when behavior contradicts the source. Start with existing evidence; rebuilds, restarts, and cache changes are experiments, not automatic prerequisites:

- [ ] Observed branch/revision and relevant uncommitted changes identified
- [ ] Build/runtime identity matches the intended candidate; timestamp alone is not proof
- [ ] Relevant cache and process lifecycle understood; change them only to test a stated hypothesis safely
- [ ] The environment under test is the one you deployed to (correct container tag, correct cluster, correct database)
- [ ] Existing trace or a safe targeted marker establishes whether the expected path was reached

If a marker is absent, distinguish stale identity, unreachable control flow, and missing logging. A current handler skipped by a faulty dispatcher is useful evidence. Retain observations with their confirmed scope rather than discarding them by assumption.

## Flaky Failures

A flaky test or intermittent failure is a real bug in the code or in the test contract. "Rerun until green" converts a reproducible signal into a production incident later.

- Force the failure: run under repetition (`--repeat`, stress loops), reduced resources, randomized ordering, or artificial latency injection until the failure is reliable.
- Replace time-based waits with condition-based waits. A `sleep(2)` that "fixes" a race documents the race without closing it.
- Audit shared state between tests: leaked globals, reused fixtures, order dependence. Run the failing test in isolation and in suite order; a verdict difference means state leakage.
- For concurrency suspects, make the schedule deterministic (single-threaded reproduction, controlled interleaving) before hypothesizing about logic.

## Multi-Bug Untangling

Symptoms rarely map one-to-one onto defects.

- If a verified fix changes the failure signature instead of clearing it, treat the new signature as a **separate** bug with its own loop and journal entry. Do not revert a proven fix because a second bug surfaced behind it.
- If two hypotheses each explain part of the evidence, split the reproduction until each repro isolates one mechanism.
- Keep one journal per failure signature. Merged journals produce merged (wrong) conclusions.

## Fix-Layer Selection

Fix where the defect originates, not where it hurts.

- If bad state is created in layer A and crashes layer C, guarding C hides A's defect and spreads null-checks across every consumer. Fix A; optionally assert in C.
- If the defect is in a dependency you do not control, isolate the workaround at the single adapter boundary, mark it as workaround debt in the bug-fix-report, and link the upstream issue.
- If the "right layer" is upstream of implementation entirely (spec or architecture contradiction), that is the course-correction-note path, not a code fix.
