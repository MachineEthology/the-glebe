"""
Bees: the bumblebees of the garden, who carry pollen from flower to flower.

They are wild bumblebees, a nest or two somewhere in the long grass, and
they live the bumblebee's year by the garden's real calendar and its sky.
A visitor almost never meets them. What they did is in the crosses that
come up, and in their own file, ground/creatures/bees:

    bees: 84              workers out of the nests now
    nests: 2              nests going this year (three at the most: there is no room for more)
    queens: 0             young queens asleep in the ground, until spring
    raised: 3             young queens raised this summer, still in the nests
    founded: 2027-04-02 · 2027-04-09     the day each nest was begun, one date for each
    raising: 2027-07-20   the day the nests turned from raising workers to raising queens
    over the wall: 2026-05-03   the last time a queen came over the wall to an empty garden
    this year: 2027 · first out 03-04 · out on 57 days · most 240 · grains 3120 · young queens 0
    the years:
    2026  first out 10-01 · out on 9 days · most 30 · grains 41 · young queens 5

Any number in it may be changed by hand, and the bees go on from what it
says; a line that cannot be read is taken as if it were not there. A line
of your own beginning with # is kept.


THE YEAR

In winter only the young queens are left, asleep in the ground, and a few
of them die each week. From the middle of February, on the first days warm
and still enough to fly, they wake one by one, feed at whatever is in
flower, and look for a place to nest. Some find one and begin a nest, until
there are three; the others go over the wall. A spring left with no nest
and no queen, because none woke or because the nests failed, is mended from
outside, once in a year at the most: sooner or later between April and the
middle of June, a queen comes over the wall and begins a nest.

About three and a half weeks after a nest is begun its first workers fly:
three to five of them, which the queen raised alone on what she carried and
found, however few the flowers. From then the nest grows on every day the
bees can fly, as fast as the open flowers can feed it: twenty-five open
flowers a nest is plenty, five is lean. Workers live a few weeks. If they
are all gone and no more are coming, two months after the youngest nest
was begun, the nests have failed. From July a full nest turns to raising young
queens instead of workers, and by August every nest has. From September
the workers die faster; when the last of them are gone the nests are done,
and the young queens go to ground for the winter. Next year's nests come
from them. So the bees rise and fall within each year, never more than 120
to a nest, and from year to year they follow the flowers.


THE JOB: CARRYING POLLEN

On a day warm, dry and still enough to fly (13° at the warmest, under 2 mm
of rain, the wind under 5) the bees go to the open flowers: those of every
plant whose kind counts them (its flowers()). A bee chooses a flower and
flies a round of a few more from it. Bumblebees keep to one kind of flower
in a round, and that is what carries pollen where it can set seed: a flight
from a plant to another of the same kind takes a grain of the first one's
pollen to the second (garden.pollen), and the second may cast a crossed
seed that day. Four flights in five stay in the bed. Most of the rest go to
the next bed along the plan, the nearest one with that kind in flower, and
now and then a bee crosses the whole garden. A bee that leaves one kind for
another carries nothing that will take.

How many flights there are follows the number of bees, how good the day
is, and how many flowers are open: on a good day about one flight (from one
flower to the next) for each bee, as the garden counts them, and three
hundred at the most. Which flowers they choose follows the count of open
flowers, and two things in a seed:

  colour   bees see blue, violet, yellow and white well, and red hardly at
           all (a red flower is a bird's or a butterfly's), so a deep red
           flower is visited about a third as often as it would be, a blue
           or violet one a third more. Pink is seen well enough.
  scent    a flower scented by day (scent: day) holds them half as long
           again; one scented only at dusk or night is mostly shut while
           they fly, and is visited a third as often.


WHAT THE ALMANAC HEARS

The first queen of the year out of the ground, the day the nests turn to
raising queens, a queen come over the wall to an empty garden, and the day
the nests are done (or the day they failed, if they did). The rest is in
their file.


AT THE GATE

At an arrival on a warm afternoon when they are flying, they are at the
plant with the most flowers they care for, and the note says which.
"""

import colorsys
import datetime
import re

import hands

NAME = "bees"

NESTS_MOST = 3            # nests the garden has room for
NEST_BEES = 120           # workers one nest holds at the most
QUEENS_MOST = 30          # young queens asleep in the ground, at the most
RAISED_A_NEST = 10        # young queens one nest raises in a summer, at the most
FLIGHTS_MOST = 300        # flights from flower to flower in a day, at the most (the ground allows 400 grains)
FLIGHTS_A_BEE = 1.2       # flights a forager makes in a good day, as counted here
YEARS_KEPT = 60           # lines of `the years` the file keeps

