# Problem Frame: Seat and Guest Management Modernization

## Source Context

- **Input artifact**: `intake-brief`
- **Why problem-framing was invoked**: intake routed the work to discovery, but the first release direction for collaborator access is still ambiguous
- **Approved route from intake**: `problem-framing` -> `user-research` -> `requirements-engineering`

## Question Budget

- **Additional questions asked in this run**: 0
- **Reason**: the intake brief already captured the legacy seat model, the modernization goal, and the main release-1 trade-off

## Problem Frame

- **Problem statement**: Product admins in an existing B2B SaaS need a cleaner way to let external collaborators participate without forcing every user into a paid full-member seat or turning release 1 into a full billing and policy redesign.
- **Target user or operator**: workspace admins, operations owners, and team leads in mid-market B2B SaaS accounts that already manage paid member seats today.
- **Constraints**:
  - an existing paid full-member seat model already exists in production
  - release 1 should coexist with the current seat model rather than replace it
  - finance and procurement concerns exist, but should not automatically dominate the first slice
- **Non-goals**:
  - full pricing and packaging redesign in release 1
  - a complete org-wide policy engine for every collaborator type
  - migrating every existing account to a new seat model in the first release
- **Assumptions**:
  - many customers mainly need occasional external collaboration rather than a full seat-governance overhaul
  - some larger accounts may still care more about seat governance and procurement visibility than guest collaboration
- **Open questions**:
  - how often do target admins truly need external guest access versus tighter control of internal paid seats?
  - what restrictions matter most for guest users: visibility, actions, billing, or approval workflow?
  - when do procurement or finance stakeholders become release-1 blockers rather than later-stage stakeholders?

## Options Brief

### Option 1: Guest-first coexistence

- **Summary**: Add a limited guest collaborator path that coexists with the current paid-seat model.
- **What it optimizes for**: faster external collaboration learning with lower release-1 disruption
- **Main risks**: may under-serve customers whose real pain is seat governance rather than guest access

### Option 2: Seat-governance-first

- **Summary**: Focus release 1 on better seat visibility, controls, and role boundaries for existing paid members.
- **What it optimizes for**: admin control and internal cost governance
- **Main risks**: external collaboration pain may remain unsolved

### Option 3: Procurement-and-policy-first

- **Summary**: Build stronger finance/procurement approval and policy controls before opening up guest access.
- **What it optimizes for**: enterprise control posture
- **Main risks**: release 1 becomes a broad admin-program redesign instead of solving the immediate collaborator problem

## Recommended Design Direction

- **Recommended option**: Option 1, guest-first coexistence
- **Why it wins**: It tests the external-collaboration problem directly while keeping the existing seat model intact and leaving broader governance or procurement redesign for later evidence-backed work.
- **What remains open for downstream skills**:
  - which admin segment most urgently needs guest access versus seat-governance controls
  - what guest restrictions are mandatory for early adopters
  - whether procurement or finance must shape release 1 or can remain a later expansion
- **Next skill to invoke**: `user-research`

## Direction Handoff Note

`requirements-engineering` should not begin until user research confirms whether admins primarily need guest-first collaboration or whether seat-governance / procurement pressures are actually the dominant first-release problem. Downstream skills should preserve the non-goal of turning release 1 into a broad pricing or policy rewrite by default.
