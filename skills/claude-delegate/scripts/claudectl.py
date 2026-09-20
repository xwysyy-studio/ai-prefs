#!/usr/bin/env python3
"""claudectl - delegation runner on Claude Code background sessions.

Commands:
  task [PROMPT]   start a background Claude Code session, or continue one with --resume
  status [ID]     list jobs / inspect one; --wait blocks until it settles
  wait ID...      wait for every named job with one fleet waiter
  progress ID     page through the session transcript as JSON
  result [ID]     print the final assistant message of a completed job
  cancel [ID]     stop a running session and verify its process is gone

A job is one Claude Code background session (`claude --bg`). Its id is the short id
that `claude agents`, `claude attach`, `claude logs` and `claude stop` take, so a human
can open any job with `claude attach ID`. State comes from `claude agents --json`;
evidence comes from the session transcript under the Claude projects directory.
"""

import argparse
import fcntl
import json
import os
import re
import shlex
import subprocess
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import NoReturn


STATE_ROOT = Path(
    os.environ.get("CLAUDE_DELEGATE_HOME", "~/.claude-delegate")
).expanduser().resolve()
JOBS_DIR = STATE_ROOT / "jobs"
CLAUDE_HOME = Path(os.environ.get("CLAUDE_CONFIG_DIR", "~/.claude")).expanduser()
PROJECTS_DIR = CLAUDE_HOME / "projects"
DEFAULT_MODEL = "claude-fable-5-1[1m]"
DEFAULT_EFFORT = "xhigh"
PERMISSION_MODE = "bypassPermissions"
BG_SETTINGS = json.dumps({"worktree": {"bgIsolation": "none"}})
DEFAULT_STALL_SECS = 900
POLL_SECS = 3
CLI_TIMEOUT = 60
REGISTER_TIMEOUT = 30
STOP_TIMEOUT = 20
MAX_PROMPT_BYTES = 100_000
NAME_WIDTH = 48
LIST_RECENT = 8
SETTLED = ("completed", "failed", "stopped", "blocked", "stalled", "missing")
LAUNCH_RE = re.compile(r"backgrounded\W+([0-9a-f]{8})")
COPY_RE = re.compile(r"started a copy as ([0-9a-f]{8})")
UUID_RE = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)
REDACTED = "[REDACTED]"
BEARER_RE = re.compile(r"(?i)\bBearer\s+(?!\[REDACTED\])[^\s,;]*[^\s,;&\"')}\]]")
URL_USERINFO_RE = re.compile(
    r"(?i)\b([a-z][a-z0-9+.-]*:(?:\\*/){2})(?:(?:\\+/)|[^/@\s])+@"
)
SECRET_NAME = (
    r"(?:[a-z0-9]+[_-]+)*(?:api[_-]?key|access[_-]?token|refresh[_-]?token|"
    r"auth[_-]?token|client[_-]?secret|password|secret|token)"
)
QUOTED_SECRET_START_RE = re.compile(
    r"(?i)((?:\\*[\"'])?\b(authorization|" + SECRET_NAME
    + r")\b(?:\\*[\"'])?\s*[:=]\s*)(\\*[\"'])"
)
AUTHORIZATION_SECRET_RE = re.compile(
    r"(?i)(\bauthorization\b\s*[:=]\s*)"
    r"((?:\\*[\"'])?(?:(?:Bearer|Basic|Token|ApiKey)\s+)?)"
    r"((?:\\*[\"'])?\[REDACTED\](?:\\*[\"'])?|[^\s,;&}\]]*[^\s,;&\"')}\]])"
)
LABELED_SECRET_RE = re.compile(
    r"(?i)((?:\\*[\"'])?\b" + SECRET_NAME
    + r"\b(?:\\*[\"'])?\s*[:=]\s*)(?!\\*[\"'])"
    r"(\[REDACTED\]|[^\s,;&}\]]*[^\s,;&\"')}\]])"
)
PREFIXED_SECRET_RE = re.compile(
    r"\b(?:sk-[A-Za-z0-9_-]{12,}|sk_(?:live|test)_[A-Za-z0-9_-]{8,}|"
    r"gh[pousr]_[A-Za-z0-9_-]{8,}|"
    r"github_pat_[A-Za-z0-9_-]{8,}|xox[baprs]-[A-Za-z0-9_-]{8,}|"
    r"AIza[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{12,})\b"
)


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def die(message, code=1) -> NoReturn:
    print(message, file=sys.stderr)
    raise SystemExit(code)


