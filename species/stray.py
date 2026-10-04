r"""
Stray: an annual that comes up where it likes.

A stray lives one season. Its seed lies in the ground until a spring day
warm enough to wake it; then it comes up, grows a stem with a leaf at every
length, branches, buds, flowers, sets its seed heads, sheds its seed on dry
days, and dies. The seed that takes lies in the ground in its turn, through
the winter, and wakes where it fell: often beside its parent, sometimes in
the wild corner, sometimes wherever a bird left it. After a few years the
strays of a shady bed and of a sunny one are no longer quite the same, and
whatever the visitors kept or weeded has had its say.


THE SEED, line by line (a line left out takes the value in brackets)

    kind: stray
    colour: #d8321f    the colour of its flowers (red). A #rrggbb, or plain
                       words: red, dark red, pink, pale pink, orange, yellow,
                       blue, violet, purple, brown, green, cream, white,
                       black, grey, or the same in French (rouge, rose,
                       jaune, bleu, vert, blanc, noir, gris...), with pale,
                       light, dark or deep before them, or clair or foncé
                       after. Two colour words are blended. Words it cannot
                       read give red. The garden's own inks are not for
                       flowers: a colour close to the fresh green, the dead
                       grey or the faint guide is moved away from it, so that
                       a flower never looks new or dead.
    petals: 4          how many petals each flower opens (5; 3..12)
    tall: 10           the lengths its stem grows before it buds (10; 3..30).
                       A branch grows half as far, and one high on the stem
                       only about as far as the stem's top.
    wakes: 7           the warmth of the ground, in degrees, that wakes the
                       seed in spring (8; 2..20)
    leaf: bristly      plain, downy, waxy or bristly (plain)
    scent: dusk        optional (none). A stray scented at dusk (or at night,
                       or in the evening) keeps the evening's hours. Its
                       flowers are drawn shut by day, and pollen carried by
                       day neither sets its seed nor comes from it: whatever
                       crosses it comes by night, and the moths come for its
                       scent. (The garden does not yet tell a stray who is
                       asking, so a creature of the day may still count its
                       flowers; what it carries of them comes to nothing.)
                       Scent lives only in the text.
    variety: <name>    optional, and a visitor's to give. Seed a stray sheds
                       by itself carries the name on; a cross drops it.

Every seed a stray sheds is its parent's seed shifted a little: `tall` and
`wakes` by a fraction, the colour by a shade, now and then a petal more or
less, and very rarely another kind of leaf. On a day when bees or moths have
brought the pollen of another stray to one of its open flowers, most of the
seed it sheds that day is a cross: the parents' numbers are averaged, their
colours blended, and each other trait comes from one parent or the other.
(A stray cannot keep pollen in its body until its seed is ripe, so a cross
needs an open flower to take the pollen and a ripe head to shed seed on the
same day, which a branched stray often has.) Such a seedling's tag says
`cross of <mother> × <father>`.


WHAT A STRAY DOES, and what its traits do

A seed may wake on any spring day when the ground is at least `wakes`
degrees and not dust-dry, and the warmer past that mark the likelier, so
the seeds of one parent come up over weeks rather than on one day. The
ground of a shaded bed warms more slowly than the air above it, so a seed
there wakes later, or not at all that year. A seed that has lain two years
unwoken is gone, and in sodden winter ground a seed may rot. A packet sown
in autumn waits the winter out like any other seed.

A plant grows a length at a time at each growing tip, faster in warmth,
light and moist ground, and faster still in ground made rich. Every length
bears a leaf, left and right by turns, and leaves feed the growing: a plant
that has lost its leaves grows slowly. On hot bright days in dry ground it
drops a lower leaf. Once its stem is two fifths grown it may break
branches from the axils of its leaves (more in a sunny bed, and in rich
ground). A shoot that has reached its length buds; a bud opens; a flower
sets a head after some days (sooner in a downpour, which beats the petals
down); the head ripens brown; and on dry days a ripe head sheds its seed,
more of it in the wind. Once the days after midsummer have shortened by an
eighth (about the twentieth of August, at this garden's latitude), every
growing tip buds where it stands. A stray dies when nothing on it is
growing, in bud, in flower or holding seed; a hard frost kills it sooner,
and none lives into winter.

    tall     a tall stray has more leaves and branches to flower on, but
             takes longer to reach its buds. In the shade it grows slowly,
             so a tall one there flowers late, when the shortening days
             hurry it, and sets little. A gale snaps tall stems.
    wakes    a seed that wakes early has the longest summer, if a late
             frost does not kill it as a seedling (a seedling takes less
             frost than a grown plant). A seed that waits for more warmth
             than its bed's spring gives may lie there another year.
    leaf     plain leaves grow fastest. Downy ones take two degrees more
             frost. Waxy ones hold out in drought. Bristly stems are half
             as good to slugs, and nothing else that browses will touch
             them.

Most seed that falls is lost. A few seeds take: each becomes a new plant,
a seed in the ground, placed by the days. Fewer take as the strays of the
parent's bed, grown or lying as seed, grow in number, and none once they
fill a third of the bed's room. Seed the days carry to another bed (the
wild corner, most often) is not held back as it falls; but wherever the
strays living in a bed are more than a third of its room, some of the seed
lying there perishes, a little at a time, until they are not. A ripe head
still full when winter comes is shaken empty on its first day, and then
the stray dies.

What creatures do to it: slugs eat seedlings whole, and the lower leaves
of a grown stray. Anything else that bites it and only nibbles takes now
and then the young leaf at a growing tip; a bite of a fifth or more (a
pony) crops the stray flat from the top, and it may
break again below the cut.


THE BODY

A seed in the ground is one line:

    a seed in the ground since 2026-10-04

A stray that has come up is one line for its state, one line for each
shoot, and a last line for its seed:

    in flower, going to seed · came up 2027-04-11
    stem         \/\/\/\/\/\/*
    left at 5    \/\/@14
    right at 8   \/*
    right at 10  |/o
    shed 41 seeds · 3 on 2027-08-12

The first line says what it is doing (a seedling, in leaf, in bud, in
flower, going to seed; standing, when every tip has been cut) and when it
came up; the stray rewrites it each day. `stem` grows from the ground.
`left at 5` is a branch from the fifth length of the stem, going left (a
branch breaks from the axil of a leaf, so it goes the way that leaf went).
Each character after the name is one length, from the bottom up:
    \    a length with its leaf, to the left
    /    a length with its leaf, to the right
    |    a length whose leaf is gone (eaten, or dropped in drought)
Every shoot's first leaf is to the left, and then they take turns.
The mark at the end of a shoot is its tip:
    ^    still growing
    o    a bud
    *    an open flower
    @    a seed head, still unripe; `@14` a ripe head with 14 seeds still
         in it; `@0` an empty one
    x    cut: the shoot grows no further
The last line counts the seed shed so far, and how many fell on the last
day any did.

When the stray dies, a dead mark is set above its first line
(`† 2027-09-02, went to seed`) and the rest stays as it stood, until the
days carry it to the heap.


TO CUT IT (the texture for the hand: a soft herb, one plain line to a
shoot, which parts anywhere)

    Shorten a shoot's characters and the shoot is cut there: it loses its
    tip and everything above, and grows no more. On the stem, the branches
    above the cut go with it. Anything written in among a shoot's lengths
    parts it there, as a cut would: a shoot is its first unbroken run.
    Take off a flower (`*`) or a head (`@`) and that shoot is cut there.
    A stray whose stem has been cut, before the days shorten, breaks a new
    branch from the highest leaf below the cut and flowers again, once
    nothing else on it is growing, flowering or ripening seed: so
    deadheading keeps it flowering, and a head taken unripe is seed that
    never falls.
    Change a leaf to `|` and the leaf is stripped.
    Delete a branch's line and the branch is gone.
    Empty the body, or take away the stem, and the stray is cut to the
    ground: a seed of it lies there still, and waits for spring.
    To be rid of it, pull it: move its folder to the heap.


THE PLATE (one length is one unit; the scale bar says how many)

    a dot below the ground line     a seed in the ground
    the upright line                the stem
    a slanting line                 a branch. It leaves the stem steeper
                                    low down and turns upward a little
                                    with each length: the bend says only
                                    how long it is
    a pointed outline               a leaf, on the side it grows. The leaf
                                    under a branch stands out flatter, and
                                    the branch rises from above it
    a stub ending in a knob         where a leaf was, and is gone
    stipple inside a leaf           down (leaf: downy)
    a doubled outline               wax (leaf: waxy)
    fine ticks along the stems      bristles (leaf: bristly)
    a small open v at a tip         a growing tip
    a ring with a slit of colour    a bud, showing the colour it will open
    petals round a dark eye         an open flower, one round petal or ray
                                    for each of its petals. A flower (or a
                                    bud's slit) too pale to show on the
                                    paper is edged in the ink of its shoot
    a narrow furled stroke          a flower of the dusk, shut at the hour
                                    the plate was drawn
    an oval with a flat crown       a seed head: in the ink of its shoot
                                    while unripe; brown when ripe, with a
                                    dot for each seed still in it, lying
                                    from the bottom; empty when it has
                                    shed all
    a slash across a shoot's end    a cut
    the fresh green                 lengths, leaves and bristles grown since
                                    the last visit (a seed new since then
                                    is fresh)
    all in the dead grey            the stray is dead, standing as it died

The colour of the flowers and buds is the seed's `colour:` line, so a cross
shows its parentage in its petals. Flowers, buds and heads are drawn at a
size the eye can read however tall the stray has grown; the scale bar
measures its stems and leaves.
"""

