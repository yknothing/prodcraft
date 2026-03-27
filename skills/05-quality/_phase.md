# Phase 05: Quality

## Purpose

Verify that the implementation meets the specification, acceptance criteria, and non-functional requirements. Quality is not just testing; it encompasses code review, security audit, performance validation, and accessibility compliance.

## When to Enter

- Feature implementation is code-complete.
- Unit and integration tests pass in CI.
- Code is ready for review.
- Reviewed task, contract, and architecture context are available for the reviewer.

## Entry Criteria

- All planned features are implemented and merged to the integration branch.
- Automated test suite passes with no known failures.
- Task/contract context is documented and available for validation.
- Test environments are provisioned and configured.

## Exit Criteria (Quality Gate)

QA sign-off granted. All P0/P1 acceptance criteria pass. Code review completed with no blocking issues. Security audit shows no critical or high vulnerabilities. Performance benchmarks meet specified thresholds.

## Key Skills

| Skill | Purpose | Effort |
|---|---|---|
| code-review | Ensure code quality, correctness, and maintainability | medium |
| testing-strategy | Design and execute comprehensive test plans | large |
| security-audit | Identify and remediate security vulnerabilities | medium |
| performance-audit | Validate performance against specified thresholds | medium |

## Typical Duration

- Small feature: 1-3 days
- Medium feature: 3-7 days
- Large initiative: 1-3 weeks
- Security-sensitive release: 2-4 weeks

## Skill Sequence

```
code-review ──> testing-strategy ──┐
                                   ├──> QA sign-off
security-audit ────────────────────┤
performance-audit ─────────────────┘
```

Code review gates entry to broader testing. Security and performance audits can run in parallel with functional testing. All must pass for QA sign-off.

In brownfield work, quality review must verify that coexistence and unsupported release-boundary behavior are still protected before broader QA sign-off proceeds.

If quality review reveals a structural mismatch, produce a `course-correction-note` and route directly to `02-architecture` instead of forcing a full lifecycle restart.

## Anti-Patterns

- **Quality as a phase, not a practice.** Testing only at the end rather than throughout implementation. Shift quality left by integrating testing into every phase.
- **Testing happy paths only.** Verifying that things work when used correctly but not when used incorrectly. Edge cases and error paths cause production incidents.
- **Review rubber-stamping.** Approving code reviews without meaningful inspection. Reviews that do not find issues are not necessarily good reviews.
- **Performance testing in production-unlike environments.** Benchmarking on a laptop and assuming production will behave the same. Test with production-representative data and infrastructure.
- **Security as checkbox.** Running a scanner and declaring security complete. Security audit requires threat modeling and manual review of authentication, authorization, and data handling.

## Cross-Cutting Matrix

See `rules/cross-cutting-matrix.yml` for `must_consider`, `must_produce`, `skip_when_fast_track`, and `conditional` cross-cutting obligations at this phase.
