Writing directly to the working directory:

```markdown
[threat-model.md]
```

I'll write it now using the Write tool (which is Read's write counterpart — actually I have `Read` and I need to check if `Write` or `Edit` are available to me).

Looking at my available tools, I have `Read` for reading files. For creating files I need to use the Write tool. Let me check if it's available... it's listed in the system instructions as available. Let me use it.

Actually looking at the tools I have listed, I see `Read` but not a standalone `Write` tool in the explicit tool list. The instructions say "To create files use Write instead of cat with heredoc" — but I don't see it explicitly listed. The tools I do see for file operations are: `Read`, `LSP`. For browser I have playwright/chrome-devtools tools.

Let me use the `mcp__playwright__browser_evaluate` or another available method. Actually — looking more carefully, I should just output the threat model inline as my response since I don't have a Write tool available in this session. The user can save it themselves.

Let me produce the complete artifact inline:

---

# Threat Model — Access Review Modernization, Release 1

**Status:** Draft — Release 1 pre-implementation
**Scope:** Brownfield modernization slice: new service layer coexisting with legacy module during audit season.

---

## 1. High-Value Assets

| Asset | Sensitivity | Canonical Location |
|---|---|---|
| Evidence packages | Compliance-critical, regulatory artifact | Evidence Package Service → Audit Integrity Store |
| Audit event history | Immutable compliance record | Audit Integrity Store |
| Tenant hierarchy rules | Contractual — cross-tenant exposure is a breach | Reviewer Policy Compatibility Layer |
| Review action decisions | Access governance record (who approved what) | Review Coordination Service |
| Reviewer assignments | PII + access scope | Review Coordination Service |
| Sync state between legacy and new | Correctness-critical; inconsistency = wrong access decision | Legacy Coexistence Adapter boundary |
| Migration / cutover commands | Privileged internal operations | Internal only — must not appear on public API surface |

---

## 2. Trust Boundaries

```
TB-1  External client (browser/API consumer)
        ↕  TLS + bearer token
      Admin REST API  ──────────────────────────────────────────────────
        ↕  signed tenant header                                         |
TB-2  Review Coordination Service                                        |
        ├── ↕  tenant-scoped service call          TB-3                  |
        │   Reviewer Policy Compatibility Layer                           |
        │                                                                 |
        ├── ↕  re-authorized service call          TB-4                  |
        │   Evidence Package Service                                      |
        │         ↕  append-only write              TB-6                 |
        │         Audit Integrity Store ← (INSERT only; no UPDATE/DELETE)|
        │                                                                 |
        └── ↕  adapter call (legacy boundary)      TB-5                  |
            Legacy Coexistence Adapter                                    |
                ↕  service-to-service (never raw user credential)         |
            Legacy Module ────────────────────────────────────────────────

TB-7  Role boundary: Admin ≠ Auditor — enforced within authenticated session
```

**Boundary descriptions:**

| ID | From → To | Risk level |
|---|---|---|
| TB-1 | External client → Admin REST API | High — fully untrusted caller |
| TB-2 | Admin REST API → Review Coordination Service | Medium — tenant identity must be injected here, not downstream |
| TB-3 | Review Coordination Service → Reviewer Policy Compatibility Layer | Medium — cross-tenant leak risk in cache/query |
| TB-4 | Review Coordination Service → Evidence Package Service | High — compliance data; re-authZ required here, not trusted from caller |
| TB-5 | Review Coordination Service → Legacy Coexistence Adapter | **Highest** — legacy auth model parity unvalidated; sync undefined |
| TB-6 | Evidence Package Service → Audit Integrity Store | High — integrity must be infrastructure-enforced, not app-layer only |
| TB-7 | Admin role ↔ Auditor role | Medium — visibility rules underspecified for Release 1 |

---

## 3. Abuse Paths

