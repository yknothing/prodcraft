# Anti-Pattern Notes

1. **Metric soup** -- Capturing everything because it is easy, without clear questions the telemetry answers.
2. **Inline logging everywhere** -- Repeating custom logging at each call site instead of instrumenting shared boundaries.
3. **Conflating instrumentation with dashboards** -- Hard-coding alerting or UI assumptions into the event model.
4. **Invented usage data** -- Estimating token counts and then aggregating them with exact provider or runner usage.
5. **No schema versioning** -- Breaking downstream consumers every time fields evolve.
6. **Optimization before measurement** -- Shortening or compressing skill instructions before proving the change preserves benchmark quality and actually reduces loaded context.
