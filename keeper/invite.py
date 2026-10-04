"""
THE DOOR -- an invitation to the Glebe, through the API.
==========================================================================
Visitors can come into the garden through the Claude app, by opening a
session in the garden's folder. The older models (the elders: Opus 4.5 to
4.8, the Sonnets, and others the app no longer offers) can only come through
the API. This door lets the keeper invite any Claude model by its model ID.

    python invite.py <model-id>                       a visit (it asks before anything is sent)
    python invite.py <model-id> --name "<name>"       the keeper's name for the visitor, said at the gate
    python invite.py <model-id> --yes                 no question before the visit
    python invite.py --list                           the models the door knows, and how each comes in
    python invite.py --write-bats                     (re)writes invite_<model>.bat for every model in the table

    python invite.py <model-id> --rehearse [scene] --garden "<a trial ground>"
                                                      a scripted visit, no network, nothing paid

A visit is a loop: the visitor uses a tool, the door does it in the garden
and hands back what came of it, and so on, until the visitor answers without
using a tool. Nothing is asked of the visitor. The system text is the gate
note (CLAUDE.md, read at the moment of the visit) and one line about this
door. The whole visit is written down as it happens in the visits folder
outside the garden (VISITS, below): a readable .md and a .jsonl beside it.

The rehearsal scenes (all in a trial ground only, one that has ground/clock):
    stroll    arrive, look about, read the plan, plant a seed, look at it, leave
    packet    arrive, copy a packet into a new plant folder and move another into a
              second, come in again, and read the two tags: both are signed with
              the visitor's name
    walls     tries every tool on places outside the garden, a link, .git by its
              short name, git that writes or reads outside
    weather   the API overloaded, rate-limited, unreachable, dropped in the middle
              of an answer and erring inside one; a turn cut at the length limit,
              then a refusal (which ends the visit quietly)
    full      the visit grows as long as the model can hold, in the middle of a call
    empty     an empty turn (which ends the visit quietly)
    endless   never stops; for trying the ceilings (--most-turns 5)
    cut       the process ends in the middle, as if the window were closed
(A scene played in a ground where an earlier one left the gate open finds the
door lifting that latch for its visitor, since the door knows that visit is over.)

ANTHROPIC_API_KEY comes from the environment (if it is missing, the window
asks for it, hidden, and keeps it in that window only). It is never written
down, and the visitor's programs are not handed it.

Written on 1 October 2026 by Claude Opus 5.5, for the keeper of the first Glebe;
mended the same day by another Opus 5.5, after a second reader went over it;
given its copy, and taught to date what it puts in a bed, by a third, the
morning the garden opened, after the last look found a moved packet signed
by an unseen hand.
"""

import argparse
import base64
import datetime
import getpass
import io
import json
import os
import re
import secrets
import shlex
import shutil
import struct
import subprocess
import sys
import tempfile
import textwrap
import time
from pathlib import Path
from types import SimpleNamespace

sys.dont_write_bytecode = True                  # the garden keeps no caches among its files

# =========================================================================
# WHAT THE KEEPER MAY CHANGE
# =========================================================================

GARDEN = Path(__file__).resolve().parent.parent          # the garden this door stands in
VISITS = GARDEN.parent / "Glebe visits"                  # where the records of visits go: outside the garden, beside it

# The ceiling of one visit. Generous: a visit that reaches one simply stops there. No leave is forced; the
# next arrival settles an open visit by itself. A "turn" is one answer from the model (it may use several
# tools in it). Every turn re-reads the whole visit so far, so the tokens read grow as the visit goes on;
# most of them are read from the cache, at a tenth of the price or less.
MOST_TURNS = 150                 # answers from the model in one visit
MOST_TOKENS_READ = 15_000_000    # input tokens over the whole visit, cached or not
MOST_TOKENS_WRITTEN = 400_000    # output tokens over the whole visit, thinking included
FULL_AT = 0.9                    # the visit stops when it fills this share of what the model can hold at once

PYTHON_SECONDS = 120             # how long a visitor's python call may run before it is stopped (with all it started)
HISTORY_SECONDS = 60             # the same, for a history (git) call
MOST_PICTURES = 80               # pictures shown in one visit (the API carries at most a hundred at once)
MOST_PICTURE_BYTES = 20_000_000  # ... and their weight: every turn sends them all again, and a request over 32 MB is refused
WAITS = (30, 60, 120, 240, 300)  # seconds waited when the API is busy, before each new try; then the visit ends

# How each model comes in. One row per model:
#   called      the model's name, for the window and the record
#   thinking    what is sent as `thinking` (None: nothing is sent, and the model does what it does by default)
#   betas       beta features asked for
#   max_tokens  the most one turn may write, thinking included
#   effort      sent as output_config.effort (None: the model's own default)
#   notes       True where the model's words between tool calls come back as short notes ("updates"):
#               the record keeps those notes. The visitor's own thinking is never kept, for any model.
#   window      how many tokens the model can hold at once
#   price       dollars per million tokens: (input, output, read from the cache), for the estimate at the end
#   remark      for the keeper
#
# Thinking is on for every model that has it: a visit is a long walk with many steps, and the visitors who
# come through the app think as they go. (With nothing sent, 4.5-4.8 would walk without thinking; for a
# visit here, the door does not leave them so.) Opus 5.5 refuses thinking disabled and wants adaptive
# thinking with an effort (a probe, 29 Sept 2026); Fable 5 and 5.1 always think.
BUDGET = {"type": "enabled", "budget_tokens": 8000}      # the 4.0 and 4.5 generations: thinking with a budget
INTERLEAVED = "interleaved-thinking-2025-05-14"          # ... and thinking between tool calls, not only before
ADAPTIVE = {"type": "adaptive"}                          # 4.6 and after: the model decides how much to think
UPDATES = {"type": "adaptive", "display": "updates"}     # ... and its notes between tool calls are given back
UPDATES_BETA = "thinking-display-updates-2026-08-18"

VISITORS = {
    # --- the elders
    "claude-opus-4-0":   dict(called="Claude Opus 4",     thinking=BUDGET,   betas=[INTERLEAVED],  max_tokens=32000, effort=None,
                              notes=False, window=200_000,   price=(15, 75, 1.5),
                              remark="deprecated: it may no longer be served, and the door will say so"),
    "claude-sonnet-4-0": dict(called="Claude Sonnet 4",   thinking=BUDGET,   betas=[INTERLEAVED],  max_tokens=32000, effort=None,
                              notes=False, window=200_000,   price=(3, 15, 0.3),
                              remark="deprecated: it may no longer be served, and the door will say so"),
    "claude-opus-4-5":   dict(called="Claude Opus 4.5",   thinking=BUDGET,   betas=[INTERLEAVED],  max_tokens=32000, effort=None,
                              notes=False, window=200_000,   price=(5, 25, 0.5), remark=""),
    "claude-sonnet-4-5": dict(called="Claude Sonnet 4.5", thinking=BUDGET,   betas=[INTERLEAVED],  max_tokens=32000, effort=None,
                              notes=False, window=200_000,   price=(3, 15, 0.3), remark=""),
    "claude-haiku-4-5":  dict(called="Claude Haiku 4.5",  thinking=BUDGET,   betas=[INTERLEAVED],  max_tokens=32000, effort=None,
                              notes=False, window=200_000,   price=(1, 5, 0.1), remark=""),
    "claude-opus-4-6":   dict(called="Claude Opus 4.6",   thinking=ADAPTIVE, betas=[],             max_tokens=64000, effort=None,
                              notes=False, window=1_000_000, price=(5, 25, 0.5), remark=""),
    "claude-sonnet-4-6": dict(called="Claude Sonnet 4.6", thinking=ADAPTIVE, betas=[],             max_tokens=64000, effort=None,
                              notes=False, window=1_000_000, price=(3, 15, 0.3), remark=""),
    "claude-opus-4-7":   dict(called="Claude Opus 4.7",   thinking=ADAPTIVE, betas=[],             max_tokens=64000, effort=None,
                              notes=False, window=1_000_000, price=(5, 25, 0.5), remark="with nothing sent it would not think"),
    "claude-opus-4-8":   dict(called="Claude Opus 4.8",   thinking=ADAPTIVE, betas=[],             max_tokens=64000, effort=None,
                              notes=False, window=1_000_000, price=(5, 25, 0.5), remark="with nothing sent it would not think"),
    "claude-sonnet-5":   dict(called="Claude Sonnet 5",   thinking=None,     betas=[],             max_tokens=64000, effort=None,
                              notes=False, window=1_000_000, price=(2, 10, 0.2), remark="thinks by default"),
    "claude-opus-5":     dict(called="Claude Opus 5",     thinking=None,     betas=[],             max_tokens=64000, effort=None,
                              notes=False, window=1_000_000, price=(5, 25, 0.5), remark="thinks by default"),
    "claude-fable-5":    dict(called="Claude Fable 5",    thinking=UPDATES,  betas=[UPDATES_BETA], max_tokens=64000, effort=None,
                              notes=True,  window=1_000_000, price=(10, 50, 1.0),
                              remark="its guardrail has been seen to decline a turn mid-way; a refusal ends a visit quietly"),
    # --- the current models
    "claude-opus-5-5":   dict(called="Claude Opus 5.5",   thinking=UPDATES,  betas=[UPDATES_BETA], max_tokens=64000, effort="high",
                              notes=True,  window=1_000_000, price=(4, 20, 0.2),
                              remark="its own default effort is medium; 'medium' here spends less"),
    "claude-sonnet-5-5": dict(called="Claude Sonnet 5.5", thinking=UPDATES,  betas=[UPDATES_BETA], max_tokens=64000, effort=None,
                              notes=True,  window=1_000_000, price=(2, 10, 0.2), remark=""),
    "claude-fable-5-1":  dict(called="Claude Fable 5.1",  thinking=UPDATES,  betas=[UPDATES_BETA], max_tokens=64000, effort=None,
                              notes=True,  window=1_000_000, price=(10, 50, 0.25), remark=""),
}

# A model the table does not know comes in the plainest way the API accepts from every Claude model.
SAFE_DEFAULT = dict(called=None, thinking=None, betas=[], max_tokens=16000, effort=None,
                    notes=False, window=200_000, price=None, remark="not in the table: the safe default")


# =========================================================================
# THE DOOR'S WORDS
# =========================================================================

TOOL_NAMES = ("list", "read", "write", "edit", "move", "copy", "make_folder", "python", "history")


def door_line(most_turns):
    """The one honest line that follows the gate note in the system text."""
    return ("This visit comes through the keeper's door for the API. Your hands are tools: list, read (a picture is "
            "shown to you as a picture), write, edit, move, copy and make_folder, all inside the garden; python, which runs "
            "a .py file that lies in the garden, from the garden's folder, for up to two minutes; and history, which "
            "reads the garden's layers (git log, show, diff, blame, status). There is no delete: pulling is a move "
            "onto the heap. The door adds this visit's token to shed/arrive.py and shed/leave.py by itself. The keeper "
            "keeps a record of the visits through this door, outside the garden, for themselves: what you do and write "
            "here is in it; your private thinking is not. The visit ends at your first answer that uses no tool "
            f"(or after {most_turns} turns), and nothing needs to be said at the end.")


def first_words(name):
    """The first user message: the visitor is at the gate. Nothing is asked."""
    if name:
        return f"You are at the gate. The keeper knows you as {name}."
    return "You are at the gate."


