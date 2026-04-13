# Domain Modeling Manual Benchmark Review

## Scope

This note reviews the checked-in manual branch-pair evidence for
`domain-modeling`.

Evidence directory:
`eval/01-specification/domain-modeling/manual-run-2026-04-10-access-review`

The comparison uses one brownfield access-review modernization slice and keeps
the same requirement fixture across both branches:

1. `without_skill`
2. `with_skill`

## Scenario: Access Review Modernization

### Baseline

The baseline domain notes are plausible, but they miss the central boundary
discipline the skill is supposed to teach:

- they treat `Sync Job` as a first-class domain object even though sync
  semantics remain unresolved
- they describe `Legacy Campaign Mirror` as if historical campaigns will
  gradually become the same canonical concept as current campaigns
- they justify bounded contexts by technical concern rather than stable
  business-language boundaries
- they never turn campaign, task, assignment, evidence, and audit language into
  a durable glossary

That is enough to distort downstream specification or architecture work.

### With-Skill

The skill-applied branch is materially stronger on the contract that matters:

- it names stable business entities instead of implementation helpers
- it keeps `LegacyCampaignReference` compatibility-only instead of quietly
  promoting history into the canonical release-1 model
- it separates review operations, policy compatibility, and evidence/audit into
  justified bounded contexts
- it refuses to invent a dedicated sync bounded context while sync semantics
  are still open
- it leaves partially understood reassignment and data-correction behavior as
  explicit domain questions rather than laundering them into the model

## Judgment

This is manual evidence, not a clean runner-backed isolated benchmark, and that
limitation should stay explicit.

Even so, the branch pair shows a direct and meaningful quality lift on the
skill's central job:

- canonical ownership language is clearer
- compatibility-only concepts stay visible
- bounded contexts are justified instead of overfit
- the artifact is materially safer for downstream spec writing

## Status Recommendation

- Recommended status: `tested`
