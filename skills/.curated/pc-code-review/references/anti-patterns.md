# Anti-Pattern Notes

1. **Rubber-stamp reviews**: Approving without reading the code. This provides false confidence and defeats the purpose of review entirely.
2. **Gatekeeping**: Using reviews to enforce personal preferences rather than team standards. Reviews should apply agreed-upon conventions, not individual taste.
3. **Review bombing**: Dumping 50 comments at once without prioritization. Classify by severity so the author knows what matters.
4. **Scope creep**: Requesting large refactors unrelated to the change. Open a separate issue for broader improvements.
5. **Delayed reviews**: Letting PRs sit for days. Aim for initial review within 4 business hours for small changes, 1 business day for large changes.
6. **Approving guessed behavior**: Letting a changeset merge even though it resolves unsupported or unresolved release-1 behavior by assumption.
7. **Turning the checklist into the output**: The checklist is an internal review aid, not a requirement to emit every item as a separate finding.
8. **Solving instead of reviewing**: Supplying implementation patches, code snippets, or merge-verdict theatrics when the prompt asked for review feedback only.
9. **Inventing blockers from suspicion alone**: Escalating a hypothetical regression or unsupported interpretation that the provided fixture does not actually demonstrate.
