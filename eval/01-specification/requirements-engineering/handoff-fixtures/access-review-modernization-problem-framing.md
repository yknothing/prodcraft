# Problem Frame: Access Review Modernization Direction

## Source Context

- **Input artifact**: `intake-brief`
- **Why problem-framing was invoked**: intake already selected a brownfield modernization route, but the narrowest release-1 direction is still unresolved
- **Approved route from intake**: `problem-framing` -> `requirements-engineering` -> `system-design`

## Question Budget

- **Additional questions asked in this run**: 0
- **Reason**: the intake brief contains enough boundary information to compare release-1 directions without reopening triage

## Problem Frame

- **Problem statement**: The team must define a release-1 modernization direction for quarterly access reviews that delivers visible improvement while preserving brownfield coexistence with the legacy module during audit season.
- **Target user or operator**: Compliance admins, auditors, and support teams managing quarterly access-review campaigns in the current SaaS product.
- **Constraints**:
  - release 1 must coexist with the legacy module during audit season
  - tenant-specific rules are only partially inventoried
  - release 1 should not silently collapse into a full migration or replacement program
- **Non-goals**:
  - full legacy replacement in release 1
  - irreversible cutover or migration sequencing decisions inside the framing step
  - pretending synchronization semantics are already settled
- **Assumptions**:
  - campaign creation, reminders, delegated approvals, and evidence packaging represent the clearest release-1 value
  - some historical and exception-heavy paths may need to remain partly legacy-backed in release 1
- **Open questions**:
  - which tenant-specific rules are contractually mandatory in release 1?
  - can historical campaigns remain read-only in the legacy module for the first release?
  - does required consistency mean near-real-time or end-of-day synchronization?
  - which reassignment and correction flows are mandatory for release 1?

## Options Brief

### Option 1: Campaign-and-evidence-first coexistence

- **Summary**: Release 1 centers on campaign management, delegated approvals, reminders, and evidence export while explicitly preserving coexistence with the legacy module.
- **What it optimizes for**: visible user value, lower release-1 scope, compatibility with audit-season constraints
- **Main risks**: some stakeholders may see it as insufficient parity if reassignment and exception-heavy flows remain partly legacy-backed

### Option 2: Near-parity modernization

- **Summary**: Release 1 attempts to include correction, reassignment, and more tenant-specific exception handling alongside the main campaign workflow.
- **What it optimizes for**: broader operational completeness and fewer near-term follow-up releases
- **Main risks**: scope expansion, hidden contractual complexity, and pressure to make architecture and migration decisions too early

### Option 3: Sync-and-transition-first

- **Summary**: Release 1 prioritizes stronger legacy/new consistency and transition behavior before narrowing the functional release slice.
- **What it optimizes for**: future cutover confidence and operational predictability
- **Main risks**: turns the framing step into migration design too early and delays delivery of the main workflow improvements

## Recommended Design Direction

- **Recommended option**: Option 1, campaign-and-evidence-first coexistence
- **Why it wins**: It best respects the release-1 coexistence boundary while delivering clear value and avoiding premature migration or parity commitments.
- **What remains open for downstream skills**:
  - exact tenant-specific compatibility obligations
  - whether historical campaigns can remain read-only in the legacy module
  - the required consistency level between legacy and modernized flows
  - the minimum reassignment/correction scope for release 1
- **Next skill to invoke**: `requirements-engineering`

## Direction Handoff Note

Downstream requirements work should preserve brownfield coexistence and open questions rather than converting them into architecture decisions. `system-design` should only begin after the release-1 boundary is expressed as reviewed requirements.
