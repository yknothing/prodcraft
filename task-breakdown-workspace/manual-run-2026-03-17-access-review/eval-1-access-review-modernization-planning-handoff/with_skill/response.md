# Release 1 Task Breakdown: Access Review Modernization

## Sequencing Principles

- Preserve coexistence with the legacy module throughout release 1.
- Sequence work around reversible seams and contract-tested slices.
- Make unresolved sync and compatibility questions visible instead of hiding them inside implementation tasks.

## Work Packages and Tasks

### Slice A: Safety Net and Compatibility Foundations

1. **Add characterization and contract tests for existing legacy access-review flows**
   - Done when critical coexistence behaviors and evidence-package expectations are captured in automated tests.
2. **Implement Legacy Coexistence Adapter skeleton**
   - Done when the adapter exposes a reversible seam for state exchange and legacy-read checks without assuming cutover semantics.
3. **Define unsupported-flow responses for non-release-1 reassignment variants**
   - Done when contract tests cover structured unsupported responses.

### Slice B: Core Release-1 Campaign Flow

4. **Implement Review Coordination Service campaign lifecycle slice**
   - Depends on tasks 1-2
   - Done when campaign creation/status flow exists for release-1 templates.
5. **Implement Campaigns API and Review Actions API**
   - Depends on task 4
   - Done when release-1 campaign and review-action endpoints satisfy contract tests.
6. **Implement Modern Access Review Experience for campaign and review-task flow**
   - Depends on task 5
   - Done when authorized admins/reviewers can create campaigns and perform review actions through the release-1 UI.

### Slice C: Evidence and Audit Integrity

7. **Implement Audit Integrity Store and audit-event write path**
   - Depends on task 4
   - Done when review actions produce tamper-evident audit records.
8. **Implement Evidence Package Service and evidence retrieval API**
   - Depends on tasks 5 and 7
   - Done when authorized users can retrieve release-1 evidence packages and audit-event history.

### Slice D: Reminder and Supported Reassignment Flow

9. **Implement reminder scheduling and reminder API behavior**
   - Depends on tasks 4 and 5
   - Done when release-1 reminders work for supported campaign states.
10. **Implement supported reassignment flow subset**
    - Depends on tasks 3, 4, and 5
    - Done when confirmed release-1 reassignment variants work and unsupported variants fail explicitly.

### Slice E: Brownfield Coexistence Readiness

11. **Implement legacy-read boundary for historical campaigns older than two years**
    - Depends on task 2
    - Done when release-1 users are routed to supported evidence/search behavior without forcing migration of old history.
12. **Implement coexistence state-visibility path between new flow and legacy module**
    - Depends on tasks 2, 4, and 5
    - Done when release-1 status visibility works within the currently approved coexistence semantics.
    - Blocked by: final decision on near-real-time vs deferred-sync semantics if that changes user-visible contract behavior.

### Slice F: Release Readiness

13. **Run end-to-end coexistence regression suite**
    - Depends on tasks 6, 8, 9, 10, 11, and 12
    - Done when release-1 flows pass regression, contract, and coexistence checks.
14. **Prepare rollback and release checklist for release-1 coexistence deployment**
    - Depends on task 13
    - Done when rollback/fallback actions are explicit and reviewed before implementation handoff completes.

## Dependency Outline

- Critical path: 1 -> 2 -> 4 -> 5 -> 6/8/9/10/12 -> 13 -> 14
- Parallelizable paths:
  - 7 can proceed after 4 while UI work proceeds after 5
  - 11 can proceed after 2 without waiting for all release-1 UI work

## Explicit Blockers / Open Questions

- Sync semantics remain an architectural blocker for any task that would expose freshness guarantees to users.
- Final release-1 tenant compatibility set remains a blocker for some policy-handling implementation details.
- Some reassignment and data-correction flows remain intentionally deferred until scope is confirmed.

## Downstream Handoff

- `tdd` should take tasks 1, 5, 8, 10, and 13 first because they anchor contract and coexistence safety.
- `feature-development` should implement vertical slices in the sequence above, not backend-only or frontend-only horizontal layers.
- `testing-strategy` should derive release-1 regression, contract, and coexistence suites from tasks 1, 3, 8, 10, 12, and 13.
