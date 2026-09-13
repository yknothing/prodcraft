# Skill Usability and Debug Expert Review

The persona and naming decisions below were superseded later on 2026-09-13 by
the [Debug Expert Skill design](../architecture/2026-09-13-debug-expert-design.md):
the advisory persona was withdrawn and the existing debugging Skill was renamed
and redesigned as `pc-debug-expert`. The usability repairs remain. This record
retains the scope and verification results of the earlier candidate.

## Scope and Routing

The user authorized continued repository improvement, prioritizing barriers to
skill use, and asked about a dedicated debug expert. This continues the existing
repository work with a bounded diagnosis, repair, advisory-role addition, and
verification route. The quality target is agent skill packages and their local
loading and handoff behavior; no public service or production mutation is involved.

Reuse `pc-systematic-debugging` rather than create a second debugging procedure.
Add an advisory persona using the existing persona schema. Apply TDD to executable
export behavior; use contract review, reference checks, and runtime parsing for
the persona and skill prose. Existing unrelated working-tree changes are preserved.

## Confirmed Findings and Repairs

### Resource links could survive export in an unusable form

The exporter checked links only in top-level `SKILL.md` and copied resource
Markdown without translating lifecycle paths. A temporary fixture demonstrated
that a valid canonical cross-phase link became a missing, out-of-surface path
after export. Missing local resources and escaping paths were also accepted.

The exporter now rewrites skill links relative to each destination resource,
including nested references, scripts, and assets. It checks every exported
Markdown document before replacing the previous output. Failed exports preserve
the prior surface. Regular-file checks run before copied resources are read,
retaining the existing symlink protections. Anchors and source-only skill text
retain their previous semantics.

Two new tests failed against the unchanged exporter for three expected assertions,
then passed after the repair. The existing symlink-swap regression also passed.
The current public surface had no observed broken links before this repair:
independent inspection covered 40 packages, 166 Markdown files, and 193 relative
links. This finding is an export acceptance defect, not evidence of a current
installed-package outage.

### Diagnosis unnecessarily required source code

The debugging I/O contract previously called source code the minimum required
input, despite allowing diagnosis-limited outcomes. It now permits investigation
from failure reports, logs, artifact identity, or configuration. Source access is
required for source corrections; causal and regression proof remains necessary
for a fixed claim. Missing tests, history, or the optional history-retrieval skill
does not require fabricating artifacts or waiting before examining current evidence.

The portable routing map now stops dependent work only when a required skill is
actually needed and unavailable. An optional helper or an untriggered conditional
skill does not block the current step. Required gates and incident containment
remain intact; the change grants no execution or approval authority.

### Dedicated diagnostic ownership was missing

`personas/debug-expert.md` now owns causal confidence, competing explanations,
runtime identity, fix placement, and evidence limits. It is registered in
`manifest.yml`, named in debugging skill metadata and gateway guidance, and linked
from both reader guides. The repository now has eight advisory personas.

Final persona inventory also found an existing mismatch: the architect's persona
file listed its own leading phase as an advisory phase, while the manifest did
not. The redundant advisory entry was removed to match the schema's ownership
distinction and the existing manifest. This was metadata drift, not a demonstrated
skill-loading outage.

The developer retains implementation ownership, QA retains acceptance ownership,
and DevOps retains incident containment. The persona does not require an extra
agent, another approval, or a persona file in a standalone public installation.
It is not an independently discoverable `pc-debug-expert` skill or a host-native
agent configuration.

## Checks and Evidence Boundary

- `skill-creator` format validation passed for the modified debugging skill.
- Independent review found no remaining issues in the scoped candidate and passed
  six focused export tests plus a complete temporary export.
- The complete Python 3.11 contract suite passed: **506 tests in 65.384 seconds**.
- Structural validation returned `valid` with no errors; context-budget and
  `git diff --check` checks passed.
- Python 3.12.14 passed all **16 export tests** in an isolated environment with
  the same pinned PyYAML and jsonschema versions. The initial system interpreter
  lacked PyYAML; cached wheels resolved that setup gap without network access or
  global package changes. The temporary environment was removed after validation.
- All **eight personas** match their manifest name, leading and advisory phases;
  every skill role reference resolves. The reader-guide checks passed again after
  the final persona metadata correction.
- Gemini CLI 0.39.1's real `loadSkillFromFile` parsed all **46 source** and **40
  curated** skill entrypoints. Names, non-empty descriptions, and body presence
  passed; the maximum description length was **303 characters**, below 1024.
  No model request was made and no canary was injected or removed.
- The configured Python remains 3.11.14 with PyYAML 6.0.3 and jsonschema 4.26.0.
- The Claude hook `args` configuration was investigated and left intact: the
  current [official exec-form contract](https://code.claude.com/docs/en/hooks#exec-form-and-shell-form)
  supports executable-plus-arguments with path placeholders. No fresh Claude model
  or native hook session was used as evidence in this change.

The planned three Codex behavior samples were **not executed**. Automatic approval
review rejected sending selected repository skill, I/O contract, and persona text
to the external model service without explicit authorization for that content and
destination. The prepared cases cover source-unavailable diagnosis, a missing
optional history helper, and a live-incident authority boundary. Local parsing and
independent review do not replace those model behavior samples or establish a
comparative quality improvement.

The modified skill remains `review`; no maturity or capability promotion is made.
Its previous reviewed package binding was
`contract-sha256:ab8d649fbd8b6f348d4c8b2c081ac695ca3b011ed7e1baababb245a3a4525f77`.
The current binding records this scoped contract review and local revalidation;
historical benchmark evidence is retained as historical evidence.

## Delivery Boundary

Acceptance logs and scoped pre-change snapshots live in the ignored, purpose-named
`build/2026-09-13-skill-usability/` directory. Generated `skills/.curated/` is updated
from source. This is repository-local delivery: no global installation, account,
credential, commit, push, or deployment is changed by this work. Revert only the
Sep13 scoped changes and regenerate curated packages to roll back this revision;
do not discard earlier working-tree work.
