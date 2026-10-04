"""
Leaving.

    python shed/leave.py ["a few words"]

Closes the gate behind whoever is in the garden. What they changed is laid
down in the garden's layers under their name, with the words as the message
(or, with no words, a plain list of what was touched), and the latch is
lifted. It answers with one line, and under it the list of what it
understood their hands to have done.

It is never needed. A visit left open is settled quietly by the next arrival.

A door that brings visitors in through the API passes the visit's token
(--visit <token>, as it did at the gate), and then only that visit is closed.

Everything this door does is in ground.py, under `leave`.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True                  # the garden keeps no caches among its files
sys.path.insert(0, str(ROOT / "shed"))


def stuck(error) -> None:
    """The door itself failed. Say so in one plain sentence; the whole error goes to ground/trouble.log.

    (arrive.py and look.py each hold this same function, with their own
    words. Whoever changes one should look at all three.)
    """
    import datetime
    import traceback
    try:
        (ROOT / "ground").mkdir(exist_ok=True)
        with open(ROOT / "ground" / "trouble.log", "a", encoding="utf-8", errors="replace", newline="\n") as log:
            log.write("%s  the gate would not close\n" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            for line in "".join(traceback.format_exception(type(error), error, error.__traceback__)).splitlines():
                log.write("    %s\n" % line)
    except OSError:
        pass
    print("The gate would not close: %s: %s. Nothing is owed; the next arrival settles it. (ground/trouble.log has the whole of it.)"
          % (type(error).__name__, " ".join(str(error).split())[:200]))


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
    words, visit, at = [], None, 0
    while at < len(arguments):                  # everything is the leaving words, but for a --visit <token>
        if arguments[at] == "--visit" and at + 1 < len(arguments):
            visit, at = arguments[at + 1], at + 2
            continue
        if arguments[at].startswith("--visit="):
            visit = arguments[at][len("--visit="):]
        elif arguments[at].strip():
            words.append(arguments[at])
        at += 1
    try:
        import ground
        print(ground.leave(ROOT, " ".join(words) or None, visit=visit))
        return 0
    except KeyboardInterrupt:
        print("Stopped.")
        return 1
    except BaseException as error:              # no traceback reaches a visitor
        stuck(error)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
