# Security Design Manual Benchmark Review

## Scope

This note reviews the checked-in manual branch-pair evidence for
`security-design`.

Evidence directory:
`eval/02-architecture/security-design/manual-run-2026-04-10-access-review`

The comparison uses one brownfield access-review modernization slice and keeps
the same architecture + API contract fixture pair across both branches:

1. `without_skill`
2. `with_skill`

## Scenario: Access Review Modernization Threat Model

### Baseline

The baseline threat model is already useful. It is not a weak control.

It identifies real trust boundaries, abuse paths, and controls, but it is
still looser than the skill-applied branch on the specific design contracts the
skill is supposed to freeze:

- unsupported-flow handling is described, but not turned into a fail-closed
  response contract
- release-blocking residual risks are present, but not cleanly separated from
  monitor-only issues
- downstream security review ownership remains implicit

### With-Skill

The with-skill branch is materially stronger:

- it maps required controls per trust boundary more explicitly
- it defines a concrete fail-closed `422 unsupported_flow` response contract
- it turns residual risks into owned items with clear ship-blocker markers
- it gives downstream security work a clearer split between policy gaps,
  control gaps, and implementation follow-ups

The response does contain some tool-chatter preamble, but the substantive
threat-model artifact is still materially better than baseline.

## Judgment

This is manual evidence, not a runner-backed isolated benchmark, and it should
stay labeled that way.

Even so, the branch pair shows a direct and meaningful quality lift on the
skill's central job: turning architecture + contract inputs into an actionable
security design artifact instead of a generic threat list.

## Status Recommendation

- Recommended status: `tested`
