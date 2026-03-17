`★ Insight ─────────────────────────────────────`
零散利益相关方输入的核心挑战：同一句话可能同时包含功能需求、NFR 和约束。例如财务的「日志保留 2 年」既是功能需求（需有日志记录功能）也是合规约束（保留周期量化）。拆分时需避免遗漏任一维度。
`─────────────────────────────────────────────────`

---

# 报销工作流 — 第一版 Requirements Set (v0.1)

**文档状态**：草稿，待利益相关方评审
**范围**：国内员工报销，第一期
**作者**：[待填写] · 日期：2026-03-16

---

## 1. 功能需求（Functional Requirements）

格式：`The system shall [action] when [condition] so that [benefit].`

| ID | 描述 | 优先级 | 来源 |
|----|------|--------|------|
| FR-01 | The system **shall** allow employees to capture and upload invoice photos directly from a mobile device when submitting an expense claim, so that field sales staff can complete reimbursement without scanning equipment. | P0 | 老板 |
| FR-02 | The system **shall** provide a linear, step-guided submission flow that requires no more than the fields necessary to complete a single claim, so that end-to-end submission can be done within 3 minutes. | P0 | 销售负责人 |
| FR-03 | The system **shall** require the submitter to enter a free-text business justification when a single expense claim amount exceeds ¥3,000, so that finance can assess business validity before approval. | P0 | 财务 |
| FR-04 | The system **shall** route any expense claim exceeding ¥10,000 through a mandatory second-level approval step before it can be marked as approved, so that high-value disbursements receive additional oversight. | P0 | 财务 |
| FR-05 | The system **shall** record an immutable audit log entry for every state transition (submitted / approved / rejected / escalated), capturing actor identity and timestamp, so that finance can reconstruct the full approval trail. | P1 | 财务 |
| FR-06 | The system **shall** deliver a rejection notification to the original submitter that includes the approver-entered reason text when a claim is rejected, so that employees can correct and resubmit without follow-up inquiry. | P0 | 销售负责人 |
| FR-07 | The system **shall** restrict read access to personal bank account numbers and national ID numbers to users holding an explicitly authorized role, so that PII is not exposed to unauthorized personnel. | P0 | 法务 |
| FR-08 | The system **shall** allow finance staff to export a monthly reimbursement summary report covering all claims within a calendar month, so that month-end accounting can be performed without manual aggregation. | P2 | 财务 |

---

## 2. 非功能需求（Non-Functional Requirements）

> 所有 NFR 均已量化；拒绝使用"快"、"安全"等不可测术语。

| ID | 类别 | 描述 | 指标 | 优先级 | 来源 |
|----|------|------|------|--------|------|
| NFR-01 | 性能 / UX | 报销提交完整流程（从打开表单到收到提交成功确认）端到端时长 | ≤ 3 分钟（用户操作时间，不含网络等待）| P0 | 销售负责人 |
| NFR-02 | 吞吐量 | 月末高峰期系统须支持同时提交请求 | ≥ 500 并发提交，无降级或超时 | P0 | 财务 |
| NFR-03 | 合规 / 数据保留 | 审计日志自生成之日起必须可查询且不可篡改 | 保留期 ≥ 2 年 | P1 | 财务 |
| NFR-04 | 安全 / 访问控制 | 含个人银行卡号、身份证号字段的所有接口和视图须实施 RBAC | 非授权角色的请求须返回 403，且不得在错误响应体中泄露字段值 | P0 | 法务 |
| NFR-05 | 可用性 | 提交与审批核心流程在月末高峰期不得出现功能降级 | 核心路径可用性目标 ≥ 99.5%（供架构阶段细化）| P1 | 财务（推断自「系统不能卡」） |

---

## 3. 优先级汇总

