# Verification Before Completion Security Review

> Date: 2026-04-10

## Scope

Security review of the `verification-before-completion` skill package as the final honesty gate before completion, release, or incident-resolution claims.

Reviewed artifacts:

- `skills/cross-cutting/verification-before-completion/SKILL.md`
- `skills/cross-cutting/verification-before-completion/references/gotchas.md`
- `eval/cross-cutting/verification-before-completion/findings.md`
- `eval/cross-cutting/verification-before-completion/isolated-benchmark-review.md`
- `eval/cross-cutting/verification-before-completion/completion-claim-review.md`

## Threat Model

This package directly protects against false release and handoff claims. Its security risk comes from failure to enforce evidence:

1. letting stale or partial checks be presented as proof
2. permitting hallucinated file, diff, or command evidence
3. treating fast-track work as exempt from verification discipline
4. allowing release-ready or incident-resolved claims without current proof

## Checks Performed

### Claim-to-Evidence Boundary Review

- confirmed the skill requires an explicit claim before verification begins
- confirmed the package still requires current evidence rather than proxy or historical proof
- confirmed artifact and handoff integrity checks remain part of the contract

### Misuse and Abuse Review

- checked that the package explicitly closes the fast-track loophole
- checked that it rejects conversational-history-only proof
- checked that it does not expand into destructive operations on its own; it only governs claim discipline

## Findings

### Blocking

None.

### Medium

None.

### Accepted Residual Risk

- The package still depends on downstream operators actually running the required checks, but it now makes skipped proof visible enough to block an honest completion claim.

## Decision

Pass.

This package is now strong enough to be part of the production public core rather than a beta-only evidence gate.
