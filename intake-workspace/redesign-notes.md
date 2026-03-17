# Intake Entry-Stack Redesign Notes

## Why Intake Returned to `review`

`intake` previously had evidence as a strong discoverability skill and as an explicit-entry gate. The entry-stack redesign keeps its routing role but changes the body contract in two important ways:

1. Intake is now explicitly limited to **routing and path comparison**, not full concept exploration.
2. Intake now has a formal downstream handoff to `problem-framing` when the route is clear but the problem or direction is still fuzzy.

Those changes preserve the original trigger intent but alter the skill's operational behavior enough that the previous `tested` status should not be treated as fully current.

## What Must Be Re-Evaluated

- Trigger eval: confirm the description still triggers appropriately after the tighter scope language
- Explicit benchmark: confirm the revised intake body still improves routing discipline without over-questioning
- Integration review: confirm `intake-brief` now captures enough observability for handoff to `problem-framing` or direct downstream skills

## Design Constraints Added in This Redesign

- Keep intake concise: default to 1-3 questions, stop when routing is clear
- Preserve observability: record why intake was used, which answers changed routing, which path was chosen, and what skill comes next
- Avoid role collapse: route to `problem-framing` instead of expanding intake into a full design workshop
