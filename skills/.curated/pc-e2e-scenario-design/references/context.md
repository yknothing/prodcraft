# Context Notes

Use this skill when the existing test strategy is directionally correct, but the scenario depth is still too thin for real confidence. The failure mode it targets is not "there are no tests." It is "the tests pass, but the product still breaks under realistic extended use."

Judge depth by the risk and state boundaries exercised, not sentence or step count. A short flow may prove a critical invariant; a long UI-only flow may not. Look for missing accumulation, re-entry, input-boundary, and dependency-failure checks where the product actually needs them.

This skill does not replace `pc-testing-strategy`. `pc-testing-strategy` decides the test layers and coverage priorities. `pc-e2e-scenario-design` deepens the scenario and edge-case layers once that strategy exists.
