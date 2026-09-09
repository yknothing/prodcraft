# Input and Output Contract Notes

## Inputs

- **user-request** -- the raw description of the work to be done
- **existing-context** -- project documentation, recent commits, open issues (read silently before asking questions)

## Quality Target Fields

- `runtime_context`: `agent_internal_skill`, `host_runtime_tool`, `local_dev_harness`, `internal_service`, `public_service`, or `unknown`
- `exposure_profile`: `no_network_listener`, `localhost_only`, `private_network`, `public_internet`, or `unknown`
- `production_target`: the actual deliverable under review
- `non_targets`: excluded products or behaviors
- `evidence_refs`: concrete artifacts or user statements supporting this classification

## Outputs

- **intake-brief** -- structured routing record: request summary, `source_language`, `artifact_record_language`, `user_presentation_locale`, intake mode, work type, entry phase, `quality_target_context`, workflow metadata (`workflow_primary` when governance is explicit, `workflow_overlays` when an overlay is active), next skill, routing rationale, key risks
- **phase-recommendation** -- the lifecycle phase where work should begin
- **workflow-recommendation** -- the methodology best suited to the work
- **route-decision** -- optional strict-mode approved route, workflow focus, obligations, revision, and operator-pinned digest
- **execution-state** -- optional strict-mode initial routed state bound to that route decision
