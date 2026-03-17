`★ Insight ─────────────────────────────────────`
Requirements engineering translates *needs* (what people said) into *obligations* (what the system shall do). The key discipline is resisting the temptation to carry design decisions into requirements — "mobile-friendly" is a need; "the system shall render the approval action in a single viewport-height screen on devices ≥320px wide" is a testable requirement. Traceability is the audit trail for your requirements: if you can't point a requirement back to a user need, it has no justification for existing.
`─────────────────────────────────────────────────`

---

# Approvals Workflow — First-Release Requirements

**Version:** 0.1-draft  
**Owner:** Product (single sign-off required per the Quality Gate)  
**Status:** Awaiting stakeholder review  
**Date:** 2026-03-16

---

## 1. Discovery Source Index

| ID | Raw finding |
|----|-------------|
| DN-01 | Every purchase request above $5,000 must require manager approval. |
| DN-02 | Finance wants an optional second-stage approval above $20,000. |
| DN-03 | Employees say approvals are buried in email and get lost. |
| DN-04 | Managers need a mobile-friendly way to approve or reject quickly. |
| DN-05 | Finance requires a searchable audit trail of who approved, rejected, or delegated. |
| DN-06 | Some companies want department-specific approval thresholds. |
| DN-07 | Users need clear status visibility: pending, approved, rejected, sent back. |
| DN-08 | Customers want rejection comments so employees know what to fix. |
| DN-09 | Approval actions should feel near-instant (interview NFR). |
| DN-10 | Audit trail must be retained for at least 1 year (interview NFR). |
| DN-11 | Only authorized approvers should be able to act on a request (interview NFR). |

---

## 2. Scope Statement

**In scope for release 1:** The approvals workflow covering single-stage and optional two-stage approval routing, an in-product notification and action surface, request status visibility, rejection comments, audit trail, and authorization enforcement.

**Non-goals (explicitly out of scope for release 1):**

| Non-goal | Rationale |
|----------|-----------|
| Department-specific approval thresholds (DN-06) | Reported by a subset of customers; adds significant routing complexity. Target release 2. |
| Native mobile application | Mobile-responsive web covers the stated need (DN-04) at lower cost. |
| Approval delegation workflows | Audit trail must record delegation (DN-05), but the mechanics of routing to a delegate are release 2. |
| ERP / accounting system integration | Not raised in interviews; out of budget for release 1. |
| AI-assisted approval recommendations | No evidence of demand; premature. |
| Email as the primary action surface | Email notifications may exist as a secondary signal, but approvals must be actioned inside the product (DN-03). |

---

## 3. Functional Requirements

Priority scale: **P0** = product unusable without it · **P1** = important, workaround exists · **P2** = nice-to-have if time permits.

---

### FR-01 — Single-stage approval gate  
**Priority:** P0  
**Source:** DN-01  
**Statement:** The system shall route a purchase request to the submitter's assigned manager for approval when the request amount exceeds $5,000, and shall block the request from proceeding to fulfillment until that approval is granted or the request is rejected.

---

### FR-02 — Optional two-stage approval gate  
**Priority:** P1  
**Source:** DN-02  
**Statement:** The system shall route a purchase request to a configured Finance approver for a second-stage review when the request amount exceeds $20,000, and shall do so only after the first-stage manager approval is granted. The second stage shall be configurable per tenant (enabled/disabled).

> **Conflict note:** DN-02 says "optional" — this is interpreted as optional at the *tenant configuration* level, not skippable per-request. If stakeholders intend per-request optionality, this requirement must be revised before sign-off.

---

### FR-03 — In-product approval action surface  
**Priority:** P0  
**Source:** DN-03  
**Statement:** The system shall present pending approval requests to approvers inside the product (dashboard or dedicated approvals queue) so that approvers can take action without leaving the application or relying on email.

---

### FR-04 — Mobile-responsive approval interface  
**Priority:** P1  
**Source:** DN-04  
**Statement:** The system shall render the approvals queue and the approve/reject action — including the request summary and any required comment field — in a fully functional layout on viewport widths of 375px and above, without requiring horizontal scrolling or modal dismissal to complete an action.

---

