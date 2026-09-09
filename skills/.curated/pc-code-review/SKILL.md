---
name: pc-code-review
description: Use when a concrete changeset needs review for correctness, security, maintainability, and compatibility before integration. Ground findings in changed behavior and explicit project policy; use the approved scope to calibrate severity.
metadata:
  phase: 05-quality
  inputs:
  - intake-brief
  - source-code
  - test-suite
  - task-list
  - api-contract
  - architecture-doc
  outputs:
  - review-report
  prerequisites:
  - pc-tdd
  quality_gate: Evidence-backed findings, integration blockers, review scope, and unresolved questions are recorded for the author
  roles:
  - reviewer
  - developer
  methodologies:
  - all
  effort: small
  internal: false
  distribution_surface: curated
  source_path: skills/05-quality/pc-code-review/SKILL.md
  public_stability: beta
  public_readiness: beta
---

# Code Review

> Systematic examination of code changes to catch defects, enforce standards, and share knowledge across the team.

## Context

Code review is the last quality gate before code enters the shared codebase. Calibrate `quality_target_context`, `runtime_context`, and `exposure_profile`; Inventing blockers from suspicion alone violates the evidence boundary.

See [context](references/context.md) and [anti-pattern](references/anti-patterns.md) notes.

## Inputs

[I/O contract notes](references/io-contract.md) define required inputs and authority.

## Process

### Step 0: Calibrate the Review Target

Read `quality_target_context` and establish the actual exposure before assigning severity. Do not infer a public-service release boundary from frameworks, route names, provider adapters, or HTTP clients. For an agent-internal skill, examine contracts, triggers, tool/file/network effects, prompt injection, artifact leakage, command safety, dependencies, and portability. CORS, public auth, rate limiting, sessions, and public API contracts require evidence of a public HTTP service.

Resolve missing or contradictory target context before exposure-dependent judgments. Continue independent checks; ask only for decision-changing facts or route a `course-correction-note` when the approved target is wrong.

### Step 1: Establish Scope

Read the approved change, acceptance conditions, affected callers, and non-targets. Reuse alignment and integrity findings for intent and evidence honesty. Add a named section to the existing `review-report` when useful; changing persona labels does not create independent review.

### Step 2: Trace Correctness and Security

Trace changed behavior through boundaries, null/error paths, authorization, input validation, command execution, secrets, dependencies, and failure handling. Check acceptance criteria and unresolved contract decisions. Apply web checks to actual web surfaces. Use `pc-security-audit` when deeper review is required; this pass does not replace it.

### Step 3: Check Maintainability and Performance

Look for confusing ownership, unnecessary complexity, duplication, undocumented decisions, unbounded work, N+1 queries, missing pagination, leaks, and blocking async operations. Name domain values when it clarifies ownership; consolidate shared concepts without coupling unrelated values. Ordinary literals do not require abstractions. Credentials and environment values need their actual security/configuration boundary.

In repositories that adopt Prodcraft's scanner, constrained literals use `ALLOW_MAGIC_NUMBER: reason, ticket` on the line or within two preceding lines. Explain why a constant/configuration entry is inappropriate and name the tracker id. Elsewhere follow local policy. Require concrete risk or an explicit policy violation for a blocker.

### Step 4: Check Verification and Compatibility

Inspect behavior tests, error paths, and assertion sensitivity; do not treat implementation-mirroring assertions as proof. Confirm test determinism and necessary dependency isolation. For brownfield work check coexistence, backward compatibility, migration safety, and authorization/tenant boundaries. Review relevant API documentation, logging, deferred-work traceability, and incomplete-feature isolation without demanding unrelated artifacts.

### Step 5: Report Actionable Findings

Use **Blocking** for concrete correctness, security, data-loss, contract, or explicit policy violations; **Should-fix** for nonblocking design concerns; **Nit** for requested style feedback; **Question** for uncertainty.

Each finding needs location, trigger, evidence-backed consequence, severity, and a correction or question. Cite the exact policy when policy alone blocks. Mark unverified concerns as questions. Report one root cause once, grouping consequences. No finding quota: when none remain, state the limits of the review.

For review-only requests, return findings without unsolicited edits or merge approval. Re-review unresolved findings and changed boundaries; do not repeat unchanged checks. Critique the code respectfully, keep scope to the changeset, and do not demand unrelated refactors.

## Automation Alignment

Only the source repository bundles `.githooks/pre-commit` and `scripts/hooks/no_magic_values_scan.py`. Public packages do not include these tools. Do not change Git configuration on invocation. For explicitly requested setup, verify the tools, inspect `core.hooksPath`, preserve existing hooks, and record how to restore the agreed setting.

See [Gotchas](references/gotchas.md) before debating scanner noise, approving one-off literals, or "cleaning up" hardcoded values by renaming variables.

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] Findings identify evidence, consequence, priority, and an actionable correction or question
- [ ] Blocking issues and security risks are explicit; an unresolved blocker prevents integration, not delivery of the review report
- [ ] Review scope, unverified concerns, and self-review limits are recorded
- [ ] The author can consume the report through `pc-receiving-code-review` without first resolving its findings

Integration still requires resolved blocking issues, author responses, and the reviewer approvals and CI checks required by the agreed path. A completed review report is not integration approval.

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/05-quality/pc-code-review/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
