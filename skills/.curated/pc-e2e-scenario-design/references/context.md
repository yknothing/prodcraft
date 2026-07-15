# Context Notes

Use this skill when the existing test strategy is directionally correct, but the scenario depth is still too thin for real confidence. The failure mode it targets is not "there are no tests." It is "the tests pass, but the product still breaks under realistic extended use."

If every test in the suite can be described as "open X, do Y, see Z" in one sentence, the suite is shallow. It mostly verifies what the developer already checked manually. Real production failures happen at state accumulation, cross-boundary navigation, session re-entry, input boundaries, and mid-session dependency failure.

This skill does not replace `pc-testing-strategy`. `pc-testing-strategy` decides the test layers and coverage priorities. `pc-e2e-scenario-design` deepens the scenario and edge-case layers once that strategy exists.
