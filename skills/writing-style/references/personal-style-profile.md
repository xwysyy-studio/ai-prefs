# Personal style profile（个人默认写作风格）

用户的默认论文写作风格，在论文任务需要语气校准时结合当前要求和认可样稿使用。材料来自用户已中稿的 ICML 论文及实读相关工作，以下结构与句式按其适用条件参考。更新时同时比较原稿、用户保留的内容和最终改法，确认哪些偏好能跨任务使用；领域特定的叙事方法保留在 `related-work-writing-notes.md`。

## 1) Voice and tone

- Prefer **active voice** and “we” for claims and actions: “We propose / We show / We find …”.
- Use **confident but bounded** language:
  - Strong: “Our results demonstrate …”
  - Bounded: “suggest”, “indicate”, “in our setting”, “under the following assumptions”
- Position the paper positively: state what the work studies, proposes, measures, and contributes. When comparing related work, name the prior work's concrete coverage or gap first; never seed an unraised objection or negate a possible claim about the present work.
- Use `\emph{...}` to emphasize **one key phrase**, not to decorate.
- **Explanatory flow**: use connectives such as However, Moreover, and Thus when they express an actual relationship. Phrases such as “Recall that …” or “Consider an example …” can help readers follow a technical argument when a recall or example is needed. Keep the default voice plain and direct, with the necessary explanation intact.
- An interrogative research question that names the open problem is a legitimate device (“Can we … using fully synthetic data?”); only writing-plan announcements are banned.

## 2) “Hook → gap → contributions” rhythm

An introduction in the reference ICML papers performs these functions. Adapt their order and space to the current argument:

1. Context: why the area matters.
2. State of the art: what exists and what it measures.
3. Gap: what is missing (one crisp sentence).
4. Why it matters: consequences of the gap (often with a motivating example).
5. Challenges/limitations: a short bullet list with bolded heads.
6. Contributions: explicit and connected to the problem and evidence; use numbering and titles when they help the reader.

## 3) Contribution blocks (high signal)

One pattern in the reference papers is `\paragraph{Contribution #i: <short title>.}` followed by a few sentences that cover:

- what it is (artifact/method/dataset/benchmark);
- what is special about it (why non-trivial);
- what it enables (evaluation / analysis / new capability);
- optionally, a concrete scale number (tasks, datasets, models, parameters).

Use it when it helps reviewers locate novelty; the number and order of sentences follow the contribution.

## 4) Abstract structure

The abstract is:

- Single paragraph
- Sentences that each do one job; their length follows the content
- Built around one load-bearing sentence, the line that changes the reader's understanding; the arc follows the paper's story (see `abstract-playbook.md`, English Abstract section)
- The usual supporting jobs: context, brief prior-work summary, gap statement, what you introduce, what’s inside the artifact (scale + properties), how you evaluate, main conclusion (qualitative and/or quantitative)

## 5) Experiments: “primary findings” + bullets

Evaluation sections often become long. One pattern from the reference papers, useful when the findings are parallel:

- A short setup
- Then “Our primary findings suggest that …”
- Then a bullet list of findings, each with:
  - A crisp claim
  - A concrete comparison/example
  - Optional: a caveat

It is reviewer-friendly and compresses well under an 8-page limit.

**Finding headers (absorbed from multiple accepted papers).** Each finding may be fronted as a standalone one-clause claim usable as a header: italic thesis at bullet start (“\emph{Graph is the dominant bottleneck.}”), bold run-in paragraph opener, boxed/numbered finding, or even a subsection title. Name the finding, don't brand it: “Task Diversity Matters More than Solution Diversity” states a result; “the Good-gets-Better Principle” is a marketing label.

**Result narration shape: number, instance, then a fresh sentence.**

- State the number, then a named concrete instance, then stop: “One exception is Llama-3.1-8B, which has the time-only dual@10 of 0.244, slightly smaller than the space-only dual@10 of 0.248.”
- A separate plain sentence often helps distinguish an observation from its interpretation. Preserve a clear attached clause when it already serves that relationship; see `paper-voice-contract.md` Category 7. Choose “It demonstrates that …”, “This may be because …”, or “We believe that …” only when the source supports that particular evidence relationship.
- Use “significant” in its statistical sense only when a test supports it; otherwise report the observed difference and its conditions, following the academic-writing evidence rules.

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
- “We use the term X to denote …” (positive terminology definition)
- “X acts as a feasibility constraint; the scoring metric measures Y” (positive separation of roles)

Avoid overusing any single phrase; treat these as patterns.
