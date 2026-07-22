---
name: writing-style
version: 1.0.0
description: |
  Unified academic writing style engine with 3 modes: style-apply (English house style),
  humanize (de-AI), chinese-academic (Chinese academic writing).
  **Trigger**: 偏好写作风格, 按我的风格写, 统一论文口吻, 统一叙事与claim强度,
  把整篇改到同一种学术英语风格, house style, writing style profile,
  去AI味, 去机器味, humanize, de-AI, AI写作痕迹, make it sound human, 润色风格,
  中文学术写作, 中文论文写作, 中文学术写作规范.
  **Use when**: applying consistent voice, removing AI patterns, or writing in Chinese academic style.
  **Skip if**: full paper drafting (use project CLAUDE.md).
  **Guardrail**: LaTeX Mode must preserve citations, environments, and technical structure;
  never introduce new factual claims during style editing.
default_mode: ask_first
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

# Writing Style — Unified Academic Style Engine

Three modes in one skill. Auto-routes based on input language and user intent.

## Mode Selection (auto-route)

| Trigger | Mode | Reference |
|---------|------|-----------|
| "去AI味/humanize/de-AI/降重/make it sound human" | **humanize** | `references/humanize.md` |
| "风格统一/house style/写作风格 profile/统一口吻" | **style-apply** | `references/style-apply.md` |
| "中文学术写作/中文论文写作/中文学术写作规范" | **chinese-academic** | `references/chinese-academic.md` |
| "润色" + English/LaTeX input | **style-apply** | `references/style-apply.md` |
| "润色" + Chinese input | **chinese-academic** | `references/chinese-academic.md` |
| "detect / audit only / 只标不改 / 只审不改" | **humanize (detect submode)** | `references/humanize.md` + `paper-voice-contract.md` |
| Ambiguous | Ask: "你需要去 AI 味、统一英文风格、还是中文学术写作？" | — |

## Mode: style-apply (English House Style)

Apply a consistent academic English voice across paper sections: structure, signposting,
paragraph rhythm, claim calibration, tables/figures, and equation conventions.

**When to use**: 统一英文论文风格 / apply house style / consistent voice across sections.

**Core workflow**:
1. **先立 voice 锚（必做，起草/改写正文前）**: 读 `references/personal-style-profile.md`；用户主动给的 "gold" 段落优先级最高；两者都不足以覆盖当前文体时，向用户索要 1-2 段理想范文（或从其已发表文本抽段请用户确认），锚定后才动笔
2. If no style preference provided, ask about: claim strength, voice, rhythm, editing freedom
3. Load `references/style-apply.md` for full rules
4. Apply section-by-section using section playbooks in `references/`

**Voice Contract**: See `references/paper-voice-contract.md` for generator voice anti-patterns.

**Section playbooks** (load on demand):
- `references/abstract-playbook.md`
- `references/introduction-playbook.md`
- `references/related-work-playbook.md`
- `references/method-playbook.md`
- `references/experiments-playbook.md`
- `references/conclusion-impact-playbook.md`
- `references/appendix-playbook.md`

**Additional references**: `references/narrative-flow-playbook.md`, `references/equations-and-notation.md`,
`references/figures-and-tables.md`, `references/citation-and-bibtex.md`, `references/latex-project-structure.md`,
`references/definitions-theorems-playbook.md`, `references/revision-checklist.md`,
`references/annotated-writing-examples.md`.

**Venue-specific profiles**: `references/icml2026-writing-requirements.md`.

**两个活文件（吸收循环）**: 风格知识只维护两处，不按领域新建档案：
- `references/personal-style-profile.md`: 用户的个人默认写作风格（从用户已中稿论文提炼）。所有起草/改写默认按它执行；从相关工作内化的措辞与手法最终沉淀到这里。
- `references/related-work-writing-notes.md`: 相关工作写作学习笔记。写新论文前，读 3-5 篇同类中稿论文，把故事骨架、修辞动作、可借鉴表述记成一个条目，写作中模仿；完稿后把值得长期保留的部分蒸馏进 personal-style-profile，条目压缩或清理。

