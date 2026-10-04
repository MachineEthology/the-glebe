"""
Lichen: a slow colony on a stone.

A lichen is two lives in one, a fungus and the green cells it keeps, and it
grows only while it is wet. Here it is a stone seen from above, written as a
grid of characters, with the crust on it cell by cell. It spreads from its
young edge by a small rule of the kind used for life-like automata, only on
days when the ground is wet, and most in the cool wet months. Its old centre
dies, so over the years it makes rings. On windy days bits of it blow off,
to start again elsewhere on the stone, or on another stone altogether.

It belongs on the stones, but it grows anywhere there is rain: faster where
the ground stays wet and the light is good, hardly at all on a dry bright
stone in August, and in deep shade only slowly.


A SEED says (any line may be left out; the default is in brackets)

    kind: lichen
    joins: 3 4 5 6 7 8   which bare cells of stone may join the colony: those
                         touching exactly this many living cells, of the eight
                         around them. A range is read too (3-8, 3..8, 3 to 8),
                         and so is life-like notation: B36/S23 means 3 6. A
                         cell joins only beside young crust. [2 3]
    thirst: 0.2          how wet the ground must be (0 dust .. 1 sodden) before
                         it grows at all. A day of rain on a dry stone wets it
                         half as well. [0.2]
    slow: 40             on a good day, each cell that may join does so with
                         one chance in this many. Cold, summer heat, shade and
                         a thin wetting make the chance smaller. [40]
    lives: 6             how old, in lichen-years, a cell of crust is when it
                         dies and goes grey: at 2, the crust of year a dies
                         as year c begins. At least 2. See A SHORT LIFE. [6]
    crust: hard          smooth, powdery or hard; see THE CRUST. [smooth]
    fruit: orange        the colour of its fruit discs, or none. One of the
                         plate's inks: red, dark red, pink, pale pink, orange,
                         yellow, blue, violet, brown, black, white, grey; or
                         #rrggbb. (French is read as well: rouge foncé, rose
                         pâle...) A colour the plate does not know is drawn
                         brown. [brown]
    stone: 52 by 38      the stone it comes up on, in cells (at most 90 by 70).
                         Left out, it finds a stone of about that size.
    variety: <name>      a name a visitor gave it. Its fragments keep it.


THE BODY is the stone, seen from above:

    stone: 52 by 38 cells
    year a began: 2026-08-01
    |          ........           |
    |      .....bbbb::bb....      |
    |     ....bbaaa:::aAab...     |
    ...

Each row of the stone lies between two bars. In a row:

    (a space)   off the stone; nothing grows there
    .           bare stone
    a b c ...   living crust, lettered by the lichen-year it grew in
    A B C ...   the same, bearing a fruit disc
    :           dead crust

A lichen-year begins on the first of August, when lichens rest in the
summer drought (the first of February south of the equator). Year a is the
one the second line names, b the year after, and so on; after z comes a
again. So the letters are the colony's growth rings, and the text shows
how far it spread in each year. Crust of this year and last year is young,
and only young crust reaches out; older crust holds its ground. The first
line only says the stone's size; the rows themselves are the stone.

The second line is checked against the day the plant was sown. A year that
has not begun yet, or one that would make most of the crust die at once
where the sowing day would not, is taken for a slip of the hand and put
right. So to make it die back, scrape it; its calendar is its own.

Any other line a hand writes into the body (a note: "scraped the east side,
to see it heal") is kept, below the rows: up to six lines, each cut to 160
characters. Notes about a plant belong more lastingly in its tag.


WHAT IT DOES, day by day

- On a day the ground is wet enough (thirst), and the stone is not frozen
  all day, each bare cell beside young crust may join: if the number of
  living cells around it is in the joins table, it joins with one chance
  in `slow`, less on a poor day. The best days are 5 to 14 degrees, in good
  light; summer heat, shade and short winter days slow it. Ground made rich
  (by a pony, or by a hand) quickens it by up to a half. Frost does it no
  harm: a lichen only waits until the stone thaws.
- At the first wetting of a new lichen-year, crust that has reached the age
  `lives` dies all at once, and the old centre goes grey. Dead crust
  crumbles back to bare stone over a year or so, faster when wet ground
  freezes.
- In autumn some of its older crust bears fruit discs, spaced apart.
- On windy days, and when heavy rain splashes, a fragment may lodge on bare
  stone and start a small new colony on the same stone. That is how a
  crumbled centre is settled again, and how rings come inside rings.
- On windy days a large colony may cast a fragment into the wind, and in
  autumn, on calm dry days, one with fruit discs may shed a spore. The
  ground sows either as a new lichen on a new stone, in this bed or the
  wild corner. A north-wall lichen is out of the wind, and casts only
  spores.
- When no living crust is left, the lichen is dead.

A SHORT LIFE. With `lives: 2` each year's crust lives two years, so the
colony is a ring that moves outward, round a grey centre. It needs room to
move: a quick table on a small stone can cover the whole stone in one year,
have nowhere to grow the next, and die whole as the third begins.


THE CRUST (the trait each seed chooses)

    smooth    an ordinary crust. It fragments now and then; on wet nights
              slugs graze a little of its new edge.
    powdery   its surface is powder (soredia). It sheds fragments freely in
              the wind, so it spreads over its stone and beyond; but it is
              soft, and slugs graze all of its new crust, not only the edge.
    hard      thick, cracked into little plates. Slugs hardly touch it and
              it seldom breaks off. It heals: its threads run into the
              stone, so a scratch one cell wide, or a pinhole, closes again
              all at once on one of the next few wet days.


TO CUT IT, scrape: turn living cells into `.` with your own hands. Every
character is a piece of the crust and comes away on its own, as it does from
a real stone. What is left keeps growing from its young edge; a patch you
scrape out of old crust stays bare (a hard crust's thin scratches heal, so
to cut a hard crust take a patch at least two cells wide). Write a letter
into bare stone and you have grafted a piece of crust of that year. Scrape
every living cell and it is dead. An empty body comes up again from the
seed, as a new colony on a new stone. Hands may garble the rows: anything
that is not one of the marks above is read as bare stone, a short row is
off the stone at its end, and a lost second line is worked out again from
the day it was sown (or, failing that, from the letters). The ground's
rings will say the plant was tended rather than cut back: a scraped stone
is no shorter as text.


CREATURES. Slugs, and anything else that grazes, take a little of it, and
only when it is wet: dry, a lichen is a hard bitter crust that nothing eats. A bite takes a trail through the
crust grown this lichen-year along its growing edge (all of this year's
crust, on a powdery one), and never much of it. Last year's crust, the old
crust and its fruit discs are left alone, so grazing slows a lichen but
cannot wear it away; and a colony still a speck, under thirty cells, is
passed over. A bite is written in the rings only when it takes a tenth of
the living crust or more.

A lichen has no flowers (flowers() is always 0), so bees and moths pass it
by, and no creature here carries its pollen: lichens do not cross in this
garden. Its fruit discs make spores, and a spore, like a fragment, carries
its parent's seed whole, variety and all.


THE PLATE shows the stone from above, one square to a cell:

    pale ground            the stone
    solid, planter's ink   living crust
    solid green            crust grown since the last visitor left
    fine paper lines       the years: a line runs wherever crust of one
                           lichen-year meets crust of another, so the rings
                           can be counted from the edge inward, as in a tree
    grey hatching          dead crust (a grey band across each cell)
    a short bar            two cells of crust that touch only at a corner
    the crust's texture    on all its living crust: none on a smooth crust;
                           short pale cracks on a hard one (little plates,
                           the same places on every drawing); on a powdery
                           one a pale prick in each cell, a stipple (in every
                           other cell, on a colony of thousands)
    round dots             fruit discs, in their own colour, with a dark rim,
                           ringed with paper
    the bar and number     a scale, in cells

The caption says how many cells are living and dead, how many lichen-years
its crust spans (from its oldest letter to this year, so a colony that has
not grown yet this year spans one more year than it has rings for), and how
many fruit discs it bears.

The shape is the rule's signature. A table of 1 alone grows thin threads
that fork and wander and never touch; high numbers only (3 and up) fill in a
tight round shield that creeps; a table from 2 up grows faster and rougher,
with holes. The rings are its years, and a short life leaves a ring round a
grey centre. A young colony is small on its stone, and is drawn so: the
stone is part of the plant.
"""

