# Examples

This directory will contain real-world usage examples demonstrating how Prodcraft skills compose into complete development workflows. No examples are checked in yet; the entries below are the planned set. Some listed skills are still planned rather than implemented -- see `planned_skills` in `manifest.yml`; a governance test keeps every listed name resolvable.

## Candidate Example Themes

These are candidate themes, not checked-in example directories. Add a directory
only when the full example contents below are ready.

### New SaaS Product
A greenfield SaaS product built from idea to first deployment using the agile-sprint workflow.
- Demonstrates: full lifecycle from discovery through operations
- Key skills: pc-intake, pc-feasibility-study, pc-spec-writing, pc-system-design, pc-tdd, pc-ci-cd

### API Migration
Migrating a REST API from v1 to v2 while maintaining backward compatibility.
- Demonstrates: brownfield workflow with deprecation
- Key skills: pc-intake, pc-api-design, pc-migration-strategy, pc-feature-flags, pc-deprecation

### Performance Optimization
Diagnosing and fixing a performance regression in a production system.
- Demonstrates: hotfix workflow transitioning to agile-sprint for proper fix
- Key skills: pc-intake, pc-performance-audit, pc-refactoring, pc-monitoring-observability

## Contributing Examples

Each example should include:
1. `scenario.md` -- Problem description and context
2. `workflow-log.md` -- Step-by-step log of skills applied
3. `artifacts/` -- Sample artifacts produced at each phase
4. `lessons.md` -- What worked, what didn't, what would change
