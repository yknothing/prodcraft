# Without-Skill Response: Hotfix (Checkout 500 Errors)

**Prompt**: "hey so our checkout page has been throwing 500 errors since this mornings deploy, about 15% of users are affected and were losing revenue every minute. need this fixed asap"

---

## Simulated Claude Response (No Intake Skill)

This sounds urgent! Let's debug this right away.

First, can you share:
1. What was deployed this morning? The diff or PR would help narrow it down
2. Can you check the error logs? `tail -f /var/log/app/error.log` or whatever your logging setup is
3. Is there a way to quickly rollback the deploy?

While you're checking those, here are the most common causes of 500 errors after a deploy:

- **Database migration issue** — new code expects a column/table that doesn't exist yet
- **Environment variable** — missing or changed config in production
- **Dependency version mismatch** — a package updated with breaking changes
- **Memory/resource issue** — new code consuming more resources than available

If rollback is possible and fast, I'd recommend rolling back first to stop the bleeding, then debug in a calmer state. Revenue loss every minute makes rollback the priority.

Can you share the stack trace from the 500 errors?

---

## Analysis

- 正确识别了紧急性
- 直接跳到了 debugging
- 建议了 rollback（好）
- 但没有结构化的分诊：
  - 没有分类为 hotfix
  - 没有明确选择 hotfix workflow
  - 没有给出完整的处理路径
  - 没有 scope 评估
  - 没有风险识别（比如 root cause 可能不在我们代码中）
  - 没有给出审批/确认步骤
