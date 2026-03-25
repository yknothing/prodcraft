# Magic Value Governance

Prodcraft enforces a single rule source for magic-value and hardcoding control:

- `skills/05-quality/code-review/SKILL.md`

The pre-commit hook is intentionally lightweight and cross-language. It is a blocking guardrail, not a semantic compiler.

## Enable Hook

```bash
git config core.hooksPath .githooks
```

## Rule Baseline

- No unapproved magic values in changed code.
- No unapproved hardcoded configuration in changed code.
- Any exception must carry the exact annotation:

`ALLOW_MAGIC_NUMBER: reason, ticket`

## Exception Format

Use the annotation on the same line or within two lines above the flagged literal:

```python
# ALLOW_MAGIC_NUMBER: protocol requires RFC fixed value, PROD-1234
DEFAULT_WINDOW_SECONDS = 300
```

The ticket must explain why a named constant/config boundary is not currently suitable.

## CI Recommendation

To avoid local bypass, run the same scanner in CI:

```bash
python3 scripts/hooks/no_magic_values_scan.py --git working-tree --fail-on-findings
```
