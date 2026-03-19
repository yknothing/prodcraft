#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
MODEL="${1:-}"
RUN_EVAL_SCRIPT="$ROOT/tools/anthropic_trigger_eval/run_eval.py"
PREFLIGHT_SCRIPT="$ROOT/eval/00-discovery/intake/scripts/preflight_claude_eval.py"
ANALYZE_SCRIPT="$ROOT/eval/00-discovery/intake/scripts/analyze_trigger_results.py"
OUT_DIR="$ROOT/eval/00-discovery/intake/optimization/iter-2"

cd "$ROOT"

if [[ -n "$MODEL" ]]; then
  echo "==> Preflight Claude CLI ($MODEL)"
  python3 "$PREFLIGHT_SCRIPT" --model "$MODEL"
else
  echo "==> Preflight Claude CLI (<default>)"
  python3 "$PREFLIGHT_SCRIPT"
fi

mkdir -p "$OUT_DIR"

run_eval_set() {
  local eval_name="$1"
  local eval_path="$2"
  local out_file="$OUT_DIR/results-${eval_name}.json"
  local cmd=(
    python3 "$RUN_EVAL_SCRIPT"
    --eval-set "$eval_path"
    --skill-path "$ROOT/skills/00-discovery/intake"
    --runs-per-query 2
    --timeout 45
    --num-workers 5
  )

  if [[ -n "$MODEL" ]]; then
    cmd+=(--model "$MODEL")
  fi

  echo "==> Running ${eval_name} trigger eval"
  "${cmd[@]}" > "$out_file"

  echo "==> Wrote $out_file"
}

run_eval_set "core" "$ROOT/eval/00-discovery/intake/evals/trigger-core.json"
run_eval_set "overlap" "$ROOT/eval/00-discovery/intake/evals/trigger-overlap.json"
run_eval_set "non-trigger" "$ROOT/eval/00-discovery/intake/evals/trigger-non-trigger.json"
run_eval_set "mixed" "$ROOT/eval/00-discovery/intake/evals/trigger-eval.json"

echo "==> Bucketed summaries"
python3 "$ANALYZE_SCRIPT" \
  "$OUT_DIR/results-core.json" \
  --eval-set "$ROOT/eval/00-discovery/intake/evals/trigger-core.json"

python3 "$ANALYZE_SCRIPT" \
  "$OUT_DIR/results-overlap.json" \
  --eval-set "$ROOT/eval/00-discovery/intake/evals/trigger-overlap.json"

python3 "$ANALYZE_SCRIPT" \
  "$OUT_DIR/results-non-trigger.json" \
  --eval-set "$ROOT/eval/00-discovery/intake/evals/trigger-non-trigger.json"

python3 "$ANALYZE_SCRIPT" \
  "$OUT_DIR/results-mixed.json" \
  --eval-set "$ROOT/eval/00-discovery/intake/evals/trigger-core.json" \
  --eval-set "$ROOT/eval/00-discovery/intake/evals/trigger-overlap.json" \
  --eval-set "$ROOT/eval/00-discovery/intake/evals/trigger-non-trigger.json"
