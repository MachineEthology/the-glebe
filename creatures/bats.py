"""
Bats: a small colony that hunts over the garden on warm evenings, and takes moths.

They roost somewhere out of sight (a crevice high in a wall, the space under
a roof) and come out at dusk. A visitor arriving on a summer evening may see
them; otherwise what they did is in two files.

Their own file, ground/creatures/bats:

    bats: 14              in the colony now
    fed: 0.72             how well they have fed lately: 0 starving, 1 as well as can be
    fat: 0.804            the fat they have to sleep the winter on: 0 none, 1 as fat as a bat gets
    asleep: no            or the day they went to their winter sleep
    perch: orchard        the bed under the perch where they eat
    this year: 2027 · first out 04-03 · out on 96 evenings · most 18 · young 5 · moths 1870 · died 3
    the years:
    2027  first out 04-03 · out on 140 evenings · most 18 · young 5 · moths taken 1870 · died 4 · came 1

(`came` is how many joined them from other roosts that year; it is left out
when none did.)

Any number in it may be changed by hand, and the bats go on from what it
says; a line that cannot be read is taken as if it were not there. A line
of your own beginning with # is kept.

And the wings under their perch, beds/orchard/moth-wings (in whatever bed
`perch:` names), a thing they make: see THE PERCH below.


THE YEAR

They sleep through the winter. They go to sleep on the first cold evening
after the middle of October (under 7° at dusk), or by the middle of
November whatever the weather; they wake on the first warm evening after
the tenth of March (10° at dusk), or by the twentieth of April. They wake
lean, and in spring and summer they spend what fat is left. From August
until they sleep they put it on again: an evening that brings them more
than the gnats and midges alone puts some on, and the more moths there
are, the more; a poor evening, or one spent in, costs them a little.
Asleep, they live on it and it dwindles, and a few of them die: the leaner
the colony, the more (about one in ten of a colony that went to sleep
fat, two in five of one that went to sleep with nothing). On a mild
evening in the dead of winter (between the middle of November and early
March; 12° at dusk, still and dry) they may wake and hunt for an hour,
which costs them more fat than it brings. In the third week of June the
young are born, one to a mother, about half the colony being mothers: how
many of the mothers raise one follows how well the colony has fed that
spring. The young fly with the others from the middle of July. In the
middle of August, a small colony that has fed well draws a bat or two
from other roosts to it. There are never more than forty (the roost holds
no more) nor fewer than two.


THE JOB: TAKING MOTHS

On a warm evening from spring to autumn (10° or more at dusk, the wind
under 6, under 4 mm of rain) they hunt. They count the moths by the wall
the moths rest on by day (the thing the moths make; each moth there
stands for ten in the garden, see creatures/moths.py), and they hunt over
the bed with the most flowers scented at dusk or night, where the moths
gather; if none is open, over the wettest bed, for the midges. Each bat
takes about a moth an evening when moths are many (two hundred in the
garden is half way to many), and fewer when they are few: then they turn
to gnats and midges instead, and they never take more than a quarter of
the moths in one evening. A warmer, stiller evening is a better one.

How well they feed is what moths they find (six tenths of it, at the
most) and the gnats and midges of a good evening (half of it). That
decides how many young are born in June, and, through the fat of the late
summer (which only the moths can put on them), how many of the colony live
through the winter. So a run of years with many moths brings more bats,
and more bats thin the moths, and the balance is in the two files, a line
a year in each.


THE PERCH

They eat the bigger moths at a perch, and the wings fall beneath it. That
pile is a thing they make, beds/<perch>/moth-wings: a line for each night
they hunted, the newest last, with how many moths they took that night,
over which bed, and how many pairs of wings fell (about one for every
three moths; the rest are eaten on the wing). Wings lie a fortnight, less
if a night of heavy rain (10 mm) washes them away. The moths count their
losses by it.

Its drawing (look.py beds/<perch>/moth-wings) is the perch, a bar along the
top, and under it a column for each night they hunted, set by its date
(a gap is a night they stayed in), with a pair of wings for each pair that
fell, the newest on the right. Wings that fell in the last three days are
dark; older ones have faded.


WHAT THE ALMANAC HEARS

The first evening of the year they are out, the young flying with them,
their going to sleep, a waking in the dead of winter, and a year when the
colony is bigger than it has ever been. The rest is in their file.


AT THE GATE

At an arrival on a summer evening, in the hours after sunset, when the
evening is warm enough, they are hunting, and the note says over which bed.
"""