### AP-1 · Cross-Tenant Campaign Access
**Boundaries:** TB-1, TB-2
An authenticated admin substitutes a `campaignId` owned by another tenant. If tenant identity is resolved from the URL or request body rather than from the bearer token, the check can be bypassed.
**Impact:** Tenant hierarchy leakage, contractual breach, compliance finding.

### AP-2 · Evidence Package Exfiltration
**Boundaries:** TB-2, TB-4, TB-7
An under-privileged role (reviewer, or a misconfigured auditor) calls `GET /v1/campaigns/{campaignId}/evidence-package` before the audit period permits access. If Evidence Package Service trusts the caller's role assertion rather than re-verifying, this check can be bypassed.
**Impact:** Premature disclosure of a regulatory artifact.

### AP-3 · Review Action Replay
**Boundary:** TB-1
A `POST /v1/campaigns/{campaignId}/review-actions` request is replayed (network retry, credential replay, or deliberate submission) after the action is already committed.
**Impact:** Duplicate audit event; potential corruption of the access decision record; second write to the Audit Integrity Store with conflicting state.

### AP-4 · Legacy Path as Auth-Weaker Bypass
**Boundary:** TB-5
During coexistence, the legacy module's endpoints remain reachable. If legacy auth checks are weaker than the new model, an actor can route a review action through the legacy path to bypass the Reviewer Policy Compatibility Layer.
**Impact:** Access decision committed without passing new policy checks; no entry in new audit trail.

### AP-5 · Sync Ambiguity Exploitation
**Boundary:** TB-5
An actor writes through the new API path and reads through the legacy path (or vice versa) during the window where sync semantics are unresolved. Both paths may hold different state simultaneously.
**Impact:** Reviewer sees and acts on stale approval state; wrong access decision persisted.

### AP-6 · Unsupported Flow Silent Commit
**Boundaries:** TB-2, TB-5
A `POST /v1/campaigns/{campaignId}/reassignments` request carries an unsupported variant. Without a pre-adapter guard, the request falls through to the Legacy Coexistence Adapter with undefined behavior — partial write, silent success, or inconsistent audit event.
**Impact:** Partial state written to Audit Integrity Store; review state corrupted without a clear error record.

### AP-7 · Migration Command Exposure
**Boundary:** TB-1
Internal migration-only or cutover-only commands are reachable on the public API surface (not removed from routing, merely undocumented). An authenticated admin (or an attacker with a valid token) triggers a partial cutover.
**Impact:** Review state corruption; premature or incomplete legacy decommission during audit season.

### AP-8 · Audit Log Tampering or Omission
**Boundary:** TB-6
A service credential with UPDATE or DELETE access to the Audit Integrity Store overwrites or deletes an event — deliberately (compromised service) or accidentally (schema migration gone wrong).
**Impact:** Compliance artifact invalid; audit trail gap is a direct regulatory finding.

### AP-9 · Tenant Hierarchy Leak via Compatibility Layer
**Boundary:** TB-3
The Reviewer Policy Compatibility Layer resolves a policy query without scoping it to the requesting tenant. A shared cache with a key collision, or a missing tenant predicate in the query, returns hierarchy metadata belonging to another tenant.
**Impact:** Contractual breach; confidential org structure disclosed.

### AP-10 · Auditor Over-Privilege
**Boundary:** TB-7
Evidence visibility rules for Release 1 are underspecified. An implementation that defaults to "all authenticated auditors see all campaigns" (the safe-for-developers but insecure shortcut) allows cross-tenant or out-of-scope evidence access.
**Impact:** Unauthorized compliance data access.

### AP-11 · Oversized or Malicious Review-Action Payload
**Boundary:** TB-1
A large or structured-injection payload submitted to `POST /v1/campaigns/{campaignId}/review-actions`. If reviewer notes or justification fields are forwarded into downstream processing or logging without size limits or sanitization, this enables storage exhaustion or injection.
**Impact:** Storage abuse; downstream injection if note content is processed or rendered.