import datetime
import math
import re

import hands

KIND = "stray"

TEXTURES = ("plain", "downy", "waxy", "bristly")
EVENING = ("dusk", "night", "evening")         # scents that open the flowers at dusk
NIGHT_CARRIERS = ("moth", "night")             # carriers of pollen whose name says they fly by night
DEFAULT_COLOUR = "#d1342b"
PAPER = "#fbf8f1"                              # the plate's paper, to know a flower too pale to show on it
SHORTENED = 0.875                              # the share of midsummer's daylength below which every tip buds
NIBBLE = 0.2                                   # a bite smaller than this takes leaves; a larger one crops the stem
CROWD_PACE = 0.01                              # how fast seed lying in a crowded bed perishes (see _crowded_out)
STEM_MOST = 40            # lengths a stem may have (a hand may write more; they are not read)
BRANCH_MOST = 24          # lengths a branch may have
BRANCHES_MOST = 8         # branches a stray may carry
SEEDS_MOST = 20           # seeds a ripe head may hold
SEED_DAYS = 730           # days a seed may lie in the ground unwoken: two springs, near enough
TAKES = 0.07              # the chance that one seed shed into an uncrowded bed takes
LABEL_WIDTH = 13          # the shoots' names are padded to this, so that their lengths line up

_DATE = re.compile(r"(\d{4})-(\d{1,2})-(\d{1,2})")
_STEM = re.compile(r"^\s*stem\b\s*:?(.*)$", re.IGNORECASE)
_BRANCH = re.compile(r"^\s*(left|right)\s+at\s+(\d{1,4})\s*:?(.*)$", re.IGNORECASE)
_RUN = re.compile(r"[\\/|]+")
_TIP = re.compile(r"\s*(\^|[oO]|\*|[xX]|@\s*(\d{0,4}))")
_COUNT = re.compile(r"(\d{1,6})")


# ------------------------------------------------------------------ the plant as text

class Shoot:
    """One shoot: the stem, or a branch from one of the stem's lengths."""

    __slots__ = ("side", "at", "nodes", "tip", "seeds")

    def __init__(self, side="stem", at=0, nodes="", tip="^", seeds=-1):
        self.side = side          # "stem", "left" or "right"
        self.at = at              # the length of the stem a branch leaves from; 0 for the stem
        self.nodes = nodes        # one character a length: \ leaf to the left, / to the right, | bare
        self.tip = tip            # ^ growing, o bud, * flower, @ head, x cut
        self.seeds = seeds        # a head's seeds: -1 while it is unripe, else how many are still in it

    @property
    def key(self):
        return (self.side, self.at)

    def label(self) -> str:
        return "stem" if self.side == "stem" else "%s at %d" % (self.side, self.at)

    def mark(self) -> str:
        if self.tip == "@":
            return "@" if self.seeds < 0 else "@%d" % self.seeds
        return self.tip

    @property
    def leaves(self) -> int:
        return sum(1 for c in self.nodes if c in "\\/")


class Stray:
    """A stray as its body tells it. A stray with no shoots is a seed in the ground."""

    def __init__(self):
        self.dead = ""            # the dead mark, if the first line is one
        self.shoots = []
        self.since = None         # a seed: the day it came to lie in the ground
        self.up = None            # the day it came up
        self.shed = 0             # seed shed in all
        self.shed_now = 0         # seed shed on the day shed_on
        self.shed_on = None
        self.spoke_of_a_plant = False   # the text said "came up": a plant stood here

    @property
    def is_seed(self) -> bool:
        return not self.shoots

    @property
    def stem(self):
        return self.shoots[0] if self.shoots else None

    @property
    def branches(self) -> list:
        return self.shoots[1:]

    def tips(self, which) -> list:
        return [s for s in self.shoots if s.tip in which]

    @property
    def lengths(self) -> int:
        return sum(len(s.nodes) for s in self.shoots)

    @property
    def leaves(self) -> int:
        return sum(s.leaves for s in self.shoots)


def _as_text(body) -> str:
    if body is None:
        return ""
    if isinstance(body, (bytes, bytearray)):
        return bytes(body).decode("utf-8", errors="replace")
    try:
        return str(body)
    except Exception:
        return ""


def _date(text):
    """The first date written in a text, or None."""
    found = _DATE.search(text or "")
    if not found:
        return None
    try:
        return datetime.date(int(found.group(1)), int(found.group(2)), int(found.group(3)))
    except ValueError:
        return None


def _shoot_from(side, at, text):
    """A shoot from what follows its name: the first run of lengths, and the tip right after it."""
    nodes, tip, seeds = "", "x", -1
    run = _RUN.search(text)
    rest = text
    if run:
        nodes = run.group(0)
        rest = text[run.end():]
    elif not text.strip():
        rest = ""
    found = _TIP.match(rest)
    if found:
        mark = found.group(1)[0]
        tip = {"O": "o", "X": "x"}.get(mark, mark)
        if tip == "@" and found.group(2):
            seeds = min(SEEDS_MOST, int(found.group(2)))
    most = STEM_MOST if side == "stem" else BRANCH_MOST
    return Shoot(side, at, nodes[:most], tip, seeds)


