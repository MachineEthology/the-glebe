"""
The hedgehog: one, a she, who has the run of this garden and the gardens round it.

Her one job is to eat slugs at night. She sleeps through the cold months, in a
nest of dead leaves she keeps in the wild corner, and in some summers she has
young.

HER FILE, ground/creatures/hedgehog, says how she is:

    weight: 780 g                 heavier in autumn, lighter after the winter
    asleep: no                    or: since 2026-11-20
    nights lately: 7.4°           how cold the nights have been, lately (the lows, smoothed over about a week)
    young: none                   or: 4, born 2027-07-12 (and ", out with her", once they go out at night)
    litters: 2027                 the summers she has had young in

A hand may change any of it: wake her, put her to sleep, give her young. The
nights go on from what they find.

WHEN SHE SLEEPS. If she has fattened enough (600 g), she goes into her nest
for the winter when the nights lately fall below four degrees in the second
half of October, or below five and a half from November to February; a hard
cold spell in the deep of winter sends her in however light she is. Asleep
she loses a little weight each day. She wakes in spring once the nights
lately are above six degrees, or sooner if she has grown too thin; a mild
spell in midwinter (nights lately above nine) may wake her for a while.

WHEN SHE HUNTS. Every night she is awake: she sleeps in the nest by day
and is out by night. The slugs she eats are taken off the slugs' count by
the slugs themselves, who read her nest to know whether she is out (see
creatures/slugs.py): she eats them only on the nights they are out too.
She fattens on mild nights, most of all in late summer and autumn.

HER YOUNG. In June, July or August, if she is heavy enough, she may have a
litter of three to five in the nest. After about four weeks they go out with
her at night, and eat slugs too; after about eight they go their own ways.
One litter a summer at most, and not every summer.

HER NEST is a thing she made: beds/wild-corner/hedgehog-nest (or the most
sheltered bed but the keeper's, if there is no wild corner). It is a few
lines of text:

    leaves: 38                                  how many dead leaves it is made of
    asleep in it: the hedgehog, since 2026-11-20
or
    by day: the hedgehog sleeps here
    by night: she is out
    young: 4, born 2027-07-12, out with her at night

She gathers leaves into it in October and November, on dry nights, and it
thins over the summer. The slugs read it (see creatures/slugs.py): on a night
it says she is out, she hunts, and her young too once they go out with her.

Its drawing (look.py beds/wild-corner/hedgehog-nest) is the nest cut through:
each leaf a leaf, laid in courses into a dome on the ground line, as many as
the file says. Inside, asleep on the ground, whoever is in it at the hour you
look: she (by day, or all winter), her back a low dome of spines and her
snout tucked down, and her young, small ones in a row beside her, while they
are in it. A nest with young in it is drawn as wide as they need. The scale
is in centimetres.

WHAT A VISITOR FINDS. In the almanac, a line when she goes to sleep for the
winter, when she wakes, when she has young, when they go out with her and
when they leave. At an arrival in the night she may be heard snuffling along
a bed; in the morning after a mild wet night her tracks are in the dew; in
winter, now and then, someone remembers she is asleep under the leaves.

Each night she goes a round of up to three beds (the sheltered ones the
likelier), and the round is the night's own, whatever hour someone comes:
in the first hours of the night she is in the first bed of it, after
midnight the second, towards morning the third; and her tracks in the dew
next morning run from the first to the last.
"""

import datetime
import math
import random
import re
import zlib

import hands

NAME = "hedgehog"

NEST = "hedgehog-nest"
WEIGHT = (420, 1250)        # grams, lightest and heaviest
SLEEP_FAT = 600             # she will not go in for the winter lighter than this, unless the cold sends her
LEAVES = (6, 60)
YOUNG_OUT, YOUNG_GONE = 28, 58  # days after birth when the young go out with her, and when they leave
NUMBERS = ("none", "one", "two", "three", "four", "five", "six")


# ------------------------------------------------------------------ reading

def _clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x


