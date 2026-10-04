"""
The thrush: a song thrush, who takes snails by day and breaks them on a stone.

Her one job is to eat snails, and the snail she eats leaves its shell behind:
she carries it to a flat stone in the stones bed, her anvil, and beats it
against the stone until it breaks. The broken shells lie round the stone.

HER FILE, ground/creatures/thrush, says:

    anvil: stones/anvil              where her anvil is (a thing she made)
    shells this year: 23             how many she has broken since January
    sang: 2026-11-28                 the day she first sang this winter

A hand may change any of it. The days go on from what they find.

WHEN SHE GOES TO THE ANVIL. Any day of the year, but most of all when the
worms are hard to get: in a dry spell, when they have gone deep, and on a
frosty day, when the ground is hard. In spring and early summer she has young
to feed and takes more. On an ordinary day there is about one chance in
twelve that she breaks a shell (one in five in a dry spell), and now and then
she breaks two. Each shell is a
snail taken from the garden: the slugs' file counts the snails, and the
slugs, reading her anvil, take each shell dated the day before off it (see
creatures/slugs.py).

HER ANVIL is a thing she made: beds/stones/anvil (or, with no stones bed,
in the driest bed but the keeper's). It is one line saying what it is, and
then one line for each shell that lies there:

    2026-10-04  a banded snail: yellow, with five dark bands
    2026-10-09  a garden snail: brown, mottled

The newest are at the bottom. Old shells crumble and blow away: a shell lies
about four months, and the anvil never holds more than forty. A hand may add
a shell, or sweep them all off; a hand that sweeps the stone takes nothing
from the snails.

Its drawing (look.py beds/stones/anvil) is the stone seen from above, with the
broken shells round it where she beat them: each shell in two to four pieces,
in its own colour, with its dark bands; the older a shell, the paler (the
sun bleaches them). The scale is in centimetres.

HER SONG. From late autumn into July she sings at dawn and dusk, each phrase
over twice or three times. The almanac says when she first sings in a
winter. At an arrival at dawn or dusk in her season she may be heard; on a
day she broke a shell, at an arrival in the daylight, the tapping is heard
from the stones.
"""

import datetime
import math
import re
import zlib

import hands

NAME = "thrush"

ANVIL = "anvil"
SHELLS_MOST = 40
SHELL_DAYS = 120            # about how long a broken shell lies before it has crumbled and blown away
HEAD = "the thrush's anvil: a flat stone among the stones, where she breaks the shells of snails"

# what she finds: the snail, its colour (an ink), and its bands (how many dark ones)
SNAILS = (("a banded snail: yellow, with five dark bands", "#d6a91c", 5),
          ("a banded snail: yellow, with no bands", "#d6a91c", 0),
          ("a banded snail: yellow, with one dark band", "#d6a91c", 1),
          ("a banded snail: pink, with five dark bands", "#d9768c", 5),
          ("a banded snail: pink, with no bands", "#d9768c", 0),
          ("a banded snail: brown, with one dark band", "#8a5a2b", 1),
          ("a garden snail: brown, mottled", "#7a5530", -1),
          ("a garden snail: brown, mottled", "#7a5530", -1),
          ("a garden snail: brown, mottled", "#7a5530", -1),
          ("a small strawberry snail: red-brown", "#9a4a3a", 0))
COLOURS = {"yellow": "#d6a91c", "pink": "#d9768c", "red-brown": "#9a4a3a", "brown": "#8a5a2b", "white": "#d8d2c0"}
_SHELL = re.compile(r"^(\d{4}-\d{2}-\d{2})\s+(.*\S)?\s*$")
_BAND_COUNT = re.compile(r"\b(one|two|three|four|five|\d)\b")


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


def _state(text) -> dict:
    keys = hands.read_keys(text or "")
    year = re.search(r"\b(\d{4})\b", hands.line(keys, "year", ""))
    return {
        "anvil": hands.line(keys, "anvil", ""),
        "count": int(hands.num(keys, "shells this year", 0, 0, 10_000)),
        "year": int(year.group(1)) if year else 0,
        "sang": _date(hands.line(keys, "sang", "")),
        "busy": _date(hands.line(keys, "busy", "")),
    }


def _text(st, today) -> str:
    lines = ["# The song thrush of the garden, and the stone she uses as an anvil. A hand may change any of this.",
             "anvil: %s" % (st["anvil"] or "none yet"),
             "shells this year: %d" % st["count"],
             "year: %d" % today.year]
    if st["sang"]:
        lines.append("sang: %s" % st["sang"].isoformat())
    if st["busy"]:
        lines.append("busy: %s" % st["busy"].isoformat())
    return "\n".join(lines) + "\n"


def _shells(text) -> list:
    """The shells lying on the anvil: [(date, words)], oldest first. Lines that are not shells are passed over."""
    found = []
    for line in (text or "").splitlines():
        match = _SHELL.match(line.strip())
        if match:
            day = _date(match.group(1))
            if day is not None:
                found.append((day, (match.group(2) or "a snail's shell")[:120]))
    return found


