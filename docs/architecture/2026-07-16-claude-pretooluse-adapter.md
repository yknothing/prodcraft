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
binds the preflight to the current work directory. The exact first `Write` to
that path is the bootstrap escape; no other Edit or Write proceeds until the
brief is structurally valid, `status: approved`, and has a non-empty approver.
Artifact-instance CLI invocations validate only the supplied instance unless
the caller explicitly adds `--check`; unrelated repository-wide drift cannot
lock every governed write.

After validation, the adapter securely reopens the canonical brief and requires
the file identity and bytes to match the validated snapshot. A symlinked parent,
file replacement, or content change fails closed. This binds one hook decision
to one stable brief snapshot. It does not claim to prevent an unrelated process
from changing repository state after the `PreToolUse` decision has returned;
that later event belongs to the host/tool execution boundary.

`micro` briefs do not grant blocking adapter authority. The schema records the
eligibility assertions, but micro approval is still notify-and-proceed rather
than an independent blocking confirmation. Use `fast-track`, `full`, or
`resume` for this adapter.

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
validator-time brief replacement; validator failure; bootstrap behavior; and
the required blocking exit code.
