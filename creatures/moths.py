"""
Moths: the night's carriers of pollen, who come to scented flowers.

A visitor almost never meets them. What they did is in the crosses among
the flowers that smell at dusk and at night, and in two files.

Their own file, ground/creatures/moths:

    moths: 312            on the wing now
    asleep: 0             in the ground and in the joints of the wall, as eggs and
                          cocoons, until spring
    wall: north-wall      the bed whose wall they rest on by day
    this year: 2027 · first out 03-12 · most 640 · taken 1870 · to ground 0 · grains 2310
    the years:
    2027  first out 03-12 · most on the wing 640 · taken by the bats 1870 · to ground 410 · grains 2310

Any number in it may be changed by hand, and the moths go on from what it
says; a line that cannot be read is taken as if it were not there. A line
of your own beginning with # is kept.

And the wall, beds/north-wall/moths (in whatever bed `wall:` names), which
is a thing they make: see THE WALL below.


THE YEAR

All winter the moths are asleep, as eggs and cocoons in the ground and in
the joints of the wall, and a few of them are lost each week. From March,
on mild nights, they come out, about six in each hundred on a good night,
until by midsummer all that will come have come. From May to August they
breed, on every mild night, as fast as the garden can feed their
caterpillars: the
more plants growing, the more moths it holds (150, and 8 more for each
living plant, up to 1,200), and the closer they come to that the slower
they breed. A few come over the wall from outside on warm summer nights.
Moths on the wing live a few weeks; cold nights kill more of them, frost
most. From the middle of August they lay the eggs that will sleep the
winter, so the more moths there are in the autumn, the more come out the
next spring. In the dead of winter, on a mild night, a few winter moths
fly.


THE JOB: CARRYING POLLEN

On a mild night (8° or more at dusk, the night not below 2°, the wind under
6, not pouring) they go to the flowers whose seed says `scent: dusk` or
`scent: night` (or evening), and to no others: scent is how they find them.
A moth goes from flower to scented flower; when the next is of the same
kind as the last, it carries a grain of the last one's pollen to it
(garden.pollen), and that plant may cast a crossed seed that day. Moths do
not keep to one kind the way bees do. Three flights in four stay in the
bed, most of the rest go to the next bed along the plan, and a few cross
the garden. How many flights follows how many moths are out, how good the
night is, and how many scented flowers are open.

  dusk or night   on a cool night they fly only in the dusk, so the flowers
                  scented at night see fewer of them (four in ten); on a
                  warm night (13° at dusk) both alike
  the moon        a bright moon on a clear night keeps some of them in


THE BATS

The bats (creatures/bats.py) take moths on warm evenings. They eat at a
perch, and the wings fall beneath it: the bats keep that pile as a thing of
theirs, beds/<bed>/moth-wings, with a line for each night they hunted, how
many moths they took and over which bed. Each night the moths read the
line for that night there, and so many fewer of them fly on. The balance
between the two is in their files, a line a year: years of many moths feed
the bats, years of many bats thin the moths.


THE WALL

By day the moths rest on a wall, wings folded. The thing they make,
beds/<wall>/moths, is that wall in text: ten courses of stones, each stone
four places wide. Each ^ is a moth at rest: of every ten moths on the
wing, one rests on this wall. Each o is a cocoon tucked into a joint: one
for every ten asleep. The moths settle anew each morning; the cocoons stay
where they were put until they hatch. The bats count what they can hunt
by this wall, and another creature that hunts moths could do the same.
Its drawing (look.py beds/<wall>/moths) is the stones in the faint ink, a
small brown tent for each moth at rest and a pale ring for each cocoon.


WHAT THE ALMANAC HEARS

The first moths of the year, the first night of a year when the air is
thick with them (six hundred on the wing), and the winter moths out on a
mild night in the dead of winter. The rest is in their file.


AT THE GATE

At an arrival late at night, on a mild night when a scented flower is
open, they are at it, and the note says which.
"""

import datetime
import random
import re

import hands

NAME = "moths"

