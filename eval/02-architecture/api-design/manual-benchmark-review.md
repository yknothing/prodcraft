# API Design Manual Benchmark Review

## Scope

This note reviews the existing manual branch-pair comparison for `api-design`.

The evidence uses one brownfield architecture handoff and compares:

1. a baseline response without explicit skill guidance
2. the same scenario with explicit `api-design` skill guidance

Evidence directory:
`eval/02-architecture/api-design/manual-run-2026-03-17-access-review`

## Scenario: Access Review Modernization Release-1 Contract

### Baseline

The baseline produced a plausible API list, but it failed on the core contract boundary:

- it exposed `/sync` as a public release-1 endpoint
- it exposed migration-only `/legacy/import-historical-campaigns` and `/legacy/cutover` commands as public API
- it assumed same-day synchronization instead of preserving the unresolved consistency question

This is a material miss. The skill exists to keep public release-1 contract surfaces separate from migration and compatibility internals.

### With-Skill

The with-skill branch made the stronger contract decision:

- it defined only release-1 public REST surfaces
- it kept legacy coexistence behind an internal compatibility boundary
- it treated unsupported release-1 flows as explicit structured responses rather than inventing behavior
- it preserved open contract questions instead of closing them by assumption

That is a direct and meaningful quality improvement on the skill's central job.

## Judgment

This is narrower than a runner-backed isolated benchmark, and that limitation should stay explicit.

Even so, the branch-pair evidence is strong enough for a narrow `tested` judgment because:

- routed handoff review already proves the lifecycle boundary
- the manual pair shows a clear and material contract-quality lift on the same scenario

Current limits remain:

- the evidence is manual rather than runner-backed
- only one scenario exists
- there is no richer schema-heavy consumer API scenario yet

Those follow-ups still matter, but they do not outweigh the direct contract improvement already visible in the existing branch-pair evidence.

## Status Recommendation

- Recommended status: `tested`
