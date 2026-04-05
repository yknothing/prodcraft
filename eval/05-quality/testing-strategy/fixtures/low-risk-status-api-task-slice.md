# Low-Risk Status API Task Slice

## Goal

Add a lightweight status endpoint and a health alias for the approvals service.

## Scope

- expose `GET /v1/status`
- keep `GET /v1/healthz` available
- include build metadata in the status response

## Constraints

- no new persistence
- no queue changes
- no rollout complexity beyond normal staging verification
