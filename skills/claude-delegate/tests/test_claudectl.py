import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
import uuid
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
RUNNER = SKILL_DIR / "scripts" / "claudectl.py"

# A stand-in for the Claude Code CLI. It keeps `claude agents --json --all` rows in a
# JSON state file, answers `--bg`, `--resume ... --bg` and `stop` the way Claude Code
# 2.1.274 does on this machine, and logs every argv it receives.
FAKE_CLAUDE = """#!{python}
import json, os, sys
state_path = os.environ["FAKE_CLAUDE_STATE"]
state = json.load(open(state_path))
argv = sys.argv[1:]
with open(os.environ["FAKE_CLAUDE_LOG"], "a") as log:
    log.write(json.dumps({{"argv": argv, "cwd": os.getcwd()}}) + "\\n")

def save():
    json.dump(state, open(state_path, "w"))

def row_by(key, value):
    for row in state["rows"]:
        if row.get(key) == value:
            return row
    return None

if argv[:1] == ["agents"]:
    state["calls"] = state.get("calls", 0) + 1
    for job_id, steps in state.get("transitions", {{}}).items():
        row = row_by("id", job_id)
        for step in steps:
            if row is not None and step["after_calls"] <= state["calls"]:
                row.update({{k: v for k, v in step.items() if k != "after_calls"}})
    save()
    print(json.dumps(state["rows"]))
elif argv[:1] == ["stop"]:
    row = row_by("id", argv[1])
    if row is None:
        print("no such session", file=sys.stderr); sys.exit(1)
    if row.get("state") in ("working", "blocked"):
        row["state"] = "stopped"
    row["pid"] = None
    row["status"] = None
    save()
    print("stopped " + argv[1])
elif "--resume" in argv:
    session = argv[argv.index("--resume") + 1]
    row = row_by("sessionId", session)
    if row is None:
        print("No conversation found with session ID: " + session, file=sys.stderr); sys.exit(1)
    if row.get("pid") or state.get("resume_copy"):
        copy = state.get("copy_id", "c0c0c0c0")
        state["rows"].append({{"id": copy, "kind": "background", "state": "working", "status": "busy",
                               "pid": 999, "sessionId": "cccccccc-0000-4000-8000-000000000000",
                               "name": row.get("name"), "cwd": row.get("cwd")}})
        save()
        print("note: session %s is already running in the background, so this started a copy as %s." % (row["id"], copy))
        print("backgrounded · " + copy)
    else:
        row.update({{"state": "working", "status": "busy", "pid": 4242}})
        save()
        print("note: woke session %s with its saved options (--name, --permission-mode, --settings, --model)." % row["id"])
        print("backgrounded · %s · %s" % (row["id"], row.get("name")))
elif "--bg" in argv:
    launch = state.get("launch") or {{}}
    if launch.get("fail"):
        print(launch["fail"], file=sys.stderr); sys.exit(1)
    name = argv[argv.index("--name") + 1] if "--name" in argv else "unnamed"
    row = {{"id": launch.get("id", "aaaa1111"), "kind": "background", "state": launch.get("state", "working"),
           "status": launch.get("status", "busy"), "pid": launch.get("pid", 111),
           "name": name, "cwd": os.getcwd()}}
    if launch.get("sessionId", "unset") != "unset":
        row["sessionId"] = launch["sessionId"]
    state["rows"].append(row)
    save()
    print("Starting background service…")
    print("backgrounded · %s · %s" % (row["id"], name))
    print("  claude agents             list sessions")
else:
    print("unexpected argv: " + json.dumps(argv), file=sys.stderr); sys.exit(64)
"""


