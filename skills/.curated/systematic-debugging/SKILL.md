---
name: systematic-debugging
description: Use when a bug, failing test, regression, or unexpected behavior needs a root-cause-first debugging loop before code changes, especially when brownfield seams, recent releases, or historical defect matches make guesswork unsafe.
metadata:
  phase: 04-implementation
  inputs:
  - source-code
  - test-suite
  - historical-defect-context
  - fix-lineage-brief
  outputs:
  - bug-fix-report
  - course-correction-note
  prerequisites: []
  quality_gate: Root cause is evidenced, fix causality is proven both ways, the chosen fix is the smallest safe change, regression coverage exists, and structural mismatches are escalated instead of patched around
  roles:
  - developer
  - tech-lead
  - qa-engineer
  methodologies:
  - all
  effort: medium
  internal: false
  distribution_surface: curated
  source_path: skills/04-implementation/systematic-debugging/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Systematic Debugging

> No code fix without an evidenced root cause for the specific behavior being changed.

## The Iron Law

```
NO FIX WITHOUT A REPRODUCED FAILURE AND A FALSIFIABLE ROOT CAUSE
```

If you cannot state what is wrong, predict what evidence would prove you wrong, and reproduce the failure on demand, you are guessing -- and a guess that happens to make the symptom disappear is still a guess.

## Context

Systematic debugging turns a bug report, failing test, or bad runtime behavior into a defensible fix. It exists to stop guess-first patching, repeated failed fixes, and "works on my machine" improvisation.

It does **not** replace `incident-response`. If production impact is live, contain it there first; root-cause work resumes once the system is safe. Containment (rollback, flag off) is never evidence of root cause.

## Inputs

- **source-code** -- Relevant code paths, configuration boundaries, and recent changes near the failure. Minimum required input.
- **test-suite** -- Existing failing tests or the closest executable safety net.
- **historical-defect-context** -- Optional. Prior incidents or regressions that may match the symptom.
- **fix-lineage-brief** -- Optional. Prior fixes, reverts, or workarounds that narrow the search space.

## Process

### Step 1: Read the Evidence You Already Have

Before forming any theory:

1. Read the **entire** error message and the **full** stack trace, not the first line. Error text frequently names the exact cause, file, and line -- treating it as noise is the single most common debugging failure.
2. Confirm you are observing the code you think you are: right branch, right environment, rebuilt artifacts, cleared caches, correct deploy target. If a print statement or deliberate syntax error at the failure site does not show up, stop -- you are debugging the wrong code.
3. Check what changed recently: `git log`/`git diff` around the failure window, dependency bumps, config and environment changes.

### Step 2: Pin the Failure Boundary

Write down concretely: what fails, where it fails, expected vs actual behavior, and how to trigger it. Classify whether the failure is local, integration-boundary, or release-boundary sensitive. If the symptom plausibly has lineage, invoke `bug-history-retrieval` now -- use matches to narrow the search, never to skip the investigation.

### Step 3: Reproduce, Then Minimize

Get a reproduction you can run on demand -- a failing automated test when possible, a deterministic manual repro otherwise. Then shrink it: smaller input, fewer components, shorter path to failure. A minimal repro is usually most of the diagnosis.

- Regression with a known-good past? Bisect the history (`git bisect` or manual halving).
- Works in one environment, fails in another? Diff the two configurations and halve the differences.
- Failure is intermittent? Treat the flakiness itself as the bug. Do not rerun until green -- make the race, ordering, or state dependency deterministic first.

Concrete recipes are in [references/techniques.md](references/techniques.md). Do not move to fixes while the reproduction is unstable.

### Step 4: Run the Hypothesis Loop

One hypothesis at a time, cheapest test first:

1. State a single falsifiable hypothesis: "X causes Y because Z."
2. Predict what a specific observation will show if the hypothesis is true -- and what would disprove it.
3. Test with the least invasive instrument: read the code path, then add targeted logging or assertions at component boundaries, capturing **actual runtime values** rather than reasoning from memory of the code.
4. Record hypothesis, prediction, and result in a short debug journal before the next iteration. Change one variable per experiment.

If evidence disproves the hypothesis, discard it fully -- do not stack a patch for the old theory under a new one.

### Step 5: Confirm Root Cause and Classify It

State the narrowest cause that explains **all** observed evidence, not just the headline symptom. Then classify:

- **Local defect** -- proceed to Step 6.
- **Structural mismatch** (requirements, architecture, or planning contradiction) -- stop patching, produce a `course-correction-note`, and route upstream.

Escalation rule across failed fix attempts:

| Failed fix count | Required response |
|------------------|-------------------|
| first | gather better evidence before changing more code |
| second | challenge the current hypothesis in writing and identify what evidence would falsify it |
| third or more | stop local patching, assume a structural mismatch until disproven, and prepare `course-correction-note` |

