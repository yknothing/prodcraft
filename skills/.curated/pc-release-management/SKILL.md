---
name: pc-release-management
description: Use when a tested release candidate needs a coordinated go/no-go decision, release window, communication path, and ownership model before deployment proceeds.
metadata:
  phase: 06-delivery
  inputs:
  - delivery-decision-record
  - test-report
  - security-report
  - performance-report
  outputs:
  - release-plan
  prerequisites:
  - pc-testing-strategy
  quality_gate: Release scope, readiness decision, communication path, and execution ownership are explicit enough for deployment planning and stakeholder alignment
  roles:
  - tech-lead
  - qa-engineer
  - devops-engineer
  methodologies:
  - all
  effort: medium
  internal: false
  distribution_surface: curated
  source_path: skills/06-delivery/pc-release-management/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Release Management

> Turn a technically ready build into a deliberately coordinated release.

## Context

Release management decides whether the current candidate should ship now, under what constraints, and with which communication and ownership model.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 1: Decide the Release Scope

Confirm what is in, what is out, which findings are accepted, and which conditions would block the release. If a `delivery-decision-record` exists, anchor the release scope to that recorded branch or PR outcome instead of reconstructing the completion state from memory. Do not carry unresolved scope ambiguity into the deployment window.

### Step 2: Make the Go/No-Go Explicit

Summarize readiness across quality, security, performance, and operations. If the release is conditional, name the conditions in plain language instead of relying on implied tribal knowledge.

### Step 3: Set Window, Owners, and Communication

Define:

- release window
- responsible owner
- approvers and escalation contacts
- stakeholder communication moments before, during, and after release
- evidence required to declare success or abort

### Step 4: Hand Off a Concrete Release Plan

Produce a release plan that downstream deployment planning can execute. The plan should say what will ship, when, who coordinates, which checks gate expansion, and what happens if the release is paused.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Release scope and known exclusions are explicit
- [ ] Go/no-go decision is documented with rationale
- [ ] Owners, approvers, and escalation path are named
- [ ] Communication moments and success criteria are defined
- [ ] The plan is concrete enough for deployment strategy to execute

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/06-delivery/pc-release-management/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
