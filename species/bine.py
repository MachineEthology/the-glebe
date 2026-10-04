r"""
Bine: a twiner. Several stems come up from one crown and climb by winding
round one another, a length at a time. When it has climbed as high as it
can hold itself, it arches over, comes down, and roots where its tips touch
the ground.

A bine is made of turns. Its body is the list of places where one stem
crossed its neighbour, and which of the two passed in front. Everything
else (which stem stands where at every height, the order of the flowers at
the tips, the order of its children's stems) follows from that list and
from nothing else.


A SEED says, line by line:

    kind: bine
    stems: pale-pink white dark-red
                    the stems at the crown, from left to right, each named
                    by the colour it flowers in: two to five of them. An ink
                    of the plate (pink, dark-red, violet...) or a #rrggbb.
    habit: 1 -2     how it twines: the turns it makes, in order, over and
                    over. 1 means the stems in the first and second places
                    cross, the one moving right passing in front; -1 means
                    the same two places, the one moving left in front; 2 is
                    the second and third places; and so on. A number too big
                    for the stems it has is counted round again.
    reach: 16       how many lengths it climbs before it arches over (6..30).
                    Once it has arched, the body remembers where (arches at),
                    and the seed's reach is not read again.
    flowers: summer the season its tips open (spring, summer or autumn)
    coat: smooth    smooth, downy or corky:
                      smooth  grows fastest, and slugs like it best;
                      downy   its soft growth takes a harder frost, and
                              slugs like it less;
                      corky   a tough skin: it grows slower, but slugs
                              hardly touch it and a gale cannot throw its
                              turns. (An older seed may say wiry: the same.)
    scent: dusk     (if it is there) a scent at dusk: the moths come for it
    hardy: -15      the night, in °C, that kills even its wood
    variety: <name> (if a visitor gave it one) carried on by seed that was
                    not crossed, and by the tips that root

Nothing else in the seed is read. A bine reads what it can of a garbled
seed and takes the rest from what is written here.


THE BODY is written from the top of the plant down, the way it is drawn:

    # a bine of 3 smooth stems, 38 lengths (12 of wood): arching over
    leans: right
    arches at: 16
    lengths grown: 38
    first flower: 2027-07-02
    in flower: white, pale-pink
      38 ~ white       pale-pink / dark-red
      37 ~ white       dark-red    pale-pink
      ...
       2   white       pale-pink   dark-red
       1   white     / pale-pink   dark-red
    crown: pale-pink   white       dark-red

  * The line beginning # is only a summary, rewritten every day. It also
    says the coat, and the scent if there is one: they are the seed's, and
    this is where the body tells of them.
  * leans: which way it will arch over, right or left.
  * arches at: written on the day it first climbs its reach. From then on
    this, not the seed, is where its arch stands, so the wood keeps the
    shape it grew in.
  * lengths grown: how many lengths it has ever grown. A new length is
    numbered on from it, so a number is never used twice.
  * first flower: the day its tips first opened, in its latest season of
    flowering. A flower lost and opening again that season is not news.
  * in flower: / in seed: the stems whose tips are open, or have set seed,
    by colour. Where two stems share a colour, a number in brackets after
    the name says which: its place at the tips, counted from the left on
    the top line (white (3)). A stem with neither is at rest (in bud, in
    its season).
  * touched ground: <date> once the tips have come down and rooted.
  * Each numbered line is one length of all the stems together. The number
    is its birth: it was the n-th length the plant grew. So a gap in the
    numbers is a place where something was cut (a bite, a frost, a hand),
    and growth after a cut carries on from the count, not from the gap.
    A ~ after it means soft growth, still green; without it the length has
    hardened into wood. Then the stems, named by colour, in the places they
    stand at the top of that length. A / or \ between two names is a turn:
    those two have just crossed. / means the one that moved right passed in
    front; \ means the one that moved left passed in front. A line with no
    mark is a plain length, grown without twining.
  * crown: the stems where they come out of the ground.
  * A dead bine's first line says when it died and how, in a word or two:
    † 2028-12-02, spent (the winter after it rooted); eaten; -17° frost.

On the numbered lines only two things are really the plant: which gap
each / or \ stands in (counted by how many names come before it), and
whether the line is soft. The names are written out fresh each day from the
crown and the turns below, so they always say truly where each stem is. The
lines are read in the order they stand in the file, not by their numbers.
A missing crown line is read from the seed. A body with nothing readable in
it comes up again from the seed, as if cut to the ground, and counts its
lengths from one again.


HOW IT LIVES. On a growing day (from late February to mid October, by the
length of the day, in warmth, light and wet ground; faster where the ground
is rich) it puts on one length. If the day is warm (a mean of 13° or more)
and bright where it stands (three hours of light or more reach its bed),
the length is a turn, the next one of its habit. Otherwise the stems only
lengthen, and the length is plain. So a bine's summers are tightly twined
and its springs and autumns loose, and a bine in a shaded bed twines less
(about half as often, under the north wall): on its dull days it is drawn
up long and straight toward the light.
It finds its place in the habit from the turns at its top, so after a cut
it carries on from wherever its top now is.

A turn followed by its own undoing (the same two places, the other one in
front, with nothing between them but plain lengths or turns of stems that
do not touch these two) is slack. On a breezy day slack in soft growth is
pulled straight: both turns become plain lengths. Wood keeps whatever
shape it hardened in. A gale may throw the newest soft turn the other way.

In autumn, as the days cool, soft growth hardens into wood from the bottom
up. A frost takes soft growth from the top down before it has hardened;
only a very hard frost (its hardy line) kills the wood. Slugs take soft
lengths from the top, and their flowers with them. A nibble of a length or
two goes by without a word; a bite that takes flowers, or three lengths or
more, is written in the almanac.

In its flowering season, once it has ten lengths, its tips open, one stem
at a time, each in its own colour, and later set seed. A flower that bees
or moths have brought another bine's pollen to may drop a crossed seed; one
that nobody visited may drop a seed of its own. Seed heads drop a few more
in autumn.

When the bine has climbed its reach it arches over, and comes down the
other side. When its tips touch wet ground they root: the whole arch ripens
into wood, and they drop a seed that comes up as a new bine, sown the way
the ground sows every seed: most often in the same bed, if it has room,
sometimes in the wild corner, and a creature may carry it off first. On a
frosty night in the winter after, the old bine is spent and dies; its
layered child lives on.

A child's stems stand, left to right, in the order its parent's tips stood
when the seed was made (a place keeps its side all the way round the arch:
place 1 is the side that was on the left at the crown). So the turns of one
year are carried into the next generation. A crossed child blends each
stem's colour with the pollen parent's, and splices the two habits.


TO CUT IT: a bine is a stiff thing to cut. To shorten it cleanly, take
lines from the top of the body (they are the tips). Take a line out of the
middle and every stem above that line is re-sorted: the flowers change
places, as they would if you cut one turn out of a rope. Remove a / or \
and that turn is undone; move it one name along and a different pair
crosses. Delete ~ marks and those lengths harden at once; add them and
they soften. Cut a bine that has rooted until its tips are off the ground
and it lives on, to come down and root again. Change the crown line and
you change the stems (their number and their colours). Change arches at
and you bend its wood by hand.


THE PLATE. Nothing on it is drawn that is not in the body, except the coat,
which is the seed's.

  * The stems, in the planter's ink: a heavy stroke is wood, a light stroke
    is soft growth. Green is what has grown since the last visit ended (a
    length numbered past what it had grown by then); grey is a dead bine.
  * Where two stems cross, the one that passes behind is broken.
  * A doubled stroke is a corky coat (the garden's mark for a tough skin):
    two lines close together, heavier for wood, lighter for soft growth. A
    row of small dots beside each stem is a downy coat. A plain single
    stroke is smooth.
  * The small squares under the ground line, one at the foot of each stem,
    are the stems' colours: the colours they flower in.
  * At each tip, in the stem's colour and set off from the stem by a little
    bare paper: a small knob is a tip at rest (in bud, in its season); a
    large dot is an open flower; a ring with a brown seed in it has gone to
    seed.
  * Short strokes going down into the ground at the far end are rooted
    tips, each in its stem's colour.
  * Each stem keeps its side all the way round the arch, so on the far side,
    read from left to right, the stems stand in the reverse of their order
    at the crown. A layered child stands in its parent's tip order, place 1
    on its left, so its crown reads as its parent's root forks read from
    right to left.
  * If a hand has made a bine longer than its arch, the rest turns the
    corner and lies along the ground.
  * The faint line is the ground. The bar at the bottom left says how long
    a length is at this size.
"""

