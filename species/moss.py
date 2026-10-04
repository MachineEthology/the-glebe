"""
Moss: a cushion that dries and revives.

A moss is a small green cushion on a stone, at a wall's foot or in a damp
crack, and its whole character is that it stops and starts. In a dry spell
its leaves curl in and it looks dead; on the first wet day every cell of it
opens at once and it is green again. Nothing dies of that. It grows only
while it is green, a cell at a time round its edge, most of all in shade and
cool damp. It dries from the rim inward. In spring it lifts capsules on hair-
thin stalks, and once a year, on a dry day with some wind in it, they let
their spore go. A spore that finds a damp crack comes up as a green film, and
in time the film raises a cushion.

On a stone in full sun a moss stays small and spends half its life curled.
At the foot of the north wall, or by the pond, it is green most of the year.


A SEED says, line by line (a line left out takes the value in brackets)

    kind: moss
    cushion: 14      the most it can spread across, in cm (12; 6..40). The
                     moss lives on a patch of that many cm each way, and
                     grows only inside the round of it.
    habit: cushion   cushion or mat. A cushion is a dense dome: it holds its
                     water, so it curls late, and it spreads slowly. A mat is
                     a flat carpet: it curls at once, and spreads about half
                     as fast again. [cushion]
    leaf: downy      plain, downy or waxy. A downy leaf ends in a pale hair
                     point that catches the dew and turns the sun: it curls
                     later still, and a bright bed does not stunt it. A waxy
                     leaf keeps a drought from taking the outer cells.
                     [plain]
    capsule: orange  the colour of its capsules: an ink of the plate or
                     #rrggbb, read loosely ("dark red", "rouge foncé").
                     (A `colour:` line is read for it too.) [brown]
    fruits: spring   the season it lifts capsules in. [spring]
    hardy: -30       the night, in degrees C, that kills it; a moss is hard
                     to kill, and nothing here goes lower than -45. [-30]
    variety: <name>  (if a visitor gave it one) carried on by its own spore
    start: spore     written by the days on every spore a moss lets go: it
                     comes up as a green film (see THE FILM). Without it,
                     what is planted is a piece of cushion: five green
                     cells near the middle of the patch.

Nothing else in the seed is read. What cannot be read is taken from what is
written here.


THE BODY, for example (a cushion of 12 cm each way, in spring):

    # a cushion of 23 cells, 11 of them curled; 2 capsules
    cushion: 12 by 12 cm
    last wet: 2027-04-11
    spores flew: 2027-04-02
    |            |
    |    .oo.    |
    |   .ooio.   |
    |   ,ooooo.  |
    |   ..oo..   |
    |            |
    ...

  * The line beginning # is only a summary, rewritten every day.
  * cushion: the patch, one cell to a cm. The rows under it are the patch
    seen from above, and they are the moss: a row is a line whose first mark
    is a bar. If the rows and the size line disagree, the rows win.
  * last wet: the last day that rain, or sodden ground, wetted it. The days
    since then are how long it has been dry.
  * spores flew: the last day its spore went on the wind (the line is
    absent until one has). A day yet to come is taken for lost.
  * heart browned: the day an old cushion's heart browned (absent until
    it has; see AGE).
  * In a row, every mark is one cell:

        (a space)  bare patch; nothing grows there yet
        o          green: open, wet, standing
        .          curled in: shut, dry
        i          green, with a capsule on a stalk
        ,          curled, with a capsule on a stalk

    Anything else is read as bare. A capital O is read as o, and so on: the
    reader is forgiving.
  * Any other line is a hand's note, kept below the rows: up to six lines,
    each cut to 160 characters.

A moss just up from a spore is a film, and its body is only:

    # a green film of moss, from a spore
    protonema: 6 damp days of 20


WHAT IT DOES, day by day

  * WET. A day of half a millimetre of rain or more, or with the ground
    round it sodden (a moss at the pond's edge drinks from the ground),
    opens every curled cell at once and sets "last wet" to today. A cushion
    that had been curled through and through for three weeks or more and
    opens again is the almanac's to tell: "greened again after a dry spell".
  * DRY. On a dry day each green cell on the rim, one with a side against a
    cell that is not green (bare, curled, or the patch's edge), may curl: so
    it dries a ring at a time, from the edge inward. The sunnier and windier
    and warmer the day, and the drier the ground, the likelier; a cushion
    holds on longer than a mat, and a downy leaf longer than a plain one.
    On a misty day, cloudy and the ground half wet, nothing curls. On a day
    that never rises above freezing nothing changes at all: it waits.
  * GROWTH. Only green cells grow, and only into the bare cells beside them,
    within the round of the patch. A bare cell with more moss around it
    takes sooner than one with a single neighbour, so the cushion fills out
    round and its bays fill in. It grows best between about 4 and 16
    degrees, best of all in shade (a bright bed stunts a plain leaf), more on
    a wet day than a dry one, a little more in ground made rich, and not at
    all in hard frost or in heat. A mat spreads faster than a cushion.
  * DROUGHT. A moss left unwetted for three weeks in warm weather begins to
    lose cells of its outer ring, a few at a time, more the longer it goes
    on; the almanac says so at five weeks. A waxy leaf keeps them. It never
    loses its heart: the inner cells stay, and open again when rain comes.
    (The reckoned sky brings so long a drought seldom, once in some years
    on the stones or at the wall's foot. The real one may bring more.)
  * CAPSULES. In the season of its fruits, on wet days, a cushion of at
    least eight cells lifts capsules on stalks from its green cells, about
    one cell in five by the season's end. A capsule stays on its cell, open
    or curled, until the season is over, and then falls.
  * SPORE. Once a year, on a dry day with a little wind (or a warm still
    one), a moss in capsule lets its spore go. Most of it is lost: about
    one year in three something comes of it, and that is its cast, one
    spore (now and then two), each with its parent's seed and a patch
    perhaps a cm or two larger or smaller. The ground sows it beside the
    parent or in the wild corner. A moss on dry ground (a bed with water
    under 0.7, like the stones) casts none: its spore finds no crack and is
    lost.
  * AGE. A cushion does not live for ever. From its fifth year (counted
    from the day its tag says it was planted) its heart may brown on any
    day that is not frozen, and most do within three years; from that day
    it grows no more and lifts no new capsules, and its cells fall away a
    few at a time, the heart first, until nothing is left and it has died
    of old age.
  * FROST. A moss shuts down in frost and takes no harm; only a night below
    its `hardy` line kills it.
  * It has no flowers, no creature eats it, and it does not cross.
  * When no cell of it is left, it is dead.


THE FILM. A spore comes up as a green film on damp ground, a thread of cells
too small to see. It counts the damp days: a day with rain, or with the
ground at least half wet, that does not freeze all day. At twenty it raises
its first cushion, three green cells in the middle of the patch, and the body
is a cushion's from then on. A film is fussy where a cushion is not. A spore
comes up only in a bed with water 0.7 or more, a damp crack: in a drier bed
it is lost on its first day. A dry day in a bed that is not wet through may
wither it, the likelier the drier the bed; at the pond's edge a film never
withers.


TO CUT IT, scrape: turn cells to spaces with your own hands. Each cell is its
own piece of moss, and comes away alone; what is left goes on from where it
is. Write an o in a bare cell and you have laid a piece of green moss there;
write a . and you have laid a dry one. A cell written outside the round the
moss may reach to stays, though the moss will not spread beyond the round.
Scrape every cell and it is dead. An emptied body comes up again from the
seed, as a new piece of cushion. Rows with garbled marks read as bare in
those places; a short row is bare at its end. A row whose left bar was
rubbed out is still a row, if it ends in its bar; one that lost both bars
is still a row among the others; characters no one can see (a zero-width
space, a mark of writing direction) are passed over. The ground's rings
call a scrape "cut back". They read a dot as bare ground, so a dry piece
laid by hand, or a cell curled by hand, is rung "cut back" too. Take away
the "heart browned" line and an old cushion grows again, until its heart
browns once more.


THE PLATE shows the patch from above, one square to a cell:

    pale stone                     the round the moss may reach to
    a tuft of upright blades       a green cell, standing; on a mat the
                                   blades are lower and lie all one way
    a low mound of two dashes      a curled cell, shut
    a stalk with a round head      a capsule, in its own colour, leaning
                                   to its cell's far corner
    a ringed white point           a downy leaf's hair point, on the tuft
                                   or on the mound
    a doubled middle blade, or a   a waxy leaf
      doubled lower dash
    in the planter's ink           a cell that was there when the last
                                   visitor left
    in the fresh green             a cell that was not: growth; and the
                                   stalk of a capsule lifted since
    a small dot high in a cell's   a cell that was there but has changed
      left side, in the planter's  its state since: on a tuft it has
      ink                          greened, on a mound it has curled in
    grey                           a dead moss
    the bar                        a length in cm

The first note says how many cells there are, how many are curled, how many
capsules. The second, when something has changed since the last visitor left,
says what: so many cells grown, greened, curled in or gone, so many capsules
lifted. Growth and waking are not the same thing, and the plate keeps them
apart: only growth is ever drawn in green ink, and a revived cell has only
its dot. A tuft has five blades where the cells are drawn large; on a wide
patch, whose cells are drawn small, it has three or two: that is the scale,
not the plant. A film is drawn as a straight thread along the ground, one
node of it for each day it grew (and the bar measures days of growth), with
faint places for the days still to come; the days it grew since the last
visitor left are in the fresh green.

Standard library and hands only. Nothing here raises on a garbled body or seed.

Mended on 1 October 2026 by the builders, before the garden opened: an old
cushion now browns and goes back, and less of its spore comes to anything; a
change of state is marked in the planter's ink, not the fresh green; rows a
hand garbled without moving a mark are read; mats, curled traits, new capsules
and a film's new days are drawn.
"""

