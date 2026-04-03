# Requirements Summary

- release 1 must support only the reviewed reassignment flows
- unsupported partner-managed variants must fail explicitly
- the modern slice must coexist with the legacy module during release 1
- historical legacy reads remain bounded and should not be flattened into full migration
- sync semantics remain unresolved and must stay visible as an open decision
