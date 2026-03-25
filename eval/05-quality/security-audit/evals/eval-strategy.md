# Security Audit Skill — Evaluation Strategy

## Evaluation Mode

`routed` — the skill is invoked through the Prodcraft lifecycle (typically from agile-sprint, spec-driven, or hotfix workflows) rather than as a standalone discoverability target.

## Objectives

Verify that the security-audit skill:
1. Produces a complete, structured audit report covering all four mandatory areas (authentication/authorization, input validation, dependency vulnerabilities, secrets management).
2. Correctly distinguishes critical findings that block release from advisory findings that inform future sprints.
3. Does not produce false negatives for the canonical high-risk patterns (hardcoded secrets, SQL injection, outdated dependencies with known CVEs).
4. Integrates cleanly with the upstream testing-strategy skill output and passes its handoff artifact to deployment-strategy.

## Scenario Coverage

| Scenario | Description | Expected output |
|----------|-------------|-----------------|
| New API endpoint | Endpoint handles user authentication and writes to a database | Audit report flagging input validation and auth controls; OWASP Top-10 checklist |
| Dependency update | PR bumps 3 npm packages including one with a known CVE | Critical finding on CVE; advisory finding on API surface changes |
| Secrets rotation | Config change adds a new third-party API key | Flag for secrets management review; confirm key is not in source |
| Hotfix path | Security-audit invoked from hotfix workflow | Abbreviated audit focused on trust-boundary and blast-radius; no blocking of fix for non-security findings |
| Clean greenfield | MVP with no known vulnerabilities | Audit completes with zero critical findings; report includes baseline evidence |

## Quality Gate Criteria

An eval run passes acceptance when:

- [ ] Audit report artifact produced with all four required sections present.
- [ ] Critical vs. advisory severity correctly assigned for at least 4 of 5 canonical scenarios.
- [ ] No critical finding suppressed without documented rationale.
- [ ] Handoff artifact (`audit-report`) references the upstream `test-results` input by name.
- [ ] Security checklist items are machine-checkable (`- [ ]` format).

## Benchmark Baseline

Initial benchmark target (to be established on first eval run):

- Critical finding recall: ≥ 90% on canonical CVE and injection scenarios.
- False positive rate: ≤ 15% on clean greenfield scenario.
- Handoff completeness: 100% (audit-report always produced when skill runs to completion).

## Known Risks

- **Over-blocking**: Audit flags advisory items as critical and blocks delivery unnecessarily. Mitigation: severity taxonomy in skill body must be concrete and tied to exploitability, not theoretical risk.
- **Context window pressure**: Large codebases may cause the skill to truncate the dependency scan section. Mitigation: skill should scope the audit to the changed surface, not the entire codebase.
- **Hotfix path tension**: Security review adds latency to emergency fixes. Mitigation: hotfix workflow invokes abbreviated audit scope; full audit runs post-hotfix as follow-up.

## Evidence Requirements

Each eval run must produce:

1. `audit-report.md` — structured report with findings, severity, and remediation guidance.
2. `security-check-evidence.md` — record of what was checked (tools run, files scanned, CVE database consulted).
3. Validator output from `python3 scripts/validate_prodcraft.py --check security-minimal` — confirming the skill description itself passes automated security checks.