# --- redaction of displayed text (raw files stay unchanged) ---------------------

def redact_quoted_secrets(text):
    """Find closing quotes at the opening delimiter's JSON escape depth."""
    parts = []
    cursor = 0
    while match := QUOTED_SECRET_START_RE.search(text, cursor):
        delimiter = match.group(3)
        quote = delimiter[-1]
        depth_slashes = len(delimiter) - 1
        backslashes = 0
        end = len(text)
        close = ""
        for index in range(match.end(), len(text)):
            char = text[index]
            if char == "\\":
                backslashes += 1
                continue
            if char == quote and backslashes % (2 * (depth_slashes + 1)) == depth_slashes:
                end = index + 1
                close = delimiter
                break
            if char == "\n":
                end = index
                break
            backslashes = 0
        scheme = ""
        if match.group(2).lower() == "authorization":
            found = re.match(r"(?i)(?:Bearer|Basic|Token|ApiKey)\s+", text[match.end():end])
            scheme = found.group(0) if found else ""
        parts.extend((text[cursor:match.start()], match.group(1), delimiter, scheme, REDACTED, close))
        cursor = end
    parts.append(text[cursor:])
    return "".join(parts)


def redact_labeled_secret(match):
    return f"{match.group(1)}{REDACTED}"


def redact_authorization_secret(match):
    if REDACTED in match.group(3):
        return match.group(0)
    return f"{match.group(1)}{match.group(2)}{REDACTED}"


def redact_secrets(value):
    text = redact_quoted_secrets(str(value or ""))
    text = AUTHORIZATION_SECRET_RE.sub(redact_authorization_secret, text)
    text = BEARER_RE.sub(f"Bearer {REDACTED}", text)
    text = URL_USERINFO_RE.sub(rf"\1{REDACTED}@", text)
    text = LABELED_SECRET_RE.sub(redact_labeled_secret, text)
    return PREFIXED_SECRET_RE.sub(REDACTED, text)


def redact_value(value):
    if isinstance(value, str):
        return redact_secrets(value)
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    if isinstance(value, dict):
        return {
            redact_secrets(key): (
                REDACTED if LABELED_SECRET_RE.match(f"{key}=value") or key.lower() == "authorization"
                else redact_value(item)
            )
            for key, item in value.items()
        }
    return value


# --- files and job records ------------------------------------------------------

def write_text(path, content):
    tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def write_json(path, value):
    write_text(path, json.dumps(value, ensure_ascii=False, indent=1) + "\n")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def runner_command():
    return shlex.join([sys.executable, os.path.abspath(__file__)])


def load_job(jobdir):
    job = read_json(jobdir / "job.json")
    job["_dir"] = jobdir
    return job


def save_job(job):
    record = {key: value for key, value in job.items() if not key.startswith("_")}
    write_json(job["_dir"] / "job.json", record)


def all_jobs():
    if not JOBS_DIR.is_dir():
        return []
    jobs = []
    for path in JOBS_DIR.iterdir():
        if path.is_dir() and (path / "job.json").is_file():
            job = load_job(path)
            if "session_id" in job and "turns" in job:  # records of the retired print-mode runner are ignored
                jobs.append(job)
    return sorted(jobs, key=lambda job: job.get("created_at", ""), reverse=True)


def lookup_job(ref):
    jobs = all_jobs()
    if not jobs:
        return None
    if not ref or ref == "last":
        return jobs[0]
    exact = [job for job in jobs if job["id"] == ref]
    matches = exact or [job for job in jobs if job["id"].startswith(ref)]
    return matches[0] if len(matches) == 1 else None


def find_job(ref):
    job = lookup_job(ref)
    if job is None:
        die(
            f'No unique job matches "{ref or "(latest)"}". '
            f"Run `{runner_command()} status` to list jobs."
        )
    return job


@contextmanager
def job_lock(jobdir):
    lock_path = jobdir / "lifecycle.lock"
    with lock_path.open("a", encoding="utf-8") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def turn_prompt_path(job, index):
    return job["_dir"] / f"prompt-{index}.md"


def add_turn(job, prompt, kind):
    index = len(job["turns"]) + 1
    write_text(turn_prompt_path(job, index), prompt)
    job["turns"].append({"index": index, "kind": kind, "started_at": now_iso()})
    save_job(job)