import datetime
import math
import random
import re

import hands

KIND = "lichen"

OFF, STONE, DEAD = 32, 46, 58          # " ", ".", ":" as bytes in a row
FIRST_LETTER = 97                      # "a"
WIDEST, TALLEST = 90, 70               # the largest stone a body holds, in cells (about 6,500 characters)
BODY_MOST = 60_000                     # characters a body may hold in this garden
NOTES_MOST, NOTE_LONGEST = 6, 160      # a hand's own lines kept in a body, and how long each may be
YOUNG = 1                              # crust this many lichen-years old or less still reaches out
CRUSTS = ("smooth", "powdery", "hard")
SEASONS = ("spring", "summer", "autumn", "winter")
DEFAULT_JOINS = frozenset((2, 3))
KEPT = ("kind", "joins", "thirst", "slow", "lives", "crust", "fruit", "variety")   # what a fragment carries on

WINDY = 4.0                            # Beaufort: wind that lifts fragments
SPLASH = 8.0                           # mm: rain heavy enough to splash fragments across the stone
LODGE = {"smooth": 0.012, "powdery": 0.03, "hard": 0.005}      # chance, on such a day, that a fragment lodges on its own stone
CAST = {"smooth": 0.01, "powdery": 0.03, "hard": 0.004}        # chance, on a windy day, that a fragment is cast to a new stone
TENDER = {"smooth": 0.1, "powdery": 0.15, "hard": 0.03}        # how much of a bite's share of its new crust it gives up
BITE_MOST = {"smooth": 4, "powdery": 6, "hard": 2}            # the most cells one bite takes: slugs graze a little
LODGE_FROM, CAST_FROM = 30, 40         # living cells a colony needs before it sheds anything (or is worth a grazer's while)
SPORE_EACH, SPORE_MOST = 0.0005, 0.01  # chance of a spore, for each fruit disc, on a calm dry autumn day
FRUITING = 0.003                       # chance, on an autumn growing day, that a cell of old crust bears a disc
CRUMBLE, CRUMBLE_THAW = 0.004, 0.02    # chance a dead cell crumbles on a wet day; on a day wet ground freezes
HEAL_AROUND = 6                        # a hard crust's bare cell with this many living around it heals
STONE_INK = "#e6e0d3"                  # the stone on the plate
PRICKS_MOST = 3000                     # a powdery colony larger than this is pricked in every other cell
RINGS_MOST = 2500                      # year lines beyond this many strokes are not drawn (only a hand's patchwork has so many)


# ------------------------------------------------------------- reading

def _table() -> bytes:
    """How each byte of a row is read: letters are crust, a space is off the stone, anything unknown is bare stone."""
    table = bytearray([STONE]) * 256
    for byte in b" \t\x0b\x0c":
        table[byte] = OFF
    table[ord(":")] = DEAD
    for byte in list(range(65, 91)) + list(range(97, 123)):
        table[byte] = byte
    return bytes(table)


_READ = _table()
_LIVING = bytes(1 if 65 <= v <= 90 or 97 <= v <= 122 else 0 for v in range(256))
_YEAR_A = re.compile(r"year\s*a\s*began\D{0,12}(\d{4})", re.IGNORECASE)
_SIZE_LINE = re.compile(r"^\s*stone\s*:\s*\d+\s*by\s*\d+", re.IGNORECASE)
_NORTHERN = ("winter", "winter", "spring", "spring", "spring", "summer",
             "summer", "summer", "autumn", "autumn", "autumn", "winter")


