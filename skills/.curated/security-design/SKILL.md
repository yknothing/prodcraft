---
name: security-design
description: Use when the architecture is defined and the team must turn trust boundaries, sensitive data paths, and attacker assumptions into concrete control design before implementation and audit.
metadata:
  phase: 02-architecture
  inputs:
  - architecture-doc
  - api-contract
  outputs:
  - threat-model
  prerequisites:
  - system-design
  quality_gate: Trust boundaries, abuse paths, and required controls are explicit enough to guide implementation and security review
  roles:
  - architect
  - tech-lead
  - devops-engineer
  methodologies:
  - all
  effort: medium
  internal: false
  distribution_surface: curated
  source_path: skills/02-architecture/security-design/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Security Design

> Make the security model an architectural decision, not a bug-fixing exercise after implementation.

## Context

Security design identifies what must be protected, who might abuse the system, and which controls must exist at each boundary. It sits upstream of security audit: the goal here is to design the defenses, not just inspect the code later.

In Prodcraft, security design is most valuable when the system adds new trust boundaries, handles sensitive data, or depends on brownfield coexistence where old and new controls may differ.

## Inputs

- **architecture-doc** -- Defines the system boundaries, deployment topology, and interaction patterns.
- **api-contract** -- Identifies externally visible actions, data entry points, and policy-sensitive operations.

## Process

### Step 1: Mark Assets and Trust Boundaries

Identify the data, operations, and integrations that would matter to an attacker or regulator. Draw the trust boundaries explicitly: browser to backend, service to service, job worker to datastore, admin surface to normal user surface.

### Step 2: Enumerate Abuse Paths

For each boundary, ask:

- how could an unauthorized actor reach this path
- what happens if input is malicious, replayed, or oversized
- what data could leak through logs, errors, or side channels
- how could rollout or coexistence create a weaker path than the intended one

### Step 3: Assign Concrete Controls

Define the required controls at each boundary:

- authentication and session controls
- authorization and tenant isolation
- input validation and output encoding
- secret handling and key rotation expectations
- audit logging, alerting, and fail-closed behavior

### Step 4: Record the Threat Model

Capture attacker assumptions, control decisions, unresolved risks, and the checks downstream phases must enforce. The output should be actionable enough that implementation and security audit know what to build and what to verify.

## Outputs

- **threat-model** -- Assets, trust boundaries, abuse paths, required controls, and explicit residual risks.

## Quality Gate

- [ ] Trust boundaries are explicit
- [ ] High-value assets and abuse paths are documented
- [ ] Required controls are assigned per boundary
- [ ] Logging and fail-closed expectations are clear
- [ ] Residual risks and unresolved assumptions are recorded for audit or follow-up

## Anti-Patterns

1. **Security by generic checklist** -- controls that ignore the real boundaries of the system.
2. **Auth-only thinking** -- focusing on login while ignoring authorization, secret handling, or data leakage.
3. **Invisible residual risk** -- acting as if security is complete when key assumptions remain open.
4. **Brownfield blind spot** -- designing new controls without modeling weaker legacy paths still in service.

## Related Skills

- [system-design](../system-design/SKILL.md) -- supplies the structural boundaries to secure
- [security-audit](../../05-quality/security-audit/SKILL.md) -- verifies the implementation against this design
- [deployment-strategy](../../06-delivery/deployment-strategy/SKILL.md) -- uses the threat model when rollout posture affects exposure
- [monitoring-observability](../../07-operations/monitoring-observability/SKILL.md) -- exposes the signals needed to detect security-relevant failure modes

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/02-architecture/security-design/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
