# Citation + BibTeX norms (ICML-style, English)

This guide focuses on **writing-facing** citation practice (how to cite in the text, and how to keep the `.bib` clean).
Formatting enforcement is handled by ICML style files + `natbib`, but reviewers will still judge citation *quality*.

## 1) In-text citation norms (ICML / author–year)

ICML uses **author–year** citations via `natbib`.

Use the right command for the rhetorical role:

- Narrative citation (author is the subject of the sentence):
  - `\citet{key}` → “Author (Year) shows …”
- Parenthetical citation (supporting evidence):
  - `\citep{key}` → “... as shown previously (Author, Year).”
- Use `\citeauthor{key}` or `\citeyear{key}` only when necessary.

### Multiple citations

Prefer **2–5 citations** that represent the landscape.
Avoid citation dumps unless the sentence truly summarizes a large body of work.

Ordering:

- If you list multiple citations, order them in a consistent way.
  - A common and reviewer-friendly choice is **chronological** for “history” claims.
  - For “category” claims, group by **theme** and order within each theme.

Do not rely on “more citations” to make a claim true; make the claim precise.

## 2) What to cite (especially in Abstract and Introduction)

### Abstract

Default: **no citations** in the abstract.

Only cite in the abstract if absolutely necessary, e.g.:
- A key benchmark/dataset definition is not common knowledge.
- You must disambiguate a named method that would confuse readers.

If you cite in the abstract, keep it to **1–2 citations** and avoid “citation-only” sentences.

### Introduction

Introduction citations should do three jobs:

1. Establish state-of-the-art (closest work).
2. Support the “gap” (what is missing).
3. Support the “why it matters” (consequences of the gap).

Best practice:
- Cite **the closest work explicitly** and compare directly.
- Cite surveys sparingly; use them to support broad statements, not novelty.

## 3) Bibliography hygiene (what reviewers notice)

Even if the style file formats the references, reviewers still notice:

- Missing venue/journal information
- Incomplete page numbers
- “arXiv preprint” used when the work is already published
- Broken URLs or vague “available at …”
- Wrong author names or inconsistent capitalization

### Protect capitalization in BibTeX titles

BibTeX may lowercase titles. Protect proper nouns and acronyms:

- Bad: `title={Benchmarking {LLM} generated code}` (LLM may become “llm” in some styles)
- Better: `title={Benchmarking {LLM}-Generated Code}`

Also protect “ICML”, “NeurIPS”, model names, dataset names, etc.

### Prefer complete entries

For conference papers:
- `@inproceedings{...}` with `booktitle`, `year`, and `pages` if available.

For arXiv:
- Prefer including the arXiv ID explicitly.
  - Many styles accept either:
    - `journal={arXiv preprint arXiv:XXXX.XXXXX}`
    - or `archivePrefix={arXiv}, eprint={XXXX.XXXXX}, primaryClass={...}`

For datasets/benchmarks:
- Cite the dataset paper (if it exists), not only a URL.

## 4) “First / novel / state-of-the-art” claims (citation-sensitive)

These claims are high-risk in Abstract and Introduction.

Prefer:
- “To our knowledge, …” **with at least one** strong related-work citation nearby.
- Or: “We are the first to evaluate X under Y and Z constraints …” (narrow, testable).

Avoid:
- “We are the first …” with no citation context.
- “Novel” as an adjective without specifying *what* is novel.
- “Significant improvement” unless you report statistics or clear margins.

## 5) Quick checklist (before submission)

- [ ] Every big claim in the Introduction has at least one supporting citation, unless it is common knowledge.
- [ ] The closest prior work is cited and compared directly.
- [ ] `.bib` titles protect acronyms and proper nouns with braces.
- [ ] References are complete (venue/journal, year, pages/doi/url when appropriate).

