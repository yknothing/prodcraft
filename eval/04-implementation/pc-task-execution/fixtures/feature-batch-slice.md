# Feature Batch Slice

## Goal

Implement the next small slice for supported reviewer reassignment.

## Approved Scope

- keep the change to the current handler path
- preserve unsupported-flow behavior
- add only the smallest next test-backed increment

## Current Risk

- scope can drift into unsupported reassignment or sync redesign if the batch is not kept tactical
