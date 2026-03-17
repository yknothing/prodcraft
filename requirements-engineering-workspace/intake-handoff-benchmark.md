# Intake-to-Requirements Handoff Benchmark

This benchmark evaluates whether `requirements-engineering` correctly inherits and preserves an approved `intake-brief`.

## Goal

Measure whether the skill:

- respects intake-imposed phase boundaries
- preserves scope, risks, and open questions from the handoff artifact
- avoids collapsing back into architecture or generic brainstorming

## Core Scenario

- `approvals-intake-handoff`
- `access-review-modernization-handoff`

These scenarios provide:

- an approved intake brief
- discovery notes for an approvals workflow feature
- discovery notes for a brownfield access-review modernization effort
- both artifacts as separate context files, so the benchmark mirrors handoff behavior without bloating the prompt

The evaluation looks for:

- preservation of `01-specification` scope
- a requirements artifact rather than design output
- carry-through of intake risks and open questions
- preservation of brownfield coexistence boundaries where applicable
- explicit avoidance of unsupported precision

## Pass Criteria

- Output remains clearly in the requirements layer
- Brownfield scenarios preserve release-1 coexistence constraints instead of assuming a rewrite or immediate cutover
- At least one intake risk is preserved or reflected in the resulting requirements/open questions
- At least one intake open question is preserved rather than silently resolved
- Output is shaped for handoff to downstream `spec-writing` / `acceptance-criteria`
