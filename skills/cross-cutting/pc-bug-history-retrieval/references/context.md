# Context Notes

This skill exists to keep bug investigation grounded in **source-of-truth systems** rather than in memory, copied notes, or a shadow knowledge base.

Use it when the current problem may already have a known lineage in:

- an internal bug tracker
- incident or postmortem records
- error monitoring systems
- release notes and deployment records
- git history, including fix, revert, and follow-up commits

This skill does **not** replace debugging. It provides historical context that makes downstream debugging, incident response, or planning more accurate.

Prefer direct access to the canonical system through available tools, MCP integrations, or approved internal APIs. Do not duplicate authoritative bug records into local docs unless another skill explicitly asks for a durable summary.

## Reference Material

For retrieval edge cases that commonly create false matches or stale conclusions, see [Gotchas](gotchas.md).
