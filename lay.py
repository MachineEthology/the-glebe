"""
Lay a garden: a Glebe of your own, from this cutting.

    python lay.py <folder> [--latitude N] [--longitude N]

It lays at <folder> the bare ground of the Glebe as this cutting holds it:
the gate note (CLAUDE.md), the beds with their `bed` files, the kinds of
plant, the creatures, the seedbox, the heap's first leaf litter, the shed
with its foundations, the keeper's side, the licences, and the settings a
Claude Code session finds in the garden's folder. Nothing is planted, and
the garden has no history yet. The README, the film and this file stay in
the cutting.

It writes ground/place: the ground is laid today, at the latitude given,
under a sky of its own (a fresh weather seed, so that two gardens laid on
the same day have different weather). The real sky is off; ground/place
says how the keeper may turn it on.

    --latitude N    where the garden lies, in degrees: north positive, south
                    negative (as -41.3). A whole degree is close enough. It
                    sets the garden's day lengths and its seasons. With none
                    given, the garden lies at 47.0.
    --longitude N   east positive, west negative. Only the real sky needs it,
                    and it can be written in ground/place later.

If git is to be had, the garden gets a repository of its own and a first
layer, "The ground is laid.", signed by the builders. Without git the garden
lives all the same, without layers.

It will not lay a garden in the cutting or inside it, inside another garden,
or in a folder that already holds anything. A garden laid here has no clock:
its days are the real ones. (Its sibling, shed/foundations/trial_ground.py,
lays a trial ground with a clock of its own, for trying things.)

Python 3.11 or later, and nothing else.
"""

import datetime
import math
import os
import random
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True                  # the garden keeps no caches among its files

CUTTING = Path(__file__).resolve().parent       # the cutting this file stands in
BUILDERS = "the builders"
BUILDERS_EMAIL = "the-builders@glebe"
FIRST_LAYER = "The ground is laid."
DEFAULT_LATITUDE = 47.0
NEEDED = ("CLAUDE.md", "shed/ground.py", "shed/sky.py", "shed/arrive.py", "shed/look.py", "shed/leave.py",
          "species", "beds", "seedbox")         # without these, the folder this file stands in is not a whole cutting
PLAIN_FILES = ("CLAUDE.md", ".gitignore", ".gitattributes", "LICENSE", "LICENSE-TEXTS", ".claude/settings.json")
WHOLE_FOLDERS = ("species", "creatures", "seedbox", "compost", "shed", "keeper")
NEVER_COPIED = shutil.ignore_patterns(".git", "__pycache__", "plate.png", "plate.svg", "sheet.png", ".drawn", ".*.part",
                                      ".heap", "humus")    # (a heap's record and its humus are a garden's, never a cutting's)
PLACE = """\
# Where and when the garden lies. The keeper may change these.
laid: {laid}
latitude: {latitude}
weather-seed: {seed}
# real-sky: yes  fetches each day's real weather for the place below from open-meteo.com.
# It needs a longitude as well as the latitude. A nearby town will do. Off unless the keeper turns it on.
real-sky: no
longitude:{longitude}
"""
USAGE = "python lay.py <folder> [--latitude N] [--longitude N]      (--help says more)"


class Refused(Exception):
    """The garden was not laid, and the message says why."""


