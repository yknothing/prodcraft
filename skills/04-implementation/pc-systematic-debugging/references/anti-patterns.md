# Anti-Pattern Notes

1. **Shotgun debugging** -- changing several things at once and keeping whatever "worked".
2. **Containment mistaken for root cause** -- assuming rollback or flag-off explains why the bug exists.
3. **Historical anchoring** -- reusing an old fix because the ticket title looks similar.
4. **Architecture patch cosplay** -- applying a local workaround after multiple failed fixes even though the evidence points upstream.
5. **Regression amnesia** -- repairing today's symptom without defining the test that catches it next time.
