No template file exists, so I'll produce the document directly following the skill's structure. Here's the requirements document:

---

# Approvals Workflow — Requirements Document (V1 / First Release)

## Intake Summary

**Work type**: New Feature (approvals workflow for existing SaaS product)
**Entry phase**: 01-specification
**Source material**: 8 operations manager interviews
**Methodology**: Agile (SaaS product, iterative delivery)

---

## Discovery Note Index

| ID | Discovery Note |
|----|----------------|
| DN-1 | Managers need every purchase request above $5,000 to require manager approval |
| DN-2 | Finance wants optional second-stage approval above $20,000 |
| DN-3 | Employees complain that current approvals are buried in email and get lost |
| DN-4 | Managers need a mobile-friendly way to approve or reject quickly |
| DN-5 | Finance requires a searchable audit trail of who approved, rejected, or delegated |
| DN-6 | Some companies want department-specific approval thresholds |
| DN-7 | Users need clear status visibility: pending, approved, rejected, sent back |
| DN-8 | Customers asked for comments on rejection so employees know what to fix |
| DN-9 | Non-functional: near-instant actions, 1-year audit retention, authorized approvers only |

---

## Functional Requirements

### P0 — Must Have (product is unusable without these)

| ID | Requirement | Source | Acceptance Criteria |
|----|-------------|--------|---------------------|
| FR-01 | The system shall route any purchase request exceeding $5,000 to the requester's direct manager for approval before the request can proceed. | DN-1 | A $5,001 request creates a pending approval task assigned to the requester's manager; a $4,999 request does not. |
| FR-02 | The system shall allow an approver to approve or reject a purchase request from the approval dashboard. | DN-1, DN-4 | An approver can select approve or reject; the request status updates immediately and the requester is notified. |
| FR-03 | The system shall display request status (pending, approved, rejected, sent back) to the requester and approver at all times. | DN-7 | Status is visible on the request detail page and in any list view; status updates within 5 seconds of an action. |
| FR-04 | The system shall provide an in-app approval dashboard listing all requests pending the current user's action. | DN-3 | Approvers see a filterable list of their pending requests without relying on email. |
| FR-05 | The system shall record an immutable audit entry for every approval, rejection, and delegation action, including actor, timestamp, and action taken. | DN-5 | Audit entries cannot be edited or deleted; each entry contains who, what, and when. |
| FR-06 | The system shall provide a searchable audit trail, filterable by requester, approver, date range, status, and amount. | DN-5 | Finance can search by any combination of these fields and receive results within 2 seconds. |
| FR-07 | The system shall enforce that only users designated as approvers for a given request can take approval actions on it. | DN-9 | A non-approver attempting to approve/reject receives an authorization error; the action is blocked and logged. |

### P1 — Should Have (important, workarounds exist)

| ID | Requirement | Source | Acceptance Criteria |
|----|-------------|--------|---------------------|
| FR-08 | The system shall support an optional second-stage approval for purchase requests exceeding $20,000, configurable by a finance administrator. | DN-2 | When enabled, a $20,001 request requires a second approver after the first approval; when disabled, single approval suffices. |
| FR-09 | The approval dashboard shall be responsive and usable on mobile devices (viewport ≥ 320px). | DN-4 | Approvers can review, approve, and reject requests from a mobile browser without horizontal scrolling or broken layouts. |
| FR-10 | The system shall require a comment when rejecting a request, visible to the requester. | DN-8 | Rejection without a comment is blocked; the requester sees the comment on the request detail page. |
| FR-11 | The system shall send in-app notifications to approvers when a new request requires their action and to requesters when their request status changes. | DN-3 | Notifications appear within 30 seconds of the triggering event; users can view notification history. |

### P2 — Could Have (include if time permits)

| ID | Requirement | Source | Acceptance Criteria |
|----|-------------|--------|---------------------|
| FR-12 | The system shall allow an approver to delegate a request to another authorized approver, with the delegation recorded in the audit trail. | DN-5 | Delegation transfers the approval task; the audit trail shows the original and delegated approver. |
| FR-13 | The system shall support a "send back" action that returns a request to the requester for revision, with an approver comment. | DN-7, DN-8 | Status changes to "sent back"; the requester can edit and resubmit; the full revision history is preserved. |

---

## Non-Goals (P3 — explicitly out of scope for V1)

