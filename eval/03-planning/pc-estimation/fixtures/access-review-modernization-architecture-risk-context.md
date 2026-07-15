# Architecture Risk Context

- release 1 must coexist with the legacy module
- unresolved sync semantics could change later delivery and rollback posture
- unsupported partner-managed reassignment paths remain out of scope
- compatibility and reversibility matter more than broad migration speed in the first release
