---
name: pc-security-audit
description: Use when a reviewed change, release candidate, or high-risk slice must be challenged for abuse paths, trust-boundary failures, secret handling, dependency risk, or data exposure before release.
metadata:
  phase: 05-quality
  inputs:
  - intake-brief
  - source-code
  - architecture-doc
  - threat-model
  outputs:
  - security-report
  prerequisites:
  - pc-code-review
  quality_gate: High and critical findings are resolved or explicitly accepted, abuse paths are reviewed, and release-blocking security risks are documented
  roles:
  - reviewer
  - qa-engineer
  - devops-engineer
  methodologies:
  - all
  effort: medium
---

# Security Audit

> Challenge the change from an attacker and misuse perspective before it ships.

## Context

Security audit is the focused quality pass for abuse resistance.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 0: Calibrate the Security Target

Read `quality_target_context` before mapping attack surface. Confirm whether the reviewed target is an agent-internal skill, host runtime tool, local harness, internal service, or public HTTP service.

Do not downgrade baseline security because the target is internal. An agent-internal skill still needs review for prompt injection, command safety, remote instruction trust, tool/file/network side effects, secrets and PII in prompts, examples, logs, and artifacts, dependency execution risk, and public export supply-chain safety.

Escalate to full service-style audit when `runtime_context=public_service`, `exposure_profile=public_internet`, or evidence shows externally reachable behavior, multi-user access, sensitive data handling, auth/authz, privileged operations, new deployment exposure, or service-to-service trust boundaries. Only then should CORS, public auth, rate limiting, browser session handling, and internet abuse paths become release blockers.

If target context is missing or contradictory, stop and request the boundary or route a `course-correction-note`; do not invent public service blockers from HTTP-shaped implementation details alone.

### Step 1: Map the Attack Surface

List the externally reachable paths, privileged operations, secret stores, data flows, and dependency changes involved in the slice. Focus on what changed, not the entire product.

### Step 2: Inspect Trust Boundaries

Check authentication, authorization, tenancy isolation, input validation, output encoding, secret handling, and failure modes. Confirm the implementation matches the intended trust model instead of assuming the architecture doc was followed.

### Step 3: Check Supply Chain and Configuration Risk

Review dependency additions or upgrades, deployment configuration, default exposure, logging of sensitive fields, and environment-specific behavior. Security failures often come from unsafe defaults rather than the core business logic.

### Step 4: Write a Release-Useful Report

Classify findings by severity and exploitability. Separate:

- release blockers that must be fixed now
- medium-risk issues that need an owner and follow-up date
- accepted risks with explicit rationale

Every finding should point to the affected boundary, evidence, and expected remediation direction.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Trust boundaries for the change were reviewed explicitly
- [ ] High and critical findings are resolved or formally accepted
- [ ] Sensitive data handling and secret exposure were checked
- [ ] Dependency and configuration changes were reviewed for security impact
- [ ] The release recommendation is explicit: pass, conditional pass, or block
