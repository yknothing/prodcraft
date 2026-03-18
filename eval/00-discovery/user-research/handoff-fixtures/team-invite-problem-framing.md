# Problem Frame: Team Invite Product Direction

## Source Context

- **Input artifact**: `intake-brief`
- **Why problem-framing was invoked**: intake already routed the work to discovery, but the release-1 direction is still fuzzy
- **Approved route from intake**: `problem-framing` -> `user-research` -> `requirements-engineering`

## Question Budget

- **Additional questions asked in this run**: 0
- **Reason**: the intake brief already contains enough information to compare the first viable directions

## Problem Frame

- **Problem statement**: Workspace owners need a low-friction way to bring coworkers into a shared product space without forcing the first release to absorb enterprise identity and bulk-admin scope too early.
- **Target user or operator**: Workspace owners and early team administrators in small-to-mid-size collaborative product teams.
- **Constraints**:
  - release 1 should unlock shared collaboration quickly
  - avoid silently expanding into enterprise identity administration
  - keep room for later enterprise-oriented invite paths
- **Non-goals**:
  - full enterprise identity onboarding in release 1
  - organization-wide bulk provisioning as the default first path
- **Assumptions**:
  - many early customers invite a small set of coworkers before they need centralized provisioning
  - different customer segments may value different onboarding paths
- **Open questions**:
  - how common is domain claim or SSO-first onboarding among the first target segment?
  - is admin bulk provisioning a must-have for release 1 or a second-stage capability?
  - should role assignment happen during invite or after acceptance?

## Options Brief

### Option 1: Email-invite-first

- **Summary**: Optimize release 1 around owner-sent email invites with basic acceptance and membership flows.
- **What it optimizes for**: speed to value, broad accessibility, low release-1 scope
- **Main risks**: may feel underpowered for larger or enterprise-leaning customers

### Option 2: Domain-claim / identity-first

- **Summary**: Optimize release 1 around company-domain capture or SSO-oriented team onboarding.
- **What it optimizes for**: stronger enterprise posture and cleaner org-level onboarding
- **Main risks**: identity/admin scope may dominate release 1 before core collaboration value is proven

### Option 3: Admin-assisted bulk provisioning

- **Summary**: Optimize release 1 around CSV or admin-managed bulk onboarding.
- **What it optimizes for**: operational efficiency for larger customer groups
- **Main risks**: introduces admin complexity before day-to-day owner invite workflows are validated

## Recommended Design Direction

- **Recommended option**: Option 1, email-invite-first
- **Why it wins**: It delivers the core collaboration outcome with the smallest release-1 scope while keeping the door open for domain and bulk-admin extensions once customer evidence is clearer.
- **What remains open for downstream skills**:
  - exact role-selection behavior at invite time
  - criteria for when domain or bulk provisioning becomes release-1 critical
  - the minimum user research needed to validate early-segment onboarding behavior
- **Next skill to invoke**: `user-research`

## Direction Handoff Note

`requirements-engineering` should not start until user research confirms whether the first segment is primarily lightweight team invites or enterprise-style onboarding. Downstream skills should preserve the non-goal of forcing enterprise identity scope into release 1 by default.
