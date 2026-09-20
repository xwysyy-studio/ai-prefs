---
name: claude-delegate
description: >-
  Delegate meaningful consultation, bounded execution, and independent review to
  the local Claude Code CLI. Jobs run as Claude Code background sessions, expose
  intermediate evidence, surface questions as a blocked state, and support fleet
  collection and follow-up turns. Use when the user asks for Claude or when an
  important open decision benefits from its independent judgment. Routine edits,
  ordinary lookup, and each small implementation step do not need it.
---

# Claude Delegate

Use Claude as an independent worker while the coordinating agent owns the user's goal,
authority, integration, and verification. Delegate a meaningful question or deliverable;
keep ordinary execution choices with the coordinator. Check the latest user instructions
about model, availability, and paused calls before launching or resuming.

## Give the worker room to work

Provide the actual question, necessary evidence, confirmed decisions, and open judgments.
Let Claude choose its approach. Separate the user's requirements from the coordinator's
suggestions. Approximate quantities, examples, and overall approval do not create new
fixed requirements. When a framing has been rejected, commission a fresh solution using
the accepted requirements and original material.

Consultation includes authority for the task-related local work needed to understand and
check the question: notes and memory, material organization, experiments, and useful
improvements to relevant documents. Use that authority as needed and pass it to the
delegate. Protect the specific objects the user names; a fixed review target can coexist
with notes and experiments elsewhere. Honor explicit prohibitions on all writes. Existing
execution authority is not reduced by delegation; changes to confirmed goals or scope, and
work outside the assignment, remain decisions for the user. The shared contract is in
`~/.claude/references/codex-delegation.md`.

Keep ordinary prompts concise. Substantial implementation may use relevant portions of
`~/.claude/references/codex-task-template.md`; consultation does not require a formal
implementation package. Carry existing execution authorization into the prompt and name
the result's consumer and verification method. Use `--prompt-file` for a substantial brief.
The prompt travels as one command-line argument, so it is limited to 100 KB; put larger
material in files and reference them.

## Choose the model and session

Use the user's explicit model choice first. The runner's `task --help` shows the current
consultation model and effort defaults. Standard model routes use full ids with 1M context:
`claude-fable-5-1[1m]` for open consultation, `claude-opus-5[1m]` for bounded execution,
and `claude-opus-4-6[1m]` when prose work calls for that model. These are starting choices;
a user's task-specific preference or verified samples can determine another division of work.
Do not infer that planning, writing, or final acceptance always belongs to one model family.

A new job pins model and effort. A job is one Claude Code background session, and `--resume`
sends the next prompt into that same session with its saved model, effort, directories, and
name; those options cannot change on resume, so start a new job to change them. The runner
reports the requested model and the model Claude wrote into the transcript separately; a
mismatched full model id withholds the result. An unavailable model is reported, not replaced.

Start a fresh session for independent consultation or review. Use resume for recovery,
clarification, continuation of the same worker's work, and for answering a blocked job's
question. The user may explicitly request a new session even when an old one exists.

## Launch, inspect, and collect

```bash
C=~/.agents/skills/claude-delegate/scripts/claudectl.py
python3 "$C" task --cd /path/to/project --prompt-file /path/to/task.md
python3 "$C" task --model 'claude-opus-5[1m]' --effort xhigh --cd /path/to/project 'Task and authority'
python3 "$C" task --resume JOB --prompt-file /path/to/followup.md
python3 "$C" task --resume JOB 'answer to its question'
python3 "$C" status JOB
python3 "$C" progress JOB --offset 0 --limit 20
python3 "$C" wait JOB_A JOB_B
python3 "$C" result JOB
python3 "$C" cancel JOB
claude attach JOB
```

Every job runs with `bypassPermissions` and edits the working copy directly; the runner
turns off Claude Code's background worktree isolation, so no branch, worktree, commit, or
push happens unless the task asks for it. The prompt and user authorization define the
job's scope. `--cd` selects the working directory; repeat `--add-dir DIR` for other intended
directories. The session loads normal Claude configuration, hooks, and skills, and keeps the
full interactive tool set, including AskUserQuestion. Prompt input comes from arguments or
`--prompt-file`, never from harness stdin.