def _date(text):
    found = re.search(r"(\d{4})-(\d{2})-(\d{2})", text or "")
    if not found:
        return None
    try:
        return datetime.date(int(found.group(1)), int(found.group(2)), int(found.group(3)))
    except ValueError:
        return None


def _state(text, today) -> dict:
    """Her file as she is. What a hand left that cannot be read is taken in the ordinary way."""
    keys = hands.read_keys(text or "")
    asleep_line = hands.line(keys, "asleep", "no").lower()
    asleep = asleep_line.startswith(("since", "yes")) or bool(_date(asleep_line))
    young_line = hands.line(keys, "young", "none")
    young = int(hands.num(keys, "young", 0, 0, 6)) if re.search(r"\d", young_line) else 0
    born = _date(young_line) if young else None
    if young and (born is None or born > today):
        born = today                                   # a birthday no one can read, or one still to come: today
    litters = sorted({int(y) for y in re.findall(r"\b(\d{4})\b", hands.line(keys, "litters", ""))})[-6:]
    slept = re.search(r"\b(\d{4})\b", hands.line(keys, "slept", ""))
    return {
        "weight": hands.num(keys, "weight", 760, *WEIGHT),
        "asleep": asleep,
        "since": _date(asleep_line) or (today if asleep else None),
        "nights": hands.num(keys, "nights lately", 8.0, -20, 30),
        "young": young,
        "born": born,
        "out": young > 0 and "out" in young_line,
        "litters": litters,
        "slept": int(slept.group(1)) if slept else 0,
    }


def _text(st) -> str:
    lines = ["# The hedgehog of the garden: one, a she. A hand may change any of this; the nights go on from it.",
             "weight: %d g" % round(st["weight"]),
             "asleep: %s" % ("since %s" % st["since"].isoformat() if st["asleep"] and st["since"] else "no"),
             "nights lately: %.1f°" % st["nights"],
             "young: %s" % ("%d, born %s%s" % (st["young"], st["born"].isoformat(), ", out with her" if st["out"] else "")
                            if st["young"] else "none")]
    if st["litters"]:
        lines.append("litters: %s" % ", ".join(str(y) for y in st["litters"]))
    if st["slept"]:
        lines.append("slept: the winter of %d" % st["slept"])
    return "\n".join(lines) + "\n"


def _winter(day) -> int:
    """The winter a day belongs to, named by the year it began in: January 2027 is in the winter of 2026."""
    return day.year if day.month >= 7 else day.year - 1


def _nest_bed(garden) -> str:
    """The wild corner; or, if there is none, the most sheltered bed but the keeper's."""
    beds = [bed for bed in garden.beds() if bed.name != "gate-border"]
    if any(bed.name == "wild-corner" for bed in beds):
        return "wild-corner"
    beds.sort(key=lambda bed: (-bed.shelter, bed.name))
    return beds[0].name if beds else ""


def _nest_of(garden):
    """Her nest as it lies (a thing she made), or None."""
    for thing in garden.things():
        if thing.maker == NAME:
            return thing
    return None


def _nest_text(st, leaves) -> str:
    lines = ["# A hedgehog's nest: dead leaves under the brambles, pressed into a dome. The hedgehog made it.",
             "leaves: %d" % leaves]
    if st["asleep"]:
        lines.append("asleep in it: the hedgehog, since %s" % st["since"].isoformat())
    else:
        lines.append("by day: the hedgehog sleeps here")
        lines.append("by night: she is out")
    if st["young"]:
        where = "out with her at night" if st["out"] else "in the nest"
        lines.append("young: %d, born %s, %s" % (st["young"], st["born"].isoformat(), where))
    return "\n".join(lines) + "\n"


def _young_age(st) -> int:
    return (st["today"] - st["born"]).days if st["young"] and st["born"] else 0


# ------------------------------------------------------------------ the night

