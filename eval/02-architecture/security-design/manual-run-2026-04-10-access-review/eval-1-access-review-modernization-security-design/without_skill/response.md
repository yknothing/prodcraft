`★ Insight ─────────────────────────────────────`
Brownfield threat models have a distinct risk profile from greenfield ones: the coexistence period is often the highest-risk window. Two systems can disagree on state while both are nominally authoritative, creating a "conflicting truth" problem that adversaries — or just bugs — can exploit to manufacture a compliant-looking audit trail from inconsistent data.
`─────────────────────────────────────────────────`

---

## Threat Model: Access Review Modernization — Release 1

**Scope:** Release 1 brownfield slice only. Legacy module is in-scope as a trust-boundary participant. Post-cutover architecture is out of scope.

---

### 1. High-Value Assets

| Asset | Sensitivity | Why It Matters |
|---|---|---|
| Evidence packages | Compliance-critical | Submitted to auditors; tampering or unauthorized access is a regulatory event |
| Audit event log | Compliance-critical | Forms the legal record of access decisions; must be tamper-evident and complete |
| Tenant hierarchy rules | Contractual confidentiality | Cross-tenant leakage is a contract breach, not merely a bug |
| Access review decisions (approve/revoke) | Integrity-critical | An incorrect or forged decision directly affects who holds privileged access |
| Campaign state | Coordination integrity | Drives downstream provisioning; inconsistency between legacy and modern stores is exploitable |
| Reassignment records | Authorization-critical | Controls who may act as a reviewer; escalation path if unvalidated |

---

### 2. Trust Boundaries

```
[ Admin / Auditor / Reviewer ]
         │
         ▼  (TBoundary A — public API surface)
[ Modern Access Review Experience ]
         │
         ▼  (TBoundary B — internal service mesh)
[ Review Coordination Service ]
    │         │          │
    ▼         ▼          ▼
[Reviewer  [Evidence  [Legacy
 Policy     Package    Coexistence
 Compat.    Service]   Adapter]
 Layer]        │          │
               ▼          ▼  (TBoundary C — legacy system)
        [Audit Integrity  [Legacy Module]
           Store]
```

**TBoundary A** — Internet-facing. Caller identity and role must be established and verified here; downstream services must not re-trust caller-supplied claims.

**TBoundary B** — Internal service-to-service. Lateral movement risk if services do not assert mutual identity; a compromised coordination service can pollute the audit store.

**TBoundary C** — Legacy system. Unknown security posture. The adapter is the only sanctioned crossing point; this boundary must be treated as untrusted-inbound.

**Implicit cross-cutting boundary: tenant** — Every request carries a tenant context. Any query that doesn't enforce it collapses all tenants into one effective security domain.

---

### 3. Abuse Paths

#### AP-1 · Cross-Tenant Campaign Data Leakage
**Entry:** `GET /v1/campaigns` or `GET /v1/campaigns/{campaignId}`
**Path:** Admin for Tenant A supplies a valid token but the server-side query omits a tenant filter, returning campaigns — and their reviewer lists and decision states — belonging to Tenant B.
**Impact:** Tenant hierarchy rule leakage; contractual breach.
**Amplifier:** Sequential or low-entropy campaign IDs make enumeration trivial without even needing a list endpoint.

#### AP-2 · Evidence Package Oversharing
**Entry:** `GET /v1/campaigns/{campaignId}/evidence-package`
**Path:** A caller with Reviewer role (or a confused-deputy internal service) fetches an evidence package that should be gated to Auditor/Admin roles per the release-1 visibility rules.
**Impact:** Premature or unauthorized disclosure of compliance-sensitive access decisions to a party who can influence or contest them.

#### AP-3 · Legacy Bypass — Decision Outside the Auditable Flow
**Entry:** Legacy Coexistence Adapter or direct legacy module endpoint
**Path:** A misconfigured service, a compromised internal caller, or an insider routes a review action through the legacy path. The decision is persisted in the legacy store but never reaches the Audit Integrity Store, leaving a gap in the audit trail. The modern system sees no record of the decision.
**Impact:** Access is revoked or preserved without an immutable evidence record. Audit fails; regulatory exposure.
**Amplifier:** Sync semantics between new and legacy flows are explicitly unresolved — there is no authoritative reconciliation step to detect this.

