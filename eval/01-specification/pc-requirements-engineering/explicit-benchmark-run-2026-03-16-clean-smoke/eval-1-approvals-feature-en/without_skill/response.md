# Approvals Workflow — First Release Requirements

**Product Area:** Purchase Request Approvals
**Release Scope:** v1.0
**Source:** 8 operations manager interviews
**Date:** 2026-03-16

---

## Assumptions

1. "Sent back" is treated as a distinct status meaning the approver returned the request to the submitter for revision (not the same as rejection).
2. Delegation is referenced only in the audit trail note; full delegation workflow is deferred to v2, but delegation events must be recorded if the capability ships.
3. "Near-instant" is interpreted as a P99 server-side action latency target (see NFR-1).
4. Thresholds are applied to the total request value in the company's base currency.

---

## Priority Tiers

| Tier | Meaning |
|------|---------|
| **P0** | Launch blocker — core value of the feature |
| **P1** | Strong should-have — ships with v1 unless de-scoped under time pressure |
| **P2** | Deferred to v2 |

---

## Functional Requirements

### FR-1 — Single-Stage Approval Threshold *(P0)*
Any purchase request with a total value ≥ $5,000 must be routed to the submitter's manager for approval before it can be fulfilled.
Requests below $5,000 are auto-approved.

**Trace:** "Managers need every purchase request above $5,000 to require manager approval."

---

### FR-2 — Optional Two-Stage Approval *(P1)*
For requests ≥ $20,000, a second-stage Finance approval step may be enabled per organization. When enabled, the request must pass manager approval first, then route to the Finance approver. When disabled, the standard single-stage flow applies regardless of amount.

**Trace:** "Finance wants optional second-stage approval above $20,000."

**Note:** "Optional" per organization means this is a tenant-level configuration toggle, not a per-request choice.

---

### FR-3 — Approvals Inbox *(P0)*
Approvers must have a dedicated in-product inbox listing all requests awaiting their action. The inbox must be reachable within two clicks from any page in the product. Email shall not be the primary or only notification surface.

**Trace:** "Current approvals are buried in email and get lost."

---

### FR-4 — Mobile-Responsive Approve / Reject Actions *(P0)*
The approve and reject actions must be fully operable on a mobile browser (viewport ≥ 375 px wide) without horizontal scrolling, pinching, or requiring a desktop view. This includes viewing request detail, selecting an action, and submitting a rejection comment.

**Trace:** "Managers need a mobile-friendly way to approve or reject quickly."

---

### FR-5 — Request Status Visibility *(P0)*
Every request must display one of four canonical statuses to the submitter and all approvers in the chain:

| Status | Meaning |
|--------|---------|
| `Pending` | Awaiting an approver action |
| `Approved` | All required stages passed |
| `Rejected` | Declined; no further routing |
| `Sent Back` | Returned to submitter for revision |

Status must update in the UI without a page refresh within 5 seconds of the approver's action (see NFR-1).

**Trace:** "Users need clear status visibility: pending, approved, rejected, sent back."

---

### FR-6 — Rejection Comments *(P0)*
When an approver selects Reject or Sent Back, they must provide a comment before the action can be submitted. The comment field must accept up to 1,000 characters. The comment is displayed to the submitter on the request detail page.

**Trace:** "Customers asked for comments on rejection so employees know what to fix."

---

### FR-7 — Searchable Audit Trail *(P0)*
Every approval event (approve, reject, sent back, and delegation if delegation ships) must be written to an immutable audit log capturing: actor identity, action type, timestamp, and request ID. The audit log must be searchable by request ID, actor name, date range, and action type. Results must be accessible to Finance administrators.

**Trace:** "Finance requires a searchable audit trail of who approved, rejected, or delegated a request."

---

### FR-8 — Department-Specific Approval Thresholds *(P2 — Deferred)*
Organizations may configure per-department approval thresholds that override the company-wide defaults. **Deferred to v2.** v1 ships with organization-wide thresholds only.

**Trace:** "Some companies want department-specific approval thresholds."

