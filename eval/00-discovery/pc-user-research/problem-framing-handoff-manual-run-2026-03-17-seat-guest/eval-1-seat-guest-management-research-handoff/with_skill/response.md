# User Research Plan: Guest-First Coexistence Validation

## Source Context

- **Input artifact**: `problem-frame`
- **Why user-research was invoked**: problem-framing selected `guest-first coexistence` as the leading release-1 direction, but user evidence is still needed before requirements should begin
- **Direction to preserve during research**: validate guest-first coexistence first; do not silently expand release 1 into a pricing redesign, full seat-governance program, or procurement-led policy system

## Research Goal

Determine whether mid-market SaaS admins primarily need lightweight external collaboration in the first release, or whether the stronger immediate pain is internal seat governance or procurement-driven control.

## Question Budget

- **Additional questions asked in this run**: 0
- **Reason**: the framing artifact already defines the target operator, chosen direction, non-goals, and unresolved questions clearly enough to plan the research

## Research Questions

1. In current accounts, how are external collaborators handled today, and what workarounds are most painful?
2. What minimum guest restrictions are required for admins to adopt a guest-first release safely?
3. At what account size or buying posture do seat-governance or procurement controls overtake guest collaboration as the dominant first-release need?
4. Which stakeholder actually blocks adoption first: workspace admin, finance owner, procurement approver, or team lead?

## Participants to Recruit

- **Primary segment**: 4-6 workspace admins or operations owners at mid-market SaaS customers who currently manage paid seats and occasionally need external collaboration
- **Contrast segment**: 2-3 finance or procurement-influenced admins from larger accounts, used to test whether guest-first coexistence fails because approval or billing pressure arrives too early

## Methods

- semi-structured interviews with recent collaborator onboarding walkthroughs
- review of support tickets, account notes, or internal escalation themes related to guest access and seat exceptions
- lightweight follow-up survey only if interview evidence is split across account tiers

## What This Research Must Preserve

- release 1 is testing `guest-first coexistence`, not reopening the whole admin-modernization search
- pricing redesign, org-wide policy engines, and forced migration of the seat model remain non-goals by default
- unanswered questions should stay visible until user evidence resolves them

## Expected Outputs

- an evidence-backed `user-persona-set` covering the primary guest-first admin segment and any clearly distinct governance-heavy segment
- a `user-journey-map` for external collaborator onboarding under the current seat model
- explicit decision triggers for when guest-first coexistence is sufficient and when governance/procurement concerns must move into scope

## Handoff Note

`requirements-engineering` should begin only after the research confirms whether guest-first coexistence is truly the right first-release boundary and what minimum restrictions or approval expectations must accompany it. Until then, keep the non-goal of broad pricing or policy redesign explicit.
