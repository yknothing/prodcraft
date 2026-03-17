`★ Insight ─────────────────────────────────────`
Requirements engineering at its core is about **traceability and testability** — every "shall" statement must link back to a stakeholder source and be falsifiable. The most common failure mode is conflating *what the system must do* with *how it should do it*. This document deliberately stays in the "what" layer.
`─────────────────────────────────────────────────`

---

# Audit Log — First-Release Requirements

**Document status:** Draft · Awaiting stakeholder sign-off
**Owner:** _[assign before architecture kickoff]_
**Date:** 2026-03-16

---

## 1. Functional Requirements

| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| FR-01 | The system shall record an audit event for every financial action performed on the platform, capturing at minimum: actor identity, affected account, action type, timestamp (UTC), and outcome. | P0 | Compliance |
| FR-02 | The system shall retain every audit record for a minimum of 7 years from the time it was created. | P0 | Compliance |
| FR-03 | The system shall prevent any product-layer operation from modifying or deleting an existing audit record. | P0 | Security |
| FR-04 | The system shall enforce role-based access control such that only explicitly authorized roles may query or export audit logs. | P0 | Security |
| FR-05 | The system shall support search of audit records filtered by: account identifier, actor identity, date range, and action type — individually or in combination. | P0 | Operations |
| FR-06 | The system shall allow an authorized customer to export their filtered audit log results as a CSV file. | P1 | Product |
| FR-07 | The system shall record an export event in the audit log capturing: the identity of the person who triggered the export, the filter criteria applied, and the timestamp of the export. | P0 | Compliance ("exported data must be traceable to who exported it and when") |
| FR-08 | The system shall produce a reviewable record of every access to audit log data (reads, searches, exports) sufficient to justify that access to a legal or compliance reviewer. | P1 | Legal |

---

## 2. Non-Functional Requirements

### 2.1 Performance

| ID | Requirement | Priority | Source / Status |
|----|-------------|----------|-----------------|
| NFR-P1 | Audit log search queries shall return results within an **[OPEN QUESTION — see §5.1]** response time at p95, including during month-end peak load periods. | P0 | Platform ("must remain responsive") — bound not specified in source; requires owner confirmation before architecture |
| NFR-P2 | The audit log subsystem shall not degrade response times of the core transaction-processing path under month-end load. | P0 | Platform |

### 2.2 Security & Compliance

| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| NFR-S1 | Audit records shall be written in an append-only manner; the write path must be isolated from any update or delete code paths accessible via the product API. | P0 | Security |
| NFR-S2 | Access to audit log search and export endpoints shall require explicit role authorization; authorization checks shall be enforced at the API layer, not only in the UI. | P0 | Security |
| NFR-S3 | All audit log data shall be protected at rest and in transit according to the platform's existing data-classification policy. | P0 | Compliance (implied by 7-year retention and financial data context) — **Assumption A1; confirm policy reference** |

### 2.3 Reliability & Retention

| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| NFR-R1 | The audit log storage tier shall have a durability SLA of **[OPEN QUESTION — see §5.2]**; no audit record may be silently lost after acknowledgement. | P0 | Compliance (7-year retention implies durability) — precise SLA is an open question |
| NFR-R2 | Audit event capture must not be bypassable; if the audit write fails, the system shall **[OPEN QUESTION — see §5.3]** (reject the financial action, queue and retry, or alert). | P0 | Compliance / Security — failure-mode policy requires owner decision |

### 2.4 Usability

| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| NFR-U1 | The CSV export format shall be self-describing (column headers, field names consistent with UI labels) and reproducible given the same filter criteria. | P1 | Product |

---

## 3. Prioritized Requirements Summary

| Priority | IDs |
|----------|-----|
| **P0 — Must have** | FR-01, FR-02, FR-03, FR-04, FR-05, FR-07, NFR-P1, NFR-P2, NFR-S1, NFR-S2, NFR-S3, NFR-R1, NFR-R2 |
| **P1 — Should have** | FR-06, FR-08, NFR-U1 |
| **P2 — Could have** | _(none identified in source material)_ |
| **P3 — Won't have (this release)** | See §4 |

---

## 4. Explicit Non-Goals (First Release)

