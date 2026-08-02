---
name: writing-style (style-apply mode)
description: >-
  Preferred writing style / house style profile for academic paper drafting and revision
  (English + LaTeX). Use when the user asks: 偏好写作风格/按我的风格写/统一论文口吻/
  统一叙事与claim强度/把整篇改到同一种学术英语风格. Apply a consistent voice, calibrated
  claims, evidence-first narrative, and LaTeX craft conventions across sections
  (Abstract/Intro/Related Work/Method/Experiments/Conclusion).
---

# Preferred Writing Style (English + LaTeX)

This skill is a **writing + LaTeX craft playbook** for keeping a paper’s voice consistent:
structure, signposting, paragraph rhythm, claim calibration, tables/figures, and equation
conventions.

It is designed to be used as a “style layer” you can apply repeatedly while drafting and
revising sections.

## Scope / non-goals

- This skill focuses on **writing quality** and **LaTeX craft**.
- It is **not** a strict venue policy checker. If the user requests strict compliance checks,
  ask which venue they target and propose a checklist-based plan before making edits.
- The stricter house rules (em-dash ban, banned-word lists) are deliberate de-AI
  tightening beyond venue norms, not review red lines: accepted papers do use these. The rules
  stay in force anyway. Em-dashes especially: whatever their pre-AI history, AI training corpora
  have made them a default AI association, so they are banned outright (global rule
  `~/.claude/rules/writing-tone.md`); use commas, colons, parentheses, or split the sentence.
  Do not present house rules as "humans don't write this way"; present them as "we choose not to".

## Ask-first: capture the user’s style profile

If the user did not provide a style preference, ask only what you need (keep it short):

- **Claim strength**: conservative (default) vs stronger wording.
- **Voice**: “we” vs impersonal; assertive vs cautious.
- **Sentence/paragraph rhythm**: shorter vs longer; how much signposting to use.
- **Editing freedom**: can you restructure paragraphs/sections, or only micro-edits?
- **LaTeX freedom**: can you refactor macros / project structure, or keep as-is?

If the user shares 1–2 “gold” paragraphs they like, treat that as the highest-priority style
reference.

### Style profile template (user fill-in, optional)

- Tone keywords (3–8):
- Claim strength: conservative / medium / strong
- Allowed rewrites: micro / moderate / restructure
- “We” voice: yes / no
- Preferred transitions: light / medium / heavy
- LaTeX constraints: keep macros / allow macro edits / allow project refactor

## Paths (so commands work)

