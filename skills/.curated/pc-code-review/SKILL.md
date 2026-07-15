---
name: pc-code-review
description: Use when a concrete code change is ready for review and the reviewer must evaluate correctness, security, maintainability, test adequacy, contract alignment, and brownfield safety before merge, especially when unsupported flows, backward compatibility, or release-boundary constraints must be enforced.
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
  quality_gate: All blocking issues resolved, no unresolved security findings, no unapproved magic values or hardcoded configuration
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

Read `quality_target_context` before assigning severity. Confirm whether the reviewed target is an agent-internal skill, host runtime tool, local harness, internal service, or public HTTP service.

Do not infer a public-service release boundary from framework shape, route names, provider adapters, or HTTP client usage alone. For an agent-internal skill, focus on skill contract correctness, trigger behavior, tool/file/network side effects, prompt injection, artifact leakage, command safety, dependency execution risk, and portability evidence. CORS, public auth, rate limiting, browser sessions, and public API contracts become blockers only when `exposure_profile` or direct evidence shows that the target is actually a public service.

If `quality_target_context` is missing or contradicts the code, stop and ask for the missing boundary or route a `course-correction-note` instead of continuing with assumed service blockers.

### Step 1: Understand the Context

Read the PR description, linked task slice, contract, and design context. Understand *what* the change is supposed to do now, what is explicitly out of scope, and which open questions remain unresolved before reading any code. If context is missing, request it before proceeding.

### Step 2: Check Correctness

Verify the code does what it claims. Trace the critical path through the logic. Check boundary conditions, null handling, and error paths. Compare behavior against the acceptance criteria.

### Step 3: Check Security

Scan for OWASP Top 10 issues: injection flaws, broken authentication, sensitive data exposure, XML external entities, broken access control, misconfiguration, XSS, insecure deserialization, known vulnerable components, insufficient logging.

### Step 4: Check Maintainability

Evaluate naming clarity, function and class structure, cyclomatic complexity, and duplication. Ask: will someone unfamiliar with this code understand it in six months? Flag overly clever code and missing documentation on non-obvious logic.

Also enforce baseline coding standards as **Blocking** issues:

- **No magic values**: Do not merge unexplained numeric literals, string literals, or structured literals that encode domain meaning, protocol fields, or policy thresholds.
- **No hardcoded configuration**: Do not merge environment-specific hosts, regions, tenant identifiers, URLs, credentials, API keys, or feature thresholds embedded directly in source without an approved configuration boundary.
- **Single source of truth**: Repeated literals that represent the same domain concept must converge to a named constant, configuration key, or shared schema -- unless the repetition is purely syntactic noise in tests.

Approved exceptions must use this exact token, either on the same line as the literal or within two preceding lines:

`ALLOW_MAGIC_NUMBER: reason, ticket`

Where `reason` is a short justification and `ticket` is a tracker id that explains why a named constant or configuration entry is not appropriate yet.

### Step 5: Check Tests

Verify test coverage for the changed code. Look for missing edge cases, missing error path tests, and tests that test implementation rather than behavior. Ensure tests are deterministic and do not rely on external state.

For brownfield or contract-sensitive work, explicitly check for:
- unsupported or deferred release-boundary behavior
- coexistence or backward-compatibility safety
- authorization and tenant-boundary coverage where policy remains partly unresolved

### Step 6: Check Performance

Look for N+1 query patterns, unbounded loops, memory leaks, missing pagination, unnecessary data loading, and blocking operations in async contexts. Flag any change that could degrade performance under load.

### Step 7: Provide Actionable Feedback

Classify each comment by severity:
- **Blocking**: Must fix before merge (bugs, security issues, data loss risks, unapproved magic values, hardcoded configuration).
- **Should-fix**: Strong recommendation, but not a merge blocker (readability, minor design issues).
- **Nit**: Optional improvement (style, naming preferences).
- **Question**: Clarification needed, not necessarily a problem.

Explain *why* something is a problem, not just *that* it is. Suggest a fix or direction when possible.

If a change silently hard-codes an unresolved architecture or contract decision, call that out as a correctness or scope-boundary issue, not a nit.

Keep the final review output disciplined:

- Default to a short, prioritized findings list rather than a broad checklist walkthrough.
- Do **not** include remediation snippets, replacement code, or step-by-step implementation instructions unless the prompt explicitly asks for them.
- Do **not** append a separate approval or merge-decision footer (`approve`, `reject`, `do not merge`) unless the prompt explicitly asks for approval state.
- When several checklist violations share one root cause, report the root cause once and mention secondary implications inside the same finding instead of emitting duplicate findings.
- Do **not** turn branch-mechanics observations into separate blocking findings when they only restate a higher-level contract or brownfield failure already identified.
- For brownfield or contract-sensitive changes, prioritize contract, coexistence, release-boundary, and test-coverage blockers ahead of generic maintainability commentary.
- Every blocking finding must be backed by evidence visible in the provided diff, contract, tests, or an explicit trace through the shown code path.
- Do **not** report hypothetical regressions unless the provided fixture lets you trace the claimed input to the claimed failure behavior.

When the caller asks for review feedback rather than remediation:

- default to findings-first output ordered by severity
- stay in review mode; do not provide code snippets, sample payloads, rewrite plans, or implementation steps unless the prompt explicitly asks for them
- do not end with approval-status language such as `approve`, `reject`, `do not merge`, or a merge-decision footer unless the caller explicitly asks for approval state
- collapse derivative checklist issues into the higher-severity root finding when they do not independently change the merge decision
- only emit a separate blocker when it changes the merge decision on its own; otherwise fold implementation details such as inverted conditions, missing constants, TODO notes, or dead-path observations into the parent finding
- if a concern is only a plausible consequence of a blocker already reported, keep it inside that blocker unless the supplied fixture proves it independently
- treat checklist-only policies such as TODO-without-ticket or one-off magic-string commentary as standalone findings only when they independently create release, contract, or safety risk; otherwise omit them from concise merge-focused output

For concise benchmark-style reviews, prefer the smallest set of findings that still preserves the real blockers.

## Review Etiquette

- Critique the code, never the person. Say "this function could be simplified" not "you wrote this wrong."
- Ask questions rather than making demands. "Have you considered X?" invites dialogue.
- Acknowledge good work. If a solution is elegant, say so.
- Keep review scope to the changeset. Do not demand refactors of unrelated code.
- Respond to review feedback within one business day.

## Review Checklist

- [ ] PR description explains the what and why
- [ ] Code compiles and tests pass in CI
- [ ] No hardcoded secrets, credentials, or PII
- [ ] No unapproved magic values or hardcoded configuration (see Blocking rules in Step 4)
- [ ] Error handling is explicit, not swallowed
- [ ] Public APIs have documentation
- [ ] Database migrations are backward-compatible
- [ ] No TODO comments without linked issues
- [ ] Logging is present at appropriate levels
- [ ] Feature flags wrap incomplete functionality

## Automation Alignment

This repository ships a lightweight, cross-language pre-commit hook that mirrors the same baseline expectations as the human review:

- Hook entrypoint: `.githooks/pre-commit`
- Scanner implementation: `scripts/hooks/no_magic_values_scan.py`

Enable it locally:

```bash
git config core.hooksPath .githooks
```

## Outputs

Produce only declared outputs at their documented quality boundary.

## Quality Gate

- [ ] All blocking issues are resolved
- [ ] No unresolved security findings
- [ ] Author has responded to all review comments
- [ ] At least one approving review from a qualified reviewer
- [ ] CI pipeline passes after final changes
- [ ] No unapproved magic values or hardcoded configuration remain in the changeset

## Gotchas

See [Gotchas](references/gotchas.md) before debating scanner noise, approving one-off literals, or "cleaning up" hardcoded values by renaming variables.

### Scanner catches an unavoidable protocol literal
- Trigger: A literal is mandated by a public protocol or platform contract.
- Failure mode: The team disables blocking checks globally to land one change.
- What to do: Keep blocking checks enabled and annotate only the constrained line with `ALLOW_MAGIC_NUMBER: reason, ticket`.
- Escalate when: The same contract literal appears in multiple files and should become a shared constant wrapper.

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/05-quality/pc-code-review/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
- Packaging stability: `beta`
- Capability readiness: `beta`
- Portability: `portable_with_caveat`
- Public caveat: Portable as skill guidance; full governance guarantees require the Prodcraft repository contracts and validation checks.
