# Debug Expert Skill Design

Date: 2026-09-13
Status: implemented design; verification recorded below
Canonical skill: `pc-debug-expert` (formerly `pc-systematic-debugging`)
Reader guide: [Chinese companion](2026-09-13-debug-expert-design.zh-CN.md)

## Intended capability

Enable an agent to turn an observed software failure into the best justified
next action: a causal correction, safe mitigation, or a bounded diagnosis that
another engineer can continue. Optimize useful decisions and engineering
outcomes before process completeness or comparison scores.

An expert may resolve an obvious defect with one decisive check. An ambiguous
failure needs a system model, competing explanations and informative experiments.
Neither path requires an extra persona, subprocess, fixed hypothesis count,
mandatory journal file, or a new approval for already authorized work.

## Capability model

| Capability | Thinking and insight | Observable expert behavior | Skill support |
|---|---|---|---|
| Frame the failure | Distinguish the user's broken contract from an incidental error | State expected/actual behavior, affected population, trigger and stakes; question a misleading test oracle | Core process 1; feedback recipes |
| Reconstruct the system | Reason about data, control, state, time and ownership across boundaries | Identify the running artifact, entry point, path, producer and consumer; separate code identity from reachability | Core process 1; runtime and boundary recipes |
| Build useful feedback | A smaller reproducer is useful only if it retains the failure mechanism | Check that the signal detects the reported defect on the unfixed system; preserve relevant concurrency, permissions and state | Core process 2; reproduction, concurrency and performance recipes |
| Form and revise explanations | Use experience as a prior, maintain falsifiable alternatives, look for contradictions | Predict an observation, seek counterevidence, distinguish absent evidence from an observed absence; revise beliefs after each result | Core process 3; experiment selection |
| Choose informative actions | Balance discrimination, feasibility, disturbance, time and user impact | Prefer the next check whose possible outcomes change the next decision; stop repeating checks that add no information | Core process 3; worked discriminator example |
| Explain causes and interactions | Separate trigger, propagation, violated invariant, enabling conditions and failure to contain | Trace the earliest relevant divergence; test interacting conditions; distinguish introduced regression, unmasked defect and changed symptom | Boundary tracing; multi-cause recipes |
| Repair at the right boundary | Preserve contracts and compatibility; contain failure when the producer is unavailable or untrusted | Correct the cause under local control; use a bounded adapter workaround otherwise; distinguish justified validation from symptom suppression | Core process 4; fix-layer recipe |
| Close and transfer knowledge | Confidence is claim-specific and bounded by evidence | Verify the user-visible contract and nearby risks on identified revisions; preserve unresolved hypotheses, evidence and the next discriminator | Core process 5–6; existing I/O contract |

## Working principles and discipline

- **Curiosity with skepticism:** read the actual error chain and boundary values;
  a familiar stack trace suggests a check, not a preselected answer.
- **Causal precision:** separate observation, inference and intervention. A
  correlation, rollback recovery, or passing rerun may support several causes.
- **Systems judgment:** reason across abstraction boundaries before deciding
  where a defect belongs. More failed edits do not prove an architecture defect.
- **Experiment economy:** use existing evidence first. Prefer small reversible
  checks that distinguish live explanations; add instrumentation where it can
  change a decision. Multiple interacting variables may require a small matrix,
  rather than an absolute one-variable rule.
- **Production care:** preserve containment and evidence during live impact.
  Do not replay harm to obtain a stronger causal story. Passive diagnosis remains
  useful while incident owners restore service.
- **Adaptive persistence:** missing source, history, tests or active access limits
  particular claims, not all investigation. Continue independent authorized work;
  give a precise resumption condition for the dependent part.
- **Intellectual honesty:** report what would falsify the current explanation.
  Name uncertainty without manufactured percentages or ritual hypothesis quotas.
- **Engineering completion:** fix the user's broken contract, preserve relevant
  compatibility, verify nearby failure paths, and remove temporary probes.

## Runtime design