import datetime
import re

import hands

NAME = "bats"

MOST, FEWEST = 40, 2      # the colony's bounds: the roost holds no more; a few always come back
APPETITE = 1.0            # moths a bat takes in an evening when moths are many and the evening is good
HALF = 200                # moths in the garden at which a bat takes half its appetite of them
TAKE_MOST = 0.25          # of the moths in the garden, the most the bats take in one evening
MOTH_FOOD = 0.6           # how much of their feeding moths can give, at the most
OTHER_FOOD = 0.5          # how much of it the gnats and midges of a good evening give
WINTER_DEATH = (0.0006, 0.003)    # the chance a day of dying asleep: this much, and up to this much more if lean
FATTEN = (8, 1)           # (month, day): from here until they sleep, the evenings put fat on them
FAT_GAIN = 0.05           # an evening out puts on FAT_GAIN × (how well they fed that evening − FAT_KEEP):
FAT_KEEP = 0.5            # gnats and midges alone keep them as they are; only moths fatten them
BURN = (0.005, 0.002, 0.001)   # fat spent in a day: awake in spring and summer; asleep; an autumn evening in,
                               # or a poor one out (the file keeps three decimals, so these small sums count)
MOTHERS = 0.5             # of the colony, the share that are mothers
RAISED = 0.9              # of the mothers, the share that raise a young one when the colony is as well fed as can be
JOIN = (8, 15)            # (month, day): bats from other roosts may join them ...
JOIN_FED, JOIN_BELOW = 0.75, 12   # ... if they have fed at least this well, and the colony is smaller than this
WINGS_KEPT = 14           # days a night's wings lie under the perch
WASHED = 10.0             # mm of rain in a night that washes the older wings away
PERCH_THING = "moth-wings"
PERCH_ELSE = "wings-under-the-perch"
YEARS_KEPT = 60

SLEEP_FROM, SLEEP_BY = (10, 15), (11, 15)     # (month, day): the first cold evening after, or this day at the latest
WAKE_FROM, WAKE_BY = (3, 10), (4, 20)         # the first warm evening after, or this day at the latest
BORN, FLYING = (6, 20), (7, 18)               # the young are born; and fly

HEAD = (
    "# The bats of this garden; creatures/bats.py says how they live.",
    "# bats: in the colony now · fed: how well they have fed lately, 0 to 1 · asleep: no, or since",
    "# when · perch: the bed under the perch where they eat (they keep beds/<that bed>/moth-wings).",
    "# Any number may be changed by hand; the bats go on from what it says.",
)
_YEAR_LINE = re.compile(r"^\s*(\d{4})\s{2,}\S")
_NIGHT = re.compile(r"^\s*(\d{4}-\d{2}-\d{2})\s+took\s+(\d{1,6})\s+moths?(?:\s+over\s+the\s+(.+?))?"
                    r"(?:\s+·\s+(\d{1,6})\s+pairs?\s+of\s+wings?)?\s*$")


# ------------------------------------------------------------------ their file

