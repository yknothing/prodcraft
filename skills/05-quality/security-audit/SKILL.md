---
name: security-audit
description: Use when a reviewed change, release candidate, or high-risk slice must be challenged for abuse paths, trust-boundary failures, secret handling, dependency risk, or data exposure before release.
metadata:
  phase: 05-quality
  inputs:
  - source-code
  - architecture-doc
  - threat-model
  outputs:
  - security-report
  prerequisites:
  - code-review
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

Security audit is the focused quality pass for abuse resistance. It is narrower than full security architecture work and deeper than ordinary code review. Use it when a change crosses trust boundaries, handles sensitive data, touches authn/authz, introduces new dependencies, or materially changes deployment exposure.

In Prodcraft, security audit exists to stop avoidable release risk. It should produce concrete findings tied to the current slice, not a generic list of best practices.

## Inputs

- **source-code** -- The implementation under audit, including configuration and integration points visible in the change.
- **architecture-doc** -- Trust boundaries, component interactions, and intended control points.
- **threat-model** -- Known attacker capabilities, abuse cases, and assumptions to verify when one exists.

## Process

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

- **security-report** -- Findings, risk classification, evidence, remediation guidance, and explicit release recommendation.

## Quality Gate

- [ ] Trust boundaries for the change were reviewed explicitly
- [ ] High and critical findings are resolved or formally accepted
- [ ] Sensitive data handling and secret exposure were checked
- [ ] Dependency and configuration changes were reviewed for security impact
- [ ] The release recommendation is explicit: pass, conditional pass, or block

## Anti-Patterns

1. **Scanner-only audit** -- treating tool output as the entire audit.
2. **Checklist without context** -- reporting generic issues that do not apply to the actual slice.
3. **Security as post-release paperwork** -- auditing after the rollout decision is already made.
4. **Severity without exploit path** -- labeling issues without explaining how the system could actually be abused.

## Related Skills

- [code-review](../code-review/SKILL.md) -- catches general correctness and maintainability issues before the deeper security pass
- [testing-strategy](../testing-strategy/SKILL.md) -- incorporates security checks into the broader verification plan
- [deployment-strategy](../../06-delivery/deployment-strategy/SKILL.md) -- consumes the audit when rollout risk or blast radius must be constrained
- [security-design](../../02-architecture/security-design/SKILL.md) -- provides deeper threat modeling and control design upstream