import datetime
import math
import re
import unicodedata

import hands

KIND = "moss"
KEPT = ("kind", "cushion", "habit", "leaf", "capsule", "colour", "color", "fruits", "hardy", "variety")   # what a spore carries on
HABITS = ("cushion", "mat")
LEAVES = ("plain", "downy", "waxy")
SEASONS = ("spring", "summer", "autumn", "winter")

BARE, TURGID, CURLED, CAP_T, CAP_C = " ", "o", ".", "i", ","
_READ = {"o": TURGID, "O": TURGID, "0": TURGID, ".": CURLED, "·": CURLED,
         "i": CAP_T, "I": CAP_T, "!": CAP_T, ",": CAP_C, ";": CAP_C, "'": CAP_C}
_GREEN = (TURGID, CAP_T)
_DRY = (CURLED, CAP_C)
_CAPPED = (CAP_T, CAP_C)

WIDEST = 40                   # the largest patch, in cells (1,600 cells; a body of some 1,700 characters)
NARROWEST = 6
NOTES_MOST, NOTE_LONGEST = 6, 160
WET_RAIN = 0.5                # mm that wets it
WICK = 0.75                   # ground this wet, in the bed, wets it too
FILM_DAYS = 20                # damp days a film needs to raise a cushion
FILM_WATER = 0.7              # the least water a bed may have for a spore to come up at all
GROW = 0.016                  # chance, for a bare cell with one-in-five neighbours at the best of vigour, to take a day
DROUGHT_EACH = 0.008          # chance, on such a day, that an outer cell is lost, and a little more for each day beyond
DROUGHT_AFTER = 21            # days unwetted, in warm weather, before the outer ring begins to go
CAPSULE_FROM = 8              # cells a cushion needs before it lifts a capsule
CAPSULE_EACH = 0.0055         # chance, for each green cell on a wet day of the fruiting season, of a capsule
CAPSULE_FALL = 0.12           # chance, for each capsule out of season, that it falls on a day
SPORE_EACH, SPORE_MOST = 0.03, 0.3   # the chance on a day it may fly: for each capsule, and at most
SPORE_EVERY = 200             # days between one flight of spore and the next: it flies once a year
SPORE_TAKES = 0.35            # the chance that anything at all comes of a year's spore
OLD_FROM = 4 * 365            # days of age before a cushion's heart may brown
OLD_EACH = 1.0 / 730          # after that, the chance on a day that it does
BACK_EACH, BACK_HEART = 0.004, 0.001   # a browned cushion: each cell's chance on a day to fall away, and more for each living cell round it
GREENED_AFTER = 21            # days shut through and through before its greening is the almanac's to tell
STONE_INK = "#e6e0d3"
FRESH_INK = "#2e9e3f"         # the plate's fresh green, which only growth wears

