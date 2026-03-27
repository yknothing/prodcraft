# Task Execution Gotchas

## Gotchas

### Tactical batch quietly becomes a new plan
- Trigger: The execution batch keeps expanding into more and more future steps because the task feels "connected."
- Failure mode: The agent recreates a long-horizon plan instead of producing the next short executable batch, and verification points drift out of sight.
- What to do: Limit the output to the next batch only. If more future work matters, note it in the checkpoint instead of bloating the current batch.
- Escalate when: The current slice cannot be executed without first revisiting planning assumptions or splitting the task again.

### Wrong implementation discipline chosen for the batch
- Trigger: The task involves a failing bug, a behavior change, and some cleanup all at once.
- Failure mode: The agent starts coding directly, skipping `systematic-debugging` or `tdd`, because the batch looks small enough to improvise.
- What to do: Route each batch to the real underlying discipline first, then resume execution with explicit verification steps.
- Escalate when: The batch no longer fits a single safe discipline and the slice must be split or rerouted.

### Checkpoint claims progress without proof
- Trigger: A batch is nearly done and the agent writes a checkpoint from memory or optimism.
- Failure mode: The checkpoint reads like progress, but it does not name the commands, files, or tests that actually verified the step.
- What to do: Record only what was really changed and how it was verified. If proof is missing, state the batch as incomplete.
- Escalate when: The next batch or a handoff depends on claiming completion that current evidence does not support.
