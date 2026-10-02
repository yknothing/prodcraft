# Input and Output Contract Notes

## Inputs

- **user-request** -- the raw description of the work to be done
- **existing-context** -- project documentation, recent commits, open issues (read silently before asking questions)

## Language Selection

1. An explicit language request takes precedence over detection or an earlier locale.
2. Otherwise match the current substantive request: English requests receive English; Chinese requests receive Chinese. For mixed prose use its dominant language; retain the established presentation locale when ambiguous. Do not ask a language question when these rules suffice.
3. Ignore code, commands, paths, API names, and quoted source text when detecting the request language. A Chinese comment in an English coding request does not switch the reply language.
4. Update `user_presentation_locale` on a substantive follow-up in another language without repeating intake or approval.
5. Localize prose, headings, questions, human-facing tags, status labels, and completion feedback. An English template heading is a display label to translate, not a fixed user-facing string.
6. Preserve canonical machine fields/enums, skill IDs, code, commands, paths, API names, and quoted original diagnostics. For example, display a localized approval label while storing the enum `approved` unchanged.
7. Write new task record prose in `user_presentation_locale` and set `artifact_record_language` to the actual record language. An explicitly requested separate record language takes precedence. Existing English records remain valid; do not translate or rewrite historical evidence merely because presentation changes. For compact micro records the locale fields may be omitted; apply the same language selection to their prose.

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

For a stored machine-readable brief, `scope_assessment` is `small`, `medium`,
`large`, or `xlarge`; put scope explanations in `routing_rationale`. Check the
record against the available schema/validator before downstream acceptance.
User approval and structural validity are separate checks; a malformed field
does not require repeating an unchanged user decision.

## Micro Record

Required fields: `artifact=intake-brief`, `schema_version=intake-brief.v1`,
`status=approved`, `intake_mode=micro`, `approver=auto (micro policy)`,
`request_summary`, `recommended_next_skill`, `routing_rationale`,
`quality_target_context` (runtime and exposure), and `micro_eligibility`.
The five eligibility fields are `single_revert`, `zero_questions`,
`no_external_effect`, `no_security_impact`, and `no_irreversible_action`, all true.
Runtime must be `agent_internal_skill`, `host_runtime_tool`, or `local_dev_harness`;
exposure must be `no_network_listener` or `localhost_only`.

Locale, work type, phase, scope, risks, and question fields may be omitted for
micro. If supplied, work type is `Documentation`, `Enhancement`, `Bug Fix`, or
`Refactoring`; scope is `small`, questions are empty, and
`routing_changed_by_answers=false`. Omit `workflow_primary`. The next skill
must exist. Other modes retain the full required schema fields; the compact
form must not be reused as a full or resume brief. The host retains tool authority.
