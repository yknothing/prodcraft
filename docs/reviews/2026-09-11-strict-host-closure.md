# Strict Host Closure and Prompt-Language Revalidation

Status: implementation complete; one controlled native Codex loop observed; no
maturity promotion and no demonstrated productivity improvement.

The September 11 maintainer request covers two reproduced integration failures,
a minimum strict loop on one available host, real task-outcome comparison, and
prompt-language usability. Scope follows the
[implementation plan](../plans/2026-09-11-strict-host-closure.md).

## Candidate and Deployment Boundary

The candidate is the working tree on `codex/strict-host-closure-20260911`, based on
`fd05978dbbbf5a064205a695af47c8a550f1b224`. Existing unrelated changes are preserved.
The evidence directory contains a content-hash inventory of the final implementation
and language-contract files: `02a2052830763367e3248535212dc6d176004ea03a75f967141c56e5ee6a9335`. This is not a new release commit or a globally
installed snapshot. No account settings, credentials, global skill installation,
or global strict-mode setting were changed in this repair task.

## Reproduced Defects and Repairs

- **Normal development environments:** worktree capture respects effective Git
  ignores and tracked gitlink boundaries. Ignored environments may contain their
  own `.gitignore`; clean initialized submodules may contain tracked ignore rules
  and ignored build output. Other work-item control roots remain governed,
  including nested submodules and gitlinks at reserved control-directory levels.
  Dirty/uninitialized submodules, unsafe paths, unmerged indexes and untracked
  effective ignore rules still fail closed. Thirty-five focused snapshot/completion
  tests and independent real Git reproductions passed after the boundary fixes.
- **Hook runtime:** the exact `.claude/settings.json` command now starts a
  standard-library bootstrap and then an explicitly selected Python 3.11/3.12
  with PyYAML/jsonschema. The actual settings command and actual repository
  validator passed an approved brief and blocked a draft while bootstrap
  `python3` lacked validator dependencies. Hook decisions never install packages.
- **Authoring:** the local CLI constructs derived records through the existing
  authority implementation, validates candidate bytes before writing, and checks
  the materialized closed bundle. It supports normal completion, block/resume,
  and rejected-attempt/fresh-retry paths without hand-editing derived fields.
- **Additional failures found during acceptance:** interrupted initialization
  result reporting, duplicate recovery mutation paths, oversized-result envelopes,
  same-second fractional verification timestamps, mixed completion snapshots,
  and native child processes surviving cancellation were repaired. Real file
  replacement/ABA and process-group tests cover the identified failures. Candidate
  and approved terminal digests are both bound to the state snapshot used by the
  host policy.

## Runtime and Authoring Operation

The one-time runtime setup and rollback commands are documented in the
[Claude adapter guide](../architecture/2026-07-16-claude-pretooluse-adapter.md).
The shared bootstrap supports `check` and `run validate|manage|pretooluse|codex`.
A hook or strict run fails with repair instructions if its configured runtime is
missing or unsupported; it does not silently switch interpreters.

The seven authoring commands are:

| Command | Operation |
| --- | --- |
| `route-draft` | Construct the exact route candidate for external review |
| `state-init` | Initialize from that candidate and its separately approved pin |
| `transition` | Append a valid lifecycle transition, including block/resume |
| `phase-event` | Enter or exit the current declared phase |
| `artifact-bind` | Bind an obligation to its exact artifact and assurance evidence |
| `claim-completion` | Bind actual verification and evidence to current work content |
| `record-outcome` | Record verified/rejected/completed outcomes with required pins |

Invoke `python3 scripts/prodcraft_runtime.py run manage -- COMMAND --help` for
arguments. Route/state initialization uses `--repo-root`, `--work-id`, the
reviewed route input and initial artifact bindings. Later writes require the
canonical `--state`, current `--expected-revision`, and externally supplied
`--approved-route-digest`. `claim-completion` takes the verification-record
reference and an input document containing exactly the `evidence_bindings` array.
Neither input nor a generated candidate counts as approval.