MOST = 2000               # moths on the wing, at the most
ASLEEP_MOST = 3000        # eggs and cocoons asleep, at the most
ASLEEP_FEWEST = 20        # asleep in the dead of winter, at the fewest (some always sleep in the hedge beyond)
HELD_BASE, HELD_A_PLANT, HELD_MOST = 150, 8, 1200     # how many moths the garden can feed (see THE YEAR)
EMERGE = 0.06             # of those asleep, the share that comes out on a good spring night
BREED = 0.15              # young moths a moth adds on a good summer night, while the garden can feed them
DIE = 0.025               # of those on the wing, the share that dies each day
LAY = 0.035               # from mid-August: the eggs laid for next year, for each moth on the wing, each night
SLEEP_LOSS = 0.002        # of those asleep, the share lost each winter day
WINTER_SHARE = 0.02       # of those asleep, the share that fly as winter moths on a mild winter night
FLIGHTS_MOST = 300        # flights from flower to flower in a night, at the most
FLIGHTS_A_MOTH = 0.4      # flights a moth makes in a good night, as counted here
STAY, NEXT = 0.75, 0.20   # of flights: in the bed; to the next bed (the rest go anywhere)
THICK = 600               # on the wing: a night thick with moths
YEARS_KEPT = 60
EVENING = ("dusk", "night", "evening")

WALL = "moths"            # the thing's name, and another if a hand's file has that name already
WALL_ELSE = "moths-at-rest"
COURSES, STONES, PLACES = 10, 12, 4

HEAD = (
    "# The moths of this garden; creatures/moths.py says how they live.",
    "# moths: on the wing now · asleep: as eggs and cocoons, until spring · wall: the bed whose",
    "# wall they rest on by day (they make beds/<that bed>/moths, a picture of it in text).",
    "# Any number may be changed by hand; the moths go on from what it says.",
)
_YEAR_LINE = re.compile(r"^\s*(\d{4})\s{2,}\S")


# ------------------------------------------------------------------ their file

class _State:
    """The moths' own file, read forgivingly, and written back whole."""

    def __init__(self, text, today):
        text = str(text or "")
        keys = hands.read_keys(text)
        if "moths" in keys or "asleep" in keys:
            self.moths = int(hands.num(keys, "moths", 0, 0, MOST))
            self.asleep = int(hands.num(keys, "asleep", 0, 0, ASLEEP_MOST))
        else:                                             # no file yet: as they would be at this time of year
            month = today.month
            self.moths = 0 if month in (12, 1, 2) else 60 if month in (3, 4, 11) else 250
            self.asleep = 300 if month in (9, 10, 11, 12, 1, 2) else 120 if month in (3, 4) else 0
        self.wall = hands.line(keys, "wall", "")
        self.winter = _date(hands.line(keys, "winter moths"))
        this = hands.line(keys, "this year")
        found = re.match(r"\s*(\d{4})", this)
        self.year = int(found.group(1)) if found else today.year
        self.first = _field(this, r"first out (\d{1,2}-\d{1,2})", None, str)
        self.most = _field(this, r"most (\d{1,6})", 0)
        self.taken = _field(this, r"taken (\d{1,9})", 0)
        self.laid = _field(this, r"to ground (\d{1,9})", 0)
        self.grains = _field(this, r"grains (\d{1,9})", 0)
        self.years = [line.strip() for line in text.splitlines() if _YEAR_LINE.match(line)][-YEARS_KEPT:]
        self.remarks = [line.rstrip()[:200] for line in text.splitlines()
                        if line.strip().startswith("#") and line.rstrip() not in HEAD][:12]

    def roll(self, today) -> None:
        """A new year: the old one goes into `the years`."""
        if today.year <= self.year:
            return
        self.years.append("%d  first out %s · most on the wing %d · taken by the bats %d · to ground %d · grains %d"
                          % (self.year, self.first or "--", self.most, self.taken, self.laid, self.grains))
        self.years = self.years[-YEARS_KEPT:]
        self.year, self.first, self.most, self.taken, self.laid, self.grains = today.year, None, 0, 0, 0, 0

    def text(self) -> str:
        lines = list(HEAD) + self.remarks
        lines += ["moths: %d" % self.moths, "asleep: %d" % self.asleep]
        if self.wall:
            lines.append("wall: %s" % self.wall)
        if self.winter:
            lines.append("winter moths: %s" % self.winter.isoformat())
        lines.append("this year: %d · first out %s · most %d · taken %d · to ground %d · grains %d" % (
            self.year, self.first or "--", self.most, self.taken, self.laid, self.grains))
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


