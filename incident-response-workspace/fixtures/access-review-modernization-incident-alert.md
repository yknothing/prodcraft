# Access Review Modernization Incident Alert

## Detection

- 12 minutes after production deployment, alerting reports a spike in 5xx responses on `POST /access-review/reassignments`.
- Error rate for the endpoint has reached 17 percent over 10 minutes.
- p95 latency for the same route is above 4 seconds.

## Scope Observed

- Supported internal reassignment flows still succeed.
- Failures cluster around partner-managed reassignment requests that should have been rejected for release 1.
- The legacy sync worker is retrying aggressively and backlog is increasing.
- Customer operations still has a manual workaround through the legacy admin experience.

## Early Evidence

- Logs suggest the service attempted an immediate legacy sync for a request shape that should have failed closed.
- No evidence yet of data loss, but duplicate retry pressure is increasing.
- No security breach signal is present.