def load_runner():
    spec = importlib.util.spec_from_file_location("claudectl_under_test", RUNNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ClaudeCtlTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.jobs = self.root / "jobs"
        self.jobs.mkdir()
        self.claude_home = self.root / "claude-home"
        (self.claude_home / "projects").mkdir(parents=True)
        self.bindir = self.root / "bin"
        self.bindir.mkdir()
        fake = self.bindir / "claude"
        fake.write_text(FAKE_CLAUDE.format(python=sys.executable), encoding="utf-8")
        fake.chmod(0o755)
        self.state_path = self.root / "fake-state.json"
        self.log_path = self.root / "fake-log.jsonl"
        self.set_state({"rows": [], "calls": 0})
        self.workdir = self.root / "work"
        self.workdir.mkdir()

    def tearDown(self):
        self.tempdir.cleanup()

    # --- fixtures ---------------------------------------------------------------

    def set_state(self, state):
        self.state_path.write_text(json.dumps(state), encoding="utf-8")

    def state(self):
        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def calls(self):
        if not self.log_path.is_file():
            return []
        return [json.loads(line) for line in self.log_path.read_text(encoding="utf-8").splitlines()]

    def make_job(self, job_id, prompt="fixture prompt", session_id=None, **overrides):
        jobdir = self.jobs / job_id
        jobdir.mkdir()
        job = {
            "id": job_id,
            "session_id": session_id or str(uuid.uuid4()),
            "name": "fixture",
            "created_at": "2026-09-17T00:00:00+00:00",
            "cwd": str(self.workdir),
            "model": "claude-fable-5-1[1m]",
            "effort": "xhigh",
            "permission_mode": "bypassPermissions",
            "add_dirs": [],
            "transcript": None,
            "actual_model": None,
            "turns": [{"index": 1, "kind": "task", "started_at": "2026-09-17T00:00:00+00:00"}],
        }
        job.update(overrides)
        (jobdir / "job.json").write_text(json.dumps(job), encoding="utf-8")
        (jobdir / "prompt-1.md").write_text(prompt, encoding="utf-8")
        return job

    def row(self, job, state="working", status: object = "busy", pid: object = 111, **extra):
        return {"id": job["id"], "kind": "background", "state": state, "status": status, "pid": pid,
                "sessionId": job["session_id"], "name": job["name"], "cwd": job["cwd"], **extra}

    def transcript_path(self, job):
        runner = load_runner()
        folder = self.claude_home / "projects" / runner.project_slug(job["cwd"])
        folder.mkdir(parents=True, exist_ok=True)
        return folder / f"{job['session_id']}.jsonl"

    def write_transcript(self, job, records, model="claude-fable-5-1"):
        lines = []
        for record in records:
            if record.get("type") == "assistant":
                record.setdefault("message", {}).setdefault("model", model)
            lines.append((json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8"))
        path = self.transcript_path(job)
        path.write_bytes(b"".join(lines))
        return path, lines

    @staticmethod
    def assistant(*blocks, sidechain=False):
        return {"type": "assistant", "isSidechain": sidechain, "timestamp": "2026-09-17T00:00:01Z",
                "message": {"role": "assistant", "content": list(blocks)}}

    @staticmethod
    def user(content, sidechain=False):
        return {"type": "user", "isSidechain": sidechain, "timestamp": "2026-09-17T00:00:00Z",
                "message": {"role": "user", "content": content}}

    def run_cli(self, *args, cwd=None):
        env = os.environ.copy()
        env.update({
            "CLAUDE_DELEGATE_HOME": str(self.root),
            "CLAUDE_CONFIG_DIR": str(self.claude_home),
            "PATH": str(self.bindir) + os.pathsep + env["PATH"],
            "FAKE_CLAUDE_STATE": str(self.state_path),
            "FAKE_CLAUDE_LOG": str(self.log_path),
        })
        return subprocess.run(
            [sys.executable, str(RUNNER), *args],
            text=True, capture_output=True, env=env, timeout=30, cwd=cwd or str(self.workdir),
        )

    # --- task -----------------------------------------------------------------------

    def test_task_starts_background_session_with_pinned_options(self):
        session = str(uuid.uuid4())
        self.set_state({"rows": [], "calls": 0, "launch": {"id": "ab12cd34", "sessionId": session}})
        result = self.run_cli("task", "Review the plan and report gaps")
        self.assertEqual(result.returncode, 0, result.stderr)
        launch = [call for call in self.calls() if "--bg" in call["argv"]][0]
        argv = launch["argv"]
        self.assertEqual(argv[0], "--bg")
        self.assertEqual(argv[argv.index("--model") + 1], "claude-fable-5-1[1m]")
        self.assertEqual(argv[argv.index("--effort") + 1], "xhigh")
        self.assertEqual(argv[argv.index("--permission-mode") + 1], "bypassPermissions")
        self.assertEqual(json.loads(argv[argv.index("--settings") + 1]), {"worktree": {"bgIsolation": "none"}})
        self.assertEqual(argv[argv.index("--name") + 1], "Review the plan and report gaps")
        self.assertEqual(argv[1], "Review the plan and report gaps")
        self.assertEqual(launch["cwd"], str(self.workdir))
        job = json.loads((self.jobs / "ab12cd34" / "job.json").read_text(encoding="utf-8"))
        self.assertEqual(job["session_id"], session)
        self.assertEqual(job["cwd"], str(self.workdir))
        self.assertEqual(len(job["turns"]), 1)
        self.assertEqual((self.jobs / "ab12cd34" / "prompt-1.md").read_text(encoding="utf-8"),
                         "Review the plan and report gaps")
        for text in ("job: ab12cd34", f"session: {session}", "attach: claude attach ab12cd34", "collect:"):
            self.assertIn(text, result.stdout)

    def test_task_uses_explicit_options_and_prompt_file(self):
        extra = self.root / "evidence"
        extra.mkdir()
        prompt_file = self.root / "task.md"
        prompt_file.write_text("Long brief\nwith two lines", encoding="utf-8")
        self.set_state({"rows": [], "calls": 0, "launch": {"id": "ab12cd35", "sessionId": str(uuid.uuid4())}})
        result = self.run_cli("task", "--model", "claude-opus-5[1m]", "--effort", "high", "--name", "review",
                              "--cd", str(self.workdir), "--add-dir", str(extra), "--prompt-file", str(prompt_file),
                              cwd=str(self.root))
        self.assertEqual(result.returncode, 0, result.stderr)
        argv = [call for call in self.calls() if "--bg" in call["argv"]][0]["argv"]
        self.assertEqual(argv[argv.index("--model") + 1], "claude-opus-5[1m]")
        self.assertEqual(argv[argv.index("--effort") + 1], "high")
        self.assertEqual(argv[argv.index("--name") + 1], "review")
        self.assertEqual(argv[argv.index("--add-dir") + 1:], [str(extra)])
        self.assertEqual(argv[1], "Long brief\nwith two lines")
        job = json.loads((self.jobs / "ab12cd35" / "job.json").read_text(encoding="utf-8"))
        self.assertEqual(job["model"], "claude-opus-5[1m]")
        self.assertEqual(job["effort"], "high")
        self.assertEqual(job["add_dirs"], [str(extra)])

    def test_task_rejects_oversized_prompt_and_launch_failures(self):
        big = self.root / "big.md"
        big.write_text("x" * 100_001, encoding="utf-8")
        result = self.run_cli("task", "--prompt-file", str(big))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("100000 bytes", result.stderr)
        self.assertEqual(self.calls(), [])

        self.set_state({"rows": [], "calls": 0, "launch": {"fail": "Error: --bg is not available here"}})
        result = self.run_cli("task", "do something")
        self.assertEqual(result.returncode, 2)
        self.assertIn("did not start a session", result.stderr)
        self.assertIn("--bg is not available here", result.stderr)
        self.assertEqual(list(self.jobs.iterdir()), [])

        self.set_state({"rows": [], "calls": 0, "launch": {"id": "ab12cd36", "sessionId": None}})
        result = self.run_cli("task", "do something")
        self.assertEqual(result.returncode, 2)
        self.assertIn("never listed its session id", result.stderr)

    # --- status -----------------------------------------------------------------------

    def test_status_maps_native_states_and_gives_next_steps(self):
        cases = {
            "running": dict(state="working", status="busy"),
            "blocked": dict(state="blocked", status="waiting", waitingFor="input needed"),
            "completed": dict(state="done", status="idle"),
            "failed": dict(state="failed", status=None, pid=None),
            "stopped": dict(state="stopped", status=None, pid=None),
        }
        ids = {"running": "aa000001", "blocked": "aa000002", "completed": "aa000003",
               "failed": "aa000004", "stopped": "aa000005"}
        rows = []
        jobs = {}
        for expected, fields in cases.items():
            job = self.make_job(ids[expected], prompt=f"{expected} prompt")
            jobs[expected] = job
            self.write_transcript(job, [self.assistant({"type": "text", "text": "working on it"})])
            rows.append(self.row(job, **fields))
        missing = self.make_job("aa0000ff", prompt="missing prompt")
        jobs["missing"] = missing
        self.set_state({"rows": rows, "calls": 0})

        for expected, job in jobs.items():
            with self.subTest(expected=expected):
                result = self.run_cli("status", job["id"])
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(f"{job['id']}  {expected}", result.stdout)
                self.assertIn(f"{expected} prompt", result.stdout)
        blocked = self.run_cli("status", jobs["blocked"]["id"]).stdout
        self.assertIn("waiting for input needed", blocked)
        self.assertIn(f"task --resume {jobs['blocked']['id']}", blocked)
        self.assertIn(f"claude attach {jobs['blocked']['id']}", blocked)
        self.assertIn("claude rm", self.run_cli("status", missing["id"]).stdout)
        listing = self.run_cli("status")
        self.assertEqual(listing.returncode, 0, listing.stderr)
        for job in jobs.values():
            self.assertIn(job["id"], listing.stdout)

    def test_blocked_status_shows_pending_question(self):
        job = self.make_job("aab10002", prompt="ask me")
        self.write_transcript(job, [
            self.assistant({"type": "tool_use", "id": "q1", "name": "AskUserQuestion",
                            "input": {"questions": [{"question": "alpha or beta?"}]}}),
        ])
        self.set_state({"rows": [self.row(job, state="blocked", status="waiting", waitingFor="input needed")],
                        "calls": 0})
        result = self.run_cli("status", job["id"])
        self.assertIn("alpha or beta?", result.stdout)
        # an answered question is no longer pending
        self.write_transcript(job, [
            self.assistant({"type": "tool_use", "id": "q1", "name": "AskUserQuestion",
                            "input": {"questions": [{"question": "alpha or beta?"}]}}),
            self.user("beta"),
            self.assistant({"type": "text", "text": "CHOSE beta"}),
        ])
        self.assertNotIn("alpha or beta?", self.run_cli("status", job["id"]).stdout)

    def test_quiet_process_with_closed_turn_is_completed_despite_working_state(self):
        job = self.make_job("aa1d1e01")
        finished = [self.user("Reply OK"), self.assistant({"type": "text", "text": "OK"}),
                    {"type": "system", "subtype": "turn_duration", "timestamp": "2026-09-17T00:00:02Z"},
                    {"type": "atis-latch", "value": 1}]
        self.write_transcript(job, finished)
        self.set_state({"rows": [self.row(job, state="working", status="idle")], "calls": 0})
        self.assertIn(f"{job['id']}  completed", self.run_cli("status", job["id"]).stdout)
        result = self.run_cli("result", job["id"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("OK", result.stdout)

        # a turn that is still open keeps the job running
        self.write_transcript(job, finished + [self.user("and now?"), self.assistant({"type": "text", "text": "thinking"})])
        self.assertIn(f"{job['id']}  running", self.run_cli("status", job["id"]).stdout)

        # background work recorded by Claude Code's own state file keeps it running too
        self.write_transcript(job, finished)
        state_dir = self.claude_home / "jobs" / job["id"]
        state_dir.mkdir(parents=True)
        (state_dir / "state.json").write_text(json.dumps({"inFlight": {"tasks": 1, "queued": 0}}), encoding="utf-8")
        self.assertIn(f"{job['id']}  running", self.run_cli("status", job["id"]).stdout)
        (state_dir / "state.json").write_text(json.dumps({"inFlight": {"tasks": 0, "queued": 0}}), encoding="utf-8")
        self.assertIn(f"{job['id']}  completed", self.run_cli("status", job["id"]).stdout)

        # a busy process is never completed, whatever the transcript says
        self.set_state({"rows": [self.row(job, state="done", status="busy")], "calls": 0})
        self.assertIn(f"{job['id']}  running", self.run_cli("status", job["id"]).stdout)

    def test_resume_restates_pending_question_when_answering_a_blocked_job(self):
        job = self.make_job("aae50004")
        question = {"questions": [{"question": "alpha or beta?", "options": [{"label": "alpha.txt"}, {"label": "beta.txt"}]}]}
        self.write_transcript(job, [
            self.user("ask me"),
            self.assistant({"type": "tool_use", "id": "q1", "name": "AskUserQuestion", "input": question}),
        ])
        self.set_state({"rows": [self.row(job, state="blocked", status="waiting", waitingFor="input needed")], "calls": 0})
        result = self.run_cli("task", "--resume", job["id"], "beta.txt")
        self.assertEqual(result.returncode, 0, result.stderr)
        sent = [call["argv"] for call in self.calls() if "--resume" in call["argv"]][0][-1]
        self.assertTrue(sent.startswith("Answer to your pending AskUserQuestion "))
        self.assertIn("alpha or beta?", sent)
        self.assertTrue(sent.endswith("\n\nbeta.txt"))
        self.assertEqual((self.jobs / job["id"] / "prompt-2.md").read_text(encoding="utf-8"), sent)

    def test_records_of_the_retired_runner_are_ignored(self):
        legacy = self.jobs / "cld-0913-120000-ab12"
        legacy.mkdir()
        (legacy / "job.json").write_text(json.dumps({"id": "cld-0913-120000-ab12", "claude_session_id": str(uuid.uuid4())}), encoding="utf-8")
        job = self.make_job("aa1e6ac1")
        self.set_state({"rows": [self.row(job, state="done", status="idle")], "calls": 0})
        listing = self.run_cli("status")
        self.assertEqual(listing.returncode, 0, listing.stderr)
        self.assertIn(job["id"], listing.stdout)
        self.assertNotIn("cld-0913", listing.stdout)

    def test_running_job_with_quiet_transcript_is_stalled(self):
        job = self.make_job("aa57a111")
        path, _ = self.write_transcript(job, [self.assistant({"type": "text", "text": "thinking"})])
        old = time.time() - 2000
        os.utime(path, (old, old))
        self.set_state({"rows": [self.row(job)], "calls": 0})
        result = self.run_cli("status", job["id"])
        self.assertIn(f"{job['id']}  stalled", result.stdout)
        self.assertIn("STALLED", result.stdout)
        self.assertIn(f"claude attach {job['id']}", result.stdout)
        relaxed = self.run_cli("status", job["id"], "--stall-secs", "5000")
        self.assertIn(f"{job['id']}  running", relaxed.stdout)

    # --- resume and cancel -----------------------------------------------------------

    def test_resume_stops_live_process_then_wakes_without_flags(self):
        job = self.make_job("aae50001", prompt="first")
        self.set_state({"rows": [self.row(job, state="done", status="idle", pid=555)], "calls": 0})
        result = self.run_cli("task", "--resume", job["id"], "second question")
        self.assertEqual(result.returncode, 0, result.stderr)
        argvs = [call["argv"] for call in self.calls() if call["argv"][:1] != ["agents"]]
        self.assertEqual(argvs[0], ["stop", job["id"]])
        self.assertEqual(argvs[1], ["--resume", job["session_id"], "--bg", "second question"])
        resumed = [call for call in self.calls() if "--resume" in call["argv"]][0]
        self.assertEqual(resumed["cwd"], str(self.workdir))
        record = json.loads((self.jobs / job["id"] / "job.json").read_text(encoding="utf-8"))
        self.assertEqual([turn["kind"] for turn in record["turns"]], ["task", "resume"])
        self.assertEqual((self.jobs / job["id"] / "prompt-2.md").read_text(encoding="utf-8"), "second question")
        self.assertIn("resume turn 2", result.stdout)
        self.assertEqual(self.state()["rows"][0]["state"], "working")

        # a retired session (no process) is woken without a stop
        self.log_path.unlink()
        self.set_state({"rows": [self.row(job, state="done", status=None, pid=None)], "calls": 0})
        result = self.run_cli("task", "--resume", "last", "third")
        self.assertEqual(result.returncode, 0, result.stderr)
        argvs = [call["argv"] for call in self.calls() if call["argv"][:1] != ["agents"]]
        self.assertEqual(argvs, [["--resume", job["session_id"], "--bg", "third"]])

    def test_resume_refuses_option_overrides_and_unlisted_sessions(self):
        job = self.make_job("aae50002")
        self.set_state({"rows": [self.row(job, state="done", status="idle")], "calls": 0})
        for option in (("--model", "claude-opus-5[1m]"), ("--effort", "high"), ("--cd", str(self.root)),
                       ("--add-dir", str(self.root)), ("--name", "x")):
            with self.subTest(option=option):
                result = self.run_cli("task", "--resume", job["id"], *option, "more")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("saved model", result.stderr)
        self.assertEqual(self.calls(), [])
        self.set_state({"rows": [], "calls": 0})
        result = self.run_cli("task", "--resume", job["id"], "more")
        self.assertEqual(result.returncode, 2)
        self.assertIn("not listed", result.stderr)

    def test_resume_stops_a_stray_copy_and_fails(self):
        job = self.make_job("aae50003")
        self.set_state({"rows": [self.row(job, state="done", status=None, pid=None)], "calls": 0,
                        "resume_copy": True, "copy_id": "c0c0c0c0"})
        result = self.run_cli("task", "--resume", job["id"], "more")
        self.assertEqual(result.returncode, 2)
        self.assertIn("started a copy c0c0c0c0", result.stderr)
        self.assertIn(["stop", "c0c0c0c0"], [call["argv"] for call in self.calls()])
        record = json.loads((self.jobs / job["id"] / "job.json").read_text(encoding="utf-8"))
        self.assertEqual(len(record["turns"]), 1)

    def test_cancel_stops_and_verifies_process_gone(self):
        job = self.make_job("aaca0001")
        self.set_state({"rows": [self.row(job)], "calls": 0})
        result = self.run_cli("cancel", job["id"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(["stop", job["id"]], [call["argv"] for call in self.calls()])
        self.assertIn("Cancelled aaca0001", result.stdout)
        record = json.loads((self.jobs / job["id"] / "job.json").read_text(encoding="utf-8"))
        self.assertIn("cancelled_at", record)
        status = self.run_cli("status", job["id"])
        self.assertIn(f"{job['id']}  stopped", status.stdout)
        self.assertIn("cancelled by claudectl", status.stdout)

        again = self.run_cli("cancel", job["id"])
        self.assertEqual(again.returncode, 2)
        self.assertIn("nothing to cancel", again.stderr)

    # --- progress ---------------------------------------------------------------------

    def test_progress_pages_transcript_records(self):
        job = self.make_job("aa960001")
        path, lines = self.write_transcript(job, [
            {"type": "permission-mode", "mode": "bypassPermissions"},
            self.user("Review note.md"),
            self.assistant(
                {"type": "thinking", "thinking": "private reasoning"},
                {"type": "text", "text": "第一项事实"},
                {"type": "text", "text": "Second fact"},
                {"type": "tool_use", "id": "t1", "name": "Read", "input": {"file_path": "note.md"}},
                {"type": "image", "source": {"type": "base64", "data": "hidden-image"}},
            ),
            self.user([{"type": "tool_result", "tool_use_id": "t1", "content": [
                {"type": "text", "text": "whole file contents"},
                {"type": "image", "source": {"data": "hidden-image"}},
            ]}]),
            self.assistant({"type": "text", "text": "subagent view"}, sidechain=True),
            {"type": "system", "subtype": "turn_duration"},
        ])
        self.set_state({"rows": [self.row(job)], "calls": 0})

        first = self.run_cli("progress", job["id"], "--limit", "2")
        self.assertEqual(first.returncode, 0, first.stderr)
        page = json.loads(first.stdout)
        self.assertEqual(page["schema_version"], 2)
        self.assertEqual(page["status"], "running")
        self.assertEqual(page["native_state"], "working")
        self.assertEqual(page["requested_model"], "claude-fable-5-1[1m]")
        self.assertEqual(page["actual_model"], "claude-fable-5-1")
        self.assertEqual(page["transcript"], str(path))
        self.assertEqual([event["kind"] for event in page["events"]], ["prompt", "message"])
        self.assertEqual(page["events"][0]["texts"], ["Review note.md"])
        self.assertEqual(page["events"][1]["texts"], ["第一项事实", "Second fact"])
        self.assertEqual(page["events"][1]["tools"][0]["name"], "Read")
        self.assertEqual(page["events"][1]["offset"], len(lines[0]) + len(lines[1]))
        self.assertEqual(page["next_offset"], sum(len(line) for line in lines[:3]))
        self.assertTrue(page["has_more"])
        self.assertNotIn("private reasoning", first.stdout)
        self.assertNotIn("hidden-image", first.stdout)

        rest = self.run_cli("progress", job["id"], "--offset", str(page["next_offset"]))
        remaining = json.loads(rest.stdout)
        self.assertEqual([event["kind"] for event in remaining["events"]], ["tool_result", "message"])
        self.assertIn("whole file contents", rest.stdout)
        self.assertTrue(remaining["events"][1]["sidechain"])
        self.assertEqual(remaining["next_offset"], path.stat().st_size)
        self.assertFalse(remaining["has_more"])

    def test_progress_keeps_unfinished_tail_and_rejects_bad_cursors(self):
        job = self.make_job("aa960002")
        self.set_state({"rows": [self.row(job)], "calls": 0})
        before = self.run_cli("progress", job["id"])
        self.assertEqual(before.returncode, 0, before.stderr)
        self.assertEqual(json.loads(before.stdout)["events"], [])
        path = self.transcript_path(job)
        line = json.dumps(self.assistant({"type": "text", "text": "ready"})).encode()
        path.write_bytes(line)
        first = json.loads(self.run_cli("progress", job["id"]).stdout)
        self.assertEqual(first["events"], [])
        self.assertEqual(first["next_offset"], 0)
        with path.open("ab") as stream:
            stream.write(b"\n")
        second = json.loads(self.run_cli("progress", job["id"]).stdout)
        self.assertEqual(len(second["events"]), 1)
        for args in (("--offset", "-1"), ("--offset", "2"), ("--offset", "100000"), ("--limit", "0")):
            with self.subTest(args=args):
                result = self.run_cli("progress", job["id"], *args)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
        path.write_bytes(b"{}\ninvalid\n")
        malformed = self.run_cli("progress", job["id"])
        self.assertNotEqual(malformed.returncode, 0)
        self.assertIn("offset 3", malformed.stderr)

    # --- result and wait --------------------------------------------------------------

    def test_result_prints_last_assistant_text_and_validates_model(self):
        job = self.make_job("aae51001")
        self.write_transcript(job, [
            self.user("Do it"),
            self.assistant({"type": "text", "text": "Starting"}, {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": "ls"}}),
            self.user([{"type": "tool_result", "tool_use_id": "t1", "content": "a.txt"}]),
            self.assistant({"type": "text", "text": "ignored sidechain"}, sidechain=True),
            self.assistant({"type": "text", "text": "Final answer"}, {"type": "text", "text": "with two blocks"}),
        ])
        self.set_state({"rows": [self.row(job, state="done", status="idle")], "calls": 0})
        result = self.run_cli("result", job["id"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Final answer\n\nwith two blocks", result.stdout)
        self.assertNotIn("ignored sidechain", result.stdout)
        self.assertIn("actual model claude-fable-5-1", result.stdout)

        wrong = self.make_job("aae51002", model="claude-opus-5[1m]")
        self.write_transcript(wrong, [self.assistant({"type": "text", "text": "Final"})])
        self.set_state({"rows": [self.row(job, state="done", status="idle"), self.row(wrong, state="done", status="idle")], "calls": 0})
        result = self.run_cli("result", wrong["id"])
        self.assertEqual(result.returncode, 2)
        self.assertIn("result withheld", result.stdout)
        self.assertIn("requested 'claude-opus-5[1m]'", result.stdout)
        self.assertNotIn("Final\n", result.stdout)

    def test_result_refuses_unfinished_and_failed_jobs(self):
        job = self.make_job("aae51003")
        self.write_transcript(job, [self.assistant({"type": "text", "text": "partial"})])
        for fields, text in ((dict(state="working", status="busy"), "is running"),
                             (dict(state="blocked", status="waiting", waitingFor="input needed"), "is blocked")):
            with self.subTest(fields=fields):
                self.set_state({"rows": [self.row(job, **fields)], "calls": 0})
                result = self.run_cli("result", job["id"])
                self.assertEqual(result.returncode, 2)
                self.assertIn(text, result.stderr)
        self.set_state({"rows": [self.row(job, state="failed", status=None, pid=None)], "calls": 0})
        result = self.run_cli("result", job["id"])
        self.assertEqual(result.returncode, 2)
        self.assertIn("FAILED", result.stdout)
        self.assertNotIn("partial", result.stdout)

    def test_wait_settles_a_fleet_with_exit_codes(self):
        done = self.make_job("aa0a1001", prompt="one")
        self.write_transcript(done, [self.assistant({"type": "text", "text": "One is done"})])
        blocked = self.make_job("aa0a1002", prompt="two")
        self.set_state({
            "rows": [self.row(done), self.row(blocked, state="blocked", status="waiting", waitingFor="permission prompt")],
            "calls": 0,
            "transitions": {done["id"]: [{"after_calls": 2, "state": "done", "status": "idle"}]},
        })
        result = self.run_cli("wait", done["id"], blocked["id"])
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertIn("One is done", result.stdout)
        self.assertIn(f"{blocked['id']}  blocked", result.stdout)
        self.assertIn("fleet summary:", result.stdout)
        self.assertGreaterEqual(len([c for c in self.calls() if c["argv"][:1] == ["agents"]]), 2)

        failed = self.make_job("aa0a1003", prompt="three")
        self.set_state({"rows": [self.row(done, state="done", status="idle"), self.row(failed, state="failed", status=None, pid=None)], "calls": 0})
        result = self.run_cli("wait", done["id"], failed["id"])
        self.assertEqual(result.returncode, 2)
        only = self.run_cli("status", done["id"], "--wait")
        self.assertEqual(only.returncode, 0, only.stderr)
        self.assertIn("One is done", only.stdout)

    # --- redaction ----------------------------------------------------------------------

    def test_displayed_surfaces_redact_secrets_without_changing_raw_files(self):
        secret = "SYNTHETIC_SECRET_TAIL_123456"
        prompt = json.dumps({"api_key": 'alpha"' + secret, "keep": "preserved"})
        job = self.make_job("aaed0001", prompt=prompt)
        path, _ = self.write_transcript(job, [
            self.assistant({"type": "text", "text": f"token={secret} keep=preserved"},
                           {"type": "tool_use", "id": "t1", "name": "configure",
                            "input": {"Authorization": f"Bearer {secret}", "password": secret, "keep": "preserved"}}),
        ])
        raw = path.read_bytes()
        self.set_state({"rows": [self.row(job, state="done", status="idle")], "calls": 0})
        for command in ("status", "result", "progress"):
            with self.subTest(command=command):
                result = self.run_cli(command, job["id"])
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotIn(secret, result.stdout + result.stderr)
                self.assertIn("[REDACTED]", result.stdout)
                self.assertIn("preserved", result.stdout)
        page = json.loads(self.run_cli("progress", job["id"]).stdout)
        projected = page["events"][0]["tools"][0]["input"]
        self.assertEqual(projected["Authorization"], "[REDACTED]")
        self.assertEqual(projected["password"], "[REDACTED]")
        self.assertEqual(projected["keep"], "preserved")
        self.assertEqual(path.read_bytes(), raw)
        self.assertEqual((self.jobs / job["id"] / "prompt-1.md").read_text(encoding="utf-8"), prompt)

    def test_quoted_authorization_values_redact_without_marker_mangling(self):
        runner = load_runner()
        cases = {
            "empty-quoted": ("Authorization: '' empty-quoted", "Authorization: '[REDACTED]' empty-quoted"),
            "single-quoted-scheme-value": ("Authorization: 'Bearer claudeysentone' end", "Authorization: 'Bearer [REDACTED]' end"),
            "double-quoted-scheme-value": ('Authorization: "Bearer claudeysenttwo" end', 'Authorization: "Bearer [REDACTED]" end'),
            "single-quoted-value": ("Authorization: 'claudeysentthree'", "Authorization: '[REDACTED]'"),
            "bare-labeled": ("password=xK)claudetailleak9A rest", "password=[REDACTED] rest"),
            "url-userinfo": ("https://user:claudeurlsecret@example.com/x", "https://[REDACTED]@example.com/x"),
        }
        for name, (sample, expected) in cases.items():
            with self.subTest(case=name):
                displayed = runner.redact_secrets(sample)
                self.assertEqual(displayed, expected)
                self.assertNotIn("[REDACTED]]", displayed)


if __name__ == "__main__":
    unittest.main()
