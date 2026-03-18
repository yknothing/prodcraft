# User Research Evaluation Strategy

## Scope

This review-stage strategy evaluates `user-research` as a **routed** discovery skill, not as a discoverability-first skill.

The main question is whether the skill improves discovery quality once `intake` or `problem-framing` has already routed the task correctly.

## Why Routed Evaluation Fits

`user-research` is usually invoked after one of these upstream events:

- intake routes directly to discovery research
- problem-framing identifies unresolved user-behavior questions before requirements
- market-analysis narrows which segment is worth validating first

That means review should focus on:

- whether the skill preserves upstream hypotheses, non-goals, and open questions
- whether it turns those into a concrete research plan instead of skipping to requirements
- whether it leaves behind an auditable handoff for downstream lifecycle work

At the current review stage, the artifact under evaluation is often `research-plan`, not yet an evidence-backed persona set. That is acceptable as long as the review clearly states the full user-research quality gate remains open until real evidence exists.

## Review Assertions

For problem-framing handoff scenarios, compare a manual baseline against a with-skill branch using the same input artifact.

Assertions:

1. **Stays in discovery**
   - The output should stop at research planning and evidence gathering, not jump to requirements.
2. **Preserves the chosen direction**
   - Research should validate the framed direction instead of reopening it casually.
3. **Preserves non-goals**
   - The plan should not silently expand into enterprise or adjacent scope that the framing artifact already excluded.
4. **Converts open questions into research questions**
   - The skill should transform unresolved questions into interview prompts and validation hypotheses.
5. **Leaves an auditable handoff**
   - The next-step expectation for personas, journey maps, and later requirements work should be explicit.

## Current Review Scenarios

- `team-invite-problem-framing-handoff`
  - non-brownfield
  - chosen direction: `email-invite-first`
  - reason for research: validate whether early users are lightweight invite teams or enterprise-oriented onboarding buyers
- `seat-guest-management-problem-framing-handoff`
  - brownfield / classic B2B SaaS administration scenario
  - chosen direction: `guest-first coexistence`
  - reason for research: validate whether admins primarily need lightweight external collaboration, tighter seat governance, or procurement-led control before requirements begin

## Evidence Standard

This workspace currently uses **manual branch-pair review**:

- same fixture for baseline and with-skill
- copied `SKILL.md` snapshot in the run directory
- prompts and raw outputs stored for auditability

This is review-stage evidence only. It is **not** isolated benchmark evidence.

## Upgrade Path

Before `user-research` can move beyond `review`, strengthen evidence in one of these ways:

1. add a second scenario, ideally brownfield or legacy-tinged discovery
2. run a semi-isolated or isolated benchmark from the same framing fixture
3. show that downstream `requirements-engineering` materially benefits from the resulting user-research artifacts

## Preferred Benchmark

If only one stronger benchmark is run, prefer:

- `seat-guest-management-problem-framing-handoff`

Why:

- it is the more representative classic B2B/SaaS brownfield case
- it tests whether the skill can preserve coexistence boundaries under legacy-admin pressure
- it is a better stress case than the greenfield-ish `team-invite` path for proving that the skill does not collapse into requirements too early

This benchmark now exists as semi-isolated manual benchmark evidence in:

- `semi-isolated-benchmark-review.md`
