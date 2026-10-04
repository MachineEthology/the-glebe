"""
The robin: on winter mornings it is there when someone comes through the gate.

One robin holds the garden. It sings nearly all the year round, and all
winter, when almost nothing else does. Its own file,
ground/creatures/robin, says so, and the day its autumn song began:

    robin: 1
    autumn song: began 2027-08-24

Hands may change the file; the robin does not mind.

It does nothing in the days that the ground keeps: it is met, not found.
The almanac hears of it once a year, on the day in late summer when it
begins its autumn song (the first fair, cooler day after the middle of
August).

At an arrival on a winter morning (December to February, and on cold
mornings in November and March, from six until eleven) it is there. Where:
on the gate post, on the north wall, on the stone table, on the rim of the
heap, or on the stake of a plant in the keeper's border, wherever those are
in this garden; and if a hand has planted something in the last three days
(and no snow lies over it), on the fresh earth beside it, since digging turns
up food. The weather is in the line too: frost, snow, fog, rain.
"""

import datetime
import re

import hands

NAME = "robin"
KEEPERS_BED = "gate-border"
MORNING = range(6, 12)                      # the hours of a morning, as an arrival counts them


def _song_began(state):
    found = re.search(r"autumn song\s*:\s*began\s+(\d{4}-\d{2}-\d{2})", state or "")
    if not found:
        return None
    try:
        return datetime.date.fromisoformat(found.group(1))
    except ValueError:
        return None


def _own_file(began) -> str:
    return ("# The robin: one robin holds the garden. It sings all winter, and on winter mornings it is there\n"
            "# when someone comes through the gate.\n"
            "robin: 1\n"
            "autumn song: %s\n" % ("began %s" % began.isoformat() if began else "not yet this year"))


def day(garden, ctx):
    began = _song_began(ctx.state)
    today, sky = ctx.date, ctx.sky
    lines = []
    if today.month == 8 and today.day >= 15 and (began is None or began.year != today.year):
        if sky.tmin < 12 and sky.rain < 1:
            began = today
            lines.append("robin: began its autumn song")
    ctx.save(_own_file(began))
    return lines


def _wintry(ctx) -> bool:
    sky, month = ctx.sky, ctx.date.month
    return sky.season == "winter" or (month == 11 and sky.tmin < 4) or (month == 3 and sky.tmin < 2)


def _perches(garden, ctx) -> list:
    """Where the robin may be this morning, among the things this garden really has."""
    perches = ["the gate post"]
    beds = garden.beds()
    if any(bed.name == "north-wall" or "north wall" in str(bed.lies).lower() for bed in beds):
        perches.append("the north wall")
    if any("stone table" in str(bed.lies).lower() for bed in beds):
        perches.append("the stone table")
    try:
        heap = any(str(where).startswith("compost/") for where, _ in ctx.soil.texts())
    except Exception:
        heap = False
    if heap:
        perches.append("the rim of the heap")
    stakes = sorted(plant.where for plant in garden.plants(bed=KEEPERS_BED) if not plant.dead)
    if stakes:
        perches.append("the stake of %s" % stakes[ctx.rng.randrange(len(stakes))])
    return perches


def present(garden, ctx):
    if ctx.hour not in MORNING or not _wintry(ctx):
        return None
    sky, rng = ctx.sky, ctx.rng
    dug = sorted(plant.where for plant in garden.plants()
                 if not plant.dead and plant.age <= 3 and str(plant.by or "") not in ("", "the days"))
    if dug and not sky.snow and rng.random() < 0.6:
        return "A robin is on the fresh earth beside %s" % dug[rng.randrange(len(dug))]
    perch = rng.choice(_perches(garden, ctx))
    words = sky.words if isinstance(getattr(sky, "words", ""), str) else ""
    if sky.snow:
        return "A robin waits on %s; its tracks cross the snow" % perch
    if words.startswith("fog"):
        return "A robin sings somewhere near the gate, in the fog"
    if sky.frost:
        return "A robin sings from %s, round against the frost" % perch
    if sky.rain >= 2:
        return "A robin sings from %s in the rain" % perch
    return "A robin sings from %s" % perch
