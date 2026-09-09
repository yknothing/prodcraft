# Prodcraft 非规范性中文导读

本文是给中文读者的导读，只帮助理解 Prodcraft 的当前形态。它不定义或修改任何项目规则。若本文与英文 `README.md`、`CLAUDE.md`、schemas、validators、workflow contracts、distribution registries 或架构状态文档冲突，以这些英文仓库 artifact 为准。

英文规范概览见 [README.md](README.md)。当前架构状态见 [Architecture State Bundle](docs/architecture/2026-04-18-prodcraft-architecture-state-bundle.md)。

## Prodcraft 是什么

Prodcraft 是一个面向生产级软件开发的生命周期技能系统。它不是单纯的技能集合，而是把工程纪律外部化到仓库中的治理系统：

- skills 负责具体工程实践
- workflows 负责组合技能和阶段顺序
- schemas 和 templates 负责协议 artifact 的形状
- validators 负责结构性检查
- evidence records 负责证明或挑战执行结果

核心目标是：让重要的工程约束不只依赖模型自觉，而是落到可审计、可验证、可跨 agent runtime 迁移的仓库合同里。

所有面向用户的 Prodcraft skill ID 都统一使用 `pc-` 前缀。这是一次有意
进行的 beta 破坏性迁移；升级旧的 flat packages 时，请遵循
[基于 provenance 的安全升级说明](docs/distribution/npx-skills-compat.md#breaking-upgrade-from-unprefixed-beta-packages)，
不要只按 `intake`、`code-review`、`tdd` 等目录名批量删除，因为这些旧名
也可能属于其他仓库。

## 当前状态

截至 2026-09-09，当前源码树中有：

- 46 个 lifecycle skill packages
- `manifest.yml` 中的成熟度为：0 个 `production`、13 个 `tested`、33 个 `review`、0 个 `draft`
- 6 个 workflow 文件，其中 3 个主流程、3 个 overlay
- 7 个 advisory personas
- 8 个注册的 protocol artifact schemas
- 40 个生成后的 public skills，位于 `skills/.curated/`

这些数字是当前仓库状态，不是永久承诺。需要以实际仓库和 validator 结果为准。

累计修改 30 个 Skill，均处于 `review`：5 个保持原状态，6 个从 `production` 回到 `review`，19 个从 `tested` 回到 `review`。旧版本的成熟度和证据保留为历史记录，不能直接证明修改后版本的行为。公开包继续按现有允许列表提供 beta 候选；相关的 `core` 标记已调整为 `beta`。源码成熟度、是否进入公开包、全局是否已经安装，是三件不同的事。

[全库设计验收](docs/reviews/2026-09-09-skill-design-acceptance.md)已记录全部 46 个 Skill 的处理结论：本轮补审其余 30 个，修复 14 个，16 个未发现新增实质问题；此前 16 个保留原评审并复核接口。[三条完整示例链](examples/README.md)覆盖真实仓库中的 bug 修复、存量兼容变更和交付收口，明确输入、决策、产物和停止条件。这是设计走查与真实改动复盘，尚未测量模型收益。

## 工作如何进入系统

Prodcraft 的入口是 `pc-intake`。

一次工程工作通常按这个路径进入：

```text
用户请求
  -> pc-intake
  -> gateway
  -> workflow
  -> routed skills
  -> artifact contracts
  -> validation and evidence
```

`pc-intake` 的职责是做路由，不是直接设计完整方案。它会记录工作类型、入口阶段、推荐流程、关键风险和下一步技能。

如果路由清楚，但问题定义还不清楚，会先进入 `pc-problem-framing`，再进入规格、架构或实现阶段。

继续已有工作时，先确认目标、范围、授权和产物仍然有效，再执行下一个尚未满足的步骤。状态询问、补充说明或技能交接本身，不要求重新走 intake 或重复询问同一个审批。新增范围、风险或外部操作仍需要对应授权。

## 2026-09-08 设计修订

本轮围绕两个层面改进：

- **单个 Skill**：明确什么时候适用、必须消费哪些输入、产生什么可用结果，以及什么条件下继续或停止；修正固定时长、重复评审、characterization 测试和交付选择中的机械规则。
- **Skill 系统**：根据尚未满足的交付要求选择尽可能短的路线；复用已接受且仍有效的产物；按当前步骤读取引用；区分意图对齐、代码缺陷、实现真实性和完成证据四类评审问题。

详见[中文设计记录与复盘](docs/architecture/2026-09-08-skill-execution-design.zh-CN.md)、[英文规范记录](docs/architecture/2026-09-08-skill-execution-design.md)和[行为评测 handoff](eval/meta/2026-09-08-skill-design-handoff.md)。

目前完成的是 Skill 指令与组合规则的设计改进，并同步了源码和 `.curated/`。按需读取、产物复用等仍由 agent 执行，不是新增了自动加载或调度引擎；9 月 9 日修订将入口静态文本从 37,978 降到 35,721 字符，但尚未测得运行时上下文节省或工程结果改善。结构校验、原生解析通过，也不等于行为评测或全局安装已经完成。

当前 Claude Edit/Write adapter 不接受 `micro`；在该适配器下需要已批准的 `fast-track` 路径，不能换工具绕过。9 月 9 日已修复技能包引用绑定、FIFO 阻塞和 draft intake 恢复；完整候选通过校验后，新的 approved 内容交给宿主确认。审查报告可以携带 blocker 交给作者，小任务可复用现有边界，保留失败工作不冒充交付成功。 后续 TOP 5 已进一步改进反馈处理、功能实现、重构、测试策略及估算排期，覆盖另外 6 个 Skill；改变后的行为仍待评测。

## 四层架构模型

当前架构状态使用四个内容层：

| 层 | 作用 |
|---|---|
| Knowledge | 提供判断、模式和取舍，但不单独证明合规。 |
| Protocol | 用 artifact 保存路线、状态、约束、纠偏和验证边界。 |
| Enforcement | 用 validator、workflow contract 或 CI 检查结构性规则。 |
| Evidence | 用验证结果、review findings、benchmark、audit trace 证明或反驳执行行为。 |

这四层会跨三个消费面被评估：

- `repo_internal`
- `host_runtime`
- `public_export`

重要边界：host adapter 只能适配仓库合同，不能变成唯一权威；public export 不能夸大离开仓库后仍然保留的治理能力。

## 当前能保证什么，不能保证什么

Prodcraft 目前能较可靠地保护结构性合同，例如 workflow entry gate、artifact schema shape、curated-surface parity、portability metadata 和 security-minimal checks。项目也可以选择启用方向 2 的严格执行闭环：仓库持有 route/execution artifacts，操作者在可写 bundle 外持有 route digest 与 terminal completion digest 两个 pin，validator 重放 lifecycle/phase 自动机、检查内容绑定 evidence 与实时 Git worktree，并输出机器可区分的 gate 或 terminal authority。

Prodcraft 不声称结构性检查能证明语义质量。schema 合法不等于需求质量高；review artifact 存在不等于 review 充分；`verification-record.v1` 合法也不等于整条路线已经完成。

严格执行模式仍是可选能力，不是所有 legacy workflow 的默认强制项。它不认证审批人、不提供可信时钟、不证明需求或评审的语义质量，也不包含 scheduler、service、database 或多写者 event authority；这些仍属于方向 3 或人工/agent 专家判断边界。

当前 AR-03 已有 provisional host adapter policy。后续工作不是从零定义政策，而是在仓库原生合同清楚后，再决定是否 formalize 成 ADR、实现 host adapters，或继续保持设计说明状态。`.curated/` 也已有 initial static portability review，后续缺口是 live full-repo versus curated-only benchmark。

## Artifact Contracts

当前注册的 protocol artifacts 包括：

- `intake-brief`
- `problem-frame`
- `requirements-doc`
- `course-correction-note`
- `review-report`
- `verification-record`
- `route-decision`
- `execution-state`

其中 `verification-record.v1` 是完成声明 proof-shape 的第一块仓库原生地基。它要求记录 evidence refs、checks run、passed、failed、remaining unverified，以及 `claim_may_be_made` 是否成立。

`route-decision.v1` 保存批准后的 workflow focus 与 reviewer-declared obligations；`execution-state.v1` 保存统一排序的 lifecycle/phase/binding history、append-only completion attempts，以及内容寻址的 evidence/work snapshot。它们不改变 `verification-record.v1.claim_scope` 的既有自由文本语义。

通用 artifact 检查不会产生 authority：

```bash
python scripts/validate_prodcraft.py --artifact-instance <artifact.json>
```

严格 gate 授权必须提供 canonical state path 和 bundle 外保存的 route digest pin；terminal 授权还必须提供覆盖最终 attempt、evidence commitment 与 terminal transition records 的 completion digest pin：

```bash
python scripts/validate_prodcraft.py \
  --authorize-execution-state .prodcraft/artifacts/<work_id>/execution-state.json \
  --approved-route-digest sha256:<operator-pinned-route-digest> \
  --approved-completion-digest sha256:<operator-pinned-completion-digest>
```

当 terminal bundle 合法但未提供 completion pin 时，命令会非零退出并报告 candidate digest，供操作者在 bundle 外评审和批准；把该值写回命令是显式 approval，不是 bundle 自证。

机器调用方可以请求单个稳定 JSON object，authority 语义与退出码不变：

```bash
python scripts/validate_prodcraft.py \
  --authorize-execution-state .prodcraft/artifacts/<work_id>/execution-state.json \
  --approved-route-digest sha256:<operator-pinned-route-digest> \
  --output-format json
```

当前对象固定包含 `status`、`authority`、`candidate_completion_digest` 和 `errors`。candidate-only 结果仍是 `status: "invalid"`、`authority: null`，并返回非零退出码。JSON 渲染只覆盖参数解析成功后的领域校验；非法参数组合仍使用标准 `argparse` stderr 和退出码 2。这个本地 CLI 投影不是带版本的方向 3 host-adapter 协议。

只有 `gate-authorized` 或 `terminal-authorized` 返回零退出码。historical/non-canonical state、missing/mismatched pin、stale work/evidence、非法状态投影和 structural-only 都会 fail closed。规范设计见 [Minimal Execution Loop Architecture](docs/architecture/2026-07-10-minimal-execution-loop.md)、[ADR-003](docs/adr/ADR-003-repository-owned-execution-state.md)、[Threat Model](docs/architecture/2026-07-10-minimal-execution-loop-threat-model.md) 和 [Acceptance Record](docs/architecture/2026-07-10-minimal-execution-loop-acceptance.md)。

## Public Install Surface

Prodcraft 支持 public Agent Skills 安装流程：

```bash
npx skills add <repo-url>/skills/.curated
npx skills add <repo-url>/skills/.curated --skill pc-intake
npx skills update
```

公共安装面是 `skills/.curated/`。它是生成结果，不应手工编辑。
Repository-root discovery is not the public contract，除非 installer 已支持按 registry 过滤；根目录 discovery 会包含仓库本地 authoring packages，不等于 curated 公共面。

Public export 由两个 registry 控制：

- `schemas/distribution/public-skill-registry.json`：决定哪些 skills 被打包。
- `schemas/distribution/public-skill-portability.json`：说明离开完整仓库上下文后，哪些价值仍然保留。

当前 public skills 采用保守分类：`portable_with_caveat`。意思是：这些 skill 作为指导仍有价值，但完整治理保证依赖 Prodcraft 仓库中的 contracts、schemas、validators 和 evidence paths。

## 本地验证

推荐使用 Python 3.11 和 `uv` 跑完整 QA：

```bash
UV_CACHE_DIR=/tmp/uv-cache-prodcraft uv run --python 3.11 --with pyyaml --with jsonschema python -m unittest discover tests
UV_CACHE_DIR=/tmp/uv-cache-prodcraft uv run --python 3.11 --with pyyaml --with jsonschema python scripts/validate_prodcraft.py
```

常用 focused checks：

```bash
python scripts/validate_prodcraft.py --check workflow-entry-gate
python scripts/validate_prodcraft.py --check artifact-schema-registry
python scripts/validate_prodcraft.py --check curated-surface
```

如果本机默认 `python3` 缺少 `PyYAML` 或版本过低，请用上面的 `uv run --python 3.11 --with pyyaml --with jsonschema` 形式。

## 目录结构

```text
prodcraft/
  skills/                    # 生命周期技能和生成后的 .curated 公共安装面
  workflows/                 # 主流程和 overlay
  personas/                  # advisory agent roles
  schemas/                   # artifact 和 distribution registries
  templates/                 # protocol artifact templates
  rules/                     # 结构性质量和治理规则
  docs/                      # 架构、ADR、distribution、observability 和计划文档
  eval/                      # skill QA evidence
  tests/                     # contract 和结构测试
  scripts/                   # validators、exporters、benchmark runners、cutover tools
  manifest.yml               # skill maturity 和 evidence index
```

## 贡献原则

1. 新工作先走 `pc-intake`，即使是小改动也要有 fast-track 路由判断。
2. 规范性仓库 artifact 使用英文。
3. 中文内容只能作为明确标记的非规范性导读或用户展示材料。
4. 新增规则前先看是否有 schema、validator、workflow contract 或 evidence 支撑。
5. 不要手工编辑 `skills/.curated/`，用 exporter 生成。
6. 完成前运行 validator 和相关测试，不要把未验证状态说成已完成。

## 许可证

MIT