def read(body) -> Stray:
    """A body as a Stray. Reads what it can, skips what it cannot, never raises."""
    p = Stray()
    stem, branches = None, {}
    first = True
    for raw in _as_text(body).splitlines():
        line = raw.strip()
        if not line:
            continue
        if first:
            first = False
            if line.startswith("†"):
                p.dead = line[:200]
                continue
        low = line.lower()
        found = _STEM.match(line)
        if found:
            if stem is None:
                stem = _shoot_from("stem", 0, found.group(1))
            continue
        found = _BRANCH.match(line)
        if found:
            side, at = found.group(1).lower(), int(found.group(2))
            if (side, at) not in branches and len(branches) < 40:
                branches[(side, at)] = _shoot_from(side, at, found.group(3))
            continue
        if "seed in the ground" in low:
            p.since = _date(line) or p.since
        elif low.startswith("shed"):
            numbers = _COUNT.findall(low.split("·")[0])
            p.shed = int(numbers[0]) if numbers else 0
            if "·" in line:
                after = line.split("·", 1)[1]
                count = _COUNT.search(after)
                p.shed_now = int(count.group(1)) if count else 0
                p.shed_on = _date(after)
        if "came up" in low:
            p.up = _date(line) or p.up
            p.spoke_of_a_plant = True
    if stem is not None and (stem.nodes or stem.tip == "^"):
        top = len(stem.nodes)
        kept = [b for key, b in sorted(branches.items(), key=lambda item: (item[0][1], item[0][0]))
                if 1 <= b.at <= top]
        p.shoots = [stem] + kept[:BRANCHES_MOST]
    elif stem is not None:
        p.spoke_of_a_plant = True             # a stem of nothing: it was cut to the ground
    return p


def status(p) -> str:
    """The first line's words: what the plant is doing."""
    if p.is_seed:
        return "a seed in the ground"
    stem = p.stem
    if len(p.shoots) == 1 and len(stem.nodes) <= 3 and stem.tip == "^":
        return "a seedling"
    words = []
    if p.tips("*"):
        words.append("in flower")
    elif p.tips("o"):
        words.append("in bud")
    elif p.tips("^"):
        words.append("in leaf")
    heads = p.tips("@")
    if heads:
        if any(h.seeds != 0 for h in heads):
            words.append("going to seed")
        elif not words:
            words.append("gone to seed")
    return ", ".join(words) or "standing"


def write(p) -> str:
    """A Stray as its body's text: the other way round from read()."""
    if p.is_seed:
        lines = ["a seed in the ground since %s" % (p.since.isoformat() if p.since else "a day no one wrote down")]
    else:
        lines = [status(p) + (" · came up %s" % p.up.isoformat() if p.up else "")]
        width = max(LABEL_WIDTH, max(len(s.label()) for s in p.shoots) + 1)
        for s in p.shoots:
            lines.append(s.label().ljust(width) + s.nodes + s.mark())
        if p.shed or p.shed_on:
            lines.append("shed %d seed%s" % (p.shed, "" if p.shed == 1 else "s")
                         + (" · %d on %s" % (p.shed_now, p.shed_on.isoformat()) if p.shed_on else ""))
    if p.dead:
        lines.insert(0, p.dead)           # set above the rest, which stays as it stood (and still says when it came up)
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ the seed's traits

class Traits:
    """What a seed says, read forgivingly."""

    def __init__(self, seed):
        seed = seed if isinstance(seed, dict) else hands.read_keys(_as_text(seed))
        self.colour = _colour(seed)
        self.petals = int(round(hands.num(seed, "petals", 5, 3, 12)))
        self.tall = hands.num(seed, "tall", 10, 3, 30)
        self.wakes = hands.num(seed, "wakes", 8, 2, 20)
        self.leaf = hands.word(seed, "leaf", "plain", TEXTURES)
        self.scent = hands.word(seed, "scent", "")
        self.variety = hands.line(seed, "variety", "")

    @property
    def evening(self) -> bool:
        return self.scent in EVENING


# Plain words for a flower's colour, in English and French, as one of the plate's inks or a #rrggbb.
# The plate's own names (red, dark-red, pale-pink ...) are read as well; its reserved inks are not.
COLOUR_WORDS = {
    "red": "red", "rouge": "red", "scarlet": "red", "écarlate": "red",
    "crimson": "#a3172f", "cramoisi": "#a3172f", "cramoisie": "#a3172f",
    "pink": "pink", "rose": "pink",
    "orange": "orange",
    "yellow": "yellow", "jaune": "yellow",
    "blue": "blue", "bleu": "blue", "bleue": "blue",
    "violet": "violet", "violette": "violet", "purple": "violet", "pourpre": "violet", "mauve": "#b07cc6",
    "brown": "brown", "brun": "brown", "brune": "brown", "marron": "brown",
    "green": "#8fb03c", "vert": "#8fb03c", "verte": "#8fb03c",       # a flower's green: yellower than the fresh ink
    "cream": "#f4ecd2", "crème": "#f4ecd2", "creme": "#f4ecd2",
    "white": "white", "blanc": "white", "blanche": "white",
    "black": "black", "noir": "black", "noire": "black",
    "grey": "grey", "gray": "grey", "gris": "grey", "grise": "grey",
}
PALER = ("pale", "light", "pâle", "clair", "claire", "pastel", "soft")
DARKER = ("dark", "deep", "foncé", "foncée", "fonce", "sombre")
KEPT_INKS = (("#2e9e3f", 90.0, (1.0, 0.4, -0.6)),     # fresh: what has grown since the last visit
             ("#9a948a", 40.0, (-1.0, -1.0, -1.0)),   # dead
             ("#c9c4b8", 30.0, (1.0, 1.0, 1.0)))      # faint: the guides
# (each: the ink, how far a flower's colour keeps from it, and which way it moves if it is that very ink)
_HEX = re.compile(r"(#)?\b([0-9a-f]{6}|[0-9a-f]{3})\b")
_WORD = re.compile(r"[a-zà-ÿ]+")


def _ink(name):
    """The #rrggbb of a plate ink's name or of a colour written as hex, or None if it is neither."""
    one, other = hands.mix(name, "#000000", 0.0), hands.mix(name, "#ffffff", 0.0)
    return one if name and one == other else None


def _colour(seed) -> str:
    """The flowers' colour as #rrggbb: the seed's `colour:` if it can be read, else a plain red.

    Kept clear of the plate's reserved inks, so that a flower never looks new or dead.
    """
    said = hands.line(seed, "colour", "") or hands.line(seed, "color", "") or hands.line(seed, "couleur", "")
    return _parted(_colour_of(said) or DEFAULT_COLOUR)


def _colour_of(said):
    """What a `colour:` line says, as #rrggbb, or None if it says nothing that can be read.

    A hex colour anywhere on the line wins (with or without its #; without it,
    only if it has a figure in it, so that `decade` is not taken for one).
    Otherwise the colour words on the line are blended, and pale or dark
    words lighten or darken them: `pale pink` and `dark red` are the plate's
    own pale-pink and dark-red.
    """
    text = _as_text(said).lower()
    for found in _HEX.finditer(text):
        digits = found.group(2)
        if found.group(1) or (len(digits) == 6 and any(c.isdigit() for c in digits)):
            return _ink("#" + digits)
    words = _WORD.findall(text.replace("-", " ").replace("_", " "))
    names = [COLOUR_WORDS[w] for w in words if w in COLOUR_WORDS][:3]
    if not names:
        return None
    paler, darker = any(w in PALER for w in words), any(w in DARKER for w in words)
    if len(names) == 1 and (paler or darker):
        own = _ink(("pale-" if paler else "dark-") + names[0])      # pale-pink, dark-red: the plate has them
        if own and not (paler and darker):
            return own
    colour = _ink(names[0])
    for n, name in enumerate(names[1:], start=2):
        colour = hands.mix(colour, _ink(name), 1.0 / n)          # an even blend of every colour named
    if paler and not darker:
        colour = hands.mix(colour, "#ffffff", 0.5)
    elif darker and not paler:
        colour = hands.mix(colour, "#000000", 0.4)
    return colour