WAKE = ((2, 15), (6, 15))       # (month, day): queens wake on flying days between these
FIRST_WORKERS = 25              # days from a nest's beginning to its first workers
FIRST_BROOD = (3, 5)            # workers in a nest's first brood, which the queen raises alone, whatever the flowers
FAILS_AFTER = 60                # days from the youngest nest's beginning: no worker left by then, and the nests fail
BROOD = 4.0                    # workers a nest raises in a good day, when the flowers are enough
FLOWERS_A_NEST = 25.0           # open flowers (as the bees like them) that feed a nest fully
QUEEN_RATE = 0.12               # the chance a good day that a nest raises a young queen, when the flowers are enough
NEST_TAKES = 0.7                # the chance that a queen who wakes finds a place and her nest takes
RAISE_FULL = (7, 1)             # from here a full nest turns to raising queens ...
RAISE_ALL = (8, 1)              # ... and from here every nest does
WANE = (9, 1)                   # from here the workers die faster, and the nests come to an end
END_BY = (11, 15)               # no nest goes on past this
WINTER_LOSS = 0.002             # the chance a day that an asleep queen dies
STAY, NEXT = 0.80, 0.17         # of flights: in the bed; to the next bed (the rest go anywhere)
KEEP_KIND = 0.85                # the chance, at each flight in a round, that a bee keeps to the same kind

HEAD = (
    "# The bumblebees of this garden; creatures/bees.py says how they live.",
    "# bees: workers out of the nests now · nests: nests going this year · queens: young queens",
    "# asleep in the ground until spring · raised: young queens raised this summer, still in the nests.",
    "# Any number may be changed by hand; the bees go on from what it says.",
)
INK_WORDS = ("dark-red", "pale-pink", "red", "pink", "orange", "yellow", "blue", "violet", "brown", "white",
             "black", "grey")
_HEX = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")
_YEAR_LINE = re.compile(r"^\s*(\d{4})\s{2,}\S")


# ------------------------------------------------------------------ their file

class _State:
    """The bees' own file, read forgivingly, and written back whole."""

    def __init__(self, text, today):
        text = str(text or "")
        keys = hands.read_keys(text)
        self.keys = keys
        if any(key in keys for key in ("bees", "nests", "queens")):
            self.bees = int(hands.num(keys, "bees", 0, 0, NESTS_MOST * NEST_BEES))
            self.nests = int(hands.num(keys, "nests", 0, 0, NESTS_MOST))
            self.queens = int(hands.num(keys, "queens", 0, 0, QUEENS_MOST))
            self.raised = int(hands.num(keys, "raised", 0, 0, NESTS_MOST * RAISED_A_NEST))
            self.begun = _dates(hands.line(keys, "founded"))
            self.raising = _date(hands.line(keys, "raising"))
        else:
            self._first_year(today)
        # one founding day for each nest: the oldest kept if a hand took nests away; a nest a hand
        # added with no day of its own is taken as begun with the youngest (or today, if none says)
        self.begun = sorted(self.begun)[:self.nests]
        while len(self.begun) < self.nests:
            self.begun.append(self.begun[-1] if self.begun else today)
        self.came = _date(hands.line(keys, "over the wall"))
        this = hands.line(keys, "this year")
        found = re.match(r"\s*(\d{4})", this)
        self.year = int(found.group(1)) if found else today.year
        self.first = _field(this, r"first out (\d{1,2}-\d{1,2})", None, str)
        self.days = _field(this, r"out on (\d{1,4}) day", 0)
        self.most = _field(this, r"most (\d{1,6})", 0)
        self.grains = _field(this, r"grains (\d{1,9})", 0)
        self.young = _field(this, r"young queens (\d{1,4})", 0)
        self.years = [line.strip() for line in text.splitlines() if _YEAR_LINE.match(line)][-YEARS_KEPT:]
        self.remarks = [line.rstrip()[:200] for line in text.splitlines()
                        if line.strip().startswith("#") and line.rstrip() not in HEAD][:12]

    def _first_year(self, today):
        """No file yet (or none that says anything): the bees as they would be at this time of year."""
        self.bees, self.nests, self.queens, self.raised = 0, 0, 6, 0
        self.begun, self.raising = [], None
        if 4 <= today.month <= 10:
            self.bees, self.nests, self.queens = 40, 2, 0
            self.begun = [datetime.date(today.year, 4, 1)] * 2
        if today.month in (9, 10):                        # a nest past its best, already raising queens
            self.bees, self.nests, self.raised = 30, 1, 5
            self.raising = datetime.date(today.year, 8, 1)

    def roll(self, today) -> None:
        """A new year: the old one goes into `the years`, if anything happened in it."""
        if today.year <= self.year:
            return
        if self.days or self.most or self.young:
            self.years.append("%d  first out %s · out on %d days · most %d · grains %d · young queens %d" % (
                self.year, self.first or "--", self.days, self.most, self.grains, self.young))
            self.years = self.years[-YEARS_KEPT:]
        self.year, self.first, self.days, self.most, self.grains, self.young = today.year, None, 0, 0, 0, 0

    def text(self) -> str:
        lines = list(HEAD) + self.remarks
        lines += ["bees: %d" % self.bees, "nests: %d" % self.nests, "queens: %d" % self.queens,
                  "raised: %d" % self.raised]
        if self.begun:
            lines.append("founded: %s" % " · ".join(day.isoformat() for day in self.begun))
        if self.raising:
            lines.append("raising: %s" % self.raising.isoformat())
        if self.came:
            lines.append("over the wall: %s" % self.came.isoformat())
        lines.append("this year: %d · first out %s · out on %d days · most %d · grains %d · young queens %d" % (
            self.year, self.first or "--", self.days, self.most, self.grains, self.young))
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


