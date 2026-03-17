# Release 1 API Contract Outline: Access Review Modernization

## Contract Boundaries

- API contracts are defined only for release-1 surfaces that the new experience must expose.
- Legacy coexistence remains explicit; this contract does **not** assume a replacement-only cutover.
- Historical campaigns older than two years remain behind a legacy-read boundary for release 1 unless a later decision changes that boundary.

## Contract Style

- **External/admin-facing contract**: REST over JSON for the Modern Access Review Experience.
- **Compatibility boundary**: internal service contract between the Review Coordination Service and the Legacy Coexistence Adapter; the exact transport can remain implementation-selectable as long as deferred-consistency behavior is preserved.

## Admin-Facing REST Resources

### Campaigns

- `POST /v1/campaigns`
  - Create a release-1 access-review campaign from a supported template.
- `GET /v1/campaigns/{campaignId}`
  - Fetch campaign summary, status, and evidence availability.
- `GET /v1/campaigns`
  - List campaigns with pagination and filter support.

### Reviewer Actions

- `POST /v1/campaigns/{campaignId}/review-actions`
  - Submit approve / reject / delegate actions for a review task.
- `GET /v1/campaigns/{campaignId}/review-tasks`
  - List pending and completed tasks for the authorized actor.

### Reminders and Reassignment

- `POST /v1/campaigns/{campaignId}/reminders`
  - Trigger or schedule reminder actions within allowed release-1 policy.
- `POST /v1/campaigns/{campaignId}/reassignments`
  - Request reviewer reassignment for the confirmed release-1 subset of reassignment flows.
  - **Note**: unsupported reassignment variants should return a structured "not supported in release 1" response rather than inventing behavior.

### Evidence Packages

- `GET /v1/campaigns/{campaignId}/evidence-package`
  - Request or download the evidence package for a campaign visible to the caller's role.
- `GET /v1/campaigns/{campaignId}/audit-events`
  - Read tamper-evident audit history visible to authorized actors.

## Compatibility / Internal Contract Surfaces

### Legacy Coexistence Adapter Contract

- Define a contract between Review Coordination Service and Legacy Coexistence Adapter for:
  - campaign state exchange
  - legacy-read availability checks
  - release-1 evidence visibility coordination

Do **not** expose cutover or migration-only commands as stable release-1 public APIs.

## Error Handling

Use a consistent error envelope:

```json
{
  "error": {
    "code": "UNSUPPORTED_RELEASE1_FLOW",
    "message": "Reviewer reassignment type is not supported in release 1.",
    "details": []
  }
}
```

Representative error classes:

- `VALIDATION_ERROR`
- `FORBIDDEN`
- `NOT_FOUND`
- `CONFLICT`
- `UNSUPPORTED_RELEASE1_FLOW`
- `COMPATIBILITY_STATE_UNAVAILABLE`

## Authorization Boundaries

- Compliance admins may create campaigns, trigger reminders, and request supported reassignment flows.
- Reviewers may fetch and act only on tasks assigned or delegated to them.
- Auditors and authorized admins may fetch evidence packages and audit-event history according to release-1 evidence visibility rules.

## Versioning and Evolution

- Use `/v1/` URL versioning for the external/admin-facing REST surface.
- Preserve additive evolution for release-1 fields where possible.
- Keep compatibility-boundary changes behind the internal adapter contract rather than leaking legacy internals into public endpoints.

## Explicit Open Questions / Deferred Contract Decisions

1. Should legacy/new state consistency be represented to API consumers as near-real-time status freshness or a deferred-sync status model?
2. Which tenant-specific hierarchy variants need explicit contract fields in release 1 versus remaining behind compatibility handling?
3. Which reassignment and data-correction flows require first-class endpoints in release 1, and which should return explicit unsupported responses?
4. Is a dedicated historical-campaign search API needed in release 1, or is legacy-read access plus evidence export sufficient?

## Downstream Handoff

- `feature-development` should implement only the release-1 public contract surfaces above, not migration-only commands.
- `testing-strategy` should derive contract tests for authorization, unsupported release-1 flows, pagination, and error-envelope consistency.
- Future API revisions may add richer compatibility and history surfaces only after architecture decisions close the current open questions.
