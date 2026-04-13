I have everything I need. Producing the artifact now.

---

# Access Review Modernization — Data Schema & Lifecycle Boundaries

**Slice:** Release 1 brownfield modernization  
**Scope of this document:** table/collection definitions, authoritative ownership, lifecycle state machines, retention and archival contracts, compatibility boundaries, change safety invariants.  
**Out of scope:** API contracts, service implementation, migration scripts, query patterns.

---

## Assumptions

1. Storage is a single relational database per tenant unless otherwise resolved; column types follow PostgreSQL conventions.
2. "Tamper-evident" is achieved with a content hash stored alongside each compliance artifact. The hash input definition is a critical decision left as a contribution request (§8).
3. Historical campaigns (>2 years old) are defined by `AccessReviewCampaign.closed_at < NOW() - INTERVAL '2 years'`. Full migration of these is an explicit non-goal.
4. "Seven years" retention is calculated from `campaign.closed_at` for campaign-scoped records; from `occurred_at` for `AuditRecord`; from `generated_at` for `EvidencePackage`.
5. `TenantPolicyProfile` is the single source of truth for which assignment variants a given tenant permits. Rows in that table are versioned, not mutated in place.

---

## 1. Entity Schemas

### 1.1 `AccessReviewCampaign`

Canonical record for a review campaign. **Owned by the modern system.**

```sql
TABLE access_review_campaigns (
  id                    UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id             TEXT          NOT NULL,
  title                 TEXT          NOT NULL,
  status                TEXT          NOT NULL
                          CHECK (status IN ('DRAFT','ACTIVE','CLOSED','ARCHIVED')),
  scope_type            TEXT          NOT NULL,   -- e.g. 'ROLE', 'APPLICATION'
  scope_ref             TEXT          NOT NULL,   -- opaque reference to scoped resource
  created_at            TIMESTAMPTZ   NOT NULL DEFAULT now(),
  created_by            TEXT          NOT NULL,   -- identity reference
  activated_at          TIMESTAMPTZ,
  closed_at             TIMESTAMPTZ,
  archived_at           TIMESTAMPTZ,
  -- Coexistence link; nullable. Presence does NOT make this record non-canonical.
  legacy_campaign_ref_id UUID         REFERENCES legacy_campaign_references(id)
                          ON DELETE RESTRICT,

  CONSTRAINT status_timestamps_consistent CHECK (
    (status = 'DRAFT'    OR activated_at IS NOT NULL) AND
    (status IN ('DRAFT','ACTIVE') OR closed_at IS NOT NULL) AND
    (status = 'ARCHIVED' OR archived_at IS NULL)
  )
);

INDEX ON access_review_campaigns (tenant_id, status);
INDEX ON access_review_campaigns (closed_at)  -- supports retention queries
  WHERE closed_at IS NOT NULL;
```

**Status lifecycle:** see §4.1.  
**Retention:** `ARCHIVED` records are soft-deleted only. Hard deletion is prohibited while `closed_at > NOW() - INTERVAL '7 years'` (evidence and audit records reference this id).

---

### 1.2 `ReviewTask`

A single unit of review work within a campaign (one subject per task). **Owned by the modern system.**

```sql
TABLE review_tasks (
  id             UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id    UUID         NOT NULL REFERENCES access_review_campaigns(id)
                               ON DELETE RESTRICT,
  subject_id     TEXT         NOT NULL,   -- identity or resource being reviewed
  subject_type   TEXT         NOT NULL,
  status         TEXT         NOT NULL
                   CHECK (status IN ('PENDING','IN_PROGRESS','COMPLETED','CANCELLED')),
  created_at     TIMESTAMPTZ  NOT NULL DEFAULT now(),
  completed_at   TIMESTAMPTZ,

  CONSTRAINT completed_at_only_when_terminal CHECK (
    (status IN ('COMPLETED','CANCELLED')) = (completed_at IS NOT NULL)
  ),
  UNIQUE (campaign_id, subject_id, subject_type)  -- no duplicate tasks per campaign
);

INDEX ON review_tasks (campaign_id, status);
```

**Status lifecycle:** see §4.2.

---

### 1.3 `ReviewerAssignment`

