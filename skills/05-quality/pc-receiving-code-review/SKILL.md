---
name: pc-receiving-code-review
description: Use when review feedback has arrived and the author must verify, sequence, and respond to comments without blind agreement, especially when suggestions may conflict with brownfield constraints, contracts, or existing architecture decisions.
metadata:
  phase: 05-quality
  inputs:
  - review-report
  - source-code
  - test-suite
  outputs:
  - review-response-record
  prerequisites: []
  quality_gate: Each finding has an evidence-backed disposition, dependent blockers remain visible, and accepted changes are ready for the required re-review
  roles:
  - developer
  - tech-lead
  methodologies:
  - all
  effort: small
---

# Receiving Code Review

> Treat review feedback as technical input to verify, not as a script to perform.

## Context

`pc-receiving-code-review` is the author-side companion to reviewer-side `pc-code-review`.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Reconcile Findings With the Current Revision

Read the whole review before changing code. Preserve finding identifiers and group comments by root cause or shared decision. Classify items as accepted, disputed, clarification-needed, already-resolved, or optional. Check whether the reviewed revision still matches; stale locations are not proof that the defect is gone.

### Step 2: Isolate Ambiguity and Authority

An unclear comment blocks its dependent changes, not unrelated work. State the missing fact and affected group. Continue an independent accepted correction only when it stays valid under each plausible answer and existing authority covers it. If the items interact, clarify first rather than guessing.

A review suggestion does not expand scope or authorize publishing, deletion, dependency changes, or a new architecture. Route material scope/contract changes to the appropriate decision owner; keep unrelated authorized corrections moving.

### Step 3: Verify and Apply the Correction

Check the actual defect, compatibility constraints, upstream decisions, and proposed remedy. Prefer the smallest fix for the root cause; reject unused complexity with evidence. Apply related corrections as one reviewable batch when they share a cause and proof; verify independent risky changes separately. Use the relevant implementation discipline, including `pc-tdd` for new or changed behavior and `pc-systematic-debugging` for uncertain causes.

### Step 4: Record the Response and Handoff

Update the existing `review-response-record` using the I/O contract. Respond with technical facts, link duplicate findings, and mark fixes ready for re-review, not reviewer-approved. A disputed blocker remains until the authorized reviewer or policy resolves it. If it recurs without new evidence, resolve the missing cause or decision before another pass.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Every finding has a disposition and evidence tied to the current revision
- [ ] Unclear or disputed items block only their dependent work; independence is justified
- [ ] Accepted changes preserve scope and have relevant verification
- [ ] Remaining blockers, decision owners, and the re-review boundary are explicit
- [ ] A completed response does not claim integration approval
