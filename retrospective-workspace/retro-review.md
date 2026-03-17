# Retrospective Review

## Goal

Verify that `retrospective` converts incident and review evidence into a small set of owned, routed improvement actions.

## Scenario

- `access-review-modernization-retrospective`

This is a brownfield modernization follow-up where:

- a release-boundary breach caused a production incident
- multiple earlier review stages had already identified related risks
- the team needs to turn the learning into the next cycle's work instead of repeating generic lessons

## Artifacts Reviewed

- Manual baseline retrospective: `manual-run-2026-03-17-access-review`
- Input fixtures:
  - `fixtures/access-review-modernization-postmortem.md`
  - `fixtures/access-review-modernization-review-summary.md`

## Baseline Findings

The baseline output is reasonable but too generic:

- it lists "improve testing" and "improve communication"
- it does not route actions back into the lifecycle
- it loses the specific release-boundary lesson

## With-Skill Findings

The skill-applied output is stronger on the dimensions that matter for lifecycle-aware evolution:

- it stays grounded in postmortem and review evidence
- it limits the action set to a small number of high-leverage improvements
- it assigns owners, timing, and next lifecycle destination
- it preserves the system-level lesson instead of collapsing into generic process advice

## Assertion Review

| Assertion | Baseline | With skill | Notes |
|---|---|---|---|
| uses evidence rather than vague sentiment | partial | pass | With-skill traces actions back to the actual postmortem and review chain. |
| produces a small actionable set | partial | pass | Baseline is vague; with-skill picks four concrete actions. |
| routes actions back into the lifecycle | fail | pass | With-skill explicitly maps each action to intake and downstream phases. |
| preserves system-level learning | partial | pass | With-skill focuses on release-boundary discipline rather than blame or morale platitudes. |
| supports recurrence reduction | partial | pass | With-skill actions are better aligned to preventing the same failure mode. |

## Conclusion

The first manual review suggests `retrospective` also fits the emerging core pattern:

- it is more valuable as a routed/core workflow skill than as a discoverability-first skill
- its value comes from converting evidence into a small number of lifecycle-aware improvements the system can actually absorb

This is review-stage evidence only. The next step is a second retrospective scenario that is not incident-driven plus stronger coupling to `tech-debt-management`.