def _anvil_bed(garden) -> str:
    """The stones; or, without them, the driest bed but the keeper's."""
    beds = [bed for bed in garden.beds() if bed.name != "gate-border"]
    if any(bed.name == "stones" for bed in beds):
        return "stones"
    beds.sort(key=lambda bed: (bed.water, -bed.light, bed.name))
    return beds[0].name if beds else ""


def _anvil(garden):
    for thing in garden.things():
        if thing.maker == NAME:
            return thing
    return None


# ------------------------------------------------------------------ the day

def day(garden, ctx):
    today, sky, rng = ctx.date, ctx.sky, ctx.rng
    st = _state(ctx.state)
    if st["year"] != today.year:
        st["count"] = 0
    lines = []

    anvil = _anvil(garden)
    shells = _shells(anvil.text) if anvil else []
    kept = [(d, w) for d, w in shells if (today - d).days <= SHELL_DAYS + (zlib.crc32(w.encode() + d.isoformat().encode()) % 30)]
    if sky.wind >= 8 and kept:                         # a gale blows some of the pieces off the stone
        kept = kept[rng.randint(1, 3):]

    hunt = 0.08
    if sky.wet < 0.15:
        hunt *= 2.5                                    # dry: the worms have gone deep
    if sky.tmin < 0:
        hunt *= 1.8                                    # frost: the ground is hard
    if today.month in (4, 5, 6, 7):
        hunt *= 1.4                                    # young in the nest
    broken = 0
    roll = rng.random()
    if roll < hunt:
        broken = 2 if roll < hunt * 0.15 else 1
    for _ in range(broken):
        kept.append((today, SNAILS[rng.randrange(len(SNAILS))][0]))
    kept = kept[-SHELLS_MOST:]
    st["count"] += broken

    if broken or kept != shells:
        bed = anvil.bed if anvil else _anvil_bed(garden)
        name = anvil.name if anvil else ANVIL
        text = HEAD + "\n" + "".join("%s  %s\n" % (d.isoformat(), w) for d, w in kept)
        if bed and (anvil or broken):
            made = garden.make(bed, name, text)
            if not made and not anvil:
                # Something not hers lies under that name (a hand's file; or her old anvil, if the ground's record
                # of what creatures made was lost): she takes another stone, two tries a day.
                for n in rng.sample(range(2, 11), 2):
                    name = "%s-%s" % (ANVIL, hands.roman(n))
                    made = garden.make(bed, name, text)
                    if made:
                        break
            if made:
                st["anvil"] = "%s/%s" % (bed, name)

    # a run at the anvil, told once in a while
    lately = sum(1 for d, _ in kept if (today - d).days < 7)
    if lately >= 5 and (st["busy"] is None or (today - st["busy"]).days > 90):
        st["busy"] = today
        why = "frost" if sky.tmin < 0 else "dry weather" if sky.wet < 0.15 else "wet"
        if why == "wet":
            lines.append("the shells piled up round the thrush's anvil, a snail a day")
        else:
            lines.append("the shells piled up round the thrush's anvil in the %s" % why)

    # her first song of the season
    early = (today.month, today.day) >= (11, 15) or today.month <= 3
    if early and (st["sang"] is None or _song_season(st["sang"]) != _song_season(today)):
        if sky.tmax > 7 and sky.wind < 4 and sky.rain < 2 and rng.random() < 0.25:
            st["sang"] = today
            lines.append("the thrush, each phrase twice over, sang for the first time this %s"
                         % ("winter" if today.month in (11, 12, 1, 2) else "spring"))

    ctx.save(_text(st, today))
    return lines


def _season_of_song(day) -> bool:
    """From mid-November into mid-July."""
    return (day.month, day.day) >= (11, 15) or day.month <= 6 or (day.month == 7 and day.day <= 15)


def _song_season(day) -> int:
    """Which season of song a day is in, named by the year it began: March 2027 is in the season of 2026."""
    return day.year if (day.month, day.day) >= (11, 15) else day.year - 1


# ------------------------------------------------------------------ at the gate

def present(garden, ctx):
    hour = ctx.hour if isinstance(ctx.hour, int) else 12
    today, sky, rng = ctx.date, ctx.sky, ctx.rng
    anvil = _anvil(garden)
    if anvil and 9 <= hour <= 17 and any(d == today for d, _ in _shells(anvil.text)):
        return "Tap, tap, tap: a thrush is breaking a snail on a stone in the %s" % anvil.bed
    if _season_of_song(today) and (5 <= hour <= 7 or 18 <= hour <= 20) and sky.rain < 3 and rng.random() < 0.5:
        st = _state(ctx.state)
        if st["sang"] is not None and _song_season(st["sang"]) == _song_season(today):
            return "A thrush is singing, each phrase over twice"
    return None


