# Spec: Access Review Modernization Release 1

## Overview

Release 1 introduces a modern access-review experience that can run beside the
legacy module during audit season. The goal is to support current campaigns,
downloadable evidence packages, and tamper-evident audit history without
pretending that sync semantics, full historical migration, or every
reassignment path are already solved.

## Goals

- support release-1 campaign creation, listing, reviewer action capture, and
  evidence export
- preserve tenant-specific reviewer hierarchy rules for the confirmed release-1
  tenant set
- keep legacy coexistence explicit during audit season
- preserve compliance evidence integrity and auditability

## Non-Goals

- full migration of historical campaigns older than two years
- same-day or near-real-time sync guarantees before consistency semantics are
  resolved
- support for every reassignment or data-correction variant in release 1
- public contract exposure of migration-only or cutover-only operations

## Release-1 Contract Boundary

### Supported User and Admin Flows

- create and list current access-review campaigns
- view campaign detail and reviewer task state
- submit reviewer decisions for supported release-1 review tasks
- request supported reminder and reassignment flows
- download evidence packages and read tamper-evident audit history through the
  authorized release-1 surface

### Policy and Compatibility Boundaries

- tenant-specific hierarchy rules remain contractual and must stay visible in
  the release-1 behavior boundary
- legacy-read history for campaigns older than two years remains available
  through a compatibility path rather than becoming part of the canonical
  release-1 current-work model
- unsupported reassignment or data-correction variants must fail explicitly
  rather than falling through to guessed behavior

### Evidence and Audit Boundary

- evidence packages are release-1 deliverables, not internal debugging output
- audit history must remain tamper-evident and externally defensible

## Rollout and Coexistence Constraints

- release 1 must coexist with the legacy module during audit season
- no contract decision in this spec may assume full cutover before coexistence
  constraints are closed
- rollout must preserve access to historical evidence while current campaigns
  move onto the release-1 surface

## Open Questions

1. what consistency model should callers observe while new and legacy paths
   coexist
2. which tenant-specific hierarchy variants need first-class release-1 support
   and which can stay behind compatibility handling
3. which reassignment and data-correction variants must be promoted from
   explicit unsupported flow to supported release-1 behavior

## Downstream Handoff Notes

- `system-design` should preserve coexistence, evidence, and policy boundaries
  without silently closing the open sync question
- `api-design` should expose only supported release-1 contract surfaces and
  keep unsupported flows explicit
- `data-modeling` should preserve read-only history boundaries, retention, and
  tamper-evident audit requirements
