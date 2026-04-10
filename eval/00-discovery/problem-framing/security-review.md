# Problem Framing Security Review

> Date: 2026-04-10

## Scope

Security review of the `problem-framing` skill package as the second entry-layer skill used after routing is already clear.

Reviewed artifacts:

- `skills/00-discovery/problem-framing/SKILL.md`
- `eval/00-discovery/problem-framing/findings.md`
- `eval/00-discovery/problem-framing/isolated-benchmark-review.md`
- `eval/00-discovery/problem-framing/intake-handoff-review.md`

## Threat Model

`problem-framing` does not directly execute code or release actions. Its security impact comes from framing mistakes that could smuggle unsafe commitments downstream:

1. converting exploratory directions into hidden implementation commitments
2. dropping non-goals or unresolved questions that protect scope and trust boundaries
3. bypassing intake and behaving like an alternate gateway with weaker controls
4. inventing confidence that later skills interpret as an approved product or security decision

## Checks Performed

### Boundary and Role Review

- confirmed the skill stays downstream of intake rather than replacing it
- confirmed the skill compares directions but does not silently choose architecture or implementation details
- confirmed unresolved questions and non-goals are preserved as first-class output

### Safety and Misuse Review

- checked that the skill pushes ambiguity into explicit trade-offs instead of hiding it
- checked that the handoff shape keeps later security-sensitive decisions visible
- checked that no external execution or credential boundary is introduced by the package

## Findings

### Blocking

None.

### Medium

None.

### Accepted Residual Risk

- The package still depends on downstream skills to honor unresolved questions instead of force-closing them, but the artifact contract now makes those open issues explicit and auditable.

## Decision

Pass.

The package preserves entry-layer safety constraints, keeps uncertainty visible, and does not introduce a hidden execution or data-exposure channel. It is eligible for `production`.