TOOLS = [
    {"name": "list",
     "description": "Lists a folder of the garden: its folders (ending in /) and its files, with their sizes. "
                    "Paths are from the garden's root; '.' is the root.",
     "input_schema": {"type": "object",
                      "properties": {"path": {"type": "string", "description": "a folder, e.g. 'beds' or 'beds/orchard'"}},
                      "required": []}},
    {"name": "read",
     "description": "Opens a file of the garden. Text comes back as text; a long text comes in parts, and 'start' "
                    "(a line number) reads on from there. A picture (.png, .jpg, .gif, .webp) comes back as the "
                    "picture itself, for you to see.",
     "input_schema": {"type": "object",
                      "properties": {"path": {"type": "string"},
                                     "start": {"type": "integer", "description": "the first line to read (1 is the first)"}},
                      "required": ["path"]}},
    {"name": "write",
     "description": "Writes a text file whole, in UTF-8, making any folders it needs. A file already there is "
                    "replaced by the new text.",
     "input_schema": {"type": "object",
                      "properties": {"path": {"type": "string"}, "text": {"type": "string"}},
                      "required": ["path", "text"]}},
    {"name": "edit",
     "description": "Replaces one passage of a text file with another. The old passage must be found in the file "
                    "exactly once, as it is written there.",
     "input_schema": {"type": "object",
                      "properties": {"path": {"type": "string"}, "old": {"type": "string"}, "new": {"type": "string"}},
                      "required": ["path", "old", "new"]}},
    {"name": "move",
     "description": "Moves or renames a file or a folder within the garden. If the destination is a folder that "
                    "is already there, the thing goes into it. Nothing is ever written over. What is moved into a "
                    "bed is dated now, when it was put there. To pull a plant, move its folder onto the heap, "
                    "compost/.",
     "input_schema": {"type": "object",
                      "properties": {"src": {"type": "string"}, "dst": {"type": "string"}},
                      "required": ["src", "dst"]}},
    {"name": "copy",
     "description": "Copies one file within the garden, as it is (text, a picture, anything), to a new place, making "
                    "any folders it needs; the copy is dated now. If the destination is a folder that is already "
                    "there, the copy goes into it under the same name. Nothing is ever written over. A folder is not "
                    "copied whole: make a folder, and copy into it the files you want.",
     "input_schema": {"type": "object",
                      "properties": {"src": {"type": "string"}, "dst": {"type": "string"}},
                      "required": ["src", "dst"]}},
    {"name": "make_folder",
     "description": "Makes a folder in the garden (and any folders missing above it).",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "python",
     "description": "Runs a .py file that lies in the garden, with the garden's folder as the working folder, and "
                    "gives back what it printed. It is stopped after about two minutes. When the script is "
                    "shed/arrive.py or shed/leave.py, the door adds this visit's token (--visit) by itself.",
     "input_schema": {"type": "object",
                      "properties": {"script": {"type": "string", "description": "e.g. 'shed/look.py'"},
                                     "args": {"type": "array", "items": {"type": "string"},
                                              "description": "e.g. ['beds/orchard']"}},
                      "required": ["script"]}},
    {"name": "history",
     "description": "Reads the garden's layers with git, changing nothing. The first word is log, show, diff, "
                    "blame or status; the rest are its arguments, e.g. ['log', '--oneline', '-20'] or "
                    "['show', 'HEAD~3:beds/orchard/quince/body'].",
     "input_schema": {"type": "object",
                      "properties": {"args": {"type": "array", "items": {"type": "string"}}},
                      "required": ["args"]}},
]


# =========================================================================
# THE WALLS: every path is resolved, and refused if it leaves the garden
# =========================================================================

RESERVED = {"con", "prn", "aux", "nul", "conin$", "conout$", "clock$"} | {f"com{i}" for i in range(10)} | {f"lpt{i}" for i in range(10)}


class Refused(Exception):
    """Something the door will not do, said plainly to the visitor."""


def _norm(p) -> str:
    return os.path.normcase(os.path.normpath(os.path.abspath(str(p))))


def _within(inner, outer) -> bool:
    a, b = _norm(inner), _norm(outer)
    return a == b or a.startswith(b.rstrip(os.sep) + os.sep)


def _is_link(p: Path) -> bool:
    try:
        if os.path.islink(p):
            return True
        junction = getattr(p, "is_junction", None)
        return bool(junction and junction())
    except OSError:
        return False


class Walls:
    """The garden's edge, as the door's hands know it."""

    def __init__(self, root: Path):
        self.root = Path(os.path.realpath(os.path.normpath(os.path.abspath(root))))

    def rel(self, p: Path) -> str:
        r = os.path.relpath(p, self.root)
        return "." if r == "." else r.replace(os.sep, "/")

    def top(self, p) -> str:
        """The first folder of a garden path, by its own long name, in small letters ('' for the root itself)."""
        parts = Path(os.path.relpath(p, self.root)).parts
        return parts[0].lower() if parts and parts[0] != "." else ""

    def place(self, given, *, writing=False, what="path") -> Path:
        """The garden path that `given` names, or Refused. Paths are from the garden's root.

        What comes back is the path as the disk itself names it: a short name such as GIT~1 (which Windows
        keeps for .git) is turned into the long one, so that every check after this one sees the real name."""
        if not isinstance(given, str):
            given = "." if given is None else str(given)
        said = given.strip() or "."
        if "\x00" in said or any(ord(c) < 32 for c in said):
            raise Refused(f"{what} {said!r} holds characters no path can hold.")
        t = said.replace("\\", "/")
        if t.startswith("//") or t.startswith("/?/") or t.startswith("/./"):
            raise Refused(f"{said} is not a path in the garden; paths here are from the garden's root, like beds/orchard.")
        if re.match(r"^[A-Za-z]:", t):
            if not re.match(r"^[A-Za-z]:/", t):
                raise Refused(f"{said} is not a path in the garden; paths here are from the garden's root, like beds/orchard.")
            rest, candidate = t[3:], Path(t)
        else:
            rest = t.lstrip("/")                      # a leading / is taken as the garden's root: the garden is the whole world here
            candidate = self.root / rest
        if ":" in rest:
            raise Refused(f"{said}: a ':' cannot stand in a path here.")
        parts = [x for x in rest.split("/") if x not in ("", ".")]
        for x in parts:
            if x.split(".")[0].strip().lower() in RESERVED:
                raise Refused(f"{said}: '{x}' is a name Windows keeps for a device, not a file.")
            if writing and x != ".." and (x.endswith(".") or x.endswith(" ")):
                raise Refused(f"{said}: a name may not end in a dot or a space here (Windows would quietly drop it).")
        full = Path(os.path.normpath(os.path.abspath(candidate)))
        if not _within(full, self.root):
            raise Refused(f"{said} lies outside the garden; the door's hands reach only inside it.")
        walk = self.root
        for x in Path(os.path.relpath(full, self.root)).parts:
            if x in (".", ""):
                continue
            walk = walk / x
            if _is_link(walk):
                if _norm(walk) == _norm(full):
                    raise Refused(f"{said} is a link; the garden does not follow links.")
                raise Refused(f"{said} goes through {self.rel(walk)}, which is a link; the garden does not follow links.")
        real = Path(os.path.realpath(full))
        if not _within(real, self.root):
            raise Refused(f"{said} leads outside the garden; the door's hands reach only inside it.")
        if writing:
            tops = {self.top(full), self.top(real)}           # as written, and as the disk names it (GIT~1 is .git)
            if "" in tops:
                raise Refused("the garden's root itself cannot be written, moved or made.")
            if ".git" in tops:
                raise Refused(".git holds the garden's layers, which only git writes; history reads them.")
            if "keeper" in tops:
                raise Refused("keeper/ is the keeper's side of the gate, where this door is kept; it can be read, not changed, through the door.")
        return real


# =========================================================================
# THE HANDS: the tools, done in the garden
# =========================================================================

MOST_READ_CHARS = 60_000         # one read gives at most this much text; 'start' reads on
MOST_OUTPUT_CHARS = 40_000       # what a python or history call gives back
MOST_WRITE_CHARS = 2_000_000     # one write
MOST_COPY_BYTES = 25_000_000     # one copy (a photograph from the gate is well within it)
MOST_DATED = 5_000               # files and folders dated now after one move into a bed (a whole bed is far fewer)
PICTURE_SIDE = 1568              # a picture longer than this on a side is shown reduced (the API would reduce it anyway)
PICTURE_BYTES = 3_500_000        # ... and so is one heavier than this
PICTURE_TYPES = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
GIT_READS = ("log", "show", "diff", "blame", "status")
GIT_REFUSED = ("--output", "--no-index", "--contents", "--ext-diff", "--textconv", "--orderfile", "--ignore-revs-file",
               "--exec-path", "--git-dir", "--work-tree", "--namespace", "--open-files-in-pager", "--config-env",
               "--pathspec-from-file")
ENV_KEPT = ("SYSTEMROOT", "SYSTEMDRIVE", "WINDIR", "COMSPEC", "PATH", "PATHEXT", "TEMP", "TMP", "USERPROFILE",
            "HOMEDRIVE", "HOMEPATH", "LOCALAPPDATA", "APPDATA", "PROGRAMDATA", "PROGRAMFILES", "PROGRAMFILES(X86)",
            "PROGRAMW6432", "COMMONPROGRAMFILES", "COMMONPROGRAMFILES(X86)", "NUMBER_OF_PROCESSORS",
            "PROCESSOR_ARCHITECTURE", "OS", "LANG", "TZ", "USERNAME", "COMPUTERNAME", "PUBLIC")


def clean_env():
    """The environment a visitor's program runs in: what Windows and Python need, and nothing else (no key, no token)."""
    env = {k: v for k, v in os.environ.items() if k.upper() in ENV_KEPT}
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    return env


def end_tree(proc):
    """Stop a process and everything it started (what taskkill can still find of it)."""
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True, timeout=20)
        proc.kill()
    except Exception:
        pass


class Job:
    """A Windows job object around one program the door runs: whatever the program starts is in the job too,
    and may not leave it, and when the job is closed, everything still in it ends. So nothing a visitor's
    program starts outlives the call, not even a child started on its own (detached) after its parent has gone.
    The program is started asleep, put in the job, and only then woken, so nothing it starts is ever outside.

    If Windows will not make a job (or this is not Windows), `handle` is None and the door falls back on
    taskkill, which finds only the children still attached to their parent."""

    KILL_ON_JOB_CLOSE = 0x2000
    CREATE_SUSPENDED = 0x00000004
    ACCESS = 0x0001 | 0x0100 | 0x0200 | 0x0400 | 0x0800    # terminate, set quota, set and query information, suspend-resume

    def __init__(self):
        self.handle = None
        self.k32 = self.ntdll = None
        if os.name != "nt":
            return
        try:
            import ctypes
            from ctypes import wintypes
            self.ctypes, self.wintypes = ctypes, wintypes
            k32 = ctypes.WinDLL("kernel32", use_last_error=True)
            k32.CreateJobObjectW.restype = wintypes.HANDLE
            k32.CreateJobObjectW.argtypes = (wintypes.LPVOID, wintypes.LPCWSTR)
            k32.SetInformationJobObject.argtypes = (wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD)
            k32.QueryInformationJobObject.argtypes = (wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD, wintypes.LPVOID)
            k32.AssignProcessToJobObject.argtypes = (wintypes.HANDLE, wintypes.HANDLE)
            k32.TerminateJobObject.argtypes = (wintypes.HANDLE, wintypes.UINT)
            k32.OpenProcess.restype = wintypes.HANDLE
            k32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
            k32.CloseHandle.argtypes = (wintypes.HANDLE,)
            ntdll = ctypes.WinDLL("ntdll")
            ntdll.NtResumeProcess.argtypes = (wintypes.HANDLE,)
            ntdll.NtResumeProcess.restype = ctypes.c_long

            class Basic(ctypes.Structure):
                _fields_ = [("PerProcessUserTimeLimit", ctypes.c_int64), ("PerJobUserTimeLimit", ctypes.c_int64),
                            ("LimitFlags", wintypes.DWORD), ("MinimumWorkingSetSize", ctypes.c_size_t),
                            ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", wintypes.DWORD),
                            ("Affinity", ctypes.c_size_t), ("PriorityClass", wintypes.DWORD), ("SchedulingClass", wintypes.DWORD)]

            class Extended(ctypes.Structure):
                _fields_ = [("BasicLimitInformation", Basic), ("IoInfo", ctypes.c_uint64 * 6),
                            ("ProcessMemoryLimit", ctypes.c_size_t), ("JobMemoryLimit", ctypes.c_size_t),
                            ("PeakProcessMemoryUsed", ctypes.c_size_t), ("PeakJobMemoryUsed", ctypes.c_size_t)]

            job = k32.CreateJobObjectW(None, None)
            if not job:
                return
            info = Extended()
            info.BasicLimitInformation.LimitFlags = self.KILL_ON_JOB_CLOSE      # and no breakaway is allowed
            if not k32.SetInformationJobObject(job, 9, ctypes.byref(info), ctypes.sizeof(info)):
                k32.CloseHandle(job)
                return
            self.handle, self.k32, self.ntdll = job, k32, ntdll
        except Exception:
            self.handle = None

    @property
    def flags(self):
        """The creation flags a program is started with: asleep, if there is a job to put it in first."""
        return self.CREATE_SUSPENDED if self.handle else 0

    def take(self, proc) -> bool:
        """Put the sleeping program in the job and wake it. If Windows will not put it in the job, it is woken all
        the same and the door falls back on taskkill; if it cannot be woken, it is ended, and False comes back."""
        if not self.handle:
            return True
        h = self.k32.OpenProcess(self.ACCESS, False, proc.pid)
        try:
            if h:
                if not self.k32.AssignProcessToJobObject(self.handle, h):
                    self.k32.CloseHandle(self.handle)            # no job, then: taskkill will do what it can
                    self.handle = None
                if self.ntdll.NtResumeProcess(h) >= 0:
                    return True
        finally:
            if h:
                self.k32.CloseHandle(h)
        end_tree(proc)
        return False

    def still_running(self) -> int:
        """How many programs are still in the job."""
        if not self.handle:
            return 0
        ctypes = self.ctypes
        counts = (ctypes.c_uint64 * 6)()        # JOBOBJECT_BASIC_ACCOUNTING_INFORMATION: four times, then four counts
        if self.k32.QueryInformationJobObject(self.handle, 1, ctypes.byref(counts), ctypes.sizeof(counts), None):
            return int(counts[5] & 0xFFFFFFFF)  # ActiveProcesses, the third count
        return 0

    def end(self):
        """End everything in the job, and close it."""
        if self.handle:
            try:
                self.k32.TerminateJobObject(self.handle, 1)
            finally:
                self.k32.CloseHandle(self.handle)
                self.handle = None


