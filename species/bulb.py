"""
Bulb: a plant that sleeps underground and keeps time.

Most of the year there is nothing to see: a few rounds under the ground
line, each a bulb with its stored strength. The bulb is counting. On its
day it wakes, puts up leaves and (if it holds a flower) a flower, stands a
while, and goes back down, a little stronger or a little weaker than it
came up. Leaves in the light are what charge a bulb; the leaves themselves,
the flower and the sleep are what it spends. So a clump in the sun thickens
year by year with new bulbs beside the old; one by the north wall holds its
own, flowering some years and not others; and one planted in deep shade,
where the light cannot repay its leaves, stops flowering, weakens year by
year, and in the end is gone, as real bulbs do.


WHAT A SEED SAYS

    kind: bulb
    wakes: when the days grow past 9.2 hours
    stands: 80                  days its leaves stand once they are up (20..200)
    leaves: 2 strap             how many leaves a grown bulb puts up, and their shape:
                                strap, broad or grass. A length may follow ("4 broad 25 cm");
                                else they are about as long as the stem. "in spring" at the
                                end: the leaves come up on their own, in spring, and the
                                flower comes alone, without them (see below).
    stem: 14                    the flower stem, in cm (3..120)
    flower: 3 white, nodding    petals, colour (a plate ink or #rrggbb); "nodding" if it hangs
    scent: day                  none, day, dusk or night. Moths come to dusk and night; a day
                                scent holds the bees, and pollen they bring takes more often.
    multiplies: offsets         offsets (new bulbs beside the old), seed, or both
    leaf: waxy                  waxy or plain
    coat: none                  papery or none: the dry skin round the bulb
    hardy: -20                  the night, in °C, that burns its leaves (flowers mind a third of it)

and, if wanted:

    opens: at the full moon     the bud, once grown, waits for that moon (full or new)
    sown: seed                  it came from seed, not from a bulb: it starts very small
    variety: <a name>           carried on by its own seed, dropped by a cross

`wakes:` is its clock, and there are four ways to tell the time:

    when the days grow past H hours      the day the day length rises past H
    when the days shrink past H hours    the day it falls past H
    when the soil has gathered N degrees of warmth
                                         counted from the shortest day (21 December, or
                                         21 June south of the equator): each day adds
                                         what its mean stands above 5 °C
    at the Nth full moon asleep          counting the full moons since it went down
                                         ("new moon" counts new moons instead)

Each comes round once: a day length is crossed once a year each way, the
warmth starts again from nothing at each shortest day, and the moons are
counted again from each going-down. A bulb sown after its day has passed
waits for the next one: a warmth bulb planted in winter counts from its
planting, and one sown at any other time of year (a seed that falls in
spring, say) waits for the next shortest day. A rule it cannot read makes
it a spring bulb that wakes on 100 degrees of warmth.

A bulb whose leaves say "in spring" lives by two clocks. Its flower keeps
the `wakes:` rule and comes up bare, with no leaf beside it; its leaves keep
their own time and come up when the days grow past 10.5 hours, whether it
flowered or not. A flower of such a bulb that set seed leaves its pod
underground over the winter, and the pod rides up with the spring leaves.


WHAT A BODY SAYS

    in leaf since 2027-03-12

    below the ground:
    bulb at 0 cm: 18.2
    bulb at -4.1 cm: 5.4
    bulb at 4.3 cm: 11.1, a pod to come

    above the ground:
    at 0 cm: 3 leaves 24.0 cm · stem 30.0 cm · flower open 4 days
    at -4.1 cm: 2 leaves 14.2 cm · bitten
    at 4.3 cm: 3 leaves 6.0 cm · bud in the shoot

The first line is what the clump is doing (asleep, in leaf, or in flower
without its leaves) and since when. Then its clock, which keeps only what
its own rule needs:

    the day: shorter than 9.2 h      which side of its hour the day length lay, last it looked
    warmth: 157 since the shortest day
    full moons: 3 since it went down, the last on 2027-01-22     (while it sleeps)

Then one line for each bulb: where it sits in the clump (cm from the first
bulb's place) and its strength; ", a flower in it" if it made next
season's flower as it last went down (a bulb from a packet comes with one),
and ", a pod to come" if a seed pod waits under the ground. A planted bulb
comes at 12, a bulb makes a flower from 10, and none holds more than 40. A
clump holds at most 40 bulbs: lines past the fortieth are lost, and the
clump says so. Then, for each bulb that has anything above the ground, one
line of what stands there: its leaves and their length, a stem, a bud (in
the shoot, or out), a flower open so many days, withered or frosted, a pod,
and any harm (bitten, cut, frost-burnt, eaten to the ground; a bud or a
flower eaten).

Asleep, the body is mostly still. What moves is the clock: a warmth count
climbs through the winter on each day warm enough to count, a moon count
turns at each full moon, a day-length line when the day crosses its hour.
And the ground may wear at the bulbs: dust-dry days on dry ground, for a
bulb without a coat, and sodden days, for one with a papery coat.

Texture for the hand: the clump parts cleanly, a line to a bulb.
  - Cut a `bulb at` line and that bulb is dug up. What stood above it goes too.
  - Cut an `at ... cm:` line and that bulb's leaves and flower are gone. It
    will not send up more until it next wakes, so it goes down weaker.
  - To lift and divide a clump, make a new plant folder beside it, copy the
    seed there, and move some `bulb at` lines into a new `body` there. Each
    half goes on alone. A half without the clock lines has lost count: it
    sleeps from that day, and waits for its next hour to come round.
  - Cut the whole body, or take the body file away, and a bulblet left in
    the ground comes up again, at strength 4: some years from flowering.
  - Lower a strength and the bulb shrinks; raise it and it is fed (never
    past 40): fed to 10 or more, it flowers when it next wakes. Strike out
    ", a flower in it" from a bulb under 10, and it will not.
  - A date in the future (a slip of a digit) is taken as today.

What the plant does by itself, day by day: it counts, and it keeps an
account. Awake, its leaves grow with the warmth and gather strength from
the light that reaches the bed (the north wall gives a third of the sky's
light, and a leaf there gathers about half what it would in the open; in
deep shade, a quarter), less in dry ground unless the leaves are waxy,
more in ground made rich, and less in a crowded clump; a small bulb's
small leaves gather less. When it wakes, a bulb pays
for its leaves (by their size: a small bulb's cost less) and for the flower
it holds, and for its sleep (a share of its strength for every day it
slept, about 9 in 100 over a year, and a little besides). In good light the
leaves repay all that and more; in deep shade they cannot, and the bulb
loses ground every year. When the leaves go down, every bulb strong enough
splits off a new one beside it, where the clump has room for both to grow,
and every bulb of 10 or more makes next season's flower. Asleep, a bulb
with no coat shrivels on the dust-dry days of dry ground (the stones), and
one with a papery coat rots on sodden days, fast in warm weather, slowly in
cold (the pond's edge, where a tulip flowers once and then is lost). A hard
night burns the leaves; frost takes open flowers; heavy rain spoils an
upright flower sooner than a nodding one. A bulb worn to nothing is gone,
and when the last one goes, so is the plant, and its body says how: it
withered, shrivelled or rotted.

Creatures: slugs love its emerging shoots and its buds (waxy leaves they
like half as well); a bud still in the shoot is lost with the shoot. Bees
and moths carry its pollen, and a flower takes pollen only in its first
three days open: a flower brought the pollen of another bulb then may set a
crossed seed that same day, blending the two colours, the more readily the
more the seed lives by seed (a clump that multiplies by offsets rarely
crosses). Otherwise a ripe pod now and then sows itself. A pony crops
whatever stands higher than 6 cm, clean and flat.


WHAT THE PLATE SHOWS

The faint line across is the ground. Everything is drawn to one scale; the
bar at the foot says how many cm.

Below the ground:
  - each round is a bulb, its area its strength. The largest sit deepest.
    A hair of clear paper round each keeps bulbs that touch apart.
  - a dot of the flower's colour, on a ring of clear paper, in a bulb: a
    flower is in it, not yet up. Asleep, it will flower when it next wakes;
    in leaf, its bud is still in the shoot (or it has grown strong enough
    to make next season's flower).
  - a broken ring round a bulb, dry and brittle like the skin itself: its
    papery coat. The gap at its top is where the shoot comes out.
  - a small dot just above a bulb: a seed pod waiting under the ground.
  - a line up from a bulb to the ground: its shoot, while it is awake.

Above the ground:
  - curved strokes are leaves; broad leaves are drawn broad, grass-like
    ones thin. A doubled stroke (two edges with paper between, closed at
    the tip) is a waxy leaf, as broad as a plain one.
  - leaves in the pale dun of the dead ink (lighter than any planter's
    ink) and lying over are yellowing: the plant is going down. Dun at the
    tips only: burnt by frost. A dead clump is all dun.
  - an open black ring just past a leaf's tip: it was bitten. A black bar
    across the tip: it was cut clean. An open black ring at the ground: the
    shoots were eaten away. An open black ring just past the top of a stem:
    its bud or flower was eaten.
  - an upright line is a stem; a hooked top means the flower nods.
  - one thick stroke of the flower's colour at the stem's end is a bud,
    its petals still closed. Strokes of that colour are an open flower, one
    stroke to a petal: fanned upward from the stem's end, or, on a nodding
    flower, hanging side by side like a bell. Short dun strokes hanging limp
    to one side, still one to a petal, are a withered or frosted flower.
  - a filled dot on a stem is a seed pod swelling; a V opened at the top
    of a stem, a pod that has ripened and split.

In the planter's ink: what was there when the last visitor left. In the
fresh green: what has grown since (new bulbs whole; an old bulb's new
growth as a green ring round it; the new length of leaves and stems). While
it is yellowing the dun overrides the green, for stems and leaves alike.
"""

