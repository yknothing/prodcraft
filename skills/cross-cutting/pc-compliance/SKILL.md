---
name: pc-compliance
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

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

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

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Binding obligations are identified with source context
- [ ] Required controls are mapped to engineering work
- [ ] Release evidence and approval checkpoints are explicit