_WEIGHT = (0.0, 0.45, 0.9, 1.4, 1.9, 2.4, 2.8, 3.2, 3.6)       # by the number of living cells among the eight round a bare one

_SIZE = re.compile(r"^\s*cushion\s*:\s*(\d+)(?:\s*(?:by|x|×)\s*(\d+))?", re.I)
_LASTWET = re.compile(r"^\s*last\s+wet\s*:\s*(\d{4})-(\d{2})-(\d{2})", re.I)
_FLEW = re.compile(r"^\s*spores?\s+flew\s*:?\s*(\d{4})-(\d{2})-(\d{2})", re.I)
_BROWNED = re.compile(r"^\s*heart\s+browned\s*:?\s*(\d{4})-(\d{2})-(\d{2})", re.I)
_FILM = re.compile(r"^\s*protonema\s*:\s*(\d{1,4})", re.I)


# ------------------------------------------------------------- the seed

def _text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    try:
        return str(value)
    except Exception:
        return ""


class Traits:
    __slots__ = ("cushion", "habit", "leaf", "capsule", "fruits", "hardy", "spore")

    def __init__(self, seed):
        if isinstance(seed, str):
            seed = hands.read_keys(seed)
        if not isinstance(seed, dict):
            seed = {}
        self.cushion = int(round(hands.num(seed, "cushion", 12, NARROWEST, WIDEST)))
        self.habit = hands.word(seed, "habit", "cushion", HABITS)
        self.leaf = hands.word(seed, "leaf", "plain", LEAVES)
        said = hands.line(seed, "capsule", "") or hands.line(seed, "colour", "") or hands.line(seed, "color", "")
        self.capsule = _colour(said or "brown")                  # "colour:" is read as well, as the other kinds write it
        self.fruits = hands.word(seed, "fruits", "spring", SEASONS)
        self.hardy = hands.num(seed, "hardy", -30.0, -45.0, 0.0)
        self.spore = hands.word(seed, "start", "") == "spore"


_COLOUR_WORDS = {"light": "pale", "clair": "pale", "claire": "pale", "pâle": "pale", "pale": "pale",
                 "foncé": "dark", "deep": "dark", "dark": "dark",
                 "rouge": "red", "rose": "pink", "jaune": "yellow", "bleu": "blue", "violette": "violet",
                 "brun": "brown", "gris": "grey", "gray": "grey", "noir": "black", "blanc": "white",
                 "orangé": "orange"}
_NO_CAPSULE_INKS = ("fresh", "dead", "faint", "ink", "wood", "white", "paper")


def _ink(name):
    if not name or name in _NO_CAPSULE_INKS:
        return None
    known = hands.mix(name, name)
    if known == "#1a1a1a" and name != "#1a1a1a":
        return None
    if _apart(known, FRESH_INK) < 90:
        return None                                  # the fresh green is the plate's, for growth: no capsule wears it
    return known if name.startswith("#") else name


def _apart(one, other) -> float:
    """How far apart two inks ('#rrggbb') are, in steps of red, green and blue together."""
    try:
        a = [int(one[i:i + 2], 16) for i in (1, 3, 5)]
        b = [int(other[i:i + 2], 16) for i in (1, 3, 5)]
    except Exception:
        return 999.0
    return math.sqrt(sum((p - q) ** 2 for p, q in zip(a, b)))


def _colour(text) -> str:
    """The capsule's colour as an ink ('#rrggbb' or a plate ink's name); a colour the plate does not know is brown."""
    words = [w.strip(",;.!?\"'()") for w in re.split(r"[\s_]+", _text(text).strip().lower())]
    words = [_COLOUR_WORDS.get(w, w) for w in words if w]
    if not words:
        return "brown"
    tries = ["-".join(words)]
    if len(words) >= 2:
        tries += ["-".join(words[:2]), "-".join(reversed(words[:2]))]
    for name in tries + words:
        ink = _ink(name)
        if ink:
            return ink
    return "brown"


# ------------------------------------------------------------- the body

class Moss:
    """A body, read. cells is a list of rows (lists of marks), or None for a film; film is its damp days, or None."""
    __slots__ = ("w", "h", "cells", "film", "wet", "flew", "browned", "notes")

    def __init__(self):
        self.w = self.h = 0
        self.cells = None
        self.film = None
        self.wet = None
        self.flew = None
        self.browned = None
        self.notes = []

    def living(self) -> int:
        return sum(1 for row in self.cells for v in row if v != BARE) if self.cells else 0

    def count(self, marks) -> int:
        return sum(1 for row in self.cells for v in row if v in marks) if self.cells else 0


