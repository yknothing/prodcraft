# Intake Brief: Team Invite Product Direction

## Work Summary

- **Request**: We need a team-invite capability so workspace owners can bring coworkers into a shared product space, but we are not yet sure whether release 1 should center on email invites, company-domain claiming, or admin-assisted bulk provisioning.
- **Why intake was used**: The request is new product work with multiple plausible directions and unclear release-1 scope.
- **Work type**: New Product
- **Entry phase**: 00-discovery
- **Recommended workflow**: greenfield
- **Scope assessment**: medium
- **Urgency**: normal

## Required Artifact

- **Artifact name**: `intake-brief`
- **Status**: approved
- **Approver**: user

## Routing Decision

1. **Recommended first skill**: `problem-framing`
   - **Output**: `problem-frame`, `options-brief`, `design-direction`
   - **Why this is next**: The product area is clear enough to enter discovery, but the release-1 direction is still fuzzy.
2. **Second skill**: `user-research`
   - **Output**: `user-persona-set`, `user-journey-map`
3. **Third skill**: `requirements-engineering`
   - **Output**: `requirements-doc`

## Question Budget

- **Questions asked**: 2
- **Did any answer change routing?** yes
- **If more than 3 questions were needed, why?**

## Alternatives Considered

- **Primary path chosen**: `problem-framing` -> `user-research` -> `requirements-engineering`
- **Alternative path considered**: go directly to `requirements-engineering`
- **Trade-off summary**: Direct requirements work would move faster, but risks locking in the wrong release-1 invite model before the product direction is framed.

## Key Risks

1. Release 1 could overfit to a provisioning model that only serves one segment.
2. The invite flow could silently expand into enterprise identity or IT-admin workflows before the first slice is understood.

## Fast-Track or Skipped Gates

- **Any shortcut taken?** no
- **If yes, why was it acceptable?**
- **What debt does this create?**

## Notes for Handoff

- Constraints: release 1 should create shared-workspace collaboration quickly; avoid forcing enterprise identity scope too early.
- Open questions:
  - Are most target customers inviting a handful of teammates or onboarding whole departments?
  - Is SSO/domain claim part of the first valuable release or a later expansion?
  - Is CSV/admin bulk provisioning a core path or only needed for larger customers?
- Context that downstream skills must preserve: do not silently choose an enterprise-first or email-only model before comparing directions.
- Should `problem-framing` run next? yes