| ID | Exclusion | Source | Rationale |
|----|-----------|--------|-----------|
| NG-01 | Department-specific approval thresholds | DN-6 | Requires multi-tenant configuration framework; plan for V2 after validating the core workflow. |
| NG-02 | Email-based approval actions (approve/reject via email reply) | DN-3 | V1 moves approvals *out of* email; email actions add complexity and security risk. |
| NG-03 | Automated approval rules (auto-approve below thresholds, time-based escalation) | — | No discovery signal; avoid scope creep. |
| NG-04 | Integration with external procurement or ERP systems | — | No discovery signal; evaluate post-launch. |

---

## Non-Functional Requirements

| ID | Category | Requirement | Source | Measurement |
|----|----------|-------------|--------|-------------|
| NFR-01 | Performance | Approval and rejection actions shall complete (server response) in < 500ms at p95 under normal load. | DN-9 ("near-instant") | Measured via server-side p95 latency on the approve/reject API endpoint under load test (100 concurrent users). |
| NFR-02 | Performance | The approval dashboard shall render initial content in < 1.5 seconds on a 4G mobile connection. | DN-4, DN-9 | Lighthouse performance audit on a throttled 4G profile; Time to Interactive < 1.5s. |
| NFR-03 | Data Retention | Audit trail records shall be retained for a minimum of 1 year from creation. | DN-9 | Records created 366 days ago are still queryable; no automated purge runs before the retention window. |
| NFR-04 | Security | Only users with an active approver role for the specific request shall be able to execute approval actions. | DN-9 | Penetration test: attempt approval with a valid session but no approver role → 403 Forbidden. |
| NFR-05 | Security | All approval actions shall be transmitted over TLS 1.2+, and audit records shall be stored with integrity protection (append-only or tamper-evident). | DN-5, DN-9 | Security review confirms TLS enforcement and append-only storage; no audit record can be modified after creation. |
| NFR-06 | Availability | The approvals service shall maintain 99.5% uptime measured monthly. | — (SaaS baseline) | Monthly uptime calculation excludes planned maintenance windows announced 48 hours in advance. |

---

## Traceability Matrix

| Discovery Note | Requirements Traced |
|----------------|---------------------|
| DN-1 | FR-01, FR-02 |
| DN-2 | FR-08 |
| DN-3 | FR-04, FR-11, NG-02 |
| DN-4 | FR-02, FR-09, NFR-02 |
| DN-5 | FR-05, FR-06, FR-12, NFR-05 |
| DN-6 | NG-01 |
| DN-7 | FR-03, FR-13 |
| DN-8 | FR-10, FR-13 |
| DN-9 | FR-07, NFR-01, NFR-02, NFR-03, NFR-04, NFR-05 |

**Coverage check**: All 9 discovery notes trace to at least one requirement or explicit non-goal. No orphan requirements exist (every FR/NFR traces to at least one DN).

---

## Assumptions

1. **Org hierarchy exists**: The SaaS product already has a user-manager relationship model that can be queried to determine the correct approver for a given requester.
2. **Single global threshold for V1**: The $5,000 and $20,000 thresholds are system-wide settings, not per-customer or per-department (department-specific thresholds are deferred to V2 per NG-01).
3. **Browser-based mobile**: "Mobile-friendly" means responsive web, not a native mobile app. Native push notifications are out of scope for V1.

---

## Quality Gate Checklist

- [x] All P0/P1 requirements documented with measurable acceptance criteria
- [x] Non-functional requirements quantified (latency in ms, retention in days, uptime as percentage)
- [x] No unresolved contradictions between requirements
- [x] Requirements traceable to discovery notes (traceability matrix complete)
- [ ] Stakeholders have reviewed and signed off *(pending — this document is ready for review)*

---

`★ Insight ─────────────────────────────────────`
**Priority decisions worth noting**: DN-6 (department-specific thresholds) was the hardest call. It came from interviews but requires a multi-tenant configuration layer that would double V1 scope. Deferring it to a non-goal with an explicit rationale preserves the stakeholder's voice while protecting the release timeline.

**NFR quantification**: The interviews said "near-instant" — I translated that to < 500ms p95 server-side. This is a judgment call. If your ops managers are comparing against consumer apps (where "instant" means < 100ms perceived), you may want to tighten this. The measurement method (p95 under load) makes it testable rather than aspirational.
`─────────────────────────────────────────────────`

This document is ready for stakeholder review. The next step in the Prodcraft lifecycle would be **spec-writing** — turning these requirements into a detailed technical specification — but that should wait until stakeholders sign off on the priorities and non-goals above.

One decision I'd surface for your review: **FR-10 (mandatory rejection comments)** is P1. Some teams find mandatory comments slow approvers down. If your ops managers feel strongly that speed trumps explanation, it could be made optional. That's a UX trade-off where your domain knowledge matters more than the interview notes alone.
