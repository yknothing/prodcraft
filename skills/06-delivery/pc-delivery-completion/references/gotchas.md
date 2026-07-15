# Delivery Completion Gotchas

## Gotchas

### Branch policy forbids local merge
- Trigger: Protected branch or repo policy requires PR-based integration.
- Failure mode: The operator treats "merge now" as always available and bypasses repository policy.
- What to do: Convert the outcome to "push and create a PR" and record the policy reason in the `delivery-decision-record`.
- Escalate when: The policy exception would require admin override or would bypass a mandatory review path.

### Stale verification after branch drift
- Trigger: New commits, rebase, or merge-base changes occur after the verification evidence was collected.
- Failure mode: Completion proceeds using evidence that no longer describes the branch state being landed.
- What to do: Re-run the critical verification before offering or executing completion options.
- Escalate when: The drift changed dependencies, generated files, or release-sensitive paths and the necessary verification is unclear.

### Discard request on active hotfix or incident follow-up
- Trigger: The user wants to discard work that was part of an incident response or active production mitigation.
- Failure mode: The team deletes the only tracked fix path without confirming operational impact.
- What to do: Stop and verify whether the work is already superseded or no longer needed before cleanup.
- Escalate when: The discard would remove the only known recovery branch or the incident remains unresolved.