These are out of scope to prevent scope creep and to keep architecture focused. Re-evaluate each at the next planning cycle.

| Non-Goal | Rationale |
|----------|-----------|
| Real-time alerting or anomaly detection on audit events | Not raised by any stakeholder; a separate security-monitoring capability |
| Audit log ingestion from third-party or external systems | Only in-platform financial actions were scoped |
| Self-service audit log access for end-users without an authorized role | Access is restricted to explicitly authorized roles; broadening is a future access-model decision |
| Structured query beyond the four supported filter dimensions (account, actor, date range, action type) | Keeping scope bounded to stated Operations need |
| Long-term archival tier management / retrieval from cold storage | Retention must be met (FR-02), but the retrieval SLA from archived records is not specified and should not be assumed |
| GDPR / right-to-erasure handling for audit records | Conflicts directly with FR-02/FR-03; this legal tension must be resolved outside this document before any erasure capability is scoped |

---

## 5. Open Questions (Require Owner Decisions Before Architecture)

| ID | Question | Owner | Why It Matters |
|----|----------|-------|----------------|
| OQ-5.1 | What is the acceptable p95 search response time, including at month-end peak? | Platform lead | Drives indexing and caching strategy |
| OQ-5.2 | What durability SLA is required for audit storage (e.g., 99.999999999%)? | Compliance owner | Determines storage tier selection |
| OQ-5.3 | If an audit write fails, should the originating financial action be rejected, queued, or only alerted? | Compliance + Engineering lead | Critical failure-mode policy — security vs. availability trade-off |
| OQ-5.4 | Which specific roles are "explicitly authorized" to search and export audit logs? | Security owner | Must be enumerated before FR-04 has testable acceptance criteria |
| OQ-5.5 | Does the 7-year retention clock start at event time, or at end of fiscal year? | Legal / Compliance | Affects retention boundary calculations |
| OQ-5.6 | How does right-to-erasure (GDPR) interact with the immutability requirement for regions that have both obligations? | Legal | Unresolved contradiction; cannot be silently deferred |
| OQ-5.7 | Which regions require "data access justification" under FR-08, and what form must that justification take? | Legal | Scopes the access-review record format |

---

## 6. Source Traceability Index

| Stakeholder | Notes mapped to | Requirements |
|-------------|-----------------|--------------|
| Compliance | 7-year retention | FR-02, NFR-R1 |
| Compliance | Exported data traceable | FR-07 |
| Security | Role-restricted search/export | FR-04, NFR-S2 |
| Security | Records not editable/deletable | FR-03, NFR-S1 |
| Operations | Fast search by account, actor, date, action | FR-05, NFR-P1, NFR-P2 |
| Product | Customer CSV export | FR-06, NFR-U1 |
| Platform | Month-end responsiveness | NFR-P1, NFR-P2 |
| Legal | Access justifiability and reviewability | FR-08, OQ-5.7 |

---

## 7. Quality Gate Checklist

- [ ] All P0/P1 requirements have acceptance criteria authored (next step: [acceptance-criteria skill](../acceptance-criteria/SKILL.md))
- [ ] Open questions OQ-5.1 through OQ-5.7 assigned to named owners
- [ ] OQ-5.6 (GDPR vs. immutability conflict) resolved before architecture begins
- [ ] Authorized roles list (OQ-5.4) confirmed by Security owner
- [ ] Document reviewed and signed off by: Compliance, Security, Legal, Platform, Product

---

`★ Insight ─────────────────────────────────────`
Three things worth flagging as you move forward:

1. **The GDPR tension (OQ-5.6) is a hard blocker** — immutability (FR-03) and right-to-erasure are directly contradictory in overlapping regions. This cannot be deferred to architecture; it's a legal decision that constrains design choices.

2. **FR-07 (export meta-audit) is a P0, not P1** — it's easy to treat it as a logging nicety, but Compliance explicitly requires traceability of who exported what. If export lands before FR-07, you have a compliance gap on day one.

3. **OQ-5.3 (audit write failure mode) is an architectural fork** — rejecting the financial action on audit failure is maximally safe but affects availability; silent queueing is operationally friendlier but creates a window where actions exist without audit records. This decision must be made before any write-path design begins.
`─────────────────────────────────────────────────`
