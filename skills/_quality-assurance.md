# Skill Quality Assurance

> Every skill in Prodcraft must pass quality assurance before being considered production-ready. This document defines the QA process, leveraging the `skill-creator` skill for evaluation, optimization, and benchmarking.

## Quality Assurance Pipeline

Every new or modified skill goes through this pipeline:

```
Draft Skill
    │
    ▼
┌─────────────────────┐
│ 1. Self-Review       │  Author reviews against _schema.md
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 2. skill-creator     │  Invoke /skill-creator for:
│    Evaluation        │  - Structure validation
│                      │  - Trigger accuracy testing
│                      │  - Description optimization
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 3. skill-creator     │  Run evals to verify:
│    Benchmarking      │  - Skill triggers correctly
│                      │  - Skill does NOT trigger falsely
│                      │  - Output quality meets standards
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 4. Security Review   │  Check for:
│                      │  - Prompt injection vectors
│                      │  - Unsafe command patterns
│                      │  - Data exfiltration risks
│                      │  - Privilege escalation
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 5. Integration Test  │  Verify skill works in:
│                      │  - Skill chains (with predecessors)
│                      │  - All declared methodologies
│                      │  - Edge cases and error paths
└─────────┬───────────┘
          │
          ▼
  Production Ready
```

## Using skill-creator for Quality Assurance

