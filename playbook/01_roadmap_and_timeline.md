# 01 全流程路线图与时间预算

本指南给出 EB-2 NIW 自主申请（self-petition）从自评到绿卡后续步骤的完整路线，以及按阶段的时间预算。时间预算是规划估计，按个人情况调整；法规、表格、费用、处理时限一律以官方页面为准，用到时再核对。

> 本指南不是法律意见。是否申请、主张哪些标准、表格如何填写，最终应由申请人自行决定，必要时请律师做 limited review。

## 一、全景

```text
自评 → 定 endeavor → 收集证据 → 推荐信 → 起草 → 多轮审阅 → 表格 → 在线递交
     → 收据 / premium processing → RFE 或批准 → I-485 调整身份 / 领馆办理
```

| # | 阶段 | 目标 | 主要产出（case-template/） | 时间预算 | 常见坑 |
| --- | --- | --- | --- | --- | --- |
| 1 | 自评 | 判断 EB-2 门槛和 Dhanasar 三个 prong 的证据基础 | `07_Factual_Verification_Questionnaire.md` 初稿 | 1 周 | 只看引用数，不看"别人是否在用你的成果" |
| 2 | 定 endeavor | 一句话写清做什么、给谁用、怎么传播、在美国哪里验证 | `case.json` 的 `locked_phrases` | 1–2 周 | 写成"推动 AI 发展"这类领域级口号 |
| 3 | 收集证据 | 按法律要素收齐、命名、登记 | `08_Evidence_Request_List.md`、`data/` 登记表 | 4–8 周，与起草并行 | 学校、HR、译者的回复周期最长，要最先发请求 |
| 4 | 推荐信 | 第一手、具体、可核实的事实信 | `letters/` | 每封 3–6 周 | 起步太晚；模板化、空泛赞美的信 |
| 5 | 起草 | Petition letter、H-1、H-2、H-3、Exhibit index、Officer roadmap | `01`–`05` | 约 3–4 周出完整初稿 | 先写再找证据，导致无据可引 |
| 6 | 审阅 | 事实核对、对抗性审阅、AAO 压力测试 | `14`、`15`、`12_Final_Readiness_Matrix.md` | 2–4 周，多轮 | 每改一次数字就要全局同步 |
| 7 | 表格 | I-140、ETA-9089 Appendix A + Final Determination、可选 I-907 | `09`、`11` | 3–5 天 | Part 6 与 endeavor 不一致；签名方式不合规 |
| 8 | 收尾与递交 | 冻结事实 → 签字 → 翻译 → 重建 → 视觉检查 → 递交 | `13_Filing_Closeout_Runbook.md`、`10_Online_I140_Filing_Control.md` | 最后 1–2 周 | 签字后又改内容，导致重签 |
| 9 | 收据 / premium | 保存确认页、收据、I-797C；记录 priority date | `10` §0、§7 | 以账户通知和 I-797C 为准 | 时区导致收据日期与本地日期不同 |
| 10 | 结果 | 批准；或 RFE / NOID | RFE 文件夹（`rfe-template/`） | 以通知为准 | RFE 期限可能远短于想象 |
| 11 | 后续 | I-485 调整身份或领馆办理（consular processing） | 状态时间线 | 取决于排期 | 以为 I-140 获批就有身份或工作许可 |

## 二、倒排时间线（规划估计）

下表是按递交日 T 倒排的规划估计，不是任何个人的经历，也不是 USCIS 的要求；按自己的证据基础、推荐信进度和身份期限调整。

| 时间点（相对递交日 T） | 建议完成的事 |
| --- | --- |
| T−12 至 T−10 周 | 发出推荐信请求（先发合作者信，再发独立用户/专家信）；向学校、HR、译者发出证据请求 |
| T−10 至 T−8 周 | 建立起草包（questionnaire、证据清单、petition 初稿） |
| T−8 至 T−4 周 | 证据收集、翻译、公开指标首次快照、出版状态核实 |
| T−5 至 T−1 周 | 多轮审阅：内容审阅、对抗性审阅、AAO 压力测试、替换段落、结构调整 |
| T−4 周 | 签字推荐信截止；之后到达的留作 RFE 储备 |
| T−1 周 | 刷新公开指标；表格逐题决策（Part 6、Final Determination 签名方式）；确定是否 premium processing |
| T−1 天至 T | 冻结叙述 PDF、手写签字扫描、表格签字扫描、记录哈希、全量视觉检查、递交 |
| T 之后 | 保存收据；按 uscis.gov/i-907 计算 premium 时限；结果或 RFE 以通知为准，RFE 回复期限按通知日历化 |

