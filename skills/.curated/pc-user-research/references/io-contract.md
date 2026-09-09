# Input and Output Contract Notes

## Inputs

- **intake-brief** -- Approved audience, goal, scope, and research question. Existing workflow or operator evidence can supply these facts; no extra discovery document is required solely for its name.
- **problem-frame** -- Conditional: reuse its direction, non-goals, and uncertainties when framing ran.
- **design-direction** -- Conditional: consume the selected option and constraints when framing produced it; research does not silently reopen that choice.
- **market-research-report** -- Optional market context for segment selection; not a prerequisite for studying an existing product or internal workflow.

## Outputs

- **research-plan** -- The immediate planning artifact when the skill is invoked before evidence collection. It should name the target segments, hypotheses, methods, evidence threshold, and what question blocks downstream requirements.
- **user-persona-set** -- Evidence-backed personas produced only after research is actually run.
- **user-journey-map** -- Journey map produced only after research evidence is sufficient to describe the primary workflow credibly.

An executable `research-plan` completes a planning-only request. It does not complete evidence collection or satisfy requirements that depend on validated findings. State which decisions remain blocked; hand the plan to the researcher and evidence-backed outputs to requirements work.

When synthesizing already-collected evidence, inspect its sources, methods, and limits; do not create a new research plan unless a remaining question actually requires another study.
