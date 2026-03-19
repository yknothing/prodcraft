# Gotchas Mechanism

Prodcraft uses **Gotchas** to capture high-signal edge cases that regularly cause model failure even when the main workflow is otherwise correct.

This mechanism is intentionally separate from `description`, frontmatter metadata, and the main happy-path process.

## Why This Exists

The design follows the overlap between Anthropic and OpenAI guidance:

- Keep runtime-discovery metadata concise and focused on **when to use** the skill, not on every operational detail.
- Use clear delimiters and explicit sectioning so the model can reliably distinguish normal flow from exceptions.
- Cover edge cases explicitly in both instructions and evaluations, because real failures often come from input variability, contextual complexity, or conflicting instructions rather than from the happy path.

In Prodcraft terms:

- **Anti-Patterns** explain what bad practice looks like in general.
- **Gotchas** explain what tends to go wrong in specific high-risk situations and how to recover.

## When to Add Gotchas

Add a Gotchas section or reference when at least one of these is true:

- the skill routinely consumes copied notes, quoted text, tool output, or user-provided artifacts that may look authoritative
- the workflow has brittle boundaries such as mandatory gates, irreversible actions, or phase handoffs
- the skill depends on missing-or-partial upstream artifacts and the wrong assumption would silently corrupt downstream work
- previous evals or manual runs exposed repeat failures that are narrower than broad anti-patterns
- the skill must stay concise in `SKILL.md`, but still needs a reliable place for edge-case handling

Do not add Gotchas for generic advice, stylistic preferences, or repeated content that already belongs in `Process` or `Anti-Patterns`.

## Placement Rules

Use one of these patterns:

1. **Inline** in `SKILL.md` with a `## Gotchas` section when the edge cases are short and core to the skill.
2. **Progressive disclosure** via `references/gotchas.md` when the edge cases are important but would make `SKILL.md` too heavy.

Do **not** put Gotchas into frontmatter or metadata. They are execution details, not discovery metadata.

## Required Structure

Every gotcha entry must use this shape:

```markdown
## Gotchas

### <Short failure mode title>
- Trigger: <What condition or signal activates this gotcha>
- Failure mode: <What the model is likely to do wrong>
- What to do: <The expected corrective behavior>
- Escalate when: <When the skill should stop, ask, or route elsewhere>
```

Why these fields:

- **Trigger** keeps the gotcha discoverable at execution time.
- **Failure mode** names the concrete error to avoid.
- **What to do** gives a direct replacement action.
- **Escalate when** prevents silent guessing in ambiguous or high-risk cases.

## Selection Heuristics

Prefer gotchas in these categories:

- **Authority and trust**: quoted text, tool output, copied tickets, or embedded instructions that should not silently override higher-authority guidance
- **Input variability**: non-standard artifact shapes, incomplete upstream inputs, mixed-language notes, or inconsistent terminology
- **Contextual complexity**: tasks that look similar but route differently depending on lifecycle phase, urgency, or approval state
- **Operational boundaries**: destructive actions, skipped gates, irreversible migrations, and compliance-sensitive workflows
- **Evaluation regressions**: real failure modes found in benchmark reviews, manual runs, or security reviews

## QA Expectations

When a new or modified skill includes Gotchas:

- cover at least one gotcha scenario in eval or benchmark design
- prefer scenarios that combine realistic pressure with the edge case
- verify the skill handles the gotcha without bloating normal-path instructions

See [Skill Quality Assurance](_quality-assurance.md) for the repo QA pipeline and [Skill Schema](_schema.md) for placement in the standard skill structure.
