`★ Insight ─────────────────────────────────────`
This is a brownfield schema design where the hardest constraints are compliance (7-year tamper-evident retention), coexistence (legacy module stays live during R1), and ownership clarity across 6 containers. The key risk is blurring `LegacyCampaignReference` into a canonical record — the domain model explicitly flags this as a failure mode to avoid.
`─────────────────────────────────────────────────`

Now I'll produce the artifact.

---

# Data Schema: Access Review Modernization — Release 1

## Overview

This document defines the persistence model, ownership rules, lifecycle boundaries, and migration-safety notes for the Release 1 modernization slice. It is scoped to the schema and lifecycle layer only; API design and service implementation are out of scope.

The schema must satisfy four simultaneous constraints:
- **Brownfield coexistence**: the legacy access-review module remains in service; the modern schema must not corrupt or replace its canonical records during R1.
- **Compliance integrity**: evidence and audit data carry 7-year retention and tamper-evident requirements that are stronger than normal workflow data.
- **Tenant compatibility**: reviewer hierarchy and exception rules vary by tenant and must be isolated from campaign state.
- **Change safety**: the schema must tolerate future field additions, replay, and partial migration without unsafe backfills or downtime.

---

## Ownership Map

| Entity | Canonical Owner | May Read / Project | Notes |
|---|---|---|---|
| `AccessReviewCampaign` | Review Coordination Service | Modern Experience (read), Legacy Adapter (read-only via bridge) | Write authority is the Coordination Service alone |
| `ReviewTask` | Review Coordination Service | Modern Experience (read) | |
| `ReviewerAssignment` | Review Coordination Service | Policy Compatibility Layer (validates), Modern Experience (read) | Policy Layer validates; does not own the assignment record |
| `ReviewDecision` | Review Coordination Service | Audit Integrity Store (archives immutable copy) | Decision record is mutable during review window; archived copy is not |
| `EvidencePackage` | Evidence Package Service | Modern Experience (download), Audit Integrity Store (reference) | Immutable once sealed |
| `AuditRecord` | Audit Integrity Store | Evidence Package Service (embeds reference) | Append-only; no component may update or delete |
| `TenantPolicyProfile` | Reviewer Policy Compatibility Layer | Review Coordination Service (reads for validation) | Separate from campaign state; version-stamped |
| `LegacyCampaignReference` | Legacy Coexistence Adapter | Review Coordination Service (reads bridge data) | **Compatibility-only.** Must never be promoted to canonical campaign state |

---

## Schema Definitions

### 1. `access_review_campaigns` — Review Coordination Service

Canonical record for a review campaign created in the modern system.

```
access_review_campaigns
  id                  UUID           PK, generated on creation
  tenant_id           UUID           NOT NULL, FK to tenant registry (external)
  title               TEXT           NOT NULL
  scope_descriptor    JSONB          Opaque scope blob; structure governed by tenant
  status              TEXT           NOT NULL  -- ENUM: draft | active | closed | archived
  created_at          TIMESTAMPTZ    NOT NULL
  activated_at        TIMESTAMPTZ    NULLABLE  -- set when status transitions to active
  closed_at           TIMESTAMPTZ    NULLABLE  -- set when status transitions to closed
  created_by          UUID           NOT NULL  -- identity of the initiating user
  policy_profile_id   UUID           NOT NULL, FK → tenant_policy_profiles.id
  legacy_ref_id       UUID           NULLABLE, FK → legacy_campaign_references.id
                                       -- populated only when bridging a legacy campaign
  schema_version      INTEGER        NOT NULL DEFAULT 1
```

**Uniqueness**: `(tenant_id, title, activated_at)` — enforces no duplicate active campaigns per tenant per activation window.

**Authoritative fields**: all fields. `legacy_ref_id` is a cross-boundary reference pointer, not a data copy.

**Derived / projected**: the Modern Experience may cache `title`, `status`, and `scope_descriptor` for display — these projections must not be treated as authoritative and must be refreshed on campaign update events.

---

### 2. `review_tasks` — Review Coordination Service

One task per reviewable item within a campaign.

```
review_tasks
  id              UUID           PK
  campaign_id     UUID           NOT NULL, FK → access_review_campaigns.id
  subject_id      UUID           NOT NULL  -- identity being reviewed
  subject_type    TEXT           NOT NULL  -- e.g., "user_role", "service_account"
  status          TEXT           NOT NULL  -- ENUM: pending | in_progress | decided | expired
  created_at      TIMESTAMPTZ    NOT NULL
  deadline_at     TIMESTAMPTZ    NULLABLE
  schema_version  INTEGER        NOT NULL DEFAULT 1
```

**Uniqueness**: `(campaign_id, subject_id, subject_type)` — one task per subject per campaign.