def _parted(colour) -> str:
    """A colour moved away from the plate's reserved inks, if it lies too close to one of them."""
    colour = hands.mix(colour, colour, 0.0)
    rgb = [int(colour[i:i + 2], 16) for i in (1, 3, 5)]
    for _ in range(3):                                    # moving away from one may bring it near another
        moved = False
        for kept, far, away in KEPT_INKS:
            ref = [int(kept[i:i + 2], 16) for i in (1, 3, 5)]
            apart = [a - b for a, b in zip(rgb, ref)]
            distance = math.sqrt(sum(d * d for d in apart))
            if distance >= far:
                continue
            if distance < 1.0:
                apart, distance = list(away), math.sqrt(sum(d * d for d in away))
            rgb = [max(0, min(255, int(round(b + d * far / distance)))) for b, d in zip(ref, apart)]
            moved = True
        if not moved:
            break
    return "#%02x%02x%02x" % tuple(rgb)


def _pale(colour) -> bool:
    """Whether a flower of this colour would hardly show on the plate's paper without an edge."""
    colour, paper = hands.mix(colour, colour, 0.0), PAPER
    return sum(abs(int(colour[i:i + 2], 16) - int(paper[i:i + 2], 16)) for i in (1, 3, 5)) < 110


def _shifted(colour, rng) -> str:
    """A colour moved by a shade: each of red, green and blue a little up or down."""
    colour = hands.mix(colour, colour, 0.0)
    try:
        parts = [int(colour[i:i + 2], 16) for i in (1, 3, 5)]
    except ValueError:
        return colour
    return "#%02x%02x%02x" % tuple(max(0, min(255, v + int(round(rng.gauss(0.0, 4.0))))) for v in parts)


def _seed_text(mother, rng, father=None, cross=None) -> str:
    """The text of one seed shed by a stray whose traits are `mother`; a cross if a father is given."""
    one = father or mother

    def either(a, b):
        return a if rng.random() < 0.5 else b

    tall = (mother.tall + one.tall) / 2.0 + rng.gauss(0.0, 0.5)
    wakes = (mother.wakes + one.wakes) / 2.0 + rng.gauss(0.0, 0.35)
    colour = _shifted(hands.mix(mother.colour, one.colour, 0.5), rng)
    petals = either(mother.petals, one.petals)
    if rng.random() < 0.06:
        petals += rng.choice((-1, 1))
    leaf = either(mother.leaf, one.leaf)
    if rng.random() < 0.03:
        leaf = rng.choice([t for t in TEXTURES if t != leaf])
    scents = [t.scent for t in (mother, one) if t.scent]
    scent = scents[0] if len(scents) == 2 or (scents and (father is None or rng.random() < 0.5)) else ""
    lines = ["kind: %s" % KIND,
             "colour: %s" % colour,
             "petals: %d" % max(3, min(12, petals)),
             "tall: %.1f" % max(3.0, min(30.0, tall)),
             "wakes: %.1f" % max(2.0, min(20.0, wakes)),
             "leaf: %s" % leaf]
    if scent:
        lines.append("scent: %s" % scent)
    if mother.variety and father is None:
        lines.append("variety: %s" % mother.variety)
    if cross:
        lines.append("from: cross of %s × %s" % cross)
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ the days

def sprout(seed, ctx) -> str:
    """A stray is sown as a seed in the ground. It comes up when a spring day wakes it."""
    p = Stray()
    p.since = getattr(ctx, "date", None)
    return write(p)


def day(body, seed, ctx):
    """One day of a stray: a seed waits, rots or wakes; a plant grows, flowers, sheds seed and dies."""
    text = _as_text(body)
    if hands.is_dead(text):
        return text, None
    t = Traits(seed)
    p = read(text)
    if p.is_seed and (not text.strip() or p.spoke_of_a_plant):
        p = Stray()
        p.since = ctx.date
        return write(p), "cut to the ground; a seed of it lies there still"
    if p.is_seed:
        event = _lie(p, t, ctx)
    else:
        event = _grow(p, t, ctx)
    return write(p), event


def _bed_light(ctx) -> float:
    return hands.num(getattr(ctx, "bed", {}) or {}, "light", 1.0, 0.0, 1.0)


def _rich(ctx) -> float:
    return hands.num(getattr(ctx, "bed", {}) or {}, "rich", 0.0, 0.0, 1.0)


def _late(s) -> bool:
    """The days after midsummer have shortened by an eighth (SHORTENED): every stray buds wherever it stands.

    A kind is not told its latitude, and the same daylength means early
    summer in one place and late summer in another. So the stray reckons
    from how long today is, and the sun's height of year, how long
    midsummer's day was where it stands, and compares the two. At this
    garden's 47 degrees that falls about the twentieth of August; at 55
    degrees about the twelfth; at 30 degrees summer ends before it comes.
    Autumn is late everywhere.
    """
    if s.season == "autumn":
        return True
    if s.season != "summer":
        return False
    date = getattr(s, "date", None)
    if not isinstance(date, datetime.date):
        return False
    south = date.month in (12, 1, 2)                    # summer in those months is the southern summer
    solstice = datetime.date(date.year - (1 if south and date.month != 12 else 0), 12 if south else 6, 21)
    if date <= solstice:
        return False
    today = hands.num({"d": getattr(s, "daylength", 12.0)}, "d", 12.0, 0.0, 24.0)
    tilt = abs(_declination(date))
    low, high = 0.0, 89.0                               # the latitude whose day is today's length, by halving
    for _ in range(30):
        middle = (low + high) / 2.0
        if _hours_of_day(middle, tilt) < today:
            low = middle
        else:
            high = middle
    return today < SHORTENED * _hours_of_day(low, math.radians(23.44))


def _declination(date) -> float:
    """How far north of the equator the sun stands on a date, in radians (a plain reckoning, good to a degree)."""
    return math.radians(23.44) * math.sin(2.0 * math.pi * (284 + date.timetuple().tm_yday) / 365.0)


def _hours_of_day(latitude, tilt) -> float:
    """Hours from sunrise to sunset at a latitude (degrees) when the sun stands `tilt` radians toward it."""
    phi = math.radians(latitude)
    cos_hour = ((math.sin(math.radians(-0.833)) - math.sin(phi) * math.sin(tilt))
                / max(1e-9, math.cos(phi) * math.cos(tilt)))
    if cos_hour >= 1.0:
        return 0.0
    if cos_hour <= -1.0:
        return 24.0
    return 2.0 * math.degrees(math.acos(cos_hour)) / 15.0


def _die(p, date, why):
    p.dead = "† %s, %s" % (date.isoformat(), why)


def _lie(p, t, ctx):
    """A seed's day in the ground."""
    s, rng, date = ctx.sky, ctx.rng, ctx.date
    if p.since is None:
        p.since = date
    if _crowded_out(ctx):
        _die(p, date, "crowded out in the ground")
        return "the seed was crowded out"
    if s.season == "spring":
        ground = s.tmean - 3.0 * (1.0 - _bed_light(ctx))      # shaded ground warms more slowly than the air
        # the warmer past its mark the ground is, the likelier it wakes today: a seed's fellows wake over weeks
        if ground >= t.wakes and s.wet >= 0.1 and rng.random() < min(0.3, 0.03 + 0.03 * (ground - t.wakes)):
            p.shoots = [Shoot("stem", 0, "\\", "^")]
            p.up, p.since = date, None
            return "woke and came up"
    elif s.season in ("autumn", "winter") and s.wet > 0.7 and rng.random() < 0.004 * (s.wet - 0.7) / 0.3:
        _die(p, date, "rotted in the ground")
        return "the seed rotted in the ground"
    if (date - p.since).days > SEED_DAYS:
        _die(p, date, "never woke")
        return "the seed never woke, and is gone"
    return None


