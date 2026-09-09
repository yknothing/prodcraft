# Input and Output Contract Notes

## Inputs

- **source-code** -- Required current implementation and affected callers. Establish the preservation boundary before changing structure.
- **test-suite** -- Required relevant behavioral protection; add characterization only where the existing checks leave the affected boundary unprotected. Report inaccessible or unverified boundaries explicitly.
- **review-report**, **tech-debt-registry** -- Optional evidence of a concrete maintenance problem. A demonstrated current change cost is sufficient without creating these documents, unless the approved workflow requires them.

## Outputs

- **source-code** -- The refactored implementation with the checked preservation boundary and a concrete before/after maintenance benefit. Pass source revision, affected callers, verification, and remaining uncertainty to `pc-code-review` using the existing change note.

For example, a repeated validation rule can become one owned function when the same rule must change together. Equal literals with unrelated ownership do not justify a shared abstraction. A lower line count alone is not the benefit.