Records who is assigned to a task and why. Reassignment creates a new row; prior rows are superseded, not deleted. **Owned by the modern system.**

```sql
TABLE reviewer_assignments (
  id                  UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  review_task_id      UUID         NOT NULL REFERENCES review_tasks(id)
                                    ON DELETE RESTRICT,
  reviewer_id         TEXT         NOT NULL,
  assigned_by         TEXT         NOT NULL,
  assigned_at         TIMESTAMPTZ  NOT NULL DEFAULT now(),
  assignment_variant  TEXT         NOT NULL,
    -- MUST match an entry in the referencing tenant's TenantPolicyProfile.
    -- Enforced at service boundary; violation is a hard failure (see §7.2).
  assignment_reason   TEXT,
  superseded_by       UUID         REFERENCES reviewer_assignments(id)
                                    ON DELETE RESTRICT,
  is_active           BOOLEAN      NOT NULL DEFAULT TRUE,

  CONSTRAINT superseded_implies_inactive CHECK (
    (superseded_by IS NULL) OR (is_active = FALSE)
  ),
  -- Only one active assignment per task at a time:
  UNIQUE (review_task_id, is_active) WHERE is_active = TRUE
);

INDEX ON reviewer_assignments (review_task_id, is_active);
```

**Change safety note:** `assignment_variant` must be validated against `tenant_policy_profiles.allowed_assignment_variants` before insert. If the variant is absent from that list the operation must be rejected with a typed error. Silent fallback or default-variant substitution is prohibited (§7.2).

---

### 1.4 `ReviewDecision`

The recorded outcome of a reviewer completing a task. Immutable once `is_final = TRUE`. **Owned by the modern system.**

```sql
TABLE review_decisions (
  id                      UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  review_task_id          UUID         NOT NULL REFERENCES review_tasks(id)
                                         ON DELETE RESTRICT,
  reviewer_assignment_id  UUID         NOT NULL REFERENCES reviewer_assignments(id)
                                         ON DELETE RESTRICT,
  decision                TEXT         NOT NULL
                             CHECK (decision IN ('APPROVE','REVOKE','ESCALATE','ABSTAIN')),
  rationale               TEXT,
  decided_at              TIMESTAMPTZ  NOT NULL DEFAULT now(),
  decided_by              TEXT         NOT NULL,
  is_final                BOOLEAN      NOT NULL DEFAULT FALSE
);

-- Enforce at most one final decision per task:
UNIQUE INDEX review_decisions_one_final
  ON review_decisions (review_task_id)
  WHERE is_final = TRUE;

INDEX ON review_decisions (review_task_id);
INDEX ON review_decisions (reviewer_assignment_id);
```

**Change safety note:** Once `is_final = TRUE` the row must not be updated or deleted. Any attempt must be rejected by the service and recorded as a `DECISION_FINALIZATION_ATTEMPT` audit event.

---

### 1.5 `EvidencePackage`

A sealed, downloadable compliance artifact generated at campaign close. **Owned by the Evidence Package Service.** Complies with 7-year retention. Append-and-seal only.

```sql
TABLE evidence_packages (
  id                   UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id          UUID         NOT NULL REFERENCES access_review_campaigns(id)
                                      ON DELETE RESTRICT,
  generated_at         TIMESTAMPTZ  NOT NULL DEFAULT now(),
  generated_by         TEXT         NOT NULL,
  status               TEXT         NOT NULL
                          CHECK (status IN ('GENERATING','READY','SEALED')),
  format_version       TEXT         NOT NULL,   -- schema version of package contents
  content_hash         TEXT,         -- populated on READY; sealed on transition to SEALED
  hash_algorithm       TEXT,         -- e.g. 'SHA-256'
  storage_location     TEXT,         -- opaque reference to immutable object store
  retention_expires_at TIMESTAMPTZ  NOT NULL,
    -- Set at insert: campaign.closed_at + INTERVAL '7 years'
    -- Must never be shortened after insert.

  CONSTRAINT sealed_requires_hash CHECK (
    status != 'SEALED' OR (content_hash IS NOT NULL AND storage_location IS NOT NULL)
  ),
  CONSTRAINT retention_minimum CHECK (
    retention_expires_at >= generated_at + INTERVAL '7 years'
  )
);

INDEX ON evidence_packages (campaign_id, status);
INDEX ON evidence_packages (retention_expires_at);
```

