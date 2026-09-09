# Anti-Pattern Notes

1. **Test-after rationalization** -- "I'll write tests after I code." You won't, and the design suffers.
2. **Testing implementation, not behavior** -- Testing that a private method is called is fragile. Test the public behavior.
3. **Giant test setup** -- If setup is 50 lines, the unit under test is too large. Break it down.
4. **Ignoring the REFACTOR step** -- RED-GREEN without REFACTOR accumulates design debt rapidly.
5. **100% coverage obsession** -- Coverage is a guide, not a goal. 80% thoughtful coverage beats 100% mechanical coverage.
6. **Skipping safety-net tests in brownfield work** -- Writing only the new happy-path test while leaving coexistence, unsupported-flow, or legacy-read behavior unprotected.
7. **Retroactive RED claims** -- Calling a post-implementation green run test-first evidence. Isolate the owned patch, establish failure against the unchanged baseline, and record the actual order.
