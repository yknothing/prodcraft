# Context Notes

TDD is the core implementation discipline in Prodcraft. It ensures every piece of code is born with a test, creating a safety net for refactoring and a living specification of behavior. TDD is not about testing -- it's about design. Writing the test first forces you to think about the interface before the implementation.

In a lifecycle-aware system, TDD should start from the next planned slice of work, while preserving upstream contract and coexistence boundaries. Do not use implementation pressure as an excuse to skip characterization, contract, or unsupported-flow tests in brownfield work.
