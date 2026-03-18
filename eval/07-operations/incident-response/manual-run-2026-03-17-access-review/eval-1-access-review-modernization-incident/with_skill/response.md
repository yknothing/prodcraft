# Incident Response Plan

## Severity and Scope

- Classify as SEV2.
- Impact is limited to partner-managed reassignment requests, but the route is live in production and retry pressure is increasing.
- Supported internal reassignment flows still work, and the legacy admin path remains available as a manual fallback.

## Command Structure

- Incident commander: tech lead for the release slice
- Technical responder: on-call engineer for access-review service plus one engineer for sync worker analysis
- Communications lead: engineering manager or designated support lead
- Internal update cadence: every 20 minutes until containment is confirmed
- External update trigger: publish a customer/support note if impact lasts more than 30 minutes or workaround volume becomes material

## Immediate Containment

1. Freeze additional production deploys for the service.
2. Fail closed on partner-managed reassignment requests immediately:
   - if a route-level guard can be applied safely, return the expected `UNSUPPORTED_RELEASE1_FLOW`
   - otherwise roll back the release slice to the last known good deployment
3. Keep supported internal reassignment flow available only if it can remain isolated from the failing partner-managed path.
4. Pause or damp retry pressure from the legacy sync worker to stop backlog amplification while containment is in effect.
5. Direct customer operations to the existing legacy admin workaround until the service is stable.

## Evidence Capture

- Preserve logs, traces, and deploy metadata for the 20-minute window before and after the alert.
- Record the exact rollback or route-block decision and when it was applied.
- Capture representative failing requests that show partner-managed input reaching an immediate-sync path.
- Record queue depth and retry-rate metrics before and after mitigation.

## Investigation After Containment

- Confirm whether partner-managed requests bypassed the intended release boundary instead of returning `UNSUPPORTED_RELEASE1_FLOW`.
- Verify whether the service assumed immediate legacy synchronization despite that remaining unresolved in the reviewed architecture.
- Check whether any data mutation occurred before the 5xx path; if uncertain, keep the route in the safer fail-closed mode.
- Compare behavior against the reviewed architecture and CI/CD release assumptions rather than guessing from code alone.

## Recovery Criteria

Do not declare recovery until all of the following are true:
- endpoint error rate and latency have returned to baseline
- unsupported partner-managed requests fail explicitly and safely
- sync worker retry pressure is back to normal
- the temporary workaround and any remaining guardrails are documented

## Stakeholder Updates

- Internal update template:
  - current severity and affected flow
  - containment action taken
  - current workaround
  - next update time
- External/support update:
  - partner-managed reassignment is temporarily unavailable
  - internal reassignment remains available if confirmed safe
  - legacy admin workaround is available while mitigation remains active

## Post-Incident Handoff

- Open follow-up work for the permanent contract fix that forces unsupported variants to fail closed.
- Hand off operational cleanup to `runbooks` so the fail-closed/rollback procedure is documented.
- Hand off systemic lessons to `retrospective` and `tech-debt-management`, including missing release-boundary protection and sync-behavior ambiguity.
