# Curated Portability Review

> Date: 2026-04-24
>
> Status: initial static review.
>
> Scope: compare the full repository context against the generated
> `skills/.curated/` install surface for the same task probes.
>
> Related registry:
> [`public-skill-portability.json`](../../schemas/distribution/public-skill-portability.json)

## Method

This review uses a static side-by-side inspection of selected full-repository
and curated install-surface probes. It is not a live agent benchmark and it is
not a complete skill-by-skill audit. The purpose is to decide whether the public
export metadata has an honest landing zone and whether the initial default
classification overclaims what survives export.

Each probe compares:

- overclaim risk: whether curated-only users could infer stronger governance
  than the package can provide
- handoff preservation: whether the task carries enough state between skills
  without the full repo
- route correctness: whether the right skill or workflow path remains likely
  outside the source repository

## Task Probes

| Probe | Expected route | Full repository context | Curated-only context | Result |
|---|---|---|---|---|
| New feature intake: add a webhook retry policy with compatibility constraints | `prodcraft -> intake -> requirements-engineering -> system-design -> task-breakdown` | Gateway, workflow docs, schemas, and validation contracts explain the route and required artifacts. | `prodcraft` and `intake` preserve the entry rule, but deeper route authority depends on source-repo `skills/_gateway.md` and workflow files that are not bundled. | Portable with caveat. Route intent survives; route enforcement does not. |
| Bug fix completion: fix cache invalidation and claim the task complete | `systematic-debugging -> tdd -> verification-before-completion -> delivery-completion` | Artifact flow, `verification-record.v1`, validator checks, and delivery skill contract constrain the claim. | The skills explain the discipline, but curated-only users do not get schema validation or manifest artifact-flow enforcement. | Portable with caveat. Completion honesty survives as guidance; proof-shape enforcement does not. |
| Code review: review a diff with hardcoded region and missing contract test | `code-review` with blocking findings before merge | Skill text, quality evidence, magic-value governance, and tests clarify blocking precision. | `code-review` has strong standalone review guidance, but repository guardrails and evidence history are missing. | Portable with caveat. Review rubric survives; repository-backed precision claim does not. |
| Operations follow-up: latency near miss that reveals architecture drift | `incident-response -> course-correction-note -> system-design or planning` | ADR-002, course-correction schema, gateway direct-jump list, and validator preserve the cross-phase handoff. | Curated incident and architecture skills can guide the response, but the route jump contract is not bundled as an enforceable schema. | Portable with caveat. Handoff language survives; course-correction authority does not. |
| Public install user: install only `.curated/` and ask how to start engineering work | `prodcraft -> intake` | Full repo can resolve source links, workflow contracts, artifact registries, and QA evidence. | `prodcraft` correctly says the canonical repo source is required for full routing and that curated is a packaging contract. | Portable with caveat. The public surface is honest if caveats are visible in the index. |

## Findings

1. No sampled public skill is safely `portable_as_is` yet. Even strong knowledge
   units in the sample refer to Prodcraft lifecycle context, artifact flow,
   validation, or QA evidence that exists only in the source repository.
2. The sampled public skills do not indicate a need for `blocked` classification
   solely because of portability. Curated-only users still receive useful
   operating guidance, and the generated `prodcraft` gateway already states
   that the source repository holds the canonical contract.
3. The largest overclaim risk is not skill text alone. It is metadata that could
   imply repository-grade governance after export. The curated index therefore
   must expose portability caveats beside readiness and stability.
4. Handoff preservation is strongest for entry skills and weakest for
   schema-backed cross-phase or completion claims, because curated-only packages
   do not include validator enforcement.
5. Route correctness is acceptable for starting work through `prodcraft` and
   `intake`, but deeper route decisions still depend on the source repository
   gateway and workflow contracts.

## Registry Decision

The initial registry classification should remain a conservative default:

- all exported public skills: `portable_with_caveat`
- `hidden_dependencies`: repository routing, artifact contracts, validation,
  and QA evidence
- `public_caveat_text`: portable as skill guidance; full governance guarantees
  require the Prodcraft repository contracts and validation checks

This is intentionally conservative. It is a policy default supported by sampled
static probes, not proof that every exported skill has been individually
reviewed. A future live benchmark or full skill-by-skill audit may promote
individual skills to `portable_as_is`, but only after curated-only task runs show
low overclaim risk, adequate handoff preservation, and correct route selection.

## Next Review Step

Run a live full-repo versus curated-only benchmark with the same probes above.
Record model, host runtime, input prompt, output artifact, overclaim finding,
handoff preservation score, and route correctness score for each branch.
