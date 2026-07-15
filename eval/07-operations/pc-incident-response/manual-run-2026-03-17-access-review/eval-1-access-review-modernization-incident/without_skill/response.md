# Baseline Incident Plan

## Severity

- Treat as SEV2 because a production feature is failing for a meaningful slice of users, but a workaround exists and the whole product is not down.

## Immediate Actions

1. Acknowledge the incident and open an incident channel.
2. Assign an incident commander and one engineer to investigate logs and traces.
3. Pause new production deployments until the issue is understood.
4. Review the last deployment and consider rollback if the issue worsens.
5. Scale the affected worker if backlog keeps growing.

## Communication

- Notify engineering leadership and support that there is an active incident.
- Share an internal update every 30 minutes until impact stabilizes.
- Prepare a customer-facing update if the incident lasts longer than 1 hour.

## Investigation

- Review logs for the failing endpoint.
- Check whether the latest deployment introduced a regression.
- Confirm whether the sync worker is contributing to latency.
- Verify whether partner-managed requests are expected to work in this release.

## Recovery

- If a safe code fix is obvious, deploy it with extra monitoring.
- Otherwise, roll back to the previous version.
- Watch errors and latency until the service stabilizes.

## Follow-Up

- Write a postmortem within 48 hours.
- Add more endpoint tests and monitor coverage for reassignment flows.