#### AP-4 · Dual-Write Inconsistency as Manufactured Evidence
**Entry:** Simultaneous actions on legacy and modern paths during coexistence
**Path:** An attacker (or a race condition) submits a `review-action` through the modern path and a contradictory action through the legacy path within the same campaign window. Both are "committed." The auditor receives the modern evidence package, which reflects only one side. The actor later presents the legacy record as authoritative for a different decision.
**Impact:** Two valid-looking audit trails disagree on the access decision. The "correct" one is ambiguous; compliance defense is undermined.

#### AP-5 · Fail-Open on Unsupported Reassignment Variant
**Entry:** `POST /v1/campaigns/{campaignId}/reassignments`
**Path:** A client submits a reassignment variant that the system does not fully support. Instead of returning a structured unsupported-flow response, the service partially executes: it records the new reviewer assignment in the coordination store but does not update the policy compatibility layer. The new reviewer has assignment-level access without a properly validated policy check.
**Impact:** A reviewer is assigned to tasks they should not review — including potentially their own access — without triggering a policy violation.

#### AP-6 · Audit Event Injection from Compromised Internal Service
**Entry:** TBoundary B — service-to-service call to Audit Integrity Store
**Path:** A compromised Review Coordination Service (or a service impersonating it) writes fabricated audit events directly to the store, back-dating or falsifying review actions.
**Impact:** False compliance evidence. If the store is not append-only and the write interface is not identity-verified, events can be inserted, modified, or deleted.

#### AP-7 · Migration Command Exposure via Public API
**Entry:** `POST /v1/campaigns` or any resource endpoint
**Path:** An internal cutover or migration command is accidentally reachable on the public API surface (e.g., an undocumented parameter, a mis-scoped route, or a debug flag left in the response). An attacker triggers premature cutover, rollback, or state reset.
**Impact:** Campaign state corruption; loss of audit trail for in-progress reviews; possible SLA/audit-season impact.

#### AP-8 · Reminder Flooding (Operational DoS)
**Entry:** `POST /v1/campaigns/{campaignId}/reminders`
**Path:** An admin-role caller with no rate limit sends bulk reminder requests, flooding reviewers with notifications. During audit season, this can drown legitimate reminders and drive reviewers to ignore or mute all notifications, causing missed deadlines.
**Impact:** Audit-season deadline failures; reputational/compliance harm.

---

### 4. Controls

#### Tenant Isolation

| Control | Where | Rationale |
|---|---|---|
| Server-side tenant filter on every query — never trust a client-supplied tenant claim as the sole scoping mechanism | Review Coordination Service, Evidence Package Service | Eliminates AP-1; defense-in-depth against IDOR |
| Tenant claim validated and bound to the session at TBoundary A; propagated as a verified internal header, not a user-editable value | Modern Access Review Experience | Caller cannot self-elevate to another tenant |
| Datastore-level row security (or equivalent partition key enforcement) scoped to tenant | Audit Integrity Store, campaign store | Last-resort containment; survives application-layer bugs |

#### Evidence Integrity

| Control | Where | Rationale |
|---|---|---|
| Append-only write interface for the Audit Integrity Store — no `UPDATE` or `DELETE` permitted, enforced at the storage layer not just the application layer | Audit Integrity Store | Eliminates AP-6 modification; makes injected events detectable |
| Cryptographic hash of each evidence package stored at generation time; hash verified at fetch time | Evidence Package Service + Audit Integrity Store | Detects tampering between generation and delivery |
| WORM or equivalent immutability for evidence package blobs | Evidence Package Service storage | Prevents post-generation substitution |
| Access to `GET /evidence-package` and `GET /audit-events` logged as audit events themselves | Audit Integrity Store | Who accessed evidence is itself compliance-relevant |
| Evidence package access restricted to Auditor and Admin roles, enforced at TBoundary A | Modern Access Review Experience | Closes AP-2; roles verified against token claims, not request parameters |

#### Fail-Closed Unsupported-Flow Handling

