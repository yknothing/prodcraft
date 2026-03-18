# Access Review API Contract Draft

## Services and Endpoints

### Review Coordination API

- `POST /v1/campaigns`
- `GET /v1/campaigns/{campaignId}`
- `POST /v1/campaigns/{campaignId}/reminders`
- `POST /v1/campaigns/{campaignId}/reassign`
- `POST /v1/campaigns/{campaignId}/sync`

### Reviewer Policy API

- `POST /v1/policies/evaluate`
- `PUT /v1/tenants/{tenantId}/hierarchy-rules`

### Evidence API

- `GET /v1/campaigns/{campaignId}/evidence-package`
- `GET /v1/campaigns/{campaignId}/audit-events`

### Legacy Migration API

- `POST /v1/legacy/import-historical-campaigns`
- `POST /v1/legacy/cutover`

## Response Shape

- All endpoints return JSON.
- Error format:
  - `code`
  - `message`

## Authorization

- Admins can create campaigns and manage reassignment.
- Reviewers can complete assigned actions.
- Auditors can download evidence packages.

## Versioning

- Use `/v1/` URL versioning.

## Assumptions

- New and legacy systems will synchronize on the same day using the `/sync` endpoint.
- Historical campaigns will be imported into the new platform over time.

## Next Step

Write OpenAPI specs for all endpoints and build the sync and cutover APIs first.
