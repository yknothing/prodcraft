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
  quality_gate: Root cause is evidenced, the chosen fix is the smallest safe change, regression coverage exists, and structural mismatches are escalated instead of patched around
  roles:
  - developer
  - tech-lead
  - qa-engineer
  methodologies:
  - all
  effort: medium
---

# Systematic Debugging

> No code fix without an evidenced root cause for the specific behavior being changed.

## Context

Systematic debugging is the implementation-side discipline for turning a bug report, failing test, or bad runtime behavior into a defensible fix. It exists to stop guess-first patching, repeated failed fixes, and "works on my machine" improvisation.

This skill belongs in `04-implementation` because its primary output is a code-level fix path: isolate the failing boundary, identify the real cause, decide whether the problem is local or structural, and then hand off to `tdd` and `feature-development` for the smallest safe change.

It does **not** replace `incident-response`. If the issue is still live in production and user impact is active, contain it first through `incident-response`. Once the system is in a safe mode, use this skill to establish the root cause before writing the code fix.

## Inputs

- **source-code** -- The relevant code paths, configuration boundaries, and recent changes near the failure.
- **test-suite** -- Existing failing tests, regression coverage, or the closest executable safety net.
- **historical-defect-context** -- Optional. Prior incidents, defects, or regressions that may match the current symptom.
- **fix-lineage-brief** -- Optional. Prior fixes, reverts, or workarounds that may narrow the search space.

## Process

### Step 1: Establish the Current Failure Boundary

Write down the concrete failure first:

- what is failing now
- where it fails
- how to reproduce it
- whether the issue is local, integration-boundary, or release-boundary sensitive

If the issue is a live production incident and containment has not happened yet, stop and route through `incident-response` before continuing. Do not confuse containment with root-cause work.

### Step 2: Pull Historical Context Before Reinventing Theory

If the symptom might match a known regression, incident, or revert pattern, invoke `bug-history-retrieval` before guessing. Use historical matches to focus the search space, not to skip the investigation.

Search for:

- the same exception or error signature
- the same component boundary
- the same release or deploy window
- prior workarounds that were later reverted

### Step 3: Reproduce and Gather Evidence

Reproduce the failure with the smallest reliable loop available:

- a failing automated test when possible
- a deterministic manual repro when automation does not exist yet
- instrumentation at component boundaries when the failure crosses services, queues, jobs, or async hops

Do not move to fixes while the reproduction is unstable or the evidence is still vague.

### Step 4: Isolate Root Cause, Not Just Symptom

Identify the narrowest cause that explains the observed failure. Check:

- recent code or config changes
- broken assumptions at contract or compatibility boundaries
- missing regression coverage
- environment or rollout differences
- incorrect workarounds copied from earlier incidents

If the evidence shows a planning, requirements, or architecture mismatch rather than a local code defect, do not keep patching. Produce a `course-correction-note` and route upstream.

Use this escalation rule:

- first failed fix attempt: gather more evidence
- second failed fix attempt: challenge the current hypothesis explicitly
- third failed fix attempt: assume a structural mismatch until disproven and prepare `course-correction-note`

### Step 5: Choose the Smallest Safe Fix Path

Once root cause is clear, define the smallest safe change:

- what exact behavior changes now
- what must remain unchanged
- what brownfield seam, compatibility rule, or release boundary must stay protected
- whether the immediate repair is a permanent fix or an explicit workaround

Then hand off to `tdd` to write the reproducing or regression test before implementation code changes expand.

### Step 6: Record the Debugging Result

Produce a `bug-fix-report` that captures:

- reproduction steps or failing test
- root cause
- evidence used to confirm it
- chosen fix scope
- regression or characterization tests required
- any follow-up debt if a workaround shipped instead of the full repair

## Outputs

- **bug-fix-report** -- Root cause, supporting evidence, fix boundary, regression protection, and follow-up notes for the chosen repair path.
- **course-correction-note** -- Produced only when repeated failed fixes or hard evidence reveal that the problem belongs upstream in specification, architecture, or planning rather than in local code.

## Quality Gate

- [ ] The current failure is reproducible or otherwise evidenced with concrete signals
- [ ] Root cause is stated as a falsifiable explanation, not a symptom label
- [ ] Historical matches were checked when the symptom plausibly had lineage
- [ ] The chosen fix path is the smallest safe change for the verified root cause
- [ ] Regression or characterization protection is defined before broader implementation proceeds
- [ ] Structural mismatches are escalated through `course-correction-note` instead of patched around

## Anti-Patterns

1. **Fix-first thrashing** -- changing code before the failure is reproducible or the cause is understood.
2. **Containment mistaken for root cause** -- assuming rollback or flag disable explains why the bug exists.
3. **Historical anchoring** -- reusing an old fix because the ticket title looks similar.
4. **Architecture patch cosplay** -- applying a local workaround after multiple failed fixes even though the evidence points upstream.
5. **Regression amnesia** -- repairing today's symptom without defining the test that would catch it next time.

## Reference Material

For recurring debugging failure modes that create false confidence or repeated misroutes, see [Gotchas](references/gotchas.md).

## Related Skills

- [bug-history-retrieval](../../cross-cutting/bug-history-retrieval/SKILL.md) -- retrieves canonical defect lineage before a new fix theory hardens
- [incident-response](../../07-operations/incident-response/SKILL.md) -- contains live production impact before code-level debugging begins
- [tdd](../tdd/SKILL.md) -- turns the verified bug boundary into reproducing and regression tests
- [feature-development](../feature-development/SKILL.md) -- implements the smallest safe repair once the test and scope boundary are clear
- [verification-before-completion](../../cross-cutting/verification-before-completion/SKILL.md) -- verifies the claimed fix with fresh evidence before completion claims
