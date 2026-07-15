# Codex Trigger Surrogate Review

## Decision

Surrogate classification result: **20/20 matched (accuracy 1.0)**.

Official vendored Claude trigger gate: **NOT SATISFIED**.

This packet is fresh supplementary discoverability evidence produced by a
pinned Codex model. It must not be represented as an execution of Anthropic's
vendored trigger harness or its routing semantics.

## Method

- Classifier: `gpt-5.6-sol` through `codex-cli 0.144.4`
- Input: skill name and description plus 20 queries
- Expected labels were withheld from the model and joined only during
  deterministic scoring
- One batched model call; one classification per query
- Strict JSON output schema with exact query IDs
- Temporary auth-only `CODEX_HOME`, user config ignored, recursive
  `systematic-debugging` preflight and postflight matches both zero

## Result

- Core positive: 5/5 matched
- Overlap: 5/5 matched
- Negative: 10/10 matched
- Total: 20/20 matched

## Boundary

The canonical eval strategy requires the vendored Anthropic harness, three runs
per query, a trigger threshold, runner observability, and a pinned Claude model.
Claude was unavailable because its OAuth session had expired. This surrogate
uses a different provider routing surface, batches all queries into one call,
and has no repeatability estimate. It therefore does not advance the official
Claude trigger gate, even though its fresh classifications match every expected
label.
