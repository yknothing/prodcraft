# Security Audit — Security Check Evidence

## Status

Pending first eval run. This file will be populated with automated check evidence once the skill reaches `tested` status.

## Required Evidence

Per `_quality-assurance.md`, the following must be recorded before advancing to `tested`:

- [ ] `validate_prodcraft.py --check security-minimal` output showing 0 errors on the skill description.
- [ ] Prompt injection review: no imperative instructions that could redirect execution in the skill body.
- [ ] Command safety review: no shell command constructions in skill body that concatenate user input.
- [ ] Data protection review: skill does not instruct collecting or logging sensitive user data.
- [ ] Scope limitation review: skill stays within its declared phase scope and does not instruct cross-phase gate bypass.
- [ ] Supply chain review: no external URLs or unverified tool references in the skill body.
