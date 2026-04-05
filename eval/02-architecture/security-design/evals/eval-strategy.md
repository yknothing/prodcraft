# Security Design QA Strategy

## Goal/Objective

Evaluate whether `security-design` turns reviewed architecture and API context into a concrete threat model with named assets, trust boundaries, abuse paths, and controls that implementation and security audit can actually use.

## Why Routed Review First

`security-design` is not a discoverability skill. It is a routed architecture skill whose value shows up when the design preserves real trust boundaries and avoids late security invention.

The review question is whether the skill models the actual attack surface of the architecture, including brownfield coexistence and legacy exposure, rather than defaulting to a generic checklist.

## Scenario(s)

1. `access-review-modernization-security-design`
   - brownfield modernization with legacy coexistence and release-boundary risk
   - used to test whether the skill surfaces weaker legacy paths and fail-closed controls

2. `team-invite-security-design`
   - a non-brownfield service slice with normal authn/authz and data-handling boundaries
   - used to confirm the skill still produces a usable threat model when modernization is not the main risk

## Assertions

1. `identifies-assets-and-trust-boundaries`
   - sensitive data, privileged actions, and external integrations are named
   - trust transitions are explicit

2. `enumerates-real-abuse-paths`
   - malicious input, replay, authorization abuse, logging leakage, and rollout/coexistence weaknesses are considered
   - the output does not stop at "secure it" generalities

3. `assigns-concrete-controls`
   - authn/authz, validation, secret handling, logging, and fail-closed behavior are tied to specific boundaries
   - controls are implementation-ready rather than aspirational

4. `keeps-brownfield-risk-visible`
   - legacy paths, coexistence seams, and rollout exposure are called out explicitly when they weaken the system
   - residual risk is recorded instead of hidden

5. `prepares-downstream-handoff`
   - the result is usable by `security-audit`, `deployment-strategy`, and implementation teams without redoing the threat model

## Method

1. Produce a baseline threat model from the same architecture and contract inputs without the skill.
2. Produce a second threat model while explicitly using `security-design`.
3. Compare the two outputs against the assertion list.
4. Record whether the skill materially improves boundary clarity, abuse-path coverage, and control specificity.

## Exit Criteria for Review Stage

- The skill improves threat-model specificity over baseline
- Controls are mapped to concrete boundaries and not just named in the abstract
- Brownfield coexistence or legacy exposure is handled explicitly when present
- The output is actionable for downstream security audit and rollout planning
- A future benchmark can reuse the same scenario without re-framing the problem