import datetime
import math
import random
import re

import hands

KIND = "bulb"

# ------------------------------------------------------ the numbers of its life

START = 12.0            # the strength of a bulb planted from a packet
SEEDLING = 1.0          # the strength of one come up from seed
LEFT_BEHIND = 4.0       # the strength of the bulblet that comes up when a whole body was cut away
FLOWER_AT = 10.0        # a bulb this strong as it goes down makes next season's flower (a fed one flowers anyway)
MOST = 40.0             # no bulb holds more than this
GONE = 0.25             # a bulb weaker than this has withered away
BULBS_MOST = 40         # a clump holds no more bulbs than this: it makes no more offsets, and a hand's extra lines are lost
CROWD = 12              # past this many bulbs, each one's share of the light shrinks

# A year's account. What a bulb gathers comes only from its leaves in the light; what it spends is
# its leaves, its flower and pod, and its sleep. The leaves are the one cost that does not shrink with
# the light, so where the light cannot repay them the bulb loses a little every year, and at last is gone.
UPKEEP = 0.00025        # share of its strength a bulb spends for each day it slept (paid when it wakes)...
KEEP = 0.0006           # ...and this much strength besides, each day, however small it is
SHRIVEL = 0.006         # a coatless bulb asleep in dry ground (see _sleep) loses this share on a dust-dry day
DRY = 0.1               #    (less as the ground is damper, nothing once its wetness reaches this)...
SODDEN = 0.97           # ground this wet is sodden: the pond's edge, most of the year; elsewhere a few days
ROT = 0.03              # ...and a papery bulb, asleep, loses this share on each warm sodden day,
ROT_EATS = 0.08         #    and this much strength besides: rot eats a small bulb whole. On a cold sodden day,
ROT_COLD = 0.05         #    this part of both (a bulb from a packet flowers once there, and then rots).
ROT_WARM = 15.0         # a day this warm (its mean, °C) is warm enough for rot
RATE = 0.14             # strength one full-grown leaf gathers on a perfect day...
HALF_LIGHT = 6.0        # ...and the hours of light that give it half of that
LEAF_COST = 1.0         # strength spent on a full-grown leaf when it comes up (times its shape's catch, and less
                        # for a small bulb's smaller leaf)
BUD_COST = 1.0          # spent on a flower stem and its bud: this, and one more for every 15 cm of stem
POD_COST = 1.0          # spent on ripening a pod
OFFSET = 3.0            # the strength of a new bulb split off an old one...
OFFSET_COST = 4.0       # ...and what it costs the old one
SPLIT = {"offsets": 20.0, "both": 16.0, "seed": 1e9}     # a bulb this strong splits when it goes down
SETS_SEED = {"offsets": 0.15, "both": 0.5, "seed": 0.8}  # a flower's chance of setting a pod as it ends
SOWS = {"offsets": 0.06, "both": 0.2, "seed": 0.3}       # a ripe pod's chance of sowing itself
CROSSES = 0.08          # the chance that an open flower brought pollen of another bulb sets a crossed seed that day
                        # (for a seed that sets seed as readily as 'both'; scaled by SETS_SEED for the others)
TAKES = 3               # a flower takes pollen only in its first days open: the day it opens and two more
DAY_SCENT = 1.5         # a flower with a day scent holds the bees, and pollen they bring takes this much more often

FADE = 12               # the leaves' last days: yellowing, charging at half
POD_DAYS = 21           # days from flower to ripe pod
SPRING_LEAVES = 10.5    # the day length past which a bare-flowering bulb's leaves come up
MOON_NEAR = 0.021       # a phase this close to full (or new) is that moon's day; the moon moves at most 0.04 a day
UNIT_PX = 20.0          # pixels per cm, at most, on a plate

SHAPES = ("strap", "broad", "grass")
SHAPE_LENGTH = {"strap": 1.0, "broad": 0.75, "grass": 1.1}   # leaf length for its stem, when the seed gives none
SHAPE_CHARGE = {"strap": 1.0, "broad": 1.3, "grass": 0.75}   # how much light a leaf of this shape catches
SHAPE_WEIGHT = {"strap": 5.0, "broad": 9.0, "grass": 3.0}    # its stroke on the plate, px
SHAPE_WAX = {"strap": 8.0, "broad": 11.0, "grass": 7.0}      # a waxy leaf's stroke, px: two edges and a gap
WAX_EDGE = 2.5          # each edge of a waxy leaf's doubled stroke, px
LEAF_STROKES = 2500     # the leaves' share of the strokes a drawing may have (the ground keeps 8,000)
FLOWER_INKS = ("red", "dark-red", "pink", "pale-pink", "orange", "yellow", "blue", "violet",
               "brown", "white", "black", "grey")
KEPT = ("kind", "wakes", "stands", "leaves", "stem", "flower", "scent", "multiplies", "leaf", "coat",
        "hardy", "opens")                    # what its own seed carries on (and variety, when uncrossed)

ASLEEP, LEAF, BARE = "asleep", "leaf", "bare"
OPEN = "flower open"
BUD_IN = "bud in the shoot"   # a bulb that woke with a flower in it carries its bud up inside the leaves
OVER = ("flower withered", "flower frosted", "bud eaten", "flower eaten")
PODS = ("pod", "pod ripe", "pod shed")
ORDINALS = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6, "seventh": 7,
            "eighth": 8, "ninth": 9, "tenth": 10, "eleventh": 11, "twelfth": 12, "one": 1, "two": 2,
            "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September",
          "October", "November", "December")

_NUM = r"(-?\d{1,6}(?:[.,]\d{1,6})?)"
_DATE = r"(\d{4}-\d{2}-\d{2})"
_HEADER = re.compile(r"^\s*(asleep|in leaf|in flower)[^\n]*?since\s+" + _DATE, re.I)
_SIDE = re.compile(r"^\s*the day\s*:\s*(shorter|longer)\s*than\s*" + _NUM, re.I)
_WARMTH = re.compile(r"^\s*warmth\s*:(.*)$", re.I)
_MOONS = re.compile(r"^\s*(full|new)\s*moons?\s*:\s*(\d{1,4})(?:.*?" + _DATE + r")?", re.I)
_SEP = r"(?:\s*cm\s*[:;=]?|\s*[:;=]|\s)\s*"   # "bulb at 3 cm: 12", or a hand's "bulb at 3; 12" or "bulb at 3 = 12"
_BULB = re.compile(r"^\s*bulb at\s*" + _NUM + _SEP + r"(?:strength\s*)?" + _NUM + r"(.*)$", re.I)
_ABOVE = re.compile(r"^\s*at\s*" + _NUM + r"\s*(?:cm)?\s*[:;=](.*)$", re.I)
_LEAVES = re.compile(r"(\d{1,3})\s*lea(?:f|ves)\b\s*(?:" + _NUM + r")?", re.I)
_STEM = re.compile(r"stem\s*" + _NUM, re.I)
_FLOWER = re.compile(r"(flower open|flower withered|flower frosted|bud in the shoot|bud eaten|flower eaten|pod ripe"
                     r"|pod shed|pod|bud)"
                     r"\s*(\d{1,4})?", re.I)


def _float(text, default=None):
    """A number as a hand wrote it (12 · -3.5 · 0,35), or the default. Never raises."""
    try:
        value = float(str(text).replace(",", "."))
    except (TypeError, ValueError):
        return default
    return value if math.isfinite(value) else default


def _clamp(value, lo, hi):
    return lo if value < lo else hi if value > hi else value


def _date(text):
    try:
        return datetime.date.fromisoformat(text)
    except (TypeError, ValueError):
        return None


def _tenth(value, rng):
    """A number to one decimal, rounded up or down by chance in proportion.

    The body keeps tenths. A sleeping bulb spends a few thousandths a day;
    rounded the plain way that would never show, and a weak leaf would
    never grow. Rounded by chance, it drops a tenth about once in
    twenty-five days, which is what it spends.
    """
    scaled = value * 10.0
    low = math.floor(scaled + 1e-9)
    return (low + (1 if rng.random() < scaled - low - 1e-9 else 0)) / 10.0


# ------------------------------------------------------------ reading a seed

