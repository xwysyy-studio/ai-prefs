---
name: writing-style
version: 2.0.1
description: |
  Unified writing style engine with 2 language layers: chinese (中文写作) and
  english (English academic + general writing). De-AI, polish, and voice
  consistency are tasks inside a layer, not separately routed modes.
  **Trigger**: 中文写作, 写一篇文章, 整理成文章, 润色文章, 中文润色, 去AI味,
  去机器味, AI写作痕迹, humanize, de-AI, make it sound human, 润色风格,
  英文写作, house style, writing style profile,
  偏好写作风格, 按我的风格写, 统一论文口吻, 统一叙事与claim强度.
  **Use when**: polishing or drafting Chinese prose (tech notes, blog, README, docs)
  or English prose (papers, LaTeX, general text).
  **Skip if**: full paper drafting pipeline (use project CLAUDE.md).
  **Guardrail**: 润色≠缩字数≠去AI味, information must survive editing; LaTeX Mode
  preserves citations, environments, and technical structure; never introduce
  new factual claims during style editing.
default_mode: direct
write_policy: may_edit_inputs
owner: academic
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Writing Style — 按语言分层的写作引擎

两个语言层，按输入语言路由。任务关键词（润色 / 去AI味 / 统一风格 / humanize）不改变加载内容：进了哪个语言层，就加载该层全部核心材料，去 AI 味只是其中一节，不是单独岔路。

## 路由

| 输入 | 层 | 核心材料（必载） |
|------|----|-----------------|
| 中文文本 | **chinese（中文写作）** | `references/chinese-writing.md` + `references/patterns-chinese.md` |
| 英文 / LaTeX | **english（英文写作）** | `references/style-apply.md` + `references/patterns-english.md` + `references/paper-voice-contract.md` |
| 中英混排 | 按正文主体语言选层 | 另一语言的片段按其所属层守卫处理 |

"只标不改 / detect / audit only" 是两层共用的子模式：仅输出问题位置、类型、原文片段引用与严重度计数，不改写。英文用 `paper-voice-contract.md` 标签清单（如 `[PLANNER_TALK]`, `[TEMPLATE_STEM]`, `[HEDGE_STACK]`），中文用 `patterns-chinese.md` 模式名。用于 rebuttal 前自查、AI 嫌疑判断、不想被改坏的旧文 audit。

长文（>8k 中文字符 / >12k 英文字符）或跨会话续写加载 `references/long-form-humanize.md`。

## 全局守卫（两层共用）

- **信息守恒**：润色≠缩字数≠去AI味。删除只针对零信息套话；删掉后读者少知道了什么，答得出就不能删。改完报告修改类型与字数变化。
- **判定边界（防过度纠正）**：不因单一特征判定 AI 味，只处理成簇出现的模式；孤立命中宁可放过。具体少见的细节、自然的自我修正、作者稳定的个人用词、长短不一的句子是真人信号，保留。引语、标题、专有名词和被当作示例讨论的文本不改写。本边界约束模式目录的判定尺度，不放松用户全局规则里的硬性禁则（破折号禁令等仍无条件执行）。
- **不新增事实**：改写只能使用原文和上下文已有的事实，不添加研究、数据或引用。
- **不改技术含义**：只改表达。
- **LaTeX 结构保真**：`\cite{}`、`\ref{}`、`\label{}`、环境、宏一律保留原位（细则见 `style-apply.md` 的 LaTeX Mode）。
- **最小编辑默认**："润色 / polish" = 微调，不重写；通顺的句子不动。
- **正面定位**：不通过否认未被提出的误解、异议或替代定位来陈述内容；"不是X而是Y"句式只用于消解读者真实会有的具体歧义。
- **结构困惑升级**：单段需删 >50% 才能"润色"、相邻段落重复同一观点、段首句关联不上任何具体主张，说明未决思路已外化为正文。停止 polish，建议转 `paper-review` Path C 做结构诊断。writing-style 处理"怎么说"；"该不该说"属于结构问题。

## Layer: chinese（中文写作）

覆盖技术笔记、博客、README、项目文档、知识库条目。学术论文不在此层（中文不做学术写作）。

总判据、工作流、母语读感手法、术语、体裁差异全在 `references/chinese-writing.md`；AI 模式目录及其使用判据在 `references/patterns-chinese.md`。

## Layer: english（英文写作）

覆盖论文起草 / 改写 / voice 统一 / 去 AI 味 / LaTeX craft，也含英文博客与 README 的通用声部（声音手法见 `style-apply.md` 的 General text voice 节；学术 LaTeX 禁止个性化，见其 Academic Safety Guard）。

**核心工作流**：
1. **先立 voice 锚（起草 / 改写正文前必做）**：读 `references/personal-style-profile.md`；用户给的 "gold" 段落优先级最高；两者不足以覆盖当前文体时索要 1-2 段理想范文，锚定后才动笔。
2. 无风格偏好时简短询问：claim strength、voice、rhythm、editing freedom。
3. 按 `references/style-apply.md` 的 Workflow A-D 执行；de-AI 目录（`patterns-english.md`）与 voice 反模式（`paper-voice-contract.md`，Categories 1-4、7 为主要目标）贯穿所有工作流，不是单独任务。

**Section playbooks**（按需加载）：`abstract-playbook.md`、`introduction-playbook.md`、`related-work-playbook.md`、`method-playbook.md`、`experiments-playbook.md`、`conclusion-impact-playbook.md`、`appendix-playbook.md`。

**其余参考**：`narrative-flow-playbook.md`、`equations-and-notation.md`、`figures-and-tables.md`、`citation-and-bibtex.md`、`latex-project-structure.md`、`definitions-theorems-playbook.md`、`annotated-writing-examples.md`、`icml2026-writing-requirements.md`。

**两个活文件（吸收循环）**：风格知识只维护两处，不按领域新建档案：
- `references/personal-style-profile.md`：个人默认写作风格（从已中稿论文提炼），所有起草 / 改写默认按它执行。
- `references/related-work-writing-notes.md`：相关工作写作学习笔记；写新论文前读 3-5 篇同类中稿论文记成条目，完稿后把值得长期保留的部分蒸馏进 personal-style-profile。
