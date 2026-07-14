# Verification Before Completion Gotchas

## Gotchas

### Earlier green run treated as current proof
- Trigger: The agent already ran tests or a build earlier in the session and wants to reuse that result for a new completion claim.
- Failure mode: A stale verification result is treated as fresh evidence even though code, configuration, or the claimed scope has changed.
- What to do: Re-run the command or explicitly narrow the claim to what the earlier output actually proves.
- Escalate when: Re-running verification is blocked by environment constraints and the remaining uncertainty affects a commit, PR, or deployment decision.

### Narrow check presented as whole-system proof
- Trigger: One focused command passes, such as a single test file or lint target, and the agent starts claiming the broader work is done.
- Failure mode: Partial evidence gets inflated into a full completion claim, hiding unverified paths or artifacts.
- What to do: Separate the local success from the broader claim and state exactly which surfaces remain unverified.
- Escalate when: The broader claim is being treated as required for release, incident closure, or user reapproval without a matching verification path.

### Tiredness translated into confidence
- Trigger: The task is nearly done, the session is long, and the agent wants to close out quickly.
- Failure mode: The agent changes tone first ("done", "looks good", "should pass") and verification second, or not at all.
- What to do: Stop wording the conclusion, name the exact claim, run the proof, then report the real result even if it delays completion.
- Escalate when: Time pressure or authority pressure is pushing for a success claim that the current evidence does not support.