The `skill-creator` skill (Anthropic's official skill quality tool) is the primary instrument for skill QA. Invoke it at these checkpoints:

### Checkpoint 1: Skill Creation/Modification

When creating a new skill or significantly modifying an existing one:

```
/skill-creator create [skill-name]
```

The skill-creator will:
- Validate the skill structure and frontmatter
- Check for common anti-patterns in skill design
- Suggest improvements to trigger descriptions for accuracy
- Ensure the skill follows best practices

### Checkpoint 2: Trigger Accuracy

After the skill is drafted, test that it triggers correctly:

```
/skill-creator eval [skill-name]
```

This runs evaluation scenarios to verify:
- **True positives**: The skill triggers when it should
- **True negatives**: The skill does NOT trigger when it shouldn't
- **Trigger precision**: The description accurately matches the intended use cases

Important: the official trigger eval is a **description-discoverability** test. It verifies whether the skill's metadata causes Claude to load the skill. It does **not** prove that the body of the skill adds value once read.

### Checkpoint 3: Performance Benchmarking

For critical skills (gateway, intake, TDD, code-review), run benchmarks:

```
/skill-creator benchmark [skill-name]
```

This measures:
- **Variance analysis**: How consistent are the skill's outputs across runs?
- **Quality scoring**: Does the output meet the defined quality gate?
- **Efficiency**: Is the skill producing maximum value with minimum token usage?

Use benchmarking to answer the separate question that trigger eval cannot answer: **does the skill improve output quality when explicitly invoked?**

For explicit-invocation benchmarks, control the environment:

- Run the **baseline** in an isolated temporary workspace outside the repo under test.
- Run the **with-skill** case in a separate isolated workspace containing only the copied skill package.
- Do not treat a benchmark as valid if the baseline can see local project instructions, repo-level agent guidance, or neighboring skills.
- Persist prompts, runtime context, and raw outputs so the evidence can be audited later.
- If the official harness fails for an environment precondition such as missing local CLI authentication, keep the failed artifact, record the blocker in the evidence review, and rerun after the precondition is restored rather than fabricating a benchmark verdict.

### Checkpoint 4: Description Optimization

Optimize the trigger description for better matching accuracy:

```
/skill-creator optimize [skill-name]
```

This refines the `description` field in frontmatter to:
- Improve triggering accuracy (reduce false positives and negatives)
- Clarify the skill's scope and boundaries
- Ensure it doesn't overlap with other skills

When editing descriptions, follow the platform guidance that governs real runtime behavior:

- Anthropic: the `description` is how Claude decides when to apply the skill, so it should include words users would naturally say and become more specific if the skill triggers too often.
- Anthropic: skill descriptions are loaded into context so Claude knows what is available, which means unnecessary verbosity creates avoidable context pressure across the whole skill set.
- OpenAI: skills should define when to use a workflow, while the detailed steps and result format belong in the skill body and supporting files rather than being packed into metadata.

## Security-Specific Checks

Skills are security-sensitive artifacts -- they control AI agent behavior. Every skill must pass these security checks:

### 1. Prompt Injection Resistance

- [ ] Skill instructions cannot be overridden by user input within the skill's context
- [ ] The skill does not echo unsanitized user input into its instructions
- [ ] The skill does not instruct the agent to bypass safety checks

### 2. Command Safety

- [ ] Any shell commands in the skill are parameterized, not constructed from user input
- [ ] The skill does not instruct execution of arbitrary commands
- [ ] Destructive operations (delete, overwrite, force push) require explicit confirmation
- [ ] The skill does not grant elevated permissions beyond what's needed

### 3. Data Protection

- [ ] The skill does not instruct logging or transmitting sensitive data
- [ ] Secrets, credentials, and PII are never included in skill outputs
- [ ] The skill respects data classification boundaries

### 4. Scope Limitation

- [ ] The skill operates within its declared phase and roles
- [ ] The skill does not attempt to override other skills' quality gates
- [ ] The skill does not instruct bypassing review or approval processes

### 5. Supply Chain Safety

- [ ] External references (URLs, packages, tools) are from trusted sources
- [ ] The skill does not dynamically fetch and execute remote instructions
- [ ] Version-pinned references are used where applicable

## Quality Metrics

Track these metrics for each skill over time:

| Metric | Target | Measurement |
|--------|--------|-------------|
| Trigger accuracy | >90% | skill-creator eval results |
| Output consistency | <15% variance | skill-creator benchmark results |
| User satisfaction | >4/5 rating | Post-use feedback |
| False trigger rate | <5% | skill-creator eval results |
| Security findings | 0 critical/high | Security review checklist |

## QA Evidence in the Repo

Prodcraft tracks QA state directly in [`manifest.yml`](../../manifest.yml):

- Every active skill declares a `status`
- Every non-draft skill declares an `evaluation_mode`
- Non-draft skills declare a `qa` mapping with evidence paths
- Paths in `qa` must resolve to checked-in artifacts or scripts

Use these conventions:

| Field | Meaning |
|-------|---------|
| `status` | Lifecycle state for the skill (`draft`, `review`, `tested`, `secure`, `production`, `deprecated`) |
| `evaluation_mode` | QA posture for the skill (`discoverability` for metadata-first skills, `routed` for workflow/intake/handoff-driven skills) |
| `qa.structure_validation_path` | Structural validator or script used to verify the skill package |
| `qa.eval_strategy_path` | Human-readable evaluation strategy or rubric |
| `qa.benchmark_plan_path` | Planned benchmark protocol when review-stage coverage is being built but final results are not ready yet |
| `qa.trigger_eval_set_path` | Pending eval inputs for skills under review |
| `qa.trigger_eval_results_path` | Latest trigger eval results for tested or production skills |
| `qa.benchmark_results_path` | Benchmark or quality-comparison artifact |
| `qa.security_review_path` | Security checklist or review record |
| `qa.integration_test_path` | Workflow-chain or end-to-end verification artifact |

Additional `*_path` evidence keys are allowed for supplemental proof, for example:

- downstream-consumer reviews for routed skills
- secondary handoff reviews for a second scenario
- manual vs isolated benchmark notes when both are useful
- historical evidence retained for audit after a skill contract changes
- revalidation plans that explain what evidence must be regenerated before status can advance

This keeps QA claims auditable. A skill is not "tested" because someone said so; it is tested because the manifest points to the evidence.

### Evaluation Modes

Prodcraft uses two QA modes because not every Anthropic-native skill should be judged mainly by discoverability:

1. `discoverability`
   - Use for skills whose value depends on being found from metadata alone.
   - Typical example: `intake`
   - Trigger eval is a primary gate before `tested`

2. `routed`
   - Use for skills normally invoked by intake, workflow routing, or explicit handoff.
   - Typical examples: `requirements-engineering`, `system-design`, `runbooks`
   - Trigger eval can still be informative, but it is not the main gate
   - Explicit-invocation benchmark and integration evidence are the main gates before `tested`

## Skill Lifecycle Status

Every skill in the manifest should have one of these statuses:

| Status | Meaning |
|--------|---------|
| `draft` | Under development, not yet QA'd |
| `review` | Submitted for skill-creator evaluation |
| `tested` | Passed skill-creator evals and benchmarks |
| `secure` | Passed security review |
| `production` | Fully QA'd, ready for use |
| `deprecated` | Scheduled for removal, use alternative |

Status transitions should be evidence-backed:

- `draft` -> `review`: structure is valid, evaluation mode is chosen, and review evidence strategy exists
- `review` -> `tested` for `discoverability`: trigger eval results exist and meet the target bar
- `review` -> `tested` for `routed`: explicit-invocation benchmark and integration evidence exist and meet the target bar
- `tested` -> `secure`: security review artifact exists with no blocking findings
- `secure` -> `production`: integration tests exist and all required QA artifacts are present

## Continuous Improvement

After a skill has been in production:

1. **Monthly review**: Run skill-creator eval to check for drift
2. **Quarterly benchmark**: Run variance analysis to detect degradation
3. **Incident-triggered review**: If a skill produces incorrect output, immediately re-evaluate
4. **User feedback integration**: Collect and act on user feedback about skill effectiveness

## Integration with Prodcraft Workflows

The skill QA process itself follows Prodcraft principles:

- **Intake**: New skill request is triaged (what gap does it fill? which phase?)
- **Specification**: Skill purpose, triggers, and quality gate are defined
- **Implementation**: Skill content is written following _schema.md
- **Quality**: skill-creator evaluates, benchmarks, and optimizes
- **Security**: Security checklist is completed
- **Delivery**: Skill is added to manifest with `production` status
- **Evolution**: Skill is monitored and improved over time
