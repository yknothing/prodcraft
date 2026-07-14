# Requirements Draft: Guest-First Coexistence Release 1

## Scope Statement

Release 1 must solve bounded external collaboration inside the existing paid-seat model. It must not become a pricing redesign, org-wide policy engine, or forced migration of every account to a new seat structure.

## P0 Functional Requirements

1. **Guest Invite Path**
   - The system shall allow a workspace admin to invite an external collaborator as a guest without consuming a standard full-member seat by default.
   - **Primary source**: Operations Admin Olivia, Team Lead Theo, primary journey stages 1-4.

2. **Guest Identity and Visibility**
   - The system shall display whether a collaborator is a guest or a full member anywhere an admin reviews current access.
   - **Primary source**: Operations Admin Olivia, journey stages 2-5.

3. **Bounded Access Controls**
   - The system shall let admins assign guest access within explicit release-1 boundaries for workspace or project participation.
   - **Primary source**: Olivia pain points, journey stages 3-5.
   - **Open question carried forward**: the minimum mandatory guest restrictions still needs confirmation from research evidence.

4. **Revocation and Lifecycle Control**
   - The system shall let admins revoke guest access cleanly when the collaboration ends.
   - **Primary source**: Olivia pain points, journey stage 6.

5. **Audit Visibility**
   - The system shall record guest invite, acceptance, and revocation events in a way admins can review later.
   - **Primary source**: Fiona pain points, journey stages 3-6.

## P1 Functional Requirements

1. **Escalation Trigger Visibility**
   - The system should make it visible when guest usage patterns begin to look like persistent seat expansion so admins know when stronger governance may be needed.
   - **Primary source**: Fiona quote and cross-persona synthesis.

2. **Configurable Approval Trigger**
   - The system should support a configurable approval check for accounts where finance or procurement pressure is a known blocker.
   - **Primary source**: Fiona persona, journey stage 3.
   - **Open question carried forward**: whether approval should be mandatory by default or only for larger account tiers.

## Non-Goals

- redesign pricing or packaging in release 1
- build an org-wide policy engine in release 1
- migrate every existing account off the current seat model

## Open Questions

- Which guest restrictions are mandatory on day one versus safe to defer?
- At what usage or account threshold must finance approval become part of the default flow?
- Should governance-heavy enterprise accounts remain a later segment rather than the primary design center for release 1?

## Downstream Handoff Note

`system-design` should now work within the guest-first coexistence boundary. `acceptance-criteria` should derive tests from the P0/P1 requirements above without expanding release 1 into pricing or policy redesign.
