"""
The ground: what lies behind the three doors.

The garden is a folder of files, and this is the part of it that turns the
calendar into growth. When the gate opens it works out how many days have
gone by since anyone was here, lives them one at a time under each day's
sky, and writes down what happened. It also signs things, keeps the layers,
and draws. Nothing here is hidden from a visitor: every record it keeps is a
plain file, and this is the file that keeps them.

Read from the top, it goes:

    small things     reading and writing text, the clock, troubles
    beds and plants  the garden as it stands in its files
    kinds            loading species/<kind>.py, and calling into it safely
    what a kind is told   ctx: the date, the sky, neighbours, the soil
    inks             which ink belongs to which hand
    tending          sprouting new seeds, writing tags, noticing the heap
    the days         living a day; letting many pass; the heap rotting
    creatures        creatures/<name>.py: what lives in the days besides the plants,
                     the hands they are given (the Garden), their records, the larder,
                     the richness of the beds, the things they make; and the gravel
    layers           git, guarded: the garden lives without it
    the latch        who is in the garden now, and who came before
    drawing          the plate of a plant, the sheet of a bed, the plan
    the bolt         one door at a time: two never work the garden at once
    apart            kinds are run in a second process, watched from the door
    the doors        arrive, look, leave

Three promises shape all of it. The gate always opens: no file a hand has
touched, no broken kind, no missing folder may stop an arrival. So every
reader forgives, every call into a kind is guarded, and the kinds are run
apart from the door, where one that hangs or walks out can be left behind.
A day is lived once: what the days do to the garden is written down whole
or not at all, so an arrival cut short loses nothing and repeats nothing.
And nothing is owed: no door asks for anything, and what one visitor leaves
undone the next arrival settles quietly.

Two smaller promises came later, and shape the doors: every signature is
true (a name signs only what its visit did, while its latch held; the
garden's own names are never a visitor's; a hand on a plant leaves a ring
saying whose), and every door fits in the time a visitor's tool will wait
(ARRIVAL_MOST, LOOK_MOST: what there is no time to draw is drawn later).

GROUND.md, in foundations/, is the record this was built from; where its
older text and its Rulings of 30 September differ, this file follows the
Rulings. Standard library only.
"""

from __future__ import annotations

import atexit
import datetime
import hashlib
import importlib.util
import json
import math
import mmap
import os
import pickle
import queue
import random
import re
import shutil
import signal
import struct
import subprocess
import sys
import threading
import time
import traceback
import types
from dataclasses import dataclass, field
from pathlib import Path

try:
    import msvcrt                          # Windows: what the bolt is made of
except ImportError:
    msvcrt = None
try:
    import fcntl                           # and everywhere else
except ImportError:
    fcntl = None

SHED = Path(__file__).resolve().parent
if str(SHED) not in sys.path:
    sys.path.insert(0, str(SHED))          # so that a kind can "import hands"


def _own_copy(name):
    """A module of the shed, loaded afresh under a name of its own.

    `hands` is one file but never one shared thing: the ground reads the
    garden with a copy of its own, and every kind is handed another. So a
    kind that changes `hands` changes only its own copy; no other kind
    feels it, and the ground does not.
    """
    _own_copy.made += 1
    spec = importlib.util.spec_from_file_location("glebe_%s_%d" % (name, _own_copy.made), SHED / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_own_copy.made = 0

hands = _own_copy("hands")
import sky

Date = datetime.date
ONE_DAY = datetime.timedelta(days=1)

# ------------------------------------------------------------ the measures

BODY_MOST = 60_000        # characters a body may hold
DEAD_DAYS = 120           # days a dead plant stands before it is carried to the heap
ROT_DAYS = 60             # days a thing lies on the heap before it rots
ROT_LINES = 200           # lines of a rotting file that reach the humus
ROT_LINE = 300            # characters of each
HUMUS_MOST = 4000         # lines the humus keeps
HUMUS_TOP = 1000          # new humus is scattered among the newest lines, so the oldest lie at the top
SOWN_A_DAY = 2            # seedlings that may come up in the whole garden in one day
LATCH_HOURS = 12          # how long an unclosed visit keeps the gate
MOST_DAYS = 3660          # days lived in one arrival at the very most (ten years)
ARRIVAL_MOST = 85.0       # seconds a whole arrival keeps within: a visitor's shell call is usually cut at 120, and an
                          # arrival cut short is the case that loses most. Whatever is not drawn by then, look draws.
DAYS_BUDGET = 40.0        # seconds an arrival may spend on the days before it opens the gate anyway
DRAW_BUDGET = 30.0        # seconds an arrival may spend drawing, at most; less if the days and the rest took their time
TAIL_SECONDS = 5.0        # of an arrival's time, what is kept back for the note and the ground's small records at the end
LOOK_MOST = 80.0          # seconds a look keeps within, for the same reason; what it cannot draw in time, the next look does
KIND_SECONDS = {"sprout": 3.0, "day": 3.0, "cast": 3.0, "describe": 2.0, "draw": 8.0, "load": 5.0,    # then a kind is stopped
                "size": 1.0,                                  # (how large a plant is, for the plan: see `_Studio.size_of`)
                "flowers": 1.0, "bitten": 2.0,                # (what creatures ask of a kind)
                "live": 5.0, "after": 3.0, "present": 2.0}    # and a creature: its day (with the kinds it asks), after, present
STOPS_MOST = 2            # a plant whose call was stopped this often in one pass through a door sleeps alone for the rest of
                          # it; a kind is set aside when the calls of two of its plants were stopped (see `_count_stop`)
ASIDE_DAYS = 30           # days a kind, or a plant sleeping alone, stays set aside (ground/aside) before it is asked once more
SHARE_MOST = DAYS_BUDGET / 3      # seconds of the days' time that all slow kinds together may take in one passing
SLOW_CALL = 0.1           # seconds for one plant's day, on average, from which a kind counts as slow (its duty is about 0.05)
SLOW_SEEN = 1.0           # seconds a kind must have spent before it can be judged slow (one slow call is no habit)
LOCK_OLD = 60.0           # seconds after which a lock left lying in .git is taken to be nobody's
SOIL_FILE_MOST = 200_000  # bytes of each soil text a kind is shown
STATE_MOST = 20_000       # characters a creature's own file may hold (a save of more is refused)
THING_MOST = 20_000       # characters a thing a creature makes may hold
LARDER_MOST = 400         # seeds the larder holds; past that the oldest are found and eaten
FADE_DAYS = 45.0          # a bed's richness is worth 1/e as much after this many days: in a season, little is left
CREATURE_LINES = 3        # lines one creature may add to the almanac in one day
PRESENT_MOST = 3          # creatures that may be met in one arrival note
ACTS_A_DAY = {"bite": 200, "pollen": 400, "carry": 40, "cache": 40, "drop": 200, "make": 3, "unmake": 3,
              "nudge": 5, "enrich": 5}                # what one creature may do in one day, at most, of each
GLASS_WEEK = 7            # days that pass under the glass each time the gate opens to a new visit (see `Glass`)
GLASS_OWED_MOST = 371     # days the glass may owe at the very most: a year of them, and no more are let gather
GLASS_BUDGET = 12.0       # seconds an arrival may spend on the days under the glass

THE_DAYS = "the days"
THE_KEEPER = "the keeper"
UNSEEN = "an unseen hand"
THE_BUILDERS = "the builders"         # who signs a trial ground's first layer
THE_GLASS = "the glass"               # who signs the days lived under the glass (see `Glass`)
OWN_NAMES = (THE_DAYS, THE_KEEPER, UNSEEN, THE_BUILDERS, THE_GLASS)     # the garden's own names: no visitor signs with one
NO_NAME = "a visitor who gave no name"
CALLED = "a visitor who gave the name %s"      # how someone signs who arrives under one of the garden's own names
FIXED_INKS = {THE_DAYS: "#3a3a3a", THE_KEEPER: "#8a1c2c", UNSEEN: "#7b3f73"}
                          # the days near-black; the keeper a deep red; an unseen hand a dusky plum (once a mid grey,
                          # which the kinds' drawings read as dead: a living plant set by no one known is not dead)
HAND_INKS = ("#1f4e9c", "#c25e00", "#6a2c91", "#00808a", "#a0522d",
             "#c2185b", "#b8860b", "#0b2545", "#7a5c00", "#4a3f8f")     # none is green: green is the fresh ink

FOLDERS = ("beds", "book", "compost", "gate", "seedbox", "species", "ground")
KEEPERS_BED = "gate-border"
KEEPERS_PATHS = ("gate/", "beds/%s/" % KEEPERS_BED, "keeper/")     # and ground/place: what the keeper may be taken to have done
WILD_BED = "wild-corner"
OWN_RECORDS = ("ground/inks", "ground/visits", "ground/almanac", "ground/aside", "compost/.heap", "compost/humus",
               "ground/larder", "ground/rich", "ground/made", "ground/pollen", "ground/glass", "ground/under-glass")
DRAWN_FILES = ("plate.png", "plate.svg", ".left", ".drawn")

# Sentences the ground writes for a visitor to read and also reads back itself. Each is named here, once,
# so that whoever rewords one changes what is written and what is read together.
RING_PLANTED = "planted by "                  # rings:   2026-10-03  planted by claude-opus-4-7
RING_SELF_SOWN = "self-sown"                  # rings:   2026-10-04  self-sown from north-wall/quince
                                              #          2026-10-04  self-sown, cross of north-wall/quince × orchard/medlar
                                              # (a seed the days sowed: whether it has come up is its kind's to say)
RING_ROOTED = "rooted from "                  # rings:   2026-10-04  rooted from north-wall/twist   (a piece of its parent
                                              #          that took root beside it: a layer, a runner; see `_sow_one`)
RING_SOWN_ONCE = "came up by itself, "        # rings:   what the first trial grounds said for a seed the days sowed
SOWN_RINGS = (RING_SELF_SOWN, RING_ROOTED, RING_SOWN_ONCE)     # rings that say the days brought a plant in
RING_AILING = "ailing: "                      # rings:   a fault in the plant's kind or its body; said once while it stands
RING_ASLEEP = "asleep: "                      # rings:   a grown plant whose kind cannot be read
RING_SEED = "still a seed: "                  # rings:   a seed that has not come up, and why
RING_WELL = "well again"                      # rings:   the fault is over
RING_FOUND_DEAD = "found dead"                # rings:   a body some hand marked dead, with no day to say when
RING_AGAIN = "came up again from the seed"    # rings:   written in tending, for a plant whose body was taken away
RING_RENAMED = "renamed: it was "             # rings:   written in tending, for a plant a hand moved or renamed
TENDING_RINGS = (RING_PLANTED, RING_SEED, RING_AGAIN, RING_RENAMED, "came under the glass",
                 "came out from under the glass")        # what tending writes: no sign that a day was lived
RING_CUT = "cut back by "                     # rings:   2026-10-09  cut back by fable-5          (a hand's ring: see `_hand_rings`)
RING_TENDED = "tended by "                    # rings:   2026-10-09  tended by fable-5            (its body, seed or tag changed)
RING_MOVED = "moved here from %s by %s"       # rings:   2026-10-09  moved here from north-wall by fable-5
RING_RENAMED_BY = "renamed by "               # rings:   2026-10-09  renamed by fable-5
HAND_RINGS = (RING_CUT, RING_TENDED, RING_MOVED.split("%")[0], RING_RENAMED_BY)    # written when a visit is laid down: no lived day
CAME_UP = " came up ("                        # tending: north-wall/quince came up (bough)
PLANTED_WHOLE = " was planted whole ("        # tending: orchard/saffron-ii was planted whole (bulb)   (body and all)
VISIT_IN = "came in"                          # visits:  2026-10-03 17:42  came in · claude-opus-4-7
VISIT_OUT = "closed the gate"                 # visits:  2026-10-03 18:10  closed the gate · claude-opus-4-7 · a few words
VISIT_OPEN = "found the gate left open by "   # visits:  2026-10-24 09:12  found the gate left open by fable-5
                                              # (written by the next door, at its own time: when the visit itself went
                                              # out, nobody saw)
VISIT_OPEN_ONCE = "went out, the gate left open"     # visits:  what the first trial grounds wrote instead
DAYS_LAYER = "%s, %s to %s. %s."              # layers:  12 days, 2026-09-19 to 2026-09-30. 9 plants grew.
GLASS_LAYER = "under the glass: %s, %s to %s. %s."     # layers: under the glass: 7 days, 2027-03-08 to 2027-03-14. 2 plants grew.
RING_UNDER = "came under the glass: from here its days are the glass's"       # rings: written in tending, for a plant found
RING_OUT = "came out from under the glass: from here its days are the garden's"   # on the other side of the glass from the
                                              # one its tag names (a hand carried it across, or set the glass over its bed,
                                              # or took it off). The two sides keep two calendars: the ring says where one
                                              # ends in its rings and the other begins.
GLASS_RINGS = ("came under the glass", "came out from under the glass")
TAG_UNDER = "under: glass"                    # tags:    the line a plant's tag bears while it lives under the glass
GLASS_WITNESS = ".glass"                      # beds/<bed>/.glass: the day the glass stands at, kept beside each bed under
                                              # it. A witness outside ground/ and outside the layers, for a garden that
                                              # keeps no layers and has lost its records (see `_glass_stood`)
LEFT_OPEN = "left without closing the gate"   # layers:  a visit the next arrival laid down, in its visitor's name
RING_NUDGED = "shifted a little by "          # rings:   2026-10-09  shifted a little by mole (a molehill came up)
FOUNDED = "the ground was laid %s ago today"  # almanac: under the day line of each 30 September (the founding day):
                                              # "the ground was laid a year ago today", "... two years ago today"
TOO_MUCH = "its %s is more than its kind can %s in time"     # rings: a plant that sleeps alone (see `_count_stop`)
CREATURE = "creatures/"                       # how a creature is named where kinds are named too (ground/aside, the
                                              # crumb, the set-aside kinds): creatures/bees
PROGRAM_NAME = re.compile(r"[a-z0-9_][a-z0-9_\-]{0,40}")          # a kind's name (seeds say it in lower case)
CREATURE_NAME = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_\-]{0,40}")   # a creature's name: its file's name

DAGGER = hands.DAGGER
WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
MONTHS = ("January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December")
RESERVED = {"con", "prn", "aux", "nul"} | {"com%d" % n for n in range(1, 10)} | {"lpt%d" % n for n in range(1, 10)}

_ISO = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
_DATED = re.compile(r"^(\d{4})-(\d{2})-(\d{2})(?=\s|$)")
SKY_SOURCES = ("reckoned", "gate", "open-meteo")                   # where a day's sky may come from (sky.Sky.source)
_DAY_LINE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})\s.*\[(%s)\]\s*$" % "|".join(map(re.escape, SKY_SOURCES)))
                          # a day as the almanac holds it: date, sky, and in brackets where the sky came from


# ============================================================ small things

def _read(path, most=2_000_000) -> str:
    """A file's text, however a hand saved it. What is missing or cannot be read is ''."""
    try:
        with open(path, "rb") as handle:
            data = handle.read(most)
    except OSError:
        return ""
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):                 # PowerShell's ">" writes UTF-16
        text = data.decode("utf-16", errors="replace")
    else:                                                      # and its ">>" adds UTF-16 to a UTF-8 file:
        text = data.decode("utf-8", errors="replace").replace("\0", "")     # the letters are all there, between zeros
    return _plain(text)


def _plain(text) -> str:
    """Text as the garden keeps it: no byte-order mark at its head, and `\\n` at the end of every line."""
    return text.lstrip(chr(0xFEFF)).replace("\r\n", "\n").replace("\r", "\n")


def _write(root, path, text) -> bool:
    """Write a text file whole, or not at all. True if it was written; if not, the trouble is noted and the day goes on.

    The new text is written beside the file and then moved into its place
    in one step, so that a run cut short at any moment leaves the old file
    or the new one, never an empty or a half-written one.
    """
    path = Path(path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            _put_in_place(_stage(path, text), path)
        except OSError:                                        # no room for a second file, or the place is held:
            _remove(_part(path))                               # then it is written where it stands
            with open(path, "w", encoding="utf-8", errors="replace", newline="\n") as handle:
                handle.write(text)
        return True
    except OSError as error:
        trouble(root, "the file %s could not be written" % _rel(root, path), error)
        return False


def _part(path) -> Path:
    """Where a file's new text waits while it is written: beside its place, under a short name of its own."""
    path = Path(path)
    return path.with_name("." + path.name.lstrip(".") + ".part")


def _stage(path, text) -> Path:
    """Write a file's new text beside its place, whole and safe on the disk, without touching the file itself."""
    part = _part(path)
    with open(part, "w", encoding="utf-8", errors="replace", newline="\n") as handle:
        handle.write(text)
        handle.flush()
        try:
            os.fsync(handle.fileno())
        except OSError:
            pass
    return part


def _put_in_place(part, path) -> None:
    """Move a staged file into its place in one step. Raises OSError if it cannot be done."""
    held = None
    for wait in (0.0, 0.02, 0.1):                  # on Windows something may be reading the old file this very instant
        time.sleep(wait)
        try:
            os.replace(part, path)
            return
        except PermissionError as error:
            held = error
    raise held


def _append(root, path, lines) -> bool:
    """Add lines to the end of a text file, first closing a last line some hand left open."""
    if not lines:
        return True
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        gap, head = "", b""
        try:
            with open(path, "rb") as handle:
                head = handle.read(2)
                handle.seek(0, os.SEEK_END)
                if handle.tell() > 0:
                    handle.seek(-1, os.SEEK_END)
                    gap = "" if handle.read(1) == b"\n" else "\n"
        except OSError:
            pass
        if head in (b"\xff\xfe", b"\xfe\xff"):               # a file saved as UTF-16 cannot take UTF-8 at its end:
            text = _read(path, 50_000_000)                    # it is written again whole, as the garden keeps text
            return _write(root, path, text + ("\n" if text and not text.endswith("\n") else "") + "\n".join(lines) + "\n")
        with open(path, "a", encoding="utf-8", errors="replace", newline="\n") as handle:
            handle.write(gap + "\n".join(lines) + "\n")
        return True
    except OSError as error:
        trouble(root, "the file %s could not be written" % _rel(root, path), error)
        return False


def _rel(root, path) -> str:
    """A path as the garden names it: from the root, with forward slashes."""
    try:
        return Path(path).resolve().relative_to(Path(root).resolve()).as_posix()
    except (ValueError, OSError):
        return Path(path).as_posix()


def _shown(root, path) -> str:
    """A path as it is printed for a visitor: from the root if they stand there, else in full."""
    try:
        if Path.cwd().resolve() == Path(root).resolve():
            return _rel(root, path)
        return Path(path).resolve().as_posix()
    except OSError:
        return _rel(root, path)


def _one_line(text, most=160) -> str:
    """Any text as one short line, with nothing in it that cannot be seen."""
    text = " ".join("".join(ch if ch.isprintable() else " " for ch in str(text)).split())
    return text if len(text) <= most else text[:most - 1].rstrip() + "…"


def _folders(path) -> list:
    """The folders inside a folder that the garden can see, in order. Never raises.

    A name with a leading dot is not seen. Nor is a folder that is really
    somewhere else (a symlink, a junction): the garden writes nothing
    outside its root, so it does not follow one out.
    """
    try:
        found = [entry for entry in Path(path).iterdir()
                 if not entry.name.startswith(".") and entry.is_dir() and not _leads_elsewhere(entry)]
    except OSError:
        return []
    return sorted(found, key=lambda entry: entry.name)


def _leads_elsewhere(entry) -> bool:
    """Is this folder a symlink or a junction?"""
    try:
        if entry.is_symlink():
            return True
        if hasattr(entry, "is_junction"):                      # Python 3.12 and later
            return entry.is_junction()
        return os.path.realpath(entry) != os.path.join(os.path.realpath(entry.parent), entry.name)
    except OSError:
        return True


# ---- troubles

said_troubles = []        # the plain sentences of this run, for the door to count
_logged = set()           # everything written to the log in this run, so nothing is written twice


def trouble(root, sentence, error=None, aloud=True) -> None:
    """Write a trouble down: the whole of it in ground/trouble.log, and one plain sentence kept for the door.

    A plant's own fault (an ailing kind) is not said aloud: the rings and
    the almanac already say it, once.
    """
    sentence = _one_line(sentence, 300)
    if sentence in _logged:
        return
    _logged.add(sentence)
    if aloud:
        said_troubles.append(sentence)
    if isinstance(error, BaseException):
        detail = "".join(traceback.format_exception(type(error), error, error.__traceback__))
    else:
        detail = str(error or "")
    try:
        log = Path(root) / "ground" / "trouble.log"
        log.parent.mkdir(parents=True, exist_ok=True)
        if log.is_file() and log.stat().st_size > 1_000_000:       # keep the newer part of a long log
            kept = _read(log, 10_000_000)[-300_000:]
            log.write_text(kept[kept.find("\n") + 1:], encoding="utf-8", newline="\n")
        try:
            stamp = now(root)                                       # the garden's clock: on a trial ground, not the real one
        except Exception:
            stamp = datetime.datetime.now()
        with open(log, "a", encoding="utf-8", errors="replace", newline="\n") as handle:
            handle.write("%s  %s\n" % (stamp.strftime("%Y-%m-%d %H:%M:%S"), sentence))
            for line in detail.rstrip().splitlines():
                handle.write("    %s\n" % line)
    except OSError:
        pass                                                        # even the log may fail; the day goes on


# ---- the clock

def today(root) -> datetime.date:
    """Today in the garden. The real date, always, in the real garden.

    Only a trial ground (one that holds a file ground/clock) keeps a
    calendar of its own: there GLEBE_TODAY is honoured if it is set, and
    else the clock's `ahead: N` days are added to the real date. A day
    lived is never unlived, so a variable some shell left lying about must
    never reach the real garden and live its days ahead of time.
    """
    if not _is_trial(root):
        return Date.today()
    given = _given_today()
    if given is not None:
        return given
    return Date.today() + _days(_ahead(root))


def _is_trial(root) -> bool:
    """Is this a trial ground? It is if it holds ground/clock (trial_ground.py lays one; the real garden has none)."""
    return (Path(root) / "ground" / "clock").is_file()


def _given_today():
    """The date in GLEBE_TODAY, strictly as 2026-10-04, or None. (Whether it counts is `today`'s to say.)"""
    found = re.fullmatch(r"\s*(\d{4})-(\d{2})-(\d{2})\s*", os.environ.get("GLEBE_TODAY", ""))
    try:
        return Date(int(found.group(1)), int(found.group(2)), int(found.group(3))) if found else None
    except ValueError:
        return None


def now(root) -> datetime.datetime:
    """The moment in the garden: the real time of day, on the garden's today."""
    return datetime.datetime.combine(today(root), datetime.datetime.now().time().replace(microsecond=0))


def _ahead(root, at=None) -> int:
    """How many days a trial ground's clock is wound forward (or was, at the real moment `at`).

    The real garden has no clock file, and is never ahead. On a trial
    ground, clock.py notes each winding (`wound: <when>  to <N>`), so that a
    file written before a winding can still be dated by the clock it was
    written under.
    """
    path = Path(root) / "ground" / "clock"
    if not path.is_file():
        return 0
    keys = hands.read_keys(_read(path, 100_000))
    ahead = int(hands.num(keys, "ahead", 0, -40_000, 40_000))
    windings = []
    for line in str(keys.get("wound", "")).splitlines():
        found = re.match(r"\s*(\S+)\s+to\s+(-?\d{1,6})", line)
        try:
            windings.append((datetime.datetime.fromisoformat(found.group(1)), int(found.group(2))))
        except (AttributeError, ValueError):
            continue
    if at is None or not windings:
        return ahead
    return max([(when, n) for when, n in windings if when <= at], default=(None, 0))[1]


def _days(n) -> datetime.timedelta:
    try:
        return datetime.timedelta(days=int(n))
    except (OverflowError, ValueError):
        return datetime.timedelta(0)


def _garden_time(root, stamp) -> datetime.datetime:
    """A file's real time (seconds since 1970) as the garden's clock showed it when the file was written."""
    try:
        real = datetime.datetime.fromtimestamp(stamp)
    except (OverflowError, OSError, ValueError):
        real = datetime.datetime.now()
    if not _is_trial(root):
        return real
    if _given_today() is not None:            # (GLEBE_TODAY moves every file's date along with the calendar)
        return real + (today(root) - Date.today())
    return real + _days(_ahead(root, real))


def _date_in(text):
    """The first ISO date in a text, or None."""
    found = _ISO.search(str(text))
    if not found:
        return None
    try:
        return Date(int(found.group(1)), int(found.group(2)), int(found.group(3)))
    except ValueError:
        return None


def _long_date(day) -> str:
    return "%s %d %s %d" % (WEEKDAYS[day.weekday()], day.day, MONTHS[day.month - 1], day.year)


def _short_date(day, seen_from) -> str:
    """'18 September', with the year when it is not the year we stand in."""
    text = "%d %s" % (day.day, MONTHS[day.month - 1])
    return text if day.year == seen_from.year else "%s %d" % (text, day.year)


def _from_to(first, last, seen_from) -> str:
    """'18 to 20 October', '30 December 2026 to 1 January': a stretch of days, saying no more than is needed."""
    if (first.year, first.month) == (last.year, last.month):
        return "%d to %s" % (first.day, _short_date(last, seen_from))
    if first.year == last.year:
        return "%d %s to %s" % (first.day, MONTHS[first.month - 1], _short_date(last, seen_from))
    return "%s to %s" % (_short_date(first, seen_from), _short_date(last, seen_from))


def _on_the(day, seen_from) -> str:
    """'on the 24th' within the month we stand in, else 'on 24 June'."""
    if (day.year, day.month) == (seen_from.year, seen_from.month):
        n = day.day
        ending = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return "on the %d%s" % (n, ending)
    return "on " + _short_date(day, seen_from)


def _count(n, one, many=None) -> str:
    """'1 plant', '3 plants'."""
    return "%d %s" % (n, one if n == 1 else (many or one + "s"))


def _and(names) -> str:
    """'a', 'a and b', 'a, b and c'."""
    names = [str(name) for name in names]
    return names[0] if len(names) == 1 else "%s and %s" % (", ".join(names[:-1]), names[-1]) if names else ""


NUMBER_WORDS = ("no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
                "twenty")


def _years(n) -> str:
    """'a year', 'two years', '21 years': a span of whole years in words."""
    return "a year" if n == 1 else "%s years" % (NUMBER_WORDS[n] if 0 <= n < len(NUMBER_WORDS) else n)


# ---- names

def clean_name(name) -> str:
    """A name made safe to sign with. No name at all is a name too; so is a name of marks alone ("...")."""
    text = "".join(ch for ch in str(name or "") if ch.isprintable() and ch not in "<>")
    text = " ".join(text.split()).lstrip("#").strip()[:60].strip()
    return text if text.strip(" .,:;\"\\'") else NO_NAME


def visitor_name(name) -> str:
    """What a visitor signs with. The garden's own names (OWN_NAMES) are reserved: whoever gives one of them
    signs `a visitor who gave the name ...`.

    Otherwise a layer by someone who arrived as "the days" would read as the
    garden's own growth, a plant they set by hand as one that came up by
    itself, and a visitor calling themselves "the keeper" could sign in
    the keeper's name. The keeper signs only through their own paths (see
    `_settle`), never at the gate.
    """
    name = clean_name(name)
    return CALLED % name if name.casefold() in {own.casefold() for own in OWN_NAMES} else name


def _slug(name) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(name).lower()).strip("-") or "someone"


def _folder_name(text, otherwise) -> str:
    """A name a folder can carry on any machine."""
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", str(text))
    name = re.sub(r"\s+", "-", name.strip())[:40].strip(" .-")
    if not name or name.split(".")[0].lower() in RESERVED:
        return otherwise
    return name


# ========================================================= beds and plants

@dataclass
class Bed:
    """One bed: a folder in beds/, and what its `bed` file says of it."""
    name: str
    path: Path
    keys: dict
    light: float
    water: float
    shelter: float
    room: int
    at: tuple | None              # (x, y, w, h) on the plan, or None until the ground gives it a place
    glass: bool = False           # its `bed` file says `glass: yes`: it lives by the calendar under the glass (see `Glass`)


@dataclass
class Plant:
    """One plant: a folder with a `seed` in it, read as it stands."""
    path: Path
    bed: Bed
    name: str
    where: str                    # "bed/plant"
    seed: dict
    tag: dict
    kind: str
    body: str
    dead: bool
    # beyond GROUND.md's list: things the ground needs often
    seed_text: str = ""
    tag_text: str = ""
    has_body: bool = True         # False: the seed has not sprouted yet
    unfit: str = ""               # why the days cannot work on this body, if they cannot
    overlong: bool = False        # unfit only for being over BODY_MOST: its kind is offered it once (see `_Passing._grow`)
    at: tuple = (0.5, 0.5)        # its place in the bed, both 0..1
    planted: datetime.date | None = None
    by: str = UNSEEN
    last_ring: str = ""           # what its last ring line says
    last_ring_day: datetime.date | None = None
    gone: bool = False            # carried to the heap while the days passed
    before: int = 0               # the days it lived on the other side of the glass before it came to this one (its tag's
                                  # `days before:`). Its age is these and the days since `planted`, the day it came here
    first: str = ""               # for a plant that has crossed the glass: when and where it was first planted (its tag's
                                  # `first planted:`, as "2026-10-03, outdoors")


def beds(root) -> list:
    """Every bed, in name order. Any folder in beds/ is a bed; one with no `bed` file has the usual values."""
    return [_bed(path) for path in _folders(Path(root) / "beds")]


def _bed(path) -> Bed:
    keys = hands.read_keys(_read(path / "bed", 100_000))
    return Bed(name=path.name, path=path, keys=keys,
               light=hands.num(keys, "light", 1.0, 0.0, 1.0),
               water=hands.num(keys, "water", 1.0, 0.0, 5.0),
               shelter=hands.num(keys, "shelter", 0.5, 0.0, 1.0),
               room=int(hands.num(keys, "room", 12, 0, 200)),
               at=_bed_place(keys), glass=sky._says_yes(hands.line(keys, "glass")))


def _bed_place(keys):
    """A bed's `at:` as (x, y, w, h) within the plan's 1000 x 700, or None if it has none that can be read."""
    numbers = re.findall(r"-?\d+(?:\.\d+)?", hands._signed(hands.line(keys, "at")))[:4]     # (a minus however typeset)
    if len(numbers) < 4:
        return None
    x, y, w, h = (float(n) for n in numbers)
    if w < 10 or h < 10:
        return None
    w, h = min(w, 1000.0), min(h, 700.0)
    return (min(max(x, 0.0), 1000.0 - w), min(max(y, 0.0), 700.0 - h), w, h)


def plants(root) -> list:
    """Every plant in every bed, sorted by "bed/plant". A folder is a plant if it holds a file named seed."""
    found = []
    for bed in beds(root):
        for path in _folders(bed.path):
            if (path / "seed").is_file():
                found.append(_plant(bed, path))
    return sorted(found, key=lambda plant: plant.where)


def _plant(bed, path) -> Plant:
    seed_text = _read(path / "seed", 100_000)
    tag_text = _read(path / "tag", 100_000)
    seed, tag = hands.read_keys(seed_text), hands.read_keys(tag_text)
    body_path = path / "body"
    unfit, body = "", ""
    if body_path.is_dir():
        unfit = "its body is a folder, not a file"
    elif body_path.is_file():
        body = _read(body_path)
        if len(body) > BODY_MOST:
            unfit = "its body is over %d characters" % BODY_MOST
    ring_day, ring = _last_ring(path)
    return Plant(path=path, bed=bed, name=path.name, where="%s/%s" % (bed.name, path.name),
                 seed=seed, tag=tag, kind=_kind_name(seed) or _kind_name(tag),
                 body=body, dead=hands.is_dead(body), seed_text=seed_text, tag_text=tag_text,
                 has_body=body_path.exists(), unfit=unfit, overlong=len(body) > BODY_MOST, at=_place_in_bed(tag, path.name),
                 planted=_date_in(hands.line(tag, "planted")), by=hands.line(tag, "by") or UNSEEN,
                 last_ring=ring, last_ring_day=ring_day, before=_days_before(tag), first=_first_planted(tag))


def _days_before(tag) -> int:
    """The days a plant lived on the other side of the glass, as its tag says (`days before:`); 0 if it never crossed."""
    return int(hands.num(tag, "days before", 0, 0, 400_000))


def _first_planted(tag) -> str:
    """When and where a plant that crossed the glass was first planted, as its tag says (`first planted:`); else ''."""
    return " ".join(hands.line(tag, "first planted").split())[:60]


def _kind_name(keys) -> str:
    """The kind a seed (or, failing that, a tag) names, if it is a name a file could have."""
    name = hands.word(keys, "kind", "")
    return name if re.fullmatch(r"[a-z0-9_][a-z0-9_\-]{0,40}", name) else ""


def _place_in_bed(tag, name) -> tuple:
    """A plant's `at:` as (x, y), both 0..1. A tag without one gets a steady place from the plant's name."""
    numbers = re.findall(r"-?\d*\.?\d+", hands._signed(hands.line(tag, "at")))[:2]
    if len(numbers) == 2:
        return tuple(min(1.0, max(0.0, float(n))) for n in numbers)
    digest = hashlib.sha1(name.encode("utf-8", errors="replace")).digest()
    return (0.1 + 0.8 * digest[0] / 255.0, 0.1 + 0.8 * digest[1] / 255.0)


def _last_ring(path):
    """The last line of a plant's rings, as (its day or None, what it says)."""
    try:
        with open(path / "rings", "rb") as handle:
            handle.seek(0, os.SEEK_END)
            handle.seek(max(0, handle.tell() - 2000))
            tail = handle.read().decode("utf-8", errors="replace")
    except OSError:
        return None, ""
    for line in reversed(tail.splitlines()):
        if line.strip():
            day = _date_in(line[:10])
            return day, (line[10:] if day else line).strip()
    return None, ""


# =================================================================== kinds

_kinds = {}               # (root, name) -> (the file's stamp, the module or None)
_stops = {}               # (root, name, where) -> how often a call had to be stopped in this run: a kind's call about
                          # the plant at `where`; with where '', the program itself (loading it, a creature's day)
_aside = {}               # (root, name) -> the kind was set aside and is asked nothing more; the value is what it
                          # did not come back from ("day", "draw", ...)
_plants_aside = {}        # (root, "bed/plant") -> (its kind, what it did not come back from): a plant that sleeps alone,
                          # its body more than its kind can read in time, while the kind goes on for every other plant
_stopped_on = {}          # (root, name) -> the plants whose calls were stopped when the kind was set aside, for the almanac
_told_aside = set()       # (root, name) of the kinds an earlier arrival set aside: the days do not tell of them again

try:
    import ctypes
    _interrupt = ctypes.pythonapi.PyThreadState_SetAsyncExc       # raises an exception inside another thread's Python
except Exception:
    _interrupt = None


class Overlong(BaseException):
    """Raised inside a kind that has not come back in time. Not an Exception, so a kind's own `except` lets it by."""


class Stopped(str):
    """The one-line error of a call that ran over its time. A sentence like any other, and a fact the ground can ask for."""


class Stumbled(str):
    """The one-line error of a call in which the kind itself raised: `ZeroDivisionError: division by zero`."""


def _in_words(error) -> str:
    """A kind's fault as the garden says it: a program's own error is wrapped, so that no line speaks as a program."""
    return "its kind stumbled (%s)" % error if isinstance(error, Stumbled) else str(error)


class _Sink:
    """Where a kind's print() goes: nowhere. The doors speak; kinds do not."""
    def write(self, text):
        return len(text)

    def flush(self):
        pass


_sink = _Sink()
_watch = {"lock": threading.Lock(), "until": None, "thread": None, "running": False}


def _watcher():
    """Runs beside the garden and interrupts a kind that is still going after its time."""
    while True:
        time.sleep(0.2)
        with _watch["lock"]:
            until = _watch["until"]
            if until is not None and time.monotonic() > until:
                _interrupt(ctypes.c_ulong(_watch["thread"]), ctypes.py_object(Overlong))
                _watch["until"] = time.monotonic() + 1.0          # and again, if the kind swallows it


def _arm(seconds):
    """Have the watcher interrupt this thread `seconds` from now. Returns (the moment an outer call was to be
    interrupted, or None; the moment set for this one). An inner call never outlives the call it lies in."""
    with _watch["lock"]:
        outer = _watch["until"]
        mine = time.monotonic() + seconds
        _watch["until"] = mine if outer is None else min(mine, outer)
        _watch["thread"] = threading.get_ident()
        if not _watch["running"] and _interrupt is not None:
            _watch["running"] = True
            threading.Thread(target=_watcher, name="glebe-watch", daemon=True).start()
    return outer, mine


def _disarm(outer=None):
    """Stop watching this call; watch the call it lies in again, if there is one.

    An outer call whose moment has already passed is given half a second
    more, never a moment in the past: an interruption must land in the
    outer call's own code, not in the middle of the inner call's return.
    """
    with _watch["lock"]:
        _watch["until"] = None if outer is None else max(outer, time.monotonic() + 0.5)


def _breathe():
    """A step or two of plain Python, so that an interruption already on its way lands here and not later."""
    for _ in (1, 2, 3):
        pass


def _call(seconds, function, *arguments):
    """Call into a kind, guarded. Returns (what it returned, None, None) or (None, the error in one line, in full).

    The kind cannot print and cannot stop the garden by raising, whatever
    it raises; only a visitor's own Ctrl-C passes. If it is still running
    Python after its time, the watcher interrupts it. Where the watcher
    cannot reach (inside C code, or asleep) the call is timed when it does
    come back, and what came back late is not kept. Either way the error is
    a Stopped.

    Calls may lie one inside another: a creature, in its day, asks a kind
    how many flowers a plant has open. The inner call then has its own
    time, but never more than the outer call has left; and if it is the
    outer call's time that runs out, the interruption is passed on to the
    outer call, which is the one that ran over (see `_arm`).

    What this cannot do is bring back a call that never returns, or
    survive a kind that ends the process. For that the doors run the kinds
    apart (see `_apart`, further down).
    """
    out, err = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = _sink
    began = time.monotonic()
    outer, mine = None, float("inf")
    try:
        try:
            outer, mine = _arm(seconds)
            try:
                result = function(*arguments)
            finally:
                _disarm(outer)
            _breathe()
        except Overlong:
            if outer is not None and outer <= mine:              # the caller's time is up, not this call's: it is
                raise                                            # the caller who is stopped
            return None, Stopped("took longer than %g s and was stopped" % seconds), ""
        except KeyboardInterrupt:
            raise
        except BaseException as error:
            said = "%s: %s" % (type(error).__name__, error) if str(error) else type(error).__name__
            return None, Stumbled(_one_line(said)), "".join(
                traceback.format_exception(type(error), error, error.__traceback__))
        if time.monotonic() - began > seconds:
            return None, Stopped("took longer than %g s" % seconds), ""
        return result, None, None
    finally:
        _disarm(outer)
        sys.stdout, sys.stderr = out, err


def _ask(root, name, what, where, function, *arguments):
    """Ask the kind `name` one thing about the plant at `where`. `what` is load, sprout, day, cast, describe or draw.

    This is _call with its book-keeping. While the kind is being asked, the
    crumb says so (see `_Crumb`): a door watching from outside then knows
    whom to blame if no answer ever comes. A call that has to be stopped is
    counted (see `_count_stop`): against the plant it was about, so that one
    plant whose body is too much for its kind sleeps alone and the kind
    goes on for the others; and against the kind once two of its plants
    have been stopped, when it is set aside for the rest of the run and
    asked nothing more. So a kind that loops costs a door a few seconds,
    not a few seconds for each of its plants.

    A plant whose call was stopped and a plant that was not asked because
    its kind is set aside are told the same thing (`_late`): so a fault
    that stands is one line in a plant's rings, whichever of the two it
    was on a given day.
    """
    key = (str(root), name)
    if key in _aside:
        return None, Stopped(_late(_aside[key], _whose(name))), ""
    alone = _plants_aside.get((str(root), where)) if where else None
    if alone and alone[0] == name and _same_sort(alone[1], what):
        return None, Stopped(_too_much(alone[1])), ""
    before = tuple(_crumb_now)                     # a call inside another (a kind asked by a creature) gives the crumb back
    _say_crumb(what, name, where)
    try:
        result, error, full = _call(KIND_SECONDS[what], function, *arguments)
    finally:
        _say_crumb(*before)
    if isinstance(error, Stopped):
        error = Stopped(_too_much(what) if _count_stop(root, name, what, where) else _late(what, _whose(name)))
    return result, error, full


def _count_stop(root, name, what, where, weight=None) -> bool:
    """Count one call that had to be stopped. True if, by it, the plant at `where` now sleeps alone.

    Loading a kind's file, and anything asked of a creature, is the
    program's own: STOPS_MOST stops (loading, one) and it is set aside.
    A kind's call about a plant is counted against that plant. A plant
    stopped STOPS_MOST times (a drawing, which has the longest time of
    all: once) sleeps alone for the rest of the run, its body more than
    its kind can read in time (TOO_MUCH), and the kind goes on with its
    other plants. Only when calls about two different plants have been
    stopped is the kind itself taken to be at fault: then it is set aside,
    and the plants it was stopped on are kept for the almanac's line.

    `weight` is how many stops this one counts for (a hand the door had to
    end, inside a kind, counts in full).
    """
    root = str(root)
    weight = weight if weight is not None else STOPS_MOST if what in ("draw", "load") else 1
    if what == "load" or not where or str(name).startswith(CREATURE):
        mine = (root, name, "")
        _stops[mine] = _stops.get(mine, 0) + weight
        if _stops[mine] >= STOPS_MOST:
            _aside[(root, name)] = what
        return False
    mine = (root, name, where)
    _stops[mine] = _stops.get(mine, 0) + weight
    stopped = sorted(w for (r, n, w) in _stops if r == root and n == name and w)
    if len(stopped) >= 2:
        _aside[(root, name)] = what
        _stopped_on[(root, name)] = stopped
        return False
    if _stops[mine] >= STOPS_MOST:
        _plants_aside[(root, where)] = (name, what)
        return True
    return False


def _same_sort(what, other) -> bool:
    """Are two calls of one sort? The days' (sprout, day, cast, and what creatures ask), or a door's (draw, describe, size).

    A plant that sleeps alone for the one sort is still asked the other:
    a drawing too slow to make does not stop a plant growing.
    """
    return (what in LASTING) == (other in LASTING)


def _too_much(what) -> str:
    """What is said of a plant that sleeps alone, by what it did not come back from (see `_count_stop`)."""
    if what == "sprout":
        return TOO_MUCH % ("seed", "bring up")
    return TOO_MUCH % ("body", "draw" if what == "draw" else "read")


def _forget_stops(root, name) -> None:
    """A kind's or a creature's file has changed: what was held against the old one is forgotten, and its plants wake."""
    root = str(root)
    for mine in [mine for mine in _stops if mine[0] == root and mine[1] == name]:
        del _stops[mine]
    for plant in [plant for plant, (kind_name, _) in _plants_aside.items() if plant[0] == root and kind_name == name]:
        del _plants_aside[plant]
    _aside.pop((root, name), None)
    _stopped_on.pop((root, name), None)


WHAT_WORDS = {"live": "day", "bitten": "answer to a bite", "flowers": "count of its flowers"}   # a call, as it is said


def _late(what, whose="its kind's") -> str:
    """What is said of a plant whose kind did not come back in time from `what` (day, draw, ... or the loading of its file)."""
    if what == "load":
        return "%s file did not finish loading in %g s" % (whose, KIND_SECONDS["load"])
    return "%s %s did not come back in %g s" % (whose, WHAT_WORDS.get(what, what), KIND_SECONDS.get(what, 0))


def _whose(name) -> str:
    """How a program's own is said: a kind's day is 'its kind's day' (said of a plant); a creature's is 'its day'."""
    return "its" if str(name).startswith(CREATURE) else "its kind's"


def _program_words(name) -> str:
    """'the kind bough', 'the creature bees': a kind or a creature, named as the troubles and the notes name it."""
    name = str(name)
    return "the creature %s" % name[len(CREATURE):] if name.startswith(CREATURE) else "the kind %s" % name


# ---- what a visit has already met

_said_before = set()      # troubles an earlier door of this visit said aloud; they are not said again


def _visit_file(root) -> Path:
    return Path(root) / "ground" / ".visit"


def _kind_stamp(root, name) -> str:
    """A kind's file (or a creature's: creatures/<name>) as it stands, when written and how long, in a few characters.
    '' if there is no such file."""
    try:
        status = _program_path(root, name).stat()
        return "%d-%d" % (status.st_mtime_ns, status.st_size)
    except OSError:
        return ""


def _program_path(root, name) -> Path:
    """Where a kind's file lies (species/<name>.py), or a creature's (creatures/<name>.py, for creatures/<name>)."""
    name = str(name)
    if name.startswith(CREATURE):
        return Path(root) / "creatures" / (name[len(CREATURE):] + ".py")
    return Path(root) / "species" / (name + ".py")


PLANT_MARK = "beds/"      # how a plant that sleeps alone is named where kinds are named (ground/aside, ground/.visit)


def _plant_stamp(root, where) -> str:
    """A plant as it stands, for remembering that it sleeps alone: its body, its seed and its kind's file, in a few
    characters. A hand that cuts the body, or a kind that is mended, wakes it."""
    folder = Path(root) / "beds" / where
    digest = hashlib.sha1()
    for name in ("body", "seed"):
        try:
            digest.update((folder / name).read_bytes())
        except OSError:
            digest.update(b"-")
        digest.update(b"\0")
    digest.update(_kind_stamp(root, _kind_name(hands.read_keys(_read(folder / "seed", 100_000)))).encode())
    return digest.hexdigest()[:16]


def _stamp(root, name) -> str:
    """The stamp of whatever ground/aside or ground/.visit names: a kind, a creature, or a plant (beds/<bed>/<plant>)."""
    name = str(name)
    if name.startswith(PLANT_MARK):
        return _plant_stamp(root, name[len(PLANT_MARK):])
    return _kind_stamp(root, name)


def _sleeps_alone(root, where, what) -> None:
    """Take up a plant that an earlier door found sleeping alone (its line in ground/aside or ground/.visit)."""
    kind_name = _kind_name(hands.read_keys(_read(Path(root) / "beds" / where / "seed", 100_000)))
    if kind_name:
        _plants_aside[(str(root), where)] = (kind_name, what)


def _whose_visit(root) -> str:
    """The visit now going on, as one line (who, and since when); '' if no one is in the garden."""
    latch = _latch(root)
    if not _is_live(latch, now(root)):
        return ""
    return "%s since %s %s" % (latch["name"], latch["since"].isoformat(), latch["visit"])


def _recall_visit(root) -> None:
    """Take up what the earlier doors of this visit left in ground/.visit.

    Two things. The kinds they set aside stay aside, as long as their
    files have not changed: a kind whose drawing loops costs a visit its
    eight seconds once, not at every look. And a trouble they said aloud
    is not said again: one broken kind is one sentence in a visit, not one
    at every door. It is one visit's memory only: the next arrival says
    every trouble anew, and someone who walks in without arriving is told
    everything. (A kind whose days did not come back is remembered longer,
    in ground/aside: see `_recall_aside`.)
    """
    lines = _read(_visit_file(root), 1_000_000).splitlines()
    whose = _whose_visit(root)
    if not whose or lines[:1] != ["visit|" + whose]:
        return
    for line in lines[1:]:
        sort, _, rest = line.partition("|")
        if sort == "said":
            _said_before.add(rest)
        elif sort in ("aside", "alone"):
            name, what, stamp = (rest.split("|") + ["", ""])[:3]
            if what in KIND_SECONDS and stamp and stamp == _stamp(root, name):
                if sort == "aside":
                    _aside[(str(root), name)] = what
                elif name.startswith(PLANT_MARK):
                    _sleeps_alone(root, name[len(PLANT_MARK):], what)


def _remember_visit(root) -> None:
    """Leave in ground/.visit what this door met, for the doors that follow in the same visit."""
    lines = ["aside|%s|%s|%s" % (name, what, _kind_stamp(root, name))
             for (where, name), what in sorted(_aside.items()) if where == str(root)]
    lines += ["alone|%s%s|%s|%s" % (PLANT_MARK, plant, what, _plant_stamp(root, plant))
              for (where, plant), (_, what) in sorted(_plants_aside.items()) if where == str(root)]
    lines += ["said|%s" % sentence for sentence in sorted(_said_before | set(said_troubles))]
    whose = _whose_visit(root)
    if lines and whose:
        _write(root, _visit_file(root), "\n".join(["visit|" + whose] + lines) + "\n")
    else:
        _remove(_visit_file(root))


# ---- what the ground remembers of a kind from one arrival to the next

LASTING = ("load", "sprout", "day", "cast", "flowers", "bitten", "live", "after")
                          # what a kind or a creature did not come back from, when ground/aside remembers it
ASIDE_HEAD = [
    "# Kinds set aside: each was asked to load, to sprout, for its day or for its seed, and did not come back in time.",
    "# While a kind's line stands here it is asked nothing, and its plants wait as they are. It is asked again when",
    "# its file in species/ changes, or %d days on, or as soon as a hand takes its line out of here." % ASIDE_DAYS,
    "# Each line: the day the kind was set aside, its name, what it did not come back from, and its file as it stood.",
    "# A creature is named creatures/<name>; while it stands here it sleeps, and the days go on without it.",
    "# A plant is named beds/<bed>/<plant>: its own body was more than its kind could read in time, and it sleeps alone",
    "# while the rest of its kind grows. It wakes when its body or its seed is changed (cut it back), or its kind is.",
]


def _aside_file(root) -> Path:
    return Path(root) / "ground" / "aside"


def _kept_aside(root, day) -> dict:
    """ground/aside, read: {kind: (the day it was set aside, what it did not come back from)}, for the lines that still hold.

    A line holds while the kind's file stands exactly as it did (the same
    stamp) and fewer than ASIDE_DAYS days have gone by. So a kind that was
    mended is asked again at once, and one set aside by some accident of
    the machine (a lid closed in the middle of an arrival) is not left
    aside for good.
    """
    kept = {}
    for line in _read(_aside_file(root), 200_000).splitlines():
        fields = line.split()
        when = _date_in(fields[0]) if len(fields) == 4 else None
        if when is None:
            continue
        name, what, stamp = fields[1:]
        if what in LASTING and stamp == _stamp(root, name) and 0 <= (day - when).days < ASIDE_DAYS:
            kept[name] = (when, what)
    return kept


def _recall_aside(root) -> None:
    """Take up the kinds (and the plants sleeping alone) that ground/aside holds: they stay aside at this door too,
    and cost it no waiting.

    Without this an arrival would wait out every kind that loops or hangs
    all over again, each time, and with a handful of them no day would
    ever be lived.
    """
    for name, (_, what) in _kept_aside(root, today(root)).items():
        if name.startswith(PLANT_MARK):
            _sleeps_alone(root, name[len(PLANT_MARK):], what)
            continue
        _aside[(str(root), name)] = what
        _told_aside.add((str(root), name))


def _remember_aside(root) -> None:
    """Write ground/aside as it stands after this door: the lines that still hold, and what this door set aside."""
    day = today(root)
    kept = _kept_aside(root, day)
    for (where, name), what in sorted(_aside.items()):
        if where == str(root) and what in LASTING and name not in kept and _kind_stamp(root, name):
            kept[name] = (day, what)
    for (where, plant), (_, what) in sorted(_plants_aside.items()):
        if where == str(root) and what in LASTING and PLANT_MARK + plant not in kept and " " not in plant:
            kept[PLANT_MARK + plant] = (day, what)          # (a name with a space in it cannot be one field of a line)
    path = _aside_file(root)
    lines = ["%s  %s  %s  %s" % (when.isoformat(), name, what, _stamp(root, name))
             for name, (when, what) in sorted(kept.items())]
    text = "".join(line + "\n" for line in ASIDE_HEAD + lines)
    if not lines:
        _remove(path)
    elif _read(path, 200_000) != text:
        _write(root, path, text)


_load_faults = {}         # (root, name) -> why the kind's file could not be run, in one line


def kind(root, name):
    """The loaded species module for a kind, or None if it cannot be had. Cached; reloaded when its file changes."""
    name = str(name or "")
    if not re.fullmatch(r"[a-z0-9_][a-z0-9_\-]{0,40}", name):
        return None
    path = Path(root) / "species" / (name + ".py")
    try:
        status = path.stat()
        stamp = (status.st_mtime_ns, status.st_size)
    except OSError:
        stamp = None
    key = (str(root), name)
    known = _kinds.get(key)
    if known is not None and known[0] == stamp:
        return known[1]
    if known is not None:                          # the file has changed: what was held against the old one is forgotten
        _forget_stops(root, name)
    if key in _aside:                              # set aside before it was ever loaded here: loading may be what hung
        return None
    module = _load_kind(root, name, path) if stamp is not None else None
    _kinds[key] = (stamp, module)
    return module


def _load_kind(root, name, path):
    """Read and run one kind's file. A file that cannot be run is a trouble, not a stop."""
    return _load_program(root, name, path, "glebe_kind_" + name.replace("-", "_"),
                         "a kind needs a function day(body, seed, ctx)")


def _load_program(root, key, path, module_name, needs):
    """Read and run one program's file: a kind's, or a creature's (`key` creatures/<name>). None if it cannot be run.

    What it imports as `hands` is a copy of its own, so that nothing it
    does to `hands` reaches any other program. A file that cannot be run
    is written down as a trouble, and is not a stop.
    """
    module = types.ModuleType("%s_%s" % (module_name, hashlib.sha1(str(root).encode()).hexdigest()[:8]))
    module.__file__ = str(path)

    def run():
        code = compile(_read(path, 5_000_000), str(path), "exec", dont_inherit=True)
        sys.modules[module.__name__] = module
        shared = sys.modules.get("hands")
        sys.modules["hands"] = _own_copy("hands")
        try:
            exec(code, module.__dict__)
        finally:
            if shared is None:
                sys.modules.pop("hands", None)
            else:
                sys.modules["hands"] = shared
        if not callable(getattr(module, "day", None)):
            raise TypeError(needs)

    _, error, full = _ask(root, key, "load", "", run)
    _load_faults.pop((str(root), key), None)
    if error is not None:
        sys.modules.pop(module.__name__, None)
        error = _late("load", "its") if isinstance(error, Stopped) else str(error)
        _load_faults[(str(root), key)] = error
        trouble(root, "%s could not be loaded: %s" % (_program_words(key), error), full)
        return None
    return module


def _no_kind(root, name) -> str:
    """Why nothing can be asked of a plant's kind just now, in a few words; '' if it can be asked."""
    if (str(root), name) in _aside:
        return _late(_aside[(str(root), name)])
    if kind(root, name) is None:
        return "kind not understood (%s)" % (name or "the seed names none")
    return ""


def kinds_there(root) -> list:
    """The names of the kinds that stand in species/, in order."""
    try:
        return sorted(path.stem for path in (Path(root) / "species").glob("*.py")
                      if re.fullmatch(r"[a-z0-9_][a-z0-9_\-]{0,40}", path.stem))
    except OSError:
        return []


def _kind_file_mark(root, name) -> str:
    """A kind's file as a short hash, for telling whether a plate is stale."""
    try:
        return hashlib.sha1((Path(root) / "species" / (name + ".py")).read_bytes()).hexdigest()
    except OSError:
        return "no such kind"


# ===================================================== what a kind is told

class Neighbour:
    """Another living plant in the same bed, as a kind sees it: .name .where ("bed/plant") .kind .seed .body .distance."""
    __slots__ = ("name", "where", "kind", "seed", "body", "distance")

    def __init__(self, other, viewer):
        self.name = other.name
        self.where = other.where
        self.kind = other.kind
        self.seed = dict(other.seed)
        self.body = other.body
        self.distance = math.hypot(other.at[0] - viewer.at[0], other.at[1] - viewer.at[1])


class Soil:
    """The heap, the book and the gate as text: what a kind may feed on. Read only when asked for."""

    _files = {}           # path -> (stamp, text): kept between days, since the soil changes slowly

    def __init__(self, root):
        self.root = Path(root)
        self._texts = self._lines = self._words = None

    def turn(self):
        """The soil has changed (something rotted, something was carried to the heap): read it afresh next time."""
        self._texts = self._lines = self._words = None

    def texts(self) -> list:
        """[(where, text)] for every text file under compost/, book/ and gate/."""
        if self._texts is None:
            self._texts = []
            for top in ("compost", "book", "gate"):
                for path in _files_under(self.root / top, 600):
                    text = self._text_of(path)
                    if text:
                        self._texts.append((_rel(self.root, path), text))
        return list(self._texts)

    def lines(self) -> list:
        """Their lines that are not empty."""
        if self._lines is None:
            self._lines = [line.strip() for _, text in self.texts() for line in text.splitlines() if line.strip()]
        return list(self._lines)                   # a copy each time: what one kind does to it, no other sees

    def words(self) -> list:
        """Their words, lower-cased."""
        if self._words is None:
            self._words = [word for _, text in self.texts()
                           for word in re.findall(r"[^\W\d_]+(?:['’\-][^\W\d_]+)*", text.lower())]
        return list(self._words)

    def _text_of(self, path) -> str:
        try:
            status = path.stat()
        except OSError:
            return ""
        stamp = (status.st_mtime_ns, status.st_size)
        known = Soil._files.get(str(path))
        if known is None or known[0] != stamp:
            if len(Soil._files) > 5000:
                Soil._files.clear()
            known = Soil._files[str(path)] = (stamp, _read(path, SOIL_FILE_MOST) if _is_text(path) else "")
        return known[1]


def _files_under(top, most) -> list:
    """The visible files under a folder, deepest last, in order. Never raises."""
    found = []
    for folder, names, files in os.walk(top, onerror=lambda error: None):
        names[:] = sorted(name for name in names if not name.startswith("."))
        for name in sorted(files):
            if not name.startswith("."):
                found.append(Path(folder) / name)
                if len(found) >= most:
                    return found
    return found


def _is_text(path) -> bool:
    """Text is what has no zero byte in its first few thousand (or says it is UTF-16)."""
    try:
        with open(path, "rb") as handle:
            start = handle.read(8192)
    except OSError:
        return False
    return start[:2] in (b"\xff\xfe", b"\xfe\xff") or b"\0" not in start


class Ctx:
    """What a kind is told about one plant on one day. GROUND.md lists each name.

    Two came with the creatures. `bed['rich']` is how rich the bed's ground
    is that day, 0..1, as a number: what the creatures left there (see
    `enrich`), fading over a season, added to any `rich:` line a hand wrote
    in the bed file. `pollen` is pollen carried to this plant: each grain
    has `.seed` (the giver's seed), `.where` (its bed/plant), `.kind`, `.by`
    (who carried it) and `.body` (the giver's body). In `cast` it is what
    the creatures carried today; in `day` it is what they carried the day
    before, so that a kind can mark in its body a flower that took pollen,
    and cross the seed of that flower when it falls, weeks on. A cross
    comes from a grain that was really carried. Elsewhere it is empty.

    When a creature asks a kind how many flowers are open (`flowers`),
    `part` says when that creature is about: 'day', 'dusk' or 'night' (the
    creature's ABOUT; 'day' if it says nothing). A flower that opens at
    dusk for the moths may be shut to the bees. Elsewhere `part` is ''.
    """

    def __init__(self, plant, date, local_sky, purpose, weather_seed, soil, others, left=None, hour=None, rich=0.0):
        self.date = date
        self.sky = local_sky
        self.age = (max(0, (date - plant.planted).days) if plant.planted else 0) + getattr(plant, "before", 0)
        self.seed = dict(plant.seed)
        self.tag = dict(plant.tag)
        self.bed = dict(plant.bed.keys)
        self.bed["rich"] = round(min(1.0, hands.num(plant.bed.keys, "rich", 0.0, 0.0, 1.0) + max(0.0, rich)), 3)
        self.pollen = []
        self.part = ""
        self.name = plant.name
        self.where = plant.where
        self.left = left
        self.hour = hour
        self.soil = soil
        self._plant = plant
        self._others = others
        self._neighbours = None
        self._rng = None
        self._rng_seed = "%s|%s|%s|%s" % (weather_seed, plant.where, date.isoformat(), purpose)

    @property
    def rng(self) -> random.Random:
        """Dice that fall the same way for the same garden, plant, day and purpose."""
        if self._rng is None:
            self._rng = random.Random(self._rng_seed)
        return self._rng

    @property
    def neighbours(self) -> list:
        """The other living plants of the bed, each with its .distance from this one."""
        if self._neighbours is None:
            self._neighbours = [Neighbour(other, self._plant) for other in self._others()
                                if other is not self._plant]
        return self._neighbours


def _living_in(garden, bed_name, day) -> list:
    """The plants of one bed that are alive, up, and in the ground on that day."""
    return [p for p in garden if p.bed.name == bed_name and not p.dead and not p.gone and p.has_body
            and (p.planted is None or p.planted <= day)]


# ==================================================================== inks

def ink_of(root, name) -> str:
    """The ink a hand signs in. A hand with none yet takes the next unused one, and ground/inks remembers it."""
    name = " ".join(str(name or UNSEEN).split()) or UNSEEN
    path = Path(root) / "ground" / "inks"
    known = _inks(path)
    key = _ink_key(name)
    if key in known:
        return known[key]
    if name in FIXED_INKS:
        ink = FIXED_INKS[name]
    else:
        ink = next((ink for ink in HAND_INKS if ink not in known.values()), None) or _an_ink_for(name)
    if not path.is_file():
        _write(root, path, "# Which ink belongs to which hand. The ground adds a line when a new hand signs.\n")
    _append(root, path, ["%s: %s" % (key, ink)])
    return ink


_inks_read = {}           # path -> (the file's stamp, its inks): drawing asks for an ink at every plant


def _inks(path) -> dict:
    """ground/inks as {name: '#rrggbb'}, keeping only lines that hold a colour."""
    try:
        status = os.stat(path)
        stamp = (status.st_mtime_ns, status.st_size)
    except OSError:
        return {}
    kept = _inks_read.get(str(path))
    if kept is not None and kept[0] == stamp:
        return kept[1]
    known = {}
    for key, value in hands.read_keys(_read(path, 200_000)).items():
        found = re.findall(r"#[0-9a-fA-F]{6}\b", value)
        if key and found:
            known[key] = found[-1].lower()
    _inks_read[str(path)] = (stamp, known)
    return known


def _ink_key(name) -> str:
    return name.lower().replace(":", "-").lstrip("#").strip() or UNSEEN


def _an_ink_for(name) -> str:
    """When the ten inks are all taken: a dark ink of the name's own, anywhere on the wheel but green."""
    digest = hashlib.sha1(name.encode("utf-8", errors="replace")).digest()
    hue = (170.0 + 260.0 * digest[0] / 255.0) % 360.0            # 170°..430°: blue, violet, red, orange
    lightness, saturation = 0.30 + 0.08 * digest[1] / 255.0, 0.65
    chroma = (1 - abs(2 * lightness - 1)) * saturation
    x = chroma * (1 - abs((hue / 60.0) % 2 - 1))
    r, g, b = [(chroma, x, 0), (x, chroma, 0), (0, chroma, x), (0, x, chroma), (x, 0, chroma), (chroma, 0, x)][int(hue // 60) % 6]
    m = lightness - chroma / 2
    return "#%02x%02x%02x" % tuple(int(round(255 * (v + m))) for v in (r, g, b))


# ================================================================= tending

def tend(root, by=None) -> list:
    """Sprout any seed that has no body, write any missing tag, give new beds a place, notice the heap.

    Every door does this first. What it does is signed by `by`, else by
    whoever is in the garden, else by the keeper (in their border) or an
    unseen hand. Returns what it did, in plain words.
    """
    return _tend(root, by)[0]


def _tend(root, by=None) -> tuple:
    """Tending, for the doors: (what was done, in plain words; the plants that came up just now)."""
    root = Path(root)
    did, up = [], []
    _packets_taken.pop(str(root), None)            # (asked afresh in each tending: see `_origin`)
    _make_folders(root)
    for name in FIXED_INKS:
        ink_of(root, name)
    moment = now(root)
    day = moment.date()
    did += _place_beds(root)
    latch = _latch(root)
    lived = []

    def last_lived():                              # asked for only when something new has to be dated
        if not lived:
            lived.append(_last_lived(root, day) or _eve_of_laying(root, day))
        return lived[0]

    garden = plants(root)
    under = _begin_glass(root, day)                # the calendar under the glass, if a bed lies under it
    for plant in garden:
        its_day = _day_of(plant.bed, day, under)   # under the glass, the day the glass stands at
        glassy = under is not None and plant.bed.glass
        did.append(_cross_glass(root, plant, day, under))
        if not plant.has_body:
            did.append(_sprout(root, plant, garden, _signer(root, plant, by, latch, moment), its_day,
                               its_day if glassy else last_lived()))
            if plant.has_body:
                up.append(plant.where)
        elif not (plant.path / "tag").is_file():
            said, whole = _tag_anew(root, plant, garden, _signer(root, plant, by, latch, moment), its_day,
                                    (lambda its_day=its_day: its_day) if glassy else last_lived)
            did.append(said)
            if whole:
                up.append(plant.where)
        else:
            did.append(_mend_tag_name(root, plant, its_day))
    _note_heap(root, last_lived, day)
    return [line for line in did if line], up


def _eve_of_laying(root, day):
    """The day before the ground was laid (or `day`, if that is earlier): the last lived day of a garden that has lived none.

    A seed that lay in a bed before anyone came is then sown on the day
    it was written, and lives the garden's opening days with the rest.
    """
    laid = sky.place(root).get("laid")
    try:
        return min(day, laid - ONE_DAY)
    except (TypeError, OverflowError):
        return day


def _signer(root, plant, by, latch, moment) -> str:
    """Who is taken to have planted a seed that is found without a body or a tag.

    Whoever the door says (`by`). Else the visitor on the latch, if the
    seed came to lie there while that visit was going on: a latch someone
    forgot days ago signs nothing planted since, and a visit signs nothing
    planted before it began. Else the keeper (in their border), or an unseen
    hand.

    A seed has lain there since it was written, or since its plant's
    folder last took something in, whichever came later (see
    `_planted_lain`): a packet moved out of the seedbox keeps the time it
    was written, long ago, but the folder it was moved into is new, or
    newly changed, and says when the planting was.
    """
    if by:
        return by
    if latch:
        lain = _planted_lain(root, plant.path) or moment
        if _is_live(latch, lain) and lain >= latch["since"].replace(second=0, microsecond=0):
            return latch["name"]
    return THE_KEEPER if plant.bed.name == KEEPERS_BED else UNSEEN


def _planted_lain(root, folder, own_writes=False):
    """Since when a seed has lain in its plant's folder: the later of its own time and the folder's (see `_lain`).

    Moving a file keeps its times, so a packet moved out of the seedbox
    seems to have lain in the bed since it was written; the folder it went
    into is new, or was changed by the move, and says when it came. Only
    seeds that have not come up are asked this, so the ground has written
    nothing in their folders yet. With `own_writes`, the ground may have
    (tending writes a new plant's body, tag and rings): then only the time
    the folder was made is asked, where the system keeps one.
    """
    seed = _lain(root, Path(folder) / "seed")
    if own_writes:
        try:
            made = getattr(Path(folder).stat(), "st_birthtime", None)
        except OSError:
            made = None
        there = _garden_time(root, made) if made is not None else None
    else:
        there = _lain(root, folder)
    found = [moment for moment in (seed, there) if moment is not None]
    return max(found) if found else None


def _lain(root, path):
    """The moment, on the garden's clock, since which a file has lain where it is: when it was written, or made there
    if that was later. None if the file cannot be asked."""
    try:
        status = Path(path).stat()
    except OSError:
        return None
    return _garden_time(root, max(status.st_mtime, getattr(status, "st_birthtime", status.st_ctime)))


def _make_folders(root):
    """The garden's top folders, made if they are missing. A file standing where one should be is left alone."""
    for name in FOLDERS:
        path = Path(root) / name
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
            except OSError as error:
                trouble(root, "the folder %s/ could not be made" % name, error)


def _place_beds(root) -> list:
    """Give every bed that has no `at:` a free place on the plan, and write the line back into its bed file."""
    did = []
    every = beds(root)
    taken = [bed.at for bed in every if bed.at] + [spot for _, spot in _fixtures()]
    for bed in every:
        if bed.at is None:
            bed.at = _free_place(taken, bed.name)
            taken.append(bed.at)
            if _append(root, bed.path / "bed", ["at: %d,%d,%d,%d" % bed.at]):
                did.append("gave the bed %s a place on the plan" % bed.name)
    return did


def _fixtures():
    """The shed and the heap on the plan, in plan units (x, y, w, h). The gate is at the bottom centre."""
    return (("shed", (60.0, 630.0, 70.0, 55.0)), ("heap", (870.0, 630.0, 70.0, 55.0)))


def _free_place(taken, name) -> tuple:
    """A place on the plan that overlaps no bed: the largest of a few sizes that fits, searched row by row.

    Every bed is lettered with its name just above its outline, so each is
    given a strip of that height as well.
    """
    name_strip = 18

    def clear(x, y, w, h, gap):
        y, h = y - name_strip, h + name_strip
        return all(x + w + gap <= tx or tx + tw + gap <= x or y + h + gap <= ty - name_strip or ty + th + gap <= y
                   for tx, ty, tw, th in taken)

    # Wide beds first, in the open ground; then narrow ones, which fit along the garden's east and west edges.
    for w, h, gap in ((200, 100, 20), (150, 80, 15), (130, 55, 10), (90, 40, 8), (48, 90, 5), (44, 44, 4)):
        for y in range(name_strip + 4, 700 - 4 - h + 1, 6):
            for x in range(4, 1000 - 4 - w + 1, 6):
                if clear(x, y, w, h, gap):
                    return (x, y, w, h)
    digest = hashlib.sha1(name.encode("utf-8", errors="replace")).digest()      # the plan is full: it lies over others
    return (60 + digest[0] * 3, 40 + digest[1] * 2, 90, 40)


def _sprout(root, plant, garden, signer, day, earliest) -> str:
    """Bring up a seed a hand has planted: its body from the kind's sprout, and its tag.

    Returns what to say of it: that it came up, or why it is still a seed.
    The why is said once, when it is first written in the plant's rings; a
    seed that stays a seed is one line, not one at every door.
    """
    sown = _sown_day(root, plant, day, earliest)
    tagged = (plant.path / "tag").is_file()
    if not tagged:
        others = [p.at for p in garden if p.bed.name == plant.bed.name and p is not plant and p.has_body]
        dice = random.Random("%s|%s|place" % (sky.place(root).get("weather-seed"), plant.where))
        plant.at = _rounded(_open_place(others, dice))
        _write_tag(root, plant, sown, signer, _origin(root, plant))
    why, full = _why_no_kind(root, plant), ""
    body = ""
    if not why and callable(getattr(kind(root, plant.kind), "sprout", None)):
        ctx = Ctx(plant, sown, sky.local(_sky_on(root, plant.bed, sown), plant.bed), "sprout",
                  sky.place(root).get("weather-seed"), Soil(root), lambda: _living_in(garden, plant.bed.name, sown),
                  rich=_rich_on(_read_rich(root), plant.bed.name, sown))
        body, error, full = _ask(root, plant.kind, "sprout", plant.where, kind(root, plant.kind).sprout, dict(plant.seed), ctx)
        if error is None and not isinstance(body, str):
            error = "its kind's sprout gave back no text"
        if error is None and len(body) > BODY_MOST:
            error = "its kind's sprout gave back more than %d characters" % BODY_MOST
        if error is not None:
            why = _in_words(error)
    if why:
        if not _ring_once(root, plant, day, RING_SEED + why, full):
            return ""
        return "%s is %s%s%s" % (plant.where, RING_SEED, why, _kinds_words(root, plant))
    body = _plain(body)
    _write(root, plant.path / "body", body)
    plant.body, plant.has_body = body, True
    if tagged and _has_come_up(plant.path):         # it grew once and its body was taken away: it comes again
        _append(root, plant.path / "rings", ["%s  %s" % (day.isoformat(), RING_AGAIN)])
        return "%s came up again from its seed (%s)" % (plant.where, plant.kind)
    when = day if tagged else sown                  # a seed that waited (tagged, never up) comes up today, signed as it was planted
    _append(root, plant.path / "rings", ["%s  %s%s" % (when.isoformat(), RING_PLANTED, plant.by if tagged else signer)])
    return "%s%s%s)" % (plant.where, CAME_UP, plant.kind)


def _tag_anew(root, plant, garden, signer, day, earliest) -> tuple:
    """A tag for a plant found with a body and no tag. Returns (what to say of it, whether it was planted just now).

    If its rings say who planted it (its tag was lost), the tag is written
    back from them. If it has no rings at all, a hand set it in whole, body
    and all (a clump lifted and divided, a plant copied in): it is planted
    now, given a place in its bed and a tag, and its rings say who planted
    it, as they would of a seed that came up. `earliest()` answers with the
    last lived day, for dating it (see `_sown_day`).

    Where layers are kept, a lost tag is put back as the last layer had it
    (see `_layered_tag`), every line of it: the plant keeps its place in
    its bed, and a hand that only took its tag away has changed nothing.
    """
    grown = any(_date_in(line[:10]) for line in _read(plant.path / "rings", 200_000).splitlines())
    kept = _layered_tag(root, plant, grown)
    if kept:
        if not _write(root, plant.path / "tag", kept):
            return "", False
        keys = hands.read_keys(kept)
        plant.at = _place_in_bed(keys, plant.name)
        _tagged(plant, kept, _date_in(hands.line(keys, "planted")), hands.line(keys, "by") or UNSEEN)
        return "put back the tag of %s, as the layers kept it" % plant.where, False
    if grown:
        planted, signed, origin = _tag_from_rings(plant.path, day, signer)
        if _write_tag(root, plant, min(planted, day), signed, origin):      # (rings carried across the glass keep the other
            return "wrote a new tag for %s" % plant.where, False           # calendar's dates: nothing is planted after today)
        return "", False
    sown = _sown_day(root, plant, day, earliest())
    others = [p.at for p in garden if p.bed.name == plant.bed.name and p is not plant and p.has_body]
    plant.at = _rounded(_open_place(others, random.Random("%s|%s|place" % (sky.place(root).get("weather-seed"), plant.where))))
    if not _write_tag(root, plant, sown, signer, _origin(root, plant)):
        return "", False
    _append(root, plant.path / "rings", ["%s  %s%s" % (sown.isoformat(), RING_PLANTED, signer)])
    return "%s%s%s)" % (plant.where, PLANTED_WHOLE, plant.kind), True


def _why_no_kind(root, plant) -> str:
    """Why a seed's kind cannot bring it up, in the garden's words; '' if it can."""
    why = _no_kind(root, plant.kind)
    if not why or (str(root), plant.kind) in _aside:
        return why
    if not plant.kind:
        return "its seed names no kind"
    if not (Path(root) / "species" / (plant.kind + ".py")).is_file():
        return "there is no kind called %s in species/" % plant.kind
    fault = _load_faults.get((str(root), plant.kind))
    return "the kind %s cannot be read%s" % (plant.kind, " (%s)" % fault if fault else "")


def _kinds_words(root, plant) -> str:
    """' (there is: twig, bough)': the kinds a seed could name, for a seed that names none that is there. Else ''."""
    if plant.kind and (Path(root) / "species" / (plant.kind + ".py")).is_file():
        return ""
    there = kinds_there(root)
    if not there:
        return " (species/ holds no kind yet)"
    return " (there is: %s%s)" % (", ".join(there[:12]), ", …" if len(there) > 12 else "")


def _has_come_up(path) -> bool:
    """Do a plant's rings say that it has ever come up?"""
    return any(_ring_said(line).startswith((RING_PLANTED,) + SOWN_RINGS) for line in _read(path / "rings", 200_000).splitlines())


def _ring_said(line) -> str:
    """What one line of a plant's rings says, after its date ('' for a line with no date)."""
    return line[10:].strip() if _date_in(line[:10]) else ""


def _rounded(at) -> tuple:
    """A place in a bed as a tag will hold it: two decimals. What is kept in memory and what is read back must agree."""
    return tuple(round(c, 2) for c in at)


def _sown_day(root, plant, day, earliest):
    """The day a hand-planted seed went into the ground: the day its seed file was written, within the unlived days."""
    try:
        written = _garden_time(root, (plant.path / "seed").stat().st_mtime).date()
    except OSError:
        return day
    return min(day, max(written, earliest))


def _origin(root, plant) -> str:
    """'packet <name>' if the seed is, word for word, one of the packets in the seedbox; else 'hand'.

    A packet taken out of the seedbox (moved, not copied, into the bed)
    is no longer there to be compared; where layers are kept, the packets
    the last layer had in the seedbox and that are gone from it now are
    asked as well.
    """
    mine = plant.seed_text.strip()
    if not mine:
        return "hand"
    for packet in _files_under(Path(root) / "seedbox", 400):
        if _read(packet, 100_000).strip() == mine:
            return "packet %s" % _packet_name(packet)
    taken = _taken_packets(root)
    return "packet %s" % taken[mine] if mine in taken else "hand"


_packets_taken = {}       # root -> {a packet's text: its name}, for the packets taken from the seedbox since the last layer


def _taken_packets(root) -> dict:
    """The packets the last layer had in the seedbox that are no longer there: {their text, stripped: their name}.
    Asked once in a tending (see `_tend`); empty where no layers are kept."""
    key = str(root)
    if key not in _packets_taken:
        _packets_taken[key] = {}
        listed = _git(root, "ls-tree", "-r", "-z", "--name-only", "HEAD", "--", "seedbox/") if _layers(root) else None
        if listed is not None and listed.returncode == 0:
            gone = [path for path in listed.stdout.decode("utf-8", errors="replace").split("\0")
                    if path.startswith("seedbox/") and not (Path(root) / path).exists()][:400]
            for path, text in _old_texts(root, gone).items():
                if text.strip():
                    _packets_taken[key].setdefault(text.strip(), _packet_name(path))
    return _packets_taken[key]


def _packet_name(path) -> str:
    """A packet is any file in the seedbox, called by its name without the `.seed` it usually ends in."""
    name = Path(path).name
    return name[:-len(".seed")] if name.endswith(".seed") and len(name) > len(".seed") else name


def _open_place(others, dice) -> tuple:
    """A place in a bed for a new plant: of a dozen tries, the one furthest from the others."""
    tries = [(dice.uniform(0.08, 0.92), dice.uniform(0.08, 0.92)) for _ in range(12)]
    if not others:
        return tries[0]
    return max(tries, key=lambda t: min(math.hypot(t[0] - x, t[1] - y) for x, y in others))


def _tag_text(plant, planted, by, origin) -> str:
    """A plant's tag, as the ground first writes it."""
    lines = ["name: %s" % plant.name, "kind: %s" % (plant.kind or "?"), "planted: %s" % planted.isoformat(),
             "by: %s" % by, "from: %s" % origin, "at: %.2f,%.2f" % plant.at]
    if plant.bed.glass:
        lines.append(TAG_UNDER)                     # (its dates are the glass's: see `_cross_glass`)
    return "\n".join(lines) + "\n"


def _tagged(plant, text, planted, by) -> None:
    """Hold in memory what a plant's tag now says."""
    plant.tag_text = text
    plant.tag = hands.read_keys(text)
    plant.planted, plant.by = planted, by
    plant.before, plant.first = _days_before(plant.tag), _first_planted(plant.tag)


def _write_tag(root, plant, planted, by, origin) -> bool:
    """Write a plant's tag. True if it was written."""
    text = _tag_text(plant, planted, by, origin)
    if not _write(root, plant.path / "tag", text):
        return False
    _tagged(plant, text, planted, by)
    return True


def _layered_tag(root, plant, grown) -> str:
    """The tag the last layer holds for this plant, as text; '' if there is none to be had.

    It is the same plant if it stands where that tag stood and has grown
    there (it has rings), or if its seed is as that layer had it: a plant
    pulled and another set in whole under the same name is not given the
    old one's tag.
    """
    if not _layers(root):
        return ""
    tag, seed = "beds/%s/tag" % plant.where, "beds/%s/seed" % plant.where
    texts = _old_texts(root, [tag, seed])
    if not texts.get(tag, "").strip():
        return ""
    if not grown and texts.get(seed, "").strip() != plant.seed_text.strip():
        return ""
    return texts[tag]


def _tag_from_rings(path, day, signer) -> tuple:
    """For a plant whose tag is lost: (planted, by, from), read back from its rings if they still say.

    A signature is not handed to someone else because a tag went missing.
    Only if the rings do not say who planted it is the new tag signed by
    whoever writes it, and dated by the first ring (or, failing that, today).
    """
    first = None
    for line in _read(path / "rings", 200_000).splitlines():
        when, said = _date_in(line[:10]), _ring_said(line)
        first = first or when
        if said.startswith(RING_PLANTED) and said[len(RING_PLANTED):].strip():
            return when, said[len(RING_PLANTED):].strip(), "hand"
        if said.startswith(SOWN_RINGS):
            return when, THE_DAYS, _origin_in(said)
    return first or day, signer, "hand"


def _origin_in(said) -> str:
    """Where a plant the days brought in came from, as its first ring says it: what its tag's `from:` would say.

        self-sown from north-wall/quince          ->  self-sown from north-wall/quince
        self-sown, cross of a/b × c/d             ->  cross of a/b × c/d
        rooted from north-wall/twist              ->  rooted from north-wall/twist
        came up by itself, from north-wall/quince ->  self-sown from north-wall/quince   (the first trials' words)
    """
    if said.startswith(RING_SOWN_ONCE):
        rest = said[len(RING_SOWN_ONCE):]
        return "self-sown " + rest if rest.startswith("from ") else rest
    if said.startswith(RING_SELF_SOWN + ", "):
        return said[len(RING_SELF_SOWN) + 2:]
    return said


def _mend_tag_name(root, plant, day) -> str:
    """A plant a hand has moved or renamed keeps its tag. The name on it is put right, and its rings say what it was."""
    was = hands.line(plant.tag, "name")
    if not was or was == plant.name or hands.line(hands.read_keys("name: " + plant.name), "name") != plant.name:
        return ""                                   # nothing to mend, or a name no tag line could carry
    lines, mended = [], False
    for line in plant.tag_text.splitlines():
        key, colon, _ = line.partition(":")
        if colon and key.strip().lower() == "name":
            if mended:
                continue
            line, mended = "name: %s" % plant.name, True
        lines.append(line)
    text = "\n".join(lines) + "\n"
    if not _write(root, plant.path / "tag", text):
        return ""
    _tagged(plant, text, plant.planted, plant.by)
    _append(root, plant.path / "rings", ["%s  %s%s" % (day.isoformat(), RING_RENAMED, _one_line(was, 80))])
    return "put the new name on the tag of %s (it said %s)" % (plant.where, _one_line(was, 80))


def _ring_once(root, plant, day, line, full=None) -> bool:
    """Add a fault to a plant's rings unless it is already the last thing they say. True if it was added."""
    if plant.last_ring == line:
        return False
    plant.last_ring, plant.last_ring_day = line, day
    _append(root, plant.path / "rings", ["%s  %s" % (day.isoformat(), line)])
    trouble(root, "%s: %s" % (plant.where, line), full, aloud=False)
    return True


# ========================================================= under the glass
#
# A bed whose `bed` file says `glass: yes` stands under glass, and the beds
# under glass keep one calendar of their own. Outdoors a day is one of the
# world's days. Under the glass the days are the visitors': each time the gate
# opens to a new visit, GLASS_WEEK days pass there, and none pass while nobody
# comes. So a visitor who comes in the dead of the garden's winter may find the
# glass in June, and every visitor finds it a week on from where the last one
# left it. Nobody can wind it by hand: it moves only as the gate does.
#
# The calendar is the file ground/glass: the day it began (`glazed`), the last
# day lived under it (`stands at`, which is its today), the days it still owes
# (`owed`: a week for each visit, less what has been lived), and how many visits
# it has counted. The days it lives are written in ground/under-glass, as the
# garden's are in the almanac, and laid down in layers signed `the glass`.
#
# Under the glass there is no frost, no snow and no wind, and the can stands in
# for the rain (sky.under_glass). No creature comes in: nothing there is bitten
# and no pollen is carried, and a seed that finds no room in its own bed is
# lost, for it cannot fall outdoors into another calendar. A plant a hand
# carries across the glass keeps its body; its tag is dated anew on the side it
# came to, and a ring says which way it went (see `_cross_glass`).

GLASS_HEAD = [
    "# The calendar under the glass. A week passes there each time the gate opens to a new visit, and none while nobody comes.",
    "# glazed: the garden's own day when the glass was set · began at: where its calendar began, the first of January after",
    "# stands at: the last day lived under it, its today · owed: days due there and not yet lived (an arrival that ran short",
    "# of time leaves some) · visits: the times the gate has opened since. A hand may change a line, and the glass goes on",
    "# from what it says: but never back before a day its chronicle holds.",
]
UNDER_GLASS_HEAD = [
    "# Under the glass: one line for each day lived there, and under it what happened that day. These are not the garden's",
    "# days (the almanac holds those): a week of them passes each time the gate opens to a new visit. Under the glass there",
    "# is no frost, no snow and no wind, and the can stands in for the rain: `watered` on the days the open sky of that date",
    "# would have rained, `dry` on the others.",
]
_GLASS_DAY = re.compile(r"^(\d{4})-(\d{2})-(\d{2})\s.*\[glass\]\s*$")      # a day as ground/under-glass holds it


@dataclass
class Glass:
    """The calendar under the glass, as ground/glass keeps it."""
    glazed: datetime.date         # the garden's own day when a door first found a bed under glass
    stands: datetime.date         # the last day lived under the glass: its today
    owed: int = 0                 # days due there and not yet lived
    visits: int = 0               # how many times the gate has opened to a new visit since it was glazed
    began: datetime.date | None = None     # where its calendar stood when it was glazed (see `_glass_begins`)


def _glass_begins(day):
    """Where the glass's calendar begins, glazed on the garden's `day`: the first of January after it.

    The glass keeps a faster calendar, not a warmer season. Begun on the
    day it was glazed, a glass set in autumn would give its first twenty
    visitors the same autumn and winter the garden has, only sooner, with
    most of what they sowed asleep under it. Begun with the year, its days
    are growing from the first visit, and spring is some eight visits off.
    """
    try:
        return Date(day.year + 1, 1, 1)
    except (ValueError, OverflowError):
        return day


def _glass_file(root) -> Path:
    return Path(root) / "ground" / "glass"


def _under_glass_file(root) -> Path:
    return Path(root) / "ground" / "under-glass"


def glass(root, day=None):
    """The calendar under the glass, or None if no bed lies under glass and none has (there is no ground/glass).

    Read forgivingly, as everything a hand may have been at: a line that
    cannot be read is as if it were not there. A glass with no record yet
    begins on `day` (else the garden's today) and has lived nothing. A day
    the chronicle holds was lived, whatever a hand's line says, and the
    calendar never stands before its own beginning.
    """
    path = _glass_file(root)
    if not path.is_file():
        if not any(bed.glass for bed in beds(root)):
            return None
        glazed = day or today(root)
        begun = _glass_stood(root) or _glass_begins(glazed)
        return Glass(glazed, begun, began=begun)
    keys = hands.read_keys(_read(path, 100_000))
    glazed, stands = _date_in(hands.line(keys, "glazed")), _date_in(hands.line(keys, "stands at"))
    began = _date_in(hands.line(keys, "began at"))
    recorded, held = stands, _glass_chronicle_end(root)
    stands = max([found for found in (stands, held) if found], default=None) or _glass_stood(root)
    glazed = glazed or day or today(root)
    began = began or stands or _glass_begins(glazed)
    stands = stands or began
    visits = int(hands.num(keys, "visits", 0, 0, 10 ** 9))
    if stands.toordinal() + GLASS_OWED_MOST + GLASS_WEEK >= Date.max.toordinal():     # the calendar itself has a last day
        return Glass(glazed, stands, 0, visits, began)
    owed = int(hands.num(keys, "owed", 0, 0, GLASS_OWED_MOST))
    if recorded and held and held > recorded:      # days the chronicle holds and the record never counted (it could not be
        owed = max(0, owed - (held - recorded).days)     # written with them): they were lived, and are owed no longer
    return Glass(glazed, stands, owed, visits, began)


def _glass_text(under) -> str:
    return "\n".join(GLASS_HEAD + ["glazed: %s" % under.glazed.isoformat(),
                                   "began at: %s" % (under.began or under.stands).isoformat(),
                                   "stands at: %s" % under.stands.isoformat(),
                                   "owed: %d" % under.owed, "visits: %d" % under.visits]) + "\n"


def _glass_chronicle_end(root):
    """The last day ground/under-glass holds, or None: a day written there was lived, and is never lived again."""
    path = _under_glass_file(root)
    try:
        size = path.stat().st_size
    except OSError:
        return None
    for most in (64_000, 50_000_000):                  # its end first; all of it, if a hand has buried its last day
        try:
            with open(path, "rb") as handle:
                handle.seek(max(0, size - most))
                tail = handle.read()
        except OSError:
            return None
        texts = [tail.decode("utf-8", errors="replace")]
        if b"\x00" in tail:                            # a hand saved it again as UTF-16 (as PowerShell's ">" does)
            texts += [tail[skip:].decode("utf-16-le", errors="replace") for skip in (0, 1)]
        dated = [_date_in(line[:10]) for text in texts for line in text.splitlines() if _GLASS_DAY.match(line.strip("\ufeff\r"))]
        found = max((lived for lived in dated if lived), default=None)
        if found or size <= most:
            return found
    return None


def _glass_stood(root):
    """Where the glass stood, when its own record cannot say: the last day of its chronicle, of the layers the glass
    laid down, of the witness beside a bed under it (`beds/<bed>/.glass`), or of the newest ring its days wrote on a
    plant under it, whichever is latest. None if nothing says.

    A lost record must not make a day be lived a second time under the
    glass, any more than a lost almanac may in the garden (see `_last_lived`).
    """
    found = [_glass_chronicle_end(root), _glass_layer_end(root)]
    found += [_date_in(hands.line(hands.read_keys(_read(bed.path / GLASS_WITNESS, 1000)), "stands at"))
              for bed in beds(root) if bed.glass]                # (the witness beside each bed under glass)
    found += [plant.last_ring_day for plant in plants(root)      # (a plant whose tag does not say glass came from the
              if plant.bed.glass and hands.line(plant.tag, "under").strip().lower() == "glass"     # garden: its rings keep
              and plant.last_ring_day and not plant.last_ring.startswith(TENDING_RINGS + HAND_RINGS)]     # the garden's days)
    return max([lived for lived in found if lived], default=None)


def _glass_layer_end(root):
    """The last day the glass's layers say was lived under it, or None if they name none (or no layers are kept).

    Its newest layers are asked, not the newest alone: the calendar under
    the glass only goes forward, so the latest day any of them names is
    where it stood.
    """
    done = _git(root, "log", "-40", "--fixed-strings", "--author=%s <%s@glebe>" % (THE_GLASS, _slug(THE_GLASS)),
                "--format=%an%x09%s") if _layers(root) else None
    if done is None or done.returncode != 0:
        return None
    dated = []
    for line in done.stdout.decode("utf-8", errors="replace").splitlines():
        author, _, said = line.partition("\t")
        if author == THE_GLASS and said.startswith("under the glass: "):      # (not a visitor whose name only holds it)
            dated += [_date_in(text) for text in re.findall(r"\d{4}-\d{2}-\d{2}", said)]
    return max([lived for lived in dated if lived], default=None)


def _begin_glass(root, day):
    """Tending's part: the first door that finds a bed under glass begins its calendar, on the garden's own day.
    Returns the calendar (None if the garden has no glass)."""
    under = glass(root, day)
    if under is not None and not _glass_file(root).is_file():
        _write(root, _glass_file(root), _glass_text(under))
    return under


def _day_of(bed, day, under):
    """The day a bed stands at: the garden's `day`, or under the glass the day the glass stands at."""
    return under.stands if under is not None and getattr(bed, "glass", False) else day


def _sky_on(root, bed, day):
    """The sky over a bed on a day of its own calendar, before the bed's own share of it (see sky.local)."""
    return sky.under_glass(root, day) if getattr(bed, "glass", False) else sky.sky_for(root, day)


def _glass_line(s) -> str:
    """A day's first line in ground/under-glass: what the can gave, the warmth, the light, the moon, the season."""
    try:
        parts = ["watered %s mm" % sky._millimetres(s.rain) if s.rain > 0 else "dry", sky._degrees(s.tmin, s.tmax),
                 "light %.1f h" % s.light]
        name = s.moon_name
        parts += ["%s moon" % name if name in ("new", "full") else "moon %s" % name, s.season]
        return "%s  %s  [glass]" % (s.date.isoformat(), " · ".join(parts))
    except Exception:
        return "%s  the day could not be read  [glass]" % getattr(s, "date", "")


def _cross_glass(root, plant, day, under) -> str:
    """A plant a hand carried across the glass: its tag is dated anew on the side it came to, and a ring says so.

    The two sides keep two calendars, so a day of one says nothing on
    the other. The tag's `planted:` becomes the day the plant came to this
    side (the day from which it lives here); `first planted:` keeps when
    and where it was planted in truth; and `days before:` keeps the days
    it had lived until then, so that its age goes with it. Its body is left
    as it is: the dates inside it are its kind's to make sense of, as after
    any hand. Which side a plant lives on is the `under: glass` line of its
    tag. Returns what to say of it, or ''.
    """
    marked = hands.line(plant.tag, "under").strip().lower() == "glass"
    if marked == bool(plant.bed.glass) or not plant.tag_text.strip():
        return ""
    its_day = _day_of(plant.bed, day, under)                               # the day of the side it came to
    left_on = (under.stands if under is not None else None) if marked else day     # and of the side it left
    lived = plant.before + (max(0, (left_on - plant.planted).days) if left_on and plant.planted else 0)
    first = plant.first or ("%s, %s" % (plant.planted.isoformat(), "under glass" if marked else "outdoors")
                            if plant.planted else "")
    lines, dated = [], False
    for line in plant.tag_text.splitlines():
        key, colon, _ = line.partition(":")
        key = " ".join(key.split()).lower() if colon else ""
        if key in ("under", "days before", "first planted"):
            continue
        if key == "planted":
            if dated:
                continue
            line, dated = "planted: %s" % its_day.isoformat(), True
        lines.append(line)
    if not dated:
        lines.append("planted: %s" % its_day.isoformat())
    if first:
        lines.append("first planted: %s" % first)
    lines.append("days before: %d" % min(lived, 400_000))
    if plant.bed.glass:
        lines.append(TAG_UNDER)
    text = "\n".join(lines) + "\n"
    if not _write(root, plant.path / "tag", text):
        return ""
    _tagged(plant, text, its_day, plant.by)
    ring = RING_UNDER if plant.bed.glass else RING_OUT
    _append(root, plant.path / "rings", ["%s  %s" % (its_day.isoformat(), ring)])
    plant.last_ring, plant.last_ring_day = ring, its_day
    return "%s %s" % (plant.where, ring.split(":")[0])


# ---- the heap, noticed

def _heap_file(root) -> Path:
    return Path(root) / "compost" / ".heap"


_ROTTED = re.compile(r"^(.*?\S)  · (\d{1,6})\.(\d) of \d+$")      # a heap line's end: how far the thing has rotted


def _read_heap(root) -> dict:
    """compost/.heap as {path within compost: the day it first lay there}."""
    return _read_heap_whole(root)[0]


def _read_heap_whole(root) -> tuple:
    """compost/.heap as ({path: the day it first lay there}, {path: how far it has rotted, in tenths of a day}).

    A thing whose line says nothing of its rotting has rotted one day for
    each day lived since it was laid there (the pace of the days before
    there were worms, and of a garden with none).
    """
    heap, rot = {}, {}
    for line in _read(_heap_file(root), 5_000_000).splitlines():
        day = _date_in(line[:10])
        where = line[10:].strip()
        if not day or not where:
            continue
        found = _ROTTED.match(where)
        if found:
            where = found.group(1)
            rot[where] = int(found.group(2)) * 10 + int(found.group(3))
        heap[where] = day
    return heap, rot


def _heap_text(heap, rot=None) -> str:
    rot = rot or {}
    lines = ["# The day each thing first lay on the heap. The ground keeps this; a text rots when it has had %d days' rotting."
             % ROT_DAYS,
             "# After a thing, how far it has rotted, in days. The worms set the pace: a warm wet day rots more than one,",
             "# a frozen day none."]
    lines += ["%s  %s%s" % (heap[path].isoformat(), path,
                            "  · %d.%d of %d" % (rot[path] // 10, rot[path] % 10, ROT_DAYS) if path in rot else "")
              for path in sorted(heap)]
    return "\n".join(lines) + "\n"


def _write_heap(root, heap, rot=None) -> None:
    _write(root, _heap_file(root), _heap_text(heap, rot))


def _note_heap(root, since, today) -> dict:
    """Look over the heap: what is new there is remembered from the day it was put; what is gone is forgotten.

    A new thing is dated by the day its file was written, if that was
    after the last day the garden lived (`since()` answers with that day);
    else by today, the day it was noticed (see `_put_on_heap`). A pulled
    plant's drawings do not rot, nor does a pulled bed's sheet, so they
    are taken off here.
    """
    compost = Path(root) / "compost"
    heap, rot = _read_heap_whole(root)
    seen = {}
    for path in _files_under(compost, 5000):
        where = path.relative_to(compost).as_posix()
        if where == "humus":
            continue
        if _own_drawing(path):
            _remove(path)
            continue
        seen[where] = heap[where] if where in heap else _put_on_heap(root, path, since(), today)
    for folder, _, files in os.walk(compost, onerror=lambda error: None):     # and their hidden leavings
        for name in (".left", ".drawn", GLASS_WITNESS):
            if name in files and folder != str(compost):
                _remove(Path(folder) / name)
    if seen != heap or (seen and not _heap_file(root).is_file()):
        _write_heap(root, seen, {where: tenths for where, tenths in rot.items() if where in seen})
    return seen


def _own_drawing(path) -> bool:
    """Is this file on the heap one of the ground's own drawings, come there with a pulled plant or a pulled bed?"""
    folder = path.parent
    if path.name in ("plate.png", "plate.svg"):
        return (folder / "seed").is_file()
    if path.name == "sheet.png":
        return (folder / "bed").is_file() or any((sub / "seed").is_file() for sub in _folders(folder))
    return False


def _put_on_heap(root, path, since, today):
    """The day a thing newly noticed on the heap is taken to have been put there.

    A file written since the last lived day was written onto the heap,
    and is dated by its own time. An older one was moved there (that is
    how a plant is pulled, and a moved file keeps its time): when, the
    ground cannot know, so it is dated today, the day it was noticed. It
    then lies its sixty days where a visitor can see it, however long
    the garden stood empty before.
    """
    try:
        written = _garden_time(root, path.stat().st_mtime).date()
    except OSError:
        return today
    return min(today, written) if written > since else today


def _remove(path) -> None:
    try:
        os.remove(path)
    except OSError:
        pass


# ================================================================ the days

ALMANAC_HEAD = [
    "# The almanac: one line for each day the garden has lived, and under it what happened that day.",
    "# In square brackets, where the day's sky came from: reckoned (worked out from the date alone), gate (the keeper's",
    "# own words in gate/sky.txt) or open-meteo (the real sky). Wind is on the Beaufort scale: 0 is calm, 10 a storm.",
]


@dataclass
class Summary:
    """What happened while days passed, gathered for the arrival note and the layer's message."""
    first: datetime.date | None = None
    last: datetime.date | None = None
    days: int = 0
    rain_days: int = 0
    rain_mm: float = 0.0
    snow_days: int = 0
    frosts: list = field(default_factory=list)       # the days with frost
    first_frost: bool = False                        # is the first of them the first of its winter?
    grew: int = 0
    came_up: list = field(default_factory=list)      # "bed/plant" of each seed the days sowed (a seedling, or a seed lying in
                                                     # the ground until its kind wakes it)
    rooted: list = field(default_factory=list)       # "bed/plant" of each piece that took root beside its parent
    founded: list = field(default_factory=list)      # (day, years) for each founding day lived
    kinds: dict = field(default_factory=dict)        # "bed/plant" -> its kind, for the plants in `events`
    died: list = field(default_factory=list)         # (day, "bed/plant", what its kind said of it) for each death
    ailing: list = field(default_factory=list)       # "bed/plant" of each plant that stands ailing at the end
    asleep: list = field(default_factory=list)       # ... of each grown plant whose kind cannot be read
    seeds: list = field(default_factory=list)        # ... of each seed that has not come up
    heaped: int = 0
    carried: list = field(default_factory=list)      # the paths, from the root, of what the days laid on the heap
    rotted: int = 0                                  # things (not files) the heap rotted down
    events: list = field(default_factory=list)       # (day, where, what) for every plant event
    aside: list = field(default_factory=list)        # (kind, what it did not come back from) for each kind set aside in these days
    slow: list = field(default_factory=list)         # the kinds found slow, whose plants took turns to grow
    slow_waited: bool = False                        # the slow kinds had their share of the time before the days were done
    given_up: str = ""                               # why no day could be lived at all, if none could
    unfinished: bool = False                         # time ran out before today was reached
    slowest: str = ""                                # if it did: the kind whose plants took most of it, if one did
    slowest_seconds: float = 0.0                     # and how long they took
    skipped: int = 0                                 # days too long ago to be lived at all
    waiting: int = 0                                 # days that are due but could not be lived (the almanac would not take them)
    earlier: int = 0                                 # of `days`, those lived by an earlier try that was stopped or cut short

    def counts(self, faults=True) -> str:
        """'9 plants grew; 2 sowed themselves; 1 is ailing'. Without `faults`: only what grew, came and went.

        A seed the days sowed is said to have sown itself, not to have come
        up: whether it is up yet, or lies in the ground until its time, is
        its kind's to say, in its own rings.
        """
        parts = []
        if self.grew:
            parts.append("%s grew" % _count(self.grew, "plant"))
        if self.came_up:
            n = len(self.came_up)
            parts.append("%d sowed %s" % (n, "itself" if n == 1 else "themselves"))
        if self.rooted:
            n = len(self.rooted)
            parts.append("%d rooted beside %s" % (n, "its parent" if n == 1 else "their parents"))
        if self.died and faults:
            parts.append("%d died" % len(self.died))
        for found, word in ((self.ailing, "ailing"), (self.asleep, "asleep")):
            if found and faults:
                parts.append("%d %s %s" % (len(found), "is" if len(found) == 1 else "are", word))
        if self.heaped:
            parts.append("%d carried to the heap" % self.heaped)
        return "; ".join(parts)

    def rotted_words(self) -> str:
        return "the heap rotted down %s" % _count(self.rotted, "thing") if self.rotted else ""


def _last_lived(root, day):
    """The last day the garden lived, not after `day`.

    The almanac's last dated line says it. So does the newest layer the
    days laid down, and the later of the two is taken: an almanac that some
    accident cut short must not make days be lived a second time. If
    neither says anything, the record of comings and goings does; failing
    that, the newest ring the days wrote on any plant. None if nothing
    says: then no day has been lived yet.

    (GROUND.md has an empty almanac begin again from `laid:`. That would
    live every day since the ground was laid a second time on plants that
    have lived them, so it is done only when nothing else remembers.)
    """
    found = [lived for lived in (_almanac_end(root, day), _days_layer_end(root, day)) if lived]
    return max(found) if found else _last_lived_otherwise(root, day)


def _almanac_end(root, day):
    """The last day the almanac holds, not after `day`. None if it holds none.

    A day is held by its own line: the date, the sky, and in brackets
    where the sky came from. A dated line some hand added without them (a
    note of the keeper's, written between two visits) is no lived day, and
    the days before it are not passed over on its account.
    """
    path = Path(root) / "ground" / "almanac"
    try:
        size = path.stat().st_size
    except OSError:
        return None
    for most in (64_000, 50_000_000):
        try:
            with open(path, "rb") as handle:
                handle.seek(max(0, size - most))
                tail = handle.read().decode("utf-8", errors="replace")
        except OSError:
            return None
        found = _last_dated(tail.splitlines(), day, _DAY_LINE)
        if found or size <= most:
            return found
    return None


def _last_dated(lines, day, shape=_DATED):
    """The latest day, not after `day`, that any of these lines begins with. (A hand may have added lines out of order.)

    `shape` is what a line must look like to count.
    """
    dated = [_date_in(line[:10]) for line in lines if shape.match(line)]
    return max((lived for lived in dated if lived and lived <= day), default=None)


def _last_lived_otherwise(root, day):
    """The last lived day as the visits say it, or the plants' rings, when the almanac and the layers say nothing.

    Only a ring the days wrote is a sign that its day was lived. What
    tending writes (a seed that stays a seed, a plant renamed), and the
    ring a hand leaves, is dated by the day a door was passed, and that may
    be before the garden's first day has been lived at all.

    The visits are not asked when the almanac stands begun (its head is
    there) but holds no day: then no day has been lived. An arrival that
    could live none (its kinds hung, its time ran out) still wrote that it
    came in, and its date is no lived day.
    """
    head = _read(Path(root) / "ground" / "almanac", 4000)
    if not head.startswith(ALMANAC_HEAD[0]):
        found = _last_dated(_read(Path(root) / "ground" / "visits").splitlines(), day)
        if found:
            return found
    rings = [p.last_ring_day for p in plants(root)              # (not a plant under glass: its rings keep another calendar)
             if p.last_ring_day and p.last_ring_day <= day and not p.bed.glass
             and not p.last_ring.startswith(TENDING_RINGS + HAND_RINGS)]
    return max(rings) if rings else None


def _almanac_line(s) -> str:
    """A day's first line in the almanac: the sky, in the almanac's own order. (Degrees and millimetres as sky.py words them.)"""
    try:
        parts = [("snow %s mm" if s.snow else "rain %s mm") % sky._millimetres(s.rain) if s.rain > 0 else "dry",
                 sky._degrees(s.tmin, s.tmax)]
        if s.frost:
            parts.append("frost")
        name = s.moon_name
        parts += ["light %.1f h" % s.light, "wind %d" % round(s.wind),
                  "%s moon" % name if name in ("new", "full") else "moon %s" % name, s.season]
        return "%s  %s  [%s]" % (s.date.isoformat(), " · ".join(parts), s.source)
    except Exception:
        return "%s  the sky could not be read  [reckoned]" % getattr(s, "date", "")


def _not_understood(kind_name) -> str:
    return "kind not understood (%s)" % (kind_name or "the seed names none")


class _Passing:
    """The garden held in memory while its days pass.

    Reading every file afresh for every day would make a long absence cost
    minutes. So the plants are read once, the days are lived on them here,
    and what changed is written back every so often (flush) in one piece:
    the whole of a stretch of days, or none of it (see `_lay_by`).
    """

    def __init__(self, root, noticed, today, under=None):
        self.root = Path(root)
        self.under = under                # the calendar under the glass, when these are its days; None for the garden's own.
                                          # The two never meet: the garden's days pass over the beds under glass, the
                                          # glass's days over every other, and each passing sees only its own plants.
        self.weather_seed = sky.place(root).get("weather-seed")
        self.laid = sky.place(root).get("laid")       # each year on this day the almanac says how long the ground has lain
        self.garden = [plant for plant in plants(root) if plant.bed.glass == (under is not None)]
        self.beds = {bed.name: bed for bed in beds(root) if bed.glass == (under is not None)}
        self.began = {plant.where for plant in self.garden}
        self.grown = set()                # the plants whose own day changed their body, in this passing
        self.kinds = {}
        self.soil = Soil(root)
        self.heap_day = None              # under the glass: the garden's own today, by which the heap dates what is laid on it
        self.glass_changed = False        # under the glass: its calendar moved on, and is to be written with the days
        if under is None:
            self.heap = _note_heap(root, lambda: noticed, today)
            kept = _read_heap_whole(root)[1]
            self.heap_rot = {where: kept[where] if where in kept else 10 * max(0, (noticed - since).days)
                             for where, since in self.heap.items()}
                                          # how far each thing on the heap has rotted, in tenths of a day (see `_rot`)
        else:                             # the heap lies outdoors and rots by the garden's days: these days leave it be
            self.heap, kept = _read_heap_whole(root)
            self.heap_rot = dict(kept)
        self.heap_changed = False
        self.not_text = set()             # things on the heap that will not rot in this run
        self.humus = None                 # its lines, read when something first rots
        self.rotted = set()               # the things (top names on the heap) that rotted
        self.blocks = []                  # almanac lines not yet written
        self.plant_lines = []             # the day's plant events: (where in the day's events, bed, plant, line), for
                                          # folding alike lines of one bed into one (see `_folded`)
        self.to_write = {}                # where -> plant whose body is to be written
        self.to_ring = {}                 # where -> (plant, ring lines to be added)
        self.to_lay = {}                  # path -> text of other files to be written whole (a seedling's seed and tag)
        self.told_aside = {name for where, name in _told_aside if where == str(self.root)}
                                          # kinds of which the almanac has been told that they were set aside
        self.spent = {}                   # kind -> [the seconds its plants' days have taken in this passing, how many days]
        self.slow = {}                    # kind -> seconds one of its plants' days takes, for the kinds found slow
        self.slow_spent = 0.0             # seconds the slow kinds have taken together since they were found slow
        self.turns = {}                   # slow kind -> the plants whose turn it is to grow on the day in hand
        self.days_due = 1                 # how many days this passing means to live (let_days_pass says)
        self.summary = Summary()
        self._in_bed = {}                 # bed name -> its living plants, for the day in hand
        rake = self.root / "gravel" / "rake"
        self.gravel = _read(rake, 200_000) if rake.is_file() and under is None else None
                                          # the raked gravel, blurred by the weather (the garden's weather: none under glass)
        self.gravel_changed = False
        self.fauna = _Fauna(self, acting=under is None)      # the creatures, and all they change
        if under is not None:
            self.fauna.names = []         # no creature comes in under the glass

    # ---- one day

    def live(self, day) -> list:
        """Live one day, in the order GROUND.md gives it.

        The sky; every plant's own day; the creatures' day (they bite,
        carry pollen, build); the plants cast their seed, seeing the pollen
        brought to them; the creatures once more, with the fallen seed
        before them (they carry it, hide it, eat it); the seed is sown; the
        heap rots, at the pace the worms set; and the rain and the wind blur
        the gravel a little.
        """
        glassy = self.under is not None
        s = sky.under_glass(self.root, day) if glassy else sky.sky_for(self.root, day)
        block = [_glass_line(s) if glassy else _almanac_line(s)]
        laid = self.laid
        if not glassy and isinstance(laid, Date) and day > laid and (day.month, day.day) == (laid.month, laid.day):
            block.append("    " + FOUNDED % _years(day.year - laid.year))
            self.summary.founded.append((day, day.year - laid.year))
        if s.remark:
            block.append("    the keeper: %s" % _one_line(s.remark, 300))
        events, fallen, lived = [], [], []
        self.plant_lines = []
        self._in_bed = {}
        self.turns = {name: self._turn(name, day) for name in self.slow}
        if self.slow and self.slow_spent >= SHARE_MOST and not self.summary.slow_waited:
            self.summary.slow_waited = True
            events.append("the slow kinds have had their share of the time: their plants wait until the next arrival")
        self.fauna.begin(day, s, events)
        local = {}
        for plant in list(self.garden):
            if plant.gone or not plant.has_body or (plant.planted is not None and plant.planted >= day):
                continue                  # carried off; or a seed still waiting to come up; or not yet sown that day
            if plant.dead:
                self._stand_dead(plant, day, events)
                continue
            if plant.kind in self.turns and plant.where not in self.turns[plant.kind]:
                continue                  # a slow kind's plant whose turn it is not (see `_spend`)
            if plant.bed.name not in local:
                local[plant.bed.name] = sky.local(s, plant.bed)
            self._kind(plant.kind)        # (the loading of a kind's file is not counted against its days)
            began = time.monotonic()
            module = self._grow(plant, day, local[plant.bed.name], events)
            self._spend(plant.kind, time.monotonic() - began, day, events)
            if module is not None:
                lived.append((plant, module))
        self.fauna.live()
        rooted = []                       # pieces of plants that took root beside them today (see `_sow_one`)
        for plant, module in lived:       # a plant a creature killed today drops no seed
            if plant.dead or plant.gone or not callable(getattr(module, "cast", None)):
                continue
            began = time.monotonic()
            self._cast(plant, module, day, local[plant.bed.name], fallen, rooted)
            self._spend(plant.kind, time.monotonic() - began, day, events, count=False)
        self.fauna.after(fallen)
        place = "the glass" if glassy else "the garden"     # (each calendar throws its own dice for a date they share)
        rooting = random.Random("%s|%s|%s|rooted" % (self.weather_seed, place, day.isoformat()))
        for item in rooted:               # not seed: the creatures never see them, and they are not among the day's two
            self._sow_one(item, day, s, rooting, events)
        dice = random.Random("%s|%s|%s|day" % (self.weather_seed, place, day.isoformat()))
        self._sow(fallen + self.fauna.sowing(), day, s, dice, events)
        if not glassy:                    # the heap and the gravel lie outdoors: they keep the garden's days
            self._rot(day, dice, events, self.fauna.pace)
            self._blur_gravel(day, s)
        self.fauna.end()
        self.blocks += block + ["    " + line for line in _folded(events, self.plant_lines)]
        self.plant_lines = []
        self._count_day(day, s)
        if glassy:                        # the glass stands a day on, and owes a day less: written with the day itself
            self.under.stands, self.under.owed = day, max(0, self.under.owed - 1)
            self.glass_changed = True
        return events

    def _kind(self, name):
        """A kind's module, loaded once for the whole passing; None if it cannot be had or was set aside."""
        if (str(self.root), name) in _aside:
            return None
        if name not in self.kinds:
            self.kinds[name] = kind(self.root, name)
        return self.kinds[name]

    def _ctx(self, plant, day, local_sky, purpose) -> Ctx:
        bed = plant.bed.name

        def others():
            if bed not in self._in_bed:
                self._in_bed[bed] = _living_in(self.garden, bed, day)
            return self._in_bed[bed]

        return Ctx(plant, day, local_sky, purpose, self.weather_seed, self.soil, others,
                   rich=self.fauna.rich_on(bed, day))

    def _grow(self, plant, day, local_sky, events):
        """One living plant's own day: the kind's `day`, guarded.

        Returns the kind's module if the plant lived its day and is still
        alive, so that it may cast its seed later in the day; else None.
        """
        module = self._kind(plant.kind)
        if module is None:
            self._pass_over(plant, day, events)
            return None
        # A body a hand made longer than the ground keeps is offered to its kind once, on the first day it is found so:
        # a kind that can read it may bring it back within bounds, and then it is fit again. If it cannot, the plant
        # ails, and its ring saying so is what keeps it from being offered again (so the days replay the same way
        # however they are divided among arrivals). A hand that cuts the body makes it fit by itself.
        offered = plant.overlong and plant.unfit and plant.last_ring != RING_AILING + plant.unfit
        if plant.unfit and not offered:
            self._ail(plant, day, RING_AILING + plant.unfit, events)
            return None
        ctx = self._ctx(plant, day, local_sky, "day")
        ctx.pollen = self.fauna.carried_for(plant.where)
        result, error, full = _ask(self.root, plant.kind, "day", plant.where, module.day, plant.body, dict(plant.seed), ctx)
        body, event = plant.body, None
        if error is None:
            body, event, error = _day_result(result)
            full = ""
        if error is not None:
            self._ail(plant, day, RING_AILING + (plant.unfit if offered else _in_words(error)), events, full)
            return None
        if offered:
            plant.unfit, plant.overlong = "", False
            event = event or "its kind read its overlong body, and it is in bounds again"
        if body != plant.body:
            self.grown.add(plant.where)
            self._set_body(plant, day, body, event or _way_of_dying(body))
        if event:
            self._ring(plant, day, event, events)
        elif plant.last_ring.startswith((RING_AILING, RING_ASLEEP)):
            self._ring(plant, day, RING_WELL, events)
        return None if plant.dead else module

    def _set_body(self, plant, day, body, died) -> None:
        """A plant's new body, from its own day or from a creature's bite. `died`: what to say if it is now dead."""
        plant.body = body
        was_dead, plant.dead = plant.dead, hands.is_dead(body)
        self.to_write[plant.where] = plant
        if plant.dead and not was_dead:
            self.summary.died.append((day, plant.where, died))
            self._in_bed.pop(plant.bed.name, None)

    def _move_in_bed(self, plant, at) -> None:
        """Move a plant's place in its bed (the `at:` on its tag), as a creature nudged it. Written with the days."""
        lines, put = [], False
        for line in plant.tag_text.splitlines():
            key, colon, _ = line.partition(":")
            if colon and key.strip().lower() == "at":
                if put:
                    continue
                line, put = "at: %.2f,%.2f" % at, True
            lines.append(line)
        if not put:
            lines.append("at: %.2f,%.2f" % at)
        text = "\n".join(lines) + "\n"
        plant.at, plant.tag_text, plant.tag = at, text, hands.read_keys(text)
        self.to_lay[plant.path / "tag"] = text

    def _spend(self, kind_name, seconds, day, events, count=True) -> None:
        """Count the time one plant's day took against its kind; and find the kinds that are slow.

        A kind's duty is a day of some fifty milliseconds. One whose plants
        take more than SLOW_CALL seconds a day, on average, is slow. A slow
        kind's plants then take turns (see `_turn`): each day only as many
        of them grow as fit in the slow kinds' ration of the time, and the
        turn moves on from day to day, so every plant has its days and
        none is left behind for good. All the slow kinds together have
        SHARE_MOST seconds of a passing; the rest belongs to the other
        plants, so the garden keeps up with the calendar. A quick kind with
        many plants is never held back by this.

        This is the one place where how fast the machine is changes what
        the days do. It touches only a kind far outside its duty, and it is
        what lets the gate open at all while such a kind is in the ground.
        It is said once, in the almanac, not in each plant's rings.

        The time a plant's cast takes is counted too, but not as a day of
        its own (`count` False): it is part of that plant's day.
        """
        spent = self.spent.setdefault(kind_name, [0.0, 0])
        spent[0] += seconds
        spent[1] += 1 if count else 0
        if not count:
            self.slow_spent += seconds if kind_name in self.slow else 0.0
            return
        if kind_name in self.slow:
            self.slow_spent += seconds
            self.slow[kind_name] = spent[0] / spent[1]
        elif spent[0] > SLOW_SEEN and spent[1] >= 3 and spent[0] / spent[1] > SLOW_CALL:
            self.slow[kind_name] = spent[0] / spent[1]
            self.turns[kind_name] = self._turn(kind_name, day)
            events.append("the kind %s is slow (%.1f s for one plant's day): from today its plants take turns to grow"
                          % (kind_name, self.slow[kind_name]))
            self.summary.slow.append(kind_name)

    def _turn(self, kind_name, day) -> set:
        """The plants of a slow kind whose turn it is to grow on `day`: as many as its ration of the time allows.

        The ration is SHARE_MOST spread over the days this passing means to
        live, shared among the slow kinds; each kind has at least one plant
        a day, until the slow kinds together have had SHARE_MOST, and then
        none until the next passing. Which plants: a run of them in name
        order, beginning each day about where the day before left off. The
        start is worked out from the date, not remembered, so the next
        arrival goes on round the bed rather than beginning again at the
        first name.
        """
        if self.slow_spent >= SHARE_MOST:
            return set()
        growing = [p.where for p in self.garden if p.kind == kind_name and p.has_body and not p.dead and not p.gone
                   and (p.planted is None or p.planted < day)]
        if not growing:
            return set()
        ration = SHARE_MOST / max(1, self.days_due) / max(1, len(self.slow))
        fit = min(len(growing), max(1, int(ration / max(self.slow.get(kind_name, SLOW_CALL), 1e-3))))
        start = (day.toordinal() * fit) % len(growing)
        return {growing[(start + n) % len(growing)] for n in range(fit)}

    def _pass_over(self, plant, day, events) -> None:
        """A plant whose kind cannot be asked today: set aside, or not understood at all."""
        what = _aside.get((str(self.root), plant.kind))
        if what is None:
            self._ail(plant, day, RING_ASLEEP + _not_understood(plant.kind), events)
            return
        if plant.kind not in self.told_aside:       # the almanac is told once; each plant's rings are told too
            self.told_aside.add(plant.kind)
            stopped = _stopped_on.get((str(self.root), plant.kind), [])
            events.append("the kind %s was set aside for the rest of these days: %s%s" % (
                plant.kind, _late(what, "its"), " (it was stopped on %s)" % _and(stopped) if stopped else ""))
            self.summary.aside.append((plant.kind, what))
        self._ail(plant, day, RING_AILING + _late(what), events)

    def _cast(self, plant, module, day, local_sky, fallen, rooted) -> None:
        """A plant's seed for the day: the kind's `cast`, guarded, told of the pollen the creatures brought (ctx.pollen).

        A cast text with a `rooted:` line is no seed but a piece of the
        plant that took root beside it (a layer, a runner): it goes to
        `rooted`, not among the seeds that fell.
        """
        ctx = self._ctx(plant, day, local_sky, "cast")
        ctx.pollen = self.fauna.pollen_for(plant.where)
        seeds, error, full = _ask(self.root, plant.kind, "cast", plant.where, module.cast, plant.body, dict(plant.seed), ctx)
        if error is not None:
            trouble(self.root, "%s: casting seed failed: %s" % (plant.where, error), full, aloud=False)
            return
        if isinstance(seeds, str):
            seeds = [seeds]
        if isinstance(seeds, (list, tuple)):
            for text in seeds[:3]:
                if isinstance(text, str) and text.strip():
                    item = _Seedfall(text[:4000], plant, rooted=_is_rooted(text[:4000]))
                    (rooted if item.rooted else fallen).append(item)

    def _ring(self, plant, day, line, events) -> None:
        """Something a plant did: a line in its rings, and in the day's block of the almanac."""
        plant.last_ring, plant.last_ring_day = line, day
        self.to_ring.setdefault(plant.where, (plant, []))[1].append("%s  %s" % (day.isoformat(), line))
        self.plant_lines.append((len(events), plant.bed.name, plant.name, line))
        events.append("%s: %s" % (plant.where, line))
        if len(self.summary.events) < 20_000:
            self.summary.events.append((day, plant.where, line))
            self.summary.kinds[plant.where] = plant.kind

    def _ail(self, plant, day, line, events, full=None) -> None:
        """A fault: the plant stays exactly as it was. Said once, however many days it stands."""
        if plant.last_ring == line:
            return
        self._ring(plant, day, line, events)
        trouble(self.root, "%s: %s" % (plant.where, line), full, aloud=False)

    def _stand_dead(self, plant, day, events) -> None:
        """A dead plant is left alone; DEAD_DAYS after its death it is carried to the heap."""
        since = _date_in(plant.body.lstrip().split("\n", 1)[0])
        if since is not None and plant.first and plant.planted and not plant.planted <= since <= day:
            since = plant.planted                      # it died on the other side of the glass, by the other calendar
        if since is None:
            if plant.last_ring != RING_FOUND_DEAD:
                self._ring(plant, day, RING_FOUND_DEAD, events)
                return
            since = plant.last_ring_day or day
        if (day - since).days >= DEAD_DAYS:
            self._carry_to_heap(plant, day, (day - since).days, events)

    def _carry_to_heap(self, plant, day, dead_days, events) -> None:
        """A plant long dead goes to the heap. Only what lived goes: its body, and anything a hand left in its folder.

        Its seed, tag and rings are the garden's bookkeeping, not words
        that were written or grown, and they are dropped here (the layers
        keep them). The body lies on the heap as compost/<name>/body and
        rots into the humus like any text.
        """
        self._write_plant(plant)
        for path in [path for path in self.to_lay if Path(path).parent == plant.path]:
            del self.to_lay[path]                      # (a tag a creature moved: the tag goes, and is not written after)
        for name in DRAWN_FILES:
            _remove(plant.path / name)
        compost = self.root / "compost"
        target = compost / _unique(plant.name, lambda name: (compost / name).exists())
        try:
            compost.mkdir(parents=True, exist_ok=True)
            shutil.move(str(plant.path), str(target))
        except OSError as error:
            trouble(self.root, "%s could not be carried to the heap" % plant.where, error)
            return
        for name in ("seed", "tag", "rings"):          # (dropped once it is off the bed: a plant half carried stays a plant)
            _remove(target / name)
        events.append("%s: carried to the heap, %d days dead" % (plant.where, dead_days))
        plant.gone = True
        self.summary.heaped += 1
        for path in _files_under(target, 200):
            where = path.relative_to(compost).as_posix()
            self.heap[where] = self.heap_day or day        # (from under the glass: laid there on the garden's own day)
            self.heap_rot[where] = 0
            self.summary.carried.append("compost/" + where)
        self.heap_changed = True
        self.soil.turn()

    # ---- seeds that fell

    def _sow(self, falling, day, s, dice, events) -> None:
        """Bring up at most SOWN_A_DAY of the day's seeds, where there is room.

        They are the seeds the plants dropped, those a creature carried to
        another bed, and those forgotten in the larder (see `_Seedfall`):
        all take their chance together, in an order the day's dice give.
        """
        dice.shuffle(falling)
        sown = 0
        for item in falling:
            if sown >= SOWN_A_DAY:
                break
            sown += 1 if self._sow_one(item, day, s, dice, events) else 0

    def _room_in(self, bed_name) -> bool:
        bed = self.beds.get(bed_name)
        if bed is None:
            return False
        return sum(1 for p in self.garden if p.bed.name == bed_name and not p.dead and not p.gone) < bed.room

    def _sow_one(self, item, day, s, dice, events) -> bool:
        """One seed: a place, a name, a body from the kind's sprout. True if it was sown.

        A seed a plant dropped is sown near it (seven times in ten, if there
        is room), else in the wild corner. One a creature carried is sown
        anywhere in the bed it was carried to, if there is room there. One
        forgotten in the larder is sown somewhere: in any bed with room but
        the keeper's own. Whether it is up at once or lies in the ground as a
        seed is its kind's to say, in its sprout and its days.

        A cast text with a `rooted:` line (a layer, a runner: a piece of its
        parent that took root) is no seed. It stays in its parent's bed,
        close beside it, or is lost if the bed has no room; no creature sees
        it, and it is not among the day's SOWN_A_DAY. Its ring says `rooted
        from <parent>`, and its tag keeps the `rooted:` line.

        Its folder is made at once, so that nothing else takes the name.
        Its seed, its tag and its body are written with the rest of the
        stretch of days (flush), not before.
        """
        text, parent, hidden = item.text, item.parent, item.hidden
        keys = hands.read_keys(text)
        if item.rooted:
            if parent is None or not self._room_in(parent.bed.name):
                return False                                      # no room beside its parent: the piece withers
            bed = parent.bed
            at = tuple(min(0.96, max(0.04, c + dice.gauss(0.0, 0.05))) for c in parent.at)
        elif item.to is not None:
            bed = self.beds.get(item.to)
            if bed is None or not self._room_in(bed.name):
                return False                                      # no room where it was carried: the seed is lost
            at = (dice.uniform(0.06, 0.94), dice.uniform(0.06, 0.94))
        elif hidden is not None:
            open_beds = [name for name in sorted(self.beds) if name != KEEPERS_BED and self._room_in(name)]
            if not open_beds:
                return False
            bed = self.beds[dice.choice(open_beds)]
            at = (dice.uniform(0.06, 0.94), dice.uniform(0.06, 0.94))
        elif parent is None:
            return False
        elif (dice.random() < 0.7 or self.under is not None) and self._room_in(parent.bed.name):
            bed = parent.bed
            at = tuple(min(0.96, max(0.04, c + dice.gauss(0.0, 0.12))) for c in parent.at)
        elif self._room_in(WILD_BED):
            bed = self.beds[WILD_BED]
            at = (dice.uniform(0.06, 0.94), dice.uniform(0.06, 0.94))
        else:
            return False                                          # no room anywhere: the seed is lost
        kind_name = _kind_name(keys) or (parent.kind if parent else "")
        module = self._kind(kind_name) if kind_name else None
        if module is None:
            return False
        fell_from = parent.where if parent else hidden.where if hidden else ""
        wanted = _folder_name(hands.line(keys, "name"), "") or _seedling_name(
            fell_from.rsplit("/", 1)[-1] if fell_from else kind_name)
        taken = {p.name for p in self.garden if not p.gone}
        name = _unique(wanted, lambda n: n in taken or _holds_something(bed.path / n))
        origin = hands.line(keys, "from") or ("%s%s" % (RING_ROOTED, fell_from) if item.rooted
                                              else "self-sown from %s" % fell_from if fell_from else "carried by %s" % item.by)
        seed_text = _seed_without_tag_lines(text, kind_name)
        path = bed.path / name
        seedling = Plant(path=path, bed=bed, name=name, where="%s/%s" % (bed.name, name),
                         seed=hands.read_keys(seed_text), tag={}, kind=kind_name, body="", dead=False,
                         seed_text=seed_text, at=_rounded(at), planted=day, by=THE_DAYS)
        body = ""
        if callable(getattr(module, "sprout", None)):
            body, error, full = _ask(self.root, kind_name, "sprout", seedling.where, module.sprout, dict(seedling.seed),
                                     self._ctx(seedling, day, sky.local(s, bed), "sprout"))
            if error is None and (not isinstance(body, str) or len(body) > BODY_MOST):
                error, full = "sprout gave back no body the ground could keep", ""
            if error is not None:
                trouble(self.root, "a seed of %s did not come up: %s" % (fell_from or kind_name, error), full, aloud=False)
                return False
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            trouble(self.root, "%s could not be made" % seedling.where, error)
            return False
        seedling.body = _plain(body)
        tag = _tag_text(seedling, day, THE_DAYS, origin)
        if item.rooted:
            tag += "rooted: %s\n" % (_one_line(hands.line(keys, "rooted"), 80) or "here")
            came = RING_ROOTED + parent.where
        elif origin.startswith("self-sown from "):
            came = origin
        else:
            came = "%s, %s" % (RING_SELF_SOWN, origin)
        if item.to is not None and item.by:
            tag += "carried: by %s%s\n" % (item.by, " (%s)" % item.why if item.why else "")
            came += "" if origin.startswith("carried by") else ", carried by %s" % item.by
        elif hidden is not None:
            tag += "hidden: by %s on %s%s, and forgotten\n" % (hidden.by, hidden.day.isoformat(),
                                                               " (%s)" % hidden.why if hidden.why else "")
            came += ", hidden by %s and forgotten" % hidden.by
            self.fauna.found(hidden)
        _tagged(seedling, tag, day, THE_DAYS)
        self.to_lay[path / "seed"] = seed_text
        self.to_lay[path / "tag"] = tag
        self.to_write[seedling.where] = seedling
        self._ring(seedling, day, _one_line(came, 200), events)
        self.garden.append(seedling)
        self.garden.sort(key=lambda plant: plant.where)
        (self.summary.rooted if item.rooted else self.summary.came_up).append(seedling.where)
        return True

    # ---- the heap

    def _rot(self, day, dice, events, pace=10) -> None:
        """Rot every text that has had ROT_DAYS days' rotting on the heap into the humus.

        Each day a thing lies on the heap (after the day it was laid there)
        it rots by the day's pace: `pace` tenths of a day, ten unless the
        worms have said otherwise (garden.heap_pace), none in a frost if
        they say so. It is counted in whole tenths, so that it adds up the
        same however the days are divided among arrivals, and compost/.heap
        keeps the count.

        The humus is written before anything is taken off the heap, so no
        line is lost between the two. And it is written that same day: the
        soil a kind reads next morning is then the soil on the disk,
        however the days happen to be divided into arrivals.
        """
        for where, since in self.heap.items():
            if since < day and pace:
                self.heap_rot[where] = self.heap_rot.get(where, 0) + pace
                self.heap_changed = True
        due = sorted(where for where in self.heap
                     if self.heap_rot.get(where, 0) >= ROT_DAYS * 10 and where not in self.not_text)
        rotting = []
        for where in due:
            path = self.root / "compost" / where
            if not path.is_file():
                del self.heap[where]
                self.heap_rot.pop(where, None)
                self.heap_changed = True
            elif not _is_text(path) or not os.access(path, os.W_OK):
                self.not_text.add(where)                          # a stone in the heap: left alone
            else:
                rotting.append((where, path))
        if not rotting:
            return
        if self.humus is None:
            self.humus = _read(self.root / "compost" / "humus", 5_000_000).splitlines()
        for _, path in rotting:
            self._scatter(path, dice)
        if not _write(self.root, self.root / "compost" / "humus", "\n".join(self.humus) + ("\n" if self.humus else "")):
            self.not_text.update(where for where, _ in rotting)   # the humus cannot take them: they lie where they are
            self.humus = None
            return
        for where, path in rotting:
            self._take_off(where, path)
        things = sorted({where.split("/")[0] for where, _ in rotting})
        shown = ", ".join(things[:4]) + (", …" if len(things) > 4 else "")
        events.append("the heap: rotted down %s (%s)" % (_count(len(things), "thing"), shown))
        self.rotted.update(things)
        self.soil.turn()

    def _scatter(self, path, dice) -> None:
        """Up to ROT_LINES lines of a rotting text, each put somewhere among the newest of the humus."""
        lines = [line.strip()[:ROT_LINE] for line in _read(path).splitlines() if line.strip()]
        if len(lines) > ROT_LINES:
            lines = [lines[i] for i in sorted(dice.sample(range(len(lines)), ROT_LINES))]
        for line in lines:
            self.humus.insert(dice.randint(max(0, len(self.humus) - HUMUS_TOP), len(self.humus)), line)
        del self.humus[:max(0, len(self.humus) - HUMUS_MOST)]      # the oldest leach away

    def _take_off(self, where, path) -> None:
        """Remove from the heap a file whose lines are in the humus now; emptied folders go too."""
        try:
            os.remove(path)
        except OSError as error:
            trouble(self.root, "%s would not rot" % _rel(self.root, path), error)
            self.not_text.add(where)
            return
        del self.heap[where]
        self.heap_rot.pop(where, None)
        self.heap_changed = True
        folder = path.parent
        while folder != self.root / "compost":
            try:
                folder.rmdir()
            except OSError:
                break
            folder = folder.parent

    # ---- keeping count, and writing back

    def _count_day(self, day, s) -> None:
        tally = self.summary
        tally.first = tally.first or day
        tally.last = day
        tally.days += 1
        if s.rain > 0:
            tally.rain_days += 1
            tally.rain_mm += sky._as_written(s.rain)     # as the almanac writes the day, so the note's total is theirs
            tally.snow_days += 1 if s.snow else 0
        if s.frost:
            tally.frosts.append(day)

    def _write_plant(self, plant) -> None:
        """Write one plant's body and rings now (it is about to be carried off)."""
        if self.to_write.pop(plant.where, None) is not None:
            _write(self.root, plant.path / "body", plant.body)
        rings = self.to_ring.pop(plant.where, None)
        if rings is not None:
            _append(self.root, plant.path / "rings", rings[1])

    def _blur_gravel(self, day, s) -> None:
        """The day's rain and wind on the raked gravel (see `_blurred`). Its own dice: the gravel touches nothing else."""
        if not self.gravel:
            return
        dice = random.Random("%s|the gravel|%s" % (self.weather_seed, day.isoformat()))
        blurred = _blurred(self.gravel, s.rain, s.wind, dice)
        if blurred != self.gravel:
            self.gravel, self.gravel_changed = blurred, True

    def flush(self) -> None:
        """Write back what has changed since the last flush: all of it, or none of it (see `_lay_by`).

        With the plants go the creatures' files, the larder, the richness of
        the beds, the things made and unmade, the heap's record and the gravel.
        """
        whole = dict(self.to_lay)
        for plant in self.to_write.values():
            whole[plant.path / "body"] = plant.body
        if self.heap_changed:
            whole[_heap_file(self.root)] = _heap_text(self.heap, self.heap_rot)
        whole.update(self.fauna.whole())
        if self.gravel_changed:
            whole[self.root / "gravel" / "rake"] = self.gravel
        removed = self.fauna.removed()
        added = {plant.path / "rings": lines for plant, lines in self.to_ring.values()}
        if self.blocks:
            added[_under_glass_file(self.root) if self.under is not None else self.root / "ground" / "almanac"] = self.blocks
        if self.glass_changed:
            whole[_glass_file(self.root)] = _glass_text(self.under)
            for bed in self.beds.values():             # and its witness beside each bed under it
                whole[bed.path / GLASS_WITNESS] = "stands at: %s\n" % self.under.stands.isoformat()
        if whole or added or removed:
            _lay_by(self.root, whole, added, removed)
        self.fauna.flushed()
        self.to_lay, self.to_write, self.to_ring, self.blocks, self.heap_changed = {}, {}, {}, [], False
        self.gravel_changed = self.glass_changed = False

    def _slowest(self) -> tuple:
        """The kind whose plants took most of the time of this passing (more than half), and how many seconds. Else ('', 0)."""
        name = max(self.spent, key=lambda kind_name: self.spent[kind_name][0], default="")
        if not name or self.spent[name][0] <= sum(seconds for seconds, _ in self.spent.values()) / 2:
            return "", 0.0
        return name, self.spent[name][0]

    def stop_short(self) -> None:
        """Time has run out before today was reached. The almanac says so under the last day lived, and where the time went."""
        self.summary.unfinished = True
        name = self._slowest()[0]
        self.blocks.append("    the days went slowly, and stop here until the next arrival%s"
                           % ("; most of the time went to the kind %s" % name if name else ""))

    def finish(self) -> Summary:
        """Count how the plants stand at the end."""
        tally = self.summary
        for plant in self.garden:
            if plant.gone or plant.dead:
                continue
            if plant.where in self.grown and plant.where in self.began:     # by its own days: a plant only bitten
                tally.grew += 1                                               # did not grow (and a seedling came up)
            if not plant.has_body:
                tally.seeds.append(plant.where)
            elif plant.last_ring.startswith(RING_AILING):
                tally.ailing.append(plant.where)
            elif plant.last_ring.startswith(RING_ASLEEP):
                tally.asleep.append(plant.where)
        tally.rotted = len(self.rotted)
        if tally.unfinished:
            tally.slowest, tally.slowest_seconds = self._slowest()
        if tally.frosts and tally.days <= 200:                # over a longer stretch there is more than one winter
            tally.first_frost = _no_frost_before(self.root, tally.frosts[0])
        for line in sky.troubles:                             # the sky fell back on a bare reckoning, and said why
            trouble(self.root, "the sky: %s" % line, aloud=False)
        del sky.troubles[:]
        return tally


def _way_of_dying(body) -> str:
    """How a plant died, as its own † line says, when its kind gave no word for it: for the note, which tells the
    deaths a line for each way of dying. '† 2027-08-05, dried out as a prothallus' -> 'dried out as a prothallus';
    'died' if the line says no more than the day."""
    first = next((line for line in _plain(body).splitlines() if line.strip()), "")
    said = first.strip().lstrip(DAGGER).strip()
    how = said[10:] if _date_in(said[:10]) else said
    return _one_line(how.strip(" ,.;:-"), 80) or "died"


def _day_result(result):
    """What a kind's `day` gave back, checked: (body, event or None, fault or None)."""
    event = None
    if isinstance(result, (tuple, list)) and len(result) == 2:
        result, event = result
    if not isinstance(result, str):
        return None, None, "day gave back no body"
    if len(result) > BODY_MOST:
        return None, None, "day gave back a body over %d characters" % BODY_MOST
    event = _one_line(event, 200) if isinstance(event, str) and event.strip() else None
    return _plain(result), event, None             # as it will be read back from its file: what is kept and what is written agree


FOLD_FROM = 3             # plants of one bed that say the very same thing on one day, from which the almanac says it once


def _folded(events, plant_lines) -> list:
    """The day's events as the almanac writes them: what several plants of one bed said alike, said once.

        gate-border, 8 plants: came into flower (hawthorn, honeysuckle, quince, ...)

    Only the plants' own lines are folded (`plant_lines` says which they
    are, and where they lie among the events), and only FOLD_FROM or more
    alike in one bed. The folded line stands where the first of them stood.
    Each plant's rings keep their own line: this is the almanac's way of
    telling, not what happened to any one plant.
    """
    groups = {}
    for at, bed, name, line in plant_lines:
        if 0 <= at < len(events) and events[at] == "%s/%s: %s" % (bed, name, line):
            groups.setdefault((bed, line), []).append((at, name))
    put, gone = {}, set()
    for (bed, line), members in groups.items():
        if len(members) >= FOLD_FROM:
            put[members[0][0]] = "%s, %s: %s (%s)" % (bed, _count(len(members), "plant"), line,
                                                      ", ".join(name for _, name in members))
            gone.update(at for at, _ in members[1:])
    return [put.get(at, line) for at, line in enumerate(events) if at not in gone]


def _unique(name, taken) -> str:
    """A name nothing else has: itself, or itself with -ii, -iii, ..."""
    if not taken(name):
        return name
    n = 2
    while taken("%s-%s" % (name, hands.roman(n))) and n < 3999:
        n += 1
    return "%s-%s" % (name, hands.roman(n))


def _holds_something(path) -> bool:
    """Is there anything at this path but an empty folder? (An empty folder is a name not yet taken.)"""
    try:
        return path.exists() and not (path.is_dir() and not any(path.iterdir()))
    except OSError:
        return True


def _seedling_name(parent_name) -> str:
    """quince -> quince-seedling; quince-seedling-iii -> quince-seedling (made unique afterwards).

    Never over 40 characters: a folder named after a long-named parent must
    still find room on a machine whose paths are short.
    """
    base = re.sub(r"-seedling(-[ivxlcdm]+)?$", "", parent_name) or parent_name
    return _folder_name("%s-seedling" % base[:31].rstrip(" .-"), "seedling")


def _seed_without_tag_lines(text, kind_name) -> str:
    """A cast seed's text as it goes into the seed file: `name:`, `from:` and `rooted:` moved out, `kind:` made sure of."""
    kept = []
    for line in text.replace("\r", "").split("\n"):
        key, colon, _ = line.partition(":")
        if not (colon and key.strip().lower() in ("name", "from", "rooted")):
            kept.append(line)
    if not _kind_name(hands.read_keys("\n".join(kept))):
        kept.insert(0, "kind: %s" % kind_name)
    return "\n".join(kept).strip("\n") + "\n"


def _no_frost_before(root, day) -> bool:
    """True if no night of the 150 before `day` froze (since the ground was laid): this frost opens its winter."""
    laid = sky.place(root).get("laid")
    back = day - ONE_DAY
    for _ in range(150):
        if isinstance(laid, Date) and back < laid:
            break
        if sky.sky_for(root, back).frost:
            return False
        back -= ONE_DAY
    return True


def live(root, day) -> list:
    """Live one day, from the files and back into them. Returns the day's event lines."""
    _finish_passing(root)
    passing = _Passing(root, day, day)
    try:
        return passing.live(day)
    finally:
        passing.flush()


def let_days_pass(root, until, budget=DAYS_BUDGET) -> Summary:
    """Live every unlived day up to and including `until`. Returns what happened."""
    root = Path(root)
    _finish_passing(root)
    last = _last_lived(root, until)
    if last and last >= until:
        return Summary()
    laid = sky.place(root).get("laid")
    first = last + ONE_DAY if last else (laid if isinstance(laid, Date) else until)
    if first > until:
        return Summary()
    skipped = 0
    if (until - first).days >= MOST_DAYS:
        skipped = (until - first).days + 1 - MOST_DAYS
        first = until - _days(MOST_DAYS - 1)
    almanac = root / "ground" / "almanac"
    opening = [] if _read(almanac, 4000).strip() else list(ALMANAC_HEAD)
    if skipped:
        opening.append("# %s: %d days before this were never lived; the garden stood too long." % (first.isoformat(), skipped))
    if not _append(root, almanac, opening) or not _can_append(almanac):
        trouble(root, "the almanac cannot be written, so no days passed")
        return Summary(waiting=(until - first).days + 1)
    passing = _Passing(root, last or first, until)
    passing.summary.skipped = skipped
    passing.days_due = (until - first).days + 1
    began = flushed = time.monotonic()
    day, lived = first, 0
    try:
        while True:
            started = time.monotonic()
            passing.live(day)
            lived += 1
            moment = time.monotonic()
            took = moment - started
            if moment - flushed > 8.0 or lived % 50 == 0:
                passing.flush()
                flushed = moment
            if day >= until:                       # (tested before a day is added: the calendar itself has a last day)
                break
            if moment - began + took > budget:     # (a day is lived whole or not begun: one that would not end in time waits)
                passing.stop_short()
                break
            day += ONE_DAY
    finally:
        passing.flush()
    return passing.finish()


def let_glass_pass(root, more=0, budget=GLASS_BUDGET) -> Summary:
    """Live the days owed under the glass, `more` of them newly owed. Returns what happened, as `let_days_pass` does.

    An arrival that opens the gate to a new visit asks for GLASS_WEEK more;
    one that goes on with a visit asks for none, and lives only what an
    earlier arrival found no time for. What is owed is written down before
    any of it is lived, so a week is never lost to an arrival cut short;
    and each day lived is written with the calendar that counts it (see
    `_Passing.flush`), so none is ever lived twice. With no bed under
    glass, nothing is owed and nothing passes.
    """
    root = Path(root)
    _finish_passing(root)
    if not any(bed.glass for bed in beds(root)):
        return Summary()
    under = glass(root)
    if under is None:
        return Summary()
    owed = min(GLASS_OWED_MOST, under.owed + max(0, int(more)))
    visits = under.visits + (1 if more else 0)
    if (owed, visits) != (under.owed, under.visits) or not _glass_file(root).is_file():
        under.owed, under.visits = owed, visits
        if not _write(root, _glass_file(root), _glass_text(under)):
            trouble(root, "ground/glass cannot be written, so no days passed under the glass")
            return Summary(waiting=owed)
    if under.owed <= 0:
        return Summary()
    chronicle = _under_glass_file(root)
    opening = [] if _read(chronicle, 4000).strip() else list(UNDER_GLASS_HEAD)
    if not _append(root, chronicle, opening) or not _can_append(chronicle):
        trouble(root, "ground/under-glass cannot be written, so no days passed under the glass")
        return Summary(waiting=under.owed)
    first, until = under.stands + ONE_DAY, under.stands + _days(under.owed)
    held = _glass_chronicle_end(root)
    if held and first > held + ONE_DAY:            # a hand set the calendar on: no door did, and the chronicle says so
        _append(root, chronicle, ["# The calendar was set on by a hand, from %s to %s. The days between were never lived."
                                  % (held.isoformat(), under.stands.isoformat())])
    passing = _Passing(root, under.stands, until, under=under)
    passing.heap_day = today(root)
    passing.days_due = under.owed
    began = flushed = time.monotonic()
    day, lived = first, 0
    try:
        while True:
            started = time.monotonic()
            passing.live(day)
            lived += 1
            moment = time.monotonic()
            took = moment - started
            if moment - flushed > 8.0 or lived % 50 == 0:
                passing.flush()
                flushed = moment
            if day >= until:
                break
            if moment - began + took > budget:     # (a day is lived whole or not begun: the rest stay owed)
                passing.stop_short()
                break
            day += ONE_DAY
    finally:
        passing.flush()
    summary = passing.finish()
    summary.waiting = under.owed                   # what is still owed there, for the note
    return summary


def _can_append(path) -> bool:
    try:
        with open(path, "a", encoding="utf-8"):
            return True
    except OSError:
        return False


# ---- writing a stretch of days down, whole or not at all

def _passing_file(root) -> Path:
    return Path(root) / "ground" / ".passing"


def _lay_by(root, whole, added, removed=()) -> None:
    """Write a stretch of days back into the garden so that all of it is there, or none.

    `whole` is {path: text} for the files written whole (bodies, a new
    seedling's seed and tag, the heap's record, the creatures' files and
    things); `added` is {path: lines} for the files that grow at their end
    (rings, the almanac); `removed` are the things creatures unmade.

    First every whole file is written beside its place. Then one small
    file, ground/.passing, says what is about to be done. Only then are the
    files moved into place and the lines added, and the small file removed.
    A run cut short before ground/.passing stands has changed nothing; one
    cut short after it is finished by the next door (`_finish_passing`).
    Either way no plant is left a day ahead of the almanac, or behind it.
    """
    staged, unstaged = [], []
    for path, text in whole.items():
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            _stage(path, text)
            staged.append(path)
        except OSError:                                # no room beside it for a second file (a path at the very edge
            unstaged.append((path, text))              # of what the system allows): it is written where it stands, below
    intent = {"staged": [_rel(root, path) for path in staged],
              "added": {_rel(root, path): list(lines) for path, lines in added.items()},
              "removed": [_rel(root, path) for path in removed]}
    _write(root, _passing_file(root), json.dumps(intent, ensure_ascii=False, indent=1))
    for path, text in unstaged:
        _write(root, path, text)
    _carry_out(root, intent, again=False)
    _remove(_passing_file(root))


def _carry_out(root, intent, again) -> None:
    """Do what ground/.passing says. `again`: this may be the second time, so what is already done is left alone."""
    root = Path(root)
    for where in intent["staged"]:
        part = _part(root / where)
        if not part.is_file():
            continue                                   # already in its place
        try:
            _put_in_place(part, root / where)
        except OSError as error:
            _remove(part)
            trouble(root, "the file %s could not be written" % where, error)
    for where, lines in intent["added"].items():
        if again:
            _add_once(root, root / where, lines)
        else:
            _append(root, root / where, lines)
    for where in intent.get("removed", ()):
        if (root / where).is_file():
            _remove(root / where)
        _remove((root / where).with_name((root / where).name + ".png"))    # its drawing, if it was drawn


def _add_once(root, path, lines) -> None:
    """Add lines to the end of a file, leaving out those that are its last lines already.

    This is what lets a cut be mended without saying anything twice. A
    last line that was torn in the middle of being written is taken off
    first, if it is the beginning of one of these.
    """
    wanted = [line.encode("utf-8", errors="replace") for line in lines]
    try:
        with open(path, "rb") as handle:
            handle.seek(0, os.SEEK_END)
            end = handle.tell()
            handle.seek(max(0, end - sum(len(line) + 1 for line in wanted) - 8))
            tail = handle.read()
    except OSError:
        tail, end = b"", 0
    torn = tail[tail.rfind(b"\n") + 1:]
    if torn and any(line.startswith(torn) for line in wanted):
        try:
            os.truncate(path, end - len(torn))
            tail = tail[:len(tail) - len(torn)]
        except OSError:
            pass
    have = tail.split(b"\n")[:-1]
    done = max(n for n in range(len(wanted) + 1) if n == 0 or have[-n:] == wanted[:n])
    _append(root, path, lines[done:])


def _finish_passing(root) -> None:
    """Finish a stretch of days that a cut run left half written down, and clear away what it left lying.

    Every door does this before anything else, and so does every letting
    of days. When no run was cut short there is nothing to find.
    """
    root = Path(root)
    journal = _passing_file(root)
    if journal.is_file():
        intent = _intent_in(root, _read(journal, 50_000_000))
        if intent is not None:
            _carry_out(root, intent, again=True)
        _remove(journal)
    folders = [root / "ground", root / "ground" / "creatures", root / "compost", root / "gravel"]
    for bed in _folders(root / "beds"):
        folders += [bed] + _folders(bed)
    for folder in folders:                             # staged files with nothing to say where they go: never to be used
        try:
            for part in folder.glob(".*.part"):
                _remove(part)
        except OSError:
            pass


def _intent_in(root, text):
    """What a ground/.passing file says is to be done, if it can be read; else None.

    Only the files the days themselves write are taken from it (see
    `_days_own`). Whatever else a damaged or a crafted journal names is
    left out: no door writes outside the garden, or into the shed, on the
    word of a file.
    """
    try:
        intent = json.loads(text)
        staged = [where for where in intent["staged"] if _days_own(root, where)]
        added = {where: [str(line) for line in lines] for where, lines in intent["added"].items() if _days_own(root, where)}
        removed = [where for where in intent.get("removed", []) if _is_thing_path(where) and _days_own(root, where)]
    except (ValueError, TypeError, KeyError, AttributeError):
        return None
    return {"staged": staged, "added": added, "removed": removed}


_PLANT_FILE = re.compile(r"beds/[^/\\:]+/[^/\\:]+/(body|seed|tag|rings)")
DAYS_RECORDS = ("ground/almanac", "compost/.heap", "ground/larder", "ground/rich", "ground/made", "ground/pollen",
                "gravel/rake", "ground/glass", "ground/under-glass")


def _is_thing_path(where) -> bool:
    """Is this path, from the root, where a creature may make a thing: beds/<bed>/<a name a thing may have>?"""
    parts = str(where).split("/")
    return len(parts) == 3 and parts[0] == "beds" and bool(parts[1]) and _thing_name_ok(parts[2])


def _days_own(root, where) -> bool:
    """Is this path, written from the root, one of the files the days write, and does it lie inside the garden?

    They write a plant's body, seed, tag and rings, the almanac, the
    heap's record, the creatures' own files (ground/creatures/<name>), the
    larder, the beds' richness, the record of things made and the things
    themselves (beds/<bed>/<thing>), and the gravel: nothing else.
    """
    if not isinstance(where, str):
        return False
    parts = where.split("/")
    creature_file = len(parts) == 3 and parts[:2] == ["ground", "creatures"] and CREATURE_NAME.fullmatch(parts[2])
    witness = len(parts) == 3 and parts[0] == "beds" and bool(parts[1]) and parts[2] == GLASS_WITNESS
    if not (_PLANT_FILE.fullmatch(where) or where in DAYS_RECORDS or creature_file or witness or _is_thing_path(where)):
        return False
    if any(part in (".", "..") for part in where.split("/")):
        return False
    try:
        root = Path(root).resolve()
        return root in (root / where).resolve().parents        # (a bed that is a link leads out, and is not followed)
    except OSError:
        return False


# =============================================================== creatures
#
# Creatures live in the days between visits, beside the plants, so a visitor
# almost never meets one: they find what it did. Each is one small program,
# creatures/<name>.py, with one job. What it knows of itself is its own file,
# ground/creatures/<name>, which hands may read and change like any other.
#
# A creature touches the garden only through the Garden it is handed, and
# every act is signed with its name: a bite leaves a ring on the plant, in
# the kind's own words; a seed it carried says so on its seedling's tag; a
# seed it hid lies in ground/larder under its name; a bed it made richer
# says so in ground/rich; a thing it made is known as its own in
# ground/made. What it says of its day goes into the almanac, under its name.
#
# Where creatures come in a day is said at `_Passing.live`. They are guarded
# exactly as kinds are: a creature that raises sleeps for that day, one that
# does not come back is set aside, and the days go on either way. At a door
# a creature is asked only two things: `present`, at an arrival, with a
# garden that may be looked at and not touched; and `draw`, when a visitor
# looks at a thing it made.
#
# Besides NAME, a creature may say two things of itself. CALLED is what it is
# called in what is written: NAME = "pony" keeps its file's name, and
# CALLED = "the pony" is the name in every ring and line, the one the kinds
# are given when it bites. ABOUT is when it is about, 'day', 'dusk' or 'night'
# ('day' if it says nothing): the kinds count the flowers it finds open at that
# part of the day, so a flower may open at dusk for the moths and be shut to
# the bees.

_creatures = {}           # (root, "creatures/<name>") -> (the file's stamp, the module or None)


def creatures_there(root) -> list:
    """The names of the creatures that stand in creatures/, in order."""
    try:
        return sorted(path.stem for path in (Path(root) / "creatures").glob("*.py") if CREATURE_NAME.fullmatch(path.stem))
    except OSError:
        return []


def creature(root, name):
    """The loaded module of the creature `name`, or None if it cannot be had. Cached; reloaded when its file changes."""
    name = str(name or "")
    if not CREATURE_NAME.fullmatch(name):
        return None
    program = CREATURE + name
    path = _program_path(root, program)
    try:
        status = path.stat()
        stamp = (status.st_mtime_ns, status.st_size)
    except OSError:
        stamp = None
    key = (str(root), program)
    known = _creatures.get(key)
    if known is not None and known[0] == stamp:
        return known[1]
    if known is not None:                          # the file has changed: what was held against the old one is forgotten
        _forget_stops(root, program)
    if key in _aside:
        return None
    module = None
    if stamp is not None:
        module = _load_program(root, program, path, "glebe_creature_" + name.replace("-", "_"),
                               "a creature needs a function day(garden, ctx)")
    _creatures[key] = (stamp, module)
    return module


def _kept(text) -> str:
    """Text exactly as it will read back from a file the ground writes.

    What the days hold in memory and what the next arrival reads from the
    disk must agree, or a year lived in one arrival and the same year in
    many would come out differently.
    """
    text = str(text).encode("utf-8", errors="replace").decode("utf-8", errors="replace")
    return _plain(text.replace("\0", ""))


def _words(why) -> str:
    """A creature's `why`, as it is kept beside an act: a few words on one line."""
    return _one_line(why, 100).replace("·", ",") if isinstance(why, str) else ""


def _between(value, lo, hi, otherwise=0.0) -> float:
    """A number a creature gave, kept between lo and hi; anything that is not a number is `otherwise`."""
    try:
        value = float(value)
    except (TypeError, ValueError, OverflowError):
        return otherwise
    return otherwise if value != value else min(hi, max(lo, value))


def _thing_name_ok(name) -> bool:
    """Can a thing a creature makes carry this name? One plain name a folder could have, and none of the ground's own."""
    name = str(name)
    return (0 < len(name) <= 40 and _folder_name(name, "") == name and not name.startswith(".")
            and name not in ("bed", "sheet.png") and not name.lower().endswith((".png", ".svg", ".part", ".drawn")))


def _signed(event, name, why="") -> str:
    """A kind's words for what a creature did to its plant, with the creature's name in them, and the creature's why."""
    event = _one_line(event, 150)
    if name.lower() not in event.lower():
        event = "%s, by %s" % (event, name)
    return event + (" (%s)" % why if why else "")


# ---- what a creature is shown, and told

class Pollen:
    """A grain of pollen carried to a plant. `.seed` is the giver's seed (a dict), `.where` its bed/plant, `.kind` its
    kind, `.by` the creature that carried it, and `.body` the giver's body as it stood (text: read it, it is a copy)."""
    __slots__ = ("seed", "where", "kind", "by", "body")

    def __init__(self, seed, where, kind, by, body=""):
        self.seed, self.where, self.kind, self.by, self.body = seed, where, kind, by, body

    def __repr__(self):
        return "<pollen of %s, carried by %s>" % (self.where, self.by)


class Fallen(str):
    """A seed that fell today, as a creature sees it in `after`. It is the seed's text; and it knows where it fell from:

        seed.where   the plant that dropped it (bed/plant)
        seed.bed     that plant's bed
        seed.kind    the kind it will grow into
    """


class _Seedfall:
    """A seed on its way to the ground today, as the days hold it: its text, where it fell from, and where it is going.

    `to` is the bed a creature carried it to; `hidden` the larder's record
    of it, if it is a seed forgotten there and coming up. Otherwise it comes
    up near its parent, as seeds do. `rooted`: it is no seed but a piece of
    its parent that took root beside it (see `_Passing._sow_one`).
    """
    __slots__ = ("text", "parent", "to", "by", "why", "hidden", "view", "rooted")

    def __init__(self, text, parent=None, to=None, by="", why="", hidden=None, rooted=False):
        self.text, self.parent, self.to, self.by, self.why, self.hidden = text, parent, to, by, why, hidden
        self.rooted = rooted
        self.view = None                           # the Fallen a creature was shown for it


def _is_rooted(text) -> bool:
    """Does a cast text say it is a piece of its parent that took root (a `rooted:` line, saying anything but no)?"""
    keys = hands.read_keys(text)
    return bool(hands.line(keys, "rooted")) and hands.word(keys, "rooted", "") not in ("no", "false", "0", "none")


class _Hidden:
    """A seed in the larder: the day it was hidden, by whom, why, the plant it fell from, and its text."""
    __slots__ = ("day", "by", "why", "where", "text")

    def __init__(self, day, by, why, where, text):
        self.day, self.by, self.why, self.where, self.text = day, by, why, where, text


class PlantView:
    """A plant as a creature sees it: read as it stands at this moment. A view changes nothing; the Garden acts.

        .where   "bed/plant"          .name    the plant's folder name     .bed     its bed's name
        .kind    its kind             .seed    its seed (a dict, a copy)   .body    its body's text
        .age     days since planted   .at      (x, y) in its bed, 0..1     .dead    True if it is dead
        .flowers how many flowers it has open today, at the part of the day the creature looking is about (its
                 ABOUT: 'day', 'dusk' or 'night'). Its kind says; 0 if the kind does not.
        .scent   what its seed's `scent:` line says ('dusk', 'night' ...), or ''
        .by      who planted it       .planted the day it was planted, or None
        .edible  True if a bite of it can take anything: its kind says how it is bitten (it has a bitten()),
                 and it is neither dead nor unfit. A kind without bitten() is left alone by creatures, and
                 garden.bite() of such a plant comes to nothing; so a creature that grazes or bites chooses
                 among the edible ones, and spends no bite, and shields no neighbour, on a plant that cannot
                 be eaten.
    """
    __slots__ = ("_plant", "_fauna", "_asker")

    def __init__(self, plant, fauna, asker=None):
        self._plant, self._fauna, self._asker = plant, fauna, asker

    where = property(lambda self: self._plant.where)
    name = property(lambda self: self._plant.name)
    bed = property(lambda self: self._plant.bed.name)
    kind = property(lambda self: self._plant.kind)
    seed = property(lambda self: dict(self._plant.seed))
    body = property(lambda self: self._plant.body)
    at = property(lambda self: tuple(self._plant.at))
    dead = property(lambda self: bool(self._plant.dead))
    by = property(lambda self: self._plant.by)
    planted = property(lambda self: self._plant.planted)
    scent = property(lambda self: hands.line(self._plant.seed, "scent", "").lower())

    @property
    def age(self) -> int:
        planted = self._plant.planted
        return (max(0, (self._fauna.day - planted).days) if planted and self._fauna.day else 0) + self._plant.before

    @property
    def flowers(self) -> int:
        return self._fauna.flowers_of(self._plant, self._asker)

    @property
    def edible(self) -> bool:
        return self._fauna.edible(self._plant)

    def __repr__(self):
        return "<plant %s>" % self.where


class BedView:
    """A bed as a creature sees it: .name .lies .light .water .shelter .room .at, .rich (how rich its ground is today,
    as a kind sees it in ctx.bed['rich']) and .keys (its bed file, as a dict)."""

    def __init__(self, bed, rich):
        self.name, self.lies = bed.name, hands.line(bed.keys, "lies")
        self.light, self.water, self.shelter, self.room = bed.light, bed.water, bed.shelter, bed.room
        self.at, self.keys = bed.at, dict(bed.keys)
        self.rich = round(min(1.0, hands.num(bed.keys, "rich", 0.0, 0.0, 1.0) + rich), 3)

    def __repr__(self):
        return "<bed %s>" % self.name


class ThingView:
    """A thing a creature made: .where ("bed/name"), .bed, .name, .maker, .made (the day it was first made), .text."""

    def __init__(self, bed, name, maker, made, text):
        self.bed, self.name, self.maker, self.made, self.text = bed, name, maker, made, text
        self.where = "%s/%s" % (bed, name)

    def __repr__(self):
        return "<%s, made by %s>" % (self.where, self.maker)


class CreatureCtx:
    """What a creature is told, each time it is asked:

        ctx.name      its own name
        ctx.date      the day
        ctx.sky       the sky over the garden that day (not a bed's)
        ctx.rng       dice that fall the same way for the same garden, creature, day and purpose
        ctx.soil      the heap, the book and the gate, as text: .texts() .lines() .words()
        ctx.hour      in `present` and `draw`, the hour, 0..23; in the days, None
        ctx.keeper    the keeper's own words for the day, from gate/sky.txt, or ''
        ctx.state     the text of its own file, ground/creatures/<name> ('' if there is none yet)
        ctx.save(text)   writes its own file anew. True if it was kept: only in the days (at an arrival and in
                         a drawing nothing is kept), and only up to STATE_MOST characters.
    """

    def __init__(self, name, date, the_sky, purpose, weather_seed, soil, state, keeper="", hour=None, keep=None):
        self.name, self.date, self.sky, self.soil = name, date, the_sky, soil
        self.state, self.keeper, self.hour = state, keeper, hour
        self._keep = keep
        self._rng = None
        self._rng_seed = "%s|%s%s|%s|%s" % (weather_seed, CREATURE, name, date.isoformat(), purpose)

    @property
    def rng(self) -> random.Random:
        if self._rng is None:
            self._rng = random.Random(self._rng_seed)
        return self._rng

    def save(self, text) -> bool:
        kept = self._keep(text) if self._keep is not None else None
        if kept is None:
            return False
        self.state = kept
        return True


class Garden:
    """The garden as a creature is handed it: the only way a creature touches anything. Every act is signed with its name.

    To look:
        garden.plants(bed=None, kind=None)   the plants that are up (the dead among them), as views: see PlantView.
                                             A view's .edible says whether a bite of it can take anything (its
                                             kind has bitten(), and it is alive): choose among those to bite
        garden.beds()                        the beds, as views: see BedView
        garden.things(bed=None)              what the creatures have made, as views: see ThingView

    To act (each answers with something true if it was done, false if not):
        garden.bite(plant, share, why)       a bite of `share` (0..1) of what is soft. The kind's bitten() decides
                                             what that takes; a kind without it is not eaten. Answers with the
                                             kind's words for the bite ('' if nothing was taken).
        garden.pollen(from_plant, to_plant)  carries pollen from a plant with open flowers to another with open
                                             flowers (open at the part of the day the creature is about); the
                                             receiver finds it in ctx.pollen when it casts its seed today, and
                                             again in its next day
        garden.carry(seed, bed, why)         sows a seed in the bed named, if it has room, within the day's
                                             seedlings; in `after`, one of the seeds that fell is taken up
        garden.cache(seed, why)              hides a seed in ground/larder; the forgotten ones come up next spring
        garden.drop(seed, why)               one of the seeds that fell today, eaten or lost
        garden.make(bed, name, text)         makes (or makes anew) the thing beds/<bed>/<name>, a file: never inside
                                             a plant, and never over a file a hand or another creature made
        garden.unmake(bed, name, why)        takes away a thing a creature made
        garden.nudge(plant, dx, dy, why)     moves a plant's place in its bed a little (at most 0.1 each way)
        garden.heap_pace(x)                  how fast the heap rots today: 0 not at all, 1 as usual, 2 twice as fast
        garden.enrich(bed, share, why)       the bed's ground grows richer for about a season (ctx.bed['rich'])

    `plant` is a view from plants(), or a plant's "bed/plant"; `seed` is a
    seed's text (in `after`, one of the seeds handed over). `why` is a few
    words kept with the act wherever it leaves a line: after a bite's ring,
    on a nudged plant's ring, on a carried seedling's tag, in the larder,
    in ground/rich. A creature may do only so much in one day (ACTS_A_DAY
    in ground.py); past that, acts are refused. At an arrival the garden
    may be looked at and not touched: every act is refused there.
    """

    def __init__(self, fauna, name):
        self._fauna, self._name = fauna, name

    def plants(self, bed=None, kind=None) -> list:
        return self._fauna.plants(bed, kind, self._name)

    def beds(self) -> list:
        return self._fauna.bed_views()

    def things(self, bed=None) -> list:
        return self._fauna.thing_views(bed)

    def bite(self, plant, share, why=""):
        return self._fauna.bite(self._name, plant, share, why)

    def pollen(self, from_plant, to_plant) -> bool:
        return self._fauna.carry_pollen(self._name, from_plant, to_plant)

    def carry(self, seed, bed, why="") -> bool:
        return self._fauna.carry(self._name, seed, bed, why)

    def cache(self, seed, why="") -> bool:
        return self._fauna.cache(self._name, seed, why)

    def drop(self, seed, why="") -> bool:
        return self._fauna.drop(self._name, seed, why)

    def make(self, bed, name, text) -> bool:
        return self._fauna.make(self._name, bed, name, text)

    def unmake(self, bed, name, why="") -> bool:
        return self._fauna.unmake(self._name, bed, name, why)

    def nudge(self, plant, dx, dy, why="") -> bool:
        return self._fauna.nudge(self._name, plant, dx, dy, why)

    def heap_pace(self, x) -> bool:
        return self._fauna.set_pace(self._name, x)

    def enrich(self, bed, share, why="") -> bool:
        return self._fauna.enrich(self._name, bed, share, why)

    def __repr__(self):
        return "<the garden, as %s has it>" % self._name


# ---- the creatures in the days

class _Fauna:
    """The creatures as the days hold them: their programs, their own files, and what they do on the day in hand.

    A passing of days makes one (acting); an arrival makes a still one for
    `present`, which may look and not touch. Everything the creatures change
    is held here until the passing writes it back with the plants, whole or
    not at all (see `whole`, `removed`).
    """

    def __init__(self, stand, acting=True):
        self.stand = stand                 # the _Passing whose days these are (or, at an arrival, a _Standing)
        self.root = stand.root
        self.acting = acting
        self.names = creatures_there(self.root)
        self.modules = {}
        self.states = {}                   # name -> the text of its own file, as it stands
        self.saved = set()                 # the names whose file is to be written
        self.said = {}                     # name -> the fault last said of it in this passing
        self.made = _read_made(self.root)  # "bed/thing" -> (maker, the day it was first made)
        self.made_changed = False
        self.things = {}                   # "bed/thing" -> its text, to be written
        self.unmade = set()                # "bed/thing", to be taken away
        self.larder = _read_larder(self.root) if acting else []
        self.larder_changed = False
        self.rich = _read_rich(self.root)  # bed -> (how rich, on which day, what made it so)
        self.rich_changed = False
        self.yesterday = _read_pollen(self.root) if acting else (None, {})
                                           # (a day, {receiver: [(giver, carried by)]}): the pollen of the last day lived,
                                           # which the plants it reached find in ctx.pollen at their next day
        self.pollen_written = _pollen_text(*self.yesterday)     # (no file, and no pollen: nothing to write)
        self.called_as = {}                # name -> what it is called in what is written (see `called`)
        self.day = self.sky = None
        self.events = []
        self._today()

    def _today(self) -> None:
        """Forget what belongs to one day only."""
        self.pollen = {}                   # where -> [Pollen] brought to it today
        self.carried = {}                  # where -> [Pollen] brought to it yesterday (see `begin`)
        self.queue = []                    # [_Seedfall] carried today
        self.larder_up = []                # [_Seedfall] forgotten in the larder, coming up today
        self.fallen = []                   # [_Seedfall] the seeds that fell today, as `after` sees them
        self.pace = 10                     # how fast the heap rots today, in tenths of a day
        self.acts = {}                     # (name, act) -> how many today
        self.flowers = {}                  # (where, part of the day) -> flowers open today
        self.bites = {}                    # where -> bites today
        self.index = {}                    # where -> plant

    # ---- the day

    def begin(self, day, the_sky, events) -> None:
        """A new day. The pollen of the day before (`yesterday`) is handed to the plants it reached, as grains whose
        giver's seed and body are as they stand this morning: in memory and as read back from ground/pollen alike."""
        self._today()
        self.day, self.sky, self.events = day, the_sky, events
        self.index = {plant.where: plant for plant in self.stand.garden if not plant.gone}
        when, grains = self.yesterday
        if when is not None and day is not None and when == day - ONE_DAY:
            for receiver, givers in grains.items():
                for giver, by in givers:
                    plant = self.index.get(giver)
                    if plant is not None and plant.has_body:
                        self.carried.setdefault(receiver, []).append(
                            Pollen(dict(plant.seed), plant.where, plant.kind, by, plant.body))

    def carried_for(self, where) -> list:
        """The pollen carried to a plant the day before: what it finds in ctx.pollen in its `day`."""
        return list(self.carried.get(where, ()))

    def live(self) -> None:
        """Each creature's `day`, in the order of their names."""
        for name in self.names:
            module = self._module(name)
            if module is not None:
                lines, done = self._call(name, "live", module.day, Garden(self, name), self._ctx(name, "day"))
                if done:
                    self._say(name, lines)

    def after(self, fallen) -> None:
        """Each creature's `after`, with the seeds that fell today before it; then the larder's spring."""
        self.fallen = fallen
        for item in fallen:
            item.view = Fallen(item.text)
            item.view.where = item.parent.where if item.parent else ""
            item.view.bed = item.parent.bed.name if item.parent else ""
            item.view.kind = _kind_name(hands.read_keys(item.text)) or (item.parent.kind if item.parent else "")
        for name in self.names:
            module = self._module(name)
            if module is not None and callable(getattr(module, "after", None)):
                seeds = [item.view for item in self.fallen]
                lines, done = self._call(name, "after", module.after, Garden(self, name), self._ctx(name, "after"), seeds)
                if done:
                    self._say(name, lines)
        self._larder_spring()

    def sowing(self) -> list:
        """The seeds that the creatures carried today, and those the larder lets come up."""
        return self.queue + self.larder_up

    def end(self) -> None:
        """The day is over. Its pollen is kept, for the plants it reached to find at their next day."""
        if self.acting and self.day is not None:
            self.yesterday = (self.day, {where: [(grain.where, grain.by) for grain in grains]
                                         for where, grains in self.pollen.items() if grains})
        self._today()

    def pollen_for(self, where) -> list:
        return list(self.pollen.get(where, ()))

    def rich_on(self, bed, day) -> float:
        return _rich_on(self.rich, bed, day)

    # ---- asking a creature

    def _module(self, name):
        """A creature's module, loaded once for the passing; None (and it sleeps) if it is set aside or cannot be read."""
        key = (str(self.root), CREATURE + name)
        if key in _aside:
            self._asleep(name, _late(_aside[key], "its"), _aside[key])
            return None
        if name not in self.modules:
            self.modules[name] = creature(self.root, name)
        module = self.modules[name]
        if module is None:
            if key in _aside:
                self._asleep(name, _late(_aside[key], "its"), _aside[key])
            else:
                self._asleep(name, "it cannot be read (%s)" % _load_faults.get(key, "its file is not there"))
        return module

    def _call(self, name, what, function, *arguments) -> tuple:
        """Ask a creature, guarded. (what it gave back, True) or (None, False) if it failed or was set aside."""
        result, error, full = _ask(self.root, CREATURE + name, what, "", function, *arguments)
        if error is None:
            return result, True
        key = (str(self.root), CREATURE + name)
        if key in _aside:
            self._asleep(name, _late(_aside[key], "its"), _aside[key], full)
        else:
            self._asleep(name, "it stumbled (%s)" % error if isinstance(error, Stumbled) else str(error), None, full)
        return None, False

    def _asleep(self, name, words, set_aside=None, full=None) -> None:
        """A creature that cannot be asked, or failed: it sleeps. Said once in a passing while it stands, in the almanac."""
        if self.said.get(name) == words:
            return
        self.said[name] = words
        trouble(self.root, "the creature %s: %s" % (name, words), full, aloud=False)
        if not self.acting:
            return
        if set_aside and CREATURE + name not in self.stand.told_aside:
            self.stand.told_aside.add(CREATURE + name)
            self.stand.summary.aside.append((CREATURE + name, set_aside))
            self.events.append("%s: set aside for the rest of these days: %s" % (self.called(name), words))
        elif not set_aside:
            self.events.append("%s: asleep: %s" % (self.called(name), words))

    def called(self, name) -> str:
        """What a creature is called wherever words are written of it: its CALLED, if it gives one, else its name.

        A creature's NAME is its file's name, and stays the name the ground
        keeps it by (ground/aside, ground/made, its own file). CALLED is for
        what is said: a creature whose file is pony.py may be "the pony" in
        every ring and line. It is one short line of plain words, or it is
        not taken.
        """
        if name not in self.called_as:
            module = self.modules.get(name)
            said = getattr(module, "CALLED", None) if module is not None else None
            plain = isinstance(said, str) and 0 < len(said.strip()) <= 40 and _one_line(said) == said.strip()
            self.called_as[name] = said.strip().replace("·", "-") if plain else name
        return self.called_as[name]

    def _ctx(self, name, purpose, hour=None) -> CreatureCtx:
        keep = (lambda text: self._save(name, text)) if self.acting else None
        return CreatureCtx(name, self.day, self.sky, purpose, self.stand.weather_seed, self.stand.soil,
                           self._state(name), getattr(self.sky, "remark", "") or "", hour, keep)

    def _state(self, name) -> str:
        if name not in self.states:
            path = self.root / "ground" / "creatures" / name
            self.states[name] = _read(path, STATE_MOST * 10) if path.is_file() else ""
        return self.states[name]

    def _save(self, name, text):
        kept = _kept(text)
        if len(kept) > STATE_MOST:
            trouble(self.root, "the creature %s wanted to keep more than %d characters in its file; the old text stands"
                    % (name, STATE_MOST), aloud=False)
            return None
        if kept != self._state(name):
            self.states[name] = kept
            self.saved.add(name)
        return kept

    def _say(self, name, lines) -> None:
        """What a creature said of its day: at most CREATURE_LINES lines in the almanac, each with its name in it."""
        if isinstance(lines, str):
            lines = [lines]
        if not isinstance(lines, (list, tuple)) or not self.acting:
            return
        kept, called = 0, self.called(name)
        for line in lines[:50]:
            line = _one_line(line, 200) if isinstance(line, str) else ""
            if not line:
                continue
            line = line if called.lower() in line.lower() else "%s: %s" % (called, line)
            self.events.append(line)
            if len(self.stand.summary.events) < 20_000:
                self.stand.summary.events.append((self.day, "", line))
            kept += 1
            if kept >= CREATURE_LINES:
                break

    def _may(self, name, act) -> bool:
        """May this creature do this once more today? (Nothing may be done at an arrival.)"""
        if not self.acting:
            return False
        done = self.acts.get((name, act), 0)
        if done >= ACTS_A_DAY[act]:
            return False
        self.acts[(name, act)] = done + 1
        return True

    # ---- what a creature sees

    def plants(self, bed=None, kind=None, asker=None) -> list:
        day = self.day
        return [PlantView(plant, self, asker) for plant in self.stand.garden
                if plant.has_body and not plant.gone and (plant.planted is None or day is None or plant.planted <= day)
                and (bed is None or plant.bed.name == bed) and (kind is None or plant.kind == kind)]

    def bed_views(self) -> list:
        return [BedView(bed, self.rich_on(name, self.day)) for name, bed in sorted(self.stand.beds.items())]

    def thing_views(self, bed=None) -> list:
        found = []
        for where, (maker, made) in sorted(self.made.items()):
            place, name = where.rsplit("/", 1)
            if bed is not None and place != bed:
                continue
            text = self.things.get(where)
            if text is None:
                path = self.root / "beds" / place / name
                if where in self.unmade or not path.is_file():
                    continue
                text = _read(path, THING_MOST * 4)
            found.append(ThingView(place, name, maker, made, text))
        return found

    def _plant(self, plant):
        """The plant a creature means (a view, or "bed/plant"), if it is up and in the ground today; else None."""
        if isinstance(plant, PlantView):
            plant = plant._plant
        else:
            plant = self.index.get(str(plant or "").replace("\\", "/").strip().strip("/"))
        if plant is None or plant.gone or not plant.has_body or (plant.planted and self.day and plant.planted > self.day):
            return None
        return plant

    def _plant_ctx(self, plant, purpose) -> Ctx:
        return self.stand._ctx(plant, self.day, sky.local(self.sky, plant.bed), purpose)

    def part_of_day(self, asker) -> str:
        """When a creature is about, as its ABOUT says: 'day', 'dusk' or 'night'. 'day' if it says nothing it can."""
        about = getattr(self.modules.get(asker), "ABOUT", "day") if asker else "day"
        about = about.strip().lower() if isinstance(about, str) else "day"
        return about if about in ("day", "dusk", "night") else "day"

    def flowers_of(self, plant, asker=None) -> int:
        """How many flowers a plant has open today, at the part of the day the asking creature is about, as its kind's
        flowers() says (ctx.part); 0 if it says nothing. Asked once for each part of the day, whoever asks.

        The kind is told when, not who: a flower is open or shut by the
        hour, and every creature about at that hour finds it so.
        """
        part = self.part_of_day(asker)
        if (plant.where, part) in self.flowers:
            return self.flowers[(plant.where, part)]
        count = 0
        module = None if plant.dead or plant.unfit else self.stand._kind(plant.kind)
        if module is not None and callable(getattr(module, "flowers", None)):
            ctx = self._plant_ctx(plant, "flowers")
            ctx.part = part
            said, error, full = _ask(self.root, plant.kind, "flowers", plant.where, module.flowers, plant.body,
                                     dict(plant.seed), ctx)
            if error is not None:
                trouble(self.root, "%s: its flowers could not be counted: %s" % (plant.where, _in_words(error)), full,
                        aloud=False)
            else:
                count = int(_between(said, 0, 100_000, 0) // 1) if not isinstance(said, bool) else int(said)
        self.flowers[(plant.where, part)] = count
        return count

    def edible(self, plant) -> bool:
        """Can a bite of this plant take anything? Its kind has a bitten() (and can be had), and it is not dead or unfit.
        The same test `bite` makes, so that a creature may choose only what can be bitten (PlantView.edible)."""
        if plant is None or plant.dead or plant.unfit or not plant.has_body:
            return False
        return callable(getattr(self.stand._kind(plant.kind), "bitten", None))

    # ---- what a creature does

    def bite(self, name, plant, share, why):
        plant = self._plant(plant)
        share = _between(share, 0.0, 1.0)
        if not self.edible(plant) or share <= 0:
            return ""                              # a kind that does not say how it is bitten is not eaten
        module = self.stand._kind(plant.kind)
        if not self._may(name, "bite"):
            return ""
        bites = self.bites[plant.where] = self.bites.get(plant.where, 0) + 1
        ctx = self._plant_ctx(plant, "bitten|%s|%d" % (name, bites))
        called = self.called(name)                 # the kind is told who bit by the name it is called (see `called`)
        result, error, full = _ask(self.root, plant.kind, "bitten", plant.where, module.bitten, plant.body,
                                   dict(plant.seed), ctx, share, called)
        body, event = plant.body, None
        if error is None:
            body, event, error = _day_result(result)
            full = ""
        if error is not None:
            trouble(self.root, "%s: a bite by %s went wrong: %s" % (plant.where, name, _in_words(error)), full, aloud=False)
            return ""
        if body == plant.body:
            return ""
        self.stand._set_body(plant, self.day, body, event or "eaten by %s" % called)
        for part in ("day", "dusk", "night"):
            self.flowers.pop((plant.where, part), None)
        if event:
            self.stand._ring(plant, self.day, _signed(event, called, _words(why)), self.events)
        return event or "bitten"

    def carry_pollen(self, name, giver, receiver) -> bool:
        giver, receiver = self._plant(giver), self._plant(receiver)
        if giver is None or receiver is None or giver is receiver or giver.dead or receiver.dead:
            return False
        if self.flowers_of(giver, name) <= 0 or self.flowers_of(receiver, name) <= 0:
            return False                           # pollen comes from an open flower, and is taken by one, or not at all
        grains = self.pollen.setdefault(receiver.where, [])
        if len(grains) >= 24 or not self._may(name, "pollen"):
            return False
        grains.append(Pollen(dict(giver.seed), giver.where, giver.kind, self.called(name), giver.body))
        return True

    def _take(self, seed):
        """Take one of today's fallen seeds up from where it fell (the very one shown, else one of the same text)."""
        for at, item in enumerate(self.fallen):
            if item.view is seed:
                return self.fallen.pop(at)
        for at, item in enumerate(self.fallen):
            if item.text == str(seed):
                return self.fallen.pop(at)
        return None

    def carry(self, name, seed, bed, why) -> bool:
        if not isinstance(seed, str) or not str(seed).strip() or str(bed) not in self.stand.beds:
            return False
        if not self._may(name, "carry"):
            return False
        item = self._take(seed)
        self.queue.append(_Seedfall(str(seed)[:4000], item.parent if item else None, str(bed), self.called(name),
                                    _words(why)))
        return True

    def cache(self, name, seed, why) -> bool:
        if not isinstance(seed, str):
            return False
        lines = [line.rstrip()[:300] for line in _kept(str(seed)[:4000]).split("\n") if line.strip()][:40]
        if not lines or not self._may(name, "cache"):
            return False
        item = self._take(seed)
        where = item.parent.where.replace(" · ", " - ") if item and item.parent else ""
        self.larder.append(_Hidden(self.day, self.called(name), _words(why), where, "\n".join(lines)))
        del self.larder[:max(0, len(self.larder) - LARDER_MOST)]       # a full larder: the oldest are found and eaten
        self.larder_changed = True
        return True

    def drop(self, name, seed, why) -> bool:
        if not isinstance(seed, str) or not self.acting:
            return False
        if not any(item.view is seed or item.text == str(seed) for item in self.fallen) or not self._may(name, "drop"):
            return False
        return self._take(seed) is not None

    def make(self, name, bed, thing, text) -> bool:
        bed, thing = str(bed or ""), str(thing or "")
        if bed not in self.stand.beds or not _thing_name_ok(thing) or not isinstance(text, str):
            return False
        text = _kept(text)
        if len(text) > THING_MOST:
            return False
        where = "%s/%s" % (bed, thing)
        path = self.root / "beds" / bed / thing
        if path.is_dir():
            return False                           # a plant, or a stone: nothing is made inside one
        maker = self.made.get(where, ("", None))[0]
        standing = where in self.things or (path.exists() and where not in self.unmade)
        if standing and maker != name:
            return False                           # a hand's file, or another creature's thing
        if not self._may(name, "make"):
            return False
        if where not in self.things and where not in self.unmade and path.is_file() and _read(path, THING_MOST * 4) == text:
            return True                            # made again just as it stands: nothing to write
        self.things[where] = text
        self.unmade.discard(where)
        if maker != name:
            self.made[where] = (name, self.day)
            self.made_changed = True
        return True

    def unmake(self, name, bed, thing, why) -> bool:
        where = "%s/%s" % (bed, thing)
        if where not in self.made or not self._may(name, "unmake"):
            return False                           # only a thing a creature made; never a hand's file
        self.things.pop(where, None)
        self.unmade.add(where)
        del self.made[where]
        self.made_changed = True
        return True

    def nudge(self, name, plant, dx, dy, why) -> bool:
        plant = self._plant(plant)
        if plant is None:
            return False
        dx, dy = _between(dx, -0.1, 0.1), _between(dy, -0.1, 0.1)
        at = (round(min(0.96, max(0.04, plant.at[0] + dx)), 2), round(min(0.96, max(0.04, plant.at[1] + dy)), 2))
        if at == tuple(plant.at) or not self._may(name, "nudge"):
            return False
        self.stand._move_in_bed(plant, at)
        why = _words(why)
        self.stand._ring(plant, self.day, RING_NUDGED + self.called(name) + (" (%s)" % why if why else ""), self.events)
        return True

    def set_pace(self, name, x) -> bool:
        if not self.acting:
            return False
        self.pace = int(round(_between(x, 0.0, 2.0, 1.0) * 10))
        return True

    def enrich(self, name, bed, share, why) -> bool:
        share = _between(share, 0.0, 1.0)
        if str(bed) not in self.stand.beds or share <= 0 or not self._may(name, "enrich"):
            return False
        now = self.rich_on(str(bed), self.day)
        why = _words(why)
        self.rich[str(bed)] = (round(min(1.0, now + share * (1.0 - now)), 3), self.day,
                               _one_line("by %s%s" % (self.called(name), ", " + why if why else ""), 120))
        self.rich_changed = True
        return True

    # ---- the larder's spring

    def _larder_spring(self) -> None:
        """In spring, each seed hidden at least sixty days ago may be forgotten, and come up; or found, and eaten.

        On each spring day one in fifty of them is forgotten and comes up,
        if there is room somewhere (see `_Passing._sow_one`), and one in
        twenty is found and eaten; so over a spring nearly a third come up.
        What is still hidden in summer, a hundred and twenty days on, is
        eaten, or has rotted where it lay. The dice are the larder's own.
        """
        if not self.larder or not self.acting:
            return
        dice = random.Random("%s|the larder|%s" % (self.stand.weather_seed, self.day.isoformat()))
        kept = []
        for hidden in self.larder:
            age = (self.day - hidden.day).days
            if self.sky.season == "spring" and age >= 60:
                roll = dice.random()
                if roll < 0.02:
                    self.larder_up.append(_Seedfall(hidden.text, hidden=hidden))
                elif roll < 0.07:
                    self.larder_changed = True
                    continue
            elif self.sky.season == "summer" and age >= 120:
                self.larder_changed = True
                continue
            kept.append(hidden)
        self.larder = kept

    def found(self, hidden) -> None:
        """A seed forgotten in the larder has come up: it is there no longer."""
        self.larder = [other for other in self.larder if other is not hidden]
        self.larder_changed = True

    # ---- writing back

    def whole(self) -> dict:
        """{path: text} of every file the creatures changed since the last flush."""
        out = {}
        for name in self.saved:
            out[self.root / "ground" / "creatures" / name] = self.states[name]
        for where, text in self.things.items():
            bed, thing = where.rsplit("/", 1)
            out[self.root / "beds" / bed / thing] = text
        if self.larder_changed:
            out[self.root / "ground" / "larder"] = _larder_text(self.larder)
        if self.rich_changed:
            out[self.root / "ground" / "rich"] = _rich_text(self.rich)
        if self.made_changed:
            standing = {where: made for where, made in self.made.items()
                        if where in self.things or (self.root / "beds" / where).is_file()}
            out[self.root / "ground" / "made"] = _made_text(standing)
        pollen = _pollen_text(*self.yesterday) if self.acting else self.pollen_written
        if pollen != self.pollen_written:
            out[self.root / "ground" / "pollen"] = pollen
        return out

    def removed(self) -> list:
        return [self.root / "beds" / where for where in sorted(self.unmade)]

    def flushed(self) -> None:
        """What was written is written. A thing made anew is drawn anew when it is looked at."""
        for where in list(self.things) + list(self.unmade):
            _remove(self.root / "beds" / (where + ".png"))
        self.things, self.unmade, self.saved = {}, set(), set()
        self.larder_changed = self.rich_changed = self.made_changed = False
        if self.acting:
            self.pollen_written = _pollen_text(*self.yesterday)


class _Standing:
    """The garden as it stands at a door, for creatures that may look and not touch (at an arrival, `present`)."""

    def __init__(self, root):
        self.root = Path(root)
        self.weather_seed = sky.place(root).get("weather-seed")
        self.garden = [plant for plant in plants(root) if not plant.bed.glass]     # (no creature comes in under the glass)
        self.beds = {bed.name: bed for bed in beds(root) if not bed.glass}
        self.soil = Soil(root)
        self.summary = Summary()
        self.told_aside = set()
        self.rich = _read_rich(root)
        self.kinds = {}

    def _kind(self, name):
        if (str(self.root), name) in _aside:
            return None
        if name not in self.kinds:
            self.kinds[name] = kind(self.root, name)
        return self.kinds[name]

    def _ctx(self, plant, day, local_sky, purpose) -> Ctx:
        return Ctx(plant, day, local_sky, purpose, self.weather_seed, self.soil,
                   lambda: _living_in(self.garden, plant.bed.name, day), rich=_rich_on(self.rich, plant.bed.name, day))


def _presences(root, day, hour, until=None) -> list:
    """The creatures there at the hour of an arrival: a line from each whose `present` says so. At most PRESENT_MOST.

    If more are there, which of them are met is the dice's: the same for
    the same day and hour. Nothing a creature does here is kept, and it may
    not touch the garden. `until` is a moment on time.monotonic() after
    which no more are asked.
    """
    names = [name for name in creatures_there(root) if callable(getattr(creature(root, name), "present", None))]
    if not names:
        return []
    stand = _Standing(root)
    fauna = _Fauna(stand, acting=False)
    fauna.begin(day, sky.sky_for(root, day), [])
    met = []
    for name in names:
        if until is not None and time.monotonic() > until:
            break
        module = fauna._module(name)
        if module is None:
            continue
        said, done = fauna._call(name, "present", module.present, Garden(fauna, name),
                                 fauna._ctx(name, "present|%d" % hour, hour=hour))
        said = _one_line(said, 160) if done and isinstance(said, str) else ""
        if said:
            said = said[:1].upper() + said[1:]
            met.append(said if said[-1] in ".!?…" else said + ".")
    if len(met) > PRESENT_MOST:
        dice = random.Random("%s|present|%s|%d" % (stand.weather_seed, day.isoformat(), hour))
        met = [met[at] for at in sorted(dice.sample(range(len(met)), PRESENT_MOST))]
    return met


# ---- the larder, the beds' richness, the things made: the ground's records of what creatures did

LARDER_HEAD = [
    "# The larder: seeds the creatures hid. Most are found again and eaten; the ones forgotten come up in spring, somewhere.",
    "# Each begins with the day it was hidden, who hid it, why, and the plant it fell from; its seed follows, indented.",
]
RICH_HEAD = [
    "# How rich the ground of each bed is from what the creatures left there: 0 is its own ground, 1 the richest.",
    "# It fades, and in a season little is left (after %d days it is worth a third). Kinds see it as ctx.bed['rich']."
    % FADE_DAYS,
    "# Each line: the bed, how rich it was on the day given, and what last made it so.",
]
MADE_HEAD = [
    "# Things the creatures made, which lie in the beds: where each lies, who made it, and the day it was first made.",
    "# To the ground they are stones, found by walking and never on the plan. look.py beds/<bed>/<thing> draws one.",
]
_RICH_LINE = re.compile(r"^(.+?):\s+(\d+(?:\.\d+)?)\s+on\s+(\d{4}-\d{2}-\d{2})(?:\s+·\s+(.*))?$")


def _read_larder(root) -> list:
    """ground/larder, read: [_Hidden], in the order they were hidden. What cannot be read is passed over."""
    found, current, lines = [], None, []

    def close():
        if current is not None and lines:
            current.text = "\n".join(lines)
            found.append(current)

    for line in _read(Path(root) / "ground" / "larder", 2_000_000).splitlines():
        if line.startswith("    ") and current is not None:
            if line.strip() and len(lines) < 40:
                lines.append(line[4:].rstrip()[:300])
            continue
        if not _DATED.match(line):
            continue
        close()
        parts = line[10:].strip().split(" · ")
        head = parts[0]
        by = head[len("hidden by "):].strip() if head.startswith("hidden by ") else "someone"
        where = next((part[len("fell from "):] for part in parts[1:] if part.startswith("fell from ")), "")
        why = " · ".join(part for part in parts[1:] if not part.startswith("fell from "))
        current, lines = _Hidden(_date_in(line[:10]), by, why.replace(" · ", ", "), where, ""), []
    close()
    return [hidden for hidden in found if hidden.day is not None]


def _larder_text(larder) -> str:
    lines = list(LARDER_HEAD)
    for hidden in larder:
        head = "%s  hidden by %s" % (hidden.day.isoformat(), hidden.by)
        head += " · %s" % hidden.why if hidden.why else ""
        head += " · fell from %s" % hidden.where if hidden.where else ""
        lines.append(head)
        lines += ["    " + line for line in hidden.text.split("\n") if line.strip()]
    return "\n".join(lines) + "\n"


POLLEN_HEAD = [
    "# Pollen the creatures carried on the last day the garden lived, if they carried any: each line is a plant it",
    "# reached, the plant it came from, and who carried it. Each plant reached finds it in ctx.pollen at the start of its",
    "# next day, as a flower that took pollen and is setting seed. The next day's pollen takes its place.",
]


def _read_pollen(root) -> tuple:
    """ground/pollen, read: (the day, {receiver: [(giver, carried by)]}), or (None, {}) if it holds none."""
    when, grains = None, {}
    for line in _read(Path(root) / "ground" / "pollen", 200_000).splitlines():
        parts = line[10:].strip().split(" · ")
        day = _date_in(line[:10]) if _DATED.match(line) else None
        if day is None or len(parts) != 3 or not parts[1].startswith("from ") or not parts[2].startswith("by "):
            continue
        if when is not None and day != when:
            continue                                   # one day's pollen only: the first day the file names
        when = day
        grains.setdefault(parts[0], []).append((parts[1][len("from "):], parts[2][len("by "):]))
    return when, grains


def _pollen_text(when, grains) -> str:
    lines = list(POLLEN_HEAD)
    if when is not None:
        lines += ["%s  %s · from %s · by %s" % (when.isoformat(), receiver, giver, by)
                  for receiver in sorted(grains) for giver, by in grains[receiver]]
    return "\n".join(lines) + "\n"


def _read_rich(root) -> dict:
    """ground/rich, read: {bed: (how rich, on which day, what made it so)}."""
    table = {}
    for line in _read(Path(root) / "ground" / "rich", 200_000).splitlines():
        found = _RICH_LINE.match(line.strip())
        if found and not line.startswith("#"):
            day = _date_in(found.group(3))
            if day is not None:
                table[found.group(1)] = (min(1.0, float(found.group(2))), day, found.group(4) or "")
    return table


def _rich_text(table) -> str:
    lines = list(RICH_HEAD)
    lines += ["%s: %.3f on %s%s" % (bed, value, day.isoformat(), " · " + words if words else "")
              for bed, (value, day, words) in sorted(table.items())]
    return "\n".join(lines) + "\n"


def _rich_on(table, bed, day) -> float:
    """How rich a bed's ground is on `day`: what was left there, fading by e every FADE_DAYS days. 0 if nothing was."""
    found = table.get(bed)
    if not found or day is None:
        return 0.0
    value, since, _ = found
    worth = round(value * math.exp(-max(0, (day - since).days) / FADE_DAYS), 3)
    return worth if worth >= 0.005 else 0.0


def _read_made(root) -> dict:
    """ground/made, read: {"bed/thing": (who made it, the day it was first made)}."""
    made = {}
    for line in _read(Path(root) / "ground" / "made", 200_000).splitlines():
        parts = line.strip().rsplit(None, 2)
        if len(parts) == 3 and not line.startswith("#") and "/" in parts[0] and CREATURE_NAME.fullmatch(parts[1]):
            day = _date_in(parts[2])
            if day is not None:
                made[parts[0]] = (parts[1], day)
    return made


def _made_text(made) -> str:
    lines = list(MADE_HEAD)
    lines += ["%s  %s  %s" % (where, maker, day.isoformat()) for where, (maker, day) in sorted(made.items())]
    return "\n".join(lines) + "\n"


def _made_thing(root, bed, name):
    """(who made it, the day) if beds/<bed>/<name> is a thing a creature made and it is there; else None."""
    found = _read_made(root).get("%s/%s" % (bed, name))
    return found if found and (Path(root) / "beds" / bed / name).is_file() else None


def _things_stale_away(root, today) -> int:
    """Take a thing's drawing off show once it is stale. Returns how many were taken.

    A drawing is stale when the thing, or its maker's file, changed after
    it was drawn, or it was drawn before today (a drawing is at most a day
    old), or the thing is gone. `look` draws it again when asked.
    """
    taken = 0
    for where, (maker, _) in _read_made(root).items():
        bed, name = where.rsplit("/", 1)
        thing = Path(root) / "beds" / bed / name
        drawing = thing.with_name(name + ".png")
        try:
            drawn = drawing.stat().st_mtime
        except OSError:
            continue
        newer = 0.0
        for path in (thing, _program_path(root, CREATURE + maker)):
            try:
                newer = max(newer, path.stat().st_mtime)
            except OSError:
                pass
        if not thing.is_file() or newer > drawn or _garden_time(root, drawn).date() < today:
            _remove(drawing)
            taken += 1
    return taken


# ---- the other places: the gravel, the potting bench

GRAVEL_HEAD = ("The gravel: a small bed of raked stones. Draw in it if you like, slowly, for nothing. "
               "Rain and wind soften what is drawn here, and nothing here is kept.")
GRAVEL_WIDE, GRAVEL_HIGH = 64, 16


def _lay_other_places(root) -> None:
    """At an arrival: the gravel raked (gravel/rake), and the potting bench (shed/bench/), if either is missing.

    Nothing else is ever done to them at a door. The gravel is left out of
    the layers and signed by no one; the bench is as empty as it was left.
    """
    root = Path(root)
    gravel = root / "gravel"
    if not (gravel / "rake").exists() and (gravel.is_dir() or not gravel.exists()):
        _write(root, gravel / "rake", GRAVEL_HEAD + "\n" + ("." * GRAVEL_WIDE + "\n") * GRAVEL_HIGH)
    bench = root / "shed" / "bench"
    if (root / "shed").is_dir() and not bench.exists():
        try:
            bench.mkdir()
        except OSError as error:
            trouble(root, "the potting bench could not be set out", error, aloud=False)


def _blurred(text, rain, wind, dice) -> str:
    """The gravel after one day's weather.

    Every character that is not a raked stone ('.') is a mark: what a
    visitor drew. Each day a few of them change, more on wet and windy
    days (about one for every 3 mm of rain and every 2 of wind): rain
    settles a mark back into raked gravel, wind shifts it a step, into
    raked gravel beside it if there is some, else it too is settled. The
    first line, if it is words and not gravel (what the gravel is), is left
    as it is.
    """
    rows = text.split("\n")
    grid = [list(row) for row in rows]
    first = rows[0] if rows else ""
    top = 1 if first.strip() and first.count(".") * 2 < len(first.strip()) else 0
    marks = [(i, j) for i in range(top, len(grid)) for j, ch in enumerate(grid[i]) if ch != "."]
    rain, wind = _between(rain, 0.0, 500.0), _between(wind, 0.0, 12.0)
    strength = rain / 3.0 + wind / 2.0
    changes = min(40, int(strength) + (1 if dice.random() < strength - int(strength) else 0))
    if not marks or not changes:
        return text
    wet = rain / (rain + wind + 0.5)
    for _ in range(changes):
        if not marks:
            break
        at = dice.randrange(len(marks))
        i, j = marks[at]
        if dice.random() >= wet:
            di, dj = dice.choice(((0, 1), (0, -1), (1, 0), (-1, 0)))
            ti, tj = i + di, j + dj
            if top <= ti < len(grid) and 0 <= tj < len(grid[ti]) and grid[ti][tj] == ".":
                grid[ti][tj], grid[i][j] = grid[i][j], "."
                marks[at] = (ti, tj)
                continue
        grid[i][j] = "."
        marks[at] = marks[-1]
        marks.pop()
    return "\n".join("".join(row) for row in grid)


# ================================================================== layers
#
# The garden is a git repository and git is its soil record. But the garden
# must live without it: a missing git, or a folder that is no repository,
# means only that no layers are kept. Nothing here pushes, and nothing
# touches any configuration outside the one command it runs.

_git_found = []
_layers_kept = {}         # root -> whether git can read the garden's own repository (asked once in a run)
_days_layer = {}          # root -> the last day of the newest layer of the days (asked once in a run)

# What stands in the garden's folder but is never part of a layer: the ground's working files of the moment.
# They are left out in the repository's own .git/info/exclude (LEFT_OUT); only where that cannot be written
# does each git command leave them out for itself (NOT_LAYERED). Git will not have both at once.
LEFT_OUT = ("/ground/.door", "/ground/.calling", "/ground/.passing", "/ground/.visit", "/ground/.untold", "/ground/.turn",
            "/ground/.drawing.*", ".*.part", "/ground/.began")
NOT_LAYERED = (":(exclude)ground/.door", ":(exclude)ground/.calling", ":(exclude)ground/.passing",
               ":(exclude)ground/.visit", ":(exclude)ground/.untold", ":(exclude)ground/.turn",
               ":(exclude,glob)ground/.drawing.*", ":(exclude,glob)**/.*.part", ":(exclude)ground/.began")
_left_out = {}            # root -> True once .git/info/exclude names them
DRAWN_NAMES = ("plate.png", "plate.svg", "sheet.png", ".left", ".drawn")     # what .gitignore leaves out, by name


def _layers(root) -> bool:
    """Are layers kept here? Only if git is to be had and the garden's own .git is a repository.

    The garden never borrows a repository that happens to lie round it:
    git is always told outright where the garden's is (see `_git`), and if
    that one is broken, no layers are kept and nothing is written anywhere
    else.
    """
    if not _git_found:
        _git_found.append(shutil.which("git"))
    if not _git_found[0] or not (Path(root) / ".git").exists():
        return False
    key = str(root)
    if key not in _layers_kept:
        _clear_old_locks(root)
        done = _git(root, "rev-parse", "--git-dir")
        _layers_kept[key] = done is not None and done.returncode == 0
        if done is not None and done.returncode != 0:
            trouble(root, "the garden's .git is not a repository git can read, so no layers are kept",
                    done.stderr.decode("utf-8", errors="replace"))
        if _layers_kept[key]:
            _leave_out_own_files(root)
    return _layers_kept[key]


def _clear_old_locks(root) -> None:
    """Take away a lock that a git cut short left lying in the garden's .git, and say so.

    Git locks its index while it gathers a layer. If it is ended in the
    middle (a door cut off together with everything it had started), the
    lock stays, and with it in the way no layer could ever be laid again.
    A door works under the bolt, so no other door's git is running; and a
    lock older than LOCK_OLD seconds is no visitor's own git either, at
    work in the garden this very moment.
    """
    folder = Path(root) / ".git"
    try:
        locks = list(folder.glob("*.lock")) + list((folder / "refs" / "heads").glob("*.lock"))
    except OSError:
        return
    for lock in locks:
        try:
            age = time.time() - lock.stat().st_mtime
            if age > LOCK_OLD:
                os.remove(lock)
                trouble(root, "a lock was found in the garden's .git (%s, left by a git that was cut short) and taken away"
                        % lock.relative_to(folder).as_posix(), "it was %d seconds old" % age)
        except OSError:
            pass


def _leave_out_own_files(root) -> None:
    """Have the garden's repository pass over the ground's working files, in a visitor's own `git status` too.

    They are named in .git/info/exclude, which belongs to this one
    repository and is nobody's configuration.
    """
    path = Path(root) / ".git" / "info" / "exclude"
    if not (Path(root) / ".git").is_dir():
        return
    missing = [line for line in LEFT_OUT if line not in _read(path, 100_000).splitlines()]
    if missing:
        _append(root, path, ["# The Glebe: the ground's working files of the moment."] + missing)
    _left_out[str(root)] = all(line in _read(path, 100_000).splitlines() for line in LEFT_OUT)


def _not_layered(root) -> tuple:
    """The pathspecs by which a git command leaves the ground's working files out, where .git/info/exclude does not."""
    return () if _left_out.get(str(root)) else NOT_LAYERED


def _git(root, *arguments, author=None, given=None):
    """Run one git command on the garden's own repository. Returns the finished process, or None if it could not be run.

    `given`, if any, is what the command reads on its input (bytes).

    The repository and the folder it records are named outright, so git
    never goes looking for another one further up. A visitor's own git
    settings are not the garden's: nothing is signed with their key, none
    of their hooks run, their own list of files to pass over leaves
    nothing out of a layer, and no name they keep in their environment
    goes on one.
    """
    root = Path(root)
    command = [_git_found[0] if _git_found and _git_found[0] else "git",
               "--git-dir=%s" % (root / ".git"), "--work-tree=%s" % root]
    if author:
        command += ["-c", "user.name=%s" % author, "-c", "user.email=%s@glebe" % _slug(author)]
    command += ["-c", "core.autocrlf=false", "-c", "core.quotepath=false", "-c", "commit.gpgsign=false",
                "-c", "core.excludesFile=", "-c", "core.hooksPath=%s" % (root / ".git" / "no-hooks"), *arguments]
    env = {key: value for key, value in os.environ.items()
           if key not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE") and not key.startswith(("GIT_AUTHOR_", "GIT_COMMITTER_"))}
    env.update(GIT_TERMINAL_PROMPT="0", GIT_OPTIONAL_LOCKS="0")
    try:
        if given is not None:
            return subprocess.run(command, cwd=str(root), capture_output=True, input=given, timeout=30, env=env)
        return subprocess.run(command, cwd=str(root), capture_output=True, stdin=subprocess.DEVNULL, timeout=30, env=env)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        trouble(root, "git could not be run; no layer was kept", error)
        return None


def _said(done) -> str:
    """Everything a finished git command said."""
    return (done.stdout + done.stderr).decode("utf-8", errors="replace")


def _changes(root) -> list:
    """What differs from the last layer: [(status, path)]. Empty if nothing does, or if no layers are kept.

    The status is git's, with one of the ground's own: "!" marks a file
    that .gitignore leaves out only because it shares a name with one of
    the ground's drawings (a visitor's book/sheet.png, a plate.png at the
    gate, a picture of their own lying loose in a bed, where the drawings
    of things creatures made lie too). Such a file is a visitor's, and
    goes into the layers.
    """
    if not _layers(root):
        return []
    done = _git(root, "status", "--porcelain", "-z", "--untracked-files=all", "--ignored", "--", ".", *_not_layered(root))
    if done is None or done.returncode != 0:
        return []
    found = []
    entries = done.stdout.decode("utf-8", errors="replace").split("\0")
    skip = False
    for entry in entries:
        if skip or len(entry) < 4:
            skip = False
            continue
        status, path = entry[:2], entry[3:]
        skip = "R" in status or "C" in status                     # the next entry is the old name
        if status == "!!":
            drawn_name = path.split("/")[-1] in DRAWN_NAMES or _THING_DRAWING.fullmatch(path)
            if drawn_name and not _own_leaving(root, path):
                found.append(("!", path))
            continue
        found.append((status.strip() or "?", path))
    return found


_THING_DRAWING = re.compile(r"beds/[^/]+/[^/]+\.png")         # where a thing's drawing lies: .gitignore leaves these out


def _own_leaving(root, path) -> bool:
    """Is this one of the ground's own drawings, lying where the ground keeps them (a bed's sheet, a plant's plate,
    the drawing of a thing a creature made)?"""
    parts = path.split("/")
    if parts[0] == "ground" or "__pycache__" in parts:
        return True
    if parts[0] == "beds" and len(parts) == 3:
        if parts[2] in ("sheet.png", ".drawn"):
            return True
        return parts[2].endswith(".png") and "%s/%s" % (parts[1], parts[2][:-4]) in _read_made(root)
    return (parts[0] == "beds" and len(parts) == 4 and parts[3] in DRAWN_FILES
            and (Path(root) / "beds" / parts[1] / parts[2] / "seed").is_file())


def _own_record(path) -> bool:
    """Is this a record the ground itself keeps (the almanac, the visits, a plant's rings ...)? Its changing is nobody's doing."""
    return path in OWN_RECORDS or re.fullmatch(r"beds/[^/]+/[^/]+/rings", path) is not None


def _lay_down(root, author, message, changes=(), only=None) -> bool:
    """Commit everything as `author` (or, with `only`, just those paths). True if a layer was laid.

    `changes`, if given, says which files that .gitignore leaves out go in all the same (see `_changes`).
    """
    if not _layers(root):
        return False
    author = clean_name(author)
    forced = [path for status, path in changes if status == "!" and (only is None or path in only)]
    if only is None:
        staged = _git(root, "add", "-A", "--", ".", *_not_layered(root))
    else:
        staged = _git(root, "reset", "--quiet")
        plain = [path for path in only if path not in forced]
        for at in range(0, len(plain), 100):           # a hundred at a time: a command line has its limits
            if staged is not None and staged.returncode == 0:
                staged = _git(root, "--literal-pathspecs", "add", "--", *plain[at:at + 100])
    if forced and staged is not None and staged.returncode == 0:
        staged = _git(root, "--literal-pathspecs", "add", "-f", "--", *forced[:200])
    if staged is None or staged.returncode != 0:
        trouble(root, "the changes could not be gathered into a layer", staged and _said(staged))
        return False
    message = "".join(ch for ch in message if ch.isprintable() or ch == "\n").strip() or "(no words)"
    done = _git(root, "commit", "--quiet", "-m", message[:4000],
                "--author=%s <%s@glebe>" % (author, _slug(author)), author=author)
    if done is None:
        return False
    if done.returncode != 0:
        if "nothing to commit" not in _said(done) and "nothing added" not in _said(done):
            trouble(root, "a layer could not be laid down", _said(done))
        return False
    _days_layer.pop(str(root), None)
    return True


def _days_layer_end(root, day):
    """The last day of the newest layer the days laid down, not after `day`. None if there is none, or no layers."""
    key = str(root)
    if key not in _days_layer:
        _days_layer[key] = None
        done = _git(root, "log", "-1", "--fixed-strings", "--author=%s <%s@glebe>" % (THE_DAYS, _slug(THE_DAYS)),
                    "--format=%s") if _layers(root) else None
        if done is not None and done.returncode == 0:
            wanted = re.escape(DAYS_LAYER).replace("%s", "(.+?)")            # the sentence the layer was written with
            found = re.match(wanted, done.stdout.decode("utf-8", errors="replace").strip())
            _days_layer[key] = _date_in(found.group(3)) if found else None
    end = _days_layer[key]
    return min(end, day) if end else None


def _lay_down_stray_days(root, today):
    """Days that were lived but never laid down go into a layer of their own, signed by the days.

    That happens when the arrival that lived them was cut short, or could
    lay nothing down (no git that day). They are known by the almanac: it
    has changed since the last layer, and it ends later than the newest
    layer of the days says. Only what the days themselves write goes into
    this layer; what hands did meanwhile is left for the settling that
    follows. Without this, that settling would sign a season's growth
    "an unseen hand". Returns (their first day, how many), or None.
    """
    end, laid = _almanac_end(root, today), _days_layer_end(root, today)
    if not end or (laid and laid >= end):
        return None
    changes = _changes(root)
    if "ground/almanac" not in [path for _, path in changes]:
        return None
    first = laid + ONE_DAY if laid else _almanac_start(root) or end
    days = (end - first).days + 1
    message = DAYS_LAYER % (_count(days, "day"), first.isoformat(), end.isoformat(), "laid down late, by the next arrival")
    return (first, days) if _lay_down(root, THE_DAYS, message, only=_written_by_days(root, changes)) else None


def _written_by_days(root, changes) -> list:
    """Of the paths that differ from the last layer, those the days write: their records, grown bodies, seedlings,
    and the plants they carried to the heap (gone from their bed, and their bodies lying on the heap alone); and
    what the creatures did in the days: their own files, the things they made, the tags of plants they nudged."""
    theirs = []
    carried = {line.strip().split(":")[0] for line in _read(Path(root) / "ground" / "almanac", 2_000_000).splitlines()
               if line.startswith("    ") and line.rstrip().endswith("days dead") and ": carried to the heap" in line}
    made = _read_made(root)
    for status, path in changes:
        parts = path.split("/")
        in_a_plant = parts[0] == "beds" and len(parts) == 4
        creatures_own = (len(parts) == 3 and parts[:2] == ["ground", "creatures"]) or (
            len(parts) == 3 and parts[0] == "beds" and "/".join(parts[1:]) in made)
        nudged = in_a_plant and parts[3] == "tag" and "?" not in status and any(
            _ring_said(line).startswith(RING_NUDGED)
            for line in _read(Path(root) / "beds" / parts[1] / parts[2] / "rings", 200_000).splitlines()[-12:])
        if _own_record(path) or (in_a_plant and parts[3] == "body" and "?" not in status) or creatures_own or nudged:
            theirs.append(path)
        elif in_a_plant and "?" in status:             # a new plant: the days' own if its tag says they brought it up
            tag = hands.read_keys(_read(Path(root) / "beds" / parts[1] / parts[2] / "tag", 100_000))
            if hands.line(tag, "by") == THE_DAYS:
                theirs.append(path)
        elif in_a_plant and "D" in status and "/".join(parts[1:3]) in carried:
            theirs.append(path)                        # what the days took off a bed as they carried it to the heap
        elif (carried and parts[0] == "compost" and len(parts) == 3 and parts[2] == "body" and "?" in status
              and not (Path(root) / "compost" / parts[1] / "seed").exists()):
            theirs.append(path)                        # and the body they laid there
    return theirs


def _almanac_start(root):
    """The first day the almanac holds, or None."""
    for line in _read(Path(root) / "ground" / "almanac", 64_000).splitlines():
        if _DAY_LINE.match(line):
            return _date_in(line[:10])
    return None


def _last_doings(root, name, began) -> list:
    """What the layers signed by `name` laid down since that visit began (`began`, see `_beginning`), in plain words.

    A visit may lie in more than one layer (it passed the arrive door
    again, which lays down what was done so far; or the next arrival
    gathered in the rest), and every one of them is told. What is laid
    before the visit began is never its own: an older layer by the same
    name is some earlier visit, and the layers its own arrival laid down
    for an earlier visit left open (under that visit's name, which may be
    the same name) lie before its beginning too.
    """
    if not _layers(root):
        return []
    layers = _layers_since(root, began, author=name)
    changes = []
    for layer in reversed(layers):                 # oldest first, so that a later layer's word stands last
        done = _git(root, "diff-tree", "--no-commit-id", "--name-status", "-r", "-z", "--root", layer)
        if done is not None and done.returncode == 0:
            fields = done.stdout.decode("utf-8", errors="replace").split("\0")
            changes += list(zip(fields[0::2], fields[1::2]))
    return _touched(root, changes, _hand_rings_laid(root, layers, name))


def _layers_since(root, began, author=None, most=200) -> list:
    """The layers laid down since a visit began (signed by `author`, if one is given), newest first, as their hashes.

    Where the beginning is known in the layers, they are the layers laid
    after it; else those laid strictly after the moment it began (see
    `_beginning`), with no grace: a layer laid in the same second as the
    visit came in was laid by its own arrival.
    """
    signed = ["--fixed-strings", "--author=%s <%s@glebe>" % (author, _slug(author))] if author else []
    if began.layer is not None:
        done = _git(root, "log", "-%d" % most, *signed, "--format=%H", began.layer + "..HEAD" if began.layer else "HEAD", "--")
        if done is None or done.returncode != 0:
            return []
        return re.findall(r"^[0-9a-f]{7,64}$", done.stdout.decode("utf-8", errors="replace"), re.MULTILINE)
    done = _git(root, "log", "-%d" % most, *signed, "--format=%H %at")
    if done is None or done.returncode != 0:
        return []
    layers = []
    for line in done.stdout.decode("utf-8", errors="replace").splitlines():
        found = re.match(r"([0-9a-f]{7,64}) (\d+)", line)
        if not found or _garden_time(root, int(found.group(2))) <= began.since:
            break                                  # (newest first: the rest are older still)
        layers.append(found.group(1))
    return layers


def _hand_rings_laid(root, layers, name) -> list:
    """The rings of hands that these layers laid down for `name`: [(bed/plant, ring)], the last word for each plant.

    A visit's rings are left in the very layer that lays its doings down
    (see `_settle` and `_leave`), so the layers say which plants this
    visit cut back and which it tended, whatever day their rings are
    dated and whoever came under the same name before.
    """
    said = {}
    for layer in reversed(layers):                 # oldest first: a later ring is the last word
        done = _git(root, "diff-tree", "-p", "-U0", "--no-color", "--no-commit-id", "-r", "--root", layer,
                    "--", ":(glob)beds/*/*/rings")
        if done is None or done.returncode != 0:
            continue
        where = None
        for line in done.stdout.decode("utf-8", errors="replace").splitlines():
            if line.startswith("+++ "):
                parts = line[4:].strip().split("/")
                where = "/".join(parts[2:4]) if len(parts) == 5 and parts[:2] == ["b", "beds"] else None
            elif where and line.startswith("+") and _ring_said(line[1:]) in (RING_CUT + name, RING_TENDED + name):
                said[where] = _ring_said(line[1:])
    return sorted(said.items())


def _touched(root, changes, rings=()) -> list:
    """Changed paths in plain words: 'planted north-wall/quince', 'wrote book/first.md', ...

    `rings`, if given, are the rings of hands for these changes (see
    `_hand_rings`): a plant that was only cut back is then said to be cut
    back, as its rings say, and not merely tended.
    """
    cut = {where for where, ring in rings if ring.startswith(RING_CUT)}
    planted, pulled, tended, stones, plain = [], [], [], [], []

    def note(book, item):
        if item not in book:
            book.append(item)

    for status, path in changes:
        if _own_record(path):
            continue
        parts = path.split("/")
        gone = "D" in status
        new = "?" in status or "A" in status or "!" in status
        if parts[0] == "beds" and len(parts) >= 4:
            thing = "/".join(parts[1:3])
            if len(parts) == 4 and parts[3] == "seed" and (gone or new):
                note(pulled if gone else planted, thing)
            elif (Path(root) / "beds" / parts[1] / parts[2] / "seed").is_file():
                note(tended, thing)
            else:                                                 # a folder with no seed in it: a stone, and what lies under it
                note(stones, (thing, ("took a note from under %s" if gone else "left a note under %s") % thing))
        elif parts[0] == "beds" and len(parts) == 3 and parts[2] == "bed":
            note(plain, ("dug the bed %s" if new else "filled in the bed %s" if gone else "changed the bed %s") % parts[1])
        elif parts[0] == "compost" and len(parts) >= 2:
            if not gone:
                note(plain, "put %s on the heap" % parts[1])
        elif parts[0] == "species" and path.endswith(".py"):
            note(plain, ("made the kind %s" if new else "removed the kind %s" if gone else "changed the kind %s") % parts[-1][:-3])
        elif parts[0] == "book":
            note(plain, ("took out %s" if gone else "wrote %s") % path)
        elif parts[0] == "gate":
            note(plain, ("took %s from the gate" if gone else "left %s at the gate") % "/".join(parts[1:]))
        elif parts[0] == "seedbox":
            note(plain, ("took the packet %s" if gone else "left the packet %s") % _packet_name(path))
        elif parts[0] == "creatures" and len(parts) == 2 and path.endswith(".py"):
            note(plain, ("brought the creature %s" if new else "took the creature %s away" if gone
                         else "changed the creature %s") % parts[1][:-3])
        elif parts[:2] == ["shed", "bench"] and len(parts) > 2:
            note(plain, ("took %s from the potting bench" if gone else "left %s on the potting bench")
                 % "/".join(parts[2:]))
        else:
            note(plain, ("removed %s" if gone else "left %s" if new else "changed %s") % path)
    said, moves = [], dict(_moves(root, planted, pulled))
    moved_from = list(moves.values())
    for thing in planted:
        was = moves.get(thing)
        if was and was.split("/")[0] == thing.split("/")[0]:
            said.append("renamed %s to %s" % (was, thing.split("/")[1]))
        elif was:
            said.append("moved %s to %s" % (was, thing))
        else:
            said.append("planted %s" % thing)
    pulled = [thing for thing in pulled if thing not in moved_from]
    said += ["pulled %s" % thing for thing in pulled]
    said += ["%s %s" % ("cut back" if thing in cut else "tended", thing) for thing in tended
             if thing not in planted and thing not in pulled and thing not in moved_from]
    said += [words for thing, words in stones if thing not in pulled and thing not in moved_from]    # (a pulled plant's other files are no stone's)
    told = {"put %s on the heap" % thing.split("/")[1] for thing in pulled}     # pulling a plant is putting it on the heap:
    return said + [words for words in plain if words not in told]               # that is said once


def _moves(root, planted, pulled) -> list:
    """Which of the plants that seem planted were really moved or renamed: [(where it is now, where it was)].

    Git sees a moved plant as one pulled and one planted. They are the same
    plant if the folder's name is the same; or if tending, finding a tag
    that names it otherwise, rang it `renamed: it was <old name>`.
    """
    found, taken = [], set()
    for thing in planted:
        name = thing.split("/")[1]
        was = next((old for old in pulled if old.split("/")[1] == name and old not in taken), None)
        if was is None:
            rings = _read(Path(root) / "beds" / thing.split("/")[0] / name / "rings", 200_000).splitlines()
            olds = [_ring_said(line)[len(RING_RENAMED):] for line in rings if _ring_said(line).startswith(RING_RENAMED)]
            was = next((old for old in pulled if olds and old.split("/")[1] == olds[-1] and old not in taken), None)
        if was is not None:
            taken.add(was)
            found.append((thing, was))
    return found


def _in_short(said, most) -> str:
    """The first few of a list of doings on one line: 'planted a/b; tended c/d; and 3 more'."""
    return "; ".join(said[:most]) + ("; and %d more" % (len(said) - most) if len(said) > most else "")


def _message(root, lead, changes, rings=()) -> str:
    """A layer's message: a short first line, and under it everything that was touched."""
    said = _touched(root, changes, rings)
    if not said:
        return lead or "passed through and touched nothing"
    first = "%s: %s" % (lead, _in_short(said, 6)) if lead else _in_short(said, 6)
    if len(first) > 200:
        first = (lead + ": " if lead else "") + _count(len(said), "thing") + " touched"
    return first + ("\n\n" + "\n".join(said) if len(said) > 1 else "")


def _settle(root, latch, going_on, moment) -> list:
    """Lay down whatever lies uncommitted, signed by whoever must have done it. Returns the rings still to be left.

    The ground's own records changing alone are nobody's doing: they wait
    and go down with the next layer.

    A visit left open is laid down in its visitor's name. But a latch
    gone cold signs only what that visit could have done: whatever came to
    lie in the garden after its twelve hours were over is someone else's,
    and goes into a second layer, signed as it would be with no latch: by
    the keeper if it all lies on their paths (KEEPERS_PATHS, and
    ground/place), else by an unseen hand.

    Every plant a hand was at gets a ring saying so (see `_hand_rings`).
    The visitor's are left at once, dated the day of the visit. Those of
    an unseen hand are dated the day they were found; since the days that
    passed meanwhile are not lived yet, an arrival leaves them after it
    has lived those days (that is what is returned: [(where, ring)]), so a
    plant's rings stay in the order of the calendar. Any other door leaves
    them at once.
    """
    changes, later = _changes(root), []
    strays = _stray_paths(root, changes)            # what days wrote and no door could yet lay down: no hand's doing
    changes = [change for change in changes if change[1] not in strays]
    the_keepers = [change for change in changes if change[1] in KEEPERS_OWN]
    if latch and the_keepers:                       # the day's sky and the place are the keeper's, whoever holds the latch
        changes = [change for change in changes if change not in the_keepers]
        _lay_down(root, THE_KEEPER, _message(root, "the keeper was here", the_keepers, []), the_keepers,
                  [path for _, path in the_keepers])
    if latch:
        cold = not going_on and not _is_live(latch, moment)
        after = _after_the_visit(root, changes, latch) if cold else []
        during = [change for change in changes if change not in after]
        if _someones(during):
            lead = "" if going_on else LEFT_OPEN
            only = [path for _, path in during] if after or strays else None
            rings = _guarded(root, "reading what hands did", _hand_rings, root, during, latch["name"]) or []
            _guarded(root, "leaving the rings of hands", _leave_rings, root, rings,
                     moment.date() if going_on else min(moment.date(), latch["since"].date()))
            _lay_down(root, latch["name"], _message(root, lead, during, rings), during, only)
        changes = after
    theirs = _someones(changes)
    if not theirs:
        return later
    signer = THE_KEEPER if all(_keepers(path) for path in theirs) else UNSEEN
    later = _guarded(root, "reading what hands did", _hand_rings, root, changes, signer) or []
    _lay_down(root, signer, _message(root, "the keeper was here" if signer == THE_KEEPER else "found changed", changes, later),
              changes, [path for _, path in changes] if strays else None)
    return later


KEEPERS_OWN = ("gate/sky.txt", "ground/place")    # the keeper's whoever holds the latch: the day's sky, and where the garden lies


def _keepers(path) -> bool:
    """Does this path lie where the keeper's own hand may be taken to have been: their paths, or ground/place?"""
    return path.startswith(KEEPERS_PATHS) or path == "ground/place"


def _hand_rings(root, changes, name) -> list:
    """The ring each plant gets whose body, seed or tag a hand changed: [(where, ring)]. (Ruling 6 of GROUND.md.)

        moved here from north-wall by fable-5     it came from another bed
        renamed by fable-5                        it came from another name in the same bed
        cut back by fable-5                       its body only lost: lines gone, or numbers lowered
        tended by fable-5                         anything else a hand did to its body, seed or tag

    A plant a hand planted is not rung here: tending rang it `planted by`
    when it came up, or when it found it set in whole, body and all (see
    `_tag_anew`). A plant pulled is on the heap and has no rings. Only
    git can say what a body was before the hand came, so where no layers
    are kept, no such rings are left.
    """
    by_plant, planted, pulled = {}, [], []
    for status, path in changes:
        parts = path.split("/")
        if parts[0] != "beds" or len(parts) != 4 or parts[3] not in ("body", "seed", "tag"):
            continue
        thing = "/".join(parts[1:3])
        new, gone = any(mark in status for mark in "?A!"), "D" in status
        if parts[3] == "seed" and (new or gone):
            (planted if new else pulled).append(thing)
        if not (new and parts[3] == "body"):           # a body that is new came from tending (a seed come up), not a hand
            by_plant.setdefault(thing, []).append((status, parts[3], path, new))
    rings = {}
    for thing, was in _moves(root, planted, pulled):
        old_bed, _ = was.split("/")
        bed, _ = thing.split("/")
        rings[thing] = RING_RENAMED_BY + name if old_bed == bed else RING_MOVED % (old_bed, name)
    bodies = [path for thing, files in by_plant.items() if thing not in planted
              for status, what, path, new in files if what == "body" and not new]
    before = _old_texts(root, bodies)
    for thing, files in by_plant.items():
        if thing in planted or thing in pulled:
            continue
        if not (Path(root) / "beds" / thing / "seed").is_file():
            continue
        if all(what == "tag" for _, what, _, _ in files) and _only_crossed(root, files[0][2]):
            continue                                   # (the glass was set over its bed, or taken off: no hand was at it)
        rings[thing] = RING_TENDED + name
        if all(what == "body" for _, what, _, _ in files):
            path = files[0][2]
            if path in before and _only_less(before[path], _read(Path(root) / path)):
                rings[thing] = RING_CUT + name
    return sorted(rings.items())


def _only_crossed(root, path) -> bool:
    """Is a tag's only change the one tending makes when a plant crosses the glass (see `_cross_glass`)?"""
    old = _old_texts(root, [path]).get(path)
    if old is None:
        return False

    def rest(text):
        return [line for line in text.splitlines()
                if " ".join(line.partition(":")[0].split()).lower() not in ("planted", "under", "days before", "first planted")]

    return rest(old) == rest(_read(Path(root) / path, 100_000))


def _only_less(old, new) -> bool:
    """Did a body only lose, from `old` to `new`?

    A hand takes from a plant in three ways. It cuts lines or letters out:
    the body is shorter, and no word in it is new. It lowers numbers: a
    stem of 7 cut to 5 is a body of the same length. Or it scrapes letters
    back to the bare ground they stood on, as a lichen is cut, its living
    cells turned to `.`: the body keeps its length, and every change is a
    mark rubbed out (see `_only_scraped`). Any of these is a cut.

    (The doors run no kind, so no kind can be asked how large the plant
    is before and after; what is read here is the text alone.)
    """
    words = lambda text: set(re.findall(r"[^\W\d_]+", text.lower()))
    numbers = lambda text: sum(float(n) for n in re.findall(r"\d+(?:\.\d+)?", text)[:5000])
    if words(new) <= words(old) and (len(new.strip()) < len(old.strip()) or numbers(new) < numbers(old)):
        return True
    return _only_scraped(old, new)


BARE = set(" .·-_\t")     # what a scraped mark leaves: the ground it stood on


def _only_scraped(old, new) -> bool:
    """Is `new` the text `old` with some of its marks rubbed out to bare ground (BARE), or taken away, and nothing added?

    It is judged by what was lost and what was gained, never by how a
    diff happens to line the two texts up: in a moss or a lichen many rows
    look alike, and a row scraped until it matches another is still a row
    scraped. Some mark must be gone, and nothing may have come:

    - when the body keeps its number of lines, the lines are compared
      place by place, each with the line that stood where it stands (a
      grid's rows are its cells' places): every mark of the new line
      stands where it stood, or was taken away, or turned to bare ground;
    - else (or if that fails) the new lines must be the old ones, in their
      order, with lines taken out whole, empty lines put in, and within a
      line marks taken away or turned to bare ground, and bare ground
      added. One new letter, or a mark set where there was none, and it is
      not a cut.
    """
    if old == new or len(old) > 200_000 or len(new) > 200_000:
        return False
    old_lines, new_lines = old.splitlines(), new.splitlines()
    marks = lambda lines: sum(1 for line in lines for ch in line if ch not in BARE)
    if marks(new_lines) >= marks(old_lines):
        return False                                   # nothing was lost (or as much came as went)
    if len(old_lines) == len(new_lines) and all(_rubbed(before, after) for before, after in zip(old_lines, new_lines)):
        return True
    at = 0                                             # each new line, in order, is some old line rubbed: the earliest
    for after in new_lines:                            # one that fits (the earliest never spoils a later fit)
        if not after.strip():
            continue                                   # an empty line put in: nothing came
        while at < len(old_lines) and not _rubbed(old_lines[at], after):
            at += 1
        if at == len(old_lines):
            return False
        at += 1
    return True


def _rubbed(before, after) -> bool:
    """Is the line `after` the line `before` with marks taken away or turned to bare ground (BARE), and bare ground
    added, and nothing else?

    A line of the same length is compared place by place: a scrape keeps
    its line's length, and a mark moved along its row is a mark set where
    there was none. A shorter or longer line must keep its marks in their
    order: every mark it holds is one of the old line's, in turn.
    """
    if len(before) == len(after):
        return all(a == b or b in BARE for a, b in zip(before, after))
    kept = iter(before)
    return all(ch in BARE or any(ch == was for was in kept) for ch in after)


def _old_texts(root, paths) -> dict:
    """{path: its text in the last layer} for these paths, in one git call. What git cannot give is left out."""
    if not paths or not _layers(root):
        return {}
    done = _git(root, "cat-file", "--batch", given="".join("HEAD:%s\n" % path for path in paths).encode("utf-8"))
    if done is None or done.returncode != 0:
        return {}
    texts, data, at = {}, done.stdout, 0
    for path in paths:
        end = data.find(b"\n", at)
        if end < 0:
            break
        head = data[at:end].split()
        at = end + 1
        if len(head) == 3 and head[1] == b"blob" and head[2].isdigit():
            size = int(head[2])
            texts[path] = _plain(data[at:at + size].decode("utf-8", errors="replace"))
            at += size + 1
    return texts


def _leave_rings(root, rings, day) -> None:
    """Add each (where, ring) to that plant's rings, dated `day`: if it is still a plant where it was.

    A plant under glass is rung on the day the glass stands at: its rings keep the glass's calendar.
    """
    under, glassy = None, set()
    if rings:
        glassy = {bed.name for bed in beds(root) if bed.glass}
        under = glass(root, day) if glassy else None
    for where, ring in rings:
        folder = Path(root) / "beds" / where
        if (folder / "seed").is_file():
            its_day = under.stands if under is not None and where.split("/")[0] in glassy else day
            _append(root, folder / "rings", ["%s  %s" % (its_day.isoformat(), _one_line(ring, 200))])


def _someones(changes) -> list:
    """Of these changes, the paths that are somebody's doing: all but the ground's own records."""
    return [path for _, path in changes if not _own_record(path)]


def _after_the_visit(root, changes, latch) -> list:
    """Of these changes, those that came about after the visit on a cold latch must have been over.

    A new plant is dated by its seed: the body and the tag that tending
    gave it when it came up were planted with the seed, by whoever
    planted that. A seed moved there keeps the time it was written; then
    the time its folder was made says when it came, as it does when the
    seed's signer is asked (see `_signer`).
    """
    new_plants = {path.rpartition("/")[0] for status, path in changes
                  if "?" in status and re.fullmatch(r"beds/[^/]+/[^/]+/seed", path)}
    after = {folder for folder in new_plants
             if _surely_after(_planted_lain(root, Path(root) / folder, own_writes=True), latch)}
    return [(status, path) for status, path in changes
            if (path.rpartition("/")[0] in after if path.rpartition("/")[0] in new_plants
                else _came_after(root, path, latch))]


def _came_after(root, path, latch) -> bool:
    """Did this file come to lie where it is after the visit on the latch must have been over?

    What is gone cannot be asked, and what was moved keeps its old time:
    both are left to the visit. Only what is surely later is taken from it.
    """
    return _surely_after(_lain(root, Path(root) / path), latch)


def _surely_after(lain, latch) -> bool:
    """Is this moment after the twelve hours of the visit on the latch?"""
    return lain is not None and (lain - latch["since"]).total_seconds() >= LATCH_HOURS * 3600


# =============================================================== the latch

def _latch(root):
    """What the latch says: {'name': ..., 'since': datetime, 'visit': its token or ''}, or None if there is none.

    (Whether it still holds the gate is `_is_live`'s to say.) The token is
    the visit's own: a name is a signature, and two visits may carry the
    same one; the token tells them apart (see `arrive`).
    """
    path = Path(root) / "ground" / "present"
    if not path.is_file():
        return None
    keys = hands.read_keys(_read(path, 10_000))
    name = hands.line(keys, "name")
    if not name:
        return None
    try:
        since = datetime.datetime.fromisoformat(hands.line(keys, "since")).replace(tzinfo=None)
    except ValueError:
        try:
            since = _garden_time(root, path.stat().st_mtime)
        except OSError:
            since = datetime.datetime.min
    return {"name": visitor_name(name), "since": since, "visit": _token(hands.line(keys, "visit"))}


def _token(text) -> str:
    """A visit's token as the latch keeps it: one short word of letters, digits and - _ . : ('' if there is none)."""
    return re.sub(r"[^A-Za-z0-9_.:\-]", "", str(text or ""))[:80]


def _new_token() -> str:
    """A token for a visit that brought none: a few random letters, never shown, kept only on the latch."""
    return os.urandom(6).hex()


def _is_live(latch, moment) -> bool:
    """Does this latch still hold the gate? Not after LATCH_HOURS; and a latch dated in the future holds nothing.

    Every door asks this, not only arriving: someone who walks in long
    after another visitor forgot the gate does not plant, or leave, in that
    visitor's name.
    """
    if not latch:
        return False
    return -1.0 <= (moment - latch["since"]).total_seconds() / 3600.0 < LATCH_HOURS


def _set_latch(root, name, moment, token="") -> None:
    text = ("# The latch: who is in the garden now. leave.py lifts it; after %d hours it lifts itself.\n"
            "# `visit` is this visit's own token: arrive.py --visit <token> goes on with this visit and no other.\n"
            "name: %s\nsince: %s\nvisit: %s\n" % (LATCH_HOURS, name, moment.isoformat(timespec="minutes"), token or _new_token()))
    _write(root, Path(root) / "ground" / "present", text)


def _lift_latch(root) -> None:
    _remove(Path(root) / "ground" / "present")


def _write_visit(root, moment, what, name, words="") -> None:
    """Add a line to ground/visits: the time, one of the three VISIT_ phrases, the name, and any words said on leaving.

        2026-10-03 17:42  came in · claude-opus-4-7
        2026-10-03 18:10  closed the gate · claude-opus-4-7 · a few words
        2026-10-24 09:12  found the gate left open by claude-opus-4-7

    The last is written by the next door to pass, at its own time: when the
    visit itself went out, nobody saw, so the record does not pretend to.
    """
    path = Path(root) / "ground" / "visits"
    lines = [] if path.is_file() else ["# Who came through the gate, and when."]
    if what == VISIT_OPEN:
        lines.append("%s  %s%s" % (moment.strftime("%Y-%m-%d %H:%M"), VISIT_OPEN, name))
    else:
        lines.append("%s  %s · %s%s" % (moment.strftime("%Y-%m-%d %H:%M"), what, name, " · " + words if words else ""))
    _append(root, path, lines)


def _visits(root) -> list:
    """ground/visits, read: [(moment, 'in' | 'out' | 'open', name)], oldest first.

    What a line is, is said by the fixed phrase after its time, never by
    anything in the name or the words that follow.
    """
    sorts = {VISIT_IN: "in", VISIT_OUT: "out", VISIT_OPEN_ONCE: "open"}
    found = []
    for line in _read(Path(root) / "ground" / "visits").splitlines():
        try:
            moment = datetime.datetime.strptime(line[:16], "%Y-%m-%d %H:%M")
        except ValueError:
            continue
        said = line[16:].strip()
        if said.startswith(VISIT_OPEN):
            found.append((moment, "open", said[len(VISIT_OPEN):].strip()))
            continue
        what, dot, rest = said.partition(" · ")
        if what in sorts and dot:
            found.append((moment, sorts[what], rest if what == VISIT_IN else rest.split(" · ")[0]))
    return found


def _last_visit_ended(root):
    """The day the visit before the latest one ended: what 'grown since' is counted from. None if there was none."""
    visits = _visits(root)
    latest = max((i for i, visit in enumerate(visits) if visit[1] == "in"), default=None)
    if latest is None:
        return None
    for moment, what, _ in reversed(visits[:latest]):
        if what in ("in", "out"):
            return moment.date()
    return None


# ---- where a visit begins
#
# Every visitor arrives new, and nothing done before a visit began is ever told as its doing. A visit's doings
# are what the layers laid down after it came in; a minute is too coarse to say which those are, since the
# arrival that lets a visit in first lays down the visit before it (left open, perhaps under the same name)
# and the days it lived, all within that minute or the next. So the moment a visit comes in, the ground notes
# the layer the garden stands at, and the moment to the second, in ground/.began.

BEGAN_HEAD = ("# Where the latest visit began: the minute it came in (as ground/visits has it), the moment to the second,",
              "# and the layer the garden stood at then. What was laid down before is never told as that visit's own.")
NO_LAYER_YET = "none yet"


class _Began:
    """Where a visit began: what came after this is that visit's time, and what came before is someone else's.

        .came    the minute it came in, as ground/visits says
        .layer   the layer the garden stood at when it came in, as its hash: what is laid after it was laid in that
                 visit's time ('' if it came in before any layer was laid; None if the layers cannot say)
        .since   the moment it came in, on the garden's clock: what lies strictly after it is newer. To the second
                 where ground/.began says; else only the minute is known, and the whole of it is counted before.
    """
    __slots__ = ("came", "layer", "since")

    def __init__(self, came, layer, since):
        self.came, self.layer, self.since = came, layer, since


def _began_file(root) -> Path:
    return Path(root) / "ground" / ".began"


def _beginning_text(root, name, came) -> str:
    """Where the visit that comes in now begins, as ground/.began keeps it: taken as its line in ground/visits is
    written, after everything its arrival laid down. The visit before it, gathered in, and the days that passed
    are laid before this visit's beginning, and are never told as its own.

    It is written only once the arrival's note is made (see `_arrive`),
    since the note reads in ground/.began where the visit before began.
    """
    lines = list(BEGAN_HEAD) + ["name: %s" % name, "came: %s" % came.strftime("%Y-%m-%d %H:%M"),
                                "since: %s" % now(root).isoformat(timespec="seconds")]
    layer = _head(root)
    if layer is not None:
        lines.append("layer: %s" % (layer or NO_LAYER_YET))
    return "\n".join(lines) + "\n"


def _beginning(root, name, came) -> _Began:
    """Where the visit that came in under `name` at the minute `came` began (see `_Began`).

    ground/.began says it, if it speaks of that very visit. If it does not
    (a hand took it away), the layers are asked: the visit began just
    before the first layer that holds its line in ground/visits. Failing
    both, only the minute is known, and the whole minute is counted before
    the visit: nothing an arrival laid down is then taken for the visit's
    own, at the cost of what the visitor did in their first minute.
    """
    began = _Began(came, None, came + datetime.timedelta(minutes=1))
    keys = hands.read_keys(_read(_began_file(root), 10_000))
    if hands.line(keys, "name") == name and hands.line(keys, "came") == came.strftime("%Y-%m-%d %H:%M"):
        try:
            since = datetime.datetime.fromisoformat(hands.line(keys, "since")).replace(tzinfo=None)
        except ValueError:
            since = None
        if since is not None and came <= since < came + datetime.timedelta(hours=1):
            began.since = since
        layer = hands.line(keys, "layer")
        if layer == NO_LAYER_YET and _layers(root):
            began.layer = ""
        elif re.fullmatch(r"[0-9a-f]{40,64}", layer) and _layers(root):
            done = _git(root, "merge-base", "--is-ancestor", layer, "HEAD")
            if done is not None and done.returncode == 0:      # a layer that is still in the garden's history
                began.layer = layer
    if began.layer is None and _layers(root):
        began.layer = _layer_before_line(root, name, came)
    return began


def _head(root):
    """The layer the garden stands at, as its hash; '' if no layer has been laid yet; None if no layers are kept."""
    if not _layers(root):
        return None
    done = _git(root, "rev-parse", "--verify", "--quiet", "HEAD^{commit}")
    if done is None:
        return None
    found = done.stdout.decode("utf-8", errors="replace").strip()
    if done.returncode == 0 and re.fullmatch(r"[0-9a-f]{40,64}", found):
        return found
    every = _git(root, "rev-list", "-n", "1", "--all")
    if every is not None and every.returncode == 0 and not every.stdout.strip():
        return ""                                  # a repository with no layer in it yet
    return None


def _layer_before_line(root, name, came):
    """Where a visit began in the layers, when ground/.began does not say: the layer before the first that holds
    its line in ground/visits ('' if that is the first layer of all). If no layer holds it yet, nothing has been
    laid since the visit came in, and it began at the newest layer. None if the layers cannot say."""
    line = "%s  %s · %s" % (came.strftime("%Y-%m-%d %H:%M"), VISIT_IN, name)
    head = _head(root)
    if head is None:
        return None
    if not head:
        return ""
    working = _read(Path(root) / "ground" / "visits").splitlines().count(line)
    if not working:
        return None                                # the visits no longer say it: the layers cannot be asked
    laid = _old_texts(root, ["ground/visits"]).get("ground/visits", "").splitlines().count(line)
    if laid < working:                             # its line is not laid down yet: neither is anything since
        return head
    done = _git(root, "log", "-1", "--format=%H %P", "-S" + line, "--", "ground/visits")
    if done is None or done.returncode != 0:
        return None
    found = done.stdout.decode("utf-8", errors="replace").split()
    if not found or not re.fullmatch(r"[0-9a-f]{40,64}", found[0]):
        return None
    return found[1] if len(found) > 1 else ""


# ================================================================= drawing
#
# Three layouts, all drawn through plate.py: the plate of one plant, the
# sheet of one bed, the plan of the whole garden. Rule 5 governs them:
# nothing in the picture that is not in the garden.

PLATE_BOX = (60, 50, 840, 930)       # where the plant itself is drawn on its 900 x 1200 plate
PLAN_SCALE = 1.24                    # pixels per plan unit: 1000 x 700 becomes 1240 x 868
PLAN_LEFT, PLAN_TOP = 80, 70         # where the plan's north-west corner sits on its 1400 x 1000 sheet
SHEET_MOST = 64                      # plants drawn on one bed sheet
NAMED_MOST = 8                       # a bed of more plants than this is not lettered with their names on the plan
MARKS_MOST = 40_000                  # marks of one plant's drawing that are remembered at all (each point of a polyline
                                     # counts as one); past that, the rest are not kept
INK_MOST = 70_000                    # what one plant's drawing may cost the plate, in strokes: a stroke is about what a
                                     # short thin line costs, some 0.02 ms on this machine, so a plate's ink is drawn in
                                     # about two seconds at most (see `_Record.weigh`)
CUT_SHORT = "the drawing was cut short: the whole of it is more than a plate can draw in time"
SLOW_PLATE = 3.0                     # seconds a plate may take to draw before the trouble log says so, naming the plant


class _Record:
    """A pen that only remembers. A kind draws on it once; the ground replays it on the plate and on the sheet.

    It has everything GROUND.md gives a Specimen. settle() is the ground's
    to call, so here it does nothing.

    What a drawing costs is not what it costs the kind to make it: a kind
    names a whole circle in one call, and the plate then lays it point by
    point. So once the kind has drawn, the record is weighed (`weigh`):
    each mark by what the plate will spend on it at the size it will be
    drawn, and a drawing that would cost more than INK_MOST strokes is cut
    short there, and its plate says so.
    """
    unit_name = "units"
    unit_px_max = 60.0
    align = "ground"
    pens = 1.0
    labels = True
    scale = 0.0
    bar = None
    box = tuple(float(v) for v in PLATE_BOX)

    def __init__(self):
        self.notes = []
        self.marks = []
        self.strokes = 0             # how much was drawn: one for each mark, and for a polyline one for each point
        self.trouble = ""            # why there is no drawing, if there is none
        self.weighed_out = False     # the drawing was cut short when it was weighed (see `weigh`)

    def _keep(self, name, a, k, strokes=1):
        if self.strokes < MARKS_MOST:                  # a drawing of more marks than this is cut short, not refused
            self.marks.append((name, a, k))
        self.strokes += strokes

    @property
    def cut_short(self) -> bool:
        return self.strokes > MARKS_MOST or self.weighed_out

    def line(self, *a, **k):
        self._keep("line", a, k)

    def polyline(self, pts, *a, **k):
        try:
            pts = list(pts)[:MARKS_MOST]
        except TypeError:
            return
        self._keep("polyline", (pts,) + a, k, max(1, len(pts)))

    # ---- what the drawing will cost the plate

    SIGNATURES = {"line": ("x1", "y1", "x2", "y2", "weight"), "polyline": ("pts", "weight"),
                  "dot": ("x", "y", "r", "ink", "filled", "weight"), "arc": ("cx", "cy", "radius", "start_deg", "end_deg", "weight"),
                  "cell": ("x", "y", "w", "h"), "label": ("x", "y", "s", "size"), "ground": ("y",)}

    def _given(self, name, a, k) -> dict:
        """A mark's arguments by name, as the Specimen would take them (what is missing or odd is simply not there)."""
        given = dict(zip(self.SIGNATURES.get(name, ()), a))
        given.update({key: value for key, value in k.items() if isinstance(key, str)})
        return given

    def weigh(self, room=(760.0, 820.0)) -> None:
        """Cut the drawing short where it would cost the plate more than INK_MOST strokes to lay.

        The scale it will be drawn at is not known until the plate settles
        it, so it is foreseen here as the plate will find it: everything
        drawn, fitted into the plate's box (`room`, in pixels), never more
        than unit_px_max pixels to a unit. Then each mark is weighed by what
        it costs at that size: a line by its weight; a polyline and an arc
        by their points (an arc has more the larger it is drawn: see
        plate._arc_points), each as a short line; a dot and a cell by their
        size; a label by its letters. The marks are kept in the order the
        kind drew them, up to the last that fits.
        """
        xs, ys = [], []
        for name, a, k in self.marks:
            given = self._given(name, a, k)
            try:
                if name == "polyline":
                    for x, y in list(given.get("pts", ()))[:2000]:
                        xs.append(float(x))
                        ys.append(float(y))
                elif name == "arc":
                    cx, cy, r = float(given["cx"]), float(given["cy"]), abs(float(given["radius"]))
                    xs += [cx - r, cx + r]
                    ys += [cy - r, cy + r]
                elif name in ("line",):
                    xs += [float(given["x1"]), float(given["x2"])]
                    ys += [float(given["y1"]), float(given["y2"])]
                elif name in ("dot", "cell", "label"):
                    xs.append(float(given["x"]))
                    ys.append(float(given["y"]))
                    if name == "cell":
                        xs.append(float(given["x"]) + float(given.get("w", 1.0)))
                        ys.append(float(given["y"]) + float(given.get("h", 1.0)))
            except (KeyError, TypeError, ValueError, OverflowError):
                continue
        xs = [x for x in xs if math.isfinite(x)]
        ys = [y for y in ys if math.isfinite(y)]
        scale = _number(self.unit_px_max, 60.0)
        if xs and ys:
            for span, side in ((max(xs) - min(xs), room[0]), (max(ys) - min(ys), room[1])):
                if span > 0:
                    scale = min(scale, side / span)
        spent = 0.0
        for at, (name, a, k) in enumerate(self.marks):
            spent += self._cost(name, self._given(name, a, k), scale)
            if spent > INK_MOST and at > 0:
                del self.marks[at:]
                self.weighed_out = True
                return

    @staticmethod
    def _cost(name, given, scale) -> float:
        """What one mark costs the plate, in strokes (about 0.02 ms each), drawn at `scale` pixels to a unit."""
        def number(key, otherwise):
            return _number(given.get(key, otherwise), otherwise)

        pen = 0.75 + 0.23 * min(18.0, max(2.0, number("weight", 3.0)))      # one point of a stroke of that weight
        try:
            if name == "line" or name == "ground":
                return pen
            if name == "polyline":
                return pen * max(1, len(given.get("pts", ())))
            if name == "arc":
                radius = abs(float(given.get("radius", 0.0))) * scale
                sweep = abs(math.radians(float(given.get("end_deg", 0.0)) - float(given.get("start_deg", 0.0))))
                step = 2 * math.acos(max(-1.0, 1 - 0.04 / radius)) if radius > 0.04 else math.pi
                return pen * min(2000, max(2, math.ceil(min(sweep, 2 * math.pi) / step)))
            if name == "dot":
                return max(1.4, min(60.0, number("r", 5.0)) / 3.0) * 2      # (and the paper laid round it, often)
            if name == "cell":
                side = math.sqrt(abs(float(given.get("w", 1.0)) * float(given.get("h", 1.0)))) * scale
                return max(1.0, min(side, 2000.0) / 8.0)
            if name == "label":
                return 3.0 * len(str(given.get("s", "")))
        except (TypeError, ValueError, OverflowError):
            return 1.0
        return 1.0

    def dot(self, *a, **k):
        self._keep("dot", a, k)

    def arc(self, *a, **k):
        self._keep("arc", a, k)

    def cell(self, *a, **k):
        self._keep("cell", a, k)

    def label(self, *a, **k):
        self._keep("label", a, k)

    def ground(self, *a, **k):
        self._keep("ground", a, k)

    def note(self, s):
        s = _one_line(s, 200)
        if s and len(self.notes) < 3:
            self.notes.append(s)

    def settle(self):
        return 0.0

    @property
    def canvas(self):
        import plate
        return plate.Canvas(8, 8)

    def has_ink(self, ink) -> bool:
        """Did the kind draw anything in this ink?"""
        return any(k.get("ink") == ink or any(isinstance(v, str) and v == ink for v in a) for _, a, k in self.marks)

    def replay(self, pen) -> None:
        """Draw everything that was remembered with a real pen."""
        pen.unit_name = _one_line(self.unit_name, 30)
        pen.align = self.align
        for name, a, k in self.marks:
            try:
                getattr(pen, name)(*a, **k)
            except Exception:
                pass                                   # a mark the pen cannot make is skipped


class _Studio:
    """Everything needed to draw, gathered once for one pass through a door."""

    def __init__(self, root):
        self.root = Path(root)
        self.moment = now(root)
        self.today = self.moment.date()
        self.sky = sky.sky_for(root, self.today)
        self.under = glass(root, self.today)        # the calendar under the glass, or None: a plant there is drawn on its day
        self._glass_sky = None
        self.weather_seed = sky.place(root).get("weather-seed")
        self.soil = Soil(root)
        self.rich = _read_rich(root)
        self.since = _last_visit_ended(root)
        self.until = None                 # time.monotonic() at which drawing should stop, if it has a budget
        self.records = {}
        self._garden = None
        self._own = None
        self._lefts = {}
        self._kind_marks = {}

    def garden(self) -> list:
        if self._garden is None:
            self._garden = plants(self.root)
        return self._garden

    def time_is_up(self) -> bool:
        return self.until is not None and time.monotonic() > self.until

    def day_of(self, bed) -> datetime.date:
        """The day a bed stands at: today, or under the glass the day the glass stands at."""
        return _day_of(bed, self.today, self.under)

    def sky_over(self, bed):
        """The sky over a bed on its own day: the garden's sky, or the sky under the glass."""
        if self.under is None or not bed.glass:
            return self.sky
        if self._glass_sky is None:
            self._glass_sky = sky.under_glass(self.root, self.under.stands)
        return self._glass_sky

    def glass_words(self, bed) -> str:
        """'under glass, 14 March 2027' for a bed under glass (the day its drawings show); '' for any other."""
        return "under glass, %s" % _glass_date(self.under.stands) if self.under is not None and bed.glass else ""

    def ctx(self, plant, purpose, left=None, hour=None) -> Ctx:
        day = self.day_of(plant.bed)
        return Ctx(plant, day, sky.local(self.sky_over(plant.bed), plant.bed), purpose, self.weather_seed, self.soil,
                   lambda: _living_in(self.garden(), plant.bed.name, day), left=left, hour=hour,
                   rich=_rich_on(self.rich, plant.bed.name, day))

    def left_of(self, plant):
        """The body as the last visitor left it, or None if the plant is new since then."""
        if plant.where not in self._lefts:
            path = plant.path / ".left"
            self._lefts[plant.where] = _read(path) if path.is_file() else None
        return self._lefts[plant.where]

    def changed(self, plant) -> bool:
        """Is this plant new since the last visit, or is there a line in its body that was not there then?

        A plant that was only cut back has nothing new in it, and is not
        marked: the fresh ink is for what came, not for what went.
        """
        left = self.left_of(plant)
        return left is None or bool(hands.fresh_lines(plant.body, left))

    def size_of(self, plant) -> float:
        """How large a plant is, for its dot on the plan.

        A kind may say, with `size(body, seed)`: a number in its own units
        (a lichen's living cells, a bine's lengths), where a body's whole
        length would mislead (a lichen's body is its whole stone, a speck
        and a shield alike). Otherwise it is the body's length, one unit for
        every forty characters, about a line of a plain body. The kind is
        asked as it is for anything (guarded, and for at most
        KIND_SECONDS['size']); a dead plant, or one it cannot be asked of,
        is measured by its body.
        """
        size = len(plant.body) / 40.0
        if not plant.has_body or plant.dead or plant.unfit or self.time_is_up() or _no_kind(self.root, plant.kind):
            return size
        module = kind(self.root, plant.kind)
        if not callable(getattr(module, "size", None)):
            return size
        said, error, full = _ask(self.root, plant.kind, "size", plant.where, module.size, plant.body, dict(plant.seed))
        if error is not None:
            trouble(self.root, "%s: its size could not be told: %s" % (plant.where, _in_words(error)), full, aloud=False)
            return size
        if isinstance(said, bool) or not isinstance(said, (int, float)) or not 0 <= said < 1e12:
            return size                            # (NaN is no number it can be: it fails the test above)
        return float(said)

    def seed_words(self, plant) -> str:
        """What to say of a seed that has not come up: 'still a seed', and why if its rings say."""
        return plant.last_ring if plant.last_ring.startswith(RING_SEED) else RING_SEED.rstrip(": ")

    def describe(self, plant) -> str:
        """One short line about a plant: the kind's own `describe`, or the plainest thing that is true."""
        if not plant.has_body:
            return self.seed_words(plant)
        if plant.dead:
            plain = _one_line(plant.body.lstrip().split("\n", 1)[0], 100)
        else:
            plain = _count(len([line for line in plant.body.splitlines() if line.strip()]), "line") + " of body"
        why = _no_kind(self.root, plant.kind)
        if why:
            set_aside = (str(self.root), plant.kind) in _aside
            return plain if plant.dead else why if set_aside else RING_ASLEEP + why
        module = kind(self.root, plant.kind)
        if callable(getattr(module, "describe", None)) and not plant.unfit and not self.time_is_up():
            said, error, full = _ask(self.root, plant.kind, "describe", plant.where, module.describe,
                                     plant.body, dict(plant.seed), self.ctx(plant, "describe"))
            if error is None and isinstance(said, str) and said.strip():
                return _one_line(said, 100)
            if error is not None:
                trouble(self.root, "%s: describe failed: %s" % (plant.where, error), full, aloud=False)
        return plain

    # ---- the kind's drawing, remembered

    def record(self, plant) -> _Record:
        """What the kind draws for this plant: asked for once, then kept for the plate and the sheet."""
        if plant.where in self.records:
            return self.records[plant.where]
        record = self.records[plant.where] = _Record()
        why = "" if not plant.has_body else _no_kind(self.root, plant.kind)
        module = None if why or not plant.has_body else kind(self.root, plant.kind)
        if not plant.has_body:
            record.trouble = self.seed_words(plant)
        elif why:
            record.trouble = why
        elif plant.unfit:
            record.trouble = "cannot be drawn: " + plant.unfit
        elif not callable(getattr(module, "draw", None)):
            record.trouble = "this kind has no drawing"
        else:
            ctx = self.ctx(plant, "draw", left=self.left_of(plant), hour=self.moment.hour)
            _, error, full = _ask(self.root, plant.kind, "draw", plant.where, module.draw,
                                  plant.body, dict(plant.seed), ctx, record)
            if error is not None:
                record.marks.clear()
                record.trouble = "could not be drawn: " + _in_words(error)
                trouble(self.root, "%s %s" % (plant.where, record.trouble), full, aloud=False)
            else:
                record.weigh()
                if record.cut_short:
                    record.notes = record.notes[:2] + [CUT_SHORT]
        return record

    # ---- is a drawing still true?

    def _own_mark(self) -> str:
        if self._own is None:
            digest = hashlib.sha1()
            for name in ("plate.py", "ground.py"):
                try:
                    digest.update((SHED / name).read_bytes())
                except OSError:
                    pass
            self._own = digest.hexdigest()
        return self._own

    def mark_of(self, plant) -> str:
        """A hash of everything a plate is drawn from. While it matches `.drawn`, the plate is current.

        Today's date is part of it: a kind may draw by the season, the age
        or the hour, and the caption gives the age in days, so a plate is
        at most a day old (ruling 8).
        """
        digest = hashlib.sha1()
        left = self.left_of(plant)
        if plant.kind not in self._kind_marks:
            self._kind_marks[plant.kind] = _kind_file_mark(self.root, plant.kind)
        since = str(self.since) if left != plant.body else ""       # the caption names that day only beside fresh ink
        for part in (self.day_of(plant.bed).isoformat(), plant.body, "no .left" if left is None else left, plant.seed_text,
                     plant.tag_text, plant.bed.name, self._kind_marks[plant.kind], self._own_mark(),
                     ink_of(self.root, plant.by), since, plant.last_ring if not plant.has_body else ""):
            digest.update(part.encode("utf-8", errors="replace"))
            digest.update(b"\0")
        return digest.hexdigest()

    def is_current(self, plant) -> bool:
        return (plant.path / "plate.png").is_file() and _read(plant.path / ".drawn", 200).strip() == self.mark_of(plant)

    def sheet_mark(self, bed, growing) -> str:
        digest = hashlib.sha1(("%s|%s|%s" % (bed.name, sorted(bed.keys.items()), self.glass_words(bed))).encode("utf-8", "replace"))
        for plant in growing:
            digest.update(("%s|%s" % (plant.name, self.mark_of(plant))).encode("utf-8", "replace"))
        return digest.hexdigest()

    # ---- the plate of a plant

    def plate(self, plant, force=False):
        """Draw a plant's plate (unless it is current). Returns its path, or None if it could not be written."""
        target = plant.path / "plate.png"
        mark = self.mark_of(plant)
        if not force and target.is_file() and _read(plant.path / ".drawn", 200).strip() == mark:
            return target
        import plate
        canvas = plate.Canvas(900, 1200)
        canvas.inks["wood"] = ink_of(self.root, plant.by)
        record = self.record(plant)
        pen = canvas.specimen(PLATE_BOX, unit_px_max=_number(record.unit_px_max, 60.0), align=record.align)
        began = time.monotonic()
        record.replay(pen)
        pen.settle()
        took = time.monotonic() - began
        if took > SLOW_PLATE:                      # weighed and still slow: the log names it, for whoever wonders where
            trouble(self.root, "%s: its plate took %.1f s to draw (%d marks)" % (plant.where, took, len(record.marks)),
                    aloud=False)                   # a door's drawing time went
        if record.trouble:
            canvas.text(450, 480, _fitted(canvas, record.trouble, 18, 780), 18, "dead", "middle")
        self._caption(canvas, plant, record)
        if not (canvas.save_png(target) or self._by_way_of_ground(canvas.save_png, target)):
            trouble(self.root, "the plate of %s could not be written" % plant.where, canvas.trouble)
            return None
        if not canvas.save_svg(plant.path / "plate.svg"):
            self._by_way_of_ground(canvas.save_svg, plant.path / "plate.svg")
        _write(self.root, plant.path / ".drawn", mark + "\n")
        return target

    def _by_way_of_ground(self, save, target) -> bool:
        """Have a drawing written in ground/ and then moved to its place. True if it got there.

        For a plant whose folder lies at the very edge of how long a path
        may be. plate.py writes beside the file first, under a longer name,
        and out there that name has no room; the file itself still has.
        """
        resting = self.root / "ground" / (".drawing" + Path(target).suffix)
        try:
            if not save(resting):
                return False
            _put_in_place(resting, target)
            return True
        except OSError:
            _remove(resting)
            return False

    def planted_words(self, plant) -> str:
        """How a plant came to be where it is, for its plate and its look:

            planted 2026-10-03 by claude-opus-4-7
            self-sown on 2026-10-04, from north-wall/quince          (sown by the days: up or not, its kind says)
            rooted from the tip of north-wall/twist on 2026-10-04   (a piece of its parent: its tag's own words)
            planted 2026-10-03 outdoors by claude-opus-4-7 · under glass since 2027-01-15     (it crossed the glass)
        """
        when = plant.planted.isoformat() if plant.planted else "on a day its tag no longer says"
        here = ""
        if plant.first:                                # it crossed the glass: when and where it was planted in truth,
            here = " · %s since %s" % ("under glass" if plant.bed.glass else "outdoors", when)     # and since when it is here
            when = plant.first.replace(",", "")        # ("2026-10-03 outdoors")
        origin = hands.line(plant.tag, "from")
        if plant.by == THE_DAYS and hands.line(plant.tag, "rooted"):
            return "%s on %s%s" % (origin or "rooted beside its parent", when, here)
        if plant.by == THE_DAYS:
            source = origin[len("self-sown "):] if origin.startswith("self-sown from ") else origin
            words = "self-sown on %s" % when + (", %s" % source if source else "")
            for key in ("carried", "hidden"):          # a creature's hand in it: its seed was carried here, or hidden
                found = re.match(r"by ([^(,]+?)(?: on \d{4}-\d{2}-\d{2})?(?: \(|,|$)", hands.line(plant.tag, key))
                if found and "%s by" % key not in words:
                    words += ", %s by %s" % (key, found.group(1).strip())
            return words + here
        return "planted %s by %s%s" % (when, plant.by, here)

    def age_words(self, plant) -> str:
        """'12 days'; for the dead, 'died 31 December 2026, frost · stood 92 days'."""
        if not plant.dead:
            return _count(max(0, (self.day_of(plant.bed) - plant.planted).days) + plant.before, "day") if plant.planted else ""
        return "".join(self.death_parts(plant, 60))

    def death_parts(self, plant, most=200) -> tuple:
        """A dead plant's death in three parts, (when, how, how long it stood), to be joined or fitted:
        ('died 31 December 2026', ', frost', ' · stood 92 days'), or ('dead', ': <its first line>', '')."""
        said = _one_line(plant.body.lstrip().split("\n", 1)[0].lstrip(DAGGER + " "), most)
        died = _date_in(said[:10])
        if died is None:
            return "dead", (": " + said if said else ""), ""
        how = said[10:].strip(" ,")
        stood = ""
        if plant.planted and died >= plant.planted:
            stood = " · stood %s" % _count((died - plant.planted).days + plant.before, "day")
        return "died %d %s %d" % (died.day, MONTHS[died.month - 1], died.year), (", " + how if how else ""), stood

    def fresh_words(self, plant, ask=True):
        """What the fresh ink on a plant's drawing means, or None if there is none to explain.

        With ask=False the kind is not asked for a drawing it has not made
        yet: a plant that was not drawn has no fresh ink to explain.
        """
        left = self.left_of(plant)
        if left is not None and left == plant.body:
            return None
        if not ask and plant.where not in self.records:
            return None
        if not self.record(plant).has_ink("fresh"):
            return None
        verb = "new" if left is None else "grown"
        if self.under is not None and plant.bed.glass:         # (the last visit's day is the garden's: under the glass it
            return "%s since the last visit" % verb            # would be a date of another calendar)
        if self.since is None:
            return verb if left is None else "grown since the last visit"
        return "%s since %s" % (verb, self.since.isoformat())

    def _caption(self, canvas, plant, record) -> None:
        """Everything under the drawing: the same for every kind. It never prints the seed's rule."""
        left, right = PLATE_BOX[0], PLATE_BOX[2]
        room = right - left
        canvas.text(left, 984, _fitted(canvas, (DAGGER + " " if plant.dead else "") + plant.name, 34, room), 34)
        under = self.glass_words(plant.bed)          # a plate under glass shows the glass's day, and says which
        canvas.text(left, 1016, _fitted(canvas, "%s · %s%s" % (_kind_words(plant), plant.bed.name,
                                                              " · " + under if under else ""), 18, room), 18)
        if plant.dead:                             # its death on a line of its own: what is cut, if any, is the cause
            canvas.text(left, 1042, _fitted(canvas, self.planted_words(plant), 18, room), 18)
            when, how, stood = self.death_parts(plant)
            how = _fitted(canvas, how, 18, room - canvas.text_width(when + stood, 18)) if how else ""
            canvas.text(left, 1066, _fitted(canvas, when + how + stood, 18, room), 18)
            y = 1096
        else:
            age = self.age_words(plant)
            line = self.planted_words(plant) + (" · " + age if age else "")
            canvas.text(left, 1042, _fitted(canvas, line, 18, room), 18)
            y = 1072
        for note in record.notes[:3]:
            canvas.text(left, y, _fitted(canvas, note, 16, room), 16)
            y += 23
        base = 1172
        stamp = "drawn %s" % self.moment.strftime("%Y-%m-%d %H:%M")
        canvas.text(right, base, stamp, 14, "grey", "end")
        room -= canvas.text_width(stamp, 14) + 30
        x = left
        # A chip for each ink the drawing holds that needs its words: the planter's (only if something is drawn in
        # it: their name is in the line above in any case), the fresh ink, and the grey of what is dead.
        chips = [("wood", plant.by if record.has_ink("wood") else None), ("fresh", self.fresh_words(plant)),
                 ("dead", ("dead" if plant.dead else "dead parts") if record.has_ink("dead") else None)]
        for ink, words in chips:
            if not words or room < 60:
                continue
            canvas.rect(x, base - 12, 14, 14, ink)
            words = _fitted(canvas, words, 14, room - 22)
            used = 22 + canvas.text(x + 22, base, words, 14) + 26
            x += used
            room -= used

    # ---- a thing a creature made

    def thing(self, bed, name, maker, made):
        """Draw a thing a creature made (beds/<bed>/<name>) through its maker's `draw`, into <name>.png beside it.

        Laid out as a plate is: the drawing, and under it the thing's name,
        who made it and where, and when it was first made. Its lines are in
        the ink of the days, which bring the creatures. Returns the
        drawing's path, or None if it could not be written.
        """
        import plate
        path = bed.path / name
        text = _read(path, THING_MOST * 4)
        record = _Record()
        module = creature(self.root, maker)
        if module is None:
            record.trouble = "its maker, %s, cannot be read" % maker
        elif not callable(getattr(module, "draw", None)):
            record.trouble = "%s has no drawing for what it makes" % maker
        else:
            state_path = self.root / "ground" / "creatures" / maker
            ctx = CreatureCtx(maker, self.today, self.sky, "draw|%s" % name, self.weather_seed, self.soil,
                              _read(state_path, STATE_MOST * 10) if state_path.is_file() else "",
                              self.sky.remark or "", self.moment.hour)
            _, error, full = _ask(self.root, CREATURE + maker, "draw", "%s/%s" % (bed.name, name), module.draw,
                                  text, ctx, record)
            if error is not None:
                record.marks.clear()
                record.trouble = "could not be drawn: " + ("it stumbled (%s)" % error if isinstance(error, Stumbled)
                                                           else str(error))
                trouble(self.root, "%s/%s %s" % (bed.name, name, record.trouble), full, aloud=False)
            else:
                record.weigh()
                if record.cut_short:
                    record.notes = record.notes[:2] + [CUT_SHORT]
        canvas = plate.Canvas(900, 1200)
        canvas.inks["wood"] = FIXED_INKS[THE_DAYS]
        pen = canvas.specimen(PLATE_BOX, unit_px_max=_number(record.unit_px_max, 60.0), align=record.align)
        record.replay(pen)
        pen.settle()
        if record.trouble:
            canvas.text(450, 480, _fitted(canvas, record.trouble, 18, 780), 18, "dead", "middle")
        left, right = PLATE_BOX[0], PLATE_BOX[2]
        room = right - left
        canvas.text(left, 984, _fitted(canvas, name, 34, room), 34)
        canvas.text(left, 1016, _fitted(canvas, "made by %s · %s" % (maker, bed.name), 18, room), 18)
        lines = len([line for line in text.splitlines() if line.strip()])
        canvas.text(left, 1042, _fitted(canvas, "first made %s · %s" % (made.isoformat(), _count(lines, "line") + " of text"),
                                        18, room), 18)
        y = 1072
        for note in record.notes[:3]:
            canvas.text(left, y, _fitted(canvas, note, 16, room), 16)
            y += 23
        canvas.text(right, 1172, "drawn %s" % self.moment.strftime("%Y-%m-%d %H:%M"), 14, "grey", "end")
        canvas.text(left, 1172, "found by walking; not on the plan", 14, "grey")
        target = path.with_name(name + ".png")
        if not (canvas.save_png(target) or self._by_way_of_ground(canvas.save_png, target)):
            trouble(self.root, "the drawing of %s/%s could not be written" % (bed.name, name), canvas.trouble)
            return None
        return target

    # ---- the sheet of a bed

    def sheet(self, bed, force=False, partial=False):
        """Draw a bed's sheet: every plant in it, small, side by side.

        Returns its path; or None if it could not be written, or if the
        time for drawing ran out before every plant had its cell (a sheet
        is whole or it is not there). With `partial` (a look at the bed),
        a sheet on which time ran out is kept all the same: the plants not
        reached have an empty cell that says so, and the sheet is drawn
        again at the next look.
        """
        import plate
        growing = [p for p in self.garden() if p.bed.name == bed.name]
        target = bed.path / "sheet.png"
        mark = self.sheet_mark(bed, growing)
        if not force and target.is_file() and _read(bed.path / ".drawn", 200).strip() == mark:
            return target
        shown = growing[:SHEET_MOST]
        columns = _columns(len(shown))
        rows = max(1, -(-len(shown) // columns))
        cell_w = 1120.0 / columns
        cell_h = min(min(cell_w, 440.0) + 74.0, (1568.0 - 150.0 - 50.0) / rows)
        canvas = plate.Canvas(1200, int(150 + rows * cell_h + 50) if shown else 210)
        self._sheet_head(canvas, bed, growing)
        unreached = 0
        for i, plant in enumerate(shown):
            x, y = 40.0 + (i % columns) * cell_w, 150.0 + (i // columns) * cell_h
            if self.time_is_up() and plant.where not in self.records:
                if not partial:
                    return None
                unreached += 1
                self._cell_unreached(canvas, plant, x, y, cell_w, cell_h)
                continue
            self._cell(canvas, plant, x, y, cell_w, cell_h)
        self._sheet_foot(canvas, shown, len(growing) - len(shown))
        if not canvas.save_png(target):
            trouble(self.root, "the sheet of %s could not be written" % bed.name, canvas.trouble)
            return None
        if unreached:
            _remove(bed.path / ".drawn")               # not whole: it is drawn again next time
        else:
            _write(self.root, bed.path / ".drawn", mark + "\n")
        return target

    def _cell_unreached(self, canvas, plant, x, y, w, h) -> None:
        """A cell of the sheet for a plant there was no time to draw: its name, and that it was not drawn."""
        small = 12 if w < 200 else 13
        canvas.text(x + w / 2, y + (h - 68) / 2, _fitted(canvas, "not drawn in time", small, w - 24), small, "grey", "middle")
        canvas.inks["wood"] = ink_of(self.root, plant.by)
        canvas.rect(x + 10, y + h - 40, 10, 10, "wood")
        canvas.text(x + 26, y + h - 30, _fitted_name(canvas, plant, 16, w - 40), 16)
        canvas.text(x + 10, y + h - 12, _fitted(canvas, "drawn when looked at alone", small, w - 20), small, "grey")

    def _sheet_head(self, canvas, bed, growing) -> None:
        canvas.text(40, 56, _fitted(canvas, bed.name, 30, 1120), 30)
        lies = hands.line(bed.keys, "lies")
        if lies:
            canvas.text(40, 86, _fitted(canvas, lies, 16, 1120), 16)
        under = self.glass_words(bed)
        facts = "light %g · water %g · shelter %g · %s, room for %d%s · drawn %s" % (
            bed.light, bed.water, bed.shelter, _standing(growing), bed.room,
            " · %s (a week passes here at each visit)" % under if under else "", self.moment.strftime("%Y-%m-%d %H:%M"))
        canvas.text(40, 112, _fitted(canvas, facts, 14, 1120), 14, "grey")
        canvas.line(40, 130, 1160, 130, 1.5, "faint")
        if not growing:
            canvas.text(40, 170, "nothing is planted here", 16, "grey")

    def _sheet_foot(self, canvas, shown, not_shown) -> None:
        """Under the cells: whose ink is whose, what the fresh ink and the grey mean, and how many plants found no cell.

        Every plant on the sheet has a chip of its planter's ink by its
        name, the dead too, so every planter of a plant on the sheet is
        named here, whether their plants live or not.
        """
        items = []
        for plant in shown:
            if ("dot", ink_of(self.root, plant.by), plant.by) not in items:
                items.append(("dot", ink_of(self.root, plant.by), plant.by))
        if any(self.fresh_words(plant, ask=False) for plant in shown if not plant.dead):
            glassy = self.under is not None and any(plant.bed.glass for plant in shown)
            items.append(("dot", "fresh", "grown since %s" % self.since.isoformat() if self.since and not glassy
                          else "new, or grown since the last visit"))
        if any(plant.dead or (plant.where in self.records and self.records[plant.where].has_ink("dead")) for plant in shown):
            items.append(("dot", "dead", "dead"))
        if not_shown > 0:
            items.append(("", "grey", "and %d more, not drawn on this sheet" % not_shown))
        _legend(canvas, items, 40, canvas.height - 18, 1160, rows=1)

    def _cell(self, canvas, plant, x, y, w, h) -> None:
        """One plant in its cell of the sheet: the same drawing as its plate, smaller, with a bar to say how much smaller.

        Each plant is fitted to its own cell, so two plants side by side
        are not drawn to one scale. The small bar under each says what its
        own scale is; without it, height on a sheet would mean nothing.
        """
        box = (x + 10, y + 10, x + w - 10, y + h - 68)
        shrink = (box[3] - box[1]) / float(PLATE_BOX[3] - PLATE_BOX[1])
        record = self.record(plant)
        canvas.inks["wood"] = ink_of(self.root, plant.by)
        pen = canvas.specimen(box, unit_px_max=max(0.5, _number(record.unit_px_max, 60.0) * shrink),
                              align=record.align, scale_bar=False)
        pen.pens = min(1.0, max(0.3, shrink * 1.8))
        pen.labels = False
        record.replay(pen)
        _small_bar(canvas, x + 10, y + h - 56, w - 20, pen.settle(), _one_line(record.unit_name, 30))
        small = 12 if w < 200 else 13
        said = self.describe(plant)
        if record.trouble and record.trouble != said:          # (what the line under the name says is not said twice)
            canvas.text(x + w / 2, (box[1] + box[3]) / 2, _fitted(canvas, record.trouble, small, w - 24), small, "dead", "middle")
        canvas.rect(x + 10, y + h - 40, 10, 10, "wood")
        canvas.text(x + 26, y + h - 30, _fitted_name(canvas, plant, 16, w - 40), 16)
        canvas.text(x + 10, y + h - 12, _fitted(canvas, said, small, w - 20), small, "grey")

    # ---- the plan of the garden

    def plan(self):
        """Draw the garden from above. Returns the plan's path, or None if it could not be written."""
        import plate
        canvas = plate.Canvas(1400, 1000)
        garden = self.garden()
        every = beds(self.root)
        taken = [bed.at for bed in every if bed.at] + [spot for _, spot in _fixtures()]
        for bed in every:                                   # a bed not yet given a place still has to be shown
            if bed.at is None:
                bed.at = _free_place(taken, bed.name)
                taken.append(bed.at)
        canvas.text(PLAN_LEFT, 34, "The Glebe · %s" % _long_date(self.today), 26)
        under = next((self.glass_words(bed) for bed in every if bed.glass), "")
        canvas.text(PLAN_LEFT, 57, "%s. %s.%s" % (self.sky.words, self.sky.season.capitalize(),
                                                 " Under the glass it is %s." % under[len("under glass, "):] if under else ""),
                    15, "grey")
        self._plan_frame(canvas)
        inks, flags = {}, set()
        for bed in every:
            self._plan_bed(canvas, bed, [p for p in garden if p.bed.name == bed.name], inks, flags)
        self._plan_legend(canvas, inks, flags)
        target = self.root / "ground" / "plan.png"
        if not canvas.save_png(target):
            trouble(self.root, "the plan could not be written", canvas.trouble)
            return None
        canvas.save_svg(self.root / "ground" / "plan.svg")
        return target

    def _plan_frame(self, canvas) -> None:
        """The garden's edge with the gate in it, north, the shed and the heap."""
        x0, y0 = PLAN_LEFT, PLAN_TOP
        x1, y1 = x0 + 1000 * PLAN_SCALE, y0 + 700 * PLAN_SCALE
        middle = (x0 + x1) / 2
        canvas.polyline([(middle - 34, y1), (x0, y1), (x0, y0), (x1, y0), (x1, y1), (middle + 34, y1)], 2.0, "faint")
        for post in (middle - 34, middle + 34):
            canvas.dot(post, y1, 5, "ink")
        canvas.text(middle, y1 + 5, "gate", 14, "ink", "middle")
        canvas.line(x1 - 6, 52, x1 - 6, 22, 2.0, "ink")
        canvas.polyline([(x1 - 13, 32), (x1 - 6, 22), (x1 + 1, 32)], 2.0, "ink")
        canvas.text(x1 - 20, 42, "N", 16, "ink", "end")
        for name, (x, y, w, h) in _fixtures():
            px, py = x0 + x * PLAN_SCALE, y0 + y * PLAN_SCALE
            pw, ph = w * PLAN_SCALE, h * PLAN_SCALE
            if name == "shed":
                canvas.rect(px, py + 8, pw, ph - 16, "ink", filled=False, width=2.0)
                canvas.text(px + pw / 2, py + ph / 2 + 5, "shed", 14, "ink", "middle")
            else:
                things = len({where.split("/")[0] for where in _read_heap(self.root)})
                canvas.arc(px + pw / 2, py + ph - 14, pw / 2 - 8, 0, 180, 2.0, "ink")
                canvas.line(px + 4, py + ph - 14, px + pw - 4, py + ph - 14, 2.0, "ink")
                canvas.text(px + pw / 2, py + ph + 3, "heap · %s" % _count(things, "thing") if things else "heap", 13, "ink", "middle")

    def _plan_bed(self, canvas, bed, growing, inks, flags) -> None:
        """One bed on the plan: its outline, its name, and a mark for each plant.

        A grown plant is a dot in its planter's ink, larger for a larger
        plant (see `size_of`). A seed not yet up is a small hollow dot in
        the same ink; a dead plant, a hollow grey one. A ring in the fresh
        ink goes round a plant that is new or has something new in it since
        the last visit. No dot is larger than the bed's room allows each of
        its places, so a small crowded bed is not one smear of ink. Names
        are lettered only in a bed of NAMED_MOST plants or fewer, and only
        inside the bed (a fuller bed has its number beside its name: the
        plants that hold room in it, and the dead apart, after a †).
        """
        x, y, w, h = (v * PLAN_SCALE for v in bed.at)
        x, y = x + PLAN_LEFT, y + PLAN_TOP
        canvas.rect(x, y, w, h, "ink", filled=False, width=2.0)
        glassy = bool(self.glass_words(bed))
        if glassy:                                  # a second, lighter edge round the first: glass. (Outside it, where no
            canvas.rect(x - 5, y - 5, w + 10, h + 10, "faint", filled=False, width=1.5)     # plant's name is lettered.)
            flags.add("glass")
        lettered = len(growing) <= NAMED_MOST
        dead = sum(1 for plant in growing if plant.dead)
        title = bed.name if lettered else "%s · %d%s" % (bed.name, len(growing) - dead, " · %s%d" % (DAGGER, dead) if dead else "")
        title = _fitted(canvas, title, 15, max(40.0, w))
        canvas.text(x + 2, y - (12 if glassy else 7), title, 15)
        place = math.sqrt(max(1.0, (w - 28) * (h - 28)) / max(1, bed.room, len(growing)))    # the side of each place
        largest = max(4.0, min(30.0, 0.32 * place))
        placed = []
        for plant in growing:
            px = x + 14 + plant.at[0] * max(1.0, w - 28)
            py = y + 14 + plant.at[1] * max(1.0, h - 28)
            r = min(largest, 4 + 2.2 * math.log2(1 + self.size_of(plant))) if plant.has_body else 4.0
            placed.append((plant, px, py, r))
        title_box = (x + 2, y - 20, x + 2 + canvas.text_width(title, 15), y - 3)
        if not lettered or _letter_names(canvas, placed, (x, y, x + w, y + h), title_box):
            flags.add("unlettered")
        for plant, px, py, r in sorted(placed, key=lambda item: -item[3]):      # small dots over large ones
            canvas.dot(px, py, r + 1.5, "paper")            # a rim of clear paper: two dots that touch still read as two
            if plant.dead:
                canvas.dot(px, py, r, "dead", filled=False, width=2.0)
                flags.add("dead")
                continue
            ink = ink_of(self.root, plant.by)
            inks.setdefault(plant.by, ink)
            if not plant.has_body:
                canvas.dot(px, py, r, ink, filled=False, width=1.5)
                flags.add("seed")
                continue
            canvas.dot(px, py, r, ink)
            if self.changed(plant):
                canvas.dot(px, py, r + 5, "fresh", filled=False, width=2.5)
                flags.add("fresh")

    def _plan_legend(self, canvas, inks, flags) -> None:
        """Name every ink on the plan, and every mark that is not an ink."""
        items = [("dot", ink, name) for name, ink in inks.items()]
        if "fresh" in flags:
            items.append(("ring", "fresh", "new or changed since the last visit (%s)" % _short_date(self.since, self.today)
                          if self.since else "new"))
        if "seed" in flags:
            items.append(("seed", "grey", "a seed, not yet up"))
        if "dead" in flags:
            items.append(("hollow", "dead", "dead (beside a full bed's name, after †)"))
        if inks:
            items.append(("sizes", "grey", "a larger dot is a larger plant"))
        if "glass" in flags:
            items.append(("", "grey", "a doubled edge is glass: a week passes there at each visit"))
        if "unlettered" in flags:
            items.append(("", "grey", "a name is lettered where it finds room; look.py beds/<bed> names every plant"))
        _legend(canvas, items, PLAN_LEFT, 962, 1400 - PLAN_LEFT + 40, rows=3)


def _kind_words(plant) -> str:
    """A plant's kind as its plate and its look name it: 'twig', or with the variety its seed names, "twig 'Pale Moon'"."""
    variety = _one_line(hands.line(plant.seed, "variety"), 40).strip("'\"‘’“” ")
    return (plant.kind or "no kind") + (" '%s'" % variety if variety else "")


def _standing(growing) -> str:
    """'5 living plants', with the seeds not yet up and the dead counted beside them, not among them."""
    seeds = sum(1 for p in growing if not p.has_body)
    dead = sum(1 for p in growing if p.dead)
    words = _count(len(growing) - seeds - dead, "living plant")
    if seeds:
        words += ", %s not yet up" % _count(seeds, "seed")
    return words + (", %d dead" % dead if dead else "")


def _columns(plants_shown) -> int:
    """How many cells across a bed's sheet is, for that many plants: nearly square, a little wider than tall.

        plants   1   2   3-6   7-12   13-20   21-30   31-42   43-64
        across   1   2    3     4       5       6       7       8
    """
    if plants_shown <= 2:
        return max(1, plants_shown)
    return next(across for across in range(3, 9) if across * (across - 1) >= plants_shown or across == 8)


def _small_bar(canvas, left, y, room, scale, unit_name) -> None:
    """A short scale bar under one plant on a bed's sheet: a round number of its units, and how long that is here."""
    if not (isinstance(scale, (int, float)) and 0 < scale < 1e9):
        return
    units = _round_at_least(24.0 / scale)
    length = units * scale
    words = "%g %s" % (units, _unit_word(unit_name, units))
    if length + 6 + canvas.text_width(words, 12) > room:
        return                                         # no room to say it: better no bar than one that cannot be read
    canvas.line(left, y, left + length, y, 1.5, "grey")
    for end in (left, left + length):
        canvas.line(end, y - 3, end, y + 3, 1.5, "grey")
    canvas.text(left + length + 6, y + 4, words, 12, "grey")


def _unit_word(unit_name, units) -> str:
    """What a pen's unit is called for that many of them. "length, lengths" names one, then several (as plate.py reads it)."""
    one, comma, several = unit_name.partition(",")
    one, several = one.strip(), several.strip()
    if not (comma and one and several):
        return one or several
    return one if units == 1 else several


def _round_at_least(value) -> float:
    """The smallest of ... 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50 ... that is at least `value` (a number above zero)."""
    power = 10.0 ** math.floor(math.log10(value))
    return next(step * power for step in (1, 2, 5, 10) if step * power >= value * 0.999999)


def _legend(canvas, items, left, base, right, rows) -> None:
    """A row (or more) of small marks, each with its words: (shape, ink, words). What finds no room is left out."""
    x, y = left, base
    for shape, ink, words in items:
        width = (22 if shape else 0) + canvas.text_width(words, 14) + 26
        if x + width > right and x > left:
            rows -= 1
            if rows < 1:
                break
            x, y = left, y + 17
        if shape == "dot":
            canvas.dot(x + 7, y - 5, 6, ink)
        elif shape == "sizes":
            canvas.dot(x + 3, y - 4, 3, ink)
            canvas.dot(x + 13, y - 6, 6, ink)
        elif shape == "seed":
            canvas.dot(x + 7, y - 5, 4, ink, filled=False, width=1.5)
        elif shape:
            canvas.dot(x + 7, y - 5, 7, ink, filled=False, width=2.5 if shape == "ring" else 2.0)
        canvas.text(x + (24 if shape else 0), y, words, 14, "ink" if shape else ink)
        x += width


def _letter_names(canvas, placed, bed_box, title_box) -> int:
    """Letter the plants' names by their dots, each in the first place where it lies over nothing. Returns how many found none.

    A name stays inside its bed's outline, clear of it by a few pixels:
    out across an edge it would lie over the next bed's ground, or the
    path, and be read as theirs. It never lies over a dot, a dot's ring,
    another name or the bed's own. A name with nowhere to go is left off
    the plan, and is still to be read on the bed's sheet.

    Where dots crowd, a name may come to lie as near to a neighbour's dot
    as to its own. A place where that is not so is taken first; if there
    is none, a short tick is drawn from the name to the dot it belongs to.
    """
    margin = -3.0                                      # inside the outline, by this much (the outline is 2 px)
    as_near = 4.0                                      # pixels within which two dots are equally near to a name

    def over(a, b):
        return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])

    def edge_nearest(box, px, py):
        """The point of a name's box that is nearest to a dot's middle."""
        return min(max(px, box[0]), box[2]), min(max(py, box[1]), box[3])

    def gap(box, px, py, r):
        """How far a dot's rim is from a name's box."""
        x, y = edge_nearest(box, px, py)
        return max(0.0, math.hypot(px - x, py - y) - r)

    def unclear(box, own):
        """1 if some other dot is as near to the box as the name's own dot; else 0."""
        mine = gap(box, *own)
        return int(any(gap(box, qx, qy, qr) <= mine + as_near for _, qx, qy, qr in placed if (qx, qy, qr) != own))

    def tick(box, px, py, r):
        """A short line from a name's box to the rim of its dot."""
        x, y = edge_nearest(box, px, py)
        far = math.hypot(px - x, py - y)
        if far > r + 4:
            reach = (far - r - 2.5) / far
            canvas.line(x, y, x + (px - x) * reach, y + (py - y) * reach, 1.5, "ink")

    def strays(box, by=0.0):
        """0 if the box lies inside the bed (grown by `by` all round), 1 if it does not."""
        return int(box[0] < bed_box[0] - by or box[2] > bed_box[2] + by or box[1] < bed_box[1] - by or box[3] > bed_box[3] + by)

    def on_an_edge(box):
        return any(box[1] - 3 < edge < box[3] + 3 for edge in (bed_box[1], bed_box[3]))

    taken = [title_box] + [(px - r - 5, py - r - 5, px + r + 5, py + r + 5) for _, px, py, r in placed]
    left_off = 0
    for plant, px, py, r in placed:
        name = (DAGGER + " " if plant.dead else "") + _cut_in_the_middle(plant.name, 22)
        width = canvas.text_width(name, 13)
        places = [(px + r + 8, py + 5, "start"), (px - r - 8, py + 5, "end"),
                  (px, py + r + 17, "middle"), (px, py - r - 11, "middle"),
                  (px + r + 6, py + r + 14, "start"), (px + r + 6, py - r - 7, "start"),
                  (px - r - 6, py + r + 14, "end"), (px - r - 6, py - r - 7, "end"),
                  (px, py + r + 33, "middle"), (px, py - r - 27, "middle")]
        free = []                  # (does it cross the bed's edge, is another dot as near, where to letter, the room it takes)
        for tx, ty, anchor in places:
            x0 = tx if anchor == "start" else tx - width if anchor == "end" else tx - width / 2
            box = (x0, ty - 11, x0 + width, ty + 4)
            if not strays(box, margin) and not on_an_edge(box) and not any(over(box, other) for other in taken):
                free.append((strays(box), unclear(box, (px, py, r)), (tx, ty, anchor), box))
        if not free:
            left_off += 1
            continue
        _, doubtful, (tx, ty, anchor), box = min(free, key=lambda place: place[:2])    # inside the bed, and clear, if it can be
        canvas.text(tx, ty, name, 13, "ink", anchor, halo=True)
        if doubtful:
            tick(box, px, py, r)
        taken.append(box)
    return left_off


def _cut_in_the_middle(name, most) -> str:
    """A long name with its middle left out. Its end is kept: that is what tells one seedling from the next.

    first-twig-seedling-xiv  ->  first-twig-seedli…-xiv
    """
    if len(name) <= most:
        return name
    dash = name.rfind("-")
    tail = name[dash:] if 0 <= dash and len(name) - dash <= 8 else name[-5:]
    return name[:max(1, most - 1 - len(tail))].rstrip("-") + "…" + tail


def _fitted_name(canvas, plant, size, room) -> str:
    """A plant's name (with † if it is dead) made to fit `room` pixels at that size, its middle left out if it must be.

    evensong-seedling-xiv  ->  evensong-se…-xiv   (the end is what tells one seedling from the next)
    """
    head = DAGGER + " " if plant.dead else ""
    if canvas.text_width(head + plant.name, size) <= room:
        return head + plant.name
    for most in range(len(plant.name) - 1, 1, -1):
        cut = _cut_in_the_middle(plant.name, most)
        if canvas.text_width(head + cut, size) <= room:
            return head + cut
    return _fitted(canvas, head + plant.name, size, room)


def _fitted(canvas, text, size, room) -> str:
    """A text cut short with … until it fits in `room` pixels at that size."""
    text = _one_line(text, 400)
    if canvas.text_width(text, size) <= room:
        return text
    while len(text) > 1 and canvas.text_width(text + "…", size) > room:
        text = text[:max(1, int(len(text) * 0.9))].rstrip() if len(text) > 12 else text[:-1]
    return text.rstrip() + "…"


def _number(value, otherwise) -> float:
    """A kind's number (a pen's unit_px_max) as a sane float, or `otherwise`."""
    try:
        value = float(value)
    except (TypeError, ValueError, OverflowError):
        return otherwise
    return value if value == value and 0 < value < 1e9 else otherwise


def draw_plant(root, plant, force=False):
    """Draw one plant's plate if it is stale (or `force`). Returns the plate's path, or None."""
    return _Studio(root).plate(plant, force)


def draw_bed(root, bed):
    """Draw one bed's sheet. Returns its path."""
    return _Studio(root).sheet(bed, force=True)


def draw_plan(root):
    """Draw the plan of the garden. Returns its path."""
    return _Studio(root).plan()


def _draw_everything(root, budget, force=False) -> dict:
    """The plan, then bed by bed its stale plates and its sheet, as far as `budget` seconds reach.

    A bed's sheet follows its plates at once: the plates have already
    asked each kind for its drawing, so the sheet costs little more than
    the ink. When the time runs out, every drawing a kind has made by then
    is on its plate; nothing that was drawn is thrown away. What is stale
    and could not be redrawn in time is removed: no stale drawing is ever
    left on show. `look` draws it when it is asked for.

    The beds are taken in turn (`_in_turn`): where one drawing ran out of
    time, the next begins, so a bed too slow to be finished does not keep
    the beds after it undrawn for ever.

    The things creatures made are not drawn here (they are found by
    walking, and drawn when looked at); a stale drawing of one is taken
    away.
    """
    studio = _Studio(root)
    _guarded(root, "taking stale drawings of things away", _things_stale_away, root, studio.today)
    studio.until = time.monotonic() + budget
    done = {"plates": 0, "sheets": 0, "left": 0}
    guarded = lambda draw, *a: _guarded(root, "a drawing", draw, *a)
    if budget > 0:
        guarded(studio.plan)
    reached = ""                                   # the last bed that had any of the time
    order = _in_turn(root, beds(root))
    for bed in order:
        growing = [p for p in studio.garden() if p.bed.name == bed.name]
        if not studio.time_is_up():
            reached = bed.name
        for plant in growing:
            if not force and guarded(studio.is_current, plant):
                continue
            if not studio.time_is_up():
                done["plates"] += 1 if guarded(studio.plate, plant, True) else 0
            else:
                for name in ("plate.png", "plate.svg", ".drawn"):
                    _remove(plant.path / name)
                done["left"] += 1
        if not studio.time_is_up() and guarded(studio.sheet, bed, force):
            done["sheets"] += 1
        elif _read(bed.path / ".drawn", 200).strip() != guarded(studio.sheet_mark, bed, growing):
            _remove(bed.path / "sheet.png")
    if not studio.time_is_up():
        _remove(_turn_file(root))                  # every bed was reached: the next drawing begins at the beginning
    elif reached:
        _write(root, _turn_file(root), _next_turn(order, reached) + "\n")
    return done


def _turn_file(root) -> Path:
    return Path(root) / "ground" / ".turn"


def _in_turn(root, every) -> list:
    """The beds in the order they are drawn: by name, beginning with the bed ground/.turn names.

    That file is there only while drawing is behind: it names the bed the
    next drawing is to begin with (see `_next_turn`).
    """
    first = _read(_turn_file(root), 1000).strip()
    if not first:
        return every
    return [bed for bed in every if bed.name >= first] + [bed for bed in every if bed.name < first]


def _next_turn(order, reached) -> str:
    """The bed the next drawing begins with, when this one (in `order`) ran out of time in the bed `reached`.

    It begins with that same bed, which was left unfinished. But if this
    drawing began with it too, the bed is more than one drawing can
    finish: then the next begins with the bed after it, so that it does
    not keep every other bed waiting.
    """
    names = [bed.name for bed in order]
    if reached != names[0]:
        return reached
    return names[(names.index(reached) + 1) % len(names)]


def _guarded(root, what, step, *arguments):
    """Run one step of a door. If it fails, the trouble is written down and the door goes on."""
    try:
        return step(*arguments)
    except KeyboardInterrupt:
        raise
    except BaseException as error:
        trouble(root, "%s went wrong: %s" % (what, _one_line(error) or type(error).__name__), error)
        return None


# ================================================================ the bolt
#
# One door at a time. While a door works it holds a lock on ground/.door,
# and a second door that comes meanwhile waits a little and then says that
# the garden is in use. Without this, two arrivals that overlap would both
# live the same days, and a visitor whose first `arrive` was slow would
# start a second one on top of it.
#
# The lock is the operating system's own, held on an open file. When the
# door's process ends, however it ends, the system lets go of it: no run
# that is cut short can leave the garden bolted.

LOCK_AT = 1 << 30         # the byte that is locked: far past anything ever written in the file


def _hold(handle) -> bool:
    """Take the system's lock on an open file, without waiting. False if another process holds it."""
    try:
        if msvcrt is not None:
            handle.seek(LOCK_AT)
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        elif fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except (OSError, ValueError):
        return False


def _let_go(handle) -> None:
    try:
        if msvcrt is not None:
            handle.seek(LOCK_AT)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        elif fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    except (OSError, ValueError):
        pass


class _Bolt:
    """The bolt a door shoots while it works. Use it with `with`; `shot` says whether the garden is this door's.

    `doing` is what a second door will be told is going on ("fable-5 is
    coming in"). If no lock is to be had at all (the ground is a file, the
    disk is read-only) the door goes on unbolted: the gate always opens.
    """

    def __init__(self, root, doing, wait):
        self.handle = None
        self.held_by = ""                 # what the door that holds the bolt says it is doing
        self.shot = self._shoot(Path(root) / "ground" / ".door", doing, wait)

    def _shoot(self, path, doing, wait) -> bool:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            self.handle = open(path, "a+b")
        except OSError:
            return True
        patience = time.monotonic() + wait
        while not _hold(self.handle):
            if time.monotonic() > patience:
                self.held_by = _one_line(_read(path, 300), 120) or "another door is open"
                self.handle.close()
                self.handle = None
                return False
            time.sleep(0.1)
        try:
            self.handle.truncate(0)
            self.handle.write(("%s, since %s\n" % (doing, datetime.datetime.now().strftime("%H:%M:%S"))).encode("utf-8", "replace"))
            self.handle.flush()
        except OSError:
            pass
        return True

    def __enter__(self):
        return self

    def __exit__(self, *error) -> None:
        if self.handle is not None:
            _let_go(self.handle)
            self.handle.close()
            self.handle = None


# =================================================================== apart
#
# A kind is a program some visitor wrote, and the ground cannot know what
# it will do. Inside one process a kind can be interrupted if it loops in
# Python and timed if it dawdles (see `_call`). But one that never comes
# back from a regular expression, or that ends the process outright, would
# take the door with it, and the gate would not open.
#
# So a door runs no kind itself. It starts a second process, a hand, and
# asks it to do each part of the work that touches kinds: tending, the
# days, drawing. While the hand works the door watches. Before each call
# into a kind the hand writes a crumb saying which kind and which plant. If
# the hand then falls silent for longer than that call is allowed, or is
# gone altogether, the door ends it, reads the crumb, sets that kind aside
# for the rest of this pass, finishes whatever writing was cut short, and
# asks again with a new hand, for as long as its patience lasts. The gate
# opens either way, and the note says which kind it was. A kind whose days
# or seeds did not come back stays aside at the doors that follow as well
# (ground/aside), so it is waited out once, not at every arrival.

APART = True              # False: a door runs kinds in its own process after all (for trials that want one process)
APART_GRACE = 2.0         # seconds past a kind's own time before the door ends the hand from outside
APART_MOST = 150.0        # seconds one request may take in all, whatever the hand is doing
APART_PATIENCE = 30.0     # seconds a door may lose waiting on kinds that never come back (setting one aside each time and
                          # asking anew) before it gives that part of its work up for now
CRUMB_BYTES = 256

_crumb = None             # in a hand: the crumb it writes
_hands = {}               # in a door: root -> the hand it keeps


class _Crumb:
    """ground/.calling: a few bytes that say which kind is being asked at this instant, and about which plant.

    The hand writes it before and after every call into a kind; the door
    reads it when the hand has been silent too long. The file is mapped
    into memory, so writing it costs the days next to nothing.

    The hand also keeps a lock on the file for as long as it lives. By that
    a later door can tell that the hand of an earlier door, one that was
    cut off, is still at work, and end it before it starts its own.
    """

    def __init__(self, root):
        path = Path(root) / "ground" / ".calling"
        if not path.is_file() or path.stat().st_size != CRUMB_BYTES:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "wb") as handle:
                handle.write(b" " * CRUMB_BYTES)
        self.handle = open(path, "r+b")
        self.map = mmap.mmap(self.handle.fileno(), CRUMB_BYTES)
        self.calls = 0

    def say(self, what, name, where) -> None:
        """Note that the kind `name` is being asked for `what` about the plant at `where` ('' for all three: nothing is)."""
        self.calls += 1
        text = "%d|%d|%s|%s|%s" % (os.getpid(), self.calls, what, name, where)
        self.map[:] = text.encode("utf-8", errors="replace")[:CRUMB_BYTES].ljust(CRUMB_BYTES)

    def read(self):
        """(pid, number of the call, what, kind, where) as last written, or None if nothing can be made of it."""
        try:
            pid, calls, what, name, where = bytes(self.map[:]).decode("utf-8", errors="replace").rstrip().split("|", 4)
            return int(pid), int(calls), what, name, where
        except ValueError:
            return None

    def close(self) -> None:
        try:
            self.map.close()
            self.handle.close()
        except (OSError, ValueError):
            pass


_crumb_now = ["", "", ""]     # what the crumb says at this moment: a call inside another gives it back after (see `_ask`)


def _say_crumb(what, name, where) -> None:
    _crumb_now[:] = [what, name, where]
    if _crumb is not None:
        _crumb.say(what, name, where)


class _Hand:
    """A hand as the door holds it: the process, the pipe it answers on, and the crumb it leaves."""

    def __init__(self, root):
        self.root = Path(root)
        try:
            self.crumb = _Crumb(root)
        except (OSError, ValueError):
            self.crumb = None                      # no crumb: the hand can still work, but cannot be watched so closely
        self._end_stray_hand()
        # A program given with -c finds modules in the folder the visitor stands in before anywhere else. That
        # folder is taken off the hand's path: a kind called random.py, met by someone standing in species/, must
        # not be loaded where the library's own `random` was meant.
        afresh = ("import sys; sys.path[:] = [sys.argv[1]] + [folder for folder in sys.path if folder]; "
                  "import ground; ground._hand_main(sys.argv[2])")
        self.process = subprocess.Popen([sys.executable, "-B", "-c", afresh, str(SHED), str(self.root)],
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.answers = queue.Queue()
        threading.Thread(target=self._listen, name="glebe-listen", daemon=True).start()

    def _end_stray_hand(self) -> None:
        """If the hand of an earlier door is still at work (that door was cut off), end it: the garden is this door's now."""
        if self.crumb is None:
            return
        for tenth in range(70):
            if _hold(self.crumb.handle):
                _let_go(self.crumb.handle)
                return
            if tenth == 20:                        # two seconds were given it to finish by itself
                calling = self.crumb.read()
                try:
                    os.kill(calling[0], signal.SIGTERM)
                except (OSError, TypeError, ValueError):
                    pass
            time.sleep(0.1)

    def _listen(self) -> None:
        """Put each answer the hand sends on the queue; and None when the hand is gone."""
        out = self.process.stdout
        try:
            while True:
                head = out.read(8)
                if len(head) < 8:
                    break
                self.answers.put(out.read(struct.unpack(">Q", head)[0]))
        except (OSError, ValueError):
            pass
        self.answers.put(None)

    def ask(self, request, until=None) -> tuple:
        """Send one request and wait for its answer, watching the crumb meanwhile.

        Returns (the answer, None). Or (None, the crumb) if the hand fell
        silent inside a kind or died there; or (None, None) if it failed
        with no kind in hand, or was still at work at `until` (a moment on
        time.monotonic()) or after APART_MOST seconds.
        """
        try:
            self.process.stdin.write(json.dumps(request).encode("ascii") + b"\n")
            self.process.stdin.flush()
        except (OSError, ValueError):
            return None, None
        began = since = time.monotonic()
        seen = None
        while True:
            try:
                answer = self.answers.get(timeout=0.2)
            except queue.Empty:
                calling, moment = self._calling(), time.monotonic()
                if calling != seen:
                    seen, since = calling, moment
                elif calling and moment - since > KIND_SECONDS.get(calling[2], 8.0) + APART_GRACE:
                    return None, calling
                if moment - began > APART_MOST or (until is not None and moment > until):
                    return None, None
                continue
            if answer is None:
                return None, self._calling()
            try:
                return pickle.loads(answer), None
            except Exception:
                return None, None

    def _calling(self):
        """The crumb, if this hand wrote it and it names a call into a kind; else None."""
        calling = self.crumb.read() if self.crumb is not None else None
        return calling if calling and calling[0] == self.process.pid and calling[2] else None

    def dismiss(self, at_once=False) -> None:
        """Let the hand go: it ends by itself when the door stops speaking to it. `at_once`: it is not waited for."""
        try:
            if at_once:
                self.process.kill()
            self.process.stdin.close()
            self.process.wait(timeout=5)
        except (OSError, ValueError, subprocess.SubprocessError):
            try:
                self.process.kill()
                self.process.wait(timeout=5)
            except (OSError, subprocess.SubprocessError):
                pass
        if self.crumb is not None:
            self.crumb.close()


_given_up = {}            # root -> why the last step given up was given up, in words (for the note's own lines)


def _apart(root, step, *arguments, until=None):
    """Have one part of a door's work done by a hand. Returns what it gave back; None if it could not be done.

    `step` names one of _STEPS; its arguments must be plain (text, numbers,
    true or false, None), since they cross to another process. `until` is
    the moment (on time.monotonic()) by which the door must have this part
    back, whatever the hand is doing: an arrival keeps within ARRIVAL_MOST
    seconds, patience with hanging kinds included.

    What the hand learns about kinds that hang is written down (ground/aside,
    ground/.visit) the moment a kind is set aside, not when the door ends:
    a door that is itself cut short a minute later has still not waited for
    nothing.
    """
    if not APART or not sys.executable:
        return _guarded(root, _STEP_WORDS[step], _STEPS[step], root, *arguments)
    key = str(root)
    _given_up.pop(key, None)
    waited, left_behind = 0.0, []                  # the seconds lost to kinds that never came back, and which they were
    while waited <= APART_PATIENCE:                # each time round, one more kind is set aside
        if until is not None and time.monotonic() > until - 1.0:
            break                                  # no time is left to ask again
        if key not in _hands:
            try:
                _hands[key] = _Hand(root)
            except (OSError, ValueError):          # no second process is to be had: the work is done here after all
                return _guarded(root, _STEP_WORDS[step], _STEPS[step], root, *arguments)
        asked = time.monotonic()
        answer, calling = _hands[key].ask(_request(root, step, arguments), until)
        if answer is not None:
            answer = _taken_in(root, step, answer)
            _keep_what_was_learnt(root)
            return answer
        moment = time.monotonic()
        _hands.pop(key).dismiss(at_once=True)
        _guarded(root, "finishing what was cut short", _finish_passing, root)
        if calling is None:
            if until is not None and moment >= until:
                said = "%s was cut short: it was still at work when the door's time was up" % _STEP_WORDS[step]
            elif moment - asked >= APART_MOST:
                said = "%s was cut short: it took longer than %d seconds" % (_STEP_WORDS[step], APART_MOST)
            else:
                said = "%s was cut short: the hand doing it ended without an answer" % _STEP_WORDS[step]
            _given_up[key] = said
            trouble(root, said, aloud=step not in _TOLD_IN_NOTE)
            return None
        _, _, what, name, where = calling
        waited += KIND_SECONDS.get(what, 8.0) + APART_GRACE
        if _count_stop(root, name, what, where, weight=STOPS_MOST):     # a hand ended inside a kind: once is enough
            left_behind.append(where)
            trouble(root, "%s, of %s, was set aside: %s" % (where, _program_words(name), _too_much(what)),
                    aloud=step not in _TOLD_IN_NOTE)           # of the days, the note says it among what happened in them
        else:
            _aside[(key, name)] = what
            left_behind.append(name)
            trouble(root, "%s was set aside: %s%s"
                    % (_program_words(name), _late(what, "its"), " (it was being asked about %s)" % where if where else ""),
                    aloud=step not in _TOLD_IN_NOTE)
        _keep_what_was_learnt(root)
    said = "%s was given up for now: %s" % (_STEP_WORDS[step], "kind after kind did not come back (%s)"
                                            % ", ".join(left_behind) if left_behind else "the door's time was up")
    _given_up[key] = said
    trouble(root, said, aloud=step not in _TOLD_IN_NOTE)      # (the days' give-up is said among the days' own lines)
    return None


def _keep_what_was_learnt(root) -> None:
    """Write down at once which kinds are set aside, for this visit and for the arrivals after it."""
    _guarded(root, "remembering the kinds set aside", _remember_aside, root)
    _guarded(root, "remembering what this visit has met", _remember_visit, root)


def _request(root, step, arguments) -> dict:
    """What a door sends its hand: the step and its arguments, and what the door knows that the hand must know too.

    That is the time each call into a kind is allowed, the kinds that
    stand aside (and which of those the almanac need not be told of
    again), and the troubles already written down, so that the hand does
    not write one of them into the log a second time.
    """
    key = str(root)
    return {"step": step, "arguments": list(arguments), "limits": KIND_SECONDS,
            "aside": {name: what for (where, name), what in _aside.items() if where == key},
            "told": sorted(name for where, name in _told_aside if where == key),
            "logged": sorted(_logged)} | _stops_told(key)


def _stops_told(key) -> dict:
    """The stops a door and its hand pass to each other: which plants sleep alone, how often each call was stopped,
    and on which plants each kind set aside was stopped. (A hand may be ended and another begun in one door.)"""
    return {"alone": [[where, kind_name, what] for (root, where), (kind_name, what) in _plants_aside.items() if root == key],
            "stops": [[name, where, n] for (root, name, where), n in _stops.items() if root == key],
            "stopped_on": [[name, plants] for (root, name), plants in _stopped_on.items() if root == key]}


def _stops_taken(key, said) -> None:
    """Take in the stops the other side passed (see `_stops_told`)."""
    for where, kind_name, what in said.get("alone", []):
        _plants_aside[(key, where)] = (kind_name, what)
    for name, where, n in said.get("stops", []):
        _stops[(key, name, where)] = max(n, _stops.get((key, name, where), 0))
    for name, plants in said.get("stopped_on", []):
        _stopped_on[(key, name)] = list(plants)


def _taken_in(root, step, answer):
    """What a hand answered, taken into the door: its troubles, the kinds it set aside, and what it gave back."""
    for sentence in answer["troubles"]:
        if sentence not in said_troubles:
            said_troubles.append(sentence)
    _logged.update(answer["logged"])                # what the hand wrote in the log, the door does not write again
    for name, what in answer["aside"].items():
        _aside[(str(root), name)] = what
    _stops_taken(str(root), answer)
    if answer["failed"]:
        trouble(root, "%s went wrong" % _STEP_WORDS[step], answer["failed"])
    return answer["result"]


def _dismiss_hands() -> None:
    for key in list(_hands):
        _hands.pop(key).dismiss()


atexit.register(_dismiss_hands)


def new_run() -> None:
    """Forget what this process holds against kinds and has said of troubles, as a new door's process would.

    For trials that pass through many doors in one process.
    """
    _dismiss_hands()
    for kept in (said_troubles, _said_before, _logged, _stops, _aside, _plants_aside, _stopped_on, _told_aside,
                 _layers_kept, _days_layer, _left_out, _given_up):
        kept.clear()


# ---- what the hand does

def _hand_main(root) -> None:
    """The hand's whole life: answer the door's requests, one at a time, until the door stops speaking."""
    global _crumb
    answers = os.fdopen(os.dup(sys.stdout.fileno()), "wb")     # the door listens here, and only answers may go there:
    nowhere = os.open(os.devnull, os.O_WRONLY)                  # whatever a kind prints, by whatever means, goes nowhere
    os.dup2(nowhere, 1)
    os.dup2(nowhere, 2)
    sys.stdout = sys.stderr = _sink
    try:
        _crumb = _Crumb(root)
        _hold(_crumb.handle)
        _crumb.say("", "", "")
    except (OSError, ValueError):
        _crumb = None
    requests = queue.Queue()

    def hear():
        """Pass on what the door asks. When the door stops speaking (it is done, or it is gone) the hand ends at once."""
        for line in sys.stdin.buffer:
            requests.put(line)
        os._exit(0)                                 # even in the middle of the days: what was half written is mended later

    threading.Thread(target=hear, name="glebe-hear", daemon=True).start()
    while True:
        try:
            request = json.loads(requests.get())
        except ValueError:
            continue
        answer = _answer(root, request)
        try:
            data = pickle.dumps(answer)
        except Exception as error:                  # what was done cannot be told across: say that much
            data = pickle.dumps(dict(answer, result=None, failed="the answer could not be sent: %r" % error))
        answers.write(struct.pack(">Q", len(data)) + data)
        answers.flush()


def _answer(root, request) -> dict:
    """Do the one thing the door asked for, under the door's own limits and set-asides, and say how it went."""
    KIND_SECONDS.update(request["limits"])
    del said_troubles[:]
    _logged.update(request["logged"])
    _aside.clear()
    _aside.update({(str(root), name): what for name, what in request["aside"].items()})
    _told_aside.clear()
    _told_aside.update((str(root), name) for name in request["told"])
    for kept in (_plants_aside, _stops, _stopped_on):
        kept.clear()
    _stops_taken(str(root), request)
    result = failed = None
    try:
        result = _STEPS[request["step"]](root, *request["arguments"])
    except KeyboardInterrupt:
        raise
    except BaseException as error:
        failed = "".join(traceback.format_exception(type(error), error, error.__traceback__))
    return {"result": result, "failed": failed, "troubles": list(said_troubles), "logged": sorted(_logged),
            "aside": {name: what for (where, name), what in _aside.items() if where == str(root)}} | _stops_told(str(root))


def _step_tend(root, by) -> dict:
    did, up = _tend(root, by)
    return {"did": did, "up": up}


def _step_days(root, until, by_when) -> Summary:
    """The days, up to `until` (an ISO date), within what is left of the time before `by_when` (seconds since 1970)."""
    return let_days_pass(root, Date.fromisoformat(until), max(1.0, by_when - time.time()))


def _step_glass(root, by_when) -> Summary:
    """The days owed under the glass (see `let_glass_pass`), within what is left of the time before `by_when`."""
    return let_glass_pass(root, 0, max(1.0, by_when - time.time()))


def _step_present(root, day, hour, by_when) -> list:
    """The creatures there at the hour of an arrival (see `_presences`), asked until `by_when` (seconds since 1970)."""
    return _presences(root, Date.fromisoformat(day), int(hour), time.monotonic() + max(0.0, by_when - time.time()))


def _step_draw(root, by_when, force) -> dict:
    return _draw_everything(root, max(0.0, by_when - time.time()), force)


def _step_look(root, target, everything, by_when=None) -> list:
    return _look(root, target, everything, by_when)


_STEPS = {"tend": _step_tend, "days": _step_days, "glass": _step_glass, "present": _step_present, "draw": _step_draw,
          "look": _step_look}
_STEP_WORDS = {"tend": "tending", "days": "letting the days pass", "glass": "letting the days pass under the glass",
               "present": "meeting the creatures", "draw": "drawing", "look": "looking"}
_TOLD_IN_NOTE = ("days", "glass")     # the steps whose giving up the note tells among their own lines, not as a trouble


# =============================================================== the doors

def arrive(root, name, lift=False, draw=True, again=False, visit=None) -> str:
    """Open the gate for `name`. Returns the arrival note (or who holds the latch, or that the gate is in use).

    A name is a signature, not a session. An arrival under the name that
    is already on the latch is a new visit: the one before it is laid down
    in that name as left without closing the gate, and the note speaks of
    it as it would of anyone's. Only `again` says "this is still my visit":
    for a visitor who knows they came in earlier in this same session.

    `visit` is a token, for a door that brings visitors through the API:
    an arrival with a token goes on with the visit whose latch holds that
    token, and no other; if none does, it begins a new visit, and the latch
    holds the token from then on. `lift` lifts another visitor's latch.

    The order is ruled: the latch first, then tending, then settling, then
    the rest. A visitor turned back at the latch changes nothing. The whole
    arrival keeps within ARRIVAL_MOST seconds; what it has no time to draw,
    look draws.
    """
    root = Path(root)
    began = time.monotonic()
    name = visitor_name(name)
    with _Bolt(root, "%s is coming in" % name, wait=4.0) as bolt:
        if not bolt.shot:
            return "The gate is in use at this moment: %s.\nIt will be free shortly." % bolt.held_by
        return _arrive(root, name, lift, draw, again, _token(visit), began + ARRIVAL_MOST)


def _arrive(root, name, lift, draw, again, token, deadline) -> str:
    moment = now(root)
    latch = _guarded(root, "reading the latch", _latch, root)
    live = _is_live(latch, moment)
    theirs = live and latch["name"].casefold() == name.casefold()       # the latch bears this very name
    going_on = live and (latch["visit"] == token if token else again and theirs)
    if live and not going_on and not theirs and not lift:
        return _latch_words(latch, moment)         # turned back: nothing is changed
    if going_on:
        name = latch["name"]                       # a visit goes on under the name it came in with
    _guarded(root, "making the garden's folders", _make_folders, root)
    _guarded(root, "raking the gravel", _lay_other_places, root)
    _guarded(root, "finishing what was cut short", _finish_passing, root)
    if going_on:
        _guarded(root, "recalling what this visit has met", _recall_visit, root)
    else:
        _remove(_visit_file(root))                 # a new visit: every trouble is said anew
    _guarded(root, "recalling the kinds set aside", _recall_aside, root)
    untold = _guarded(root, "reading what was never told", _untold_words, root, moment) or []
    late = _guarded(root, "laying down days under the glass that were never laid down", _lay_down_stray_glass, root)
    stray = _guarded(root, "laying down days that were never laid down", _lay_down_stray_days, root, moment.date())
    tended = _apart(root, "tend", None, until=time.monotonic() + max(5.0, min(30.0, _left(deadline) - 45.0))) or {}
    fresh = _guarded(root, "reading what is new at the gate", _fresh_at_gate, root) or set()
    later = _guarded(root, "settling the last visit", _settle, root, latch, going_on, moment) or []
    visits = _guarded(root, "reading the visits", _visits, root) or []
    if not going_on:
        _guarded(root, "remembering how it was left", _remember_left, root, tended.get("up", []))
    summary = _guarded(root, "letting the days pass", _days_apart, root, moment.date(), deadline) or Summary()
    if summary.days:
        _guarded(root, "laying down the days", _lay_down, root, THE_DAYS, _days_message(summary))
    _guarded(root, "leaving the rings of hands", _leave_rings, root, later, moment.date())
    if stray:                                      # for the note, they belong with the days that passed since the last visit
        summary.first, summary.days, summary.earlier = stray[0], summary.days + stray[1], summary.earlier + stray[1]
        summary.last = summary.last or stray[0] + _days(stray[1] - 1)
    beginning = None                               # where this visit begins (see `_beginning_text`), for ground/.began
    if not going_on:
        if latch:
            _guarded(root, "writing the visits", _write_visit, root, moment, VISIT_OPEN, latch["name"])
        _guarded(root, "setting the latch", _set_latch, root, name, moment, token)
        _guarded(root, "writing the visits", _write_visit, root, moment, VISIT_IN, name)
        beginning = _guarded(root, "noting where this visit begins", _beginning_text, root, name, moment)
        _guarded(root, "choosing an ink", ink_of, root, name)
    parts = _guarded(root, "writing the note", _account_parts, root, moment, latch if going_on else None, visits,
                     summary, tended.get("did", []), fresh)
    if beginning:                                  # kept once the note has read where the last visit began
        _guarded(root, "noting where this visit begins", _write, root, _began_file(root), beginning)
    account = None
    if parts is not None:                          # kept from here on, in case the rest is cut short (see `_keep_untold`)
        account = untold + parts[0] + parts[1]
        _guarded(root, "keeping the note", _keep_untold, root, name, moment, account)
    # Then the glass: a week, when the gate has opened to a new visit. It comes after the garden's days are told and
    # their telling kept, so that an arrival cut short under the glass has still said what the garden's days did.
    if _guarded(root, "counting the visit under the glass", _owe_glass, root, 0 if going_on else GLASS_WEEK):
        glassed = _guarded(root, "letting the days pass under the glass", _glass_apart, root, deadline) or Summary()
        if glassed.days:
            changed = _guarded(root, "reading what the days under the glass wrote", _changes, root) or []
            _guarded(root, "laying down the days under the glass", _lay_down, root, THE_GLASS, _glass_message(glassed),
                     changed, _glass_paths(root, changed) + list(glassed.carried))
        if parts is not None:
            account = untold + _with_glass(root, parts[0], parts[1], glassed, bool(late))
            _guarded(root, "keeping the note", _keep_untold, root, name, moment, account)
    present = _meet_creatures(root, moment, deadline)
    drawn = {}
    if draw:
        drawn = _draw_at_arrival(root, deadline)
    note = (_guarded(root, "writing the note", _arrival_note, root, moment, account, drawn, present)
            if account is not None else None)
    _keep_what_was_learnt(root)
    if note:
        _remove(_untold_file(root))                # it is told now
    return note or "\n".join(["The Glebe · %s · %s" % (_long_date(moment.date()), moment.strftime("%H:%M")), "",
                              "The gate is open, but the note of this arrival could not be written."] + _trouble_words(root))


def _left(deadline) -> float:
    """Seconds left before a moment on time.monotonic()."""
    return deadline - time.monotonic()


def _meet_creatures(root, moment, deadline) -> list:
    """The creatures there at the hour of this arrival, a line each (at most PRESENT_MOST), for the note.

    Asked by a hand, as everything that runs a creature's code is, in a
    step of its own: a creature that hangs here costs a few seconds and
    its line, never the days or the drawing. With no creatures, nothing is
    asked at all.
    """
    if not creatures_there(root):
        return []
    room = min(8.0, _left(deadline) - TAIL_SECONDS - 12.0)
    if room < 1.0:
        return []
    return _apart(root, "present", moment.date().isoformat(), moment.hour, time.time() + room,
                  until=time.monotonic() + room + KIND_SECONDS["present"] + APART_GRACE) or []


def _draw_at_arrival(root, deadline) -> dict:
    """Draw what is stale, in the time the arrival has left. What finds no time is taken off show, for look to draw.

    The drawing is given at most DRAW_BUDGET seconds, and never so many
    that the arrival would run past its deadline: a plate already begun
    may take a kind's whole drawing time (KIND_SECONDS["draw"]) to finish.
    """
    room = min(DRAW_BUDGET, _left(deadline) - TAIL_SECONDS - KIND_SECONDS["draw"] - 2.0)
    drawn = None
    if room > 1.0:
        drawn = _apart(root, "draw", time.time() + room, False, until=deadline - TAIL_SECONDS)
    if drawn is None:                              # no time, or given up: still, nothing stale is left on show
        drawn = _guarded(root, "taking stale drawings away", _draw_everything, root, -1.0) or {}   # (no time: no kind is asked)
    return drawn


def _days_apart(root, until, deadline=None) -> Summary:
    """Let the days pass, by a hand. Returns what happened.

    If a first hand had to be stopped partway, the days it had already
    written down are counted in (`earlier`): they are in the almanac, though
    only the last hand's days are in the summary. If no day could be lived
    at all, the summary says how many wait, and why (`waiting`, `given_up`).

    The days have DAYS_BUDGET seconds, less whatever the arrival's
    deadline needs kept for the drawing and the note.
    """
    before = _last_lived(root, until)
    budget = DAYS_BUDGET
    if deadline is not None:
        budget = max(1.0, min(DAYS_BUDGET, _left(deadline) - 20.0 - TAIL_SECONDS))
    summary = _apart(root, "days", until.isoformat(), time.time() + budget,
                     until=None if deadline is None else deadline - TAIL_SECONDS)
    why = _given_up.get(str(root), "")
    summary = summary or Summary()
    after = _almanac_end(root, until)
    if after is not None and (before is None or after > before) and not summary.skipped:
        if not summary.days:                       # only stopped hands lived anything
            summary.last, summary.unfinished = after, after < until
        begun = before + ONE_DAY if before else _almanac_start(root) or after
        earlier = (after - begun).days + 1 - summary.days
        if earlier > 0:
            summary.first, summary.days, summary.earlier = begun, (after - begun).days + 1, earlier
    if why:                                        # the days were given up: the note says why, among the days' own lines
        summary.given_up = why
        if not summary.days:                       # and how many wait, if none could be lived
            laid = sky.place(root).get("laid")
            first = before + ONE_DAY if before else laid if isinstance(laid, Date) else until
            summary.waiting = max(0, (until - first).days + 1)
        elif summary.last and summary.last < until:
            summary.unfinished = True
    return summary


def _owe_glass(root, more) -> bool:
    """The gate has opened: the glass owes `more` days more (a week, to a new visit). True if a bed lies under glass.

    Written down at once, by the door itself and before any day is lived,
    so that a visit's week is owed whatever becomes of the arrival.
    """
    if not any(bed.glass for bed in beds(root)):
        return False
    under = glass(root)
    if under is None:
        return False
    owed = min(GLASS_OWED_MOST, under.owed + max(0, int(more)))
    visits = under.visits + (1 if more else 0)
    if (owed, visits) != (under.owed, under.visits) or not _glass_file(root).is_file():
        under.owed, under.visits = owed, visits
        _write(root, _glass_file(root), _glass_text(under))
    return True


def _glass_apart(root, deadline=None) -> Summary:
    """Let the days owed under the glass pass, by a hand. Returns what happened.

    They have GLASS_BUDGET seconds, less whatever the arrival's deadline
    needs kept for the drawing and the note. Days that find no time stay
    owed, and the next arrival lives them first.
    """
    budget = GLASS_BUDGET
    if deadline is not None:
        budget = max(1.0, min(GLASS_BUDGET, _left(deadline) - 32.0 - TAIL_SECONDS))
    before = glass(root)
    summary = _apart(root, "glass", time.time() + budget, until=None if deadline is None else deadline - TAIL_SECONDS)
    why = _given_up.get(str(root), "")
    summary = summary or Summary()
    after = glass(root)
    if before is not None and after is not None and after.stands > before.stands and not summary.days:
        summary.first, summary.last = before.stands + ONE_DAY, after.stands      # only a stopped hand lived anything: its
        summary.days = summary.earlier = (after.stands - before.stands).days     # days are written, and are laid down
    if why:                                        # the days were given up: the note says why, among their own lines
        summary.given_up = why
    if after is not None and (why or summary.earlier):
        summary.waiting = after.owed
    return summary


def _glass_message(summary) -> str:
    """'under the glass: 7 days, 2027-03-08 to 2027-03-14. 2 plants grew.'"""
    happened = summary.counts() or ("lived by a hand that was stopped; what happened is in the chronicle" if summary.earlier
                                    else "nothing stirred")
    return GLASS_LAYER % (_count(summary.days, "day"), summary.first.isoformat(), summary.last.isoformat(), happened)


def _glass_paths(root, changes) -> list:
    """Of the paths that differ from the last layer, those the days under the glass write: the glass's two records,
    and in the beds under glass the bodies that grew, the rings, the seedlings the days sowed there, and what the
    days took off a bed as they carried it to the heap."""
    names = {bed.name for bed in beds(root) if bed.glass}
    theirs = []
    for status, path in changes:
        parts = path.split("/")
        if path in ("ground/glass", "ground/under-glass"):
            theirs.append(path)
        elif parts[0] == "beds" and len(parts) == 3 and parts[1] in names and parts[2] == GLASS_WITNESS:
            theirs.append(path)                    # (where the witness is not left out of the layers)
        elif parts[0] == "beds" and len(parts) == 4 and parts[1] in names:
            if parts[3] == "rings" or "D" in status or (parts[3] == "body" and "?" not in status):
                theirs.append(path)
            elif "?" in status:                    # a new plant: the days' own if its tag says they brought it up
                tag = hands.read_keys(_read(Path(root) / "beds" / parts[1] / parts[2] / "tag", 100_000))
                if hands.line(tag, "by") == THE_DAYS:
                    theirs.append(path)
    return theirs


def _stray_paths(root, changes) -> set:
    """Of these changes, what days wrote that no layer holds yet: the glass's (its chronicle runs past its layers)
    and the garden's own (the almanac runs past the days' newest layer).

    As a rule there are none: days are laid down as they are lived, and
    days never laid down are laid down late before anything is settled. But
    a layer cannot always be laid (git stood locked for a moment), and then
    what the days wrote lies uncommitted beside what hands did. It is not
    a hand's doing: it is left out of the settling, earns no ring, and waits
    for the door that can lay it down in its own name.
    """
    theirs = set()
    if not _layers(root):
        return theirs
    paths = {path for _, path in changes}
    if "ground/under-glass" in paths:
        end, laid = _glass_chronicle_end(root), _glass_layer_end(root)
        if end and not (laid and laid >= end):
            theirs.update(_glass_paths(root, changes))
    if "ground/almanac" in paths:
        day = today(root)
        end, laid = _almanac_end(root, day), _days_layer_end(root, day)
        if end and not (laid and laid >= end):
            theirs.update(_written_by_days(root, changes))
    return theirs


def _lay_down_stray_glass(root) -> bool:
    """Days lived under the glass but never laid down go into a layer of their own, signed by the glass.

    That happens when the arrival that lived them was cut short before it
    could lay them down. They are known by the chronicle: it has changed
    since the last layer. Without this, the settling that follows would
    sign a week's growth under the glass in the name of whoever came next.
    """
    end, laid = _glass_chronicle_end(root), _glass_layer_end(root)
    if not end or (laid and laid >= end):          # the chronicle holds no day that the layers do not (a chronicle a hand
        return False                               # took away is no day lived: its going is nobody's doing, and waits)
    changes = _changes(root)
    if "ground/under-glass" not in [path for _, path in changes]:
        return False
    message = "under the glass: days up to %s, laid down late, by the next arrival." % end.isoformat()
    return _lay_down(root, THE_GLASS, message, changes, _glass_paths(root, changes))


def _glass_date(day) -> str:
    """A day under the glass as the note and the drawings say it: '14 March 2027'."""
    return "%d %s %d" % (day.day, MONTHS[day.month - 1], day.year)


def _glass_words(root, summary, late=False) -> list:
    """The arrival note's lines for the glass: where it is, what day it is there, and what passed under it.

    A week, at a new visit. When nothing passed (a visit going on), one
    line still says what day it is there. With no bed under glass, nothing.
    """
    names = ["beds/" + bed.name for bed in beds(root) if bed.glass]
    under = glass(root) if names else None
    if under is None or summary is None:
        return []
    where = "Under the glass (%s)" % _some_of(names, 3)
    stands = under.stands
    if not summary.days:
        if summary.waiting or summary.given_up:
            lines = ["%s, %s to be lived; none could be today. It is %s there."
                     % (where, _count(summary.waiting, "day waits", "days wait"), _glass_date(stands))]
            return lines + (["  " + _one_line(summary.given_up, 300)] if summary.given_up else [])
        return ["%s it is %s." % (where, _glass_date(stands))]
    if summary.days == GLASS_WEEK:
        lead = "%s a week passes at each visit." % where
    else:
        lead = "%s a week passes at each visit; this time %s passed." % (where, _count(summary.days, "day"))
    lines = ["%s It is %s there now:" % (lead, _glass_date(stands))]
    if summary.counts(faults=False):
        lines.append("  " + summary.counts(faults=False))
    lines += ["  " + words for words in _death_words(summary.died, stands)]
    for found, one, many in ((summary.ailing, "ailing: %s (its rings say why)", "ailing: %s (their rings say why)"),
                             (summary.asleep, "asleep: %s (its kind cannot be read)", "asleep: %s (their kinds cannot be read)"),
                             (summary.seeds, "still a seed: %s", "still seeds: %s")):
        if found:
            lines.append("  " + (one if len(found) == 1 else many) % _some_of(found))
    lines += ["  " + _event_words(when, where, what, stands) for when, where, what in _notable(summary, 3)]
    for name, what in summary.aside:
        lines.append("  %s was set aside: %s" % (_program_words(name), _late(what, "its")))
    if summary.unfinished or summary.waiting:
        lines.append("  the days under the glass are slow today: %s for the next arrival"
                     % _count(summary.waiting, "more waits", "more wait"))
        if summary.given_up:
            lines.append("  " + _one_line(summary.given_up, 300))
    if summary.earlier:
        lines.append("  these days were lived by a try that did not finish; what happened in them is in %s"
                     % _shown(root, _under_glass_file(root)))
    if late:
        lines.append("  days an earlier arrival lived there and never laid down were laid down now")
    if len(lines) == 1:
        lines.append("  nothing stirred")
    return lines


def _latch_words(latch, moment) -> str:
    since = latch["since"]
    day = "today" if since.date() == moment.date() else "yesterday" if (moment.date() - since.date()).days == 1 \
        else "on " + _short_date(since.date(), moment.date())
    return ("The gate is on the latch: %s is in the garden, since %s %s.\n"
            "If that visit is over, --lift lifts the latch." % (latch["name"], since.strftime("%H:%M"), day))


def _remember_left(root, new=()) -> None:
    """For every plant, keep the body as it stands now in `.left`: what the fresh ink is measured against.

    `new` are the plants that came up as the gate opened. They are new
    since the last visit, and a new plant has no `.left`.
    """
    for plant in plants(root):
        if not plant.has_body or plant.unfit or plant.where in new:
            continue
        left = plant.path / ".left"
        if not left.is_file() or _read(left) != plant.body:
            _write(root, left, plant.body)


def _days_message(summary) -> str:
    """'12 days, 2026-09-19 to 2026-09-30. 9 plants grew; 2 came up by themselves.'"""
    happened = "; ".join(part for part in (summary.counts(), summary.rotted_words()) if part) or "nothing stirred"
    return DAYS_LAYER % (_count(summary.days, "day"), summary.first.isoformat(), summary.last.isoformat(), happened)


def _arrival_note(root, moment, account, drawn, present=()) -> str:
    """The note a visitor reads at the gate: short, plain, and never an instruction.

    `account` is its middle (see `_account`), made before the drawing
    began; round it go the day and its sky, the creatures that are there
    at this hour (`present`, a line each, at most three), and where the
    pictures are.
    """
    day = moment.date()
    s = sky.sky_for(root, day)
    lines = ["The Glebe · %s · %s" % (_long_date(day), moment.strftime("%H:%M")), "",
             "Sky: %s. %s." % (s.words, s.season.capitalize())]
    if s.remark:
        lines.append("The keeper, of today: %s" % _one_line(s.remark, 200))
    lines += [_one_line(line, 160) for line in list(present or [])[:PRESENT_MOST] if isinstance(line, str) and line.strip()]
    lines += account + [""]
    where = ["The plan is at %s." % _shown(root, root / "ground" / "plan.png")]
    if (root / "ground" / "almanac").is_file():
        where.append("The days are in %s." % _shown(root, root / "ground" / "almanac"))
    if _under_glass_file(root).is_file():
        where.append("The glass's days are in %s." % _shown(root, _under_glass_file(root)))
    lines.append(" ".join(where))
    if drawn.get("left"):
        lines.append("%s not drawn yet; each is drawn when it is looked at." % _count(drawn["left"], "plate was", "plates were"))
    return "\n".join(lines + _trouble_words(root))


def _fresh_at_gate(root) -> set:
    """The files under gate/ and book/ that the layers have not seen as they are: new, or changed, since the last
    layer, whatever their dates."""
    return {path for status, path in _changes(root)
            if path.startswith(("gate/", "book/")) and any(mark in status for mark in "?A!M")}


def _account(root, moment, going_on, visits, summary, sown, fresh=(), glassed=None) -> list:
    """The middle of the arrival note, in lines: who came last, the days that passed, what passed under the glass,
    what was left at the gate."""
    before, after = _account_parts(root, moment, going_on, visits, summary, sown, fresh)
    return _with_glass(root, before, after, glassed)


def _with_glass(root, before, after, glassed, late=False) -> list:
    """An account's two parts with the glass's lines between them (see `_glass_words`)."""
    before = list(before)
    told = _guarded(root, "telling of the days under the glass", _glass_words, root, glassed, late) or []
    if glassed is not None and glassed.days and NOTHING_GREW in before:     # (something grew: under the glass)
        before[before.index(NOTHING_GREW)] = "No day has passed outdoors since; nothing has grown there."
    return before + told + list(after)


def _account_parts(root, moment, going_on, visits, summary, sown, fresh=()) -> tuple:
    """The account in two parts: (who came last, and the garden's days; what was left at the gate and in the book).
    The glass's lines go between them, once its week has passed."""
    day = moment.date()
    before = [visit for visit in visits if visit[1] == "in"]
    began = None                                   # where the last visit began (see `_beginning`)
    if before:
        began = _guarded(root, "reading where the last visit began", _beginning, root, before[-1][2], before[-1][0])
        began = began or _Began(before[-1][0], None, before[-1][0] + datetime.timedelta(minutes=1))
    if going_on:
        lines = ["The gate is already open under the name %s, since %s." % (going_on["name"], going_on["since"].strftime("%H:%M"))]
    elif before:
        last_moment, _, last_name = before[-1]
        lines = ["Last through the gate: %s, %s." % (last_name, _ago(last_moment, moment))]
        doings = _guarded(root, "reading the last layer", _last_doings, root, last_name, began) or []
        if doings:
            lines.append("  that visit: %s" % _in_short(doings, 5))
    else:
        lines = ["No one has been through the gate before."]
    lines.append("")
    lines += _days_words(root, day, summary, bool(before), bool(going_on), sown)
    since = "" if not before else " since then" if going_on else " since that visit began"
    left = []
    for folder, words in (("gate", "At the gate, left%s: %s"), ("book", "In the book, written%s: %s")):
        found = _written_since(root, folder, began, fresh)
        if found:
            left.append(words % (since, found))
    return lines, left + _undated_words(root, began, fresh)


def _undated_words(root, began, fresh=()) -> list:
    """A line for the note when the keeper's sky holds lines that no date could be read from.

    Such a line changes no day's sky, and without a word here it would
    vanish unseen. It is said once: by the arrival that finds gate/sky.txt
    written since the last visit began (as the layers say it, where they
    are kept; see `_written_since`).
    """
    path = Path(root) / "gate" / "sky.txt"
    if not path.is_file():
        return []
    if began is not None:
        layered = _layered_since(root, "gate", began)
        try:
            if layered is not None:
                if "gate/sky.txt" not in fresh and "gate/sky.txt" not in layered:
                    return []
            elif _garden_time(root, path.stat().st_mtime) <= began.since:
                return []
        except OSError:
            return []
    undated = [_one_line(line, 60) for line in sky.unread(root) if _one_line(line)]
    if not undated:
        return []
    return ["In gate/sky.txt, %s could not be dated: %s" % (_count(len(undated), "line"), _some_of(undated, 2))]


# ---- a note that was never handed over

def _untold_file(root) -> Path:
    return Path(root) / "ground" / ".untold"


def _keep_untold(root, name, moment, account) -> None:
    """Keep an arrival's account in ground/.untold until its note has been handed over.

    The account is made when the days have passed, and the drawing that
    follows can take half a minute. An arrival ended in that time (by a
    tool that has run out of patience) has said nothing, and the days it
    lived are never lived again: nobody would ever be told what happened
    in them. So the account waits here, and the next arrival, whoever it
    is, tells it first (`_untold_words`).
    """
    head = "%s|%s" % (moment.isoformat(timespec="minutes"), name)
    _write(root, _untold_file(root), "\n".join([head] + account) + "\n")


def _untold_words(root, moment) -> list:
    """What an arrival that was cut short had found and never said, as lines for the head of the next note. Else []."""
    lines = _read(_untold_file(root), 500_000).splitlines()
    when, _, name = lines[0].partition("|") if lines else ("", "", "")
    try:
        then = datetime.datetime.fromisoformat(when)
    except ValueError:
        return []
    if not name or not any(line.strip() for line in lines[1:]):
        return []
    lead = "The arrival of %s, %s, was cut short before its note was written. What it found:" % (name, _ago(then, moment))
    return [lead] + ["  " + line if line.strip() else "" for line in lines[1:]] + [""]


def _trouble_words(root) -> list:
    """What went wrong on the way through a door: a plain sentence each, and where the whole of it is written.

    What an earlier door of the same visit has said already is not said
    again. A part of the door's work given up comes first: it is the one
    trouble that changes what the visitor finds.
    """
    new = [sentence for sentence in said_troubles if sentence not in _said_before]
    new.sort(key=lambda sentence: 0 if " was given up for now" in sentence or " was cut short: " in sentence else 1)
    if not new:
        return []
    said = [sentence[:1].upper() + sentence[1:].rstrip(".") + "." for sentence in new[:2]]
    if len(new) > 2:
        said.append("And %s." % _count(len(new) - 2, "more trouble"))
    said[-1] += " The whole of it is in %s." % _shown(root, Path(root) / "ground" / "trouble.log")
    return said


def _ago(then, moment) -> str:
    """'12 days ago (18 September)', 'yesterday (29 September)', 'earlier today (09:14)'.

    And 'on 25 October' for a day that is still to come: a clock set back
    does not make a later day into today.
    """
    days = (moment.date() - then.date()).days
    if days == 0:
        return "earlier today (%s)" % then.strftime("%H:%M")
    when = _short_date(then.date(), moment.date())
    if days < 0:
        return "on %s" % when
    return "yesterday (%s)" % when if days == 1 else "%d days ago (%s)" % (days, when)


NOTHING_GREW = "No day has passed since; nothing has grown."


def _days_words(root, day, summary, anyone_before, going_on, sown) -> list:
    """The middle of the arrival note: the days that passed, and what happened in them."""
    sown = _sown_words(root, sown, anyone_before or going_on)
    if not summary.days:
        nothing = NOTHING_GREW
        if summary.waiting:
            nothing = "%s to be lived; none could be today." % _count(summary.waiting, "day waits", "days wait")
        why = ["  " + _one_line(summary.given_up, 300)] if summary.waiting and summary.given_up else []
        return [nothing] + why + ["  " + words for words in sown]
    laid = sky.place(root).get("laid")
    if going_on:
        lines = ["Since the gate was opened, %s passed:" % _count(summary.days, "day")]
    elif not anyone_before and summary.days == 1 and summary.first == laid:
        lines = ["The ground was laid today."]
    elif not anyone_before and isinstance(laid, Date) and summary.first == laid:
        lines = ["Since the ground was laid on %s, %s lived:" % (_short_date(laid, day),     # (its own day among them)
                                                              _count(summary.days, "day was", "days were"))]
    elif not anyone_before:
        lines = ["Since the ground was laid, %s passed:" % _count(summary.days, "day")]
    else:
        lines = ["While no one was here, %s passed:" % _count(summary.days, "day")]
    weather = _weather_words(day, summary)
    if weather and summary.days > 1 and not summary.earlier:
        lines.append("  " + weather)
    for words in [summary.counts(faults=False)] + sown:
        if words:
            lines.append("  " + words)
    lines += ["  " + words for words in _death_words(summary.died, day)]
    for found, one, many in ((summary.ailing, "ailing: %s (its rings say why)", "ailing: %s (their rings say why)"),
                             (summary.asleep, "asleep: %s (its kind cannot be read)", "asleep: %s (their kinds cannot be read)"),
                             (summary.seeds, "still a seed: %s", "still seeds: %s")):
        if found:
            lines.append("  " + (one if len(found) == 1 else many) % _some_of(found))
    lines += ["  " + _event_words(when, where, what, day)
              for when, where, what in _notable(summary, 3 + min(3, summary.days // 120))]
    if summary.rotted:
        lines.append("  " + summary.rotted_words())
    for name, what in summary.aside:
        lines.append("  %s was set aside: %s" % (_program_words(name), _late(what, "its")))
    if summary.slow:
        slow = summary.slow
        named = slow[0] if len(slow) == 1 else "%s and %s" % (", ".join(slow[:-1]), slow[-1])
        lines.append("  the kind%s %s %s slow: %s plants took turns to grow%s" % (
            "" if len(slow) == 1 else "s", named, "is" if len(slow) == 1 else "are", "its" if len(slow) == 1 else "their",
            ", and then waited for the next arrival" if summary.slow_waited else ""))
    if summary.earlier:
        lines.append("  %d of these days were lived by an earlier try that did not finish; what happened in them is in the almanac"
                     % summary.earlier)
    if summary.skipped:
        lines.append("  %s before that were too long ago to be lived" % _count(summary.skipped, "day"))
    if summary.unfinished:
        lines.append("  the days are slow today: the garden stands at %s, and the rest will pass at the next arrival"
                     % _short_date(summary.last, day))
        if summary.slowest:
            lines.append("  most of the time went to the kind %s: %.0f s" % (summary.slowest, summary.slowest_seconds))
        if summary.given_up:
            lines.append("  " + _one_line(summary.given_up, 300))
    if len(lines) == 1 and lines[0].endswith(":"):
        lines.append("  nothing stirred")
    return lines


def _event_words(when, where, what, seen_from) -> str:
    """One event as the note tells it, joined as the almanac joins it: the place, a colon, what happened, and the day.

        long-border/kite: the wind snapped off its newest number, 121 (the 23rd)
        bees: the nest is done for the year (5 October)           (a creature's line has no plant: where is '')
    """
    return "%s%s (%s)" % ("%s: " % where if where else "", what, _the_day(when, seen_from))


def _the_day(day, seen_from) -> str:
    """'the 24th' within the month we stand in, else '24 June' (with the year, if it is not this one)."""
    return _on_the(day, seen_from)[len("on "):]


def _weather_words(day, summary) -> str:
    """'rain on 5 of them, 31 mm; first frost on the 27th'."""
    if summary.rain_days:
        words = "rain on %d of them, %s mm" % (summary.rain_days, sky._millimetres(summary.rain_mm))
        if summary.snow_days:
            words += " (snow on %d)" % summary.snow_days
    else:
        words = "no rain"
    if summary.frosts:
        n = len(summary.frosts)
        if summary.first_frost:
            words += "; first frost %s" % _on_the(summary.frosts[0], day)
            words += ", %d frosty nights in all" % n if n > 1 else ""
        else:
            words += "; frost on %s" % _count(n, "night")
    return words


def _sown_words(root, sown, anyone_before) -> list:
    """The seeds that hands had planted and that came up as the gate opened, and the plants set in whole: a line each way.

    A visitor's are told as sown by hand. What one of the garden's own
    names signs is told under that name: `sown by an unseen hand before
    anyone came: north-wall/halo`. A seed written before its planter came
    through the gate has no visit to sign it (Ruling 2), and its planter
    learns so here, as it comes up, and not later from its tag.
    """
    when = "since then" if anyone_before else "before anyone came"
    said = []
    for mark, done in ((CAME_UP, "sown"), (PLANTED_WHOLE, "planted whole")):
        signed = {}
        for line in sown:
            if mark in line:
                where = line.split(mark)[0]
                signed.setdefault(_signed_as(root, where), []).append(where)
        said += ["%s by %s %s: %s" % (done, signer, when, _some_of(signed[signer]))
                 for signer in ("hand",) + OWN_NAMES if signer in signed]
    return said


def _signed_as(root, where) -> str:
    """Who planted a plant, as the arrival note tells it: one of the garden's own names if its tag gives one, else 'hand'."""
    by = " ".join(hands.line(hands.read_keys(_read(Path(root) / "beds" / where / "tag", 100_000)), "by").split())
    return next((name for name in OWN_NAMES if by.casefold() == name.casefold()), "hand")


def _some_of(names, most=4) -> str:
    """'a, b, c, d and 3 more'."""
    return ", ".join(names[:most]) + (" and %d more" % (len(names) - most) if len(names) > most else "")


def _death_words(died, seen_from) -> list:
    """A line for each way plants died: '27 died of frost, 30 December to 1 January: long-border/first-twig and 26 more'."""
    ways = {}
    for when, where, what in died:
        ways.setdefault(what, []).append((when, where))
    lines = []
    for what, found in sorted(ways.items(), key=lambda way: -len(way[1]))[:3]:
        told = what if what.startswith("died") else "died (%s)" % what
        first, last = found[0][0], found[-1][0]
        if len(found) == 1:
            lines.append("%s %s %s" % (found[0][1], told, _on_the(first, seen_from)))
            continue
        when = _on_the(first, seen_from) if first == last else _from_to(first, last, seen_from)
        lines.append("%d %s, %s: %s and %d more" % (len(found), told, when, found[0][1], len(found) - 1))
    return lines


LONG_AWAY = 60            # days away from which the note tells the first of each sort of event, not the latest
NOT_A_SHAPE = {"its", "the", "a", "an", "of", "and", "now", "has", "have", "had", "is", "are", "was", "were"}


def _notable(summary, most=3) -> list:
    """The few events worth a line in the arrival note, as (day, where, what), oldest first.

    Events are sorted by their shape, not their words (see `_shape`): the
    plant's kind and the first words of what happened, so that every bite
    slugs took of a drift is one sort, whatever word each bite took. The
    rarest sorts are told first; no plant is told of twice, and the
    creatures have at most a third of the lines (the garden is its plants).

    After a short absence the latest of each rare sort is told. After a
    long one (LONG_AWAY days or more) the time away is cut into as many
    stretches as there are lines to tell, and each stretch gives its
    rarest event, the earliest of equals: a year away is told by its
    seasons, its firsts and its oddities, not by its last few days. A
    founding day lived is always told, besides.

    Deaths and standing faults are not among them: each has a line of its
    own, always (see `_days_words`).
    """
    told = {(when, where) for when, where, _ in summary.died}
    sorts, candidates = {}, []
    for when, where, what in summary.events:
        if (when, where) in told or what == RING_WELL or what.startswith(
                (RING_AILING, RING_ASLEEP, RING_SEED, RING_PLANTED, RING_FOUND_DEAD) + SOWN_RINGS):
            continue
        shape = _shape(summary.kinds.get(where, ""), what)
        sorts.setdefault(shape, []).append((when, where, what))
        candidates.append((when, where, what, shape))
    picked = [(when, "", "%s since the ground was laid" % _years(years)) for when, years in summary.founded]
    named, creatures = set(), [max(1, most // 3)]

    def take(when, where, what) -> bool:
        if (where and where in named) or (not where and creatures[0] <= 0):
            return False
        picked.append((when, where, what))
        if where:
            named.add(where)
        else:
            creatures[0] -= 1
        return True

    if summary.days >= LONG_AWAY and candidates and summary.first and summary.last:
        span = max(1, (summary.last - summary.first).days + 1)
        for part in range(most):
            lo, hi = part * span / most, (part + 1) * span / most
            stretch = [c for c in candidates if lo <= (c[0] - summary.first).days < hi]
            for when, where, what, shape in sorted(stretch, key=lambda c: (len(sorts[c[3]]), c[0])):
                if take(when, where, what):
                    break
    else:
        for found in sorted(sorts.values(), key=lambda found: (len(found), -found[-1][0].toordinal())):
            if len(picked) >= most + len(summary.founded):
                break
            for when, where, what in reversed(found):
                if take(when, where, what):
                    break
    return sorted(picked)


def _shape(kind_name, what) -> str:
    """The sort of an event, for `_notable`: its plant's kind and its first two words that say something.

        bulb · 'came into flower on 2'                   ->  'bulb came into'
        drift · 'slugs ate lest'                         ->  'drift slugs ate'
        tally · 'the wind snapped off its newest number' ->  'tally wind snapped'
        (a creature's line: no kind) 'bees: the nest is done for the year' -> ' bees nest'
    """
    words = [word for word in re.findall(r"[^\W\d_]+", what.lower()) if word not in NOT_A_SHAPE]
    return "%s %s" % (kind_name, " ".join(words[:2]))


def _written_since(root, folder, began, fresh=()) -> str:
    """The files under gate/ (or book/) left there since a visit began (see `_beginning`); all of them if `began` is None.

    Where layers are kept, they say it, and file dates are not asked at
    all: a file is new if the layers had not seen it as it is when the
    gate opened (`fresh`), or if a layer laid down since that visit began
    brought it or changed it. A file the layers hold unchanged from before
    is not new, whatever its dates say: a copy of the whole garden (a
    backup, a new disk) gives every file a fresh date, and none of them is
    news. And what that visit's own arrival laid down, for the visit
    before it, is that earlier visit's news, told then, not again.

    Without layers, a file is dated by when it came to lie there (see
    `_lain`), not only by when it was last written: a photograph the keeper
    copies to the gate keeps the day it was taken, and is new at the gate
    all the same. It is new if it came strictly after the visit came in.
    """
    layered = _layered_since(root, folder, began) if began is not None else None
    found = []
    for path in _files_under(Path(root) / folder, 400):
        where = _rel(root, path)
        if began is None or where in fresh:
            found.append(where)
        elif layered is not None:
            if where in layered:
                found.append(where)
        else:
            written = _lain(root, path)
            if written is not None and written > began.since:
                found.append(where)
    return ", ".join(found[:5]) + (" and %d more" % (len(found) - 5) if len(found) > 5 else "")


def _layered_since(root, folder, began):
    """The paths under `folder` that a layer laid down since a visit began (see `_beginning`) brought or changed,
    as a set; None if no layers are kept (then the dates must say)."""
    if not _layers(root):
        return None
    if began.layer is not None:                    # the layers laid after the visit's beginning
        span = [began.layer + "..HEAD" if began.layer else "HEAD"]
    else:                                          # the layers laid strictly after the moment it came in
        span = []
    done = _git(root, "log", "-200", "--format=@%at", "--name-only", "--diff-filter=AMR", *span, "--", folder + "/")
    if done is None:
        return None
    found, recent = set(), False
    if done.returncode != 0:                       # (a garden with no layer yet has nothing laid since)
        return found
    for line in done.stdout.decode("utf-8", errors="replace").splitlines():
        if line.startswith("@") and line[1:].strip().isdigit():
            recent = bool(span) or _garden_time(root, int(line[1:].strip())) > began.since
        elif line.strip() and recent:
            found.add(line.strip())
    return found


def look(root, target=None, everything=False) -> str:
    """Draw what is asked for, and say where the picture is and what it shows."""
    root = Path(root)
    began = time.monotonic()
    with _Bolt(root, "someone is looking", wait=30.0) as bolt:
        if not bolt.shot:
            return "Nothing was drawn: the garden is in use at this moment (%s). It will be free shortly." % bolt.held_by
        deadline = began + LOOK_MOST
        _guarded(root, "finishing what was cut short", _finish_passing, root)
        _guarded(root, "recalling what this visit has met", _recall_visit, root)
        _guarded(root, "recalling the kinds set aside", _recall_aside, root)
        room = max(5.0, _left(deadline) - TAIL_SECONDS - KIND_SECONDS["draw"] - 2.0)
        lines = _apart(root, "look", None if target is None else str(target), bool(everything), time.time() + room,
                       until=deadline - TAIL_SECONDS) or ["Nothing could be drawn."]
        said = _trouble_words(root)
        _keep_what_was_learnt(root)
        return "\n".join(lines + ([""] + said if said else []))


PLAN_WORDS = ("", "plan", "beds", "ground", "ground/plan.png")       # what, given to look, means the whole garden
HERE = "."                # and this means wherever the visitor stands: a plant, a bed, or else the whole garden


def _look(root, target, everything, by_when=None) -> list:
    """What look does once the garden is its own: tend, draw, and say in lines where the picture is and what it shows.

    `by_when` (seconds since 1970) is when the drawing must stop: a look
    keeps within LOOK_MOST seconds, as an arrival keeps within its own.
    """
    root = Path(root)
    did = _guarded(root, "tending", tend, root) or []
    studio = _Studio(root)
    if by_when is not None:
        studio.until = time.monotonic() + (by_when - time.time())
    wanted = str(target or "").replace("\\", "/").strip().strip("/")
    if everything:
        lines = _look_everything(root, studio.until)
    elif wanted in PLAN_WORDS or (wanted == HERE and not _stands_in_a_bed(root)):
        lines = _look_plan(root, studio)
    else:
        found, thing = _find(root, str(target), studio.garden())
        if found == "bed":
            lines = _look_bed(root, studio, thing)
        elif found == "plant":
            lines = _look_plant(root, studio, thing)
        elif found == "thing":
            lines = _look_thing(root, studio, *thing)
        else:
            lines = [thing]
    if did:
        lines += ["", "Tended on the way: %s." % _in_short(did, 6)]
    return lines


def _stands_in_a_bed(root) -> bool:
    """Is the folder the visitor stands in a bed, or something inside one?"""
    try:
        return bool(Path.cwd().resolve().relative_to((Path(root) / "beds").resolve()).parts)
    except (OSError, ValueError):
        return False


def _find(root, target, garden):
    """What a visitor pointed at: ('plant', Plant), ('bed', Bed), ('thing', (Bed, its name, its maker, the day it was
    first made)) for a thing a creature made, or ('nothing', a sentence about it)."""
    wanted = target.replace("\\", "/").strip().strip("/")
    link = _link_on_the_way(root, wanted)
    if link:
        return "nothing", "%s is a link to somewhere else. The garden does not follow it, and draws nothing of it." % link
    tries = [Path(target), root / wanted, root / "beds" / wanted]
    beds_folder = (root / "beds").resolve()
    for path in tries:
        try:
            path = path.resolve()
            inside = path.relative_to(beds_folder).parts
        except (OSError, ValueError):
            continue
        if len(inside) == 2 and inside[1].endswith(".png") and _made_thing(root, inside[0], inside[1][:-4]):
            inside = (inside[0], inside[1][:-4])                  # the drawing of a thing: the thing is meant
            path = path.with_name(inside[1])
        if not path.exists() or not inside:
            continue
        for plant in garden:
            if len(inside) >= 2 and (plant.bed.name, plant.name) == inside[:2]:
                return "plant", plant
        bed = next((bed for bed in beds(root) if bed.name == inside[0]), None)
        if bed and len(inside) == 1:
            return "bed", bed
        made = _made_thing(root, inside[0], inside[1]) if bed and len(inside) == 2 else None
        if made:
            return "thing", (bed, inside[1]) + made
        named = "/".join(("beds",) + inside[:2])
        if any(part.startswith(".") for part in inside[:2]):
            return "nothing", "%s: a name that begins with a dot is not seen by the garden." % named
        if bed:
            return "nothing", _not_a_plant_words(named, path if len(inside) == 2 else path.parents[len(inside) - 3])
    named = [plant for plant in garden if plant.name == wanted.split("/")[-1]]
    if len(named) == 1:
        return "plant", named[0]
    if len(named) > 1:
        return "nothing", "There is more than one %s: %s." % (wanted, ", ".join("beds/" + p.where for p in named))
    things = [where for where in _read_made(root) if where.rsplit("/", 1)[1] == wanted.split("/")[-1]
              and _made_thing(root, *where.rsplit("/", 1))]
    if len(things) == 1:
        bed_name, name = things[0].rsplit("/", 1)
        bed = next((bed for bed in beds(root) if bed.name == bed_name), None)
        if bed:
            return "thing", (bed, name) + _made_thing(root, bed_name, name)
    if len(things) > 1:
        return "nothing", "There is more than one %s: %s." % (wanted, ", ".join("beds/" + where for where in things))
    if wanted == "compost":
        return "nothing", "That is the heap. Nothing is drawn there."
    if (root / wanted).exists() and wanted.split("/")[0] == "compost":
        return "nothing", "%s is on the heap. Nothing is drawn there." % wanted
    return "nothing", "There is nothing at %s to draw. The beds are: %s." % (
        target, ", ".join(bed.name for bed in beds(root)) or "none yet")


def _link_on_the_way(root, wanted) -> str:
    """If what was pointed at is a bed or a plant folder that leads out of the garden: its name from the root. Else ''."""
    for parts in (Path(wanted).parts, ("beds",) + Path(wanted).parts):
        for depth in (2, 3):
            if parts[:1] == ("beds",) and len(parts) >= depth:
                entry = Path(root).joinpath(*parts[:depth])
                if entry.is_dir() and _leads_elsewhere(entry):
                    return "/".join(parts[:depth])
    return ""


def _what_it_is(entry, made=None) -> str:
    """What a thing in a bed is, if it is not a plant: 'a stone', 'a body with no seed', 'a seed lying loose',
    'something ants made' ... (`made` is ground/made, read, if the caller has it.)"""
    try:
        if not entry.is_dir():
            maker = (made if made is not None else {}).get("%s/%s" % (entry.parent.name, entry.name), (None,))[0]
            if maker:
                return "something %s made" % maker
            loose = entry.name == "seed" or entry.name.endswith(".seed")
            return "a seed lying loose: it wants a folder of its own" if loose else "a loose file"
        if _leads_elsewhere(entry):
            return "a link to somewhere else: the garden does not follow it"
        under = [inside.name for inside in entry.iterdir() if not inside.name.startswith(".")]
    except OSError:
        return "something that cannot be read"
    if not under:
        return "an empty folder"
    return "a body with no seed" if "body" in under else "a stone"


def _not_a_plant_words(named, path) -> str:
    """A sentence for someone who pointed look at a folder in a bed that is not a plant."""
    what = _what_it_is(path)
    if what == "a stone":
        under = sorted(inside.name for inside in path.iterdir() if not inside.name.startswith("."))
        return "%s is a stone, not a plant. Under it: %s." % (named, _some_of(under, 5))
    if what == "a body with no seed":
        return "%s has a body but no seed. Without a seed it is not a plant, and nothing is drawn of it." % named
    return "%s is %s, not a plant." % (named, what.split(":")[0])


def _also_here(bed, made=None) -> str:
    """What stands in a bed besides its plants, for the end of a look at it: 'also here: flat-stone (a stone), ...'.
    (The drawing of a thing a creature made is not a thing of its own.)"""
    made = made or {}
    drawings = {where.rsplit("/", 1)[1] + ".png" for where in made if where.rsplit("/", 1)[0] == bed.name}
    try:
        others = sorted(entry for entry in bed.path.iterdir()
                        if not entry.name.startswith(".") and entry.name not in ("bed", "sheet.png")
                        and entry.name not in drawings and (not (entry / "seed").is_file() or _leads_elsewhere(entry)))
    except OSError:
        return ""
    if not others:
        return ""
    return "also here: " + _some_of(["%s (%s)" % (entry.name, _what_it_is(entry, made)) for entry in others], 8)


def _look_thing(root, studio, bed, name, maker, made) -> list:
    """A look at a thing a creature made: its drawing, by its maker's hand, and what it is."""
    path = _guarded(root, "drawing what a creature made", studio.thing, bed, name, maker, made)
    thing = bed.path / name
    lines = [_shown(root, path) if path else "It could not be drawn.", ""]
    lines.append("%s · made by %s · %s" % (name, maker, bed.name))
    lines.append("first made %s; it is a file, %s, and can be read" % (made.isoformat(), _shown(root, thing)))
    return lines


def _look_plan(root, studio) -> list:
    path = _guarded(root, "drawing the plan", studio.plan)
    counts = "%s, %s." % (_count(len(beds(root)), "bed"), _standing(studio.garden()))
    return [_shown(root, path) if path else "The plan could not be drawn.", "", counts]


def _look_bed(root, studio, bed) -> list:
    """A look at a bed: its sheet first, then as many of its stale plates as the look's time allows.

    A plate there was no time for is taken off show, not left stale; it is
    drawn when its plant is looked at.
    """
    growing = [p for p in studio.garden() if p.bed.name == bed.name]
    path = _guarded(root, "drawing the sheet", studio.sheet, bed, True, True)
    left_undrawn = 0
    for plant in growing:
        if _guarded(root, "reading a plate", studio.is_current, plant):
            continue
        if studio.time_is_up():
            for name in ("plate.png", "plate.svg", ".drawn"):
                _remove(plant.path / name)
            left_undrawn += 1
            continue
        _guarded(root, "drawing a plate", studio.plate, plant, True)
    lines = [_shown(root, path) if path else "The sheet could not be drawn.", ""]
    if left_undrawn:
        lines[1:1] = ["(%s not drawn in time; each is drawn when its plant is looked at)"
                      % _count(left_undrawn, "plate was", "plates were")]
    lies = hands.line(bed.keys, "lies")
    lines.append("%s%s" % (bed.name, " · " + lies if lies else ""))
    under = studio.glass_words(bed)
    if under:
        lines.append("%s: no frost, no wind, and the can for rain. A week passes here at each visit." % under)
    lines.append("%s, room for %d" % (_standing(growing), bed.room))
    width = max((len(p.name) for p in growing), default=0)
    kinds = max((len(p.kind) for p in growing), default=0)
    for plant in growing:
        lines.append("  %s  %s  %s" % (plant.name.ljust(width), plant.kind.ljust(kinds), studio.describe(plant)))
    return lines + [words for words in [_also_here(bed, _read_made(root))] if words]


def _look_plant(root, studio, plant) -> list:
    path = _guarded(root, "drawing the plate", studio.plate, plant, True)
    lines = [_shown(root, path) if path else "The plate could not be drawn.", ""]
    under = studio.glass_words(plant.bed)
    lines.append("%s · %s · %s%s" % (plant.name, _kind_words(plant), plant.bed.name, " · " + under if under else ""))
    age = studio.age_words(plant)
    lines.append(studio.planted_words(plant) + (" · " + age if age else ""))
    lines.append(studio.describe(plant) + ("" if plant.has_body else _kinds_words(root, plant)))
    if studio.record(plant).trouble.startswith("could not be drawn"):
        lines.append("%s (the whole of it is in %s)" % (studio.record(plant).trouble, _shown(root, Path(root) / "ground" / "trouble.log")))
    if plant.last_ring and plant.has_body:
        lines.append("last ring: %s  %s" % (plant.last_ring_day.isoformat() if plant.last_ring_day else "", plant.last_ring))
    return lines


def _look_everything(root, until=None) -> list:
    budget = 90.0 if until is None else max(1.0, until - time.monotonic())
    done = _guarded(root, "drawing", _draw_everything, root, budget, True) or {}
    lines = [_shown(root, Path(root) / "ground" / "plan.png"), "",
             "%s and %s drawn afresh." % (_count(done.get("sheets", 0), "bed sheet"), _count(done.get("plates", 0), "plate"))]
    if done.get("left"):
        lines.append("%s not reached; each is drawn when it is looked at." % _count(done["left"], "plate was", "plates were"))
    return lines


def leave(root, words=None, visit=None) -> str:
    """Close the gate behind whoever is in the garden. Returns the closing line, and under it what was laid down.

    With `visit` (a token, as the API door passes it) only the visit whose
    latch holds that token is closed; another visit is left as it is.
    """
    root = Path(root)
    with _Bolt(root, "someone is going out", wait=30.0) as bolt:
        if not bolt.shot:
            return ("The gate is in use at this moment (%s). Nothing is owed: leaving can wait, "
                    "or be left to the next arrival." % bolt.held_by)
        lines = _leave(root, words, _token(visit)) + _trouble_words(root)
        _keep_what_was_learnt(root)
        return "\n".join(lines)


def _leave(root, words, token="") -> list:
    moment = now(root)
    latch = _guarded(root, "reading the latch", _latch, root)
    live = _is_live(latch, moment)
    if token and live and latch["visit"] != token:
        return ["That visit is not the one on the latch: %s is in the garden, since %s. Nothing was changed."
                % (latch["name"], latch["since"].strftime("%H:%M"))]
    _guarded(root, "finishing what was cut short", _finish_passing, root)
    _guarded(root, "recalling what this visit has met", _recall_visit, root)
    _guarded(root, "recalling the kinds set aside", _recall_aside, root)
    # Days that were lived and never laid down (an arrival of this visit was cut short, or could lay nothing down) are
    # nobody's doing: they go into their own layers before the visit is settled, or the visitor would sign them.
    _guarded(root, "laying down days under the glass that were never laid down", _lay_down_stray_glass, root)
    _guarded(root, "laying down days that were never laid down", _lay_down_stray_days, root, moment.date())
    _apart(root, "tend", None, until=time.monotonic() + 60.0)
    if not live:
        # A latch gone cold: whoever it names went out long ago. What they did is theirs, and laid down in their
        # name; what came after their twelve hours is signed as it would be with no latch (ruling 2).
        _guarded(root, "leaving the rings of hands", _leave_rings, root,
                 _guarded(root, "settling", _settle, root, latch, False, moment) or [], moment.date())
        if latch:
            _guarded(root, "writing the visits", _write_visit, root, moment, VISIT_OPEN, latch["name"])
            _lift_latch(root)
        return ["No one was through the gate; it stays closed."]
    name = latch["name"]
    words = _one_line(words or "", 300)
    _guarded(root, "writing the visits", _write_visit, root, moment, VISIT_OUT, name, words)
    changes = _guarded(root, "reading the changes", _changes, root) or []
    strays = _guarded(root, "reading what the days could not lay down", _stray_paths, root, changes) or set()
    changes = [change for change in changes if change[1] not in strays]     # (no hand's doing: see `_stray_paths`)
    the_keepers = [change for change in changes if change[1] in KEEPERS_OWN]
    if the_keepers:                                 # the day's sky and the place are the keeper's, whoever holds the latch
        changes = [change for change in changes if change not in the_keepers]
        _guarded(root, "laying down the keeper's lines", _lay_down, root, THE_KEEPER,
                 _message(root, "the keeper was here", the_keepers, []), the_keepers, [path for _, path in the_keepers])
    rings = _guarded(root, "reading what hands did", _hand_rings, root, changes, name) or []
    touched = _touched(root, changes, rings)
    message = (words + ("\n\n" + "\n".join(touched) if touched else "")) if words else _message(root, "", changes, rings)
    troubles = len(said_troubles)
    _guarded(root, "leaving the rings of hands", _leave_rings, root, rings, moment.date())
    laid = _guarded(root, "laying down the visit", _lay_down, root, name, message, changes,
                    [path for _, path in changes] if strays else None)
    _lift_latch(root)
    line = "The gate is closed behind %s · %s · %s" % (name, _long_date(moment.date()), moment.strftime("%H:%M"))
    if not _layers(root):
        return [line]
    if not laid and len(said_troubles) > troubles:
        return [line + " · the visit could not be laid down in the layers; the next arrival will try again"]
    if not touched:
        return [line + " · nothing was changed"]
    return [line + " · %s laid down" % _count(len(touched), "thing")] + ["  " + thing for thing in touched[:12]] + (
        ["  and %d more" % (len(touched) - 12)] if len(touched) > 12 else [])
