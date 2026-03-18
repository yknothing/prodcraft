# Intake Trigger Eval Strategy

## Why split the eval set

`intake` is a routing skill. That makes trigger evaluation structurally different from evaluating a leaf skill like `code-review` or `tdd`.

Some prompts are:

- **core intake cases**: the main value is triage and routing
- **overlap cases**: multiple skills can reasonably claim them
- **clear non-trigger cases**: specific execution, review, debugging, or Q&A tasks

If all of these are mixed into one binary trigger score, the metric becomes hard to interpret:

- low recall may mean the description is weak
- or it may mean another high-priority skill is winning
- or it may mean the task is already sufficiently scoped and should fast-track

## Evaluation buckets

### 1. Core trigger set

These are prompts where `intake` should be the strongest or most defensible trigger:

- new product / greenfield
- large migration / modernization
- vague "not sure where to start" requests
- multi-sprint tech debt initiative
- broad documentation initiative

This bucket measures whether the description can surface the skill in its highest-signal territory.

### 2. Overlap trigger set

These are prompts where `intake` competes with other process skills:

- new feature requests vs `brainstorming`
- hotfix / bug / incident vs `systematic-debugging`
- large refactor vs `module-design`
- compliance / architecture-heavy work vs `software-architecture`

This bucket should not be read as a pure "right or wrong" trigger metric. It measures routing competition.

### 3. Non-trigger set

These are tasks already in progress or too narrow to justify intake:

- typo fix
- rename one function
- run a command
- review a PR
- debug a specific stack trace
- write tests for a known function
- answer a technical question

This bucket measures false-positive control.

### 4. Mixed continuity set

Keep the original `trigger-eval.json` as a continuity benchmark only.

Use it to compare against earlier iterations, but do not let its single blended score override the bucketed interpretation above.

## Interpretation rules

- **Core recall** is the most important trigger metric for `intake`.
- **Non-trigger precision** must remain high.
- **Overlap cases** should be analyzed qualitatively, not collapsed into the same meaning as core misses.

## Practical rule

When reporting intake trigger quality, use:

1. Core trigger recall
2. Non-trigger precision
3. Overlap case notes
4. Mixed-set continuity score

Do not treat all positive misses as equivalent.

## Success thresholds for iteration 2

- **Core recall target**: at least 4/5 core prompts should trigger.
- **Non-trigger precision target**: 10/10 non-trigger prompts should stay non-trigger.
- **Overlap target**: document which competing skill wins each case; do not force a binary pass/fail interpretation.
- **Mixed continuity target**: do not accept a large blended-score regression unless core recall clearly improves and false positives stay controlled.

## Post-Redesign Follow-Up (2026-03-17)

`intake` has since been tightened as the first layer of a two-step entry stack:

- `intake` handles routing and path comparison
- `problem-framing` handles deeper option shaping when routing is already clear

Because the body contract changed, the old trigger and benchmark evidence should be treated as historically useful but not fully current.

The next intake QA pass should verify:

1. **Core discoverability still holds** for the strongest entry prompts.
2. **Question load remains low** after the tighter routing-only positioning.
3. **Observability improves** because the `intake-brief` now records why intake was used, which answers changed routing, and what skill is next.
4. **Handoff discipline improves** by routing fuzzy post-intake cases to `problem-framing` instead of stretching intake into a full design conversation.
