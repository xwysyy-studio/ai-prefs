# Paper Voice Contract

A shared contract defining generator voice anti-patterns and remediation strategies for academic writing. Referenced by: `writing-style`, `paper-review`.

## Purpose

Ensure consistent, human-sounding academic prose by identifying and eliminating common AI/generator voice patterns. This contract provides a shared vocabulary and repair strategies across writing and editing skills.

## Generator Voice Anti-Patterns

### Category 1: Planner Talk (meta-commentary that describes intent instead of executing)

| Anti-Pattern | Example (BAD) | Fix (GOOD) |
|---|---|---|
| Announcing intent | "In this section, we will discuss the methodology we employ to address this challenge." | "We formulate the problem as a constrained optimization over..." |
| Meta-guidance | "It is important to note that..." / "It should be emphasized that..." | Delete the meta-phrase; let the content speak for itself. |
| Roadmap filler | "The remainder of this paper is organized as follows. Section 2 presents... Section 3 describes..." | Use a 1-sentence roadmap only if non-obvious; otherwise delete. |
| Self-narration | "We now turn our attention to..." / "Having established X, we proceed to Y." | Start directly with the content of Y. |

> Carve-out: an interrogative research question that names the actual open problem ("Can we bypass the reliance on real-world data and elevate models to expert-level reasoning using fully synthetic data?") is NOT planner talk and is a common device in accepted papers. Only sentences announcing the writing plan are.

### Category 2: Template Stems (formulaic sentence openings)

| Anti-Pattern | Example (BAD) | Fix (GOOD) |
|---|---|---|
| Hollow openers | "In recent years, X has attracted significant attention..." | State the specific finding or gap directly. |
| Generic importance | "X plays a crucial role in..." / "X is of paramount importance..." | Quantify or specify: "X reduces latency by 40% in..." |
| False novelty | "To the best of our knowledge, this is the first..." | Scope precisely: "Among methods tested on benchmark Y, ours is the first to..." |
| AI vocabulary | "delve into", "landscape", "tapestry", "paradigm shift", "nuanced", "multifaceted", "underscores" | Replace with precise, concrete terms. |

### Category 3: Hedge Stacking (excessive qualification)

| Anti-Pattern | Example (BAD) | Fix (GOOD) |
|---|---|---|
| Triple hedge | "It could potentially perhaps improve..." | Choose one appropriate hedge or state directly. |
| Weasel attribution | "Some researchers have suggested that..." | Cite specifically: "Chen et al. (2024) showed that..." |
| Vague improvement | "Our method achieves better results." | "Our method improves F1 by 3.2 points (Table 2)." |

### Category 4: Symmetry Addiction (forced parallelism and balance)

| Anti-Pattern | Example (BAD) | Fix (GOOD) |
|---|---|---|
| Rule of three | "Our approach is simple, effective, and scalable." | Keep only if all three are independently demonstrated. |
| Forced contrast | "While X excels at A, it struggles with B; conversely, Y excels at B but struggles with A." | State the actual tradeoff with evidence. |
| Balanced listing | "The advantages include A, B, and C. The disadvantages include D, E, and F." | Prioritize by impact; not every point needs a counterpoint. |

### Category 5: Citation Contamination

| Anti-Pattern | Example (BAD) | Fix (GOOD) |
|---|---|---|
| Citation dump | "Many works have studied this problem [1-15]." | Group by approach: "Encoder methods [1,3,7] vs. decoder methods [2,5,9]..." |
| Ghost citation | "As shown by Smith et al., X is true." (no actual cite key) | Add \cite{} or mark [CITATION NEEDED]. |
| Memory citation | BibTeX entry generated from memory | Fetch programmatically via DOI/Semantic Scholar. |

### Category 6: Grandiose Framing

| Anti-Pattern | Example (BAD) | Fix (GOOD) |
|---|---|---|
| Overclaiming | "revolutionizes", "groundbreaking", "transformative" | Use calibrated language: "improves", "addresses", "reduces" |
| Scope inflation | "This work has broad implications for all of machine learning." | "This result applies to autoregressive models on text generation tasks." |
| Unbounded promise | "This opens up exciting new avenues for future research." | Either specify the avenue or delete. |

### Category 7: Syntactic Over-Elaboration (academic camouflage)

When the vocabulary bans above are enforced, generator residue migrates into syntax: constructions that read as "analytical" but are statistical filler in grammatical form. Calibration source: the user's own two accepted ML-benchmark papers, one written natively (3 participial analytical tails, 0 uses of "reveal") and one AI-assisted (11 and 12). The frequency rule below is a heuristic calibrated on ML/CS academic prose, not a universal law; in other registers, judge by ear. Heuristic: one ", suggesting that ..." per section is normal academic hedging; three or more clustered is a rewrite signal.

| Anti-Pattern | Example (BAD) | Fix (GOOD) |
|---|---|---|
| Participial analytical tail | "...rises from 0.367 in pass@1 to 0.597 in pass@5, indicating that additional attempts often recover a correct solution by exploring alternative approaches and interaction strategies." | End the sentence at the number or named instance. If interpretation is needed, start a NEW plain sentence: "This may be because additional attempts explore alternative interaction strategies." |
| Abstract nominal subject | "This long-horizon bookkeeping amplifies small update mistakes over many rounds." | Concrete subject + verb: "The solver must update its state after every reply, so small mistakes compound over rounds." |
| Stacked infinitival/prepositional tails | "This reflects the need to acquire information from an initially unrevealed structure under strict query budgets, and to track state under partial observability." | Split into short clauses: "Graph tasks hide the structure. The model must query it under a tight budget and track what it learns." |
| Pseudo-analytical verb tic | "reveal(s)" as the default verb for every result | Rotate plain verbs (shows, gives, yields) or state the finding directly. |

The aloud test: if the tail could attach to any result in any paper of the genre, it is filler. Native glosses take the form of a fresh short sentence: "It demonstrates that ...", "This may be because ...", "We believe that ...".

## Diagnosis Protocol

When reviewing text for voice contamination:

1. **Scan** each paragraph for patterns from the 7 categories above
2. **Tag** each instance with its category (e.g., `[PLANNER_TALK]`, `[TEMPLATE_STEM]`, `[HEDGE_STACK]`, `[SYMMETRY]`, `[CITATION_CONTAM]`, `[GRANDIOSE]`, `[SYNTAX_ORNATE]`)
3. **Severity**: Count instances per 500 words
   - 0-1: Clean (no action needed)
   - 2-3: Light contamination (local fixes)
   - 4+: Heavy contamination (paragraph rewrite recommended)
4. **Fix**: Apply the corresponding fix from the table; prefer deletion over replacement

## Integration Points

### writing-style (style-apply mode)
- Apply this contract during `references/style-apply.md` Workflow B (rewrite) and Workflow D (final polish)
- Use the diagnosis protocol as a pre-check before style application

### writing-style (humanize mode)
- This contract extends the humanize mode's existing pattern detection
- Categories 1-4 and 7 are primary targets; Categories 5-6 are secondary
- In LaTeX Mode, preserve all \cite{}, \ref{}, and environments while fixing voice

## Voice Quality Gate

A paragraph passes the voice gate if:
- Zero Category 5 (Citation Contamination) instances
- Zero Category 6 (Grandiose Framing) instances for claims without evidence
- ≤1 instance from Categories 1-4 per 300 words
- No 3+ clustered Category 7 instances in one section (isolated instances are acceptable academic hedging)
- No consecutive sentences starting with the same template stem
