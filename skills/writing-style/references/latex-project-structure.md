# LaTeX project structure playbook (ICML-style)

This playbook summarizes a clean LaTeX structure for ICML-style projects.

## Recommended layout

- `main.tex`: preamble + title/author controls + `\input{macro}` + `\input{section-files}`
- `macro.tex`: all `\newcommand`, `\DeclareMathOperator`, notation shortcuts
- `tables/*.tex`: large `tabular` blocks only (no `table` environment)
- `imgs/`: figures (PDF/PNG)
- `refs.bib`: BibTeX database

## Why this helps

- Makes reviews easier (each section is readable in isolation).
- Makes collaboration easier (less merge conflict).
- Makes tables maintainable (especially wide `table*`).

## Table handling pattern

- In the paper: create the `table*` wrapper with caption/label and `\resizebox`.
- Put the `tabular` in `tables/<name>.tex`.

## Numeric macros: single source of truth

Define every reported result number once (in `macro.tex` or a dedicated `results.tex`), e.g. `\newcommand{\nBOursFC}{10.62}`, and compute deltas with `\FPeval` where possible. Abstract, intro, and tables then cannot drift when results update.

## Cross-references

Use a consistent pattern:

- `Figure~\ref{fig:...}` and `Table~\ref{tab:...}`
- `Section~\ref{sec:...}`
- `Appendix~\ref{app:...}`

`cleveref` can help, but consistency matters more than the tool.