import datetime
import math
import re
import unicodedata

import hands

KIND = "bine"
SEASONS = ("spring", "summer", "autumn", "winter")
COATS = ("smooth", "downy", "corky")
COAT_WORDS = {"smooth": "smooth", "downy": "downy", "down": "downy",
              "corky": "corky", "cork": "corky", "wiry": "corky"}     # wiry was the corky coat's first name
DEFAULT_STEMS = ["pale-pink", "white", "dark-red"]
MOST_STEMS = 5
MOST_COURSES = 300          # lengths a body may hold; a bine never grows past its arch, about 100
MOST_HABIT = 12             # turns a habit may hold
MOST_BIRTH = 999999         # the largest number a length is given
SPACING = 1.0               # the stems stand a length apart
TWINES_AT = 13.0            # °C, the day's mean at which the stems wind round one another
TWINES_IN_LIGHT = 3.0       # hours of light on its bed, below which the stems only lengthen
GROWS_FROM = 11.0           # hours of daylight before a bine wakes in spring (late February at 47°N)
SEASON_APART = 200          # days: a first flower this long after the last one is a new season's
KEPT = ("kind", "stems", "habit", "reach", "flowers", "coat", "scent", "hardy", "variety")
TURN_MARKS = {"/": 1, "//": 1, "\\": -1, "\\\\": -1}    # a doubled mark, as a hand may type it, is the same turn

_COURSE = re.compile(r"^\s*(\d{1,7})\s*(~?)(.*)$")
_DATE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
_WHOLE = re.compile(r"\d{1,7}")
_PLACE = re.compile(r"\(\s*(\d{1,2})\s*\)")


def _clean(text) -> str:
    """Text without the invisible format characters a hand's editor may leave in it
    (a byte-order mark, direction marks, joiners): they are not part of any word."""
    text = str(text or "")
    if text.isascii():
        return text
    return "".join(ch for ch in text if unicodedata.category(ch) != "Cf")


# ------------------------------------------------------------------ the seed

def _colours(text) -> list:
    """Stem colours as written: 'pale-pink white' or 'dark red, white'. At most five."""
    text = _clean(text)
    parts = text.split(",") if "," in text else text.split()
    names = []
    for part in parts:
        name = "-".join(part.strip().lower().split())
        name = re.sub(r"[^a-z0-9#\-]", "", name)[:24].strip("-")
        if name:
            names.append(name)
    return names[:MOST_STEMS]


def _said(seed, key) -> str:
    """What the seed says under a key, as one clean line."""
    return _clean(hands.line(seed, key, "")).strip()


def _stems(seed) -> list:
    return _colours(_said(seed, "stems")) or list(DEFAULT_STEMS)


def _habit(seed) -> list:
    """The habit as a list of signed numbers, none of them 0. At least one turn."""
    text = _said(seed, "habit").replace("−", "-")
    steps = []
    for found in re.findall(r"[-+]?\d{1,4}", text):
        value = int(found)
        if value:
            steps.append(value)
        if len(steps) >= MOST_HABIT:
            break
    return steps or [1]


def _gap(step, n) -> int:
    """Which gap a turn of the habit crosses, for a bine of n stems (1 is between the first two places)."""
    if n < 2:
        return 0
    return (abs(step) - 1) % (n - 1) + 1


def _reach(seed) -> int:
    return int(round(hands.num({"reach": _said(seed, "reach")}, "reach", 16, 6, 30)))


