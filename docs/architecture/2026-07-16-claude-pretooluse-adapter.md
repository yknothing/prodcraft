# Claude Code Approved-Intake PreToolUse Adapter

## Status

Implemented as a legacy-mode repository preflight. It is not ADR-003 execution
authority.

## Mirrored Contract

The project-scoped `.claude/settings.json` hook matches Claude Code `Edit` and
`Write`, then calls `.claude/hooks/prodcraft_pretooluse.py`. The adapter reads
the canonical brief without following any symlink path component, copies those
exact bytes to a private snapshot, and calls the repository-owned validator:

```bash
python scripts/validate_prodcraft.py \
  --artifact-instance <private-snapshot>/intake-brief.json \
  --output-format json
```

Set `PRODCRAFT_WORK_ID` before starting a new Claude Code session. The adapter
looks only at `.prodcraft/artifacts/$PRODCRAFT_WORK_ID/intake-brief.json`, which
binds the preflight to the current work directory. A complete `Write` to
that canonical path can bootstrap or repair the brief; no other Edit or Write proceeds until the
brief is structurally valid, `status: approved`, and has a non-empty approver.
Artifact-instance CLI invocations validate only the supplied instance unless
the caller explicitly adds `--check`; unrelated repository-wide drift cannot
lock every governed write.

Bootstrap and repair validate the proposed content through the same repository
validator before returning. An existing draft or malformed JSON may be replaced
with a valid draft. Drafts do not authorize ordinary work. Use complete `Write`
replacement for this control file; `Edit` cannot bypass candidate validation.
A new or changed non-micro approved candidate returns
`hookSpecificOutput.permissionDecision: "ask"` to the host. An identical approved
record needs no new approval. The adapter never emits `allow`; ordinary host
permissions still apply. The host confirmation covers the displayed intake and
scope, not strict execution authority. See the official
[PreToolUse decision contract](https://code.claude.com/docs/en/hooks#pretooluse-decision-control).

After validation, the adapter securely reopens the canonical brief and requires
the file identity and bytes to match the validated snapshot. A symlinked parent,
file replacement, or content change fails closed. This binds one hook decision
to one stable brief snapshot. It does not claim to prevent an unrelated process
from changing repository state after the `PreToolUse` decision has returned;
that later event belongs to the host/tool execution boundary.

Reads use nonblocking descriptors before checking the regular-file type, so a
FIFO is rejected immediately. Repair preserves path and snapshot checks;
symlink aliases, symlinked parents, special files, and validation-time replacement
remain blocked. The hook is an Edit/Write preflight, not a filesystem security
boundary against unrelated tools or processes.

Updated October 2: valid compact `micro` records are accepted as bookkeeping,
with no permission override when storing the record. Each subsequent work
`Edit`/`Write` returns `permissionDecision: "ask"`, so micro never grants
write authority. Non-micro approval behavior remains unchanged. The record
must pass the same schema, path, and snapshot checks before either decision.

## Failure Semantics

Every malformed input, missing dependency, validator rejection, timeout,
symlink, wrong work directory, or unexpected exception maps to exit code `2`.
Claude Code treats exit `2` from `PreToolUse` as blocking; exit `1` is not a
blocking policy result, so the adapter never forwards the validator return code
unchanged.

## Authority Boundary

Generic `--artifact-instance` validation proves artifact structure only. It
does not return `gate-authorized` or `terminal-authorized`. Strict execution
authority still requires the canonical
`.prodcraft/artifacts/<work_id>/execution-state.json`, the external route pin,
and the external completion pin defined by ADR-003. The adapter does not persist
or infer those pins.

Codex, Gemini, and other hosts remain prose-gated unless they explicitly bind
this same repository-owned CLI. No cross-host enforcement claim is made.

Project settings are loaded at Claude Code session start. Restart the session
after changing the hook configuration.

## Evidence

`tests/test_claude_pretooluse_adapter.py` exercises a scratch repository with
missing, draft, invalid, micro, wrong-work, and symlinked briefs and parents;
validator-time brief replacement; validator failure; FIFO rejection; draft and
malformed-content recovery; approved-candidate confirmation; and the blocking
exit code. A real-validator integration case covers draft -> approved -> ordinary
write and rejects an unknown routed skill. This does not establish live Claude
UI confirmation behavior; no fresh native Claude session was run for the repair.


## Explicit Python Runtime

The settings command is `python3 scripts/prodcraft_runtime.py run pretooluse`.
The bootstrap uses only the standard library, then executes the configured
Python in isolated mode. Configure the supported runtime once, outside hooks:

```bash
uv venv --python 3.11 build/prodcraft-runtime
uv pip install --python build/prodcraft-runtime/bin/python PyYAML==6.0.3 jsonschema==4.26.0
python3 scripts/prodcraft_runtime.py setup --python "$PWD/build/prodcraft-runtime/bin/python"
python3 scripts/prodcraft_runtime.py check
```

Python 3.11 and 3.12 are supported. `setup` validates an existing interpreter and
its dependencies; `check` and hook execution never install packages or use the
network. The selection is stored in `build/prodcraft-runtime.json`. A missing,
unsupported or dependency-incomplete configured runtime fails with actionable
setup instructions. Hook failures retain blocking exit code `2`.

The September 11 acceptance invoked the exact settings command with the actual
repository validator while bootstrap `python3` lacked PyYAML: the approved brief
passed with exit `0`, and the draft brief blocked with exit `2`. Claude's native
model call was unavailable because of organization subscription policy. This
configured-command proof does not claim native Claude completion-hook support.
The separate [Codex strict closure](../reviews/2026-09-11-strict-host-closure.md)
is the currently exercised native completion surface.

To roll back this runtime integration, restore the previous project hook
configuration or remove its PreToolUse entry. Removing only the runtime config
while the hook remains enabled intentionally leaves the hook fail-closed.