### FR-05 — Searchable audit trail  
**Priority:** P0  
**Source:** DN-05, DN-10, DN-11  
**Statement:** The system shall record an immutable audit event for every state transition of a purchase request (submitted, approved at stage 1, approved at stage 2, rejected, delegated, sent back), capturing: actor identity, actor role, timestamp, request ID, amount, and any comment. The audit log shall be searchable by request ID, actor, date range, and outcome.

---

### FR-06 — Request status visibility  
**Priority:** P0  
**Source:** DN-07  
**Statement:** The system shall expose the current status of a purchase request — one of `Pending`, `Approved`, `Rejected`, or `Sent Back` — to both the submitting employee and all approvers assigned to that request, updated in real time following any state transition.

---

### FR-07 — Rejection comments  
**Priority:** P1  
**Source:** DN-08  
**Statement:** The system shall require an approver to enter a free-text comment (minimum 10 characters) before submitting a rejection or send-back action, and shall display that comment to the submitting employee on the request detail view.

---

### FR-08 — Approver authorization enforcement  
**Priority:** P0  
**Source:** DN-11  
**Statement:** The system shall prevent any user who is not the designated approver for a given stage of a specific request from performing an approve, reject, or send-back action on that request, and shall return an authorization error if such an action is attempted via any interface or API endpoint.

---

## 4. Non-Functional Requirements

All NFRs are P0 unless noted.

| ID | Attribute | Requirement | Source | Measurement method |
|----|-----------|-------------|--------|--------------------|
| NFR-01 | Performance | The system shall complete an approve, reject, or send-back action — from user submission to confirmed state change — in < 500 ms at the 95th percentile under normal load (defined as up to 200 concurrent approvers). | DN-09 | Synthetic load test in staging; production p95 latency metric on the action endpoint. |
| NFR-02 | Durability | The system shall retain all audit trail records for a minimum of 365 calendar days from the date of the recorded event, with no data loss during that window. | DN-10 | Monthly backup verification; retention policy enforced at the storage layer. |
| NFR-03 | Security — authorization | The system shall enforce approver authorization checks server-side on every state-transition request; client-side gating alone is insufficient. Zero unauthorized transitions shall be permitted. | DN-11 | Penetration test: direct API calls bypassing the UI must return HTTP 403; automated auth test suite in CI. |
| NFR-04 | Security — audit immutability | Audit trail records shall be write-once; no application-layer path shall permit editing or deletion of an existing record. | DN-05, DN-10 | Schema-level constraints + code review gate; quarterly audit. |
| NFR-05 | Accessibility | The approval action surface shall meet WCAG 2.1 Level AA for keyboard navigation and screen reader compatibility. | DN-04 (mobile implies broad accessibility) | Automated axe-core scan + manual screen reader test on release candidate. |

---

## 5. Open Questions (must resolve before sign-off)

| # | Question | Blocking requirement | Owner |
|---|----------|----------------------|-------|
| OQ-01 | Is the two-stage Finance approval optional per-tenant or per-request? | FR-02 | Product + Finance stakeholder |
| OQ-02 | Who configures which manager is the approver for a given employee — HR system sync, manual admin, or self-service? | FR-01, FR-08 | Product + Engineering |
| OQ-03 | What is "normal load" for NFR-01? 200 concurrent approvers is an assumption. | NFR-01 | Product + Data |
| OQ-04 | Are email notifications (not actions) in scope as a secondary alert for pending approvals? | FR-03 | Product |
| OQ-05 | Is the 365-day retention a legal/compliance requirement or a product preference? If legal, it affects the deletion-proof storage choice. | NFR-02 | Legal + Engineering |

---

## 6. Quality Gate Checklist

- [ ] All P0/P1 requirements reviewed by at least one operations manager participant and one Finance stakeholder
- [ ] Open questions OQ-01 through OQ-05 resolved and requirements updated accordingly
- [ ] Non-functional requirements validated as achievable by tech lead
- [ ] No unresolved contradictions (see FR-02 conflict note)
- [ ] Acceptance criteria authored for each P0/P1 requirement (next step: run `acceptance-criteria` skill)
- [ ] Single requirements owner named and documented
