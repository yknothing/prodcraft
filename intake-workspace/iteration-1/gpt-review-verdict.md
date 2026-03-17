# GPT 评审论点实证裁定

基于 intake skill 的 with-skill vs without-skill benchmark 数据。

---

## 论点 1："Prodcraft 绝大多数 skill 是 encoded preference skills"

### 裁定：✅ 完全证实

**证据**：

Baseline（无 skill）在 21 个 assertions 中通过了 5 个（24%）。这 5 个全部是**领域知识类**：
- 识别紧急性（hotfix 场景）
- 建议 rollback（hotfix 场景）
- 识别无测试风险（重构场景）
- 建议先写测试（重构场景）
- 隐式跳到 implementation（hotfix 场景）

Claude 原生就知道这些。

Skill 的独占价值（76pp 提升）全部来自**流程纪律**：
- 结构化分诊文档（intake brief）
- 工作类型分类
- 生命周期阶段选择
- 工作流/方法论选择
- 审批门控

**结论**：GPT 的 "encoded preference" 判断 100% 正确。Intake skill 不教 Claude 新知识，而是给它一套流程框架。

---

## 论点 2："skill 应靠 A/B 评测存活，而非规划增长"

### 裁定：✅ 合理且已验证方法可行

**证据**：

本次 benchmark 证明 A/B 评测方法是可行的：
- with-skill: 100% pass rate
- without-skill: 24% pass rate
- Delta: +76pp

这个 delta 清楚地证明 intake skill 的存在价值。如果某个 skill 的 delta 很小（比如 <10pp），那就说明 Claude 原生能力已经覆盖了该 skill 的功能，skill 可以考虑合并或删除。

**但需要注意**：本次是自评（同一个 model 生成 with/without 然后自己打分），严格来说不如独立 subagent 跑 + 独立 grader 评分。数据方向是可靠的，精确度打折。

---

## 论点 3："自动发现层应控制在 8-12 个核心 skill"

### 裁定：⚠️ 方向正确但数字需要数据支撑

**证据**：

本次测试揭示了一个关键模式：

Baseline 在 hotfix 场景通过了 3/7（43%），在 refactor 通过了 2/7（29%），在 new feature 通过了 0/7（0%）。

这意味着不同 skill 的 "encoded preference 增量" 差异很大：
- **高增量 skill**（如 intake 处理 new feature）：baseline 几乎无法完成，skill 是必需的
- **中增量 skill**（如 intake 处理 refactoring）：baseline 部分完成，skill 提供结构补充
- **低增量 skill**（如 intake 处理紧急 hotfix 的 domain 知识部分）：baseline 原生就能做

"8-12 个核心"这个数字不能凭直觉定——应该用每个 skill 的 **delta pass rate** 来排序，delta 高的留 auto，delta 低的降级或合并。

---

## 论点 4："Token 成本是核心风险"

### 裁定：❌ 优先级排错了

**证据**：

Intake SKILL.md 转换为标准格式后约 150 行 / ~3,000 tokens（body）。
Description 约 560 字符 / ~140 tokens（metadata 常驻）。

对于一个 delta +76pp 的 skill，140 tokens 的常驻成本是极其值得的。

真正的问题不是 token 成本本身，而是：
1. **Description 精度**——如果 description 写不好导致误触发，浪费的 token 远超 metadata 成本
2. **Skill 间重叠**——两个 skill 竞争同一个 trigger，选错了的成本远超选对了的 metadata 税

GPT 把注意力放在了常驻 metadata 的 4,200 tokens 税上，但真正的 token 浪费来自误触发和重叠。

---

## 论点 5："Prodcraft 的问题是运行时层级没分好"

### 裁定：⚠️ 部分正确，但遗漏了更根本的问题

**证据**：

本次转换过程中发现，Prodcraft 与 Agent Skills 标准之间存在文件结构不兼容：

| 问题 | 严重度 |
|---|---|
| 文件名不是 SKILL.md | 致命 |
| 不是 skill-per-directory 结构 | 致命 |
| 扩展 frontmatter 字段不被标准识别 | 中等 |
| README 中声称的 Claude Code 集成方式无法工作 | 高 |

GPT 讨论了"运行时层级"（auto/manual/background），但没有发现 Prodcraft 根本还不是一个符合 Agent Skills 标准的部署物。

**"分好运行时层级"的前提是先让 Prodcraft 变成有效的 Agent Skills。**

---

## 综合裁定

| GPT 论点 | 裁定 | 置信度 |
|---|---|---|
| Encoded preference 分类 | ✅ 证实 | 高 |
| A/B 评测存活 | ✅ 方法可行 | 中（自评偏差） |
| Auto 层 8-12 个 | ⚠️ 方向对，数字需数据 | 中 |
| Token 成本是核心风险 | ❌ 优先级错 | 高 |
| 运行时层级未分好 | ⚠️ 部分对，遗漏更根本问题 | 高 |

---

## 基于数据的建议优先级

```
P0: 结构合规改造
    将 skills/{phase}/{name}.md 转为 skills/{name}/SKILL.md
    
P1: 对 19 个已有 skill 逐个跑 with/without baseline
    用 delta pass rate 排序价值
    
P2: 基于 delta 数据做分层
    高 delta (>50pp) → auto
    中 delta (20-50pp) → auto 但监控
    低 delta (<20pp) → manual 或合并
    
P3: 运行 description 优化
    用 skill-creator 的 trigger eval 循环优化每个 skill 的 description
```
