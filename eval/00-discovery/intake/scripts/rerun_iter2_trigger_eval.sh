#!/usr/bin/env bash
set -euo pipefail

MODEL="${1:-claude-opus-4-6}"
ROOT="/Users/whatsup/workspace/2026/prodcraft"
SKILL_CREATOR="/Users/whatsup/.claude/plugins/cache/claude-plugins-official/skill-creator/b36fd4b75301/skills/skill-creator"
OUT_DIR="$ROOT/intake-workspace/optimization/iter-2"

cd "$ROOT"

echo "==> Preflight Claude CLI ($MODEL)"
python3 intake-workspace/scripts/preflight_claude_eval.py --model "$MODEL"

mkdir -p "$OUT_DIR"

cd "$SKILL_CREATOR"

run_eval_set() {
  local eval_name="$1"
  local eval_path="$2"
  local out_file="$OUT_DIR/results-${eval_name}.json"

  echo "==> Running ${eval_name} trigger eval"
  python3 -m scripts.run_eval \
    --eval-set "$eval_path" \
    --skill-path "$ROOT/skills/00-discovery/intake" \
    --model "$MODEL" \
    --runs-per-query 2 \
    --timeout 45 \
    --num-workers 5 \
    > "$out_file"

  echo "==> Wrote $out_file"
}

run_eval_set "core" "$ROOT/intake-workspace/evals/trigger-core.json"
run_eval_set "overlap" "$ROOT/intake-workspace/evals/trigger-overlap.json"
run_eval_set "non-trigger" "$ROOT/intake-workspace/evals/trigger-non-trigger.json"
run_eval_set "mixed" "$ROOT/intake-workspace/evals/trigger-eval.json"

cd "$ROOT"

echo "==> Bucketed summaries"
python3 intake-workspace/scripts/analyze_trigger_results.py \
  "$OUT_DIR/results-core.json" \
  --eval-set "$ROOT/intake-workspace/evals/trigger-core.json"

python3 intake-workspace/scripts/analyze_trigger_results.py \
  "$OUT_DIR/results-overlap.json" \
  --eval-set "$ROOT/intake-workspace/evals/trigger-overlap.json"

python3 intake-workspace/scripts/analyze_trigger_results.py \
  "$OUT_DIR/results-non-trigger.json" \
  --eval-set "$ROOT/intake-workspace/evals/trigger-non-trigger.json"

python3 intake-workspace/scripts/analyze_trigger_results.py \
  "$OUT_DIR/results-mixed.json" \
  --eval-set "$ROOT/intake-workspace/evals/trigger-core.json" \
  --eval-set "$ROOT/intake-workspace/evals/trigger-overlap.json" \
  --eval-set "$ROOT/intake-workspace/evals/trigger-non-trigger.json"