# ------------------------------------------------------------------ the drawing

def draw(text, ctx, pen):
    """The anvil from above: the flat stone, and round it the broken shells, each in its own colour. Centimetres."""
    today = ctx.date
    shells = _shells(text)
    pen.unit_name = "cm"
    pen.align = "center"
    # the stone: a flat, roughly oval slab, the same every time it is drawn
    stone = []
    for k in range(14):
        t = 2 * math.pi * k / 14
        wobble = 1.0 + ((zlib.crc32(b"anvil-%d" % k) % 100) - 50) / 400.0
        stone.append((15.0 * wobble * math.cos(t), 10.5 * wobble * math.sin(t)))
    pen.polyline(stone, 5, "grey", closed=True)
    for index, (day, words) in enumerate(shells):
        _broken_shell(pen, index, day, words, today)
    if shells:
        pen.note("%d broken shell%s; the newest broken on %s" % (len(shells), "" if len(shells) == 1 else "s",
                                                                shells[-1][0].isoformat()))
    else:
        pen.note("no shells on it just now")
    pen.note("each shell in its own colour; the older, the paler")


def _look_of(words):
    """A shell's colour and its dark bands, as its line says."""
    words = words.lower()
    colour = next((ink for name, ink in sorted(COLOURS.items(), key=lambda item: -len(item[0])) if name in words),
                  "#8a5a2b")
    if "mottled" in words:
        return colour, -1
    if "no band" in words:
        return colour, 0
    found = None
    for part in words.split(","):           # a number, and after it in the same part of the line, 'band': each part is
        first = _BAND_COUNT.search(part)    # gone over once (a pattern going on to 'band' from every number in a long
        if first and "band" in part[first.end():]:     # line would go over the rest of it again from each)
            found = first
            break
    count = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}.get(found.group(1), None) if found else 0
    if count is None:
        count = int(found.group(1))
    return colour, min(5, count)


def _broken_shell(pen, index, day, words, today):
    """One shell beaten on the stone: its whorl, a spiral, broken into two to four pieces flung a little apart.

    Where it lies round the stone, and how it broke, come from its own line,
    so it is drawn the same each time it is looked at. Its bands run along
    the outer turn of the whorl; a mottled shell has dark flecks there.
    """
    colour, bands = _look_of(words)
    age = max(0, (today - day).days) if today else 0
    pale = _clamp(age / 160.0, 0.0, 0.7)
    colour = hands.mix(colour, "#fbf8f1", pale)
    band_ink = hands.mix("#3a2418", "#fbf8f1", pale)
    seed = zlib.crc32(("%s|%s|%d" % (day.isoformat(), words, index)).encode())
    angle = (seed % 360) * math.pi / 180
    reach = 16.0 + (seed >> 9) % 60 / 10.0                 # how far from the stone's middle it lies
    cx, cy = reach * math.cos(angle) * 1.02, reach * math.sin(angle) * 0.78
    turn0 = (seed >> 13) % 360 * math.pi / 180             # how the shell lay
    whorl = 2.4 * 2 * math.pi                              # two turns and a bit
    grow = math.log(1.25 / 0.12) / whorl                   # from 0.12 cm at the tip to 1.25 cm at the mouth

    def at(theta, shrink=1.0):
        r = 1.25 * shrink * math.exp(-grow * (whorl - theta))
        return r * math.cos(theta + turn0), r * math.sin(theta + turn0)

    pieces = 2 + (seed >> 17) % 3
    cuts = sorted([0.0, whorl] + [whorl * (0.25 + 0.6 * ((seed >> (5 * k + 3)) % 100) / 100.0) for k in range(pieces - 1)])
    for k in range(len(cuts) - 1):
        a, b = cuts[k] + 0.12, cuts[k + 1] - 0.12
        if b - a < 0.3:
            continue
        mid = (a + b) / 2
        mx, my = at(mid)
        norm = math.hypot(mx, my) or 1.0
        drift = 0.25 + 0.2 * k
        ox, oy = cx + mx / norm * drift, cy + my / norm * drift
        steps = max(3, int((b - a) / 0.25))
        line = [(ox + x, oy + y) for x, y in (at(a + (b - a) * s / steps) for s in range(steps + 1))]
        pen.polyline(line, 4, colour)
        outer = max(a, whorl - 2 * math.pi)
        if b - outer < 0.3:
            continue
        steps = max(3, int((b - outer) / 0.25))
        if bands > 0:
            for n in range(min(bands, 3)):
                shrink = 0.86 - 0.14 * n
                pen.polyline([(ox + x, oy + y) for x, y in (at(outer + (b - outer) * s / steps, shrink)
                                                            for s in range(steps + 1))], 2, band_ink)
        elif bands < 0:
            for s in range(0, steps + 1, 2):
                x, y = at(outer + (b - outer) * s / steps, 0.8)
                pen.dot(ox + x, oy + y, 3, band_ink)