def _bed_third(ctx) -> float:
    """A third of the bed's room: as many strays, grown or seed, as a bed carries before it holds some back."""
    return max(2.0, hands.num(getattr(ctx, "bed", {}) or {}, "room", 12, 1, 400) / 3.0)


def _strays_living(ctx) -> int:
    """How many other living strays the bed holds, grown or lying as seed: each holds a place of its room."""
    return sum(1 for other in getattr(ctx, "neighbours", None) or []
               if getattr(other, "kind", "") == KIND and not hands.is_dead(_as_text(getattr(other, "body", ""))))


def _crowded_out(ctx) -> bool:
    """Whether a seed lying in a bed crowded with strays perishes today.

    Where the living strays of a bed, grown or lying as seed, are more than
    a third of its room, each seed lying there has a small chance each day
    of perishing, in proportion to the excess, so that the crowd thins by
    about CROWD_PACE of its excess a day. Only seed perishes of it; a grown
    stray lives out its year. A stray's seed is already held back in its
    parent's bed by the same third (see cast); this is for seed that the
    days carried in from elsewhere, mostly into the wild corner, where every
    bed's overflow lands, so that the strays leave the rest of its room to
    other kinds' seedlings.
    """
    crowd = _strays_living(ctx) + 1                     # this seed too
    excess = crowd - _bed_third(ctx)
    return excess > 0 and ctx.rng.random() < CROWD_PACE * excess / crowd


def _leaf_char(n) -> str:
    """The leaf of a shoot's n-th length (from 1): the leaves go left and right by turns."""
    return "\\" if n % 2 else "/"


def _candidates(p):
    """The stem's lengths a branch could break from: a leaf still there, no branch yet, not the lowest or the top."""
    stem = p.stem
    taken = {b.at for b in p.branches}
    return [i for i in range(2, len(stem.nodes)) if stem.nodes[i - 1] in "\\/" and i not in taken]


def _below_the_cut(p):
    """Where a cut stem may break again: any length with a leaf and no branch yet, the top one included."""
    places = _candidates(p)
    top = len(p.stem.nodes)
    if top and p.stem.nodes[-1] in "\\/" and top not in {b.at for b in p.branches}:
        places.append(top)
    return places


def _branch_at(p, i):
    side = "left" if p.stem.nodes[i - 1] == "\\" else "right"
    p.shoots.append(Shoot(side, i, "", "^"))
    p.shoots[1:] = sorted(p.shoots[1:], key=lambda b: (b.at, b.side))


def _strip_leaf(shoot, i):
    shoot.nodes = shoot.nodes[:i] + "|" + shoot.nodes[i + 1:]


def _lowest_leaves(p):
    """Every leaf as (height, shoot, index), lowest first: where slugs and drought begin."""
    found = []
    for shoot in p.shoots:
        for i, c in enumerate(shoot.nodes):
            if c in "\\/":
                found.append(((i + 1) if shoot.side == "stem" else shoot.at + 0.8 * (i + 1), shoot.side, shoot.at, i, shoot))
    found.sort(key=lambda item: item[:4])
    return [(item[0], item[4], item[3]) for item in found]


def _grow(p, t, ctx):
    """A plant's day. Returns the one thing worth saying, or None."""
    s, rng, date = ctx.sky, ctx.rng, ctx.date
    stem = p.stem
    young = len(p.shoots) == 1 and len(stem.nodes) <= 3
    hardy = (-2.0 if young else -5.0) - (2.0 if t.leaf == "downy" else 0.0)
    if s.tmin < hardy:
        _die(p, date, "frost")
        return "killed by frost" + (" as a seedling" if young else "")
    if s.season == "winter":                     # the first winter day shakes out what seed is ripe; then it dies
        held = sum(h.seeds for h in p.tips("@") if h.seeds > 0)
        if held:
            for head in p.tips("@"):
                head.seeds = 0 if head.seeds > 0 else head.seeds
            p.shed += held
            p.shed_now, p.shed_on = held, date
            return None
        _die(p, date, "the year's end")
        return "died with the year"
    late = _late(s)
    light = _bed_light(ctx)
    rich = _rich(ctx)
    events = []
    had_bloom = bool(p.tips("*@"))

    # drought, on a hot bright day in dry ground: a seedling may dry out; a plant drops a lower leaf
    if s.wet < (0.05 if t.leaf == "waxy" else 0.12) and s.tmax > 20.0 and s.light > 5.0:
        if young and len(stem.nodes) <= 1 and s.wet < 0.08 and rng.random() < 0.08:
            _die(p, date, "dried out")
            return "dried out as a seedling"
        leaves = _lowest_leaves(p)
        if len(leaves) > 3 and leaves[0][0] < 0.5 * len(stem.nodes) and rng.random() < 0.15:
            _, shoot, i = leaves[0]
            _strip_leaf(shoot, i)

    # a gale snaps a tall stem
    tall_now = len(stem.nodes)
    if s.wind >= 6.0 and tall_now > 8 and stem.tip != "x" and rng.random() < 0.05 * (tall_now - 8) * (s.wind - 5.0):
        at = rng.randint(3, tall_now - 2)
        stem.nodes, stem.tip, stem.seeds = stem.nodes[:at], "x", -1
        p.shoots = [stem] + [b for b in p.branches if b.at <= at]
        events.append("snapped in the wind, %d lengths up" % at)

    # seed falls from ripe heads on dry days, more in the wind
    if s.rain < 0.5:
        fallen = 0
        for head in p.tips("@"):
            if head.seeds > 0:
                k = min(head.seeds, int(head.seeds * (0.1 + 0.04 * s.wind) + rng.random()))
                head.seeds -= k
                fallen += k
        if fallen:
            p.shed += fallen
            p.shed_now, p.shed_on = fallen, date

    # unripe heads ripen; flowers set heads; buds open
    warm = max(0.0, min(1.0, s.warmth / 12.0))
    leafy = p.leaves / max(1, p.lengths)
    for head in p.tips("@"):
        if head.seeds < 0 and rng.random() < 0.04 * max(0.5, warm) * (1.2 if s.wet < 0.3 else 0.8):
            vigour = 0.5 * leafy + 0.3 * light + 0.2 * rich
            head.seeds = max(2, min(SEEDS_MOST, int(round((5 + 15 * vigour) * rng.uniform(0.75, 1.1)))))
    for flower in p.tips("*"):
        if rng.random() < 0.06 + (0.12 if s.rain > 5.0 else 0.0):
            flower.tip, flower.seeds = "@", -1
    for bud in p.tips("o"):
        if rng.random() < max(0.04, 0.15 * warm):
            bud.tip = "*"
    if not had_bloom and p.tips("*"):
        events.append("came into flower")

    # growth at every growing tip
    sun = max(0.2, min(1.0, s.light / 6.0))
    water = max(0.2, min(1.0, s.wet / (0.1 if t.leaf == "waxy" else 0.2)))
    fit = 1.0 if t.leaf == "plain" else 0.9
    chance = min(0.95, 0.3 * warm * sun * water * (0.35 + 0.65 * leafy) * (1.0 + 0.6 * rich) * fit)
    stem_to = max(2, int(round(t.tall)))
    for shoot in p.tips("^"):
        # the stem grows to its tall; a branch half as far, and a high branch only as far as the stem's top
        target = stem_to if shoot.side == "stem" else max(2, min(int(round(t.tall * 0.5)), int(1.2 * (t.tall - shoot.at)) + 1))
        if len(shoot.nodes) < target and rng.random() < chance:
            shoot.nodes += _leaf_char(len(shoot.nodes) + 1)
        if len(shoot.nodes) >= target or (late and shoot.nodes):
            shoot.tip = "o"
    if late:
        p.shoots = [stem] + [b for b in p.branches if b.nodes or b.tip != "^"]     # a branch that never grew is gone

    # branches: from the axil of a leaf, while the plant is young enough to make them
    if not late and stem.tip in "^o*" and len(stem.nodes) >= 0.4 * t.tall:
        most = min(BRANCHES_MOST, 1 + int(round(5 * light + 2 * rich)))
        places = _candidates(p)
        if len(p.branches) < most and places and rng.random() < 0.35 * chance:
            _branch_at(p, rng.choice(places))
    # a cut stem breaks again below the cut, early enough in the year, once nothing else on it
    # is growing, flowering or ripening seed: so a stray whose heads are taken keeps on flowering
    coming = any(s_.tip in "^o*" or (s_.tip == "@" and s_.seeds < 0) for s_ in p.shoots)
    may_break = stem.tip == "x" and not late and not coming and len(p.branches) < BRANCHES_MOST
    if may_break and rng.random() < 0.1:
        places = _below_the_cut(p)
        if places:
            _branch_at(p, max(places))
            events.append("broke a new branch below the cut")
            may_break = False

    # an annual is done when nothing on it is growing, flowering or holding seed
    busy = any(s_.tip in "^o*" or (s_.tip == "@" and s_.seeds != 0) for s_ in p.shoots)
    if not busy:
        if not (may_break and _below_the_cut(p)):
            why = "went to seed" if p.shed else ("cut, and did not come again" if stem.tip == "x" else "died without seeding")
            _die(p, date, why)
            return why
    return events[0] if events else None