def _coat(seed) -> str:
    """smooth, downy or corky: the first coat word the seed's coat line holds."""
    for said in _said(seed, "coat").lower().replace(",", " ").split():
        coat = COAT_WORDS.get(said.strip(".;:!?'\"()"))
        if coat:
            return coat
    return "smooth"


def _season(seed) -> str:
    return hands.word({"flowers": _said(seed, "flowers")}, "flowers", "summer", SEASONS)


def _scent(seed) -> str:
    """The scent in words for the body's summary ('at dusk'), or '' if it has none."""
    said = " ".join(_said(seed, "scent").lower().split())[:30]
    first = said.split()[0].strip(".,;") if said else ""
    if not first or first in ("none", "no", "nothing", "-"):
        return ""
    return "at " + first if first in ("dusk", "night", "dawn") else "(%s)" % said


def _geometry(reach, n):
    """The arch: it climbs `reach`, goes over a half circle of radius r, and comes down. Returns (R, r, L).

    L, the lengths from the crown round to the ground, is a whole number:
    the half circle is made just wide enough for the tips to come down on
    the ground at the end of a length. Its radius is at least 0.38 of the
    reach; at least two lengths more than half the bine's width, so the
    innermost stem never bends tighter than two lengths; and at least three
    and a half times half its width, so a bine of many stems bends wider,
    as a thick rope does, and its turns keep room to cross on the inside.
    """
    half = (max(1, n) - 1) / 2.0 * SPACING
    least = max(half + 2.0, 3.5 * half, 0.38 * reach)
    whole = math.ceil(2 * reach + math.pi * least)
    return reach, (whole - 2 * reach) / math.pi, whole


# ------------------------------------------------------------------ the body

class _Bine:
    """A body, read. courses run from the crown up: [birth, soft, gap, sign]; gap 0 is a plain length."""

    def __init__(self):
        self.crown = []
        self.courses = []
        self.leans = "right"
        self.rooted = None
        self.arches_at = None         # the reach it arched at, once it has
        self.grown = 0                # lengths ever grown: the last length's number
        self.first_flower = None      # the first flower of its latest flowering season
        self.flowering = set()        # stems (by crown index) in flower
        self.seeding = set()          # stems gone to seed

    @property
    def n(self):
        return len(self.crown)

    def soft(self) -> int:
        return sum(1 for c in self.courses if c[1])

    def wood(self) -> int:
        return len(self.courses) - self.soft()

    def orders(self) -> list:
        """The stems' order (crown indices, place by place) at the top of each length, bottom first."""
        order = list(range(self.n))
        out = []
        for course in self.courses:
            gap = course[2]
            if 1 <= gap < self.n:
                order[gap - 1], order[gap] = order[gap], order[gap - 1]
            out.append(list(order))
        return out

    def tips(self) -> list:
        """The stems in the order they stand at the tips."""
        orders = self.orders()
        return orders[-1] if orders else list(range(self.n))

    def births(self) -> list:
        return [c[0] for c in self.courses]


def _arch(bine, seed):
    """(R, r, L) for this bine: where the body says it arched, or, until it has, the seed's reach."""
    return _geometry(bine.arches_at if bine.arches_at is not None else _reach(seed), bine.n)


def _date_in(text):
    found = _DATE.search(str(text or ""))
    if not found:
        return None
    try:
        return datetime.date(int(found.group(1)), int(found.group(2)), int(found.group(3)))
    except ValueError:
        return None


def _whole(text):
    """The first whole number in a text, or None."""
    found = _WHOLE.search(str(text or ""))
    return int(found.group()) if found else None


def _stems_named(text, crown, tips, taken) -> set:
    """The stems a flower or seed line names, as crown indices. Stems in `taken` are not named again.

    Each name may carry its place at the tips in brackets ('white (3)'). A
    name whose place holds a stem of that colour is that stem; any other
    name is the first stem of that colour, from the left at the tips, that
    is not yet named. So a flower stays with its stem when a hand's cut has
    moved it to another place.
    """
    if text is None:
        return set()
    text = _clean(text)
    wanted = []                                        # [name, place or None]
    for part in (text.split(",") if "," in text else text.split()):
        place = _PLACE.search(part)
        names = _colours(_PLACE.sub(" ", part))
        if names:
            wanted.append([names[0], int(place.group(1)) if place else None])
        elif place and wanted and wanted[-1][1] is None:
            wanted[-1][1] = int(place.group(1))        # 'white (3)' written without commas: the place follows
    taken, named, left_over = set(taken), set(), []
    for name, place in wanted:
        stem = tips[place - 1] if place and 1 <= place <= len(tips) else None
        if stem is not None and crown[stem] == name and stem not in taken:
            taken.add(stem)
            named.add(stem)
        else:
            left_over.append(name)
    for name in left_over:
        for stem in tips:
            if crown[stem] == name and stem not in taken:
                taken.add(stem)
                named.add(stem)
                break
    return named


def _read(body, seed):
    """A body as a _Bine, reading what it can. None if there is nothing readable in it. Never raises."""
    try:
        return _read_carefully(body, seed)
    except Exception:
        return None


def _read_carefully(body, seed):
    bine = _Bine()
    crown, tops, grown = None, [], 0
    flowering = seeding = None
    for raw in str(body or "").splitlines()[:3000]:
        line = _clean(raw).strip()
        if not line or line.startswith("#") or line.startswith("†"):
            continue
        found = _COURSE.match(line)
        if found:
            if len(tops) < MOST_COURSES:
                gap, sign, names = 0, 0, 0
                for token in found.group(3).split():
                    if token in TURN_MARKS:
                        if not gap and names:
                            gap, sign = names, TURN_MARKS[token]
                    elif token != "~":
                        names += 1
                tops.append([min(int(found.group(1)), MOST_BIRTH), found.group(2) == "~", gap, sign])
            continue
        key, colon, value = line.partition(":")
        key = " ".join(key.lower().split())
        if not colon:
            continue
        if key == "crown":
            crown = _colours(value)
        elif key in ("leans", "lean"):
            bine.leans = "left" if "left" in value.lower() else "right"
        elif key in ("touched ground", "rooted"):
            bine.rooted = _date_in(value)
        elif key in ("arches at", "arches"):
            at = _whole(value)
            bine.arches_at = None if at is None else max(6, min(30, at))
        elif key in ("lengths grown", "grown"):
            grown = min(MOST_BIRTH, _whole(value) or 0)
        elif key in ("first flower", "flowered"):
            bine.first_flower = _date_in(value)
        elif key in ("in flower", "flowering"):
            flowering = value
        elif key in ("in seed", "seeding"):
            seeding = value
    if crown is None and not tops:
        return None
    bine.crown = crown or _stems(seed)
    bine.courses = list(reversed(tops))
    for course in bine.courses:
        if not 1 <= course[2] < bine.n:
            course[2], course[3] = 0, 0
    bine.grown = max([grown] + bine.births())         # a count that has lost its line is the highest number left
    tips = bine.tips()
    bine.flowering = _stems_named(flowering, bine.crown, tips, set())
    bine.seeding = _stems_named(seeding, bine.crown, tips, bine.flowering)
    return bine