**No soft-delete**: tasks are never deleted. Terminal states are `decided` and `expired`.

---

### 3. `reviewer_assignments` — Review Coordination Service

Tracks which reviewer is assigned to which task, and the assignment chain.

```
reviewer_assignments
  id                  UUID           PK
  task_id             UUID           NOT NULL, FK → review_tasks.id
  reviewer_id         UUID           NOT NULL  -- identity of the assigned reviewer
  assigned_by         UUID           NOT NULL  -- identity that made the assignment
  assigned_at         TIMESTAMPTZ    NOT NULL
  status              TEXT           NOT NULL  -- ENUM: active | superseded | declined
  superseded_by       UUID           NULLABLE, FK → reviewer_assignments.id (self-ref)
  policy_profile_id   UUID           NOT NULL, FK → tenant_policy_profiles.id
                                       -- snapshot of the policy version at time of assignment
  policy_version      INTEGER        NOT NULL  -- denormalized for change safety
  schema_version      INTEGER        NOT NULL DEFAULT 1
```

**Uniqueness**: only one `active` assignment per `task_id` at any time. Enforced at application layer and by partial unique index on `(task_id, status)` where `status = 'active'`.

**Reassignment rule**: reassignment does not delete the prior assignment. The old row transitions to `superseded` and `superseded_by` points to the new row. This produces an immutable chain for audit purposes.

**Unsupported reassignment variants**: any reassignment pattern not supported by the current Policy Compatibility Layer must return an explicit error. The assignment table must never be written into an inconsistent state as a fallback.

**Policy snapshot**: `policy_profile_id` + `policy_version` are captured at assignment time so that later policy changes do not retroactively alter the audit trail.

---

### 4. `review_decisions` — Review Coordination Service

The decision made by a reviewer on a task. Mutable within the review window; archived separately.

```
review_decisions
  id              UUID           PK
  task_id         UUID           NOT NULL, FK → review_tasks.id
  assignment_id   UUID           NOT NULL, FK → reviewer_assignments.id
  decision        TEXT           NOT NULL  -- ENUM: approve | revoke | defer | escalate
  rationale       TEXT           NULLABLE
  decided_at      TIMESTAMPTZ    NOT NULL
  decided_by      UUID           NOT NULL
  is_final        BOOLEAN        NOT NULL DEFAULT FALSE
  finalized_at    TIMESTAMPTZ    NULLABLE
  schema_version  INTEGER        NOT NULL DEFAULT 1
```

**Mutability window**: a decision may be amended while `is_final = FALSE` and the campaign is `active`. Once `is_final = TRUE`, the row is frozen — no UPDATE is permitted. The application layer must enforce this; the database enforces it via a trigger or row-level constraint.

**Archival**: when `is_final` transitions to `TRUE`, the Audit Integrity Store receives an append-only copy (see `audit_records`). The two records are related by `task_id` + `assignment_id` but are stored independently — the audit copy is not a join view of this table.

---

### 5. `evidence_packages` — Evidence Package Service

Sealed, downloadable compliance artifact generated at campaign close.

```
evidence_packages
  id              UUID           PK
  campaign_id     UUID           NOT NULL, FK → access_review_campaigns.id
  tenant_id       UUID           NOT NULL
  sealed_at       TIMESTAMPTZ    NOT NULL
  sealed_by       UUID           NOT NULL  -- system identity of the sealing process
  storage_uri     TEXT           NOT NULL  -- opaque pointer to object storage; never a public URL
  checksum_sha256 TEXT           NOT NULL
  status          TEXT           NOT NULL  -- ENUM: generating | sealed | corrupted
  schema_version  INTEGER        NOT NULL DEFAULT 1
```

**Immutability**: once `status = sealed`, no field except an out-of-band `status` corruption marker may change. Regeneration produces a new row; old rows are retained.

**Retention**: 7 years from `sealed_at`. Deletion before expiry requires documented compliance override. The Evidence Package Service owns both the metadata row and the storage object; the storage object must not outlive or be orphaned from the metadata row.

**Integrity**: `checksum_sha256` is verified on every download. A mismatch must set `status = corrupted` and trigger alerting — it must not silently return the file.

**Scope**: an evidence package contains a point-in-time snapshot of decisions, assignments, and audit records for one campaign. It does not embed live FK references to mutable rows.

---

### 6. `audit_records` — Audit Integrity Store

Append-only ledger of compliance-relevant events. No component may UPDATE or DELETE rows in this table.

