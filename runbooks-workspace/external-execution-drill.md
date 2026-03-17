# Runbook External Execution Drill

## Purpose

Move `runbooks` from "author judged this executable" toward stronger evidence that another responder can follow it without major improvisation.

## What This Means

An "external execution drill" does **not** mean a real outage. It means a second person, or at least a second independent run, follows the runbook against a scenario and reports:

- where they hesitated
- where they lacked decision criteria
- where they needed missing environment detail
- whether verification and communication steps were sufficient

## Minimal Drill Protocol

1. Pick one existing runbook scenario.
2. Give the responder only:
   - the incident summary
   - observability summary
   - the runbook itself
3. Ask them to simulate the response step by step.
4. Record:
   - steps that were ambiguous
   - steps that required tribal knowledge
   - missing branch conditions
   - missing recovery or evidence checks
5. Update the runbook and attach the drill notes as stronger QA evidence.

## Review Threshold

For `runbooks` to move beyond `review`, at least one runbook should pass this drill with only minor clarification edits required.

## Current Status

This protocol is defined, but no external execution drill evidence has been recorded yet.
