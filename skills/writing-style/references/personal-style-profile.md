# Personal style profile（个人默认写作风格）

用户的默认写作风格，起草和改写一律按它执行，除非用户另有指定。谱系：从用户自己已中稿的 ICML 论文提炼，并持续吸收相关工作中验证过的措辞与手法（吸收入口见 `related-work-writing-notes.md`：写作时模仿相关工作，完稿后把值得保留的蒸馏到这里）。

## 1) Voice and tone

- Prefer **active voice** and “we” for claims and actions: “We propose / We show / We find …”.
- Use **confident but bounded** language:
  - Strong: “Our results demonstrate …”
  - Bounded: “suggest”, “indicate”, “in our setting”, “under the following assumptions”
- Use `\emph{...}` to emphasize **one key phrase**, not to decorate.
- **Lecture-style flow**: sentence-initial connectives used freely and densely (However / Moreover / Further / Thus / Instead / Finally), plus conversational moves: “A natural next question is …”, “Note that …”, “Recall that …”, “We remark that …”, “Consider an example …”. This chattiness is the house voice; do not strip it toward cold nominalized prose.
- An interrogative research question that names the open problem is a legitimate device (“Can we … using fully synthetic data?”); only writing-plan announcements are banned.

## 2) “Hook → gap → contributions” rhythm

The intro follows a strong ICML rhythm:

1. Context: why the area matters.
2. State of the art: what exists and what it measures.
3. Gap: what is missing (one crisp sentence).
4. Why it matters: consequences of the gap (often with a motivating example).
5. Challenges/limitations: a short bullet list with bolded heads.
6. Contributions: explicit, numbered, titled, and aligned to the challenges.

## 3) Contribution blocks (high signal)

A distinctive pattern is using `\paragraph{Contribution #i: <short title>.}` followed by 2–4 sentences:

- Sentence 1: what it is (artifact/method/dataset/benchmark).
- Sentence 2: what is special about it (why non-trivial).
- Sentence 3: what it enables (evaluation / analysis / new capability).
- Optional: a concrete scale number (tasks, datasets, models, parameters).

This structure makes it easy for reviewers to locate novelty.

## 4) Abstract structure

The abstract is:

- Single paragraph
- Many short sentences (each “does one job”)
- Contains:
  - Context
  - Prior work summary (very brief)
  - Gap statement
  - What you introduce
  - What’s inside the artifact (scale + properties)
  - How you evaluate
  - Main conclusion (qualitative and/or quantitative)

## 5) Experiments: “primary findings” + bullets

Evaluation sections often become long. The house pattern:

- A short setup
- Then “Our primary findings suggest that …”
- Then a bullet list of findings, each with:
  - A crisp claim
  - A concrete comparison/example
  - Optional: a caveat

This is reviewer-friendly and compresses well into 8 pages.

**Finding headers (absorbed from multiple accepted papers).** Each finding may be fronted as a standalone one-clause claim usable as a header: italic thesis at bullet start (“\emph{Graph is the dominant bottleneck.}”), bold run-in paragraph opener, boxed/numbered finding, or even a subsection title. Name the finding, don't brand it: “Task Diversity Matters More than Solution Diversity” states a result; “the Good-gets-Better Principle” is a marketing label.

**Result narration shape: number, instance, then a fresh sentence.**

- State the number, then a named concrete instance, then stop: “One exception is Llama-3.1-8B, which has the time-only dual@10 of 0.244, slightly smaller than the space-only dual@10 of 0.248.”
- If interpretation is needed, start a NEW short plain sentence: “It demonstrates that …”, “This may be because …”, “We believe that …”. Never hang the interpretation off the data sentence as a participial tail (“…, indicating that …”); see `paper-voice-contract.md` Category 7.
- “significant” is fine only with a number adjacent to it.

## 6) LaTeX conventions

Common conventions used consistently:

- `Figure~\ref{...}` / `Table~\ref{...}` (with non-breaking space `~`)
- `\label{...}` and `\ref{...}` everywhere
- Modular files: `\input{1-introduction}`, `\input{tables/main_results}`
- Tables use `booktabs` (`\toprule`, `\midrule`, `\bottomrule`)
- Wide artifacts use `figure*` / `table*` and `\resizebox{0.98\textwidth}{!}{...}`

## 7) Phrases worth reusing (generic)

- “To fill this gap, we …”
- “Our primary findings suggest that …”
- “We observe that …”
- “An exception is …, which …” (honest counterexample, then stop)
- “Due to the page limit, we defer … to the appendix.”

Absorbed from related work (validated in accepted papers):

- “This leaves a clear void for …” (related-work gap closer)
- “We revisit this claim …” (re-evaluation framing)
- “This setup is intentionally more challenging, yet more aligned with real-world practices” (turn a design cost into a virtue)
- “We use the term X rather than Y because …” (terminology justification, a group habit)
- “… acts as a feasibility constraint rather than a component of the scoring metric” (one sentence defining what is NOT measured)

Avoid overusing any single phrase; treat these as patterns.

