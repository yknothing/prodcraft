---
name: pc-verification-before-completion
description: Use when about to claim a phase, fix, task, build, or release is complete, fixed, passing, or ready for handoff and fresh evidence must be checked before making the claim or creating a commit, PR, or deployment decision.
metadata:
  phase: cross-cutting
  inputs:
  - route-decision
  - execution-state
  outputs:
  - verification-record
  - execution-state
  prerequisites: []
  quality_gate: Every completion claim is backed by fresh verification evidence, relevant artifact checks, and an explicit statement of what remains unverified
  roles:
  - developer
  - tech-lead
  - qa-engineer
  - devops-engineer
  methodologies:
  - all
  effort: small
---

# Verification Before Completion

> Evidence before claims. No completion, fix, or readiness statement without fresh verification.

## Context

`pc-verification-before-completion` is the cross-cutting gate that protects Prodcraft from false completion claims. It exists because implementation success, review approval, or deployment confidence often drifts into assertion before evidence.

This skill does not replace the phase-local quality work. It is the final honesty check before saying:

- the bug is fixed
- the phase is complete
- the tests pass
- the release is ready
- the handoff is safe

Fast-track work may shorten the verification surface, but it does not waive this gate. The Iron Law stays the same.

## Inputs

No fixed artifact is required up front. Start from the current claim and the strongest available verification command, artifact, or checklist for that claim.

## Process

### Step 1: Name the Claim Precisely

State exactly what is about to be claimed:

- "the fix works"
- "all tests pass"
- "this phase is complete"
- "the release is ready to ship"
- "the incident is resolved"

If the claim is vague, split it into smaller claims. Verification is only meaningful when the claim is concrete.

### Step 2: Identify the Fresh Evidence Required

For each claim, name the proof needed now:

- command output
- failing-then-passing regression evidence
- artifact presence and handoff checks
- quality gate checklist
- rollout or recovery verification

Do not rely on stale runs, partial checks, or "it should still be green."

Use this quick reference before moving on:

| Claim | Requires now | Not sufficient |
|-------|--------------|----------------|
| "the fix works" | current repro or regression evidence showing failing-then-passing behavior | an older passing run, "the patch is obvious", or a reviewer saying it looks right |
| "all tests pass" | current command output and exit status for the intended test scope | a previous run, a subset proxy, or "they passed before the last change" |
| "this phase is complete" | current phase quality gate plus required artifact and handoff checks | a summary from memory or a nearby but weaker check |
| "the release is ready" | current release evidence, verification checkpoints, and artifact integrity | green CI alone or confidence that the rollout plan probably still applies |
| "the handoff is safe" | accessible outputs, explicit next-step context, and any schema-backed artifact checks needed | "the next person can figure it out" |
| "the incident is resolved" | current service checks, recovery evidence, and explicitly named remaining unknowns | lack of new alerts for a short period or rollback alone |

### Step 3: Run the Verification Now

Execute the relevant verification in the current message or session:

- run the full command, not a weaker proxy
- read the actual output and exit status
- confirm the expected artifact or file exists
- confirm the current phase gate is satisfied
- note any unverified areas explicitly

For `fast-track` work, run the narrowest command set that still proves the claim. "Fast" changes the scope of proof, not the need for proof. NEVER assume a file was modified or a task was completed based on context or conversational history. If you cannot see the change via a diff, `cat`, or directory listing, the evidence is missing and the verification MUST fail. Proof cannot be hallucinated or waived just because a fix is small.

### Step 4: Check Artifact and Handoff Integrity

Before making the claim, verify that:

- required phase outputs exist and are accessible
- any schema-backed artifact still satisfies its contract when applicable
- handoff context is explicit enough for the next skill or operator
- any skipped checks are logged as real gaps, not implied away

When producing a repository artifact instance, store it under the governed
project's `.prodcraft/artifacts/` directory when that directory exists. If the
project has no `.prodcraft/` convention yet, write the instance in the nearest
existing evidence or handoff directory and record that path in the handoff.

For a `verification-record` instance, run:

```bash
python scripts/validate_prodcraft.py --artifact-instance <path-to-verification-record.json>
```

When the project has opted into the strict execution loop, generic artifact
validation is not completion authority. Bind the accepted verification record and
its evidence snapshots into the current completion attempt, then run:

```bash
python scripts/validate_prodcraft.py \
  --authorize-execution-state .prodcraft/artifacts/<work_id>/execution-state.json \
  --approved-route-digest sha256:<operator-pinned-route-digest> \
  --approved-completion-digest sha256:<operator-pinned-completion-digest>
```

Only `terminal-authorized` permits an unqualified route-level completion claim.
`gate-authorized` is non-terminal progress authority. A historical, non-canonical,
missing-pin, stale-work, or structurally-valid-only result blocks the claim.
Run the terminal command once without the completion pin to obtain a non-authoritative
candidate digest, review the frozen verification commitment and terminal records,
then supply the approved digest from outside the writable bundle.

If the verification reveals a gap, do not translate it into optimistic language. State the actual status.

### Step 5: Record the Result Honestly

Produce a `verification-record` that states:

- the exact claim tested
- the commands or checks run
- what passed
- what failed
- what remains unverified
- whether the claim may now be made without qualification

When the Prodcraft source repository (or a repository that vendored its validators) is available, validate the structured record instead of eyeballing it:

```bash
python scripts/validate_artifact_instance.py <verification-record file>
```

This checks the schema contract plus the completion-claim bindings (evidence freshness against the recorded work state). Outside that context, check the record manually against the `verification-record.v1` fields and say so explicitly.

Only after this step may the workflow say the work is complete, fixed, passing, or ready for handoff.

## Outputs

- **verification-record** -- Fresh evidence for the specific completion claim, including commands run, artifact checks, and any remaining gaps.
- **execution-state** -- Optional strict-mode completion attempt and content-bound verification envelope.

## Quality Gate

- [ ] The completion claim is explicit rather than implied
- [ ] Fresh verification was run for the actual claim, not a nearby proxy
- [ ] Relevant artifacts and handoff requirements were checked
- [ ] Failures, skips, or unknowns are stated plainly
- [ ] The final wording matches the evidence instead of the hoped-for result
- [ ] When strict mode is active, the canonical state returns `terminal-authorized` against both operator pins and the live worktree

## Anti-Patterns

1. **Optimistic paraphrase** -- changing "not fully verified" into "looks good."
2. **Proxy verification** -- treating lint, typecheck, or one passing test as proof that the whole claim is true.
3. **Stale green** -- relying on an earlier run after code or context changed.
4. **Fast-track loophole hunting** -- assuming urgency waives evidence.
5. **Agent trust fall** -- repeating another agent's success claim without checking the output or artifacts yourself.

## Reference Material

For common completion-claim failure modes and recovery patterns, see [Gotchas](references/gotchas.md).

## Related Skills

- [pc-systematic-debugging](../../04-implementation/pc-systematic-debugging/SKILL.md) -- verifies that a claimed fix is backed by a root-cause-first debugging result
- [pc-code-review](../../05-quality/pc-code-review/SKILL.md) -- provides review evidence that may feed the final completion claim
- [pc-testing-strategy](../../05-quality/pc-testing-strategy/SKILL.md) -- supplies test reports for broader validation
- [pc-incident-response](../../07-operations/pc-incident-response/SKILL.md) -- uses this gate before declaring a live issue resolved
