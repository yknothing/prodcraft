# Context Notes

Debug expertise turns a broken software contract into a justified next action. Model the running system, choose evidence that separates explanations, and correct the responsible boundary. Use a direct path for clear defects; deepen investigation when uncertainty or risk warrants it.

Use `pc-incident-response` to prioritize containment during live impact. Passive diagnosis can proceed safely in parallel; active experiments must preserve containment. Recovery after a rollback or flag change does not, by itself, establish the cause.

## Reference Material

- [Techniques](techniques.md) -- feedback signals, experiment selection, invariant tracing, bisection, runtime/Skill loading, concurrency, performance, multiple causes and fix-layer selection. Read the section relevant to the next decision.
- [Gotchas](gotchas.md) -- recurring failure modes that create false confidence or misroutes.
