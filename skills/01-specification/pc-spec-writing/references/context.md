# Context Notes

Spec writing is the heaviest specification skill, used primarily in spec-driven and waterfall workflows. In greenfield work, it can be used in a lighter form to lock the first-release contract before architecture begins. In brownfield work, it documents current behavior, target-state boundaries, or modernization constraints that downstream design and implementation must not rediscover from scratch.

Do not reach for this skill during routine agile story refinement. In day-to-day sprint work, prefer lightweight requirements, acceptance criteria, and task breakdown unless the change is large enough to need a shared written contract.

The core contract of this skill is not "write more detail." It is to freeze the boundary between:

- what release 1 must do
- what is explicitly out of scope
- which constraints downstream architecture must preserve
- which open questions remain visible instead of being silently guessed away