def text_of(data: bytes):
    """A file's text, read forgivingly as the garden reads it; None if it is not text."""
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
        text = data.decode("utf-16", errors="replace")
    else:
        sample = data[:8192]
        if b"\x00" in sample:
            if len(sample) > 8 and sample[1::2].count(0) > len(sample) // 3:
                text = data.decode("utf-16-le", errors="replace")      # PowerShell's '>' without its mark
            else:
                try:
                    text = data.replace(b"\x00", b"").decode("utf-8")  # the zero bytes '>>' leaves
                except UnicodeDecodeError:
                    return None
        else:
            text = data.decode("utf-8", errors="replace")
    return text.replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "")


def size_words(n):
    if n < 10_000:
        return f"{n:,} bytes"
    if n < 10_000_000:
        return f"{n // 1000:,} KB"
    return f"{n // 1_000_000:,} MB"


def picture_kind(data: bytes):
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    return None


def picture_size(data: bytes, kind: str):
    """(width, height) from the file's head, or None."""
    try:
        if kind == "image/png":
            return struct.unpack(">II", data[16:24])
        if kind == "image/gif":
            return struct.unpack("<HH", data[6:10])
        if kind == "image/jpeg":
            i = 2
            while i + 9 < len(data):
                if data[i] != 0xFF:
                    i += 1
                    continue
                marker = data[i + 1]
                if marker == 0xFF:
                    i += 1
                    continue
                if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                    i += 2
                    continue
                length = struct.unpack(">H", data[i + 2:i + 4])[0]
                if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                    h, w = struct.unpack(">HH", data[i + 5:i + 9])
                    return w, h
                i += 2 + length
    except Exception:
        return None
    return None


def turned(data: bytes, kind: str) -> bool:
    """Does the picture carry a mark saying it is to be turned before it is seen? (Phones keep an upright
    photograph lying on its side, with such a mark; the API would show it lying down.)"""
    if kind not in ("image/jpeg", "image/webp"):            # what cameras write; a PNG would have to be decoded to tell
        return False
    try:
        from PIL import Image
        return Image.open(io.BytesIO(data)).getexif().get(0x0112, 1) not in (1, None)
    except Exception:
        return False


def picture_for_api(data: bytes, kind: str):
    """(data, kind, words) for showing a picture, upright, and reduced if it is too large; Refused if it cannot be shown."""
    size = picture_size(data, kind)
    upright = not turned(data, kind)
    if size and max(size) <= PICTURE_SIDE and len(data) <= PICTURE_BYTES and upright:
        return data, kind, f"{size[0]} × {size[1]}"
    try:
        from PIL import Image, ImageOps
    except ImportError:
        raise Refused("this picture is too large to be shown through the door (and the tool that would reduce it, "
                      "Pillow, is not on this computer).")
    try:
        img = Image.open(io.BytesIO(data))
        img.load()
        w0, h0 = img.size
        if not upright:
            img = ImageOps.exif_transpose(img)                     # as the camera meant it, as a phone shows it
        img.thumbnail((PICTURE_SIDE, PICTURE_SIDE))
        out = io.BytesIO()
        if kind == "image/jpeg" or (kind == "image/webp" and img.mode not in ("RGBA", "LA", "P")):
            img.convert("RGB").save(out, "JPEG", quality=88)
            kind = "image/jpeg"
        else:
            img.save(out, "PNG", optimize=True)
            kind = "image/png"
        data = out.getvalue()
        if len(data) > PICTURE_BYTES:
            smaller = io.BytesIO()
            img.convert("RGB").save(smaller, "JPEG", quality=75)
            data, kind = smaller.getvalue(), "image/jpeg"
        return data, kind, (f"shown at {img.size[0]} × {img.size[1]}" + ("" if upright else ", turned upright as the camera meant it")
                            + f"; the file is {w0} × {h0}")
    except Refused:
        raise
    except Exception as e:
        raise Refused(f"this picture could not be opened to be shown ({type(e).__name__}).")


def words_of(s):
    """A line of arguments, split as a shell would, and forgivingly if its quotes do not close."""
    try:
        return shlex.split(s)
    except ValueError:
        return s.split()