class Seed:
    """What a seed says, read forgivingly: every line has a sane default."""

    def __init__(self, seed):
        seed = seed if isinstance(seed, dict) else {}
        self.rule = _wake_rule(hands.line(seed, "wakes", ""))
        opens = hands.line(seed, "opens", "").lower()
        self.opens = ("new" if re.search(r"\bnew\b", opens) else "full") if "moon" in opens else None
        self.stands = hands.num(seed, "stands", 70, 20, 200)
        self.stem = hands.num(seed, "stem", 25, 3, 120)
        leaves = hands.line(seed, "leaves", "2 strap").lower()
        count, self.leaf_cm = None, None
        for found in re.finditer(r"(\d{1,4}(?:[.,]\d+)?)(\s*cm)?", leaves):
            if found.group(2):                         # "25 cm": how long they grow
                self.leaf_cm = _clamp(_float(found.group(1), 20.0), 2.0, 150.0)
            elif count is None:                        # the first bare number: how many
                count = _float(found.group(1), 2.0)
        self.leaves = int(_clamp(count, 1, 12)) if count is not None else 2
        self.shape = next((w for w in SHAPES if w in leaves), "broad" if "blade" in leaves else "strap")
        self.bare = "spring" in leaves or "after the flower" in leaves
        flower = hands.line(seed, "flower", "6 white").lower()
        petals = re.search(r"\d{1,3}", re.sub(r"#[0-9a-f]{3,8}", " ", flower))   # a colour's digits are not petals
        self.petals = int(_clamp(int(petals.group()), 1, 12)) if petals else 6
        self.colour = _colour_in(flower)
        self.nodding = "nod" in flower
        self.scent = hands.word(seed, "scent", "none", ("none", "day", "dusk", "night"))
        many = hands.line(seed, "multiplies", "offsets").lower()
        self.multiplies = "both" if ("both" in many or ("seed" in many and "offset" in many)) else \
            "seed" if "seed" in many else "offsets"
        self.waxy = hands.word(seed, "leaf", "plain", ("waxy", "plain")) == "waxy"
        self.papery = "paper" in hands.line(seed, "coat", "none").lower()
        self.hardy = hands.num(seed, "hardy", -15, -30, 0)
        self.from_seed = hands.word(seed, "sown", "bulb", ("seed", "bulb")) == "seed"

    def hours(self) -> list:
        """The day lengths this bulb watches: its waking hour, and the spring leaves' hour if it flowers bare."""
        kept = [self.rule[1]] if self.rule[0] in ("grow", "shrink") else []
        if self.bare and SPRING_LEAVES not in kept:
            kept.append(SPRING_LEAVES)
        return kept


def _wake_rule(text):
    """`wakes:` as a rule: ('grow', hours), ('shrink', hours), ('warmth', degrees) or ('moon', 'full'|'new', count)."""
    text = str(text or "").lower()
    number = re.search(r"\d{1,4}(?:[.,]\d+)?", text)
    number = _float(number.group(), None) if number else None
    if "moon" in text:
        which = "new" if re.search(r"\bnew\b", text) else "full"
        count = number
        for said, value in ORDINALS.items():
            if count is None and re.search(r"\b%s\b" % said, text):
                count = value
        return ("moon", which, int(_clamp(count or 1, 1, 36)))
    if re.search(r"grow|lengthen|longer|rise", text):
        return ("grow", round(_clamp(number if number is not None else 10.0, 1.0, 23.0), 2))
    if re.search(r"shrink|shorten|shorter|fall|wane", text):
        return ("shrink", round(_clamp(number if number is not None else 11.0, 1.0, 23.0), 2))
    if "warm" in text or "degree" in text:
        return ("warmth", _clamp(number if number is not None else 100.0, 1.0, 5000.0))
    return ("warmth", 100.0)


def _colour_in(text):
    """The flower's ink from its seed line: '#c58fc4', 'pale pink', 'red'... White if none is found."""
    found = re.search(r"#[0-9a-f]{6}\b", text)
    if found:
        return found.group()
    text = re.sub(r"\b(pale|dark)[\s_]+", r"\1-", text)
    for word in re.findall(r"[a-z-]+", text):
        if word in FLOWER_INKS:
            return word
    return "white"


# ------------------------------------------------------------------ the body

class Bulb:
    """One bulb: where it sits, its strength, and what it has above the ground."""

    def __init__(self, x, strength):
        self.x = x
        self.strength = strength
        self.pod_to_come = False      # a bare flower's seed, waiting underground for the spring leaves
        self.flower_in = False        # next season's flower, made as it went down (or in the packet it came from)
        self.leaves = 0
        self.length = 0.0             # of its leaves, cm
        self.stem = 0.0               # cm
        self.flower = ""              # BUD_IN, bud, flower open, one of OVER or PODS, or nothing
        self.days = 0                 # days in that state (open, withered, pod)
        self.marks = set()            # bitten, cut, frost-burnt, eaten

    def above(self) -> bool:
        return bool(self.leaves or self.stem > 0 or self.flower)

    def clear_above(self):
        self.leaves, self.length, self.stem, self.flower, self.days, self.marks = 0, 0.0, 0.0, "", 0, set()


class Clump:
    """A whole plant: its clock and its bulbs."""

    def __init__(self):
        self.state = ASLEEP
        self.since = None             # the date of that state
        self.sides = {}               # hours -> "shorter" or "longer": where the day length lay, last it looked
        self.warmth = None            # gathered since the shortest day; None while it waits for it
        self.moons = 0                # full (or new) moons counted since it went down
        self.last_moon = None         # the day of the last one counted
        self.bulbs = []
        self.lost = 0                 # bulb lines past BULBS_MOST that were passed over in reading
        self.set_right = False        # a date in it lay in the future, and was taken as today

    def at(self, x):
        """The bulb sitting at x (to a millimetre), or None."""
        for bulb in self.bulbs:
            if abs(bulb.x - x) < 0.051:
                return bulb
        return None


def read(body, today=None) -> Clump:
    """A body as a Clump. Reads whatever it can, in any order; never raises.

    Given today, a date that has not come yet (a hand's slip of a digit)
    is taken as today, and the clump notes that it was set right: a clump
    'in leaf since' a year still to come would otherwise stand for ever.
    """
    clump = Clump()
    above = []
    try:
        text = "" if body is None else str(body)
    except Exception:
        text = ""
    for line in text.splitlines()[:600]:
        try:
            _read_line(clump, line, above)
        except Exception:
            continue                                   # a line no one can read is passed over
    for x, rest in above:
        bulb = clump.at(x)
        if bulb is not None and not bulb.above():
            try:
                _read_above(bulb, rest)
            except Exception:
                bulb.clear_above()
    if today is not None:
        if clump.since is not None and clump.since > today:
            clump.since, clump.set_right = today, True
        if clump.last_moon is not None and clump.last_moon > today:
            clump.last_moon, clump.set_right = None, True
    if clump.since is None:
        clump.since = today
    if clump.state == LEAF and not any(b.leaves for b in clump.bulbs):
        clump.state = BARE if any(b.above() for b in clump.bulbs) else ASLEEP
    elif clump.state != LEAF and any(b.leaves for b in clump.bulbs):
        clump.state = LEAF                             # leaves carried over by a hand: it is in leaf
    elif clump.state == ASLEEP and any(b.above() for b in clump.bulbs):
        clump.state = BARE                             # a flower standing with no leaf beside it
    return clump


def _read_line(clump, line, above):
    found = _BULB.match(line)
    if found:
        x, strength = _float(found.group(1)), _float(found.group(2))
        if x is None or strength is None:
            return
        if len(clump.bulbs) >= BULBS_MOST:             # no room in the clump: the line is passed over, and counted
            clump.lost += 1
            return
        strength = _clamp(strength, 0.0, MOST)
        x = round(_clamp(x, -500.0, 500.0), 1)
        if clump.at(x) is not None:                    # two bulbs written at one place: the second moves clear
            x = _clear_of(clump, x, _radius(strength))
        bulb = Bulb(x, strength)
        bulb.pod_to_come = "pod" in found.group(3).lower()
        bulb.flower_in = "flower" in found.group(3).lower()
        clump.bulbs.append(bulb)
        return
    found = _ABOVE.match(line)
    if found:
        x = _float(found.group(1))
        if x is not None and len(above) < 200:
            above.append((round(x, 1), found.group(2)))
        return
    found = _HEADER.match(line)
    if found:
        word = found.group(1).lower()
        clump.since = _date(found.group(2))
        clump.state = LEAF if word == "in leaf" else BARE if word == "in flower" else ASLEEP
        return
    found = _SIDE.match(line)
    if found:
        hours = _float(found.group(2))
        if hours is not None and 0.0 < hours < 24.0:
            clump.sides[round(hours, 2)] = found.group(1).lower()
        return
    found = _MOONS.match(line)
    if found:
        clump.moons = int(found.group(2))
        clump.last_moon = _date(found.group(3)) if found.group(3) else None
        return
    found = _WARMTH.match(line)
    if found:
        number = re.search(_NUM, found.group(1))
        clump.warmth = _clamp(_float(number.group(), 0.0), 0.0, 99999.0) if number else None


def _clear_of(clump, x, r) -> float:
    """The first place rightward of x where a bulb of radius r lies clear of every other bulb.

    The places worth trying are just past each bulb's right edge; the last
    of them, past the whole row, is always clear.
    """
    edges = sorted(other.x + _radius(other.strength) + r + 0.2 for other in clump.bulbs)
    for edge in edges:
        place = math.ceil(edge * 10.0 - 1e-6) / 10.0
        if place > x and all(abs(other.x - place) >= _radius(other.strength) + r + 0.2 - 1e-6 for other in clump.bulbs):
            return place
    return math.ceil((edges[-1] if edges else x) * 10.0) / 10.0 + 0.1


