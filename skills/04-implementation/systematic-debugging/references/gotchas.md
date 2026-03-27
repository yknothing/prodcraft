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
