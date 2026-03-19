**Assumption:** Since we are operating in a non-interactive environment, I am bypassing the clarifying questions step. I assume the goal is a zero-downtime transition, the constraints involve backwards compatibility with legacy rules, and the quality bar is production-grade.

## Intake Brief

**Work type**: Migration
**Entry phase**: 00-discovery
**Recommended workflow**: brownfield
**Key skills needed**: problem-framing, software-architecture, writing-plans
**Scope assessment**: xlarge (multi-quarter)
**Key risks**: 
- Disrupting existing user access during the transition.
- Uncovering undocumented legacy permission rules that require complex mapping.

### Proposed Path
1. `problem-framing` -- Define the exact scope, uncover legacy constraints, and establish the functional boundaries of the new access-review system.
2. `software-architecture` -- Design the transitional architecture (e.g., dual-writing, strangler fig pattern) for a safe, phased migration.
3. `writing-plans` -- Create a detailed implementation plan broken down by milestone/quarter to guide the engineering effort.

### Alternative Approach
If the legacy permissions model only affects a small subset of isolated features, we could perform a single "big-bang" cutover per service rather than a gradual system-wide migration, which would reduce transitional architectural complexity but increase deployment risk.
