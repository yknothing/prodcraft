# Receiving Code Review Gotchas

## Gotchas

### External reviewer suggestion conflicts with local architecture
- Trigger: A review comment sounds reasonable in isolation but pushes against a documented contract, brownfield seam, or upstream design decision.
- Failure mode: The author implements it anyway to appear cooperative, creating a hidden architectural regression.
- What to do: Check the suggestion against the architecture or contract artifacts first, then respond with technical reasoning if the comment is misaligned.
- Escalate when: The reviewer and local architecture evidence point in different directions and the author cannot resolve the conflict alone.

### One unclear item inside a larger review batch
- Trigger: Most review items are clear, but one or two comments are ambiguous or appear related to the rest.
- Failure mode: The author implements the understood subset, then later learns the ambiguous items changed the scope or intent of the batch.
- What to do: Pause and ask for clarification before implementing any of the grouped items.
- Escalate when: Clarification would materially delay a hotfix or release decision and the remaining ambiguity affects correctness.

### Praise-first reply masks lack of verification
- Trigger: The author starts drafting "good catch" or "you're right" language before checking the codebase reality.
- Failure mode: Social agreement hardens into blind implementation, even when the suggestion is incomplete or wrong.
- What to do: Replace praise with the technical fact pattern, verify the suggestion, then either implement it or push back with evidence.
- Escalate when: The discussion becomes social or authority-driven instead of technical and evidence-based.
