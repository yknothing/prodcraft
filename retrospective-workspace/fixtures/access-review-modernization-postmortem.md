# Access Review Modernization Postmortem Summary

## Incident

- Partner-managed reassignment requests triggered 5xx responses shortly after deployment.
- The service attempted an immediate legacy sync for a request shape that should have failed with `UNSUPPORTED_RELEASE1_FLOW`.
- Retry pressure in the sync worker amplified latency.

## What Went Well

- Detection happened quickly.
- Legacy admin fallback existed for operations.
- Containment restored stability without evidence of data loss.

## What Went Poorly

- The release boundary was not enforced in production for the unsupported partner-managed path.
- Immediate-sync behavior was assumed even though sync semantics were unresolved.
- Operational communication templates had to be improvised.

## Action Candidates

- strengthen unsupported-flow contract checks
- document safer rollback and fail-closed procedure
- clarify sync semantics before the next release slice
- tighten incident communication templates