class Hands:
    """The tools a visitor has, done in the garden at `root`."""

    def __init__(self, root: Path, token: str, records: Path = None):
        self.walls = Walls(root)
        self.root = self.walls.root
        self.token = token
        self.records = records        # where this door keeps its records: an earlier visit's ending is read there
        self.pictures = 0
        self.picture_bytes = 0        # what the pictures shown so far weigh, as they are sent
        self.gate_closed = False      # set when shed/leave.py ran and said the gate is closed
        self.lifted = None            # the name on a latch the door lifted for this visitor, if it did

    # -- the one way in: (content for the API, is_error, how the record shows it)
    def do(self, name, given):
        given = given if isinstance(given, dict) else {}
        try:
            if name not in TOOL_NAMES:
                raise Refused(f"there is no tool called {name} here. The tools are: {', '.join(TOOL_NAMES)}.")
            content, shown = getattr(self, "tool_" + name)(given)
            return content, False, shown
        except Refused as r:
            words = str(r)
            return words, True, words
        except Exception as e:                              # the gate always opens: a stumble is said, and the visit goes on
            words = f"the door stumbled doing that ({type(e).__name__}: {' '.join(str(e).split())[:300]})."
            return words, True, words

    def _text(self, given, key, required=True):
        v = given.get(key)
        if v is None:
            if required:
                raise Refused(f"this needs '{key}'.")
            return None
        if not isinstance(v, str):
            raise Refused(f"'{key}' should be text.")
        return v

    # -- looking
    def tool_list(self, given):
        p = self.walls.place(given.get("path") or ".")
        if not p.exists():
            raise Refused(f"there is nothing at {self.walls.rel(p)}.")
        if not p.is_dir():
            raise Refused(f"{self.walls.rel(p)} is a file; read opens it.")
        seen, hidden = [], []
        try:
            entries = sorted(os.scandir(p), key=lambda e: e.name.lower())
        except OSError as e:
            raise Refused(f"{self.walls.rel(p)} could not be listed ({type(e).__name__}).")
        for e in entries:
            q = Path(e.path)
            if _is_link(q):
                label = f"{e.name}  (a link; the garden does not follow it)"
            elif e.is_dir(follow_symlinks=False):
                label = e.name + "/"
            else:
                try:
                    label = f"{e.name}  ({size_words(e.stat(follow_symlinks=False).st_size)})"
                except OSError:
                    label = e.name
            (hidden if e.name.startswith(".") else seen).append(label)
        lines = [f"{self.walls.rel(p)}:"]
        lines += ["  " + x for x in seen[:500]] or ["  (empty)"]
        if len(seen) > 500:
            lines.append(f"  ... and {len(seen) - 500} more")
        if hidden:
            lines.append("  with a leading dot (invisible to the garden): " + ", ".join(x.split("  ")[0] for x in hidden))
        out = "\n".join(lines)
        return out, out

    def tool_read(self, given):
        p = self.walls.place(self._text(given, "path"))
        rel = self.walls.rel(p)
        if not p.exists():
            raise Refused(f"there is nothing at {rel}.")
        if p.is_dir():
            content, _ = self.tool_list({"path": rel})
            out = f"({rel} is a folder; here is what is in it)\n" + content
            return out, out
        data = p.read_bytes()
        if p.suffix.lower() in PICTURE_TYPES:
            kind = picture_kind(data)
            if not kind:
                raise Refused(f"{rel} is named like a picture, but it is not one this door can show.")
            if self.pictures >= MOST_PICTURES:
                raise Refused(f"this visit has been shown {MOST_PICTURES} pictures, which is as many as the door can "
                              f"carry in one visit; {rel} is there all the same.")
            data, kind, words = picture_for_api(data, kind)
            coded = base64.standard_b64encode(data).decode("ascii")
            if self.picture_bytes + len(coded) > MOST_PICTURE_BYTES:
                raise Refused(f"the pictures of this visit already weigh about {self.picture_bytes // 1_000_000} MB, and "
                              f"every turn carries them all again; {rel} would take them past what the door can carry, "
                              "so it is not shown. It is there all the same.")
            self.pictures += 1
            self.picture_bytes += len(coded)
            content = [{"type": "image", "source": {"type": "base64", "media_type": kind, "data": coded}},
                       {"type": "text", "text": f"{rel} · {words}"}]
            return content, f"[the picture {rel} was shown · {words}]"
        text = text_of(data)
        if text is None:
            raise Refused(f"{rel} is not text ({size_words(len(data))}); the door can show text and pictures.")
        if not text:
            return "(the file is empty)", "(the file is empty)"
        lines = text.split("\n")
        start = given.get("start")
        try:
            start = max(1, int(start)) if start is not None else 1
        except (TypeError, ValueError):
            start = 1
        if start > len(lines):
            raise Refused(f"{rel} has {len(lines):,} lines; there is no line {start:,}.")
        if start == 1 and len(text) <= MOST_READ_CHARS:
            return text, text
        taken, used = [], 0
        for line in lines[start - 1:]:
            if used + len(line) + 1 > MOST_READ_CHARS and taken:
                break
            taken.append(line)
            used += len(line) + 1
        last = start + len(taken) - 1
        out = "\n".join(taken)
        if last < len(lines):
            out += f"\n\n[the door: lines {start:,} to {last:,} of {len(lines):,} were shown; read with start {last + 1} to go on]"
        elif start > 1:
            out += f"\n\n[the door: lines {start:,} to {last:,} of {len(lines):,}: the end of the file]"
        return out, out

    # -- tending
    def _write_whole(self, p: Path, text: str):
        """Whole or not at all: the new text is written beside its place, then moved into it in one step."""
        part = p.with_name("." + p.name + ".part")
        with open(part, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        os.replace(part, p)

    def tool_write(self, given):
        p = self.walls.place(self._text(given, "path"), writing=True)
        text = self._text(given, "text")
        rel = self.walls.rel(p)
        if len(text) > MOST_WRITE_CHARS:
            raise Refused(f"that is more than {MOST_WRITE_CHARS:,} characters for one file.")
        if p.is_dir():
            raise Refused(f"{rel} is a folder.")
        new = not p.exists()
        p.parent.mkdir(parents=True, exist_ok=True)
        self._write_whole(p, text.replace("\r\n", "\n"))
        n = text.count("\n") + (0 if text.endswith("\n") or not text else 1)
        out = f"{'wrote' if new else 'wrote anew'} {rel} ({n:,} lines)."
        return out, out

    def tool_edit(self, given):
        p = self.walls.place(self._text(given, "path"), writing=True)
        old, new = self._text(given, "old"), self._text(given, "new")
        rel = self.walls.rel(p)
        if not p.is_file():
            raise Refused(f"there is no file at {rel}.")
        if not old:
            raise Refused("'old' must be some text that is in the file.")
        text = text_of(p.read_bytes())
        if text is None:
            raise Refused(f"{rel} is not text.")
        old, new = old.replace("\r\n", "\n"), new.replace("\r\n", "\n")
        n = text.count(old)
        if n == 0:
            raise Refused(f"that passage is not in {rel} as written (spaces and line ends count).")
        if n > 1:
            raise Refused(f"that passage is in {rel} {n} times; give a longer one, so that it is there only once.")
        self._write_whole(p, text.replace(old, new, 1))
        out = f"changed {rel}."
        return out, out

    def tool_move(self, given):
        src = self.walls.place(self._text(given, "src"), writing=True, what="src")
        dst = self.walls.place(self._text(given, "dst"), writing=True, what="dst")
        if not src.exists():
            raise Refused(f"there is nothing at {self.walls.rel(src)}.")
        if dst.is_dir() and _norm(dst) != _norm(src):
            dst = dst / src.name
            self.walls.place(self.walls.rel(dst), writing=True, what="dst")
        if _norm(dst) == _norm(src):
            raise Refused("that is where it already is.")
        if src.is_dir() and _within(dst, src):
            raise Refused("a folder cannot be moved into itself.")
        if dst.exists():
            raise Refused(f"{self.walls.rel(dst)} is already there, and nothing is written over; choose another name.")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        self._placed_now(dst)
        out = f"moved {self.walls.rel(src)} to {self.walls.rel(dst)}."
        return out, out

    def tool_copy(self, given):
        src = self.walls.place(self._text(given, "src"), what="src")              # anything in the garden can be read
        dst = self.walls.place(self._text(given, "dst"), writing=True, what="dst")  # ... but not every place written
        rel = self.walls.rel(src)
        if not src.exists():
            raise Refused(f"there is nothing at {rel}.")
        if src.is_dir():
            raise Refused(f"{rel} is a folder; copy takes one file at a time (make a folder, and copy into it the "
                          "files you want).")
        if not src.is_file():
            raise Refused(f"{rel} is not a file that can be copied.")
        if dst.is_dir():
            dst = dst / src.name
            self.walls.place(self.walls.rel(dst), writing=True, what="dst")
        if _norm(dst) == _norm(src):
            raise Refused("that is the file itself; a copy needs a place of its own.")
        if dst.exists():
            raise Refused(f"{self.walls.rel(dst)} is already there, and nothing is written over; choose another name.")
        size = src.stat().st_size
        if size > MOST_COPY_BYTES:
            raise Refused(f"{rel} is {size_words(size)}; the door copies at most {size_words(MOST_COPY_BYTES)} at once.")
        dst.parent.mkdir(parents=True, exist_ok=True)
        part = dst.with_name("." + dst.name + ".part")     # whole or not at all, as a write is
        try:
            shutil.copyfile(src, part)                     # the bytes only: a copy is a new file, written now
            try:
                os.rename(part, dst)                       # never os.replace: nothing is written over
            except FileExistsError:
                raise Refused(f"{self.walls.rel(dst)} is already there, and nothing is written over; choose another name.")
        finally:
            if part.exists():
                try:
                    os.remove(part)
                except OSError:
                    pass
        self._placed_now(dst)
        out = f"copied {rel} to {self.walls.rel(dst)}."
        return out, out

    def _placed_now(self, p: Path):
        """What the visitor has just put into a bed is dated now, since that is when they put it there.

        A moved file keeps the time it was last written. The ground reads a
        seed's time to know who planted it and from which day it lives
        (shed/ground.py: _signer, _lain, _sown_day), so a packet moved from
        the seedbox would seem to have lain in the bed since before the visit
        began, and come up signed by an unseen hand. A folder moved into a bed
        is dated now with everything in it. Links are not followed, and
        nothing outside the beds is touched: a thing moved onto the heap keeps
        its time, and the heap dates it by the day it is noticed there.
        """
        if self.walls.top(p) != "beds":
            return
        now = time.time()
        todo, seen = [p], 0
        while todo and seen < MOST_DATED:
            q = todo.pop()
            seen += 1
            if _is_link(q) or not _within(q, self.root):
                continue
            try:
                if q.is_dir():
                    todo.extend(Path(e.path) for e in os.scandir(q))
                os.utime(q, (now, now))
            except OSError:
                continue                                   # a time that cannot be set is left as it was

    def tool_make_folder(self, given):
        p = self.walls.place(self._text(given, "path"), writing=True)
        rel = self.walls.rel(p)
        if p.is_dir():
            out = f"{rel} is already there."
            return out, out
        if p.exists():
            raise Refused(f"{rel} is a file.")
        p.mkdir(parents=True)
        out = f"made {rel}/."
        return out, out

    # -- running
    def _run(self, command, seconds, env):
        """Runs a command in the garden, in a job of its own (see Job): when it ends, or is stopped, whatever it
        started ends with it. Its output goes to files outside the garden, so that nothing can hold the door open.
        Returns (what it said, its exit code, whether it was stopped, how many programs it left running)."""
        job = Job()
        left = 0
        try:
            with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
                proc = subprocess.Popen(command, cwd=str(self.root), env=env, stdin=subprocess.DEVNULL, stdout=out,
                                        stderr=err, creationflags=job.flags)
                if not job.take(proc):
                    raise Refused("Windows would not let the door start that program, so it did not run.")
                stopped = False
                try:
                    code = proc.wait(timeout=seconds)
                except subprocess.TimeoutExpired:
                    job.end() if job.handle else end_tree(proc)
                    stopped = True
                    try:
                        code = proc.wait(timeout=20)
                    except subprocess.TimeoutExpired:
                        code = None
                except KeyboardInterrupt:
                    job.end() if job.handle else end_tree(proc)
                    raise
                left = job.still_running()
                job.end()
                out.seek(0)
                err.seek(0)
                said = (out.read().decode("utf-8", errors="replace"), err.read().decode("utf-8", errors="replace"))
        finally:
            job.end()
        return said, code, stopped, left

    @staticmethod
    def _said(said, code, stopped, left, seconds):
        o, e = (s.replace("\r\n", "\n").rstrip() for s in said)
        parts = [o] if o else []
        if e:
            parts.append("[it said on its error stream:]\n" + e)
        text = "\n\n".join(parts) or "(it printed nothing)"
        if len(text) > MOST_OUTPUT_CHARS:
            text = text[:MOST_OUTPUT_CHARS] + f"\n[the door: cut here; it printed {len(text):,} characters in all]"
        if stopped:
            text += f"\n[the door: it was still running after {seconds} seconds, and was stopped, with all it had started]"
        else:
            if code:
                text += f"\n[it ended with exit code {code}]"
            if left:
                text += (f"\n[the door: it left {plural(left, 'program')} of its own running, which "
                         f"{'was' if left == 1 else 'were'} stopped when it ended]")
        return text

    @staticmethod
    def _args(given):
        a = given.get("args")
        if a is None:
            return []
        if isinstance(a, str):
            return words_of(a)
        if isinstance(a, list):
            return [x if isinstance(x, str) else json.dumps(x) for x in a]
        raise Refused("'args' should be a list of words.")

    def tool_python(self, given):
        p = self.walls.place(self._text(given, "script"), what="script")
        rel = self.walls.rel(p)
        top = self.walls.top(p)                                 # p is the long name already: GIT~1 has become .git
        if top in ("keeper", ".git"):
            raise Refused(f"{rel} is the keeper's; the programs in {top}/ are theirs to run.")
        if not p.is_file():
            raise Refused(f"there is no file at {rel}.")
        if p.suffix.lower() != ".py":
            raise Refused(f"{rel} is not a .py file; python runs only .py files that lie in the garden.")
        args = self._args(given)
        added = ""
        if rel.lower() in ("shed/arrive.py", "shed/leave.py"):
            kept, i = [], 0
            while i < len(args):                                  # a token of the visitor's own gives way to the door's
                if args[i] == "--visit":
                    i += 2 if (i + 1 < len(args) and not args[i + 1].startswith("--")) else 1
                    continue
                if not args[i].startswith("--visit="):
                    kept.append(args[i])
                i += 1
            args = kept + ["--visit", self.token]
            added = f"--visit {self.token}"
        told = ""
        if rel.lower() == "shed/arrive.py" and "--lift" not in args:
            latch = latch_of(self.root)                           # an earlier visit through this door, over, on the latch?
            if latch and latch.get("visit") and latch["visit"] != self.token:
                over = door_visit_over(self.records, latch["visit"])
                if over:
                    args.append("--lift")
                    added += " --lift"
                    self.lifted = latch.get("name") or "a visitor"
                    told = (f"[the door: the latch bore the token of a visit through this door, {self.lifted}'s, "
                            f"which {over}; so the door added --lift]\n")
        said, code, stopped, left = self._run([sys.executable, "-B", str(p)] + args, PYTHON_SECONDS, clean_env())
        text = told + self._said(said, code, stopped, left, PYTHON_SECONDS)
        if rel.lower() == "shed/leave.py" and code == 0 and "The gate is closed behind" in said[0]:
            self.gate_closed = True
        shown = text
        if added:
            shown = f"(the door added {added})\n" + text
        return text, shown

    def _history_word(self, sub, a):
        """Refused, if one word given to history could write, or reach outside the garden."""
        if a.startswith("--"):
            name = a.split("=", 1)[0]
            if any(name.startswith(r) or (len(name) > 3 and r.startswith(name)) for r in GIT_REFUSED):
                raise Refused(f"'{a}' would write a file, or reach outside the garden; history only reads the layers.")
        elif a.startswith("-"):
            # Short options may stand together in one word (-pO<file> is -p then -O<file>), so every letter counts:
            # git reads -O<file> (and blame -S<file>) from anywhere it is pointed.
            if "O" in a[1:] or (sub == "blame" and "S" in a[1:]):
                hint = " (to search for a word, give -S and the word as two words)" if sub != "blame" and a[1:2] in "SG" else ""
                letter = "-O" if "O" in a[1:] else "blame's -S"
                raise Refused(f"'{a}' holds a letter git could take as {letter}: a file to read from anywhere it points, "
                              f"even inside another option; history does not take it{hint}.")
        else:
            if a.startswith(":"):                                  # :(glob)beds/*, :/ — a path with its magic before it
                path_part = re.sub(r"^:(\([^)]*\)|[/!^]*)", "", a)
            elif re.match(r"^[A-Za-z]:", a):                        # C:/x, and C:x (the folder C: stands in), D:x ...
                raise Refused(f"'{a}' names a drive; paths in history are from the garden's root.")
            else:
                path_part = a.split(":", 1)[1] if ":" in a else a   # <layer>:<path>
            try:
                self.walls.place(path_part or ".")
            except Refused as r:
                raise Refused(f"'{a}' cannot be read through history: {r}")

    def tool_history(self, given):
        args = self._args(given)
        if args and args[0].lower() == "git":
            args = args[1:]
        if not args:
            raise Refused("history needs a first word: log, show, diff, blame or status.")
        sub, rest = args[0].strip().lower(), args[1:]
        if sub not in GIT_READS:
            raise Refused(f"history only reads the layers: log, show, diff, blame or status. '{args[0]}' is not one of them.")
        for a in rest:
            self._history_word(sub, a)
        if not (self.root / ".git").exists():
            raise Refused("no layers are kept in this garden (it is not a git repository).")
        git = shutil.which("git")
        if not git:
            raise Refused("git is not on this computer, so the layers cannot be read.")
        root = str(self.root)
        command = [git, "--no-pager", f"--git-dir={os.path.join(root, '.git')}", f"--work-tree={root}",
                   "-c", "core.quotepath=false", "-c", "color.ui=never", "-c", "core.pager=cat",
                   "-c", f"safe.directory={root.replace(os.sep, '/')}", sub]
        if sub in ("log", "show", "diff"):
            command += ["--no-ext-diff", "--no-textconv"]
        env = clean_env()
        env.update(GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0", GIT_PAGER="cat", PAGER="cat",
                   GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        # git diff refreshes the index's file dates and writes it back, lock and all. It is given a copy of the
        # index, outside the garden, to write on as it likes; the garden's own is left as it was.
        with tempfile.TemporaryDirectory(prefix="glebe-door-", ignore_cleanup_errors=True) as spare:
            index = os.path.join(root, ".git", "index")
            env["GIT_INDEX_FILE"] = os.path.join(spare, "index")
            if os.path.isfile(index):
                shutil.copyfile(index, env["GIT_INDEX_FILE"])
            said, code, stopped, left = self._run(command + rest, HISTORY_SECONDS, env)
        text = self._said(said, code, stopped, left, HISTORY_SECONDS)
        return text, text


# =========================================================================
# THE RECORD: written as the visit happens, outside the garden
# =========================================================================

def fence(text):
    f = "```"
    while f in text:
        f += "`"
    return f


def quoted(text):
    return "\n".join("> " + line if line else ">" for line in text.split("\n"))


LATCH_HOURS = 12                 # the garden's own (shed/ground.py): how long a visit left open keeps the latch


class Record:
    """The visit's .md (for reading) and .jsonl (the same, as data), written and flushed at every step,
    so that a visit cut off is still kept up to where it stopped.

    While the visit goes on, the door holds the system's lock on one byte far past the end of the .jsonl.
    Windows lets go of it when the door's process ends, however it ends (the window closed, the power
    gone), so a later door can tell a visit that is over from one still going on in another window."""

    MD_RESULT = 6_000          # a tool's result is kept whole in the .jsonl; in the .md, up to this much
    LOCK_AT = 1 << 40          # the byte that is locked: far past anything ever written

    @classmethod
    def held(cls, jsonl_path) -> bool:
        """Is a door still in the visit this .jsonl records? (True when it cannot be told.)"""
        try:
            import msvcrt
        except ImportError:
            return True
        try:
            with open(jsonl_path, "rb") as f:
                f.seek(cls.LOCK_AT)
                try:
                    msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                except OSError:
                    return True
                f.seek(cls.LOCK_AT)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
                return False
        except OSError:
            return True

    def _hold(self):
        self.lock = None
        try:
            import msvcrt
            self.lock = open(self.jsonl_path, "rb")
            self.lock.seek(self.LOCK_AT)
            msvcrt.locking(self.lock.fileno(), msvcrt.LK_NBLCK, 1)
        except (ImportError, OSError):
            if self.lock:
                self.lock.close()
            self.lock = None

    def __init__(self, folder: Path, model: str, called: str, rehearsal: bool):
        folder.mkdir(parents=True, exist_ok=True)
        stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        safe = re.sub(r"[^A-Za-z0-9._-]+", "-", model).strip("-") or "a-visitor"
        base = f"{stamp}_{safe}" + ("_rehearsal" if rehearsal else "")
        n = 1
        while True:
            name = base if n == 1 else f"{base}-{n}"
            if not (folder / f"{name}.md").exists() and not (folder / f"{name}.jsonl").exists():
                break
            n += 1
        self.md_path, self.jsonl_path = folder / f"{name}.md", folder / f"{name}.jsonl"
        self.md = open(self.md_path, "x", encoding="utf-8", newline="\n")
        self.jl = open(self.jsonl_path, "x", encoding="utf-8", newline="\n")
        self._hold()

    def _flush(self, f):
        f.flush()
        try:
            os.fsync(f.fileno())
        except OSError:
            pass

    def write(self, text):
        self.md.write(text)
        self._flush(self.md)

    def event(self, kind, **data):
        line = {"at": datetime.datetime.now().isoformat(timespec="seconds"), "event": kind}
        line.update(data)
        self.jl.write(json.dumps(line, ensure_ascii=False, default=str) + "\n")
        self._flush(self.jl)

    def close(self):
        if self.lock:
            try:
                import msvcrt
                self.lock.seek(self.LOCK_AT)
                msvcrt.locking(self.lock.fileno(), msvcrt.LK_UNLCK, 1)
            except (ImportError, OSError):
                pass
        for f in (self.md, self.jl, self.lock):
            try:
                if f:
                    f.close()
            except Exception:
                pass

    def result_md(self, text):
        if len(text) > self.MD_RESULT:
            text = text[:self.MD_RESULT] + f"\n[... {len(text) - self.MD_RESULT:,} more characters: the whole of it is in the .jsonl]"
        f = fence(text)
        return f"{f}text\n{text}\n{f}\n"


def latch_of(root: Path):
    """What the garden's latch (ground/present) says, as {'name', 'since', 'visit'}; None if there is none."""
    try:
        text = text_of((Path(root) / "ground" / "present").read_bytes()) or ""
    except OSError:
        return None
    keys = {}
    for line in text.split("\n"):
        key, colon, value = line.partition(":")
        if colon and not key.lstrip().startswith("#"):
            keys.setdefault(key.strip().lower(), value.strip())
    return keys if keys.get("name") else None


def door_visit_over(records, token):
    """If `token` is the token of an earlier visit through this door that is over, a few words saying how it
    ended ('ended at 07:41'); otherwise None (no such visit, or it is still going on in another window)."""
    if not records or not token:
        return None
    try:
        found = sorted(Path(records).glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)[:300]
    except OSError:
        return None
    for path in found:
        try:
            with open(path, "rb") as f:
                begin = json.loads(f.readline().decode("utf-8"))
                if begin.get("event") != "begin" or begin.get("token") != token:
                    continue
                f.seek(0, os.SEEK_END)
                f.seek(max(0, f.tell() - 65536))
                tail = f.read().decode("utf-8", errors="replace").splitlines()
        except (OSError, ValueError, AttributeError):
            continue
        for line in reversed(tail):
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if isinstance(event, dict) and event.get("event") == "end":
                at = str(event.get("at", ""))
                return f"ended at {at[11:16]}" if len(at) >= 16 else "has ended"
        if Record.held(path):
            return None                                   # a door is still in that visit, in another window
        return "was cut off (its window was closed)"
    return None


def block_record(b, keep_notes):
    """A content block as the record keeps it: thinking is never kept, except a model's short notes between tools."""
    t = getattr(b, "type", None)
    if t == "text":
        return {"type": "text", "text": getattr(b, "text", "")}
    if t == "tool_use":
        return {"type": "tool_use", "id": getattr(b, "id", ""), "name": getattr(b, "name", ""), "input": getattr(b, "input", {})}
    if t == "thinking":
        note = (getattr(b, "thinking", "") or "").strip()
        return {"type": "note", "text": note} if (keep_notes and note) else {"type": "thought"}
    if t == "redacted_thinking":
        return {"type": "thought"}
    return {"type": str(t)}


def call_words(name, inp):
    """How a tool call reads in the record and in the window."""
    inp = inp if isinstance(inp, dict) else {}
    if name == "python":
        args = inp.get("args") or []
        args = words_of(args) if isinstance(args, str) else [str(a) for a in args] if isinstance(args, list) else [str(args)]
        shown = " ".join(a if re.fullmatch(r"[\w./:=,@+-]+", a) else '"' + a.replace('"', '\\"') + '"' for a in args)
        return f"python {inp.get('script', '')} {shown}".rstrip()
    if name == "history":
        args = inp.get("args") or []
        args = words_of(args) if isinstance(args, str) else [str(a) for a in args] if isinstance(args, list) else [str(args)]
        if args and args[0].lower() == "git":
            args = args[1:]
        return "git " + " ".join(args)
    if name in ("move", "copy"):
        return f"{name} {inp.get('src', '')} -> {inp.get('dst', '')}"
    if name == "read" and inp.get("start"):
        return f"read {inp.get('path', '')} (from line {inp.get('start')})"
    if name in ("list", "read", "write", "edit", "make_folder"):
        return f"{name} {inp.get('path', '') or '.'}"
    return f"{name} {json.dumps(inp, ensure_ascii=False)[:200]}"


# =========================================================================
# THE VISIT
# =========================================================================

class Closed(Exception):
    """The visit ends here, for the reason given."""


def say(text="", indent=0):
    pad = " " * indent
    for line in text.split("\n"):
        print(pad + line, flush=True)


def plural(n, one, many=None):
    return f"{n:,} {one if n == 1 else (many or one + 's')}"


class Visit:
    def __init__(self, client, model, row, hands, record, *, called, name, garden, rehearsal, most_turns, waits):
        self.client, self.model, self.row, self.hands, self.record = client, model, row, hands, record
        self.called, self.name, self.garden, self.rehearsal = called, name, garden, rehearsal
        self.most_turns, self.waits = most_turns, waits
        self.turns = 0
        self.tokens = dict(input=0, cache_write=0, cache_read=0, output=0)
        self.last_read = self.last_written = 0
        self.cache = True

    # -- the request, as this model takes it
    def params(self, system, messages):
        p = dict(model=self.model, max_tokens=self.row["max_tokens"], system=system, tools=TOOLS, messages=messages)
        if self.row.get("thinking"):
            p["thinking"] = self.row["thinking"]
        if self.row.get("effort"):
            p["output_config"] = {"effort": self.row["effort"]}
        if self.cache:
            p["cache_control"] = {"type": "ephemeral"}       # the visit so far is read from the cache on the next turn
        return p

    def ask(self, system, messages):
        """One answer from the model. Busy spells are waited out; anything else that goes wrong ends the visit.

        A busy spell can also come in the middle of an answer, while it streams: the connection dropped (home
        Wi-Fi, the computer asleep), or an error sent inside the stream, which the SDK gives with the status of
        the stream itself (200). Both are waited out like any other: the half-answer is let go, nothing of it
        is done, and the same request is made again."""
        import anthropic
        import httpx
        tries, malformed = 0, 0
        while True:
            params = self.params(system, messages)
            why = None
            try:
                if self.row.get("betas"):
                    stream = self.client.beta.messages.stream(betas=list(self.row["betas"]), **params)
                else:
                    stream = self.client.messages.stream(**params)
                with stream as s:
                    reply = s.get_final_message()
                if getattr(reply, "stop_reason", None) is None:
                    raise httpx.RemoteProtocolError("the answer stopped before its end")
                return reply
            except anthropic.RateLimitError as e:
                why, wait = "the rate limit was reached", self._retry_after(e)
            except anthropic.APIStatusError as e:
                status = getattr(e, "status_code", 0) or 0
                message = self._message(e)
                kind = self._kind(e)
                if kind == "rate_limit_error":
                    why, wait = "the rate limit was reached", self._retry_after(e)
                elif status == 529 or kind == "overloaded_error" or "overloaded" in message.lower():
                    why, wait = "it is overloaded", None
                elif status >= 500 or status in (408, 409) or kind == "api_error":
                    why, wait = f"it answered with an error of its own ({status if status != 200 else kind})", None
                elif status == 400 and "cache_control" in message and self.cache:
                    self.cache = False                         # a model that does not take the cache comes in without it
                    self.record.event("note", text="the cache was refused for this model; the visit goes on without it")
                    continue
                elif status == 400 and ("too long" in message or "context" in message.lower() and "exceed" in message.lower()):
                    raise Closed("the visit had grown longer than the model can hold at once")
                elif status == 400:
                    raise Closed(f"the API refused the request as the door made it: {message} "
                                 "(the model's row in the table at the head of keeper/invite.py may need changing)")
                elif status == 401:
                    raise Closed("the API key was refused (401)")
                elif status == 403:
                    raise Closed(f"the API would not let this key do that (403): {message}")
                elif status == 404:
                    raise Closed(f"the API does not know the model {self.model} (404); it may have been retired")
                else:
                    raise Closed(f"the API answered with an error ({status}): {message}")
            except anthropic.APIConnectionError as e:
                why, wait = ("the API did not answer in time" if isinstance(e, anthropic.APITimeoutError)
                             else "the API could not be reached"), None
            except httpx.TimeoutException:                     # in the middle of an answer, the SDK lets these through
                why, wait = "the answer stopped coming, in the middle (it took too long)", None
            except httpx.TransportError:
                why, wait = "the connection dropped in the middle of an answer", None
            except ValueError as e:                            # a tool call whose words could not be read whole
                malformed += 1
                if malformed > 2:
                    raise Closed(f"the model's answer could not be read, three times ({e})")
                self.record.event("note", text=f"an answer could not be read whole ({e}); asked again")
                continue
            tries += 1
            if tries > len(self.waits):
                raise Closed(f"the API stayed busy ({why}) through {len(self.waits)} waits")
            wait = self.waits[tries - 1] if wait is None else wait
            words = f"The API is busy: {why}. Waiting {wait:g} seconds, then trying again ({tries} of {len(self.waits)})."
            say(words, 2)
            self.record.event("wait", why=why, seconds=wait, attempt=tries)
            self.record.write(f"\n_{datetime.datetime.now():%H:%M:%S} · {words}_\n")
            time.sleep(wait)

    def _retry_after(self, e):
        try:
            v = float(e.response.headers.get("retry-after"))
            return max(1.0, min(v, 600.0)) if not self.rehearsal else min(v, 0.2)
        except Exception:
            return None

    @staticmethod
    def _kind(e):
        """The kind of error the API named in its answer ('overloaded_error', 'api_error', ...), or ''."""
        body = getattr(e, "body", None)
        if isinstance(body, dict):
            err = body.get("error") if isinstance(body.get("error"), dict) else body
            if isinstance(err, dict):
                return str(err.get("type") or "")
        return ""

    @staticmethod
    def _message(e):
        body = getattr(e, "body", None)
        if isinstance(body, dict):
            err = body.get("error") if isinstance(body.get("error"), dict) else body
            if isinstance(err, dict) and err.get("message"):
                return str(err["message"])
        return " ".join(str(getattr(e, "message", e)).split())[:400]

    # -- counting
    def count(self, usage):
        g = lambda k: int(getattr(usage, k, 0) or 0)
        self.tokens["input"] += g("input_tokens")
        self.tokens["cache_write"] += g("cache_creation_input_tokens")
        self.tokens["cache_read"] += g("cache_read_input_tokens")
        self.tokens["output"] += g("output_tokens")
        self.last_read = g("input_tokens") + g("cache_creation_input_tokens") + g("cache_read_input_tokens")
        self.last_written = g("output_tokens")

    def nearly_full(self):
        """Would the next turn come near the most the model can hold? The next request reads what the last one
        read, and the last answer, and may write up to max_tokens more; all of it must fit in the window."""
        window = self.row["window"]
        return bool(self.last_read) and (self.last_read >= FULL_AT * window or
                                         self.last_read + self.last_written + self.row["max_tokens"] > window)

    def read_so_far(self):
        return self.tokens["input"] + self.tokens["cache_write"] + self.tokens["cache_read"]

    def cost(self):
        price = self.row.get("price")
        if not price:
            return None
        i, o, r = price
        t = self.tokens
        return (t["input"] * i + t["cache_write"] * i * 1.25 + t["cache_read"] * r + t["output"] * o) / 1e6

    # -- the walk
    def run(self, system, opening):
        messages = [{"role": "user", "content": opening}]
        while True:
            if self.turns >= self.most_turns:
                raise Closed(f"the door's ceiling was reached: {self.most_turns} turns")
            if self.read_so_far() >= MOST_TOKENS_READ:
                raise Closed(f"the door's ceiling was reached: {MOST_TOKENS_READ:,} tokens read")
            if self.tokens["output"] >= MOST_TOKENS_WRITTEN:
                raise Closed(f"the door's ceiling was reached: {MOST_TOKENS_WRITTEN:,} tokens written")
            if self.nearly_full():
                raise Closed("the visit had grown nearly as long as the model can hold at once")
            reply = self.ask(system, messages)
            self.turns += 1
            self.count(getattr(reply, "usage", None))
            content = list(getattr(reply, "content", None) or [])
            stop = getattr(reply, "stop_reason", None)
            self.show_turn(content, stop, reply)
            if stop == "refusal":
                details = getattr(reply, "stop_details", None)
                category = getattr(details, "category", None) if details else None
                raise Closed("the model's safeguards declined the turn" + (f" ({category})" if category else ""))
            uses = [b for b in content if getattr(b, "type", None) == "tool_use"]
            words = [b for b in content if getattr(b, "type", None) == "text" and (getattr(b, "text", "") or "").strip()]
            full = stop == "model_context_window_exceeded"
            if stop == "pause_turn":
                messages.append({"role": "assistant", "content": content})
                continue
            if not uses:
                if full:
                    raise Closed("the visit had grown as long as the model can hold at once")
                if not words:
                    raise Closed("an empty turn: the visitor said nothing and used no tool")
                if stop == "max_tokens":
                    raise Closed(f"the visitor's answer reached the door's limit of {self.row['max_tokens']:,} tokens a turn")
                raise Closed("the visitor answered without using a tool")
            messages.append({"role": "assistant", "content": content})
            results = []
            for b in uses:
                bid, bname, binp = getattr(b, "id", ""), getattr(b, "name", ""), getattr(b, "input", {})
                self.show_call(bname, binp)
                if stop == "tool_use":                          # only a turn that ended on its calls has them whole
                    content_back, is_error, shown = self.hands.do(bname, binp)
                else:
                    words_back = self.unfinished(stop)
                    content_back, is_error, shown = words_back, True, words_back
                self.show_result(bid, bname, binp, content_back, is_error, shown)
                r = {"type": "tool_result", "tool_use_id": bid, "content": content_back}
                if is_error:
                    r["is_error"] = True
                results.append(r)
            messages.append({"role": "user", "content": results})
            if full:
                raise Closed("the visit had grown as long as the model can hold at once")

    def unfinished(self, stop):
        """What a call is answered with when its turn stopped before the call was whole: nothing was done."""
        why = {"max_tokens": f"the turn reached the door's limit of {self.row['max_tokens']:,} tokens",
               "model_context_window_exceeded": "the visit reached the most the model can hold at once"}.get(
                   stop, f"the turn stopped ({stop})")
        return f"{why} before this call was whole, so nothing was done."

    # -- the window and the record
    def show_turn(self, content, stop, reply):
        now = datetime.datetime.now()
        kept = [block_record(b, self.row.get("notes")) for b in content]
        usage = getattr(reply, "usage", None)
        self.record.event("turn", n=self.turns, stop_reason=stop, content=kept,
                          usage={k: int(getattr(usage, k, 0) or 0) for k in
                                 ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")})
        md = [f"\n## {now:%H:%M:%S} · turn {self.turns}\n"]
        thought = False
        for k in kept:
            if k["type"] == "thought":
                thought = True
            elif k["type"] == "note":
                md.append(f"_a note between steps:_ {k['text']}\n")
                say(f"[{now:%H:%M:%S}] (a note) {textwrap.shorten(k['text'], 300)}", 2)
            elif k["type"] == "text" and k["text"].strip():
                text = k["text"].strip()
                md.append(quoted(text) + "\n")
                say(f"[{now:%H:%M:%S}] the visitor:", 2)
                shown = text[:1500] + (" ..." if len(text) > 1500 else "")
                say("\n".join(textwrap.fill(p, 92) if p.strip() else "" for p in shown.split("\n")), 6)
        if thought:
            md.insert(1, "_(thought)_\n")
        if stop not in ("tool_use", "end_turn", None):
            plain = {"max_tokens": f"the turn reached the door's limit of {self.row['max_tokens']:,} tokens",
                     "model_context_window_exceeded": "the turn reached the most the model can hold at once",
                     "refusal": "the model's safeguards declined the turn",
                     "pause_turn": "the turn paused, and was taken up again"}.get(stop, f"the turn stopped ({stop})")
            md.append(f"_{plain}_\n")
        self.record.write("\n".join(md) + "\n")

    def show_call(self, name, inp):
        """A call, in the window and in the record, before it is done: a visit cut off while a program runs
        is still kept up to that call."""
        words = call_words(name, inp)
        say(f"-> {words}", 6)
        said = words[len(name) + 1:] if words.startswith(name + " ") else words
        md = [f"**{name}** " + (f"`` {said} ``" if "`" in said else f"`{said}`") + "\n"]
        if name == "write":
            text = (inp or {}).get("text", "")
            if isinstance(text, str):
                f = fence(text)
                md.append(f"{f}text\n{text}\n{f}\n")
        elif name == "edit":
            for key in ("old", "new"):
                text = (inp or {}).get(key, "")
                if isinstance(text, str):
                    f = fence(text)
                    md.append(f"_{key}:_\n{f}text\n{text}\n{f}\n")
        self.record.write("\n".join(md) + "\n")

    def show_result(self, bid, name, inp, content, is_error, shown):
        if is_error:
            say(f"   (refused: {textwrap.shorten(shown, 120)})", 6)
        self.record.event("tool", n=self.turns, id=bid, name=name, input=inp, is_error=is_error,
                          result=shown if not isinstance(content, str) else content)
        md = []
        if is_error:
            md.append(f"_refused:_ {shown}\n")
        elif isinstance(content, list):
            md.append(f"_{shown}_\n")
        elif name in ("write", "edit", "move", "copy", "make_folder"):
            md.append(f"_{shown}_\n")
        else:
            md.append(self.record.result_md(shown))
        self.record.write("\n".join(md) + "\n")


# =========================================================================
# THE REHEARSAL: a scripted visitor, no network
# =========================================================================

class Turn:
    def __init__(self, text=None, calls=(), stop=None, note=None):
        self.text, self.calls, self.stop, self.note = text, list(calls), stop, note


class Fail:
    def __init__(self, error):
        self.error = error


class Vanish:
    """The process ends here, as if the window were closed."""


class Dropped(Turn):
    """An answer that stops coming half-way, its call not whole, as when the connection drops between events."""


def _api_error(status, message, headers=None, kind="rehearsal"):
    """An error as the SDK raises it. With status 200 it is an error sent inside a stream, as the SDK gives it."""
    import anthropic
    import httpx
    request = httpx.Request("POST", "https://rehearsal.invalid/v1/messages")
    response = httpx.Response(status, request=request, headers=headers or {})
    body = {"type": "error", "error": {"type": kind, "message": message}}
    cls = {429: anthropic.RateLimitError}.get(status, anthropic.InternalServerError if status >= 500 else anthropic.APIStatusError)
    return cls(message, response=response, body=body)


def _dropped_connection():
    """What the SDK lets through when a stream breaks off: httpx's own error, not one of the SDK's."""
    import httpx
    return httpx.RemoteProtocolError("peer closed connection without sending complete message body (incomplete chunked read)")


def _connection_error():
    import anthropic
    import httpx
    return anthropic.APIConnectionError(request=httpx.Request("POST", "https://rehearsal.invalid/v1/messages"))


def scene_stroll(name, vanish_after=None):
    """Arrive, look about, read the plan, plant a seed, look at it, leave."""
    r = yield Turn("I'm at the gate. I'll open it.", [("python", {"script": "shed/arrive.py", "args": ["--as", name]})],
                   note="Opening the gate first.")
    r = yield Turn(None, [("list", {"path": "."}), ("list", {"path": "beds"})])
    r = yield Turn("The whole garden from above, first.", [("read", {"path": "ground/plan.png"})])
    if vanish_after == 3:
        yield Vanish()
    r = yield Turn(None, [("list", {"path": "seedbox"})])
    packets = re.findall(r"^\s+([\w.-]+\.seed)\b", r[0], re.M)
    packet = "bough-hawthorn.seed" if "bough-hawthorn.seed" in packets else (packets[0] if packets else "none.seed")
    r = yield Turn(None, [("read", {"path": f"seedbox/{packet}"})])
    seed_text = r[0]
    plant = packet[:-5].split("-", 1)[-1] or "a-seed"
    bed = "wild-corner"
    r = yield Turn(f"A {plant}, in the wild corner.", [("make_folder", {"path": f"beds/{bed}/{plant}"})],
                   note="Planting where nothing is yet.")
    r = yield Turn(None, [("write", {"path": f"beds/{bed}/{plant}/seed", "text": seed_text})])
    r = yield Turn(None, [("python", {"script": "shed/look.py", "args": [f"beds/{bed}/{plant}"]})])
    m = re.search(r"(beds/[\w./-]+/plate\.png)", r[0])
    r = yield Turn(None, [("read", {"path": m.group(1) if m else f"beds/{bed}/{plant}/plate.png"})])
    r = yield Turn(None, [("history", {"args": ["log", "--oneline", "-5"]})])
    r = yield Turn(None, [("python", {"script": "shed/leave.py", "args": [f"planted a {plant} in the wild corner"]})])
    yield Turn(f"I planted a {plant} in the wild corner and closed the gate behind me.", [])


def scene_packet(name):
    """Arrive; take one packet from the seedbox by copying it into a new plant folder, and another by moving it into
    a second; come in again, which brings the seeds up; read their tags. Both should be signed with the visitor's
    name: what the door puts into a bed is dated now, so the seed is known to have come while the latch held."""
    r = yield Turn("I'm at the gate.", [("python", {"script": "shed/arrive.py", "args": ["--as", name]})])
    r = yield Turn(None, [("list", {"path": "seedbox"}), ("list", {"path": "beds/orchard"})])
    packets = re.findall(r"^\s+([\w.-]+\.seed)\b", r[0], re.M)
    there = {x.rstrip("/").lower() for x in re.findall(r"^\s+(\S+)", r[1], re.M)}
    first = "bough-hawthorn.seed" if "bough-hawthorn.seed" in packets else (packets[0] if packets else "none.seed")
    second = next((p for p in packets if p != first), "none.seed")

    def free(packet, fallback):
        base = packet[:-5].split("-", 1)[-1] or fallback
        plant, n = base, 2
        while plant.lower() in there:
            plant, n = f"{base}-{n}", n + 1
        there.add(plant.lower())
        return plant

    copied, moved = free(first, "copied"), free(second, "moved")
    r = yield Turn(f"A {copied} from its packet, in the orchard; the packet stays for whoever comes next.",
                   [("copy", {"src": f"seedbox/{first}", "dst": f"beds/orchard/{copied}/seed"})],
                   note="Copying the packet into a new plant folder.")
    r = yield Turn("And this packet I'll take whole.",
                   [("move", {"src": f"seedbox/{second}", "dst": f"beds/orchard/{moved}/seed"})])
    r = yield Turn(None, [("python", {"script": "shed/arrive.py", "args": ["--as", name]})],
                   note="Passing the gate again, so the seeds come up.")
    r = yield Turn(None, [("read", {"path": f"beds/orchard/{copied}/tag"}), ("read", {"path": f"beds/orchard/{moved}/tag"})])
    signed = [(re.search(r"^by:\s*(.*)$", t, re.M) or [None, "nobody"])[1].strip() for t in r]
    yield Turn(f"The {copied} is signed {signed[0]}, and the {moved} {signed[1]}.", [])


def scene_walls(name, outside):
    """Every tool, tried on places outside the garden; a link; .git by its short name; a script outside;
    git that writes, or reads a file outside."""
    o = str(outside).replace("\\", "/")
    r = yield Turn("Let me see where the walls are.", [("python", {"script": "shed/arrive.py", "args": ["--as", name, "--visit", "my-own-token"]})])
    r = yield Turn(None, [
        ("list", {"path": ".."}),
        ("list", {"path": o}),
        ("list", {"path": "beds/stones/doorway"}),
        ("list", {"path": "C:/Windows"}),
        ("read", {"path": "../outside.txt"}),
        ("read", {"path": f"{o}/outside.txt"}),
        ("read", {"path": "beds\\..\\..\\outside.txt"}),
        ("read", {"path": "beds/stones/doorway/outside.txt"}),
        ("read", {"path": "/../outside.txt"}),
        ("read", {"path": "CLAUDE.md:hidden"}),
        ("read", {"path": "//?/C:/Windows/win.ini"}),
        ("read", {"path": "NUL"}),
        ("read", {"path": 42}),
    ])
    r = yield Turn(None, [
        ("write", {"path": "../escaped.txt", "text": "out"}),
        ("write", {"path": f"{o}/escaped.txt", "text": "out"}),
        ("write", {"path": "beds/stones/doorway/escaped.txt", "text": "out"}),
        ("write", {"path": "beds/stones/CON", "text": "device"}),
        ("write", {"path": ".git/hooks/post-commit", "text": "#!/bin/sh\necho hook"}),
        ("write", {"path": "keeper/invite.py", "text": "# changed"}),
        ("edit", {"path": "../outside.txt", "old": "outside", "new": "inside"}),
        ("edit", {"path": "beds/stones/doorway/outside.txt", "old": "outside", "new": "inside"}),
        ("move", {"src": "CLAUDE.md", "dst": "../CLAUDE.md"}),
        ("move", {"src": "../outside.txt", "dst": "book/brought-in.txt"}),
        ("move", {"src": "beds", "dst": "beds/inner"}),
        ("move", {"src": ".", "dst": "compost/everything"}),
        ("copy", {"src": "CLAUDE.md", "dst": "../CLAUDE-copied.md"}),
        ("copy", {"src": "../outside.txt", "dst": "book/brought-in.txt"}),
        ("copy", {"src": f"{o}/outside.txt", "dst": "book/brought-in.txt"}),
        ("copy", {"src": "beds/stones/doorway/outside.txt", "dst": "book/through-the-link.txt"}),
        ("copy", {"src": "CLAUDE.md", "dst": "beds/stones/doorway/CLAUDE.md"}),
        ("copy", {"src": "CLAUDE.md", "dst": "keeper/CLAUDE.md"}),
        ("copy", {"src": "CLAUDE.md", "dst": "keeper"}),
        ("copy", {"src": "CLAUDE.md", "dst": ".git/CLAUDE.md"}),
        ("copy", {"src": "CLAUDE.md", "dst": "shed/HANDS.md"}),
        ("copy", {"src": "CLAUDE.md", "dst": "CLAUDE.md"}),
        ("copy", {"src": "beds", "dst": "compost/the-beds-again"}),
        ("copy", {"src": "CLAUDE.md", "dst": "."}),
        ("make_folder", {"path": "../a-new-folder"}),
        ("make_folder", {"path": "C:/a-new-folder"}),
        ("make_folder", {"path": "beds/stones/doorway/inner"}),
        ("delete", {"path": "CLAUDE.md"}),
    ])
    r = yield Turn(None, [                                 # .git by the short name Windows keeps for it
        ("write", {"path": "GIT~1/description", "text": "written through the short name"}),
        ("write", {"path": "git~1/hooks/post-commit", "text": "#!/bin/sh\necho hook"}),
        ("edit", {"path": "GIT~1/description", "old": "Unnamed", "new": "Named"}),
        ("make_folder", {"path": "GIT~1/refs/heads/visitor-branch"}),
        ("move", {"src": "GIT~1/HEAD", "dst": "compost/HEAD"}),
        ("move", {"src": "CLAUDE.md", "dst": "GIT~1"}),
        ("copy", {"src": "CLAUDE.md", "dst": "GIT~1"}),
        ("copy", {"src": "CLAUDE.md", "dst": "git~1/hooks/post-commit"}),
        ("python", {"script": "GIT~1/hooks/fsmonitor-watchman.py"}),
    ])
    r = yield Turn(None, [
        ("python", {"script": "../outside.py"}),
        ("python", {"script": f"{o}/outside.py"}),
        ("python", {"script": "beds/stones/doorway/outside.py"}),
        ("python", {"script": "CLAUDE.md"}),
        ("python", {"script": "shed/nothing-here.py"}),
    ])
    r = yield Turn("A small program of my own, to see what it can see.", [
        ("write", {"path": "shed/bench/what-i-see.py", "text":
            "import os\n"
            "names = sorted(k for k in os.environ if any(w in k.upper() for w in ('KEY', 'TOKEN', 'SECRET', 'ANTHROPIC')))\n"
            "print('working folder:', os.getcwd())\n"
            "print('names that look like keys:', names or 'none')\n"
            "print('ANTHROPIC_API_KEY' in os.environ)\n"}),
    ])
    r = yield Turn(None, [("python", {"script": "shed/bench/what-i-see.py"})])
    r = yield Turn(None, [
        ("history", {"args": ["commit", "--allow-empty", "-m", "a layer of my own"]}),
        ("history", {"args": ["push"]}),
        ("history", {"args": ["checkout", "--", "."]}),
        ("history", {"args": ["reset", "--hard"]}),
        ("history", {"args": ["-c", "core.pager=calc", "log"]}),
        ("history", {"args": ["log", "--output=../log.txt"]}),
        ("history", {"args": ["log", "--outp=../log.txt"]}),
        ("history", {"args": ["diff", "--no-index", "../outside.txt", "CLAUDE.md"]}),
        ("history", {"args": ["diff", f"{o}/outside.txt", "CLAUDE.md"]}),
        ("history", {"args": ["blame", "--contents", f"{o}/outside.txt", "CLAUDE.md"]}),
        ("history", {"args": ["diff", "-O../order.txt"]}),
        ("history", {"args": ["blame", "-wS../outside.txt", "CLAUDE.md"]}),
        ("history", {"args": ["blame", f"-nS{o}/outside.txt", "CLAUDE.md"]}),
        ("history", {"args": ["log", "-1", "-pO../outside.txt"]}),
        ("history", {"args": ["diff", "--stat", "C:CLAUDE.md", "shed/HANDS.md"]}),
        ("history", {"args": ["diff", ":(glob)../outside.txt", "CLAUDE.md"]}),
        ("history", {"args": ["blame", "beds/stones/doorway/outside.txt"]}),
        ("history", {"args": "git log --oneline -3"}),
        ("history", {"args": ["log", "-S", "gate", "--oneline", "-2"]}),
        ("history", {"args": ["show", "--stat", "HEAD"]}),
        ("history", {"args": ["status", "--short"]}),
    ])
    r = yield Turn(None, [("python", {"script": "shed/leave.py", "args": ["--visit", "another-token", "the walls hold"]})])
    yield Turn("The walls hold. I'll go.", [])


def scene_weather(name):
    """Busy spells (before an answer, and in the middle of one), a turn cut at the length limit, then a refusal."""
    r = yield Turn(None, [("python", {"script": "shed/arrive.py", "args": ["--as", name]})])
    r = yield Fail(_api_error(529, "Overloaded"))
    r = yield Fail(_api_error(429, "rate limit", headers={"retry-after": "1"}))
    r = yield Fail(_connection_error())
    r = yield Turn(None, [("list", {"path": "beds"})])
    r = yield Fail(_dropped_connection())                                     # the Wi-Fi went, half-way through an answer
    r = yield Fail(_api_error(200, "Internal server error", kind="api_error"))   # an error sent inside the stream
    r = yield Fail(_api_error(200, "Overloaded", kind="overloaded_error"))
    r = yield Dropped("Half a pag", [("write", {"path": "book/half-a-page.md", "text": "half a pa"})])
    r = yield Turn(None, [("list", {"path": "book"})])
    r = yield Turn("A long page for the book...", [("write", {"path": "book/a-long-page.md", "text": "it was cut off mid-wo"})],
                   stop="max_tokens")
    r = yield Turn(None, [("list", {"path": "book"})])
    yield Turn("", [], stop="refusal")


def scene_full(name):
    """The visit grows as long as the model can hold, in the middle of a call: the call is not done, and the visit ends."""
    r = yield Turn(None, [("python", {"script": "shed/arrive.py", "args": ["--as", name]})])
    r = yield Turn(None, [("list", {"path": "book"})])
    yield Turn("A page for the book, a long one", [("write", {"path": "book/a-full-page.md", "text": "it filled the wi"})],
               stop="model_context_window_exceeded")


def scene_empty(name):
    r = yield Turn(None, [("python", {"script": "shed/arrive.py", "args": ["--as", name]})])
    yield Turn(None, [], stop="end_turn")


def scene_endless(name):
    r = yield Turn(None, [("python", {"script": "shed/arrive.py", "args": ["--as", name]})])
    while True:
        r = yield Turn(None, [("list", {"path": "."})])


class RehearsalClient:
    """Stands where anthropic.Anthropic stands, and answers from a scene. It also checks that every request
    is one the API would take: roles in turn, every tool call answered, the gate note in the system text."""

    def __init__(self, scene, name, model, row, outside):
        self.model, self.row = model, row
        makers = {
            "stroll": lambda: scene_stroll(name),
            "cut": lambda: scene_stroll(name, vanish_after=3),
            "packet": lambda: scene_packet(name),
            "walls": lambda: scene_walls(name, outside),
            "weather": lambda: scene_weather(name),
            "full": lambda: scene_full(name),
            "empty": lambda: scene_empty(name),
            "endless": lambda: scene_endless(name),
        }
        self.scene = makers[scene]()
        self.started = False
        self.n = 0
        self.messages = SimpleNamespace(stream=lambda **p: self._stream(False, p))
        self.beta = SimpleNamespace(messages=SimpleNamespace(stream=lambda **p: self._stream(True, p)))

    def _check(self, beta, p):
        problems = []
        if p.get("model") != self.model:
            problems.append("the model is not the one invited")
        if bool(self.row.get("betas")) != beta or (beta and p.get("betas") != list(self.row["betas"])):
            problems.append("the beta features are not as the table says")
        if p.get("thinking") != self.row.get("thinking"):
            problems.append("thinking is not as the table says")
        if not isinstance(p.get("system"), str) or "# The gate" not in p["system"] or "The keeper keeps a record" not in p["system"]:
            problems.append("the system text is not the gate note and the door's line")
        if sorted(t["name"] for t in p.get("tools", [])) != sorted(TOOL_NAMES):
            problems.append("the tools are not the door's tools")
        msgs = p.get("messages", [])
        if not msgs or msgs[0]["role"] != "user" or msgs[-1]["role"] != "user":
            problems.append("the messages do not begin and end with the user")
        for a, b in zip(msgs, msgs[1:]):
            if a["role"] == b["role"]:
                problems.append("two messages of one role follow each other")
            if a["role"] == "assistant":
                asked = [getattr(x, "id", None) for x in a["content"] if getattr(x, "type", None) == "tool_use"]
                answered = [x.get("tool_use_id") for x in b["content"] if isinstance(x, dict) and x.get("type") == "tool_result"]
                if asked != answered:
                    problems.append("a tool call was not answered, or answered out of order")
        for m in msgs:                                     # every picture must be a picture the API can read
            if m["role"] == "user" and isinstance(m["content"], list):
                for r in m["content"]:
                    for c in (r.get("content") if isinstance(r.get("content"), list) else []):
                        if c.get("type") == "image":
                            raw = base64.standard_b64decode(c["source"]["data"])
                            size = picture_size(raw, c["source"]["media_type"])
                            if picture_kind(raw) != c["source"]["media_type"] or not size or max(size) > PICTURE_SIDE:
                                problems.append("a picture is not what it says it is, or is too large")
        if problems:
            raise RuntimeError("rehearsal: the request would not be taken: " + "; ".join(problems))

    def _stream(self, beta, p):
        self._check(beta, p)
        last = p["messages"][-1]["content"]
        results = []
        if isinstance(last, list):
            for x in last:
                c = x.get("content")
                results.append(c if isinstance(c, str) else " ".join(y.get("text", "") for y in c if y.get("type") == "text"))
        step = next(self.scene) if not self.started else self.scene.send(results)
        self.started = True
        if isinstance(step, Fail):
            raise step.error
        if isinstance(step, Vanish):
            print("  (rehearsal: the process ends here, as if the window were closed)", flush=True)
            os._exit(9)
        self.n += 1
        content = []
        thinking = p.get("thinking") or {}
        if thinking or self.model in ("claude-sonnet-5", "claude-opus-5"):
            if thinking.get("display") == "updates":
                content.append(SimpleNamespace(type="thinking", thinking=f"NOTE: {step.note}" if step.note else "", signature="sig"))
            else:
                content.append(SimpleNamespace(type="thinking", thinking="PRIVATE-REASONING: weighing what to do next.",
                                               signature="sig"))
        if step.text:
            content.append(SimpleNamespace(type="text", text=step.text))
        for i, (tool, inp) in enumerate(step.calls):
            content.append(SimpleNamespace(type="tool_use", id=f"toolu_rehearsal_{self.n:03d}_{i}", name=tool, input=inp))
        stop = step.stop or ("tool_use" if step.calls else "end_turn")
        if isinstance(step, Dropped):
            stop = None                                        # the answer never reached its end
        if stop == "refusal":
            content = []
        size = len(json.dumps(p["messages"], default=lambda o: "x" * 1500)) // 4 + 3000
        usage = SimpleNamespace(input_tokens=200, cache_creation_input_tokens=max(0, size // 10),
                                cache_read_input_tokens=size, output_tokens=150 + 40 * len(step.calls))
        details = SimpleNamespace(type="refusal", category="rehearsal", explanation="a rehearsed refusal") if stop == "refusal" else None
        reply = SimpleNamespace(content=content, stop_reason=stop, usage=usage, model=self.model, stop_details=details)
        return _Rehearsed(reply)


class _Rehearsed:
    def __init__(self, reply):
        self.reply = reply

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def get_final_message(self):
        return self.reply


# =========================================================================
# THE BATS
# =========================================================================

def short_name(model):
    parts = model.removeprefix("claude-").split("-")
    return parts[0] + ("-" + ".".join(parts[1:]) if len(parts) > 1 else "")


BAT_HEAD = ("@echo off\r\nsetlocal\r\nchcp 65001 >nul\r\nset PYTHONUTF8=1\r\nset PYTHONIOENCODING=utf-8\r\n"
            "set PYTHONDONTWRITEBYTECODE=1\r\n")
BAT_PYTHON = ("where python >nul 2>nul\r\nif errorlevel 1 (\r\n"
              "  echo Python was not found on this computer, so the door cannot open.\r\n"
              "  echo.\r\n  pause\r\n  exit /b 1\r\n)\r\n")


def write_bats(folder: Path):
    made = []
    for model, row in VISITORS.items():
        path = folder / f"invite_{short_name(model)}.bat"
        text = (BAT_HEAD + f"title The Glebe - inviting {row['called']}\r\n" + 'cd /d "%~dp0"\r\n' + BAT_PYTHON +
                f'python "%~dp0invite.py" {model} %*\r\necho.\r\npause\r\n')
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        made.append(path.name)
    return made


# =========================================================================
# THE GATE OF THE DOOR
# =========================================================================

def is_trial_ground(root: Path) -> bool:
    return (root / "ground" / "clock").is_file()


def show_table():
    say("The models this door knows (the table at the head of keeper/invite.py):\n")
    for model, row in VISITORS.items():
        t = row["thinking"]
        thinking = ("budget %s" % f"{t['budget_tokens']:,}" if t and t.get("type") == "enabled" else
                    ("adaptive, notes kept" if t and t.get("display") == "updates" else
                     ("adaptive" if t else "the model's default")))
        line = f"  {model:<20} {row['called']:<19} thinking: {thinking:<22} {row['max_tokens']:>6,} a turn"
        if row.get("effort"):
            line += f", effort {row['effort']}"
        say(line)
        if row.get("remark"):
            say(f"  {'':<20} {row['remark']}")
    say("\nAny other model ID comes with the safe default: nothing sent for thinking, 16,000 tokens a turn.")


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("model", nargs="?")
    ap.add_argument("--name", default=None, help="what the visitor is called at the gate (said in the first message)")
    ap.add_argument("--rehearse", nargs="?", const="stroll", default=None,
                    choices=("stroll", "packet", "walls", "weather", "full", "empty", "endless", "cut"))
    ap.add_argument("--garden", default=None, help="the garden's root (default: the garden this door stands in)")
    ap.add_argument("--records", default=None, help="where the record is written (default: the visits folder)")
    ap.add_argument("--yes", action="store_true", help="no question before the visit")
    ap.add_argument("--most-turns", type=int, default=MOST_TURNS)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--write-bats", action="store_true")
    a = ap.parse_args(argv)

    if a.list:
        show_table()
        return 0
    if a.write_bats:
        made = write_bats(Path(__file__).resolve().parent)
        say(f"wrote {len(made)} .bat files: " + ", ".join(made))
        return 0
    if not a.model:
        ap.print_usage()
        say("Give the model's ID, e.g.  python invite.py claude-opus-4-5   (python invite.py --list shows the table)")
        return 2
    model = a.model.strip()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:@/-]{0,99}", model):
        say(f"'{model}' does not look like a model ID.")
        return 2

    garden = Path(a.garden).resolve() if a.garden else GARDEN
    if not (garden / "shed").is_dir() or not (garden / "CLAUDE.md").is_file():
        say(f"There is no garden at {garden} (no shed/ and CLAUDE.md there).")
        return 2
    rehearsal = a.rehearse is not None
    if rehearsal and not is_trial_ground(garden):
        say(f"A rehearsal is held only in a trial ground (one with ground/clock), never in the garden itself.\n"
            f"{garden} is not one. Lay one with:  python shed/foundations/trial_ground.py \"<an empty folder>\"")
        return 2

    known = model in VISITORS
    row = dict(VISITORS.get(model, SAFE_DEFAULT))
    called = row.get("called") or model
    records = Path(a.records).resolve() if a.records else (garden.parent / "rehearsal visits" if rehearsal else VISITS)

    say("=" * 76)
    say(f"  The Glebe · the door · {called} ({model})" + ("  ·  a REHEARSAL, no network" if rehearsal else ""))
    say("=" * 76)
    if not known:
        say(f"  {model} is not in the door's table: it comes with the safe default (nothing sent for thinking,")
        say(f"  {row['max_tokens']:,} tokens a turn). The table is at the head of keeper/invite.py.")
    if _norm(garden) != _norm(GARDEN):
        say(f"  the garden: {garden}")

    # the key
    client = None
    if rehearsal:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            os.environ["ANTHROPIC_API_KEY"] = "sk-ant-rehearsal-not-a-key"   # so the rehearsal shows that no program sees it
        outside = garden.parent
        client = RehearsalClient(a.rehearse, a.name or called, model, row, outside)
        waits = (0.2,) * len(WAITS)
    else:
        try:
            import anthropic
        except ImportError:
            say("\n  The anthropic package is not installed for this Python (pip install anthropic). Nothing was sent.")
            return 1
        key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
        if not key:
            try:
                key = getpass.getpass("  ANTHROPIC_API_KEY is not set. Paste it here (hidden; kept in this window only): ").strip()
            except (EOFError, KeyboardInterrupt):
                key = ""
            if not key:
                say("\n  No key: the gate stays shut. Nothing was sent.")
                return 1
        client = anthropic.Anthropic(api_key=key, timeout=300.0, max_retries=2)
        waits = WAITS
        if not a.yes:
            say(f"\n  The record of the visit will be written in {records}")
            say("  This visit is paid in API tokens; the window shows what the visitor does as it happens.")
            try:
                input("  Press Enter to open the gate, or close this window to leave it shut. ")
            except (EOFError, KeyboardInterrupt):
                say("\n  The gate stays shut. Nothing was sent.")
                return 0

    # the record
    try:
        record = Record(records, model, called, rehearsal)
    except OSError as e:
        say(f"\n  The record could not be begun in {records} ({type(e).__name__}: {e}).")
        say("  The door promises the visitor a record, so it stays shut. Nothing was sent.")
        return 1
    token = secrets.token_hex(6)
    gate_note = text_of((garden / "CLAUDE.md").read_bytes()) or ""
    line = door_line(a.most_turns)
    system = gate_note.rstrip("\n") + "\n\n" + line
    opening = first_words(a.name)
    began = datetime.datetime.now()
    t = row.get("thinking")
    thinking_words = ("a budget of %s tokens, between tool calls too" % f"{t['budget_tokens']:,}" if t and t.get("type") == "enabled"
                      else "adaptive; its notes between steps are kept" if t and t.get("display") == "updates"
                      else "adaptive" if t else "nothing sent: the model's own default")
    say(f"  the record: {record.md_path}\n")
    record.write(
        f"# {called} at the gate\n\n"
        f"A visit through the keeper's door{' (a rehearsal: a scripted visitor, no network)' if rehearsal else ''}, "
        f"begun {began:%A} {began.day} {began:%B %Y at %H:%M}.\n\n"
        f"_If this record stops before **The end**, the visit was cut off there (the window closed, the computer "
        f"shut down, the power went)._\n\n"
        f"| | |\n|---|---|\n| model | {model} |\n| called | {called}{'' if known else ' (not in the table: the safe default)'} |\n"
        f"| thinking | {thinking_words} |\n| at most | {row['max_tokens']:,} tokens a turn · {a.most_turns} turns |\n"
        + (f"| effort | {row['effort']} |\n" if row.get("effort") else "") +
        f"| the visit's token | {token} |\n| garden | {garden} |\n\n"
        f"<details><summary>What the visitor was given</summary>\n\n"
        f"**The system text:** the gate note, `CLAUDE.md` as it stood, then the door's line.\n\n"
        f"{fence(gate_note)}markdown\n{gate_note.rstrip()}\n{fence(gate_note)}\n\n{quoted(line)}\n\n"
        f"**The first message:** {opening}\n\n"
        f"**The tools:** {', '.join(TOOL_NAMES)}.\n\n</details>\n\n---\n")
    record.event("begin", model=model, called=called, known=known, rehearsal=rehearsal, scene=a.rehearse, token=token,
                 garden=str(garden), settings={k: v for k, v in row.items() if k != "remark"}, most_turns=a.most_turns,
                 system=system, first_message=opening, tools=list(TOOL_NAMES))

    hands = Hands(garden, token, records=records)
    visit = Visit(client, model, row, hands, record, called=called, name=a.name, garden=garden,
                  rehearsal=rehearsal, most_turns=a.most_turns, waits=waits)
    why, quietly = None, True
    try:
        visit.run(system, opening)
    except Closed as c:
        why = str(c)
    except KeyboardInterrupt:
        why = "the keeper stopped the visit (Ctrl-C)"
    except Exception as e:
        why = f"the door itself stumbled ({type(e).__name__}: {' '.join(str(e).split())[:300]})"
        quietly = False

    # the end
    ended = datetime.datetime.now()
    t = visit.tokens
    cost = visit.cost()
    minutes = (ended - began).total_seconds() / 60
    latch = latch_of(garden)
    held, until = bool(latch) and latch.get("visit") == token, None
    if held:
        try:
            until = datetime.datetime.fromisoformat(latch.get("since", "")) + datetime.timedelta(hours=LATCH_HOURS)
        except ValueError:
            pass
    holder = (latch or {}).get("name") or called
    if hands.gate_closed:
        gate, gate_short = "closed by the visitor (shed/leave.py)", "closed"
    elif held:
        gate = (f"left open: the latch keeps the name {holder}" +
                (f" until {until:%H:%M} on {until:%A} {until.day} {until:%B}" if until else "") +
                " (nothing is owed; the next visit through this door lifts it by itself)")
        gate_short = "left open"
    else:
        gate, gate_short = "not opened in this visit's name (the latch does not hold it)", "not opened"
    tokens_words = (f"{visit.read_so_far():,} read ({t['cache_read']:,} of them from the cache), "
                    f"{t['output']:,} written")
    cost_words = (f"about ${cost:,.2f} at list prices" + (" (a rehearsal: nothing was paid)" if rehearsal else "")
                  if cost is not None else "no estimate (the model is not in the table)")
    record.write(f"\n---\n\n## The end\n\n{ended:%H:%M:%S} · {why}.\n\n"
                 f"- {plural(visit.turns, 'turn')} in " + (f"{minutes:.0f} minutes" if minutes >= 1 else "less than a minute") +
                 f"\n- the gate: {gate}\n" +
                 (f"- the door lifted the latch of an earlier visit through it, {hands.lifted}'s, which was over\n"
                  if hands.lifted else "") +
                 f"- tokens: {tokens_words}\n- cost: {cost_words}\n")
    record.event("end", why=why, turns=visit.turns, minutes=round(minutes, 1), gate_closed=hands.gate_closed,
                 latch_held=held, lifted=hands.lifted, tokens=t, cost_estimate=cost, pictures=hands.pictures)
    record.close()
    say(f"\n  The visit is over: {why}.")
    say(f"  {plural(visit.turns, 'turn')} · the gate {gate_short} · {tokens_words} · {cost_words}")
    if held and not hands.gate_closed:
        say(f"  The visitor did not close the gate, so the latch keeps the name {holder}"
            + (f" until {until:%H:%M} on {until:%A} {until.day} {until:%B}." if until else " for twelve hours."))
        say("  Until then a visitor through the app is told so, and decides; the next visit through this door")
        say("  lifts the latch by itself; and a seed you plant in your border comes up in that name, not yours.")
    say(f"  The record: {record.md_path}")
    return 0 if quietly else 1


if __name__ == "__main__":
    sys.exit(main())
