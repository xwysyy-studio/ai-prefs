---
name: writing-style
version: 2.0.3
description: |
  Unified writing style engine with 2 language layers: chinese (中文写作) and
  english (English academic + general writing). De-AI, polish, and voice
  consistency are tasks inside a layer, not separately routed modes.
  **Trigger**: 中文写作, 写一篇文章, 整理成文章, 润色文章, 中文润色, 去AI味,
  去机器味, AI写作痕迹, humanize, de-AI, make it sound human, 润色风格,
  英文写作, 论文润色, 论文修改, 写摘要, 写引言, 写结论, 压缩论文,
  组织实验章节, 防御性写作, defensive writing, house style, writing style profile,
  论文故事怎么讲, 结果怎么组织成论文, 实验部分写作思路, paper story,
  organize results into a paper, 偏好写作风格, 按我的风格写, 统一论文口吻,
  统一叙事与claim强度.
  **Use when**: polishing or drafting Chinese prose (tech notes, blog, README, docs)
  or English prose (papers, LaTeX, general text), including developing a whole
  paper's story, section logic, experiment narrative, and focused defensive-writing
  audits from real project material.
  **Skip if**: selecting a new research direction (use research-idea), independently
  assessing a manuscript as a reviewer/advisor, running a whole-manuscript
  defensive-writing audit, or checking before submission (use paper-review), or
  responding to actual reviews after submission (use rebuttal).
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

"只标不改 / detect / audit only" 是两层共用的子模式：仅输出问题位置、类型、原文片段引用与严重度计数，不改写。英文用 `paper-voice-contract.md` 标签清单（如 `[PLANNER_TALK]`, `[TEMPLATE_STEM]`, `[HEDGE_STACK]`, `[DEFENSIVE_POSTURE]`），中文用 `patterns-chinese.md` 模式名。用于 rebuttal 前自查、不想被改坏的旧文 audit。审计输出只描述表达问题；词汇、格式与单项模式的命中只触发审读，不据此判断文本由谁写成。

长文（>8k 中文字符 / >12k 英文字符）或跨会话续写加载 `references/long-form-humanize.md`。

## 全局守卫（两层共用）

- **信息守恒**：润色≠缩字数≠去AI味。删除只针对零信息套话；删掉后读者少知道了什么，答得出就不能删。改完报告修改类型与字数变化。
- **判定边界（防过度纠正）**：不因单一特征判定 AI 味，只处理成簇出现的模式；孤立命中宁可放过。具体少见的细节、自然的自我修正、作者稳定的个人用词、长短不一的句子是真人信号，保留。引语、标题、专有名词和被当作示例讨论的文本不改写。本边界约束模式目录的判定尺度，不放松用户全局规则里的硬性禁则（破折号禁令等仍无条件执行）。
- **不新增事实**：改写只能使用原文和上下文已有的事实，不添加研究、数据或引用。
- **声音来源守恒**：改写只保留或显化原文与用户上下文已有的第一人称、立场、情绪、对立关系和节奏，不为显得像人而新增这些内容。
- **不改技术含义**：只改表达。
- **LaTeX 结构保真**：`\cite{}`、`\ref{}`、`\label{}`、环境、宏一律保留原位（细则见 `style-apply.md` 的 LaTeX Mode）。
- **最小编辑默认**："润色 / polish" = 微调，不重写；通顺的句子不动。
- **正面定位**：研究对象、成立范围与贡献直接写成正面、带范围的 claim。原稿自身的 `we do not claim`、`not X but Y` 或自我削弱句不构成读者世界里的质疑来源；润色时把其中的有效范围改成正面陈述。只有原文证据、相关工作或真实审稿意见已经提出具体歧义时，才保留回应所必需的否定。
- **防御性写作处理**：先从原句拆出对象、条件、结果、数值和有效 qualifier，再用主体、动作、条件、结果直接重写。作者如何限制、否认或评价自己的 claim 不进入正文；若删掉这类姿态句后事实与范围仍完整，就删除。终检时逐句回答“读者新知道了什么事实”；只能回答“作者更谨慎了”的句子继续重写。
- **学术主张与证据**：论文围绕实际材料能够支撑的最有价值中心主张组织，不平均展示全部过程和结果。主张强度由证据决定；结果实质限制或推翻中心主张时，交用户收窄或重构故事并如实披露。评价依据在结果产生前按研究问题与领域惯例确定，结果产生后不得通过静默换指标、数据或比较条件掩盖失败。
- **结构动作边界**：单段需删 >50% 才能"润色"、相邻段落重复同一观点、段首句关联不上任何具体主张，说明微调不足以完成任务。用户要求起草、改写或组织论文时，在本 skill 内升级到故事和章节结构；用户要求独立评判整篇稿件时转 `paper-review`。

## Layer: chinese（中文写作）

覆盖技术笔记、博客、README、项目文档、知识库条目。学术论文不在此层（中文不做学术写作）。

总判据、工作流、母语读感手法、术语、体裁差异全在 `references/chinese-writing.md`；AI 模式目录及其使用判据在 `references/patterns-chinese.md`。

## Layer: english（英文写作）

覆盖整篇论文故事与章节逻辑的发展、实验叙事、论文起草 / 改写 / voice 统一 / 去 AI 味 / LaTeX craft，也含英文博客与 README 的通用声部（声音手法见 `style-apply.md` 的 General text voice 节；学术 LaTeX 禁止个性化，见其 Academic Safety Guard）。

**核心工作流**：
1. **先读真实材料**：加载项目 CLAUDE.md / AGENTS.md、已定 story、论文全文、相关工作笔记与实际结果。项目口径是当前论文的第一权威。
2. **学术起草与结构改写先立全文逻辑**：加载 `references/narrative-flow-playbook.md`，用 `assets/claim-evidence-map.md` 选择实际证据支撑的中心主张并安排支持性主张。故事已由 `research-idea` 或项目上下文拍板时直接发展；材料只能支持更窄口径或核心结果与原故事冲突时，把差距交给用户决定。
3. **再立 voice 锚**：读 `references/personal-style-profile.md`；用户给的 "gold" 段落优先级最高；两者不足以覆盖当前文体时索要 1-2 段理想范文，锚定后才动笔。
4. 无风格偏好时简短询问 voice、rhythm、editing freedom；claim strength 始终由证据决定。
5. 按 `references/style-apply.md` 的 Workflow A-D 执行；de-AI 目录（`patterns-english.md`）与 voice 反模式（`paper-voice-contract.md`，Categories 1-4、7-8 为主要目标）贯穿所有工作流，不是单独任务。

**Section playbooks**（按需加载）：`abstract-playbook.md`、`introduction-playbook.md`、`related-work-playbook.md`、`method-playbook.md`、`experiments-playbook.md`、`conclusion-impact-playbook.md`、`appendix-playbook.md`。

**其余参考**：`narrative-flow-playbook.md`、`equations-and-notation.md`、`figures-and-tables.md`、`citation-and-bibtex.md`、`latex-project-structure.md`、`definitions-theorems-playbook.md`、`annotated-writing-examples.md`、`icml2026-writing-requirements.md`。

**两个活文件（吸收循环）**：风格知识只维护两处，不按领域新建档案：
- `references/personal-style-profile.md`：个人默认写作风格（从已中稿论文提炼），所有起草 / 改写默认按它执行。
- `references/related-work-writing-notes.md`：相关工作写作学习笔记；写新论文前读 3-5 篇同类中稿论文记成条目，完稿后把值得长期保留的部分蒸馏进 personal-style-profile。
