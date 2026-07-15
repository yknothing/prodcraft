# Input and Output Contract Notes

## Inputs

- **intake-brief** -- Must identify the work type, entry phase, recommended workflow, key risks, `quality_target_context`, and the next likely skill.
  Preserve the intake language boundary fields instead of silently guessing them away: `source_language`, `artifact_record_language`, and `user_presentation_locale`. Preserve `quality_target_context` so downstream quality and security work does not reconstruct the runtime or exposure boundary from guesses.

## Outputs

- **problem-frame** -- The clarified problem, constraints, and non-goals
- **options-brief** -- Small set of viable directions with trade-offs
- **design-direction** -- Approved recommendation plus next lifecycle destination