class _Stone:
    """A body, read: the stone as one bytearray with a rim of OFF all round, so every cell has eight neighbours."""
    __slots__ = ("w", "h", "stride", "g", "base", "said", "notes")

    def __init__(self, w, h, base=None):
        self.w, self.h, self.stride = w, h, w + 2
        self.g = bytearray([OFF]) * ((w + 2) * (h + 2))
        self.base = base                     # the calendar year in which lichen-year a began, if known
        self.said = base                     # the same, as the body's second line said it
        self.notes = []                      # a hand's own lines, kept below the rows

    def at(self, r, c) -> int:
        return (r + 1) * self.stride + c + 1

    def around(self) -> tuple:
        s = self.stride
        return (-s - 1, -s, -s + 1, -1, 1, s - 1, s, s + 1)

    def row(self, r) -> bytes:
        i = self.at(r, 0)
        return bytes(self.g[i:i + self.w])


def _text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    try:
        return str(value)
    except Exception:
        return ""


def _is_row(line) -> bool:
    at = line.find("|")
    return at >= 0 and not line[:at].strip()


def _notes(text) -> list:
    """A hand's own lines in a body: not a row, not the size line, not the year line, not the dagger. Bounded."""
    notes, base_seen = [], False
    for line in _text(text).splitlines():
        if not line.strip() or _is_row(line) or _SIZE_LINE.match(line) or line.lstrip().startswith(hands.DAGGER):
            continue
        if not base_seen and _YEAR_A.search(line):
            base_seen = True                         # the first such line is the calendar, not a note
            continue
        if len(notes) < NOTES_MOST:
            notes.append(line.rstrip()[:NOTE_LONGEST])
    return notes


def _read(body):
    """A body as a _Stone, or None if no stone can be read in it. Never raises.

    A row is a line whose first mark is a bar; what lies between its first
    bar and its last is the row. Any other line may name year a, and any
    other line still is a hand's note.
    """
    text = _text(body)
    rows, base = [], None
    for line in text.splitlines():
        if _is_row(line):
            if len(rows) < TALLEST:
                inner = line[line.find("|") + 1:]
                end = inner.rfind("|")
                rows.append((inner[:end] if end >= 0 else inner)[:WIDEST])
        elif base is None:
            found = _YEAR_A.search(line)
            if found and 1000 <= int(found.group(1)) <= 9999:
                base = int(found.group(1))
    width = max((len(row) for row in rows), default=0)
    if not width:
        return None
    stone = _Stone(width, len(rows), base)
    for r, row in enumerate(rows):
        cells = row.encode("ascii", errors="replace").translate(_READ)
        i = stone.at(r, 0)
        stone.g[i:i + len(cells)] = cells
    if not any(v != OFF for v in stone.g):
        return None
    stone.notes = _notes(text)
    return stone


def _write(stone, turn) -> str:
    """A _Stone as the text of a body: the size, the calendar, the rows, and a hand's notes."""
    lines = ["stone: %d by %d cells" % (stone.w, stone.h)]
    if stone.base is not None:
        lines.append("year a began: %04d-%02d-01" % (stone.base, turn))
    lines += ["|%s|" % stone.row(r).decode("ascii") for r in range(stone.h)]
    lines += stone.notes
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------- the seed

class _Traits:
    __slots__ = ("joins", "thirst", "slow", "lives", "crust", "fruit")


def _joins(text):
    """The counts a joins line names, as a frozenset of 1..8; None if it names none.

    `3 4 5`, `3-5`, `3..5` and `3 to 5` all mean 3 4 5. Life-like `B36/S23`
    means 3 6: only the birth half, the part before the slash, is ours.
    """
    text = _text(text).lower()
    life_like = re.search(r"\bb\s*([1-8]+)\s*/", text)
    if life_like:
        text = life_like.group(1)
    counts = set()
    for low, high in re.findall(r"([1-8])\s*(?:-|–|\.\.+|to)\s*([1-8])", text):
        counts.update(range(min(int(low), int(high)), max(int(low), int(high)) + 1))
    counts.update(int(ch) for ch in text if ch in "12345678")
    return frozenset(counts) or None


_NO_FRUIT = ("none", "no", "sterile", "-", "nothing", "aucun", "aucune", "sans", "pas")
_NOT_FRUIT_INKS = ("ink", "wood", "fresh", "faint", "dead", "paper")   # the plate's own inks, which mean something else
_COLOUR_WORDS = {"light": "pale", "deep": "dark",                       # English shades, and French words, as the plate names them
                 "rouge": "red", "rose": "pink", "jaune": "yellow", "bleu": "blue", "bleue": "blue",
                 "violette": "violet", "brun": "brown", "brune": "brown", "marron": "brown", "noir": "black",
                 "noire": "black", "blanc": "white", "blanche": "white", "gris": "grey", "grise": "grey",
                 "gray": "grey", "foncé": "dark", "fonce": "dark", "foncée": "dark", "pâle": "pale",
                 "clair": "pale", "claire": "pale"}


def _ink(name):
    """A plate ink's name, or a #rrggbb, if the plate knows it as a colour for fruit; else None."""
    if not name or name in _NOT_FRUIT_INKS:
        return None
    known = hands.mix(name, name)                   # the ink as #rrggbb; the plate's near-black if unreadable
    if known == "#1a1a1a" and name != "#1a1a1a":
        return None
    return known if name.startswith("#") else name


