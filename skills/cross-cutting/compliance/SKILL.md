---
name: compliance
description: Use when legal, contractual, regulatory, or internal policy requirements must be translated into engineering constraints, evidence, and approval checkpoints before delivery.
metadata:
  phase: cross-cutting
  inputs: []
  outputs:
    - compliance-guidance
  prerequisites: []
  quality_gate: Compliance obligations, evidence expectations, and approval points are explicit enough for planning, implementation, and release review
  roles:
    - product-manager
    - tech-lead
    - devops-engineer
  methodologies:
    - all
  effort: large
---

# Compliance

> Compliance is an engineering constraint only when it is translated into concrete controls, evidence, and release gates.

## Context

Use this skill when regulatory duties, customer contracts, data handling rules, or internal controls materially affect architecture, delivery, or operations.

## Inputs

- The relevant policy, contract, or regulatory requirement
- Affected systems, workflows, and environments
- Current evidence or control gaps

## Process

### Step 1: Identify the binding obligations

Separate binding requirements from preferences. Record the source and the affected system boundary.

### Step 2: Translate obligations into engineering controls

Map each obligation to concrete implementation, operational, or approval requirements.

### Step 3: Define evidence and checkpoints

State what documentation, test evidence, or approvals must exist before release.

### Step 4: Record unresolved risk

If the current plan cannot satisfy the requirement, document the gap, the risk owner, and the escalation path.

## Outputs

- **compliance-guidance** -- the mapped obligations, required controls, evidence expectations, and approval checkpoints

## Quality Gate

- [ ] Binding obligations are identified with source context
- [ ] Required controls are mapped to engineering work
- [ ] Release evidence and approval checkpoints are explicit

## Anti-Patterns

1. **Compliance by slogan** -- naming a standard without mapping controls changes nothing.
2. **Late legal surprise** -- waiting until release review to interpret obligations causes avoidable churn.
3. **Evidence after the fact** -- if proof is not planned early, it is usually missing when needed.

## Related Skills

- [requirements-engineering](../../01-specification/requirements-engineering/SKILL.md) -- captures regulated requirements
- [system-design](../../02-architecture/system-design/SKILL.md) -- maps controls into architecture
- [deployment-strategy](../../06-delivery/deployment-strategy/SKILL.md) -- enforces release approvals
