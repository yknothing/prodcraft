# Requirements Engineering Eval Strategy

`requirements-engineering` is an upstream specification skill. Its QA should verify two things separately:

1. **Triggering**: it appears for real requirements-definition work and stays out of execution, design, and review tasks.
2. **Execution quality**: when explicitly invoked, it produces precise, prioritized, traceable requirements rather than vague notes or solutioning.

For the first pass, prioritize trigger accuracy so this skill can enter the official `skill-creator` pipeline with a clean scope.

## Current Findings (2026-03-16)

Trigger eval has now been run three times with progressively sharper descriptions:

1. `results-trigger-iter1.json` -- initial migrated description
2. `results-trigger-iter2-baseline.json` -- explicit what+when description after fixing wrapped frontmatter
3. `results-trigger-iter3.json` -- upstream-positioned routing description

All three runs produced the same outcome:

- positive recall: `0/4`
- negative precision: `6/6`

Interpretation:

- The skill package itself is structurally valid.
- The problem is not just frontmatter formatting.
- In the current local skill ecosystem, `requirements-engineering` is not winning discovery against broader competing skills.

Decision:

- Keep `requirements-engineering` in `review` status.
- Do not continue endless description-only iterations.
- Move the next QA step to explicit invocation quality and chain quality (`intake` -> `requirements-engineering`), because that is the more meaningful measure for an upstream specification skill.
