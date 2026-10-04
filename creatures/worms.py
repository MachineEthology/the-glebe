"""
Worms: the earthworms under the beds and in the heap.

Their one job is to set how fast the heap rots: quicker when it is warm and
wet, slowly in the cold and the dry, and not at all in a frost. What lies on
the heap (compost/) rots into the humus once it has had sixty days' worth of
rotting; the worms say how many days' worth each real day is.

THEIR FILE, ground/creatures/worms, says:

    worms: 1400          how many, about, in the heap and the beds round it
    pace: 1.2            how fast the heap rotted on the last day lived (1 is a day's rotting in a day)
    dry days: 4          how many days the drought has lasted, if there is one
    deep: 2026-12-03     the last time the frost sent them down (the almanac is told once a winter)
    dry: 2027-07-30      the last time a drought sent them deep (told once a summer)
    back: 2027-03-04     the last spring day they were back at the heap (told once a year)

A hand may change the number; the days go on from it.

THE PACE. In a frost (a night below nothing) they are down out of reach and
the heap does not rot at all that day. Otherwise the pace rises with the
warmth of the day (slowly in the cold, for a heap is warmer than the air;
fully at about seventeen degrees) and with the wet of the last fortnight. In
a drought (a hot day after a dry fortnight) they go deep and the heap barely
rots. More worms work faster, fewer slower: from about half the pace to a
third again more. So in a mild wet autumn a letter left on the heap is humus
in six weeks, and one left in December may lie until March.

THEIR NUMBERS. They breed in the mild wet months, fewer as they fill the
ground (and the heap, while it has much on it, feeds more of them); drought
and hard frost thin them. Never fewer than 300, nor more than 3,000.

WHAT A VISITOR FINDS. In the almanac, once a winter, the day the frost sends
them down and the heap stops; once a summer, if a drought of ten days or
more sends them deep; once a year, the spring day they are back at the
heap. At an arrival on a mild wet night they lie out on the paths.
"""

import datetime
import re

import hands

NAME = "worms"

WORMS = (300, 3000)
TYPICAL = 1200


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


def _state(text) -> dict:
    keys = hands.read_keys(text or "")
    return {
        "worms": hands.num(keys, "worms", TYPICAL, *WORMS),
        "pace": hands.num(keys, "pace", 1.0, 0.0, 2.0),
        "deep": _date(hands.line(keys, "deep", "")),
        "dry": _date(hands.line(keys, "dry", "")),
        "dry days": int(hands.num(keys, "dry days", 0, 0, 1000)),
        "back": _date(hands.line(keys, "back", "")),
    }


def _text(st) -> str:
    lines = ["# The earthworms of the garden, under the beds and in the heap. A hand may change the number.",
             "worms: %d" % round(st["worms"]),
             "pace: %.2f" % st["pace"]]
    if st["dry days"]:
        lines.append("dry days: %d" % st["dry days"])
    for key in ("deep", "dry", "back"):
        if st[key]:
            lines.append("%s: %s" % (key, st[key].isoformat()))
    return "\n".join(lines) + "\n"


def pace(sky, worms) -> float:
    """How fast the heap rots under this sky with this many worms: 0 in a frost, up to 2."""
    if sky.tmin < 0:
        return 0.0
    warmth = _clamp(0.15 + (sky.tmean - 2.0) / 12.0, 0.1, 1.25)     # a heap is warmer than the air: they work in the cool
    moist = _clamp(0.35 + 1.3 * sky.wet, 0.3, 1.1)
    if _drought(sky):
        moist = 0.2                                    # they have gone deep
    vigour = _clamp((worms / TYPICAL) ** 0.5, 0.55, 1.35)
    return round(_clamp(1.7 * warmth * moist * vigour, 0.0, 2.0), 2)


def _drought(sky) -> bool:
    return sky.wet < 0.1 and sky.tmax > 22


def _heap_food(ctx) -> int:
    """How many texts lie on the heap waiting to rot: the more there are, the more worms it feeds."""
    try:
        return sum(1 for where, _ in ctx.soil.texts()
                   if where.startswith("compost/") and where not in ("compost/humus", "compost/.heap"))
    except Exception:
        return 0


def day(garden, ctx):
    today, sky = ctx.date, ctx.sky
    st = _state(ctx.state)
    lines = []
    st["pace"] = pace(sky, st["worms"])
    garden.heap_pace(st["pace"])

    # their numbers
    room = _clamp(2400 + 40 * min(_heap_food(ctx), 15), 0, WORMS[1])
    n = st["worms"]
    if sky.tmin >= 0 and sky.tmean > 5 and sky.wet > 0.25:
        n += n * 0.02 * _clamp(sky.wet, 0.0, 1.0) * max(0.0, 1.0 - n / room)
    st["dry days"] = st["dry days"] + 1 if _drought(sky) else 0
    if _drought(sky):
        n -= n * 0.004
    if sky.tmin < -4:
        n -= n * 0.006
    n -= n * 0.0008
    st["worms"] = _clamp(n, *WORMS)

    # what the almanac is told, rarely
    winter = today.year if today.month >= 7 else today.year - 1
    if sky.tmin < 0 and (st["deep"] is None or (st["deep"].year if st["deep"].month >= 7 else st["deep"].year - 1) != winter):
        st["deep"] = today
        lines.append("the worms went down for the frost, and the heap lay still")
    elif st["dry days"] >= 10 and (st["dry"] is None or st["dry"].year != today.year):
        st["dry"] = today
        lines.append("the drought sent the worms deep, and the heap slowed")
    elif (today.month in (3, 4) and st["pace"] >= 0.6 and st["deep"] is not None
          and (st["back"] is None or st["back"].year != today.year)):
        st["back"] = today
        lines.append("the worms came back to work in the heap")
    ctx.save(_text(st))
    return lines


def present(garden, ctx):
    hour = ctx.hour if isinstance(ctx.hour, int) else 12
    sky = ctx.sky
    if (hour >= 22 or hour <= 4) and sky.tmin > 5 and (sky.rain > 3 or sky.wet > 0.6) and ctx.rng.random() < 0.5:
        return "Worms lie out on the wet path, and draw back at a step"
    return None
