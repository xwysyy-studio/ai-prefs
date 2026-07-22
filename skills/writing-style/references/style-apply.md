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
- The stricter house rules (em-dash minimization, banned-word lists) are deliberate de-AI
  tightening beyond venue norms, not review red lines: accepted papers do use these. The rules
  stay in force anyway. Em-dashes especially: whatever their pre-AI history, AI training corpora
  have made them a default AI association, so keep them rare. Do not present house rules as
  "humans don't write this way"; present them as "we choose not to".

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

- If the user has **no draft** → Workflow A (outline + storyline).
- If the user has a **draft** → Workflow B (rewrite + strengthen narrative).
- If the user needs **LaTeX help** → Workflow C (LaTeX craft).
- If the user is close to submission → Workflow D (final polish + submission-aware self-checks).

## Workflow A — Outline + storyline

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

Reference: `references/revision-checklist.md`.
Also useful: `references/conclusion-impact-playbook.md`.

## Mentor review rubric (what I check first)

This is the high-leverage checklist I use when “reviewing as an advisor”:

1. **Spine clarity**: one-sentence thesis + 2–4 contributions, each tied to a figure/table.
2. **Abstract quality**: single paragraph; gap is explicit; includes at least one concrete number; bounded claims.
3. **Introduction arc**: context → closest work → gap → why hard → approach → contributions → (optional) results preview.
4. **Claim calibration**: avoid “the first” unless narrowly scoped; “significant” requires an adjacent number (the accepted-paper norm is adjacency, not avoidance).
5. **Evidence alignment**: every contribution is verified by experiments; no “paper-only” promises.
6. **LaTeX hygiene**: no undefined refs; tables/figures are readable; captions are self-contained.

## Key references (quick links)

### Style and structure
- `references/personal-style-profile.md` (个人默认写作风格；所有起草/改写默认按它执行)
- `references/related-work-writing-notes.md` (相关工作写作学习笔记；写新论文前先读对应条目并模仿)
- `references/narrative-flow-playbook.md` (起承转合 systematic guidance)
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
- `references/revision-checklist.md`

### Templates and assets
- `assets/latex-snippets.tex` (copy/paste LaTeX patterns)
- `assets/macro-template.tex` (macro.tex starter template)
- `assets/claim-evidence-map.md`
- `assets/icml-8page-outline.md`
- `assets/transition-phrasebank.md` (中文过渡词短语库，仅 chinese-academic 模式使用)
