# Core Production Wave

> Date: 2026-04-10

## Purpose

Promote the current public core spine from `tested` to `production` where the repository already has:

- routed benchmark evidence
- routed integration evidence
- current findings
- a newly added security review artifact

This wave is intentionally narrow. It does **not** attempt to move every `tested` skill in the repository to `production`.

## Selected Batch

- `intake`
- `problem-framing`
- `requirements-engineering`
- `task-breakdown`
- `tdd`
- `verification-before-completion`

## Why This Batch

These skills already form the repository's most defensible default spine:

- route the work
- frame the problem
- specify what should be built
- break it into safe slices
- enforce test-first implementation discipline
- block false completion claims

They were already the closest skills to a truthful production claim. The missing artifact was security review, not more benchmark churn.

## Explicit Non-Goals

- do not mass-promote the entire `tested` set
- do not widen the public surface again in the same wave
- do not upgrade public packaging `stability` from `beta` to `stable`
- do not imply that every public beta skill is now part of the hardened promise

## Resulting State

After this wave:

- `production`: `6`
- `tested`: `28`
- `review`: `10`
- `draft`: `0`

The public install surface remains packaging-`beta`, but the production-backed core path is now explicit in the manifest.
