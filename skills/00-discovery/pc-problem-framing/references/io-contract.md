# Input and Output Contract Notes

## Inputs

- **intake-brief** -- Must identify the work type, entry phase, recommended workflow, key risks, `quality_target_context`, and the next likely skill.
  Preserve `source_language` and current `user_presentation_locale`; honor any explicit separate record-language request and record the actual language of the new artifact in `artifact_record_language`. If compact intake omitted locale fields, derive them from the current substantive request using the intake language-selection rules. Preserve `quality_target_context` so downstream quality and security work does not reconstruct the runtime or exposure boundary from guesses.

## Outputs

- **problem-frame** -- The clarified problem, constraints, and non-goals
- **options-brief** -- Small set of viable directions with trade-offs
- **design-direction** -- Approved recommendation plus next lifecycle destination