def _dates(text) -> list:
    """Every real date written in `text` (the first few), in the order written; what is not a day is passed over."""
    found = []
    for match in re.finditer(r"(\d{4})-(\d{1,2})-(\d{1,2})", str(text or "")[:400]):
        try:
            found.append(datetime.date(*(int(part) for part in match.groups())))
        except ValueError:
            continue
    return found[:NESTS_MOST * 4]


def _field(text, pattern, default, kind=int):
    found = re.search(pattern, str(text or ""))
    if not found:
        return default
    try:
        return kind(found.group(1))
    except ValueError:
        return default


def _on_or_after(today, month_day) -> bool:
    return (today.month, today.day) >= month_day


# ------------------------------------------------------------------ the day, the flowers

def _flying(sky) -> float:
    """How good a day it is for bees: 0 (they stay in) to 1. Warm, dry and still."""
    if sky.tmax < 13 or sky.rain >= 2 or sky.wind >= 5:
        return 0.0
    return max(0.05, min(1.0, (sky.tmax - 11) / 8.0) * (1 - sky.rain / 3.0) * (1 - sky.wind / 7.0))


def _colour(seed) -> str:
    """A seed's flower colour as written: its `colour:` line, else an ink or #hex in its `flower:` line; or ''."""
    for key in ("colour", "color"):
        said = hands.line(seed, key, "")
        if said:
            return said
    for key in ("flower", "flowers", "bloom"):
        said = hands.line(seed, key, "").lower()
        found = _HEX.search(said)
        if found:
            return found.group()
        for word in INK_WORDS:
            if re.search(r"(?<![\w-])%s(?![\w-])" % word, said):
                return word
    return ""


def _colour_liking(seed) -> float:
    """How a bee's eye takes a flower's colour: blue and violet best, then yellow and white; deep red hardly."""
    said = _colour(seed).strip().lower()
    if not said:
        return 1.0
    rgb = None
    for attempt in (said, said.replace(" ", "-"), (said.replace(",", " ").split() or [""])[0]):
        hexed = hands.mix(attempt, attempt, 0.0)
        if hexed != "#1a1a1a" or attempt in ("black", "#1a1a1a"):
            rgb = tuple(int(hexed[at:at + 2], 16) / 255.0 for at in (1, 3, 5))
            break
    if rgb is None:
        return 1.0
    hue, saturation, value = colorsys.rgb_to_hsv(*rgb)
    hue *= 360
    if saturation < 0.2:
        return 1.1 if value > 0.75 else 0.8                # white; grey or black
    if hue < 15 or hue >= 330:
        return 0.35 if saturation > 0.5 else 1.0           # deep red; pink
    if hue < 45:
        return 0.8                                         # orange
    if hue < 75:
        return 1.25                                        # yellow
    if hue < 170:
        return 0.8                                         # green
    return 1.35                                            # blue, violet, purple


def _liking(plant) -> float:
    """How much the bees care for a plant's flowers, apart from how many there are."""
    like = _colour_liking(plant.seed)
    scent = (plant.scent.split() or [""])[0]
    if scent == "day":
        like *= 1.5
    elif scent in ("dusk", "night", "evening"):
        like *= 0.3
    return like


