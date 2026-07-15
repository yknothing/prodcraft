# User Persona Set: Team Invite Release-1 Validation

> QA fixture for downstream skill evaluation. This is a synthetic, evidence-shaped artifact used to test handoff quality. It is not real production customer research.

## Fixture Research Summary

- **Interviews represented**: 7 interviews across 5 collaborative SaaS teams
- **Supplemental signal**: 14 onboarding support threads and 3 sales notes about team expansion friction
- **Direction under evaluation**: `email-invite-first`
- **What the fixture is meant to simulate**: completed `user-research` after the `team-invite` discovery path

## Persona 1: Workspace Owner Wendy

- **Role**: founder, team lead, or workspace owner at a 10-80 person product team
- **Primary goal**: bring a few coworkers into a shared workspace quickly so collaboration starts the same day
- **Pain points**:
  - current manual onboarding is inconsistent
  - inviting teammates should not require enterprise identity work
  - role setup is often unclear during invite
- **Behaviors**:
  - prefers fast email-based onboarding first
  - tolerates lightweight guardrails if the flow stays simple
- **Representative quote**: "I just need the team in the workspace today; we can get fancy later."

## Persona 2: Growing Admin Ian

- **Role**: admin or ops-influenced owner at a 100-300 person organization
- **Primary goal**: support team invites now without painting the company into a corner later
- **Pain points**:
  - email invite works today, but domain ownership and SSO questions are starting to appear
  - the team wants a path that can later grow into stronger onboarding without rework
- **Behaviors**:
  - accepts invite-first for release 1 if later enterprise paths remain possible
  - pays attention to role and policy drift as the team grows
- **Representative quote**: "Email invite is probably enough right now, but I do not want to rebuild the whole flow once the company gets bigger."

## Persona 3: Team Manager Maya

- **Role**: department or project manager inviting teammates into an existing workspace
- **Primary goal**: add people quickly and give them the right role without admin friction
- **Pain points**:
  - manual role assignment can slow down collaboration
  - the current onboarding path does not make role expectations obvious
- **Behaviors**:
  - values clarity and speed over centralized admin ceremony
  - only escalates to heavier onboarding when scale makes it unavoidable
- **Representative quote**: "Inviting someone should feel like starting work, not opening an IT project."

## Cross-Persona Synthesis

- **Primary pattern**: small-to-mid-size collaborative teams overwhelmingly prefer simple email invitation in release 1
- **Secondary pattern**: domain claim and SSO become relevant as the team scales, but they are not the dominant day-one blocker
- **Release-1 implication**: `email-invite-first` is the right first direction if role clarity and basic invite lifecycle controls are included
- **Non-goals that remained stable across the fixture**:
  - no enterprise identity-first onboarding in release 1
  - no admin bulk provisioning as the default first path
  - no attempt to solve every future org-onboarding path at once

## Open Questions Still Carried Forward

- should role selection happen during invite creation or after acceptance?
- what usage threshold makes domain claim or SSO a release-1 blocker instead of a later extension?
- when does admin bulk provisioning become a real early-segment need?
