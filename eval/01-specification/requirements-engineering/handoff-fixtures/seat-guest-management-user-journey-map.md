# User Journey Map: Guest-First Coexistence

> QA fixture for downstream skill evaluation. This is a synthetic journey artifact used to test how well downstream specification preserves user-research evidence.

## Primary Persona

- **Persona**: Operations Admin Olivia
- **Scenario**: invite a short-term external collaborator without converting the person into a full paid member seat

## Journey Stages

### 1. Need Identified

- **Trigger**: project team needs an agency partner, contractor, or auditor in the workspace within one business day
- **Current pain**: admin must choose between an overpowered full seat or a support workaround
- **Opportunity**: provide a clearly bounded guest path

### 2. Access Request Created

- **Admin intent**: invite the external collaborator with explicit limits
- **Current pain**: no obvious distinction between temporary collaborator and standard member
- **Opportunity**: make guest status visible before the invite is sent

### 3. Guardrails Checked

- **Admin expectation**: confirm what the guest can see, do, and how long the access should last
- **Current pain**: policy and billing implications are ambiguous
- **Opportunity**: expose simple release-1 guardrails and clearly defer larger governance cases

### 4. Invite Accepted

- **Desired outcome**: collaborator can enter the intended workspace or project context quickly
- **Current pain**: acceptance path can inherit full-member assumptions
- **Opportunity**: keep invite acceptance lightweight while preserving guest identity

### 5. Collaboration Active

- **Admin expectation**: the collaborator can contribute within bounded permissions
- **Current pain**: visibility into guest activity and lifecycle is weak
- **Opportunity**: show guest status, scope, and revocation path clearly

### 6. Offboarding or Escalation

- **Expected branch A**: guest access is revoked cleanly when the work ends
- **Expected branch B**: if the collaborator becomes persistent, the team intentionally upgrades or reroutes the account to stronger governance
- **Current pain**: current workaround hides when that threshold is crossed
- **Opportunity**: keep the threshold visible as a release-1 decision trigger

## Journey-Level Signals for Requirements

- release 1 must optimize for fast bounded collaboration, not general seat-model redesign
- guest identity, visibility, and revocation are core to trust
- approval and finance pressure are important, but should enter release 1 only where evidence shows they are blockers
