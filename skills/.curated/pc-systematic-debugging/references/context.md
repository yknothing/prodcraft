# Context Notes

Systematic debugging turns a bug report, failing test, or bad runtime behavior into a defensible fix. It exists to stop guess-first patching, repeated failed fixes, and "works on my machine" improvisation.

It does **not** replace `pc-incident-response`. If production impact is live, contain it there first; root-cause work resumes once the system is safe. Containment (rollback, flag off) is never evidence of root cause.

## Reference Material

- [Techniques](techniques.md) -- bisection recipes, differential debugging, instrumentation patterns, flaky-failure stabilization, stale-artifact checklist, multi-bug untangling.
- [Gotchas](gotchas.md) -- recurring failure modes that create false confidence or misroutes.
