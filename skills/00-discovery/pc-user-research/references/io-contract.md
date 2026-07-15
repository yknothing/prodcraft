# Input and Output Contract Notes

## Inputs

- **intake-brief** -- produced by the preceding skill in the lifecycle
- **problem-frame** -- produced by the preceding skill in the lifecycle
- **market-research-report** -- produced by the preceding skill in the lifecycle

## Outputs

- **research-plan** -- The immediate planning artifact when the skill is invoked before evidence collection. It should name the target segments, hypotheses, methods, evidence threshold, and what question blocks downstream requirements.
- **user-persona-set** -- Evidence-backed personas produced only after research is actually run.
- **user-journey-map** -- Journey map produced only after research evidence is sufficient to describe the primary workflow credibly.

If only `research-plan` exists, the discovery work is better framed but the skill's full quality gate is still open. Do not pretend that planning alone equals validated research.