Helper scripts live in this skill's `scripts/` directory. Run them with a path relative to
the skill root (the directory containing this skill's SKILL.md, written `<skill-root>` below),
so commands work regardless of where the skill is installed.

## What to ask the user for (inputs)

When asked to “write/rewrite a paper in my preferred style”, request:

1. The LaTeX project (at least the main `.tex`, `macro.tex` if any, `.bib`, and key `tables/*.tex`).
2. Paper stage: “outline only”, “first draft”, “revise existing draft”, or “final polish”.
3. Claimed contributions (2–4 bullet points) and the strongest evidence for each (figure/table/metric).
4. Target audience + closest related work (2–5 papers).
5. Any venue constraints the user cares about (page limit / anonymization / required sections).

## Workflow selector

- If the user has **no draft** → Workflow A (outline from a settled story).
- If the user has a **draft** → Workflow B (rewrite + strengthen narrative).
- If the user needs **LaTeX help** → Workflow C (LaTeX craft).
- If the user is close to submission → Workflow D (final polish + submission-aware self-checks).

## Workflow A — Outline from a settled story

0. Start from the settled one-sentence story (from `research-idea` or the user): what prior approaches flatten, conflate, or leave out of view, and what this paper lays open. Every step below expands that sentence. If the story is still unsettled, route to `research-idea` first.
1. Create a claim→evidence map (use `assets/claim-evidence-map.md`).
2. Draft an outline with a page budget if applicable (use `assets/icml-8page-outline.md` as a generic template).
3. Plan figures/tables first (what supports each claim).
4. Write a “reviewer-proof” introduction arc:
   - Context → gap → why hard → approach → contributions → results preview.
5. Produce section-specific TODOs for Method and Experiments (what must be said, what can be deferred to appendix).

Reference: `references/personal-style-profile.md`, `references/introduction-playbook.md`.
Also useful: `references/method-playbook.md`, `references/experiments-playbook.md`.

## Workflow B — Rewrite + improve clarity (existing draft)

1. Extract structure (optional):
   - `python3 <skill-root>/scripts/extract_tex_outline.py --tex <main.tex>`
2. Improve the paper’s “spine”:
   - One-sentence thesis, then 2–4 contributions, then claim→evidence alignment.
3. Rewrite Abstract + Introduction first (highest leverage).
4. Make each section start with its key message (1–2 sentences).
5. Add signposting transitions between sections and within long sections.

Reference: `references/abstract-playbook.md`, `references/personal-style-profile.md`.
Also useful: `references/related-work-playbook.md`, `references/method-playbook.md`, `references/experiments-playbook.md`.

## Workflow C — LaTeX craft (equations / figures / tables / structure)

1. Enforce clean project structure:
   - Main file imports packages + `\input{macro}`.
   - Sections live in separate `*.tex` files.
   - Large tables live in `tables/*.tex` and are `\input{}` into `table*`.
2. Equations and notation:
   - Define symbols before use.
   - Use `\triangleq` for definitions and `\text{}` for textual subscripts.
   - Prefer one equation per concept; push long derivations to appendix.
3. Figures/tables:
   - Captions are self-contained and interpret the figure (not just “results”).
   - Use `booktabs` style tables; avoid vertical rules.
   - Ensure readability in grayscale (color as an accent, not the only channel).

References: `references/latex-project-structure.md`, `references/equations-and-notation.md`, `references/figures-and-tables.md`, `assets/latex-snippets.tex`.

## Workflow D — Final polish + submission-aware self-checks

1. Run quick writing checks (heuristic):
   - `python3 <skill-root>/scripts/icml2026_writing_quickcheck.py --tex <main.tex>`
2. Ensure:
   - Abstract is one paragraph and states problem, gap, approach, and results.
   - Contributions are explicit and match experiments.
   - Limitations are specific (not generic “future work”).
3. If the user targets a double-blind venue, check anonymization leaks (acknowledgements, URLs, PDF metadata) and ask before making structural edits.

Reference: `references/conclusion-impact-playbook.md`.

## Mentor review rubric (what I check first)

This is the high-leverage checklist I use when “reviewing as an advisor”:

1. **Spine clarity**: one-sentence thesis + 2–4 contributions, each tied to a figure/table.
2. **Abstract quality**: single paragraph; gap is explicit; includes at least one concrete number; bounded claims.
3. **Introduction arc**: context → closest work → gap → why hard → approach → contributions → (optional) results preview.
4. **Claim calibration**: avoid “the first” unless narrowly scoped; “significant” requires an adjacent number (the accepted-paper norm is adjacency, not avoidance).
5. **Evidence alignment**: every contribution is verified by experiments; no “paper-only” promises.
6. **LaTeX hygiene**: no undefined refs; tables/figures are readable; captions are self-contained.

## General text voice（非学术英文：博客 / README / 随笔）

Academic Safety Guard 只约束学术链路。通用英文文本在清除模式之外还要有真人声音，无声的"干净"文本同样一眼是 AI：句长均一、零观点、零第一人称、读起来像新闻通稿。手法：有观点就表态，不中性罗列事实；长短句混排；承认复杂感受（"impressive but also unsettling"比"impressive"真实）；合适处用 "I"；允许一两句离题；情绪写具体不写笼统。完整前后对照见 `examples/english.md`（Example 6）。README 与产品文案的禁词及叙事规则以 `~/.claude/rules/writing-tone.md` 的 User-facing Docs 区为准。

## De-AI in academic LaTeX (applies across all workflows)

De-AI is not a separate task: pattern removal runs inside every workflow above. Catalogs: `references/patterns-english.md` (read its usage criteria first) + `references/paper-voice-contract.md` (Categories 1-4 and 7 are the primary targets). The real de-AI target in academic LaTeX is syntactic over-elaboration: participial analytical tails (", indicating/suggesting that...") and abstract nominal subjects (see `paper-voice-contract.md` Category 7).

### Academic Safety Guard (强制规则)

在学术论文链路中做 de-AI / 润色时：

1. **禁止新增事实**：不添加任何原文未包含的研究、统计数据或引用。
2. **禁止第一人称**：不使用 I/we（除非原文已有且符合会议惯例）。
3. **禁止幽默/个性化**：不加入 humor、edge、personality（general text 的 voice 建议在学术链路整体失效）。
4. **编辑范围**：删除 AI 模式痕迹、改善句式节奏、去除模板化表达；删除仍受信息守恒约束，只删零信息模式，承载论点或证据的句子改句形不删内容。
5. **Voice 边界**：参照 claim calibration 规则与 `personal-style-profile.md`。

### Preservation Rules (non-negotiable)

1. **Citations**: every `\cite{...}` stays in place, attached to its original semantic context; never move a citation to a different claim.
2. **Non-prose environments**: do not modify anything inside math, float, algorithm, or code environments (`equation`, `align`, `figure`, `table`, `algorithm`, `lstlisting`, ...). Prose environments (`abstract`, theorem statement wording, list items) are body text and follow normal editing rules.
3. **LaTeX commands**: do not alter `\ref{}`, `\label{}`, `\cref{}`, `\autoref{}`, `\eqref{}`, or structural commands.
4. **Figure/table references**: do not alter cross-references. During de-AI passes keep each caption's meaning and target intact; rewriting a caption is its own task and follows `figures-and-tables.md` caption standards.
5. **Technical terminology**: do not expand abbreviations or change established terminology.

### Rhythm refinement

- Sentence length variation: mix short (5-12 words), medium (13-22), and long (23-35) sentences; avoid 3+ consecutive sentences of similar length.
- Paragraph length variation: short (2-3 sentences) for emphasis or transitions, medium (4-5) for standard exposition, long (6-8) for complex arguments.
- Filler removal: "in order to" → "to"; "due to the fact that" → "because"; "in the context of" → "in"/"for"; "a large number of" → "many"; "at the present time" → "now"; "for the purpose of" → "to". "It is worth noting that" 后接具体发现/对比/数据则保留，后接空泛 claim 则删。
- Prefer active voice; replace vague verbs ("shows", "does", "works") with concrete ones; avoid repeated sentence openings across adjacent sentences; replace hedge stacks ("may potentially") with one qualifier.

### Transition calibration

Sentence-initial connectives (However, Moreover, Thus, Further, Finally) are NOT an AI marker in academic prose; accepted native-written papers use them densely. Do not strip them by default. Remove only:

- "As mentioned above," / "As previously discussed," (pure back-reference filler)
- "It should be noted that" / "In this regard," (meta-phrases)
- A connective restating a relationship the sentence structure already makes explicit

### Per-section processing + verification

Process one section at a time: read fully → identify all `\cite{...}` and their claims → apply catalogs + rhythm + filler removal → verify before finalizing:

- [ ] Citation count unchanged; each citation still supports its original claim
- [ ] No 3+ consecutive sentences of similar length; paragraph lengths vary
- [ ] Back-reference filler and meta-phrases eliminated (normal connectives kept)
- [ ] Technical accuracy preserved; no non-prose environments or cross-references modified
- [ ] Information conservation: nothing the reader needed to know was deleted

### Short-Text Quick Pass

当输入为一小段英文 LaTeX（非全文）且用户要求"去 AI 味"时，自动启用。输出格式（零多余文本）：

- Part 1 [LaTeX]：重写后代码（已足够好则保留原文）
- Part 2 [Translation]：中文直译
- Part 3 [Modification Log]：修改说明或"[检测通过] 原文表达地道自然，无明显 AI 味，建议保留。"

额外约束：严禁列表格式，转为连贯段落；移除机械连接词（back-reference 填充与 meta 短语，句首正常连接词不算）；禁用加粗/斜体强调；保持 LaTeX 纯净，保留数学公式；宁缺毋滥，已自然的文本直接判定"检测通过"；高频 AI 词判定参照 `patterns-english.md` 的高频词表（触发器不是判决书）。

## Key references (quick links)

### Style and structure
- `references/personal-style-profile.md` (个人默认写作风格；所有起草/改写默认按它执行)
- `references/related-work-writing-notes.md` (相关工作写作学习笔记；写新论文前先读对应条目并模仿)
- `references/narrative-flow-playbook.md` (承重因果链 + Bridge test)
- `references/icml2026-writing-requirements.md` (optional: ICML-flavored constraints; treat as reference, not strict policy)
- `references/paper-voice-contract.md` (generator voice anti-patterns shared across skills)

### Section playbooks
- `references/abstract-playbook.md`
- `references/introduction-playbook.md`
- `references/related-work-playbook.md`
- `references/method-playbook.md`
- `references/experiments-playbook.md`
- `references/conclusion-impact-playbook.md`
- `references/appendix-playbook.md` (appendix organization)

### LaTeX and formatting
- `references/equations-and-notation.md`
- `references/definitions-theorems-playbook.md` (formal environments)
- `references/figures-and-tables.md`
- `references/latex-project-structure.md`
- `references/citation-and-bibtex.md`

### Templates and assets
- `assets/latex-snippets.tex` (copy/paste LaTeX patterns)
- `assets/macro-template.tex` (macro.tex starter template)
- `assets/claim-evidence-map.md`
- `assets/icml-8page-outline.md`
