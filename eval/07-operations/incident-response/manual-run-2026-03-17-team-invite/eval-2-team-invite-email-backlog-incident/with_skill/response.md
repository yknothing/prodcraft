# Incident Response Plan

## Severity and Scope

- Classify as SEV3 initially.
- Impact is limited to delayed invite email delivery, but the delay is user-visible and may escalate if queue age keeps growing or acceptance starts failing too.

## Command Structure

- Incident commander: invite-service owner or on-call tech lead
- Technical responder: on-call engineer for queue/provider integration
- Communications lead: support lead or engineering manager
- Internal update cadence: every 30 minutes while delays remain user-visible
- External/support update trigger: immediately if queue age exceeds the published delay threshold or if backlog continues growing after mitigation

## Immediate Containment

1. Freeze non-essential deploys that could complicate diagnosis.
2. Reduce blast radius:
   - pause bulk invite sends if they are contributing to the queue surge
   - consider reducing retry pressure if provider timeouts are amplifying backlog
3. Keep invite creation available if it does not worsen queue recovery; otherwise degrade the flow explicitly with a user-facing delay notice.
4. Notify support with current scope, expected delay, and whether invite acceptance remains healthy.

## Evidence Capture

- Record queue age, retry rate, and provider timeout rate at the start of the incident.
- Capture deploy markers or config changes near the time the alert began.
- Record when any mitigation branch started and whether queue age began recovering.

## Investigation After Containment

- Verify whether the incident is provider-driven, retry-driven, or deploy-driven.
- Check whether invite creation is feeding backlog faster than delivery can recover.
- If acceptance health starts degrading too, raise severity and widen containment.

## Recovery Criteria

- Queue age trends back under the user-visible delay threshold
- Provider timeout rate returns toward baseline
- Support updates no longer need delay messaging
- Invite acceptance remains healthy throughout recovery

## Post-Incident Handoff

- Hand off reusable operational steps to `runbooks`
- Capture alert and dashboard improvements for `monitoring-observability`
- Open follow-up work only if delivery controls, queue policy, or provider handling need structural change
