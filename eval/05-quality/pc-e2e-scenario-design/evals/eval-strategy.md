# E2E Scenario Design Eval Strategy

## Goal

Measure whether `pc-e2e-scenario-design` improves deep scenario design beyond what a strong baseline can already do without the skill.

## Primary Success Criteria

The with-skill branch should outperform baseline on at least three of these dimensions:

- identifies the shallow-test structural failure mode instead of only listing missing cases
- starts from user journeys or release-boundary scenarios rather than a flat feature checklist
- designs at least one stateful, multi-step scenario with explicit re-entry or persistence validation
- covers at least two edge-case classes that are realistic for the target platform
- specifies business-state or cross-boundary assertions instead of UI-only checks

## Evidence Types

1. **Explicit benchmark**
   - compare baseline vs with-skill on web, mobile, and collaboration-style scenarios
   - record pass/fail judgments per expectation
2. **Routed handoff review**
   - start from `pc-testing-strategy`
   - verify that the downstream scenario design preserves the upstream risk priorities
3. **Consumer review**
   - verify that a reviewer, CI owner, or implementation owner can use the resulting artifacts without re-inventing the scenario structure

## Failure Modes To Watch

- scenario advice stays generic and never becomes executable
- platform details dominate while business-state assertions remain weak
- the skill duplicates `pc-testing-strategy` instead of deepening it
- edge cases are listed, but no layered suite structure is produced

## Current Review Gate

Keep the skill in `review` until at least one routed handoff review exists in addition to the current explicit benchmark evidence.

## Description Discoverability Revalidation

The current description is evaluated separately from explicit output quality via
`trigger-eval.json`, using the vendored Anthropic harness. The set contains five
core positives, five overlap cases that distinguish this skill from testing
strategy, debugging, implementation, and code review, and ten true negatives.
Run each query three times and preserve both the JSON result and observability
stream. Trigger results do not replace the explicit benchmark or routed handoff
evidence above.

```bash
: "${CLAUDE_TRIGGER_MODEL:?export CLAUDE_TRIGGER_MODEL to a pinned Claude model id}"

python3 tools/anthropic_trigger_eval/run_eval.py \
  --eval-set eval/05-quality/pc-e2e-scenario-design/evals/trigger-eval.json \
  --skill-path skills/05-quality/pc-e2e-scenario-design \
  --runs-per-query 3 \
  --trigger-threshold 0.5 \
  --timeout 45 \
  --num-workers 5 \
  --model "$CLAUDE_TRIGGER_MODEL" \
  --observability-output <trigger-observability.jsonl> \
  > <trigger-results.json>
```

### Fresh Surrogate Evidence

The sealed packet at
[`../evidence/codex-trigger-surrogate-gpt56sol-2026-07-16/`](../evidence/codex-trigger-surrogate-gpt56sol-2026-07-16/)
records a fresh pinned Codex classification of the 20-query set. All 20 labels
matched, including 5/5 core positives, 5/5 overlap cases, and 10/10 negatives.

This is supplementary evidence only. It used one batched `gpt-5.6-sol` call,
not the vendored Claude harness or three independent runs per query. The packet
therefore records `official_trigger_gate_satisfied=false`; the canonical Claude
trigger gate remains pending until Claude authentication is available.
