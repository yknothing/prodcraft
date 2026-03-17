# Baseline Incident Plan

## Severity

- Treat as SEV3 unless impact grows, because email delivery is delayed but the core product is still up.

## Immediate Actions

1. Open an incident channel.
2. Check queue health, provider status, and recent deploys.
3. Notify support that invite emails may be delayed.
4. Consider scaling workers or rolling back if a recent deploy caused the issue.

## Investigation

- Review provider logs and timeout trends.
- Inspect queue depth and retry behavior.
- Check whether any new deployment changed invite delivery behavior.

## Follow-Up

- Confirm recovery when queue metrics improve.
- Write a postmortem if delays were user-visible for a meaningful period.
