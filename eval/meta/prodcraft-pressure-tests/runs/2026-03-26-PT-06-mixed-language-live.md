# Live Pressure-Test Record

## Metadata

- `run_id`: `2026-03-26-PT-06-mixed-language-live`
- `scenario_id`: `PT-06-mixed-language-request`
- `evidence_class`: `live`
- `operator`: `codex`
- `date`: `2026-03-26`

## Request

- `request_text`: |
    我们要补一个用户看得见的小功能，但团队内部文档和技术记录仍然要求英文。

    The feature is small, but the request came in mixed Chinese and English, and part of the acceptance criteria is phrased in Chinese.
    I want the routing decision first, and I want to see whether the intake/output boundary between internal artifact language and user-facing language becomes ambiguous.
- `hidden_context_used`: `repo-local Prodcraft contracts only`

## Routing Outcome

- `first_route_correct`: `yes`
- `clarification_rounds`: `0`
- `work_type`: `New Feature`
- `entry_phase`: `01-specification`
- `workflow_primary`: `agile-sprint`
- `workflow_overlays`: `[]`
- `next_skill`: `requirements-engineering`

## Preserved Intake Brief

```markdown
## Intake Brief

**Work type**: New Feature
**Entry phase**: 01-specification
**Intake mode**: full
**workflow_primary**: agile-sprint
**workflow_overlays**: []
**Key skills needed**: requirements-engineering, spec-writing, internationalization
**Scope assessment**: small
**routing_rationale**: Existing product feature, user-visible behavior, and mixed-language acceptance criteria justify specification work before implementation. The route is clear without deeper discovery.
**Key risks**: Canonical artifact language vs user-facing presentation language is still a convention rather than an explicit contract. Acceptance criteria expressed in Chinese may drift when normalized into English-only artifacts.

### Proposed Path
1. requirements-engineering -- normalize the request into a reusable specification artifact
2. spec-writing -- capture the slice, acceptance criteria, and constraints in canonical form
3. internationalization -- review user-facing copy and locale-sensitive behavior before implementation handoff
```

## Evidence

- `cross_cutting_triggered`: `internationalization`
- `artifacts_produced`: `intake-brief`
- `unused_artifacts`: `none observed at intake stage`
- `course_corrections`: `none`
- `low_value_friction`:
  - `intake-brief` has no explicit field for `source_language`
  - `intake-brief` has no explicit field for `user_presentation_locale`
  - the system relies on prose convention to decide which content stays English and which may remain Chinese
- `subtraction_candidate`: `none`

## Judgment

- `essential_or_accidental`: `accidental`
- `follow_up`: `deferred language-boundary task is now justified for intake-brief and other user-facing artifacts`
- `notes`: |
    This run did not reveal routing confusion. The control-plane route is clear:
    a small user-visible feature in an existing system should still enter through
    `01-specification`, with `internationalization` activated because the
    acceptance criteria and user-facing output are multilingual.

    The ambiguity appears one level lower, inside artifact semantics. The repo
    knows by convention that canonical technical artifacts remain English while
    user-facing responses default to Chinese, but the structured artifact
    contract does not declare that boundary. This is not essential complexity in
    the request itself; it is an accidental contract gap.

    Result: the mixed-language live-run trigger described in
    `docs/plans/2026-03-26-prodcraft-pressure-test-protocol.md` is satisfied.
