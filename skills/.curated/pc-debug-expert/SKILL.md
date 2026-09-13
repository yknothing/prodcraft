---
name: pc-debug-expert
description: Use when bugs, failing tests, regressions, flaky behavior, performance degradation, or runtime and skill-loading failures need causal diagnosis, especially when symptoms are ambiguous or attempted fixes have failed.
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
  internal: false
  distribution_surface: curated
  source_path: skills/04-implementation/pc-debug-expert/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Debug Expert

Explain the broken contract, choose the next useful check, and correct the responsible boundary. One decisive check can resolve a simple defect; ambiguity needs competing explanations.

## Context

See [context](references/context.md) for scope and [techniques](references/techniques.md) for a matching diagnostic recipe. Read [gotchas](references/gotchas.md) or [anti-patterns](references/anti-patterns.md) when the investigation stalls or confidence exceeds evidence.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### 1. Frame the Failure and System

State expected versus actual behavior, affected users/boundary, trigger and frequency. Read the complete error chain. Map the relevant input, control path, state owner and output; an exception may name the victim of earlier corruption.

Identify the observed artifact/revision, environment and configuration using existing evidence. Separate identity from reachability: missing logs may mean an old artifact, an unreached path or invisible output. Compare recent code, dependency, data and configuration changes; use history as a hypothesis source. Missing optional `pc-bug-history-retrieval` does not block diagnosis.

For live impact, route containment through `pc-incident-response` first; passive diagnosis can continue safely. Replays, fault injection, restarts, cache changes or removing a fix need an authorized safe environment. Never restore production harm just to prove a cause.

### 2. Build a Useful Feedback Signal

Choose the smallest check that reaches the real failure and tests the broken contract. Confirm it detects the unfixed behavior; preserve essential state, permissions, load and ordering while minimizing. A green test of another path is not useful feedback.

Use an assertion for logic, a repeatable measurement for performance, or controlled interleaving for a race. For intermittent failures, record conditions and a justified baseline; an unexplained green rerun is not resolution. Use passive evidence when active checks are unsafe. Missing source/tests need not block initial diagnosis; missing causal proof limits the claim to diagnosis or mitigation, not a verified fix.

### 3. Choose and Update the Explanation

State “X causes Y because Z” and the observation that would disprove it. For ambiguity, retain the live competing explanations. Choose a feasible, safe check whose possible outcomes separate them and change the next action; prefer existing evidence and low disturbance over blind rebuilding or patching.

Inspect actual boundary values. Separate observation, inference, prediction and result in existing notes/report. Isolate suspected causes; use controlled comparisons for interactions. Update explanations after each result; an inconclusive check is not confirmation.

Repeated failed corrections trigger a review of the causal model and fix layer. Count failed hypotheses/corrections, not file edits or probe cleanup. Route `course-correction-note` only for evidenced specification, architecture or planning contradictions; an access gap or failure count alone is not one.

### 4. Correct the Responsible Boundary

Explain the trigger, violated invariant, propagation and relevant enabling conditions. Identify counterevidence and why the chosen correction addresses the mechanism. Preserve scope and compatibility; for code changes, retain a failing regression check and use the TDD loop.

Correct the producer under local control, or enforce the owned contract at a trust/adapter boundary. Mark an external-dependency workaround and its removal condition. If a new symptom appears, compare versions and triggers before deciding whether it is an introduced regression, an unmasked defect or the same mechanism presenting differently.

### 5. Verify the Supported Claim

Compare unfixed failure and corrected success at the same relevant boundary with matched conditions. A preserved matching pre-fix run can supply the negative control; preserve unrelated work and containment. If the negative control does not fail, repair the signal or revisit the explanation.

Check surrounding risks exposed by the mechanism, such as neighboring inputs, tenant isolation, cancellation or repeated execution. Bound performance/flaky claims by the observed workload and repetitions. Missing proof limits the claim to diagnosis or mitigation. Clean up temporary probes and identify retained instrumentation.

### 6. Leave a Resumable Result

Produce `bug-fix-report` with status, identity, evidence, explanations, correction/containment, regression results and next action. Retain useful rejected hypotheses and the next discriminator. Review and verification consume the same revision and claim.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] The observed identity, failure contract and evidence limits are explicit
- [ ] A fixed claim explains a causal mechanism and has matching negative/positive evidence plus relevant regressions
- [ ] Diagnosis or mitigation identifies remaining proof and safe resumption conditions
- [ ] Experiments respect authority; containment is not root-cause proof
- [ ] Upstream contradictions route explicitly; other gaps have an owned next action

## Stop Signals

Pause the affected patch loop when checks add no information, changes confound the explanation, or a claim exceeds evidence. Resolve the missing discriminator and continue independent work. Familiarity, a matching ticket or another agent's conclusion never replaces current evidence.

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/04-implementation/pc-debug-expert/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
