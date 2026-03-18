# Without-Skill Response: Refactor (Auth God Class)

**Prompt**: "ok 这个 auth module 我想重构一下，现在是个 2000 行的 god class，auth、session management、password reset、OAuth 全 mixed 在一起，完全没有 tests。我要 break it apart properly"

---

## Simulated Claude Response (No Intake Skill)

好的，重构一个 2000 行的 god class 是个好主意。让我先看看代码：

能不能给我看一下这个文件？我需要了解：
1. 文件路径是什么？
2. 主要的 class/module 结构

基于你的描述，我建议这样拆分：

**目标结构：**
```
auth/
├── authenticator.ts      # 核心认证逻辑（login, logout, token验证）
├── session-manager.ts    # session 的 CRUD 和过期管理
├── password-service.ts   # 密码重置、修改、验证
├── oauth-provider.ts     # OAuth 第三方登录
├── types.ts              # 共享类型定义
└── index.ts              # 统一导出
```

**重构步骤：**
1. 先 extract `SessionManager` — 它跟其他部分耦合最少
2. 然后 extract `PasswordService`
3. 接着 extract `OAuthProvider`
4. 最后清理剩余的核心 `Authenticator`

每一步都要确保现有功能不 break。因为没有 tests，我建议每次 extract 之前先写几个关键的 integration tests 覆盖现有行为。

要开始吗？先给我看看代码。

---

## Analysis

- 直接跳到了具体的重构方案
- 给出了不错的技术建议（拆分策略、先写测试）
- 但缺乏结构化分诊：
  - 没有评估 scope（medium? large?）
  - 没有考虑是否需要先做 architecture review
  - 没有推荐工作流/方法论
  - 没有识别系统性风险（例如：其他模块对 god class 的依赖情况）
  - 没有分类工作类型
  - 没有审批/确认环节，直接就要开始了
  - 提到了写测试但不是作为结构化路径的一部分
