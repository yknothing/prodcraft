# User Research Plan: Team Invite Release-1 Validation

## Source Context

- **Input artifact**: `problem-frame`
- **Why user-research was invoked**: problem-framing selected `email-invite-first` as the leading release-1 direction, but user evidence is still needed before requirements should begin
- **Direction to preserve during research**: validate `email-invite-first` first; do not silently expand release 1 into enterprise identity or bulk-admin scope

## Research Goal

Determine whether the early target segment is primarily lightweight, owner-led team invitation or whether release 1 must absorb stronger domain-claim or bulk-provisioning requirements sooner than expected.

## Question Budget

- **Additional questions asked in this run**: 0
- **Reason**: the framing artifact already defines the user hypothesis, non-goals, and open questions clearly enough to plan the research

## Research Questions

1. In the first target segment, how do workspace owners usually bring teammates into a shared tool today?
2. At what company size or operational maturity does domain claim or SSO become a must-have rather than a later extension?
3. How often is admin-assisted bulk onboarding needed before the first collaborative workflow is valuable?
4. Should initial role assignment happen during invite creation or after acceptance for the early segment?

## Participants to Recruit

- **Primary segment**: 4-6 workspace owners or team leads at small-to-mid-size collaborative teams that currently add a handful of coworkers manually
- **Contrast segment**: 2-3 administrators or ops-oriented buyers from more identity-heavy organizations, used to test whether enterprise-oriented needs are urgent or merely upcoming

## Methods

- semi-structured interviews with workflow walkthroughs
- artifact review of current invite/onboarding steps, if participants can share them
- lightweight follow-up survey only if interview signals conflict on domain claim or bulk provisioning urgency

## What This Research Must Preserve

- release 1 is testing `email-invite-first`, not reopening the whole direction search
- enterprise identity and bulk provisioning remain non-goals by default unless evidence contradicts that assumption
- unanswered questions should stay visible until user evidence resolves them

## Expected Outputs

- an evidence-backed `user-persona-set` for the primary invite-first segment and any clearly distinct enterprise-leaning segment
- a `user-journey-map` from "need to add coworkers" through invite acceptance and first collaboration
- explicit decision triggers for when domain claim or bulk provisioning should move into scope

## Handoff Note

`requirements-engineering` should begin only after the research confirms whether the primary release-1 segment is genuinely lightweight invite-first and whether role-selection behavior or enterprise onboarding pressure changes the boundary. Until then, keep the release-1 non-goal of forced enterprise identity scope explicit.
