# Intake Brief

Use this template whenever `pc-intake` routes new work into a workflow.

## Required Artifact

- artifact: `intake-brief`
- schema_version: `intake-brief.v1`
- status:
- approver:

## Work Summary

- request_summary:
- source_language: `BCP-47 locale such as en or zh-Hans, or mixed`
- artifact_record_language: `en`
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
- why intake was used:
- proposed_path: `ordered skill names, when more than the next skill is already clear`

## Question Budget

- questions_asked:
- routing_changed_by_answers:
- if more than 3 questions were needed, why?

## Alternatives Considered

- primary path chosen:
- alternative path considered:
- trade-off summary:

## Key Risks

- key_risks:
  - 
  - 

## Fast-Track or Skipped Gates

- any shortcut taken? yes / no
- if yes, why was it acceptable?
- what debt does this create?

## Notes for Handoff

- constraints:
- open questions:
- context that downstream skills must preserve:
- should `pc-problem-framing` run next? yes / no

## Micro Mode Compact Form

For `intake_mode: micro`, emit the brief as one compact block in the same
message as the work instead of filling the full template. Every schema-required
field appears once, one line each. Micro is limited to `Documentation`,
`Enhancement`, `Bug Fix`, or `Refactoring` work on an `agent_internal_skill`,
`host_runtime_tool`, or `local_dev_harness` with `no_network_listener` or
`localhost_only` exposure. `questions_asked` must be empty,
`routing_changed_by_answers` must be `false`, and every route name must be a
canonical implemented `pc-*` skill:

```
artifact: intake-brief | schema_version: intake-brief.v1 | intake_mode: micro
status: approved | approver: auto (micro policy)
micro_eligibility: single_revert=true | zero_questions=true | no_external_effect=true |
  no_security_impact=true | no_irreversible_action=true
request_summary: fix typo in README quick-start command
source_language: en | artifact_record_language: en | user_presentation_locale: en
work_type: Documentation | entry_phase: cross-cutting
quality_target_context: runtime_context=agent_internal_skill, exposure_profile=no_network_listener,
  production_target=repo docs, non_targets=[behavior change], evidence_refs=[README.md diff]
scope_assessment: small | recommended_next_skill: pc-documentation
routing_rationale: single-line reversible doc fix, unambiguous route
key_risks: none beyond doc accuracy | questions_asked: [] | routing_changed_by_answers: false
```
