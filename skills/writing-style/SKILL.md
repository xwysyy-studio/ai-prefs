---
name: writing-style
description: >-
  Draft, polish, and restructure Chinese or English prose, including academic
  papers, README files, and technical notes. Use for humanizing text, following
  an established voice, and developing a settled paper's narrative. Research
  direction selection belongs to research-idea; independent manuscript review
  to paper-review; responses to submitted reviews to rebuttal.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Writing style

Improve the requested text for its actual reader. Read the source, relevant
project requirements, and any approved sample before editing. Use the user's
confirmed scope and voice directly; ask only when missing information or a
material conflict would change the result. For specified additions or
deletions, make those changes and preserve unrelated text. Polishing addresses
expression; drafting and authorized restructuring allow content selection
and organization appropriate to the task.

## Select the material needed for this task

Read the required material for the applicable domain before doing the work.

| Task | Read |
|---|---|
| Chinese notes, blogs, README files, or other general prose | [chinese-writing.md](references/chinese-writing.md) |
| General English prose | Use this entry's expression and preservation guidance, the supplied text, and approved examples |
| Academic writing or LaTeX paper prose | [style-apply.md](references/style-apply.md), [paper-voice-contract.md](references/paper-voice-contract.md), and `~/.claude/rules/academic-writing.md`, including when the manuscript is Markdown |

For mixed-language text, apply the relevant language guidance to each passage.
General English uses plain, direct sentences and complete logical
relationships. Keep useful explanation and the author's existing personality;
adjust sentence length where it improves understanding. Apply the
user-facing documentation preferences in `~/.claude/rules/writing-tone.md`
when writing README files or product copy. The references below are read when
their stated task conditions apply.

## Preserve meaning while improving expression

- Polishing retains facts, numbers, reasoning, examples, conditions,
  comparisons, uncertainty, and useful explanation. Remove empty wording;
  express vague content more concretely only with facts already supplied.
  Leave sound wording alone. Keep quotations, names, and text discussed as
  examples intact unless the requested operation changes them. Shorter text
  is not the objective.
- Drafting and authorized restructuring select material for the reader's
  purpose. Before drafting, restructuring an argument, or interpreting results,
  match each core claim to its source, comparison conditions, scope, and
  substantive counterevidence. Preserve what the reader needs to assess those
  claims. A change to the paper's direction or a result's meaning requires a
  user decision.
- Keep the author's established terminology and voice. First-person
  experience, emotion, opinions, and factual claims must come from the source
  or user context. Do not invent them to make prose sound human.
- Write objects, actions, conditions, and results directly. Position the work
  positively with its actual scope. Preserve real negative findings; respond
  to objections only when they exist in reader-visible material.
- Preserve citation-to-claim relationships, cross-references, mathematical
  meaning, code, labels, and non-prose environments. In authorized structural
  edits, move citations with the claims they support.
- Apply corrections at the extent authorized by the current request. For
  substantive corrections to facts, meaning, argument, or structure, follow
  Core Rule 7: identify the facts, reasoning, conditions, examples, details,
  and author stance to retain; compare that content with the original for each
  affected paragraph or section, then rewrite the affected portions and verify
  preservation against both the inventory and the source. For substantive
  correction of long passages or repeated substantive corrections, use a clean context with the confirmed
  requirements, retained content, and original evidence to regenerate the
  affected portions. Check analogous passages and adjacent transitions for the
  same issue, repair authorized instances, and report any needed extension.
  Explicit narrow additions or deletions preserve unrelated text. Keep revision
  history in the handoff.

Read the result against the input and task. Check the actual information and
argument, not word counts or pattern scores. Complete the authorized scope
and deliver the requested prose, file, or diff; return only prose when that
is what the user asks for. For rendered layout changes, inspect the affected
pages.

## Read references when they resolve a concrete need

For a polishing, humanizing, voice-consistency, or style-audit pass, read the
corresponding language catalog, [patterns-chinese.md](references/patterns-chinese.md)
or [patterns-english.md](references/patterns-english.md), and apply it to the
actual passages. Academic prose also follows the required
[paper-voice-contract.md](references/paper-voice-contract.md). Catalog matches
locate passages to read; they do not establish authorship or justify deleting
information. User-wide expression preferences remain binding, including the
ban on em dashes.

For “只标不改 / detect / audit only,” identify the location, quoted passage,
and concrete expression problem without changing the text. Use plain problem
names or the relevant catalog's categories; counts are useful only when the
user needs an aggregate audit.

For paper writing or polishing, read the current approved passages and
[personal-style-profile.md](references/personal-style-profile.md) to apply the
established voice; the user's current samples take precedence. For a
whole-paper narrative or substantial structural rewrite, use
[narrative-flow-playbook.md](references/narrative-flow-playbook.md);
mapping claims to evidence is required as described above. When several claims
or result groups share evidence, use the existing
[claim-evidence-map.md](assets/claim-evidence-map.md) format to keep their
relationships explicit; it does not require a separate file. Read
[long-form-humanize.md](references/long-form-humanize.md) when work spans
sections or sessions or involves long content or repeated substantive corrections.

Paper section guidance is available for the requested section:
[abstract](references/abstract-playbook.md),
[introduction](references/introduction-playbook.md),
[related work](references/related-work-playbook.md),
[method](references/method-playbook.md),
[experiments](references/experiments-playbook.md),
[conclusion and impact](references/conclusion-impact-playbook.md), and
[appendix](references/appendix-playbook.md).

For technical presentation, read the matching resource:
[equations and notation](references/equations-and-notation.md),
[figures and tables](references/figures-and-tables.md),
[citations and BibTeX](references/citation-and-bibtex.md),
[LaTeX structure](references/latex-project-structure.md), or
[definitions and theorems](references/definitions-theorems-playbook.md).
Use [ICML 2026 requirements](references/icml2026-writing-requirements.md)
only for that venue and year, checking current official requirements when
they affect the task.

Examples are available for [Chinese](examples/chinese.md),
[English](examples/english.md), and
[annotated academic writing](references/annotated-writing-examples.md).
They illustrate choices under their supplied facts. For additional paper
calibration, use
[related-work-writing-notes.md](references/related-work-writing-notes.md).
Only confirmed, cross-task preferences belong in the personal style profile;
domain-specific examples and their conditions stay in the existing notes.
