# Intake Brief

Translate headings and human-readable values into the requested language. Lead with the work's descriptive title; preserve machine fields, enums, and existing references.
Use this template whenever `pc-intake` routes new work into a workflow.

## Required Artifact

- artifact: `intake-brief`
- schema_version: `intake-brief.v1`
- status:
- approver:

## Work Summary

- request_summary:
- source_language: `BCP-47 locale such as en or zh-Hans, or mixed`
- artifact_record_language: `BCP-47 locale of record prose; normally user_presentation_locale`
- user_presentation_locale: `BCP-47 locale`
- intake_mode:
- work_type:
- entry_phase:
- quality_target_context:
  - runtime_context: `agent_internal_skill` / `host_runtime_tool` / `local_dev_harness` / `internal_service` / `public_service` / `unknown`
  - exposure_profile: `no_network_listener` / `localhost_only` / `private_network` / `public_internet` / `unknown`
  - production_target:
  - non_targets:
    -
  - evidence_refs:
    -
- workflow_primary: `required for full/resume; omit when fast-track or micro routing keeps the primary workflow implicit`
- workflow_overlays: `omit when no overlay is active`
- scope_assessment:
- urgency:

## Routing Decision

- recommended_next_skill:
- routing_rationale:
- existing approval and artifact references: `include in routing_rationale when resuming; record the actual user authority`
- proposed_path: `ordered skill names, when more than the next skill is already clear`

## Question Budget

- questions_asked:
- routing_changed_by_answers:

## Key Risks

- key_risks:
  - 
  - 

Record a meaningful alternative, shortcut rationale, or authorized gate change in routing_rationale only when applicable. A note does not waive a blocking gate.

## Notes for Handoff

- constraints:
- open questions:
- context that downstream skills must preserve:
- accepted artifact paths/revisions and the next skill's acceptance condition:

## Micro Mode Compact Form

Present only the concrete change, its low risk, and verification in one or two
sentences in the requested language. Save the machine record below only when the
runtime or downstream consumer needs it; do not print it as a second user report.
The compact form requires 10 top-level fields. Locale and classification fields
are optional; old expanded micro records remain valid. All five eligibility
assertions must be true. Supplied questions must be empty, scope must be small,
and workflow_primary must be absent. The existing full/fast-track/resume form
above keeps its required fields.

```json
{
  "artifact": "intake-brief",
  "schema_version": "intake-brief.v1",
  "status": "approved",
  "intake_mode": "micro",
  "approver": "auto (micro policy)",
  "request_summary": "Fix a typo in the README quick-start explanation",
  "recommended_next_skill": "pc-documentation",
  "routing_rationale": "One reversible wording change; verify the diff contains no command or behavior change",
  "quality_target_context": {
    "runtime_context": "agent_internal_skill",
    "exposure_profile": "no_network_listener"
  },
  "micro_eligibility": {
    "single_revert": true,
    "zero_questions": true,
    "no_external_effect": true,
    "no_security_impact": true,
    "no_irreversible_action": true
  }
}
```

The host still owns tool permission. The Claude adapter treats this record as
bookkeeping and asks for native confirmation on each actual work write.
