# Academic English and LaTeX

Read this reference for paper writing and LaTeX tasks. General English prose
uses SKILL.md's common guidance and does not require paper references.
For paper prose, also read paper-voice-contract.md and the applicable
`~/.claude/rules/academic-writing.md` requirements before writing or polishing.

Use the user's requested operation to select the work. Existing prose,
project requirements, approved examples, and the actual evidence establish
the scope and voice. The current task and the skill's shared rules take
precedence over example structures.

## Establish what is being changed

Read the supplied text and the locally available material relevant to the
request before asking for inputs. Determine the intended reader, paper stage,
editing scope, and applicable venue constraints from that material.
Read personal-style-profile.md and the user's approved passages to calibrate
selection, density, and expression; current approved samples take precedence.
Ask only about unresolved choices that would materially change the result.

Determine the operation from the current request. For specified additions or
deletions, change the identified content and preserve unrelated text. Wording
edits, new explanations, and structural work each follow their authorized
scope. Preserve settled decisions and complete that scope without requiring
a separate confirmation for each paragraph.

## Polishing an existing passage

Read the passage with its relevant context. Identify specific problems in
clarity, wording, sentence flow, or redundant phrasing. Revise those problems
and leave sound text alone. Retain the original claims, values, conditions,
comparisons, and uncertainty.

An aside about what the paper has not claimed or tested may be removed when
it has no bearing on the passage's claims, evidence, or reader purpose.
Apply paper-voice-contract.md Category 8 to distinguish it from a meaningful
limitation or author judgment. A requested word-level change leaves the rest
of the passage intact.

Read patterns-english.md for the polishing pass and judge the actual sentences.
Repeated wording can be necessary for technical precision; variation can
improve rhythm when the
meaning is unchanged. Clarify an abstract subject using facts already present
in the material, rather than adding new specifics.

Check the resulting text against the source. If the problem requires changing
the paper's direction or the meaning of a result, explain that issue to the
user instead of treating it as an expression edit.

## Drafting from material

Read the project's question, settled story, related work, and actual results.
When the research direction itself remains open, use research-idea; when the
direction is settled, develop its explanation here.

Before drafting, restructuring, or interpreting results, map each core claim
to the actual source, comparison conditions, supported scope, uncertainty, and
substantive counterevidence. Distinguish reported observations from stronger
inferences and identify the evidence each inference needs. For a whole-paper
narrative or substantial structural rewrite, read narrative-flow-playbook.md
to organize the supported central claim and its supporting sections. When
several claims or result groups share evidence, use the existing
assets/claim-evidence-map.md format; the mapping can stay in current task
material and does not require a separate file. Resolve material contradictions
with the user before building the prose on them.

Arrange sections, figures, tables, and examples according to the reader's
questions and the applicable paper format. Plan an introduction that explains
the problem, relevant prior work, gap, approach, and supported contribution
in an order suited to this paper. The job each passage performs matters more
than a fixed number of paragraphs or contribution items.

Use the appropriate section playbooks. Choose a concrete result for an
abstract when it carries the central finding; preserve the needed qualitative
explanation and conditions. A numerical result is not a quota for every
abstract. When experiments are still pending, organize the questions they
need to answer without inventing their results.

For an ICML-style eight-page main paper, assets/icml-8page-outline.md is an
available example; other formats use their own requirements. Read and follow
current official venue requirements when the task depends on them.

## Restructuring an authorized section or paper

Read the material in the requested scope and determine why its current
organization does not serve the reader. If useful, extract an outline with
scripts/extract_tex_outline.py, using the actual main TeX file.

Identify the content the final version needs: claims, supporting evidence,
conditions, definitions, examples, and substantive counterevidence. Check
that this inventory preserves what remains necessary from the current draft.
Choose the new order, then rewrite the affected sections from that material.

Start with the part whose organization controls the requested change.
Abstract and Introduction are appropriate starting points for a full-paper
reframing, while an experiment-section task can stay within that section and
its actual dependencies. Change other sections only within the authorized
scope, or report the needed extension.

Read the assembled result in order and check both the argument and the
meaning of every retained result. Citations follow the claims they support.
Use long-form-humanize.md when the work needs multiple sections or sessions.

## LaTeX and presentation work

Make the requested formatting or technical change in the project's existing
structure. Read the relevant reference: latex-project-structure.md,
equations-and-notation.md, figures-and-tables.md, or
definitions-theorems-playbook.md.

