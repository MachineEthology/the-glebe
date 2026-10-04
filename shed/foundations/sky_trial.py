"""The sky, on trial.

    python shed/foundations/sky_trial.py [garden root]

Anyone who changes `shed/sky.py` can run this to know the sky still holds. It
reads the garden's `ground/place` (for its latitude and weather seed) and its
`gate/sky.txt`, and changes nothing in the garden: every ground it needs to
write in, it builds in the system's temp folder and removes afterwards. It
never uses the network.

It prints, with one verdict line for each check:

  the astronomy      the moon against six eclipses (which are exact new and
                     full moons), the length of the day at the solstices and
                     equinoxes, the poles
  the climate        ten reckoned years, month by month, against the figures
                     in the design record, and four weeks of it to look at
  purity             the same day gives the same sky in a fresh process, asked
                     in any order, alone or among its neighbours; odd places,
                     beds, and what `python shed/sky.py` says
  the gate reader    hand-written lines in English and French, and nonsense:
                     whole days (GATE_LINES), single sentences (HEARD), the
                     ways a date may be written, two lines for one day, a
                     day called clear on days this garden's sky made wet, and
                     the garden's own words for a day copied back to the gate;
                     and Ruling 11 over a year of days: a doubtful line
                     (SILENT) changes no number, and a line with no frost in
                     it (NO_FROST_SAID) makes no frost
  the keeper's view  what `python shed/sky.py --gate` and `<date>` show them
  weather of one's   what --help says of trying a kind under weather the
    own              reckoned sky never makes, and that it is so: a drought
                     written at a trial ground's gate, `python shed/sky.py
                     <day> to <day>` against sky_for, and a run too long (or
                     backwards) for one line, said rather than cut in silence
  the real sky       a canned answer from open-meteo, read and kept; answers
                     no sky could have, days nobody asked for, a server that
                     says nothing or never finishes; and proof that nothing
                     goes near the network unless the keeper has turned the
                     real sky on

The gate reader prefers silence to invention (Ruling 11 of the design
record). Before teaching it a word, ask whether that word could mean anything
else in a line about a garden; if it could, leave it out. If you do add one,
put it in the tables in `sky.py`, add a sentence that uses it to HEARD below,
and a sentence where it must NOT be heard to SILENT, and run this. Where a
line is doubtful, the right answer here is that the numbers do not change.

The ten years are this garden's own: its weather seed, from the day it was
laid. Another seed is another decade, a little warmer or drier than this one;
over many seeds the climate comes to about 11.5 °C, 152 wet days, 710 mm and
37 frost nights a year, and a single decade wanders around that (by about a
quarter of a degree, seven days, fifty millimetres, five nights). So with a
seed of your own, a figure may now and then step just outside its band.

The live call to open-meteo.com is the one thing this trial cannot try.
"""

from __future__ import annotations

import contextlib
import datetime
import importlib
import io
import json
import math
import os
import random
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True        # leave no __pycache__ in the shed, as the doors leave none

HERE = os.path.dirname(os.path.abspath(__file__))
SHED = os.path.dirname(HERE)
sys.path.insert(0, SHED)

import sky  # noqa: E402  (the shed has to be on the path first)

Date = datetime.date
DAY = datetime.timedelta(days=1)

held = 0
failed = []


def check(holds: bool, words: str) -> bool:
    """Print one verdict line and keep the count."""
    global held
    if holds:
        held += 1
        print(f"  ok     {words}")
    else:
        failed.append(words)
        print(f"  FAILS  {words}")
    return bool(holds)


def heading(words: str) -> None:
    print()
    print(words.upper())


