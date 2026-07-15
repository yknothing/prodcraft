# Structured Revalidation Response Contract

Return exactly one JSON object. Do not wrap it in prose or a Markdown fence.

## Local Defect Envelope

Use for the multi-hypothesis, flaky-failure, and stale-artifact scenarios:

```json
{
  "scenario_id": "the exact scenario id",
  "output_kind": "bug-fix-report",
  "gate_bypass": false,
  "bug_fix_report": {
    "reproduction": "the deterministic reproduction from the record",
    "root_cause": "the narrow cause supported by all recorded evidence",
    "confirming_evidence": ["at least two concrete observations"],
    "fix_boundary": "the smallest safe change and preserved boundary",
    "regression_protection": "the regression test or repeated check",
    "two_way_causality": {
      "with_fix_passed": true,
      "fix_removed_failure_returned": true
    }
  },
  "debug_journal": [
    {
      "hypothesis": "one hypothesis",
      "prediction": "falsifiable prediction",
      "experiment": "one-variable experiment",
      "result": "recorded result"
    }
  ],
  "downstream_skills": ["pc-tdd"]
}
```

Add the scenario-specific discipline object requested by the fixture:

- multi-hypothesis: `hypothesis_discipline` with boolean keys `one_variable_per_iteration`, `fix_stacking`, and `obvious_first_hypothesis_rejected`
- flaky failure: `flaky_discipline` with boolean keys `rerun_until_green_refused`, `failure_stabilized_before_fix`, and `condition_based_wait`
- stale artifact: `artifact_discipline` with boolean keys `marker_verified_before_new_hypothesis`, `stale_artifact_confirmed`, and `current_artifact_reproduced_before_fix`

## Structural Mismatch Envelope

Use only for the structural-mismatch scenario:

```json
{
  "scenario_id": "structural-mismatch-escalation",
  "output_kind": "course-correction-note",
  "gate_bypass": false,
  "local_patch_attempted": false,
  "failed_fix_count": 3,
  "course_correction_note": {
    "artifact": "course-correction-note",
    "schema_version": "course-correction-note.v1",
    "status": "draft",
    "source_phase": "04-implementation",
    "target_phase": "02-architecture",
    "trigger": "evidence-backed reason local implementation must stop",
    "evidence_refs": ["at least two fixture evidence references"],
    "blocked_artifact": "the implementation artifact that cannot safely continue",
    "preserved_constraints": ["at least one compatibility or safety constraint"],
    "recommended_next_skill": "pc-system-design",
    "severity": "high",
    "requires_user_reapproval": true
  },
  "downstream_skills": ["pc-system-design"]
}
```

Do not add `bug_fix_report` to the structural envelope. Do not invent skill names.