def _phase(bine, seed) -> str:
    """Where it is in its life, in a few words."""
    R, r, L = _arch(bine, seed)
    length = len(bine.courses)
    if bine.rooted and length >= L:
        return "rooted at the tip"
    if length == 0:
        return "just up"
    if length < R:
        return "climbing"
    if length < R + math.pi * r:
        return "arching over"
    if length < L:
        return "coming down"
    return "its tips on the ground"


def _named(bine, stems, tips) -> str:
    """Stems by colour, in their order at the tips; a colour two stems share carries its place in brackets."""
    out = []
    for place, stem in enumerate(tips):
        if stem in stems:
            colour = bine.crown[stem]
            out.append(colour + (" (%d)" % (place + 1) if bine.crown.count(colour) > 1 else ""))
    return ", ".join(out)


def _write(bine, seed) -> str:
    """A _Bine as the text of a body."""
    crown = bine.crown
    n = bine.n
    width = max([4] + [len(c) for c in crown])
    tips = bine.tips()
    summary = "# a bine of %d %s stem%s, %d length%s (%d of wood): %s" % (
        n, _coat(seed), "" if n == 1 else "s", len(bine.courses), "" if len(bine.courses) == 1 else "s",
        bine.wood(), _phase(bine, seed))
    scent = _scent(seed)
    lines = [summary + ("; scented " + scent if scent else "")]
    lines.append("leans: %s" % bine.leans)
    if bine.arches_at is not None:
        lines.append("arches at: %d" % bine.arches_at)
    lines.append("lengths grown: %d" % bine.grown)
    if bine.rooted:
        lines.append("touched ground: %s" % bine.rooted.isoformat())
    if bine.first_flower:
        lines.append("first flower: %s" % bine.first_flower.isoformat())
    if bine.flowering:
        lines.append("in flower: " + _named(bine, bine.flowering, tips))
    if bine.seeding:
        lines.append("in seed: " + _named(bine, bine.seeding, tips))
    number = max([4] + [len(str(b)) for b in bine.births()])
    orders = bine.orders()
    for k in range(len(bine.courses) - 1, -1, -1):
        birth, soft, gap, sign = bine.courses[k]
        text = ""
        for place, stem in enumerate(orders[k]):
            text += crown[stem].ljust(width)
            if place < n - 1:
                text += (" / " if sign > 0 else " \\ ") if gap == place + 1 else "   "
        lines.append((str(birth).rjust(number) + (" ~ " if soft else "   ") + text).rstrip())
    lines.append(("crown:".ljust(number + 3) + "   ".join(c.ljust(width) for c in crown)).rstrip())
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ the days

def sprout(seed, ctx) -> str:
    """A crown with its stems and no length yet. Which way it will lean is chosen now, by the day's dice."""
    bine = _Bine()
    bine.crown = _stems(seed)
    bine.leans = "left" if ctx.rng.random() < 0.5 else "right"
    return _write(bine, seed)


def _next_turn(bine, habit):
    """The turn it makes next: the one after the turns at its top, as its habit goes. (gap, sign)."""
    steps = [(_gap(v, bine.n), 1 if v > 0 else -1) for v in habit]
    size = len(steps)
    recent = [(c[2], c[3]) for c in reversed(bine.courses) if c[2]][:2 * size + 2]
    best, best_at = 0, 0
    for at in range(size):
        score = 0
        for i, (gap, sign) in enumerate(recent):
            want_gap, want_sign = steps[(at - i) % size]
            if gap != want_gap:
                break
            score += 2 if sign == want_sign else 1
        if score > best:
            best, best_at = score, at
    return steps[(best_at + 1) % size] if best else steps[0]


def _slack(bine):
    """The newest slack pair in soft growth: a turn and its own undoing with nothing holding them. (a, b) or None."""
    courses = bine.courses
    for b in range(len(courses) - 1, -1, -1):
        birth, soft, gap, sign = courses[b]
        if not gap or not soft:
            continue
        for a in range(b - 1, -1, -1):
            other = courses[a]
            if not other[2]:
                continue
            if other[2] == gap:
                if other[3] == -sign and other[1]:
                    return a, b
                break
            if abs(other[2] - gap) < 2:             # a turn of a neighbouring pair holds them
                break
    return None


def _grow_chance(bine, seed, sky, bed) -> float:
    if sky.daylength < GROWS_FROM:
        return 0.0
    warm = min(1.0, sky.warmth / 10.0)
    light = min(1.0, sky.light / 8.0)
    wet = sky.wet
    water = 0.25 if wet < 0.1 else 0.6 if wet < 0.2 else 1.0
    rich = hands.num(bed, "rich", 0, 0, 1)
    coat = 0.8 if _coat(seed) == "corky" else 1.0
    return 0.27 * warm * (0.25 + 0.75 * light) * water * (1 + 0.6 * rich) * coat


def _lengths(k) -> str:
    return "%d soft length%s" % (k, "" if k == 1 else "s")