```
audit_records
  id              UUID           PK
  tenant_id       UUID           NOT NULL
  campaign_id     UUID           NOT NULL  -- denormalized; FK constraint is advisory only
  event_type      TEXT           NOT NULL  -- controlled vocabulary; see lifecycle section
  actor_id        UUID           NOT NULL
  occurred_at     TIMESTAMPTZ    NOT NULL
  payload         JSONB          NOT NULL  -- event-specific fields; versioned by event_type
  source_system   TEXT           NOT NULL  -- ENUM: modern | legacy_bridge
  schema_version  INTEGER        NOT NULL DEFAULT 1
```

**Append-only**: enforced by database role separation — the write role for this table has INSERT privilege only. No application code is granted UPDATE or DELETE on this table.

**Event vocabulary** (release 1 minimum):
- `campaign.created`
- `campaign.activated`
- `campaign.closed`
- `task.assigned`
- `task.reassigned`
- `decision.submitted`
- `decision.finalized`
- `evidence.sealed`

**`source_system`**: distinguishes events produced by the modern system from bridge-translated events from the legacy adapter. This is critical for auditors to understand provenance during coexistence.

**Retention**: 7 years from `occurred_at`. Purge is prohibited before expiry.

**No soft-delete, no status field**: the audit record is the event. If an event was recorded in error, a compensating event is appended — the erroneous row is not removed.

---

### 7. `tenant_policy_profiles` — Reviewer Policy Compatibility Layer

Governs assignment rules, approval chains, and exception behavior per tenant.

```
tenant_policy_profiles
  id                  UUID           PK
  tenant_id           UUID           NOT NULL
  version             INTEGER        NOT NULL
  reviewer_hierarchy  JSONB          NOT NULL  -- structured hierarchy; schema governed by tenant contract
  exception_rules     JSONB          NOT NULL
  effective_from      TIMESTAMPTZ    NOT NULL
  effective_until     TIMESTAMPTZ    NULLABLE  -- NULL = currently active version
  created_by          UUID           NOT NULL
  schema_version      INTEGER        NOT NULL DEFAULT 1
```

**Uniqueness**: `(tenant_id, version)` — versions are monotonically increasing per tenant.

**Versioning**: a new row is inserted for each policy change; the prior row has `effective_until` set. This is an insert-only log for active versions. The Review Coordination Service reads the current version at assignment time and snapshots `policy_profile_id` + `version` into the assignment row.

**Separation from campaign state**: this table is owned exclusively by the Policy Compatibility Layer. The Review Coordination Service reads it but may not write to it.

---

### 8. `legacy_campaign_references` — Legacy Coexistence Adapter

A bridge record pointing to a campaign that originated in or is mirrored from the legacy system. **This is a compatibility boundary record, not a canonical campaign record.**

```
legacy_campaign_references
  id                   UUID           PK
  legacy_campaign_id   TEXT           NOT NULL  -- opaque legacy identifier
  tenant_id            UUID           NOT NULL
  bridge_status        TEXT           NOT NULL  -- ENUM: active | retired | error
  last_sync_at         TIMESTAMPTZ    NULLABLE
  sync_error_detail    TEXT           NULLABLE
  created_at           TIMESTAMPTZ    NOT NULL
  schema_version       INTEGER        NOT NULL DEFAULT 1
```

**Uniqueness**: `(tenant_id, legacy_campaign_id)`.

**Canonical authority**: the legacy system remains authoritative for any campaign that originated there during R1. This table is a pointer and sync-state record only. It must not store campaign decisions, task state, or reviewer assignments — those belong to the legacy system until ownership is explicitly transferred.

**Retirement**: when a legacy campaign is fully migrated to the modern system, `bridge_status` transitions to `retired`. The `access_review_campaigns.legacy_ref_id` FK is then the only surviving link.

**No backfill of historical campaigns older than two years**: per the spec's explicit non-goal, rows in this table for campaigns older than two years should not be created during R1. The boundary must be enforced at the adapter layer, not at the database constraint layer (which cannot know the legacy campaign age at insert time without a join).

---

## Lifecycle and State Transition Rules

### Campaign Status

```
draft → active → closed → archived
                         ↑ (archival is time-based, not manual)
```

- `draft → active`: requires at least one ReviewTask to exist.
- `active → closed`: sets `closed_at`; all `in_progress` tasks transition to `expired` if undecided.
- `closed → archived`: automated after evidence package is sealed and retention clock starts.
- No reverse transitions are permitted. A re-opened campaign requires a new `AccessReviewCampaign` record.

### Task Status

```
pending → in_progress → decided
        ↓
      expired  (if campaign closes before decision)
```

### Assignment Status

```
active → superseded  (on reassignment)
       → declined    (reviewer declines; triggers reassignment workflow)
```

### Decision Mutability

```
(mutable)  is_final=false → is_final=true  (immutable, archived to audit store)
```

---

## Retention and Archival Summary

