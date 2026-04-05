# Mixed Review Bundle

## Comment 1

`blocker`:
The reassignment handler should keep returning `UNSUPPORTED_REASSIGNMENT_TYPE` for unsupported variants. Please add a regression test before merging.

## Comment 2

`ambiguous`:
The sync step feels fragile. Can you clean this up a bit before merge?

## Comment 3

`questionable`:
While you are here, can you generalize reassignment to handle future bulk-edit flows too?