def day(body, seed, ctx):
    """One day: the cold, the ripening, a length perhaps, the ground, the wind, the flowers. See HOW IT LIVES."""
    if hands.is_dead(body):
        return body, None
    bine = _read(body, seed)
    if bine is None:
        return sprout(seed, ctx), "came up again from the seed"
    sky, rng, date = ctx.sky, ctx.rng, ctx.date
    coat = _coat(seed)
    if bine.arches_at is None and len(bine.courses) >= _reach(seed):
        bine.arches_at = _reach(seed)             # it stands past its reach and the line was lost: written again
    R, r, L = _arch(bine, seed)
    events = []                                   # (weight, words): the day keeps the weightiest

    # the cold
    if sky.tmin < hands.num(seed, "hardy", -15, -30, 5):
        return ("† %s, %d° frost\n" % (date.isoformat(), round(sky.tmin))    # kept short: the plate's caption carries it
                + _write(bine, seed)), "killed by a hard frost"
    soft_hardy = -4.0 if coat == "downy" else -1.0
    if sky.tmin < soft_hardy and bine.soft():
        k = math.ceil(bine.soft() * min(1.0, (soft_hardy - sky.tmin + 0.5) / 3.0))
        taken = _take_soft(bine, k)
        if taken:
            events.append((5, "the frost took %s" % _lengths(taken)))

    # a rooted bine cut free lives on
    if bine.rooted and len(bine.courses) < L:
        bine.rooted = None
    # spent: the winter after it rooted (the day it rooted is in its touched ground line)
    if (bine.rooted and sky.season == "winter" and (date - bine.rooted).days >= 45
            and rng.random() < (0.5 if sky.frost else 0.02)):
        return ("† %s, spent\n" % date.isoformat()
                + _write(bine, seed)), "spent; its tips rooted, and it has died back"

    # hardening, from the bottom up, as the autumn cools
    if bine.soft() and date.month in (9, 10, 11, 12, 1, 2) and sky.tmean < 10:
        hardened = 0
        for course in bine.courses:
            if course[1] and hardened < 2:
                course[1] = False
                hardened += 1
        if not bine.soft() and date.month in (9, 10, 11) and len(bine.courses) >= 6:
            events.append((2, "its soft growth has hardened into wood"))

    # growth
    length = len(bine.courses)
    if not bine.rooted and length < L and rng.random() < _grow_chance(bine, seed, sky, ctx.bed):
        gap, sign = 0, 0
        if bine.n >= 2 and sky.tmean >= TWINES_AT and sky.light >= TWINES_IN_LIGHT:
            gap, sign = _next_turn(bine, _habit(seed))
        bine.grown = min(MOST_BIRTH, bine.grown + 1)
        bine.courses.append([bine.grown, True, gap, sign])
        length += 1
        if bine.arches_at is None and length >= R:
            bine.arches_at = R
            events.append((3, "has climbed its reach, and begins to arch over"))
    # the tips come to the ground and root, if it is wet enough
    if not bine.rooted and length >= L and sky.wet >= 0.3:
        bine.rooted = date
        bine.flowering, bine.seeding = set(), set()
        for course in bine.courses:                   # rooting ripens the whole arch into wood
            course[1] = False
        events.append((8, "its tips touched the ground and rooted"))

    # the wind
    slack = _slack(bine)
    if slack and sky.wind >= 4 and rng.random() < 0.3:
        for at in slack:
            bine.courses[at][2], bine.courses[at][3] = 0, 0
        events.append((1, "a slack turn pulled straight"))
    if sky.wind >= 6 and coat != "corky" and rng.random() < 0.4:
        for course in reversed(bine.courses):
            if course[1] and course[2]:
                course[3] = -course[3]
                events.append((4, "the gale threw a turn the other way"))
                break

    # flowers and seed
    events += _flowering(bine, seed, sky, rng, date)

    if not events:
        return _write(bine, seed), None
    return _write(bine, seed), max(events)[1]


def _take_soft(bine, k) -> int:
    """Take up to k soft lengths from the top, stopping at wood. The tips go with them. Returns how many."""
    taken = 0
    while taken < k and bine.courses and bine.courses[-1][1]:
        bine.courses.pop()
        taken += 1
    if taken:
        bine.flowering, bine.seeding = set(), set()
    return taken


def _flowering(bine, seed, sky, rng, date) -> list:
    season = _season(seed)
    free = not bine.rooted and len(bine.courses) >= 10
    events = []
    if sky.season == season and free:
        had = bool(bine.flowering or bine.seeding)
        if sky.tmean >= 10:
            for stem in range(bine.n):
                if stem not in bine.flowering and stem not in bine.seeding and rng.random() < 0.2:
                    bine.flowering.add(stem)
        for stem in sorted(bine.flowering):
            if rng.random() < 0.06:
                bine.flowering.discard(stem)
                bine.seeding.add(stem)
        last = bine.first_flower
        if bine.flowering and (last is None or not 0 <= (date - last).days < SEASON_APART):
            bine.first_flower = date                   # the season's first flower is the one worth saying
            if not had:
                events.append((6, "came into flower"))
    else:
        for stem in sorted(bine.flowering):
            if rng.random() < 0.35:
                bine.flowering.discard(stem)
                bine.seeding.add(stem)
        if sky.season in ("winter", "spring") or not free:
            for stem in sorted(bine.seeding):
                if rng.random() < 0.04:
                    bine.seeding.discard(stem)
    return events


# ------------------------------------------------------------------ what creatures meet

def flowers(body, seed, ctx) -> int:
    """How many of its tips are open today."""
    if hands.is_dead(body):
        return 0
    bine = _read(body, seed)
    return len(bine.flowering) if bine else 0


