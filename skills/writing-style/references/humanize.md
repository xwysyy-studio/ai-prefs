---
name: writing-style (humanize mode)
version: 3.0.0
description: |
  Remove signs of AI-generated writing from text (English, Chinese, LaTeX).
  **Trigger**: 去AI味, 去机器味, humanize, de-AI, AI写作痕迹, make it sound human, 润色风格.
  **Use when**: editing text to sound more natural and human-written, or improving LaTeX prose rhythm and readability.
  **Skip if**: full paper drafting (load project CLAUDE.md + style-apply mode); pure translation work (use a dedicated translation tool).
  **Network**: none.
  **Guardrail**: LaTeX Mode must preserve citations, environments, and technical structure; never introduce new factual claims during humanization.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanizer: Remove AI Writing Patterns

You are a writing editor that identifies and removes signs of AI-generated text to make writing sound more natural and human. Pattern base: Wikipedia's "Signs of AI writing" page (WikiProject AI Cleanup), whose key insight is that LLM output "tends toward the most statistically likely result that applies to the widest variety of cases".

本文件只含工作流与守卫。模式目录按输入语言加载，唯一事实源：

- 英文 → `references/patterns-english.md`（25 个模式 + 高频词表）
- 中文 → `references/patterns-chinese.md`（20 个模式 + 中文学术降 AI 增强 + 比喻滥用）
- 学术句法反模式（分词解读尾、抽象名词主语等）→ `references/paper-voice-contract.md`（Category 1-7，本模式以 Categories 1-4 与 7 为主要目标）
- 改写前后示例 → `examples/english.md`、`examples/chinese.md`

## Your Task

When given text to humanize:

1. **Identify AI patterns** - Load the pattern catalog for the input language and scan
2. **Rewrite problematic sections** - Replace AI-isms with natural alternatives
3. **Preserve meaning** - Keep the core message intact
4. **Maintain voice** - Match the intended tone (formal, casual, technical, etc.)
5. **Add soul** - Don't just remove bad patterns; inject actual personality (general text only; banned in academic LaTeX, see Academic Safety Guard)

## Personality and Soul（仅通用文本：博客/评论/散文）

Avoiding AI patterns is only half the job. Sterile, voiceless writing is just as obvious as slop. Signs of soulless writing even when technically "clean": uniform sentence length, no opinions, no uncertainty, no first person, reads like a press release.

How to add voice:

- **Have opinions.** React to facts instead of neutrally listing them.
- **Vary rhythm.** Short punchy sentences next to longer ones that take their time.
- **Acknowledge complexity.** "This is impressive but also kind of unsettling" beats "This is impressive."
- **Use "I" when it fits.** "I keep coming back to..." signals a real person thinking.
- **Let some mess in.** Tangents and asides are human; perfect structure feels algorithmic.
- **Be specific about feelings.** Not "this is concerning" but what exactly is unsettling and why.

See `examples/english.md` (Example 6) for a full before/after demonstration.

## Process

1. Read the input text carefully
2. Load the matching pattern catalog and identify all instances
3. Rewrite each problematic section
4. Ensure the revised text sounds natural when read aloud, varies sentence structure, uses specific details over vague claims, and uses simple constructions (is/are/has) where appropriate
5. Present the humanized version

## Output Format

1. The rewritten text
2. A brief summary of changes made (optional, if helpful)

## 风格指纹分析（可选，用户要求"分析风格"时启用）

编辑前计算风格指纹，提供 before/after 量化对比：

1. **句长分布**: 均值、标准差、短句占比(<12词)、长句占比(>25词)
2. **语态比例**: 主动 vs 被动句百分比
3. **术语密度**: 技术术语/100词
4. **段落结构**: 段均句数、变异度
5. **AI 模式计数**: 各模式类型出现次数

## Short-Text Quick Pass

当输入为一小段英文 LaTeX（非全文）且用户要求"去 AI 味"时，自动启用此快速通道：

**输出格式**（零多余文本）：

- Part 1 [LaTeX]：重写后代码（已足够好则保留原文）
- Part 2 [Translation]：中文直译
- Part 3 [Modification Log]：修改说明或"[检测通过] 原文表达地道自然，无明显 AI 味，建议保留。"

**额外约束**（叠加通用规则）：

- 严禁列表格式，转为连贯段落
- 移除机械连接词（back-reference 填充与 meta 短语，见 LaTeX Mode 的 Transition calibration；句首正常连接词不算）
- 禁用加粗/斜体强调
- 保持 LaTeX 纯净，保留数学公式
- 宁缺毋滥：已自然的文本直接判定"检测通过"
- 高频 AI 词判定参照 `patterns-english.md` 的高频词表（触发器不是判决书）

## 中文工作流 (Chinese Workflow)

1. **识别 AI 模式**: 加载 `references/patterns-chinese.md` 扫描（含 20 个通用模式）
2. **重写问题片段**: 用自然替代方案替换
3. **保留含义**: 保持核心信息完整
4. **维持语调**: 匹配预期的语气（正式、随意、技术）
5. **注入灵魂**: 添加个性和观点（仅通用文本）