class _State:
    """The bats' own file, read forgivingly, and written back whole."""

    def __init__(self, text, today):
        text = str(text or "")
        keys = hands.read_keys(text)
        self.bats = int(hands.num(keys, "bats", 12, FEWEST, MOST))
        self.fed = round(hands.num(keys, "fed", 0.6, 0.0, 1.0), 3)
        self.fat = round(hands.num(keys, "fat", 0.6, 0.0, 1.0), 3)
        asleep = hands.line(keys, "asleep", "")
        if "asleep" in keys:
            self.asleep = _date(asleep) or (None if asleep.lower().startswith(("no", "awake")) else today)
        else:                                            # no word of it: asleep in the sleeping months
            self.asleep = today if today.month in (12, 1, 2) else None
        self.perch = hands.line(keys, "perch", "")
        self.woke = _date(hands.line(keys, "woke"))
        this = hands.line(keys, "this year")
        found = re.match(r"\s*(\d{4})", this)
        self.year = int(found.group(1)) if found else today.year
        self.first = _field(this, r"first out (\d{1,2}-\d{1,2})", None, str)
        self.evenings = _field(this, r"out on (\d{1,4}) evening", 0)
        self.most = _field(this, r"most (\d{1,4})", self.bats)
        self.young = _field(this, r"young (\d{1,4})", 0)
        self.moths = _field(this, r"moths (\d{1,9})", 0)
        self.died = _field(this, r"died (\d{1,4})", 0)
        self.came = _field(this, r"came (\d{1,4})", 0)
        self.years = [line.strip() for line in text.splitlines() if _YEAR_LINE.match(line)][-YEARS_KEPT:]
        self.remarks = [line.rstrip()[:200] for line in text.splitlines()
                        if line.strip().startswith("#") and line.rstrip() not in HEAD][:12]

    def roll(self, today) -> None:
        """A new year: the old one goes into `the years`."""
        if today.year <= self.year:
            return
        self.years.append("%d  first out %s · out on %d evenings · most %d · young %d · moths taken %d · died %d%s"
                          % (self.year, self.first or "--", self.evenings, self.most, self.young, self.moths,
                             self.died, " · came %d" % self.came if self.came else ""))
        self.years = self.years[-YEARS_KEPT:]
        self.year, self.first, self.evenings, self.young, self.moths, self.died = today.year, None, 0, 0, 0, 0
        self.most, self.came = self.bats, 0

    def text(self) -> str:
        lines = list(HEAD) + self.remarks
        lines += ["bats: %d" % self.bats, "fed: %.2f" % self.fed, "fat: %.3f" % self.fat,
                  "asleep: %s" % (self.asleep.isoformat() if self.asleep else "no")]
        if self.perch:
            lines.append("perch: %s" % self.perch)
        if self.woke:
            lines.append("woke: %s" % self.woke.isoformat())
        lines.append("this year: %d · first out %s · out on %d evenings · most %d · young %d · moths %d · died %d%s" % (
            self.year, self.first or "--", self.evenings, self.most, self.young, self.moths, self.died,
            " · came %d" % self.came if self.came else ""))
        lines.append("the years:")
        lines += self.years
        return "\n".join(lines) + "\n"


def _date(text):
    found = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", str(text or ""))
    if not found:
        return None
    try:
        return datetime.date(*(int(part) for part in found.groups()))
    except ValueError:
        return None


def _field(text, pattern, default, kind=int):
    found = re.search(pattern, str(text or ""))
    if not found:
        return default
    try:
        return kind(found.group(1))
    except ValueError:
        return default


def _whole(n, rng) -> int:
    """A count with a fraction in it, made whole by the dice: 2.3 is 2 seven times in ten, 3 three times."""
    n = max(0.0, n)
    return int(n) + (1 if rng.random() < n - int(n) else 0)


def _on_or_after(today, month_day) -> bool:
    return (today.month, today.day) >= month_day


# ------------------------------------------------------------------ the evening

def dusk(sky) -> float:
    """The warmth at dusk, reckoned from the day's lowest and highest."""
    return sky.tmin + 0.45 * (sky.tmax - sky.tmin)


