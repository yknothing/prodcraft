# With-Skill Response: Refactor (Auth God Class)

**Prompt**: "ok 这个 auth module 我想重构一下，现在是个 2000 行的 god class，auth、session management、password reset、OAuth 全 mixed 在一起，完全没有 tests。我要 break it apart properly"

**Skill applied**: intake (SKILL.md)

---

## Simulated Claude Response (With Intake Skill)

*[Step 1: Silently explores context — checks existing architecture docs, module dependencies]*

*[Step 2: Classifies work type]*

这是一个 **Refactoring** — structural improvement without behavior change。但 scope 比较大。

有一个关键问题：

**这个 auth module 有多少其他模块在直接 import/调用它？** 如果依赖很广，拆分的影响面会大得多，可能需要先做 architecture review。

---

*[After user responds: "基本上所有需要 auth 的地方都直接 import 这个文件，大概有 30+ 个文件引用它"]*

---

## Intake Brief

**Work type**: Refactoring
**Entry phase**: 02-architecture（30+ 文件依赖，需要先做 architecture review 规划拆分边界）
**Recommended workflow**: agile-sprint（拆分可以增量完成，每个 module 独立 PR）
**Key skills needed**: system-design (component boundaries) → task-breakdown → tdd (characterization tests) → refactoring → code-review
**Scope assessment**: large（2000 行 god class + 30+ 依赖文件 + 零测试覆盖）
**Key risks**:
1. **无测试覆盖** — 最大风险。重构没有 safety net，任何拆分都可能引入 regression。必须先写 characterization tests。
2. **广泛依赖** — 30+ 文件引用意味着 API 变更影响面很大。需要 facade pattern 或 re-export 策略来保持向后兼容。
3. **隐藏耦合** — god class 内部的 4 个关注点之间可能有非显式依赖（共享 state、互相调用）。

### Proposed Path
1. **system-design** — 画出当前依赖关系图，设计目标 module 边界（auth / session / password / oauth），确定 API contract
2. **task-breakdown** — 按依赖关系排序拆分顺序，每步一个独立 PR
3. **tdd** — 在动任何代码之前，先写 characterization tests 覆盖当前行为（这是 safety net）
4. **refactoring (iterative)** — 逐个 extract module：
   - Step A: Extract SessionManager（耦合最少）
   - Step B: Extract PasswordService
   - Step C: Extract OAuthProvider
   - Step D: Clean up core Authenticator
5. **code-review** — 每个 extract 步骤独立 review

### Alternative Approach
如果时间紧，可以只做 Strangler Fig pattern：新建 module 结构，新代码写在新 module 里，老代码逐步迁移。不一次性重构，而是 organic migration。Timeline 更长但风险更低。

**你倾向哪个方案？或者需要调整？**

---

## Analysis

- ✅ 结构化 intake brief
- ✅ 正确分类为 Refactoring
- ✅ Scope 评估为 large（准确，考虑了依赖广度和零测试）
- ✅ 推荐从 02-architecture 开始（不是直接开写）
- ✅ 识别了 3 个关键风险，特别是"无测试覆盖"作为最大风险
- ✅ 建议 characterization tests 先行（test-first for refactoring）
- ✅ 给出了渐进式拆分路径
- ✅ 提供了替代方案（Strangler Fig）
- ✅ 等待用户审批
- ✅ 只问了 1 个关键问题（依赖数量）
