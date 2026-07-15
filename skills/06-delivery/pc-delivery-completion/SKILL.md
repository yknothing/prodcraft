---
name: pc-delivery-completion
description: Use when verified implementation work must be merged, handed off through a PR, preserved for later, or explicitly discarded with a recorded outcome instead of an ambiguous "done".
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
---

# Delivery Completion

> Turn verified work into an explicit integration decision: land it, open a PR, keep it for later, or discard it deliberately.

## Context

Delivery completion is the narrow bridge between "the work is verified" and "the work has an explicit fate." It does **not** replace release management or deployment strategy.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Confirm Fresh Verification Evidence

Do not present completion options until you have current evidence that the work is actually passing. If merge-base drift, dependency updates, or additional commits changed the verified surface, re-run the necessary verification first.

When strict execution state is active, require a fresh `terminal-authorized`
result for the canonical state and operator-pinned route and completion digests. Do not substitute
`--artifact-instance`, `gate-authorized`, a historical snapshot, or an earlier
terminal result from a different worktree state.

### Step 2: Determine the Completion Target

Clarify:

- the intended base branch or integration target
- whether the work should land now or wait for later handling
- whether branch policy requires a PR instead of local merge
- whether discard is even allowed for the current change

If the user asks to discard work that affects an active hotfix, incident follow-up, or team-owned branch, escalate before deleting anything.

### Step 3: Present Exactly Four Completion Options

Present these four outcomes, with the concrete branch names or paths filled in:

1. Merge or land to the integration branch now
2. Push and create a PR for review or later release handling
3. Keep the branch or worktree as-is for later
4. Discard the work

Do not offer vague "what do you want to do next?" prompts. Completion should end in an explicit outcome.

### Step 4: Execute the Chosen Outcome

#### Option 1: Merge or Land Now

- confirm the integration target
- land the work only if repository policy allows it
- re-run the critical verification on the merged result when the merge changes the tested surface
- record the merged commit or resulting branch state

#### Option 2: Push and Create a PR

- push the branch
- create the PR with a concise summary and explicit verification evidence
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

- [ ] Fresh verification evidence was checked before offering completion options
- [ ] Exactly one completion outcome was chosen and recorded
- [ ] Discard path requires typed confirmation
- [ ] Cleanup behavior matches the chosen outcome
- [ ] Downstream release handoff is explicit when the work continues toward shipping