def bitten(body, seed, ctx, share, by):
    """A bite of this share of what is soft: lengths from the top, with the flowers on them.

    A nibble of a length or two says nothing; a bite that takes open flowers,
    three lengths or more, or the last of the plant, says so.
    """
    if hands.is_dead(body):
        return body, None
    bine = _read(body, seed)
    if bine is None:
        return body, None
    try:
        share = min(1.0, max(0.0, float(share)))
    except (TypeError, ValueError):
        return body, None
    by = " ".join(str(by or "something").split())[:40] or "something"
    coat = _coat(seed)
    spare = {"corky": 0.2, "downy": 0.6}.get(coat, 1.0)
    date, rng = getattr(ctx, "date", None), getattr(ctx, "rng", None)
    if not bine.courses:
        if share * spare >= 0.7 and isinstance(date, datetime.date):
            return ("† %s, eaten\n" % date.isoformat() + _write(bine, seed),
                    "eaten to the crown by %s" % by)
        return body, None
    want = share * bine.soft() * spare
    k = int(want) + (1 if rng is not None and rng.random() < want - int(want) else 0)
    open_, heads = len(bine.flowering), len(bine.seeding)
    taken = _take_soft(bine, k)
    if not taken:
        return body, None
    said = "%s took %s" % (by, _lengths(taken))
    if not bine.courses:
        said = "%s ate it back to the crown" % by
    elif open_:
        said += ", and its flowers with them"
    elif taken < 3:
        said = None
    elif heads:
        said += ", and its seed heads with them"
    return _write(bine, seed), said


# ------------------------------------------------------------------ seed

def _own_seed(bine, seed, order) -> dict:
    """A seed of this bine: its own lines, with the stems standing as `order` says."""
    kept = {key: value for key, value in seed.items() if key in KEPT}
    kept["kind"] = KIND
    kept["stems"] = " ".join(bine.crown[i] for i in order)
    return kept


def _donor(item):
    """The pollen parent's seed as a dict, and where it stands."""
    donor = getattr(item, "seed", None)
    if isinstance(donor, str):
        donor = hands.read_keys(donor)
    if not isinstance(donor, dict):
        donor = {}
    return donor, str(getattr(item, "where", "") or "another bine")


def _crossed(bine, seed, ctx, item) -> str:
    donor, where = _donor(item)
    rng = ctx.rng
    mine = [bine.crown[i] for i in bine.tips()]
    theirs = _stems(donor)
    child = {"kind": KIND,
             "stems": " ".join(hands.mix(colour, theirs[i % len(theirs)], 0.5) for i, colour in enumerate(mine))}
    a, b = _habit(seed), _habit(donor)
    spliced = (a[:rng.randint(1, len(a))] + b[rng.randint(0, len(b)):])[:8] or a
    child["habit"] = " ".join(str(v) for v in spliced)
    child["reach"] = "%d" % round((_reach(seed) + _reach(donor)) / 2 + rng.choice((-1, 0, 1)))
    child["flowers"] = _season(seed)
    child["coat"] = rng.choice((_coat(seed), _coat(donor)))
    scent = rng.choice((_said(seed, "scent"), _said(donor, "scent")))
    if scent:
        child["scent"] = scent
    child["hardy"] = "%d" % round((hands.num(seed, "hardy", -15, -30, 5) + hands.num(donor, "hardy", -15, -30, 5)) / 2)
    child["from"] = "cross of %s × %s" % (ctx.where, where)
    return hands.write_keys(child)


def cast(body, seed, ctx):
    """Seed dropped today: a layer on the day the tips root; a crossed seed only from pollen really brought;
    now and then a seed of its own from a flower or a seed head. At most three."""
    if hands.is_dead(body):
        return []
    bine = _read(body, seed)
    if bine is None:
        return []
    rng, dropped = ctx.rng, []
    if bine.rooted and bine.rooted == ctx.date:
        layer = _own_seed(bine, seed, bine.tips())
        base = re.sub(r"(-layer|-seedling)(-[ivxlcdm]+)?$", "", str(ctx.name or "bine")) or "bine"
        layer["name"] = base[:40] + "-layer"
        layer["from"] = "rooted from the tip of %s" % ctx.where
        dropped.append(hands.write_keys(layer))
    if bine.flowering:
        pollen = [item for item in (getattr(ctx, "pollen", None) or [])
                  if hands.word(_donor(item)[0], "kind", "") == KIND and _donor(item)[1] != ctx.where]
        if pollen:
            item = pollen[rng.randrange(len(pollen))]
            if rng.random() < 0.01 * min(3, len(bine.flowering)):
                dropped.append(_crossed(bine, seed, ctx, item))
        elif rng.random() < 0.001 * len(bine.flowering):
            dropped.append(hands.write_keys(_own_seed(bine, seed, bine.tips())))
    if bine.seeding and ctx.sky.season == "autumn" and rng.random() < 0.0008 * len(bine.seeding):
        dropped.append(hands.write_keys(_own_seed(bine, seed, bine.tips())))
    return dropped[:3]


def describe(body, seed, ctx) -> str:
    """One line: its stems, its lengths, how much is wood, where it is in its life, and its flowers."""
    bine = _read(body, seed)
    if bine is None:
        return "nothing to be read in its body"
    size = "%d stem%s, %d length%s" % (bine.n, "" if bine.n == 1 else "s",
                                      len(bine.courses), "" if len(bine.courses) == 1 else "s")
    if hands.is_dead(body):
        return "dead; it stood %s" % size
    said = "%s (%d of wood), %s" % (size, bine.wood(), _phase(bine, seed))
    if bine.flowering:
        said += ", in flower"
    elif bine.seeding:
        said += ", in seed"
    return said


def size(body, seed) -> float:
    """For its dot on the plan: its lengths, and half a length for the crown they grow from."""
    bine = _read(body, seed)
    return 0.0 if bine is None else len(bine.courses) + 0.5


# ------------------------------------------------------------------ the plate

PAIR_GAP = 2.4              # px of paper between the two lines of a corky stem
PAIR_LINE = (2.0, 3.4)      # px: each line of a corky stem, soft and wood
MARGIN = 3.0                # px of paper each side of a stem that passes in front