def _colour(text):
    """The fruit's colour as an ink ('#rrggbb' or a plate ink's name), or None for none.

    'dark red' is dark-red, 'light pink' pale-pink, 'rose pâle' pale-pink,
    'reddish brown' brown. A colour the plate does not know is brown.
    """
    words = [w.strip(",;.!?\"'()") for w in re.split(r"[\s_]+", _text(text).strip().lower())]
    words = [w for w in words if w]
    if not words or words[0] in _NO_FRUIT:
        return None
    words = [_COLOUR_WORDS.get(w, w) for w in words]
    tries = ["-".join(words)]
    if len(words) >= 2:
        tries += ["-".join(words[:2]), "-".join(reversed(words[:2]))]    # French puts the shade after
    for name in tries + words:
        ink = _ink(name)
        if ink:
            return ink
    return "brown"


def _traits(seed) -> _Traits:
    if isinstance(seed, str):
        seed = hands.read_keys(seed)
    if not isinstance(seed, dict):
        seed = {}
    t = _Traits()
    t.joins = _joins(hands.line(seed, "joins", "")) or DEFAULT_JOINS
    t.thirst = hands.num(seed, "thirst", 0.2, 0.0, 1.0)
    t.slow = hands.num(seed, "slow", 40.0, 2.0, 100000.0)
    t.lives = int(round(hands.num(seed, "lives", 6, 2, 20)))   # at 1, every cell would die as it first turned a year
    t.crust = hands.word(seed, "crust", "smooth", CRUSTS)
    t.fruit = _colour(hands.line(seed, "fruit", "brown")) if "fruit" in seed else "brown"
    return t


# ----------------------------------------------------- sky and seasons

def _f(thing, name, default=0.0) -> float:
    try:
        value = float(getattr(thing, name, default))
    except Exception:
        return default
    return value if value == value and abs(value) < 1e9 else default


def _date(ctx):
    date = getattr(ctx, "date", None)
    return date if isinstance(date, datetime.date) else None


def _turn(ctx) -> int:
    """The month a lichen-year begins: August, or February where the seasons are the other way round."""
    date = _date(ctx)
    season = _text(getattr(getattr(ctx, "sky", None), "season", "")).strip().lower()
    if date is not None and season in SEASONS and season != _NORTHERN[date.month - 1]:
        return 2
    return 8


def _lichen_year(date, turn) -> int:
    return date.year if date.month >= turn else date.year - 1


def _autumn(ctx, turn) -> bool:
    """The three months after the lichen-year turns: when discs are borne and spores fly."""
    date = _date(ctx)
    return date is not None and (date.month - turn) % 12 in (1, 2, 3)


def _latest_letter(stone, lives=6):
    """The letter (0..25) that is most likely this year's, for a body whose second line was lost.

    The letters go round a circle, so any of them could be this year. Each
    reading is weighed by the crust it keeps alive (younger than `lives`),
    the younger the better, and the heaviest is chosen: a colony is mostly
    young at its edge and old in its middle, and a few letters a hand wrote
    into the stone weigh little against it.
    """
    counts = [0] * 26
    for v in stone.g:
        if _LIVING[v]:
            counts[(v | 32) - FIRST_LETTER] += 1
    if not any(counts):
        return None
    best, choice = None, 0
    for now in range(26):
        weight = sum(n * (1.0 - 0.5 * ((now - k) % 26) / lives)
                     for k, n in enumerate(counts) if n and (now - k) % 26 < lives)
        if best is None or weight > best:
            best, choice = weight, now
    return choice


def _keeps(stone, now, lives) -> float:
    """The share of the living crust that a reading of this year's letter as `now` keeps alive."""
    alive = total = 0
    for v in stone.g:
        if _LIVING[v]:
            total += 1
            alive += (now - ((v | 32) - FIRST_LETTER)) % 26 < lives
    return alive / total if total else 1.0


def _now(stone, ctx, turn, lives=6) -> int:
    """This lichen-year's letter, 0..25. Sets stone.base to the calendar it was read by.

    The second line is trusted unless it is a slip of the hand: a year not
    yet begun, or one that would kill most of the crust where the sowing day
    (ctx.age) would not. Such a line, or a lost one, is worked out again from
    the sowing day if the crust agrees, else from the letters.
    """
    date = _date(ctx)
    if date is None:
        latest = _latest_letter(stone, lives)
        return latest if latest is not None else 0
    year = _lichen_year(date, turn)
    age = getattr(ctx, "age", None)
    sown = None
    if isinstance(age, int) and 0 <= age < 40000:
        sown = _lichen_year(date - datetime.timedelta(days=age), turn)
    if stone.base is not None and stone.base > year:
        stone.base = None                            # a year that has not begun
    if stone.base is not None and sown is not None and stone.base != sown:
        stated = _keeps(stone, (year - stone.base) % 26, lives)
        if stated < 0.5 and _keeps(stone, (year - sown) % 26, lives) > stated:
            stone.base = None                        # it would kill most of the crust, and the sowing day would not
    if stone.base is None:
        if sown is not None and _keeps(stone, (year - sown) % 26, lives) >= 0.5:
            stone.base = sown
        else:
            latest = _latest_letter(stone, lives)
            stone.base = year - (latest if latest is not None else 0)
    return (year - stone.base) % 26


def _warmth(mean) -> float:
    """How a wet lichen likes the day's warmth: best between 5 and 14 degrees, little in frost or heat."""
    points = ((-4.0, 0.0), (0.0, 0.25), (5.0, 1.0), (14.0, 1.0), (20.0, 0.45), (27.0, 0.08))
    if mean <= points[0][0]:
        return 0.0
    for (t0, v0), (t1, v1) in zip(points, points[1:]):
        if mean <= t1:
            return v0 + (v1 - v0) * (mean - t0) / (t1 - t0)
    return points[-1][1]


def _water(sky, traits) -> float:
    """1 if the ground is wet enough; 0.5 if only today's rain wets the stone; 0 if it is dry."""
    if _f(sky, "wet") >= traits.thirst:
        return 1.0
    return 0.5 if _f(sky, "rain") >= 1.0 else 0.0


