# Input and Output Contract Notes

## Inputs

- **design-direction** -- Preferred directional input when `pc-problem-framing` has already compared options and selected a path. Treat this as the strongest signal for what release or iteration direction should be converted into requirements.
- **problem-frame** -- Clarifies the problem statement, non-goals, assumptions, open questions, and language-boundary context that requirements must preserve rather than silently resolve.
- **intake-brief** -- Sufficient directional input when it records an approved outcome, affected users/workflow, scope, and known constraints. Preserve urgency, methodology, handoff risks, and language boundaries.
- **market-research-report** -- Market context, competitor gaps, or opportunity framing when the work is still anchored in discovery evidence.
- **user-persona-set** -- User goals, pain points, and behavior patterns that requirements should trace back to.
- **feasibility-report** -- Go/no-go and risk context. Use especially when viability, operational constraints, or timeline limits shape what can become a requirement.

Minimum expectation:

- an approved intake or existing product/change brief with a clear outcome and target user/workflow; or
- an approved `design-direction`; or
- a reviewed discovery evidence set that makes the problem and target user clear enough to write requirements without guessing

Clarify only missing facts that prevent requirements from being stated without guessing. Use upstream framing when the direction is unresolved, not merely because a named artifact is absent. Missing discovery evidence limits claims about user demand; it does not erase an explicitly requested behavior change.

Preserve upstream `source_language` and use the current `user_presentation_locale` for new requirements prose and headings. Set `artifact_record_language` to the actual record language; an explicit record-language request takes precedence. A follow-up language switch changes new presentation without translating or renumbering accepted source evidence.

## Outputs

- **requirements-doc** -- Approved scope, prioritized behavior, sources, measurable acceptance intent, non-goals, and owned questions. Feed specification, acceptance-criteria, and architecture work; a section in an existing approved document is sufficient when the workflow permits it.