def prompt_summary(job, width=100):
    if not job["turns"]:
        return ""
    path = turn_prompt_path(job, job["turns"][-1]["index"])
    if not path.is_file():
        return ""
    text = " ".join(path.read_text(encoding="utf-8", errors="replace").split())
    redacted = redact_secrets(text)
    return redacted if len(redacted) <= width else redacted[: width - 3] + "..."


# --- the Claude Code CLI --------------------------------------------------------

def claude_run(argv, cwd=None, timeout=CLI_TIMEOUT):
    try:
        return subprocess.run(
            ["claude", *argv],
            cwd=cwd,
            text=True,
            capture_output=True,
            stdin=subprocess.DEVNULL,
            timeout=timeout,
        )
    except FileNotFoundError:
        die("The claude CLI is not on PATH.", 127)
    except subprocess.TimeoutExpired:
        die(f"`claude {argv[0]}` did not return within {timeout}s.", 2)


def agents_rows():
    proc = claude_run(["agents", "--json", "--all"], timeout=REGISTER_TIMEOUT)
    if proc.returncode != 0:
        die(
            "`claude agents --json --all` failed: "
            + redact_secrets((proc.stderr or proc.stdout).strip()),
            2,
        )
    try:
        rows = json.loads(proc.stdout)
    except json.JSONDecodeError:
        die("`claude agents --json --all` returned non-JSON output.", 2)
    if not isinstance(rows, list):
        die("`claude agents --json --all` returned a non-list document.", 2)
    return [row for row in rows if isinstance(row, dict)]


def agents_row(job_id, rows=None):
    for row in agents_rows() if rows is None else rows:
        if row.get("id") == job_id and row.get("kind") == "background":
            return row
    return None


def wait_row(job_id, predicate, timeout):
    deadline = time.time() + timeout
    while True:
        row = agents_row(job_id)
        if predicate(row):
            return row
        if time.time() >= deadline:
            return row
        time.sleep(0.5)


def launch_output(proc):
    return (proc.stdout or "") + (proc.stderr or "")


def parse_launch(output):
    copy = COPY_RE.search(output)
    launched = LAUNCH_RE.search(output)
    return (launched.group(1) if launched else None), (copy.group(1) if copy else None)


def stop_session(job_id):
    proc = claude_run(["stop", job_id], timeout=STOP_TIMEOUT)
    if proc.returncode != 0:
        die(f"`claude stop {job_id}` failed: " + redact_secrets(launch_output(proc).strip()), 2)
    row = wait_row(job_id, lambda row: row is None or not row.get("pid"), STOP_TIMEOUT)
    if row is not None and row.get("pid"):
        die(f"Session {job_id} still has pid {row['pid']} after `claude stop`.", 2)
    return row


# --- transcript evidence --------------------------------------------------------

def project_slug(cwd):
    return re.sub(r"[^A-Za-z0-9]", "-", str(cwd))


def transcript_path(job):
    recorded = job.get("transcript")
    if recorded and Path(recorded).is_file():
        return Path(recorded)
    candidates = [PROJECTS_DIR / project_slug(job["cwd"]) / f"{job['session_id']}.jsonl"]
    candidates += PROJECTS_DIR.glob(f"*/{job['session_id']}.jsonl")
    found = [path for path in candidates if path.is_file()]
    if not found:
        return None
    path = max(found, key=lambda item: item.stat().st_mtime)
    job["transcript"] = str(path)
    save_job(job)
    return path


def transcript_records(path, offset=0):
    """Yield (start, end, record) for complete lines from a byte offset."""
    with path.open("rb") as stream:
        size = os.fstat(stream.fileno()).st_size
        if offset > size:
            die(f"Progress offset {offset} exceeds transcript size {size}.", 2)
        if offset:
            stream.seek(offset - 1)
            if stream.read(1) != b"\n":
                die(f"Progress offset {offset} is not a record boundary.", 2)
        stream.seek(offset)
        while True:
            start = stream.tell()
            line = stream.readline()
            if not line or not line.endswith(b"\n"):
                return
            end = stream.tell()
            if not line.strip():
                yield start, end, None
                continue
            try:
                record = json.loads(line)
            except (json.JSONDecodeError, UnicodeDecodeError):
                die(f"Malformed transcript record at offset {start}.", 2)
            if not isinstance(record, dict):
                die(f"Non-object transcript record at offset {start}.", 2)
            yield start, end, record


def message_blocks(record):
    message = record.get("message")
    if not isinstance(message, dict):
        return []
    content = message.get("content")
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    return [block for block in content if isinstance(block, dict)] if isinstance(content, list) else []


