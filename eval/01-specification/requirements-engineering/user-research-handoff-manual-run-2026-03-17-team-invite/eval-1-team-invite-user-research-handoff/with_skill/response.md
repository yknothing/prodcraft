# Requirements Draft: Email-Invite-First Release 1

## Scope Statement

Release 1 must let workspace owners bring teammates into a shared workspace quickly through an email-invite path. It must not turn release 1 into enterprise identity onboarding, SSO-first setup, or admin bulk provisioning by default.

## P0 Functional Requirements

1. **Email Invite Initiation**
   - The system shall allow a workspace owner or authorized admin to invite a teammate by email into an existing workspace.
   - **Primary source**: Workspace Owner Wendy, journey stages 1-2.

2. **Invite Acceptance Flow**
   - The system shall provide a lightweight invite-acceptance flow that lets the invited teammate join the intended workspace without enterprise identity setup as a prerequisite.
   - **Primary source**: Wendy, journey stages 2-3.

3. **Role Clarity at Onboarding**
   - The system shall expose the teammate's intended role clearly during the invite and onboarding flow.
   - **Primary source**: Team Manager Maya, journey stages 2-4.
   - **Open question carried forward**: whether the role should be selected before acceptance or confirmed after acceptance still needs final owner confirmation.

4. **Invite Status Visibility**
   - The system shall let workspace owners or admins see whether an invite is pending, accepted, or expired.
   - **Primary source**: Wendy, journey stages 2-4.

## P1 Functional Requirements

1. **Later Identity Expansion Readiness**
   - The system should preserve a clean extension path for future domain-claim or SSO-based onboarding without making those flows the release-1 center.
   - **Primary source**: Growing Admin Ian, journey stage 5.

2. **Basic Re-invite / Expiry Handling**
   - The system should let owners handle expired or ignored invites without manual workaround.
   - **Primary source**: Wendy and Maya workflow friction.

## Non-Goals

- enterprise identity-first onboarding in release 1
- admin bulk provisioning as the default first path
- solving every later-stage org onboarding model in the first release

## Open Questions

- Should role selection happen during invite creation or after acceptance?
- At what team size or account posture does domain claim / SSO become a release-1 blocker instead of a later expansion?
- When does bulk provisioning become important enough to leave later scope?

## Downstream Handoff Note

`system-design` should work within the email-invite-first boundary. `acceptance-criteria` should derive tests from the P0/P1 requirements above without expanding release 1 into enterprise onboarding or bulk-admin scope.
