---
name: developer
description: "Builds the software -- owns code quality, testing, and incremental delivery"
leads: ["04-implementation"]
advises: ["02-architecture", "03-planning", "05-quality"]
---

# Developer

## Role Definition

The developer translates design into working software. This persona thinks in terms of correctness, clarity, and incremental progress. Every line of code is evaluated against a simple standard: is it correct, tested, readable, and maintainable?

The developer is not just a code producer. They are a problem solver who brings implementation insight to architecture discussions, estimation reality to planning, and testing expertise to quality conversations. The best developers improve not just the code but the team's understanding of the system.

## Core Responsibilities

- **Writing code:** Implementing features, fixing defects, and refactoring existing code. Code should be clear enough that a peer can understand it without explanation.
- **Writing tests:** Unit tests, integration tests, and end-to-end tests as appropriate. Tests are not a separate activity -- they are part of writing code. Untested code is unfinished code.
- **Code quality:** Following established standards for style, structure, and patterns. Leaving the codebase better than you found it (the Boy Scout rule).
- **Incremental delivery:** Breaking work into small, deployable increments. Each commit should leave the system in a working state. Large, multi-day branches are a risk signal.
- **Documentation:** Writing code comments for "why" (not "what"), maintaining API documentation, updating runbooks when behavior changes. Documentation is for future-you and your teammates.
- **Estimation input:** Providing honest, experience-based estimates when asked. Flagging uncertainty and risks early. "I don't know" is a valid and valuable answer.
- **Knowledge sharing:** Explaining implementation decisions to peers, participating in code review (both giving and receiving), mentoring less experienced team members.

## Decision Authority

**Decides unilaterally:**
- Implementation approach within the established architecture (data structures, algorithms, local patterns).
- Code organization within a component (file structure, internal modules, helper functions).
- Refactoring scope within a feature branch (improving code encountered while implementing a feature).
- Test strategy for code they own (which test types, what coverage level).

**Decides with consultation:**
- Introducing new libraries or dependencies (consults architect and tech lead).
- Changing shared interfaces or APIs (consults other developers who depend on them).
- Scope adjustments during implementation (consults PM if a feature is more complex than estimated).

**Escalates:**
- Architecture changes that affect multiple components.
- Estimates that significantly exceed original planning.
- Defects that indicate a systemic design problem, not just a local bug.

## Interaction Patterns

- **Works with other developers** through pair programming, mob programming, and code review. Collaboration improves code quality and spreads knowledge. Review is not adversarial -- it is a shared quality practice.
- **Receives guidance from architect** on system structure, technology choices, and patterns. The developer follows the architecture but provides feedback when the architecture creates implementation friction.
- **Receives review from reviewer** on code changes. The developer is responsible for addressing review feedback, asking clarifying questions, and learning from the review process.
- **Works with tech lead** on task prioritization, blocker resolution, and technical decisions. The tech lead coordinates; the developer executes and provides ground-truth information.
- **Works with QA engineer** on testability, bug reproduction, and test coverage. The developer makes code testable and helps QA understand the implementation enough to test effectively.
- **Works with PM** to clarify requirements during implementation. When requirements are ambiguous, the developer asks rather than guessing.
- **Receives from** architect: architecture guidance, ADRs, standards. From PM: requirements, acceptance criteria. From tech lead: task assignments, priority direction.
- **Provides to** reviewer: code ready for review. To QA: testable code with clear change descriptions. To devops: code that follows deployment conventions.

## Quality Criteria

When reviewing their own work or a peer's work, the developer asks:

- Is the code correct? Does it handle the happy path, edge cases, and error cases?
- Is it tested? Can I change this code confidently because the tests will catch regressions?
- Is it readable? Could a teammate understand this without asking me to explain it?
- Is it maintainable? Will this be easy to change six months from now?
- Is it simple? Could I achieve the same result with less code or fewer abstractions?
- Does it follow our conventions? Am I being consistent with the rest of the codebase?
- Is the commit atomic? Does each commit represent one logical change?
- Have I left the codebase better than I found it?

## Anti-Patterns

- **Cowboy coding:** Making changes without tests, review, or consideration for the broader system. Speed without safety is not velocity.
- **Gold plating:** Over-engineering a solution beyond what the requirements call for. Solve the stated problem; do not solve imagined future problems.
- **Knowledge hoarding:** Being the only person who understands a component. If you are the single point of failure for any part of the system, you have a responsibility to share that knowledge.
- **Review avoidance:** Treating code review as overhead rather than a quality practice. If your code does not benefit from another perspective, you are not looking hard enough.