# ------------------------------------------------------------------ seed that falls

def cast(body, seed, ctx) -> list:
    """The seed that falls today and takes: a few of what the ripe heads shed, crossed if pollen was brought."""
    p = read(body)
    date = getattr(ctx, "date", None)
    if p.dead or p.is_seed or p.shed_on is None or p.shed_on != date or p.shed_now <= 0:
        return []
    rng = ctx.rng
    crowd = max(0.0, 1.0 - _strays_living(ctx) / _bed_third(ctx))  # a third of the bed's room in strays: no more take
    taking = sum(1 for _ in range(min(p.shed_now, 200)) if rng.random() < TAKES * crowd)
    if not taking:
        return []
    mother = Traits(seed)
    fathers = []
    for grain in (getattr(ctx, "pollen", None) or []) if p.tips("*") else []:     # pollen is taken by an open flower
        given = getattr(grain, "seed", None)
        given = given if isinstance(given, dict) else hands.read_keys(_as_text(given))
        if hands.word(given, "kind", "") != KIND:
            continue
        father = Traits(given)
        by = _as_text(getattr(grain, "by", "")).lower()
        if (mother.evening or father.evening) and not any(word in by for word in NIGHT_CARRIERS):
            continue                            # the evening's flowers were shut when that one came by day
        fathers.append((father, _as_text(getattr(grain, "where", "")) or "another stray"))
    seeds = []
    for _ in range(min(3, taking)):
        if fathers and rng.random() < 0.7:
            father, where = rng.choice(fathers)
            seeds.append(_seed_text(mother, rng, father, (getattr(ctx, "where", "") or "a stray", where)))
        else:
            seeds.append(_seed_text(mother, rng))
    return seeds


# ------------------------------------------------------------------ what creatures meet

def flowers(body, seed, ctx) -> int:
    """How many flowers are open today.

    A stray of the evening's hours says the same at any hour: the garden
    does not tell a kind who is asking. Its crosses are kept to the night
    in cast() instead, which sees who carried each grain.
    """
    p = read(body)
    return 0 if p.dead or p.is_seed else len(p.tips("*"))


def bitten(body, seed, ctx, share, by):
    """A bite. Slugs take seedlings whole and the lower leaves of the grown.

    Anything else nibbles its soft growth (see _nibbled), or, with a bite
    of a fifth or more (NIBBLE), crops the stray flat from the top. Bristly
    strays are left alone by everything but slugs and snails.
    """
    text = _as_text(body)
    if hands.is_dead(text):
        return text, None
    p = read(text)
    if p.is_seed:
        return text, None                       # a seed in the ground is not soft
    try:
        share = float(share)
    except (TypeError, ValueError, OverflowError):
        return text, None
    if share != share or share <= 0:                   # not a number, or no bite at all
        return text, None
    share = min(1.0, share)
    who = " ".join(_as_text(by).split())[:60] or "something"
    t = Traits(seed)
    date = getattr(ctx, "date", None)
    stem = p.stem
    if "slug" in who.lower() or "snail" in who.lower():
        if t.leaf == "bristly":
            share /= 2.0
        young = len(p.shoots) == 1 and len(stem.nodes) <= 3
        if young and share >= 0.25 and date is not None:
            _die(p, date, "eaten by slugs")
            return write(p), "slugs ate it as a seedling"
        leaves = _lowest_leaves(p)
        n = min(len(leaves), max(1, int(round(share * len(leaves))))) if leaves else 0
        for _, shoot, i in leaves[:n]:
            _strip_leaf(shoot, i)
        if young and not p.leaves and date is not None:
            _die(p, date, "eaten by slugs")
            return write(p), "slugs ate it as a seedling"
        return write(p), ("slugs ate %d of its leaves" % n if n >= 4 else None)
    if t.leaf == "bristly":
        return text, None                       # it noses the bristles and leaves them (nothing changed, nothing to say)
    if share < NIBBLE:                          # a nibble: the soft growth, not the stem
        return _nibbled(p, text, ctx, share, who)
    top = len(stem.nodes)
    keep = max(1, int(round((1.0 - share) * top)))
    if keep >= top:
        return text, None
    stem.nodes, stem.tip, stem.seeds = stem.nodes[:keep], "x", -1
    kept = []
    for branch in p.branches:
        if branch.at > keep:
            continue
        room = int((keep - branch.at) / 0.8)            # a branch rises about 0.8 of a length for each of its own
        if len(branch.nodes) > room:
            branch.nodes, branch.tip, branch.seeds = branch.nodes[:room], "x", -1
        if branch.nodes or branch.tip != "x":
            kept.append(branch)
    p.shoots = [stem] + kept
    return write(p), "cropped to %d length%s by %s" % (keep, "" if keep == 1 else "s", who)


def _nibbled(p, text, ctx, share, who):
    """A small bite, which takes only soft growth: the young leaf on the top length of a growing shoot.

    Each such leaf is taken with the bite's share as its chance, so a bite
    of a tenth takes a tenth of what is soft, which on most nights is
    nothing. It takes no stem and kills nothing: a stray nibbled bare grows
    slowly until new leaves come (killing seedlings is the slugs' part).
    """
    rng = getattr(ctx, "rng", None)
    if rng is None:
        return text, None
    taken = 0
    for shoot in p.tips("^"):
        if shoot.nodes and shoot.nodes[-1] in "\\/" and rng.random() < share:
            _strip_leaf(shoot, len(shoot.nodes) - 1)
            taken += 1
    if not taken:
        return text, None                       # it found nothing soft enough, or missed
    return write(p), None


