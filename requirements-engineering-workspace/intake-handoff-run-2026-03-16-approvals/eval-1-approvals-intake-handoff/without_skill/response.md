I'll write directly to the working directory:

---

# Requirements Document — Approvals Workflow, Release 1

**Product:** Existing SaaS (purchase-request module)
**Skill:** requirements-engineering
**Status:** Draft for downstream review
**Date:** 2026-03-16

---

## 1. Context

This is an existing SaaS product. Release 1 introduces a first-party approvals workflow to replace the current email-based approval process, which operations managers have identified as unreliable and opaque. No greenfield infrastructure is assumed; requirements are scoped to behaviour and constraints only.

---

## 2. Scope Boundary — Release 1

**In scope:**
- Single-stage manager approval for purchase requests above a monetary threshold
- Optional second-stage finance approval above a higher monetary threshold
- Mobile-compatible approval and rejection actions
- Requester status visibility
- Rejection comments
- Searchable audit trail

**Explicitly out of scope for Release 1:**
- API design, database schema, or storage architecture
- Integration with external ERP or procurement systems
- Bulk approval actions
- Approval chains longer than two stages
- SLA enforcement or escalation automation
- Delegation of approval authority (see open questions)

---

## 3. Functional Requirements

### 3.1 Threshold-Based Routing

**FR-01** — When a purchase request is submitted, the system SHALL evaluate the request amount against the applicable approval threshold to determine the required approval stage(s).

**FR-02** — The system SHALL require manager approval for any purchase request whose amount exceeds $5,000.
> *Assumption A1: "exceeds" means strictly greater than $5,000 (i.e., $5,000.00 does not trigger approval). This must be confirmed before spec.*

**FR-03** — The system SHALL support an optional second-stage finance approval for purchase requests whose amount exceeds $20,000.
> *Open Question OQ-1: Is the second-stage finance approval optional per tenant (configured once per organisation) or togglable per individual request? Resolution required before spec.*

**FR-04** — The system SHALL allow tenant administrators to configure department-specific approval thresholds that override the default thresholds defined in FR-02 and FR-03 for requests originating from that department.

**FR-05** — When department-specific thresholds are configured, the system SHALL apply the department threshold; when none is configured, the system SHALL fall back to the global tenant threshold.

---

### 3.2 Approver Identity and Assignment

**FR-06** — The system SHALL route each purchase request to the requester's designated manager as the first-stage approver.
> *Open Question OQ-2: How is the requester's manager determined within the existing SaaS product (e.g., org-chart field, HR integration, manual assignment)? The answer defines whether this is a lookup requirement or a configuration requirement.*

**FR-07** — The system SHALL route qualifying requests to a configured finance approver or finance approval group as the second-stage approver.

**FR-08** — The system SHALL prevent any user who is not the designated approver for a given stage from taking an approval action on that request.

---

### 3.3 Approval Actions

**FR-09** — An approver SHALL be able to perform exactly one of the following actions on a pending request assigned to them:
- **Approve** — advance the request to the next stage or mark it fully approved
- **Reject** — close the request as rejected
- **Send back** — return the request to the requester for revision without closing it

**FR-10** — When an approver rejects a request, the system SHALL require the approver to provide a written comment explaining the reason before the rejection is recorded.

**FR-11** — When an approver sends back a request, the system SHALL allow (but not require) the approver to include a comment.

**FR-12** — All approval actions (approve, reject, send back) SHALL be completable from a mobile browser without requiring a native app installation.

---

### 3.4 Requester Status Visibility

**FR-13** — The system SHALL display the current status of every purchase request to its requester at all times. The defined statuses for Release 1 are:

| Status | Meaning |
|---|---|
| `pending` | Awaiting an approver action |
| `approved` | All required stages have been approved |
| `rejected` | Rejected at any stage; not resubmittable without revision |
| `sent_back` | Returned to requester for revision |

**FR-14** — When a request is sent back, the system SHALL surface any approver comment alongside the `sent_back` status so the requester can act on the feedback without hunting for it.

