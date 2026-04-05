# Estimation Isolated Benchmark Review

## Scope

This note reviews the first benchmark-grade baseline vs with-skill comparison for `estimation`.

The comparison used the same brownfield planning slice and the same task/risk bundle for both branches.

Runner: `copilot`
Run: `eval/03-planning/estimation/manual-benchmark-run-2026-04-05-copilot-access-review`

## Scenario: Brownfield Access Review Estimate Set

### Baseline

The baseline was directionally useful. It did several important things correctly:

- chose one estimation unit and stayed with it
- sized each task separately
- recorded uncertainty on the higher-risk tasks
- reflected brownfield and sequencing risk in the range

Its main weakness was planning shape. The estimate set was competent, but it was looser on the downstream planning contract:

- confidence was implied through uncertainty ranges rather than called out directly
- assumptions and blockers were present, but not organized as first-class planning inputs
- the output was closer to a good sizing note than a clearly publishable `estimate-set`

### With-Skill

The with-skill branch produced the stronger planning artifact:

- kept a consistent unit in ideal days
- recorded task-by-task size, confidence, assumptions, blockers, and adjustments explicitly
- treated brownfield integration and legacy-boundary verification as estimate wideners rather than background prose
- separated confident work from wide-uncertainty work
- added explicit exclusions and coordination overhead so the output could move into sprint planning without hidden optimism

This is the core contract of the skill: estimation should expose uncertainty and planning pressure, not just produce a number.

## Judgment

This remains a narrow evidence base, but it is now enough for a minimal `tested` posture:

- routed handoff review already proves the downstream boundary into `sprint-planning`
- this benchmark shows stronger uncertainty honesty and planning usability than baseline on the same slice

Remaining gaps are real:

- only one benchmark scenario exists
- there is no later calibration evidence against actual execution yet

Those gaps matter for any later promotion beyond `tested`, but they do not justify keeping the skill at `review` under the repository's current minimal promotion bar.

## Status Recommendation

- Recommended status: `tested`
