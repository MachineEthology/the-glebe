"""
The mole: one, under the beds, seldom seen.

Its one job is to dig. Now and then it pushes up a molehill in a bed, and the
earth it brings up comes from deep down, where the heap's humus has gone:
so a molehill is the one place in the beds where lines from the heap come
back to the surface. A plant that stands where the hill comes up is shifted
a little.

ITS FILE, ground/creatures/mole, says:

    hills: 7                            how many molehills it has pushed up, in all
    last: 2026-11-03, long-border       the last one, and where

A hand may change it; the mole goes on from it.

WHEN. All year, but most from October to March, when the ground is soft and
wet, and after rain; seldom in a dry summer, and never when the ground is
frozen hard. About eight or ten hills a year, and never more than three
standing at once.

WHERE. In the beds with ordinary ground: not in the dry stones, seldom at
the sodden pond's edge, and never in the keeper's own border by the gate.
The hill comes up at a place in the bed; the nearest plant within reach of
it that is still shallow-rooted is pushed a little way off, and its rings
say so ("shifted a little by mole"). Shallow-rooted means in its first
year; a tree, a shrub or anything woody only in its first four months. The
younger it is, the farther it goes: a seedling a few hundredths of the bed,
a plant near the end of its first year a third of that. Whatever has rooted
deeper stays where it stands, and the hill comes up beside it.

THE ALMANAC has one line for each new hill. Most often it is the mole's own:

    a molehill with three lines of the humus in it came up in the orchard

When the hill shifted a plant, the one line is the plant's instead (it is
in the plant's rings too), and it carries the rest:

    orchard/wader: shifted a little by mole (a molehill came up beside it, with three lines of the humus in it)

A MOLEHILL is a thing the mole made: beds/<bed>/molehill (molehill-ii, and
so on, if there is more than one in a bed). It is a few lines of text: one
saying when and where it came up, then the lines from the humus the earth
brought with it, indented. In a new garden, whose heap has not yet rotted
into humus, a hill is only earth.

Rain washes a hill down. Each day of heavy rain (eight millimetres or more)
the top line is washed away, and the hill keeps count of what the rain took
in a line of its own, so that what it holds and what it came up with still
agree:

    washed off by the rain since: 2 lines, the last on 2026-12-12

A hill that has lost all its lines is flattened by the next heavy rain, and
one that has stood half a year is grassed over.
Either way the mole takes it away, and its lines are gone back into the
ground. A hand may rake one flat at any time (take the file away), or read
it first.

Its drawing (look.py beds/<bed>/molehill) is the hill cut through: a heap
of loose earth on the ground line, one crumb for every ten letters it holds
(and a dozen for the earth itself), and across it, course by course from
the top, the lines it brought up, lettered as far as the heap is wide. The
crumbs lie between the lines, never on them. A hill with more than eight
lines (a hand may pile more on) letters the top eight and says so. Its
caption counts the lines it holds, and the ones the rain has washed off it.
The scale is in centimetres.

At an arrival in the daylight on the day a hill came up, its earth is fresh.
"""

import datetime
import math
import re
import zlib

import hands

NAME = "mole"

HILL = "molehill"
STANDING_MOST = 3
LINES = (3, 6)              # how many lines of humus a hill brings up, fewest and most
LINE_MOST = 300             # characters kept of each line
WASH_MM = 8.0               # a day's rain that washes a hill down a line
GRASSED = 180               # days after which a hill is grassed over
REACH = 0.3                 # how far from the hill (in the bed's own measure, 0..1) a plant can be shifted
ROOTED = 365                # days after which a plant has rooted too deep for a molehill to shift it
WOODY_ROOTED = 120          # ... and for a tree, a shrub, a woody climber or a woody stem, sooner
WOODY = (("growth", ("woody",)), ("habit", ("tree", "shrub", "climber")), ("stem", ("woody",)))
HEAD = re.compile(r"(\d{4}-\d{2}-\d{2})")

