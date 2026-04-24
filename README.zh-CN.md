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

## 当前状态

截至 2026-04-24，仓库中有：

- 44 个 lifecycle skill packages
- 6 个 workflow 文件，其中 3 个主流程、3 个 overlay
- 7 个 advisory personas
- 6 个注册的 protocol artifact schemas
- 40 个生成后的 public skills，位于 `skills/.curated/`

这些数字是当前仓库状态，不是永久承诺。需要以实际仓库和 validator 结果为准。

## 工作如何进入系统

Prodcraft 的入口是 `intake`。

一次工程工作通常按这个路径进入：

```text
用户请求
  -> intake
  -> gateway
  -> workflow
  -> routed skills
  -> artifact contracts
  -> validation and evidence
```

`intake` 的职责是做路由，不是直接设计完整方案。它会记录工作类型、入口阶段、推荐流程、关键风险和下一步技能。

如果路由清楚，但问题定义还不清楚，会先进入 `problem-framing`，再进入规格、架构或实现阶段。

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

Prodcraft 目前能较可靠地保护结构性合同，例如 workflow entry gate、artifact schema shape、curated-surface parity、portability metadata 和 security-minimal checks。

Prodcraft 不声称结构性检查能证明语义质量。schema 合法不等于需求质量高；review artifact 存在不等于 review 充分；`verification-record.v1` 合法也不等于整条路线已经完成。

下游执行闭环仍在加固中。AR-01、AR-02、AR-03 和 public portability review 都是治理工作流，不代表所有执行关键规则已经被完整强制执行。

当前 AR-03 已有 provisional host adapter policy。后续工作不是从零定义政策，而是在仓库原生合同清楚后，再决定是否 formalize 成 ADR、实现 host adapters，或继续保持设计说明状态。`.curated/` 也已有 initial static portability review，后续缺口是 live full-repo versus curated-only benchmark。

## Artifact Contracts

当前注册的 protocol artifacts 包括：

- `intake-brief`
- `problem-frame`
- `requirements-doc`
- `course-correction-note`
- `review-report`
- `verification-record`

其中 `verification-record.v1` 是完成声明 proof-shape 的第一块仓库原生地基。它要求记录 evidence refs、checks run、passed、failed、remaining unverified，以及 `claim_may_be_made` 是否成立。

这不是完整的语义验收系统。它只能约束证明形状；某条路线是否真的完成，仍要看 workflow rules、artifact-flow checks，以及具体上下文中的 review 和 evidence。

## Public Install Surface

Prodcraft 支持 public Agent Skills 安装流程：

```bash
npx skills add <repo-url>
npx skills add <repo-url> --skill intake
npx skills update
```

公共安装面是 `skills/.curated/`。它是生成结果，不应手工编辑。

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

1. 新工作先走 `intake`，即使是小改动也要有 fast-track 路由判断。
2. 规范性仓库 artifact 使用英文。
3. 中文内容只能作为明确标记的非规范性导读或用户展示材料。
4. 新增规则前先看是否有 schema、validator、workflow contract 或 evidence 支撑。
5. 不要手工编辑 `skills/.curated/`，用 exporter 生成。
6. 完成前运行 validator 和相关测试，不要把未验证状态说成已完成。

## 许可证

MIT
