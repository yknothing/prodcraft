# Strict Host Closure and Language Usability Implementation Plan

**Goal:** Repair the two reproduced integration failures, make one Codex CLI workflow complete through the existing strict authority engine, and evaluate task outcomes and prompt-language behavior on the resulting candidate.

**Authority:** The maintainer explicitly requested these repairs and the minimum single-host strict loop on September 11. This selects the existing Direction 2 adoption design's core authoring path; it does not enable strict mode globally or authorize a new service architecture.

**Architecture:** Reuse `tools/execution_state.py`, `tools/execution_validation.py`, the v1 artifact/result schemas, and external route/completion pins. Add the planned local authoring CLI and an opt-in Codex completion wrapper. Preserve a guidance-only path when strict mode is not explicitly configured. Follow the user's prompt language in user-visible responses, headings, and labels; preserve canonical protocol values and source identifiers.

**Execution:** Use `pc-tdd` for executable changes and direct contract/reference checks for prose changes. Work through the following bounded slices; reuse the accepted [adoption implementation plan](2026-07-12-direction2-adoption-implementation-plan.md) for state semantics, locking, recovery, and exact capacity rules. Existing unrelated working-tree changes are preserved.

## Acceptance and implementation slices

### 1. Correct Git snapshot boundaries

Files: `tools/execution_state.py`, `tests/test_execution_state_io.py`.

- [x] Add regression cases for an ignored environment with its own `.gitignore`, an initialized clean submodule with its own tracked ignore rules, and ignored submodule build output.
- [x] Observe failure on the existing implementation.
- [x] Respect the parent Git index's gitlink boundaries and effective tracked ignore rules. Continue rejecting untracked ignore rules that could hide governed files, unsafe paths, dirty/uninitialized submodules, and unmerged indexes. Keep other work-item control roots governed.
- [x] Run `python -m unittest tests.test_execution_state_io tests.test_execution_state_completion -q` and repeat the native `uv venv` reproduction.

### 2. Make hook runtime setup explicit and reproducible

Files: `.claude/settings.json`, `.claude/hooks/prodcraft_pretooluse.py`, an explicit repository-owned runtime launcher/setup command, `tests/test_claude_pretooluse_adapter.py`, and the adapter documentation.

- [x] Test the actual settings command under a PATH without validator dependencies, rather than invoking the hook through the QA interpreter implicitly.
- [x] Provide an explicit, validated Python 3.11/3.12 runtime with the existing PyYAML/jsonschema dependencies. Hooks must never install dependencies or access the network while deciding a tool action.
- [x] Expose a readiness check and actionable environment-repair instructions. Keep invalid or unavailable configured enforcement fail-closed.
- [x] Retain candidate confirmation, draft recovery, snapshot/alias protection, and legacy behavior. Run the configured launcher and its native host integration, not just a direct Python unit test.

### 3. Finish the existing core state-authoring path

Files: planned `tools/execution_authoring.py`, `tools/execution_result.py`, `scripts/manage_execution_state.py`, focused authoring/CLI/recovery tests, and the existing validation service when a shared contract seam is required.

- [x] Implement the planned commands `route-draft`, `state-init`, `transition`, `phase-event`, `artifact-bind`, `claim-completion`, and `record-outcome`.
- [x] Reuse canonical digest/projection and semantic validation functions. Validate exact candidate bytes before materialization and the actual bundle after writing.
- [x] Enforce safe create paths, a per-work local lock, expected revision, raw-file freshness, atomic replacement, and recoverable state-init materialization. Preserve externally supplied pins and the verified-to-completed repin.
- [x] Reject invalid, stale, unsafe, over-capacity, and mismatched-pin requests without canonical mutation. Distinguish unresolved materialization as `recovery-required`.
- [x] Exercise normal completion, block/resume, and rejected-attempt/fresh-retry workflows without manual derived-field edits. Reroute authoring remains outside this minimum slice.

### 4. Connect one host to completion authority

The native target changed to Codex CLI after actual Claude organization-policy and Gemini account/client failures. The Claude PreToolUse runtime repair remains separately verified through the exact settings command.

Files: a Codex CLI completion wrapper, explicit opt-in host configuration/setup, and adapter integration tests/documentation.

- [x] Bind the selected work ID and externally supplied route/completion approval to the repository-owned authority command. Approval inputs must remain outside the agent-writable control bundle and must not be inferred from a generated digest.
- [x] A configured strict completion boundary accepts only the canonical completed state with current terminal authority. Missing state, stale work, missing/mismatched pins, and rejected attempts cannot pass as completed.
- [x] Keep a blocked or approval-pending run honestly interruptible; avoid a Stop-hook loop that prevents the user receiving a request for the required approval.
- [x] Demonstrate a native Codex CLI path through the opt-in strict wrapper, plus negative cases at the host/CLI boundary. Document the exact enforced surface and retained host-permission boundary.

### 5. Follow the user's language consistently

Files: `CLAUDE.md`, `skills/_gateway.md`, the gateway renderer, intake presentation/I/O guidance, any exposed new launcher/adapter messages, and language contract tests. Regenerate curated output rather than editing it directly.

- [x] Default to the current substantive user request's language: English request -> English; Chinese request -> Chinese. Explicit language selection wins; code/paths alone do not switch the response language. For mixed prose, use the dominant substantive language and retain an established locale if ambiguous.
- [x] Apply that language to prose, headings, human-facing tags/status labels, questions, and completion feedback. Preserve code, commands, paths, API names, canonical machine fields/enums, and quoted original diagnostics.
- [x] Keep canonical repository artifact records in English where required; present their summaries and display labels in the user-facing locale.
- [x] Check English and Chinese prompts, explicit overrides, mixed prose, follow-up locale changes, and literal code/protocol preservation. Rebind changed skill candidates without maturity promotion.

### 6. Verify operation and actual task outcomes

- [x] Run focused failing-then-passing regressions, full repository structural/contracts checks, relevant Python 3.11/3.12 checks, curated parity/references, description/name bounds, and native package loading.
- [x] Review the completed authority, filesystem, host, and language boundaries adversarially under the existing adoption acceptance requirements.
- [x] Execute a bounded real-task comparison using the existing no-skill / short-guidance / Prodcraft design. Preserve candidate, host/model, prompts, actual actions, results, elapsed time, approval/false-block counts, and available usage. Keep acceptance independent of process wording and report inconclusive results as such.
- [x] Record the final candidate and installation/host scope separately from source validation and semantic outcomes. Do not treat a fresh hash, a synthetic workflow, or file parsing as a productivity gain.

## Alternatives and rollback

The selected approach is the existing local CLI plus a single host adapter. A new orchestration service would add identity, persistence, scheduling, and operating obligations that are unnecessary for this scope. A prompt-only workaround would leave the demonstrated integration gap unresolved.

Snapshot fixes retain the declared whole-worktree identity policy. Runtime setup is explicit and can be disabled through the documented host configuration rollback. Strict host binding remains opt-in. Authoring changes preserve v1 history and must not rewrite accepted artifacts on rollback; remove the adapter/binding to restore guidance-only operation while keeping evidence available for inspection.

## Acceptance result

See the [final review and evidence record](../reviews/2026-09-11-strict-host-closure.md). The single simple-task comparison found no productivity improvement; strict completion adds deliberate review/approval cost. Native language samples are bounded and do not establish general model reliability. The strict wrapper is opt-in and does not control the Codex app task checkbox or other host completion surfaces. Global installed snapshots remain unchanged.