**Status lifecycle:** `GENERATING → READY → SEALED`. `SEALED` is terminal; no column may be updated after sealing. The `content_hash` covers the full package payload — see §8 for the contribution request on hash input definition.  
**Archival:** at `retention_expires_at`, the storage artifact may be deleted by a scheduled archival job. The row itself must be retained with `status = 'SEALED'` and `storage_location = NULL` to preserve the evidence record of what existed.

---

### 1.6 `AuditRecord`

Append-only, tamper-evident log of every state-changing event in the modern system. **Owned by the Audit Integrity Store.** No UPDATE or DELETE ever. 7-year retention.

```sql
TABLE audit_records (
  id                 UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id        UUID         REFERENCES access_review_campaigns(id)
                                   ON DELETE RESTRICT,  -- nullable for system-level events
  entity_type        TEXT         NOT NULL,  -- 'CAMPAIGN','TASK','ASSIGNMENT','DECISION','EVIDENCE'
  entity_id          TEXT         NOT NULL,
  event_type         TEXT         NOT NULL,  -- e.g. 'CAMPAIGN_ACTIVATED', 'DECISION_FINALIZED'
  actor_id           TEXT         NOT NULL,
  occurred_at        TIMESTAMPTZ  NOT NULL DEFAULT now(),
  sequence_number    BIGINT       NOT NULL,  -- monotonically increasing per campaign; see §7.3
  payload            JSONB        NOT NULL,  -- immutable snapshot of the event at occurrence time
  payload_hash       TEXT         NOT NULL,  -- hash of payload; algorithm recorded separately
  hash_algorithm     TEXT         NOT NULL,
  retention_expires_at TIMESTAMPTZ NOT NULL   -- occurred_at + INTERVAL '7 years'
);

-- No primary key on (campaign_id, sequence_number) because system-level events have NULL campaign_id;
-- application must enforce sequence monotonicity per campaign before insert.
INDEX ON audit_records (campaign_id, sequence_number);
INDEX ON audit_records (entity_type, entity_id, occurred_at);
INDEX ON audit_records (retention_expires_at);
```

**Change safety:** rows in this table must never be mutated or removed except by a privileged, separately authorized archival process at `retention_expires_at`. No application-layer code path may issue UPDATE or DELETE against this table.

---

### 1.7 `TenantPolicyProfile`

Governs per-tenant reviewer hierarchy and permitted assignment behavior. Versioned, not mutated in place. **Owned by the Reviewer Policy Compatibility Layer.**

```sql
TABLE tenant_policy_profiles (
  id                         UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id                  TEXT         NOT NULL,
  version                    INTEGER      NOT NULL,
  reviewer_hierarchy_rules   JSONB        NOT NULL,
    -- Opaque to this schema; interpreted by Reviewer Policy Compatibility Layer only.
  allowed_assignment_variants JSONB       NOT NULL,
    -- Array of permitted variant strings, e.g. ["DIRECT","DELEGATED","MANAGER_CASCADE"].
    -- ReviewerAssignment.assignment_variant must appear in this list at assignment time.
  exception_rules            JSONB        NOT NULL,
  effective_from             TIMESTAMPTZ  NOT NULL,
  effective_to               TIMESTAMPTZ,          -- NULL means currently effective

  CONSTRAINT version_unique_per_tenant UNIQUE (tenant_id, version),
  CONSTRAINT effective_range_valid CHECK (
    effective_to IS NULL OR effective_to > effective_from
  )
);

-- At most one currently-effective profile per tenant:
UNIQUE INDEX tenant_policy_one_active
  ON tenant_policy_profiles (tenant_id)
  WHERE effective_to IS NULL;

INDEX ON tenant_policy_profiles (tenant_id, effective_from);
```

**Change safety:** profiles are versioned, not updated. To change a policy: insert a new row with an incremented version, set `effective_to` on the prior row, set `effective_from` on the new row to the transition timestamp. No in-place edits to `reviewer_hierarchy_rules` or `allowed_assignment_variants`.

