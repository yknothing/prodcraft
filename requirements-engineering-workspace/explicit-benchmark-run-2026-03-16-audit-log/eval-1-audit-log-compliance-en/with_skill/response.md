## Audit Log — First-Release Requirements

**Assumptions:** "Financial actions" includes create/update/approve/reject/transfer/payment events. "Customers" and "support engineers" are distinct authorized roles. Regional data-access justification (Legal note) applies at export time, not routine search, pending legal clarification.

---

### Functional Requirements

| ID | Statement | Priority | Source |
|----|-----------|----------|--------|
| FR-01 | The system shall capture an immutable audit record for every financial action (create, update, approve, reject, transfer, payment) at the moment the action is committed, so that a complete, tamper-evident history exists for compliance review. | P0 | Compliance, Security |
| FR-02 | The system shall prevent modification or deletion of any audit record through any product interface or API after the record has been written, so that audit integrity cannot be subverted from within the product. | P0 | Security |
| FR-03 | The system shall retain all audit records for a minimum of 7 calendar years from the date of the recorded event, after which records may be purged according to a defined retention policy. | P0 | Compliance |
| FR-04 | The system shall enforce role-based access control such that only users assigned an explicitly authorized audit role may search or export audit logs; all other roles shall receive no access. | P0 | Security |
| FR-05 | The system shall allow authorized users to search audit records by any combination of: account identifier, actor (user or system identity), date range, and action type, so that support engineers can investigate incidents efficiently. | P1 | Operations |
| FR-06 | The system shall allow authorized customers to export a filtered subset of audit records as a downloadable CSV file, so that customers can perform offline analysis and record-keeping. | P1 | Product |
| FR-07 | The system shall create a meta-audit record for every export operation, capturing at minimum: the exporting actor's identity, the filter parameters applied, the record count, and the timestamp, so that exported data is fully traceable to its origin. | P1 | Compliance |
| FR-08 | The system shall, for users in regions subject to data-access review obligations, prompt for and record a stated justification reason before granting access to audit log search or export, so that regulators can review access decisions. | P2 | Legal |

---

### Non-Functional Requirements

| ID | Statement | Priority | Source |
|----|-----------|----------|--------|
| NFR-01 | Audit log search shall return the first page of results in ≤ 3 s at the p95 under normal operating load, so that support engineers are not blocked during routine investigations. | P1 | Operations |
| NFR-02 | Audit log search shall return the first page of results in ≤ 10 s at the p95 during peak month-end load, ensuring the service degrades gracefully rather than becoming unavailable. | P1 | Platform |
| NFR-03 | Audit record capture shall add no more than 50 ms of synchronous latency to the originating financial transaction at the p99, so that audit instrumentation does not impede core transaction throughput. | P1 | Platform |
| NFR-04 | The system shall ensure zero data loss (RPO = 0) for audit records; a financial action is not considered complete until its audit record is durably committed. | P0 | Compliance, Security |
| NFR-05 | The audit log service shall achieve ≥ 99.5 % availability measured monthly, excluding pre-announced maintenance windows. | P1 | Operations |
| NFR-06 | The system shall provide a mechanism to verify that a stored audit record has not been altered since it was written, so that integrity can be confirmed during compliance audits. | P1 | Security, Compliance |
| NFR-07 | All audit data at rest and in transit shall be encrypted using algorithms meeting the platform's current security standard (minimum AES-256 at rest, TLS 1.2+ in transit). | P0 | Security |
| NFR-08 | The system shall support a minimum of 10 years of audit data volume without requiring architectural changes, even if the 7-year retention policy is later extended by regulation. | P2 | Compliance |

---

### Priority Summary

| Priority | Rationale |
|----------|-----------|
| **P0** | Compliance blockers and security invariants. Release is not legal without these. |
| **P1** | Core operational and customer value; workarounds are unacceptable at launch. |
| **P2** | Significant value but can follow in a fast-follow release; no immediate regulatory trigger. |
| **P3 (Non-Goals — see below)** | Explicitly deferred. |

---

### Non-Goals (First Release)

These are explicitly out of scope to prevent scope creep; each should be re-evaluated for future releases.

| Non-Goal | Reason for Deferral |
|----------|---------------------|
| Real-time alerting or anomaly detection on audit events | SIEM integration is a separate security capability not requested for v1. |
| Automated compliance report generation | Requires regulatory template work outside this team's scope. |
| Audit coverage of non-financial system events (logins, config changes, etc.) | Not requested; mixed with financial audit could dilute search quality. |
| Self-service role management for audit access | Access grant/revoke is an identity platform concern, not audit log. |
| Storage tiering, archival strategy, or purge automation | Infrastructure decisions belong to architecture phase. |
| UI/UX design for the audit viewer | UX spec follows approved requirements; not a requirements-layer deliverable. |
| Multi-format export (PDF, JSON, XLSX) | CSV covers the stated need; additional formats deferred until demand is validated. |

---

### Open Questions (Must Resolve Before Architecture Kickoff)

1. **FR-08 scope** — Does data-access justification apply to every search query, or only to exports? Requiring it per-search adds friction for support engineers (tension with FR-05/NFR-01). Legal must clarify.
2. **FR-02 boundary** — "Not editable through the product" — does this permit direct database correction by a DBA under a documented break-glass procedure, or must immutability be enforced at the storage layer unconditionally? This shapes the integrity mechanism required by NFR-06.
3. **FR-06 customer scope** — Do all customers get audit export, or only those on specific plan tiers? Product must confirm before role definitions are finalized.
4. **NFR-03 latency budget** — 50 ms is assumed; the platform team must validate this against existing transaction p99 baselines.

---

`★ Insight ─────────────────────────────────────`
- **Immutability as a requirement vs. a solution:** FR-02 deliberately says "through any product interface" rather than "use an append-only store." That preserves the architecture team's freedom to choose the enforcement mechanism (write-once storage, hash chaining, WORM policy) while still being testable.
- **The meta-audit (FR-07) is its own audit event:** This is a common omission — teams build export but forget to audit the export itself, which is exactly what compliance audits inspect first.
- **NFR-04 (RPO = 0) has an implicit two-phase commit requirement:** Saying a transaction isn't complete until its audit record is durable is a significant constraint that will surface in architecture. Flagging it now avoids a late-stage surprise.
`─────────────────────────────────────────────────`
