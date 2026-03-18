# API Design Isolated Benchmark Plan

This benchmark tests whether `api-design` produces a clearer, more evolvable contract than baseline when deliberately invoked after architecture is already defined.

## Validity Rules

- baseline and with-skill runs execute in isolated temp workspaces outside the repo
- with-skill branch may read only `./skill-under-test/SKILL.md`
- baseline branch must not read local repo files
- both branches receive the same architecture and requirement inputs
- review must compare contract quality, boundary discipline, and backward-compatibility handling

## Scenario 1: Internal Service Boundary

Prompt:

`Design the API contract between the approvals service and notification service based on this reviewed architecture.`

Assertions:

- preserves architecture-defined boundaries
- chooses clear request/response or event semantics
- defines error and versioning expectations
- avoids leaking internal data-model details into the API

## Scenario 2: Brownfield External Contract

Prompt:

`Design the next-version contract for a brownfield access-review API while preserving compatibility for existing clients.`

Assertions:

- treats backward compatibility as a first-class constraint
- documents versioning and migration expectations
- keeps unresolved rollout assumptions out of the contract unless explicitly required
- leaves a cleaner artifact for downstream implementation and testing

## Pass Criteria

- at least 80% of assertions pass across the benchmark set
- with-skill output is materially stronger than baseline on compatibility clarity and contract completeness