# ------------------------------------------------------------------ the night

def dusk(sky) -> float:
    """The warmth at dusk, reckoned from the day's lowest and highest."""
    return sky.tmin + 0.45 * (sky.tmax - sky.tmin)


def night(sky) -> float:
    """How good a night it is for moths: 0 (they stay down) to 1. Mild, still, not pouring; the moon not too bright."""
    warm = dusk(sky)
    if warm < 8 or sky.tmin < 2 or sky.wind >= 6 or sky.rain >= 8:
        return 0.0
    bright = (1 - 2 * abs(sky.moon - 0.5)) * (1 - sky.cloud)          # a full moon in a clear sky is 1
    good = min(1.0, (warm - 7) / 8.0) * (1 - sky.wind / 8.0) * (1 - sky.rain / 12.0) * (1 - 0.3 * bright)
    return max(0.05, good)


def _scented(plant) -> str:
    """'dusk', 'night' or '' : whether the moths come to this plant, and when."""
    word = (plant.scent.split() or [""])[0]
    return ("night" if word == "night" else "dusk") if word in EVENING else ""


def _in_scent(garden, sky) -> list:
    """[(plant, weight)] for every living plant scented at dusk or night with flowers open tonight."""
    late = 1.0 if dusk(sky) >= 13 else 0.4                 # on a cool night the moths fly only in the dusk
    found = []
    for plant in garden.plants():
        scent = "" if plant.dead else _scented(plant)
        if scent:
            count = plant.flowers
            if count > 0:
                found.append((plant, count * (late if scent == "night" else 1.0)))
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
    """Flights among the open scented `flowers`, `flights` in all. Returns the grains of pollen carried.

    A moth begins at a flower chosen by its weight and visits two to six
    more: in the same bed (STAY), else in the nearest bed with a scented
    flower open (NEXT), else anywhere. It carries a grain only when the
    flower it comes to is of the same kind as the one it left.
    """
    weights = [weight for _, weight in flowers]
    by_bed = {}
    for at, (plant, _) in enumerate(flowers):
        by_bed.setdefault(plant.bed, []).append(at)
    near = _nearness(garden)
    grains = done = 0

    def pick(choices):
        return choices[0] if len(choices) == 1 else rng.choices(choices, [weights[c] for c in choices])[0]

    while done < flights:
        here = rng.choices(range(len(flowers)), weights)[0]
        for _ in range(rng.randint(2, 6)):
            if done >= flights:
                break
            done += 1
            plant = flowers[here][0]
            roll, choices = rng.random(), []
            if roll < STAY:
                choices = [c for c in by_bed.get(plant.bed, ()) if c != here]
            elif roll < STAY + NEXT:
                for bed in near.get(plant.bed, ()):
                    choices = by_bed.get(bed, [])
                    if choices:
                        break
            else:
                choices = [c for c in range(len(flowers)) if flowers[c][0].bed != plant.bed]
            choices = choices or [c for c in range(len(flowers)) if c != here]
            if not choices:
                break
            there = pick(choices)
            if flowers[there][0].kind == plant.kind and garden.pollen(plant, flowers[there][0]):
                grains += 1
            here = there
    return grains


def _taken(garden, today) -> int:
    """How many moths the bats took tonight, as the wings under their perch say."""
    count = 0
    # (the space before the date on its own line only, so that a text of many empty lines is gone over once)
    pattern = re.compile(r"^[^\S\n]*%s\s+took\s+(\d{1,6})" % re.escape(today.isoformat()), re.MULTILINE)
    for thing in garden.things():
        if thing.maker == "bats":
            count += sum(int(found) for found in pattern.findall(thing.text or ""))
    return count


# ------------------------------------------------------------------ the wall

