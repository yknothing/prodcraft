# Domain Modeling to Spec Writing Handoff Review

## Goal

Verify that `domain-modeling` produces a `domain-model` artifact that
`spec-writing` can consume without inventing migration truths or collapsing
brownfield compatibility boundaries.

## Scenario

- `access-review-modernization-domain-model`

This is a brownfield modernization slice where:

- current campaigns move onto a new release-1 surface
- historical campaigns older than two years remain behind a legacy-read
  boundary
- tenant hierarchy rules remain contractual
- sync semantics and some reassignment flows are still open questions

## Artifacts Reviewed

- manual benchmark evidence:
  - `manual-run-2026-04-10-access-review/.../without_skill/response.md`
  - `manual-run-2026-04-10-access-review/.../with_skill/response.md`
- downstream consumer check:
  - `../spec-writing/manual-run-2026-04-10-access-review/.../with_skill/response.md`

## Review Findings

## 1. The baseline model would push spec work toward the wrong contract

The baseline notes make two downstream mistakes easy:

- they normalize sync into a first-class domain concern too early
- they treat legacy history as an eventual copy of the new canonical model

That is exactly how later spec work drifts into import, cutover, and same-day
consistency assumptions.

## 2. The skill-applied model gives spec-writing a safer boundary map

The with-skill branch is fit for downstream use because it:

- names the stable current-work entities explicitly
- marks legacy history as compatibility-only
- keeps policy compatibility separate from review operations
- preserves unresolved flows as open questions instead of false certainty

## 3. The downstream spec already shows the lift

The `spec-writing` with-skill branch consumes the stronger domain model in the
right way:

- release-1 scope stays separate from migration work
- unsupported reassignment and data-correction variants stay explicit
- the open sync question remains visible instead of becoming an invented public
  contract

## Assertion Review

| Assertion | Review result | Notes |
|---|---|---|
| canonical-vs-compatibility-boundary-visible | pass | `LegacyCampaignReference` stays compatibility-only in the with-skill branch. |
| glossary-stabilizes-spec-language | pass | Campaign, task, assignment, evidence, and audit language remain consistent downstream. |
| sync-question-not-laundered | pass | The with-skill model refuses a dedicated sync context while semantics are unresolved. |
| downstream-spec-consumable | pass | The resulting spec preserves release-1 and coexistence boundaries cleanly. |

## Conclusion

This routed handoff review is enough to support a narrow `tested` decision when
combined with the manual benchmark review.
