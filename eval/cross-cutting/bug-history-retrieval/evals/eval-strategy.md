# Bug History Retrieval Evaluation Strategy

## Goal

Evaluate whether `bug-history-retrieval` finds canonical historical evidence for a current failure and turns that evidence into an explicit next action instead of a vague "seen before" claim.

## Why Routed Review First

This skill is routed because its value comes from using live source-of-truth systems, not from trigger discoverability.
The first question is whether the skill can recover a reliable defect lineage from canonical records before downstream debugging or incident work begins.

## Scenarios

1. `access-review-modernization` regression symptom with a known error string and a deployment window.
2. Repeated incident pattern with a commit or revert candidate in git history.
3. Ambiguous operational symptom where tracker and monitoring results may point to different historical matches.

## Assertions

1. It queries canonical sources before relying on memory or local notes.
2. It distinguishes probable matches from useful analogs and keyword noise.
3. It extracts fix lineage, including versions, commits, reverts, or workarounds when available.
4. It does not overclaim that a closed record is fixed in the currently affected release.
5. It ends with a concrete next step such as debugging, incident response, or debt tracking.

## Method

1. Run a baseline retrieval pass without the skill.
2. Run the same query with `bug-history-retrieval` explicitly invoked.
3. Compare the two outputs for evidence quality, lineage completeness, and next-action clarity.
4. Record the strongest canonical match and the confidence level for each match class.

## Exit Criteria for Review Stage

- At least one canonical source is queried for each scenario.
- The output includes a ranked match list with evidence.
- At least one scenario yields a defensible next action grounded in history.
- Review-stage evidence shows the skill narrows the investigation rather than widening it.
