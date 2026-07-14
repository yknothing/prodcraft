# Bug History Retrieval Gotchas

## Gotchas

### Closed issue, missing fix in the current release
- Trigger: A tracker result is marked fixed or closed, but the current environment still shows the same symptom.
- Failure mode: The agent assumes the prior fix is present everywhere and stops checking release or branch lineage.
- What to do: Verify whether the fix commit, PR, or release actually reached the affected branch, deployment ring, or tenant before treating the bug as solved.
- Escalate when: The release lineage is ambiguous or the deployment system cannot confirm whether the historical fix is present.

### Similar symptom, different subsystem
- Trigger: Multiple historical bugs share the same user-facing symptom or error keyword.
- Failure mode: The agent picks the first similar ticket and anchors on the wrong code path.
- What to do: Rank matches by component boundary, stack trace, release window, and mitigation pattern, not by wording alone.
- Escalate when: Two or more candidates remain equally plausible after checking subsystem and release evidence.

### Historical workaround treated as current policy
- Trigger: A prior incident record includes a containment step, manual workaround, or emergency bypass.
- Failure mode: The agent treats the old workaround as standing guidance and applies it without checking current controls.
- What to do: Treat historical workarounds as evidence, then validate them against the current workflow, safety gates, and operational ownership before reuse.
- Escalate when: Reusing the workaround would bypass a current approval gate, security boundary, or rollout policy.
