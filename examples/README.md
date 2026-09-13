# Repository-Grounded Workflow Walkthroughs

These three walkthroughs explain how Prodcraft's current contracts compose using real changes and evidence from this repository. They are retrospective/design traces, not new end-to-end model runs, installation demonstrations, or reconstructed tool transcripts. The skill column maps the current responsibility; it does not attest that every historical step invoked that exact skill.

The [whole-library acceptance record](../docs/reviews/2026-09-09-skill-design-acceptance.md) records coverage and limits. Current candidate identities and the checks actually performed are in the [evaluation handoff](../eval/meta/2026-09-08-skill-design-handoff.md).

## 1. Bug Repair: Reject a FIFO Intake File Promptly

**Problem.** The Claude Edit/Write adapter opened the current intake path for reading before checking its file type. A FIFO could block at `open`, so a later validator timeout did not bound the whole operation. The [original audit F2](../docs/reviews/bs-skill-auditor/2026-09-08-health-report.md#f2--p2-the-claude-adapter-can-block-on-a-fifo-before-checking-its-type) records the reproduced failure.

**Accepted scope.** Reject special files without waiting, preserve normal-file validation and approval behavior, and keep the fix local to the adapter. No running production system needs to be disturbed.

| Responsibility | Input consumed | Decision and output consumed next |
|---|---|---|
| pc-intake | Explicitly approved adapter repair, observed failure, local host-tool target | Direct bug-fix route with a bounded file/behavior scope; no market, architecture, or sprint artifact is needed |
| pc-debug-expert | Reproducer, real adapter open flags, and observed blocking point | Cause: blocking FIFO open precedes `fstat`; define nonblocking open followed by regular-file validation |
| pc-tdd / implementation | Same failure boundary and the existing adapter tests | Regression protects prompt rejection; implementation retains symlink and snapshot checks rather than broadly exempting intake files |
| pc-code-review | Actual diff, rejection/authorized-recovery cases, and scope | Review the file-descriptor behavior and approval boundary; actionable findings go back to the author without pretending integration is approved |
| pc-verification-before-completion | Current test output and inspected source | Claim only local adapter regression coverage, with native host dispatch/confirmation explicitly unverified |
| pc-delivery-completion | Scoped verification and the authorized local-edit outcome | Preserve the patch and hand off host verification; no implied installation, merge, or release |

Concrete artifacts:

- [Adapter implementation](../.claude/hooks/prodcraft_pretooluse.py)
- [Adapter regressions](../tests/test_claude_pretooluse_adapter.py), including `test_fifo_brief_is_rejected_without_waiting_for_a_writer`
- [Adapter behavior and limits](../docs/architecture/2026-07-16-claude-pretooluse-adapter.md)

A focused replay, using the repository's documented Python environment:

```bash
python -m unittest tests.test_claude_pretooluse_adapter.ClaudePreToolUseAdapterTests.test_fifo_brief_is_rejected_without_waiting_for_a_writer
```

**Stop conditions.** Missing permissions or unsafe reproduction limits the diagnosis; it does not justify replaying harmful effects. A passing local check cannot establish the inherited interpreter or confirmation UI in an installed Claude session.

**Process cost.** The original failing observation and matching regression are reused across debugging, review, and verification. They need not be rerun once per skill while the relevant implementation and environment are unchanged.

## 2. Brownfield Change: Migrate Package Identity Without Rewriting Evidence History

**Problem.** The former package digest covered selected main-file sections but excluded loaded reference content. A behavior-changing reference edit could retain the old identity. Consumers already depended on the manifest fields and generated public packages.

**Preservation boundary.** Keep public package names and the `contract-sha256:` field format; retain old evidence dates, scope, and maturity provenance. Do not imply that rehashing runs a benchmark or proves the evidence itself.

| Responsibility | Input consumed | Decision and output consumed next |
|---|---|---|
| pc-intake / pc-task-breakdown | Approved binding repair, existing exporter roots, current manifest/evidence schema | One bounded compatibility change with explicit non-goals; existing architecture references carry the boundary |
| pc-system-design, only for the changed identity decision | Actual package export shape and evidence consumers | Hash full `SKILL.md` plus `references/`, `scripts/`, and `assets/` paths/bytes under `skill-package.v3`; leave external workflows/evidence-file content outside this identity and state that limit |
| pc-tdd / implementation | Existing digest function, package fixtures, and migration constraint | Tests detect edits, additions/removals, renames, and special files; update the existing function rather than add an identity service |
| pc-code-review / integrity review | Digest logic, migration data, retained evidence, generated surface | Check that current content is bound and historical benchmark results are not relabeled as new behavior evidence |
| pc-verification-before-completion | Current registry, validator, package resource tests, curated export | Confirm parity and identity consistency for the current candidate; retain explicit limitations |
| pc-delivery-completion | Local migration result and accepted scope | Preserve the review candidates and their history; installed/public runtime rollout remains a separate action |

Concrete artifacts:

- [Binding algorithm and migration limits](../docs/quality/evidence-content-binding.md)
- [Digest implementation and validator](../scripts/validate_prodcraft.py)
- [Evidence registry](../eval/meta/skill-evidence-bindings.yml), including `previous_contract_projection` and `previous_revision`
- [Package resource regressions](../tests/test_manifest_evidence_binding.py)
- [Public registry](../schemas/distribution/public-skill-registry.json) and [generated index](../skills/.curated/index.json)

Reproduce consistency checks in this order:

```bash
python scripts/export_curated_skills.py
python scripts/validate_prodcraft.py
python -m unittest tests.test_manifest_evidence_binding tests.test_curated_distribution_surface
```

**Rollback decision.** Preserve a copy of the intended pre-migration records and restore only that source/metadata slice before regenerating packages. Do not reset unrelated work. Restoring the old projection also restores its known reference-binding limitation; a valid old digest does not make that limitation disappear.

**Process cost.** Existing boundary documentation, export tooling, and registry fields satisfy the producer/consumer needs. A new architecture diagram, migration scheduler, database, or parallel production deployment would add no value to this local identity migration.

## 3. Delivery Closeout: Finish Design Work Without Claiming Release Readiness

**Current request.** Complete whole-library design acceptance after the first sixteen revisions, repair supported defects, and check bug, brownfield, and delivery paths. Model behavior evaluation remains handed off separately.

| Responsibility | Input consumed | Decision and output consumed next |
|---|---|---|
| pc-intake | The user's explicit instruction to proceed as recommended and the existing approved design direction | Resume the current scope; no repeated choice of methodology or integration target |
| pc-code-review / independent design review | Thirty remaining main files, all their references, current consumers, and prior sixteen reviews | Forty-six explicit dispositions, fourteen new repair families, and a reread of the repairs |
| pc-receiving-code-review / implementation | Exact counterexamples and source locations | Fix valid dependent groups; reconcile follow-up findings without claiming that the author can grant independent approval |
| pc-documentation | Current design decisions, changed maturity, actual checks, and historical records | Update canonical English guidance, the requested Chinese companion, and the existing evaluation handoff |
| pc-verification-before-completion | Current package hashes, frontmatter/reference checks, native parsing, context budgets, and deterministic results | A bounded design/packaging acceptance statement; no model-benefit, installed-host, or production claim |
| pc-delivery-completion | User requested local improvements, with no integration/release action | Preserve the changes and record evaluation ownership and next acceptance condition |

**Delivery decision for this pass.** Keep the local worktree. The [acceptance record](../docs/reviews/2026-09-09-skill-design-acceptance.md) states final checks; the [handoff](../eval/meta/2026-09-08-skill-design-handoff.md) lists exact candidate identities and deferred behavior cases. Earlier changes and unrelated user material remain intact. Task scratch files are removed at closeout. No commit, push, merge, global installation, or release is asserted by this record.

**Stop conditions.** A new release request needs its actual target and authority. If strict execution is selected, the canonical state and external operator pins remain required; these walkthrough tables do not produce strict terminal authority.

**Process cost.** One canonical acceptance record supplies the design, evidence, and delivery handoff. A separate report per reviewer persona, repeated intake approval, forced PR-choice menu, or empty documentation artifact is unnecessary.

## Using These Examples

Adapt the decisions and evidence boundaries, not the file names or historic counts. A consumer project must supply its own source, scope, required workflow gates, and actual verification. For fresh behavioral evaluation, preserve the model/runtime, exact package subject, raw actions, and hidden acceptance checks described in the existing handoff.
