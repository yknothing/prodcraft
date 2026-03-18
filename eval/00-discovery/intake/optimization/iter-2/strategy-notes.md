# Intake Iteration 2 Strategy Notes

## Core conclusion

`intake` is best treated as an **encoded preference routing skill**, not a capability-uplift skill.

Its differentiator is not raw problem solving. Its differentiator is:

- classify first
- choose phase and workflow
- surface risks
- get approval before downstream work

This matches Anthropic's March 3, 2026 guidance on encoded preference skills: value comes from fidelity to the workflow, not from teaching Claude net-new technical capability.

## What the current evals revealed

Iteration 1 already showed two distinct phenomena:

1. **Core wins**:
   - greenfield
   - migration
   - vague "not sure where to start"

2. **Overlap losses**:
   - feature requests vs brainstorming
   - hotfix / incidents vs debugging
   - major refactors vs module-design

These are not the same kind of miss.

## Why the description strategy changed

The previous description tried to win by:

- explicitly naming competing skills
- claiming upstream priority
- covering almost every new-work scenario

That creates two problems:

1. It is less aligned with Anthropic's "one focused workflow" guidance.
2. It optimizes for competition with other process skills instead of for `intake`'s clearest trigger territory.

## New hypothesis

The best next description should:

- say **what the skill does** and **when to use it**
- center `intake` on routing / triage
- prioritize high-signal core use cases
- mention overlap cases only as secondary
- avoid naming competitor skills in the metadata

## What success should mean

For `intake`, trigger success should be read in three layers:

1. **Core recall**
   - new product
   - migration
   - broad initiative
   - vague "where do I start?"

2. **Non-trigger precision**
   - typo
   - command execution
   - PR review
   - known test-writing task
   - pure Q&A

3. **Overlap diagnostics**
   - not pure failures
   - evidence about routing collisions with other process skills

## Immediate next step

Rerun trigger evaluation against:

- `trigger-core.json`
- `trigger-overlap.json`
- `trigger-non-trigger.json`
- the existing mixed set, if desired for continuity

Then compare:

- core recall delta
- non-trigger precision
- overlap-case notes

Do not judge the new description on one blended score alone.
