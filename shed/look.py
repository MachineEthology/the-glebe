"""
Looking.

    python shed/look.py                        the whole garden from above
    python shed/look.py beds/<bed>             one bed: all its plants side by side, and a line about each
    python shed/look.py beds/<bed>/<plant>     one plant: its plate, drawn as it stands now
    python shed/look.py beds/<bed>/<thing>     something a creature made (a web, a hill), drawn by its maker
    python shed/look.py .                      the bed or the plant you stand in (anywhere else, the whole garden)
    python shed/look.py --all                  draws everything afresh

Each time it says where the picture is; open that file to see it. A seed
planted a moment ago comes up when this door is passed, so looking at a new
plant is also how it is first seen.

A plant may be named by its path, from here or from the garden's root, or by
its name alone.

A look keeps within about eighty seconds. A bed whose plants are slow to draw
shows on its sheet those there was time for, says which were not reached, and
draws them when it is looked at again, or when each plant is looked at alone.

Everything this door does is in ground.py, under `look`.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True                  # the garden keeps no caches among its files
sys.path.insert(0, str(ROOT / "shed"))


def stuck(error) -> None:
    """The door itself failed. Say so in one plain sentence; the whole error goes to ground/trouble.log.

    (arrive.py and leave.py each hold this same function, with their own
    words. Whoever changes one should look at all three.)
    """
    import datetime
    import traceback
    try:
        (ROOT / "ground").mkdir(exist_ok=True)
        with open(ROOT / "ground" / "trouble.log", "a", encoding="utf-8", errors="replace", newline="\n") as log:
            log.write("%s  looking failed\n" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            for line in "".join(traceback.format_exception(type(error), error, error.__traceback__)).splitlines():
                log.write("    %s\n" % line)
    except OSError:
        pass
    print("Nothing could be drawn: %s: %s." % (type(error).__name__, " ".join(str(error).split())[:200]))
    print("The whole of it is in ground/trouble.log.")


def not_a_garden() -> bool:
    """True, having said so, when this is the cutting itself: lay.py beside the shed and no ground/place.

    The cutting is the bare ground a garden is laid from. A door passed in it would make it a garden
    dated from the first garden's day, so the doors stay shut there and say where a garden comes from.
    (arrive.py, look.py and leave.py each hold this same function.)
    """
    if (ROOT / "lay.py").is_file() and not (ROOT / "ground" / "place").is_file():
        print("This folder is the cutting of the Glebe, the bare ground a garden is laid from, and not a "
              "garden: its doors do not open here. A garden is laid from it with: python lay.py "
              "\"<an empty folder>\" (README.md says more).")
        return True
    return False


def main(arguments) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if "--help" in arguments or "-h" in arguments:
        print(__doc__.strip())
        return 0
    if not_a_garden():
        return 1
    paths = [word for word in arguments if not word.startswith("--")]
    try:
        import ground
        print(ground.look(ROOT, " ".join(paths) or None, everything="--all" in arguments))
        return 0
    except KeyboardInterrupt:
        print("Stopped.")
        return 1
    except BaseException as error:              # no traceback reaches a visitor
        stuck(error)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
