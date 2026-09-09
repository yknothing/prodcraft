# Input and Output Contract Notes

## Inputs

- **verification-record** -- Required current passing evidence for landing or ready-for-review handoff. For preservation, authorized draft PR, or discard, record known failures and verification gaps; do not manufacture a passing record or claim successful completion. Stale evidence must be refreshed before the action that relies on it.
- **execution-checkpoint** -- Optional batch context when the work was executed through `pc-task-execution`.

## Outputs

- **delivery-decision-record** -- The chosen completion outcome, verification evidence used, branch/PR target, cleanup action taken, and whether the work hands off to `pc-release-management` or stops here.
