# Intake Brief: Access Review Modernization Direction

## Work Summary

- **Request**: Modernize the quarterly access-review workflow, but release 1 must coexist with the legacy module during audit season and the team is not yet aligned on the narrowest viable direction.
- **Why intake was used**: This is brownfield modernization work with a known lifecycle route but unresolved release-1 direction and scope boundaries.
- **Work type**: Migration
- **Entry phase**: 00-discovery
- **Recommended workflow**: brownfield
- **Scope assessment**: large
- **Urgency**: elevated but not an incident

## Required Artifact

- **Artifact name**: `intake-brief`
- **Status**: approved
- **Approver**: user

## Routing Decision

1. **Recommended first skill**: `problem-framing`
   - **Output**: `problem-frame`, `options-brief`, `design-direction`
   - **Why this is next**: The modernization route is clear, but the release-1 direction still needs trade-off framing before requirements or research can proceed cleanly.
2. **Second skill**: `requirements-engineering`
   - **Output**: `requirements-doc`
3. **Third skill**: `system-design`
   - **Output**: `architecture-doc`

## Question Budget

- **Questions asked**: 3
- **Did any answer change routing?** yes
- **If more than 3 questions were needed, why?**

## Alternatives Considered

- **Primary path chosen**: `problem-framing` -> `requirements-engineering` -> `system-design`
- **Alternative path considered**: go directly to `system-design`
- **Trade-off summary**: Jumping to architecture would move faster, but the team still lacks agreement on the release-1 boundary and coexistence direction.

## Key Risks

1. Architecture work could hard-code a migration or synchronization choice before the release-1 boundary is agreed.
2. Stakeholders may conflate modernization with full legacy replacement, causing hidden scope expansion.

## Fast-Track or Skipped Gates

- **Any shortcut taken?** no
- **If yes, why was it acceptable?**
- **What debt does this create?**

## Notes for Handoff

- Constraints: release 1 must coexist with the legacy module during audit season; tenant-specific rules are only partially inventoried.
- Open questions:
  - Should release 1 focus on campaign management and evidence packaging first, or include reassignment/correction flows immediately?
  - Can historical campaigns remain read-only in the legacy module for release 1?
  - What consistency level is actually required between legacy and new workflows during coexistence?
- Context that downstream skills must preserve: do not silently decide rewrite-vs-coexistence or real-time-vs-batch sync inside the framing step.
- Should `problem-framing` run next? yes
