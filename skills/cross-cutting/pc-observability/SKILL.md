---
name: pc-observability
description: Use when code, workflows, or AI execution paths need structured telemetry such as logs, metrics, traces, skill-invocation records, model-usage accounting, or token usage records so behavior, failures, and cost stay observable across the lifecycle.
metadata:
  phase: cross-cutting
  inputs: []
  outputs:
    - observability-spec
    - execution-event-schema
  prerequisites: []
  quality_gate: Signal contracts answer the agreed questions with supported fields, ownership, consumers, and explicit design versus runtime evidence
  roles:
    - developer
    - devops-engineer
    - tech-lead
  methodologies:
    - all
  effort: medium
---

# Observability

> Make the boundaries that matter to debugging, delivery, cost, or safety observable.

## Context

This skill designs instrumentation contracts. [Context](references/context.md) separates signal production from monitoring; [anti-patterns](references/anti-patterns.md) identify common mistakes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Name the Consumer's Question

Choose questions that change an actual decision: which request/job failed, where latency occurred, which skill/runner ran, or what an AI invocation cost. Identify the boundary, consumer, and required evidence before choosing a logging API. Discard signals with no useful consumer.

### Step 2: Reuse or Define the Signal Contract

Start with the existing log, metric, trace, or event schema. Define only needed changes: identity/correlation, outcome, timing, field meaning, units, unavailable-data rules, and version compatibility. Consider data sensitivity and cardinality before collecting payloads or labels.

For AI accounting, use `model_name`, `token_input`, `token_output`, and `token_total`. Record unavailable provider/runner usage as `null` with its source limitation; never invent it. Keep estimated runner usage separate from exact provider or runner usage.

For skill-context measurements, report exact byte/character counts for loaded or deferred content. These are not token counts; label any estimate separately unless a model-specific tokenizer or provider token-count API supplies the count.

### Step 3: Instrument the Relevant Boundary

Use an existing request middleware, job wrapper, runner adapter, or workflow seam when it captures the event once with consistent meaning. Avoid both scattered duplicate logging and a new shared abstraction that a single local change does not need.

Ordinary application instrumentation need not emit AI fields. In AI systems, distinguish skill invocation, runner execution, and model usage so retries and nested work are not double-counted.

### Step 4: Validate Scope and Evidence

Trace representative success/failure signals to the selected questions and the real emitting path. Check identity, units, outcomes, timing, correlation, and missing-data handling. Simple log inspection is sufficient when reliable; no dashboard or backend is mandatory.

A design-only request may deliver a schema and verification plan, with emission explicitly unverified. An implementation claim needs observed signals from the instrumented path. A token-saving claim additionally needs comparable baseline and with-skill exact usage evidence; changed source size alone is insufficient.

### Step 5: Assign Consumption and Follow-Up

Name who consumes the signals and when to review them. Keep capture independent from dashboard/alert implementation. Route actual recurring failures or missing evidence to the relevant code or operational owner. Skill systems may update gotchas, benchmark plans, or routing from those observations; general application telemetry need not produce those artifacts.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Each selected question maps to a scoped signal and an accountable consumer
- [ ] Field meanings, units, schema compatibility, and unavailable values are explicit
- [ ] AI usage and skill-context rules apply only to their actual boundaries
- [ ] Exact usage, estimates, and byte/character measurements remain distinct
- [ ] Claims match design or runtime evidence; any token-saving claim has a comparable exact baseline
- [ ] Ownership, consumption, and unresolved verification are documented