def _date(y, m, d):
    try:
        return datetime.date(int(y), int(m), int(d))
    except Exception:
        return None


def _unseen(line) -> str:
    """A line without the characters no one can see (a zero-width space, a mark of writing direction): a hand that
    left one before a bar did not mean to move the moss. A mark typed at full width (ｏ, ｜) is read as itself."""
    if line.isascii():
        return line
    return "".join(chr(ord(ch) - 0xFEE0) if "！" <= ch <= "～" else ch
                   for ch in line if unicodedata.category(ch) != "Cf")


def _marks_only(text) -> bool:
    """Is this text made of a row's marks and spaces alone, with at least one mark?"""
    return any(ch in _READ for ch in text) and all(ch == " " or ch in _READ for ch in text)


def _row(line):
    """The cells of a row as text, or None if the line is no row.

    A row is a line whose first mark is a bar; its cells lie between that bar and its last one (or run to its end).
    A line of marks and spaces that ends in a bar is a row too, whose left bar a hand rubbed out.
    """
    line = _unseen(line)
    kept = line.lstrip()
    if kept.startswith("|"):
        inner = line[line.find("|") + 1:]
        end = inner.rfind("|")
        return inner[:end] if end >= 0 else inner
    kept = line.rstrip()
    if kept.endswith("|") and _marks_only(kept[:-1]):
        return kept[:-1]
    return None


def _read(body):
    """A body as a Moss, or None if neither a film nor a patch can be read in it. Never raises."""
    text = _text(body)
    m = Moss()
    rows, loose, notes = [], [], []
    for at, line in enumerate(text.splitlines()):
        row = _row(line)
        if row is not None:
            rows.append((at, row[:WIDEST]))
            continue
        if not line.strip() or line.lstrip().startswith(("#", hands.DAGGER)):
            continue
        found = _FILM.match(line)
        if found and m.film is None:
            m.film = min(int(found.group(1)), 9999)
            continue
        found = _LASTWET.match(line)
        if found and m.wet is None:
            m.wet = _date(*found.groups())
            continue
        found = _FLEW.match(line)
        if found and m.flew is None:
            m.flew = _date(*found.groups())
            continue
        found = _BROWNED.match(line)
        if found and m.browned is None:
            m.browned = _date(*found.groups())
            continue
        if _SIZE.match(line):
            continue
        plain = _unseen(line).rstrip()
        if _marks_only(plain):
            loose.append((at, plain[:WIDEST]))          # marks with both bars rubbed out: a note, unless it is all the moss there is
        notes.append((at, line.rstrip()[:NOTE_LONGEST]))
    if loose:
        if not any(ch in _READ for _, row in rows for ch in row):
            taken = loose                               # the rows hold no moss, but these lines do: they are its rows
        else:
            taken = [(at, row) for at, row in loose if rows[0][0] < at < rows[-1][0]]     # a row among rows
        rows = sorted(rows + taken)
        taken = set(at for at, _ in taken)
        notes = [(at, note) for at, note in notes if at not in taken]
    rows = [row for _, row in rows[:WIDEST]]
    m.notes = [note for _, note in notes[:NOTES_MOST]]
    if rows and any(ch != " " for row in rows for ch in row):
        m.w = max(len(row) for row in rows)
        m.h = len(rows)
        m.cells = [[_READ.get(ch, BARE) for ch in row.ljust(m.w)] for row in rows]
        m.film = None                        # a patch and a film at once: the patch wins
    elif rows:
        m.w = max(len(row) for row in rows)
        m.h = len(rows)
        m.cells = [[BARE] * m.w for _ in range(m.h)]
    elif m.film is None:
        return None
    return m


def _write(m, summary="") -> str:
    lines = []
    if summary:
        lines.append("# " + summary)
    if m.cells is None:
        lines.append("protonema: %d damp days of %d" % (m.film or 0, FILM_DAYS))
    else:
        lines.append("cushion: %d by %d cm" % (m.w, m.h))
        if m.wet is not None:
            lines.append("last wet: %s" % m.wet.isoformat())
        if m.flew is not None:
            lines.append("spores flew: %s" % m.flew.isoformat())
        if m.browned is not None:
            lines.append("heart browned: %s" % m.browned.isoformat())
        lines += ["|%s|" % "".join(row) for row in m.cells]
    lines += m.notes
    return "\n".join(lines) + "\n"


def _summary(m, habit="cushion") -> str:
    if m.cells is None:
        return "a green film of moss, from a spore"
    living = m.living()
    curled = m.count(_DRY)
    caps = m.count(_CAPPED)
    words = "a %s of %d cell%s" % ("mat" if habit == "mat" else "cushion", living, "" if living == 1 else "s")
    if living and curled == living:
        words += ", all curled"
    elif curled:
        words += ", %d of them curled" % curled
    if caps:
        words += "; %d capsule%s" % (caps, "" if caps == 1 else "s")
    if m.browned is not None:
        words += "; old, and going back"
    return words


# ------------------------------------------------------------- the sky

def _f(thing, name, default=0.0) -> float:
    try:
        value = float(getattr(thing, name, default))
    except Exception:
        return default
    return value if value == value else default


def _warmth(mean) -> float:
    """How a green moss likes the day's warmth: best between 4 and 16 degrees; little in frost or heat."""
    points = ((-2.0, 0.0), (1.0, 0.3), (4.0, 1.0), (16.0, 1.0), (22.0, 0.35), (28.0, 0.0))
    if mean <= points[0][0]:
        return 0.0
    for (t0, v0), (t1, v1) in zip(points, points[1:]):
        if mean <= t1:
            return v0 + (v1 - v0) * (mean - t0) / (t1 - t0)
    return 0.0