def lay(target, latitude=None, longitude=None, source=CUTTING) -> tuple:
    """Lay a garden at `target`. Raises Refused if it must not be done.

    Returns (what to say about it, whether it was laid whole): a ground/place
    that does not read back as written is said, and no layer is laid on it.
    """
    source = Path(source).resolve()
    target = Path(target).expanduser().resolve()
    missing = [name for name in NEEDED if not (source / name).exists()]
    if missing:
        raise Refused("lay.py lays a garden from the cutting it stands in, and %s is not a whole cutting: "
                      "it has no %s." % (source.as_posix(), ", no ".join(missing)))
    if _within(target, source):
        raise Refused("That is the cutting itself, or a folder inside it. A garden is laid somewhere of its own.")
    garden = _garden_round(target)
    if garden is not None:
        raise Refused("That folder lies inside a garden (%s). A new garden is laid somewhere of its own."
                      % garden.as_posix())
    if target.exists() and not target.is_dir():
        raise Refused("%s is a file, not a folder. A garden is laid in an empty folder." % target.as_posix())
    if target.exists() and any(target.iterdir()):
        raise Refused("%s already holds something. A garden is laid in an empty folder." % target.as_posix())

    target.mkdir(parents=True, exist_ok=True)
    for name in PLAIN_FILES:
        if (source / name).is_file():
            (target / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / name, target / name)
    for name in WHOLE_FOLDERS:
        if (source / name).is_dir():
            shutil.copytree(source / name, target / name, ignore=NEVER_COPIED)
    beds = _copy_beds(source, target)

    laid = datetime.date.today()
    given = latitude is not None
    latitude = DEFAULT_LATITUDE if latitude is None else latitude
    seed = random.SystemRandom().randint(10_000_000, 99_999_999)
    (target / "ground").mkdir(exist_ok=True)
    _write(target / "ground" / "place", PLACE.format(
        laid=laid.isoformat(), latitude=_degrees(latitude), seed=seed,
        longitude="" if longitude is None else " " + _degrees(longitude)))
    wrong = _read_back(target, {"laid": laid, "latitude": float(_degrees(latitude)), "weather-seed": seed,
                                "real-sky": False,
                                "longitude": None if longitude is None else float(_degrees(longitude))})

    said = ["A garden is laid at %s." % target.as_posix(),
            "Laid today, %s, at latitude %s%s" % (
                laid.isoformat(), _degrees(latitude),
                "." if given else ", the latitude a garden has when none is given. If it lies elsewhere, "
                                  "change the line `latitude:` in ground/place before the first visit."),
            "Its sky is its own: weather seed %d. The real sky is off%s" % (
                seed, "." if longitude is None else "; longitude %s is written for the day it is turned on."
                                                    % _degrees(longitude)),
            "%d beds with nothing planted in them, %d kinds of plant, %d creatures, %d packets in the seedbox." % (
                beds, _count(target / "species", "*.py"), _count(target / "creatures", "*.py"),
                _count(target / "seedbox", "*.seed"))]
    if wrong:
        return said + ["But ground/place does not read back as it was written (%s), so no layer was laid. "
                       "Look at ground/place before anyone visits." % "; ".join(wrong)], False
    layered = _first_layer(target)
    if layered is True:
        said.append('Its history begins with a first layer, "%s", signed by %s.' % (FIRST_LAYER, BUILDERS))
    elif layered is None:
        said.append("git was not to be had here, so the garden lives without layers. It grows all the same.")
    else:
        said.append("git was found, but the first layer could not be laid (%s). The garden lives all the same; "
                    "if its folder holds a .git, its first door lays the first layer." % layered)
    return said + [
        "",
        "To begin:",
        "- With Claude Code: start a new session and choose %s as the session's own folder, before the first "
        "message. The gate note, CLAUDE.md, is then the first thing the visitor reads." % target.as_posix(),
        "- Through the API: keeper/KEEPER.md, in the garden, says how its door brings a model in.",
        "The three doors, as the gate note gives them to every visitor, from the garden's folder:",
        '    python shed/arrive.py --as "<a name>"    opens the gate',
        "    python shed/look.py                      draws the garden from above",
        "    python shed/leave.py                     closes the gate",
        "Hand it over the way the gate note does: nothing is asked, and leaving at once is fine.",
    ], True


def _within(target, folder) -> bool:
    """Is `target` the folder itself, or inside it? Asked by name and, where a folder exists, of the disk itself."""
    path, base = os.path.normcase(str(target)), os.path.normcase(str(folder))
    if path == base or path.startswith(base.rstrip(os.sep) + os.sep):
        return True
    for place in (target, *target.parents):
        try:
            if place.exists() and os.path.samefile(place, folder):
                return True
        except OSError:
            continue
    return False


def _garden_round(target):
    """The garden (or trial ground) that `target` lies in, if it lies in one; else None."""
    for place in (target, *target.parents):
        try:
            if (place / "shed" / "ground.py").is_file() and (place / "ground" / "place").is_file():
                return place
        except OSError:
            continue
    return None


def _copy_beds(source, target) -> int:
    """Every bed with its `bed` file, and nothing else that may stand in it."""
    (target / "beds").mkdir(exist_ok=True)
    count = 0
    for bed in sorted((source / "beds").iterdir()):
        if not bed.is_dir() or bed.name.startswith("."):
            continue
        count += 1
        (target / "beds" / bed.name).mkdir()
        if (bed / "bed").is_file():
            shutil.copy2(bed / "bed", target / "beds" / bed.name / "bed")
    return count


def _count(folder, pattern) -> int:
    return len(list(folder.glob(pattern))) if folder.is_dir() else 0


def _degrees(number) -> str:
    """An angle as ground/place writes it: 47.0, -41.3, 2.3522 (to a millionth of a degree at most)."""
    written = ("%.6f" % (round(number, 6) + 0.0)).rstrip("0")      # (+ 0.0 turns -0.0 into 0.0)
    return written + "0" if written.endswith(".") else written


