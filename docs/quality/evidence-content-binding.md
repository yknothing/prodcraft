# Evidence-to-Contract Binding

Prodcraft records the contract projection that each tested, secure, or
production skill was verified against. The manifest field is:

```yaml
evidence_verified_against: contract-sha256:<64 lowercase hex characters>
```

`contract-projection.v2` hashes normalized YAML frontmatter and every H2
section except `Context`, `Inputs`, `Outputs`, `Anti-Patterns`, `Reference
Material`, `Related Skills`, and `Distribution`. This includes `Process`,
`Quality Gate`, iron laws, hard gates, red flags, and other normative sections.
Duplicate H2 headings are rejected because they make the projection ambiguous.

The matching record in `eval/meta/skill-evidence-bindings.yml` identifies the
date and repository evidence paths reviewed for that digest. The validator
fails closed when a required binding is missing, malformed, stale, unmatched,
or points to missing evidence.

This mechanism proves repository-local freshness: evidence was reviewed for a
specific skill contract and has not silently drifted. It is not an external
signature, a trusted timestamp, or proof that the evidence itself is correct.
Independent model, human, or CI authority must still be represented by the
referenced evidence and the governing acceptance process.