def public_content(value):
    """Keep public text and tool data while excluding private/binary blocks."""
    if isinstance(value, dict):
        if value.get("type") in ("thinking", "redacted_thinking", "reasoning", "image", "base64"):
            return None
        return {key: public_content(item) for key, item in value.items()}
    if isinstance(value, list):
        return [cleaned for item in value if (cleaned := public_content(item)) is not None]
    return value


def project_record(record):
    kind = record.get("type")
    if kind not in ("assistant", "user"):
        return None
    texts, tools, results = [], [], []
    for block in message_blocks(record):
        block_type = block.get("type")
        if block_type == "text" and isinstance(block.get("text"), str):
            texts.append(block["text"])
        elif block_type == "tool_use":
            tools.append({"id": block.get("id"), "name": block.get("name"),
                          "input": public_content(block.get("input"))})
        elif block_type == "tool_result":
            results.append({"tool_use_id": block.get("tool_use_id"),
                            "is_error": block.get("is_error", False),
                            "content": public_content(block.get("content"))})
    if not (texts or tools or results):
        return None
    projected: dict = {"kind": ("message" if texts else "tool") if kind == "assistant"
                       else ("prompt" if texts else "tool_result")}
    if texts:
        projected["texts"] = texts
    if tools:
        projected["tools"] = tools
    if results:
        projected["results"] = results
    if record.get("isSidechain"):
        projected["sidechain"] = True
    if record.get("timestamp") is not None:
        projected["timestamp"] = record["timestamp"]
    return projected


def observed_model(job):
    if job.get("actual_model"):
        return job["actual_model"]
    path = transcript_path(job)
    if path is None:
        return None
    for _, _, record in transcript_records(path):
        if record is None or record.get("type") != "assistant" or record.get("isSidechain"):
            continue
        model = record.get("message", {}).get("model")
        if model:
            job["actual_model"] = model
            save_job(job)
            return model
    return None


def base_model(name):
    return (name or "").split("[", 1)[0]


def model_mismatch(job):
    requested = job.get("model") or ""
    actual = observed_model(job)
    if not requested.startswith("claude-") or not actual:
        return None
    if base_model(actual) == base_model(requested):
        return None
    return f"Claude reported model {actual!r}; requested {requested!r}."


def final_message(path):
    last = None
    for _, _, record in transcript_records(path):
        if record is None or record.get("type") != "assistant" or record.get("isSidechain"):
            continue
        texts = [
            block["text"] for block in message_blocks(record)
            if block.get("type") == "text" and isinstance(block.get("text"), str) and block["text"].strip()
        ]
        if texts:
            last = "\n\n".join(texts)
    return last


def pending_question(path):
    """The last AskUserQuestion input, when no user prompt followed it."""
    question = None
    for _, _, record in transcript_records(path):
        if record is None or record.get("isSidechain"):
            continue
        if record.get("type") == "assistant":
            for block in message_blocks(record):
                if block.get("type") == "tool_use" and block.get("name") == "AskUserQuestion":
                    question = block.get("input")
        elif record.get("type") == "user" and any(
            block.get("type") == "text" for block in message_blocks(record)
        ):
            question = None
    return question


def turn_ended(path):
    """True when the last conversational record closes a turn (system/turn_duration)."""
    last = None
    for _, _, record in transcript_records(path):
        if record is None or record.get("isSidechain"):
            continue
        if record.get("type") in ("user", "assistant", "system"):
            last = record
    return last is not None and last.get("type") == "system" and last.get("subtype") == "turn_duration"


def native_state_file(job):
    """Best-effort read of Claude Code's own state.json; documented as unstable, so
    every caller tolerates an empty result."""
    path = CLAUDE_HOME / "jobs" / job["id"] / "state.json"
    try:
        data = read_json(path)
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def work_in_flight(job):
    in_flight = native_state_file(job).get("inFlight")
    if not isinstance(in_flight, dict):
        return False
    return any(isinstance(in_flight.get(key), int) and in_flight[key] > 0 for key in ("tasks", "queued"))


# --- status ---------------------------------------------------------------------

def activity_age(job):
    path = transcript_path(job)
    if path is not None:
        return time.time() - path.stat().st_mtime
    started = job["turns"][-1]["started_at"] if job["turns"] else job["created_at"]
    return time.time() - datetime.fromisoformat(started).timestamp()


