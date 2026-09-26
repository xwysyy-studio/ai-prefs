# Paper Voice Contract

A shared contract defining generator voice anti-patterns and remediation strategies for academic writing. Referenced by: `writing-style`, `paper-review`.

## Purpose

Ensure consistent, human-sounding academic prose by identifying and eliminating common AI/generator voice patterns. This contract provides a shared vocabulary and repair strategies across writing and editing skills.

## Generator Voice Anti-Patterns

### Category 1: Planner Talk (meta-commentary that describes intent instead of executing)

| Anti-Pattern | Example (BAD) | Fix (GOOD) |
|---|---|---|
| Announcing intent | "In this section, we will discuss the methodology we employ to address this challenge." | Start with the method actually described in the supplied material; remove the announcement. |
| Meta-guidance | "It is important to note that..." / "It should be emphasized that..." | Delete the meta-phrase; let the content speak for itself. |
| Roadmap filler | "The remainder of this paper is organized as follows. Section 2 presents... Section 3 describes..." | Use a 1-sentence roadmap only if non-obvious; otherwise delete. |
| Self-narration | "We now turn our attention to..." / "Having established X, we proceed to Y." | Start directly with the content of Y. |

> Carve-out: an interrogative research question that names the actual open problem ("Can we bypass the reliance on real-world data and elevate models to expert-level reasoning using fully synthetic data?") is NOT planner talk and is a common device in accepted papers. Only sentences announcing the writing plan are.

### Category 2: Template Stems (formulaic sentence openings)

| Anti-Pattern | Example (BAD) | Fix (GOOD) |
|---|---|---|
| Hollow openers | "In recent years, X has attracted significant attention..." | State the specific finding or gap directly. |
| Generic importance | "X plays a crucial role in..." / "X is of paramount importance..." | State the actual role supported by the material; use a measured effect only when its number and conditions are supplied. |
| False novelty | "To the best of our knowledge, this is the first..." | State the contribution and its verified comparison scope. Retain a priority claim only when the evidence supports it. |
| AI vocabulary | "delve into", "landscape", "tapestry", "paradigm shift", "nuanced", "multifaceted", "underscores" | Replace with precise, concrete terms. |

### Category 3: Hedge Stacking (excessive qualification)

| Anti-Pattern | Example (BAD) | Fix (GOOD) |
|---|---|---|
| Triple hedge | "It could potentially perhaps improve..." | Choose one appropriate hedge or state directly. |
| Weasel attribution | "Some researchers have suggested that..." | Identify the authors from the actual source while retaining the strength of "suggested"; flag the missing attribution if the source does not identify them. |
| Vague improvement | "Our method achieves better results." | Identify the metric, comparison, and result in the supplied evidence; retain the current claim or flag the missing detail if that evidence is unavailable. |

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
| Scope inflation | "This work has broad implications for all of machine learning." | State the evaluated models, tasks, or settings supplied by the evidence. Do not invent a narrower setting. |
| Unbounded promise | "This opens up exciting new avenues for future research." | Either specify the avenue or delete. |

### Category 7: Syntactic Over-Elaboration (academic camouflage)

Calibration source: the user's own two accepted ML-benchmark papers, one written natively (3 participial analytical tails, 0 uses of "reveal") and one AI-assisted (11 and 12). These observations help locate repetitive expression in similar prose; they do not establish authorship or a permitted frequency. Read what each clause contributes, whether its relation to the result is supported, and whether the repeated construction makes the passage harder to follow.

| Anti-Pattern | Example (BAD) | Fix (GOOD) |
|---|---|---|
| Participial analytical tail | "...rises from 0.367 in pass@1 to 0.597 in pass@5, indicating that additional attempts often recover a correct solution by exploring alternative approaches and interaction strategies." | If separating the observation and interpretation clarifies their relationship, end the first sentence at the result and give the supported interpretation in a plain sentence. Preserve its uncertainty and basis; the proposed mechanism needs support in the source. |
| Abstract nominal subject | "This long-horizon bookkeeping amplifies small update mistakes over many rounds." | "Small update mistakes become more consequential over many rounds of bookkeeping." |
| Stacked infinitival/prepositional tails | "This reflects the need to acquire information from an initially unrevealed structure under strict query budgets, and to track state under partial observability." | "The task requires discovering information about an initially hidden structure within a strict query budget. It also requires tracking state from partial observations." |
| Pseudo-analytical verb tic | "reveal(s)" as the default verb for every result | State what was measured or observed, using the verb that fits that relationship. Repetition can remain when accurate; do not rotate verbs as interchangeable style variants. |

Check whether the clause adds a specific supported interpretation. A separate sentence can make that interpretation easier to follow; a clear attached clause can remain. Phrases such as "It demonstrates that ...", "This may be because ...", and "We believe that ..." express different evidence relationships and are not interchangeable style variants.

