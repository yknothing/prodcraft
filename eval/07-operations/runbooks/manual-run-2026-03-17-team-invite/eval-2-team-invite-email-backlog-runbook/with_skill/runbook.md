# Team Invite Email Backlog Runbook

## Trigger

- Alert: invite dispatch queue age crosses user-visible delay threshold or provider timeout rate spikes
- Severity range: SEV3 by default, escalate to SEV2 if invite acceptance also degrades or queue age keeps increasing after mitigation
- Owner: on-call responder for invite service

## Procedure

1. Confirm whether the incident is limited to email dispatch or also affecting invite acceptance.
2. Freeze non-essential invite-related deploys while triage is active.
3. Check provider timeout rate and queue retry trend.
4. Apply the correct branch:
   - if provider timeout rate is the main issue, reduce retry pressure and pause bulk invite sends
   - if a recent deploy introduced the issue, roll back the invite service to the previous stable release
5. Notify support if user-visible invitation delays exceed the communication threshold.
6. Capture evidence:
   - queue age snapshot
   - provider timeout rate
   - deploy ID if applicable
   - time mitigation started
7. Verify recovery:
   - queue age trends down
   - provider timeout rate returns to baseline
   - invite acceptance remains healthy
8. If recovery does not start within the expected window, escalate severity and engage service owner.

## Communication

- Internal update cadence: every 30 minutes while backlog remains user-visible
- Support update: include expected delay and whether invite acceptance is still healthy

## Follow-Up

- Record whether the mitigation branch worked
- Update the runbook if a missing step or decision point forced improvisation
