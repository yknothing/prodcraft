# Domain Model Summary

## Core Entities

- **AccessReviewCampaign**
- **ReviewTask**
- **ReviewerAssignment**
- **ReviewDecision**
- **EvidencePackage**
- **AuditRecord**
- **TenantPolicyProfile**
- **LegacyCampaignReference**

## Key Modeling Boundaries

- `LegacyCampaignReference` is compatibility-only and must not become the canonical current-state record.
- `TenantPolicyProfile` governs assignment and approval behavior but should stay separate from the core campaign state.
- `EvidencePackage` and `AuditRecord` are compliance artifacts with stronger retention and integrity rules than normal workflow data.
