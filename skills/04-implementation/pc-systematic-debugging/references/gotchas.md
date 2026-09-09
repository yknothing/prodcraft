# Systematic Debugging Gotchas

## Gotchas

### Live incident still hurting users
- Trigger: The responder starts tracing code paths while the production issue is still actively impacting users and no containment has happened.
- Failure mode: Debugging consumes the response window while user harm continues and rollback or fail-closed options are ignored.
- What to do: Route through `pc-incident-response` first, contain the incident, then resume root-cause work with lower pressure and better evidence.
- Escalate when: The team cannot agree whether the issue is contained or whether a rollback or fail-closed action is still required.

### Historical match becomes confirmation bias
- Trigger: `pc-bug-history-retrieval` returns a probable prior match or workaround that looks very similar to the current bug.
- Failure mode: The agent treats the prior ticket as proof and skips reproduction, boundary checks, or release-specific evidence.
- What to do: Use history to narrow hypotheses, then verify the current mechanism with a safe reproducer or preserve an explicit diagnosis limit when the environment prevents verification.
- Escalate when: Two historical lineages remain plausible after checking the current code path and release boundary.

### Third failed fix still treated as a local bug
- Trigger: Repeated corrections against the same symptom fail without new causal evidence. Probe edits and cleanup are not failed fixes.
- Failure mode: Repeated patching hides a requirements, architecture, or planning mismatch and increases risk without improving confidence.
- What to do: Pause the patch loop, restate the evidence, and prepare a `course-correction-note` if the failure boundary no longer fits a local code fix.
- Escalate when: The evidence points upstream but ownership of the route change is disputed or blocked.

### Debugging code that is not actually running
- Trigger: Observed behavior contradicts the source being read, or an added log line never appears in output.
- Failure mode: Stale identity or an unreachable path is mistaken for a local logic defect; conversely, valid evidence is discarded merely because a marker is absent.
- What to do: Check existing artifact identity and trace reachability separately using [techniques](techniques.md). Use a probe only when safe; do not automatically rebuild, redeploy, or clear shared caches.
- Escalate when: Identity or routing cannot be inspected within current access, and name the evidence/access needed to resume.

### Flaky failure "fixed" by rerunning
- Trigger: A test or job fails intermittently and passes on retry, and the retry is about to be accepted as resolution.
- Failure mode: A real race, ordering, or shared-state bug is reclassified as noise, ships to production, and returns as an incident that no longer has a fresh trail.
- What to do: In a safe isolated environment, investigate with repetition, controlled ordering, or latency injection; replace time-based waits with condition-based waits and isolate shared state. Preserve a verification gap if the failure cannot be safely exercised.
- Escalate when: The nondeterminism traces to shared infrastructure or another team's harness and cannot be stabilized within the current scope.

### Error message names the victim, not the culprit
- Trigger: The stack trace points at a line that looks obviously innocent, or the same exception appears across unrelated call sites.
- Failure mode: The fix hardens the crash site (null guard, catch-and-ignore) while the corrupt state keeps flowing from an upstream producer, so the defect resurfaces at the next consumer.
- What to do: Trace the bad value backward from the crash site to where it was created; instrument state before the failing call, not just the exception after it. Fix the producing layer and, at most, assert at the consuming layer.
- Escalate when: The producing layer is outside the current codebase or contract, which makes this a dependency workaround plus upstream report rather than a local fix.
