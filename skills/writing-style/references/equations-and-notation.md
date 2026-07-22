# Equations and notation playbook (ICML-style, LaTeX)

## 1) Notation discipline

- Define symbols before use; do not make readers search.
- Prefer a small set of symbols used consistently throughout.
- Use `\mathcal{}` for sets, `\mathbf{}` for vectors, `\operatorname{}` for multi-letter operators.
- Use `\text{}` for textual subscripts: `S_\text{eval}`.

## 2) Equation writing patterns

High-quality patterns observed:

- Use `\triangleq` when defining a metric.
- Provide a brief sentence before and after an equation:
  - before: what it represents
  - after: what each symbol means
- Label important equations: `\label{eq:...}` and refer with `Eq.~\eqref{eq:...}` or `\cref{eq:...}`.

## 3) When to move math to the appendix

Move to appendix if:

- The derivation is longer than ~8–12 lines.
- The result is not needed to understand the algorithm.
- The proof is standard and the key intuition can be summarized.

Keep in main text if:

- It defines the core method.
- It is required to understand the experimental claim.

## 4) Math typesetting

- `\ell` instead of `l` to avoid confusion with digit `1`.
- Multi-letter operators: `\operatorname{softmax}`, `\textrm{proj}`, `\textrm{enc}` — never bare italic.
- Use built-in commands when available: `\arg\max`, `\min`, `\sin`, `\tanh`, `\exp`, `\det`, `\inf`.
- Auto-scaling brackets: `\left( \right)`, `\left\{ \middle| \right\}` — not bare `()`.
- Multi-line equations: `align` with `&=` for alignment; avoid `gather` when alignment helps readability.
- Equations are part of the sentence: end with `,` or `.` as grammar requires.
- Only number equations that are `\ref`'d or `\eqref`'d; use `\nonumber` or `equation*` for the rest.

## 5) LaTeX generation conventions (auto-apply when writing LaTeX)

- Formal register: `do not` / `cannot` / `we have` — never `don't` / `can't` / `we've`.
- Latin abbreviations with trailing comma: `e.g.,` / `i.e.,` / `et al.`
- Non-breaking space before references: `Figure~\ref{}`, `Table~\ref{}`, `Section~\ref{}`, `Eq.~\eqref{}`.
- Non-breaking space before citations when inline: `BERT~\citep{bert}`.
- `\citep{}` for parenthetical citations; `\citet{}` when the author is a grammatical subject/object. Default to `\citep` unless the citation is a sentence constituent.
- LaTeX quotes: `` ` ` `` and `''` — never straight `"..."`.
- Avoid excessive pronoun `it` / `they` when referring to models or methods; use the abbreviated name directly (clearer, costs few characters).

## 6) LaTeX snippets

See `assets/latex-snippets.tex` for equation + definition templates consistent with the extracted style.