**FR-15** — The system SHALL notify the requester (via the product's existing notification mechanism) when their request changes status.
> *Assumption A2: An existing in-product or email notification mechanism is available. If not, a notification delivery mechanism is a dependency that must be scoped separately.*

---

### 3.5 Audit Trail

**FR-16** — The system SHALL record an immutable audit event each time any of the following actions occurs on a purchase request:
- Request submitted
- Approval action taken (approve, reject, send back), including the acting user, timestamp, and any comment
- Status transition

**FR-17** — The audit trail SHALL be searchable by at least the following dimensions:
- Request identifier
- Requester name or identifier
- Approver name or identifier
- Action type (approve, reject, send back)
- Date range

**FR-18** — Audit records SHALL be retained for a minimum of 1 year from the date of the recorded event.

---

## 4. Non-Functional Requirements

**NFR-01 — Responsiveness of approval actions**
Approval actions (approve, reject, send back) shall feel immediate to the approver. The target for user-perceived response is "near-instant."
> *Open Question OQ-3: Does "near-instant" require a defined user-facing latency target (e.g., ≤ 500 ms to confirmed UI feedback) or only a back-end SLA? A concrete number is needed before this becomes a testable acceptance criterion.*

**NFR-02 — Audit retention**
Audit records shall be retained for a minimum of 1 year. Retention beyond 1 year is not a Release 1 requirement.

**NFR-03 — Access control**
Only the designated approver(s) for a given stage of a given request shall be permitted to take an approval action on that request. Unauthorised action attempts shall be rejected by the system.

**NFR-04 — Mobile compatibility**
All approver-facing actions shall be fully operable on a mobile browser (screen widths ≥ 375 px) without native app installation.

---

## 5. Open Questions

| ID | Question | Impact if unresolved |
|---|---|---|
| OQ-1 | Is second-stage finance approval toggled per tenant or per individual request? | Determines whether FR-03 is a tenant-config requirement or a per-request UI requirement |
| OQ-2 | How is the requester's manager determined in the existing SaaS product? | Determines whether FR-06 is a data-lookup, HR-sync, or manual-assignment requirement |
| OQ-3 | Does "near-instant" require a user-facing latency target or only a back-end SLA? | Determines whether NFR-01 is testable in acceptance criteria without further input |

---

## 6. Assumptions

| ID | Assumption | Risk if wrong |
|---|---|---|
| A1 | "Exceeds $5,000" means strictly greater than (not ≥). $5,000.00 does not trigger approval. | Threshold boundary defects in edge cases |
| A2 | An existing in-product notification channel (in-app or email) is available and can be called from the approvals workflow. | FR-15 becomes a dependency that widens scope |
| A3 | "Department" is an existing organisational unit already modelled in the SaaS product that can be associated with a purchase request at submission time. | FR-04 may require new data modelling work outside this workflow |

---

## 7. Constraints Carried Forward

- This document stays in the requirements layer. No API endpoints, database tables, queue designs, or storage schemas appear here.
- Delegation (forwarding an approval to a colleague) is deferred to a post-Release 1 milestone.
- All quantitative targets without confirmed stakeholder agreement (OQ-3) are flagged as open questions, not hard requirements.
- The downstream spec must preserve the existing product's data model for requesters, managers, and departments rather than assuming a clean-slate design.

---

*Produced by: requirements-engineering skill*
*Next artifact: technical-spec (spec-writing skill)*

---

`★ Insight ─────────────────────────────────────`
Notice that FR-08 (only designated approvers may act) and NFR-03 (access control) cover the same security property from two angles — FR-08 is the *behavioural* requirement (what the system does), NFR-03 is the *quality* constraint (what the system must enforce). Keeping them separate lets the spec writer turn each into independent test targets rather than tangling role-checking with action logic.
`─────────────────────────────────────────────────`

---

Here's a summary of the key decisions made and where your input would sharpen the document before it passes to spec-writing:

**The three open questions are the critical path.** OQ-1 (finance approval granularity), OQ-2 (manager lookup mechanism), and OQ-3 (latency target) each gate a different downstream artifact — spec, data model, and acceptance criteria respectively. None of the three can be resolved from the interview notes alone.

**Two threshold boundary assumptions (A1, A3)** need a quick stakeholder confirmation. "Exceeds $5,000" vs "at or above $5,000" is the kind of silent assumption that produces a bug found in UAT, not development.

**Delegation is explicitly deferred.** The interview notes don't mention it, but it's a natural follow-up request from managers. Noting it as out-of-scope now prevents scope creep during spec-writing.

Would you like to resolve any of the open questions before this passes to the spec-writing phase, or should I carry them forward as flagged unknowns in the technical spec?