def day(garden, ctx):
    today, sky, rng = ctx.date, ctx.sky, ctx.rng
    st = _state(ctx.state, today)
    st["today"] = today
    month = today.month
    st["nights"] += (sky.tmin - st["nights"]) * 0.2
    lines = []

    if st["asleep"]:
        st["weight"] -= 1.5
        spring = month in (3, 4, 5, 6) and st["nights"] > 6.0
        thaw = month in (12, 1, 2) and st["nights"] > 9.0 and rng.random() < 0.2
        if spring or st["weight"] <= 470 or month in (7, 8, 9):
            st["asleep"], st["since"] = False, None
            lines.append("the hedgehog woke from her winter sleep and came out of her nest in the %s"
                         % (_nest_bed(garden) or "garden"))
        elif thaw:
            st["asleep"], st["since"] = False, None
            lines.append("the hedgehog woke in a mild spell and went out at night again")
    else:
        if sky.tmin > 4:                   # a mild night: she finds plenty, most on a wet one; she fattens in autumn
            st["weight"] += (0.8 + 1.6 * _clamp(sky.wet, 0.0, 1.0)) * (1.8 if month in (8, 9, 10) else 1.0)
        else:
            st["weight"] -= 2.0
        if st["young"] and _young_age(st) < YOUNG_GONE:
            st["weight"] -= 1.5            # feeding them
        cold = 4.0 if month == 10 and today.day >= 15 else 5.5 if month in (11, 12, 1, 2) else -99.0
        if (st["nights"] < cold and st["weight"] >= SLEEP_FAT) or (month in (11, 12, 1, 2) and st["nights"] < 1.5):
            st["asleep"], st["since"] = True, today
            if st["slept"] == _winter(today):
                lines.append("the hedgehog went back to sleep in her nest")
            else:
                lines.append("the hedgehog went to sleep for the winter, under the leaves of her nest in the %s"
                             % (_nest_bed(garden) or "garden"))
            st["slept"] = _winter(today)

    # her young
    if not st["asleep"]:
        if (st["young"] == 0 and month in (6, 7, 8) and st["weight"] >= 700 and today.year not in st["litters"]
                and rng.random() < 0.015):
            st["young"], st["born"], st["out"] = rng.randint(3, 5), today, False
            st["litters"] = sorted(set(st["litters"] + [today.year]))[-6:]
            lines.append("the hedgehog had %s young in her nest" % NUMBERS[st["young"]])
        elif st["young"]:
            age = _young_age(st)
            if age >= YOUNG_GONE:
                st["young"], st["born"], st["out"] = 0, None, False
                lines.append("the young hedgehogs went their own ways")
            elif age >= YOUNG_OUT and not st["out"]:
                st["out"] = True
                lines.append("the hedgehog's young went out with her at night for the first time")
    elif st["young"]:
        st["young"], st["born"], st["out"] = 0, None, False    # the young go off before the winter; they do not sleep
        #                                                        with her

    st["weight"] = _clamp(st["weight"], *WEIGHT)
    _keep_nest(garden, st, rng, month, sky)
    ctx.save(_text(st))
    return lines


def _keep_nest(garden, st, rng, month, sky) -> None:
    """Gather leaves in autumn, let the nest thin in summer, and say in it whether she is asleep there."""
    bed = _nest_bed(garden)
    if not bed:
        return
    nest = _nest_of(garden)
    leaves = int(hands.num(hands.read_keys(nest.text), "leaves", 20, *LEAVES)) if nest else 12
    if nest and nest.bed != bed and not garden.unmake(nest.bed, nest.name, "she moved her nest"):
        bed = nest.bed
    if not st["asleep"]:
        if month in (10, 11) and sky.rain < 1 and leaves < 48:
            leaves += rng.randint(1, 4)
        elif month in (5, 6, 7, 8) and rng.random() < 0.06:
            leaves -= 1
    leaves = int(_clamp(leaves, *LEAVES))
    text = _nest_text(st, leaves)
    if nest and nest.bed == bed:
        garden.make(bed, nest.name, text)
    elif not garden.make(bed, NEST, text):
        # Something not hers lies under that name (a hand's file; or her old nest, if the ground's record of
        # what creatures made was lost): she builds under another, two tries a day.
        for n in rng.sample(range(2, 11), 2):
            if garden.make(bed, "%s-%s" % (NEST, hands.roman(n)), text):
                break