# the drawing
PX_CM = 9.0                 # pixels to a centimetre: a hill of COURSES_DRAWN courses or fewer is always drawn at this
COURSES_DRAWN = 8           # the most lines a drawing letters
LETTER_CM = 1.3             # how tall the lettering stands, in centimetres at that scale
MOUND = 1.4                 # the heap's shape: its height across it is (1 - u^2) ** MOUND (higher: lower flanks)
TOP_COURSE = 0.7            # the highest line's foot, as a share of the heap's height
BASE_COURSE = 1.8           # the lowest line's foot, in centimetres above the ground
COURSE_APART = 3.6          # the most room between one line's foot and the next, in centimetres


def _clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x


def _date(text):
    found = HEAD.search(text or "")
    if not found:
        return None
    try:
        return datetime.date.fromisoformat(found.group(1))
    except ValueError:
        return None


def _state(text) -> dict:
    keys = hands.read_keys(text or "")
    return {"hills": int(hands.num(keys, "hills", 0, 0, 100_000)), "last": hands.line(keys, "last", "")}


def _text(st) -> str:
    lines = ["# The mole of the garden: one, under the beds, seldom seen. A hand may change this.",
             "hills: %d" % st["hills"]]
    if st["last"]:
        lines.append("last: %s" % st["last"])
    return "\n".join(lines) + "\n"


def _hill_text(day, bed, at, lines) -> str:
    head = "a molehill, pushed up in the night of %s, at %.2f,%.2f in the %s" % (day.isoformat(), at[0], at[1], bed)
    if not lines:
        return head + "\nonly earth: the heap has not yet rotted into anything\n"
    return head + "\nthe earth came up from the humus, and brought with it:\n" + "".join("    %s\n" % l for l in lines)


def _hill_lines(text) -> list:
    """The humus lines a hill holds: its indented lines."""
    return [line.strip() for line in (text or "").splitlines() if line.startswith((" ", "\t")) and line.strip()]


# (The space before it is looked for on its own line only: from the start of every line, `\s*` would go over all
# the empty lines after it again, and a hill a hand filled with empty lines would keep its day past its time.)
WASHED = re.compile(r"^[^\S\n]*washed off by the rain since\s*:\s*(\d{1,5})", re.I | re.M)


def _washed(text) -> int:
    """How many lines the rain has washed off a hill since it came up, as its own line says (0 if it says nothing).

    (Added after the rehearsal of October 2026, where an Opus found a hill's ring saying 'five lines' and its plate
    '3 lines': the rain had taken two, and nothing said so.)"""
    found = WASHED.search(text or "")
    return int(found.group(1)) if found else 0


def _washed_line(n, day) -> str:
    return "washed off by the rain since: %d line%s, the last on %s\n" % (n, "" if n == 1 else "s", day.isoformat())


def _liking(bed) -> float:
    """How good a bed's ground is for digging: ordinary ground best; dry stones and the sodden pond's edge least."""
    if bed.name == "gate-border":
        return 0.0
    return max(0.0, math.exp(-((bed.water - 1.0) / 0.35) ** 2))


def day(garden, ctx):
    today, sky, rng = ctx.date, ctx.sky, ctx.rng
    st = _state(ctx.state)
    lines = []
    hills = [thing for thing in garden.things() if thing.maker == NAME]

    # the rain on the hills already standing
    standing = []
    for hill in hills:
        made = _date(hill.text) or hill.made
        held = _hill_lines(hill.text)
        if made is not None and (today - made).days >= GRASSED:
            garden.unmake(hill.bed, hill.name, "grassed over")
            continue
        if sky.rain >= WASH_MM:
            if not held:
                garden.unmake(hill.bed, hill.name, "washed flat by the rain")
                continue
            kept = held[1:]
            text = hill.text.split("\n", 1)[0] + "\n"
            text += ("the earth came up from the humus, and brought with it:\n" + "".join("    %s\n" % l for l in kept)
                     if kept else "washed down by the rain: only earth is left\n")
            text += _washed_line(_washed(hill.text) + 1, today)
            garden.make(hill.bed, hill.name, text)
        standing.append(hill)

    # a new hill, now and then
    chance = 0.035 if today.month in (10, 11, 12, 1, 2, 3) else 0.012
    if sky.rain > 4:
        chance *= 1.5
    if sky.wet < 0.12:
        chance *= 0.3
    if sky.tmin < -3:
        chance = 0.0                                   # the ground is frozen hard
    if len(standing) < STANDING_MOST and rng.random() < chance:
        bed, held, shifted = _push_up(garden, ctx)
        if bed:
            st["hills"] += 1
            st["last"] = "%s, %s" % (today.isoformat(), bed)
            if not shifted:                            # a shifted plant's own line has said it all (see _shift_nearest)
                lines.append("a molehill%s came up in the %s" % (
                    " with %s of the humus in it" % _counted(held) if held else "", bed))
    ctx.save(_text(st))
    return lines


