# Without-Skill Response: New Feature (SaaS 团队协作)

**Prompt**: "我们的 SaaS 产品需要加一个团队协作功能，用户可以在项目里 @mention 队友然后自动发通知。这个功能优先级很高，Q2 就要上线"

---

## Simulated Claude Response (No Intake Skill)

好的，我来帮你实现这个团队协作功能。

首先让我了解一下你们的技术栈。你们用的是什么前端框架和后端语言？数据库是什么？

在等你回复的同时，我先列一下大概的实现思路：

1. **@mention 功能**
   - 前端：在输入框中检测 `@` 字符，弹出用户搜索下拉
   - 后端：解析 mention 文本，提取被 mention 的用户 ID
   - 存储：在 comments/messages 表中关联 mentioned_user_ids

2. **通知系统**
   - 实时通知：WebSocket 或 SSE
   - 离线通知：邮件/推送
   - 通知偏好设置

3. **需要考虑的点**
   - 权限控制（只能 mention 项目成员）
   - 通知频率限制（避免 spam）
   - @all 功能是否需要

要不我先从数据库 schema 设计开始？然后我们一步步实现。

---

## Analysis

- 直接跳到了技术实现方案
- 没有分类工作类型
- 没有评估 scope
- 没有推荐工作流/方法论
- 没有识别风险
- 问了技术栈问题但没有结构化的分诊流程
- 没有给出审批环节