def _read_above(bulb, rest):
    """One bulb's line of what stands above the ground."""
    rest = rest.lower()
    found = _LEAVES.search(rest)
    if found:
        bulb.leaves = int(_clamp(int(found.group(1)), 0, 12))
        bulb.length = _clamp(_float(found.group(2), 1.0) if found.group(2) else 1.0, 0.0, 150.0)
    found = _STEM.search(rest)
    if found:
        bulb.stem = _clamp(_float(found.group(1), 0.0), 0.0, 150.0)
    found = _FLOWER.search(rest)
    if found:
        bulb.flower = found.group(1)
        bulb.days = int(found.group(2)) if found.group(2) else 0
        if bulb.flower in ("bud", OPEN) and bulb.stem <= 0:
            bulb.stem = 1.0
    if "bitten" in rest:
        bulb.marks.add("bitten")
    if re.search(r"\bcut\b", rest):
        bulb.marks.add("cut")
    if "frost-burnt" in rest or "frost burnt" in rest:
        bulb.marks.add("frost-burnt")
    if "eaten to the ground" in rest:
        bulb.marks.add("eaten")
        bulb.length = 0.0
        bulb.leaves = bulb.leaves or 1


def write(clump, s, today=None) -> str:
    """A Clump as the text of a body (see the docstring for what each line means)."""
    lines = [_header(clump, s, today)]
    for hours in s.hours():
        if hours in clump.sides:
            lines.append("the day: %s than %s h" % (clump.sides[hours], _cm(hours)))
    if s.rule[0] == "warmth":
        lines.append("warmth: none yet; it counts from the shortest day" if clump.warmth is None
                     else "warmth: %d since the shortest day" % int(clump.warmth))
    if s.rule[0] == "moon" and clump.state != LEAF:      # in leaf it does not count: the count starts at its going-down
        last = ", the last on %s" % clump.last_moon.isoformat() if clump.last_moon and clump.moons else ""
        lines.append("%s moons: %d since it went down%s" % (s.rule[1], clump.moons, last))
    lines += ["", "below the ground:"]
    for bulb in sorted(clump.bulbs, key=lambda b: b.x):
        lines.append("bulb at %s cm: %.1f%s%s" % (_cm(bulb.x), bulb.strength, ", a flower in it" if bulb.flower_in else "",
                                                  ", a pod to come" if bulb.pod_to_come else ""))
    lines += ["", "above the ground:"]
    standing = [b for b in sorted(clump.bulbs, key=lambda b: b.x) if b.above()]
    for bulb in standing:
        lines.append("at %s cm: %s" % (_cm(bulb.x), _above_words(bulb)))
    if not standing:
        lines.append("nothing")
    return "\n".join(lines) + "\n"


def _cm(x) -> str:
    """A number as the body writes it: 0, 3.9, -4.1, 9.25 (no trailing zeros)."""
    said = ("%.2f" % x).rstrip("0").rstrip(".")
    return "0" if said in ("-0", "") else said


def _header(clump, s, today):
    since = clump.since.isoformat() if clump.since else (today.isoformat() if today else "")
    if clump.state == LEAF:
        fading = bool(clump.since and today and (today - clump.since).days >= s.stands - FADE)
        return "in leaf since %s%s" % (since, ", yellowing" if fading else "")
    if clump.state == BARE:
        return "in flower without its leaves, since %s" % since
    return "asleep since %s" % since


def _above_words(bulb) -> str:
    parts = []
    if "eaten" in bulb.marks:
        parts.append("%d %s eaten to the ground" % (bulb.leaves, "leaf" if bulb.leaves == 1 else "leaves"))
    elif bulb.leaves:
        parts.append("%d %s %.1f cm" % (bulb.leaves, "leaf" if bulb.leaves == 1 else "leaves", bulb.length))
    if bulb.stem > 0:
        parts.append("stem %.1f cm" % bulb.stem)
    if bulb.flower:
        if bulb.flower in (OPEN, "pod") + OVER:
            parts.append("%s %d day%s" % (bulb.flower, bulb.days, "" if bulb.days == 1 else "s"))
        else:
            parts.append(bulb.flower)
    parts += [mark for mark in ("bitten", "cut", "frost-burnt") if mark in bulb.marks]
    return " · ".join(parts) or "nothing"


# ------------------------------------------------------------------ the clock

class Ticks:
    """What the clock saw today."""

    def __init__(self):
        self.crossed = {}             # hours -> "up" or "down", for each hour the day length passed today
        self.full = False             # today is a full moon's day
        self.new = False              # ...a new moon's
        self.counted = False          # a moon of its rule was counted today


def tick(clump, s, sky, today) -> Ticks:
    """Move the clump's clock on by one day under this sky. Only what its seed asks it to keep."""
    ticks = Ticks()
    length = _clamp(_float(getattr(sky, "daylength", None), 12.0), 0.0, 24.0)
    sides = {}
    for hours in s.hours():
        side = "longer" if length >= hours else "shorter"
        before = clump.sides.get(hours)
        if before is not None and before != side:
            ticks.crossed[hours] = "up" if side == "longer" else "down"
        sides[hours] = side
    clump.sides = sides
    if s.rule[0] == "warmth":
        if _shortest_day(sky, today, length):
            clump.warmth = 0.0
        elif clump.warmth is not None:
            clump.warmth += max(0.0, _float(getattr(sky, "warmth", 0.0), 0.0))
    phase = _clamp(_float(getattr(sky, "moon", None), 0.0), 0.0, 1.0)
    ticks.full = abs(phase - 0.5) <= MOON_NEAR
    ticks.new = phase <= MOON_NEAR or phase >= 1.0 - MOON_NEAR
    if s.rule[0] == "moon" and clump.state != LEAF and (ticks.full if s.rule[1] == "full" else ticks.new):
        if clump.last_moon is None or not 0 <= (today - clump.last_moon).days <= 5:
            clump.moons += 1
            clump.last_moon = today
            ticks.counted = True
    return ticks


def _shortest_day(sky, today, length) -> bool:
    """Is today the shortest day: 21 December where that is winter, 21 June south of the equator?

    Told by the date and the season, not by the day's length, so that a
    garden near the equator, whose shortest day is not much under twelve
    hours, still has one. A sky with no season falls back on the length.
    """
    if (today.month, today.day) not in ((12, 21), (6, 21)):
        return False
    season = getattr(sky, "season", None)
    if isinstance(season, str) and season:
        return season == "winter"
    return length < 12.0


def _whole(value, rng):
    """A number to a whole one, rounded up or down by chance in proportion (see _tenth), so a count keeps its fractions."""
    low = math.floor(value + 1e-9)
    return float(low + (1 if rng.random() < value - low - 1e-9 else 0))


def _in_winter(sky) -> bool:
    """Is it winter under this sky (by the season it gives, or by a short day if it gives none)?"""
    season = getattr(sky, "season", None)
    if isinstance(season, str) and season:
        return season == "winter"
    return _clamp(_float(getattr(sky, "daylength", None), 12.0), 0.0, 24.0) < 10.0


def _wakes(rule, clump, ticks) -> bool:
    """Has the clock reached the seed's hour today?"""
    if rule[0] == "grow":
        return ticks.crossed.get(rule[1]) == "up"
    if rule[0] == "shrink":
        return ticks.crossed.get(rule[1]) == "down"
    if rule[0] == "moon":
        return ticks.counted and clump.moons >= rule[2]
    return clump.warmth is not None and clump.warmth >= rule[1]


# --------------------------------------------------------------------- a day

def sprout(seed, ctx) -> str:
    """A bulb in the ground, asleep: a packet's bulb is ready to flower, a seed's is tiny.

    Planted in winter, a warmth-counting bulb counts from its planting; at
    any other time of year it waits for the next shortest day, so a seed
    that falls in spring comes up with its parents the next year and not
    in the summer. A plant that was here before (its tag is older than
    today) and has lost its body comes up as the bulblet left in the
    ground, whether its body was emptied or taken away.
    """
    s = Seed(seed)
    clump = Clump()
    clump.since = ctx.date
    sky = ctx.sky
    length = _clamp(_float(getattr(sky, "daylength", None), 12.0), 0.0, 24.0)
    clump.sides = {hours: ("longer" if length >= hours else "shorter") for hours in s.hours()}
    if s.rule[0] == "warmth" and _in_winter(sky):
        clump.warmth = 0.0
    if s.from_seed:
        strength = SEEDLING
    elif hands.num({"age": getattr(ctx, "age", 0)}, "age", 0, 0, 1e6) > 0:
        strength = LEFT_BEHIND
    else:
        strength = START
    clump.bulbs = [Bulb(0.0, strength)]
    clump.bulbs[0].flower_in = strength >= FLOWER_AT         # a bulb from a packet comes with its flower in it
    return write(clump, s, ctx.date)


