# Input and Output Contract Notes

## Inputs

- **user-request** -- the raw description of the work to be done
- **existing-context** -- project documentation, recent commits, open issues (read silently before asking questions)

## Outputs

- **intake-brief** -- structured routing record: request summary, `source_language`, `artifact_record_language`, `user_presentation_locale`, intake mode, work type, entry phase, `quality_target_context`, workflow metadata (`workflow_primary` when governance is explicit, `workflow_overlays` when an overlay is active), next skill, routing rationale, key risks
- **phase-recommendation** -- the lifecycle phase where work should begin
- **workflow-recommendation** -- the methodology best suited to the work
- **route-decision** -- optional strict-mode approved route, workflow focus, obligations, revision, and operator-pinned digest
- **execution-state** -- optional strict-mode initial routed state bound to that route decision
