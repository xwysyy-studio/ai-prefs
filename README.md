# ai-prefs

How one person wants an AI assistant to write, reason and check its work. This is an
unedited export of the rule and skill files used by local coding agents (Claude Code and
Codex), published so that a web model such as ChatGPT can align with the same
preferences. Read selectively: some parts describe machinery that only exists on the
author's machine and are irrelevant to you.

## What to read, in order

1. `claude/CLAUDE.md`, section **Core Rules**: how to treat facts and sources, how to
   write for the reader, how to handle corrections, how to scope implementation. These
   apply to any assistant. Skip **Git 安全** (item 2), the **运行边界** section and the
   **按任务读取** table; they concern local tools, paths and permissions.
2. `claude/rules/writing-tone.md` and `claude/rules/academic-writing.md`: the writing
   preferences for Chinese and English prose, technical notes and papers. Apply them to
   every draft.
3. `claude/rules/dev-core.md` and `claude/rules/verification.md`: judgement rules for
   code and for deciding whether something is verified. Use the reasoning; ignore the
   references to local scripts, test runners and delegation.
4. `skills/writing-style/`: the drafting and polishing method, with the author's own
   voice profile and worked examples. Start at `SKILL.md` and open the reference the
   task needs (introduction, experiments, Chinese writing, humanizing long text, ...).
5. `skills/research-idea/`: how to develop and evaluate a research idea before writing.

`codex/AGENTS.md` is the same rule set phrased for the Codex runtime; read it only if
`claude/CLAUDE.md` is unavailable. `codex/rules/default.rules` is a local command
allowlist with no meaning outside that machine.

## Conventions you will meet

- Paths such as `~/.claude/...` or `~/.agents/skills/...`, and tools such as `repo-state`,
  `codex-delegate`, `find-and-fetch` or `browser-use`, are local to the author's setup. When a
  rule tells the assistant to consult one of them, treat it as "check the real source before
  asserting" and use whatever you have.
- Chinese is the default language for replies to the author; English is used for code,
  scripts and messages to other models. Papers follow their venue's language.
- The files are the live originals, copied on each backup; nothing here is rewritten for
  publication.
