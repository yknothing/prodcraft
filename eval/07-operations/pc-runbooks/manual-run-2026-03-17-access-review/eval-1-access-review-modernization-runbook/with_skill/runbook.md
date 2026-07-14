# Partner-Managed Reassignment Incident Runbook

## Trigger

- Alert: partner-managed reassignment path returns 5xx or latency breach instead of explicit unsupported response
- Severity range: SEV2 unless broader service impact appears
- Owner: on-call responder starts; escalate to incident commander if alert persists beyond 10 minutes

## Procedure

1. Confirm on the responder dashboard that the issue is isolated to partner-managed reassignment and that supported internal reassignment remains healthy.
2. Freeze new deploys for the service.
3. Apply the safer containment branch:
   - if route-level guard is available, force partner-managed reassignment to return `UNSUPPORTED_RELEASE1_FLOW`
   - otherwise initiate rollback to the last known good deployment
4. Check legacy admin fallback availability and notify customer operations if manual fallback is required.
5. Inspect sync worker retry rate and oldest-event age.
   - if retries remain elevated after containment, pause or damp retry pressure according to operational policy
6. Post an internal incident update with current severity, affected flow, containment action, workaround, and next update time.
7. Capture evidence:
   - failing request examples
   - deploy ID
   - dashboard screenshots or metrics for queue/retry state
   - exact time the guard or rollback was applied
8. Verify recovery:
   - partner-managed requests fail explicitly instead of 5xx
   - supported internal reassignment remains healthy if intentionally left enabled
   - sync worker metrics trend back toward baseline
9. If any verification fails, escalate from route-level guard to rollback or broader containment.

## Communication

- Internal cadence: every 20 minutes until the system is stable
- External/support update: required if workaround is active longer than 30 minutes

## Follow-Up

- Open incident postmortem work item
- Update runbook after the incident if any step required improvisation
