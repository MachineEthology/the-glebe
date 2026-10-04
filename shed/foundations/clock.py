"""
The clock of a trial ground.

    python shed/foundations/clock.py                  says what day it is in this ground
    python shed/foundations/clock.py --advance 12     winds its calendar twelve days on

Run it inside a trial ground (one laid by trial_ground.py). It works through
the file ground/clock there, which holds one line: `ahead: N`. The ground's
today is the real date plus N days, so the next arrival finds that N more
days have passed and lives them.

The real garden has no ground/clock and keeps the real calendar; this file
will not give it one. The clock only winds forward: a day that has been
lived is never lived again.

The clock is also what makes a ground a trial ground: only a ground that has
one honours the environment variable GLEBE_TODAY (a date that overrides the
clock). The real garden ignores that variable, so a stray one left in a
shell can never live its days ahead of time. Prefer winding the clock:
GLEBE_TODAY moves every file's date along with the calendar, so what depends
on when a file was written (a seed sown on the day it was planted, a note
left at the gate "since then") cannot be tried with it; the clock keeps file
dates honest.
"""

import datetime
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent        # the ground this file stands in
CLOCK = ROOT / "ground" / "clock"
WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
MONTHS = ("January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December")


def ahead() -> int:
    """How far the clock is wound already, as the file says. A file no one can read says 0."""
    try:
        text = CLOCK.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0
    found = re.search(r"^\s*ahead\s*:\s*(-?\d{1,6})", text, re.MULTILINE)
    return int(found.group(1)) if found else 0


def wind(days) -> int:
    """Wind the clock `days` further on. Returns how far ahead it now is.

    Each winding is noted with the real moment it was done, so the ground
    can tell which clock a file was written under: a seed planted before a
    winding was planted on the earlier day, and lives the days wound past.
    """
    total = ahead() + days
    try:
        earlier = [line for line in CLOCK.read_text(encoding="utf-8", errors="replace").splitlines()
                   if line.strip().startswith("wound:")]
    except OSError:
        earlier = []
    moment = datetime.datetime.now().isoformat()        # to the microsecond: files are dated as finely
    with open(CLOCK, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("# This is a trial ground, with a clock of its own. foundations/clock.py winds it.\n"
                     "ahead: %d\n" % total)
        handle.write("".join(line.strip() + "\n" for line in earlier[-200:]))
        handle.write("wound: %s  to %d\n" % (moment, total))
    return total


def asked(arguments):
    """The number of days asked for: from `--advance 12`, `--advance=12` or a bare `12`. None if none was."""
    for at, argument in enumerate(arguments):
        if argument.startswith("--advance="):
            argument = argument.split("=", 1)[1]
        elif argument == "--advance":
            argument = arguments[at + 1] if at + 1 < len(arguments) else ""
        if re.fullmatch(r"[-+]?\d{1,6}", argument.strip()):
            return int(argument)
    return None


def main(arguments) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if "--help" in arguments or "-h" in arguments:
        print(__doc__.strip())
        return 0
    if not CLOCK.is_file():
        print("This ground has no clock: it keeps the real calendar. Only a trial ground can be wound on\n"
              "(python shed/foundations/trial_ground.py <path> lays one).")
        return 1
    days = asked(arguments)
    if days is not None and days < 0:
        print("The clock only winds forward.")
        return 1
    try:
        total = wind(days) if days else ahead()
    except OSError as error:
        print("The clock could not be wound: %s" % error)
        return 1
    today = datetime.date.today() + datetime.timedelta(days=total)
    said = "%s %d %s %d" % (WEEKDAYS[today.weekday()], today.day, MONTHS[today.month - 1], today.year)
    if days:
        print("Wound %d day%s on. In this ground it is now %s (%d ahead of the real calendar)."
              % (days, "" if days == 1 else "s", said, total))
    else:
        print("In this ground it is %s (%d ahead of the real calendar)." % (said, total))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