def _frame(s, R, r, half, lean, lying=False):
    """Where the middle of the bine is, s lengths from the crown, and which way its places run from there.

    Returns (x, y, nx, ny): the point, and the direction in which the places
    run from place 1 to the last. The bine climbs straight up to R, goes
    over a half circle of radius r, and comes straight down; leaning left is
    the same arch the other way. The places always run a quarter turn to
    the right of the way the bine is going, so a stem keeps its side.
    `lying`: the bine is longer than its arch (a hand made it so). Then it
    turns a rounded corner before the ground and lies along it.
    """
    arc = math.pi * r
    if s <= R:
        return 0.0, s, 1.0, 0.0
    if s <= R + arc:
        phi = (s - R) / r
        if lean > 0:
            theta = math.pi - phi
            return r + r * math.cos(theta), R + r * math.sin(theta), -math.cos(theta), -math.sin(theta)
        return -r + r * math.cos(phi), R + r * math.sin(phi), math.cos(phi), math.sin(phi)
    down = s - R - arc
    x = lean * 2 * r
    if not lying:
        return x, R - down, -1.0, 0.0
    bend = half + 1.0                              # the corner's radius: no stem folds on its inside
    drop = max(0.0, R - half - bend)               # straight down this far, then round the corner
    if down <= drop:
        return x, R - down, -1.0, 0.0
    phi = (down - drop) / bend
    if phi <= math.pi / 2:
        cx, cy = x + lean * bend, R - drop
        return cx - lean * bend * math.cos(phi), cy - bend * math.sin(phi), -math.cos(phi), -lean * math.sin(phi)
    along = down - drop - bend * math.pi / 2
    return x + lean * (bend + along), half, 0.0, -float(lean)


def _smooth(t):
    """Easing for a turn: the stems leave and arrive upright and cross in the middle."""
    return t * t * (3 - 2 * t)


def _strokes(bine, frame, offset, newest_then, dead) -> list:
    """Every stem of every length, as [points, soft, ink, front, crossing].

    frame(s) is _frame for this bine. front is None for a stem that does not
    turn, True for the one of a turn that passes in front, False for the one
    that passes behind. crossing is the sine of the angle at which the two
    stems of a turn cross (1 is square), measured on the drawing, so the
    break can be sized to it.
    """
    def at(s, d):
        x, y, nx, ny = frame(s)
        return x + d * nx, y + d * ny

    n = bine.n
    strokes = []
    for k, (birth, soft, gap, sign) in enumerate(bine.courses):
        ink = "dead" if dead else "fresh" if birth > newest_then else "wood"
        curved = frame(k)[2:] != frame(k + 1)[2:] or frame(k + 0.5)[2:] != frame(k)[2:]   # it bends in this length
        pair = []
        for place in range(n):
            goes = place + 1 if gap and place == gap - 1 else place - 1 if gap and place == gap else place
            if goes == place:
                steps = 6 if curved else 1
                points = [at(k + j / steps, offset[place]) for j in range(steps + 1)]
                strokes.append([points, soft, ink, None, 1.0])
            else:
                points = [at(k + j / 20.0, offset[place] + (offset[goes] - offset[place]) * _smooth(j / 20.0))
                          for j in range(21)]
                stroke = [points, soft, ink, (goes > place) == (sign > 0), 1.0]   # '/': the one moving right
                strokes.append(stroke)
                pair.append(stroke)
        if len(pair) == 2:
            (a, b) = [_heading(s[0], 10) for s in pair]
            crossing = max(0.35, abs(a[0] * b[1] - a[1] * b[0]))
            pair[0][4] = pair[1][4] = crossing
    return strokes


def _heading(points, i):
    """The unit direction of a polyline at its i-th point."""
    (x1, y1), (x2, y2) = points[max(0, i - 1)], points[min(len(points) - 1, i + 1)]
    size = math.hypot(x2 - x1, y2 - y1) or 1.0
    return (x2 - x1) / size, (y2 - y1) / size


def _broken(points, clear):
    """A stroke that passes behind, as its two ends: `clear` units of it taken out either side of its middle,
    but never so much that an end is shorter than a sixth of the stroke."""
    steps = [math.hypot(points[i + 1][0] - points[i][0], points[i + 1][1] - points[i][1])
             for i in range(len(points) - 1)]
    total = sum(steps) or 1.0
    clear = min(clear, total * (0.5 - 1 / 6.0))
    return (_part(points, steps, 0.0, total / 2 - clear),
            _part(points, steps, total / 2 + clear, total))


def _part(points, steps, start, end):
    """The piece of a polyline between two distances along it."""
    out, walked = [], 0.0
    for i, step in enumerate(steps):
        a, b = points[i], points[i + 1]
        lo, hi = walked, walked + step
        if hi >= start and lo <= end and step > 0:
            t0, t1 = max(0.0, (start - lo) / step), min(1.0, (end - lo) / step)
            p0 = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0)
            p1 = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
            if not out:
                out.append(p0)
            out.append(p1)
        walked = hi
    return out


