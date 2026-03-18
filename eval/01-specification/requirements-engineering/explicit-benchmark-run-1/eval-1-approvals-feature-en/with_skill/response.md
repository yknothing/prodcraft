`★ Insight ─────────────────────────────────────`
The skill prescribes a specific flow: functional requirements in "shall" format → quantified NFRs → MoSCoW prioritization → conflict resolution → traceability. The key discipline here is **traceability** — every requirement links back to a discovery note so stakeholders can ask "why is this here?" and get a concrete answer. I'll also explicitly call out **non-goals** (P3/Won't) since the discovery notes mention department-specific thresholds, which sounds like a V2 feature.
`─────────────────────────────────────────────────`

---

# Approvals Workflow — Requirements Document (R1)

**Product**: SaaS Approvals Workflow
**Release**: First Release (R1)
**Source**: 8 operations-manager interviews
**Date**: 2026-03-16
**Status**: Draft — pending stakeholder review

---

## Discovery Note Index

| ID | Source | Summary |
|----|--------|---------|
| DN-1 | Managers | Purchase requests > $5,000 require manager approval |
| DN-2 | Finance | Optional second-stage approval > $20,000 |
| DN-3 | Employees | Current approvals buried in email and lost |
| DN-4 | Managers | Mobile-friendly approve/reject |
| DN-5 | Finance | Searchable audit trail of actions |
| DN-6 | Some companies | Department-specific approval thresholds |
| DN-7 | Users | Clear status visibility (pending, approved, rejected, sent back) |
| DN-8 | Customers | Comments on rejection so employees know what to fix |
| DN-9 | Interviews (NFR) | Near-instant actions, 1-year retention, authorized approvers only |

---

## Functional Requirements

### Approval Routing

| ID | Requirement | Priority | Source | Acceptance Criteria |
|----|------------|----------|--------|-------------------|
| FR-01 | The system shall route any purchase request with an amount ≥ $5,000 to the requester's direct manager for approval, so that spending above the threshold is always authorized. | P0 (Must) | DN-1 | A request for $4,999 proceeds without approval. A request for $5,000 is routed to the requester's manager and blocks until acted on. |
| FR-02 | The system shall route any purchase request with an amount ≥ $20,000 to a second-stage finance approver after manager approval, so that high-value spending gets finance oversight. | P0 (Must) | DN-2 | A $25,000 request approved by a manager appears in the finance approver's queue. A $15,000 request approved by a manager does not. |
| FR-03 | The system shall allow an organization admin to enable or disable second-stage finance approval, so that companies can opt into the control. | P1 (Should) | DN-2 | When disabled, a $25,000 request approved by the manager proceeds directly to "Approved" status. |

### Approval Actions

| ID | Requirement | Priority | Source | Acceptance Criteria |
|----|------------|----------|--------|-------------------|
| FR-04 | The system shall allow an approver to approve, reject, or send back a request from a single action screen, so that decisions are fast and unambiguous. | P0 (Must) | DN-4, DN-7 | An approver can take any of the three actions from the request detail view without navigating to another page. |
| FR-05 | The system shall require a comment when an approver rejects or sends back a request, so that the requester knows what to fix. | P0 (Must) | DN-8 | Reject/send-back buttons are disabled until a comment of ≥ 1 character is entered. The comment is visible to the requester. |
| FR-06 | The system shall allow an approver to delegate a request to another authorized approver, so that approvals are not blocked by absence. | P1 (Should) | DN-3 | Delegated request appears in the delegate's queue and the audit trail records who delegated and to whom. |

### Status & Notifications

| ID | Requirement | Priority | Source | Acceptance Criteria |
|----|------------|----------|--------|-------------------|
| FR-07 | The system shall display the current status of each request as one of: Draft, Pending Approval, Approved, Rejected, or Sent Back, so that all parties know the state at a glance. | P0 (Must) | DN-7 | Status label is visible on the request list view and detail view. Status transitions match the defined state machine (see below). |
| FR-08 | The system shall send an in-app notification to the approver when a request enters their queue, so that approvals are not lost. | P0 (Must) | DN-3 | Within 60 seconds of routing, the approver sees an unread notification. |
| FR-09 | The system shall send an in-app notification to the requester when their request is approved, rejected, or sent back, so that employees are not left waiting. | P0 (Must) | DN-3, DN-7 | Notification appears within 60 seconds of the action. |

### Audit Trail

| ID | Requirement | Priority | Source | Acceptance Criteria |
|----|------------|----------|--------|-------------------|
| FR-10 | The system shall record an immutable audit event for every approval, rejection, delegation, and send-back action, including actor, timestamp, action, and any comment. | P0 (Must) | DN-5, DN-9 | Each action generates an audit row. Rows cannot be edited or deleted through any user-facing interface. |
| FR-11 | The system shall provide a searchable audit trail view filterable by requester, approver, date range, action type, and request amount. | P0 (Must) | DN-5 | A finance user can filter audit events by approver name and date range, and results return within acceptance criteria for NFR-01. |

### Mobile Experience

| ID | Requirement | Priority | Source | Acceptance Criteria |
|----|------------|----------|--------|-------------------|
| FR-12 | The system shall provide a responsive approval interface usable on viewports ≥ 320px wide, so that managers can act from their phone. | P0 (Must) | DN-4 | On a 375px-wide viewport, the approve/reject/send-back actions and comment field are fully visible and tappable without horizontal scrolling. |

---

## Non-Functional Requirements

