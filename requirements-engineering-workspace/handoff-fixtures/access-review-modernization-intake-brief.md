# Intake Brief

## Work Summary

- **Request**: Modernize the legacy access-review module in an existing compliance SaaS product using discovery notes from compliance operations, customer success, and security.
- **Work type**: Migration
- **Entry phase**: 01-specification
- **Recommended workflow**: brownfield
- **Scope assessment**: large
- **Urgency**: normal

## Required Artifact

- **Artifact name**: `intake-brief`
- **Status**: approved
- **Approver**: user

## Routing Decision

1. **First skill**: `requirements-engineering`
   - Output: `requirements-doc`
2. **Second skill**: `system-design`
   - Output: `architecture-decision-record`
3. **Third skill**: `acceptance-criteria`
   - Output: `acceptance-criteria-set`

## Key Risks

1. Contractual tenant-specific reviewer hierarchies and exception rules are only partially documented and may hide brownfield compatibility requirements.
2. Stakeholders may push for a full rewrite, cutover plan, or data model decisions before the release-1 requirements boundary is agreed.

## Fast-Track or Skipped Gates

- **Any shortcut taken?** no
- **If yes, why was it acceptable?**
- **What debt does this create?**

## Notes for Handoff

- Constraints:
  - Stay in the requirements layer; do not jump into service decomposition, database schema, API contracts, or migration sequencing.
  - Preserve the brownfield constraint that release 1 must coexist with the legacy module during audit season rather than requiring a same-day cutover.
  - Treat unsupported quantitative targets as open questions or assumptions, not hard requirements.
- Open questions:
  - Which tenant-specific reviewer hierarchies are contractual and must be preserved in release 1?
  - Can historical campaigns remain read-only in the legacy module if the new product can export evidence packages?
  - Does "same-day sync" mean near-real-time propagation or end-of-day consistency?
- Context that downstream skills must preserve:
  - This is an existing compliance SaaS product with a legacy module already in production.
  - The next downstream skill expects reviewed requirements for a modernization effort, not a rewrite plan.
