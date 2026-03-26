# Intake Routing Signals and Examples

Use this reference when the main `intake` workflow is clear but you need a quick calibration aid for classification or workflow selection.

## Methodology Selection Signals

- **Spec-driven**: regulated industry, contractual deliverable, large team, compliance, safety-critical
- **Agile**: product iteration, startup, evolving requirements, small team, SaaS
- **Waterfall**: well-understood requirements, enterprise, distributed teams, compliance checkpoints
- **Hotfix**: production down, security vulnerability, data corruption, revenue impact
- **Greenfield**: no existing codebase, new product/service, proof of concept
- **Brownfield**: legacy system exists, migration needed, modernization goal

## Worked Examples

### Feature Request

```text
User: "Add dark mode support to the settings page"

Intake Brief:
- Work type: New Feature
- Entry phase: 01-specification
- Workflow: agile-sprint
- Skills: requirements-engineering -> acceptance-criteria -> task-breakdown -> tdd -> code-review
- Scope: medium
- Risks: current styling approach may not support clean theming boundaries
```

### Production Bug

```text
User: "Users are getting 500 errors on checkout"

Intake Brief:
- Work type: Hotfix
- Entry phase: 04-implementation
- Workflow: hotfix
- Skills: incident-response -> tdd -> code-review -> ci-cd
- Scope: small
- Risks: the root cause may be upstream of the application code
```

### New Project

```text
User: "I want to build a CLI tool for managing database migrations"

Intake Brief:
- Work type: New Product
- Entry phase: 00-discovery
- Workflow: greenfield
- Skills: feasibility-study -> requirements-engineering -> system-design -> task-breakdown -> tdd
- Scope: large
- Risks: scope creep and unclear differentiation from existing tools
```