### Category 8: Defensive Claim Posture (unnecessary self-justification)

This pattern adds self-justification that does not help the reader understand the subject, assess a relevant claim, or answer the task's question. It includes both author-stance wrappers and factual, impersonal accounts of what the text has not established. Check what the reader would misunderstand without the sentence; a relevant need may arise from the question or context without a separately written claim. An author's interpretation, hypothesis, uncertainty, or disagreement carries meaning and is not a removable wrapper merely because it uses first person.

| Anti-Pattern | Example (BAD) | Fix (GOOD) |
|---|---|---|
| Claim denial | "We do not claim that the method is generally effective." | State the evaluated scope and result directly. |
| Self-limiting contribution | "Our contribution is limited to showing a 6-point gain under a 2,000-token budget." | "Under a 2,000-token budget, the method achieves a 6-point gain." Specify the metric when it is supplied by the context. |
| Scope narration | "We confine our effectiveness claim to two of the three datasets." | State the observed result on those datasets using the supplied metric and comparison. Preserve what the third dataset establishes and the original strength of the effectiveness claim. |
| Defensive contrast | "The method is not generally superior; rather, it only helps in low-budget settings." | "Across the evaluated settings, [state the observed overall result]. Under low-budget settings, the method improves [metric] by [value]." |
| Unrelated missing comparison | A note explaining system costs ends with "This note does not compare training stability." | Omit the sentence when stability is outside the reader's question and the passage makes no stability claim. If the reader is asking about stability, directly explain that the supplied evidence does not answer it. |

Before repairing the prose, determine whether the passage carries an observed failure, negative result, counterexample, or an author's judgment about the evidence. Preserve real counterevidence as a direct factual result and use it to narrow the claim or revisit the paper story. Preserve the distinction between that result and its interpretation.

Repair procedure: identify the observation, its source and conditions, and any interpretation or uncertainty expressed in the original. Check which claim or reader need the explanation serves. Remove an unrelated self-protective aside when the claims, evidence, and author judgment needed by the reader remain intact; making the aside more objective is not a repair. For a relevant boundary, write the supported result directly and keep the interpretation at its original strength. Remove a stance phrase only when the remaining sentence preserves who is making the judgment and what the evidence establishes. If a direct rewrite would turn a belief into a finding or a possible explanation into a mechanism, retain or rephrase the epistemic qualification. Conditions such as "on two of three datasets" and "under a 2,000-token budget" remain attached to the proposition. When an unsupported inference is the problem, correct that inference within the authorized scope instead of leaving it in place with a disclaimer.

A direct denial may answer an objection in a review or cited source, clarify an ambiguity in the passage, or address the reader's actual question. Its value depends on that use, not on first-person wording or whether it appears in an ordinary manuscript or a rebuttal.

## Diagnosis Protocol

When reviewing text for voice contamination:

Read the passage in context and identify the concrete problem in meaning,
clarity, unsupported framing, or repetition. For an audit, report its location,
quoted wording, and relevant category, such as `[PLANNER_TALK]`,
`[TEMPLATE_STEM]`, `[HEDGE_STACK]`, `[SYMMETRY]`, `[CITATION_CONTAM]`,
`[GRANDIOSE]`, `[SYNTAX_ORNATE]`, or `[DEFENSIVE_POSTURE]`.

Choose repair scope from the problem's effect on the reader and the authorized
operation. A wrong citation or unsupported claim matters even once; repeated
wording matters when it obscures the argument or makes the prose mechanical.
Keep valid terminology and useful variation. Remove empty wording and
irrelevant self-justification under Category 8's criteria; preserve the facts,
reasoning, conditions, and evidence strength needed for the passage's purpose.
Narrowly specified edits leave unrelated text intact. In audit-only tasks,
report without editing.

## Integration Points

### writing-style（学术写作）
- Apply this contract to expression problems within the drafting, polishing, and restructuring tasks defined in `references/style-apply.md`
- Use the categories relevant to the actual passage; citation integrity and evidence strength remain required in every task
- Use the diagnosis protocol to locate expression problems; during polishing preserve citation-to-claim relationships, cross-references, and non-prose environments. During authorized restructuring, citations move with the claims they support (see style-apply.md Preservation Rules).

## Verify the revised passage

Compare the revision with the source and the requested task. Citations must
support their attached claims; conditions, negative findings, author judgments,
and uncertainty must remain accurate. Compare observations and interpretations
separately so that removing a wrapper does not strengthen either. Position the
work through factual scope; qualifications and denials must serve an actual
claim, ambiguity, or reader question. Read the
argument for complete relationships and useful explanation. Counts and
category labels help locate passages; the actual content and readability
determine whether another edit is needed.
