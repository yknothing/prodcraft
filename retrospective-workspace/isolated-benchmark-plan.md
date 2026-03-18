# Retrospective Isolated Benchmark Plan

This benchmark tests whether `retrospective` converts execution evidence into a more useful improvement loop than baseline.

## Validity Rules

- baseline and with-skill runs execute in isolated temp workspaces outside the repo
- with-skill branch may read only `./skill-under-test/SKILL.md`
- baseline branch must not read local repo files
- both branches receive the same sprint, release, or incident evidence bundle
- review must compare ownership clarity, improvement quality, and lifecycle routing

## Scenario 1: Sprint Retrospective

Prompt:

`Run the retrospective for this sprint using the attached review findings, defect trends, and delivery notes.`

Assertions:

- converts evidence into a small number of real actions
- assigns owners and deadlines
- avoids generic team-morale commentary as the main output
- routes meaningful follow-up work back into planning or intake

## Scenario 2: Incident-Driven Retrospective

Prompt:

`Run the retrospective for this incident-heavy release cycle and turn the postmortem evidence into next-cycle actions.`

Assertions:

- keeps the output system-focused rather than blame-oriented
- links repeated failures to owned improvement actions
- distinguishes urgent fixes from longer-term process changes
- leaves an artifact future planning can consume

## Pass Criteria

- at least 80% of assertions pass across the benchmark set
- with-skill output is materially more actionable and lifecycle-aware than baseline
