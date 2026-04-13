# Domain Model Summary

## Core Entities

- **AccessReviewCampaign** -- the governed review exercise with lifecycle, scope, and evidence obligations
- **ReviewTask** -- a reviewer-visible unit of work linked to a campaign
- **ReviewerAssignment** -- the authoritative mapping between a review task and the current responsible reviewer under tenant policy
- **ReviewDecision** -- the recorded approve / reject / delegate action and its rationale
- **EvidencePackage** -- the exportable compliance record for a campaign
- **AuditRecord** -- the tamper-evident event trail for campaign and reviewer actions
- **TenantPolicyProfile** -- the tenant-specific hierarchy and exception rules that constrain assignment and approval behavior
- **LegacyCampaignReference** -- the compatibility link to legacy-read-only campaign history

## Authoritative Relationships

- `AccessReviewCampaign` owns many `ReviewTask` records
- each `ReviewTask` has one active `ReviewerAssignment`
- `ReviewerAssignment` is constrained by one `TenantPolicyProfile`
- `ReviewDecision` belongs to one `ReviewTask`
- `EvidencePackage` and `AuditRecord` belong to one `AccessReviewCampaign`
- `LegacyCampaignReference` is compatibility-only and must not become the future authoritative campaign record

## Ubiquitous Language

- **campaign** means the governed review exercise, not a generic batch job
- **reviewer assignment** means the currently accountable reviewer under policy, not every possible historical routing hint
- **evidence package** means the externally consumable compliance artifact, not internal debug output
- **audit record** means the tamper-evident event trail, not a mutable activity log
- **legacy campaign** is a compatibility and history concept, not the canonical release-1 record for current work

## Candidate Bounded Contexts

- **Review Operations** -- campaigns, tasks, assignments, decisions
- **Policy Compatibility** -- tenant-specific hierarchy and exception rules
- **Evidence and Audit** -- evidence packages and tamper-evident audit records

The split is justified because policy compatibility and evidence retention have distinct rules and should stay visible during brownfield coexistence.