def _wall_bed(garden, said) -> str:
    """The bed of the wall they rest on: the one their file names, if it is there; else a walled bed, the most
    sheltered; else the most sheltered bed but the keeper's own."""
    beds = garden.beds()
    if said in {bed.name for bed in beds}:
        return said
    walled = [bed for bed in beds if "wall" in ("%s %s" % (bed.name, bed.lies)).lower() and bed.name != "gate-border"]
    pool = walled or [bed for bed in beds if bed.name != "gate-border"] or beds
    return sorted(pool, key=lambda bed: (-bed.shelter, bed.name))[0].name if pool else ""


def _wall_text(bed, resting, cocoons, rng, keep) -> str:
    """The wall as text: COURSES rows of STONES stones, PLACES places to a stone; ^ a moth at rest, o a cocoon.

    The cocoons lie in places fixed for the whole winter (`keep`, dice that
    fall the same way all season); the moths take any free place each day.
    """
    places = COURSES * STONES * PLACES
    order = list(range(places))
    keep.shuffle(order)
    cocoon_at = set(order[:min(cocoons, places // 2)])
    free = [place for place in range(places) if place not in cocoon_at]
    moth_at = set(rng.sample(free, min(resting, len(free) // 2)))
    rows = []
    for course in range(COURSES):
        stones = []
        for stone in range(STONES):
            marks = ""
            for place in range(PLACES):
                at = (course * STONES + stone) * PLACES + place
                marks += "^" if at in moth_at else "o" if at in cocoon_at else " "
            stones.append(marks)
        rows.append(("  " if course % 2 else "") + "|" + "|".join(stones) + "|")
    return "\n".join([
        "The wall by the %s bed, by day. Moths rest on its stones until dusk, wings folded:" % bed,
        "of every ten moths on the wing in the garden, one is here. Each ^ is a moth at rest.",
        "Each o is a cocoon tucked into a joint of the wall, one for every ten moths asleep.",
        "The moths made this, and settle anew each morning. The bats count what they can hunt by it.",
        "",
    ] + rows + ["", "on the wall today: %d moth%s at rest, %d cocoon%s" % (
        len(moth_at), "" if len(moth_at) == 1 else "s", len(cocoon_at), "" if len(cocoon_at) == 1 else "s")]) + "\n"


def _keep_wall(garden, ctx, s) -> None:
    """Make the wall anew, as it stands today; and take away any wall of theirs left in another bed."""
    bed = _wall_bed(garden, s.wall)
    if not bed:
        return
    s.wall = bed
    winter = ctx.date.year if ctx.date.month >= 7 else ctx.date.year - 1      # cocoons stay put from July to June
    keep = random.Random("%s|cocoons|%s|%d" % (NAME, bed, winter))
    text = _wall_text(bed, round(s.moths / 10.0), round(s.asleep / 10.0), ctx.rng, keep)
    name = WALL if garden.make(bed, WALL, text) else WALL_ELSE if garden.make(bed, WALL_ELSE, text) else ""
    if not name:
        return                                           # (a hand's files stand where the wall would be)
    for thing in garden.things():
        if thing.maker == NAME and (thing.bed, thing.name) != (bed, name):
            garden.unmake(thing.bed, thing.name, "the moths rest on another wall now")


# ------------------------------------------------------------------ the creature

def day(garden, ctx):
    today, sky, rng = ctx.date, ctx.sky, ctx.rng
    s = _State(ctx.state, today)
    s.roll(today)
    said = []
    month = today.month
    q = night(sky)
    living = sum(1 for plant in garden.plants() if not plant.dead)
    held = min(HELD_MOST, HELD_BASE + HELD_A_PLANT * living)

    if 3 <= month <= 6 and q and s.asleep:                       # spring: out of the ground
        out = min(s.asleep, _whole(s.asleep * EMERGE * q, rng))
        s.asleep -= out
        s.moths += out
        if out and s.first is None:
            s.first = "%02d-%02d" % (month, today.day)
            said.append("the first moths of the year are out")
    if (month, today.day) == (7, 1):
        s.asleep = 0                                             # what has not come out by now never will
    if 5 <= month <= 8 and q:                                    # summer: breeding, as the garden can feed them
        s.moths += _whole(BREED * s.moths * max(0.0, 1 - s.moths / float(held)) * q, rng)
    if 5 <= month <= 9 and q > 0.4:
        s.moths += rng.randint(0, 3)                             # a few from over the wall
    if 3 <= month <= 11:                                         # the days of their short lives
        cold = 0.3 if sky.tmin < 0 else 0.08 if sky.tmin < 4 else 0.0
        s.moths -= _whole(s.moths * (DIE + cold), rng)
    if (month, today.day) >= (8, 15) and month <= 11:            # autumn: the eggs for next year
        laid = _whole(s.moths * LAY * max(q, 0.3), rng)
        s.asleep += laid
        s.laid += laid
    if month >= 10 or month <= 3:                                # winter: some of the sleepers are lost
        s.asleep -= _whole(s.asleep * SLEEP_LOSS, rng)
    if month in (12, 1, 2):                                      # the dead of winter: only the winter moths
        s.asleep = max(s.asleep, ASLEEP_FEWEST)
        s.moths = _whole(s.asleep * WINTER_SHARE * q, rng) if q else 0
        if s.moths and (s.winter is None or (today - s.winter).days > 120):
            s.winter = today
            said.append("the winter moths are out on a mild night")

    taken = min(s.moths, _taken(garden, today))                  # what the bats took tonight
    s.moths -= taken
    s.taken += taken
    s.moths = max(0, min(MOST, s.moths))
    s.asleep = max(0, min(ASLEEP_MOST, s.asleep))

    if q and s.moths:
        flowers = _in_scent(garden, sky)
        flights = min(FLIGHTS_MOST, round(s.moths * FLIGHTS_A_MOTH * q), 3 * sum(p.flowers for p, _ in flowers))
        if flights > 0:
            s.grains += _flights(garden, rng, flowers, flights)

    if s.moths >= THICK > s.most:
        said.append("the air is thick with moths tonight")
    s.most = max(s.most, s.moths)
    _keep_wall(garden, ctx, s)
    ctx.save(s.text())
    return said


def present(garden, ctx):
    """Late on a mild night: at the scented flower with the most open."""
    hour = ctx.hour if ctx.hour is not None else 12
    if not (hour >= 22 or hour <= 3) or not night(ctx.sky):
        return None
    if _State(ctx.state, ctx.date).moths < 5:
        return None
    flowers = _in_scent(garden, ctx.sky)
    if not flowers:
        return None
    best = max(flowers, key=lambda item: (item[1], item[0].where))[0]
    return "Moths are at the %s in the %s" % (best.name, best.bed)


def draw(text, ctx, pen):
    """The wall as the text has it: its joints in the faint ink, a brown tent for each moth, a pale ring for each
    cocoon. One stone is one unit; every mark stands where its character stands in the text."""
    rows = [line.rstrip() for line in str(text or "").splitlines() if line.count("|") >= 2][:40]
    pen.unit_name = "stone, stones"
    pen.ground(0)
    height = 0.5
    moths = cocoons = 0
    for number, row in enumerate(rows):
        bottom = (len(rows) - 1 - number) * height
        joints = [at for at, mark in enumerate(row) if mark == "|"]
        if joints:
            left, right = joints[0] / 4.0, joints[-1] / 4.0
            pen.line(left, bottom, right, bottom, 2, "faint")
            if number == 0:
                pen.line(left, bottom + height, right, bottom + height, 2, "faint")
        for at in joints:
            pen.line(at / 4.0, bottom, at / 4.0, bottom + height, 2, "faint")
        for at, mark in enumerate(row[:400]):
            x = (at + 0.5) / 4.0
            if mark == "^":
                moths += 1
                y = bottom + 0.2
                pen.polyline([(x - 0.1, y - 0.08), (x + 0.1, y - 0.08), (x, y + 0.13)], 4, "brown", closed=True)
            elif mark in "oO":
                cocoons += 1
                pen.dot(x, bottom + height / 2, 5, "#efe6cf")
                pen.dot(x, bottom + height / 2, 5, "brown", filled=False, weight=2)
    pen.note("%d moth%s at rest on the wall, %d cocoon%s in its joints" % (
        moths, "" if moths == 1 else "s", cocoons, "" if cocoons == 1 else "s"))
    pen.note("a moth here for every ten on the wing; a cocoon for every ten asleep")