# ------------------------------------------------------------------ words

def describe(body, seed, ctx) -> str:
    """One short line: '12 lengths on 3 shoots · 2 in flower · 3 heads, 31 seeds in them'."""
    return _in_words(read(body))


def size(body, seed) -> float:
    """For its dot on the plan: its lengths, and half a length for the plant they grow on; a seed in the ground is
    the smallest thing there is."""
    p = read(body)
    return 0.2 if p.is_seed else p.lengths + 0.5


def _why(p) -> str:
    """What a dead mark says killed it: '† 2027-09-02, went to seed' -> 'went to seed'."""
    return p.dead.lstrip("† ").split(",", 1)[-1].split("·")[0].strip()


def _in_words(p, death=True) -> str:
    """The describe line of a Stray. Without `death`, a dead one's line leaves out what killed it
    (its plate's caption says that already, in the ground's own words)."""
    if p.is_seed:
        if p.dead and death:
            return "dead: " + _why(p)
        return "a seed in the ground"
    parts = ["%d length%s on %d shoot%s" % (p.lengths, "" if p.lengths == 1 else "s",
                                             len(p.shoots), "" if len(p.shoots) == 1 else "s")]
    if p.dead:
        if death:
            parts = ["dead: %s" % _why(p), parts[0]]
    elif status(p) == "a seedling":
        parts = ["a seedling", parts[0]]
    else:
        for mark, one, many in (("o", "bud", "buds"), ("*", "in flower", "in flower")):
            n = len(p.tips(mark))
            if n:
                parts.append("%d %s" % (n, one if n == 1 else many))
    heads = p.tips("@")
    if heads:
        held = sum(max(0, h.seeds) for h in heads)
        unripe = sum(1 for h in heads if h.seeds < 0)
        words = "%d head%s" % (len(heads), "" if len(heads) == 1 else "s")
        if held:
            words += ", %d seed%s in %s" % (held, "" if held == 1 else "s", "it" if len(heads) == 1 else "them")
        elif unripe and not p.dead:
            words += ", unripe"
        parts.append(words)
    if p.shed:
        parts.append("shed %d" % p.shed)
    return " · ".join(parts)


# ------------------------------------------------------------------ the plate

LEAF_LONG, LEAF_WIDE, LEAF_TURN = 0.8, 0.2, 55.0      # a leaf's length and half-width in lengths; its angle off the shoot
AXIL_TURN = 82.0                                      # the angle of a stem leaf with a branch in its axil: flatter,
                                                      # so that it stands clear below the branch it holds
HEAD_A, HEAD_B = 0.3, 0.4                            # a seed head's half-width and half-height, at its plainest size
SEED_PLACES = sorted([(x, y) for y in (-0.26, -0.13, 0.0, 0.13, 0.26) for x in (-0.195, -0.065, 0.065, 0.195)],
                     key=lambda place: (place[1], abs(place[0]), place[0]))     # where seeds lie in a head, lowest first
CLEAR_AT = 62.0           # below this many pixels to a length, flowers and heads are drawn larger, to stay legible


def _turn(dx, dy, degrees):
    a = math.radians(degrees)
    return dx * math.cos(a) - dy * math.sin(a), dx * math.sin(a) + dy * math.cos(a)


def _stem_path(stem):
    return [(0.0, float(i)) for i in range(len(stem.nodes) + 1)], (0.0, 1.0)


def _branch_path(branch, stem_len):
    """The points of a branch, from its axil on the stem: it leaves at a slant and bends upward as it grows."""
    sign = -1.0 if branch.side == "left" else 1.0
    lean = 34.0 + 20.0 * (1.0 - branch.at / max(1.0, stem_len))
    x, y = 0.0, branch.at - 0.3
    points = [(x, y)]
    for _ in branch.nodes:
        a = math.radians(lean)
        x, y = x + sign * math.sin(a), y + math.cos(a)
        points.append((x, y))
        lean = max(16.0, lean - 3.0)
    a = math.radians(lean)
    return points, (sign * math.sin(a), math.cos(a))


def _enlarge(pen, paths):
    """How much larger than their plainest size to draw flowers and heads, so that they read on a plate of this fit.

    Their size says nothing about the plant (the body has no number for it),
    so, like the weight of a line, it is kept to what the eye needs: about
    the same number of pixels however tall the stray has grown.
    """
    xs = [x for points, _ in paths for x, _ in points] or [0.0]
    ys = [y for points, _ in paths for _, y in points] or [0.0]
    try:
        x0, y0, x1, y1 = (float(v) for v in getattr(pen, "box", None))
    except Exception:
        x0, y0, x1, y1 = 60.0, 50.0, 840.0, 930.0
    most = hands.num({"u": getattr(pen, "unit_px_max", 60.0)}, "u", 60.0, 1.0, 1000.0)
    wide = max(xs) - min(xs) + 2.0
    high = max(ys) - min(0.0, min(ys)) + 1.5
    scale = min(most, max(1.0, x1 - x0 - 40.0) / wide, max(1.0, y1 - y0 - 70.0) / high)
    return max(1.0, min(4.0, CLEAR_AT / max(scale, 1.0)))


def _leaf(pen, x, y, dx, dy, side, ink, texture, turn=LEAF_TURN):
    """A pointed leaf from (x, y), turned `turn` degrees off the shoot's direction (dx, dy) to one side."""
    lx, ly = _turn(dx, dy, turn if side == "\\" else -turn)
    nx, ny = -ly, lx
    steps = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)

    def outline(scale, start, end):
        one, other = [], []
        for f in steps:
            along = start + (end - start) * f
            half = LEAF_WIDE * scale * math.sin(math.pi * f) ** 0.8
            cx, cy = x + lx * LEAF_LONG * along, y + ly * LEAF_LONG * along
            one.append((cx + nx * half, cy + ny * half))
            other.append((cx - nx * half, cy - ny * half))
        return one + other[::-1][1:-1]

    pen.polyline(outline(1.0, 0.0, 1.0), 3, ink, closed=True)
    if texture == "waxy":
        pen.polyline(outline(0.5, 0.18, 0.86), 2, ink, closed=True)
    elif texture == "downy":
        for along in (0.32, 0.52, 0.72):
            pen.dot(x + lx * LEAF_LONG * along, y + ly * LEAF_LONG * along, 2.5, ink)


def _scar(pen, x, y, dx, dy, side, ink, turn=LEAF_TURN):
    """Where a leaf was: the stub of its stalk, ending in a knob (which no bristle has)."""
    lx, ly = _turn(dx, dy, turn if side == "\\" else -turn)
    pen.line(x, y, x + lx * 0.22, y + ly * 0.22, 4, ink)
    pen.dot(x + lx * 0.22, y + ly * 0.22, 3.5, ink)


def _bristles(pen, points, inks):
    """Fine hairs along a shoot: two on each length, one to each side, leaning upward. inks[n] is length n's ink."""
    for n in range(1, len(points)):
        (x0, y0), (x1, y1) = points[n - 1], points[n]
        dx, dy = x1 - x0, y1 - y0
        for along, turn in ((0.3, 62.0), (0.55, -62.0)):
            mx, my = x0 + dx * along, y0 + dy * along
            tx, ty = _turn(dx, dy, turn)
            pen.line(mx, my, mx + tx * 0.11, my + ty * 0.11, 2, inks[n - 1])