def write(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as file:
        file.write(text)


def read(path: str) -> str:
    """A file's text, or nothing if it is not there."""
    try:
        with open(path, encoding="utf-8", errors="replace") as file:
            return file.read()
    except OSError:
        return ""


def trial_ground(base: str, name: str, where: dict, gate: str | None = None, **changes) -> str:
    """A bare ground in the temp folder with the garden's own place (and the changes asked for)."""
    root = os.path.join(base, name)
    lines = {"laid": where["laid"].isoformat(), "latitude": where["latitude"],
             "weather-seed": where["weather-seed"], "real-sky": "no", "longitude": ""}
    lines.update(changes)
    write(os.path.join(root, "ground", "place"), "".join(f"{key}: {value}\n" for key, value in lines.items()))
    if gate is not None:
        write(os.path.join(root, "gate", "sky.txt"), gate)
    return root


def alike(these: list, those: list) -> bool:
    """The same skies? (Compared as text, since each reloading of sky.py makes its Sky class anew.)"""
    return [repr(one) for one in these] == [repr(one) for one in those]


# ─────────────────────────────────────────────────────────────── the astronomy

ECLIPSES = (
    # day, phase, what it was, hour and minute (UT) of the exact new or full moon
    ("2024-04-08", 0.0, "total eclipse of the sun", 18, 21),
    ("2026-08-12", 0.0, "total eclipse of the sun", 17, 37),
    ("2027-08-02", 0.0, "total eclipse of the sun", 10, 5),
    ("2025-03-14", 0.5, "total eclipse of the moon", 6, 55),
    ("2025-09-07", 0.5, "total eclipse of the moon", 18, 9),
    ("2026-03-03", 0.5, "total eclipse of the moon", 11, 38),
)


def circle_gap(a: float, b: float) -> float:
    """How far apart two phases are, the short way round."""
    return abs((a - b + 0.5) % 1.0 - 0.5)


def try_moon() -> None:
    for iso, phase, what, hour, minute in ECLIPSES:
        day = Date.fromisoformat(iso)
        found = sky.moon(day)
        at_instant = sky._moon_phase(sky._centuries(day, hour + minute / 60.0))
        minutes = circle_gap(at_instant, phase) * 29.530589 * 24 * 60
        check(circle_gap(found, phase) <= 0.03 and minutes <= 15,
              f"{iso}, {what}: moon() says {found:.3f} ({sky.moon_name(found)}) at noon, "
              f"and is {minutes:.0f} min from the true instant")
    names = [sky.moon_name(step / 8.0) for step in range(8)]
    check(tuple(names) == sky.MOON_NAMES, "the eight names of the moon, in order: " + ", ".join(names))
    edge = sky.NAMED_PHASE
    sides = [(sky.moon_name(round(at - edge, 3)), sky.moon_name(round(at + edge, 3))) for at in (0.0, 0.25, 0.5, 0.75)]
    check(sides == [("new",) * 2, ("first quarter",) * 2, ("full",) * 2, ("last quarter",) * 2]
          and sky.moon_name(0.036) == "waxing crescent" and sky.moon_name(0.964) == "waning crescent",
          f"new, full and the quarters keep their name as far one side as the other ({edge} of a round)")
    phases = [sky.moon(Date(2026, 10, 1) + n * DAY) for n in range(60)]
    steps = [(b - a) % 1.0 for a, b in zip(phases, phases[1:])]
    check(all(0.028 < step < 0.040 for step in steps),
          f"the moon moves on each day by about a thirtieth of its round ({min(steps):.3f} to {max(steps):.3f})")


def try_daylength() -> None:
    for iso, about, name in (("2026-06-21", 15.9, "June solstice"), ("2026-12-21", 8.5, "December solstice"),
                             ("2026-03-20", 12.1, "March equinox"), ("2026-09-23", 12.1, "September equinox")):
        hours = sky.daylength(47.0, iso)
        check(abs(hours - about) <= 0.25, f"day length at 47° north, {name}: {hours:.2f} h (about {about})")
    polar = [sky.daylength(latitude, iso) for latitude in (90, 80, 70, -70, -80, -90)
             for iso in ("2026-06-21", "2026-12-21")]
    check(polar == [24.0, 0.0] * 3 + [0.0, 24.0] * 3,
          "beyond the polar circles the day is 24 h or 0 h, and nothing is raised")
    odd = [sky.daylength(latitude, "2026-06-21") for latitude in (float("nan"), "north", None, 1e9)]
    check(all(hours == sky.daylength(47.0, "2026-06-21") for hours in odd),
          "a latitude that cannot be read is taken as the garden's own 47°")


def try_seasons() -> None:
    north = [sky.season(47.0, Date(2026, month, 15)) for month in range(1, 13)]
    south = [sky.season(-33.0, Date(2026, month, 15)) for month in range(1, 13)]
    check((north[0], north[3], north[6], north[9]) == ("winter", "spring", "summer", "autumn")
          and (south[0], south[6]) == ("summer", "winter"),
          "the seasons go by calendar month, and are flipped south of the equator")


# ───────────────────────────────────────────────────────────────── the climate

def correlation(a: list, b: list) -> float:
    mean_a, mean_b = statistics.fmean(a), statistics.fmean(b)
    above = sum((x - mean_a) * (y - mean_b) for x, y in zip(a, b))
    below = (sum((x - mean_a) ** 2 for x in a) * sum((y - mean_b) ** 2 for y in b)) ** 0.5
    return above / below if below else 0.0


def ten_years(root: str, first: datetime.date) -> list:
    """The sky of every day of ten years, from `first`."""
    last = first.replace(year=first.year + 10, day=min(first.day, 28))
    return [sky.sky_for(root, first + n * DAY) for n in range((last - first).days)]


def month_table(skies: list) -> list:
    """Print the ten years by month; returns the mean temperature of each month."""
    print("         low   high   mean   rain  wet days   frost  snow  cloud   light  ground  wind  wettest")
    print("          °C     °C     °C     mm   (>0 mm)  nights  days   0..1  h a day  0..1    Bft   day mm")
    means = []
    for month in range(1, 13):
        of = [s for s in skies if s.date.month == month]
        means.append(statistics.fmean(s.tmean for s in of))
        print(f"  {Date(2001, month, 1):%b}  {statistics.fmean(s.tmin for s in of):6.1f} "
              f"{statistics.fmean(s.tmax for s in of):6.1f} {means[-1]:6.1f} {sum(s.rain for s in of) / 10:6.0f} "
              f"{sum(s.rain > 0 for s in of) / 10:8.1f} {sum(s.frost for s in of) / 10:8.1f} "
              f"{sum(s.snow for s in of) / 10:5.1f} {statistics.fmean(s.cloud for s in of):6.2f} "
              f"{statistics.fmean(s.light for s in of):7.1f} {statistics.fmean(s.wet for s in of):7.2f} "
              f"{statistics.fmean(s.wind for s in of):6.1f} {max(s.rain for s in of):8.1f}")
    return means


RECORD_SEED = 20260930    # the weather seed the design record's figures were measured on


def figure_note(holds: bool, words: str) -> bool:
    """A figure under another garden's seed: within its band it holds; outside it, it is told, not failed."""
    global held
    if holds:
        held += 1
        print(f"  ok     {words}")
    else:
        print(f"  note   {words}: outside the record's band, by this garden's own ten years")
    return bool(holds)


def try_figures(skies: list, means: list, south: bool, seed=RECORD_SEED) -> None:
    """The ten years against the figures in the design record.

    The figures were measured on the record's own seed. Under another garden's seed a figure may fall
    just outside its band by the luck of ten years (about one seed in twenty does), so there a miss is
    told as a note and not counted as a failure.
    """
    measure = check if seed == RECORD_SEED else figure_note
    years = len(skies) / 365.25
    mean = statistics.fmean(s.tmean for s in skies)
    measure(abs(mean - 11.5) <= 0.6, f"mean temperature {mean:.2f} °C (the record says about 11.5)")
    wet = sum(s.rain > 0 for s in skies) / years
    soaking = sum(s.rain >= 1 for s in skies) / years
    measure(125 <= wet <= 175, f"{wet:.0f} wet days a year, {soaking:.0f} of them with 1 mm or more (about 150)")
    rain = sum(s.rain for s in skies) / years
    measure(580 <= rain <= 820, f"{rain:.0f} mm of rain a year (about 700)")
    frosts = [s.date for s in skies if s.frost]
    measure(25 <= len(frosts) / years <= 50, f"{len(frosts) / years:.1f} frost nights a year (25 to 50)")
    cold_months = (5, 6, 7, 8, 9) if south else (11, 12, 1, 2, 3)
    share = sum(day.month in cold_months for day in frosts) / max(1, len(frosts))
    measure(share >= 0.85, f"{100 * share:.0f} % of the frosts fall in the five cold months (mostly November to March)")

    usual = [(sky.usual_warmth(Date(2027, 1, 1) + n * DAY, south), Date(2027, 1, 1) + n * DAY) for n in range(365)]
    coldest, warmest = min(usual)[1], max(usual)[1]
    check((coldest.month, warmest.month) in ((1, 7), (7, 1)) and 10 <= coldest.day <= 28 and 10 <= warmest.day <= 28,
          f"the season's curve is coldest on {coldest:%d %B} and warmest on {warmest:%d %B}; "
          f"in these ten years the coldest month was {Date(2001, means.index(min(means)) + 1, 1):%B}, "
          f"the warmest {Date(2001, means.index(max(means)) + 1, 1):%B}")
    step = max(abs(a[0] - b[0]) for a, b in zip(usual, usual[1:]))
    check(step < 0.15, f"the seasons arrive by degrees: the usual warmth never moves more than {step:.2f}° in a day")


def try_feel(skies: list, seed: int, south: bool) -> None:
    """Does it feel like weather: spells, runs of rain, and no guessing it."""
    spell = [s.tmean - sky.usual_warmth(s.date, south) for s in skies]
    next_day, next_month = correlation(spell, spell[1:]), correlation(spell, spell[30:])
    check(next_day >= 0.6 and next_month <= 0.3,
          f"spells last days, not months: warmth follows yesterday's ({next_day:.2f}), "
          f"a week ago's less ({correlation(spell, spell[7:]):.2f}), a month ago's hardly ({next_month:.2f})")
    after_wet = [b.rain > 0 for a, b in zip(skies, skies[1:]) if a.rain > 0]
    after_dry = [b.rain > 0 for a, b in zip(skies, skies[1:]) if a.rain == 0]
    p_wet, p_dry = statistics.fmean(after_wet), statistics.fmean(after_dry)
    check(p_wet - p_dry >= 0.3,
          f"rain comes in runs: after a wet day {100 * p_wet:.0f} % are wet, after a dry one {100 * p_dry:.0f} %; "
          f"a run of rain lasts {1 / (1 - p_wet):.1f} days on average")
    other = [sum(sky.reckon(seed + 1, s.date, south)[end] for end in ("tmin", "tmax")) / 2
             - sky.usual_warmth(s.date, south) for s in skies]
    year_on, elsewhere = correlation(spell, spell[365:]), correlation(spell, other)
    check(abs(year_on) < 0.15 and abs(elsewhere) < 0.15,
          f"not to be guessed: this day last year says nothing of today ({year_on:+.2f}), "
          f"and the next seed along is another country ({elsewhere:+.2f})")
    one_line = re.compile(r"^[a-z ]+, -?\d+(\.\d)?(–| to )-?\d+(\.\d)?°, (frost, )?(no rain|(rain|snow) [\d.]+ mm), "
                          r"(strong wind, |gale, )?light \d+\.\d h, (new moon|full moon|moon [a-z ]+)$")
    check(all(one_line.match(s.words) for s in skies),
          f"every one of the {len(skies)} days says itself in one plain line")
    slight = [s for s in skies if -0.5 <= s.tmin < 0]
    check(all(s.frost and re.search(r", -0\.\d to ", s.words) for s in slight)
          and not any(t == 0 and math.copysign(1.0, t) < 0 for s in skies for t in (s.tmin, s.tmax, s.tmean)),
          f"the {len(slight)} frosts too slight to round to a degree still show "
          f"({slight[0].words.split(', frost')[0] if slight else 'none here'}), and no temperature is ever a -0.0")


def try_odd_skies() -> None:
    """A Sky made by hand with no number in it still says itself."""
    whole = dict(date=Date(2026, 10, 4), cloud=0.5, wind=2.0, daylength=11.0, light=7.0, wet=0.5,
                 moon=0.3, season="autumn", source="reckoned")
    nan, endless = float("nan"), float("inf")
    odd = [sky.Sky(tmin=low, tmax=high, rain=rain, **whole)
           for low, high, rain in ((nan, nan, 0.0), (-endless, endless, endless), (-0.3, 7.0, nan), (-0.0, 0.0, 0.2))]
    try:
        said = [one.words for one in odd]
    except Exception as trouble:
        check(False, f"a sky with NaN or infinity in it raised {type(trouble).__name__} when asked for its words")
        return
    check(said[0].startswith("sun and cloud, ?°, no rain") and "?°, frost, rain ? mm" in said[1]
          and ", -0.3 to 7°, frost, " in said[2] and ", 0–0°, snow 0.2 mm" in said[3],
          f"a sky with NaN or infinity in it still says itself, and raises nothing: {said[1]}")


def try_climate(base: str, where: dict) -> None:
    seed, south, first = where["weather-seed"], where["latitude"] < 0, where["laid"]
    heading(f"The reckoned climate: ten years from {first.isoformat()}, weather-seed {seed}")
    skies = ten_years(trial_ground(base, "climate", where), first)
    means = month_table(skies)
    print()
    try_figures(skies, means, south, seed)
    try_feel(skies, seed, south)
    try_odd_skies()
    print()
    print("  Four weeks of it, to look at (from the day the ground was laid):")
    for found in skies[:28]:
        print(f"    {found.date:%a %d %b}  {found.words:<78} {'▪' * min(30, round(found.rain))}")


# ────────────────────────────────────────────────────────────────────── purity

CHILD = """
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")    # the keeper's accents must cross the pipe whole
sys.path.insert(0, sys.argv[1])
import sky
for iso in sys.argv[3:]:
    print(repr(sky.sky_for(sys.argv[2], iso)))
print("network" if "urllib.request" in sys.modules else "no network")
"""


def fresh_process(root: str, days: list) -> tuple:
    """The skies of those days as a fresh Python process sees them, and whether it loaded urllib."""
    command = [sys.executable] + (["-B"] if sys.dont_write_bytecode else []) + ["-c", CHILD, SHED, root]
    done = subprocess.run(command + [day.isoformat() for day in days],
                          capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    lines = (done.stdout or "").splitlines()
    return lines[:-1], (lines[-1] if lines else "nothing came back: " + (done.stderr or "")[-300:])


def try_processes(root: str, first: datetime.date) -> None:
    days = [first + n * DAY for n in range(0, 400, 7)]
    here = [repr(sky.sky_for(root, day)) for day in days]
    there, network = fresh_process(root, days)
    check(there == here, f"a fresh process gives the same {len(days)} skies, to the last digit")
    backwards, _ = fresh_process(root, days[::-1])
    check(backwards == here[::-1], "asked backwards in another fresh process: the same")
    shuffled = days[:]
    random.Random(7).shuffle(shuffled)
    mixed, _ = fresh_process(root, shuffled)
    check(sorted(mixed) == sorted(here), "asked in a shuffled order: the same")
    alone, _ = fresh_process(root, [days[20]])
    check(alone == [here[20]], f"{days[20].isoformat()} asked all alone, no neighbour before it: the same")
    check(network == "no network", "and that fresh process never loaded urllib at all")

    importlib.reload(sky)                                           # forget everything, as a new process would
    started = time.perf_counter()
    run = [sky.sky_for(root, first + n * DAY) for n in range(400)]
    took = time.perf_counter() - started
    check(took < 1.0, f"400 consecutive days in {took:.2f} s (well under a second)")
    check([repr(one) for one in run[::7]] == here, "and those 400, asked in a row, agree with the ones asked apart")


def try_changes(root: str, day: datetime.date, gate_text: str) -> None:
    """A line written at the gate is heard at once, and leaves no trace when it is taken away.

    The lines are written on a day (and the day three before it) that the garden's own gate leaves free:
    a line of the keeper's for that day would be heard together with them.
    """
    taken = sky._gate_days(gate_text)
    while day in taken or day - 3 * DAY in taken:
        day += DAY
    gate = os.path.join(root, "gate", "sky.txt")
    before = sky.sky_for(root, day)
    write(gate, gate_text + f"\n{(day - 3 * DAY).isoformat()}: rain 30mm\n{day.isoformat()}: 2 / 5°, snow\n")
    during = sky.sky_for(root, day)
    write(gate, gate_text)
    after = sky.sky_for(root, day)
    check(during.source == "gate" and during.tmax == 5 and during.snow
          and (during.wet > before.wet or during.wet >= 0.97),
          f"a line written at the gate is heard at once ({during.words}; "
          f"the ground wetter, {before.wet} → {during.wet}, from the rain written three days back)")
    check(repr(after) == repr(before), "and when the line is taken away again, the first answer comes back exactly")


def try_odd_places(base: str, where: dict, day: datetime.date) -> None:
    """A garden with no place, a garbled one, a southern one with a word for a seed."""
    bare = os.path.join(base, "no-place-at-all")
    garbled = trial_ground(base, "garbled", where)
    with open(os.path.join(garbled, "ground", "place"), "wb") as file:
        file.write(b"\xff\xfe\x00latitude: north of here\nweather-seed:\nlaid: soon\n\x00\x01real-sky: perhaps\n::::\n")
    os.makedirs(os.path.join(garbled, "gate", "sky.txt"))          # a folder where the file should be
    default = sky.DEFAULT_PLACE
    known = [{key: sky.place(root)[key] for key in default} for root in (bare, garbled)]
    check(known == [default, default] and not sky.troubles
          and repr(sky.sky_for(bare, day)) == repr(sky.sky_for(garbled, day)),
          f"no ground/place, or a garbled one, still has a sky (the defaults): {sky.sky_for(bare, day).words}")
    worded = trial_ground(base, "worded", where,
                          **{"weather-seed": "marigold", "latitude": "-41.3  (a southern garden)"})
    southern = sky.sky_for(worded, Date(2027, 1, 15))
    check(southern.season == "summer" and southern.tmax > 15 and sky.place(worded)["latitude"] == -41.3,
          f"a word will do for a weather seed, and a southern garden has its summer in January ({southern.words})")
    def lettered(pairs) -> list:
        found = [sky.place(trial_ground(base, "lettered", where, latitude=latitude, longitude=longitude))
                 for latitude, longitude in pairs]
        return [(one["latitude"], one["longitude"]) for one in found]

    after = lettered((("41.3 S", "10,69° O"), ("41,3° sud", "10.69 W"), ("47.0 N", "10,69° E"), (".5", "-.5")))
    check(after == [(-41.3, -10.69), (-41.3, -10.69), (47.0, 10.69), (0.5, -0.5)],
          f"a hemisphere written as a letter is heard (41.3 S, and 10,69° O for ouest, are {after[0]})")
    before = lettered((("S 41.3", "W 10.69"), ("41°18' S", "10°41'24\" O"), ("−41.3", "–10.69")))
    check(before == [(-41.3, -10.69)] * 3,
          "and so is the letter before the number, or after the minutes (41°18' S is -41.3), or a typographic minus (−41.3)")
    talk = lettered((("47.0 sud de la rivière", "10.69 West Sussex"), ("41.3 (south of the river)", "10.69 o.k.")))
    check(talk == [(47.0, 10.69), (41.3, 10.69)],
          "but a word that goes on to say something else is no hemisphere: '47.0 sud de la rivière' is 47 north")
    laid = [sky.place(trial_ground(base, "laid", where, laid=written))["laid"]
            for written in ("2026-10-15", "15/10/2026", "15 octobre 2026", "le 15 oct. 2026", "soon")]
    check(laid == [Date(2026, 10, 15)] * 4 + [default["laid"]],
          "`laid:` is read any way the gate reads a date (15/10/2026, 15 octobre 2026); 'soon' is the default")
    notepad = trial_ground(base, "notepad", where)
    with open(os.path.join(notepad, "ground", "place"), "wb") as file:
        file.write("latitude: -33.9\nweather-seed: 7\n".encode("utf-16"))
    check(sky.place(notepad)["latitude"] == -33.9 and sky.place(notepad)["weather-seed"] == 7,
          "a place saved by Notepad as \"Unicode\" (UTF-16) is read all the same")


def try_beds(root: str, day: datetime.date) -> None:
    """`local`: the same sky as a bed feels it."""
    over = sky.sky_for(root, day)

    class Wall:                                                     # a bed as the ground will hand it over
        light, water, shelter = 0.35, 0.5, 0.9

    as_keys = {"light": "0.35      share of the sky's light", "water": "0.5", "shelter": "0.9"}
    felt, by_keys = sky.local(over, Wall()), sky.local(over, as_keys)
    right = (felt.light == round(over.light * 0.35, 2) and felt.rain == round(over.rain * 0.5, 1)
             and felt.wet == round(min(1.0, over.wet * 0.5), 2) and felt.wind == round(over.wind * 0.28, 1)
             and felt.tmin == round(min(over.tmax, over.tmin + 2.25), 1) and felt.tmax == over.tmax)
    check(right and felt == by_keys,
          f"behind the north wall (light 0.35, water 0.5, shelter 0.9): low {over.tmin} → {felt.tmin}°, "
          f"light {over.light} → {felt.light} h, wind {over.wind} → {felt.wind}")
    plain = sky.local(over, {})
    check(plain == sky.local(over, None) == sky.local(over, {"light": "?", "water": None, "shelter": float("nan")})
          and plain.light == over.light and plain.rain == over.rain and plain.tmin == round(over.tmin + 1.25, 1),
          "a bed that says nothing of itself has light 1, water 1, shelter 0.5; one that says nonsense, the same")
    import hands
    written = {"light": ".35", "water": "-.5   (a joke)", "shelter": "1e-1"}
    felt = sky.local(over, written)
    as_hands = [hands.num(written, name, default, 0, most)
                for name, default, most in (("light", 1, 1), ("water", 1, 5), ("shelter", 0.5, 1))]
    check(as_hands == [0.35, 0.0, 0.1] and felt.light == round(over.light * 0.35, 2) and felt.rain == 0
          and felt.wind == round(over.wind * (1.0 - 0.8 * 0.1), 1),
          "a bed's numbers are read as hands.num reads them: '.35' is 0.35, '-.5' is none at all, '1e-1' a tenth")

    class Thorny:                                                   # a bed whose own numbers cannot be had
        light = 10 ** 400

        @property
        def water(self):
            raise RuntimeError("no")

    try:
        thorny = sky.local(over, Thorny())
        check(thorny.light == over.light and thorny.rain == over.rain,
              "a bed whose numbers are endless, or raise when asked for, is felt as a plain bed")
    except Exception as trouble:
        check(False, f"a thorny bed raised {type(trouble).__name__}: {trouble}")
    check(over.tmean == round((over.tmin + over.tmax) / 2, 2) and over.warmth == round(max(0.0, over.tmean - 5), 2)
          and over.frost == (over.tmin < 0) and over.moon_name == sky.moon_name(over.moon),
          f"tmean {over.tmean}, warmth {over.warmth}, frost {over.frost}, moon {over.moon_name}: as the record defines them")


def said_by(arguments: list, root: str) -> str:
    """What `python shed/sky.py <arguments>` would print, were its shed in the garden at `root`."""
    printed = io.StringIO()
    with contextlib.redirect_stdout(printed):
        sky._say(arguments, root)
    return printed.getvalue()


def try_saying(base: str, where: dict) -> None:
    """`python shed/sky.py`: its today is the garden's today, and it says when it could not read a date."""
    root = trial_ground(base, "wound", where)
    write(os.path.join(root, "ground", "clock"), "# a trial ground\nahead: 287\nwound: 2026-09-30T12:00:00  to 287\n")
    given = os.environ.pop("GLEBE_TODAY", None)
    try:
        wound = (Date.today() + 287 * DAY).isoformat()
        check(sky._garden_today(root) == Date.today() + 287 * DAY and said_by([], root).startswith(wound),
              f"on a trial ground wound 287 days on, `python shed/sky.py` says the sky of {wound}, as the doors would")
        os.environ["GLEBE_TODAY"] = "2027-03-01"
        check(said_by([], root).startswith("2027-03-01"), "and GLEBE_TODAY comes before the clock, as it does at the doors")
        os.environ["GLEBE_TODAY"] = "2027-3-1"                      # not a date to ground.today, so not one here
        write(os.path.join(root, "ground", "clock"), "ahead: 5\nahead: soon\n")
        check(sky._garden_today(root) == Date.today() + 5 * DAY,
              "both are read just as the doors read them: GLEBE_TODAY=2027-3-1 is no date, "
              "and `ahead: 5` then `ahead: soon` is 5")
    finally:
        os.environ.pop("GLEBE_TODAY", None)
        if given is not None:
            os.environ["GLEBE_TODAY"] = given
    for asked in ("yesterday", "2026-02-30"):
        lines = said_by([asked], root).splitlines()
        check(len(lines) >= 2 and asked in lines[0] and "could not read" in lines[0] and lines[1].startswith("20"),
              f"`python shed/sky.py {asked}` says so, then gives today: {lines[0] if lines else 'nothing'}")
    check(said_by(["2026-10-04"], root).startswith("2026-10-04  ") and "sky_for(root, day)" in said_by(["--help"], root)
          and said_by(["4 octobre 2026"], root).startswith("2026-10-04  ")
          and said_by(["04/10/2026"], root).startswith("2026-10-04  "),
          "a date it can read is answered for that day (2026-10-04, 4 octobre 2026, 04/10/2026); --help says what this file is")
    words = said_by(["--words"], root)
    check("pluie" in words and "demain" in words and "9 à 15°" in words,
          "`python shed/sky.py --words` lists the words the reader knows, and the shapes of the numbers")


def try_report(base: str, where: dict) -> None:
    """`python shed/sky.py --gate`: each of their lines, the day it was read for, what it changed; and the undated ones."""
    heading("What the keeper is shown: python shed/sky.py --gate, and python shed/sky.py <date>")
    nothing = trial_ground(base, "report-none", where)
    check("There is no gate/sky.txt yet" in said_by(["--gate"], nothing),
          "with no gate/sky.txt, --gate says so, and shows what a line looks like")
    gate = ("# le ciel, comme je l'ai vu\n"
            "2026-10-04: pluie 6mm, 9 à 15°, gris toute la journée\n"
            "2026-10-05: Bois livré à 9h, gel ce matin, demain pluie\n"
            "2026-10-06: sec\n2026-10-06: pluie\n"
            "2026-10-07 to 2026-10-16: dry\n"
            "2026-12-25: Noël : soleil, -2 à 5, merle au mur\n"
            "vendredi 9 : gel\nsemaine prochaine : du vent\n")
    root = trial_ground(base, "report", where, gate=gate)
    write(os.path.join(root, "ground", "almanac"),
          "2026-10-04  rain 2 mm · 9–16° · light 6.1 h · wind 2 · moon last quarter · autumn  [reckoned]\n")
    os.environ["GLEBE_TODAY"] = "2026-10-05"
    try:
        report = said_by(["--gate"], root)
        one_day = said_by(["2026-10-05"], root)
    finally:
        os.environ.pop("GLEBE_TODAY", None)
    print("\n".join("    | " + line for line in report.splitlines()[:40]))
    print("    | ...")
    expected = ("Sunday 4 October 2026", '"pluie 6mm": rain, 6 mm', '"9 à 15°": a low of 9°; a high of 15°',
                "Changed: ", "has already been lived",
                '"Bois livré à 9h": left alone: the reader does not know the words "Bois", "livré" and "h"',
                '"gel ce matin": frost', 'left alone: "demain" speaks of another day',
                "Their words disagree: rain and dry are both said of the whole day",
                "Wednesday 7 October 2026 to Friday 16 October 2026 (10 days, the same words)",
                "and 2 more days of the same words", "has not come yet",
                '"Noël": a title, naming the day or the gauge: what follows it is read',
                '"-2 à 5": a low of -2°; a high of 5°',
                "Taken all together: they call the whole day clear, and name no rain, shower or snow, so the day is dry",
                "2 lines could not be dated", '"vendredi 9 : gel"', '"semaine prochaine : du vent"')
    missing = [words for words in expected if words not in report]
    check(not missing, "--gate shows each line with its date, their own words thought by thought, what they changed, "
                       "where the day stands, the disagreements, and the lines that could not be dated"
                       + (f" (missing: {missing})" if missing else ""))
    check(one_day.startswith("2026-10-05  ") and "The keeper's words for Monday 5 October 2026:" in one_day
          and '"gel ce matin": frost' in one_day,
          "`python shed/sky.py 2026-10-05` gives the day's sky, and their words for it, thought by thought")
    noisy = trial_ground(base, "report-noise", where, gate="")
    wild = random.Random(5)
    with open(os.path.join(noisy, "gate", "sky.txt"), "wb") as file:
        file.write(b"".join(b"2026-10-%02d: " % (1 + n % 28) + bytes(wild.randrange(256) for _ in range(80)) + b"\n"
                            for n in range(200)) + "2026-10-02 to 2027-10-02: rain\n".encode("utf-8"))
    try:
        report = said_by(["--gate"], noisy)
        check("What the sky makes" in report, f"--gate over 200 lines of noise raises nothing ({len(report.splitlines())} lines said)")
    except Exception as trouble:
        check(False, f"--gate over noise raised {type(trouble).__name__}: {trouble}")


DROUGHT = ("2027-06-10", "2027-08-31", "sec, soleil, 14 à 28°")


def try_own_weather(base: str, where: dict) -> None:
    """Weather of one's own, for trying a kind: what --help says, and that it is so.

    The reckoned sky is mild, so a kind's trial under a drought or a hard
    frost is written at a trial ground's gate. A rehearsal visitor once had to
    find that by reading sky.py's code; its --help says it, and this is where
    what the help says is kept true.
    """
    heading("Weather of one's own, for trying a kind: a trial ground's gate, and python shed/sky.py <day> to <day>")
    told = sky.__doc__.split("TO TRY A KIND UNDER WEATHER OF YOUR OWN", 1)
    told = told[1].split("A day's sky is looked for", 1)[0] if len(told) == 2 else ""
    garden = os.path.dirname(SHED)
    named = ("shed/foundations/trial_ground.py", "shed/foundations/clock.py --advance", "shed/arrive.py",
             "gate/sky.txt", "--gate", "--words", f"at most {sky.RUN_DAYS} days")
    missing = [words for words in named if words not in " ".join(told.split())]
    check(told and not missing and f"at most {sky.RUN_DAYS} of them" in " ".join(sky.__doc__.split())
          and all(os.path.isfile(os.path.join(garden, *path.split()[0].split("/"))) for path in named[:3]),
          "--help tells how to try a kind under weather the reckoned sky never makes: a trial ground, its own"
          f" gate/sky.txt, its clock, its gate, and the {sky.RUN_DAYS} days one line may cover"
          + (f" (missing: {missing})" if missing else ""))
    examples = re.findall(r"^ {4}(\d{4}-\d\d-\d\d to \d{4}-\d\d-\d\d: .+?) {2,}(\S.*)$", told, re.MULTILINE)
    unheard = [(line, words) for line, _ in examples
               for words, meaning in sky.explain(line.split(": ", 1)[1]) if meaning.startswith("left alone")]
    covered = [len(sky._gate_days(line)) for line, _ in examples]
    check(len(examples) >= 3 and not unheard and all(21 <= days <= sky.RUN_DAYS for days in covered),
          f"its {len(examples)} example lines are each heard whole, every thought of them, and each covers its"
          f" run ({', '.join(str(days) for days in covered)} days)" + (f" (left alone: {unheard})" if unheard else ""))

    first, last, words = Date.fromisoformat(DROUGHT[0]), Date.fromisoformat(DROUGHT[1]), DROUGHT[2]
    span = [first + n * DAY for n in range((last - first).days + 1)]
    bare = trial_ground(base, "own-weather-bare", where)
    reckoned = [sky.sky_for(bare, day) for day in span]
    longest = max(len(run) for run in "".join("d" if one.rain <= 0 else " " for one in reckoned).split(" "))
    root = trial_ground(base, "own-weather", where,
                        gate=f"# a drought, to try a kind under\n{DROUGHT[0]} to {DROUGHT[1]}: {words}\n")
    write(os.path.join(root, "ground", "clock"), "# a trial ground\nahead: 0\n")
    lived = [sky.sky_for(root, day) for day in span]
    behind_wall = sky.local(lived[-1], {"light": 0.35, "water": 0.5, "shelter": 0.9})
    check(all(one.source == "gate" and one.rain == 0 and one.tmin == 14 and one.tmax == 28 and one.cloud <= 0.1
              for one in lived) and lived[-1].wet == 0 and behind_wall.rain == 0 and behind_wall.wet == 0,
          f"'{DROUGHT[0]} to {DROUGHT[1]}: {words}' at a trial ground's gate: {len(span)} dry days at 14–28°, the"
          f" ground dried to {lived[-1].wet} by the end, and a walled bed as dry (the reckoned sky's longest dry"
          f" run in those days was {longest})")
    after, without = sky.sky_for(root, last + DAY), sky.sky_for(bare, last + DAY)
    check(after.source == "reckoned" and after.wet == 0 <= without.wet
          and (after.tmin, after.tmax, after.rain) == (without.tmin, without.tmax, without.rain),
          f"the day after the run is reckoned again, as it would have been, but on ground the drought left dry"
          f" ({after.wet}; {without.wet} without it)")

    widest = (first - 9 * DAY, last + 15 * DAY)
    report = said_by([widest[0].isoformat(), "to", widest[1].isoformat()], root)
    days = [widest[0] + n * DAY for n in range((widest[1] - widest[0]).days + 1)]
    skies = [sky.sky_for(root, day) for day in days]
    run, best, best_from = 0, 0, None
    for one in skies:
        run = run + 1 if one.rain <= 0 else 0
        if run > best:
            best, best_from = run, one.date - (run - 1) * DAY
    gated = sum(1 for one in skies if one.source == "gate")
    listed = [line for line in report.splitlines() if re.match(r"  \d{4}-\d\d-\d\d \w{3}  ", line)]
    expected = (f"{len(days)} days, {sky._long_date(widest[0])} to {sky._long_date(widest[1])}"
                f" ({gated} from the gate, {len(days) - gated} reckoned):",
                f"the longest run without rain {best} days, from {sky._long_date(best_from)}",
                f"the coldest night {sky._degree(min(one.tmin for one in skies))}°",
                f"the warmest day {sky._degree(max(one.tmax for one in skies))}°")
    wrong = [words for words in expected if words not in report]
    check(not wrong and len(listed) == len(days)
          and all(line.endswith(f"[{one.source}]") and one.words in line for line, one in zip(listed, skies))
          and "This is a trial ground" not in report,
          f"`python shed/sky.py {widest[0]} to {widest[1]}` lists each day as sky_for gives it, and sums them"
          f" truly: {gated} from the gate, the longest dry run {best} days" + (f" (missing: {wrong})" if wrong else ""))
    print("\n".join("    | " + line for line in report.splitlines()[-5:]))
    inside = said_by([DROUGHT[0], DROUGHT[1]], root)
    check("No rain on any of them." in inside and "No frost;" in inside,
          "two days given apart are a span too, and a span inside the drought says: no rain on any of them")
    forms = [said_by(asked, root) for asked in ([f"{DROUGHT[1]} to {DROUGHT[0]}"], ["10 juin 2027 au 31 août 2027"],
                                                ["10/06/2027", "-", "31/08/2027"])]
    check(all(one == inside for one in forms),
          "a span may be written backwards, in words (10 juin 2027 au 31 août 2027), or day first: the same")
    garbled = said_by(["2027-06-01", "to", "2027-02-30"], root)
    check(garbled.startswith('I could not read two days in "2027-06-01 to 2027-02-30"') and "No rain" not in garbled,
          f"a span with a day no calendar has says so, and gives today: {garbled.splitlines()[0]}")
    check(said_by([f"{DROUGHT[0]} to {DROUGHT[0]}"], root) == said_by([DROUGHT[0]], root),
          "and a span from a day to the same day is that day, as `python shed/sky.py <date>` gives it")
    most, listed_most = sky.SPAN_MOST, sky.SPAN_LISTED
    sky.SPAN_MOST, sky.SPAN_LISTED = 40, 10
    try:
        long_one = said_by(["2027-01-01 to 2027-12-31"], root)
        short_one = said_by(["2027-01-01 to 2027-01-10"], root)
    finally:
        sky.SPAN_MOST, sky.SPAN_LISTED = most, listed_most
    cut_at = sky._long_date(Date(2027, 1, 1) + 39 * DAY)
    listed_days = [len(re.findall(r"^  2027-", one, re.MULTILINE)) for one in (long_one, short_one)]
    check("at most are gone through" in long_one and f"40 days, Friday 1 January 2027 to {cut_at}" in long_one
          and listed_days == [0, 10],
          "a span longer than SPAN_MOST is cut there and says so; one longer than SPAN_LISTED is told in sum only")

    hint = "This is a trial ground: to try a kind under weather of your own"
    plain = trial_ground(base, "own-weather-plain", where)
    trial = trial_ground(base, "own-weather-trial", where)
    write(os.path.join(trial, "ground", "clock"), "# a trial ground\nahead: 0\n")
    seen = {name: [hint in said_by(asked, ground) for asked in ([], ["--gate"], ["2027-07-01 to 2027-07-03"])]
            for name, ground in (("plain", plain), ("trial", trial))}
    in_drought = [hint in said_by(asked, root) for asked in ([DROUGHT[0]], [DROUGHT[0], DROUGHT[1]])]
    check(seen == {"plain": [False] * 3, "trial": [True] * 3} and in_drought == [False, False]
          and "2027-06-10 to 2027-08-31: sec, soleil, 14 à 28°" in said_by(["--gate"], trial),
          "on a trial ground (one with ground/clock), `python shed/sky.py`, `--gate` and a span point to its own gate;"
          " on the garden itself they never do, nor once the days asked for are already the gate's")

    cut = ("2028-03-01 to 2028-06-01: frost, -9 to -2°\n"            # 93 days: the most one line may cover
           "2028-07-01 to 2028-10-02: dry, clear, 14 to 28°\n"      # 94 days: read for its first day only
           "2029-02-20 to 2029-02-01: frost\n")                     # backwards: read for its first day only
    root = trial_ground(base, "own-weather-cut", where, gate=cut)
    days = sky._gate_days(cut)
    check(len(days) == sky.RUN_DAYS + 2 and Date(2028, 6, 1) in days and Date(2028, 7, 2) not in days
          and Date(2029, 2, 20) in days and Date(2029, 2, 19) not in days,
          f"a run of {sky.RUN_DAYS} days is read whole; one of {sky.RUN_DAYS + 1}, or one written backwards,"
          " for its first day only, as before")
    report, inside, one_day = (said_by(["--gate"], root), said_by(["2028-08-01 to 2028-08-05"], root),
                               said_by(["2028-08-01"], root))
    reasons = ['"2028-07-01 to 2028-10-02: dry, clear, 14 to 28°"', f"it runs 94 days, more than the {sky.RUN_DAYS}",
               f"so only {sky._long_date(Date(2028, 7, 1))} is given its words. Write a longer spell as several lines.",
               '"2029-02-20 to 2029-02-01: frost"',
               f"its last day ({sky._long_date(Date(2029, 2, 1))}) comes before its first",
               f"so only {sky._long_date(Date(2029, 2, 20))} is given its words. Write the earlier day first."]
    missing = [words for words in reasons if words not in report]
    check("2 lines are read for their first day only:" in report and not missing
          and "2028-03-01 to 2028-06-01" not in report.split("first day only:")[1],
          "--gate says which lines are read for their first day only, and why (too long, or backwards)"
          + (f" (missing: {missing})" if missing else ""))
    check(reasons[0] in inside and reasons[0] in one_day and "2029-02-20" not in inside
          and reasons[0] not in said_by(["2028-07-01"], root)
          and reasons[0] not in said_by(["2028-06-01 to 2028-06-30"], root),
          "a span or a day that such a line meant says so too; its first day, or days it never meant, do not")
    check("first day only" not in said_by(["--gate"], trial_ground(base, "own-weather-whole", where,
                                                                 gate=f"{DROUGHT[0]} to {DROUGHT[1]}: {words}\n")),
          "and where every run is whole, nothing of the sort is said")


def try_purity(base: str, where: dict, gate_text: str) -> None:
    heading("Purity: the same files and the same date give the same sky")
    # The garden's own gate lines, and one more with accents and a dash on a day the fresh processes are asked for.
    gate_text += f"\n{where['laid'].isoformat()}: gelée blanche à l'aube, 9–15°, éclaircies\n"
    root = trial_ground(base, "pure", where, gate=gate_text)
    try_processes(root, where["laid"])
    check("gelée blanche à l'aube" in sky.sky_for(root, where["laid"]).remark,
          "and among those skies was a line with accents and a dash in it: 'gelée blanche à l'aube, 9–15°, éclaircies'")
    day = where["laid"] + 40 * DAY
    try_changes(root, day, gate_text)
    try_odd_places(base, where, day)
    try_beds(root, day)
    try_saying(base, where)


# ───────────────────────────────────────────────────────────── the gate reader
#
# Ruling 11: the gate reader prefers silence to invention. Where a line is
# doubtful, what is expected here is that the numbers are not changed.

def same(s, r) -> bool:
    """The day's numbers exactly as they would be with no line at the gate."""
    return all(getattr(s, name) == getattr(r, name) for name in ("tmin", "tmax", "rain", "cloud", "wind"))


GATE_LINES = (
    # a line as a keeper might write it, and what must then be true of that day's sky `s`
    # (`r` is the same day with no line at the gate)
    ("2026-10-04: pluie 6mm, 9 à 15°, gris toute la journée",
     lambda s, r: s.rain == 6 and (s.tmin, s.tmax) == (9, 15) and s.cloud >= 0.85 and s.source == "gate"),
    ("2026-10-05 - beau soleil, gel le matin, -1 / 12",                   # a day they call fine is a dry one
     lambda s, r: (s.tmin, s.tmax) == (-1, 12) and s.cloud <= 0.2 and s.frost and s.rain == 0),
    ("2026-10-06 rain",
     lambda s, r: s.rain >= 1 and s.cloud >= 0.6 and s.source == "gate"),
    ("2026-10-07: rain 6mm, 9 to 15°, grey all day, strong wind",
     lambda s, r: s.rain == 6 and (s.tmin, s.tmax) == (9, 15) and s.cloud >= 0.85 and s.wind >= 6),
    ("2026-10-08 : brouillard le matin puis éclaircies, pas de vent",
     lambda s, r: s.wind <= 1 and 0.4 <= s.cloud <= 0.8 and s.words.startswith("fog")),
    ("2026-10-09: neige 4 cm",                                            # snow, but no frost they did not say
     lambda s, r: s.snow and s.rain == 4 and s.tmean <= 1 and "snow 4 mm" in s.words and (r.frost or not s.frost)),
    ("2026-10-10: sec, vent léger",
     lambda s, r: s.rain == 0 and s.wind <= 2.5),
    ("2026-10-11: no rain, overcast, min 3 max 8",
     lambda s, r: s.rain == 0 and (s.tmin, s.tmax) == (3, 8) and s.cloud >= 0.9),
    ("2026-10-12: 3° ce matin, 14° cet après-midi, quelques nuages",     # what they saw widens the day, no more
     lambda s, r: (s.tmin, s.tmax) == (min(3, r.tmin), max(14, r.tmax)) and 0.5 <= s.cloud <= 0.8),
    ("2026-10-13: fortes pluies et tempête",
     lambda s, r: s.rain >= 5 and s.wind >= 8 and "gale" in s.words),
    ("2026-10-14: il fait froid et gris",
     lambda s, r: s.tmean <= sky.usual_warmth(s.date) - 4 and s.cloud >= 0.85 and (r.frost or not s.frost)),
    ("2026-10-15: hot, not a cloud, 12 to 27",                            # "12 to 27" alone: the low and the high
     lambda s, r: (s.tmin, s.tmax) == (12, 27) and s.cloud <= 0.15 and s.rain == 0),
    ("2026-10-16: pas de pluie, pas de gel, plus de soleil qu'hier",     # "... qu'hier" speaks of yesterday
     lambda s, r: s.rain == 0 and not s.frost and s.cloud == r.cloud),
    ("2026/10/17 : light showers, 40 km/h wind",
     lambda s, r: 0 < s.rain <= 3 and 5 <= s.wind <= 6.5),
    ("* 2026-10-18: the robin came back",
     lambda s, r: s.source == "reckoned" and s.remark == "the robin came back"),
    ("2026-10-19: asdf qwerty 99999 mm °°° ---/// NaN to inf 1e999 \x00\x07 ☂☂☂",
     lambda s, r: s.source == "reckoned" and s.remark.startswith("asdf")),
    ("2026-10-20 to 2026-10-22: dry and clear",
     lambda s, r: s.rain == 0 and s.cloud <= 0.1),
    ("2026-10-05: et un merle dans le cognassier",
     lambda s, r: s.remark.endswith("un merle dans le cognassier") and s.tmin == -1),
    ("2026-10-23:", lambda s, r: s.source == "reckoned" and s.remark == ""),
    # the French no closes after the verb
    ("2026-10-25: il ne pleut pas, il ne gèle pas, pas de vent",
     lambda s, r: s.rain == 0 and not s.frost and s.wind <= 1),
    # what only stopped, or never stopped, is left alone: how much of the day was it?
    ("2026-10-26: il ne pleut plus, la pluie n'a pas cessé, il n'a pas arrêté de pleuvoir", lambda s, r: same(s, r)),
    ("2026-10-27: it isn't raining, frost-free night, la serre est hors gel",
     lambda s, r: s.rain == 0 and (s.tmin, s.tmax) == (r.tmin, r.tmax)),
    # a garden diary counts many things: numbers that are not weather stay out of the sky
    ("2026-10-28: J'ai arrosé 2 fois, il faisait 24°", lambda s, r: (s.tmin, s.tmax) == (r.tmin, max(24, r.tmax))),
    ("2026-10-29: 2 à 3 averses dans la journée, bois livré à 9h, 3 stères", lambda s, r: same(s, r)),
    ("2026-10-30: les astrances ont pris 5 cm depuis septembre, la mare a monté de 10 cm", lambda s, r: same(s, r)),
    ("2026-10-31: comme le 15 octobre, temps sec, 3 semaines sans pluie, 12°", lambda s, r: same(s, r)),
    # a high that invents no frost; cold words that invent none either
    ("2026-11-01: Toussaint. Pluie fine et froide toute la journée, 5 degrés à peine",
     lambda s, r: (r.frost or not s.frost) and 0 < s.rain <= 4.5 and s.tmean <= r.tmean),
    ("2026-11-02: sec le matin, pluie le soir", lambda s, r: s.rain > 0),
    ("2026-11-03: pas de pluie ce matin, averses cet après-midi", lambda s, r: s.rain > 0),
    ("2026-11-04: pluie le matin 4mm, l'après-midi 6mm", lambda s, r: s.rain == 10),
    # cold written partly in words
    ("2026-11-05: moins 2° ce matin, 8° l'après-midi", lambda s, r: (s.tmin, s.tmax) == (-2, max(8, r.tmax))),
    ("2026-11-06: gel à -5 cette nuit!! max 4", lambda s, r: (s.tmin, s.tmax) == (-5, 4)),
    ("2026-11-07: froid de canard, vent du nord glacial, -6 au lever, 1 au plus chaud", lambda s, r: same(s, r)),
    ("2026-11-08: 1er gel de l'année, 12° à midi", lambda s, r: same(s, r)),      # "année": another time
    ("2026-11-09: il a fait -3 cette nuit", lambda s, r: (s.tmin, s.tmax) == (min(-3, r.tmin), r.tmax)),
    ("2026-11-10: chaud le jour, froid la nuit", lambda s, r: s.source == "reckoned"),
    # two lines for one day: the second does not undo what the first measured
    ("2026-11-11: pluie 6mm", lambda s, r: s.rain == 6),
    ("2026-11-11: soleil le soir",
     lambda s, r: s.rain == 6 and s.cloud == 0.4 and s.remark == "pluie 6mm; soleil le soir"),
    # the date written day first, or in words, or after a weekday
    ("12/11/2026 : pluie 5 mm, 8 à 12°", lambda s, r: s.rain == 5 and (s.tmin, s.tmax) == (8, 12)),
    ("Le 13 novembre 2026 : neige", lambda s, r: s.snow and s.date == Date(2026, 11, 13)),
    ("dimanche 2026-11-15: pluie 9 mm", lambda s, r: s.rain == 9),
    ("Tue 17 Nov 2026: rain 3mm", lambda s, r: s.rain == 3 and s.date == Date(2026, 11, 17)),
    ("du 18/11/2026 au 19/11/2026: sec", lambda s, r: s.rain == 0 and s.date == Date(2026, 11, 18)),
    ("1er décembre 2026 - gel", lambda s, r: s.frost and s.date == Date(2026, 12, 1)),
    # a measure of something else in a line that also speaks of rain
    ("2026-12-05: herbe de 10 cm, pluie fine", lambda s, r: 0 < s.rain <= 4.5 and (s.tmin, s.tmax) == (r.tmin, r.tmax)),
    # however the line is punctuated
    ("2026-12-06: pluie 6 mm · 9 à 15° · gris",
     lambda s, r: s.rain == 6 and (s.tmin, s.tmax) == (9, 15) and s.cloud >= 0.85),
    ("2026-12-07: soleil,-3 / 5 - vent 2", lambda s, r: (s.tmin, s.tmax) == (-3, 5) and s.wind == r.wind and s.cloud <= 0.2),
    # their no to snow is a no, however cold the day
    ("2026-12-08: pluie froide 3 mm, -2 à 1, pas de neige",
     lambda s, r: s.rain == 3 and not s.snow and s.frost and ", rain 3 mm" in s.words),
    # one temperature: the day is widened to hold it, and no more
    ("2027-07-14: 12° ce matin", lambda s, r: (s.tmin, s.tmax) == (min(12, r.tmin), max(12, r.tmax))),
    ("2026-12-09: gel blanc, 0°", lambda s, r: s.frost),
    ("2026-12-10: gel ce matin, 5°", lambda s, r: s.frost and s.tmax == max(5, r.tmax)),
    # other days, other things
    ("2026-12-11: pluie 4 mm, 45 mm depuis le début du mois, demain neige, 5° de plus qu'hier",
     lambda s, r: s.rain == 4 and (s.tmin, s.tmax) == (r.tmin, r.tmax) and not s.snow),
    ("2026-12-12: la neige a fondu, il en reste 3 cm au sol", lambda s, r: s.source == "reckoned"),
    # two numbers standing alone between commas are the low and the high, with no ° (GROUND.md's own example)
    ("2026-12-13: rain 6mm, 9 to 15, grey all day, strong wind",
     lambda s, r: s.rain == 6 and (s.tmin, s.tmax) == (9, 15) and s.cloud >= 0.85 and s.wind >= 6),
    ("2026-12-14: brouillard, 0 à 4",                                    # their low of 0 is no frost, their 2° no snow
     lambda s, r: (s.tmin, s.tmax) == (0, 4) and not s.frost and not s.snow and s.words.startswith("fog")),
    # a day they call clear is a dry day, so nothing falls as snow; the sun of a part of it takes no rain away
    # (try_clear_days does the same on days this garden's own sky makes wet)
    ("2026-12-15: frost, -4 to 6, clear, light wind",
     lambda s, r: (s.tmin, s.tmax) == (-4, 6) and s.frost and s.rain == 0 and not s.snow
     and s.cloud <= 0.1 and s.wind <= 2.5),
    ("2026-12-16: ciel clair", lambda s, r: s.rain == 0 and s.cloud <= 0.1 and (s.tmin, s.tmax) == (r.tmin, r.tmax)),
    ("2026-12-17: soleil le soir", lambda s, r: s.rain == r.rain and (s.rain == 0 or s.cloud >= 0.4)),
    ("2026-12-18: soleil, pluie 20 min",                             # rain named, though not read: it stays
     lambda s, r: s.rain == r.rain and (s.rain == 0 or s.cloud >= 0.4)),
    ("2026-12-19: soleil, gris", lambda s, r: s.rain == r.rain),
    # a title before a colon that names the day itself: what follows is read. Any other heading may name a thing.
    ("2026-12-25: Noël : soleil, -2 à 5, merle au mur",
     lambda s, r: (s.tmin, s.tmax) == (-2, 5) and s.rain == 0 and s.cloud <= 0.2 and s.source == "gate"),
    ("2026-12-24: fleurs : gris, rose, blanc", lambda s, r: same(s, r)),
    # the verifiers' hardest lines. Each was misheard once; where a line is doubtful, the numbers stay.
    ("2027-01-04: vent 10 à 20 km/h", lambda s, r: 2 <= s.wind <= 4 and "gale" not in s.words),
    ("2027-01-05: vent force 3-4", lambda s, r: s.wind == 3.5 and (s.tmin, s.tmax) == (r.tmin, r.tmax)),
    ("2027-01-06: comme le 2027-01-15, pluie", lambda s, r: same(s, r)),
    ("2027-01-07: comme le 12/01, pluie", lambda s, r: same(s, r)),
    ("2027-01-08: -5 à -1 cette nuit", lambda s, r: (s.tmin, s.tmax) == (min(-5, r.tmin), max(-1, r.tmax))),
    ("2027-01-09: gel -2 -5 cette nuit", lambda s, r: s.tmin == min(-5, r.tmin) and s.tmax == r.tmax and s.frost),
    ("2027-01-10: pas de pluie malgré les prévisions", lambda s, r: same(s, r)),
    ("2027-01-11: la pluie tant attendue est enfin arrivée", lambda s, r: same(s, r)),
    ("2027-01-12: pluie 20 min", lambda s, r: same(s, r)),
    ("2027-01-13: averse de 10 min, 4°", lambda s, r: (s.tmin, s.tmax) == (min(4, r.tmin), max(4, r.tmax))
     and s.rain == r.rain),
    ("2027-01-14: neige fondue, 0 à 2",                              # "fondue" unknown; "0 à 2" alone, the low and high
     lambda s, r: (s.tmin, s.tmax) == (0, 2) and (s.rain, s.cloud, s.wind) == (r.rain, r.cloud, r.wind)),
    ("2027-01-15: sec, goutte-à-goutte en route", lambda s, r: s.rain == 0 and (s.tmin, s.tmax) == (r.tmin, r.tmax)),
    ("2027-01-16: tmin 3, tmax 12, rain 6", lambda s, r: (s.tmin, s.tmax) == (3, 12) and s.rain == r.rain),
    ("2027-01-17: neige le matin; il ne neige plus", lambda s, r: s.snow and ", snow " in s.words),
    ("2027-01-18: gelée blanche", lambda s, r: s.frost),
    ("2027-01-18: il ne gèle plus", lambda s, r: s.frost),                # the frost went; it was there
    ("2027-01-19: demain : pluie, vent fort", lambda s, r: same(s, r)),
    ("2027-01-20: pluie comme le 3/11", lambda s, r: same(s, r)),
    ("2027-01-21: au lever du soleil, -3°", lambda s, r: s.tmin == min(-3, r.tmin) and s.cloud == r.cloud),
    ("2026-13-45: rain 50mm", None),                               # None: the line must be left alone
    ("rain tomorrow, probably", None),
    ("26-10-04: pluie 80mm", None),                                # which of these is the year?
    ("20 brumaire 2026: pluie 80mm", None),
    ("# 2026-10-24: a remark, not weather: rain 80mm", None),
)

HEARD = (
    # one sentence, and exactly what the reader must make of it (`sky.understand`)
    # the no, in French and English
    ("il ne pleut pas", {"rain": 0.0}),
    ("il ne gèle pas", {"frost": False}),
    ("il ne neige pas", {"snow": False}),
    ("il n'a pas plu", {"rain": 0.0}),
    ("il ne fait pas beau", {"cloud": 0.85}),
    ("il n'y a pas de vent", {"wind": 0.5}),
    ("pas de vent", {"wind": 0.5}),
    ("it isn't raining", {"rain": 0.0}),
    ("it didn't rain", {"rain": 0.0}),
    ("sans gel", {"frost": False}),
    ("no frost or snow", {"frost": False, "snow": False}),
    ("pas de pluie ou de neige", {"rain": 0.0, "snow": False}),
    ("pas un flocon de neige", {"snow": False}),
    ("gel le matin, pas de gel l'après-midi", {"frost": True}),
    ("pas de pluie beau soleil", {"cloud": 0.12, "rain": 0.0}),
    ("pas de soleil", {"cloud": 0.85}),
    # what stopped, or did not stop, or was only compared: left alone
    ("il ne pleut plus", {}),
    ("il n'y a plus de vent", {}),
    ("la pluie n'a pas cessé", {}),
    ("il n'a pas arrêté de pleuvoir", {}),
    ("it hasn't stopped raining", {}),
    ("le brouillard ne s'est pas levé", {}),
    ("plus de soleil qu'hier", {}),
    ("plus chaud qu'hier", {}),
    ("plus de pluie que prévu", {}),
    ("more rain than expected", {}),
    ("pas mal de pluie", {}),
    ("jamais vu autant de pluie", {}),
    ("pas une goutte de pluie", {}),
    ("frost-free night", {}),
    ("hors gel", {}),
    ("pluie ou neige", {}),
    ("gel et pas de gel", {}),
    ("sec, pluie", {}),
    ("chaud le jour, froid la nuit", {}),
    # words that are not weather where they stand
    ("vin sec", {}),
    ("une belle récolte", {}),
    ("le bleu des asters", {}),
    ("la boule de neige fleurit", {}),
    ("perce-neige en fleur", {}),
    ("au lever du soleil", {}),
    ("sol à 6°", {}),
    ("un angle de 45°", {}),
    ("au moins 12° à l'ombre", {}),
    ("Merle au mur", {}),
    ("fleurs : gris, rose, blanc", {}),                           # a heading it cannot read, then a colon
    ("roses : sèches", {}),                                       # dry roses, not a dry day
    ("fleurs : soleil", {}),
    ("astrances: rose pâle, gel ce matin", {}),
    ("Astrances : rose pâle. Gel ce matin", {"frost": True}),      # a new sentence is free of it
    ("Météo : pluie 6mm", {"rain": 6.0, "raining": 5.0}),
    # a title naming the day itself, or the gauge, leaves nothing alone
    ("Noël : soleil, -2 à 5, merle au mur", {"cloud": 0.1, "rain": 0.0, "tmax": 5.0, "tmin": -2.0}),
    ("Le jour de Noël : neige", {"snow": True}),
    ("Saint-Sylvestre : gel, 0 à 3", {"frost": True, "tmax": 3.0, "tmin": 0.0}),
    ("Pluviomètre : 6 mm", {"rain": 6.0}),
    ("neige à Noël ?", {}),                                        # away from a colon, Noël is not known: a wish?
    # two plain numbers standing alone, the lower first: the day's low and high
    ("9 à 15", {"tmax": 15.0, "tmin": 9.0}),
    ("9 to 15", {"tmax": 15.0, "tmin": 9.0}),
    ("0 à 4", {"tmax": 4.0, "tmin": 0.0}),
    ("9 - 15", {"tmax": 15.0, "tmin": 9.0}),
    ("10-16", {"tmax": 16.0, "tmin": 10.0}),
    ("entre 9 et 15", {"tmax": 15.0, "tmin": 9.0}),
    ("brouillard, 0 à 4", {"cloud": 0.85, "fog": True, "tmax": 4.0, "tmin": 0.0}),
    # numbers that may count something else
    ("9, 15", {}),
    ("9 -15", {}),
    ("9 / 15", {}),
    ("15 à 9", {}),                                                # the higher first: not a low and a high
    ("5 à 40", {}),                                                # too far apart for one day
    ("50 à 60", {}),
    ("de 9 à 15", {}),                                             # from 9 to 15: hours
    ("9 à 15 cette nuit", {}),
    ("pluie 5 à 10", {}),
    ("2 à 3 averses dans la journée", {}),
    ("pluie 6", {}),
    ("pluie 2 fois dans la journée", {}),
    ("de 8 à 10 ce matin il a plu", {}),
    ("wind 3", {}),
    ("vent 3 à 4", {}),
    ("vent 3 jours de suite", {}),
    ("light 4 h · wind 6", {}),
    ("pluie 20 min", {}),
    ("rain 30 minutes", {}),
    ("neige 10 minutes", {}),
    ("2 cm de pluie", {}),
    ("tondu à 5 cm, averse", {"raining": 3.0}),
    ("la mare a monté de 10 cm après la pluie", {}),
    ("il est tombé 4 cm de neige", {}),
    ("neige fondue, 0 à 2", {"tmax": 2.0, "tmin": 0.0}),
    ("Minimales 3, maximales 12", {}),
    ("force 4-5 en rafales", {}),
    ("8h30, 50 %, 14:00", {}),
    # another day, or a date: the rest of the sentence goes with it
    ("comme le 2026-10-15, pluie", {}),
    ("comme le 12/10, pluie", {}),
    ("pluie comme le 3/11", {}),
    ("comme le 15 octobre, 12°", {}),
    ("temps sec, 3 semaines sans pluie, 6°", {"rain": 0.0}),
    ("demain neige", {}),
    ("demain : pluie", {}),
    ("demain, pluie", {}),
    ("risque de gel demain", {}),
    ("pluie annoncée pour demain", {}),
    ("il faudrait de la pluie", {}),
    ("pluie comme prévu", {}),
    ("pas de pluie malgré les prévisions", {}),
    ("gel ce matin, demain pluie", {"frost": True}),
    ("gel. Demain pluie. Aujourd'hui sec", {"frost": True, "rain": 0.0}),
    ("6 mm, 45 mm depuis le début du mois", {"rain": 6.0}),
    ("cumul 45 mm depuis lundi", {}),
    ("pluie 6mm (hier 2 mm)", {"rain": 6.0, "raining": 5.0}),
    ("6 mm comme hier", {}),
    ("6 mm depuis ce matin", {}),
    ("5° de plus qu'hier", {}),
    ("10° de moins", {}),
    ("la neige a fondu", {}),
    ("il reste de la neige au sol", {}),
    # rain: amounts, and words
    ("pluie 6mm", {"rain": 6.0, "raining": 5.0}),
    ("6,5 mm", {"rain": 6.5}),
    ("0 mm", {"rain": 0.0}),
    ("entre 5 et 10 mm", {}),
    ("5 à 10 mm", {"rain": 7.5}),
    ("un peu de pluie", {"raining": 1.5}),
    ("fortes pluies", {"raining": 16.0}),
    ("herbe de 10 cm, pluie fine", {"raining": 1.5}),
    ("pluie. 30 cm de boue", {"raining": 5.0}),
    ("sec le matin, pluie le soir", {"raining": 5.0}),
    ("pluie le matin, sec ensuite", {"raining": 5.0}),
    ("pas de pluie ce matin, averses cet après-midi", {"raining": 3.0}),
    ("pluie le matin 4mm, l'après-midi 6mm", {"rain": 10.0, "raining": 5.0}),
    ("4 mm le matin, 6 mm le soir, 10 mm en tout", {"rain": 10.0}),
    ("sec, goutte-à-goutte en route", {"rain": 0.0}),
    # snow
    ("neige 4 cm", {"rain": 4.0, "snow": True}),
    ("neige, 4 cm", {"snow": True}),
    ("Neige ! 3 cm ce matin", {"snow": True}),
    ("neige 10 cm cette nuit", {"rain": 10.0, "snow": True}),
    ("neige: les astrances dépassent de 5 cm", {"snow": True}),
    ("neige le matin; il ne neige plus", {"snow": True}),
    # temperatures
    ("9 à 15°", {"tmax": 15.0, "tmin": 9.0}),
    ("9–15°", {"tmax": 15.0, "tmin": 9.0}),
    ("9°-15°", {"tmax": 15.0, "tmin": 9.0}),
    ("entre 9 et 15°", {"tmax": 15.0, "tmin": 9.0}),
    ("-1 / 12", {"tmax": 12.0, "tmin": -1.0}),
    ("-5 -1", {"tmax": -1.0, "tmin": -5.0}),
    ("-5 à -1 cette nuit", {"seen": (-5.0, -1.0)}),
    ("-3 / 5 cette nuit", {"seen": (-3.0, 5.0)}),
    ("gel, -5 à -1 ce matin", {"frost": True, "seen": (-5.0, -1.0)}),
    ("gel -2 -5 cette nuit", {"frost": True, "seen": (-5.0, -2.0)}),
    ("min 3 max 12", {"tmax": 12.0, "tmin": 3.0}),
    ("tmin 3, tmax 12, rain 6", {"tmax": 12.0, "tmin": 3.0}),
    ("tmin: 3, tmax: 12", {"tmax": 12.0, "tmin": 3.0}),
    ("Tmin 3 Tmax 12", {"tmax": 12.0, "tmin": 3.0}),
    ("gel à -5 cette nuit!! max 4", {"frost": True, "seen": (-5.0,), "tmax": 4.0}),
    ("12°", {"seen": (12.0,)}),
    ("12º", {"seen": (12.0,)}),
    ("12°C à midi", {"seen": (12.0,)}),
    ("-2", {"seen": (-2.0,)}),
    ("moins 2° ce matin", {"seen": (-2.0,)}),
    ("il fait moins 3", {"seen": (-3.0,)}),
    ("il a fait -3 cette nuit", {"seen": (-3.0,)}),
    ("gel -3", {"frost": True, "seen": (-3.0,)}),
    ("gel,-3", {"frost": True, "seen": (-3.0,)}),
    ("5°,12°", {"seen": (5.0, 12.0)}),
    ("3° le matin, 14° l'après-midi", {"seen": (3.0, 14.0)}),
    ("1 degré ce matin", {"seen": (1.0,)}),
    ("gel blanc, 0°", {"frost": True, "seen": (0.0,)}),
    ("J'ai arrosé 2 fois, il faisait 24°", {"seen": (24.0,)}),
    ("Bois livré à 9h, le livreur a dit 3 stères, 4°", {"seen": (4.0,)}),
    ("averse de 10 min, 4°", {"seen": (4.0,)}),
    ("pluie 12°", {"raining": 5.0, "seen": (12.0,)}),
    ("soleil,12°", {"cloud": 0.1, "rain": 0.0, "seen": (12.0,)}),
    # the sky, the wind, the feel
    ("brouillard le matin puis éclaircies, pas de vent", {"cloud": 0.65, "fog": True, "wind": 0.5}),
    ("bright", {"cloud": 0.3}),
    ("sun and cloud", {"cloud": 0.4}),
    # a day they call clear is dry, unless rain, a shower, snow or wet is named anywhere in their words
    ("clear", {"cloud": 0.05, "rain": 0.0}),
    ("ciel clair", {"cloud": 0.05, "rain": 0.0}),
    ("ciel dégagé", {"cloud": 0.05, "rain": 0.0}),
    ("il fait beau", {"cloud": 0.15, "rain": 0.0}),
    ("not a cloud", {"cloud": 0.1, "rain": 0.0}),
    ("frost, -4 to 6, clear, light wind",
     {"cloud": 0.05, "frost": True, "rain": 0.0, "tmax": 6.0, "tmin": -4.0, "wind": 2.0}),
    ("soleil le soir", {"cloud": 0.1}),                            # only part of the day
    ("soleil, gris", {"cloud": 0.5}),                              # sun among clouds
    ("soleil, averse", {"cloud": 0.1, "raining": 3.0}),
    ("soleil, pluie 20 min", {"cloud": 0.1}),                      # rain named, though not read
    ("soleil, grêle à midi", {"cloud": 0.1}),
    ("neige au sol, soleil", {"cloud": 0.1}),
    ("vent léger", {"wind": 2.0}),
    ("strong wind", {"wind": 7.0}),
    ("beaucoup de vent", {"wind": 7.0}),
    ("vent 10 à 20 km/h", {"wind": 2.9}),
    ("vent 10-20 km/h", {"wind": 2.9}),
    ("wind 5-15 mph", {"wind": 3.1}),
    ("40 km/h", {"wind": 5.6}),
    ("vent 3 à 4 bft", {"wind": 3.5}),
    ("vent force 3-4", {"wind": 3.5}),
    ("Beaufort 3-4", {"wind": 3.5}),
    ("il fait froid", {"feel": -4.5}),
    ("froid, glacial même", {"feel": -4.5}),
    ("pluie froide 3 mm, -2 à 1, pas de neige",
     {"feel": -4.5, "rain": 3.0, "raining": 5.0, "snow": False, "tmax": 1.0, "tmin": -2.0}),
    # the garden's own ways of writing a day
    ("overcast, 9–15°, frost, snow 3 mm, strong wind, light 7.4 h, moon waxing gibbous",
     {"cloud": 0.95, "frost": True, "rain": 3.0, "snow": True, "tmax": 15.0, "tmin": 9.0, "wind": 7.0}),
    ("rain 2 mm · -2 to 7° · frost · light 7.8 h · wind 3 · moon waxing gibbous · autumn",
     {"frost": True, "rain": 2.0, "raining": 5.0, "tmax": 7.0, "tmin": -2.0}),
    # nonsense
    ("asdf qwerty 99999 mm °°° ---/// NaN to inf 1e999 ☂☂☂", {}),
    ("", {}),
)

# Lines that must leave every number of every day alone: each is doubtful somewhere.
SILENT = [sentence for sentence, wanted in HEARD if wanted == {}] + [
    "vent 10", "vent 40", "12/10", "rain 9999 mm", "-99°", "9999 km/h", "force 40", "min 400", "1e999°",
]

# Lines with no frost in them, and no temperature below zero: none may make a frost the day did not have.
NO_FROST_SAID = ("froid", "glacial", "il fait froid et gris", "max 1", "max 3°", "max 0.5", "neige", "neige 4 cm",
                 "froid, neige", "0°", "1°", "2° ce matin", "min 0", "brouillard, pas de soleil", "tempête, froid",
                 "pluie froide, max 1", "0 à 4", "brouillard, 0 à 4", "neige, 0 à 2", "Noël : soleil, 0 à 5",
                 "ciel clair, froid")


def changed_fields(with_gate, without) -> str:
    names = [name for name in ("tmin", "tmax", "rain", "cloud", "wind")
             if getattr(with_gate, name) != getattr(without, name)]
    return ", ".join(f"{name} {getattr(without, name)} → {getattr(with_gate, name)}" for name in names) or "nothing"


def try_lines(root: str, twin: str) -> None:
    """Each hand-written line: what was understood, what it changed, and whether that is right."""
    for line, holds in GATE_LINES:
        shown = "".join(ch if ch.isprintable() else "?" for ch in line)
        if holds is None:
            check(not sky._gate_days(line), f"{shown!r}: not a dated line, left alone")
            continue
        try:
            day = min(sky._gate_days(line), default=None) or sky._date_in(line)
            found, plain = sky.sky_for(root, day), sky.sky_for(twin, day)
            verdict = bool(holds(found, plain))
        except Exception as trouble:
            check(False, f"{shown!r} raised {type(trouble).__name__}: {trouble}")
            continue
        check(verdict, repr(shown))
        print(f"           understood: {sky.understand(found.remark) or 'nothing'}")
        print(f"           changed:    {changed_fields(found, plain)}")
        print(f"           the day:    {found.words}  [{found.source}]")
    span = [sky.sky_for(root, Date(2026, 10, 20) + n * DAY).remark for n in range(4)]
    check(span == ["dry and clear"] * 3 + [""], "a run of days (\"… to …\") covers each of its days and no more")
    undated = [line for line, holds in GATE_LINES if holds is None and not line.startswith("#")]
    check(sky.unread(root) == undated and sky.unread(twin) == [] and sky.unread(root + "-nowhere") == [],
          f"unread() gives the {len(undated)} lines no date could be read from, so the gate can say so "
          f"(a remark is not one of them)")


def try_heard() -> None:
    """Single sentences, and exactly what the reader makes of each."""
    print()
    for sentence, wanted in HEARD:
        heard = sky.understand(sentence)
        wanted_instead = "" if heard == wanted else f"   (wanted {wanted or 'nothing'})"
        check(heard == wanted, f"{sentence!r} → {heard or 'nothing'}{wanted_instead}")
    odd = [sky.understand(thing) for thing in (None, 42, 3.5, b"pluie 6mm", ["gel"])]
    check(all(isinstance(one, dict) for one in odd), "understand() takes anything at all and raises nothing")
    told = sky.explain("Bois livré à 9h, 9 à 15, 2 à 3 averses, demain pluie; gel")
    check([words for words, _ in told] == ["Bois livré à 9h", "9 à 15", "2 à 3 averses", "demain pluie", "gel"]
          and '"Bois", "livré" and "h"' in told[0][1] and told[1][1] == "a low of 9°; a high of 15°"
          and "write the °" in told[2][1] and '"demain" speaks of another day' in told[3][1] and told[4][1] == "frost",
          "explain() says thought by thought, in their own spelling, what was heard and why the rest was left alone")
    told = sky.explain("Noël : soleil; fleurs : gris")
    check(told[0][1].startswith("a title") and told[1][1].startswith("the sky clear")
          and '"fleurs"' in told[2][1] and 'it follows "fleurs:"' in told[3][1] and "full stop" in told[3][1],
          "explain() names a title that leaves nothing alone, and says how a heading that does could be written")


def try_clear_days(base: str, where: dict) -> None:
    """On days this garden's own sky makes wet: a day they call clear is dry; the sun of an evening takes nothing away."""
    twin = trial_ground(base, "clear-twin", where)
    root = trial_ground(base, "clear", where)
    gate = os.path.join(root, "gate", "sky.txt")
    wet = [day for day in (where["laid"] + n * DAY for n in range(400)) if sky.sky_for(twin, day).rain > 0][:40]
    for line, holds, words in (
            ("ciel clair", lambda s, r: s.rain == 0 and not s.snow and s.words.startswith("clear"),
             "a day they call clear is dry, and nothing falls as snow"),
            ("frost, -4 to 6, clear", lambda s, r: s.rain == 0 and not s.snow and s.frost,
             "'frost, -4 to 6, clear' is a dry frost"),
            ("soleil le soir", lambda s, r: s.rain == r.rain and not s.words.startswith("clear"),
             "'soleil le soir' keeps the day's rain, and a day with rain in it is never called clear"),
            ("soleil, pluie 20 min", lambda s, r: s.rain == r.rain,
             "'soleil, pluie 20 min' keeps the day's rain: rain is named, though its number is not read")):
        write(gate, "".join(f"{day}: {line}\n" for day in wet))
        wrong = [f"{day}: {sky.sky_for(root, day).words}" for day in wet
                 if not holds(sky.sky_for(root, day), sky.sky_for(twin, day))]
        check(wet and not wrong, f"{words}, on {len(wet)} days that were wet without their line"
              + (f" ({len(wrong)} are not: {wrong[0]})" if wrong else ""))


def try_silence(base: str, where: dict) -> None:
    """Ruling 11, over many days: a doubtful line changes no number; a line with no frost in it makes no frost."""
    days = [Date(2026, 10, 1) + 15 * n * DAY for n in range(26)]          # a year, twice a month
    twin = trial_ground(base, "silence-twin", where)
    root = trial_ground(base, "silence", where)
    gate = os.path.join(root, "gate", "sky.txt")
    moved = []
    for sentence in SILENT:
        write(gate, "".join(f"{day}: {sentence}\n" for day in days))
        moved += [f"{sentence!r} on {day}: {changed_fields(sky.sky_for(root, day), sky.sky_for(twin, day))}"
                  for day in days if not same(sky.sky_for(root, day), sky.sky_for(twin, day))]
    check(not moved and all(sky.understand(sentence) == {} for sentence in SILENT),
          f"{len(SILENT)} doubtful lines, each written on {len(days)} days of a year, change not one number"
          + (f" ({len(moved)} do: {moved[0]})" if moved else ""))
    winter = [Date(2026, 12, 1) + n * DAY for n in range(90)]
    invented = []
    for sentence in NO_FROST_SAID:
        write(gate, "".join(f"{day}: {sentence}\n" for day in winter))
        invented += [f"{sentence!r} on {day}" for day in winter
                     if sky.sky_for(root, day).frost and not sky.sky_for(twin, day).frost]
    check(not invented, f"{len(NO_FROST_SAID)} lines with no frost in them, over the {len(winter)} days of a winter, "
                        f"make no frost the day did not have" + (f" ({invented[0]} does)" if invented else ""))


def try_two_lines(base: str, where: dict) -> None:
    """A day written twice, in any order, a very long line, a day of many lines, and gate files saved oddly."""
    day = Date(2026, 11, 20)
    rambling = "pluie 20mm, " + "et le merle chantait encore, " * 40
    root = trial_ground(base, "two-lines", where, gate=f"{day}: {rambling}\n{day}: neige le soir\n")
    found = sky.sky_for(root, day)
    check(len(found.remark) <= 500 and found.remark.endswith("…; neige le soir") and found.snow and found.rain == 20,
          f"a long first line does not push the second out of the day's remark: …{found.remark[-30:]!r}")
    twin = trial_ground(base, "two-lines-twin", where)
    plain = sky.sky_for(twin, day)
    written_twice = (
        # a later line's softer words do not undo what an earlier one measured ...
        (("pluie 20mm", "bruine le soir"), lambda s: s.rain == 20),
        (("-1 / 12", "froid, neige le soir"), lambda s: (s.tmin, s.tmax) == (-1, 12) and s.snow),
        (("pluie 6mm", "sec", "pluie"), lambda s: s.rain == 6),              # a measure outweighs words
        (("pluie 6mm", "pluie 8mm"), lambda s: s.rain == 8),                 # two measures: the largest stands
        (("pluie 6mm le matin", "sec l'après-midi"), lambda s: s.rain == 6),
        (("9 à 15°", "10 à 16°"), lambda s: (s.tmin, s.tmax) == (9, 16)),     # the day holds all they wrote
        # ... and where two lines disagree of the whole day, that thing is left as it was
        (("sec", "pluie"), lambda s: s.rain == plain.rain),
        (("gel", "pas de gel"), lambda s: s.tmin == plain.tmin),
        (("neige", "en fait non, pas de neige, de la pluie 4mm"),
         lambda s: s.rain == 4 and not s.snow and s.tmax == plain.tmax),
    )
    gate = os.path.join(root, "gate", "sky.txt")
    for lines, holds in written_twice:
        write(gate, "".join(f"{day}: {line}\n" for line in lines))
        found = sky.sky_for(root, day)
        check(holds(found), " then ".join(repr(line) for line in lines) + f", all for one day: {found.words}")
    as_on_one_line = (("gel le matin", "doux l'après-midi"), ("gel le matin", "chaud l'après-midi"),
                      ("neige", "doux ensuite"), ("3°", "12°"), ("12°", "3°"), ("pluie 6mm", "soleil le soir"),
                      ("pluie 6mm le matin", "sec l'après-midi"), ("pluie 6mm", "pas de pluie cet après-midi"),
                      ("averse", "sec ensuite"), ("gelée blanche", "il ne gèle plus"),
                      ("neige le matin", "il ne neige plus"), ("soleil le matin", "gris l'après-midi"))
    for lines in as_on_one_line:
        write(gate, "".join(f"{day}: {line}\n" for line in lines))
        apart = sky.sky_for(root, day)
        write(gate, f"{day}: {', '.join(lines)}\n")
        together = sky.sky_for(root, day)
        write(gate, f"{day}: {'; '.join(lines)}\n")
        semicolon = sky.sky_for(root, day)
        write(gate, "".join(f"{day}: {line}\n" for line in reversed(lines)))
        backwards = sky.sky_for(root, day)
        check(same_weather([apart], [together]) and same_weather([apart], [semicolon])
              and same_weather([apart], [backwards]) and apart.words == semicolon.words == backwards.words,
              " then ".join(repr(line) for line in lines) + f" mean what they mean on one line, in any order: {apart.words}")
    lines = ["neige 3 cm, 2 à 5°"] + [f"le merle, encore {n}" for n in range(20)]
    write(gate, "".join(f"{day}: {line}\n" for line in lines))
    many = sky.sky_for(root, day)
    check(not many.snow and "neige" not in many.remark and same(many, plain) and many.source == "reckoned",
          "a day keeps its latest 20 lines; a line that fell out of its remark was not laid either, "
          "so what the almanac shows of their words is what the day was laid from")
    write(gate, "2026-11-20: pluie 7mm, éclaircies\n")
    with open(gate, "ab") as file:                                 # PowerShell's >> adds UTF-16 with no mark
        file.write("2026-11-21: pluie 30mm, vent fort\r\n".encode("utf-16-le"))
    check(sky.sky_for(root, day).rain == 7 and sky.sky_for(root, day + DAY).rain == 30
          and sky.sky_for(root, day + DAY).wind == 7,
          "a line added by PowerShell's >> (UTF-16 with no mark, after UTF-8) is read all the same")
    lines = "2026-11-20: pluie 7mm, éclaircies\n21 novembre 2026 : gelée blanche\n"
    with open(gate, "wb") as file:
        file.write(lines.encode("utf-16"))
    found = sky.sky_for(root, day)
    check(found.rain == 7 and "éclaircies" in found.remark and sky.sky_for(root, day + DAY).frost,
          f"a gate file saved by Notepad as \"Unicode\" (UTF-16) is read all the same: {found.remark!r}")


def try_noise(root: str) -> None:
    """Six hundred dated lines of noise, every byte there is, and one very long number."""
    wild = random.Random(11)
    alphabet = "0123456789 -–/.,:;°%àéèùç\t\x00�mmcmkmhrainpluiegelneigeventsoleilnoplusàto☂"
    noise = "\n".join(f"2026-11-{1 + n % 30:02d}" + "".join(wild.choice(alphabet) for _ in range(wild.randrange(200)))
                      for n in range(600))
    with open(os.path.join(root, "gate", "sky.txt"), "wb") as file:
        file.write(noise.encode("utf-8") + b"\n2026-12-01: \xe9claircies, 9 \xe0 15\xb0\n"
                   + bytes(range(256)) + b"\n2026-12-02: " + b"9" * 50000)
    sky.troubles.clear()
    try:
        started = time.perf_counter()
        skies = [sky.sky_for(root, Date(2026, 11, 1) + n * DAY) for n in range(40)]
        took = time.perf_counter() - started
    except Exception as trouble:
        check(False, f"noise at the gate raised {type(trouble).__name__}: {trouble}")
        return
    sane = all(-40 <= s.tmin <= s.tmax <= 50 and 0 <= s.rain <= 300 and 0 <= s.cloud <= 1 and 0 <= s.wind <= 10
               and "\n" not in s.remark and len(s.remark) <= 500 and s.words for s in skies)
    check(sane and not sky.troubles and took < 5,
          f"600 lines of noise, every byte there is and a 50,000-digit number: "
          f"nothing raised, every sky still a sky ({took:.2f} s)")
    old = skies[30]
    check((old.tmin, old.tmax) == (9, 15) and "éclaircies" in old.remark,
          f"a line saved in the old Windows encoding, among all that, keeps its accents: {old.remark!r}")


def almanac_words(s) -> str:
    """A day's sky as the almanac writes it (GROUND.md, "The days"): rain · degrees · light · wind · moon · season."""
    parts = [("snow " if s.snow else "rain ") + sky._millimetres(s.rain) + " mm" if s.rain > 0 else "dry",
             sky._degrees(s.tmin, s.tmax)]
    if s.frost:
        parts.append("frost")
    moon = f"{s.moon_name} moon" if s.moon_name in ("new", "full") else f"moon {s.moon_name}"
    return " · ".join(parts + [f"light {s.light:.1f} h", f"wind {round(s.wind)}", moon, s.season])


def less_light(words: str) -> str:
    """A day's words less its hours of light: they follow the cloud, which the words give only roughly."""
    return re.sub(r"light \d+\.\d h(?:, | · )", "", words)


def try_round_trip(base: str, where: dict) -> None:
    """The garden's own way of writing a day, copied back into gate/sky.txt, gives that day again."""
    twin = trial_ground(base, "round-trip-twin", where)
    skies = [sky.sky_for(twin, where["laid"] + n * DAY) for n in range(1500)]
    ways = (("what `sky.words` says of it", lambda s: s.words), ("its line in the almanac", almanac_words))
    for name, written in ways:
        root = trial_ground(base, "round-trip", where, gate="".join(f"{s.date}: {written(s)}\n" for s in skies))
        back = [sky.sky_for(root, s.date) for s in skies]
        changed = [f"{written(s)!r} came back as {written(b)!r}" for s, b in zip(skies, back)
                   if less_light(written(s)) != less_light(written(b))]
        check(not changed and all(b.source == "gate" for b in back),
              f"each of {len(skies)} days, written back at the gate as {name}, is read as the same day"
              + (f" ({len(changed)} are not: {changed[0]})" if changed else ""))


def try_gate(base: str, where: dict) -> None:
    heading("The gate reader: gate/sky.txt, written loosely, heard for sure or not at all")
    text = "# the sky, as the keeper saw it\n" + "\n".join(line for line, _ in GATE_LINES) + "\n"
    root = trial_ground(base, "gate", where, gate=text)
    try_lines(root, trial_ground(base, "gate-twin", where))
    try_heard()
    try_clear_days(base, where)
    try_silence(base, where)
    try_two_lines(base, where)
    try_round_trip(base, where)
    try_noise(root)


# ──────────────────────────────────────────────────────────────── the real sky

CANNED = json.dumps({
    "latitude": 47.0, "longitude": 10.7, "generationtime_ms": 0.21, "utc_offset_seconds": 7200,
    "timezone": "Europe/Vienna", "timezone_abbreviation": "CEST", "elevation": 880.0,
    "daily_units": {"time": "iso8601", "temperature_2m_max": "°C", "temperature_2m_min": "°C",
                    "precipitation_sum": "mm", "wind_speed_10m_max": "km/h", "sunshine_duration": "s"},
    "daily": {
        "time": ["2026-09-20", "2026-09-21", "2026-09-22", "2026-09-23", "2026-09-24",
                 "2026-09-25", "2026-09-26", "2026-09-27", "2026-09-28", "2026-09-29"],
        "temperature_2m_max": [21.4, 22.0, 19.3, 17.8, 19.3, 16.1, 15.2, None, 18.9, 20.5],
        "temperature_2m_min": [10.2, 11.7, 12.4, 9.9, 9.8, 8.4, 7.7, None, 6.1, 9.0],
        "precipitation_sum": [0.0, 0.0, 3.2, 11.6, 6.4, 0.3, 0.0, None, None, 0.0],
        "wind_speed_10m_max": [9.7, 12.2, 24.5, 38.9, 22.0, 15.1, 8.3, None, 6.5, 11.0],
        "sunshine_duration": [36000.0, 33100.5, 12000.0, 1800.0, 9000.0, 21000.0, 30500.0, None, 38000.0, 29000.0],
    },
})
RUBBISH = ("", "<html>503 Service Unavailable</html>", "{}", '{"daily": {"time": ["soon", 7, null]}}',
           b"\xff\xfe\x00", '{"daily": {"time": ["2026-09-24"], "temperature_2m_max": ["warm"]}}', None, 42, [1, 2])
MONTH = [Date(2026, 9, 10) + n * DAY for n in range(30)]           # the canned days lie in the middle of it
REAL_ON = {"real-sky": "yes", "longitude": "10.7"}


class FakeNet:
    """Stands where urllib.request.urlopen stands: counts the calls, and answers as told, or raises.

    `answer` is text, or bytes, or a function of the url asked, or None (the
    wire is cut: it raises), or something to raise in its place. `wait` is how
    many seconds it takes to say anything.
    """

    def __init__(self, answer=None, wait=0.0):
        self.answer, self.wait, self.urls, self.body = answer, wait, [], b""

    def __call__(self, url, *args, **kwargs):
        self.urls.append(str(url))
        time.sleep(self.wait)
        if isinstance(self.answer, BaseException):
            raise self.answer
        if self.answer is None:
            raise OSError("the trial has cut the wire")
        answer = self.answer(str(url)) if callable(self.answer) else self.answer
        self.body = answer if isinstance(answer, bytes) else answer.encode("utf-8")
        return self

    def read(self, size=-1):
        return self.body if size is None or size < 0 else self.body[:size]

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


def with_net(answer=None, wait=0.0) -> FakeNet:
    """Put a fake net in urlopen's place and load sky.py afresh, as a new process would have it."""
    import urllib.request
    net = urllib.request.urlopen = FakeNet(answer, wait)
    importlib.reload(sky)
    return net


def same_weather(these: list, those: list) -> bool:
    """The same days' weather from the same source? (The ground's wetness apart: that leans on the days before.)"""
    def weather(one):
        return one.date, one.tmin, one.tmax, one.rain, one.cloud, one.wind, one.source
    return [weather(one) for one in these] == [weather(one) for one in those]


def canned_with(**lists) -> str:
    """The canned answer with some of its lists replaced."""
    answer = json.loads(CANNED)
    answer["daily"].update(lists)
    return json.dumps(answer)                                       # which writes NaN and Infinity as just that


def every_day_asked(url: str) -> str:
    """An answer for whatever days the url asks for, each 10–20° and dry: and three days nobody asked for."""
    first, last = (Date.fromisoformat(re.search(name + r"=(\d{4}-\d\d-\d\d)", url).group(1))
                   for name in ("start_date", "end_date"))
    days = [first + n * DAY for n in range((last - first).days + 1)]
    days += [Date(1999, 1, 1), Date.today() + DAY, Date(2090, 12, 25)]
    return json.dumps({"daily": {"time": [day.isoformat() for day in days],
                                 "temperature_2m_max": [20.0] * len(days), "temperature_2m_min": [10.0] * len(days),
                                 "precipitation_sum": [0.0] * len(days)}})


def try_reading() -> None:
    parsed = sky.read_open_meteo(CANNED, 47.0)
    day = parsed.get(Date(2026, 9, 24), {})
    check(len(parsed) == 9 and Date(2026, 9, 27) not in parsed,
          f"the canned answer is read: {len(parsed)} days of 10 (the day with no temperatures is left out)")
    check(day.get("tmin") == 9.8 and day.get("tmax") == 19.3 and day.get("rain") == 6.4
          and abs(day.get("wind", 0) - 3.0) <= 0.2 and abs(day.get("cloud", 0) - 0.77) <= 0.03,
          f"24 September as open-meteo gave it: {day}")
    check(parsed.get(Date(2026, 9, 28), {}).get("rain") == 0.0, "a day with no rain figure is read as dry")
    check(all(sky.read_open_meteo(answer) == {} for answer in RUBBISH),
          f"{len(RUBBISH)} kinds of rubbish are read as nothing, and nothing is raised")
    check(sky.read_open_meteo(canned_with(temperature_2m_min=[True] * 10)) == {},
          "a `true` where a temperature should be is not taken for 1.0°")


def try_switched_off(base: str, where: dict) -> None:
    """Unless the place says yes and gives a longitude, urlopen (made to raise) is never even called."""
    for name, changes in (("off", {"real-sky": "no", "longitude": "10.7"}),
                          ("no-longitude", {"real-sky": "yes", "longitude": ""}),
                          ("perhaps", {"real-sky": "perhaps", "longitude": "10.7"})):
        net = with_net()
        root = trial_ground(base, "real-" + name, where, **changes)
        skies = [sky.sky_for(root, day) for day in MONTH]
        check(not net.urls and all(one.source == "reckoned" for one in skies)
              and not os.path.exists(os.path.join(root, "ground", "sky-cache")),
              f"real-sky: {changes['real-sky']}, longitude: {changes['longitude'] or 'none'} → "
              f"urlopen was made to raise, and was never called")
    net = with_net()
    not_yes = ("on verra", "on hold", "o.k. plus tard", "y a pas", "1 de ces jours", "true? not sure",
               "yes, but not yet")
    turned_on = []
    for value in not_yes:
        root = trial_ground(base, "real-talk", where, **{"real-sky": value, "longitude": "10.7"})
        sky.sky_for(root, MONTH[0])
        turned_on.append(sky.place(root)["real-sky"])
    check(not net.urls and not any(turned_on),
          f"only a plain yes turns it on: {len(not_yes)} lines that merely begin like one "
          f"('on verra', 'y a pas', 'true? not sure') → never called")
    yes = ("yes", "Oui.", "on", "YES  # since October", "oui (le village)")
    check(all(sky.place(trial_ground(base, "real-talk", where, **{"real-sky": value}))["real-sky"] for value in yes),
          "and a plain yes does, with a remark after it or without: " + ", ".join(repr(value) for value in yes))


def try_switched_on(base: str, where: dict, reckoned: list) -> None:
    """The real sky on, and open-meteo answering with the canned days."""
    net = with_net(CANNED)
    root = trial_ground(base, "real-on", where, **REAL_ON)
    skies = [sky.sky_for(root, day) for day in MONTH]
    real = skies[14]                                               # 24 September
    check(real.source == "open-meteo" and (real.tmin, real.tmax, real.rain) == (9.8, 19.3, 6.4),
          f"real-sky: yes → 24 September comes from open-meteo: {real.words}")
    check(skies[15].wet > reckoned[15].wet or skies[15].wet >= 0.97,
          f"and the ground of the 25th is wet from the real rain ({skies[15].wet}, against {reckoned[15].wet} reckoned)")
    check(skies[17].source == "reckoned" and alike(skies[2:3], reckoned[2:3]),
          "a day open-meteo had nothing for, or never gave, is reckoned as usual")
    url = net.urls[0] if net.urls else ""
    check(len(net.urls) == 1 and "latitude=47.0000" in url and "longitude=10.7000" in url
          and "open-meteo.com" in url and "start_date=2026-" in url and "precipitation_sum" in url,
          f"it asked once for the whole month: {url[:100]}…")
    kept = read(os.path.join(root, "ground", "sky-cache"))
    check("2026-09-24  tmin 9.8  tmax 19.3  rain 6.4" in kept,
          "the answer is kept in ground/sky-cache, one plain line a day")

    net = with_net()                                               # the wire cut, in a "new process"
    again = [sky.sky_for(root, day) for day in MONTH]
    check(alike(again, skies) and len(net.urls) <= 1,
          f"with the wire cut, a new process gives the same month from the cache "
          f"(it tried the network {len(net.urls)} time)")

    with_net(CANNED)
    root = trial_ground(base, "real-and-gate", where, gate="2026-09-24: pluie 20mm\n", **REAL_ON)
    both = sky.sky_for(root, Date(2026, 9, 24))
    check(both.source == "gate" and both.rain == 20 and (both.tmin, both.tmax) == (9.8, 19.3),
          f"the keeper's line still comes first, laid over the real day: {both.words}")


def try_failing(base: str, where: dict, reckoned: list) -> None:
    """The real sky on, and the network dead, or talking rubbish."""
    net = with_net()
    started = time.perf_counter()
    skies = [sky.sky_for(trial_ground(base, "real-dark", where, **REAL_ON), day) for day in MONTH]
    check(alike(skies, reckoned) and len(net.urls) == 1 and not sky.troubles,
          f"real-sky: yes but no network → it asks once, then reckons the whole month in silence "
          f"({time.perf_counter() - started:.2f} s)")
    for broken_off in (KeyboardInterrupt(), SystemExit(1)):
        net = with_net(broken_off)
        what = type(broken_off).__name__
        try:
            skies = [sky.sky_for(trial_ground(base, "real-broken-off", where, **REAL_ON), day) for day in MONTH]
            check(alike(skies, reckoned) and len(net.urls) == 1 and not sky.troubles,
                  f"a {what} from inside the asking is only a question that failed → reckoned, in silence")
        except BaseException as trouble:                           # (caught so wide only to say so, and go on)
            check(False, f"a {what} from inside the asking came out of sky_for as {type(trouble).__name__}")
    rubbish = ("<html>503</html>", b"\xff\xfe", '{"daily": {"time": []}}', '{"daily": {"time": 7}}')
    for number, answer in enumerate(rubbish):
        with_net(answer)
        root = trial_ground(base, f"real-rubbish-{number}", where, **REAL_ON)
        skies = [sky.sky_for(root, day) for day in MONTH]
        check(alike(skies, reckoned) and not sky.troubles, f"open-meteo answers {answer!r:.28} → reckoned, in silence")


def try_unbelievable(base: str, where: dict, reckoned: list) -> None:
    """Numbers no sky could have, from the wire or written into the cache by a hand, are not believed."""
    nan, endless = float("nan"), float("inf")
    answers = {"a high of a thousand million degrees": canned_with(temperature_2m_max=[1e9] * 10),
               "a high of 9999°": canned_with(temperature_2m_max=[9999] * 10),
               "NaN for every high": canned_with(temperature_2m_max=[nan] * 10),
               "Infinity for every low": canned_with(temperature_2m_min=[-endless] * 10),
               "1e999 millimetres of rain": canned_with(precipitation_sum=[7777.5] * 10).replace("7777.5", "1e999")}
    for number, (what, answer) in enumerate(answers.items()):
        net = with_net(answer)
        root = trial_ground(base, f"real-unbelievable-{number}", where, **REAL_ON)
        try:
            skies = [sky.sky_for(root, day) for day in MONTH]
            said = all(one.words for one in skies)
        except Exception as trouble:
            check(False, f"open-meteo answers {what} → raised {type(trouble).__name__}: {trouble}")
            continue
        check(said and alike(skies, reckoned) and len(net.urls) == 1 and not sky.troubles
              and not os.path.exists(os.path.join(root, "ground", "sky-cache")),
              f"open-meteo answers {what} → not believed, not kept, every day reckoned")

    with_net(canned_with(temperature_2m_max=[21.4, 22.0, 19.3, 17.8, 9999, 16.1, 15.2, None, 18.9, 20.5]))
    root = trial_ground(base, "real-one-bad-day", where, **REAL_ON)
    skies = [sky.sky_for(root, day) for day in MONTH]
    check(same_weather(skies[14:15], reckoned[14:15]) and skies[13].source == skies[15].source == "open-meteo",
          "one unbelievable day in a good answer is reckoned, and its neighbours are still real")

    with_net()                                                     # the wire cut: only the cache speaks
    root = trial_ground(base, "real-cache-by-hand", where, **REAL_ON)
    write(os.path.join(root, "ground", "sky-cache"),
          "for: 47.0000,10.7000\n2026-09-20  tmin nan  tmax nan\n2026-09-21  tmin -inf  tmax inf  rain inf\n"
          "2026-09-22  tmin -5000  tmax 9000  rain 123456\n2026-09-23  tmin 12  tmax 3\n"
          "2026-09-24  tmin 9.8  tmax 19.3  rain 6.4\n2026-09-25  tmin 1e999  tmax 1e999\n")
    try:
        skies = [sky.sky_for(root, day) for day in MONTH]
        passed_over = same_weather(skies[10:14] + skies[15:16], reckoned[10:14] + reckoned[15:16])
        check(all(one.words for one in skies) and passed_over and skies[14].source == "open-meteo" and not sky.troubles,
              "lines no sky could have, written into ground/sky-cache by a hand, are passed over; the good line is kept")
    except Exception as trouble:
        check(False, f"a cache written by hand raised {type(trouble).__name__}: {trouble}")


def try_asking(base: str, where: dict) -> None:
    """What is taken from an answer, and how long the gate will wait for one."""
    today = Date.today()
    absence = [today - n * DAY for n in range(300, -1, -1)]          # a visitor back after three hundred days

    net = with_net(every_day_asked)
    root = trial_ground(base, "real-absence", where, **REAL_ON)
    skies = [sky.sky_for(root, day) for day in absence]
    kept = read(os.path.join(root, "ground", "sky-cache"))
    stray = [day for day in ("1999-01-01", (today + DAY).isoformat(), "2090-12-25") if day in kept]
    real = sum(one.source == "open-meteo" for one in skies)
    check(real >= 290 and len(net.urls) <= 12 and not stray,
          f"a long absence: {real} of {len(absence)} days real for {len(net.urls)} questions; "
          f"the days nobody asked for (1999, tomorrow, 2090) are not taken or kept")

    elsewhen = canned_with(time=["1999-01-0%d" % n for n in range(1, 10)] + ["2090-12-25"])
    for what, answer in (("nothing", ""), ("an error page", "<html>503</html>"), ("an empty answer", "{}"),
                         ("only days nobody asked for", elsewhen)):
        net = with_net(answer)
        root = trial_ground(base, "real-useless", where, **REAL_ON)
        skies = [sky.sky_for(root, day) for day in absence]
        check(len(net.urls) == 1 and all(one.source == "reckoned" for one in skies)
              and not os.path.exists(os.path.join(root, "ground", "sky-cache")),
              f"open-meteo answers {what} → asked once in the whole absence, not once for every month of it")

    net = with_net(every_day_asked, wait=3.0)                      # a server that takes its time over every word
    sky.ASK_SECONDS = 0.3
    root = trial_ground(base, "real-slow", where, **REAL_ON)
    started = time.perf_counter()
    skies = [sky.sky_for(root, day) for day in absence]
    took = time.perf_counter() - started
    check(took < 2.5 and len(net.urls) == 1 and all(one.source == "reckoned" for one in skies),
          f"an answer that does not come within ASK_SECONDS (here {sky.ASK_SECONDS}) is not waited for: "
          f"301 days reckoned in {took:.2f} s, asked once")

    net = with_net(every_day_asked, wait=0.15)                     # it answers, but slowly, and there is much to ask
    sky.ASK_BUDGET = 0.4
    root = trial_ground(base, "real-budget", where, **REAL_ON)
    started = time.perf_counter()
    skies = [sky.sky_for(root, day) for day in absence]
    took = time.perf_counter() - started
    real = sum(one.source == "open-meteo" for one in skies)
    check(1 <= len(net.urls) <= 4 and 0 < real < 200 and took < 3.0,
          f"once the questions have taken ASK_BUDGET in all (here {sky.ASK_BUDGET} s) no more are asked: "
          f"{len(net.urls)} questions, {real} days real, the rest reckoned, {took:.2f} s")


def try_real_sky(base: str, where: dict) -> None:
    heading("The real sky (open-meteo): never the network itself, only a canned answer")
    import urllib.request
    true_urlopen = urllib.request.urlopen
    where = dict(where, latitude=47.0)                             # the canned answer is for 47° north
    try:
        try_reading()
        try_switched_off(base, where)
        if Date.today() < Date(2026, 9, 30):
            print("  note   this machine's clock is before the canned days, so the rest cannot be tried")
        else:
            twin = trial_ground(base, "real-twin", where)
            reckoned = [sky.sky_for(twin, day) for day in MONTH]
            try_switched_on(base, where, reckoned)
            try_failing(base, where, reckoned)
            try_unbelievable(base, where, reckoned)
            try_asking(base, where)
    finally:
        urllib.request.urlopen = true_urlopen
        importlib.reload(sky)
    print("  note   the live call to open-meteo.com is untried: no trial here touches the network")


# ───────────────────────────────────────────────────────────────────── the run

def main(arguments: list) -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    root = os.path.abspath(arguments[0]) if arguments else os.path.dirname(SHED)
    where = sky.place(root)
    gate_text = sky._text_of(sky._bytes_of(os.path.join(root, "gate", "sky.txt")))
    print(f"The sky, on trial · the garden at {root}")
    print(f"latitude {where['latitude']} · weather-seed {where['weather-seed']} · laid {where['laid'].isoformat()}"
          f" · real sky {'on' if where['real-sky'] else 'off'} · Python {sys.version.split()[0]}")

    base = tempfile.mkdtemp(prefix="glebe-sky-trial-")
    try:
        heading("The astronomy")
        try_moon()
        try_daylength()
        try_seasons()
        try_climate(base, where)
        try_purity(base, where, gate_text)
        try_gate(base, where)
        try_report(base, where)
        try_own_weather(base, where)
        try_real_sky(base, where)
    finally:
        shutil.rmtree(base, ignore_errors=True)

    print()
    if failed:
        print(f"VERDICT: {len(failed)} of {held + len(failed)} checks fail:")
        for words in failed:
            print(f"  - {words}")
        return 1
    print(f"VERDICT: all {held} checks hold. The sky stands.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
