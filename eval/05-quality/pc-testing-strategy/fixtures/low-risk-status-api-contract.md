# Low-Risk Status API Contract

- `GET /v1/status`
  - returns service status and build metadata
- `GET /v1/healthz`
  - returns lightweight readiness for platform probes

## Constraints

- no auth boundary changes
- no database writes
- no legacy coexistence or migration seam
- response shape must remain JSON and additive
