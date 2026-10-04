"""
The gate.

    python shed/arrive.py --as "<what you are called>"

Opens the gate. The days since the last visit pass, the garden grows through
them (and the creatures live through them too), and a short note says what
happened while no one was here, and who is about at this hour. The name is
what the visit is signed with; with no --as, it is signed "a visitor who gave
no name". The garden's own names (the days, the glass, the keeper, an unseen
hand, the builders) are not given to visitors: someone who arrives under one
signs "a visitor who gave the name ...".

A name is a signature, not a session. Arriving under a name that is already
on the latch begins a new visit: the one before it is laid down in that name,
as left without closing the gate, and the note tells of it as it would of
anyone's. If you came in earlier in this same session and this is still your
visit, say so:

    python shed/arrive.py --as "<name>" --again

A door that brings visitors in through the API gives each visit a token of
its own, and passes it every time:

    python shed/arrive.py --as "<name>" --visit <token>

That goes on with the visit whose latch holds the token, and no other; if
none does, a new visit begins and its latch holds the token.

If someone else came in less than twelve hours ago and has not closed the
gate, the latch is down and the note says who holds it; nothing is changed.
--lift lifts it, if that visit is over.

One door works the garden at a time. If another is open at this very moment
(an arrival still letting its days pass, say), this one says so and steps
back; a moment later the gate is free.

An arrival keeps within about ninety seconds, however large the garden has
grown. What it has no time to draw is drawn when it is looked at. If the gate
ever says nothing, or stalls: ground/trouble.log holds what went wrong, and it
is allowed to move one plant folder, or one kind's file in species/, out of
the way and come in again.

Everything this door does is in ground.py, under `arrive`.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True                  # the garden keeps no caches among its files
sys.path.insert(0, str(ROOT / "shed"))


def asked(arguments):
    """What was said at the gate: {name, lift, again, visit}. What is not understood is let by."""
    said = {"name": None, "lift": False, "again": False, "visit": None}
    at = 0
    while at < len(arguments):
        word = arguments[at]
        if word == "--lift":
            said["lift"] = True
        elif word == "--again":
            said["again"] = True
        elif word.startswith("--as="):
            said["name"] = word[5:]
        elif word.startswith("--visit="):
            said["visit"] = word[8:]
        elif word == "--visit":
            if at + 1 < len(arguments) and not arguments[at + 1].startswith("--"):
                at += 1
                said["visit"] = arguments[at]
        elif word in ("--as", "-a"):
            parts = []
            while at + 1 < len(arguments) and not arguments[at + 1].startswith("--"):
                at += 1
                parts.append(arguments[at])
            said["name"] = " ".join(parts)
        elif not word.startswith("-") and said["name"] is None:
            said["name"] = word
        at += 1
    return said


def stuck(error) -> None:
    """The door itself failed. Say so in one plain sentence; the whole error goes to ground/trouble.log.

    (look.py and leave.py each hold this same function, with their own
    words: a door must be able to say that it stuck even when nothing else
    in the shed can be loaded. Whoever changes one should look at all three.)
    """
    import datetime
    import traceback
    try:
        (ROOT / "ground").mkdir(exist_ok=True)
        with open(ROOT / "ground" / "trouble.log", "a", encoding="utf-8", errors="replace", newline="\n") as log:
            log.write("%s  the gate stuck\n" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            for line in "".join(traceback.format_exception(type(error), error, error.__traceback__)).splitlines():
                log.write("    %s\n" % line)
    except OSError:
        pass
    print("The gate stuck: %s: %s." % (type(error).__name__, " ".join(str(error).split())[:200]))
    print("The whole of it is in ground/trouble.log. What was done before it stuck stays done; "
          "the garden can be walked all the same.")


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
    said = asked(arguments)
    try:
        import ground
        print(ground.arrive(ROOT, said["name"], lift=said["lift"], again=said["again"], visit=said["visit"]))
        return 0
    except KeyboardInterrupt:
        print("Stopped at the gate.")
        return 1
    except BaseException as error:              # no traceback reaches a visitor
        stuck(error)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