# ------------------------------------------------------------------ at the gate

def present(garden, ctx):
    hour = ctx.hour if isinstance(ctx.hour, int) else 12
    st = _state(ctx.state, ctx.date)
    st["today"] = ctx.date
    rng, sky = ctx.rng, ctx.sky
    if st["asleep"]:
        if 9 <= hour <= 16 and rng.random() < 0.25:
            nest = _nest_of(garden)
            return "Under the leaves in the %s the hedgehog is asleep" % (nest.bed if nest else _nest_bed(garden) or "garden")
        return None
    if (hour >= 22 or hour <= 3) and sky.tmin > 4:
        night = ctx.date if hour >= 22 else ctx.date - datetime.timedelta(days=1)
        went = _round(garden, night)
        stage = 0 if hour >= 22 else 1 if hour <= 1 else 2
        where = went[min(stage, len(went) - 1)] if went else "garden"
        if st["young"] and st["out"]:
            return "A hedgehog and her young snuffle along the %s" % where
        return "A hedgehog snuffles along the %s" % where
    if 5 <= hour <= 8 and sky.tmin > 3 and sky.wet > 0.3:
        went = _round(garden, ctx.date - datetime.timedelta(days=1))
        where = "from the %s to the %s" % (went[0], went[-1]) if len(went) > 1 else "in the %s" % (went or ["garden"])[0]
        return "Small tracks cross the dew %s: the hedgehog was out in the night" % where
    return None


def _round(garden, night) -> list:
    """The beds she went along in the night that began on the evening of `night`, in the order she went: up to three.

    The night's own dice choose them, from every bed but the keeper's, the
    sheltered ones the likelier. They are not ctx.rng: at an arrival those
    dice fall anew for each hour, and her round must be the same whatever
    hour someone comes, so that the tracks in the morning lie where she was
    heard in the dark. (They are dice of the date alone, so they replay.)
    """
    beds = sorted((bed for bed in garden.beds() if bed.name != "gate-border"), key=lambda bed: bed.name)
    dice = random.Random("the hedgehog's round|%s" % night.isoformat())
    went = []
    while beds and len(went) < 3:
        weights = [0.3 + (_clamp(bed.shelter, 0.0, 1.0) if bed.shelter == bed.shelter else 0.5) for bed in beds]
        bed = dice.choices(beds, weights)[0]
        beds.remove(bed)
        went.append(bed.name)
    return went


# ------------------------------------------------------------------ the drawing

def draw(text, ctx, pen):
    """Her nest cut through: its leaves in courses, and inside it whoever is in it at this hour. Centimetres."""
    keys = hands.read_keys(text or "")
    leaves = int(hands.num(keys, "leaves", 20, 0, 200))
    asleep = "asleep in it" in keys
    hour = ctx.hour if isinstance(ctx.hour, int) else 12
    by_day = 6 <= hour <= 20
    young_line = hands.line(keys, "young", "")
    young = int(hands.num(keys, "young", 0, 0, 8)) if re.search(r"\d", young_line) else 0
    young_in = young if ("in the nest" in young_line or by_day) else 0
    she_in = asleep or by_day
    pen.unit_name = "cm"
    pen.ground(0)
    # who is in it, side by side on the ground: she (her snout to the left), then her young
    row = []
    if she_in:
        row.append(1.0)
    row += [YOUNG_SIZE] * young_in
    span = sum(_LONG * size for size in row) + 0.6 * max(0, len(row) - 1)
    # the dome: leaves laid in courses along half-ellipses, the outermost course first; a course not filled is
    # spread thin over the whole dome. It is as wide as its leaves make it, or as those asleep in it need.
    width = max(30.0 + 0.4 * leaves, span + 8.0)
    height = max(14.0 + 0.2 * leaves, 0.42 * width)
    placed, course = 0, 0
    while placed < leaves and course < 12:
        a, b = width / 2 - course * 3.2, height - course * 2.6
        if a < 9 or b < 7:
            a, b = 9.0 + (course % 2) * 1.6, 7.0 + (course % 2) * 1.3          # (a nest packed full: courses close in)
        room = max(3, int(math.pi * (a + b) / 2 / 3.6))
        room = min(room, leaves - placed)
        for k in range(room):
            t = math.pi * (k + 0.5) / room
            x, y = a * math.cos(t), b * math.sin(t)
            tilt = t + math.pi / 2 + (zlib.crc32(("%d-%d" % (course, k)).encode()) % 60 - 30) * math.pi / 180
            _leaf(pen, x, y, tilt, 2.4, "brown")
        placed += room
        course += 1
    x = -span / 2
    for size in row:
        _hedgehog(pen, x + _SNOUT * size + _BODY * size, size, "brown")
        x += _LONG * size + 0.6
    if she_in:
        pen.note("the hedgehog is in it, %s" % ("asleep for the winter" if asleep else "asleep for the day"))
    elif not asleep:
        pen.note("%s at this hour: she is out in the night" % ("only her young are in it" if young_in else "empty"))
    if young:
        pen.note("%d young, %s" % (young, "in the nest" if young_in else "out with her"))
    pen.note("%d dead leaves" % leaves)


