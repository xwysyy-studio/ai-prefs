# Definitions and Theorems Playbook (ICML-style)

This playbook provides guidance on using formal mathematical environments.

## When to Use Formal Environments

Use `\begin{definition}...\end{definition}` when:
- Introducing a novel concept central to your contribution
- The definition will be referenced multiple times
- Precision is critical for understanding

Use inline definitions when:
- The concept is standard or well-known
- It's a minor supporting concept
- Space is limited

## Environment Types

Standard preamble:

```latex
\theoremstyle{plain}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{corollary}[theorem]{Corollary}

\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{assumption}[theorem]{Assumption}
\newtheorem{remark}[theorem]{Remark}
```

## Usage Patterns

### Definition Pattern

```latex
\begin{definition}\label{def:pareto-optimum}
A code (or an algorithm) is \emph{Pareto optimal} in terms of
efficiency when it cannot make time efficiency better off
without making space efficiency worse off, and vice versa.
\end{definition}
```

### Referencing

```latex
By Definition~\ref{def:pareto-optimum}, all three algorithms
are Pareto optimal.
```

## Writing Guidelines

1. **Be precise:** Every term should be unambiguous
2. **Be minimal:** Include only necessary conditions
3. **Use emphasis:** `\emph{key term}` for the defined term
4. **Add context:** Follow with an example or intuition

## Placement

- Place definitions before first use
- Group related definitions together
- Move complex proofs to appendix