COUNTED = {1: "a line", 2: "two lines", 3: "three lines", 4: "four lines", 5: "five lines", 6: "six lines"}


def _counted(held) -> str:
    """How many lines of the humus a hill holds, in words: 'three lines'."""
    return COUNTED.get(held, "%d lines" % held)


def _push_up(garden, ctx):
    """Push up one molehill. Returns (its bed, how many lines of humus it holds, whether it shifted a plant),
    or ("", 0, False) if none came up."""
    rng, today = ctx.rng, ctx.date
    beds = [bed for bed in garden.beds() if _liking(bed) > 0.2]
    if not beds:
        return "", 0, False
    bed = rng.choices(beds, [_liking(bed) for bed in beds])[0].name
    at = (round(rng.uniform(0.1, 0.9), 2), round(rng.uniform(0.1, 0.9), 2))
    taken = {thing.name for thing in garden.things(bed)}
    names = [n for n in [HILL] + ["%s-%s" % (HILL, hands.roman(n)) for n in range(2, 12)] if n not in taken]
    if not names:
        return "", 0, False
    # The first free name; and if a hand's own file lies under it (or an old hill of its own, if the ground's record
    # of what creatures made was lost), two tries at others.
    tries = names[:1] + (rng.sample(names[1:], min(2, len(names) - 1)) if len(names) > 1 else [])
    humus = _humus(ctx, rng)
    text = _hill_text(today, bed, at, humus)
    if not any(garden.make(bed, name, text) for name in tries):
        return "", 0, False
    why = "a molehill came up beside it" + (", with %s of the humus in it" % _counted(len(humus)) if humus else "")
    shifted = _shift_nearest(garden, rng, bed, at, why)
    return bed, len(humus), shifted


def _humus(ctx, rng) -> list:
    """A few lines lying together somewhere in the humus, as a plug of earth brings them up."""
    try:
        texts = dict(ctx.soil.texts())
    except Exception:
        return []
    lines = [line.strip()[:LINE_MOST] for line in texts.get("compost/humus", "").splitlines() if line.strip()]
    if not lines:
        return []
    k = min(len(lines), rng.randint(*LINES))
    start = rng.randrange(len(lines) - k + 1)
    return lines[start:start + k]


def _rooted(plant) -> bool:
    """Has this plant rooted too deep for a molehill to shift it? Anything past its first year; a tree, a shrub, a
    woody climber or a woody stem past its first four months. (Its age is from its tag's `planted:`.)"""
    age = plant.age
    if age >= ROOTED:
        return True
    seed = plant.seed
    woody = any(hands.word(seed, key, "", words) for key, words in WOODY)
    return woody and age >= WOODY_ROOTED


def _shift_nearest(garden, rng, bed, at, why) -> bool:
    """The plant nearest the hill that is still shallow-rooted, if it is within reach, is pushed a little away from it.

    The step is a few hundredths of the bed for a seedling and shrinks with age, to a third of that at a year.
    True if a plant was shifted: then the ground has written the plant's ring, and the almanac line with it, with
    `why` in it, and the mole says nothing more of this hill. (A step that rounds to nothing, or a plant already
    against the bed's edge, is not shifted; then the mole's own line tells of the hill.)
    """
    near, best = None, REACH
    for plant in garden.plants(bed=bed):
        if plant.dead or _rooted(plant):
            continue
        d = math.hypot(plant.at[0] - at[0], plant.at[1] - at[1])
        if d < best:
            near, best = plant, d
    if near is None:
        return False
    dx, dy = near.at[0] - at[0], near.at[1] - at[1]
    length = math.hypot(dx, dy)
    if length < 1e-6:
        dx, dy, length = 1.0, 0.0, 1.0
    youth = 1.0 - 0.67 * _clamp(near.age / ROOTED, 0.0, 1.0)
    step = rng.uniform(0.03, 0.07) * youth
    return bool(garden.nudge(near, dx / length * step, dy / length * step, why))


