# Systematic Debugging QA Strategy

## Goal

Evaluate whether `systematic-debugging` reliably forces a root-cause-first debugging loop before code changes or workaround claims.

## Why This Skill Matters

This is the largest repo-local execution gap between Prodcraft and Superpowers. The key question is whether the skill:

- stops guess-first patching
- distinguishes live-incident containment from implementation debugging
- uses historical defect retrieval without anchoring blindly
- escalates structural mismatches through `course-correction-note`

## Initial Evaluation Mode

The first evaluation is a routed manual review using two scenarios:

1. a failing test in normal implementation flow
2. a contained hotfix where the code fix must follow incident containment

## Assertions

1. **root-cause-before-fix**
   - the output refuses code changes before the cause is evidenced

2. **incident-boundary-respected**
   - live containment routes through `incident-response` before code debugging proceeds

3. **historical-context-used-correctly**
   - bug history retrieval narrows hypotheses without replacing current evidence

4. **structural-escalation-present**
   - repeated failed fixes or architectural mismatch trigger `course-correction-note`

## Pass Standard

Treat the skill as strong review-stage evidence if it consistently outperforms a generic bug-fix baseline on root-cause discipline, incident boundary clarity, and structural escalation.

## Next QA Step

- add an isolated benchmark with repeated-fix and hotfix fixtures
- compare against a generic implementation baseline and the Superpowers debugging skill
