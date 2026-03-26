---
name: code-review
description: Use when a concrete code change is ready for review and the reviewer must evaluate correctness, security, maintainability, test adequacy, contract alignment, and brownfield safety before merge, especially when unsupported flows, backward compatibility, or release-boundary constraints must be enforced.
metadata:
  phase: 05-quality
  inputs:
  - source-code
  - test-suite
  - task-list
  - api-contract
  - architecture-doc
  outputs:
  - review-report
  prerequisites:
  - tdd
  quality_gate: All blocking issues resolved, no unresolved security findings, no unapproved magic values or hardcoded configuration
  roles:
  - reviewer
  - developer
  methodologies:
  - all
  effort: small
  internal: false
  distribution_surface: curated
  source_path: skills/05-quality/code-review/SKILL.md
---

# Code Review

> Systematic examination of code changes to catch defects, enforce standards, and share knowledge across the team.

## Context

Code review is the last quality gate before code enters the shared codebase. It catches bugs that automated tests miss, prevents security vulnerabilities from reaching production, distributes system knowledge across the team, and maintains architectural consistency. Effective reviews balance thoroughness with turnaround speed -- a review that takes three days damages velocity more than the bugs it catches.

## Inputs

- **source-code**: The diff or changeset under review, with sufficient context to understand the change.
- **test-suite**: Accompanying tests that validate the change. Verify they exist and are meaningful.
- **task-list**: The reviewed implementation slice or task context that defines what was actually supposed to land now.
- **api-contract**: The contract or externally visible behavior that the changeset must preserve or implement.
- **architecture-doc**: System design context to verify the change aligns with architectural decisions.

In a lifecycle-aware system, review should not silently approve code that closes unresolved upstream questions by accident. Brownfield coexistence, unsupported release-1 flows, and contract boundaries are review concerns, not "later" concerns.

## Process

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

- **review-report**: Written feedback on the changeset with classified issues, approval status, and any follow-up actions. Stored as PR review comments or a formal review document.

## Quality Gate

- [ ] All blocking issues are resolved
- [ ] No unresolved security findings
- [ ] Author has responded to all review comments
- [ ] At least one approving review from a qualified reviewer
- [ ] CI pipeline passes after final changes
- [ ] No unapproved magic values or hardcoded configuration remain in the changeset

## Anti-Patterns

1. **Rubber-stamp reviews**: Approving without reading the code. This provides false confidence and defeats the purpose of review entirely.
2. **Gatekeeping**: Using reviews to enforce personal preferences rather than team standards. Reviews should apply agreed-upon conventions, not individual taste.
3. **Review bombing**: Dumping 50 comments at once without prioritization. Classify by severity so the author knows what matters.
4. **Scope creep**: Requesting large refactors unrelated to the change. Open a separate issue for broader improvements.
5. **Delayed reviews**: Letting PRs sit for days. Aim for initial review within 4 business hours for small changes, 1 business day for large changes.
6. **Approving guessed behavior**: Letting a changeset merge even though it resolves unsupported or unresolved release-1 behavior by assumption.

## Gotchas

See [Gotchas](references/gotchas.md) before debating scanner noise, approving one-off literals, or "cleaning up" hardcoded values by renaming variables.

### Scanner catches an unavoidable protocol literal
- Trigger: A literal is mandated by a public protocol or platform contract.
- Failure mode: The team disables blocking checks globally to land one change.
- What to do: Keep blocking checks enabled and annotate only the constrained line with `ALLOW_MAGIC_NUMBER: reason, ticket`.
- Escalate when: The same contract literal appears in multiple files and should become a shared constant wrapper.

## Related Skills

- [feature-development](../../04-implementation/feature-development/SKILL.md) -- produces the code under review
- [testing-strategy](../testing-strategy/SKILL.md) -- defines the testing standards applied during review
- [security-audit](../security-audit/SKILL.md) -- deeper security analysis for high-risk changes
- [tech-debt-management](../../08-evolution/tech-debt-management/SKILL.md) -- consumes review findings to track systemic issues

## Distribution

- Public install surface: `skills/.curated`
- Canonical authoring source: `skills/05-quality/code-review/SKILL.md`
- This package is exported for `npx skills add/update` compatibility.
