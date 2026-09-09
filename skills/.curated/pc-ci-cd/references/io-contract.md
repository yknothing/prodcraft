# Input and Output Contract Notes

## Inputs

- **source-code** -- Required repository content, existing workflows/build commands, and target artifacts; documentation-only repositories are valid inputs.
- **test-strategy-doc** -- Required validation obligations, from a reviewed strategy or existing project policy. Route unresolved coverage decisions to testing strategy instead of inventing test types.
- **architecture-doc** -- Conditional target-platform, dependency, compatibility, and deployment constraints; reuse existing documented facts when sufficient.
- **task-list** -- Optional scope context. The approved request and release policy define which pipeline changes and external actions are authorized.

## Outputs

- **ci-cd-pipeline** -- Triggers, required checks, artifact flow, platform/environment configuration, and release approvals. Record actual run evidence and unverified stages for review and delivery.
- **build-artifacts** -- Only when a build/package ran: resulting candidate identity and provenance. Validation-only pipelines can produce check reports without inventing a deployable binary.
