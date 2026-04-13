# Release 1 API Contract Summary

## Admin-Facing REST Resources

- `POST /v1/campaigns`
- `GET /v1/campaigns`
- `GET /v1/campaigns/{campaignId}`
- `GET /v1/campaigns/{campaignId}/review-tasks`
- `POST /v1/campaigns/{campaignId}/review-actions`
- `POST /v1/campaigns/{campaignId}/reminders`
- `POST /v1/campaigns/{campaignId}/reassignments`
- `GET /v1/campaigns/{campaignId}/evidence-package`
- `GET /v1/campaigns/{campaignId}/audit-events`

## Release-1 Security and Boundary Notes

- unsupported reassignment variants must return structured unsupported-flow responses
- public APIs must not expose migration-only or cutover-only commands
- auditors and admins can fetch evidence packages according to release-1 evidence visibility rules
- compatibility behavior behind the Legacy Coexistence Adapter remains internal
- unresolved sync behavior must remain explicit rather than being silently treated as immediate consistency