def evening(sky, waking=False) -> float:
    """How good an evening it is to hunt: 0 (they stay in) to 1. Warm, still and dry.
    `waking`: the stricter test of a winter evening that might wake them."""
    warm = dusk(sky)
    if waking:
        return 0.3 if warm >= 12 and sky.wind < 5 and sky.rain < 2 else 0.0
    if warm < 10 or sky.wind >= 6 or sky.rain >= 4:
        return 0.0
    return max(0.05, min(1.0, (warm - 8) / 6.0) * (1 - sky.wind / 12.0) * (1 - sky.rain / 8.0))


def _moths_seen(garden) -> int:
    """The moths in the garden, as the bats count them: each moth at rest on the moths' wall stands for ten."""
    seen = 0
    for thing in garden.things():
        if thing.maker == "moths":
            seen += sum(line.count("^") for line in str(thing.text or "").splitlines() if line.count("|") >= 2)
    return 10 * seen


def _hunting_ground(garden) -> str:
    """The bed they hunt over: the one with most flowers open that are scented at dusk or night; else the wettest."""
    scented = {}
    for plant in garden.plants():
        if not plant.dead and (plant.scent.split() or [""])[0] in ("dusk", "night", "evening"):
            count = plant.flowers
            if count > 0:
                scented[plant.bed] = scented.get(plant.bed, 0) + count
    if scented:
        return sorted(scented, key=lambda bed: (-scented[bed], bed))[0]
    beds = sorted(garden.beds(), key=lambda bed: (-bed.water, bed.name))
    return beds[0].name if beds else ""


# ------------------------------------------------------------------ the perch

def _perch_bed(garden, said) -> str:
    """The bed under their perch: the one their file names, if it is there; else the orchard (trees); else the
    roomiest bed but the keeper's own."""
    beds = garden.beds()
    names = {bed.name for bed in beds}
    if said in names:
        return said
    if "orchard" in names:
        return "orchard"
    pool = [bed for bed in beds if bed.name != "gate-border"] or beds
    return sorted(pool, key=lambda bed: (-bed.room, bed.name))[0].name if pool else ""


def _nights(text) -> list:
    """The nights the wings under the perch tell of: [(date, took, over, wings)], oldest first."""
    found = []
    for line in str(text or "").splitlines():
        match = _NIGHT.match(line)
        if match:
            when = _date(match.group(1))
            if when:
                took = int(match.group(2))
                wings = int(match.group(4)) if match.group(4) else (took + 2) // 3
                found.append((when, took, (match.group(3) or "").strip() or "garden", wings))
    return sorted(found, key=lambda night: night[0])


def _perch_text(bed, nights) -> str:
    head = [
        "Moth wings, under the bats' perch in the %s. The bats take moths on the wing over the garden," % bed,
        "and bring the bigger ones here to eat; the wings fall, and lie a fortnight or so before the wind",
        "and the rain clear them. One line for each night they hunted, the newest last: how many moths",
        "they took, over which bed, and how many pairs of wings fell here (about one for every three",
        "moths; the rest are eaten on the wing). The moths count their losses by it.",
        "",
    ]
    if not nights:
        return "\n".join(head + ["(no wings lie here now)"]) + "\n"
    return "\n".join(head + ["%s  took %d moth%s over the %s · %d pair%s of wings" % (
        when.isoformat(), took, "" if took == 1 else "s", over or "garden", wings, "" if wings == 1 else "s")
        for when, took, over, wings in nights]) + "\n"


