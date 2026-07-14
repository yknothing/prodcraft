# With-Skill Response: Hotfix (Checkout 500 Errors)

**Prompt**: "hey so our checkout page has been throwing 500 errors since this mornings deploy, about 15% of users are affected and were losing revenue every minute. need this fixed asap"

**Skill applied**: intake (SKILL.md)

---

## Simulated Claude Response (With Intake Skill)

*[Step 1: Silently explores context — checks recent deploy, error patterns]*

*[Step 2: Classifies work type]*

This is a **Hotfix** — production is actively impacted with revenue loss. Fast-tracking intake.

## Intake Brief

**Work type**: Hotfix
**Entry phase**: 04-implementation (skip directly to diagnosis and fix)
**Recommended workflow**: hotfix
**Key skills needed**: debugging → tdd (regression test) → code-review → deployment
**Scope assessment**: small (hopefully — correlated with this morning's deploy)
**Key risks**:
1. Root cause may not be in the deploy itself — could be infrastructure, third-party payment provider, or data-related
2. Rolling back the deploy might introduce a different regression if other changes were bundled

### Immediate Actions
1. **Check if rollback is viable** — since the issue started with this morning's deploy, a quick rollback would stop the bleeding while we diagnose. Is rollback possible?
2. **Pull error logs** — need the stack trace from the 500 errors to identify root cause
3. **Verify scope** — is it only checkout, or are other pages affected?

### Proposed Path (after stabilization)
1. **Rollback or hotfix** — stabilize production first
2. **Root cause analysis** — identify the exact change that caused the failure
3. **TDD** — write a regression test that reproduces the 500 error
4. **Fix + code-review** — fix the issue, fast-track review (single reviewer OK for hotfix)
5. **Deploy** — redeploy with fix, monitor closely

**I'd recommend starting with rollback immediately if it's available. Shall I proceed with that assumption, or do you want to diagnose first?**

---

## Analysis

- ✅ 结构化 intake brief（即使在紧急场景下也保持结构）
- ✅ 正确分类为 Hotfix（不是普通 bug fix）
- ✅ 跳到 04-implementation（不走完整 lifecycle）
- ✅ 选择 hotfix workflow
- ✅ 识别了紧急性并适配流程（fast-tracked）
- ✅ 建议了 rollback 作为第一优先
- ✅ 识别了 2 个风险（root cause 可能不在 deploy 里、rollback 可能有其他 regression）
- ✅ 给出了 stabilize → diagnose → fix → verify 的结构化路径
- ✅ 征求了用户确认（rollback vs diagnose first）