| 优先级 | 含义 | 覆盖需求 |
|--------|------|---------|
| **P0（Must）** | 缺失则产品不可上线 | FR-01, FR-02, FR-03, FR-04, FR-06, FR-07, NFR-01, NFR-02, NFR-04 |
| **P1（Should）** | 重要，存在临时替代方案，需在第一期内完成 | FR-05, NFR-03, NFR-05 |
| **P2（Could）** | 有价值但可延后至第二优先级迭代 | FR-08 |
| **P3（Won't）** | 本期明确不做（见第 5 节） | — |

---

## 4. 来源追踪（Traceability）

| 原始输入 | 映射需求 | 备注 |
|---------|---------|------|
| 老板：移动端拍照上传 | FR-01 | 直接映射 |
| 销售负责人：提交流程 ≤ 3 分钟 | FR-02, NFR-01 | 拆成功能设计约束 + 可测量 NFR |
| 财务：> ¥3,000 补充说明 | FR-03 | 业务规则，触发条件已量化 |
| 财务：> ¥10,000 二级审批 | FR-04 | 工作流分支规则 |
| 财务：提交/审批/驳回日志，保留 2 年 | FR-05, NFR-03 | 功能 + 保留周期分开表述 |
| 法务：银行卡/身份证 RBAC | FR-07, NFR-04 | 功能限制 + 安全测试指标 |
| 财务：月末 500 并发不卡 | NFR-02, NFR-05 | "不卡"量化为并发数 + 可用性目标 |
| 销售负责人：驳回须告知原因 | FR-06 | 直接映射 |
| 老板：第一期国内员工 | 范围约束（见第 5 节）| 转为不做项 |
| 财务：月度报表（第二优先级）| FR-08 | 来源已自带优先级，对齐为 P2 |

---

## 5. 明确的不做项（Out of Scope — Phase 1）

> 这些项目已有来源输入，但本期明确排除，避免范围蔓延。

| 不做项 | 排除原因 | 来源 |
|--------|---------|------|
| 海外法律实体报销 | 老板明确限定第一期为国内员工 | 老板 |
| 多币种支持（外币报销、汇率换算）| 同上 | 老板 |
| 境外员工账号与身份管理 | 随海外实体一并排除 | 老板（推断） |
| 月度汇总报表（实时/自动推送）| 功能本身列为 P2，实时推送超出现有输入范围 | 财务 |
| 与外部财务系统（ERP/SAP）的集成 | 无输入提及，纳入会扩大范围 | 无输入，主动排除 |
| 报销预算管控 / 超额预警 | 无输入提及 | 无输入，主动排除 |

---

## 6. 待决问题（Open Questions）

> 以下问题在进入架构设计前需要答案，以避免遗漏约束。

| # | 问题 | 影响需求 | 需回答的角色 |
|---|------|---------|-------------|
| OQ-1 | 「授权角色」（可查看 PII）具体包含哪些角色？是否有分级（如只读 vs 全字段）？ | FR-07, NFR-04 | 法务 + 财务 |
| OQ-2 | 二级审批人由系统自动路由（按金额/部门）还是人工指定？ | FR-04 | 财务 |
| OQ-3 | 驳回后员工是否可原单修改重提，还是必须新建单？ | FR-06 | 财务 + 销售负责人 |
| OQ-4 | 审计日志的查询入口是内嵌工具还是导出文件？（影响 FR-05 的实现复杂度）| FR-05 | 财务 |
| OQ-5 | 月度报表（FR-08）的下载格式要求？（Excel / CSV / PDF）| FR-08 | 财务 |

---

`★ Insight ─────────────────────────────────────`
**来源追踪（Traceability）的真实价值**：当需求被质疑或砍掉时，能立刻指向「这是法务要求的」或「老板说的」，避免争论变成意见对碰。这也是质量门控（Quality Gate）中「each requirement links to a user need」的核心目的。
`─────────────────────────────────────────────────`

---

**下一步**：此文档需要老板、财务、销售负责人、法务四方评审并解答 OQ-1 至 OQ-5，然后再进入架构设计阶段。
