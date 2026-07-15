# Context Notes

This skill is an adversarial quality audit for implementation honesty. It looks for bugs that are easy to miss when the diff appears complete: fake green paths, mocks with production names, handler failures logged as success, tests that assert fixtures rather than behavior, swallowed errors, and runtime evidence that does not prove the claim being made.

Use it when a previous review missed obvious issues, when agent-generated code may have optimized for passing tests, or when mocks/fakes/simulated runtimes are present near a production-facing boundary.