def _bed(ctx) -> dict:
    bed = getattr(ctx, "bed", None)
    return bed if isinstance(bed, dict) else {}


def _light(ctx) -> float:
    """The share of the sky's light the bed gets, 0..1."""
    return hands.num(_bed(ctx), "light", 0.8, 0.0, 1.0)


def _water(ctx) -> float:
    return hands.num(_bed(ctx), "water", 1.0, 0.0, 5.0)


def _curl_chance(sky, ctx, s) -> float:
    """The chance, on a dry day, that a green cell at the rim curls: sun, warmth, wind, and the ground's dryness."""
    sun = min(1.0, _f(sky, "light", 4.0) / 9.0)
    air = 0.10 + 0.55 * sun + 0.025 * max(0.0, _f(sky, "tmax", 10.0) - 6.0) + 0.03 * _f(sky, "wind", 2.0)
    dryness = 1.0 - 0.9 * min(1.0, _f(sky, "wet", 0.3))
    habit = 0.55 if s.habit == "cushion" else 1.0
    leaf = 0.6 if s.leaf == "downy" else 1.0
    if s.leaf == "downy":
        air = max(0.1, air - 0.25 * sun)             # a hair point turns the sun
    return max(0.04, min(0.95, air * dryness * habit * leaf))


def _vigour(sky, ctx, s, wets) -> float:
    """How well a green moss grows today, 0 .. about 1.6: warmth, shade, wetness, richness."""
    warmth = _warmth((_f(sky, "tmin", 5.0) + _f(sky, "tmax", 10.0)) / 2)
    if warmth <= 0:
        return 0.0
    shade = max(0.3, min(1.0, 1.2 - 0.8 * _light(ctx)))
    if s.leaf == "downy":
        shade = max(shade, 0.7)                      # a hoary moss is not stunted by sun
    moist = 1.0 if wets else 0.35
    rich = hands.num(_bed(ctx), "rich", 0.0, 0.0, 1.0)
    habit = 1.0 if s.habit == "mat" else 0.65
    return warmth * shade * moist * (1.0 + 0.5 * rich) * habit


# ------------------------------------------------------------- the patch

def _reach(m, r, c) -> bool:
    """Whether a cell lies inside the round the moss may spread to."""
    dx = (c + 0.5 - m.w / 2.0) / (m.w / 2.0)
    dy = (r + 0.5 - m.h / 2.0) / (m.h / 2.0)
    return dx * dx + dy * dy <= 1.05


def _around(m, r, c):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if (dr or dc) and 0 <= r + dr < m.h and 0 <= c + dc < m.w:
                yield m.cells[r + dr][c + dc]


def _rim(m, r, c) -> bool:
    """A green cell on the rim: one of its four sides touches a cell that is not green (or the edge of the patch)."""
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        rr, cc = r + dr, c + dc
        if not (0 <= rr < m.h and 0 <= cc < m.w) or m.cells[rr][cc] not in _GREEN:
            return True
    return False


def _outer(m, r, c) -> bool:
    """A living cell with a bare side: the outer ring of the cushion."""
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        rr, cc = r + dr, c + dc
        if not (0 <= rr < m.h and 0 <= cc < m.w) or m.cells[rr][cc] == BARE:
            return True
    return False


def _new_patch(size) -> Moss:
    m = Moss()
    m.w = m.h = size
    m.cells = [[BARE] * size for _ in range(size)]
    return m