---

### 1.8 `LegacyCampaignReference`

A compatibility record linking a modern campaign (if one exists) to a legacy system campaign id. **Owned by the Legacy Coexistence Adapter. Must not become a canonical current-state record.** Read-only from all other services.

```sql
TABLE legacy_campaign_references (
  id                    UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  legacy_system_id      TEXT         NOT NULL,
  legacy_campaign_key   TEXT         NOT NULL,
  modern_campaign_id    UUID         REFERENCES access_review_campaigns(id)
                                      ON DELETE RESTRICT,  -- nullable until linked
  sync_status           TEXT         NOT NULL DEFAULT 'UNLINKED'
                           CHECK (sync_status IN ('UNLINKED','LINKED','SHADOW_ONLY')),
  last_legacy_read_at   TIMESTAMPTZ,
  is_historical         BOOLEAN      NOT NULL DEFAULT FALSE,
    -- TRUE when the legacy campaign closed_at > 2 years ago; read-only in modern system.
  created_at            TIMESTAMPTZ  NOT NULL DEFAULT now(),

  UNIQUE (legacy_system_id, legacy_campaign_key),
  CONSTRAINT historical_cannot_link CHECK (
    NOT (is_historical = TRUE AND sync_status = 'LINKED')
  )
);

INDEX ON legacy_campaign_references (modern_campaign_id)
  WHERE modern_campaign_id IS NOT NULL;
INDEX ON legacy_campaign_references (sync_status);
```

**Boundary contract:** this table is the only sanctioned read path into the legacy system's campaign identifiers. No other modern table holds a legacy system identifier directly. `SHADOW_ONLY` means the legacy record exists but no modern campaign has been created; `LINKED` means a modern campaign is the authoritative record.

---

## 2. Ownership Registry

| Entity | Owner Service | Write Access | Read Access | Notes |
|---|---|---|---|---|
| `access_review_campaigns` | Review Coordination Service | Review Coordination | All | Canonical record |
| `review_tasks` | Review Coordination Service | Review Coordination | All | |
| `reviewer_assignments` | Review Coordination Service | Review Coordination | All | Variant validated against TenantPolicyProfile |
| `review_decisions` | Review Coordination Service | Review Coordination | All | Immutable once final |
| `evidence_packages` | Evidence Package Service | Evidence Package | All | Immutable once sealed |
| `audit_records` | Audit Integrity Store | Audit Integrity Store only | Compliance/read-only | Append-only |
| `tenant_policy_profiles` | Reviewer Policy Compatibility Layer | Reviewer Policy Compat. | All (read) | Versioned, not mutated |
| `legacy_campaign_references` | Legacy Coexistence Adapter | Legacy Coexistence Adapter | Adapter + Coordination read | Must not become canonical |

---

## 3. Retention and Archival Policy

| Table | Retention Clock Starts | Retention Duration | Hard Deletion Allowed | Archival Behavior |
|---|---|---|---|---|
| `audit_records` | `occurred_at` | 7 years | At `retention_expires_at` by authorized archival job only | Row kept; `payload` may be nulled post-expiry if storage pressure requires, but `payload_hash` must be retained |
| `evidence_packages` | `generated_at` | 7 years | Storage artifact at `retention_expires_at`; row never | Row retained with `storage_location = NULL`; `content_hash` and `status = 'SEALED'` preserved forever |
| `access_review_campaigns` | `closed_at` | Must not be hard-deleted while any `audit_records` or `evidence_packages` reference it | No hard delete until all referencing compliance rows are expired | Transitions to `ARCHIVED`; soft-delete available |
| `review_tasks`, `reviewer_assignments`, `review_decisions` | Follow parent campaign | Same as campaign | Cascade from campaign after compliance expiry | No independent archival; lifecycle is campaign-scoped |
| `tenant_policy_profiles` | `effective_to` | No automatic expiry | No | Expired (non-null `effective_to`) profiles must be retained for audit of historical decisions |
| `legacy_campaign_references` | `created_at` | As long as the linked legacy campaign requires read access | Only after legacy system decommission | `is_historical = TRUE` rows are read-only indefinitely |

---

## 4. Lifecycle State Machines