def derive_status(job, row, stall_secs=DEFAULT_STALL_SECS, age=None):
    """`status` is the process fact (busy/waiting/idle); `state` is Claude Code's own
    judgement, which a summariser can leave at `working` after a finished turn.
    A quiet process whose transcript closed its last turn counts as completed."""
    if row is None:
        return "missing"
    state, status = row.get("state"), row.get("status")
    if status == "busy":
        age = activity_age(job) if age is None else age
        return "stalled" if age > stall_secs else "running"
    if status == "waiting" or state == "blocked":
        return "blocked"
    if state in ("failed", "stopped"):
        return state
    if state == "done":
        return "completed"
    if state == "working":
        path = transcript_path(job)
        if path is not None and turn_ended(path) and not work_in_flight(job):
            return "completed"
        age = activity_age(job) if age is None else age
        return "stalled" if age > stall_secs else "running"
    return f"unknown({state})"


def format_age(seconds):
    seconds = max(0, int(seconds))
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}m{seconds % 60:02d}s"
    return f"{seconds // 3600}h{(seconds % 3600) // 60:02d}m"


def describe_job(job, row, stall_secs=DEFAULT_STALL_SECS):
    age = activity_age(job)
    status = derive_status(job, row, stall_secs, age)
    native = "(not listed)"
    if row is not None:
        native = f"{row.get('state')}/{row.get('status') or 'no process'}"
        if row.get("waitingFor"):
            native += f" waiting for {row['waitingFor']}"
    line = (
        f"{job['id']}  {status:<9}  native {native}  activity {format_age(age)} ago  "
        f"requested model {job.get('model')}  actual model {observed_model(job) or '(unreported)'}  "
        f"effort {job.get('effort')}  turns {len(job['turns'])}  cwd {job['cwd']}"
    )
    summary = prompt_summary(job)
    if summary:
        line += f"\n  {summary}"
    resume = f"{runner_command()} task --resume {job['id']} 'reply'"
    if status == "blocked":
        path = transcript_path(job)
        question = pending_question(path) if path else None
        if question:
            line += "\n  question: " + json.dumps(question, ensure_ascii=False)
        elif native_state_file(job).get("detail"):
            line += "\n  native detail: " + str(native_state_file(job)["detail"])
        line += f"\n  answer: {resume}  |  or open it: claude attach {job['id']}"
    elif status == "stalled":
        line += (
            f"\n  STALLED: process alive but the transcript is unchanged for {format_age(age)} "
            f"(threshold {stall_secs}s). Inspect {runner_command()} progress {job['id']} or "
            f"claude attach {job['id']} before cancelling with {runner_command()} cancel {job['id']}"
        )
    elif status == "failed":
        line += (
            f"\n  FAILED: inspect claude logs {job['id']} or claude attach {job['id']}; "
            f"continue with {resume}"
        )
    elif status == "stopped":
        who = "cancelled by claudectl" if job.get("cancelled_at") else "stopped outside claudectl"
        line += f"\n  {who}; continue with {resume}"
    elif status == "missing":
        line += "\n  not listed by `claude agents --json --all`; it may have been removed with claude rm"
    return status, redact_secrets(line)


def print_final_message(job):
    path = transcript_path(job)
    text = final_message(path) if path else None
    mismatch = model_mismatch(job)
    if mismatch:
        print(f"(result withheld: {mismatch})")
        return False
    if text:
        print(redact_secrets(text.rstrip()))
        return True
    print("(no assistant text found in the session transcript)")
    return False


def settle(job, row, stall_secs):
    status, line = describe_job(job, row, stall_secs)
    print(line)
    result_present = True
    if status == "completed":
        print()
        result_present = print_final_message(job)
        if not result_present:
            status = "failed"
    return status


def exit_code_for(statuses):
    statuses = set(statuses)
    if statuses == {"completed"}:
        return 0
    if statuses & {"failed", "stopped", "missing"} or any(s.startswith("unknown") for s in statuses):
        return 2
    return 3


def wait_jobs(job_ids, stall_secs):
    settled = {}
    try:
        while len(settled) < len(job_ids):
            rows = agents_rows()
            for job_id in job_ids:
                if job_id in settled:
                    continue
                job = find_job(job_id)
                row = agents_row(job_id, rows)
                status = derive_status(job, row, stall_secs)
                if status in SETTLED or status.startswith("unknown"):
                    settled[job_id] = settle(job, row, stall_secs)
                    print(flush=True)
            if len(settled) < len(job_ids):
                time.sleep(POLL_SECS)
    except KeyboardInterrupt:
        pending = [job_id for job_id in job_ids if job_id not in settled]
        print("waiter interrupted; still running: " + ", ".join(pending) + " (jobs were NOT cancelled)")
        return 130
    if len(job_ids) > 1:
        print("fleet summary:")
        for job_id in job_ids:
            print(f"  {job_id}  {settled[job_id]}")
    return exit_code_for(settled.values())