Preserve the semantics of symbols, equations, labels, and reference targets.
Use the project's notation and conventions. Modular section files, separate
large tables, booktabs, and self-contained captions are available practices
when they fit the task; a local LaTeX question does not authorize reorganizing
the project.

Helpers live in the skill's scripts/ directory; resolve their paths from the
skill root. assets/latex-snippets.tex and assets/macro-template.tex provide
examples for requested formatting work. Inspect the actual rendered artifact
after layout changes.

## Final polish

Respect the approved content and the submission stage. Fix the requested
language, reference, data, or visible rendering problems. Reopen a settled
argument only when new evidence materially changes it and the user decides
how to proceed.

For ICML 2026, scripts/icml2026_writing_quickcheck.py provides a heuristic
check when its assumptions match the task. Use applicable checks for other
venues. Verify required sections and anonymization when requested or
required for the authorized submission work.

Independent manuscript assessment belongs to paper-review. A writing pass
checks that its own changes are faithful, clear, and usable.

## Expression and voice

Academic English is plain, direct, and specific. Keep the user's established
voice, including active voice and we where appropriate. First-person stance,
opinions, and experiences must come from the original text or user context.
Academic polishing adds no humor or personal narrative.

For polishing, humanizing, voice consistency, or expression audit, read
patterns-english.md and apply the already required paper-voice-contract.md.
Logical connectives such as However, Moreover, and Thus are normal academic
devices when their relationships are real. Remove empty announcements and
redundant transitions while preserving useful explanation.

Let sentence length follow the argument. Split a long sentence when that
makes its subjects, conditions, and result easier to follow; retain a longer
sentence when its relationship is clear. Do not manufacture rhythm by
changing sentences solely to meet a length distribution.

Combine redundant hedges only when the proposition's uncertainty stays
equivalent. A qualifier that limits the evaluated population, setting, or
strength of evidence remains attached to the claim. Keep explanations of
results when they contribute new, supported meaning.

Use the user's approved passages for calibration; examples/english.md can
help with a concrete expression problem. Personal style preferences are not
venue rules or evidence that a text was written by AI.

## Preservation Rules

During polishing:

- Keep each citation attached to the claim it supports.
- Preserve reference commands and targets, labels, mathematical statements,
  algorithms, code, and other non-prose environments.
- Preserve the meaning and target of each caption. Caption rewriting or
  layout changes follow the requested scope and figures-and-tables.md.
- Keep established terminology, values, units, comparisons, and effective
  qualifiers. Do not introduce studies, findings, or references from memory.

During authorized restructuring, text and citations can move together.
Recheck cross-references and the new context; changing organization does not
authorize changing mathematical or empirical meaning. During requested
LaTeX work, alter only the relevant structures and verify the rendered result.

## Verification and delivery

Read the edited result against the input and the requested operation.
Check factual and logical preservation, citation-to-claim alignment,
cross-references, and any non-prose content affected by the task.
Use the pattern catalog only to guide this reading.

When feedback corrects facts, meaning, argument, or structure, apply Core Rule
7 within the authorized scope: inventory the evidence, conditions, reasoning,
examples, details, and author stance that must survive; compare the inventory
with the original for each affected paragraph or section, then rewrite the
affected content and check the result against the source. For substantive
correction of long passages or repeated substantive corrections, read
long-form-humanize.md and regenerate
the affected portions in a clean context carrying the confirmed requirements,
retained content, and original evidence. Inspect analogous passages and
adjacent transitions for the same issue; repair instances within scope and
report any needed extension. Explicit narrow additions or deletions preserve
unrelated text. A request to reduce detail can call for selecting fewer
information units; smoother language calls for clearer expression of the
retained units.

Return the requested text, file, or diff. For a short LaTeX passage with no
specified output format, the existing quick-pass form is the revised LaTeX,
a Chinese translation, and a brief modification note. If the user asks only
for the revised passage, return only that passage. Preserve a passage that
already meets the request.

## Supporting references

The required personal-style-profile.md supplies the default paper voice;
related-work-writing-notes.md provides examples of how papers develop their
arguments. Section guidance is in abstract-playbook.md,
introduction-playbook.md, related-work-playbook.md, method-playbook.md,
experiments-playbook.md, conclusion-impact-playbook.md, and
appendix-playbook.md. Citation handling is in citation-and-bibtex.md.