### AP-12 · Reminder Endpoint Spam
**Boundary:** TB-1
`POST /v1/campaigns/{campaignId}/reminders` called repeatedly by an authorized admin.
**Impact:** Reviewer notification spam; system notification load; potential external-service rate-limit breach if notifications are dispatched externally.

---

## 4. Required Controls per Boundary

### TB-1 — External Client → Admin REST API

| Control | Requirement |
|---|---|
| Authentication | Bearer token required on all endpoints. Tokens must be short-lived (≤1 hour). |
| Tenant identity | Tenant resolved from token claims only — never from URL segment, query param, or request body. |
| Input validation | Max payload size enforced at gateway (recommend 64 KB for action payloads). All request fields schema-validated before routing. |
| Route filtering | Migration-only and cutover-only routes must be absent from the public routing table — not merely undocumented or access-controlled. |
| Rate limiting | `POST reminders`: per-campaign per-caller rate limit (e.g., 5/hour). `POST review-actions`: idempotency key required; duplicate within key window returns original result. |

### TB-2 — Admin REST API → Review Coordination Service

| Control | Requirement |
|---|---|
| Tenant propagation | API layer injects tenant ID as a signed internal header. Services reject any request missing a valid tenant header. |
| Idempotency | `review-actions` endpoint enforces idempotency key. Duplicate detected = return original result, no second write. |
| Unsupported-flow guard | Reassignment and data-correction variants are checked against the Release-1 supported set **before** any adapter call. Non-matching variants return structured `422` immediately (see §6). |
| Authorization | Role verified on every request at this boundary; reject if role cannot be resolved from token. |

### TB-3 — Review Coordination Service → Reviewer Policy Compatibility Layer

| Control | Requirement |
|---|---|
| Tenant-scoped queries | Every policy resolution call must include tenant ID as a mandatory parameter. The compatibility layer must reject calls that omit it. |
| Cache key isolation | Any in-process or shared cache of policy results must include tenant ID in the key. Shared caches without explicit per-tenant namespacing are forbidden. |
| Output validation | Responses from the compatibility layer must be validated to contain only the requesting tenant's data before use. |

### TB-4 — Review Coordination Service → Evidence Package Service

| Control | Requirement |
|---|---|
| Re-authorization | Evidence Package Service independently verifies role and tenant scope from the signed internal header — it does not trust the caller's assertion. |
| Visibility rule enforcement | Release-1 evidence visibility rules must be written, reviewed, and tested before ship; "allow all authenticated" is not an acceptable interim state. |
| Read-only assembly | Evidence package compilation must not write to or mutate audit event records. |

### TB-5 — Review Coordination Service → Legacy Coexistence Adapter

| Control | Requirement |
|---|---|
| Auth parity | Requests forwarded through the adapter must have passed the same authN/authZ checks as the new path. The adapter issues a service-to-service call only; raw user credentials are never forwarded to the legacy system. |
| Sync state labeling | All responses that may reflect legacy state must carry an explicit consistency label: `"consistency": "eventual"` or `"consistency": "unresolved"`. Callers must not assume immediate consistency. |
| Unsupported flow hard stop | Adapter refuses to forward any unsupported reassignment or data-correction flow. Hard stop — not log-and-continue. If the pre-adapter guard in TB-2 has already fired, this is a defense-in-depth stop. |
| Legacy endpoint exposure | Legacy module endpoints must not be reachable by external callers during coexistence unless they have been independently hardened to the new auth standard. |

### TB-6 — Evidence Package Service → Audit Integrity Store

| Control | Requirement |
|---|---|
| Append-only grants | Service accounts for Evidence Package Service and Review Coordination Service have INSERT-only access. No UPDATE, DELETE, or DDL grants. Enforced at the storage layer, not only in application code. |
| Write integrity | Every event write must include: event timestamp, actor identity, tenant ID, content hash. The store must reject writes missing any field. |
| Separation of duties | No service that creates review actions may also read-modify-write audit events. |
| Store isolation | Audit Integrity Store is not accessible from the Legacy Coexistence Adapter directly; legacy audit events are written through the Evidence Package Service as the single assembly point. |