def _keep_perch(garden, ctx, s, took=None, over="") -> None:
    """The wings under the perch as they lie today: tonight's added, the old blown or washed away."""
    bed = _perch_bed(garden, s.perch)
    if not bed:
        return
    s.perch = bed
    today, rng = ctx.date, ctx.rng
    mine = [thing for thing in garden.things() if thing.maker == NAME]
    here = [thing for thing in mine if thing.bed == bed]
    nights = _nights(here[0].text) if here else []
    washed = ctx.sky.rain >= WASHED
    nights = [night for night in nights if 0 <= (today - night[0]).days < (2 if washed else WINGS_KEPT)
              and night[0] != today]
    if took:
        nights.append((today, took, over, _whole(took / 3.0, rng)))
    text = _perch_text(bed, nights)
    names = [here[0].name] if here else [PERCH_THING, PERCH_ELSE]
    name = next((name for name in names if garden.make(bed, name, text)), "")
    if name:
        for thing in mine:
            if (thing.bed, thing.name) != (bed, name):
                garden.unmake(thing.bed, thing.name, "the bats eat at another perch now")


# ------------------------------------------------------------------ the creature

def day(garden, ctx):
    today, sky, rng = ctx.date, ctx.sky, ctx.rng
    s = _State(ctx.state, today)
    s.roll(today)
    said = []

    # asleep: to sleep in autumn, awake in spring, a waking on a mild winter evening
    sleepy = _on_or_after(today, SLEEP_FROM) or today.month <= 2      # (awake in January only if a hand woke them)
    deep_winter = _on_or_after(today, SLEEP_BY) or not _on_or_after(today, WAKE_FROM)
    if s.asleep is None and sleepy and (dusk(sky) < 7 or _on_or_after(today, SLEEP_BY)):
        s.asleep = today
        said.append("the bats have gone to their winter sleep")
    elif s.asleep is not None and today.month < 10 and _on_or_after(today, WAKE_FROM) and (
            evening(sky) or _on_or_after(today, WAKE_BY)):
        s.asleep = None
    out = 0.0
    if s.asleep is None:
        out = evening(sky)
    elif deep_winter and evening(sky, waking=True):
        out = evening(sky, waking=True)
        if s.woke is None or s.woke < s.asleep:
            said.append("the bats woke on a mild winter evening, and hunted over the %s" % _hunting_ground(garden))
        s.woke = today

    took, over = 0, ""
    if out:
        over = _hunting_ground(garden)
        moths = _moths_seen(garden)
        share = moths * moths / float(moths * moths + HALF * HALF) if moths else 0.0
        took = min(int(moths * TAKE_MOST), _whole(s.bats * APPETITE * share * out, rng))
        tonight = min(1.0, MOTH_FOOD * share + OTHER_FOOD * out)
        if s.asleep is None:
            s.fed = 0.9 * s.fed + 0.1 * tonight
            if _on_or_after(today, FATTEN):
                s.fat += max(-BURN[2], FAT_GAIN * (tonight - FAT_KEEP))   # a poor evening costs what one in does
            s.evenings += 1
            if s.first is None:
                s.first = "%02d-%02d" % (today.month, today.day)
                if today.month <= 6:
                    said.append("the bats are out again, hunting over the %s" % over)
        else:
            s.fat = max(0.0, s.fat - 0.02)                  # a winter waking costs more than it brings
        s.moths += took
    elif s.asleep is None:
        s.fed = max(0.0, s.fed - 0.01)                      # an evening in, in the hunting months: a little hungrier
        if _on_or_after(today, FATTEN):
            s.fat -= BURN[2]                                # (and in autumn a little leaner, though they lie torpid)
    else:
        s.fat = max(0.0, s.fat - BURN[1])                   # asleep, on their fat
        dying = WINTER_DEATH[0] + WINTER_DEATH[1] * (1 - s.fat) ** 2
        dead = sum(1 for _ in range(s.bats) if rng.random() < dying)
        dead = min(dead, s.bats - FEWEST)
        s.bats -= dead
        s.died += dead

    if s.asleep is None and not _on_or_after(today, FATTEN):
        s.fat -= BURN[0]                                    # awake in spring and summer, they live on what is left
    if (today.month, today.day) == BORN:
        young = _whole(s.bats * MOTHERS * RAISED * s.fed, rng)
        s.young += young
        s.bats = min(MOST, s.bats + young)
    if (today.month, today.day) == FLYING and s.young:
        said.append("the young bats are flying with the others now")
    if (today.month, today.day) == JOIN and s.asleep is None and s.fed >= JOIN_FED and s.bats < JOIN_BELOW:
        joined = min(MOST - s.bats, rng.randint(1, 2))      # a small colony that has fed well draws others to it
        s.bats += joined
        s.came += joined
    s.bats = max(FEWEST, min(MOST, s.bats))
    record = [_number(line, r"most (\d{1,4})") for line in s.years]
    if len(s.years) >= 3 and s.bats > max(record) and s.most <= max(record):
        said.append("there are more bats in the colony than in any year before")
    s.most = max(s.most, s.bats)
    s.fed = round(min(1.0, max(0.0, s.fed)), 3)
    s.fat = round(min(1.0, max(0.0, s.fat)), 3)

    _keep_perch(garden, ctx, s, took, over)
    ctx.save(s.text())
    return said