def _vigour(sky, bed, traits, water) -> float:
    """How well it grows today, 0 .. about 1.6: wetness, warmth, light and the ground's richness."""
    if water <= 0 or _f(sky, "tmax", 10.0) <= 0:
        return 0.0                                   # dry, or frozen all day
    warmth = _warmth((_f(sky, "tmin", 5.0) + _f(sky, "tmax", 10.0)) / 2)
    light = min(1.0, _f(sky, "light", 3.0) / 3.0)
    try:
        if getattr(sky, "snow", False):
            light *= 0.2                             # under snow it is dim
    except Exception:
        pass
    rich = hands.num(bed if isinstance(bed, dict) else {}, "rich", 0.0, 0.0, 1.0)
    return water * warmth * light * (1.0 + 0.6 * rich)


def _draws(rng, n, chance) -> int:
    """How many of n things a chance falls on today: its expected number, the fraction settled by one throw."""
    expected = n * chance
    whole = int(expected)
    return min(n, whole + (1 if rng.random() < expected - whole else 0))


# -------------------------------------------------------- the colony

def _stone_size(seed, rng) -> tuple:
    """The stone a seed asks for, in cells, kept to 8..90 by 6..70. A number too long to be a size is a large one."""
    said = [int(n) if len(n) <= 4 else 9999
            for n in re.findall(r"\d+", hands.line(seed if isinstance(seed, dict) else {}, "stone", ""))]
    w = said[0] if said else rng.randint(40, 56)
    h = said[1] if len(said) > 1 else (rng.randint(28, 40) if not said else w * 3 // 4)
    return max(8, min(WIDEST, w)), max(6, min(TALLEST, h))


def _new_stone(w, h, rng) -> _Stone:
    """A flat stone of about w by h cells, with an uneven edge. Its rows come trimmed to the stone."""
    waves = [(k, rng.uniform(0.02, 0.075), rng.uniform(0.0, 2 * math.pi)) for k in (2, 3, 4, 5)]
    inside = []
    for r in range(h):
        dy = (r + 0.5) / h * 2 - 1
        for c in range(w):
            dx = (c + 0.5) / w * 2 - 1
            theta = math.atan2(dy, dx)
            edge = 0.98 - sum(a * (1 + math.cos(k * theta + phase)) for k, a, phase in waves)
            if math.hypot(dx, dy) <= edge:
                inside.append((r, c))
    rows = [r for r, _ in inside] or [0]
    cols = [c for _, c in inside] or [0]
    top, left = min(rows), min(cols)
    stone = _Stone(max(cols) - left + 1, max(rows) - top + 1)
    for r, c in inside:
        stone.g[stone.at(r - top, c - left)] = STONE
    return stone


def _nucleus(stone, i, letter, rng) -> int:
    """A fragment lodges at cell i: a small cross of crust and one corner. Returns how many cells took."""
    s = stone.stride
    took = 0
    for j in (i, i - 1, i + 1, i - s, i + s, i + rng.choice((-s - 1, -s + 1, s - 1, s + 1))):
        if stone.g[j] == STONE:
            stone.g[j] = letter
            took += 1
    return took


def _clear_spot(stone, rng):
    """A bare cell of the stone with no living crust within two cells, found by a few throws; or None."""
    g = stone.g
    for _ in range(60):
        r, c = rng.randrange(stone.h), rng.randrange(stone.w)
        i = stone.at(r, c)
        if g[i] != STONE:
            continue
        if all(not _LIVING[g[stone.at(rr, cc)]]
               for rr in range(max(0, r - 2), min(stone.h, r + 3))
               for cc in range(max(0, c - 2), min(stone.w, c + 3))):
            return i
    return None


def sprout(seed, ctx) -> str:
    """A new stone, and on it the first fragment of crust, near the middle."""
    rng = getattr(ctx, "rng", None) or random.Random(0)
    w, h = _stone_size(seed, rng)
    stone = _new_stone(w, h, rng)
    turn = _turn(ctx)
    date = _date(ctx)
    stone.base = _lichen_year(date, turn) if date is not None else None
    bare = [(r, c) for r in range(stone.h) for c in range(stone.w) if stone.g[stone.at(r, c)] == STONE]
    if bare:
        mid_r = stone.h / 2 + rng.uniform(-0.12, 0.12) * stone.h
        mid_c = stone.w / 2 + rng.uniform(-0.12, 0.12) * stone.w
        r, c = min(bare, key=lambda rc: (rc[0] + 0.5 - mid_r) ** 2 + (rc[1] + 0.5 - mid_c) ** 2)
        _nucleus(stone, stone.at(r, c), FIRST_LETTER, rng)
    return _write(stone, turn)


def _again(seed, ctx, text) -> str:
    """The body come up again from the seed, on a new stone, with a hand's notes from the old body kept."""
    notes = _notes(text)
    body = sprout(seed, ctx)
    return body + "".join(note + "\n" for note in notes)


def day(body, seed, ctx):
    """One day on the stone. Returns the new body, and a line for the almanac on the rare days worth one."""
    text = _text(body)
    if hands.is_dead(text):
        return (body, None) if len(text) <= BODY_MOST else (text[:BODY_MOST // 2], None)
    if "|" not in text:
        return _again(seed, ctx, text), "came up again from the seed, on a new stone"
    if len(text) > BODY_MOST:                        # a hand pasted in more than a stone can hold
        stone = _read(text)
        if stone is None:
            return _again(seed, ctx, text), "came up again from the seed, on a new stone"
        _now(stone, ctx, _turn(ctx), _traits(seed).lives)
        return _write(stone, _turn(ctx)), None
    traits = _traits(seed)
    sky = getattr(ctx, "sky", None)
    water = _water(sky, traits)
    vigour = _vigour(sky, getattr(ctx, "bed", None), traits, water)
    windy, splash = _f(sky, "wind") >= WINDY, _f(sky, "rain") >= SPLASH
    thaw = _f(sky, "tmin", 5.0) < 0 and _f(sky, "wet") >= 0.3
    if not water and not (windy or splash or thaw):
        return body, None                            # a dry, still day: a lichen rests
    stone = _read(text)
    if stone is None:
        return _again(seed, ctx, text), "came up again from the seed, on a new stone"
    rng = getattr(ctx, "rng", None) or random.Random(len(text))
    turn = _turn(ctx)
    now = _now(stone, ctx, turn, traits.lives)
    g, around = stone.g, stone.around()
    living, young, dying, dead, discs = [], [], [], [], 0
    for i, v in enumerate(g):
        if _LIVING[v]:
            age = (now - ((v | 32) - FIRST_LETTER)) % 26
            living.append(i)
            if age >= traits.lives:
                dying.append(i)
            elif age <= YOUNG:
                young.append(i)
            if v < FIRST_LETTER:
                discs += 1
        elif v == DEAD:
            dead.append(i)
    changed, said = stone.base != stone.said, []     # a calendar lost or put right is written back

    if water and dying:                              # the first wetting of the year: the old crust dies
        for i in dying:
            g[i] = DEAD
        gone = set(dying)
        living = [i for i in living if i not in gone]
        said.append("its oldest crust died back, %d cell%s" % (len(dying), "" if len(dying) == 1 else "s"))
        changed = True

    if dead and (water or thaw):                     # dead crust crumbles back to stone
        for i in rng.sample(dead, _draws(rng, len(dead), CRUMBLE_THAW if thaw else CRUMBLE)):
            g[i] = STONE
            changed = True

    joined = []
    if vigour > 0 and living:
        chance = min(0.95, vigour / traits.slow)
        edge = set()                                 # bare cells beside young crust
        for i in young:
            for d in around:
                if g[i + d] == STONE:
                    edge.add(i + d)
        for j in sorted(edge):
            n = sum(_LIVING[g[j + d]] for d in around)
            if n in traits.joins and rng.random() < chance:
                joined.append(j)
        if traits.crust == "hard":                   # a hard crust heals its scratches and pinholes
            scars = set()                            # a bare cell with six living around it has living crust on
            for i in living:                         # both sides along some line: look one cell across, four ways
                for d in (1, around[5], around[6], around[7]):
                    if g[i + d] == STONE and _LIVING[g[i + 2 * d]]:
                        scars.add(i + d)
            scars = [j for j in sorted(scars - set(joined)) if sum(_LIVING[g[j + d]] for d in around) >= HEAL_AROUND]
            if scars and rng.random() < max(0.5, chance):
                joined += scars                      # a break closes all at once, and is said once
                front = set(young)                   # (notches beside young crust are only its front filling in)
                if sum(1 for j in scars if not any(j + d in front for d in around)) >= 3:
                    said.append("a break in its crust healed over")
        if joined:
            touches = [j for j in joined if any(g[j + d] == OFF for d in around)]
            reached = touches and not any(g[i + d] == OFF for i in living for d in around)
            letter = FIRST_LETTER + now
            for j in joined:
                g[j] = letter
            living += joined
            changed = True
            if reached:
                said.append("reached the edge of its stone")

    if traits.fruit and water and vigour > 0 and _autumn(ctx, turn):
        old = [i for i in living if g[i] >= FIRST_LETTER and (now - (g[i] - FIRST_LETTER)) % 26 >= 2]
        opened = 0
        for i in rng.sample(old, _draws(rng, len(old), FRUITING)):
            if not any(65 <= g[i + d] <= 90 for d in around):
                g[i] -= 32
                opened += 1
        if opened:
            changed = True
            if not discs:                            # (nothing grazes discs, so this is said once, not every autumn)
                said.append("fruit discs opened on its old crust")

    if (windy or splash) and len(living) >= LODGE_FROM and rng.random() < LODGE[traits.crust]:
        spot = _clear_spot(stone, rng)
        if spot is not None and _nucleus(stone, spot, FIRST_LETTER + now, rng):
            said.append("a fragment took hold elsewhere on its stone")
            changed = True

    if not any(_LIVING[v] for v in g):               # died back to the stone, or scraped bare by a hand
        date = _date(ctx)
        return ("† %s, no living crust was left on its stone\n" % (date.isoformat() if date else "")
                + _write(stone, turn)), "died: no living crust was left on its stone"
    if not changed:
        return body, None
    return _write(stone, turn), "; ".join(said[:2]) or None


# ------------------------------------------------ seeds, and creatures

def _child_name(parent, how) -> str:
    base = re.sub(r"-(fragment|spore|seedling|cross)(-[ivxlcdm]+)?$", "", _text(parent)) or "lichen"
    return "%s-%s" % (base[:30].rstrip(" .-"), how)


def _offspring(seed, ctx, how) -> str:
    """A fragment or a spore: the parent's seed carried on, variety and all (the stone is left behind)."""
    keys = {"kind": KIND}
    for key in KEPT:
        if key in seed and key != "kind":
            keys[key] = seed[key]
    where = _text(getattr(ctx, "where", "")) or "a lichen"
    keys["name"] = _child_name(getattr(ctx, "name", ""), how)
    keys["from"] = ("a fragment blown from %s" if how == "fragment" else "a spore of %s") % where
    return hands.write_keys(keys)


def cast(body, seed, ctx) -> list:
    """A fragment on a windy day, or a spore on a calm dry autumn one. Lichens do not cross here: see CREATURES."""
    if hands.is_dead(body) or "|" not in _text(body):
        return []
    seed = seed if isinstance(seed, dict) else hands.read_keys(seed)
    traits = _traits(seed)
    sky = getattr(ctx, "sky", None)
    stone = _read(body)
    if stone is None:
        return []
    living = sum(_LIVING[v] for v in stone.g)
    discs = sum(1 for v in stone.g if 65 <= v <= 90)
    if _f(sky, "wind") >= WINDY and living >= CAST_FROM:
        chance, how = CAST[traits.crust], "fragment"
    elif discs and not _water(sky, traits) and _autumn(ctx, _turn(ctx)):
        chance, how = min(SPORE_MOST, SPORE_EACH * discs), "spore"
    else:
        return []
    rng = getattr(ctx, "rng", None) or random.Random(living)
    if rng.random() >= chance:
        return []
    return [_offspring(seed, ctx, how)]


def flowers(body, seed, ctx) -> int:
    """A lichen has no flowers. Its fruit discs make spores, which no bee or moth carries."""
    return 0


def bitten(body, seed, ctx, share, by):
    """A creature grazes it, on a wet night: a trail through this lichen-year's crust along its growing edge.

    `share` (0..1) is how much of that soft new crust the creature would
    take; a lichen gives up only part of it, and never more than a few
    cells. Dry crust, old crust and fruit discs are not eaten, and a colony
    of fewer than LODGE_FROM cells is passed over. Returns the body, and a
    line only when the bite took a tenth of the living crust or more.
    """
    text = _text(body)
    if hands.is_dead(text):
        return body, None
    traits = _traits(seed)
    if not _water(getattr(ctx, "sky", None), traits):
        return body, None                           # dry, a lichen is a hard bitter crust
    try:
        share = min(1.0, max(0.0, float(share)))
    except Exception:
        return body, None
    if share != share or share <= 0:
        return body, None
    stone = _read(text)
    if stone is None:
        return body, None
    rng = getattr(ctx, "rng", None) or random.Random(len(text))
    turn = _turn(ctx)
    now = _now(stone, ctx, turn, traits.lives)
    g, around = stone.g, stone.around()
    this_year = FIRST_LETTER + now
    living, soft = 0, set()
    for i, v in enumerate(g):
        if not _LIVING[v]:
            continue
        living += 1
        if v == this_year and (traits.crust == "powdery" or any(not _LIVING[g[i + d]] for d in around)):
            soft.add(i)
    if living < LODGE_FROM or not soft:
        return body, None                           # a speck, or nothing new to graze
    wanted = min(BITE_MOST[traits.crust], _draws(rng, len(soft), share * TENDER[traits.crust]))
    if wanted < 1:
        return body, None
    trail, eaten = None, 0
    while eaten < wanted and soft:
        if trail is None or trail not in soft:
            trail = rng.choice(sorted(soft))
        soft.discard(trail)
        g[trail] = STONE
        eaten += 1
        onward = [trail + d for d in around if trail + d in soft]
        trail = rng.choice(onward) if onward else None
    event = None
    if eaten * 10 >= living:
        who = _text(by).strip() or "something"
        event = "%s grazed off %d cells of its new crust" % (who, eaten)
    return _write(stone, turn), event


# ------------------------------------------------------ describe, draw

def _counts(stone, now):
    living = dead = discs = 0
    years = set()
    for v in stone.g:
        if _LIVING[v]:
            living += 1
            years.add((now - ((v | 32) - FIRST_LETTER)) % 26)
            discs += v < FIRST_LETTER
        elif v == DEAD:
            dead += 1
    return living, dead, discs, (max(years) + 1 if years else 0)


def describe(body, seed, ctx) -> str:
    stone = _read(body)
    if stone is None:
        return "a bare stone"
    now = _now(stone, ctx, _turn(ctx), _traits(seed).lives)
    living, dead, discs, years = _counts(stone, now)
    if hands.is_dead(body):
        return "dead; %d cells of crust are left on its stone" % (living + dead)
    words = "%d living cell%s" % (living, "" if living == 1 else "s")
    if years > 1:
        words += " from %d lichen-years" % years
    if dead:
        words += ", %d dead" % dead
    if discs:
        words += ", %d fruit disc%s" % (discs, "" if discs == 1 else "s")
    return words


def size(body, seed) -> float:
    """For its dot on the plan: its living cells, as a moss tells its own. (Its body is its whole stone, a speck
    and a shield alike, so the body's length says nothing of the crust.)"""
    stone = _read(body)
    return 0.0 if stone is None else float(sum(1 for v in stone.g if _LIVING[v]))


def _crack(r, c):
    """Where a hard crust is cracked, and which way: 'upright', 'level' or None. A fixed pattern of the stone."""
    k = ((r * 92821) ^ (c * 68917) ^ (r * c * 131)) % 10
    return "upright" if k < 2 else "level" if k < 4 else None


def draw(body, seed, ctx, pen) -> None:
    """The stone from above, one square to a cell. The docstring's last section says what each mark means."""
    pen.unit_name = "cell, cells"
    pen.align = "center"
    pen.unit_px_max = 48
    stone = _read(body)
    if stone is None:
        pen.note("no stone can be read in its body")
        return
    traits = _traits(seed)
    gone = hands.is_dead(body)
    now = _now(stone, ctx, _turn(ctx), traits.lives)
    left = getattr(ctx, "left", None)
    before = _read(left) if left is not None else None
    g, h, w = stone.g, stone.h, stone.w
    was_row = _matching_rows(stone, before)

    def was_living(r, c) -> bool:
        k = was_row[r]
        if before is None or k is None or c >= before.w:
            return False
        return bool(_LIVING[before.g[before.at(k, c)]])

    # what each cell is drawn as: 0 off the stone, 1 bare, 2 dead, 3 living, 5 new since the last visit;
    # and for living crust, its year (the letter), for the rings
    rows, years = [], []
    for r in range(h):
        codes, marks = [], []
        for c in range(w):
            v = g[stone.at(r, c)]
            year = -1
            if v == OFF:
                codes.append(0)
            elif v == DEAD or (gone and _LIVING[v]):
                codes.append(2)
            elif not _LIVING[v]:
                codes.append(1)
            else:
                codes.append(3 if was_living(r, c) else 5)
                year = v | 32
            marks.append(year)
        rows.append(codes)
        years.append(marks)

    for r, codes in enumerate(rows):                      # the stone first, under everything
        y = h - 1 - r
        for c0, c1, code in _runs(codes):
            if code:
                pen.cell(c0, y, c1 - c0, 1, STONE_INK)
    for r, codes in enumerate(rows):                      # living crust solid, dead crust hatched
        y = h - 1 - r
        for c0, c1, code in _runs(codes):
            if code == 3:
                pen.cell(c0, y, c1 - c0, 1, "wood")
            elif code == 5:
                pen.cell(c0, y, c1 - c0, 1, "fresh")
            elif code == 2:
                pen.cell(c0, y + 0.32, c1 - c0, 0.36, "dead")

    box = getattr(pen, "box", None) or (60, 50, 840, 930)
    try:
        across = min(float(getattr(pen, "unit_px_max", 48) or 48),
                     (float(box[2]) - float(box[0]) - 6) / w, (float(box[3]) - float(box[1]) - 36) / h)
    except Exception:
        across = 14.0                                     # about how many pixels a cell will be on the plate

    # Where two cells of living crust touch only at a corner, a short bar across the corner shows they are joined.
    for r in range(h - 1):
        for c in range(w):
            here = rows[r][c]
            if here < 3:
                continue
            for dc in (-1, 1):
                if 0 <= c + dc < w and rows[r + 1][c + dc] >= 3 and rows[r][c + dc] < 3 and rows[r + 1][c] < 3:
                    ink = "fresh" if 5 in (here, rows[r + 1][c + dc]) else "wood"
                    px, py = c + (1 if dc > 0 else 0), h - 1 - r
                    pen.line(px - 0.3 * dc, py + 0.3, px + 0.3 * dc, py - 0.3, max(2.0, 0.45 * across), ink)

    if not gone:
        _texture(pen, traits.crust, rows, h, w)
        _rings(pen, rows, years, h, w)

    radius = max(3.0, 0.3 * across)
    for r in range(h):
        for c in range(w):
            if 65 <= g[stone.at(r, c)] <= 90:
                x, y = c + 0.5, h - 1 - r + 0.5
                pen.dot(x, y, radius + 2.5, "paper")
                if gone:
                    pen.dot(x, y, radius, "dead")
                else:
                    pen.dot(x, y, radius + 1.0, "ink")    # a dark rim, so a disc shows on crust of its own colour
                    pen.dot(x, y, radius, traits.fruit or "ink")
    pen.note(describe(body, seed, ctx))


def _texture(pen, crust, rows, h, w) -> None:
    """The crust's trait on all its living crust: pale cracks on a hard one, a pale prick in each cell of a powdery one."""
    if crust == "powdery":
        cells = [(r, c) for r in range(h) for c in range(w) if rows[r][c] >= 3]
        every = len(cells) <= PRICKS_MOST
        for r, c in cells:
            if every or (r + c) % 2 == 0:
                pen.cell(c + 0.37, h - 1 - r + 0.37, 0.26, 0.26, "paper")
    elif crust == "hard":
        for r in range(h):
            for c in range(w):
                if rows[r][c] >= 3:
                    way = _crack(r, c)
                    if way == "upright":
                        pen.cell(c + 0.44, h - 1 - r + 0.2, 0.12, 0.6, STONE_INK)
                    elif way == "level":
                        pen.cell(c + 0.2, h - 1 - r + 0.44, 0.6, 0.12, STONE_INK)


def _rings(pen, rows, years, h, w) -> None:
    """A fine paper line along every edge where living crust of one lichen-year meets crust of another.

    Edges in a line are drawn as one stroke. A body a hand has made into a
    patchwork of years may ask for more strokes than a plate can carry; then
    no rings are drawn, rather than some of them.
    """
    strokes = []
    for r in range(h - 1):                                # level edges, between row r and the row below it
        start = None
        for c in range(w + 1):
            meet = c < w and years[r][c] >= 0 and years[r + 1][c] >= 0 and years[r][c] != years[r + 1][c]
            if meet and start is None:
                start = c
            elif not meet and start is not None:
                strokes.append((start, h - 1 - r, c, h - 1 - r))
                start = None
    for c in range(w - 1):                                # upright edges, between column c and the one to its right
        start = None
        for r in range(h + 1):
            meet = r < h and years[r][c] >= 0 and years[r][c + 1] >= 0 and years[r][c] != years[r][c + 1]
            if meet and start is None:
                start = r
            elif not meet and start is not None:
                strokes.append((c + 1, h - start, c + 1, h - r))
                start = None
        if len(strokes) > RINGS_MOST:
            break
    if len(strokes) > RINGS_MOST:
        pen.note("its years are too many and too mixed to draw as rings")
        return
    for x1, y1, x2, y2 in strokes:
        pen.line(x1, y1, x2, y2, 2.0, "paper")


def _matching_rows(stone, before) -> list:
    """For each row of the stone, the row of the body as the last visitor left it that it is to be compared with.

    A row found there unchanged is that row, wherever it now stands; the
    others keep the offset of the nearest such row above them. So a hand
    that added or took away a whole line does not make the rest of the
    stone look newly grown: the fresh ink is for what grew.
    """
    if before is None:
        return [None] * stone.h
    waiting = {}
    for k in range(before.h):
        waiting.setdefault(before.row(k), []).append(k)
    found = []
    for r in range(stone.h):
        same = waiting.get(stone.row(r))
        found.append(same.pop(0) if same else None)
    offset, matched = 0, []
    for r, k in enumerate(found):
        if k is not None:
            offset = k - r
        else:
            k = r + offset
        matched.append(k if 0 <= k < before.h else None)
    return matched


def _runs(codes):
    """(start, end, code) for each stretch of equal codes in a row."""
    start = 0
    for c in range(1, len(codes) + 1):
        if c == len(codes) or codes[c] != codes[start]:
            yield start, c, codes[start]
            start = c