规划要点：

1. **起草宜提前 2–3 个月启动**，推荐信和翻译要更早。最后一个月通常主要花在审阅和一致性维护上。
2. **推荐信是关键路径**。邀请、对方修改、签字、扫描，每封往往需要数周。未能在截止日前到位的信不能成为论证支柱。
3. **每次修改都有连锁成本**：改一个指标要同步 petition、H-1、H-2、CV、展品、索引；签字后改内容必须重签。
4. **按常见薄弱点提前准备证据**：national importance 只证明了"领域重要"而非"本 endeavor 有广泛影响"；缺少第三方采用/集成/使用的客观证据；缺少清晰的未来计划、持续合作、资金或机构支持；Prong 3 只是重复前两项。详见 `playbook/08_common_weaknesses.md`。

## 三、尽早决定的事项（Decide early）

| 事项 | 为什么要早定 | 依据 / 去哪里查 |
| --- | --- | --- |
| 是否 premium processing（Form I-907） | 影响费用预算、递交方式（并行或递交后单独提交）、以及 RFE 何时来 | uscis.gov/i-907；费用见 uscis.gov/g-1055（verified on {{DATE}}） |
| 是否可同时递交 I-485 | 只有排期 current 时才可 concurrent filing；取决于当月 visa bulletin 与 USCIS 指定使用的表（Dates for Filing 或 Final Action） | USCIS "Adjustment of Status Filing Charts from the Visa Bulletin" 页面；8 CFR 245.2(a)(2) |
| 在线递交还是纸质 | 决定表格签名、付款、上传准备方式 | uscis.gov/file-online/forms-available-to-file-online |
| I-140 Part 4：调整身份还是领馆办理 | 表格必须二选一，并与长期计划一致 | Form I-140 instructions |
| 是否请律师做 limited review | 表格（尤其 Part 6、ETA-9089 Final Determination）最容易出程序性错误 | — |
| 推荐信策略（是否放、找谁） | 周期最长 | 见 playbook 推荐信指南 |
| 雇主外部活动 / 知识产权政策 | 在职期间做的独立研究、开源是否被允许；不确认就不要主张 | 员工手册、入职协议（私下保存，不递交） |
| 姓名一致性 | 公开资料用英文名或常用名时，需要在材料中说明一次对应关系 | 护照、公开主页 |
| 维持非移民身份 | I-140 递交或获批都不给身份、不延长工作许可、不保证出入境 | 状态时间线；出行前咨询律师 |

## 四、身份与期限管理

- 维护一份私有状态时间线：身份有效期、文件有效期、在职期间、出入境、递交与收据、visa bulletin 快照。
- 推导出的期限要自动计算：premium processing 截止日按工作日（跳过联邦假日）；OPT 失业天数；文件到期提醒；priority date 是否 current。
- visa bulletin 每月更新；USCIS 的调整身份图表页面可作为自动化数据源。travel.state.gov 常屏蔽自动化访问，遇到拦截就停止并手动查看。
- 每次收到通知、身份变化、换工作、出入境后，立即更新时间线。

## 五、相关文件

| 主题 | 文件 |
| --- | --- |
| 法律标准 | `playbook/02_legal_standard.md` |
| 证据收集 | `playbook/05_evidence_collection.md` |
| 在线递交 | `playbook/06_online_filing.md` |
| 审阅方法 | `playbook/07_review_method.md` |
| 常见薄弱点与对策 | `playbook/08_common_weaknesses.md` |
| 收尾执行 | `case-template/workproduct/13_Filing_Closeout_Runbook.md` |
