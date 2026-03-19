**Assumption**: Since I am operating in a non-interactive environment, I will bypass the clarifying questions phase (Step 3) and proceed directly to proposing an intake approach based on the ambiguity stated in your request. The primary unknown is the scope (web only vs. all surfaces), which requires upstream framing before any technical specification or implementation begins.

Here is the intake assessment and proposed routing:

## Intake Brief

**Work type**: Enhancement
**Entry phase**: 00-discovery
**Recommended workflow**: agile-sprint
**Key skills needed**: problem-framing, specification, implementation
**Scope assessment**: medium (highly dependent on final surface target)
**Key risks**: 
- **Scope creep**: Attempting to implement across all surfaces without fully understanding the required effort.
- **Inconsistent UX**: Users encountering disjointed experiences if dark mode is only available in localized settings without a cohesive strategy.

### Proposed Path
Because the problem and solution direction are still too fuzzy for immediate specification, we should start with problem-framing.

1. **problem-framing** -- Define the target surfaces, align on the scope trade-offs (web-only vs. all surfaces), and establish the desired outcome.
2. **specification** -- Draft the technical spec defining color tokens, state management, and the implementation approach for the agreed-upon scope.
3. **implementation** -- Execute the code changes, add tests, and verify the dark mode experience.

### Alternative Approach
If minimizing time-to-market is the absolute priority, we can constrain the scope immediately:

1. **specification** -- Unilaterally scope the effort to an MVP for **web settings only**, detailing the tokens and boundaries.
2. **implementation** -- Deliver the web settings dark mode and treat other surfaces as separate, future enhancements. 

Please review and confirm which path you would like to proceed with, or let me know if we should adjust the scope.