def _write(path, text) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def _read_back(target, written) -> list:
    """Read ground/place with the new garden's own sky, as its doors will. Returns what differs from what was written."""
    shed = str(target / "shed")
    kept_path = list(sys.path)
    kept_modules = {name: sys.modules.pop(name) for name in ("sky", "hands") if name in sys.modules}
    sys.path.insert(0, shed)
    try:
        import sky
        found = sky.place(target)
    except Exception as error:
        return ["the garden's sky could not read it: %s" % error]
    finally:
        sys.path[:] = kept_path
        for name in ("sky", "hands"):
            sys.modules.pop(name, None)
        sys.modules.update(kept_modules)
    return ["%s was written %s and reads %s" % (key, value, found.get(key))
            for key, value in written.items() if found.get(key) != value]


def _first_layer(target):
    """git init, and one commit by the builders. True if it was laid; None if git is not to be had; else what went wrong.

    As in trial_ground.py, and as in ground._git: nobody's own git settings
    sign, hook, name, or leave anything out of a layer.
    """
    git = shutil.which("git")
    if not git:
        return None
    sign = ["-c", "user.name=%s" % BUILDERS, "-c", "user.email=%s" % BUILDERS_EMAIL, "-c", "core.autocrlf=false",
            "-c", "commit.gpgsign=false", "-c", "core.excludesFile=",
            "-c", "core.hooksPath=%s" % (target / ".git" / "no-hooks")]
    steps = (("init", ["init", "--quiet"]),
             ("add", sign + ["add", "-A"]),
             ("commit", sign + ["commit", "--quiet", "-m", FIRST_LAYER,
                                "--author=%s <%s>" % (BUILDERS, BUILDERS_EMAIL)]))
    env = {key: value for key, value in os.environ.items()
           if key not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE") and not key.startswith(("GIT_AUTHOR_", "GIT_COMMITTER_"))}
    for name, step in steps:
        try:
            done = subprocess.run([git, "-C", str(target)] + step, capture_output=True, stdin=subprocess.DEVNULL,
                                  timeout=120, env=dict(env, GIT_TERMINAL_PROMPT="0"))
        except (OSError, subprocess.SubprocessError) as error:
            return "git %s could not be run: %s" % (name, error)
        if done.returncode != 0:
            words = (done.stderr or done.stdout).decode("utf-8", errors="replace").strip().splitlines()
            return "git %s said: %s" % (name, words[-1] if words else "nothing, and failed")
    return True


def _angle(word, name, most):
    """A number of degrees given on the command line, between -most and most. Raises Refused if it is not one."""
    try:
        number = float(word.strip().replace(",", ".", 1))
    except ValueError:
        number = None
    if number is None or not math.isfinite(number) or not -most <= number <= most:
        raise Refused("--%s takes a number of degrees between -%d and %d (%s); %r is not one." % (
            name, most, most, "south is negative, as -41.3" if name == "latitude" else "west is negative, as -1.5", word))
    return number


def parsed(arguments) -> dict:
    """What was asked: {folder, latitude, longitude, help}. Raises Refused for anything not understood."""
    asked = {"folder": None, "latitude": None, "longitude": None, "help": False}
    folders = []
    at, plain = 0, False
    while at < len(arguments):
        word = arguments[at]
        name, equals, value = word.partition("=")
        if plain or not word.startswith("-") or word == "-":
            folders.append(word)
        elif word == "--":
            plain = True
        elif word in ("--help", "-h"):
            asked["help"] = True
        elif name in ("--latitude", "--longitude"):
            if not equals:
                if at + 1 >= len(arguments):
                    raise Refused("%s needs a number after it." % name)
                at += 1
                value = arguments[at]
            key = name[2:]
            asked[key] = _angle(value, key, 90 if key == "latitude" else 180)
        else:
            raise Refused("%s is not something lay.py understands." % word)
        at += 1
    if not asked["help"]:
        if len(folders) != 1:
            raise Refused("Name one folder for the garden." if not folders
                          else "Name one folder for the garden, not %d." % len(folders))
        asked["folder"] = folders[0]
    return asked


def main(arguments) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if sys.version_info < (3, 11):
        print("The Glebe needs Python 3.11 or later, and this is Python %d.%d." % sys.version_info[:2])
        return 1
    try:
        asked = parsed(arguments)
    except Refused as refusal:
        print(refusal)
        print("Usage: " + USAGE)
        return 1
    if asked["help"]:
        print(__doc__.strip())
        return 0
    try:
        said, whole = lay(asked["folder"], latitude=asked["latitude"], longitude=asked["longitude"])
    except Refused as refusal:
        print(refusal)
        return 1
    except OSError as error:
        print("The garden could not be laid: %s" % error)
        return 1
    for line in said:
        print(line)
    return 0 if whole else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