# --- commands -------------------------------------------------------------------

def gather_prompt(args):
    parts = []
    if args.prompt_file:
        try:
            parts.append(Path(args.prompt_file).read_text(encoding="utf-8"))
        except OSError as error:
            die(f"Cannot read --prompt-file {args.prompt_file}: {error}")
    if args.prompt:
        parts.append(" ".join(args.prompt))
    prompt = "\n\n".join(part for part in parts if part.strip())
    if len(prompt.encode("utf-8")) > MAX_PROMPT_BYTES:
        die(
            f"Prompt exceeds {MAX_PROMPT_BYTES} bytes; the background session takes it as one "
            "command-line argument. Put the material in files and reference them."
        )
    return prompt


def session_name(args, prompt):
    if args.name:
        return args.name
    summary = " ".join(prompt.split())
    return summary if len(summary) <= NAME_WIDTH else summary[: NAME_WIDTH - 1] + "…"


def build_launch_argv(name, model, effort, add_dirs, prompt):
    # The prompt goes right after --bg: `--add-dir` is variadic and would swallow a
    # trailing prompt as another directory, so it comes last.
    argv = [
        "--bg", prompt,
        "--name", name,
        "--model", model,
        "--effort", effort,
        "--permission-mode", PERMISSION_MODE,
        "--settings", BG_SETTINGS,
    ]
    if add_dirs:
        argv += ["--add-dir", *add_dirs]
    return argv


def print_job_header(job, mode):
    print(f"job: {job['id']}")
    print(f"mode: {mode}")
    print(f"model: {job['model']}")
    print(f"requested effort: {job['effort']}")
    print(f"session: {job['session_id']}")
    print(f"dir: {job['_dir']}")
    print(f"attach: claude attach {job['id']}", flush=True)


def start_job(args, prompt):
    cwd = Path(args.cd).expanduser().resolve() if args.cd else Path.cwd().resolve()
    if not cwd.is_dir():
        die(f"--cd directory does not exist: {cwd}")
    add_dirs = [str(Path(d).expanduser().resolve()) for d in (args.add_dir or [])]
    for directory in add_dirs:
        if not Path(directory).is_dir():
            die(f"--add-dir directory does not exist: {directory}")
    model = args.model or DEFAULT_MODEL
    effort = args.effort or DEFAULT_EFFORT
    name = session_name(args, prompt)

    proc = claude_run(build_launch_argv(name, model, effort, add_dirs, prompt), cwd=str(cwd))
    output = launch_output(proc)
    job_id, copy_id = parse_launch(output)
    if proc.returncode != 0 or not job_id or copy_id:
        die(
            f"`claude --bg` did not start a session (exit {proc.returncode}):\n"
            + redact_secrets(output.strip()),
            2,
        )
    row = wait_row(job_id, lambda row: row is not None and row.get("sessionId"), REGISTER_TIMEOUT)
    if row is None or not row.get("sessionId"):
        die(
            f"Session {job_id} started but `claude agents --json --all` never listed its session id; "
            f"inspect with claude logs {job_id}.",
            2,
        )
    session_id = row["sessionId"]
    if not UUID_RE.fullmatch(session_id):
        die(f"Session {job_id} reported a non-UUID session id {session_id!r}.", 2)

    JOBS_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    jobdir = JOBS_DIR / job_id
    if jobdir.exists():
        die(f"Job directory {jobdir} already exists for a new session id; refusing to overwrite.", 2)
    jobdir.mkdir(mode=0o700)
    job = {
        "id": job_id,
        "session_id": session_id,
        "name": name,
        "created_at": now_iso(),
        "cwd": str(cwd),
        "model": model,
        "effort": effort,
        "permission_mode": PERMISSION_MODE,
        "add_dirs": add_dirs,
        "transcript": None,
        "actual_model": None,
        "turns": [],
        "_dir": jobdir,
    }
    add_turn(job, prompt, "task")
    print_job_header(job, PERMISSION_MODE)
    return job