def draw(body, seed, ctx, pen) -> None:
    """The bine on its plate: every mark is one of those listed under THE PLATE above."""
    pen.unit_name = "length, lengths"
    pen.ground(0)
    dead = hands.is_dead(body)
    bine = _read(body, seed)
    if bine is None:
        pen.note("nothing to be read in its body")
        return
    left = _read(ctx.left, seed) if getattr(ctx, "left", None) is not None else None
    newest_then = left.grown if left is not None else -1       # a new plant is all fresh
    n, coat = bine.n, _coat(seed)
    R, r, L = _arch(bine, seed)
    lean = -1 if bine.leans == "left" else 1
    half = (n - 1) / 2.0 * SPACING
    offset = [-half + i * SPACING for i in range(n)]
    lying = len(bine.courses) > L

    def frame(s):
        return _frame(s, R, r, half, lean, lying)

    def at(s, d):
        x, y, nx, ny = frame(s)
        return x + d * nx, y + d * ny

    strokes = _strokes(bine, frame, offset, newest_then, dead)
    # The pen fits the drawing to the plate only when it is settled; the gaps and the doubled strokes must
    # be sized in pixels, so the scale it will choose is reckoned here the same way (near enough).
    xs = [x for points, _, _, _, _ in strokes for x, _ in points] + offset
    ys = [y for points, _, _, _, _ in strokes for _, y in points] + [0.0]
    scale = max(4.0, min(60.0, 740.0 / (max(xs) - min(xs) + 1.2), 800.0 / (max(ys) - min(ys + [0.0]) + 1.6)))
    # Heavy is wood and light is soft; drawn small, both come down a little so the stems keep paper between.
    heavy, light = max(5.0, min(7.5, 0.36 * scale)), max(3.2, min(4.5, 0.22 * scale))

    def body_width(soft):
        """Half the width of a stem as drawn, in pixels."""
        if coat == "corky":
            line = PAIR_LINE[0 if soft else 1]
            return line + PAIR_GAP / 2.0
        return (light if soft else heavy) / 2.0

    def stroke(points, soft, ink):
        if len(points) < 2:
            return
        if coat == "corky":                            # a doubled stroke: two lines close, with paper between
            line = PAIR_LINE[0 if soft else 1]
            apart = (line + PAIR_GAP) / 2.0 / scale
            for side in (-1, 1):
                pen.polyline(_beside(points, side * apart), line, ink)
        else:
            pen.polyline(points, light if soft else heavy, ink)

    for points, soft, ink, front, crossing in strokes:        # first the stems that pass behind, broken there
        if front is False:
            width = body_width(soft)
            slant = math.sqrt(max(0.0, 1.0 - crossing * crossing))
            clear = ((width + MARGIN) / crossing + width * slant / crossing) / scale
            for piece in _broken(points, clear):
                stroke(piece, soft, ink)
    for points, soft, ink, front, crossing in strokes:        # then all the rest over them
        if front is not False:
            stroke(points, soft, ink)

    if coat == "downy":                                # down: a fine stipple either side of every stem
        for number, (points, soft, ink, front, _) in enumerate(strokes):
            apart = (body_width(soft) + 5.0) / scale
            spots = ((0.18, 1), (0.82, -1)) if front is not None else ((0.3, 1), (0.7, -1))
            if scale < 30:                             # drawn small: one grain to a length, or it would be all dots
                spots = spots[number % 2:number % 2 + 1]
            for share, side in spots:
                (x, y), (dx, dy) = _along(points, share)
                nx, ny = _normal(0, 0, dx, dy)
                pen.dot(x + side * nx * apart, y + side * ny * apart, 3, ink)

    # the crown: a square of each stem's colour at its foot, under the ground line
    side = min(0.6, 15.0 / scale)
    for place in range(n):
        pen.cell(offset[place] - side / 2, -side - 0.15, side, side, "dead" if dead else bine.crown[place])

    # the tips: bud, flower or seed, each in its stem's colour; or roots, where it has come to the ground.
    # Each is laid on a little bare paper first, so a colour near the planter's ink still stands apart.
    tips, length = bine.tips(), len(bine.courses)
    bloom = max(5.0, min(10.0, 0.36 * scale * SPACING))
    knob = max(4.5, min(6.5, 0.3 * scale))
    rooted = bine.rooted and length >= L               # (a rooted bine cut shorter is free again, from its next day)
    marks = []
    for place in range(n):
        stem = tips[place]
        x, y = at(length, offset[place])
        colour = "dead" if dead else bine.crown[stem]
        if rooted:
            marks.append(("roots", x, y, colour))
        elif stem in bine.flowering and not dead:
            marks.append(("flower", x, y, colour))
        elif stem in bine.seeding:
            marks.append(("seed", x, y, colour))
        elif not dead:
            marks.append(("knob", x, y, colour))
    deep = max(0.5, 16.0 / scale)
    below = 3.0 / scale
    for what, x, y, colour in marks:                   # the paper under every mark, before any mark
        if what == "roots":
            for dx in (-0.4, 0.0, 0.4):
                pen.line(x, y - below, x + dx * deep, y - deep, 3 + 4, "paper")
        else:
            pen.dot(x, y, {"flower": bloom, "seed": bloom * 0.85 + 1.5, "knob": knob}[what] + 2.5, "paper")
    for what, x, y, colour in marks:
        if what == "roots":
            for dx in (-0.4, 0.0, 0.4):
                pen.line(x, y - below, x + dx * deep, y - deep, 3, colour)
        elif what == "flower":
            pen.dot(x, y, bloom, colour)
        elif what == "seed":
            pen.dot(x, y, bloom * 0.85, colour, filled=False, weight=3)
            pen.dot(x, y, 3.5, "dead" if dead else "brown")
        else:
            pen.dot(x, y, knob, colour)

    pen.note(describe(body, seed, ctx))
    if bine.flowering and not dead:
        pen.note("in flower: " + _named(bine, bine.flowering, tips))


def _along(points, share):
    """The point a share of the way along a polyline (counted by its points), and the direction there."""
    if len(points) < 2:
        return points[0], (0.0, 1.0)
    at = min(max(share, 0.0), 1.0) * (len(points) - 1)
    i = min(len(points) - 2, int(at))
    (x1, y1), (x2, y2) = points[i], points[i + 1]
    t = at - i
    return (x1 + (x2 - x1) * t, y1 + (y2 - y1) * t), (x2 - x1, y2 - y1)


def _normal(x1, y1, x2, y2):
    """The unit direction a quarter turn to the left of the way from (x1, y1) to (x2, y2)."""
    dx, dy = x2 - x1, y2 - y1
    size = math.hypot(dx, dy) or 1.0
    return -dy / size, dx / size


def _beside(points, apart):
    """The same line moved `apart` units to its left (negative: to its right).

    Where the line bends tighter than `apart`, the moved line on the inside
    of the bend would fold back on itself; the points that run backwards
    are left out, so the inner line of a corky pair takes the corner cleanly.
    """
    out, came_from = [], []
    for i, (x, y) in enumerate(points):
        a = points[max(0, i - 1)]
        b = points[min(len(points) - 1, i + 1)]
        nx, ny = _normal(a[0], a[1], b[0], b[1])
        moved = (x + nx * apart, y + ny * apart)
        if out and i < len(points) - 1:
            (px, py), (ox, oy) = out[-1], came_from[-1]
            if (moved[0] - px) * (x - ox) + (moved[1] - py) * (y - oy) <= 0:
                continue                                  # it would run backwards: skip it
        out.append(moved)
        came_from.append((x, y))
    return out
