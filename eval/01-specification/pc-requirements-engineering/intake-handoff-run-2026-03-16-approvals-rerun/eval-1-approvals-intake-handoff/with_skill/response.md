`★ Insight ─────────────────────────────────────`
Requirements engineering is distinct from spec-writing: the output is **what the system shall do**, not how. The key discipline is resisting the urge to invent precision — "near-instant" must stay as an open question, not a fabricated p99 target, until an owner confirms a bound.
`─────────────────────────────────────────────────`

---

# Requirements Document — Approvals Workflow (Release 1)

**Status:** Draft — pending stakeholder review
**Phase:** 01-Specification
**Source documents:** `approvals-intake-brief.md`, `approvals-discovery-notes.md`
**Owner:** TBD (one person must be named before quality gate)
**Downstream handoff:** `spec-writing` — expects a reviewed requirements doc, not architecture decisions

---

## 1. Scope Statement

This document covers the **first-release** approvals workflow for an existing SaaS product. It is scoped to purchase-request approval routing, approver actions, status visibility, in-product notification, and audit trail. It does **not** cover API design, database schema, storage strategy, or any architecture decision.

### 1.1 In Scope — Release 1

- Approval routing triggered by monetary thresholds ($5 k, $20 k)
- Manager-level approval and reject actions
- Optional finance second-stage approval
- Status visibility for requesters
- Rejection comments
- In-product approval surface (replacing email-only discovery)
- Mobile-friendly approver actions
- Searchable audit trail

### 1.2 Explicitly Out of Scope — Release 1 (P3)

| Item | Reason deferred |
|---|---|
| Department-specific approval thresholds | Requested by "some companies" (minority signal); adds routing complexity; reserved for release 2 |
| API or database design | Requirements layer only; downstream skill owns this |
| Email integration replacement | Notification channel design is an implementation decision |

---

## 2. Functional Requirements

Format: **The system shall [action] when [condition] so that [benefit].**

### 2.1 Approval Routing (Trigger)

| ID | Requirement | Priority | Source |
|---|---|---|---|
| FR-01 | The system shall route a purchase request to the requester's manager for approval when the request amount is ≥ $5,000, so that managers can exercise spending oversight. | P0 | Discovery: "Managers need every purchase request above $5,000 to require manager approval." |
| FR-02 | The system shall route an approved request to finance for a second-stage approval when the request amount is ≥ $20,000, so that finance retains control over large expenditures. | P1 | Discovery: "Finance wants optional second-stage approval above $20,000." — See OQ-01 on whether optional means per-tenant or per-request. |

### 2.2 Approver Actions

| ID | Requirement | Priority | Source |
|---|---|---|---|
| FR-03 | The system shall allow an authorized approver to approve a pending request, so that compliant requests can proceed. | P0 | Discovery: manager approval workflow. |
| FR-04 | The system shall allow an authorized approver to reject a pending request with a mandatory comment, so that the requester understands what to fix. | P0 | Discovery: "Customers asked for comments on rejection so employees know what to fix." |
| FR-05 | The system shall allow an authorized approver to send a request back to the requester without rejecting it, so that minor corrections can be made without a full re-submission cycle. | P1 | Discovery: "sent back" listed as a distinct status alongside approved/rejected/pending. |
| FR-06 | The system shall allow an authorized approver to delegate an approval action to another eligible approver, so that coverage is maintained during absence. | P1 | Discovery: audit trail must record "who approved, rejected, or **delegated** a request." Delegation is implied as a first-class action. |

### 2.3 Status Visibility

| ID | Requirement | Priority | Source |
|---|---|---|---|
| FR-07 | The system shall display the current status of a purchase request (pending, approved, rejected, sent back) to the requester, so that they have clear visibility without relying on email. | P0 | Discovery: "Users need clear status visibility: pending, approved, rejected, sent back." |

### 2.4 In-Product Discovery (Replacing Email-Buried Approvals)

| ID | Requirement | Priority | Source |
|---|---|---|---|
| FR-08 | The system shall surface pending approval requests to the approver within the product UI, so that approval actions are not lost in email. | P1 | Discovery: "Employees complain that current approvals are buried in email and get lost." |
| FR-09 | The system shall notify an approver when a new request is assigned to them for approval, so that approvers are alerted without polling. | P1 | Discovery: same signal; notification mechanism is an implementation detail for spec-writing. |

### 2.5 Mobile-Friendly Actions

| ID | Requirement | Priority | Source |
|---|---|---|---|
| FR-10 | The system shall allow an authorized approver to approve or reject a request from a mobile device without degraded functionality, so that approvers are not blocked when away from desktop. | P1 | Discovery: "Managers need a mobile-friendly way to approve or reject quickly." |

### 2.6 Audit Trail

| ID | Requirement | Priority | Source |
|---|---|---|---|
| FR-11 | The system shall record every approval action (approve, reject, delegate, send back) with the actor identity, timestamp, and action taken, so that a complete decision history exists. | P1 | Discovery: "Finance requires a searchable audit trail of who approved, rejected, or delegated a request." |
| FR-12 | The system shall allow authorized users to search the audit trail, so that finance and compliance stakeholders can retrieve decision history on demand. | P1 | Discovery: "searchable audit trail." — See OQ-05 on who can search. |

---

## 3. Non-Functional Requirements

