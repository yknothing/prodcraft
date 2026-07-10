# Execution P2 Hardening Design

> Status: approved for implementation on 2026-07-10

## Goal

Close the accepted Direction 2 P2 issues without adding resource-policy profiles or changing authority semantics.

## Decisions

1. Increase the fixed Git subprocess timeout from 5 seconds to 300 seconds. The timeout is a final liveness guard against blocking Git config/FIFO input, not a performance target. Large repositories are allowed to run slowly.
2. Keep strict JSON bounded at 16 MiB because route, state, and verification protocol documents are control records, not bulk evidence containers.
3. Hash raw evidence and governed regular files in fixed-size chunks. Worktree digest bytes and Git blob identity must remain byte-for-byte compatible with `git-worktree-content-v1`.
4. Add `--output-format json` while retaining the current text output and exit codes. JSON output has exactly `status`, `authority`, `candidate_completion_digest`, and `errors`.
5. Make the CLI test module work through both canonical discovery and package-module invocation.

## Non-Goals

- No named resource profiles, adaptive timeout, total-byte budget, scheduler, or host-specific override.
- No change to route/completion pin semantics, canonical paths, worktree scope, or v1 schemas.
- No authenticated identity, trusted clock, multi-writer concurrency, or Direction 3 runtime.

## Data And Error Flow

- Strict JSON opens one nonblocking, non-symlink regular-file descriptor, checks the 16 MiB size limit, reads once, and computes digest plus semantics from those bytes.
- Evidence SHA-256 reads the same safe descriptor in chunks and never materializes the complete file.
- Worktree capture writes canonical length prefixes to the existing digest, streams file chunks into both the worktree digest and Git blob digest, and fails if descriptor metadata changes during capture.
- A Git command that runs for 300 seconds fails with the existing `WorktreeSnapshotError`; no caller can disable the bound.
- JSON CLI output reports invalid candidate-only terminal state without upgrading it to authority.

## Compatibility

- Default CLI remains text.
- Existing text messages and nonzero candidate-only result remain unchanged.
- Existing `git-worktree-content-v1` digests remain unchanged for identical bytes.
- Existing direct function callers require no new arguments.

## Acceptance

- Oversized strict JSON fails before allocating its complete content.
- `file_sha256` and worktree capture pass while whole-file `Path.read_bytes()` is unavailable.
- A known fixture retains its pre-change worktree digest.
- Git timeout regression uses a patched short constant so the test remains fast; the production constant is asserted as 300 seconds.
- JSON output covers generic success, candidate-only terminal failure, and terminal authorization.
- Python 3.11 and 3.12 full suites, repository validator, Ruff, mypy, diff hygiene, skill frontmatter/reference/loadability, and self-hosted terminal authorization pass.

## Commit Boundaries

1. `docs(execution): define focused P2 hardening design`
2. `fix(execution): allow slow Git operations and stream file hashing`
3. `feat(cli): add structured execution authority output`
