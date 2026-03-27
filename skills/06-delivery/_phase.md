# Phase 06: Delivery

## Purpose

Ship the verified product to users safely and repeatably. Delivery focuses on the mechanics of getting code from the integration branch to production with minimal risk, maximum observability, and clear rollback paths.

## When to Enter

- QA sign-off is granted.
- All blocking issues from quality phase are resolved.
- Release artifacts are built and tested.
- Rollback and coexistence expectations for the release are explicit enough to automate.

## Entry Criteria

- QA sign-off document exists.
- Release candidate artifacts are built from a tagged commit.
- Deployment runbook is prepared or updated.
- Rollback procedure is documented and tested.
- Stakeholders are notified of the release window.
- Test strategy and quality findings are reflected in pipeline gate expectations.

## Exit Criteria (Quality Gate)

Code is deployed to production and verified. Smoke tests pass in production. Monitoring confirms no degradation in error rates, latency, or resource utilization. Release notes are published.

## Key Skills

| Skill | Purpose | Effort |
|---|---|---|
| ci-cd | Automate build, test, and deployment pipelines | medium |
| delivery-completion | Turn verified work into an explicit merge/PR/keep/discard outcome | small |
| release-management | Coordinate the release process across teams | medium |
| deployment-strategy | Choose and execute the right deployment pattern | medium |
| feature-flags | Control feature rollout independently from deployment | small |

## Typical Duration

- Continuous deployment (per change): minutes to hours
- Scheduled release: 1-3 days
- Major version release: 1-2 weeks
- Migration-heavy release: 2-4 weeks

## Skill Sequence

```
ci-cd ──> delivery-completion ──> release-management ──> deployment-strategy
                                                         │
                                                   feature-flags
```

CI/CD is the foundation. Delivery completion makes the verified branch or PR outcome explicit. Release management coordinates the human process and readiness decision. Deployment strategy turns that plan into a concrete rollout and rollback path. Feature flags decouple deployment from release.

In brownfield work, delivery must prove the release can fail closed and recover safely; CI/CD is part of that control surface, not just automation glue.

Cross-cutting obligations for this phase are defined in `rules/cross-cutting-matrix.yml` via `must_consider`, `must_produce`, `skip_when_fast_track`, and `conditional`.

## Anti-Patterns

- **Manual deployment.** Deploying through SSH and manual commands. Every deployment step should be automated, versioned, and repeatable.
- **Big-bang releases.** Accumulating weeks of changes into a single release. Ship small, ship often, and use feature flags to decouple deployment from activation.
- **No rollback plan.** Assuming deployments succeed. Every deployment needs a tested rollback path that can execute in minutes.
- **Friday deploys.** Shipping before reduced-staffing periods. Deploy when the team is available to respond to issues.
- **Invisible releases.** Deploying without notifying support, operations, or customers. Releases have communication obligations beyond the code.
