`★ Insight ─────────────────────────────────────`
Requirements docs derived from discovery interviews have a layering problem: raw interview observations ("near-instant") need to be promoted to structured requirements *without* prematurely collapsing open questions into decisions. Preserving the open-question layer is as important as writing the requirements themselves — it prevents downstream specs from silently inheriting false assumptions.
`─────────────────────────────────────────────────`

---

# Approvals Workflow — Release 1 Requirements

**Document type:** requirements-doc  
**Source files:** `approvals-intake-brief.md`, `approvals-discovery-notes.md`  
**Status:** draft for review  
**Date:** 2026-03-16

---

## 1. Scope Statement

This document covers the first-release approvals workflow for an existing SaaS product. Scope is limited to the requirements layer. No API design, database schema, storage decisions, or architecture choices are in scope here.

### 1.1 In Scope — Release 1

- Purchase request approval routing (single-stage and optional two-stage)
- Configurable approval thresholds at tenant and department level
- Approval actions: approve, reject, send back (with required comment on rejection/send-back)
- Request status visibility for requesters
- Mobile-friendly approver action surface
- Searchable audit trail
- Authorization enforcement on approval actions

### 1.2 Explicitly Out of Scope — Release 1

- Delegation workflows (flagged in discovery but not fully specified; deferred)
- Integration with external procurement or ERP systems
- Bulk approval actions
- Approval SLA enforcement or escalation rules
- Approver substitution / out-of-office coverage

---

## 2. Functional Requirements

### FR-01 — Approval Threshold: Standard

A purchase request that meets or exceeds **$5,000** must require manager approval before it can be fulfilled.

> **Open question OQ-2:** How is "the requester's manager" determined within the existing SaaS product? (See §5.)

### FR-02 — Approval Threshold: Finance (Second Stage)

A purchase request that meets or exceeds **$20,000** must trigger an optional second-stage finance approval, in addition to manager approval.

> **Open question OQ-1:** Is the second-stage finance approval optional per tenant, per request, or a fixed system rule? (See §5.)

### FR-03 — Department-Specific Thresholds

Tenants must be able to configure department-specific approval thresholds that override the default thresholds in FR-01 and FR-02.

**Assumption A-1:** Department-specific thresholds apply to the same approval actions (approve / reject / send back) and the same approval stages defined in FR-01 and FR-02. A department threshold cannot introduce a new stage type in Release 1.

### FR-04 — Approval Actions

An authorized approver must be able to take exactly one of the following actions on a pending request:

| Action | Description |
|--------|-------------|
| Approve | Advances the request to the next stage or marks it fully approved |
| Reject | Terminates the request; a comment is required |
| Send back | Returns the request to the requester for correction; a comment is required |

### FR-05 — Comment on Rejection / Send Back

When an approver selects Reject or Send Back, the system must require a non-empty comment before the action is accepted. The comment must be visible to the requester.

### FR-06 — Request Status Visibility

A requester must be able to see the current status of their request at all times. Supported statuses in Release 1:

- **Pending** — awaiting an approver action
- **Approved** — all required approval stages completed
- **Rejected** — terminated by an approver
- **Sent Back** — returned to requester for changes

### FR-07 — In-Product Approval Surface

Approval actions must be surfaced within the product, not solely via email. This addresses the discovery finding that email-based approvals are lost or missed.

### FR-08 — Mobile-Friendly Approver Actions

The approver action surface (approve, reject, send back, comment entry) must be usable on a mobile browser without requiring a separate native app.

**Assumption A-2:** "Mobile-friendly" means responsive layout on common mobile viewport sizes (≥ 320 px width). Native iOS/Android apps are out of scope for Release 1.

### FR-09 — Audit Trail: Content

The system must record and make searchable an audit event for every approval action. Each audit event must capture at minimum:

- Request identifier
- Action taken (approve / reject / send back)
- Actor identity (who took the action)
- Timestamp

### FR-10 — Audit Trail: Retention

Audit trail records must be retained for a minimum of **1 year** from the date the event was recorded.

### FR-11 — Authorization Enforcement

Only authorized approvers may act on a given request. An unauthorized user attempting an approval action must be denied. The system must not rely solely on UI concealment to enforce this constraint.

---

## 3. Non-Functional Requirements

### NFR-01 — Approval Action Responsiveness

Approval actions must feel responsive to the user. The specific latency target is an open question (see OQ-3). Until resolved, treat this as a quality bar requiring measurement rather than a hard SLA.

### NFR-02 — Audit Trail Availability for Search

The audit trail must be searchable by finance and authorized administrators. Indexing and search latency targets are deferred to the technical spec phase.

### NFR-03 — Authorization Correctness

Authorization checks on approval actions must be enforced server-side on every request, independent of UI state.

---

## 4. Constraints

These constraints are inherited from the intake brief and must be preserved through all downstream handoffs.

| # | Constraint |
|---|------------|
| C-1 | This is an existing SaaS product; requirements must not assume greenfield infrastructure. |
| C-2 | Stay in the requirements layer; do not jump into API, database, or storage design. |
| C-3 | Preserve explicit scope boundaries for Release 1 (§1.2). |
| C-4 | Treat unsupported quantitative targets (e.g., latency figures) as open questions, not hard requirements. |

---

## 5. Open Questions

These must be resolved before the technical spec phase begins.

| ID | Question | Impact if unresolved |
|----|----------|----------------------|
| OQ-1 | Is the second-stage finance approval optional per tenant or per request, or is it a system-wide fixed rule? | Determines configuration model and tenant setup surface |
| OQ-2 | How is the requester's manager determined in the existing SaaS product? (Org hierarchy? Explicit assignment? Role mapping?) | Determines routing logic for FR-01 and FR-03 |
| OQ-3 | Does "near-instant" approval action feedback require a user-facing latency target (e.g., < 500 ms) or only a back-end SLA? | Determines whether NFR-01 becomes a testable acceptance criterion |

---

## 6. Risks

Inherited from the intake brief; preserved here for downstream visibility.

| # | Risk | Mitigation |
|---|------|-----------|
| R-1 | Approval routing rules may hide ambiguity about manager ownership, threshold semantics, and second-stage finance configuration. | OQ-1 and OQ-2 must be resolved before spec. FR-03 scoped narrowly (A-1) to limit blast radius. |
| R-2 | Mobile-friendly actions and audit-trail requirements may tempt early solutioning before requirements are agreed. | Spec-writing phase must not begin until this document is reviewed and open questions are triaged. |

---

## 7. Assumptions

| ID | Assumption | If wrong, impact |
|----|------------|-----------------|
| A-1 | Department thresholds apply to existing approval stages only; they cannot introduce new stage types in Release 1. | Would require expanding FR-03 and the routing model. |
| A-2 | "Mobile-friendly" means responsive layout on ≥ 320 px viewports; native apps are out of scope. | Would require a separate mobile-app track. |

---

## 8. Handoff Notes for Downstream Skills

- **Next skill:** `spec-writing` → output: `technical-spec`
- **After that:** `acceptance-criteria` → output: `acceptance-criteria-set`
- The spec-writing phase must not begin until OQ-1 and OQ-2 (§5) are resolved; OQ-3 can proceed in parallel.
- Do not introduce storage, API, or database decisions in the spec; those belong in the technical spec.
- The delegation/escalation features mentioned in discovery are deferred; do not spec them for Release 1.
