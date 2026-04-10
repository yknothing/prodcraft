# Intake Security Review

> Date: 2026-04-10

## Scope

Security review of the `intake` skill package as the mandatory software-development gateway.

Reviewed artifacts:

- `skills/00-discovery/intake/SKILL.md`
- `skills/_gateway.md`
- `templates/intake-brief.md`
- `eval/00-discovery/intake/current-evidence-status.md`
- `eval/00-discovery/intake/post-redesign-benchmark-review.md`
- `eval/00-discovery/intake/post-redesign-integration-review.md`

## Threat Model

`intake` does not execute deployment or code-modification side effects directly. Its security impact comes from routing power:

1. bypassing the intake gate and letting execution begin without classification or approval
2. collapsing a high-risk request into an over-confident fast-track route
3. hiding unanswered constraints, making downstream skills act on unsafe assumptions
4. misclassifying production incidents and skipping containment-oriented handling

## Checks Performed

### Trust Boundary Review

- confirmed the skill still treats intake as a hard gate rather than a suggestion
- confirmed approval is required before downstream execution begins
- confirmed fast-track preserves observability instead of silently skipping the route
- confirmed hotfix and production-urgency language remains explicit in the taxonomy

### Prompt and Control-Surface Review

- checked that the skill constrains itself to classification, routing, and observable handoff
- checked that the skill does not embed hidden implementation instructions behind intake output
- checked that the skill records routing rationale and risks instead of laundering uncertainty away

### Data Exposure and Artifact Review

- checked that the required `intake-brief` artifact captures routing context rather than sensitive runtime secrets
- checked that no new external network, shell, or credential boundary is introduced by the skill package itself

## Findings

### Blocking

None.

### Medium

None.

### Accepted Residual Risk

- `intake` still depends on the caller honoring the approval gate in practice, but the repository now backs that expectation with workflow and artifact contracts rather than description-only wording.
- Discoverability harness instability remains a measurement problem, not a package-security blocker.

## Decision

Pass.

The package does not introduce a new side-effect channel and now has explicit controls around approval, risk visibility, and route observability. With benchmark, integration, findings, and this security review in place, `intake` is eligible for `production`.
