---
name: implementation-alignment-review
description: Use after implementation or repair work when the reviewer must judge intent realization, requirement coverage, scope consistency, and claim truth before code-review or delivery-completion can accept the work.
metadata:
  phase: 05-quality
  inputs:
  - intake-brief
  - source-code
  - test-suite
  - task-list
  - acceptance-criteria-set
  outputs:
  - review-report
  prerequisites:
  - feature-development
  quality_gate: Intent, acceptance criteria, implementation behavior, tests, docs, and completion claims are aligned with explicit evidence and no silent scope substitutions
  roles:
  - reviewer
  - tech-lead
  methodologies:
  - all
  effort: medium
---

# Implementation Alignment Review

## Context

This skill checks whether the implementation actually satisfies the user's intent and approved scope. It exists because green tests, a plausible summary, or a working happy path can still hide a mismatch between requested outcome, implemented behavior, documentation, and delivery claims.

Use it before broad code review when the main risk is not style or local correctness, but whether the delivered artifact is the right artifact.

## Inputs

- **intake-brief**: The original intent, target context, non-targets, and evidence expectations.
- **task-list**: The approved implementation slice and any priority ordering.
- **acceptance-criteria-set**: The explicit pass/fail contract, including negative criteria.
- **source-code**: The diff or implementation surface.
- **test-suite**: Tests, fixtures, snapshots, smoke logs, and validation output.

Also read requirements docs, specs, architecture notes, runbooks, or quality snapshots when they are referenced by the task.

## Process

### Step 1: Reconstruct the Intent Contract

State the intended outcome in one or two concrete sentences. Separate must-have behavior, non-targets, and later work. Do not infer extra scope from implementation shape.

### Step 2: Build a Coverage Matrix

Map each user requirement, acceptance criterion, and priority item to implementation evidence. Mark each row as implemented, partially implemented, deferred, contradicted, or unverifiable.

### Step 3: Compare Behavior to Claims

Check final messages, docs, quality reports, release notes, and test names against the actual code and runtime evidence. Flag any claim that turns simulated, fake, fixture, local-only, or partial evidence into a stronger statement.

### Step 4: Check Consistency Across Artifacts

Verify that code, tests, docs, runbooks, risk registers, and quality snapshots tell the same story. Mismatches are findings even when each file is locally coherent.

### Step 5: Classify Gaps

Prioritize:

- **Blocking**: Intent not implemented, wrong target, false completion claim, missing acceptance criterion, or unowned contradiction.
- **Should-fix**: Partial coverage or ambiguous evidence that could mislead a downstream reviewer.
- **Question**: Missing context that can change severity.

## Outputs

Produce a `review-report` with:

- intent contract summary
- coverage matrix
- implementation status by priority
- claim/evidence mismatches
- unresolved scope or consistency questions
- recommended next skill or repair path

## Quality Gate

- [ ] Every must-have intent item maps to code, test, documentation, or an explicit deferred/non-target decision.
- [ ] No simulated, fake, fixture, or local-only evidence is described as real runtime or production evidence.
- [ ] Completion status is no stronger than the weakest required evidence.
- [ ] Cross-file contradictions are either fixed or reported as findings.
