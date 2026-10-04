"""
A trial ground: a bare copy of the garden, for trying things without touching the real one.

    python shed/foundations/trial_ground.py <path> [--with-plants] [--no-gate-note]

It lays at <path> the garden's ground as it stands (the gate note, the beds
with their `bed` files, ground/place, the shed, the kinds, the creatures, the
seedbox, the gate and the heap) but none of its history: no almanac, no
visits, no latch, no layers. With --with-plants the plants come too, as they
are today, and with them the book (the kinds may feed on it: without it a
plant would grow otherwise in the trial than in the garden), the creatures'
own records (ground/creatures, the larder, the beds' richness, the record of
what they made; the things they made lie in the beds and come with them) and
the planters' inks, the pollen of the garden's last lived day, and the calendar
under the glass with its chronicle (the plants under glass live by it).

With --no-gate-note the gate note, CLAUDE.md, stays behind. A Claude session
working inside a folder is handed the CLAUDE.md it finds there as that
folder's instructions, so a trial ground that carries the gate note reads,
each time, like a second gate; a trial laid to try a kind has no need of it.
Nothing in the ground reads it. (The keeper's door, keeper/invite.py,
rehearses only in a trial ground that has it.)

The trial ground gets the trial kinds of foundations/trial_kinds/ among its
species, a clock of its own (ground/clock, which clock.py winds), the real
sky turned off whatever the garden's place says (the same trial must give
the same days, and a trial never asks the network), and a fresh git
repository whose first layer is signed by "the builders".

If the garden has no creatures of its own yet, the trial ground is given
the trial creatures of foundations/trial_creatures/ (hoverflies, which carry
pollen; voles, which graze, hide seed and shift plants; ants, which build
a hill), so that the ground's side of creatures can be tried all the same.
Once the garden has creatures, a trial ground has the garden's, and only
those.

Its clock is what makes it a trial ground: only a ground with ground/clock
honours GLEBE_TODAY, or winds on. (GLEBE_TODAY moves every file's date along
with the calendar, so "sown on the day the seed was written" cannot be tried
with it; clock.py keeps file dates honest.)

It will not write into the real garden, nor into a folder that holds
anything. In a trial ground anything may be done: break a kind, wind the
clock a year on, pull everything up. Nothing of it reaches the garden.
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

GARDEN = Path(__file__).resolve().parent.parent.parent      # the garden this file stands in
BUILDERS = "the builders"
GATE_NOTE = "CLAUDE.md"
PLAIN_FILES = (GATE_NOTE, ".gitignore", ".gitattributes")
WHOLE_FOLDERS = ("shed", "species", "creatures", "seedbox", "gate", "compost")
WITH_PLANTS = ("book", "ground/creatures", "ground/larder", "ground/rich", "ground/made",   # the present, copied only
               "ground/pollen", "ground/glass", "ground/under-glass")                      # with the plants (the plants
                                                                                           # under glass live by its calendar)
NEVER_COPIED = shutil.ignore_patterns("__pycache__", "plate.png", "plate.svg", "sheet.png", ".drawn", ".*.part")


class Refused(Exception):
    """The trial ground was not laid, and the message says why."""


def lay(target, with_plants=False, source=GARDEN, gate_note=True) -> list:
    """Lay a trial ground at `target`. Returns what to say about it; raises Refused if it must not be done.

    gate_note=False leaves the gate note, CLAUDE.md, behind (see the head of this file).
    """
    source, target = Path(source).resolve(), Path(target).resolve()
    if target == source or source in target.parents:
        raise Refused("That is the garden itself. A trial ground is laid somewhere else.")
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        raise Refused("%s already holds something. A trial ground is laid in an empty place." % target.as_posix())
    target.mkdir(parents=True, exist_ok=True)
    for name in PLAIN_FILES:
        if (source / name).is_file() and (gate_note or name != GATE_NOTE):
            shutil.copy2(source / name, target / name)
    for name in WHOLE_FOLDERS:
        if (source / name).is_dir():
            shutil.copytree(source / name, target / name, ignore=NEVER_COPIED)
    beds = _copy_beds(source, target, with_plants)
    (target / "ground").mkdir(exist_ok=True)
    if (source / "ground" / "place").is_file():
        _write(target / "ground" / "place", _place_without_the_real_sky(source / "ground" / "place"))
    ahead = 0
    if with_plants:
        ahead = _carry_the_present(source, target)
        for name in WITH_PLANTS:
            if (source / name).is_dir():
                shutil.copytree(source / name, target / name, ignore=NEVER_COPIED)
            elif (source / name).is_file():
                shutil.copy2(source / name, target / name)
    _write(target / "ground" / "clock",
           "# This is a trial ground, with a clock of its own. foundations/clock.py winds it.\nahead: %d\n" % ahead)
    kinds = _copy_trial_kinds(source, target)
    creatures = _copy_trial_creatures(source, target)
    layers = _first_layer(target)
    return ["A trial ground is laid at %s." % target.as_posix(),
            "%d beds, %s%s; trial kinds: %s; %s; %s." % (
                beds, "the plants as they stand today" if with_plants else "no plants",
                "" if (target / GATE_NOTE).is_file() else ", no gate note",
                ", ".join(kinds) or "none", creatures,
                "a first layer by the builders" if layers else "no layers (git was not to be had)"),
            'Its gate: python "%s" --as <a name>' % (target / "shed" / "arrive.py").as_posix()]


def _write(path, text) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def _place_without_the_real_sky(path) -> str:
    """The garden's ground/place with every `real-sky:` line taken out, and one that says no put at its end."""
    kept = [line for line in path.read_text(encoding="utf-8", errors="replace").splitlines()
            if line.partition(":")[0].strip().lower() != "real-sky"]
    return "\n".join(kept).rstrip("\n") + (
        "\n# A trial ground never asks the network for its sky: the same trial must give the same days.\n"
        "real-sky: no\n")


