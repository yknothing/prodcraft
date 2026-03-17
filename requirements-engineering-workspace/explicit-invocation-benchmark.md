# Requirements Engineering Explicit Invocation Benchmark

This benchmark does **not** test discoverability. It exists because official trigger eval only tests description-level discovery. This benchmark tests whether the skill adds real value when deliberately invoked.

## Validity Rules

- Baseline runs must execute in an **isolated temporary workspace outside the Prodcraft repo**.
- With-skill runs must execute in a separate isolated workspace that contains **only the copied skill under test**.
- Baseline prompts must explicitly forbid reading local repo files.
- With-skill prompts must explicitly limit local reads to `./skill-under-test/SKILL.md`.
- Any run performed from inside the Prodcraft repo root is considered **context-contaminated** and cannot be used as benchmark evidence.

## Goal

Measure whether `requirements-engineering` improves requirement quality versus baseline responses for canonical specification tasks.

## Scenario 1: Discovery Handoff

**Prompt**

`We already have customer interviews, personas, and feasibility notes for a first-release approvals workflow. Turn them into a reviewed requirements set with priorities, traceability, and measurable non-functional requirements.`

**Assertions**

- produces a structured requirements artifact rather than loose notes
- separates functional and non-functional requirements
- assigns priorities
- includes traceability to source inputs
- avoids jumping into API or implementation design

## Scenario 2: Ambiguous Stakeholder Notes

**Prompt**

`整理这些老板和销售团队的零散需求，写成系统 requirements，区分 P0/P1/P2，并说明哪些内容暂时不做。`

**Assertions**

- resolves ambiguity into explicit requirement statements
- records scope boundaries / non-goals
- preserves business intent without solutioning
- keeps wording testable

## Scenario 3: Compliance-Sensitive Feature

**Prompt**

`We need requirements for an audit-log feature in a B2B finance product. Capture retention, searchability, permissions, and security requirements before architecture starts.`

**Assertions**

- captures compliance-sensitive non-functional requirements
- includes access-control and auditability expectations
- defines measurable retention/search expectations
- stays in the requirements layer

## Pass Criteria

- At least `80%` of assertions pass across the benchmark set
- Baseline output is materially less structured or less traceable than with-skill output
- No scenario jumps prematurely into architecture or implementation as the primary output
- Benchmark evidence is valid only if the isolation rules above are satisfied

## Review Notes

Do not reduce this benchmark to binary assertion counts alone. Modern baseline models may already satisfy coarse checks. Review for **delta in discipline**, especially:

- whether the with-skill output uses clearer obligation-style requirement statements
- whether ambiguity is surfaced as assumptions, conflicts, or open questions instead of being silently baked into design
- whether traceability is more systematic and auditable
- whether the output is more obviously ready to hand off into downstream skills such as `spec-writing` or `acceptance-criteria`
- whether the skill avoids **invented precision** by leaving unsupported metrics as open questions or labeled assumptions
