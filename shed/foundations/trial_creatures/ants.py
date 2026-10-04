"""
Ants: a trial creature, the one that makes something.

It lives in the trials of shed/foundations/: trial_ground.py brings it into a
trial ground that has no creatures of its own, so that the ground's side of
creatures can be tried before the garden has any. It is also a short, honest
example of a creature that makes a thing a visitor can find and look at:
read it before writing the spider or the birds' nest.

Its own file, ground/creatures/ants, says how many there are, where their
hill is, and how high it stands:

    ants: 800
    hill: long-border/anthill
    courses: 5

They keep one anthill, in the sunniest bed but the keeper's own. It is a
file, beds/<bed>/anthill, and a picture in text: the hill in section, one
line to a course, the top course narrowest, each grain of it a ^. On warm
days from spring to autumn they add a course now and then, up to twelve. A
heavy rain (over 12 mm) washes some courses down, or the whole hill flat,
and then they build it again. In winter they are below, and the hill stands
as it was left.

On warm days they hurry the heap along (ants break down what lies on it).
Now and then they carry a fallen seed off to their own bed, as ants do for
the oil on it. And each October the ground round the hill is left a little
richer.

The drawing of the hill (look.py beds/<bed>/anthill) is its courses, a cell
for each grain, standing on the ground line.

At an arrival on a warm day, they are busy on the hill.
"""

import re

NAME = "ants"
FEWEST, MOST = 100, 5000
HILL = "anthill"
COURSES_MOST = 12


def _keys(state) -> dict:
    keys = {}
    for line in (state or "").splitlines():
        key, colon, value = line.partition(":")
        if colon:
            keys[key.strip().lower()] = value.strip()
    return keys


def _number(keys, key, default, lo, hi) -> int:
    found = re.match(r"\d{1,6}", keys.get(key, ""))
    return min(hi, max(lo, int(found.group()))) if found else default


def _hill_bed(garden, keys) -> str:
    """The bed of their hill: where the file says, if that bed is there; else the sunniest bed but the keeper's."""
    beds = {bed.name: bed for bed in garden.beds()}
    said = keys.get("hill", "").rsplit("/", 1)[0]
    if said in beds:
        return said
    open_beds = sorted((bed for bed in beds.values() if bed.name != "gate-border"), key=lambda bed: (-bed.light, bed.name))
    return open_beds[0].name if open_beds else ""


def _hill(courses) -> str:
    """The hill in section, as text: `courses` lines, the top one narrowest."""
    wide = 2 * courses - 1
    return "".join(("^" * (2 * row + 1)).center(wide).rstrip() + "\n" for row in range(courses))


def day(garden, ctx):
    keys = _keys(ctx.state)
    n = _number(keys, "ants", 800, FEWEST, MOST)
    courses = _number(keys, "courses", 0, 0, COURSES_MOST)
    bed = _hill_bed(garden, keys)
    sky, rng, lines = ctx.sky, ctx.rng, []
    if not bed:
        return []
    was = courses
    if sky.rain > 12 and courses:
        courses = 0 if sky.rain > 25 else max(0, courses - rng.randint(1, 3))
        lines.append("the rain washed the anthill in %s %s" % (bed, "flat" if not courses else "down"))
    elif sky.season != "winter" and sky.tmean >= 12 and courses < COURSES_MOST and rng.random() < 0.08 * (1 + n / 2000):
        courses += 1
    if courses != was:
        if courses:
            garden.make(bed, HILL, _hill(courses))
        else:
            garden.unmake(bed, HILL, "washed flat by the rain")
    elif courses:
        garden.make(bed, HILL, _hill(courses))       # (as it stands: made again, nothing changes)
    if sky.tmean >= 12:
        garden.heap_pace(1.3)
        n += int(n * 0.025 * (1 - n / MOST))           # a warm day: the nest grows, less as it fills
    elif sky.tmean < 4:
        n -= n // 30
    if ctx.date.month == 10 and ctx.date.day == 1 and courses:
        garden.enrich(bed, 0.3, "the anthill's leavings")
    n = min(MOST, max(FEWEST, n))
    ctx.save("ants: %d\nhill: %s/%s\ncourses: %d\n" % (n, bed, HILL, courses))
    return lines


def after(garden, ctx, seeds):
    """Now and then a fallen seed is carried off to their own bed."""
    keys = _keys(ctx.state)
    bed = _hill_bed(garden, keys)
    if not bed or ctx.sky.tmean < 10:
        return []
    for seed in list(seeds):
        if getattr(seed, "bed", "") != bed and ctx.rng.random() < 0.08:
            garden.carry(seed, bed, "for the oil on it")
    return []


def draw(text, ctx, pen):
    """The hill in section: a cell for each grain, course on course, on the ground line."""
    rows = [line for line in str(text or "").splitlines() if "^" in line]
    pen.unit_name = "grain, grains"
    pen.ground(0)
    for height, line in enumerate(reversed(rows)):
        for across, mark in enumerate(line):
            if mark == "^":
                pen.cell(across, height, 0.9, 0.9, "brown")
    pen.note("%d course%s of the anthill" % (len(rows), "" if len(rows) == 1 else "s"))


def present(garden, ctx):
    keys = _keys(ctx.state)
    if not (10 <= (ctx.hour or 0) <= 17 and ctx.sky.tmean >= 12 and _number(keys, "courses", 0, 0, COURSES_MOST)):
        return None
    return "Ants are busy on their hill in the %s" % keys.get("hill", "").rsplit("/", 1)[0]