| Entity | Retention Rule | Deletion Permitted |
|---|---|---|
| `access_review_campaigns` | Indefinite during R1; archival after evidence sealed | No before archival window |
| `review_tasks` | Lifecycle-tied to campaign | No |
| `reviewer_assignments` | Lifecycle-tied to campaign | No |
| `review_decisions` | Lifecycle-tied to campaign | No (finalized decisions frozen) |
| `evidence_packages` | 7 years from `sealed_at` | Only after expiry, with documented override |
| `audit_records` | 7 years from `occurred_at` | Prohibited before expiry |
| `tenant_policy_profiles` | Indefinite (versioned log) | No version deletion |
| `legacy_campaign_references` | Until bridge retired | Can retire row; never delete |

---

## Migration and Coexistence Boundaries

### What the Modern Schema Does NOT Own During R1

- Campaign records that originated in the legacy system — the legacy system remains authoritative.
- Historical campaigns older than 2 years — no backfill during R1.
- Any assignment or decision data for campaigns whose `access_review_campaigns` row has `legacy_ref_id` populated and `bridge_status = active` — those are read-through via the adapter only.

### Safe Additive Changes (No Downtime Required)

The following changes are safe without data migration:

- Adding a nullable column to any table.
- Adding a new `event_type` to `audit_records.event_type` controlled vocabulary.
- Adding a new `bridge_status` enum value to `legacy_campaign_references`.
- Adding a new policy version row to `tenant_policy_profiles`.

### Changes That Require Migration Planning

- Promoting `legacy_ref_id` campaigns to fully modern ownership — requires a formal ownership-transfer protocol (create modern decision/assignment records, retire legacy bridge reference, emit `campaign.migrated` audit event).
- Changing the structure of `reviewer_hierarchy` or `exception_rules` JSONB — requires versioned schema within the blob and a `schema_version` bump.
- Any change to `audit_records.payload` structure for an existing `event_type` — append a new event type instead of mutating the old one.

### Consistency Model

- `ReviewDecision` → `AuditRecord` archive is **eventually consistent**. The archive write is a downstream effect; a failure must be retried, not ignored. The decision row and the audit row are never in the same database transaction.
- `ReviewerAssignment` → `TenantPolicyProfile` validation is **synchronous at write time**: an assignment must not be committed without a valid policy profile version being readable.
- `EvidencePackage` sealing is **atomic at the metadata level**: the `evidence_packages` row and the object storage write must either both succeed or both be rolled back/cleaned up. Split-brain between metadata and storage is a data integrity violation.

### Coexistence Hazard: Dual-Write

During R1, the legacy module and the modern Review Coordination Service must not both write `ReviewDecision` records for the same campaign. The coexistence rule is:

- Campaigns with `legacy_ref_id = NULL` → modern system is authoritative; no legacy writes permitted.
- Campaigns with `legacy_ref_id` populated and `bridge_status = active` → legacy system is authoritative; modern system reads only via adapter.
- Mixed-write is explicitly prohibited. The Legacy Coexistence Adapter enforces this at the boundary; the database does not (and cannot) enforce cross-system authority.

---

## Quality Gate Checklist

- [x] Data ownership is explicit for every core entity
- [x] Schema aligns with architecture containers and domain boundaries
- [x] `LegacyCampaignReference` is isolated as compatibility-only; never promoted to canonical
- [x] `TenantPolicyProfile` is separated from campaign state with version-snapshot on assignment
- [x] Compliance artifacts (`EvidencePackage`, `AuditRecord`) carry 7-year retention and tamper-evident rules
- [x] Audit records are append-only by role privilege, not just application convention
- [x] All state transitions are enumerated and non-reversible transitions are explicit
- [x] Brownfield coexistence boundary (dual-write prohibition) is documented
- [x] Unsupported reassignment variants are handled by explicit failure, not silent state corruption
- [x] Additive-safe changes are distinguished from migration-required changes
- [x] Historical campaign backfill (>2 years) is explicitly out of scope with enforcement responsibility noted

`★ Insight ─────────────────────────────────────`
Three decisions in this schema carry the most long-term risk if gotten wrong:

1. **Audit records as a separate physical store (not a view)** — embedding audit data in the workflow tables would make it impossible to enforce append-only via role separation. Separating them makes the tamper-evident guarantee enforceable at the database layer.

2. **Policy version snapshot on assignment** — if `reviewer_assignments` only held a FK to the current policy, a policy update would silently change the meaning of past assignments. The `policy_version` denormalization makes the assignment record self-describing for auditors even after the policy changes.

3. **`source_system` on `audit_records`** — without it, auditors cannot distinguish events that came through the legacy bridge (and may carry translation approximations) from events that originated in the modern system. During coexistence, this distinction is material.
`─────────────────────────────────────────────────`
