---
name: pc-security-design
description: Use when the architecture is defined and the team must turn trust boundaries, sensitive data paths, and attacker assumptions into concrete control design before implementation and audit.
metadata:
  phase: 02-architecture
  inputs:
  - architecture-doc
  - api-contract
  outputs:
  - threat-model
  prerequisites:
  - pc-system-design
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
  source_path: skills/02-architecture/pc-security-design/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Security Design

> Make the security model an architectural decision, not a bug-fixing exercise after implementation.

## Context

Security design identifies what must be protected, who might abuse the system, and which controls must exist at each boundary.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

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

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Trust boundaries are explicit
- [ ] High-value assets and abuse paths are documented
- [ ] Required controls are assigned per boundary
- [ ] Logging and fail-closed expectations are clear
- [ ] Residual risks and unresolved assumptions are recorded for audit or follow-up

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/02-architecture/pc-security-design/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
