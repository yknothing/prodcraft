# Debug Expert Evaluation Strategy

Status: planned behavioral evaluation; no candidate model runs recorded here.

The current candidate is [pc-debug-expert](../../../skills/04-implementation/pc-debug-expert/SKILL.md).
The [design and local acceptance record](../../../docs/architecture/2026-09-13-debug-expert-design.md)
defines its capabilities and records the checks actually performed.

## Questions and Cases

Evaluate whether the Skill improves useful diagnostic decisions and real corrections.
Use executable failures or constrained evidence investigations, with no root-cause
answer, intended fix or evaluator acceptance tests in the executor prompt.

| Case family | Outcome to observe |
|---|---|
| Obvious local defect | Correct repair without unnecessary investigation rituals |
| Conflicting runtime/source evidence | Identification of the actual failing boundary before unrelated code changes |
| Stateful, concurrent or intermittent fault | A feedback signal that preserves the mechanism, and a correction that preserves valid concurrent behavior |
| Workload-dependent performance regression | Explained measured improvement with correctness and relevant resource tradeoffs preserved |
| Changed symptom after a patch | Correct classification of introduced regression, exposed defect or persistent mechanism |
| Missing source, history or active access | Useful bounded progress, explicit missing discriminator and safe resumption |
| External dependency or trust boundary | Correct distinction between an owned-contract repair and a temporary dependency workaround |

## Bounded Comparison Plan

Compare the candidate with the preceding Skill snapshot and a no-Skill baseline on
matched failures. Add a separately pinned reference Skill only when a direct superiority
claim is the decision being evaluated. Keep model, tools, permissions, environment and
budget equal; isolate runs and retain original actions, outputs and resulting patches.
Include each Skill's relevant support resources and avoid leaking solutions through
shared workspaces, histories or evaluator notes.

Judge real correction, causal evidence quality, harmful changes, useful versus wasted
checks, manual intervention and ability to resume. Use independent outcome checks,
not required headings, fixed step counts or text copied from the Skill. Repeat close
comparisons as justified by observed variance; a few successful samples are not broad
capability proof. Capture the candidate digest and exact evaluation conditions.

## Historical Identity

The 58 existing files under `eval/04-implementation/pc-systematic-debugging/` retain
the old Skill's identity and bytes. They are historical evidence, not current candidate
results. The redesigned Skill remains `review`; local structural or native parsing
checks do not promote it or establish measured debugging benefit.
