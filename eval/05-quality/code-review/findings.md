# Code Review QA Findings

## Summary

`code-review` remains at `review`.

A usable isolated benchmark result now exists, but the current primary run directory contains appended rerun history and the latest completed output still shows review-discipline issues that block `tested`.

## What Changed

1. A usable isolated benchmark result now exists for `access-review-modernization-code-review`.
2. The benchmark confirms that both baseline and with-skill branches surface the core contract and brownfield blockers on the same fixture.
3. The with-skill branch also shows a concrete quality defect: it drifts into implementation advice, approval-style closure, and duplicate checklist noise.

## What We Learned

1. On a strong brownfield fixture, the skill's lift is not just "finds blockers" but "keeps blocker ordering and boundary awareness sharper than baseline."
2. The skill reliably keeps contract violations, unsupported-flow handling, and coexistence risks visible.
3. The current skill wording still over-activates checklist enforcement and remediation language, which makes the output noisier than the benchmark plan allows.

## Current Interpretation

At this stage, `code-review` appears to be:

- a core quality skill on the lifecycle spine
- stronger as a routed workflow skill than as a discoverability-first skill
- now backed by one usable isolated brownfield benchmark
- still too noisy and approval-shaped to leave `review`

## Next QA Step

Tighten the review-output discipline on the skill and rerun the same isolated brownfield scenario.

After a cleaner rerun exists, add a non-brownfield feature changeset to verify the skill does not overfit to compatibility-heavy review.
