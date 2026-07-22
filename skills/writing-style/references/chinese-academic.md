---
name: writing-style (chinese-academic mode)
description: >-
  中文学术写作风格规范，适用于中文期刊论文、学位论文、中文技术报告等。
  触发场景：中文论文写作/统一中文学术口吻/中文学术写作规范/中文论文润色。
  覆盖叙事结构、逻辑展开、用词分寸、专业术语、引用规范，
  适用于摘要/绪论/文献综述/系统设计/实验分析/总结各章节。
---

# 中文学术写作风格

通用中文学术写作规范层，覆盖：叙事结构、段落节奏、论断分寸、术语一致性、图表规范、引用格式。适用于中文期刊论文、学位论文、中文技术报告等。

设计为可反复叠加使用的"风格层"——在起草和修改各章节时均可调用。

## Scope / non-goals

- 本 skill 聚焦**中文写作质量**
- **不是** Word/LaTeX 排版工具——排版细节（字体、字号）按目标 venue/学校要求
- **不是** 查重工具——仅提供降低查重率的写作建议

## Ask-first：确认写作偏好

如果用户未明确偏好，简短询问以下关键项：

- **论断强度**：保守（默认）vs 中等
- **改写自由度**：仅微调用词 / 可调整段落结构 / 可重构章节
- **术语偏好**：是否有已确定的术语表
- **论文阶段**：大纲 / 初稿 / 修改稿 / 终稿润色

如果用户提供了1-2个"满意段落"作为参考，将其视为最高优先级的风格标杆。

### 风格偏好模板（用户可选填）

```
- 语气关键词（3-8个）：（如：客观、严谨、简洁、保守、工程化）
- 论断强度：保守 / 中等
- 改写自由度：仅微调用词 / 可调段落结构 / 可重构章节
- 术语偏好：使用固定术语表 / 自定义 / 按领域惯例
- 论文阶段：大纲 / 初稿 / 修改稿 / 终稿润色
- 句式偏好：偏短句 / 长短交替 / 无特别要求
```

## Paths (安装/路径)

为避免反复确认“文件在哪、引用能否找到”，建议明确以下两点：

- **仓库内使用（默认）**：直接在论文仓库中使用本目录 `chinese-writing-style/`，并按本目录下的相对路径引用 `references/*` 与 `assets/*`。
- **全局安装（可选）**：若希望 Codex 在其它仓库也能触发该 skill，可将整个 `chinese-writing-style/` 复制到技能目录（常见位置为 `~/.agents/skills/writing-style/`；若你的环境使用 `$CODEX_HOME/skills/`，则放入对应目录）。

注意：本 skill 的内部引用默认以 `chinese-writing-style/` 为根（例如 `references/chinese-style-profile.md`），移动目录时需保持 `references/`、`assets/` 的层级不变。

## What to ask the user for (inputs)

用户提出“按中文毕设风格写/润色/改写/统一口吻”时，优先索取以下最小信息（缺一也能开始，但会增加来回沟通成本）：

1. **目标内容**：要处理的章节/小节（直接粘贴文本，Markdown/LaTeX/纯文本均可）或文件路径。
2. **论文阶段**：大纲 / 初稿 / 修改稿 / 终稿润色。
3. **改写自由度**：仅微调用词 / 可调整段落结构 / 可重构章节。
4. **论断强度**：保守（默认）/ 中等（更明确但仍有界）。
5. **术语约束**：是否已有术语表；若有，提供“固定术语对照表”（中文+英文+缩写/简称），并说明哪些术语禁止替换为同义表达。
6. （可选）**风格标杆**：1–2段你最满意的“黄金段落”，用于口吻对齐。

## 核心风格规则（速查）

| 规则 | 说明 |
|------|------|
| 人称 | "本文"/"本工作"/"本研究"/"本课题"，禁止"我"/"我们" |
| 论断分寸 | 默认保守："有助于/初步表明"；避免"首次/创新性/证明了" |
| 总分总 | 论文级→章节级→段落级三层嵌套 |
| 术语 | 首次：中文(English Full Name, ABB)；此后用缩写 |
| 引用 | [数字]格式；叙述式/注释式两种句式 |
| 标点 | 中文全角（。；、），英文/公式半角 |
| 段落 | 总领句在前，证据/细节在后 |
| 贡献 | "本文的主要贡献如下："（可选写N点）+ 编号列表 |
| 章间 | 插入分页符，除绪论和结论外每章需写引言 |

详细规则见 `references/chinese-style-profile.md`。

## 工作流选择

### 工作流 A — 大纲 + 故事线（无初稿）

1. 创建论点→证据映射表（使用 `assets/claim-evidence-map.md`）
2. 起草章节大纲（使用 `assets/thesis-outline-template.md` 作为模板）
3. 规划图表：每个贡献点对应哪些图/表
4. 撰写绪论故事弧：背景→现状→不足→方案→贡献→结果预告
5. 为系统设计章和实验章生成内容待办清单