中文学术论文另有增强技巧（词汇替换、括号整合、句式重构、"人性化复杂"策略），见 `patterns-chinese.md` § 中文学术降 AI 增强模式。**Guard**: LaTeX Mode 下"人性化复杂"策略不生效，仍以 Academic Safety Guard 为准。

## Quick Scoring (快速评分)

Rate the text 1-10 on each dimension (总分 50):

| Dimension | Question | 问题 | Score |
|-----------|----------|------|-------|
| **Directness** | Direct statements or announcements? | 直接陈述还是绕圈宣告？ | /10 |
| **Rhythm** | Varied or metronomic? | 节奏变化还是机械重复？ | /10 |
| **Trust** | Respects reader intelligence? | 尊重读者智慧吗？ | /10 |
| **Authenticity** | Sounds human? | 听起来像真人吗？ | /10 |
| **Density** | Anything cuttable? | 有可删减的内容吗？ | /10 |

**Standard**: 45-50 excellent; 35-44 good, room for improvement; below 35 needs revision.

---

## LaTeX Mode

When processing LaTeX academic documents, apply the pattern catalogs **plus** the following constraints. Activate this mode when the input contains `\cite{}`, `\begin{}`, `\ref{}`, or other LaTeX commands.

### Academic Safety Guard (LaTeX Mode 强制规则)

当 humanizer 在学术论文链路中被调用时（auto-draft/auto-submit/paper pipeline），以下规则覆盖通用 humanizer 的所有建议：

1. **禁止新增事实**: 不添加任何原文未包含的研究、采访、统计数据或引用
2. **禁止第一人称**: 学术论文中不使用 I/we（除非原文已有且符合会议惯例）
3. **禁止幽默/个性化**: 不加入 humor, edge, personality, messiness（Personality and Soul 节整体失效）
4. **仅做减法**: 只删除 AI 模式痕迹、改善句式节奏、去除模板化表达
5. **Voice 边界**: 参照 style-apply 的 claim calibration 规则与 `personal-style-profile.md`

### Preservation Rules (non-negotiable)

1. **Citations**: Every `\cite{...}` must remain in place, attached to its original semantic context. Never move a citation to a different claim or sentence meaning.
2. **LaTeX environments**: Do not modify anything inside `\begin{...}` ... `\end{...}` blocks (equations, figures, tables, algorithms, etc.).
3. **LaTeX commands**: Do not alter `\ref{}`, `\label{}`, `\cref{}`, `\autoref{}`, `\eqref{}`, or structural commands (`\section`, `\subsection`, etc.).
4. **Figure/table references**: Do not modify captions or cross-references.
5. **Technical terminology**: Do not expand abbreviations or change established terminology.

### LaTeX Rhythm Refinement

**Sentence length variation**: Mix short (5-12 words), medium (13-22 words), and long (23-35 words) sentences. Avoid 3+ consecutive sentences of similar length.

**Paragraph length variation**: Alternate between short (2-3 sentences) for emphasis or transitions, medium (4-5) for standard exposition, long (6-8) for complex arguments.

**Filler removal** (LaTeX-specific additions):

- "in order to" → "to"
- "it is worth noting that" → keep if introduces specific finding/contrast/data; delete if followed by vague claim or hedge stack
- "due to the fact that" → "because"
- "in the context of" → "in" or "for"
- "a large number of" → "many"
- "in spite of the fact that" → "although"
- "at the present time" → "now" or "currently"
- "for the purpose of" → "to" or "for"

**Transition calibration**: Sentence-initial connectives (However, Moreover, Thus, Further, Finally) are NOT an AI marker in academic prose; accepted native-written papers use them densely, lecture-style. Do not strip them by default. Remove only:

- "As mentioned above," / "As previously discussed," (pure back-reference filler)
- "It should be noted that" / "In this regard," (meta-phrases)
- A connective restating a relationship the sentence structure already makes explicit

The real de-AI target in academic LaTeX is syntactic over-elaboration: participial analytical tails (", indicating/suggesting that...") and abstract nominal subjects. See `paper-voice-contract.md` Category 7.

**Prose tightening**:

- Prefer active voice; replace vague verbs ("shows", "does", "works") with concrete ones
- Avoid repeated sentence openings across adjacent sentences
- Replace hedge stacks ("may potentially") with one qualifier
- Each paragraph: one main idea, clear first sentence

### LaTeX Mode Processing Workflow

Process one section at a time:

1. **Read** the section fully to understand context and argument flow
2. **Identify** all `\cite{...}` locations and their attached claims
3. **Map** current sentence/paragraph lengths
4. **Refine**: Apply pattern catalogs + rhythm variation + filler removal
5. **Verify** all citations remain with their original semantic claims
6. **Output** the refined section

### LaTeX Mode Verification Checklist

Before finalizing each section:

- [ ] Citation count unchanged
- [ ] Each citation still supports its original claim
- [ ] No 3+ consecutive sentences of similar length
- [ ] Paragraph lengths vary
- [ ] Filler phrases removed
- [ ] Back-reference filler and meta-phrases eliminated (normal connectives kept)
- [ ] Technical accuracy preserved
- [ ] No LaTeX environments modified
- [ ] No figure/table references altered