**Deferral rationale:** Requires a department configuration model that does not exist in the current data model. Building it correctly is a larger scoping effort; the company-wide threshold covers all interviewed customers for launch.

---

## Non-Functional Requirements

### NFR-1 — Action Latency *(P0)*
The server must process an approve, reject, or sent-back action and return a success response within **500 ms at P99** under normal load (defined as ≤ 500 concurrent approval actions). Status updates reflected in the submitter's UI must propagate within **5 seconds** of the approver's action.

**Trace:** "Approval actions should feel near-instant."

---

### NFR-2 — Audit Trail Retention *(P0)*
Audit log records must be retained for a minimum of **365 calendar days** from the date of the event. Records must not be deleted or altered by any user action during the retention period. After 365 days, records may be archived but must remain retrievable within 24 hours of a Finance administrator request.

**Trace:** "The audit trail must be retained for at least 1 year."

---

### NFR-3 — Authorization Enforcement *(P0)*
Only the designated approver(s) for a request (as determined by the routing rules in FR-1 and FR-2) may take an approval action on that request. Attempts by any other authenticated user to approve, reject, or send back a request must return an authorization error and must be logged. There must be no path — including direct API calls — that bypasses this check.

**Trace:** "Only authorized approvers should act on a request."

---

## Non-Goals for v1

| Non-Goal | Rationale |
|----------|-----------|
| Department-level thresholds | Deferred (FR-8); data model work required |
| Delegation workflow (full) | Mentioned only in audit trail context; full delegation UX is v2 |
| Native mobile app | Mobile-responsive web covers the interview need |
| Bulk approval actions | Not raised in interviews; can be added based on adoption data |
| ERP / procurement system integration | Out of scope; finance workflow is internal-only in v1 |
| Custom approval chain builder | Two-stage covers all interviewed cases; freeform chains are v2 |
| Automated escalation on inactivity | Not raised; add once usage patterns are known |

---

## Traceability Matrix

| Discovery Note | Requirement(s) |
|----------------|---------------|
| Purchase requests >$5K need manager approval | FR-1 |
| Optional second-stage approval >$20K | FR-2 |
| Approvals buried in email, get lost | FR-3 |
| Mobile-friendly approve/reject | FR-4 |
| Clear status visibility | FR-5 |
| Comments on rejection | FR-6 |
| Searchable audit trail | FR-7 |
| Department-specific thresholds | FR-8 (P2, deferred) |
| Approval actions feel near-instant | NFR-1 |
| Audit trail retained ≥ 1 year | NFR-2 |
| Only authorized approvers can act | NFR-3 |

---

## Open Questions Before Development Starts

1. **Approver assignment:** How is the "manager" relationship defined in the current user model — org chart, a direct manager field, or a manual mapping? This determines the routing implementation for FR-1.
2. **Finance approver identity:** Is the second-stage Finance approver a role, a named user, or a group? FR-2 routing depends on this.
3. **"Sent Back" re-routing:** After a submitter revises a sent-back request, does it restart the full approval chain or resume at the stage that sent it back?
4. **Threshold currency handling:** Are all requests already normalized to a single base currency, or does FR-1/FR-2 need to handle multi-currency conversion?

---

`★ Insight ─────────────────────────────────────`

**Why "optional" in FR-2 matters architecturally:** Modeling the two-stage flow as a tenant-level toggle (on/off) keeps the routing engine simple for v1. If you instead model it as "always two stages but Finance approval is waived below $20K," you get equivalent behavior but it becomes much harder to turn off cleanly later and complicates the audit trail.

**Immutability in NFR-2 is a systems contract, not just a policy:** Stating that records "must not be deleted or altered by any user action" forces the engineering team to choose an append-only storage strategy at design time — not retrofit it after a compliance request.

**The four status values in FR-5 are a bounded vocabulary:** Keeping statuses as an enum rather than free text ensures the audit trail, inbox filtering, and status visibility all share a single source of truth. Every additional status added later is a schema migration and a UI change — so the list should be minimal and deliberate.

`─────────────────────────────────────────────────`
