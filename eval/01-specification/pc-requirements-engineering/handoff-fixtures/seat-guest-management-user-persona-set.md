# User Persona Set: Seat and Guest Management Modernization

> QA fixture for downstream skill evaluation. This is a synthetic, evidence-shaped artifact used to test handoff quality. It is not real production customer research.

## Fixture Research Summary

- **Interviews represented**: 8 stakeholder interviews across 6 mid-market B2B SaaS accounts
- **Supplemental signal**: 21 support threads and 4 account-escalation summaries related to guest access, seat exceptions, and contractor onboarding
- **Direction under evaluation**: `guest-first coexistence`
- **What the fixture is meant to simulate**: completed `user-research` after the `seat-and-guest-management` discovery path

## Persona 1: Operations Admin Olivia

- **Role**: workspace administrator at a 150-400 seat SaaS customer
- **Primary goal**: let contractors, agencies, or auditors collaborate quickly without burning full paid seats
- **Pain points**:
  - current workaround is issuing full member seats to occasional external collaborators
  - revocation and visibility are manual, so admins fear guest sprawl
  - external collaborator requests arrive urgently and compete with finance approval processes
- **Behaviors**:
  - prefers lightweight access paths with guardrails over long approval chains
  - only escalates to finance when the access pattern starts to look persistent
- **Representative quote**: "Most of the time I just need to let someone in for a short collaboration window without turning them into a permanent seat."

## Persona 2: Finance Admin Fiona

- **Role**: finance or procurement-influenced system owner at a 500+ seat customer
- **Primary goal**: avoid uncontrolled seat leakage and surprise billing exposure
- **Pain points**:
  - guest and full-member usage are currently blurred together
  - finance hears about collaborator access only after seat counts move
  - exception handling is hard to audit
- **Behaviors**:
  - tolerates lightweight guest access only if visibility and approval triggers are explicit
  - cares more about policy thresholds than about day-to-day invite convenience
- **Representative quote**: "I do not need a giant redesign on day one, but I need to know when guest access starts behaving like paid-seat expansion."

## Persona 3: Team Lead Theo

- **Role**: delivery or project lead who needs outside collaborators for short-lived work
- **Primary goal**: bring a contractor or agency partner in the same day so project work does not stall
- **Pain points**:
  - asking for a full member seat feels heavy for short-term collaboration
  - admin-controlled workarounds slow down project starts
  - access boundaries are unclear once a collaborator is invited
- **Behaviors**:
  - will accept guardrails if onboarding stays fast
  - escalates only when access delays block customer-facing work
- **Representative quote**: "I need the collaborator in today, but I also need everyone to know they are not a normal full-seat member."

## Cross-Persona Synthesis

- **Primary pattern**: the most frequent immediate pain is lightweight external collaboration, not full seat-governance redesign
- **Secondary pattern**: finance and procurement pressure becomes decisive in larger accounts, but usually as a threshold question rather than a release-1 design center
- **Release-1 implication**: `guest-first coexistence` is the right first direction if the system preserves explicit guardrails, visibility, and revocation
- **Non-goals that remained stable across the fixture**:
  - no pricing or packaging redesign in release 1
  - no forced migration of all seat types
  - no org-wide policy engine as the day-one centerpiece

## Open Questions Still Carried Forward

- what guest restrictions are truly mandatory in release 1 versus later governance layers?
- at what usage threshold must finance approval or billing visibility become part of the flow?
- should approval behavior differ by account tier or remain optional in release 1?
