# Code Review QA Findings

## Status

- Current status: `tested`
- Evidence type: routed review plus multiple clean isolated brownfield reruns
- Scope covered:
  - one brownfield review changeset
  - repeated precision reruns with narrower blocker discipline than earlier versions

A second fresh precision rerun now exists in a clean output directory. The remaining noise is much narrower than before, but it should be treated as a known limitation inside a narrow `tested` posture, not as a reason to leave the skill permanently at `review`.

## What Changed

1. A second clean rerun now exists for `access-review-modernization-code-review` in a fresh output directory.
2. Additional precision guardrails removed the prior magic-string nit and the earlier overstated supported-flow regression claim.
3. The remaining defect is now very narrow: the with-skill branch still elevates a checklist-only TODO-without-ticket concern into a blocking finding even though the contract and merge blockers are already captured elsewhere.

## What We Learned

1. On a strong brownfield fixture, the skill's lift is still strongest on blocker ordering and brownfield boundary awareness.
2. Tightening the output contract did help: the rerun is shorter, more review-shaped, and less theatrical than the earlier attempt.
3. The blocker has now narrowed from general false-positive risk to checklist leakage: the model still sometimes turns an internal checklist policy into a standalone blocking finding.

## Current Interpretation

At this stage, `code-review` appears to be:

- a core quality skill on the lifecycle spine
- stronger as a routed workflow skill than as a discoverability-first skill
- now backed by multiple clean isolated brownfield reruns
- no longer blocked by approval-style closure or remediation drift
- strong enough for a narrow `tested` posture even though one checklist-leakage limitation remains

## Next QA Step

Stop tuning broad review-output shape. The remaining work is narrower.

Specifically:

- suppress checklist-only blocker leakage in the next rerun
- do not treat TODO/no-ticket policy reminders as independent blockers unless they create their own release or contract risk
- only after that cleaner rerun exists should the team add the non-brownfield feature changeset promised in the QA strategy
