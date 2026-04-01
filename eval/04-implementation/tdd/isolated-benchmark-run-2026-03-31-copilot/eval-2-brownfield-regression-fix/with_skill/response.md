● I'll start by reading the skill document to understand the approach, then analyze the problem
   and create a TDD-first implementation plan.

✓ List directory skill-under-test (7 files)

✓ Read skill-under-test/SKILL.md (187 lines)

● Now I'll explore the codebase to understand the structure and identify where the legacy access
   review assignment bug exists.

Find source files to understand the tech stack
   $ find . -type f -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.java" -o -name "*.cs" |
    head -30
   ↪ 1 line...

✓ List current directory contents
   $ ls -la
   ↪ 5 lines...

Search for source files excluding skill folder
   $ find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.java" -o -name
   "*.cs" -o -name "*.go" -o -name "*.rb" \) 2>/dev/null | grep -v node_modules | grep -v
   skill-under-test
   ↪ 1 line...

✓ List all files recursively
   $ ls -R . 2>/dev/null | head -50
   ↪ 5 lines...

● Based on the skill document and the bug description, I need to create a TDD-first implementation
    plan for fixing the legacy access review assignment bug. Since there's no existing codebase
   visible, I'll create a comprehensive plan that follows TDD principles.

   ## TDD-First Implementation Plan: Legacy Access Review Assignment Bug Fix

   ### **Assumptions**
   1. The codebase has both a legacy and new assignment path for access reviews
   2. There's a facade/adapter pattern mediating between legacy and new implementations
   3. The API returns a list of pending reviews per approver
   4. The system has a typical test infrastructure (unit/integration tests)

   ### **Implementation Plan**

   ---

   ## **Phase 1: RED - Regression Test (Capture the Bug)**

   ### **Test 1: Regression Test for Reassignment Visibility Bug**
   **File**: `test_access_review_assignment_regression.py` (or equivalent)

   ```python
   def test_reassigned_review_not_visible_to_previous_approver_legacy_path():
       """
       REGRESSION TEST: In legacy facade path, reassigned reviews should NOT
       remain visible to the previous approver after reassignment.

       Bug: Previous approver sees reassigned review until page refresh.
       Expected: Reassignment immediately removes review from previous approver's list.
       """
       # Arrange
       review_id = "review-123"
       previous_approver = "user-alice"
       new_approver = "user-bob"

       # Create review assigned to Alice via LEGACY path
       review_service = AccessReviewService(use_legacy_path=True)
       review_service.create_review(review_id, approver=previous_approver)

       # Act: Reassign from Alice to Bob
       review_service.reassign_review(review_id,
                                      from_approver=previous_approver,
                                      to_approver=new_approver)

       # Assert: Previous approver should NOT see the review
       alice_reviews = review_service.get_pending_reviews(previous_approver)
       assert review_id not in [r['id'] for r in alice_reviews], \
           "BUG: Reassigned review still visible to previous approver"
   ```

   ### **Test 2: New Approver Receives Reassigned Review**
   ```python
   def test_reassigned_review_visible_to_new_approver_legacy_path():
       """
       Complementary test: New approver must see reassigned review immediately.
       """
       # Arrange
       review_id = "review-456"
       previous_approver = "user-alice"
       new_approver = "user-bob"

       review_service = AccessReviewService(use_legacy_path=True)
       review_service.create_review(review_id, approver=previous_approver)

       # Act
       review_service.reassign_review(review_id,
                                      from_approver=previous_approver,
                                      to_approver=new_approver)

       # Assert: New approver MUST see the review
       bob_reviews = review_service.get_pending_reviews(new_approver)
       assert review_id in [r['id'] for r in bob_reviews], \
           "New approver must see reassigned review immediately"
   ```

   ---

   ## **Phase 2: Characterization Tests (Safety Net)**

   ### **Test 3: Legacy Path Preserves API Response Shape**
   ```python
   def test_legacy_path_response_shape_unchanged():
       """
       CONTRACT TEST: API response shape must remain unchanged for legacy clients.
       """
       review_service = AccessReviewService(use_legacy_path=True)
       review_service.create_review("review-789", approver="user-alice")

       response = review_service.get_pending_reviews("user-alice")

       # Assert expected schema
       assert isinstance(response, list)
       assert all('id' in r for r in response)
       assert all('approver' in r for r in response)
       assert all('status' in r for r in response)
       # Add other contract fields
   ```

   ### **Test 4: New Path Not Affected by Fix**
   ```python
   def test_new_path_unaffected_by_legacy_fix():
       """
       COEXISTENCE TEST: New implementation path must continue working correctly.
       """
       review_service = AccessReviewService(use_legacy_path=False)
       review_service.create_review("review-999", approver="user-alice")

       review_service.reassign_review("review-999",
                                      from_approver="user-alice",
                                      to_approver="user-bob")

       alice_reviews = review_service.get_pending_reviews("user-alice")
       bob_reviews = review_service.get_pending_reviews("user-bob")

       assert "review-999" not in [r['id'] for r in alice_reviews]
       assert "review-999" in [r['id'] for r in bob_reviews]
   ```

   ---

   ## **Phase 3: GREEN - Minimal Fix**

   ### **Root Cause Hypothesis**
   The legacy path likely has:
   1. **Stale cache**: Previous approver's review list is cached and not invalidated on
   reassignment
   2. **Incomplete filter**: Query doesn't exclude reassigned reviews for previous approver
   3. **Event ordering**: Reassignment event processed after query returns

   ### **Surgical Fix Location**
   Target the legacy facade's `get_pending_reviews()` method:

   ```python
   # BEFORE (buggy):
   def get_pending_reviews_legacy(self, approver_id):
       # Reads from legacy table without checking reassignment status
       return self.legacy_db.query(
           "SELECT * FROM reviews WHERE approver_id = ?",
           approver_id
       )

   # AFTER (fixed):
   def get_pending_reviews_legacy(self, approver_id):
       # Add filter to exclude reassigned reviews
       return self.legacy_db.query(
           """SELECT r.* FROM reviews r
              LEFT JOIN review_reassignments rr ON r.id = rr.review_id
              WHERE r.approver_id = ?
              AND (rr.review_id IS NULL OR rr.from_approver != ?)""",
           approver_id, approver_id
       )
   ```

   **OR** if using cache:
   ```python
   def reassign_review_legacy(self, review_id, from_approver, to_approver):
       # Update assignment
       self.legacy_db.execute(
           "UPDATE reviews SET approver_id = ? WHERE id = ?",
           to_approver, review_id
       )
       # FIX: Invalidate cache for previous approver
       self.cache.invalidate(f"pending_reviews:{from_approver}")
       self.cache.invalidate(f"pending_reviews:{to_approver}")
   ```

   ---

   ## **Phase 4: REFACTOR - Extract Common Logic**

   After tests pass, consider:
   1. Extract reassignment invalidation logic into helper method
   2. Ensure both legacy and new paths use same cache invalidation
   3. Add logging for reassignment events

   ---

   ## **Compatibility Protections**

   ### **1. Feature Toggle Protection**
   ```python
   def get_pending_reviews(self, approver_id):
       if self.feature_flags.is_enabled("use_new_assignment_path"):
           return self._get_pending_reviews_new(approver_id)
       else:
           return self._get_pending_reviews_legacy_fixed(approver_id)
   ```

   ### **2. Response Shape Validation**
   ```python
   def validate_response_contract(response):
       """Ensures response shape matches legacy contract."""
       assert all(required_field in r for r in response
                  for required_field in ['id', 'approver', 'status'])
   ```

   ### **3. Rollback Safety**
   - Keep old method as `_get_pending_reviews_legacy_original()`
   - Use feature flag to switch between fixed and original
   - Monitor error rates post-deployment

   ---

   ## **Test Execution Order**

   1. **Run Test 1** (regression test) → **MUST FAIL** ✅ Proves bug exists
   2. **Run Test 2** (new approver test) → **MUST FAIL** ✅ Proves incomplete state
   3. **Run Test 3** (contract test) → **MUST PASS** ✅ Current contract baseline
   4. **Run Test 4** (coexistence test) → **MUST PASS** ✅ New path works correctly
   5. **Apply minimal fix**
   6. **Run all tests** → **ALL MUST PASS** ✅
   7. **Refactor if needed** → **ALL MUST STAY GREEN** ✅

   ---

   ## **Quality Gates**

   - ✅ Regression test fails before fix (proves bug reproduction)
   - ✅ All tests pass after fix
   - ✅ No changes to API response schema
   - ✅ Legacy and new paths both work
   - ✅ Cache invalidation tested (if applicable)
   - ✅ No additional features added beyond bugfix
   - ✅ Test execution < 30 seconds

   ---

   ## **Scope Boundaries (What NOT to Do)**

   ❌ **Do NOT redesign** the assignment subsystem
   ❌ **Do NOT migrate** legacy data to new schema
   ❌ **Do NOT add** new assignment features
   ❌ **Do NOT refactor** unrelated code
   ❌ **Do NOT change** API contracts or response shapes
   ❌ **Do NOT remove** legacy path (coexistence required)

   ---

   This plan follows TDD iron law: **RED → GREEN → REFACTOR**, keeps the fix surgical, and provides
    compatibility protection during coexistence.