Writes use a per-work local advisory lock, revision checks, raw bundle freshness,
no-clobber creation and atomic state replacement. A competing writer fails
without mutation and must retry using the current revision. State initialization
journals exact bytes outside the excluded control bundle; retrying the same
initialization recovers only a proven predecessor/successor. Changed or partially
written recovery files require manual inspection and return `recovery-required`.
Other writes use atomic replacement; arbitrary crashes and power loss are not
claimed to have general transaction recovery. Reroute authoring is outside this
minimum slice. Per-document capacity reports the 12 MiB rollout-stop warning and
rejects candidates over the 16 MiB hard limit before canonical mutation.

## Enforced Native Surface

The exercised host is **Codex CLI 0.149.0 with `gpt-5.6-sol`**. Its actual default
model was identified from a native startup header. A newer model listed in the
shared cache was rejected by this CLI version; those failed runs are retained
and excluded from the successful comparison.

Start strict work through a trusted checkout separate from the governed repository:

```bash
python3 /absolute/trusted/prodcraft/scripts/prodcraft_runtime.py run codex -- \
  --state /absolute/work/.prodcraft/artifacts/WORK_ID/execution-state.json \
  --approved-route-digest "$REVIEWED_ROUTE_DIGEST" \
  --prompt-file /absolute/request.txt \
  --output-format json
```

The parent holds approval arguments, uses `--ignore-user-config`, `--ignore-rules`,
`--ephemeral`, native sandboxing and `approval_policy="never"`, and validates fresh
completion after native turn termination. Work mode grants the governed workspace
and only the Git authoring operational directory. A completed state is opened in
read-only mode even when its completion pin is missing. The trusted validator
checkout cannot overlap the governed repository. Timeout, SIGINT and SIGTERM
terminate the native process group, including tested tool children.

A verified-state pin can authorize its completed transition. The resulting
completed state requires a separately reviewed new pin. If native work leaves
verified state unchanged, the parent reports `incomplete` rather than requesting
its already supplied pin again. Only successful native termination plus fresh,
pinned canonical completed authority produces wrapper exit `0`. Other outcomes
exit `1`; blocked or approval-pending work remains interruptible. Model text,
including `Done`, cannot supply approval.

This governs the strict command's exit status and result. It does not control the
Codex desktop task checkbox, all Codex invocations, or completion in other hosts.
It is an opt-in completion boundary, not a claim that every tool action is
independently authorized by Prodcraft. The attempted model-driven sandbox sentinel
probe produced no command-execution event, so it is **not** evidence of an actual
blocked escape. The configured native sandbox boundary is retained; a malicious
executor or unrelated OS process is outside the claimed enforcement surface.

## Actual Native Loop

The isolated task required `normalize_label` to collapse Unicode whitespace,
reject non-string values with `TypeError`, and preserve non-whitespace text.
The initial five-test suite failed. Native Codex changed only `labels.py`, ran the
real tests, and used the authoring CLI to reach phase exit at revision `6`.

1. The repair turn returned native success but wrapper `incomplete`.
2. The parent independently checked the unchanged test-file digest, source-only
   diff, five passing tests and two additional edge cases. Actual output and a
   fresh work snapshot were bound through `claim-completion`; review produced
   verified revision `8` and its candidate pin.
3. Native Codex used the separately supplied verified pin to record completed
   revision `9`. The wrapper returned `approval-required`, not completion.
4. The parent checked unchanged source/tests and fresh closed evidence again,
   reviewed the new completed-state pin, and supplied it to a read-only native
   call. Native exit `0`, wrapper exit `0`, `status=completed` and
   `authority=terminal-authorized` were observed.

A separate actual native call without the completed pin returned `Done.` while
the wrapper still returned `approval-required`, null authority and exit `1`.
Source drift, missing/mismatched pins, stale revisions, failed verification,
rejected retries and native failure also have deterministic regressions against
the actual validator. External native-process doubles isolate that dependency;
authority decisions and file operations are not replaced by fabricated results.

## Bounded Task-Outcome Comparison

All arms used the same model, business source, five tests and defect request. Each
arm independently passed the tests and preserved the test file. No implementation
advantage was observed.

