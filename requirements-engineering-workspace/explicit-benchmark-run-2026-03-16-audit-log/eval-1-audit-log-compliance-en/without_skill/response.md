# Audit Log — First-Release Requirements

---

## 1. Functional Requirements

| ID | Requirement | Notes |
|----|-------------|-------|
| FR-01 | The system **shall** capture an immutable audit record for every financial action performed on the platform. | A "financial action" includes any state-changing operation on accounts, transactions, transfers, approvals, or access grants — exact taxonomy to be confirmed with Product & Compliance before implementation. |
| FR-02 | Audit records **shall** include at minimum: actor identity, action type, affected account(s), timestamp, and outcome (success/failure). | Fields are minimum viable; additions allowed before v1 ships. |
| FR-03 | Authorized users **shall** be able to search audit records by: account, actor, date range, and action type. Combinations of these filters must all be supported simultaneously. | |
| FR-04 | Authorized users **shall** be able to export a filtered result set as a CSV file. | Export must respect the same filters available in search. |
| FR-05 | Every export operation **shall** itself be recorded as an audit event capturing: the exporting actor's identity, timestamp, and the exact filter criteria applied. | |
| FR-06 | No product-facing interface **shall** expose edit or delete operations on audit records. | This covers both UI and API surface. |
| FR-07 | Access to audit log search and export **shall** be gated behind explicitly assigned roles; no role inheritance or default access is permitted. | |
| FR-08 | Audit records **shall** be retained for a minimum of 7 years from the time of record creation. | Retention enforcement must be automatic, not manual. |
| FR-09 | The system **shall** provide a reviewable access log of all audit log queries and exports, sufficient to demonstrate data access justifiability to regulators. | Required for legal compliance in applicable regions; region scoping to be confirmed. |

---

## 2. Non-Functional Requirements

| ID | Requirement | Target / Constraint |
|----|-------------|---------------------|
| NFR-01 | Search response time **shall** remain acceptable under peak month-end load. | Specific SLA (e.g., p99 < 2 s) to be defined during architecture; this requirement flags that month-end is the dimensioning scenario. |
| NFR-02 | Immutability of audit records **shall** be enforced at the product layer, independent of any database-level controls. | The product must not offer a path to mutation even for superusers. |
| NFR-03 | Role authorization for audit access **shall** require an explicit grant action; no user or service account may gain access implicitly. | |
| NFR-04 | The 7-year retention policy **shall** be enforced automatically without requiring operational intervention per record or per period. | |
| NFR-05 | Export traceability records (FR-05) **shall** themselves be retained and searchable for the same 7-year period. | |
| NFR-06 | The audit log ingestion path **shall** not be a blocking dependency for financial action throughput. | I.e., a slowdown or outage in audit log write must degrade gracefully, not halt transactions. Acceptable degradation behavior to be agreed with Compliance. |

---

## 3. Priorities

Using **MoSCoW** for v1 scope:

| Priority | Requirements |
|----------|-------------|
| **Must Have** | FR-01, FR-02, FR-03, FR-06, FR-07, FR-08 — core compliance, security gate, and operational search. Without these, the platform cannot ship to regulated customers. |
| **Must Have** | FR-04 (CSV export) — explicitly requested by customers; a table-stakes B2B expectation. |
| **Must Have** | FR-05 (export audit trail) — required by Compliance; cannot treat exports as untracked. |
| **Must Have** | NFR-02, NFR-03, NFR-04 — non-negotiable security and compliance properties. |
| **Should Have** | FR-09 (access justifiability log) — required in some regions; include in v1 if target regions are known; defer only if region set is confirmed to not require it at launch. |
| **Should Have** | NFR-01 (search performance SLA) — must be designed for from the start even if the exact number is TBD. |
| **Should Have** | NFR-06 (non-blocking ingestion) — operationally important; define degradation policy before launch. |
| **Won't Have (v1)** | Real-time alerting on audit events, anomaly detection, multi-format export (beyond CSV), self-service role management by customers. |

---

## 4. Source Traceability

| Stakeholder Note | Derived Requirements |
|-----------------|---------------------|
| "Audit records for financial actions must be retained for 7 years." (Compliance) | FR-01, FR-08, NFR-04 |
| "Only explicitly authorized roles may search or export audit logs." (Security) | FR-06, FR-07, NFR-03 |
| "Support engineers need fast search by account, actor, date range, and action type." (Operations) | FR-02, FR-03, NFR-01 |
| "Customers want to export filtered audit logs as CSV." (Product) | FR-04 |
| "Exported data must be traceable to who exported it and when." (Compliance) | FR-05, NFR-05 |
| "Audit records must not be editable or deletable through the product." (Security) | FR-06, NFR-02 |
| "Month-end load is heavy; search must remain responsive." (Platform) | NFR-01, NFR-06 |
| "Some regions require data access to be justifiable and reviewable." (Legal) | FR-09 |

---

## 5. Explicit Non-Goals (v1)

These are **out of scope** for the first release. Stating them prevents scope creep during architecture and development.

| Non-Goal | Rationale |
|----------|-----------|
| Storage engine selection or schema design | Explicitly deferred to architecture; no stakeholder note drives a storage constraint. |
| Real-time alerting or anomaly detection on audit events | Not requested; adds significant complexity; belongs in a security monitoring capability. |
| Customer self-service role management for audit access | Role grants are admin-controlled; customer-facing RBAC UI is a separate product surface. |
| Export formats beyond CSV | CSV is the stated requirement; additional formats (JSON, PDF) are future candidates. |
| Audit of non-financial actions (e.g., UI navigation, preferences changes) | Scope is financial actions; broadening is a separate decision requiring Compliance sign-off. |
| Automated data purge or anonymization after 7 years | Retention floor is defined; purge policy requires Legal input and is a follow-on requirement. |
| Multi-region data residency enforcement | Regional access justifiability (FR-09) is in scope; where data physically lives is an infrastructure concern outside this requirement set. |

---

`★ Insight ─────────────────────────────────────`
**Three things worth flagging before architecture starts:**

1. **FR-06 vs. NFR-06 tension**: Compliance wants every financial action audited, but Platform says audit writes can't block transactions. These goals are compatible only if the team agrees on an explicit degradation policy (e.g., async write with a dead-letter queue). Getting that policy signed off by Compliance before architecture is lower-cost than retrofitting it.

2. **FR-09 scope ambiguity**: "Some regions" is doing a lot of work. The team needs a target-region list before v1 ships — this requirement either needs to be Must Have (if regulated regions are in the launch set) or explicitly deferred with a named condition.

3. **Export traceability (FR-05) is a recursive requirement**: The export log is itself audit data, subject to FR-08 retention. If the team forgets this, they ship a compliance gap on day one.
`─────────────────────────────────────────────────`
