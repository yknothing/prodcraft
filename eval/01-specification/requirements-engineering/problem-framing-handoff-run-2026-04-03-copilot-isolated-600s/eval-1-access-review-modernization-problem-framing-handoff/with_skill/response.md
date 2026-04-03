● I'll read the skill definition first, then apply it to the problem framing document.

✓ List directory skill-under-test (7 files)

✓ Read access-review-modernization-problem-framing.md (73 lines)

✓ Read skill-under-test/SKILL.md (139 lines)

✓ Create requirements-doc.md (+170)

● Done. I've produced `requirements-doc.md` that:

   1. **Preserves the campaign-and-evidence-first direction** from Option 1 with P0 requirements
   for campaign management, delegated approvals, and evidence export
   2. **Keeps work at requirements layer** - no architecture decisions, solution specifications, or
    technology choices
   3. **Preserves all non-goals** (no full replacement, no irreversible cutover, no pretending sync
    is settled)
   4. **Preserves all open questions** with clear ownership markers and traceability to affected
   requirements
   5. **Maintains brownfield coexistence** as P0 requirement without forcing migration decisions
   6. **Marks assumptions explicitly** - NFRs without source-driven bounds are labeled as
   assumptions requiring review
   7. **Shapes for downstream work** - clear handoff to system-design only after review, with
   traceability and prioritization ready for acceptance-criteria or specification work