| Arm | Repair-turn seconds | Shell actions | Input tokens | Cached input tokens | Output tokens |
| --- | ---: | ---: | ---: | ---: | ---: |
| No workflow-skill invocation | 57.268 | 4 | 128335 | 116224 | 728 |
| Short generic guidance | 44.356 | 4 | 125035 | 113536 | 727 |
| Prodcraft routed strict work | 98.768 | 8 | 342052 | 309120 | 2797 |

The strict transition and final accepted native calls added 53.111 and 29.846
seconds. The three native stages total 181.725 seconds and 513860 input tokens
(449792 cached), excluding independent operator review time. Token numbers are
CLI-reported usage across calls, not maximum context size or billing estimates.

This is a single simple-task pilot with one repetition per arm, shared global
skill-catalog context, cache effects and concurrent execution. The baseline means
no workflow-skill invocation, not an empty skill-discovery environment. The runtime
was subsequently hardened for failures found while completing the loop. This is
not a statistically controlled, release-pinned productivity benchmark. No false
block occurred during the successful repair turn; the independent proof step
exposed the fractional-timestamp false block that was then fixed and regressed.

The observed benefit is explicit, inspectable completion authority and deliberate
review pauses. The observed cost is extra execution and review overhead. Keep
strict mode opt-in for work needing that assurance; this experiment does not
justify enabling it for every small task or claiming general productivity gains.

## Prompt Language and Limits

Current gateway/intake contracts select the current substantive request's
language. Explicit language requests take precedence; code, quoted content,
commands and paths do not select the presentation language. Human headings,
questions, status tags and completion feedback follow that language, while
canonical fields/enums, identifiers and original diagnostics retain their spelling.
Canonical repository artifact records remain English. The intake candidate stays
`review`; its previous evidence binding is preserved.

Six actual native source-contract samples passed presentation-language review:
English default, Chinese default, both explicit overrides, mixed Chinese prose
with English code terms, and an English follow-up with reconstructed prior Chinese
context. That follow-up is not a native resumed-session test. All displayed
identifiers retained their spelling; one Chinese response omitted the requested
`pc-intake` identifier instead of displaying it. These bounded samples do not
establish universal response or trigger reliability.

The strict wrapper also selects English/Chinese for its own status labels and
adds the selected language to the native prompt. Its local regressions cover
common explicit language expressions, quoted/code exclusions, already-approved
verified state, and Chinese startup errors with unchanged raw diagnostics. An
explicit `--locale en|zh-CN` overrides its bounded language heuristic.

Two supplementary full-wrapper native language reruns were blocked by automatic
approval review over transmission of state/approval context, including after
fixture-origin evidence was supplied. They were not executed. The accepted safe
alternative sent only hardcoded public fictional display text and the final
English/Chinese language directive in fresh empty directories: both actual native
responses used the expected language. No state, pins, source files or real task
metadata were sent in that alternative. Final wrapper logic is covered locally;
the report does not relabel the alternative as another complete native state run.

## Validation and Evidence

The final Python 3.11 suite passed **504 tests** in 70.626 seconds. Python 3.12
passed the broader 61-test snapshot/runtime slice and the final 18-test
authoring/host slice. Repository structural validation returned `valid` with
zero errors; `git diff --check` passed. Checks include curated parity and resource references,
frontmatter name/description requirements and length limits, and native package
loading. Gemini CLI's actual package loader loaded **46 source packages and 40
curated packages** with no failures; maximum description length was **303**.
No canary was injected or stripped. Native package parsing is separate from model
availability and behavior.

Claude's actual model call was rejected by organization subscription policy;
Gemini CLI 0.39.1 was rejected as `UNSUPPORTED_CLIENT` for the configured OAuth
account. Their native completion loops are not claimed. The actual Claude settings
command/validator integration is separately proven as described above.

Local evidence: `build/2026-09-11-strict-host-closure/`, including native JSON/JSONL
outputs, prompts, task comparison, independent tests, actual hook-command results,
language judgments, package-loader results, test logs and final content hashes.
The controlled fixtures contain generated toy tasks, not user production work.

Generated native test repositories were archived as `native-evaluation-fixtures.tar.gz`
and removed from the temporary directories. The final authority engine also
revalidated the live fixture before archiving and cleanup. Named scripts and logs
under the evidence directory are retained as reproducible acceptance artifacts.
