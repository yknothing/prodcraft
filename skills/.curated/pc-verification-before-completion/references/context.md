# Context Notes

`pc-verification-before-completion` is the cross-cutting gate that protects Prodcraft from false completion claims. It exists because implementation success, review approval, or deployment confidence often drifts into assertion before evidence.

This skill does not replace the phase-local quality work. It is the final honesty check before saying:

- the bug is fixed
- the phase is complete
- the tests pass
- the release is ready
- the handoff is safe

Fast-track work may shorten the verification surface, but it does not waive this gate. The Iron Law stays the same.

## Reference Material

For common completion-claim failure modes and recovery patterns, see [Gotchas](gotchas.md).