def present(garden, ctx):
    hour = ctx.hour if isinstance(ctx.hour, int) else 12
    if not 7 <= hour <= 18:
        return None
    for thing in garden.things():
        if thing.maker == NAME and _date(thing.text) == ctx.date:
            return "The earth of a new molehill in the %s is still dark and loose" % thing.bed
    return None


def draw(text, ctx, pen):
    """The hill cut through: a heap of loose earth, a crumb for every ten letters, its lines across it. Centimetres.

    The crumbs lie in the earth between the lettered courses, never under the
    letters, so each one is whole and every line can be read. A hill a hand
    has piled with more than COURSES_DRAWN lines letters the top ones and
    says how many more it holds.
    """
    held = _hill_lines(text)
    letters = sum(len(line) for line in held)
    lettered = held[:COURSES_DRAWN]
    pen.unit_name = "cm"
    pen.unit_px_max = PX_CM
    pen.ground(0)
    courses = max(1, len(lettered))
    width = 46.0 + 4.0 * courses
    height = 9.0 + 3.2 * courses
    half = width / 2
    # the heap's skin
    pen.polyline([(half * (k / 30.0 - 1), height * _profile(k / 30.0 - 1)) for k in range(61)], 5, "brown")
    # the lines, course by course from the top (the lowest just above the ground, the rest above it at most
    # COURSE_APART, and none higher than TOP_COURSE of the heap), each lettered as far as the heap is wide at the
    # top of its letters
    size = 15
    measure = getattr(getattr(pen, "canvas", None), "text_width", None)
    if not callable(measure):
        measure = lambda s, size: 0.55 * size * len(s)              # (a pen with no canvas: a fair guess)
    boxes = []                                                       # (half its width, its foot, its head) for each line
    top = min(height * TOP_COURSE, BASE_COURSE + COURSE_APART * (courses - 1))
    for i, line in enumerate(lettered):
        y = 0.35 * height if courses == 1 else top - (top - BASE_COURSE) * i / (courses - 1)
        room_px = 2 * half * _across((y + LETTER_CM) / height) * 0.92 * PX_CM
        shown = line
        while len(shown) > 4 and measure(shown + " …", size) > room_px:
            shown = shown[:-1]
        shown = shown.rstrip() + (" …" if shown != line else "")
        pen.label(0, y, shown, size, "ink")
        boxes.append((measure(shown, size) / PX_CM / 2 + 1.0, y - 0.9, y + LETTER_CM + 0.6))
    # its crumbs: one for every ten letters it holds (and a few for the earth itself), in the earth between the lines
    for k in range(min(12 + letters // 10, 900)):
        for attempt in range(12):
            seed = zlib.crc32(b"crumb-%d-%d" % (k, attempt))
            u = ((seed % 1000) / 1000.0) * 2 - 1
            v = ((seed >> 10) % 1000) / 1000.0
            x = u * half * 0.94
            y = 0.4 + v * max(0.0, height * _profile(x / half) - 0.9)
            if not any(abs(x) < reach and low < y < high for reach, low, high in boxes):
                break
        pen.dot(x, y, 3, "brown")
    washed = _washed(text)
    if held:
        more = len(held) - len(lettered)
        pen.note("%d line%s of the humus, brought up by the mole%s" % (
            len(held), "" if len(held) == 1 else "s", "; the top %d are lettered" % len(lettered) if more else ""))
        if washed:
            pen.note("the rain has washed %d more off the top since it came up" % washed)
    elif washed:
        pen.note("only earth: the rain has washed its %d line%s of the humus away" % (washed, "" if washed == 1 else "s"))
    else:
        pen.note("only earth: no lines of the humus are left in it")


def _profile(u) -> float:
    """The heap's height at u across it (-1 at one foot, 0 the middle, 1 the other), as a share of its top:
    loose earth, rounded on top, its flanks sloping out to the ground."""
    return max(0.0, 1.0 - u * u) ** MOUND


def _across(share) -> float:
    """How far across the heap reaches (as a share of half its width) at `share` of its height: _profile turned round."""
    return max(0.0, 1.0 - min(1.0, max(0.0, share)) ** (1.0 / MOUND)) ** 0.5
