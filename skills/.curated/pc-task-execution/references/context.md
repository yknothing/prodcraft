# Context Notes

`pc-task-execution` is the tactical companion to `pc-task-breakdown`.

- `pc-task-breakdown` defines the bounded, independently reviewable implementation slice
- `pc-task-execution` adds a short batch with verification points and stop conditions when direct execution needs that coordination; 2-5 minutes is a heuristic

This skill exists to prevent a common failure mode: a task is "small enough" on paper, but execution still drifts into long, unverified editing sessions, hidden blockers, or broad opportunistic changes.

It does **not** replace `pc-feature-development`, `pc-systematic-debugging`, or `pc-tdd`. It prepares and governs the batch that those skills will execute.

## Reference Material

For tactical execution failure modes that cause hidden drift or false progress, see [Gotchas](gotchas.md).
