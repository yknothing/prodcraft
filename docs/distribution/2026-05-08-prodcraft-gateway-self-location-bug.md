# Prodcraft Gateway Self-Location Bug

> Date: 2026-05-08
>
> Status: fixed in source; pending live portability rerun.
>
> Scope: public/global `prodcraft` gateway package resolution.

## Bug

A real agent run activated the public/global `prodcraft` gateway, inspected the
installed `prodcraft` directory, found only `SKILL.md`, and inferred that no
downstream Prodcraft skills were available. It then continued with a manual
production review/testing flow instead of preserving the `intake` and downstream
skill boundaries.

That inference is invalid. A singleton `prodcraft/SKILL.md` gateway directory is
an expected install shape. Downstream operating context may live in the current
source repository, in a global runtime locator, or in sibling public skill
packages.

## Root Cause

- The generated gateway text described the source repository and routed
  invocation model, but did not explicitly say that a singleton gateway
  directory is valid.
- The global installer wrote only `SKILL.md`, so host runtimes had no
  machine-readable locator for the canonical repository, gateway file, source
  skill root, or workflows.
- Partial-entry behavior was not named. Agent runtimes could fall back to
  manual review while sounding as if repository workflow gates and QA skills had
  executed.

## Repair Boundary

The repair keeps Prodcraft's existing positioning:

- `prodcraft` remains a gateway package, not a bundled orchestrator.
- `.curated/` remains the public install and upgrade surface, not the full
  repository governance plane.
- Public skills remain `portable_with_caveat`; full governance guarantees still
  require source repository contracts, validators, and evidence paths.
- The global install may use a machine-specific `prodcraft-runtime.json`
  locator, while the curated package must not embed local absolute paths.

## Fixed Behavior

Agent runtimes should resolve Prodcraft context in this order:

1. Global `prodcraft-runtime.json` beside the installed gateway skill.
2. The current source repository only when it matches the locator's
   `canonical_repo_root`, sits inside that root, or has been explicitly
   identified by the user or host runtime as the Prodcraft source repository.
3. Sibling public skill packages installed beside `prodcraft`.
4. Partial-entry mode if no deeper context is available.

Partial-entry mode may produce only an entry-level route recommendation and must
name the missing context. It must not claim that `code-review`,
`testing-strategy`, `security-audit`, repository validators, workflow approval,
QA evidence, or completion gates ran.

## Regression Protection

- Renderer contract tests cover global and curated gateway text.
- Global installer tests cover `prodcraft-runtime.json` creation and status
  reporting.
- Curated surface tests cover the generated public gateway boundary text.
- Public positioning tests cover the singleton gateway confusion.
- AR-04 live portability plan now includes a `global-gateway-only` probe for
  real runtime evidence.