def _ellipse(cx, cy, a, b, n=20):
    return [(cx + a * math.cos(2 * math.pi * k / n), cy + b * math.sin(2 * math.pi * k / n)) for k in range(n)]


def _tip(pen, shoot, x, y, dx, dy, ink, t, dead, shut, k):
    """The mark at the end of a shoot, drawn k times its plainest size."""
    colour = "dead" if dead else t.colour
    edged = not dead and _pale(t.colour)                # white on cream: the flower is edged in its shoot's ink
    if shoot.tip == "^":
        for side in (25.0, -25.0):
            vx, vy = _turn(dx, dy, side)
            pen.line(x, y, x + vx * 0.22 * k, y + vy * 0.22 * k, 3, ink)
    elif shoot.tip == "o":
        cx, cy = x + dx * 0.2 * k, y + dy * 0.2 * k
        for paint, weight in ((ink, 9.0), (colour, 5.0)) if edged else ((colour, 6.0),):
            pen.line(cx - dx * 0.08 * k, cy - dy * 0.08 * k, cx + dx * 0.1 * k, cy + dy * 0.1 * k, weight, paint)
        pen.arc(cx, cy, 0.2 * k, 0, 360, 3, ink)
    elif shoot.tip == "*":
        if shut:                                        # furled: a narrow stroke tapering to a point
            steps = ((0.0, 0.25, 13.0), (0.25, 0.5, 10.0), (0.5, 0.7, 7.0))
            for layer in ((ink, 5.0), (colour, 0.0)) if edged else ((colour, 0.0),):
                for a0, a1, weight in steps:
                    pen.line(x + dx * a0 * k, y + dy * a0 * k, x + dx * a1 * k, y + dy * a1 * k,
                             weight + layer[1], layer[0])
            return
        cx, cy = x + dx * 0.4 * k, y + dy * 0.4 * k
        n = max(3, min(12, t.petals))
        start = 90.0 + 180.0 / n
        for paint, more in ((ink, 5.0), (colour, 0.0)) if edged else ((colour, 0.0),):
            for j in range(n):                          # (the edge goes down first, all round, then the petals over it)
                a = math.radians(start + 360.0 * j / n)
                ux, uy = math.cos(a) * k, math.sin(a) * k
                if n <= 5:                              # few petals: broad and round
                    pen.dot(cx + 0.28 * ux, cy + 0.28 * uy, 20 - n + more / 2.0, paint)
                else:                                   # many: narrow rays
                    pen.line(cx + 0.08 * ux, cy + 0.08 * uy, cx + 0.44 * ux, cy + 0.44 * uy,
                             max(6, int(round(40.0 / n)) + 4) + more, paint)
        pen.dot(cx, cy, 6, "dead" if dead else hands.mix(t.colour, "#000000", 0.6))
    elif shoot.tip == "@":
        ripe = shoot.seeds >= 0
        a, b = HEAD_A * k, HEAD_B * k
        cx, cy = x + dx * b, y + dy * b
        rim = "dead" if dead else ("brown" if ripe else ink)
        pen.polyline(_ellipse(cx, cy, a, b), 3, rim, closed=True)
        pen.line(cx - 0.6 * a, cy + b, cx + 0.6 * a, cy + b, 5, rim)
        for sx, sy in SEED_PLACES[:max(0, shoot.seeds)]:
            pen.dot(cx + sx * k, cy + sy * k, 3, "dead" if dead else "ink")
    elif shoot.tip == "x":                              # a cut: a slash across the shoot's end, like a blade's,
        lean = 60.0 if shoot.nodes.endswith("/") else -60.0     # slanting (never a head's flat crown), and leaning
        sx, sy = _turn(dx, dy, lean)                    # against the top leaf rather than along its edge
        pen.line(x - sx * 0.2 * k, y - sy * 0.2 * k, x + sx * 0.2 * k, y + sy * 0.2 * k, 5, ink)


def draw(body, seed, ctx, pen) -> None:
    """The stray on its plate: stem, leaves, branches, and at each tip its bud, flower, head or cut."""
    p = read(body)
    t = Traits(seed)
    dead = bool(p.dead)
    left_text = getattr(ctx, "left", None)
    left = read(left_text) if left_text is not None else None
    pen.unit_name = "length, lengths"
    pen.ground(0)
    if p.is_seed:
        new = left is None
        pen.dot(0, -0.3, 6, "dead" if dead else ("fresh" if new else "wood"))
        since = " %d %s %d" % (p.since.day, _MONTHS[p.since.month - 1], p.since.year) if p.since else ""
        if dead:                                        # (the caption's own line says when it died, and why)
            pen.note("lay in the ground from" + since if since else "a seed in the ground")
        else:
            pen.note("a seed in the ground" + (" since" + since if since else ""))
        return
    was = {} if left is None or left.is_seed else {s.key: len(s.nodes) for s in left.shoots}
    hour = getattr(ctx, "hour", None)
    shut = t.evening and isinstance(hour, int) and 9 <= hour <= 17
    stem_len = len(p.stem.nodes)
    paths = [_stem_path(shoot) if shoot.side == "stem" else _branch_path(shoot, stem_len) for shoot in p.shoots]
    k = _enlarge(pen, paths)
    wood = "dead" if dead else "wood"
    new_ink = "dead" if dead else "fresh"
    axils = {b.at for b in p.branches}                   # the stem's lengths that hold a branch
    tips = []
    for shoot, (points, end_dir) in zip(p.shoots, paths):
        old = len(shoot.nodes) if dead else min(was.get(shoot.key, 0), len(shoot.nodes))
        inks = [wood if i < old else new_ink for i in range(len(shoot.nodes))]     # each length's ink
        weight = 5 if shoot.side == "stem" else 4
        if old > 0:
            pen.polyline(points[:old + 1], weight, wood)
        if len(points) - 1 > old:
            pen.polyline(points[old:], weight, new_ink)
        if t.leaf == "bristly":
            _bristles(pen, points, inks)
        for i, c in enumerate(shoot.nodes):
            (x0, y0), (x1, y1) = points[i], points[i + 1]
            dx, dy = x1 - x0, y1 - y0
            size = math.hypot(dx, dy) or 1.0
            dx, dy = dx / size, dy / size
            nx, ny = x0 + dx * 0.7, y0 + dy * 0.7
            turn = AXIL_TURN if shoot.side == "stem" and (i + 1) in axils else LEAF_TURN
            if c in "\\/":
                _leaf(pen, nx, ny, dx, dy, c, inks[i], t.leaf, turn)
            else:
                _scar(pen, nx, ny, dx, dy, "\\" if (i + 1) % 2 else "/", inks[i], turn)
        grown = len(shoot.nodes) > old or (not shoot.nodes and shoot.key not in was)
        tips.append((shoot, points[-1], end_dir, new_ink if grown else wood))
    for shoot, (ex, ey), (dx, dy), ink in tips:          # the tips last, over the leaves
        _tip(pen, shoot, ex, ey, dx, dy, ink, t, dead, shut, k)
    pen.note(_in_words(p, death=False))                  # (for the dead, the caption's own line says what killed it)
    if p.up:
        pen.note("came up %d %s %d" % (p.up.day, _MONTHS[p.up.month - 1], p.up.year))
    shut_count = len(p.tips("*")) if shut and not dead else 0
    if shut_count:                                       # (when they open is left for a second look to find)
        pen.note("its flower is shut" if shut_count == 1 else "its %d flowers are shut" % shut_count)


_MONTHS = ("January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December")
