# Observability Plan

## Priority Signals

1. Invite creation success and latency
2. Email dispatch queue age, retry rate, and provider timeout rate
3. Invite acceptance success rate and token-validation failures
4. Release markers for deploy and rollback events

## Alerts

- Warn on invite dispatch queue age crossing user-visible delay threshold.
- Page on sustained provider timeout rate or invite acceptance failure spike.
- Warn when token-validation failures exceed expected baseline after deploy.

## Dashboards

- Responder dashboard with:
  - invite creation vs acceptance health
  - dispatch queue age and retry trend
  - provider timeout rate
  - deploy markers for correlation

## Operational Notes

- Keep invite dispatch and invite acceptance visible as separate boundaries.
- Validate post-deploy that invite creation and invite acceptance remain healthy before treating the release as complete.
