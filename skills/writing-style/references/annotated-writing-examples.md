# Academic passages and their roles

Use these actual manuscript excerpts to examine what each passage helps the
reader understand. They are examples of writing functions, not fixed templates
or independent validation of the papers' claims. Use the current project's
evidence when drafting its prose.

## Introducing the benchmark and its finding

Source: TESTEVAL, acl_latex.tex, abstract, in
$HOME/Code/CP-Survey/papers/039_TESTEVAL/latex/.
The excerpt expands the source's method and platform macros for readability.

> We collect 210 Python programs from an online programming platform, LeetCode, and design three different tasks: overall coverage, targeted line/branch coverage, and targeted path coverage. We further evaluate 17 popular LLMs, including both commercial and open-source ones, on TESTEVAL. We find that generating test cases to cover specific program lines/branches/paths is still challenging for current LLMs, indicating a lack of ability to comprehend program logic and execution paths.

The first sentence identifies the material and the questions the benchmark
tests. The second gives the evaluation scope. The third states the authors'
finding and interpretation. When revising a similar passage, check whether
the result supports its interpretation and retain the conditions needed to
understand it. The number of tasks and sentences follows this study.

## Explaining why a comparison is inadequate

Source: TC-Bench, iclr2026_conference.tex, Introduction, in
$HOME/Code/CP-Survey/papers/070_TC-Bench/latex/.
WC denotes a wrong code submission in this manuscript.

> Furthermore, one WC doesn't equal one kind of error.
> Indeed, the population of WCs is dominated by numerous trivial or repetitive errors, with only a few representing core, hard-to-detect faults (Figure~\ref{fig:intro} (a) ).
> A mediocre method that only identifies common errors can thus achieve a score similar to a superior method that finds rare corner cases, as the small number of critical faults gets statistically overwhelmed.
> Consequently, this diminishes the benchmark's discriminative power.

The passage connects a property of the evaluation population to a weakness
in what its score distinguishes. The example figure supplies the surrounding
evidence. The useful writing function is this relationship between the
observed setup and the question the paper addresses. Another paper should
develop the relationship supported by its own material.

## Explaining an evaluation procedure

Source: TESTEVAL, acl_latex.tex, Task Description, in the source directory above.

> After generation, all test cases must undergo a correctness check, which consists of \textit{syntactic correctness}, \textit{execution correctness}, and \textit{assertion correctness}. Syntactic correctness determines if the generated test case is free of syntax errors, while execution correctness evaluates if the test case can be executed successfully without any runtime errors. Assertion correctness evaluates whether the generated test case contains correct test assertions. Regarding execution correctness, we do not consider incorrect test assertion statements to be failed cases, since test cases with assertion errors can still cover the program under test.

The definitions tell readers how the reported measurements differ. The final
sentence explains a choice that affects those measurements. That explanation
is substantive information even though it resembles a qualification or
exception. A language edit should retain the distinction and its consequence.

## Applying a sample

Read its full surrounding argument when using it to guide a real task.
Identify the supported claim, the information needed to interpret it, and
the role of any figure or example. Use the sample's selection and explanation
as a reference while keeping the current paper's facts, scope, and voice.

When the user's draft is sound, preserve it. When structure is the problem,
decide what the reader must know and in what order, then rewrite the authorized
scope. When expression is the problem, repair the wording while retaining
the relationship already present.
