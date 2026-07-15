# Anti-Pattern Notes

1. **Blame culture** -- "Who broke it?" kills incident reporting. Focus on "what broke and why."
2. **Hero culture** -- One person always fixes everything. This is a single point of failure.
3. **Postmortem without action items** -- A postmortem that identifies problems but assigns no fixes will see the same incident again.
4. **Skipping postmortem for "small" incidents** -- Small incidents reveal systemic issues. Review them.
5. **Debug-first incident handling** -- Spending 45 minutes proving root cause while user impact continues. Contain first.
6. **Unsafe availability bias** -- Keeping a risky path live instead of failing closed at the reviewed release boundary.
