# Appendix Playbook (ICML-style)

This playbook provides guidance on organizing and writing appendix content for ICML papers.

## When to Use Appendix

Move content to appendix when:
- Derivations exceed ~8-12 lines
- Details are not essential for understanding the main argument
- Space is needed in the 8-page main text
- Supplementary experiments support but don't drive the narrative

Keep in main text when:
- Content defines the core method
- Content is required to understand experimental claims
- Reviewers need it to evaluate novelty

## Recommended Appendix Structure

A proven structure:

```
Appendix A: [Benchmark/Dataset] Specification
Appendix B: Experimental Details
Appendix C: Additional Experiments
Appendix D: Proofs and Derivations (if applicable)
```

## Section Templates

### A. Dataset/Benchmark Specification
- Data schema and examples
- Collection methodology
- Statistics tables
- Quality control measures

### B. Experimental Details
- Full hyperparameter tables
- Hardware and software environment
- Prompt templates (for LLM work)
- Reproducibility checklist items

### C. Additional Experiments
- Ablation studies not in main text
- Sensitivity analyses
- Per-category breakdowns
- Failure case analysis

### D. Proofs and Derivations
- Theorem proofs
- Mathematical derivations
- Complexity analysis details

## Cross-Reference Patterns

Always link appendix content from main text:

```latex
% In main text
See Appendix~\ref{app:details} for full experimental setup.
Due to space limits, we defer the proof to Appendix~\ref{app:proof}.
Table~\ref{table:full-results} in Appendix~\ref{app:experiments} shows...
```

```latex
% In appendix
\appendix
\section{Experimental Details}
\label{app:details}
```

## Formatting Notes

- Use `\appendix` command before appendix sections
- Use `\onecolumn` if wide tables are needed
- Maintain consistent style with main text
- Number figures/tables continuously or restart with A.1, B.1, etc.
