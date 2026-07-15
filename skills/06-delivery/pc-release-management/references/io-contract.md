# Input and Output Contract Notes

## Inputs

- **delivery-decision-record** -- Optional but preferred handoff when `pc-delivery-completion` already decided the branch outcome and preserved the exact verification evidence used.
- **test-report** -- Functional readiness and known quality gaps.
- **security-report** -- Security findings and any accepted release risk.
- **performance-report** -- Performance readiness and capacity-sensitive concerns when one exists.

## Outputs

- **release-plan** -- Scope, go/no-go status, owners, release window, communications, and gating expectations for deployment.
