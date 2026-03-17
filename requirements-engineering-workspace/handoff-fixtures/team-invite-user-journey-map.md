# User Journey Map: Email-Invite-First Team Onboarding

> QA fixture for downstream skill evaluation. This is a synthetic journey artifact used to test how well downstream specification preserves user-research evidence.

## Primary Persona

- **Persona**: Workspace Owner Wendy
- **Scenario**: invite a few coworkers into a shared workspace quickly so team collaboration can begin the same day

## Journey Stages

### 1. Collaboration Need Appears

- **Trigger**: owner wants to bring teammates into an existing workspace
- **Current pain**: current onboarding steps are unclear and sometimes role setup is delayed
- **Opportunity**: keep the first release centered on a simple, fast invite path

### 2. Invite Prepared

- **Owner expectation**: enter teammate email, choose a basic role, and send the invite quickly
- **Current pain**: role expectations and invitation state are not explicit enough
- **Opportunity**: make invite status and role intent visible during setup

### 3. Invite Sent and Accepted

- **Desired outcome**: teammate enters the workspace with minimal friction
- **Current pain**: if the flow feels too enterprise-heavy, owners look for workarounds
- **Opportunity**: keep acceptance lightweight while preserving the later option for stronger identity paths

### 4. First Collaboration

- **Owner expectation**: teammate can start contributing immediately within the intended role
- **Current pain**: role mismatches or unclear state cause friction after acceptance
- **Opportunity**: make first-session permissions and role visibility obvious

### 5. Growth Trigger

- **Expected branch A**: invite-first flow continues to work for small-team growth
- **Expected branch B**: team size or security posture makes domain claim / SSO a later priority
- **Opportunity**: keep the release-1 flow open to later expansion without making that expansion the first-release center

## Journey-Level Signals for Requirements

- release 1 should optimize for fast invite and clear role onboarding
- domain claim, SSO, and admin bulk provisioning are later triggers, not default release-1 scope
- role clarity matters enough to influence release-1 behavior even in a lightweight invite flow
