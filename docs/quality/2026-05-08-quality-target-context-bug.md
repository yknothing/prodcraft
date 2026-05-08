# Quality Target Context Bug

> Date: 2026-05-08
> Scope: Prodcraft intake and phase-05 quality routing.

## Symptom

A real agent run used Prodcraft to review a chatbot-like implementation that the
user later clarified was an agent-internal skill capability, not a standalone
external SaaS/API service. The routed quality pass produced a public-service
style report: open CORS, missing public API key/JWT/IP limits, Flask limiter
recommendations, dependency CVE release blocking, browser/API testing, and a
service release-block posture.

Those concerns may be valid for a public HTTP service. They were over-applied
to the observed target because the quality flow did not first record the target
runtime, exposure, and non-targets.

## Root Cause

The `intake-brief` carried work type, lifecycle phase, scope, and next skill,
but it did not carry `quality_target_context`. Downstream quality skills then
had to infer product shape from implementation details such as routes, HTTP
clients, CORS, Flask, or model provider adapters.

That inference path is unsafe in both directions:

- It can overbuild an agent-internal skill into a public-service architecture.
- It can under-review a real public service if the agent treats "internal" as a
  reason to skip trust-boundary work.

## Fixed Behavior

Every intake brief now carries `quality_target_context`:

- `runtime_context`
- `exposure_profile`
- `production_target`
- `non_targets`
- `evidence_refs`

The gateway and phase-05 quality docs require this context before service-style
quality chains run. `code-review`, `security-audit`, and `testing-strategy`
calibrate severity and test layers from this context rather than inferring a
public HTTP service from implementation shape.

## Safety Boundary

This fix does not create an internal-skill bypass. Agent-internal skills still
need security review for prompt injection, command safety, remote instruction
trust, tool/file/network side effects, dependency execution risk, secrets and PII
in artifacts, and curated export supply-chain safety.

Public services, internet-exposed components, multi-user APIs, sensitive-data
flows, auth/authz changes, privileged operations, and deployment exposure still
escalate to full service-style review. CORS, public auth, rate limiting,
browser behavior, API contracts, and abuse paths remain blocking when evidence
supports that exposure.

## Regression Protection

- Schema tests require `quality_target_context` in `intake-brief`.
- Gateway and phase docs are tested for the quality target context gate.
- Source and curated `code-review`, `security-audit`, and `testing-strategy`
  skills are tested for agent-internal versus public-service calibration.
- The public/global `prodcraft` gateway text is tested so partial-entry or
  missing-context installs cannot assume a public HTTP service.
