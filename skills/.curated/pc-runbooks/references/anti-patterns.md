# Anti-Pattern Notes

1. **Narrative instead of procedure** -- If every step has to be inferred, it is not a runbook.
2. **Author-only knowledge** -- A runbook that depends on tribal memory is already failing.
3. **No rollback or safe-stop branch** -- Procedures that assume the happy path are dangerous under pressure.
4. **Outdated environment details** -- Old commands and links are silent operational hazards.
5. **Missing communication checkpoints** -- Recovery can still fail if stakeholders do not know the current state.
6. **Magic thresholds** -- Saying "if the threshold is exceeded" without naming the threshold or policy source forces responders to guess.