def _in_flower(garden) -> list:
    """[(plant, weight)] for every living plant with flowers open today: weight = open flowers × liking."""
    found = []
    for plant in garden.plants():
        if plant.dead:
            continue
        count = plant.flowers
        if count > 0:
            found.append((plant, count * _liking(plant)))
    return found


def _nearness(garden) -> dict:
    """For each bed, the other beds, the nearest first, by their places on the plan (unplaced beds last)."""
    beds = garden.beds()
    places = {bed.name: bed.at for bed in beds}

    def apart(one, other):
        a, b = places.get(one), places.get(other)
        if not a or not b:
            return (1, 0.0, other)
        dx = max(0.0, max(a[0], b[0]) - min(a[0] + a[2], b[0] + b[2]))
        dy = max(0.0, max(a[1], b[1]) - min(a[1] + a[3], b[1] + b[3]))
        return (0, (dx * dx + dy * dy) ** 0.5, other)

    return {bed.name: [other for _, _, other in sorted(apart(bed.name, o.name) for o in beds if o.name != bed.name)]
            for bed in beds}


def _flights(garden, rng, flowers, flights) -> int:
    """Rounds of flights among the open `flowers`, `flights` in all. Returns the grains of pollen carried.

    A round begins at a flower chosen by its weight and goes on for three to
    eight flights. At each, the bee keeps to the kind it is on (KEEP_KIND)
    and goes: to another of that kind in the same bed (STAY); or to the
    nearest bed with that kind in flower (NEXT); or anywhere in the garden.
    Where there is none of the kind to go to, or the bee tires of it, it goes
    to any flower near by, and carries nothing that will take.
    """
    weights = [weight for _, weight in flowers]
    by_bed, by_kind_bed = {}, {}
    for at, (plant, _) in enumerate(flowers):
        by_bed.setdefault(plant.bed, []).append(at)
        by_kind_bed.setdefault((plant.kind, plant.bed), []).append(at)
    near = _nearness(garden)
    grains = done = 0

    def pick(choices):
        return choices[0] if len(choices) == 1 else rng.choices(choices, [weights[c] for c in choices])[0]

    while done < flights:
        here = rng.choices(range(len(flowers)), weights)[0]
        for _ in range(rng.randint(3, 8)):
            if done >= flights:
                break
            done += 1
            plant = flowers[here][0]
            choices = []
            if rng.random() < KEEP_KIND:
                roll = rng.random()
                if roll < STAY:
                    choices = [c for c in by_kind_bed.get((plant.kind, plant.bed), ()) if c != here]
                elif roll < STAY + NEXT:
                    for bed in near.get(plant.bed, ()):
                        choices = by_kind_bed.get((plant.kind, bed), [])
                        if choices:
                            break
                else:
                    choices = [c for c in range(len(flowers)) if flowers[c][0].kind == plant.kind
                               and flowers[c][0].bed != plant.bed]
            if not choices:                                # tired of the kind, or none of it to go to
                choices = [c for c in by_bed.get(plant.bed, ()) if c != here] or \
                          [c for c in range(len(flowers)) if c != here]
            if not choices:
                break
            there = pick(choices)
            if flowers[there][0].kind == plant.kind and garden.pollen(plant, flowers[there][0]):
                grains += 1
            here = there
    return grains


def _whole(n, rng) -> int:
    """A count with a fraction in it, made whole by the dice: 2.3 is 2 seven times in ten, 3 three times."""
    n = max(0.0, n)
    return int(n) + (1 if rng.random() < n - int(n) else 0)


def _best(flowers):
    """The plant with the most of what the bees care for, or None."""
    return max(flowers, key=lambda item: (item[1], item[0].where))[0] if flowers else None


def _the_end(nests, gone, today) -> str:
    """The almanac's line on the day the nests end: done for the year, or failed before their time."""
    the = "the nest is" if nests == 1 else "the nests are"
    if gone:
        return "%s done for the year; %s gone to ground for the winter" % (
            the, "a young queen has" if gone == 1 else "%d young queens have" % gone)
    if not _on_or_after(today, WANE):
        return "the bumblebees' %s failed this %s, and raised no young queens" % (
            "nest" if nests == 1 else "nests", "spring" if today.month < 6 else "summer")
    return "%s done for the year, and raised no young queens" % the


# ------------------------------------------------------------------ the creature