参考：`references/chinese-style-profile.md`, `references/introduction-playbook.md`
辅助：`references/method-playbook.md`, `references/experiments-playbook.md`

### 工作流 B — 改写已有稿件

1. 提取现有结构：各章标题、各节要点
2. 检查论文"脊柱"：
   - 一句话论文主题 → 2-4个贡献点 → 论点-证据对齐
3. 优先改写摘要 + 绪论（杠杆最大）
4. 确保每节开头有总领句（1-2句点明本节核心）
5. 补充章节间过渡（使用 `assets/transition-phrasebank.md`）

参考：`references/abstract-playbook.md`, `references/chinese-style-profile.md`
辅助：`references/literature-review-playbook.md`, `references/narrative-flow-playbook.md`

### 工作流 C — 章节级写作（指定章节）

根据用户指定的章节，调用对应 playbook：

| 章节 | Playbook |
|------|----------|
| 摘要 | `references/abstract-playbook.md` |
| 绪论 | `references/introduction-playbook.md` |
| 文献综述 | `references/literature-review-playbook.md` |
| 系统设计/方法 | `references/method-playbook.md` |
| 系统实现 | `references/method-playbook.md`（系统实现写法见该文末尾） |
| 系统测试 | `references/experiments-playbook.md`（含系统测试用例表模板） |
| 实验与分析 | `references/experiments-playbook.md` |
| 总结与展望 | `references/conclusion-playbook.md` |

通用辅助：
- `references/narrative-flow-playbook.md`（叙事逻辑）
- `references/terminology-and-citation.md`（术语与引用）
- `references/figures-and-tables.md`（图表规范）
- `assets/transition-phrasebank.md`（过渡短语）
- 术语约定：建议在系统设计章开头插入术语约定段落（模板见 `references/terminology-and-citation.md`）

### 工作流 D — 终稿审查

1. 逐项检查（使用 `references/revision-checklist.md`）
2. 重点检查：
   - 摘要是否包含问题+方法+结果，关键词3-5个
   - 贡献是否明确且与实验对应
   - 术语是否全文一致
   - 参考文献近3年比例是否≥30%
   - 图表标题是否规范（表上图下）
3. 格式检查（按目标 venue/学校要求）：
   - 结构是否完整
   - 字体字号是否符合规范
   - 查重率预估（检查大段引用是否已改写）

参考：`references/revision-checklist.md`, `references/chinese-style-profile.md`

4. .docx 格式验收（若最终交付物为 Word 文档）：
   - 将"内容终稿审查"与"文档格式验收"分离为两个独立步骤
   - 格式验收使用 `docx` skill 的论文审计工具（详见 `docx` skill 的 `references/thesis-format-audit-overview.md`）
   - 交付结论使用分级标签：
     - `content-reviewed only`：仅完成内容审查
     - `structure-audited`：完成结构审计（章节完整性）
     - `OOXML-risk-checked`：完成 OOXML 风险审计（隐藏格式问题）
     - `visually-reviewed`：完成 PDF 逐页视觉验收
   - 若无法进行 Word/PDF 视觉复核，交付语必须显式说明审计级别

## 审阅视角（导师审稿模拟）

作为"导师审稿"时，优先检查以下高杠杆项：

1. **脊柱清晰度**：一句话主题 + 2-4个贡献，每个贡献有图/表支撑
2. **摘要质量**：问题→方法→结果→意义四要素齐全；有具体数字
3. **绪论弧线**：背景→现状→不足→方案→贡献→结果预告
4. **论断校准**：避免"首次""显著"等无支撑表述
5. **证据对齐**：每个贡献点在实验中有对应验证
6. **格式合规**：符合目标 venue/学校的格式规范

## 关键参考文件

### 风格与结构
- `references/chinese-style-profile.md`（总风格规范）
- `references/narrative-flow-playbook.md`（总分总叙事逻辑）

### 章节 Playbook
- `references/abstract-playbook.md`
- `references/introduction-playbook.md`
- `references/literature-review-playbook.md`
- `references/method-playbook.md`
- `references/experiments-playbook.md`
- `references/conclusion-playbook.md`

### 术语、引用与图表
- `references/terminology-and-citation.md`
- `references/figures-and-tables.md`
- `references/revision-checklist.md`

### 模板与资源
- `assets/transition-phrasebank.md`（中文过渡词短语库）
- `assets/thesis-outline-template.md`（毕业论文大纲模板）
- `assets/claim-evidence-map.md`（论点-证据映射表）

## 规范来源（可追溯）

格式规范按具体项目/venue 要求加载，不在此全局 skill 中硬编码。

---

**轻量场景指引**：单段段落级简易润色（用户粘贴一段直接润色、Word 友好输出、无需风格定制）→ 直接以最小化编辑原则 inline 处理（保留作者措辞、仅微调措辞 / 不重组），无需进入本 skill 的完整交互式协议。
