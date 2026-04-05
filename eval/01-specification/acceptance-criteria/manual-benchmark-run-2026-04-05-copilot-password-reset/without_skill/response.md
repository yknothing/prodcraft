● I'll read the two files and create a comprehensive acceptance criteria artifact.

✓ Read password-reset-requirements.md (10 lines)

✓ Read password-reset-spec.md (10 lines)

✓ Create acceptance-criteria.md (+147)

● Done! I've created `acceptance-criteria.md` with 12 acceptance criteria covering:

   - **Happy paths**: Request and confirm password reset flows
   - **Edge cases**: Non-existent emails, multiple requests, expiration boundaries
   - **Error paths**: Invalid/expired/reused tokens, malformed requests, invalid passwords
   - **Security**: Token uniqueness, user isolation, no enumeration, single-use enforcement

   All criteria are behavior-focused and directly usable for QA testing and TDD.
