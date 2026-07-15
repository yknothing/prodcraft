# Input and Output Contract Notes

## Inputs

- **design-direction** -- Preferred directional input when `pc-problem-framing` has already compared options and selected a path. Treat this as the strongest signal for what release or iteration direction should be converted into requirements.
- **problem-frame** -- Clarifies the problem statement, non-goals, assumptions, open questions, and language-boundary context that requirements must preserve rather than silently resolve.
- **intake-brief** -- Supplemental routing and scope context. Useful for preserving work type, urgency, methodology choice, handoff risks, and the upstream language boundary.
- **market-research-report** -- Market context, competitor gaps, or opportunity framing when the work is still anchored in discovery evidence.
- **user-persona-set** -- User goals, pain points, and behavior patterns that requirements should trace back to.
- **feasibility-report** -- Go/no-go and risk context. Use especially when viability, operational constraints, or timeline limits shape what can become a requirement.

Minimum expectation:

- either an approved `design-direction`, or
- a reviewed discovery evidence set that makes the problem and target user clear enough to write requirements without guessing

If neither exists, stop and route back upstream instead of inventing requirements from vague intent.

When upstream artifacts declare `source_language`, `artifact_record_language`, and `user_presentation_locale`, copy those fields forward instead of re-deciding them implicitly.

## Outputs

- **requirements-doc** -- produced by this skill
