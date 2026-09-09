---
name: pc-systematic-debugging
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
  quality_gate: Fixed claims require causal and regression evidence; limited diagnoses identify missing proof and resumption conditions, with upstream contradictions routed explicitly
  roles:
  - developer
  - tech-lead
  - qa-engineer
  methodologies:
  - all
  effort: medium
---

# Systematic Debugging

> Do not claim a code fix without an evidenced cause and verification of the changed behavior.

## Context

Turn a failure into a defensible correction or an explicit diagnosis limit.
See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes. Use [gotchas](references/gotchas.md) when a matching failure pattern appears.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Establish Evidence and Safety

Read the complete error and cause chain. Confirm the observed revision/artifact, environment, and configuration using existing identity and runtime evidence. Compare recent code, dependency, and configuration changes.

Separate code identity from reachability: a missing log marker can mean stale deployment, wrong logging, or a current code path that was never reached. Preserve observations while distinguishing these hypotheses.

Live user impact routes through `pc-incident-response` for containment first. Use passive evidence before probes. Replays, fault injection, restarts, cache changes, or removing a fix require an authorized environment where their effects are safe; do not restore a harmful production condition merely to prove causality.

### Step 2: Define and Reproduce the Failure

Record expected versus actual behavior, affected boundary, trigger, and observed frequency. If history may help, use `pc-bug-history-retrieval` as a hypothesis source, not proof.

Build the smallest safe reproducer: an automated test where possible, otherwise a repeatable manual procedure. For intermittent failures, control ordering/state or measure a justified failure-rate baseline; an unexplained green rerun is not resolution. Choose a recipe from [techniques](references/techniques.md) only when needed.

When reproduction or active verification is unsafe or unavailable, preserve containment and current evidence. Report the diagnosis as limited or unverified, the missing discriminator, owner, and safe resumption condition. This completes a bounded investigation report, not a verified fix.

### Step 3: Test a Falsifiable Hypothesis

State “X causes Y because Z,” predict supporting and disproving observations, and run the cheapest discriminating check. Inspect the real boundary values before changing the theory. Record hypothesis, prediction, and result in a compact journal; vary one suspected cause per experiment.

A failed correction triggers reassessment. After repeated failures against the same symptom, pause patching and review the causal model and fix layer. Count failed hypotheses/corrections, not file edits or probe cleanup. Produce `course-correction-note` only when evidence identifies a requirements, architecture, or planning contradiction. An access or reproduction gap alone is not an upstream design defect.

### Step 4: Choose the Smallest Causal Correction

Explain the cause using the observed mechanism and relevant counterevidence. Preserve the accepted scope and compatibility boundary. For a local defect, reuse the reproducer as TDD regression protection before implementation expands. For an upstream contradiction, hand off its evidence and required decision before dependent edits.

Distinguish a permanent correction from a workaround. A different failure after a change is a new hypothesis to investigate; it does not by itself prove that the first fix worked or should be reverted.

### Step 5: Verify the Claim

In a safe isolated comparison, show the failure on the unfixed revision and success on the corrected revision, holding relevant inputs/environment constant. A preserved matching pre-fix run can supply the negative control; do not repeat destructive actions or disturb unrelated work. Run the affected surrounding checks.

If the negative control does not fail, return to the hypothesis loop. If causality cannot be checked, narrow the report to diagnosis or mitigation with explicit verification gaps; do not label it fixed. Clean up temporary probes and identify retained instrumentation.

### Step 6: Hand Off the Result

Produce `bug-fix-report` with status, evidence/reproducer, cause or remaining hypotheses, correction/workaround boundary, regression results, containment, and next action. Review and verification consume the same revision and evidence. Keep failed hypotheses only when they explain the remaining uncertainty or prevent repeated work.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Observed revision, environment, failure boundary, and evidence limits are explicit
- [ ] A fixed claim has a falsifiable cause, matching negative/positive evidence, and relevant regression checks
- [ ] Diagnosis-only or mitigation outcomes state what is unverified and how verification can resume
- [ ] Experiments respect the actual environment and authority; containment is not root-cause proof
- [ ] Upstream contradictions route through `course-correction-note`; other gaps have an owned next action

## Stop Signals

Pause the affected patch loop when evidence was not read, several suspected causes changed at once, repeated corrections add no new information, or a success claim exceeds the observed result. Resolve the missing discriminator before continuing. Prior familiarity, a similar ticket, or another agent's conclusion never replaces current evidence.
