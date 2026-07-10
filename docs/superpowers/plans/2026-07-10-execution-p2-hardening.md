# Execution P2 Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove Direction 2 memory-pressure and short-timeout P2 issues and expose a stable machine-readable authority result without changing existing authority semantics.

**Architecture:** Preserve the current strict descriptor and canonical digest boundaries. Bound strict JSON, stream bulk bytes through existing hashes, widen the fixed Git liveness timeout, and project existing validation state into optional JSON output.

**Tech Stack:** Python 3.11/3.12 standard library, `unittest`, existing JSON Schema validator and Prodcraft CLI.

---

### Task 1: Stream file hashing and allow slow Git operations

**Files:**
- Modify: `tools/execution_state.py`
- Modify: `tests/test_execution_state_io.py`
- Modify: `docs/architecture/2026-07-10-minimal-execution-loop.md`
- Modify: `docs/architecture/2026-07-10-minimal-execution-loop-acceptance.md`

- [ ] **Step 1: Write failing resource-boundary tests**

Add tests that patch `STRICT_JSON_MAX_BYTES` to a small value, assert a larger JSON file raises `StrictJSONError`, assert `GIT_COMMAND_TIMEOUT_SECONDS == 300`, and patch `Path.read_bytes` to fail while `file_sha256` and `capture_git_worktree` still succeed.

- [ ] **Step 2: Run RED**

Run `python3 -m unittest tests/test_execution_state_io.py`.

Expected: FAIL because the size constant and streaming behavior do not exist and the timeout is still 5.

- [ ] **Step 3: Add safe descriptor streaming**

Add these constants to `tools/execution_state.py`:

```python
STRICT_JSON_MAX_BYTES = 16 * 1024 * 1024
FILE_HASH_CHUNK_BYTES = 1024 * 1024
GIT_COMMAND_TIMEOUT_SECONDS = 300
```

Factor the existing `lstat`/`os.open`/`fstat` checks into one context-managed regular-file descriptor. Use a limited read for strict JSON, chunked reads for `file_sha256`, and chunked updates to the unchanged worktree and Git blob digests.

- [ ] **Step 4: Preserve digest identity**

Before replacing `_snapshot_entry`, record the deterministic fixture digest. After streaming, assert the fixture produces the same digest and file mutation still changes it.

- [ ] **Step 5: Run GREEN**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_execution_state*.py'
ruff check tools/execution_state.py tests/test_execution_state_io.py
mypy tools/execution_state.py
```

Expected: all pass.

- [ ] **Step 6: Update architecture wording**

Replace the five-second residual risk with the 300-second liveness guard, document strict JSON rejection, and mark evidence/worktree memory pressure closed through streaming.

- [ ] **Step 7: Commit**

```bash
git add tools/execution_state.py tests/test_execution_state_io.py docs/architecture/2026-07-10-minimal-execution-loop.md docs/architecture/2026-07-10-minimal-execution-loop-acceptance.md
git commit -m "fix(execution): allow slow Git operations and stream file hashing"
```

### Task 2: Add machine-readable authority output

**Files:**
- Modify: `tools/execution_state.py`
- Modify: `scripts/validate_prodcraft.py`
- Modify: `tests/test_execution_state_cli.py`
- Modify: `README.md`
- Modify: `README.zh-CN.md`

- [ ] **Step 1: Write failing CLI contract tests**

Add subprocess tests for `--output-format json` that parse stdout and assert these exact keys:

```python
{
    "status": "invalid",
    "authority": None,
    "candidate_completion_digest": "sha256:<64 lowercase hex>",
    "errors": ["<candidate-only error>"],
}
```

Also test generic success, terminal-authorized success, and package-module invocation.

- [ ] **Step 2: Run RED**

Run `python3 -m unittest tests.test_execution_state_cli`.

Expected: FAIL because the option is unknown and the sibling fixture import is not package-safe.

- [ ] **Step 3: Carry candidate metadata explicitly**

Extend `ValidationResult` with:

```python
candidate_completion_digest: str | None = None
```

Set it only when a valid terminal bundle lacks the completion pin. Return the result from authority validation even when it is non-authoritative so presentation never parses error text.

- [ ] **Step 4: Render stable JSON**

Add `--output-format {text,json}` with default `text`. JSON mode prints one sorted object with `status`, `authority`, `candidate_completion_digest`, and `errors`; text mode keeps current output and exit status unchanged.

- [ ] **Step 5: Run GREEN**

Run:

```bash
python3 -m unittest tests.test_execution_state_cli
python3 -m unittest discover -s tests -p 'test_execution_state*.py'
```

Expected: all pass and existing text assertions remain unchanged.

- [ ] **Step 6: Document and commit**

Add one JSON example to both READMEs, then run `git diff --check` and commit:

```bash
git add tools/execution_state.py scripts/validate_prodcraft.py tests/test_execution_state_cli.py README.md README.zh-CN.md
git commit -m "feat(cli): add structured execution authority output"
```

### Task 3: Final verification and adversarial review

**Files:**
- Modify only if review finds a confirmed defect.

- [ ] **Step 1: Run both supported Python suites**

Run the full discovered suite on Python 3.12 and Python 3.11. Expected: all tests pass.

- [ ] **Step 2: Run repository and distribution gates**

Run exporter, full validator, Ruff, mypy, `git diff --check`, frontmatter/description/reference/loadability checks. Expected: all pass and curated output is unchanged unless source skills changed.

- [ ] **Step 3: Regenerate self-hosted acceptance**

Regenerate `.prodcraft/artifacts/prodcraft-direction2/`; missing completion pin must return a candidate with exit 1, and the current route/completion pins must return `terminal-authorized`.

- [ ] **Step 4: Run three independent adversarial reviews**

Require architecture/process, implementation-integrity, and developer-experience/compatibility reviewers to classify P0/P1/P2 findings and explicitly state PASS or FAIL.

- [ ] **Step 5: Record consensus and disagreements**

Treat findings shared by at least two reviewers as consensus. Preserve material one-reviewer objections separately with evidence and final disposition; do not force artificial unanimity.