### 4.1 `AccessReviewCampaign.status`

```
DRAFT ──────────────────────► ACTIVE ─────────────────────────► CLOSED ─► ARCHIVED
  │                               │                                 │
  │   [activated_at set]          │   [closed_at set;               │   [archived_at set;
  │                               │    tasks reach terminal]        │    soft-delete;
  │                               │                                 │    evidence sealed]
  └──────────[no skip]────────────┴──────────[no skip]─────────────┘

Forbidden transitions: DRAFT→CLOSED, DRAFT→ARCHIVED, ACTIVE→ARCHIVED, CLOSED→ACTIVE
```

### 4.2 `ReviewTask.status`

```
PENDING ──────────────────► IN_PROGRESS ─────────────────────► COMPLETED
   │                              │                                 
   │                              └────────────────────────────► CANCELLED
   │                                                               │
   └───────────────────────────────────────────────────────────────┘
                                [campaign cancelled]
```

### 4.3 `ReviewerAssignment` reassignment

```
AssignmentRow(is_active=TRUE)
    │
    ├── [reassignment requested; variant in allowed_assignment_variants]
    │       └── INSERT new AssignmentRow(is_active=TRUE)
    │           UPDATE old row: is_active=FALSE, superseded_by=new.id
    │
    └── [reassignment requested; variant NOT in allowed_assignment_variants]
            └── REJECT with typed error UNSUPPORTED_ASSIGNMENT_VARIANT
                Emit AuditRecord(event_type='ASSIGNMENT_REJECTED_UNSUPPORTED_VARIANT')
                [no state change]
```

### 4.4 `EvidencePackage.status`

```
GENERATING ──────────► READY ──────────────────────► SEALED (terminal)
                         │
                         └── [content_hash computed; storage confirmed]
```

---

## 5. Compatibility Boundaries

### 5.1 The single crossing point

`LegacyCampaignReference` is the **only** table that holds a legacy system identifier. No other modern table should embed a legacy system key directly. Any new service that needs to correlate with the legacy system must go through this table.

### 5.2 Historical campaign read path

| Campaign age | Modern read | Write | Evidence generation |
|---|---|---|---|
| < 2 years | Full access | Full access | Allowed |
| ≥ 2 years | Via `LegacyCampaignReference.last_legacy_read_at` + Legacy Coexistence Adapter | Prohibited (full migration not in scope) | Prohibited |

A request to create a campaign in the modern system that maps to a `is_historical = TRUE` legacy reference must be rejected.

### 5.3 Policy version at assignment time

The `assignment_variant` is validated against the `TenantPolicyProfile` version that is `effective_to IS NULL` at `assigned_at`. A policy change that removes a variant does not retroactively invalidate existing `ReviewerAssignment` rows where `is_active = FALSE` (history) but does prohibit new assignments of that variant.

### 5.4 `TenantPolicyProfile` isolation

Other services may read `tenant_policy_profiles` for validation, but only the Reviewer Policy Compatibility Layer may write to it. If the legacy system's reviewer hierarchy changes, the compatibility layer is responsible for inserting a new profile version; it must not patch the current row.

---

## 6. Archival Sequence

The archival job must execute in this order to satisfy foreign key constraints:

1. Identify `evidence_packages` with `retention_expires_at <= NOW()` and `status = 'SEALED'`. Null `storage_location`; do not delete the row.
2. Identify `audit_records` with `retention_expires_at <= NOW()`. Delete or null payload per policy. Retain `id`, `event_type`, `entity_id`, `occurred_at`, `payload_hash`.
3. For campaigns where all referencing `evidence_packages` have passed step 1 and all `audit_records` have passed step 2, the campaign may be considered fully expired. Even then, hard deletion is prohibited; the row must remain for referential integrity with `legacy_campaign_references`.

No archival job may run steps out of order. Each step must be idempotent.

---

## 7. Change Safety Invariants

### 7.1 Immutability invariants (enforced at service layer; not expressible as a single DB constraint)