def _seed_cells(m, rng, count) -> None:
    """Set the first green cells near the middle: a plus of five, or a small L of three."""
    jr = int(round(rng.uniform(-0.1, 0.1) * m.h))
    jc = int(round(rng.uniform(-0.1, 0.1) * m.w))
    r0 = max(1, min(m.h - 2, m.h // 2 + jr)) if m.h >= 3 else 0
    c0 = max(1, min(m.w - 2, m.w // 2 + jc)) if m.w >= 3 else 0
    spots = [(r0, c0), (r0, c0 + 1), (r0 + 1, c0)] if count < 5 else \
        [(r0, c0), (r0 - 1, c0), (r0 + 1, c0), (r0, c0 - 1), (r0, c0 + 1)]
    for r, c in spots:
        if 0 <= r < m.h and 0 <= c < m.w:
            m.cells[r][c] = TURGID


def sprout(seed, ctx) -> str:
    s = Traits(seed)
    m = Moss()
    if s.spore:
        m.film = 0
        return _write(m, _summary(m))
    rng = getattr(ctx, "rng", None)
    if rng is None:
        import random
        rng = random.Random(0)
    m = _new_patch(s.cushion)
    _seed_cells(m, rng, 5)
    m.wet = getattr(ctx, "date", None)
    return _write(m, _summary(m, s.habit))


# ------------------------------------------------------------- the days

def _age(ctx):
    """Days since it was planted, as its tag says, or None if that cannot be told."""
    try:
        age = float(getattr(ctx, "age", None))
    except Exception:
        return None
    return age if age == age else None


def _dead(ctx, why) -> str:
    """The first line of a dead body: the dagger, the day, and why."""
    today = getattr(ctx, "date", None)
    return "%s %s, %s\n" % (hands.DAGGER, today.isoformat() if today else "", why)


def day(body, seed, ctx):
    if hands.is_dead(body):
        return body, None
    s = Traits(seed)
    sky, today = ctx.sky, ctx.date
    m = _read(body)
    if m is None:
        return sprout(seed, ctx), "came up again from the seed"
    if _f(sky, "tmin", 5.0) < s.hardy:
        return _dead(ctx, "frost") + _write(m), "died of frost"
    if m.cells is None:
        return _film_day(m, s, ctx, sky, today)
    if m.living() == 0:
        return _dead(ctx, "scraped bare") + _write(m), "died: nothing was left of it"
    rng = ctx.rng
    event = None

    if m.wet is None or m.wet > today:
        m.wet = today                                  # a lost date, or one yet to come, is taken for today
    if m.flew is not None and m.flew > today:
        m.flew = None                                  # a flight yet to come never was: the date is taken for lost
    if m.browned is not None and m.browned > today:
        m.browned = None
    frozen = _f(sky, "tmax", 10.0) <= 0.0
    rained = _f(sky, "rain", 0.0) >= WET_RAIN
    wicked = _f(sky, "wet", 0.0) >= WICK
    wets = (rained or wicked) and not frozen
    living = m.living()

    if wets:
        curled = m.count(_DRY)
        dry_days = (today - m.wet).days if m.wet else 0
        if curled and living >= 6 and curled >= 0.9 * living and dry_days >= GREENED_AFTER:
            event = "greened again after a dry spell"
        for row in m.cells:
            for c, v in enumerate(row):
                if v == CURLED:
                    row[c] = TURGID
                elif v == CAP_C:
                    row[c] = CAP_T
        m.wet = today
    elif not frozen:
        misty = _f(sky, "cloud", 0.5) >= 0.75 and _f(sky, "wet", 0.0) >= 0.5
        if not misty:
            chance = _curl_chance(sky, ctx, s)
            rim = [(r, c) for r in range(m.h) for c in range(m.w) if m.cells[r][c] in _GREEN and _rim(m, r, c)]
            for r, c in rim:
                if rng.random() < chance:
                    m.cells[r][c] = CURLED if m.cells[r][c] == TURGID else CAP_C

    # age: an old cushion's heart may brown, and from then on it grows no more
    age = _age(ctx)
    if m.browned is None and not frozen and age is not None and age >= OLD_FROM and rng.random() < OLD_EACH:
        m.browned = today
        event = "its heart has browned with age"

    # growth: only the green, only into bare cells beside them, only inside the round
    if not frozen and m.browned is None:
        vig = _vigour(sky, ctx, s, wets)
        if vig > 0 and m.count(_GREEN):
            chance = GROW * vig
            joined = []
            for r in range(m.h):
                for c in range(m.w):
                    if m.cells[r][c] != BARE or not _reach(m, r, c):
                        continue
                    near = list(_around(m, r, c))
                    if not any(v in _GREEN for v in near):
                        continue
                    n = sum(1 for v in near if v != BARE)
                    if rng.random() < chance * _WEIGHT[min(n, len(_WEIGHT) - 1)]:
                        joined.append((r, c))
            for r, c in joined:
                m.cells[r][c] = TURGID

    # drought: after weeks unwetted in warm weather the outer ring begins to go; never the heart
    if not wets and m.wet is not None and s.leaf != "waxy" and not frozen:
        dry_days = (today - m.wet).days
        if dry_days >= DROUGHT_AFTER and _f(sky, "tmax", 10.0) >= 14.0 and m.living() > 4:
            chance = DROUGHT_EACH + 0.0002 * (dry_days - DROUGHT_AFTER)
            gone = [(r, c) for r in range(m.h) for c in range(m.w)
                    if m.cells[r][c] in _DRY and _outer(m, r, c) and rng.random() < chance]
            gone = gone[:max(0, m.living() - 4)]
            for r, c in gone:
                m.cells[r][c] = BARE
            if dry_days == 35:
                event = "five weeks without a wet day: its outer cells are going"

    # capsules
    season = getattr(sky, "season", "")
    caps_before = m.count(_CAPPED)
    if season == s.fruits:
        if wets and m.living() >= CAPSULE_FROM and m.browned is None:
            for r in range(m.h):
                for c in range(m.w):
                    if m.cells[r][c] == TURGID and rng.random() < CAPSULE_EACH:
                        m.cells[r][c] = CAP_T
            if caps_before == 0 and m.count(_CAPPED) and event is None:
                event = "lifted its first capsules"
    elif caps_before:
        for r in range(m.h):
            for c in range(m.w):
                if m.cells[r][c] in _CAPPED and rng.random() < CAPSULE_FALL:
                    m.cells[r][c] = TURGID if m.cells[r][c] == CAP_T else CURLED

    # spore: once a year, on a dry day with a little wind (or a warm still one), from a moss in capsule
    caps = m.count(_CAPPED)
    windy = _f(sky, "wind", 0.0) >= 1.5 or _f(sky, "tmax", 10.0) >= 15.0
    due = m.flew is None or (today - m.flew).days > SPORE_EVERY
    if caps and due and windy and not rained and not wets and not frozen:
        if rng.random() < min(SPORE_MOST, SPORE_EACH * caps + 0.05):
            m.flew = today
            if event is None:
                event = "its spores went on the wind"

    # an old cushion goes back: its cells fall away a few at a time, the heart first, until nothing is left
    if m.browned is not None and not frozen:
        gone = [(r, c) for r in range(m.h) for c in range(m.w) if m.cells[r][c] != BARE and
                rng.random() < BACK_EACH + BACK_HEART * sum(1 for v in _around(m, r, c) if v != BARE)]
        for r, c in gone:
            m.cells[r][c] = BARE
        if m.living() == 0:
            return _dead(ctx, "old age") + _write(m), "died of old age"

    return _write(m, _summary(m, s.habit)), event


def _film_day(m, s, ctx, sky, today):
    rng = ctx.rng
    water = _water(ctx)
    if water < FILM_WATER:
        return _dead(ctx, "no damp crack for it") + _write(m), "found no damp crack and was lost"
    wet = _f(sky, "wet", 0.0)
    rain = _f(sky, "rain", 0.0)
    if _f(sky, "tmax", 10.0) > 0 and (rain >= WET_RAIN or wet >= 0.5):
        m.film = (m.film or 0) + 1
    elif wet < 0.12 and rain < WET_RAIN and water < 1.5 and rng.random() < 0.12 * max(0.0, 1.5 - water):
        return _dead(ctx, "dried as a film") + _write(m), "dried out as a film"
    if (m.film or 0) >= FILM_DAYS:
        size = s.cushion
        patch = _new_patch(size)
        _seed_cells(patch, rng, 3)
        patch.wet = today
        patch.notes = m.notes
        return _write(patch, _summary(patch, s.habit)), "raised its first cushion"
    return _write(m, _summary(m)), None


# ------------------------------------------------------------- spore

def _tweak(rng, value, lo, hi, step) -> int:
    value += rng.choice((-step, 0, 0, 0, step))
    return int(max(lo, min(hi, value)))


def cast(body, seed, ctx) -> list:
    """On the day its spore flew: most years nothing comes of it; now and then one spore, or two, each carrying the
    parent's seed, the patch's size a little shifted."""
    if hands.is_dead(body):
        return []
    m = _read(body)
    today = getattr(ctx, "date", None)
    if m is None or m.cells is None or m.flew is None or today is None or m.flew != today:
        return []
    seed = seed if isinstance(seed, dict) else hands.read_keys(seed)
    if _water(ctx) < FILM_WATER:
        return []                              # on dry stone a spore finds no damp crack: it is lost on the wind
    rng = ctx.rng
    if rng.random() >= SPORE_TAKES:
        return []                              # most of it is lost: this year none of it came to anything
    out = []
    for _ in range(2 if rng.random() < 0.1 else 1):
        child = {key: value for key, value in seed.items() if key in KEPT}
        child["kind"] = KIND
        child["cushion"] = str(_tweak(rng, int(round(hands.num(seed, "cushion", 12, NARROWEST, WIDEST))), NARROWEST, WIDEST, 2))
        child["start"] = "spore"
        out.append(hands.write_keys(child))
    return out


# ------------------------------------------------------------- the plant

def size(body, seed) -> float:
    m = _read(body)
    return float(m.living()) if m is not None and m.cells is not None else 0.2


def describe(body, seed, ctx) -> str:
    m = _read(body)
    if m is None:
        return "no moss can be read in its body"
    if m.cells is None:
        words = "a film of moss, from a spore"
        return ("dead; " + words) if hands.is_dead(body) else words
    living = m.living()
    if hands.is_dead(body):
        return "dead; it stood %d cell%s" % (living, "" if living == 1 else "s")
    return _summary(m, Traits(seed).habit)


def _since(m, left) -> str:
    """What the weather and the days did since the last visitor left: cells grown, greened, curled in, gone; capsules
    lifted."""
    if left is None or left.cells is None or m.cells is None:
        return ""
    grown = greened = curled = lifted = gone = 0
    for r in range(max(m.h, left.h)):
        for c in range(max(m.w, left.w)):
            now = m.cells[r][c] if r < m.h and c < m.w else BARE
            then = left.cells[r][c] if r < left.h and c < left.w else BARE
            if now == BARE:
                gone += then != BARE
                continue
            if now in _CAPPED and then not in _CAPPED:
                lifted += 1
            if then == BARE:
                grown += 1
            elif (now in _GREEN) != (then in _GREEN):
                if now in _GREEN:
                    greened += 1
                else:
                    curled += 1
    parts = []
    if grown:
        parts.append("%d grown" % grown)
    if greened:
        parts.append("%d greened" % greened)
    if curled:
        parts.append("%d curled in" % curled)
    if gone:
        parts.append("%d gone" % gone)
    if lifted:
        parts.append("%d capsule%s lifted" % (lifted, "" if lifted == 1 else "s"))
    return "since the last visitor left: " + ", ".join(parts) if parts else ""


def draw(body, seed, ctx, pen) -> None:
    """The patch from above, one square to a cell. The docstring's last section says what each mark means."""
    pen.unit_name = "cm"
    pen.align = "center"
    pen.unit_px_max = 48
    m = _read(body)
    if m is None:
        pen.note("no moss can be read in its body")
        return
    dead = hands.is_dead(body)
    s = Traits(seed)
    left = getattr(ctx, "left", None)
    before = _read(left) if left is not None else None
    if m.cells is None:
        then = before.film if before is not None and before.cells is None else None
        _draw_film(pen, m, dead, then)
        pen.note(describe(body, seed, ctx))
        more = min(m.film or 0, FILM_DAYS) - min(then or 0, FILM_DAYS)
        if not dead and then is not None and more > 0:
            pen.note("since the last visitor left: %d more day%s of growth" % (more, "" if more == 1 else "s"))
        return
    if before is not None and before.cells is None:
        before = None
    w, h = m.w, m.h
    box = getattr(pen, "box", None) or (60, 50, 840, 930)
    try:
        across = min(48.0, (float(box[2]) - float(box[0]) - 6) / w, (float(box[3]) - float(box[1]) - 36) / h)
    except Exception:
        across = 14.0
    # the stone under it: every cell the moss may reach to, and any it has been given
    for r in range(h):
        y = h - 1 - r
        c = 0
        while c < w:
            if _reach(m, r, c) or m.cells[r][c] != BARE:
                c0 = c
                while c < w and (_reach(m, r, c) or m.cells[r][c] != BARE):
                    c += 1
                pen.cell(c0, y, c - c0, 1, STONE_INK)
            else:
                c += 1

    def was(r, c):
        if before is None:
            return None
        return before.cells[r][c] if r < before.h and c < before.w else BARE

    ink_of = lambda fresh: "dead" if dead else ("fresh" if fresh else "wood")
    weight = 5.0 if across >= 22 else 4.0
    capsules, changed = [], []
    for r in range(h):
        y = h - 1 - r
        for c in range(w):
            v = m.cells[r][c]
            if v == BARE:
                continue
            then = was(r, c)
            grown = before is None or then == BARE          # a cell the last visitor did not see
            ink = ink_of(grown)
            x = c
            if v in _GREEN:
                _tuft(pen, x, y, r, c, across, ink, s.leaf, s.habit, dead)
            else:
                _mound(pen, x, y, across, weight, ink, s.leaf, dead)
            if v in _CAPPED:
                capsules.append((x, y, ink_of(grown or then not in _CAPPED)))     # a capsule lifted since: its stalk is new
            if then is not None and then != BARE and not dead and (then in _GREEN) != (v in _GREEN):
                changed.append((x, y))
    head = max(4.0, min(7.5, across * 0.16))
    for x, y, ink in capsules:                              # a capsule on its stalk, leaning to its cell's far corner
        pen.line(x + 0.62, y + 0.3, x + 0.8, y + 0.8, 2.5, ink)
        pen.dot(x + 0.8, y + 0.84, head, "dead" if dead else "ink")
        pen.dot(x + 0.8, y + 0.84, head - 1.5, "dead" if dead else s.capsule)
    for x, y in changed:                                    # last, over everything: a dot high in the cell's left side
        pen.dot(x + 0.1, y + 0.68, 3.5, "wood")
    pen.note(describe(body, seed, ctx))
    since = "" if dead else _since(m, before)
    if since:
        pen.note(since)


def _mound(pen, x, y, across, weight, ink, leaf, dead) -> None:
    """A curled cell: a low flat mound, two dashes one on the other; the lower one doubled if the leaf is waxy, and a
    pale point on top if it is downy."""
    if leaf == "waxy" and not dead:
        for dy in (0.11, 0.23):                              # a doubled stroke: wax
            pen.line(x + 0.2, y + dy, x + 0.8, y + dy, max(2.0, weight - 2.0), ink)
        pen.line(x + 0.34, y + 0.36, x + 0.66, y + 0.36, weight, ink)
        return
    pen.line(x + 0.2, y + 0.17, x + 0.8, y + 0.17, weight, ink)
    pen.line(x + 0.34, y + 0.3, x + 0.66, y + 0.3, weight, ink)
    if leaf == "downy" and not dead:
        _hair(pen, x + 0.5, y + 0.42, across, ink)


def _hair(pen, x, y, across, ink) -> None:
    """A downy leaf's hair point: a pale point, ringed in the cell's own ink so that it shows on the pale stone (where
    the cells are drawn small there is no room for the ring, and the plate's own fine rim must do)."""
    if across >= 30:
        pen.dot(x, y, 4.5, ink)
    pen.dot(x, y, 3.0, "white")


def _tuft(pen, x, y, r, c, across, ink, leaf, habit, dead) -> None:
    """A green cell: upright blades that stand in the cell, crowded where the cell is wide on the plate. A cushion's
    stand up in a dome; a mat's are lower and lie over all one way, a flat carpet."""
    wobble = ((r * 31 + c * 17) % 5 - 2) * 0.01          # the same on every drawing: too little to mean anything
    if across >= 36:
        blades, weight = ((0.12, 0.42), (0.31, 0.74), (0.5, 0.9), (0.69, 0.72), (0.88, 0.44)), 5.0
    elif across >= 22:
        blades, weight = ((0.2, 0.5), (0.5, 0.88), (0.8, 0.5)), 4.5
    else:
        blades, weight = ((0.3, 0.5), (0.7, 0.55)), 3.5
    mat = habit == "mat"
    tip = None
    for i, (bx, top) in enumerate(blades):
        foot, lean = (bx - 0.07, 0.14) if mat else (bx, wobble / 2)
        if mat:
            top = 0.1 + (top - 0.1) * 0.5
        top += wobble if i % 2 else -wobble
        if leaf == "waxy" and not dead and i == len(blades) // 2:
            for dx in (-0.06, 0.06):                      # a doubled stroke: wax
                pen.line(x + foot + dx, y + 0.1, x + foot + dx + lean, y + top, max(2.0, weight - 2.0), ink)
        else:
            pen.line(x + foot, y + 0.1, x + foot + lean, y + top, weight, ink)
        if i == len(blades) // 2:
            tip = (x + foot + lean, y + top)
    if leaf == "downy" and not dead and tip is not None:
        _hair(pen, tip[0], tip[1] + 0.07, across, ink)


def _draw_film(pen, m, dead, then=None) -> None:
    """A film: a fine thread lying on the ground, one node of it for each day it grew (the bar measures days of
    growth), and faint places for the days still to come. The days it grew since the last visit are in the fresh ink."""
    pen.unit_name = "day of growth, days of growth"
    pen.ground(0)
    days = min(m.film or 0, FILM_DAYS)
    since = 0 if then is None else min(max(0, then), FILM_DAYS)       # with nothing to go by, all of it is new
    for i in range(days, FILM_DAYS):
        pen.dot(i + 1.0, 0.5, 2.5, "faint")
    for i in range(days):
        ink = "dead" if dead else ("fresh" if i >= since else "wood")
        pen.line(float(i), 0.5, i + 1.0, 0.5, 3.0, ink)
        pen.dot(i + 1.0, 0.5, 3.5, ink)