## Mode: humanize (De-AI)

Remove signs of AI-generated writing. Supports English, Chinese, and LaTeX.

**When to use**: 去AI味 / humanize / de-AI / 降重 / make it sound human.

**Core workflow**:
1. Load `references/humanize.md` (工作流 + LaTeX 守卫) plus the pattern catalog for the input language: `references/patterns-english.md` (英) / `references/patterns-chinese.md` (中)
2. Identify AI writing patterns (formulaic openings, hedge stacking, syntactic over-elaboration, etc.)
3. Rewrite with natural alternatives — preserve meaning, maintain voice, add soul (general text only)
4. For LaTeX: preserve all `\cite{}`, `\ref{}`, environments, and technical structure

**Sub-modes**:
- English prose → standard humanization with pattern catalog
- Chinese prose → load `references/patterns-chinese.md`
- LaTeX Mode → preserve citations/environments, focus on prose rhythm and readability
- **Detect submode** (触发: detect / audit only / 只标不改) → 仅审计不改写。扫描后输出 `paper-voice-contract.md` 标签清单（如 `[PLANNER_TALK]`, `[TEMPLATE_STEM]`, `[HEDGE_STACK]`）+ 原文片段引用 + 严重度计数 + 一句 "clear problem vs judgment call" 判断；不修改原文。用于 rebuttal 前自查、审稿人 AI 嫌疑判断、不想被改坏的旧文 audit。

**Voice Contract**: Implements Categories 1-4 and 7 from `references/paper-voice-contract.md` as primary targets.

**References**: `references/humanize.md`, `references/patterns-english.md`, `references/patterns-chinese.md`, `references/long-form-humanize.md` (load for docs >8k chars or multi-session workflows).

## Mode: chinese-academic (中文学术写作)

中文学术写作风格，适用于中文期刊论文、学位论文、中文技术报告等。

**When to use**: 中文学术写作 / 中文论文写作 / 中文学术写作规范。

**Core workflow**:
1. **先立 voice 锚（必做，起草/改写正文前）**: 读 `references/chinese-style-profile.md`；不足以覆盖当前文体时，向用户索要 1-2 段理想范文，锚定后才动笔
2. If no preference provided, ask about: 论断强度、改写自由度、术语偏好、论文阶段
3. Load `references/chinese-academic.md` for full rules
4. Apply section-by-section using Chinese playbooks

**Section playbooks** (load on demand):
- `references/abstract-playbook.md` (Chinese variant in chinese-academic.md)
- `references/introduction-playbook.md` (Chinese variant)
- `references/literature-review-playbook.md`
- `references/method-playbook.md` (Chinese variant)
- `references/experiments-playbook.md` (Chinese variant)
- `references/conclusion-playbook.md`

**Additional references**: `references/chinese-style-profile.md`, `references/terminology-and-citation.md`,
`references/narrative-flow-playbook.md`, `references/figures-and-tables.md`, `references/revision-checklist.md`.

## Non-Negotiables (all modes)

- **Never introduce new factual claims** during style editing
- **Never change technical meaning** — only improve expression
- **Preserve all LaTeX structure** (citations, labels, environments, macros)
- **Minimal edit by default** — "润色/polish" = micro-adjustments, not rewrite
- **Voice contract compliance** — check against `references/paper-voice-contract.md`
- **结构困惑升级** — 风格编辑中遇到以下信号，停止 polish，建议转 `paper-review` Path C 做结构诊断：(a) 单段需删 >50% 才能"润色"（不是废话多，是未决思路的外化）；(b) 同一观点相邻段落重复陈述；(c) 段首句无法关联论文任何具体 claim。writing-style 解决"怎么说"，不解决"该不该说"，后者是结构问题。
