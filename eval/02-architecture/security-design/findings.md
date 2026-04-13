# Security Design QA Findings

## Status

- Current status: `tested`
- Evidence type: manual benchmark review + routed handoff review
- Scope covered:
  - one brownfield access-review architecture slice
  - one downstream handoff into `security-audit`

## What Changed

1. The skill now has a checked-in manual branch-pair benchmark review.
2. The repository now has a routed handoff review showing that the resulting
   threat model is actionable for downstream audit work.
3. The repository now has fixture-backed evidence for unsupported-flow
   hard-stop rules, evidence visibility risk, and brownfield coexistence
   controls in this skill.

## What We Learned

1. A strong baseline can already produce a serious threat model, so this is not
   a weak-control promotion.
2. Explicit `security-design` invocation materially improves downstream
   usability by turning boundary-level concerns into concrete controls,
   ship-blockers, and owned residual risks.
3. The skill adds the most value when a slice already has real architecture and
   API boundaries, but the team still needs a threat model that freezes
   brownfield trust assumptions before implementation.

## Open Issues

- Evidence is still narrow: one manual benchmark scenario is enough for
  `tested`, but not for any later promotion.
- The benchmark is manual rather than runner-backed because the preferred
  runner lanes were unstable on this wave.

## Notes

The current evidence is enough for `tested` because the manual branch pair and
the routed `security-audit` handoff both validate the central contract of the
skill.
