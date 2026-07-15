# Systematic Debugging Gotchas

## Gotchas

### Live incident still hurting users
- Trigger: The responder starts tracing code paths while the production issue is still actively impacting users and no containment has happened.
- Failure mode: Debugging consumes the response window while user harm continues and rollback or fail-closed options are ignored.
- What to do: Route through `incident-response` first, contain the incident, then resume root-cause work with lower pressure and better evidence.
- Escalate when: The team cannot agree whether the issue is contained or whether a rollback or fail-closed action is still required.

### Historical match becomes confirmation bias
- Trigger: `bug-history-retrieval` returns a probable prior match or workaround that looks very similar to the current bug.
- Failure mode: The agent treats the prior ticket as proof and skips reproduction, boundary checks, or release-specific evidence.
- What to do: Use historical context to narrow hypotheses, then reproduce the current failure and verify the same cause exists in the current branch, release, or environment.
- Escalate when: Two historical lineages remain plausible after checking the current code path and release boundary.

### Third failed fix still treated as a local bug
- Trigger: Two fixes have already failed or partially reverted and the next attempt still assumes the problem is a small local defect.
- Failure mode: Repeated patching hides a requirements, architecture, or planning mismatch and increases risk without improving confidence.
- What to do: Pause the patch loop, restate the evidence, and prepare a `course-correction-note` if the failure boundary no longer fits a local code fix.
- Escalate when: The evidence points upstream but ownership of the route change is disputed or blocked.

### Debugging code that is not actually running
- Trigger: Observed behavior contradicts the source being read, or an added log line never appears in output.
- Failure mode: Hours of hypothesis work are spent against a stale build, cached artifact, wrong branch, or wrong environment, and every collected observation is about some other code.
- What to do: Place a deliberate marker at the failure site and confirm it appears in observed output. Run the stale-artifact checklist in `references/techniques.md` before trusting any further observation.
- Escalate when: The marker still does not appear after a clean rebuild and redeploy, which suggests the deployment or routing path itself is the defect.

### Flaky failure "fixed" by rerunning
- Trigger: A test or job fails intermittently and passes on retry, and the retry is about to be accepted as resolution.
- Failure mode: A real race, ordering, or shared-state bug is reclassified as noise, ships to production, and returns as an incident that no longer has a fresh trail.
- What to do: Treat the flakiness as the bug. Force the failure with repetition, randomized ordering, or latency injection; replace time-based waits with condition-based waits; isolate shared state.
- Escalate when: The nondeterminism traces to shared infrastructure or another team's harness and cannot be stabilized within the current scope.

### Error message names the victim, not the culprit
- Trigger: The stack trace points at a line that looks obviously innocent, or the same exception appears across unrelated call sites.
- Failure mode: The fix hardens the crash site (null guard, catch-and-ignore) while the corrupt state keeps flowing from an upstream producer, so the defect resurfaces at the next consumer.
- What to do: Trace the bad value backward from the crash site to where it was created; instrument state before the failing call, not just the exception after it. Fix the producing layer and, at most, assert at the consuming layer.
- Escalate when: The producing layer is outside the current codebase or contract, which makes this a dependency workaround plus upstream report rather than a local fix.
