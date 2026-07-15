# Audit Log — First-Release Requirements

---

## Functional Requirements

| ID | Requirement | Notes |
|----|-------------|-------|
| FR-01 | The system **shall** capture an audit record for every financial action performed on the platform. | "Financial action" must be enumerated in the action-type catalogue before development begins. |
| FR-02 | Each audit record **shall** include, at minimum: actor identity, action type, affected account identifier, timestamp (UTC), and outcome (success / failure). | Field list is a floor, not a ceiling — teams may propose additions. |
| FR-03 | Audit records **shall** be immutable once written; no product-layer interface may modify or delete them. | Applies to all roles including internal admins. |
| FR-04 | Audit records **shall** be retained for a minimum of **7 years** from the time of creation. | Retention applies to the original record; any derivative (e.g., export) does not reset the clock. |
| FR-05 | Only explicitly authorized roles **shall** be permitted to search audit logs. | Role list must be approved by Security before release. |
| FR-06 | Only explicitly authorized roles **shall** be permitted to export audit logs. | May be a subset of FR-05 roles; must be defined explicitly. |
| FR-07 | Authorized users **shall** be able to search audit logs using the following filter dimensions: account identifier, actor identity, date range, and action type. Combinations of filters must be supported. | |
| FR-08 | Authorized users **shall** be able to export a filtered audit log result set as a CSV file. | Export must honor the same filter dimensions as search (FR-07). |
| FR-09 | Every export operation **shall** itself generate an audit record capturing: exporting actor, filters applied, record count, and timestamp. | This is a first-class audit event, not a side-channel log. |
| FR-10 | All search and export access events **shall** be logged and made reviewable so that data access can be justified on request. | Supports legal review in applicable regions. |

---

## Non-Functional Requirements

| ID | Requirement | Category |
|----|-------------|----------|
| NFR-01 | Search results **shall** be returned within a latency budget acceptable to support engineers during both normal and month-end peak load. *(Specific threshold to be agreed with Operations and Platform before implementation.)* | Performance |
| NFR-02 | Search throughput **shall** not degrade materially during month-end load spikes relative to baseline. | Scalability |
| NFR-03 | The audit record store **shall** be durable; records must survive single-node or single-zone failure without loss. | Durability |
| NFR-04 | Immutability of audit records **shall** be enforceable and verifiable — it must be possible to demonstrate to an auditor that no record has been altered. | Integrity |
| NFR-05 | Role-based access to search and export **shall** be enforced at the service boundary, not only at the UI layer. | Security |
| NFR-06 | CSV exports **shall** include sufficient metadata (e.g., export timestamp, exporting actor, applied filters) to make the file traceable without reference to internal systems. | Traceability |
| NFR-07 | The system **shall** support per-region data access justifiability by making access logs reviewable by authorized Legal/Compliance personnel. | Legal / Compliance |

---

## Priorities

| Priority | IDs | Rationale |
|----------|-----|-----------|
| **P0 — Blocking; must ship in release 1** | FR-01, FR-02, FR-03, FR-04, NFR-03, NFR-04, NFR-05 | Regulatory non-negotiables. Without immutable capture and 7-year retention the platform cannot operate in regulated markets. |
| **P1 — Required for release 1** | FR-05, FR-06, FR-07, FR-08, FR-09, NFR-01, NFR-02, NFR-06 | Operability and customer-facing value. Search and export are the primary use cases; export traceability is a compliance requirement tied directly to the export feature. |
| **P2 — Required before general availability, can trail release 1 by one sprint** | FR-10, NFR-07 | Legal justifiability review is region-specific and does not block core functionality, but must be complete before GA in affected regions. |

---

## Source Traceability

| Requirement(s) | Source |
|----------------|--------|
| FR-01, FR-02 | Compliance: *"audit records for financial actions"*; Operations: *"search by account, actor, date range, and action type"* (implies record structure) |
| FR-03, NFR-04 | Security: *"audit records must not be editable or deletable through the product"* |
| FR-04 | Compliance: *"retained for 7 years"* |
| FR-05, FR-06, NFR-05 | Security: *"only explicitly authorized roles may search or export"* |
| FR-07, NFR-01, NFR-02 | Operations: *"fast search by account, actor, date range, and action type"*; Platform: *"month-end load is heavy; search must remain responsive"* |
| FR-08 | Product: *"customers want to export filtered audit logs as CSV"* |
| FR-09, NFR-06 | Compliance: *"exported data must be traceable to who exported it and when"* |
| FR-10, NFR-07 | Legal: *"some regions require data access to be justifiable and reviewable"* |
| NFR-03 | Platform: *"month-end load"* — implies durability needs alongside availability |

---

## Explicit Non-Goals (Release 1)

| Non-Goal | Reason for Exclusion |
|----------|----------------------|
| Storage, schema, or index design | Explicitly out of scope per request; architecture phase follows requirements. |
| Real-time alerting or anomaly detection on audit events | Not requested by any stakeholder; would expand scope significantly. |
| Audit coverage for non-financial actions (e.g., profile updates, UI navigation) | Stakeholder note scopes to financial actions only. |
| Self-service customer-facing audit UI | Product asked for CSV export only; a browsable UI is a separate product decision. |
| Automated retention enforcement / purge scheduling | Retention policy is defined here; the mechanism is an architecture concern. |
| Data masking, anonymization, or redaction within audit records | Not raised by any stakeholder; introducing it could conflict with the immutability requirement. |
| SIEM or external log-pipeline integration | Not requested; would require security review of data egress paths. |
| Audit log access for end-customer support agents (customer-side roles) | Access roles are defined only for internal authorized roles in this release. |

---

`★ Insight ─────────────────────────────────────`
**On the immutability / retention tension:** FR-03 and FR-04 interact in a subtle way — "immutable" must be scoped to mean *content-immutable*, while the retention lifecycle (archival, tiering, eventual deletion at year 7) is a separate operational concern. Conflating the two in architecture leads to systems that are either accidentally deletable or impossible to legally purge.

**On the meta-audit (FR-09/FR-10):** Requiring that exports and access events are themselves audited is a recursive design constraint. Whatever captures financial audit records must also be able to capture audit-of-audit records — that single decision has knock-on effects on the write path and role model.

**On P2 timing:** Legal's justifiability requirement (FR-10) is deliberately separated from the core search/export path so it doesn't block an MVP, but it should inform data structure decisions in architecture even if the review UI ships later.
`─────────────────────────────────────────────────`

---

**Open questions to resolve before architecture begins**

1. What is the approved enumeration of "financial actions" (FR-01)?
2. What specific latency budget is acceptable for search at peak load (NFR-01)?
3. Which roles are explicitly authorized for search vs. export (FR-05/FR-06)?
4. Which regions trigger the legal justifiability requirement (NFR-07/FR-10)?
5. Is the 7-year clock based on event timestamp, record-creation timestamp, or account closure — whichever is later?
