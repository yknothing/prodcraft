# Anti-Pattern Notes

1. **Refactor by intuition** -- changing structure because it "feels cleaner" without evidence of real cost.
2. **Behavior change in disguise** -- sneaking in requirement changes under the label of cleanup.
3. **Unsafe large-step rewrite** -- moving too much code at once to reason about regressions.
4. **Testless cleanup** -- improving structure without a safety net strong enough to catch breakage.