Keep one Skill and the existing output contracts. The main body carries the
adaptive decision loop and fixed/mitigated/diagnosis-limited boundaries. Existing
references carry detailed recipes, examples and resumption fields. References
are read on demand; their contents are not a mandatory checklist.

Concrete improvements over the previous design:

1. Define useful feedback explicitly, including failing oracle sensitivity and
   preservation of the real path, state and schedule.
2. Choose a discriminator by its predicted outcomes and resulting decisions,
   rather than mechanically trying a series of plausible patches.
3. Trace violated invariants through producers, transformations and consumers;
   separate triggers and enabling conditions from the correction boundary.
4. Supply executable reasoning for runtime/Skill loading, concurrency, performance
   and data/authorization invariants using existing tools, without new dependencies.
5. Replace premature "new signature = separate bug" and "serial green = fixed"
   shortcuts with comparisons that distinguish competing mechanisms.
6. Make investigation resumable through the existing report, with useful evidence
   links and rejected explanations, without a new artifact schema.

## Composition and migration

- Remove the newly introduced advisory `debug-expert` persona and registration.
  Preserve the existing developer, QA, tech-lead and incident-response boundaries.
- Rename the source and public package to `pc-debug-expert`. Update active routing,
  workflows, artifact consumers, registry entries and package references together.
  Do not keep a second Skill under the old name.
- Preserve historical eval directories and sealed records under
  `eval/04-implementation/pc-systematic-debugging/`. Those bytes evaluated the old
  identity and do not establish the redesigned Skill's effectiveness.
- Record current identity and local design validation in the manifest and evidence
  binding; retain the prior binding. Keep the redesigned Skill at `review`.
- Preserve old and new name detection in local benchmark isolation checks. Do not
  run a model benchmark as a side effect of a name migration.
- Existing global installations are outside this repository change. Their old
  explicit invocations must migrate when the new package is installed; no alias
  or automatic host modification is implied.

## Acceptance and limits

Local acceptance completed on 2026-09-13:

- One canonical source/public identity, `pc-debug-expert`; no old package or
  independent persona remains. Seven existing personas resolve all Skill roles.
- Source description is 215 characters. Skill-creator format validation, local
  resource checks, repository validation and aggregate context checks pass.
- Gemini CLI 0.39.1's native package parser reads all 46 source and 40 public
  packages with no failures. This proves file parsing, not host discovery,
  activation, model adherence or debugging benefit.
- All 58 historical evaluation files are byte-identical to the pre-change snapshot.
  Current QA plans use the new identity; old results are explicitly historical.
- Benchmark isolation regressions reproduced a missed new-name package and an
  ancestor-path false positive before correction. All 25 runner tests pass after
  correction; legacy detection and old metadata remain supported.
- Final repository suite: 508 tests pass in 63.157 seconds. The first run found
  two migration gaps in localized-document and eval-directory registration; both
  were repaired before the final full run. No model request was part of these tests.
- Independent design/contract review closed an external-boundary classification
  conflict and two documentation migration findings; no actionable findings remain
  in that bounded review. `git diff --check` passes.

The five changed package contracts are `pc-debug-expert`, `pc-intake`,
`pc-task-execution`, `pc-receiving-code-review` and `pc-incident-response`.
Only the debugging Skill's substantive method changed; the other four replace
the referenced canonical name. Their prior statuses and evidence remain recorded.

Local snapshots, exact contract migration, native parsing results, regression logs
and the scoped diff are retained for reproducibility under the ignored
`build/2026-09-13-debug-expert-design/` directory. These are local QA artifacts,
not portable published evidence. No global installation, commit, push or external
behavior benchmark was performed by this change.

The capability map and its methods are design decisions. They do not establish
superiority over another Skill or a measured increase in debugging success.
Future behavioral evaluation should use runnable failures without supplied
answers, equal tools/model/budget, and outcome checks independent of this Skill's
wording. Diagnostic quality, harmful interventions, useful experiment choice and
real correction matter more than adherence to a fixed process.

The [current evaluation strategy](../../eval/04-implementation/pc-debug-expert/eval-strategy.md)
keeps this plan under the new identity while leaving historical results untouched.