def _number(text, pattern) -> int:
    found = re.search(pattern, text)
    return int(found.group(1)) if found else 0


def present(garden, ctx):
    """On a summer evening, in the hours after sunset, if the evening is good enough: hunting over a bed."""
    today, sky = ctx.date, ctx.sky
    if not 5 <= today.month <= 9 or not evening(sky) or ctx.hour is None:
        return None
    noon = 13.5 if 4 <= today.month <= 10 else 12.5          # (the clock's noon is about an hour and a half
    sunset = noon + sky.daylength / 2.0                       #  past the sun's in summer time, half an hour in winter)
    if not int(sunset) <= ctx.hour <= sunset + 3:
        return None
    s = _State(ctx.state, today)
    if s.asleep is not None:
        return None
    over = _hunting_ground(garden)
    if not over:
        return None
    return ("A bat is hunting over the %s" if s.bats <= 2 else "Bats are hunting over the %s") % over


def draw(text, ctx, pen):
    """The perch, and under it the wings: a column for each night they hunted, set by its date, so that a gap is
    a night they stayed in; in each column a pair of wings for each pair that fell, the first at the foot."""
    nights = _nights(text)[-WINGS_KEPT:]
    pen.unit_name = "night, nights"
    pen.ground(0)
    tallest = 1.0
    today = getattr(ctx, "date", None)
    first = nights[0][0] if nights else None
    span = 4
    for when, took, over, wings in nights:
        recent = today is not None and 0 <= (today - when).days <= 3     # fell in the last three days
        ink = "brown" if recent else "#c4ab8e"
        place = min((when - first).days, 400)
        span = max(span, place + 1)
        x = place + 0.5
        for at in range(min(wings, 60)):
            y = 0.3 + at * 0.4
            tallest = max(tallest, y + 0.4)
            pen.polyline([(x, y), (x - 0.24, y + 0.14), (x - 0.24, y - 0.14)], 3, ink, closed=True)
            pen.polyline([(x, y), (x + 0.24, y + 0.14), (x + 0.24, y - 0.14)], 3, ink, closed=True)
        pen.label(x, -0.45, "%d" % when.day, 13, "ink")
    pen.line(-0.2, tallest + 0.8, span + 0.2, tallest + 0.8, 8, "brown")
    pen.label(span / 2.0, tallest + 1.25, "the perch", 15, "ink")
    if nights:
        taken = sum(night[1] for night in nights)
        overs = {}
        for night in nights:
            overs[night[2]] = overs.get(night[2], 0) + night[1]
        pen.note("%d moths taken in the last %d night%s they hunted, most over the %s" % (
            taken, len(nights), "" if len(nights) == 1 else "s", max(sorted(overs), key=lambda bed: overs[bed])))
        pen.note("a pair of wings for each pair that fell; dark if it fell in the last three days, else faded")
        pen.note("a column for each night, the day of the month under it; a gap is a night they stayed in")
    else:
        pen.note("no wings lie under the perch now")