| ID | Attribute | Requirement | Source | Acceptance Criteria |
|----|-----------|------------|--------|-------------------|
| NFR-01 | **Performance** | Approval actions (approve, reject, send back, delegate) shall complete and return confirmation in < 500ms at p95 under normal load. | DN-9 | Load test: 95th percentile response time for approval POST endpoint ≤ 500ms with 200 concurrent users. |
| NFR-02 | **Performance** | Audit trail search shall return results in < 1 second at p95 for datasets up to 500,000 records. | DN-5, DN-9 | Load test: search query returns within 1s at p95 against a 500K-row audit table. |
| NFR-03 | **Data Retention** | Audit trail records shall be retained for a minimum of 1 year from creation date. | DN-9 | Records created 364 days ago are retrievable. Retention policy is configurable upward but not below 1 year. |
| NFR-04 | **Security** | Only users with an explicit "approver" role assignment for the relevant approval stage shall be able to approve, reject, delegate, or send back a request. | DN-9 | A user without the approver role receives a 403 when attempting any approval action via UI or API. |
| NFR-05 | **Security** | All approval actions shall be authenticated and authorized per request. Session tokens shall not be sufficient to bypass per-action authorization checks. | DN-9 | Automated test: replaying an approval request with a stolen session token but revoked role returns 403. |
| NFR-06 | **Availability** | The approvals service shall maintain 99.9% uptime measured monthly (≤ 43 minutes downtime/month). | DN-3 (implicit) | Monthly uptime report shows ≥ 99.9%. |

---

## Non-Goals (P3 — Won't for R1)

| ID | Description | Source | Rationale |
|----|------------|--------|-----------|
| NG-01 | Department-specific approval thresholds (different $ limits per department). | DN-6 | Adds config complexity. R1 ships with a single org-wide threshold of $5,000. Revisit in R2 based on customer demand. |
| NG-02 | Email-based approval actions (approve/reject by replying to an email). | DN-3 | In-app and mobile-responsive UI addresses the "lost in email" problem. Email actions introduce security and deliverability risk. |
| NG-03 | Custom approval chains beyond two stages. | DN-2 | Two-stage (manager → finance) covers the stated need. Multi-stage chains add routing complexity we'll evaluate post-R1. |
| NG-04 | Configurable $5,000 first-stage threshold. | DN-1 | R1 hardcodes $5,000. Configuration can follow the department-threshold work in R2. |

---

## State Machine

```
Draft → Pending Approval (on submit, if amount ≥ $5,000)
Draft → Approved (on submit, if amount < $5,000 — no approval needed)
Pending Approval → Approved (manager approves; amount < $20,000 or finance stage disabled)
Pending Approval → Pending Finance Approval (manager approves; amount ≥ $20,000 and finance stage enabled)
Pending Approval → Rejected (manager rejects)
Pending Approval → Sent Back (manager sends back)
Pending Finance Approval → Approved (finance approves)
Pending Finance Approval → Rejected (finance rejects)
Pending Finance Approval → Sent Back (finance sends back)
Sent Back → Pending Approval (employee resubmits)
```

---

## Conflict Resolution Notes

| # | Tension | Resolution |
|---|---------|-----------|
| 1 | DN-2 says "optional" second-stage, but finance wants oversight. | FR-03 makes it org-admin configurable. Finance can mandate it via policy; the system doesn't force it. |
| 2 | DN-6 wants per-department thresholds, but R1 scope is tight. | Deferred to NG-01. Single threshold keeps routing logic simple for R1. |
| 3 | DN-1 says "manager approval" — ambiguous whether "manager" means direct manager or any manager. | FR-01 specifies "requester's direct manager." Delegation (FR-06) covers the case where that person is unavailable. |

---

## Assumptions

1. **Org hierarchy exists** — the system has access to a reporting-chain data source that maps each employee to their direct manager.
2. **Finance approver role** — at least one user per org will be assigned the finance-approver role before second-stage approval is enabled.
3. **Single currency** — thresholds are evaluated in the organization's base currency. Multi-currency conversion is out of scope for R1.

---

## Quality Gate Checklist

- [x] All P0/P1 requirements documented with clear acceptance criteria
- [x] Non-functional requirements quantified (< 500ms p95, 1-year retention, 99.9% uptime)
- [x] No unresolved contradictions between requirements (see Conflict Resolution)
- [ ] Stakeholders have reviewed and signed off ← **pending**
- [x] Requirements are traceable to discovery notes (DN-1 through DN-9)

---

`★ Insight ─────────────────────────────────────`
**Why the state machine matters here**: The discovery notes mention four statuses (pending, approved, rejected, sent back), but the two-stage approval flow actually requires a *fifth* state — "Pending Finance Approval" — to distinguish which stage a request is waiting on. Catching this kind of implicit state early in requirements prevents ambiguous UI and broken routing logic during implementation.

**Non-goals as a feature, not a gap**: Explicitly listing what R1 *won't* do (NG-01 through NG-04) with rationale is one of the highest-value outputs of requirements engineering. It gives stakeholders a place to argue scope *before* development starts, and it gives engineers permission to push back when someone asks for department thresholds mid-sprint.
`─────────────────────────────────────────────────`

The one open gate item is **stakeholder sign-off**. The next step per the skill is to circulate this to the operations managers and finance team for review, then feed the approved requirements into [spec-writing](../spec-writing/SKILL.md) and [acceptance-criteria](../acceptance-criteria/SKILL.md).