| Row condition | Prohibited operations |
|---|---|
| `review_decisions.is_final = TRUE` | UPDATE, DELETE |
| `evidence_packages.status = 'SEALED'` | UPDATE any column, DELETE |
| `audit_records` (all rows) | UPDATE any column, DELETE (except by authorized archival job post-expiry) |
| `tenant_policy_profiles` with `effective_to IS NULL` | UPDATE `reviewer_hierarchy_rules`, `allowed_assignment_variants`, `exception_rules` — version these instead |

### 7.2 Assignment variant guard

Before inserting a `ReviewerAssignment`:

1. Fetch `tenant_policy_profiles` where `tenant_id = campaign.tenant_id AND effective_to IS NULL`.
2. Assert `assignment_variant ∈ allowed_assignment_variants`.
3. If assertion fails: emit `AuditRecord(event_type = 'ASSIGNMENT_REJECTED_UNSUPPORTED_VARIANT')` and return a typed error. **Do not fall back to a default variant.**

### 7.3 Audit record sequence monotonicity

`sequence_number` must be monotonically increasing per `campaign_id`. The issuing service is responsible for acquiring a per-campaign sequence slot (e.g. via `SELECT ... FOR UPDATE` on the campaign row) before inserting. Gaps are permitted; reversal is not. Out-of-order writes are a change-safety violation.

### 7.4 `LegacyCampaignReference.sync_status` transition guard

| From | To | Allowed |
|---|---|---|
| `UNLINKED` | `LINKED` | Yes, when a modern campaign is created |
| `UNLINKED` | `SHADOW_ONLY` | Yes |
| `SHADOW_ONLY` | `LINKED` | Yes, when a modern campaign is subsequently created |
| `LINKED` | `UNLINKED` | **No** — modern campaign exists and is the canonical record |
| `LINKED` | `SHADOW_ONLY` | **No** |
| Any | Any while `is_historical = TRUE` | **No** — historical references are read-only |

---

## 8. Contribution Request — Evidence Package Hash Input

`★ Design Decision ───────────────────────────────`
I've set up `EvidencePackage` with `content_hash` and `hash_algorithm` columns. The tamper-evidence guarantee is only as strong as what goes into the hash.

**This is a meaningful trade-off**: a narrow hash (decisions only) is simpler to regenerate for verification, but a wider hash (full campaign snapshot: tasks, assignments, decisions, timeline) is harder to forge partially but heavier to compute and more sensitive to schema evolution.
`─────────────────────────────────────────────────`

**In `evidence_packages`, define the `compute_package_hash_input` contract.**

Located at: the interface between `EvidencePackage` sealing and the object store write — this is a pre-write hook, ~8–10 lines of pseudocode or a function signature with a documented input object.

**Consider:**

- **Narrow hash** (decisions + task IDs + decided_at): easier to verify, less data, but a tampered reviewer assignment would not be detected if the decision text was preserved.
- **Wide hash** (full campaign state: tasks, assignments, decisions, campaign metadata, sequence numbers from audit log): tamper-resistant to partial state modification but requires a canonical serialization order that must be versioned alongside `format_version`.
- **Audit-log hash chain**: hash the `evidence_packages.content_hash` over the sequence of `audit_records.payload_hash` for that campaign — this ties evidence to the append-only audit trail rather than a point-in-time snapshot.

Whichever you choose, `format_version` must encode the hash input definition so future verifiers know what to reconstruct.

---

## 9. Unresolved Questions (Kept Visible Per Architectural Driver 5)

| Question | Impact on Schema | Status |
|---|---|---|
| Sync semantics (near-real-time vs. eventual) between legacy and modern | `LegacyCampaignReference.last_legacy_read_at` staleness tolerance; whether a `sync_lag_seconds` column is needed | Unresolved per architecture doc |
| Historical-data treatment for campaigns 1–2 years old | Whether the `is_historical` boundary of 2 years is a hard cutoff or a phased migration | Unresolved per spec |
| Exact performance bound on reviewer list responsiveness | Potential indexing changes on `reviewer_assignments`; possible read replica routing | Unresolved per architecture doc |
| `sequence_number` contention under high concurrency | Whether per-campaign row locking is acceptable or a sequence table is needed | Not resolved in source documents |

These questions must remain visible. Schema changes to address them require a new version of this document and explicit sign-off; they must not be silently resolved by an implementation choice.
