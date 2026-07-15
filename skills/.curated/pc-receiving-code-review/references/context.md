# Context Notes

`pc-receiving-code-review` is the author-side companion to reviewer-side `pc-code-review`. Its job is to stop two failure modes:

- blind implementation of feedback that breaks the real codebase
- performative agreement that sounds collaborative but skips technical verification

In Prodcraft, review reception must preserve brownfield constraints, existing contracts, release boundaries, and upstream decisions. External feedback is useful input, not automatic truth.

## Reference Material

For common feedback-handling traps, see [Gotchas](gotchas.md).