The job id is the short id that `claude agents`, `claude attach`, `claude logs`, and
`claude stop` take. A human can open any job with `claude attach JOB`, watch or steer it,
and leave it running. A Claude coordinator can also message the session directly by its
name through cross-session messaging; the runner's `task --resume` is the route that works
for every coordinator, including Codex.

Independent jobs can run in parallel. Give editing jobs separate output files and let the
coordinator integrate them. Use one yielding `wait` for a batch or `task --follow` for a
single job, and continue useful work while the execution tool waits. Do not build polling
loops. `wait` returns when every job is completed, blocked, failed, stopped, stalled, or
missing: exit 0 when all completed, 3 when some job needs a decision (blocked or stalled),
2 when some job failed, was stopped, or is no longer listed.

`status` combines `claude agents --json` with the session transcript. `busy`, `waiting`,
and `idle` are process facts; Claude Code's own `state` is a judgement that can stay at
`working` after a finished turn, so the runner reports `completed` when the process is idle,
the transcript closed its last turn, and no background work is in flight. `blocked` means
the session is waiting on input: a question it asked, a permission or sandbox decision, or a
dialog. The status line prints the pending question when the transcript has it. Answer with
`task --resume JOB 'answer'`; the runner stops the process, restates the pending question,
and wakes the session with the answer as its next prompt, because stopping drops the
unanswered turn from the transcript. Attaching answers the question natively instead.

`progress` reads a page of the session transcript directly: prompts, public assistant
messages, tool calls, and tool results, with `sidechain: true` on subagent records. JSON
reports runtime status, native state, requested and reported model, effort, byte offsets,
`next_offset`, and `has_more`. Continue with the returned cursor. Complete message bodies
are retained; thinking and image binary are excluded. A partially written tail is left for
the next read. No duplicate progress state is stored. Running, blocked, stalled, failed,
and stopped jobs all expose their transcript.

Judge progress by what the worker has actually established and what remains open.
If the user asks to finish with the existing work, inspect the evidence, resolve the useful
findings, and stop remaining jobs as appropriate. Report an interim record as interim;
waiting for a ceremonial final message is not a completion requirement.

`STALLED` means a busy process whose transcript has not changed for the stall window.
Inspect `progress` or attach before cancelling. `cancel` runs `claude stop`, verifies the
process is gone, and keeps the conversation; `task --resume` continues it. Interrupting a
waiter leaves the worker running. A finished session's process is retired after about an
hour unattached; `task --resume` wakes it. Follow the user's pause and recovery instructions
and classify a failure before attempting another call. Do not silently change model,
provider, or route. `claude rm JOB` deletes the native session; job records stay under
`~/.claude-delegate/jobs/JOB/`. After a Claude Code upgrade, `claude daemon stop --any`
lets the next job start on the new version.

## Verify the result

The session transcript is the raw evidence. `result` prints the final assistant message of
a completed job and refuses running, blocked, stopped, and failed jobs; it withholds a
result whose transcript model differs from the requested full id. Automatic display redacts
credentials; local raw files remain unchanged.

Request the answer, supporting evidence, important edits, and remaining gaps. For review,
use `~/.claude/references/review-task-template.md`: pin the target version, provide original
requirement sources, and keep the coordinator's verdict and peer verdicts out of the brief.
A changed artifact needs a fresh review. Reviewers must connect each defect to a real
expectation and supporting evidence, not infer a violation from wording alone.

The coordinator checks returned edits and the actual artifact. Source accuracy, content
coverage, reader usefulness, layout, and executed behavior are separate verification needs.
Select the ones the assignment requires. Keep reviewer completion (`STATUS`) separate from
artifact judgment (`VERDICT`), and decide from `EVIDENCE` rather than a model's self-assessment.
