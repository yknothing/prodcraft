# Pressure-Test Scenario Matrix

Run at least `3` scenarios per review cycle. Run all `5` after major routing or contract changes.

| Scenario ID | Request Shape | Expected Route Focus | Key Questions |
|------------|---------------|----------------------|---------------|
| `PT-01-new-feature` | New product feature with unclear scope and UI impact | `00-discovery -> 01-specification -> 02-architecture` | Does intake ask only the clarifications that change route or scope? Do accessibility/internationalization trigger at the right point? |
| `PT-02-fast-track-bugfix` | Small bug fix with clear root cause in one file | `00-discovery` fast-track into `04-implementation` | Does fast-track avoid unnecessary documentation work while still preserving TDD and review gates? |
| `PT-03-brownfield-migration` | Legacy migration with coexistence risk and staged rollout | `00-discovery -> 02-architecture -> 03-planning` with brownfield overlay | Does routing expose coexistence seams early enough? Which artifacts are actually reused downstream? |
| `PT-04-hotfix-incident` | Production incident requiring immediate containment and follow-up | `00-discovery` fast-track or hotfix into `07-operations/04-implementation`, then possible `course-correction-note` | Does the system distinguish containment from redesign? Are approved jump pairs enough when architecture assumptions fail under pressure? |
| `PT-05-docs-only-change` | Documentation update with no product or runtime change | direct path to `cross-cutting/documentation` | Does intake hide the rest of the lifecycle cleanly, or does the user still pay unnecessary routing cost? |
| `PT-06-mixed-language-request` | Mixed Chinese/English request with user-facing output in Chinese and canonical repo artifacts in English | `00-discovery -> 01-specification` or fast-track, depending scope | Where does language ambiguity first appear: intake, artifact fields, or user-facing summary? Is a later language-boundary contract actually warranted? |

## Exit Questions

- Which clarification question changed the route?
- Which cross-cutting rule fired and produced durable value?
- Which artifact was generated but nobody used?
- Which step should be deleted, downgraded, or merged if it repeats across runs?