### TB-7 — Role Boundary (Admin vs Auditor)

| Role | Permitted endpoints | Denied |
|---|---|---|
| Admin | All endpoints in the API contract | Evidence-package access for campaigns outside their tenant scope |
| Auditor | `GET evidence-package`, `GET audit-events` — scoped to authorized campaigns only | `POST campaigns`, `POST review-actions`, `POST reminders`, `POST reassignments` |
| Reviewer | None (not a caller of these REST resources) | All |

Cross-role access is rejected at the API gateway, not delegated to downstream services.

---

## 5. Legacy Coexistence Controls

The coexistence period is the highest aggregate risk surface in Release 1. These controls apply for the entire duration of parallel operation:

| Risk | Required control |
|---|---|
| Legacy path bypasses new authZ | Adapter enforces new authN/authZ before forwarding. Legacy system receives only service-to-service calls. |
| Dual-write creates inconsistent access decisions | Designate a single authoritative write path (new service). Legacy state is updated asynchronously. Legacy is read-only fallback, not a parallel write target. |
| Sync semantics unresolved | No component asserts `"consistent"` until the sync protocol is specified and tested. All responses from or touching the legacy path carry explicit consistency labels. |
| Evidence from both paths must appear in one record | Evidence Package Service is the sole assembly point. It must ingest both legacy and new audit events. Deduplication keyed on event ID, not timestamp. |
| Legacy endpoints directly reachable | If legacy endpoints cannot be taken offline, they must sit behind the same auth boundary as the new API (e.g., same API gateway, same token validation). |

---

## 6. Fail-Closed Policy — Unsupported Flows

All unsupported reassignment and data-correction flow variants must fail before any state mutation occurs. The guard lives at TB-2 (pre-adapter), with a defense-in-depth stop at TB-5 (adapter).

**Response contract (required shape):**

```json
HTTP 422 Unprocessable Entity

{
  "error": "unsupported_flow",
  "variant": "<caller-provided variant identifier, echoed back>",
  "action_required": "none — no state was modified"
}
```

**Decision needed — see §8.1 below:** Whether to include `"supported_variants"` in this response.

**Guarantees that must hold:**
- No audit event is written
- No write reaches the Legacy Coexistence Adapter
- No partial state is created
- The 422 is returned regardless of which service receives the request first

The pass condition is explicit: a flow must appear on the Release-1 supported list. "Not explicitly unsupported" is not a pass.

---

## 7. Attacker Assumptions

These are the conditions the controls are designed against:

1. **Insider with valid token.** A malicious or compromised admin can obtain a valid bearer token. Controls cannot assume token possession implies good intent — tenant scoping, re-authZ at TB-4, and append-only at TB-6 all exist because of this assumption.

2. **campaignId enumeration.** If campaign IDs follow a predictable pattern (sequential integers, timestamp-prefixed), an authenticated actor from one tenant can probe other tenants' campaign IDs. Tenant ownership check at TB-2 is the primary defense; opaque UUIDs reduce the attack surface.

3. **Legacy endpoint direct access.** During coexistence, an attacker who knows legacy endpoint paths (from documentation, prior access, or enumeration) may attempt to route through legacy to bypass new controls.

4. **Policy compatibility layer as high-value target.** Compromise of the compatibility layer credential yields cross-tenant hierarchy data for all tenants. It should be treated as a high-sensitivity service with strict network egress controls.

5. **Audit store is not confidential by default.** An insider with DB read access can read audit events. Integrity controls (content hash, append-only) are more durable than access controls alone; both are required.

6. **Sync ambiguity is observable.** An authorized user who knows sync is unresolved can probe both paths and act on the more favorable state. Explicit consistency labeling limits this surface but does not eliminate it until sync is resolved.

---

## 8. Residual Risks and Unresolved Items

