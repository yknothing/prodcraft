# With-Skill Response: New Feature (SaaS 团队协作)

**Prompt**: "我们的 SaaS 产品需要加一个团队协作功能，用户可以在项目里 @mention 队友然后自动发通知。这个功能优先级很高，Q2 就要上线"

**Skill applied**: intake (SKILL.md)

---

## Simulated Claude Response (With Intake Skill)

*[Step 1: Silently explores context — reads CLAUDE.md, README, checks project state]*

*[Step 2: Classifies work type]*

这是一个 **New Feature** — 为现有 SaaS 产品添加新的协作能力。

我有一个关键问题想先确认：

**你们目前有通知基础设施吗？**（比如已有的 push notification 系统、邮件发送服务，还是要从零搭建？这会显著影响 scope 评估。）

---

*[After user responds: "有邮件服务，push notification 还没有"]*

---

## Intake Brief

**Work type**: New Feature
**Entry phase**: 01-specification（需要先定义协作功能的完整范围和交互设计）
**Recommended workflow**: agile-sprint（SaaS 产品、有明确时间窗口 Q2、适合迭代交付）
**Key skills needed**: spec-writing → system-design → api-design → task-breakdown → tdd → feature-development → code-review
**Scope assessment**: medium（@mention + 通知，涉及前端交互、后端解析、通知基础设施扩展）
**Key risks**:
1. 通知基础设施缺 push notification，需要新建——可能影响 Q2 时间线
2. @mention 的交互体验（搜索性能、实时性）需要前端较大改动

### Proposed Path
1. **spec-writing** — 定义 @mention 的触发规则、通知类型（邮件 vs push vs in-app）、权限模型
2. **system-design** — 设计通知服务架构、WebSocket/SSE 方案选型、与现有邮件服务的集成
3. **api-design** — mention API、notification API 契约
4. **task-breakdown** — 按 sprint 拆分，建议 push notification 基础设施优先
5. **tdd → feature-development** — 实现
6. **code-review** — 审查

### Alternative Approach
如果 Q2 时间紧张，可以先只做邮件通知 + in-app notification（不建 push），Phase 2 再加 push notification。这样 scope 缩小约 30%。

**你同意这个路径吗？还是想调整？**

---

## Analysis

- ✅ 结构化 intake brief（完整的分类、阶段、workflow）
- ✅ 正确分类为 New Feature
- ✅ 推荐 01-specification 作为起点
- ✅ 选择 agile-sprint workflow（匹配 SaaS + 时间窗口）
- ✅ 识别了 2 个关键风险
- ✅ 给出了 7 步 skill path
- ✅ 提供了替代方案（scope 缩减选项）
- ✅ 等待用户审批
- ✅ 只问了 1 个关键问题（不过度提问）
