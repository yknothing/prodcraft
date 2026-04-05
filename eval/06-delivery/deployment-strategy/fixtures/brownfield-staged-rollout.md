# Brownfield Staged Rollout

- Release type: brownfield increment that routes traffic through a facade to a new implementation.
- Blast radius: moderate because legacy and new paths coexist.
- Data migration: none yet, but sync semantics remain constrained and should not be assumed safe.
- Reversibility: rollback speed matters; the old path must stay available during verification.
- Customer impact: user-facing and behavior-sensitive, so verification must happen before traffic expands.
- Rollout expectation: staged or canary expansion, not a direct full cutover.