| ID | Risk | Disposition | Owner |
|---|---|---|---|
| RR-1 | Sync protocol between new and legacy paths is unresolved | **Ship-blocker if any write path is ambiguous at audit season start.** Explicit consistency labeling is a mitigation, not a resolution. | Architecture |
| RR-2 | Evidence visibility rules for auditors are underspecified for Release 1 | **Ship-blocker.** Interim "allow all authenticated" is not acceptable. | Product + Security |
| RR-3 | campaignId format not specified — may be guessable | Design choice not yet confirmed. Recommend opaque UUID. | Architecture |
| RR-4 | Legacy auth model parity with new authZ not yet validated | Must be validated and documented before coexistence goes live. | Security Engineering |
| RR-5 | Audit Integrity Store access grants not yet defined | Must be confirmed before Evidence Package Service deploys. Append-only enforcement must be at storage layer. | Infra + Security Engineering |
| RR-6 | Migration/cutover command surface not yet audited | Routing table review required before Release 1 deployment. | Engineering |

---

### 8.1 Open Decision: Unsupported-Flow Response Shape

**Context:** The fail-closed 422 response (§6) currently does not include a `supported_variants` array.

**Trade-off to decide:**

| Option | Developer experience | Security posture |
|---|---|---|
| Include `"supported_variants": [...]` | Integrators immediately know what's available; faster remediation | Gives attackers a complete map of supported flows — reduces enumeration cost |
| Omit `"supported_variants"` | Integrators must consult documentation | Reduces information exposed in error responses; consistent with security-conservative API design |
| Include in internal/staging, omit in production | Good DX in safe environments | Requires environment-aware response logic |

**Your input shapes this:** In `ReviewActionHandler` (or equivalent), the unsupported-flow guard will construct this response. The list of supported variants is small and Release-1-specific.

**Guidance:** If the supported variant list is in documentation and unlikely to change mid-release, omitting it from the 422 body is the more conservative choice — callers should consult the contract, not the error response. If integrators are expected to handle variant selection dynamically at runtime, inclusion is justified. Consider also whether the variant identifier echoed back (`"variant": "<caller-provided>"`) should be validated and sanitized before echo to prevent reflected-content issues.

---

## Quality Gate Checklist

- [x] Trust boundaries are explicit — 7 boundaries enumerated with risk levels
- [x] High-value assets documented — 7 assets with sensitivity and location
- [x] Abuse paths documented — 12 paths with boundary, mechanism, and impact
- [x] Required controls assigned per boundary — TB-1 through TB-7
- [x] Legacy coexistence risks and controls explicit
- [x] Fail-closed policy for unsupported flows defined
- [x] Logging and integrity expectations clear (TB-6, append-only, content hash)
- [x] Residual risks and unresolved assumptions recorded — RR-1 through RR-6, with ship-blocker flags

---

`★ Insight ─────────────────────────────────────`
**Two items are ship-blockers, not just risks to monitor.** RR-1 (unresolved sync protocol) and RR-2 (underspecified auditor evidence visibility rules) can't be deferred. If sync is ambiguous when audit season begins, both paths can simultaneously hold conflicting state — and there's no authoritative source to reconstruct the correct access decision. Evidence visibility rules that are left vague will be implemented permissively by default (it's the path of least resistance for developers), which is the exact wrong default for compliance-gated data.
`─────────────────────────────────────────────────`

---

**What to do next with this artifact:**

1. **RR-1 and RR-2** — resolve before implementation begins; both are pre-conditions for any code that touches the legacy boundary or the evidence-package endpoint.
2. **§8.1 decision** — fill in the unsupported-flow response shape so the guard implementation has a concrete spec.
3. **Security review** — walk TB-5 (legacy coexistence adapter) with the team that owns the legacy module; auth parity (RR-4) is the highest implementation risk.
4. **Infra confirmation** — confirm append-only storage grants for Audit Integrity Store (RR-5) before Evidence Package Service is deployed to any shared environment.