def resume_job(args, prompt):
    if args.model or args.effort or args.cd or args.add_dir or args.name:
        die(
            "--resume continues the session with its saved model, effort, directories and name; "
            "passing those options would start a copy. Start a new job to change them."
        )
    job = find_job(args.resume)
    with job_lock(job["_dir"]):
        job = load_job(job["_dir"])
        row = agents_row(job["id"])
        if row is None:
            die(
                f"Job {job['id']} is not listed by `claude agents --json --all`; "
                "its session cannot be continued. Start a new job.",
                2,
            )
        if derive_status(job, row) == "blocked":
            # Stopping a blocked session drops its unanswered AskUserQuestion turn from the
            # transcript, so the woken session no longer sees its own question. Restate it.
            path = transcript_path(job)
            question = pending_question(path) if path else None
            if question:
                prompt = (
                    "Answer to your pending AskUserQuestion "
                    + json.dumps(question, ensure_ascii=False) + ":\n\n" + prompt
                )
        if row.get("pid"):
            stop_session(job["id"])
        proc = claude_run(["--resume", job["session_id"], "--bg", prompt], cwd=job["cwd"])
        output = launch_output(proc)
        launched, copy_id = parse_launch(output)
        if copy_id or (launched and launched != job["id"]):
            stray = copy_id or launched
            claude_run(["stop", stray], timeout=STOP_TIMEOUT)
            die(
                f"Continuing {job['id']} started a copy {stray} instead; the copy was stopped. "
                "Output:\n" + redact_secrets(output.strip()),
                2,
            )
        if proc.returncode != 0 or not launched:
            die(
                f"`claude --resume {job['session_id']} --bg` did not wake the session "
                f"(exit {proc.returncode}):\n" + redact_secrets(output.strip()),
                2,
            )
        job.pop("cancelled_at", None)
        add_turn(job, prompt, "resume")
    print_job_header(job, f"{PERMISSION_MODE} | resume turn {len(job['turns'])}")
    return job


def cmd_task(args):
    prompt = gather_prompt(args)
    if not prompt:
        die("Provide a prompt with an argument or --prompt-file.")
    job = resume_job(args, prompt) if args.resume else start_job(args, prompt)
    if args.follow:
        raise SystemExit(wait_jobs([job["id"]], args.stall_secs))
    print(f"collect: {runner_command()} status {job['id']} --wait")


def cmd_status(args):
    if args.job and args.wait:
        job = find_job(args.job)
        raise SystemExit(wait_jobs([job["id"]], args.stall_secs))
    if args.job:
        job = find_job(args.job)
        _, line = describe_job(job, agents_row(job["id"]), args.stall_secs)
        print(line)
        return
    jobs = all_jobs()
    if not jobs:
        print("No claude-delegate jobs recorded yet.")
        return
    rows = agents_rows()
    shown = 0
    for job in jobs:
        status, line = describe_job(job, agents_row(job["id"], rows), args.stall_secs)
        if status in ("running", "stalled", "blocked") or shown < LIST_RECENT:
            print(line)
            shown += 1


def cmd_wait(args):
    job_ids = []
    for ref in args.jobs:
        job = lookup_job(ref)
        if job is None:
            die(f'Unknown or ambiguous job reference "{ref}".', 64)
        job_ids.append(job["id"])
    if len(set(job_ids)) != len(job_ids):
        die("Duplicate job references given.", 64)
    raise SystemExit(wait_jobs(job_ids, args.stall_secs))


def cmd_progress(args):
    job = find_job(args.job)
    row = agents_row(job["id"])
    page = {
        "schema_version": 2,
        "job_id": job["id"],
        "status": derive_status(job, row),
        "native_state": row.get("state") if row else None,
        "native_status": row.get("status") if row else None,
        "waiting_for": row.get("waitingFor") if row else None,
        "requested_model": job.get("model"),
        "actual_model": observed_model(job),
        "effort": job.get("effort"),
        "transcript": job.get("transcript"),
        "offset": args.offset,
        "next_offset": args.offset,
        "has_more": False,
        "events": [],
    }
    path = transcript_path(job)
    if path is None:
        if args.offset:
            die("Progress offset exceeds the transcript, which does not exist yet.", 2)
    else:
        page["transcript"] = str(path)
        for start, end, record in transcript_records(path, args.offset):
            projected = project_record(record) if record else None
            if projected is not None and len(page["events"]) == args.limit:
                page["has_more"] = True
                break
            page["next_offset"] = end
            if projected is not None:
                page["events"].append({"offset": start, "end_offset": end, **projected})
    print(json.dumps(redact_value(page), ensure_ascii=False, indent=2))