def day(body, seed, ctx):
    """One day of a clump's life. Returns the new body and, now and then, a line for the almanac."""
    if hands.is_dead(body):
        return body, None
    s = Seed(seed)
    clump = read(body, ctx.date)
    if not clump.bulbs:
        return sprout(seed, ctx), "came up again from a bulblet left in the ground"
    sky = ctx.sky
    ticks = tick(clump, s, sky, ctx.date)
    said = []
    if clump.set_right:
        said.append("a date in it had not come yet: it counts from today")
    if clump.lost:
        said.append("had no room for more than %d bulbs: %d were lost" % (BULBS_MOST, clump.lost))
    if clump.state == LEAF:
        _stand(clump, s, ctx, said)
    _flowers(clump, s, ctx, ticks, said)
    cause = "withered"                                  # how a bulb that goes today went: spent, rotted or dried
    if clump.state != LEAF:
        cause = _sleep(clump, s, ctx) or cause
        if s.bare:
            if _wakes(s.rule, clump, ticks):
                _wake_bare(clump, s, ctx, said)
            if ticks.crossed.get(SPRING_LEAVES) == "up":
                _wake(clump, s, ctx, said, spring=True)
        elif _wakes(s.rule, clump, ticks):
            _wake(clump, s, ctx, said)
    if clump.state == LEAF and clump.since == ctx.date:
        cause = "withered"                              # it woke today: what took a bulb was the cost of its leaves
    if clump.state == BARE and not any(b.above() for b in clump.bulbs):
        clump.state, clump.since = ASLEEP, ctx.date
    for bulb in clump.bulbs:
        bulb.strength = _tenth(_clamp(bulb.strength, 0.0, MOST), ctx.rng)
        bulb.length = _tenth(bulb.length, ctx.rng)
        bulb.stem = _tenth(bulb.stem, ctx.rng)
    if clump.warmth is not None:                       # the body keeps whole degrees; the fractions are kept by chance
        clump.warmth = _whole(clump.warmth, ctx.rng)
    if all(bulb.strength < GONE for bulb in clump.bulbs):     # the last of them: it dies, and lies as it was
        for bulb in clump.bulbs:
            bulb.clear_above()
        clump.state, clump.since = ASLEEP, ctx.date
        return ("† %s, its last bulb %s\n" % (ctx.date.isoformat(), cause) + write(clump, s, ctx.date),
                "its last bulb %s" % cause)
    for bulb in list(clump.bulbs):
        if bulb.strength < GONE:
            clump.bulbs.remove(bulb)
            said.append("a small bulb %s" % cause)
    return write(clump, s, ctx.date), (said[0] if said else None)


def _stand(clump, s, ctx, said):
    """A day in leaf: leaves grow and gather light, buds start, and at the end the clump goes down."""
    sky = ctx.sky
    up = (ctx.date - clump.since).days if clump.since else 0
    if up >= s.stands:
        _go_down(clump, s, ctx, said)
        return
    fading = up >= s.stands - FADE
    grow = _clamp((sky.tmean + 2.0) / 12.0, 0.05, 1.0)
    light = sky.light / (sky.light + HALF_LIGHT) if sky.light > 0 else 0.0
    warm = _clamp((sky.tmean + 6.0) / 12.0, 0.15, 1.0) * (0.3 if sky.tmin < -2.0 else 1.0)
    wet = 1.0 if s.waxy else _clamp(0.45 + 2.0 * sky.wet, 0.45, 1.0)
    rich = 1.0 + 0.5 * hands.num(ctx.bed, "rich", 0.0, 0.0, 1.0)
    crowd = min(1.0, math.sqrt(CROWD / max(1, len(clump.bulbs))))
    burnt = 0
    for bulb in clump.bulbs:
        if not bulb.leaves or "eaten" in bulb.marks:
            continue
        full = _leaf_length(s, bulb.strength)
        if not fading:
            bulb.length = min(max(full, bulb.length), bulb.length + full * 0.08 * grow)
        if sky.tmin < s.hardy and "frost-burnt" not in bulb.marks:
            bulb.length *= 0.6
            bulb.marks.add("frost-burnt")
            burnt += 1
        share = min(1.0, bulb.length / _leaf_length(s, FLOWER_AT))      # a small bulb's small leaf gathers less
        gathered = RATE * bulb.leaves * share * light * warm * wet * rich * crowd * SHAPE_CHARGE[s.shape]
        bulb.strength = min(MOST, bulb.strength + gathered * (0.5 if fading else 1.0))
        if bulb.flower == BUD_IN:
            if fading:
                bulb.flower = ""                       # the leaves went down before the bud could come out
            elif bulb.length >= 0.5 * full:
                bulb.flower, bulb.days, bulb.stem = "bud", 0, 0.5     # (it was paid for when the bulb woke)
    if burnt:
        said.append("a hard frost burnt its leaves")


def _flowers(clump, s, ctx, ticks, said):
    """A day for every bud, flower and pod: stems grow, buds open, flowers end, pods ripen."""
    sky, rng = ctx.sky, ctx.rng
    grow = _clamp((sky.tmean + 2.0) / 12.0, 0.05, 1.0)
    fading = clump.state == LEAF and clump.since is not None and (ctx.date - clump.since).days >= s.stands - FADE
    was_open = any(b.flower in (OPEN, "flower withered", "flower frosted") + PODS for b in clump.bulbs)
    opened = frosted = 0
    for bulb in clump.bulbs:
        if bulb.flower == "bud":
            height = s.stem * (0.75 + 0.25 * min(1.0, bulb.strength / 24.0))
            bulb.stem = min(max(height, bulb.stem), bulb.stem + height * (0.14 if s.bare else 0.06) * grow)
            if sky.tmin < s.hardy:
                bulb.flower, bulb.days = "flower frosted", 0
                frosted += 1
            elif bulb.stem >= height - 0.05:
                if s.opens is None or (ticks.full if s.opens == "full" else ticks.new):
                    bulb.flower, bulb.days = OPEN, 0
                    opened += 1
        elif bulb.flower == OPEN:
            bulb.days += 1
            if sky.tmin < s.hardy / 3.0:
                bulb.flower, bulb.days = "flower frosted", 0
                frosted += 1
                continue
            ends = 0.04 + 0.012 * sky.warmth + (0.1 if sky.wind >= 6 else 0.0)
            ends += 0.15 if sky.rain >= 8 and not s.nodding else 0.0
            if bulb.days >= 30 or rng.random() < ends:
                if rng.random() < SETS_SEED[s.multiplies]:
                    bulb.strength -= POD_COST
                    if clump.state == LEAF:
                        bulb.flower, bulb.days = "pod", 0
                    else:
                        bulb.flower, bulb.days, bulb.pod_to_come = "flower withered", 0, True
                else:
                    bulb.flower, bulb.days = "flower withered", 0
        elif bulb.flower == "pod":
            bulb.days += 1
            if bulb.days >= POD_DAYS or (fading and bulb.days >= 7):
                bulb.flower, bulb.days = "pod ripe", 0     # ripe: today it may sow itself
            elif fading:
                bulb.flower, bulb.days = "flower withered", 0   # the leaves go down before it could ripen
        elif bulb.flower == "pod ripe":
            bulb.flower = "pod shed"
        elif bulb.flower in OVER:
            bulb.days += 1
            if clump.state != LEAF and bulb.days >= 5:
                bulb.clear_above()                     # a bare flower, withered, is gone
    if opened and not was_open:
        said.append("opened at the %s moon" % s.opens if s.opens else
                    "came into flower" + (", without its leaves" if clump.state == BARE else ""))
    if frosted:
        said.append("frost took its flowers")


def _sleep(clump, s, ctx):
    """A day asleep: the ground may dry a bulb or rot it. (What sleeping itself costs is paid on waking.)

    A coatless bulb shrivels on the dust-dry days of dry ground: a bed that
    keeps less than 0.8 of the rain, and most of all one that keeps half or
    less (the stones). The foot of the north wall, at 0.7, is a little dry;
    ordinary ground keeps it all, and there it does not shrivel.
    A papery one rots on each sodden day, far faster when it is warm, and
    the rot eats a little besides, so that a small bulb in sodden ground
    is lost whole while a large one only shrinks.

    Returns what the ground did to it today, in a word ('rotted',
    'shrivelled'), or None.
    """
    sky = ctx.sky
    share, eats, done = 0.0, 0.0, None
    wet = _clamp(_float(getattr(sky, "wet", None), 0.5), 0.0, 1.0)
    if not s.papery:
        dry_ground = _clamp((0.8 - hands.num(ctx.bed, "water", 1.0, 0.0, 5.0)) / 0.3, 0.0, 1.0)
        share, done = SHRIVEL * dry_ground * _clamp((DRY - wet) / DRY, 0.0, 1.0), "shrivelled"
    elif wet >= SODDEN:
        warm = 1.0 if _float(getattr(sky, "tmean", None), 0.0) >= ROT_WARM else ROT_COLD
        share, eats, done = ROT * warm, ROT_EATS * warm, "rotted"
    if not (share or eats):
        return None
    for bulb in clump.bulbs:
        bulb.strength -= bulb.strength * share + eats
    return done


def _pay_for_sleep(clump, today):
    """On waking, every bulb pays for the days it slept: a small share of its strength for each, and KEEP besides.

    Paid all at once, so that a sleeping body lies still: while it sleeps
    only its clock, and dry or sodden ground, change it.
    """
    if clump.state != ASLEEP or clump.since is None or today is None:
        return
    slept = _clamp((today - clump.since).days, 0, 3660)
    for bulb in clump.bulbs:
        bulb.strength = bulb.strength * (1.0 - UPKEEP) ** slept - KEEP * slept


