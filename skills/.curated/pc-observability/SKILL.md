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
  quality_gate: Relevant execution boundaries emit structured, versioned observability events with clear field definitions, ownership, and downstream consumption paths
  roles:
  - developer
  - devops-engineer
  - tech-lead
  methodologies:
  - all
  effort: medium
  internal: false
  distribution_surface: curated
  source_path: skills/cross-cutting/pc-observability/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Observability

> If a boundary matters to delivery, debugging, cost, or safety, instrument it deliberately and name the signal contract explicitly.

## Context

This skill covers **cross-cutting instrumentation design**, not just runtime dashboards.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Map the Boundary That Must Become Visible

Start from the operational or product question, not from logging APIs.

Examples:

- which skill was invoked, by what route, and what happened next
- which model was used, with what token input and output
- which runner or wrapper failed, timed out, or retried
- which execution chain consumed the most cost or latency

If the question cannot change debugging, product decisions, or operational behavior, it is probably noise.

### Step 2: Define a Small, Versioned Event Schema

Write a stable schema before instrumenting code. At minimum, define:

- event types
- required fields shared by every event
- field names for model and token accounting
- null or unavailable rules for data the runner cannot provide
- versioning rules for future extensions

For AI execution telemetry, prefer canonical field names:

- `model_name`
- `token_input`
- `token_output`
- `token_total`

Do not invent token values. If the runner cannot provide usage, record `null` and state the source limitation explicitly.

### Step 3: Instrument at Shared Entry Points

Prefer wrappers, decorators, middleware, or context managers around execution boundaries instead of scattering ad hoc logging across many call sites.

Good candidates:

- model runner adapters
- skill dispatch or invocation boundaries
- benchmark or eval execution wrappers
- workflow orchestration seams

The goal is to capture execution once per boundary with a consistent schema.

For skill systems, capture two different signals:

- real model usage from the provider or runner when exposed
- exact byte/character measurements for what the skill loaded or deferred

Do not mix the two. Exact provider or runner usage answers token and billing questions. Skill-context byte/character counts answer context-size questions until a model-specific tokenizer or provider token-count API is available.

### Step 4: Separate Signal Capture from Signal Consumption

Keep the instrumentation contract independent from dashboards and alerts.

- this skill defines and emits structured events
- downstream operational skills consume those events for triage and alerting

That separation keeps instrumentation stable even when dashboard tools or operational needs change.

### Step 5: Validate with Real Failure and Cost Questions

Before calling the design complete, verify that a reviewer can answer:

- which skill ran
- which model and runner were used
- how many tokens were consumed
- how many skill-context bytes and characters were loaded or deferred
- where the time went
- where the chain failed or stopped

If those questions still require ad hoc grep or guesswork, the instrumentation boundary is incomplete.

### Step 6: Close the Runtime Feedback Loop

Do not stop at event emission. Summarize recurring failures, missing usage data, and high-risk actions on a regular cadence, then feed the findings back into:

- skill gotchas
- benchmark plans
- routing rules
- approval points for risky actions

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Important execution boundaries are explicitly identified before instrumentation begins
- [ ] Event schema is versioned and uses stable field names
- [ ] Skill invocation, runner execution, and model usage are distinguishable event types
- [ ] Model and token accounting fields use canonical names and never fabricate unavailable values
- [ ] Estimated runner usage is kept separate from exact provider or runner usage
- [ ] Skill-context measurements use exact byte/character counts unless a model-specific tokenizer or provider token-count API is available
- [ ] Runtime summaries can compare baseline and with-skill exact token usage before any token-saving claim is accepted
- [ ] Ownership and downstream consumption path are documented
- [ ] Runtime summaries can identify recurring failures, missing usage, and risky actions

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/cross-cutting/pc-observability/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
