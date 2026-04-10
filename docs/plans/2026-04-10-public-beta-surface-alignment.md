# Public Beta Surface Alignment

> Date: 2026-04-10

## Problem

The repository now has a much larger manifest-backed `tested` set than the
public `npx skills` surface exposes.

Before this wave:

- manifest `tested` / `secure` / `production`: `34`
- public curated skills: `19`
- generated public-only exceptions below `tested`: `1` (`system-design`)
- tested-or-better skills missing from public export: `17`

This made the repository look more mature in source form than it did through the
actual installer contract.

## Decision

Align the public beta surface with the manifest-backed tested set.

That means:

- every skill at `tested`, `secure`, or `production` should be installable from
  `skills/.curated/`
- production claims remain narrow and honest in `manifest.yml`
- `readiness: core` remains limited to the hardened default spine
- all newly published non-core skills stay `readiness: beta`
- the one existing below-tested exception (`system-design`) remains explicit
  rather than silently implied

## Added To Public Beta

- `user-research`
- `tech-selection`
- `api-design`
- `estimation`
- `risk-assessment`
- `sprint-planning`
- `systematic-debugging`
- `task-execution`
- `refactoring`
- `receiving-code-review`
- `e2e-scenario-design`
- `release-management`
- `runbooks`
- `tech-debt-management`
- `retrospective`
- `documentation`
- `accessibility`

## Non-Goals

- do not mass-promote these skills to manifest `production`
- do not claim that `beta` public skills have the same evidence strength as the
  core production spine
- do not remove the explicit registry gate between authoring status and public
  export

## Result

After this wave:

- public curated skills: `36`
- manifest `tested` / `secure` / `production` skills missing from public export:
  `0`
- public below-tested exceptions: `1` (`system-design`)

This restores a more honest relationship between the repository maturity story
and what `npx skills` users can actually install.