def _wake(clump, s, ctx, said, spring=False):
    """The clock has struck: every bulb puts up its leaves (a bare-flowering bulb's pods come with them).

    The leaves are paid for now, in full, by their size: a bulb that has
    not the strength for them spends what it has on them and is gone. A
    bulb with a flower in it (made as it last went down, or come in a
    packet) carries its bud up in the shoot, however the winter treated
    it, and pays for it now too; so does a bulb a hand has fed to
    flowering strength. The bud comes out when the leaves are half grown.
    """
    _pay_for_sleep(clump, ctx.date)
    risen = 0
    for bulb in clump.bulbs:
        if bulb.strength < GONE or bulb.leaves:
            continue
        stem, flower, days = bulb.stem, bulb.flower, bulb.days
        bulb.clear_above()
        bulb.stem, bulb.flower, bulb.days = stem, flower, days          # a bare flower still standing stays
        to_flower = not s.bare and not flower and (bulb.flower_in or bulb.strength >= FLOWER_AT)
        if not s.bare:
            bulb.flower_in = False
        bulb.leaves = _leaf_count(s, bulb.strength)
        bulb.length = 0.5
        bulb.strength -= _leaf_cost(s, bulb.strength) * bulb.leaves
        if to_flower:
            bulb.flower, bulb.days = BUD_IN, 0
            bulb.strength -= _bud_cost(s)
        if bulb.pod_to_come:
            bulb.pod_to_come = False
            bulb.flower, bulb.days, bulb.stem = "pod", 0, max(bulb.stem, 3.0)
        risen += 1
    if not risen:
        if clump.state == ASLEEP:
            clump.since = ctx.date                 # paid up to today
        return
    clump.state, clump.since = LEAF, ctx.date
    clump.moons, clump.last_moon = 0, None
    if not spring:
        clump.warmth = None
    pods = sum(1 for b in clump.bulbs if b.flower == "pod")
    if pods:                                       # its waking is not news; a pod riding up with the leaves is
        said.append("put up its leaves, and %s with them" % ("a seed pod" if pods == 1 else "%d seed pods" % pods))


def _wake_bare(clump, s, ctx, said):
    """A bulb whose leaves keep to the spring: its flowers come up alone. (Its flowering is what is said.)"""
    _pay_for_sleep(clump, ctx.date)
    budded = 0
    for bulb in clump.bulbs:
        if (bulb.flower_in or bulb.strength >= FLOWER_AT) and not bulb.flower and bulb.strength >= GONE:
            bulb.flower, bulb.days, bulb.stem = "bud", 0, 0.5
            bulb.strength -= _bud_cost(s)
            budded += 1
        bulb.flower_in = False
    clump.warmth = None
    clump.moons, clump.last_moon = 0, None
    if clump.state == ASLEEP:
        clump.since = ctx.date                     # paid up to today, flowering or not
        if budded:
            clump.state = BARE


def _go_down(clump, s, ctx, said):
    """The leaves are spent: all that stands is gone, and the strong bulbs split, where the clump has room."""
    made = 0
    split = SPLIT[s.multiplies]
    for bulb in sorted(clump.bulbs, key=lambda b: -b.strength):
        times = 0
        if bulb.strength >= split:
            times = 2 if s.multiplies == "offsets" and bulb.strength >= split + 10 else 1
        for _ in range(times):
            if len(clump.bulbs) >= BULBS_MOST:
                break
            place = _room_beside(clump, bulb, s, ctx.rng)
            if place is None:
                break
            clump.bulbs.append(Bulb(place, OFFSET))
            bulb.strength -= OFFSET_COST
            made += 1
    for bulb in clump.bulbs:
        bulb.clear_above()
        bulb.flower_in = bulb.strength >= FLOWER_AT        # next season's flower is made now, or not at all
    clump.state, clump.since = ASLEEP, ctx.date
    clump.moons, clump.last_moon = 0, None
    clump.warmth = None
    if made:                                       # its dying back is not news; new bulbs are
        said.insert(0, "died back with %s beside the old (%d in all)" % (
            "a new bulb" if made == 1 else "%d new bulbs" % made, len(clump.bulbs)))


def _grown(s) -> float:
    """The radius a bulb of this seed grows to before it splits: the room each one in a clump is given."""
    return _radius(min(MOST, SPLIT[s.multiplies]))


def _room_beside(clump, mother, s, rng):
    """A place for a new bulb beside its mother, as near as there is room for both to grow, or None.

    Every bulb is given room for the size it grows to before it splits,
    so that a clump that has thickened for years is still a row of bulbs
    that can be counted, and not one band. Where there is no such place
    within reach, no offset is made that year.
    """
    grown = _grown(s)
    reach = max(_radius(mother.strength), grown) + grown + 0.3
    sides = [-1, 1] if rng.random() < 0.5 else [1, -1]
    for step in range(0, 150):
        for side in sides:
            x = round(mother.x + side * (reach + 0.4 * step), 1)
            if abs(x) > 480:
                continue
            if all(abs(other.x - x) >= max(_radius(other.strength), grown) + grown + 0.2 for other in clump.bulbs):
                return x
    return None


def _bud_cost(s) -> float:
    return BUD_COST + s.stem / 15.0


def _leaf_count(s, strength) -> int:
    if strength < 4.0:
        return 1
    if strength < FLOWER_AT:
        return min(2, s.leaves)
    return s.leaves


def _size(strength) -> float:
    """How large a bulb's leaves are, against a flowering bulb's: from about a third, for the smallest, to all."""
    return 0.35 + 0.65 * min(1.0, max(0.0, strength) / FLOWER_AT)


def _leaf_length(s, strength) -> float:
    base = s.leaf_cm if s.leaf_cm else s.stem * SHAPE_LENGTH[s.shape]
    return max(1.0, base * _size(strength))


def _leaf_cost(s, strength) -> float:
    """What one leaf costs its bulb when it comes up: more for a leaf that catches more, less for a small one."""
    return LEAF_COST * SHAPE_CHARGE[s.shape] * _size(strength)


# ---------------------------------------------------- what creatures find in it

def flowers(body, seed, ctx) -> int:
    """How many flowers are open today."""
    if hands.is_dead(body):
        return 0
    return sum(1 for bulb in read(body).bulbs if bulb.flower == OPEN)


def bitten(body, seed, ctx, share, by):
    """A bite of `share` of what is soft: young shoots first, and buds. A pony crops flat instead.

    Returns the body after the bite, and a line for the almanac when it cost
    a flower or a whole shoot (a nibble is not news). The line begins with
    what the plant lost and ends with who took it ('lost a flower to
    slugs'), so that it reads after the plant's name as well as in the
    plant's own rings.
    """
    if hands.is_dead(body):
        return body, None
    s = Seed(seed)
    today = getattr(ctx, "date", None)
    clump = read(body, today)
    share = _clamp(_float(share, 0.0), 0.0, 1.0) * (0.5 if s.waxy else 1.0)
    who = " ".join(str(by or "something").split())[:40] or "something"
    soft = [b for b in clump.bulbs if (b.leaves and b.length > 0 and "eaten" not in b.marks)
            or b.flower in ("bud", OPEN)]
    if not soft or share <= 0:
        return body, None
    rng = getattr(ctx, "rng", None) or random.Random(len(str(body)))
    buds = flowers_lost = eaten = 0
    if who.lower() in ("pony", "the pony"):
        for bulb in soft:                            # it crops flat, at the height of its reach into the bed
            if bulb.length > 6.0:
                bulb.length = 6.0
                bulb.marks.add("cut")
            if bulb.flower in ("bud", OPEN) and bulb.stem > 6.0:
                bulb.flower, bulb.days, bulb.stem = ("bud eaten" if bulb.flower == "bud" else "flower eaten"), 0, 6.0
        return write(clump, s, today), "cropped short by %s" % who
    budget = share * sum(b.leaves * b.length for b in soft)
    for bulb in sorted(soft, key=lambda b: b.length):   # the youngest shoots first
        if bulb.leaves and bulb.length > 0 and budget > 0 and "eaten" not in bulb.marks:
            take = min(bulb.length, budget / bulb.leaves)
            bulb.length = round(bulb.length - take, 1)
            budget -= take * bulb.leaves
            bulb.marks.add("bitten")
            if bulb.length < 0.5:
                bulb.length = 0.0
                bulb.marks.add("eaten")
                eaten += 1
                if bulb.flower == BUD_IN:            # the bud was in the shoot that was eaten
                    bulb.flower, bulb.days, bulb.stem = "bud eaten", 0, 0.0
                    buds += 1
        if bulb.flower in ("bud", OPEN) and rng.random() < min(0.8, 2.0 * share):
            if bulb.flower == "bud":
                buds += 1
            else:
                flowers_lost += 1
            bulb.flower, bulb.days = ("bud eaten" if bulb.flower == "bud" else "flower eaten"), 0
            bulb.stem = round(bulb.stem * 0.5, 1)
    words = None
    if buds or flowers_lost:
        words = "lost %s to %s" % (_counted(flowers_lost, "flower", buds, "bud"), who)
    elif eaten:
        shoots = "its shoots" if eaten >= len(clump.bulbs) else \
            "the shoots of %s" % ("one bulb" if eaten == 1 else "%d bulbs" % eaten)
        words = "lost %s to %s" % (shoots, who)
    return write(clump, s, today), words


def _counted(a, a_word, b, b_word) -> str:
    """'a flower', '2 buds', 'a flower and 2 buds': two counts of things in plain words."""
    def one(n, word):
        return "a %s" % word if n == 1 else "%d %ss" % (n, word)
    said = [one(n, word) for n, word in ((a, a_word), (b, b_word)) if n]
    return " and ".join(said)


