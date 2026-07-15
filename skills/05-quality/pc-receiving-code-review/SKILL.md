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
  prerequisites:
  - pc-code-review
  quality_gate: Every review item is understood, verified against current codebase reality, and either implemented with evidence or answered with technical reasoning
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

### Step 1: Read the Whole Review Before Acting

Do not start implementing the first comment immediately. Read the full review and group items into:

- blocking corrections
- clarifications needed
- technically questionable suggestions
- optional improvements

If multiple comments appear related, keep them together until the interaction is understood as a whole.

### Step 2: Clarify Before Partial Implementation

If any review item is ambiguous, stop and ask before changing code. Do not implement the subset you understand while guessing at the rest.

Clarify when:

- the requested behavior is unclear
- the suggested scope is larger than the current slice
- the comment may conflict with an architecture or product boundary
- the reviewer appears to assume context that is not visible in the diff

### Step 3: Verify Against Codebase Reality

For each review item, check:

- does the suggestion fit the current code and tests
- does it preserve brownfield compatibility and unsupported-flow rules
- does it violate YAGNI or introduce unused complexity
- does it conflict with reviewed architecture or contract decisions
- is the reviewer pointing at the real defect, or only at a local symptom

If the feedback is correct, implement it. If not, respond with technical reasoning and evidence instead of social agreement.

### Step 4: Respond Factually, Not Performatively

Do not write praise or social filler such as:

- "You're absolutely right"
- "Great point"
- "Excellent feedback"

Instead:

- restate the technical issue
- say what changed
- say what remains unclear
- say why the suggestion should not be applied when evidence contradicts it

### Step 5: Implement One Verified Item at a Time

Apply accepted feedback in a controlled order:

1. blocking correctness or security fixes
2. scope-safe cleanups
3. optional or stylistic improvements last

Run the relevant tests after each meaningful change. If one item reopens another, record that explicitly instead of silently batch-editing everything at once.

### Step 6: Produce a Review Response Record

Produce a `review-response-record` that captures:

- each review item
- whether it was implemented, challenged, or clarified
- the evidence used to decide
- the tests or checks run after accepted changes
- any remaining disputed items that still need reviewer or user resolution

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Every review item is classified before implementation begins
- [ ] Ambiguous feedback is clarified before partial implementation
- [ ] Accepted suggestions are verified against current codebase reality
- [ ] Pushback, when needed, is technical and evidence-based
- [ ] Relevant tests are rerun after accepted changes
- [ ] The final response states what changed and what remains unresolved