| Control | Where | Rationale |
|---|---|---|
| Explicit allowlist of supported reassignment variants; anything outside returns HTTP 422 with a structured `unsupported-flow` body before any state mutation occurs | Review Coordination Service | Closes AP-5; no partial execution |
| Data-correction flows blocked at the API gateway (TBoundary A), not only at the service layer | Modern Access Review Experience | Defense-in-depth; service-layer bypass via internal caller is still caught |
| Unsupported-flow rejections emitted as audit events (even though no state changed) | Audit Integrity Store | Probes and reconnaissance become visible |

#### Legacy Coexistence

| Control | Where | Rationale |
|---|---|---|
| Designate a single canonical source of truth per campaign (modern store) for Release 1; legacy reads are allowed but legacy writes must route through the adapter, not directly | Legacy Coexistence Adapter | Eliminates AP-4 dual-write ambiguity; legacy store becomes a follower, not a peer |
| The adapter is the only sanctioned crossing point at TBoundary C; legacy module endpoints not reachable from inside the service mesh except via the adapter | Network/service mesh policy | Closes AP-3 direct-bypass path |
| Sync state exposed explicitly in API responses (`X-Sync-Status: eventual` or equivalent); callers must not infer immediate consistency | Review Coordination Service | Prevents application logic from treating unresolved sync as confirmed |
| Reconciliation job (or explicit gap-detection) that alerts when a legacy-path action has no corresponding modern-store record | Operational | Makes AP-3 and AP-4 incidents detectable rather than silent |
| Deprecation response headers on any legacy-proxied routes; no new features added through the adapter | Legacy Coexistence Adapter | Signals the boundary clearly; reduces surface area |

#### Authorization & Service Identity

| Control | Where | Rationale |
|---|---|---|
| RBAC with discrete roles: `CampaignAdmin`, `Reviewer`, `Auditor` (evidence/audit read-only), `InternalService` | TBoundary A + service layer | Least-privilege; Reviewers cannot manage campaigns or fetch evidence |
| Reviewers may only act on tasks assigned to them — scoped authorization enforced at the task level, not just the campaign level | Review Coordination Service | Prevents a reviewer from approving or revoking access outside their assignment |
| Reassignment requires `CampaignAdmin` role; the target reviewer must pass a policy-compatibility check before the reassignment is committed | Reviewer Policy Compatibility Layer | Closes AP-5 at the policy layer |
| Service-to-service calls across TBoundary B authenticated via mTLS or short-lived service identity tokens; no anonymous internal calls | Internal service mesh | Prevents a compromised service from impersonating another to write to the Audit Integrity Store |
| Migration-only and cutover-only commands excluded from public API routing table; enforced at gateway level | Modern Access Review Experience / API gateway | Closes AP-7 |
| Rate limit on `POST /reminders` per campaign per time window, enforced before any send logic | Modern Access Review Experience | Closes AP-8 |

---

### 5. Residual Risks Requiring Explicit Ownership

1. **Sync semantics are architecturally unresolved.** The reconciliation control above detects divergence but does not resolve it. Until a tie-breaking policy is defined (modern wins, latest-timestamp wins, human review required), a detected divergence has no automated remediation path. This must be an explicit decision before audit season.

2. **Reviewer Policy Compatibility Layer correctness.** Tenant hierarchy rules are contractual. If the layer produces a policy evaluation inconsistent with what the legacy system would have produced for the same tenant, decisions made under the new flow may be invalid by contract. This requires test coverage using real tenant configurations, not synthetic ones.

3. **Evidence package generation timing.** If a campaign is in-flight during coexistence and has decisions on both the legacy and modern paths, the evidence package may be incomplete by construction. The visibility rules for Release 1 need to state whether a mixed-path campaign can produce a complete evidence package or whether it is explicitly unsupported.

---

`★ Insight ─────────────────────────────────────`
The three residual risks above are not implementation gaps — they are specification gaps. Threat models for coexistence periods are most useful when they force these ambiguities into the open before the audit window, not after. The sync tie-breaking policy and the mixed-path campaign evidence rule are the two decisions most likely to become an incident if left implicit.
`─────────────────────────────────────────────────`
