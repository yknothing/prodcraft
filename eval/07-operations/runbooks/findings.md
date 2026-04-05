# Runbooks Findings

## Status

- Current status: `tested`
- Evidence type: manual routed review plus manual branch-pair benchmark
- Scope covered:
  - one brownfield incident runbook scenario
  - one non-brownfield incident runbook scenario

## What Improved

- The skill now emphasizes executable procedure instead of generic operational prose.
- Output quality improves when the skill is used explicitly with incident and signal context.
- The resulting runbook is better aligned with incident-response and observability evidence.
- A stricter single-author replay found only minor threshold/policy ambiguity rather than structural failure.
- The manual branch-pair benchmark shows a clear skill lift over baseline on trigger clarity, containment, verification, and rollback coverage.

## Current Limits

- No true isolated runner-backed benchmark yet
- External execution evidence is still protocol-heavy rather than a clean second-responder pass
- No trigger/discoverability evidence, and none is required for routed use

## Recommendation

Promote `runbooks` from `review` to `tested`.

Keep the tested posture narrow until:

1. a responder other than the author can execute the runbook successfully
2. a true isolated benchmark exists for at least one scenario
3. incident-response and observability updates reuse the same runbook shape cleanly
