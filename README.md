# EB-2 NIW 自助申请套件

给想自己准备 EB-2 NIW（National Interest Waiver）I-140 自申的人用的一套工作系统：

- **方法**（`playbook/`）：完整流程、法律标准、文书写法、推荐信、证据收集、在线递交、多轮自审、常见薄弱点与对策、RFE 应对。
- **模板**（`case-template/`）：申请信、Proposed Endeavor 陈述、个人陈述、Officer Roadmap、证据清单、主张-证据台账、事实核对表、表格与递交控制、自审清单、推荐信与翻译证明、RFE 回复骨架。全部英文，和递交材料一致。
- **工具链**（`tools/kit.py`）：Markdown → Pandoc → Typst → PDF。自动检查每个 `[Exhibit X-n]` 引用都能对上、没有遗漏的占位符、核心表述在各文件中一致；生成带书签的证据 binder，以及按 USCIS 在线上传单文件大小限制切好的上传包和哈希清单。

> **免责声明**：这不是法律意见，也不预测结果。工具只证明文件完整、可复现，不证明法律上够格。表格选项、费用、递交渠道等每次使用前都要以 USCIS 官网为准；建议至少请移民律师做一次有限审阅（limited-scope review）。

## 快速开始

需要 macOS 或 Linux、[Homebrew](https://brew.sh)（或自行安装 `uv`、`pandoc`、`typst`、`poppler`）。

```bash
make bootstrap
```

```bash
make doctor
```

```bash
make demo
```

`make demo` 用空白模板加占位 PDF 跑一遍完整流程，输出在 `.tmp/demo/output/`，可以先看看最终产物长什么样。

开始自己的案子：

```bash
make new ID=my-niw NAME="Your Full Name"
```

```bash
make check CASE=cases/my-niw
```

之后就是：填模板 → 把证据 PDF 放进 `cases/my-niw/evidence/` 并登记到 `data/exhibit_registry.json` → `make check` → `make review` 看草稿 PDF → 循环。

## 建议阅读顺序

| 顺序 | 文件 | 什么时候看 |
| --- | --- | --- |
| 1 | `playbook/01_roadmap_and_timeline.md` | 第一天：全流程、时间预算、需要尽早决定的事 |
| 2 | `playbook/02_legal_standard.md` | 第一周：EB-2 门槛、Dhanasar 三要素、一手法律来源 |
| 3 | `playbook/08_common_weaknesses.md` | 第一周：常见薄弱点与对策——起草前就按这些点准备证据 |
| 4 | `playbook/03_writing_the_petition.md` | 确定 endeavor、开始写申请信时 |
| 5 | `playbook/04_recommendation_letters.md` | 尽早——推荐信最耗时间 |
| 6 | `playbook/05_evidence_collection.md` | 收集证据期间 |
| 7 | `playbook/07_review_method.md` | 初稿完成后，多轮自审 |
| 8 | `playbook/06_online_filing.md` | 递交前两周 |
| 9 | `playbook/09_rfe_response.md` | 收到 RFE 时（也建议递交前读一遍，提前补强） |

## 目录

| 路径 | 内容 | Git |
| --- | --- | --- |
| `playbook/` | 中文方法指南 | 跟踪 |
| `case-template/` | 空白案件模板（英文） | 跟踪 |
| `cases/<id>/workproduct/` | 你的草稿与控制文件 | 跟踪 |
| `cases/<id>/data/` | 证据登记表、文件清单、冻结记录 | 跟踪 |
| `cases/<id>/evidence/` | 递交用的证据 PDF | **忽略** |
| `cases/<id>/source_documents/` | 原件扫描、身份文件 | **忽略** |
| `cases/<id>/private/` | 表格预填、A 号、护照号、地址等 | **忽略** |
| `cases/<id>/output/` | 生成的 PDF | **忽略** |
| `tools/`、`templates/`、`tests/` | 构建引擎、排版主题、测试 | 跟踪 |

如果用 Git 同步，请用**私有**仓库。默认 `.gitignore` 会忽略所有 PDF 和图片，身份文件永远不进 Git。

## 常用命令

| 命令 | 作用 |
| --- | --- |
| `make check` | 草稿检查：引用解析、每个证据都被引用、核心表述一致、隐私号码扫描；缺证据和占位符只报 warning |
| `make final` | 递交前检查：占位符、占位 PDF、缺失证据全部变成 error |
| `make stubs` | 为还没到手的证据生成红色 PLACEHOLDER 页，方便提前预览排版 |
| `make review` | 带 DRAFT 水印的申请信和完整审阅包 PDF |
| `make binder` | 所有证据按登记顺序合成一个带书签和封面的 PDF |
| `make preview` | 带水印的在线上传包（允许有缺口） |
| `make online` | 正式在线上传包：`make final` 不通过就拒绝生成 |
| `make freeze LABEL=filed-2026-01-31` | 递交后记录上传包和证据的 SHA-256；之后 `make verify-frozen` 可证明没改过 |

多个案件时加 `CASE=cases/<id>`；只有一个案件时会自动选中。

## 模板约定

- `{{PLACEHOLDER}}`：需要你填的内容。`make final` 会拦下任何没填的。
- `<!-- GUIDE: ... -->`：写作指导和"为什么"，不会出现在 PDF 里。很多经验写在这里，填之前先读。
- 证据引用只能写成 `[Exhibit B-1]`、`[Exhibits D-1, D-2]`、`[Exhibits D-1–D-3]`（en dash）。
- Markdown 里的 `---` 在 PDF 里是分页。
- 证据编号：A 身份/身份状态，B 学位，C 工作，D 论文与引用，E 采用与影响，F 审稿，G 国家重要性的客观背景，H 申请人陈述与简历，I 推荐信，J 奖项。不用的编号直接从登记表删掉；RFE 补充的新证据用新字母（K、L、M…），不要改已递交的编号。

## 配合 AI agent 使用

仓库根目录的 `AGENTS.md`（Claude Code 读 `CLAUDE.md`）写了 agent 的规则：不编造事实、每个主张都要有出处、法律以一手来源为准、隐私边界、递交后冻结。用 agent 起草或审稿时，让它先读 `AGENTS.md` 和对应的 playbook 章节；它写的每一句事实，你都要对着证据核一遍。