Distinguish outcomes precisely: the **same** failure persisting after a fix means the hypothesis was wrong; a **new, different** failure appearing often means the first fix was correct and a second bug is now exposed. The first resets your hypothesis; the second is progress -- start a fresh loop for the new failure instead of reverting blindly.

### Step 6: Fix Once, Prove Causality Both Ways

Define the smallest safe change for the verified cause: what changes, what must not change, which brownfield seam or compatibility boundary stays protected, and whether this is a permanent fix or a declared workaround. Hand off to `tdd` so a reproducing test exists before implementation expands.

Then prove causality in both directions:

- **Fix applied** -- the original reproduction passes, plus the surrounding test scope.
- **Fix removed** -- the original failure returns.

If removing the fix does not bring the failure back, you have not fixed the cause; something else moved. Return to Step 4.

### Step 7: Record the Result

Produce a `bug-fix-report`: reproduction, root cause, confirming evidence, fix boundary, regression protection, and any follow-up debt if a workaround shipped. Keep the debug journal reference when the session had multiple attempts -- failed hypotheses are lineage for the next debugger.

## Outputs

- **bug-fix-report** -- Root cause, supporting evidence, fix boundary, regression protection, and follow-up notes.
- **course-correction-note** -- Only when evidence shows the problem belongs upstream in specification, architecture, or planning.

## Quality Gate

- [ ] The full error output was read and the failure is reproducible on demand
- [ ] The observed code path is confirmed current (no stale build, cache, or wrong environment)
- [ ] Root cause is stated as a falsifiable explanation that accounts for all evidence, not a symptom label
- [ ] Historical matches were checked when the symptom plausibly had lineage
- [ ] Fix causality is proven both ways: repro passes with the fix, fails again without it
- [ ] Regression or characterization protection is defined before broader implementation proceeds
- [ ] Structural mismatches are escalated through `course-correction-note` instead of patched around

## Rationalization Prevention

When one of these thoughts appears, treat it as a stop signal:

| Excuse | Required response |
|--------|-------------------|
| "I'll try the obvious fix first and investigate if it fails" | Stop. Return to reproduction and evidence gathering before changing code. |
| "The error message is generic, no point reading the rest" | Read all of it, including the trace bottom and caused-by chain. It usually names the culprit. |
| "I saw this bug before, so I know the cause" | Use history to narrow the search, then prove the current root cause anyway. |
| "Rollback fixed it, so we know what happened" | Containment is not explanation; identify why the bad behavior existed. |
| "The repro is flaky, but I can still patch around it" | Stabilize the failure boundary or instrument it before writing the fix. |
| "Rerunning made it pass, so it's fine" | An unexplained pass is the same bug waiting; find the nondeterminism. |
| "This is probably just environment weirdness" | Name the environment difference and prove it explains the symptom. |
| "It's too hard to reproduce, I'll fix it by inspection" | Inspection produces hypotheses, not proof; instrument the boundary instead. |
| "I'll make the broad fix now and tighten it later" | Choose the smallest safe change for the evidenced root cause. |
| "This is the third try, but I think this version will work" | Stop local patching and prepare `course-correction-note`. |
| "The test passes now, so the fix works" | Also remove the fix and watch the failure return; otherwise causality is unproven. |
| "Another agent already investigated this" | Read the evidence yourself before accepting the conclusion. |

## Red Flags -- Stop and Restart the Loop

- code changed before the failure was reproduced
- more than one variable changed per experiment
- a fix explanation contains "probably", "somehow", or "should"
- the same file is being patched for the third time this session
- each fix attempt reveals the same failure in a new costume
- instrumentation output was never actually read before the next change

## Anti-Patterns

1. **Shotgun debugging** -- changing several things at once and keeping whatever "worked".
2. **Containment mistaken for root cause** -- assuming rollback or flag-off explains why the bug exists.
3. **Historical anchoring** -- reusing an old fix because the ticket title looks similar.
4. **Architecture patch cosplay** -- applying a local workaround after multiple failed fixes even though the evidence points upstream.
5. **Regression amnesia** -- repairing today's symptom without defining the test that catches it next time.

## Reference Material

- [Techniques](references/techniques.md) -- bisection recipes, differential debugging, instrumentation patterns, flaky-failure stabilization, stale-artifact checklist, multi-bug untangling.
- [Gotchas](references/gotchas.md) -- recurring failure modes that create false confidence or misroutes.

## Related Skills

- [bug-history-retrieval](../../cross-cutting/bug-history-retrieval/SKILL.md) -- retrieves canonical defect lineage before a new fix theory hardens
- [incident-response](../../07-operations/incident-response/SKILL.md) -- contains live production impact before code-level debugging begins
- [tdd](../tdd/SKILL.md) -- turns the verified bug boundary into reproducing and regression tests
- [feature-development](../feature-development/SKILL.md) -- implements the smallest safe repair once the test and scope boundary are clear
- [verification-before-completion](../../cross-cutting/verification-before-completion/SKILL.md) -- verifies the claimed fix with fresh evidence before completion claims

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/04-implementation/systematic-debugging/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
