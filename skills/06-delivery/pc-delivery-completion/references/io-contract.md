# Input and Output Contract Notes

## Inputs

- **verification-record** -- Fresh evidence from `pc-verification-before-completion`. If the evidence is stale, stop and re-run verification before making any completion claim.
- **execution-checkpoint** -- Optional batch context when the work was executed through `pc-task-execution`.

## Outputs

- **delivery-decision-record** -- The chosen completion outcome, verification evidence used, branch/PR target, cleanup action taken, and whether the work hands off to `pc-release-management` or stops here.
