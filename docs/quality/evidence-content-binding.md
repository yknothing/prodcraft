# Evidence-to-Contract Binding

Prodcraft records a package identity for each review, tested, secure, or
production skill and links it to its evidence record. The manifest field is:

```yaml
evidence_verified_against: contract-sha256:<64 lowercase hex characters>
```

`skill-package.v3` covers the complete bytes of `SKILL.md` and every file
recursively under `references/`, `scripts/`, and `assets/`, matching the
exporter's resource roots. Content edits, additions, deletions, and renames
invalidate the binding, including changes to input contracts and gotchas.
Symlinks and non-regular resource files are rejected; file reads do not block
on FIFOs. Empty directories and filesystem timestamps are not identity inputs.

For each file, form `[package-relative POSIX path, "sha256:<file hash>"]`.
Sort by path, serialize `["skill-package.v3", sorted_file_pairs]` as JSON with
`ensure_ascii=True` and `separators=(",", ":")`, then SHA-256 its UTF-8 bytes.
Retain the `contract-sha256:` prefix for manifest compatibility. Duplicate H2
headings and missing Process/Quality Gate sections remain invalid.

The matching record in `eval/meta/skill-evidence-bindings.yml` identifies the
date and repository evidence paths reviewed for that digest. The validator
fails closed when a required binding is missing, malformed, stale, unmatched,
or points to missing evidence.

This detects package drift relative to the recorded identity. It does not hash
external workflows, other skill packages, or the contents of evidence files;
their links remain separate contracts. It is not an external signature, a
trusted timestamp, a concurrent-tree snapshot, or proof that evidence is correct.
Independent model, human, or CI authority must still be represented by the
referenced evidence and the governing acceptance process.

## September 9 Migration

The earlier `contract-projection.v2` omitted supporting files and several body
sections. The migration binds all 46 current packages, retains each prior v2
digest under `previous_contract_projection`, and records `package_bound_at`.
Existing `verified_at`, evidence paths, scopes, and maturity are carried forward;
the migration is deterministic identity capture, not a new review of all
resources or a model evaluation. The first ten design candidates and the six later design revisions remain at
`review`; no skill is promoted by rehashing. Historical evidence qualifies only
the behavior it actually evaluated. A changed package needs an explicit evidence
disposition before its new digest is accepted.