| ID | Requirement | Priority | Source | Bound type |
|---|---|---|---|---|
| NFR-01 | The system shall retain audit trail records for a minimum of 1 year. | P0 | Discovery: "audit trail must be retained for at least 1 year." | Sourced |
| NFR-02 | The system shall permit approval actions only by users who are designated authorized approvers for that request, so that unauthorized actors cannot alter approval state. | P0 | Discovery: "only authorized approvers should act on a request." | Sourced (direction only; enforcement mechanism is an implementation decision) |
| NFR-03 | Approval actions shall feel near-instant to the approver. | P1 | Discovery: "approval actions should feel near-instant." | **Open question — see OQ-03.** No latency bound is sourced; do not convert to a number without owner confirmation. |

---

## 4. Open Questions

These must be resolved before the quality gate closes. Each has a named owner slot; owners must be filled in before handoff to spec-writing.

| ID | Question | Why it blocks | Owner |
|---|---|---|---|
| OQ-01 | Is the second-stage finance approval (≥ $20 k) optional per **tenant** (configured once at account level) or optional per **request** (toggled case-by-case)? | Changes routing model and FR-02 scope significantly. | TBD |
| OQ-02 | How is the requester's manager determined in the existing SaaS product? Does a manager relationship already exist in the data model, or must it be set up as part of this feature? | FR-01 cannot be implemented without knowing the manager-resolution mechanism; this is an integration point with the existing system. | TBD |
| OQ-03 | Does "near-instant" (NFR-03) require a user-facing latency SLA, or only a back-end processing SLA? What is the acceptable bound? | Without a bound, NFR-03 is untestable. | TBD |
| OQ-04 | What exactly does "sent back" mean in the workflow? Does the requester receive an editable request to correct and resubmit, or does it simply return to draft state? | Determines whether FR-05 implies a resubmission sub-flow in scope. | TBD |
| OQ-05 | Who can search the audit trail — all users, only approvers, only finance/admin roles? | Determines access-control scope for FR-12. | TBD |

---

## 5. Risks

Carried forward from intake brief verbatim:

1. **Routing rule ambiguity** — Manager ownership, threshold semantics (e.g., ≥ vs. >, inclusive of fees/taxes), and second-stage finance configuration may hide unresolved decisions. OQ-01 and OQ-02 are the primary vectors.
2. **Premature solutioning** — Mobile-friendly actions and audit-trail requirements invite architecture decisions (push notifications, storage schema, indexing) before requirements are agreed. Spec-writing must not begin until this document passes stakeholder review.

---

## 6. Assumptions (Requiring Owner Confirmation)

| ID | Assumption | If wrong, impact |
|---|---|---|
| ASM-01 | "Optional second-stage" (FR-02) means the tenant can configure whether it is required; when not configured, requests ≥ $20 k skip the finance stage. | Routing logic and P1 priority change. |
| ASM-02 | Delegation (FR-06) is available to any authorized approver, not restricted to a manager or admin role. | Access control model changes. |
| ASM-03 | The 1-year audit-trail retention (NFR-01) refers to calendar year from the date of the action, with no purge trigger before that. | Retention and storage implications change. |

---

## 7. Requirements Traceability Summary

| Req ID | User need | Priority |
|---|---|---|
| FR-01 | Manager oversight of purchases ≥ $5 k | P0 |
| FR-02 | Finance control of purchases ≥ $20 k | P1 |
| FR-03 | Approvers can act to approve | P0 |
| FR-04 | Approvers can reject with comment | P0 |
| FR-05 | Approvers can send back for correction | P1 |
| FR-06 | Approvers can delegate during absence | P1 |
| FR-07 | Requesters see clear status | P0 |
| FR-08 | Approvals visible in-product, not only email | P1 |
| FR-09 | Approvers notified of new assignments | P1 |
| FR-10 | Mobile-friendly approve/reject | P1 |
| FR-11 | Complete, recorded decision history | P1 |
| FR-12 | Searchable audit trail for finance/compliance | P1 |
| NFR-01 | 1-year audit-trail retention | P0 |
| NFR-02 | Authorized-approvers-only access control | P0 |
| NFR-03 | Near-instant action responsiveness | P1 (bound pending OQ-03) |

---

## 8. Quality Gate Checklist

- [ ] All P0/P1 requirements have acceptance criteria (downstream: `acceptance-criteria` skill)
- [ ] OQ-01 through OQ-05 resolved and owners confirmed
- [ ] ASM-01 through ASM-03 confirmed or corrected by stakeholders
- [ ] NFR-03 latency bound confirmed or formally deferred
- [ ] No architecture decisions embedded in this document
- [ ] Single named owner assigned to this requirements doc
- [ ] Stakeholder review sign-off obtained before handoff to spec-writing

---

`★ Insight ─────────────────────────────────────`
Three things worth noting in this output:
1. **"Optional" is a landmine word.** "Finance wants optional second-stage approval" was left as OQ-01 rather than arbitrarily resolved — "optional per tenant" vs "optional per request" produces entirely different routing models in the spec.
2. **Delegation was inferred, not stated.** It appeared only in the audit trail note ("who approved, rejected, or *delegated*"). Surfacing it as FR-06 makes the implicit contract explicit before spec-writing locks it in.
3. **NFR-03 has no number.** "Near-instant" is a feeling, not a target. Recording it without inventing a p95/p99 figure preserves honesty — the number must come from a product or engineering owner, not from the requirements author.
`─────────────────────────────────────────────────`