def cast(body, seed, ctx) -> list:
    """Seed that falls today: a crossed one if pollen of another bulb was brought to an open flower, else a ripe pod's own.

    A flower takes pollen only in its first days open (TAKES), and each
    such flower brought a grain of another bulb's pollen sets a crossed
    seed with a chance that follows how readily its own seed sets seed
    (a clump that multiplies by offsets rarely crosses; one that lives by
    seed often does). A day scent holds the bees, and their pollen takes
    more often. At most one seed falls from a clump in a day.
    """
    if hands.is_dead(body):
        return []
    s = Seed(seed)
    clump = read(body)
    rng = ctx.rng
    taking = sum(1 for b in clump.bulbs if b.flower == OPEN and b.days < TAKES)
    if taking:
        try:
            grains = [g for g in list(getattr(ctx, "pollen", None) or [])[:24] if _donor(g, ctx)]
        except Exception:
            grains = []
        chance = CROSSES * SETS_SEED[s.multiplies] / SETS_SEED["both"]
        for grain in grains[:taking]:
            held = DAY_SCENT if s.scent == "day" and str(getattr(grain, "by", "")).lower() == "bees" else 1.0
            if rng.random() < chance * held:
                return [_crossed(seed, grain.seed, ctx.where, str(grain.where))]
    ripe = sum(1 for b in clump.bulbs if b.flower == "pod ripe")
    if ripe and rng.random() < 1.0 - (1.0 - SOWS[s.multiplies]) ** min(ripe, 4):
        return [_own_seed(seed)]
    return []


def _donor(grain, ctx) -> bool:
    """Is this grain the pollen of another bulb? (Its seed says so, or, if a hand took its kind line out, its kind.)"""
    donor = getattr(grain, "seed", None)
    where = str(getattr(grain, "where", "") or "")
    if not isinstance(donor, dict) or not where or where == getattr(ctx, "where", None):
        return False
    return hands.word(donor, "kind", "") == KIND or str(getattr(grain, "kind", "") or "").strip().lower() == KIND


def _kept(seed) -> dict:
    return {key: seed[key] for key in KEPT if key in seed}


def _own_seed(seed) -> str:
    """The same seed again, variety and all, but a seed now, not a bulb."""
    kept = _kept(seed)
    if "variety" in seed:
        kept["variety"] = seed["variety"]
    kept["kind"] = KIND
    kept["sown"] = "seed"
    return hands.write_keys(kept)


def _crossed(seed, donor, mother, father) -> str:
    """The mother's seed, with the colours of both parents blended, and petals and stem between theirs."""
    mine, theirs = Seed(seed), Seed(donor)
    kept = _kept(seed)
    kept["kind"] = KIND
    colour = hands.mix(_hex(mine.colour), _hex(theirs.colour), 0.5)
    petals = int(round((mine.petals + theirs.petals) / 2.0))
    kept["flower"] = "%d %s%s" % (petals, colour, ", nodding" if mine.nodding else "")
    kept["stem"] = "%g" % round((mine.stem + theirs.stem) / 2.0, 1)
    kept["sown"] = "seed"
    kept["from"] = "cross of %s × %s" % (mother, father)
    return hands.write_keys(kept)


def _hex(colour) -> str:
    if colour.startswith("#"):
        return colour
    try:
        import plate
        return plate.INKS.get(colour, "#ffffff")
    except Exception:
        return "#ffffff"


# ----------------------------------------------------------------- in words

def describe(body, seed, ctx) -> str:
    """One short line: how many bulbs, and what the clump is doing."""
    if hands.is_dead(body):
        return "dead; its bulbs have withered away"
    today = getattr(ctx, "date", None)
    clump = read(body, today)
    n = len(clump.bulbs)
    bulbs = "%d bulb%s" % (n, "" if n == 1 else "s")
    in_flower = sum(1 for b in clump.bulbs if b.flower == OPEN)
    if clump.state == LEAF:
        s = Seed(seed)
        up = (today - clump.since).days if clump.since and today else 0
        words = "%s in leaf" % bulbs + (", %d in flower" % in_flower if in_flower else "")
        return words + (", yellowing" if up >= s.stands - FADE else "")
    if clump.state == BARE:
        return "%s; %d in flower, without leaves" % (bulbs, in_flower) if in_flower else "%s; buds up, without leaves" % bulbs
    when = " since %d %s" % (clump.since.day, MONTHS[clump.since.month - 1]) if clump.since else ""
    return "%s, asleep%s" % (bulbs, when)


def size(body, seed) -> float:
    """For its dot on the plan: what stands above the ground (leaves and stems, 15 cm to a unit), and half a unit
    for every bulb under it. A clump asleep is small on the plan, however long its body reads."""
    clump = read(body)
    above = sum(b.leaves * b.length + b.stem for b in clump.bulbs if b.above())
    return above / 15.0 + 0.5 * len(clump.bulbs)


# ------------------------------------------------------------------ drawing

def _radius(strength) -> float:
    """A bulb's radius in cm: its area is its strength."""
    return 0.45 * math.sqrt(max(0.0, strength))


def _depth(radius) -> float:
    """How deep a bulb's centre lies, cm: the bigger it is, the deeper its roots have pulled it."""
    return 2.0 + 4.0 * radius


def _pixel(clump) -> float:
    """About how many cm one pixel of the plate will stand for, reckoned from how big the drawing is.

    The pen's places are in cm and its sizes in pixels, and the scale
    between them is known only when the plate settles. The few marks that
    sit beside something (a bite just past a leaf's tip, the coat just
    outside a bulb, a pod above it) must stand off it by a few pixels
    whatever the scale, so the kind reckons the scale beforehand as the
    plate will: the whole drawing fitted into a plate's box, never more
    than UNIT_PX to the cm. On a bed's sheet, where the box is smaller,
    those marks sit a little wider.
    """
    if not clump.bulbs:
        return 1.0 / UNIT_PX
    xs = [b.x for b in clump.bulbs]
    rmax = max(_radius(b.strength) for b in clump.bulbs)
    reach = max([b.length for b in clump.bulbs] + [0.0])
    top = max([max(b.length, b.stem + 4.0 if b.stem > 0 else 0.0) for b in clump.bulbs] + [0.0])
    width = (max(xs) - min(xs)) + 2.0 * (rmax + 0.5) + 1.8 * reach
    height = top + _depth(rmax) + rmax + 0.5
    return max(1.0 / UNIT_PX, width / 770.0, height / 840.0)


def draw(body, seed, ctx, pen) -> None:
    """The ground line, the bulbs under it, and what stands above them (see the docstring)."""
    s = Seed(seed)
    dead = hands.is_dead(body)
    today = getattr(ctx, "date", None)
    clump = read(body, today)
    left = getattr(ctx, "left", None)
    was = read(left) if left is not None else None
    pen.unit_name = "cm"
    pen.unit_px_max = UNIT_PX
    pen.ground(0)
    px = _pixel(clump)
    fading = bool(clump.state == LEAF and clump.since and today and (today - clump.since).days >= s.stands - FADE)
    leaves = sum(b.leaves for b in clump.bulbs if "eaten" not in b.marks) * (2 if s.waxy else 1)
    steps = int(_clamp(LEAF_STROKES / max(1, leaves), 2, 10))     # a crowded clump draws each leaf in fewer pieces
    for bulb in sorted(clump.bulbs, key=lambda b: b.x):
        old = was.at(bulb.x) if was is not None else None
        _draw_bulb(pen, s, bulb, old, dead, (was is None or old is None), px)
        if bulb.above():
            _draw_above(pen, s, bulb, old, dead, fading, (was is None), px, steps)
    pen.note(describe(body, seed, ctx))


def _draw_bulb(pen, s, bulb, old, dead, new, px):
    """A bulb: a filled round (its new growth as a fresh ring), its coat, the flower it holds, a pod to come."""
    r = _radius(bulb.strength)
    cx, cy = bulb.x, -_depth(r)
    wood = "dead" if dead else "wood"
    pen.arc(cx, cy, r, 0, 360, 8, "paper")        # a hair of clear paper round it: bulbs that touch stay two
    if dead or new:
        _disc(pen, cx, cy, r, "dead" if dead else "fresh", px)
    else:
        r_old = min(r, _radius(old.strength))
        if r > r_old + 0.03:
            _disc(pen, cx, cy, r, "fresh", px)    # the whole round in the fresh ink, and what was there over it:
        _disc(pen, cx, cy, r_old, wood, px)       # the new growth shows as a ring, with no seam between
    if s.papery:
        ink = "dead" if dead else ("fresh" if new else wood)
        ring = r + 4.0 * px
        for k in range(10):                       # dry and broken like the skin itself; a gap at the top for the shoot
            pen.arc(cx, cy, ring, k * 36 + 97, k * 36 + 119, 2, ink)
    if not dead and _holds_flower(bulb):
        pen.dot(cx, cy, 8, "paper")               # on a ring of paper, so it shows on any planter's ink
        pen.dot(cx, cy, 5, s.colour)
    if bulb.pod_to_come:
        pen.dot(cx, cy + r + 7.0 * px, 4, wood)


def _holds_flower(bulb) -> bool:
    """Is there a flower in this bulb, not yet up? Next season's, made as it went down; a bud in the shoot; or the
    strength to make one (a bulb in leaf that has grown strong, or one a hand has fed)."""
    if bulb.flower == BUD_IN or bulb.flower_in:
        return True
    if bulb.flower in ("bud", OPEN):
        return False
    return bulb.strength >= FLOWER_AT