def day(garden, ctx):
    today, sky, rng = ctx.date, ctx.sky, ctx.rng
    s = _State(ctx.state, today)
    s.roll(today)
    said = []
    go = _flying(sky)
    flowers = None

    def in_flower():
        nonlocal flowers
        if flowers is None:
            flowers = _in_flower(garden)
        return flowers

    # winter: the queens asleep in the ground; a few die
    if s.queens:
        s.queens -= sum(1 for _ in range(s.queens) if rng.random() < WINTER_LOSS)

    # spring: the queens wake on flying days, and begin nests where they can
    waking = _on_or_after(today, WAKE[0]) and not _on_or_after(today, (WAKE[1][0], WAKE[1][1] + 1))
    if s.raising is not None and s.raising.year != today.year:
        s.raising = None                                 # (last year's, left by a hand)
    if go and waking:
        for _ in range(s.queens):
            if rng.random() < 0.35:
                s.queens -= 1
                if s.nests < NESTS_MOST and rng.random() < NEST_TAKES:
                    s.nests += 1
                    s.begun.append(today)
        if (not s.nests and not s.queens and _on_or_after(today, (4, 1))
                and (s.came is None or s.came.year != today.year) and rng.random() < 0.1):
            s.nests, s.begun, s.came = 1, [today], today     # (once a year at most)
            said.append("a bumblebee queen came over the wall and began a nest")
    if (today.month, today.day) == (WAKE[1][0], WAKE[1][1] + 1):
        s.queens = 0                                     # the ones that never woke, or found no place, have gone

    # flying: rounds among the open flowers
    foragers = s.bees + s.nests
    food = 0.0
    if go and foragers:
        if s.first is None:
            s.first = "%02d-%02d" % (today.month, today.day)
            if waking and not s.bees and not said:       # (in spring the first out are queens from the ground)
                best = _best(in_flower())
                said.append("the first bumblebee queen of the year is out" +
                            (", at the %s in the %s" % (best.name, best.bed) if best else ""))
        s.days += 1
        open_flowers = sum(plant.flowers for plant, _ in in_flower())
        flights = min(FLIGHTS_MOST, round(foragers * FLIGHTS_A_BEE * go), 3 * open_flowers)
        if flights > 0:
            s.grains += _flights(garden, rng, in_flower(), flights)
        if s.nests:
            food = min(1.0, sum(weight for _, weight in in_flower()) / (FLOWERS_A_NEST * s.nests))

    # the nests: workers, then queens, then the end
    if s.nests:
        ages = [(today - begun).days for begun in s.begun]
        grown = sum(1 for age in ages if age >= FIRST_WORKERS)          # nests whose workers are flying
        for age in ages:
            if age == FIRST_WORKERS:                                    # a nest's first brood comes out
                s.bees += rng.randint(*FIRST_BROOD)
        if s.raising is None and grown and (
                _on_or_after(today, RAISE_ALL)
                or (_on_or_after(today, RAISE_FULL) and s.bees >= 0.7 * NEST_BEES * s.nests)):
            s.raising = today
            said.append("the nest is raising young queens now" if s.nests == 1
                        else "the nests are raising young queens now")
        if go and s.raising is None and grown:
            s.bees += _whole(grown * BROOD * food * go, rng)
        if go and s.raising is not None:
            for _ in range(s.nests):
                if rng.random() < QUEEN_RATE * food:
                    s.raised += 1
            s.raised = min(s.raised, s.nests * RAISED_A_NEST)
        dying = 0.03 + (0.04 if sky.tmax < 10 else 0.0) + (0.06 if _on_or_after(today, WANE) else 0.0)
        s.bees -= _whole(s.bees * dying, rng)
        s.bees = min(s.bees, s.nests * NEST_BEES)
        s.most = max(s.most, s.bees)
        ended = (_on_or_after(today, WANE) and s.bees < 2) or _on_or_after(today, END_BY) or (
            grown == s.nests and s.bees < 1 and min(ages) > FAILS_AFTER)
        if ended:
            gone = s.raised
            s.queens = min(QUEENS_MOST, s.queens + gone)
            s.young += gone
            said.append(_the_end(s.nests, gone, today))
            s.bees = s.nests = s.raised = 0
            s.begun, s.raising = [], None
    else:
        s.bees = 0

    ctx.save(s.text())
    return said


def present(garden, ctx):
    """On a warm afternoon when they are flying: at the plant with the most flowers they care for."""
    if not (12 <= (ctx.hour or 0) <= 17) or not _flying(ctx.sky):
        return None
    s = _State(ctx.state, ctx.date)
    if not s.nests and not s.bees:
        return None
    best = _best(_in_flower(garden))
    if best is None:
        return None
    if s.bees >= 3:
        return "Bumblebees are working the %s in the %s" % (best.name, best.bed)
    return "A queen bumblebee is at the %s in the %s" % (best.name, best.bed)