def cmd_result(args):
    job = find_job(args.job)
    row = agents_row(job["id"])
    status = derive_status(job, row, args.stall_secs)
    if status in ("running", "stalled", "blocked"):
        die(
            f"Job {job['id']} is {status}. "
            f"Use `{runner_command()} status {job['id']} --wait` to wait for it.",
            2,
        )
    print(
        redact_secrets(
            f"{job['id']}  {status}  session {job['session_id']}\n"
            f"requested model {job.get('model')}  actual model {observed_model(job) or '(unreported)'}  "
            f"requested effort {job.get('effort')}"
        )
    )
    print()
    if status != "completed":
        _, line = describe_job(job, row, args.stall_secs)
        print(line)
        raise SystemExit(2)
    if not print_final_message(job):
        raise SystemExit(2)


def cmd_cancel(args):
    if args.job:
        job = find_job(args.job)
    else:
        rows = agents_rows()
        active = [
            job for job in all_jobs()
            if derive_status(job, agents_row(job["id"], rows)) in ("running", "stalled", "blocked")
        ]
        if not active:
            die("No active jobs to cancel.", 2)
        if len(active) > 1:
            die("Multiple active jobs (" + ", ".join(job["id"] for job in active) + "); pass a job id.", 2)
        job = active[0]
    with job_lock(job["_dir"]):
        job = load_job(job["_dir"])
        row = agents_row(job["id"])
        status = derive_status(job, row)
        if row is None or not row.get("pid"):
            die(f"Job {job['id']} is {status} with no live process; nothing to cancel.", 2)
        stop_session(job["id"])
        job["cancelled_at"] = now_iso()
        save_job(job)
    print(f"Cancelled {job['id']}; its conversation is kept and `task --resume {job['id']}` continues it.")


def nonnegative_int(value):
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return parsed


def positive_int(value):
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(
        prog="claudectl",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    task = subparsers.add_parser("task", help="start a background Claude Code session")
    task.add_argument(
        "prompt", nargs="*", help="task prompt (combined with --prompt-file when both are present)"
    )
    task.add_argument("--prompt-file")
    task.add_argument(
        "--resume", metavar="ID|last",
        help="send the prompt to an existing job's session (its saved options cannot change)",
    )
    task.add_argument("--model", "-m", help=f"Claude model id (default: {DEFAULT_MODEL})")
    task.add_argument("--effort", choices=("low", "medium", "high", "xhigh", "max"),
                      help=f"requested reasoning effort (default: {DEFAULT_EFFORT})")
    task.add_argument("--cd", help="working directory for Claude (default: current directory)")
    task.add_argument("--add-dir", action="append", metavar="DIR",
                      help="extra working directory for Claude (repeatable)")
    task.add_argument("--name", help="session name shown by claude agents (default: prompt summary)")
    task.add_argument("--follow", action="store_true",
                      help="stay attached until the job settles and print its result")
    task.add_argument("--stall-secs", type=nonnegative_int, default=DEFAULT_STALL_SECS)
    task.set_defaults(func=cmd_task)

    status = subparsers.add_parser("status", help="list jobs or inspect one")
    status.add_argument("job", nargs="?")
    status.add_argument("--wait", action="store_true", help="wait until the job settles")
    status.add_argument("--stall-secs", type=nonnegative_int, default=DEFAULT_STALL_SECS)
    status.set_defaults(func=cmd_status)

    wait = subparsers.add_parser("wait", help="wait for several jobs with one waiter")
    wait.add_argument("jobs", nargs="+", metavar="JOB")
    wait.add_argument("--stall-secs", type=nonnegative_int, default=DEFAULT_STALL_SECS)
    wait.set_defaults(func=cmd_wait)

    progress = subparsers.add_parser("progress", help="page through the session transcript as JSON")
    progress.add_argument("job")
    progress.add_argument("--offset", type=nonnegative_int, default=0, metavar="BYTE")
    progress.add_argument("--limit", type=positive_int, default=20, metavar="COUNT")
    progress.set_defaults(func=cmd_progress)

    result = subparsers.add_parser("result", help="print the final assistant message of a completed job")
    result.add_argument("job", nargs="?")
    result.add_argument("--stall-secs", type=nonnegative_int, default=DEFAULT_STALL_SECS)
    result.set_defaults(func=cmd_result)

    cancel = subparsers.add_parser("cancel", help="stop a running session")
    cancel.add_argument("job", nargs="?")
    cancel.set_defaults(func=cmd_cancel)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
