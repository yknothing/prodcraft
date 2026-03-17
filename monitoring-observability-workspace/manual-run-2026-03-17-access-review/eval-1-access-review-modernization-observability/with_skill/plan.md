# Observability Plan

## Priority Signals

1. Endpoint health split by flow type:
   - supported internal reassignment success/error/latency
   - partner-managed reassignment attempts, especially any 5xx or non-`UNSUPPORTED_RELEASE1_FLOW` outcomes
2. Sync worker health:
   - queue depth
   - retry rate
   - age of oldest pending event
3. Release state:
   - deploy marker on dashboards
   - rollback or fallback activation marker
4. Legacy fallback health:
   - read-only legacy admin availability

## Alerts

- Page on sustained 5xx or latency breach for supported internal reassignment.
- Page on any partner-managed reassignment path returning 5xx instead of the expected explicit unsupported response.
- Warn on sync worker retry amplification or queue age crossing recovery thresholds.
- Warn if rollback/fallback health checks fail after deploy or containment.

## Dashboards

- Responder dashboard showing:
  - deploy marker
  - supported vs unsupported route behavior
  - sync worker queue and retry trend
  - legacy fallback availability
- Release verification dashboard for the first 30 minutes after deployment.

## Operational Notes

- Every alert should link to the relevant incident or runbook entry.
- Do not merge supported and unsupported path behavior into one aggregate error graph.
- Validate the partner-managed unsupported-flow alert during release verification before treating the setup as ready.