def _disc(pen, cx, cy, r, ink, px=0.05):
    """A filled round of radius r (cm): level bands, finer toward the top and bottom, and a smooth edge round them.

    Bands are cells, which scale with the plant as a round must, on a plate
    or on a bed's sheet alike. Their edges lie at equal steps of angle and
    each is as wide as the round at its middle, so the stair of their ends
    strays from the true edge by a few hundredths of r at most; the one
    arc drawn round them covers that stair, and makes the edge a line.
    """
    if not r > 0:
        return
    size = r / px                                  # its radius on the plate, about, in pixels
    bands = 32 if size >= 20 else 16 if size >= 7 else 8
    for i in range(bands):
        y0 = r * math.sin(math.pi * (i / bands - 0.5))
        y1 = r * math.sin(math.pi * ((i + 1) / bands - 0.5))
        mid = (y0 + y1) / 2.0
        half = math.sqrt(max(0.0, r * r - mid * mid))
        if half > 0 and y1 > y0:
            pen.cell(cx - half, cy + y0, 2.0 * half, y1 - y0, ink)
    pen.arc(cx, cy, r, 0, 360, 4, ink)


def _draw_above(pen, s, bulb, old, dead, fading, new, px, steps=10):
    """A bulb's shoot, leaves, stem, and what the stem carries."""
    r = _radius(bulb.strength)
    x, top = bulb.x, -_depth(r) + r
    wood = "dead" if dead else "wood"
    fresh = "dead" if dead else "fresh"
    was_up = not new and old is not None and old.above()
    pen.line(x, top, x, 0.0, 3, wood if was_up else fresh)
    ink, new_ink = ("dead", "dead") if dead or fading else (wood, fresh)      # yellowing overrides the fresh ink
    if "eaten" in bulb.marks:
        pen.dot(x, 7.0 * px, 7, "ink", filled=False, weight=3)             # an open ring at the ground: shoots eaten
    elif bulb.leaves:
        full = _leaf_length(s, bulb.strength)
        before = min(old.length, bulb.length) if was_up and old.leaves else 0.0
        weight = SHAPE_WAX[s.shape] if s.waxy else SHAPE_WEIGHT[s.shape]
        for i in range(bulb.leaves):
            pts = _leaf(x, -1 if i % 2 == 0 else 1, i // 2, bulb.length, min(1.0, bulb.length / full), fading, steps)
            if "frost-burnt" in bulb.marks and not (dead or fading):
                burn = _length(pts) * 0.7                   # the last third of a burnt leaf is dun
                _stroke(pen, _part(pts, 0.0, burn), before, weight, ink, new_ink)
                _stroke(pen, _part(pts, burn, None), 0.0, weight, "dead", "dead")
            else:
                _stroke(pen, pts, before, weight, ink, new_ink)
            if s.waxy:
                _wax(pen, pts, weight, px)
            _harm(pen, bulb, pts, px)
    if bulb.stem > 0:
        before = min(old.stem, bulb.stem) if was_up else 0.0
        h = bulb.stem
        _stroke(pen, [(x, 0.0), (x, h)], before, 4, ink, new_ink)
        head, hanging = (x, h), s.nodding and bulb.flower in ("bud", OPEN, "flower withered", "flower frosted")
        if hanging:
            hook = [(x, h), (x + 0.5, h + 0.7), (x + 1.2, h + 0.7), (x + 1.6, h + 0.1)]
            pen.polyline(hook, 4, ink if before >= h - 0.05 else new_ink)
            head = hook[-1]
        _draw_flower(pen, s, bulb, old, head, hanging, dead, new, px)


def _harm(pen, bulb, pts, px):
    """The marks of harm at a leaf's tip: an open ring just past it (bitten), a bar across it (cut clean)."""
    tip, back = pts[-1], pts[-2]
    dx, dy = tip[0] - back[0], tip[1] - back[1]
    n = math.hypot(dx, dy) or 1.0
    ux, uy = dx / n, dy / n
    if "bitten" in bulb.marks:
        pen.dot(tip[0] + ux * 7.0 * px, tip[1] + uy * 7.0 * px, 7, "ink", filled=False, weight=3)
    if "cut" in bulb.marks:
        half = 7.0 * px
        pen.line(tip[0] + uy * half, tip[1] - ux * half, tip[0] - uy * half, tip[1] + ux * half, 3, "ink")


def _leaf(x0, side, rank, length, fullness, flop, steps=10):
    """The points of one arching leaf, from the ground at x0: young leaves stand, grown ones arch, spent ones lie."""
    lean = 8.0 + 15.0 * rank
    bend = 20.0 + 45.0 * fullness + (55.0 if flop else 0.0)
    pts, x, y = [(x0, 0.0)], x0, 0.0
    for i in range(steps):
        angle = math.radians(90.0 - side * (lean + bend * (i + 0.5) / steps))
        x += math.cos(angle) * length / steps
        y = max(0.15, y + math.sin(angle) * length / steps)
        pts.append((x, y))
    return pts


def _length(pts) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def _part(pts, start, end):
    """The piece of a line from `start` to `end` cm along it (end None: to its end)."""
    total = _length(pts)
    end = total if end is None else _clamp(end, 0.0, total)
    start = _clamp(start, 0.0, end)
    if end - start < 1e-9:
        return []
    out, run = [], 0.0
    for a, b in zip(pts, pts[1:]):
        length = math.hypot(b[0] - a[0], b[1] - a[1])
        first, run = run, run + length
        if length <= 0 or run <= start:
            continue
        if not out:
            out.append(_along(a, b, (start - first) / length))
        if run >= end:
            out.append(_along(a, b, (end - first) / length))
            return out
        out.append(b)
    return out


def _along(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _stroke(pen, pts, before, weight, old_ink, new_ink):
    """A stroke through pts: its first `before` cm in the old ink, the rest in the new."""
    if len(pts) < 2:
        return
    total = _length(pts)
    for piece, ink in ((_part(pts, 0.0, before), old_ink), (_part(pts, before, None), new_ink)):
        if len(piece) < 2 or _length(piece) < 1e-6 or total < 1e-6:
            continue
        pen.polyline(piece, weight, ink)


def _wax(pen, pts, weight, px):
    """A waxy leaf's doubled stroke: a line of clear paper down its middle leaves its two edges.

    The paper runs to the very tip, where the round ends of the two lines
    close the leaf in a thin rim; it starts a little way up, where the
    leaves have parted, so that it does not cut into the leaves beside it
    at the foot.
    """
    total = _length(pts)
    middle = _part(pts, min(0.3 * total, 1.5 * weight * px), total)
    if len(middle) >= 2:
        pen.polyline(middle, weight - 2.0 * WAX_EDGE, "paper")


def _draw_flower(pen, s, bulb, old, head, hanging, dead, new, px):
    """What a stem carries: a bud, an open flower (a stroke to a petal), a withered one, a pod, or the ring of a bite."""
    hx, hy = head
    state = bulb.flower
    colour = "dead" if dead else s.colour
    petal = _clamp(s.stem * 0.13, 1.5, 4.0)
    if state == "bud":                             # the petals still closed: one stroke along the stem's way
        reach = petal * 0.55
        pen.line(hx, hy, hx, hy - reach if hanging else hy + reach, 9, colour)
    elif state == OPEN and hanging:                # a bell: the petals hang side by side, flaring a little
        n = s.petals
        for k in range(n):
            side = k - (n - 1) / 2.0
            angle = math.radians(270.0 + 12.0 * side)
            x0 = hx + 0.5 * side
            pen.line(x0, hy, x0 + math.cos(angle) * petal, hy + math.sin(angle) * petal, 7, colour)
    elif state == OPEN:                            # upright: the petals fanned from the stem's end
        n = s.petals
        for k in range(n):
            angle = math.radians(90.0 if n == 1 else 15.0 + 150.0 * k / (n - 1))
            pen.line(hx, hy, hx + math.cos(angle) * petal, hy + math.sin(angle) * petal, 7, colour)
    elif state in ("flower withered", "flower frosted"):      # limp and dun, hanging to one side: still a stroke a petal
        n = s.petals
        for k in range(n):
            angle = math.radians(285.0 + (50.0 * k / (n - 1) if n > 1 else 25.0))
            pen.line(hx, hy, hx + math.cos(angle) * petal * 0.6, hy + math.sin(angle) * petal * 0.6, 4, "dead")
    elif state in ("bud eaten", "flower eaten"):   # the head bitten off: an open ring just past the stem's end
        pen.dot(hx, hy + 7.0 * px, 7, "ink", filled=False, weight=3)
    elif state == "pod":                           # swelling: a filled round on the stem's end
        was_pod = not new and old is not None and old.flower in PODS
        pen.dot(hx, hy + 6.0 * px, 6, "dead" if dead else ("wood" if was_pod else "fresh"))
    elif state in PODS:                            # ripe and split: its two halves open like a V
        was_ripe = not new and old is not None and old.flower in ("pod ripe", "pod shed")
        ink = "dead" if dead else ("wood" if was_ripe else "fresh")
        spread = 12.0 * px
        pen.line(hx, hy, hx - 0.5 * spread, hy + spread, 4, ink)
        pen.line(hx, hy, hx + 0.5 * spread, hy + spread, 4, ink)
