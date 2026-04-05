# Low-Risk Service Release

- A stateless status API adds a new `GET /v1/healthz` alias and a small logging improvement.
- There is no database migration, no tenant-policy change, and no legacy coexistence boundary.
- The release can roll out normally after tests and a staging smoke check.
- If staging fails, the release should stop before production.
