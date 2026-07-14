# Phase 05: Quality

## Purpose

Verify that the implementation meets the specification, acceptance criteria, and non-functional requirements. Quality is not just testing; it encompasses code review, security audit, performance validation, and accessibility compliance.

## When to Enter

- Feature implementation is code-complete.
- Unit and integration tests pass in CI.
- Code is ready for review.
- Reviewed task, contract, and architecture context are available for the reviewer.
- The intake brief includes `quality_target_context` with `runtime_context`, `exposure_profile`, `production_target`, `non_targets`, and `evidence_refs`.

## Entry Criteria

- All planned features are implemented and merged to the integration branch.
- Automated test suite passes with no known failures.
- Task/contract context is documented and available for validation.
- Test environments are provisioned and configured.
- Quality target context is explicit enough to distinguish an agent-internal skill, host runtime tool, local harness, internal service, or public service.

## Exit Criteria (Quality Gate)

QA sign-off granted. All P0/P1 acceptance criteria pass. Code review completed with no blocking issues. Security audit shows no critical or high vulnerabilities. Performance benchmarks meet specified thresholds.

## Key Skills

| Skill | Purpose | Effort |
|---|---|---|
| pc-implementation-alignment-review | Verify that implementation, tests, docs, and completion claims match the original intent and accepted scope | medium |
| pc-implementation-integrity-audit | Audit low-level defects, deceptive success paths, improper mocks, and fake evidence before claims are trusted | medium |
| pc-code-review | Ensure code quality, correctness, and maintainability | medium |
| pc-receiving-code-review | Verify and respond to review feedback with technical rigor | small |
| pc-testing-strategy | Design and execute comprehensive test plans | large |
| pc-e2e-scenario-design | Design deep, stateful E2E scenarios from user journeys across any platform or language | large |
| pc-security-audit | Identify and remediate security vulnerabilities | medium |
| pc-performance-audit | Validate performance against specified thresholds | medium |

## Typical Duration

- Small feature: 1-3 days
- Medium feature: 3-7 days
- Large initiative: 1-3 weeks
- Security-sensitive release: 2-4 weeks

## Skill Sequence

```
pc-implementation-alignment-review ──┐
pc-implementation-integrity-audit ────┼──> pc-code-review <──> pc-receiving-code-review ──> pc-testing-strategy ──> pc-e2e-scenario-design ──┐
                                      │                                                                                                      ├──> QA sign-off
pc-security-audit ────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────┤
pc-performance-audit ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

`pc-implementation-alignment-review` checks whether the right thing was built. `pc-implementation-integrity-audit` checks whether the implementation and evidence are honest enough to trust. Use either before `pc-code-review` when the risk is intent drift, fake success, fixture masquerade, or low-level implementation shortcuts.

Code review establishes the reviewer-side findings. `pc-receiving-code-review` governs the author-side follow-up on those findings before broader testing closes out the phase. `pc-testing-strategy` decides the layered plan; `pc-e2e-scenario-design` deepens the scenario and edge-case layers when shallow E2E coverage would otherwise hide release risk. Security and performance audits can run in parallel with functional testing. All must pass for QA sign-off.

Do not assume public HTTP service from framework or transport details. `pc-security-audit`, `pc-testing-strategy`, and `pc-e2e-scenario-design` are calibrated branches, not automatic service-style follow-ups. For agent-internal skill or host-runtime work, the quality target may be trigger behavior, artifact safety, tool boundaries, validators, curated export, and runtime portability. For public service work, browser/API contracts, CORS, public auth, rate limiting, and internet abuse paths remain in scope when supported by evidence.

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
