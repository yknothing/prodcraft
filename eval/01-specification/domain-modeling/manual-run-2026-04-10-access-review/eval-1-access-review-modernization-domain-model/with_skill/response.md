# Domain Model: Access Review Modernization

## Core Entities

- **AccessReviewCampaign** -- the governed review exercise with lifecycle, scope, and evidence obligations
- **ReviewTask** -- the reviewer-visible unit of work inside a campaign
- **ReviewerAssignment** -- the authoritative mapping between a review task and the currently accountable reviewer under tenant policy
- **ReviewDecision** -- the approve, reject, or delegate action plus rationale recorded against a review task
- **EvidencePackage** -- the exportable compliance artifact for one campaign
- **AuditRecord** -- the tamper-evident event trail for campaign and reviewer actions
- **TenantPolicyProfile** -- the tenant-specific hierarchy and exception rules that constrain assignment and approval behavior
- **LegacyCampaignReference** -- the compatibility link to read-only campaign history that remains in the legacy experience

## Authoritative Relationships

- One **AccessReviewCampaign** owns many **ReviewTask** records.
- Each **ReviewTask** has one active **ReviewerAssignment** at a time.
- One **ReviewerAssignment** is constrained by one **TenantPolicyProfile**.
- One **ReviewDecision** belongs to one **ReviewTask**.
- One **EvidencePackage** belongs to one **AccessReviewCampaign**.
- Many **AuditRecord** entries belong to one **AccessReviewCampaign** and may also reference the affected **ReviewTask**.
- **LegacyCampaignReference** is compatibility-only. It points to legacy history, but it is not the canonical release-1 campaign record.

## Ubiquitous Language

- **campaign** means the governed review exercise, not a background sync batch
- **review task** means the work item a reviewer must act on, not a generic queue message
- **reviewer assignment** means the currently accountable reviewer under policy, not every historical routing hint
- **evidence package** means the externally consumable compliance artifact, not internal debug output
- **audit record** means the tamper-evident event trail, not a mutable activity feed
- **legacy campaign** means a compatibility and history concept, not the canonical current-work model

## Justified Bounded Contexts

1. **Review Operations**
   - `AccessReviewCampaign`
   - `ReviewTask`
   - `ReviewerAssignment`
   - `ReviewDecision`
2. **Policy Compatibility**
   - `TenantPolicyProfile`
   - tenant-specific reviewer hierarchy and exception terms that must remain visible during release 1
3. **Evidence and Audit**
   - `EvidencePackage`
   - `AuditRecord`

No separate "sync" bounded context is justified yet. Sync semantics are unresolved and should remain an open cross-boundary concern rather than becoming a canonical business domain.

## Scenario Check

- **Current campaigns during audit season**: `AccessReviewCampaign`, `ReviewTask`, and `ReviewerAssignment` explain current release-1 behavior without assuming cutover.
- **Historical campaigns older than two years**: `LegacyCampaignReference` keeps the read-only compatibility boundary visible instead of pretending history already lives in the new model.
- **Partially understood reassignment and data-correction flows**: those remain attached to `ReviewerAssignment` and `ReviewDecision` as open domain questions rather than being silently collapsed into sync or migration language.
