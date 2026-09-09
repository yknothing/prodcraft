---
name: pc-delivery-completion
description: Use when implementation work needs an explicit merge, PR handoff, preservation, or authorized discard outcome, including incomplete or failing work that must be preserved without a completion claim.
metadata:
  phase: 06-delivery
  inputs:
  - verification-record
  - execution-checkpoint
  - route-decision
  - execution-state
  outputs:
  - delivery-decision-record
  prerequisites:
  - pc-verification-before-completion
  quality_gate: Delivery outcome, integration path, cleanup decision, and downstream release handoff are explicit
  roles:
  - developer
  - tech-lead
  methodologies:
  - all
  effort: small
  internal: false
  distribution_surface: curated
  source_path: skills/06-delivery/pc-delivery-completion/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Delivery Completion

> Give work an explicit outcome with the evidence and authority that outcome requires.

## Context

Delivery completion is the narrow bridge between "the work is verified" and "the work has an explicit fate." It does **not** replace release management or deployment strategy.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Identify the Outcome and Evidence Boundary

Read the requested outcome before deciding what verification is needed. Merge, landing, or a ready-for-review PR requires current passing evidence. If the verified surface changed, re-run the affected checks before that action.

When strict execution state is active, a successful completion claim requires a fresh `terminal-authorized`
result for the canonical state and operator-pinned route and completion digests. Do not substitute
`--artifact-instance`, `gate-authorized`, a historical snapshot, or an earlier
terminal result from a different worktree state.

Keeping work for later or explicitly discarding it does not require passing tests. Record current failures, incomplete checks, and remaining obligations without marking the work successfully completed. A preservation record does not satisfy a strict terminal gate or authorize deletion of its evidence. An explicitly authorized draft PR may carry the same incomplete status; do not describe it as ready to merge.

### Step 2: Determine the Completion Target

Read the user's existing instructions and repository policy first. Resolve only missing facts:

- the intended base branch or integration target
- whether the work should land now or wait for later handling
- whether branch policy requires a PR instead of local merge
- whether discard is even allowed for the current change

If the user asks to discard work that affects an active hotfix, incident follow-up, or team-owned branch, escalate before deleting anything.

### Step 3: Reuse the Authorized Outcome or Resolve the Choice

If the user already authorized a concrete outcome and target, proceed to Step 4 after verification. Do not ask them to choose it again. Carry only the authorized actions: commit, push, PR creation, merge, and deployment are separate actions. A request to commit and push does not imply creating a PR or deploying.

If the outcome is unresolved, present the applicable choices with concrete branch names or paths:

1. Merge or land to the integration branch now
2. Push and create a PR for review or later release handling
3. Keep the branch or worktree as-is for later
4. Discard the work

Exclude choices forbidden by repository policy. Do not force a destructive option into a routine handoff. If the task only requests local edits or a review, preserve the work and record that boundary without an unnecessary integration question.

### Step 4: Execute the Chosen Outcome

#### Option 1: Merge or Land Now

- confirm the integration target
- land the work only if repository policy allows it
- re-run the critical verification on the merged result when the merge changes the tested surface
- record the merged commit or resulting branch state

#### Option 2: Push and Create a PR

- push the branch when authorized
- create a PR only when that action is authorized or required by the agreed integration path; include a concise summary and explicit verification evidence
- record the PR path or remote branch name
- hand off to `pc-release-management` when the change now needs coordinated release handling

#### Option 3: Keep for Later

- preserve the branch and worktree
- record why it is being kept
- record the next expected checkpoint so the branch does not become ambiguous dead state

#### Option 4: Discard

- list exactly what will be deleted
- require typed `discard` confirmation before destructive cleanup
- delete only after confirmation
- record that the work was intentionally discarded rather than silently abandoned

### Step 5: Clean Up and Hand Off

- Clean up merged or discarded worktrees when repository policy and user intent allow it.
- Keep PR branches and explicitly preserved branches intact.
- If the change is moving toward release, pass the `delivery-decision-record` into `pc-release-management`.
- If the change stops here, say so explicitly instead of implying downstream delivery work exists.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Evidence and authorization match the chosen outcome; incomplete preservation or discard is not reported as successful implementation
- [ ] Exactly one completion outcome was chosen and recorded
- [ ] Discard path requires typed confirmation
- [ ] Cleanup behavior matches the chosen outcome
- [ ] Downstream release handoff is explicit when the work continues toward shipping

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/06-delivery/pc-delivery-completion/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
