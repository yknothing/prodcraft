# Core Skill Backfill Design

## Goal

Improve Prodcraft's overall system effectiveness by replacing four planned-but-central lifecycle nodes with real skill packages:

- `feature-development`
- `refactoring`
- `security-audit`
- `deployment-strategy`

## Why These Four

These skills already appear in the gateway, phase overviews, artifact flow, and related-skill guidance. Leaving them as planned makes the lifecycle diagram look complete while the execution path remains hollow.

## Design Decisions

1. Keep the new skills at `draft` status. This improves system completeness without pretending they have full QA evidence.
2. Make `feature-development` and `refactoring` first-class implementation skills and update artifact flow so shared code artifacts can have multiple producers.
3. Clarify implementation ownership by making `tdd` the producer of `test-suite`, while `feature-development` and `refactoring` produce `source-code`.
4. Wire the new skills into workflows and neighboring skills so routing, phase sequencing, and related-skill links all align.

## Non-Goals

- No fabricated benchmark or security-review evidence
- No new personas
- No workflow philosophy changes beyond wiring in the missing skills
