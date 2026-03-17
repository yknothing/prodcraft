# Phase 06: Delivery

## Purpose

Ship the verified product to users safely and repeatably. Delivery focuses on the mechanics of getting code from the integration branch to production with minimal risk, maximum observability, and clear rollback paths.

## When to Enter

- QA sign-off is granted.
- All blocking issues from quality phase are resolved.
- Release artifacts are built and tested.

## Entry Criteria

- QA sign-off document exists.
- Release candidate artifacts are built from a tagged commit.
- Deployment runbook is prepared or updated.
- Rollback procedure is documented and tested.
- Stakeholders are notified of the release window.

## Exit Criteria (Quality Gate)

Code is deployed to production and verified. Smoke tests pass in production. Monitoring confirms no degradation in error rates, latency, or resource utilization. Release notes are published.

## Key Skills

| Skill | Purpose | Effort |
|---|---|---|
| ci-cd | Automate build, test, and deployment pipelines | medium |
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
ci-cd ──> deployment-strategy ──> release-management
                │
          feature-flags
```

CI/CD is the foundation. Deployment strategy determines how code reaches production. Feature flags decouple deployment from release. Release management coordinates the human process.

## Anti-Patterns

- **Manual deployment.** Deploying through SSH and manual commands. Every deployment step should be automated, versioned, and repeatable.
- **Big-bang releases.** Accumulating weeks of changes into a single release. Ship small, ship often, and use feature flags to decouple deployment from activation.
- **No rollback plan.** Assuming deployments succeed. Every deployment needs a tested rollback path that can execute in minutes.
- **Friday deploys.** Shipping before reduced-staffing periods. Deploy when the team is available to respond to issues.
- **Invisible releases.** Deploying without notifying support, operations, or customers. Releases have communication obligations beyond the code.