def _leaf(pen, x, y, angle, length, ink):
    """A leaf: a pointed oval along `angle`, with its midrib."""
    dx, dy = math.cos(angle) * length / 2, math.sin(angle) * length / 2
    nx, ny = -dy * 0.38, dx * 0.38
    pen.polyline([(x - dx, y - dy), (x + nx, y + ny), (x + dx, y + dy), (x - nx, y - ny)], 3, ink, closed=True)
    pen.line(x - dx, y - dy, x + dx, y + dy, 2, ink)


_BODY, _SNOUT = 7.0, 2.4          # a grown hedgehog's half-length, and her snout, in centimetres
_LONG = 2 * _BODY + _SNOUT        # her whole length, asleep
YOUNG_SIZE = 0.4                  # a nestling, as a share of her


def _hedgehog(pen, cx, size, ink):
    """A hedgehog asleep on the ground, seen from the side: her back a low dome of spines, her snout tucked in.

    `size` 1 is a grown one, about fifteen centimetres long; her young are drawn smaller.
    """
    a, b = _BODY * size, 0.8 * _BODY * size
    back = [(cx + a * math.cos(math.pi * k / 24), b * math.sin(math.pi * k / 24)) for k in range(25)]
    pen.polyline(back, 4 if size > 0.6 else 3, ink)
    pen.line(cx - a, 0.0, cx + a, 0.0, 3, ink)
    for row in range(3 if size > 0.6 else 2):                      # the spines, lying back along her
        ra, rb = a * (1.0 - 0.22 * row), b * (1.0 - 0.22 * row)
        count = int(14 * size * (1.0 - 0.2 * row)) + 3
        for k in range(count):
            t = math.pi * (0.06 + 0.8 * (k + 0.5 * (row % 2)) / count)
            x, y = cx + ra * math.cos(t), rb * math.sin(t)
            ex, ey = x + 1.3 * size * math.cos(t - 1.1), y + 1.3 * size * math.sin(t - 1.1)
            floor = 0.2 * size                                     # a spine at her rump lies along the ground,
            if ey < floor:                                         # never into it
                if y <= floor:
                    continue
                cut = (y - floor) / (y - ey)
                ex, ey = x + (ex - x) * cut, floor
            pen.line(x, y, ex, ey, 2, ink)
    nose = (cx - a - _SNOUT * size, 0.9 * size)                    # her face, tucked down at the front
    pen.polyline([(cx - a + 0.4 * size, 2.6 * size), nose, (cx - a + 0.2 * size, 0.2 * size)], 3, ink)
    pen.dot(nose[0], nose[1], 3 if size < 0.6 else 4, "black")
    pen.arc(cx - a - 0.4 * size, 1.9 * size, 0.45 * size, 200, 340, 2, "black")      # an eye, shut
