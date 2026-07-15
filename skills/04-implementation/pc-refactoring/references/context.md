# Context Notes

Refactoring keeps implementation quality from decaying between releases. It is not cleanup for its own sake. In Prodcraft, refactoring is justified when reviews, tech-debt evidence, or repeated implementation friction show that the current structure is increasing future cost or risk.

The constraint is strict: externally observable behavior must stay stable. If behavior changes, the work is feature development or defect fixing, not refactoring.