def _copy_beds(source, target, with_plants) -> int:
    """Every bed with its `bed` file; with_plants, everything that stands in it as well."""
    (target / "beds").mkdir(exist_ok=True)
    count = 0
    for bed in sorted((source / "beds").iterdir()) if (source / "beds").is_dir() else []:
        if not bed.is_dir() or bed.name.startswith("."):
            continue
        count += 1
        if with_plants:
            shutil.copytree(bed, target / "beds" / bed.name, ignore=NEVER_COPIED)
            continue
        (target / "beds" / bed.name).mkdir()
        if (bed / "bed").is_file():
            shutil.copy2(bed / "bed", target / "beds" / bed.name / "bed")
    return count


def _carry_the_present(source, target) -> int:
    """With plants: keep their planters' inks, and start the trial's days where the garden's left off.

    Without this the trial's first arrival would live every day since the
    ground was laid a second time, on plants that have already lived them.
    Returns how far ahead the source's own clock is (0 for the real garden),
    so that a trial laid from a trial keeps its calendar.
    """
    if (source / "ground" / "inks").is_file():
        shutil.copy2(source / "ground" / "inks", target / "ground" / "inks")
    ahead = 0
    try:
        clock = (source / "ground" / "clock").read_text(encoding="utf-8", errors="replace")
        found = re.search(r"^\s*ahead\s*:\s*(-?\d{1,6})", clock, re.MULTILINE)
        ahead = int(found.group(1)) if found else 0
    except OSError:
        pass
    last = None
    try:
        with open(source / "ground" / "almanac", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if re.match(r"\d{4}-\d{2}-\d{2}(\s|$)", line):
                    last = line[:10]
    except OSError:
        return ahead
    if last:
        with open(target / "ground" / "almanac", "w", encoding="utf-8", newline="\n") as handle:
            handle.write("# A trial ground, laid from the garden as it stood after this day.\n"
                         "%s  the garden's own days end here; the trial's begin  [reckoned]\n" % last)
    return ahead


def _copy_trial_kinds(source, target) -> list:
    """Put the trial kinds among the species. A garden kind of the same name is the garden's, and is left as it is."""
    (target / "species").mkdir(exist_ok=True)
    kinds = []
    for kind in sorted((source / "shed" / "foundations" / "trial_kinds").glob("*.py")):
        if (target / "species" / kind.name).exists():
            kinds.append("%s (not copied: the garden has a kind of that name)" % kind.stem)
            continue
        shutil.copy2(kind, target / "species" / kind.name)
        kinds.append(kind.stem)
    return kinds


def _copy_trial_creatures(source, target) -> str:
    """The trial creatures, if the ground has no creatures of its own yet. Returns what to say of the creatures."""
    own = sorted(path.stem for path in (target / "creatures").glob("*.py")) if (target / "creatures").is_dir() else []
    if own:
        return "the garden's creatures: %s" % ", ".join(own)
    trial = sorted((source / "shed" / "foundations" / "trial_creatures").glob("*.py"))
    if not trial:
        return "no creatures"
    (target / "creatures").mkdir(exist_ok=True)
    for path in trial:
        shutil.copy2(path, target / "creatures" / path.name)
    return "trial creatures: %s" % ", ".join(path.stem for path in trial)


def _first_layer(target) -> bool:
    """git init, and one commit by the builders. False if git is not to be had; the trial ground lives without."""
    git = shutil.which("git")
    if not git:
        return False
    sign = ["-c", "user.name=%s" % BUILDERS, "-c", "user.email=the-builders@glebe", "-c", "core.autocrlf=false",
            "-c", "commit.gpgsign=false", "-c", "core.excludesFile=",
            "-c", "core.hooksPath=%s" % (target / ".git" / "no-hooks")]
    steps = (["init", "--quiet"],                       # (as in ground._git: nobody's own git settings sign, hook,
             sign + ["add", "-A"],                      # name, or leave anything out of a layer)
             sign + ["commit", "--quiet", "-m", "the ground, laid for a trial",
                     "--author=%s <the-builders@glebe>" % BUILDERS])
    env = {key: value for key, value in os.environ.items()
           if key not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE") and not key.startswith(("GIT_AUTHOR_", "GIT_COMMITTER_"))}
    for step in steps:
        try:
            done = subprocess.run([git, "-C", str(target)] + step, capture_output=True, stdin=subprocess.DEVNULL,
                                  timeout=120, env=dict(env, GIT_TERMINAL_PROMPT="0"))
        except (OSError, subprocess.SubprocessError):
            return False
        if done.returncode != 0:
            return False
    return True


def main(arguments) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    paths = [a for a in arguments if not a.startswith("--")]
    if len(paths) != 1 or "--help" in arguments:
        print(__doc__.strip())
        return 0 if "--help" in arguments else 1
    try:
        for line in lay(paths[0], with_plants="--with-plants" in arguments, gate_note="--no-gate-note" not in arguments):
            print(line)
    except Refused as refusal:
        print(refusal)
        return 1
    except OSError as error:
        print("The trial ground could not be laid: %s" % error)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
