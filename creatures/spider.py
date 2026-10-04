"""
The spider: a garden spider, and the one creature whose work is met at the hour someone comes.

From late August until the first hard frost she keeps a web between two real
plants in a bed. It holds what flew into it, beads with dew after clear cold
nights, bellies with the day's wind, breaks in a gale and is built again.
Before the cold takes her she leaves an egg sac, and in spring the
spiderlings go out on the wind: the almanac calls those days gossamer.

Her own file, ground/creatures/spider, says where she is in her year:

    spider: in her web           (or: waiting · without a web · gone)
    season: 2027
    web: long-border/web
    webs this season: 4
    caught this season: 6 bees, 3 moths
    egg sac: long-border/egg-sac · laid 2027-11-02
    gossamer: 2028-04-30

Any line may be changed by hand. What she has made is the truth of her: if a
hand takes her web away she spins another, and if a hand moves her into
the winter early she goes.

Her year, as the days live it:

  She comes. From 20 August, on a dry and quiet day, she is there (the
  spiderlings of the spring have grown up in the grass, or one came in on
  the wind).

  She spins. On a night when the air in a bed is still (the wind as the bed
  feels it, under force 3.5), she hangs a web between two plants that stand
  near each other in that bed: any kind, up three weeks or more, or a dead
  stem; the more flowers between them the likelier, and her own bed rather
  than another. Every few days she spins it afresh between the same two
  plants; now and then she moves. In the cold of late autumn her webs are
  smaller.

  A plant must stand above the ground to hold a thread, and she reads its
  body to know: a seed still lying in the ground, a bulb asleep with
  nothing above it, a reed or a bine with no stem up, a bough with fewer
  than three lengths of wood, a lichen's crust on its stone, a moss (a
  cushion a finger high, or a green film), a fern's crown with no living
  frond up, the small green heart a fern's spore comes up as, an empty
  body: none of these holds one. Where the body gives a height in cm (a
  bulb's leaves and stem, a reed's stems, a fern's fronds), the web is made
  small enough to hang below it; a fern stands as high as its fronds reach
  as they arch over, as its own plate draws them, not as long as they are.
  A kind whose body she cannot read stands, as far as she can tell. If one
  of her two plants stops standing (a bulb's flower withers and goes down,
  a hand cuts a reed to the rootstock, the first frost kills a fern's
  fronds), the web comes down.

  It catches. Whatever carries pollen through her bed that day (bees, moths,
  any creature whose flights the garden records) may fly into the web:
  most likely on the way to or from the two plants it hangs from. At most
  two a day. What it caught is written on the web, the latest twelve; she
  has eaten the ones before.

  The weather. After a clear, still night with a low under 10° in her bed
  it is beaded with dew at dawn, or white with rime if the night froze.
  The day's wind in her bed is written on it, and the web bellies with it.
  A wind of force 4.5 or more as her bed feels it tears it, and she spins
  again on the next still night. The more sheltered the bed, the harder
  the garden's wind must blow for that: about force 6 over the long border
  and the stones, 7 by the pond, a gale in the wild corner; in the keeper's
  border and under the north wall the wind never comes so hard.

  She goes. The first night that falls to -2° in her bed is the hard frost
  that ends her season (after 20 November any frost will do, and by 15
  December her season is over whatever the nights do). If she has not
  yet left her egg sac she leaves it then; mostly she has, in October or
  at the first frost. Her web hangs empty until the wind takes it down (a
  wind of force 4 in its bed, or three weeks), or until one of its two
  plants stops standing (the frost that ends her season may be the one that
  lays a fern's fronds down, and then the web comes down at once); while it
  hangs, the days' wind and dew are still written on it.

  The egg sac lies through the winter on a stem of one of the plants of her
  last web, if one of them still stands (or else in the shelter of that
  bed, or of the most sheltered bed if she had no web). On a mild day
  of spring the eggs hatch into a gold ball of spiderlings, and on the first
  warm, light-aired, dry day after that they go out on the wind, each on a
  thread of its own: a gossamer day. Sometimes there is a second. The empty
  sac weathers away by midsummer.

The web is a file, beds/<bed>/web, and the egg sac beds/<bed>/egg-sac. The
web's text names its two plants (and their heights, when their bodies gave
them: `heights: 30 cm · unknown`), how wide it is, its spokes and the turns
of its spiral, when it was spun, the day's wind and dew, and one line for
each thing it caught:

    caught: 2027-09-15 · a bee · flying to twig-3

A hand may change any of it, and the drawing follows the text.

The drawing (python shed/look.py beds/<bed>/web) is the web seen face on, as
it stood at the end of the last day lived. The two plants it hangs from
stand as grey uprights, named at their feet: as tall as they stand, where
the web knows their heights, and otherwise drawn only a little above the
highest thread tied to them (how tall such a plant is, its own plate
shows). The anchor threads run to them, and one guy line to the ground.
Then the frame, the spokes from the hub,
the few rings of the hub, the clear ring round it, and the sticky spiral.
Dew is pale blue beads on the spiral (white beads for rime), shown only on
the morning it fell; looked at after eleven, it has dried. The day's wind
bows the web to one side, deeper the harder it blew. Each thing caught is a
small dot in a ring of silk: yellow for a bee, brown for a moth, orange
for a hoverfly, black for anything else. She is drawn too, small and brown
and head down: at the hub in the dark and in the morning, and from ten
o'clock until dusk in her retreat at the web's top corner. A torn web is a
few threads hanging from its anchors. An empty one is grey, and still takes
the dew and the wind.

The egg sac's drawing (look.py beds/<bed>/egg-sac) is the stem it is fixed
to and the tuft of silk; in spring the gold ball of spiderlings, and once
they have gone, the opened sac and the threads they left on.

At an arrival while her web stands, she is met: the web beaded with dew in
the morning, bellying in the wind, or herself at its hub in the dark. Dew
is met from first light until ten; before first light she waits at the hub.
(First light is taken from the day's length, on a clock whose noon falls
near one o'clock, as it does across much of western Europe: half an hour before
sunrise, give or take the hour that summer time moves it.) After her season
an empty web is met only on a morning when the dew or the rime is on it.
"""

import datetime
import math
import re
import zlib

import hands

NAME = "spider"
WEB, SAC = "web", "egg-sac"
STILL = 3.5              # the wind in a bed (force) under which she spins
TEAR = 4.5               # the wind in her bed that tears a web
TAKEN_DOWN = 4.0         # the wind in its bed that takes an empty web down
NOON = 13.0              # the clock's hour nearest the sun's noon (as across much of western Europe: 12:40 in winter time, 13:40 in summer time)
LENGTHS_LEAST = 3        # lengths of stem a plant measured in lengths must have up to hold a thread
NARROWEST = 16           # cm across: the smallest web she spins
HARD = -2.0              # a night this cold in her bed ends her season
DEW_COLD = 10.0          # a clear still night with a low under this beads the web
CAUGHT_KEPT = 12         # catches written on the web; the earlier ones she has eaten
FLIGHT = 0.012           # the chance that a flight through her bed ends in the web
FLIGHT_NEAR = 0.05       # the same, for a flight to or from one of the web's two plants
CATCH_MOST = 2           # caught in one day, at the most
PLANTS_MOST = 24         # plants of one bed weighed as places for a web
UP_DAYS = 20             # a plant must have been up this many days (or be a dead stem) to hold a thread
MOVES = 0.08             # of the times she spins afresh, the share she spins somewhere new
MONTHS = ("January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December")

_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


# ------------------------------------------------------------ small things

def _date(text):
    found = _DATE.search(str(text or ""))
    if not found:
        return None
    try:
        return datetime.date.fromisoformat(found.group())
    except ValueError:
        return None


def _number(text, default, lo, hi) -> float:
    return hands.num({"n": str(text or "")}, "n", default, lo, hi)


def _said(day) -> str:
    return "%d %s" % (day.day, MONTHS[day.month - 1]) if day else ""


def _nth(n) -> str:
    n = int(n)
    return "%d%s" % (n, "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


def _crc(*parts) -> int:
    """A number that is always the same for the same words (Python's own hash() changes from run to run)."""
    return zlib.crc32("|".join(str(part) for part in parts).encode("utf-8", errors="replace"))


def _one(by) -> str:
    """What one of a creature is called: bees -> bee, hoverflies -> hoverfly."""
    by = " ".join(str(by or "something").lower().split())[:30] or "something"
    known = {"bees": "bee", "moths": "moth", "hoverflies": "hoverfly", "butterflies": "butterfly", "flies": "fly",
             "wasps": "wasp", "gnats": "gnat", "midges": "midge", "beetles": "beetle"}
    if by in known:
        return known[by]
    if by.endswith("ies"):
        return by[:-3] + "y"
    if by.endswith("s") and not by.endswith("ss"):
        return by[:-1]
    return by


def _a(word) -> str:
    return ("an " if word[:1] in "aeiou" else "a ") + word


def _shelter(bed) -> float:
    try:
        return max(0.0, min(1.0, float(bed.shelter)))
    except (AttributeError, TypeError, ValueError):
        return 0.5


def _wind_in(sky, bed) -> float:
    """The day's wind as a bed feels it."""
    return sky.wind * (1.0 - 0.8 * _shelter(bed))


def _low_in(sky, bed) -> float:
    """The night's low as a bed feels it."""
    return sky.tmin + 2.5 * _shelter(bed)


def _dew(sky, bed) -> str:
    """'dew' after a clear, still, cold night; 'rime' if it froze; '' otherwise."""
    if sky.cloud > 0.45 or sky.wind > 3.5 or sky.rain > 0.5:
        return ""
    low = _low_in(sky, bed)
    return "rime" if low < 0 else "dew" if low <= DEW_COLD else ""


def _gossamer_day(sky) -> bool:
    """Warm, dry, with a light air moving: a day for spiderlings to go out on the wind."""
    return sky.tmax >= 14 and 0.8 <= sky.wind <= 3.5 and sky.rain <= 0 and sky.cloud < 0.6


def _light(sky) -> tuple:
    """(first light, last light) as hours on the clock: half an hour of twilight either side of the day."""
    try:
        half = max(0.0, min(24.0, float(sky.daylength))) / 2.0
    except (AttributeError, TypeError, ValueError):
        half = 6.0
    return NOON - half - 0.5, NOON + half + 0.5


def _dark(sky, hour) -> bool:
    """Is it dark at this hour of the clock? (The middle of the hour is what counts.)"""
    first, last = _light(sky)
    return not first <= hour + 0.5 <= last


# ------------------------------------------------------------ what stands

_CM = re.compile(r"(\d{1,4}(?:\.\d+)?)\s*cm\b")
_SHOOT = re.compile(r"^(?:stem|left at \d+|right at \d+)\s+([\\/|]+)", re.I)

# The moss and the fern came into the garden after her, and at first she took a moss cushion a finger high, or a fern's
# sleeping crown, for a stem she could tie to (so the rehearsal's visitors found, the Opus among them, who mended it
# there first). She knows them now by the lines their own kinds read: a moss's `cushion: 12 by 12 cm` or its film's
# `protonema: 6 damp days of 20`; a fern's `crown: 2 buds` (a bine's crown is colours, never a number) or its
# prothallus's `prothallus: 23 damp days of 60`.
_MOSS = re.compile(r"^(?:cushion|protonema)\s*:\s*\d")
_FERN = re.compile(r"^(?:crown\s*:\s*\d|prothallus\s*:\s*\d)")
_FROND = re.compile(r"^frond\s+(\d{1,5})\b(.*)$")
_FROND_UP = re.compile(r"\bup\s+(\d{4}-\d{2}-\d{2})")
# A length is read from the start of a number only, as the fern reads it: tried from inside a long run of digits,
# the pattern would go over the rest of the run again from every digit, and one frond line of a few thousand digits
# kept her day past its time (she was set aside, and again each time she came back, while the fern stood so).
_FROND_CM = re.compile(r"(?<![\d.,])(\d+(?:[.,]\d+)?)\s*cm", re.I)
_FROND_UNROLLING = re.compile(r"\bunrolling\s*(\d{1,3})")
_FROND_GONE = re.compile(r"\b(killed by frost|frost|scorched|cut|died|dead|fell|withered)\b")
_FROND_STANDS = re.compile(r"\bunroll(?:ed|ing)\b")
FRONDS_READ = 48         # frond lines of one fern read at the most (the fern itself keeps 24 living and 24 dead)


def _standing(plant) -> tuple:
    """Does a plant stand above the ground, so that a thread can be tied to it? (yes or no, its height in cm or None)

    She reads what she can of its body. A dead plant's first line (the †)
    is passed over: what stood of it stands on, dead. The height is known
    only where a body gives it in cm (a bulb's leaves and stem, a reed's
    stems, a fern's fronds); a kind she cannot read stands, its height
    unknown. A moss and a fern are known by their bodies, or by their kind's
    name when a hand has left too little of the body to tell.

    (Reading bodies is a stopgap. If the garden one day tells creatures how
    tall a plant stands, as a number of cm in `plant.stands`, she takes
    that instead.)
    """
    try:
        told = getattr(plant, "stands", None)
        if isinstance(told, (int, float)) and not isinstance(told, bool) and told == told and abs(told) < 1e6:
            return told > 0, (float(told) if told > 0 else None)
    except Exception:
        pass
    try:
        lines = [line.strip() for line in str(plant.body or "").splitlines() if line.strip()]
    except Exception:
        return False, None
    if lines and lines[0].startswith("†"):
        lines = lines[1:]
    if not lines:
        return False, None                                   # an empty body: it is cut to the ground
    low = [line.lower() for line in lines]
    if low[0].startswith("a seed in the ground"):
        return False, None                                   # a stray's seed, not yet up
    if "above the ground:" in low:                           # a bulb: what stands is listed under that line
        above = [line for line in low[low.index("above the ground:") + 1:] if line != "nothing"]
        if not above:
            return False, None
        heights = [float(cm) for line in above for cm in _CM.findall(line.partition(":")[2])]
        return True, (max(heights) if heights else None)
    if any(line.startswith("rootstock:") for line in low):   # a reed: its stems, each with its length in cm
        heights = [float(cm) for line in low if line.startswith("stem ") for cm in _CM.findall(line)]
        return (True, max(heights)) if heights else (False, None)
    if low[0].startswith("stone:"):
        return False, None                                   # a lichen: a crust on a stone, nothing upright
    kind = str(getattr(plant, "kind", "") or "").strip().lower()
    if any(_MOSS.match(line) for line in low) or kind == "moss":
        return False, None                                   # a moss: a cushion a finger high, or a film on the ground
    if any(_FERN.match(line) for line in low) or kind == "fern":
        return _fern_standing(lines, getattr(plant, "seed", None))
    for line in low:
        if line.startswith("lengths grown:"):                # a bine
            grown = re.search(r"\d+", line)
            return (int(grown.group()) >= LENGTHS_LEAST if grown else False), None
    if low[0].startswith("# a bough"):                       # a bough: its lengths of wood, the remarks left out
        wood = sum(line.partition("#")[0].count("F") for line in lines)
        return wood >= LENGTHS_LEAST, None
    shoots = [_SHOOT.match(line) for line in lines]
    if any(shoots):                                          # a stray that is up: its stem, a length to a mark
        stem = next((found.group(1) for found in shoots if found and found.group(0).lower().startswith("stem")), "")
        return len(stem) >= LENGTHS_LEAST, None
    return True, None


def _fern_standing(lines, seed) -> tuple:
    """A fern holds a thread by its living fronds, and stands as high as the highest of them reaches.

    The fronds are read as the fern reads them: the lines under 'fronds:', save any that says how it died in place
    of how it stands (a hand may move a frond to the dead by writing 'cut' on it; words after 'unrolled' or
    'unrolling n%' are only a note); those under 'dead fronds:' lie along the ground. A crown
    with no living frond up (a fern asleep in winter), or a prothallus, holds none. Each frond rises from the crown
    and bends over by the seed's arch, the newest standing straightest, as the fern's own plate draws it: so its
    height is the highest point of that curve, not its length.
    """
    living, under_dead, numbers = [], False, set()
    for raw in lines:
        line = raw.strip()
        low = line.lower()
        if not line or line.startswith("#") or line.startswith(hands.DAGGER):
            continue
        if low.startswith("prothallus"):
            return False, None                               # the small green heart a spore comes up as: flat
        if low.startswith("dead fronds"):
            under_dead = True
            continue
        if low.startswith("fronds"):
            under_dead = False
            continue
        found = _FROND.match(low)
        if not found or int(found.group(1)) in numbers:
            continue
        numbers.add(int(found.group(1)))
        if len(numbers) > FRONDS_READ:
            break
        rest = found.group(2)
        gone, stands = _FROND_GONE.search(rest), _FROND_STANDS.search(rest)
        if under_dead or (gone and not (stands and stands.start() < gone.start())):
            continue
        cm = _FROND_CM.search(rest)
        try:
            length = max(0.0, min(400.0, float(cm.group(1).replace(",", ".")))) if cm else 0.0
        except ValueError:
            length = 0.0
        unrolling = _FROND_UNROLLING.search(rest)
        up = _FROND_UP.search(rest)
        living.append(((up.group(1) if up else ""), int(found.group(1)), length,
                       min(int(unrolling.group(1)), 99) if unrolling else 100))
    if not living:
        return False, None
    try:
        arch = hands.num(seed if isinstance(seed, dict) else {}, "arch", 0.6, 0.0, 1.0)
    except Exception:
        arch = 0.6
    living.sort()
    count, highest = len(living), 0.0
    for i, (_, _, length, unroll) in enumerate(living):
        lean = 8.0 + 11.0 * min(6, count - 1 - i)            # the newest stands straight, the oldest lean out
        highest = max(highest, _frond_rise(max(0.5, length), lean, arch * (0.5 + 0.5 * unroll / 100.0)))
    return True, round(highest, 1)


def _frond_rise(length, lean, arch, steps=14) -> float:
    """How high a frond `length` cm long reaches, leaning `lean` degrees and bending over by `arch` (as fern.py's
    _path lays its rachis, a piece at a time from the crown)."""
    y = top = 0.0
    for i in range(steps):
        t = (i + 0.5) / steps
        angle = math.radians(90.0 - min(108.0, lean + arch * 100.0 * t))
        y = max(0.3, y + math.sin(angle) * length / steps)
        top = max(top, y)
    return top


def _frame(width) -> tuple:
    """A web `width` cm across, as it is drawn: (how tall the picture of it is, the hub's x and y, its radius)."""
    tall = max(width * 1.05, 30.0) + 8.0
    return tall, width / 2.0, tall * 0.52, width * 0.40


def _highest_tie(width) -> float:
    """How high up its plants the web's highest threads are tied, at most (in cm)."""
    tall, cx, cy, radius = _frame(width)
    return cy + 0.98 * radius


def _across(apart, heights):
    """How wide a web she spins between plants this far apart (0..1.42 of the bed): a lower plant makes it smaller.
    None if no web of hers would hang below the lower of them."""
    across = int(round(max(22, min(64, 20 + apart * 110))))
    known = [height for height in heights if height is not None]
    if known:
        while across > NARROWEST and _highest_tie(across) > min(known):
            across -= 1
        if _highest_tie(across) > min(known):
            return None
    return across


# ------------------------------------------------------------ her own file

class State:
    """Her file, read forgivingly: where she is in her year, and what this season has held."""

    def __init__(self, text):
        keys = hands.read_keys(text)
        said = hands.line(keys, "spider", "waiting").lower()
        self.status = ("gone" if "gone" in said else "without" if "without" in said
                       else "in" if "web" in said else "waiting")
        self.season = int(hands.num(keys, "season", 0, 0, 9999))
        self.webs = int(hands.num(keys, "webs this season", 0, 0, 100_000))
        self.caught = {}
        for count, what in re.findall(r"(\d{1,6})\s+([a-z][a-z\-]*)", hands.line(keys, "caught this season", "").lower()):
            self.caught[_one(what)] = self.caught.get(_one(what), 0) + int(count)
        self.sac = hands.line(keys, "egg sac", "")
        laid = _date(self.sac)
        self.sac_season = laid.year if laid else 0
        self.gossamer = [_date(part) for part in hands.line(keys, "gossamer", "").split(",") if _date(part)]
        self.web = hands.line(keys, "web", "")

    def text(self) -> str:
        words = {"waiting": "waiting", "in": "in her web", "without": "without a web", "gone": "gone"}[self.status]
        tally = ", ".join(_many(what, count) for what, count in sorted(self.caught.items())) or "nothing yet"
        return ("# The spider: a garden spider, the one creature whose work is met at the hour someone comes.\n"
                "# From late August until the first hard frost she keeps a web between two plants in a bed; then she\n"
                "# leaves an egg sac, and in spring the spiderlings go out on the wind. The web and the sac lie in\n"
                "# the beds as things she made (look.py draws them). Any line here may be changed by hand.\n"
                "spider: %s\n"
                "season: %s\n"
                "web: %s\n"
                "webs this season: %d\n"
                "caught this season: %s\n"
                "egg sac: %s\n"
                "gossamer: %s\n" % (words, self.season or "none yet", self.web or "none", self.webs, tally,
                                    self.sac or "none",
                                    ", ".join(day.isoformat() for day in self.gossamer[-4:]) or "none yet"))


# ------------------------------------------------------------ the web, as text

class Web:
    """A web as its file says it."""

    def __init__(self):
        self.bed, self.a, self.b = "", "", ""
        self.heights = (None, None)         # how tall a and b stand, in cm, where their bodies said
        self.across, self.spokes, self.turns = 36, 24, 24
        self.spun, self.nth = None, 1
        self.wind = 0.0
        self.dew, self.rime = None, False
        self.caught = []                    # [(day, what, how)]
        self.torn, self.torn_by = None, ""
        self.empty = None


# The two names on a web's `between:` line, parted at ' · ' or ' and '. Each part is tried only from the first space
# of a run, so that a long run of spaces a hand left on the line is gone over once, not again from every space in it.
_BETWEEN = re.compile(r"(?<!\s)\s+·\s+|(?<!\s)\s+and\s+")
# An egg sac's `laid:` line, wherever it stands. The space before it is looked for on its own line only, so that a
# text of many empty lines is gone over once, not again from the start of every one.
_LAID = re.compile(r"^[^\S\n]*laid\s*:", re.M)


def read_web(text, bed="") -> Web:
    """A web's file, read as well as it can be. Never raises."""
    web = Web()
    web.bed = bed
    for raw in str(text or "").splitlines():
        key, colon, value = raw.strip().partition(":")
        key = key.strip().lower()
        if not colon:
            continue
        if key == "between":
            parts = [part.strip() for part in _BETWEEN.split(value.strip()) if part.strip()]
            if len(parts) >= 2:
                web.a, web.b = parts[0][:60], parts[1][:60]
        elif key == "heights":
            parts = (value.split("·") + ["", ""])[:2]
            web.heights = tuple(_number(part, None, 5.0, 400.0) if re.search(r"\d", part) else None
                                for part in parts)
        elif key == "across":
            web.across = int(_number(value, 36, 10, 120))
        elif key == "spokes":
            web.spokes = int(_number(value, 24, 5, 60))
        elif key == "spiral":
            web.turns = int(_number(value, 24, 3, 60))
        elif key == "spun":
            web.spun = _date(value)
            found = re.search(r"(\d{1,5})(?:st|nd|rd|th)", value)
            web.nth = int(found.group(1)) if found else 1
        elif key == "wind":
            web.wind = _number(value, 0.0, 0.0, 12.0)
        elif key == "dew":
            web.dew, web.rime = _date(value), "rime" in value.lower()
        elif key == "caught" and len(web.caught) < 60:
            parts = [part.strip() for part in value.split("·")]
            when = _date(parts[0]) if parts else None
            if when is not None:
                web.caught.append((when, (parts[1] if len(parts) > 1 else "something")[:40],
                                   (parts[2] if len(parts) > 2 else "")[:80]))
        elif key == "torn":
            web.torn = _date(value)
            web.torn_by = value.partition("·")[2].strip()[:80]
        elif key == "empty":
            web.empty = _date(value)
    return web


def _bellies(wind) -> str:
    if wind < 1.0:
        return "still air: it hangs flat"
    if wind < 2.5:
        return "it stirs"
    if wind < 4.0:
        return "it bellies a little"
    return "it bellies like a sail"


def web_text(web) -> str:
    lines = ["a web, spun by the spider in the %s, between %s and %s" % (web.bed, web.a, web.b), "",
             "between: %s · %s" % (web.a, web.b)]
    if any(height is not None for height in web.heights):
        lines.append("heights: %s" % " · ".join("unknown" if height is None else "%d cm" % round(height)
                                                for height in web.heights))
    lines += ["across: %d cm" % web.across,
             "spokes: %d" % web.spokes,
             "spiral: %d turns" % web.turns]
    if web.spun:
        lines.append("spun: %s · her %s web this season" % (web.spun.isoformat(), _nth(web.nth)))
    lines.append("wind: %.1f · %s" % (web.wind, _bellies(web.wind)))
    if web.dew:
        lines.append("dew: %s at dawn on %s" % ("white with rime" if web.rime else "beaded", web.dew.isoformat()))
    for when, what, how in web.caught[-CAUGHT_KEPT:]:
        lines.append("caught: %s · %s%s" % (when.isoformat(), what, " · " + how if how else ""))
    if web.torn:
        lines.append("torn: %s · %s" % (web.torn.isoformat(), web.torn_by or "by the wind"))
    if web.empty:
        lines.append("empty: %s · she is gone, and her season with her" % web.empty.isoformat())
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------ the egg sac, as text

class Sac:
    def __init__(self):
        self.on = ""
        self.laid = self.hatched = self.gone = None
        self.eggs = 400


def read_sac(text) -> Sac:
    sac = Sac()
    for raw in str(text or "").splitlines():
        found = re.match(r"\s*on a stem of (.+?), low down", raw)
        if found:
            sac.on = found.group(1).strip()[:60]
            continue
        key, colon, value = raw.strip().partition(":")
        key = key.strip().lower()
        if not colon:
            continue
        if key == "laid":
            sac.laid = _date(value)
        elif key == "eggs":
            sac.eggs = int(_number(value, 400, 0, 5000))
        elif key == "hatched":
            sac.hatched = _date(value)
        elif key == "gone":
            sac.gone = _date(value)
    return sac


def sac_text(sac, bed) -> str:
    lines = ["an egg sac, left by the spider in the %s" % bed,
             "on a stem of %s, low down" % sac.on if sac.on else "in the shelter of the %s, near the ground" % bed,
             ""]
    if sac.laid:
        lines.append("laid: %s" % sac.laid.isoformat())
    lines.append("eggs: about %d" % sac.eggs)
    if sac.hatched:
        lines.append("hatched: %s · a ball of spiderlings, gold, on the silk" % sac.hatched.isoformat())
    if sac.gone:
        lines.append("gone: %s · out on the wind, each on a thread (gossamer)" % sac.gone.isoformat())
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------ what flew

def _flights(garden) -> list:
    """Today's flights, as the pollen the creatures carried records them: [(who, from, to)].

    The Garden has no door of its own for this yet, so it is read from the
    pollen the ground holds for the day (looked at, never touched). If that
    cannot be had, nothing flew that she can know of.
    """
    try:
        pollen = getattr(getattr(garden, "_fauna", None), "pollen", None)
        if not isinstance(pollen, dict):
            return []
        found = []
        for receiver in sorted(pollen):
            for grain in list(pollen[receiver])[:24]:
                found.append((str(getattr(grain, "by", "") or "something"), str(getattr(grain, "where", "") or ""),
                              str(receiver)))
        return found
    except Exception:
        return []


def _catches(garden, ctx, web) -> list:
    """What flew into the web today: [(day, 'a bee', 'flying to twig-3', 'bees')], two at the most."""
    rng, mine = ctx.rng, web.bed + "/"
    anchors = {mine + web.a, mine + web.b}
    caught = []
    for by, giver, receiver in _flights(garden):
        if not (giver.startswith(mine) or receiver.startswith(mine)):
            continue
        near = giver in anchors or receiver in anchors
        if rng.random() >= (FLIGHT_NEAR if near else FLIGHT):
            continue
        how = ("flying to %s" % receiver[len(mine):]) if receiver.startswith(mine) else ("flying from %s" % giver[len(mine):])
        if by.lower() == "moths":
            how = "in the night, " + how
        caught.append((ctx.date, _a(_one(by)), how, _one(by)))
        if len(caught) >= CATCH_MOST:
            break
    return caught


# ------------------------------------------------------------ spinning

def _apart(a, b):
    """How far apart two plants stand in their bed, or None if their places cannot be read."""
    try:
        return math.hypot(a.at[0] - b.at[0], a.at[1] - b.at[1])
    except (TypeError, IndexError, ValueError):
        return None


def _spin(garden, ctx, st, beds, home=None, keep=None, avoid=None):
    """A new web, between two plants of a bed where the air is still tonight; None if there is nowhere.

    She needs something standing to hang it from: a plant up at least
    UP_DAYS days, or a dead stem, with something above the ground (see
    _standing). `home` is the bed she was in: she stays there if she can.
    `keep` is the pair her web hung from: if both still stand and the air
    there is still, she spins between them again. `avoid` is a pair she is
    leaving.
    """
    sky, rng = ctx.sky, ctx.rng
    by_bed, height = {}, {}
    for plant in garden.plants():
        if plant.dead or plant.age >= UP_DAYS:
            stands, tall = _standing(plant)
            if stands:
                by_bed.setdefault(plant.bed, []).append(plant)
                height[plant.where] = tall
    if keep and home in by_bed and home in beds and _wind_in(sky, beds[home]) < STILL:
        pair = {plant.name: plant for plant in by_bed[home] if plant.name in keep}
        if len(pair) == 2:
            a, b = pair[keep[0]], pair[keep[1]]
            apart = _apart(a, b)
            if apart is not None and 0.04 <= apart <= 0.45:
                across = _across(apart, (height[a.where], height[b.where]))
                if across is not None:
                    return _new_web(ctx, st, beds, home, a, b, across, height)
    flowers = {}

    def flowering(plant):
        if plant.where not in flowers:
            flowers[plant.where] = 0 if plant.dead else max(0, min(50, int(plant.flowers or 0)))
        return flowers[plant.where]

    choices, weights = [], []
    for name in sorted(by_bed):
        bed = beds.get(name)
        if bed is None or _wind_in(sky, bed) >= STILL:
            continue
        standing = sorted(by_bed[name], key=lambda plant: plant.name)[:PLANTS_MOST]
        for i, a in enumerate(standing):
            for b in standing[i + 1:]:
                apart = _apart(a, b)
                if apart is None or not 0.04 <= apart <= 0.45:
                    continue
                if avoid and name == home and {a.name, b.name} == set(avoid):
                    continue
                across = _across(apart, (height[a.where], height[b.where]))
                if across is None:
                    continue                        # too low a plant for any web of hers
                weight = 1.0 + min(12, flowering(a) + flowering(b))
                weight *= (0.5 if a.dead else 1.0) * (0.5 if b.dead else 1.0) * (4.0 if name == home else 1.0)
                choices.append((name, a, b, across))
                weights.append(weight)
    if not choices:
        return None
    name, a, b, across = rng.choices(choices, weights)[0]
    return _new_web(ctx, st, beds, name, a, b, across, height)


def _new_web(ctx, st, beds, name, a, b, across, height):
    """A web freshly spun between plants a and b of the bed `name`, `across` cm wide (see _across)."""
    sky, rng = ctx.sky, ctx.rng
    if b.at[0] < a.at[0]:
        a, b = b, a                                 # the western of the two on the left
    web = Web()
    web.bed, web.a, web.b = name, a.name, b.name
    web.heights = (height.get(a.where), height.get(b.where))
    web.across = across
    cold = sky.tmean < 9
    web.spokes = rng.randint(21, 31) - (3 if cold else 0)
    web.turns = rng.randint(18, 30) - (5 if cold else 0)
    web.spun, web.nth = ctx.date, st.webs + 1
    web.wind = round(_wind_in(sky, beds[name]), 1)
    dew = _dew(sky, beds[name])
    web.dew, web.rime = (ctx.date if dew else None), dew == "rime"
    return web


# ------------------------------------------------------------ the days

def _lay(garden, ctx, st, web, beds, old_sac, lines) -> None:
    """She leaves her egg sac: on a stem of one of her web's plants if one still stands, else in the shelter of
    that bed; in the most sheltered bed if she had no web."""
    rng = ctx.rng
    if old_sac is not None:
        garden.unmake(old_sac.bed, old_sac.name, "an old sac, weathered away")
    places = []
    if web is not None and web.bed in beds:
        standing = {plant.name for plant in garden.plants(bed=web.bed) if _standing(plant)[0]}
        places.append((web.bed, next((name for name in (web.b, web.a) if name and name in standing), "")))
    for bed in sorted(beds.values(), key=lambda bed: (-_shelter(bed), bed.name)):
        if bed.name not in [place for place, _ in places]:
            places.append((bed.name, ""))
    for bed, on in places[:4]:
        sac = Sac()
        sac.on, sac.laid, sac.eggs = on, ctx.date, 10 * rng.randint(30, 60)
        if garden.make(bed, SAC, sac_text(sac, bed)):
            st.sac, st.sac_season = "%s/%s · laid %s" % (bed, SAC, ctx.date.isoformat()), ctx.date.year
            lines.append("the spider has left an egg sac %s, in the %s"
                         % ("on a stem of %s" % on if on else "in the shelter there", bed))
            return
    st.sac, st.sac_season = "none could be laid · %s" % ctx.date.isoformat(), ctx.date.year


def _tend_sac(garden, ctx, st, thing, lines) -> None:
    """The egg sac through the spring: the gold ball, the gossamer days, and the empty sac weathering away."""
    sac, today, sky, rng = read_sac(thing.text), ctx.date, ctx.sky, ctx.rng
    if sac.gone:
        since = (today - sac.gone).days
        this_spring = [day for day in st.gossamer if day.year == today.year]
        if 1 <= since <= 12 and len(this_spring) == 1 and _gossamer_day(sky) and rng.random() < 0.5:
            st.gossamer.append(today)
            lines.append("gossamer again: more of the spiderlings went out on the wind")
        if today.month >= 7 or since >= 60:
            garden.unmake(thing.bed, thing.name, "the empty sac has weathered away")
        return
    if sac.laid is None or sac.laid.year >= today.year and today.month >= 7:
        return                                      # laid this autumn: it waits for the spring
    spring = (today.month == 3 and today.day >= 25) or today.month in (4, 5, 6)
    if spring and sac.hatched is None:
        if sky.tmean >= 11 and rng.random() < 0.25:
            sac.hatched = today
            garden.make(thing.bed, thing.name, sac_text(sac, thing.bed))
    elif spring and (today - sac.hatched).days >= 2 and (
            _gossamer_day(sky) or (today.month == 6 and today.day >= 15 and sky.wind <= 4)):
        sac.gone = today
        st.gossamer.append(today)
        garden.make(thing.bed, thing.name, sac_text(sac, thing.bed))
        lines.append("gossamer: the spiderlings went out on the wind from the egg sac in the %s (fils de la Vierge)"
                     % thing.bed)
    elif today.month >= 7 and sac.laid.year < today.year:
        sac.gone = today                            # they went unseen
        garden.make(thing.bed, thing.name, sac_text(sac, thing.bed))


def _down(garden, web, beds) -> str:
    """Why a web can hang no longer: one of its two plants is gone, or no longer stands (see _standing), or its bed
    is gone. '' while it can hang."""
    there = {plant.name: plant for plant in garden.plants(bed=web.bed)}
    fallen = [name for name in (web.a, web.b) if name not in there]
    sunk = [name for name in (web.a, web.b) if name in there and not _standing(there[name])[0]]
    if fallen:
        return "%s is gone" % fallen[0]
    if sunk:
        return "%s no longer stands" % sunk[0]
    return "" if web.bed in beds else "a plant it hung from is gone"


def _season_ends(garden, ctx, st, thing, web, beds, sac_thing, lines, why) -> None:
    """Her season is over: the egg sac if she has not left it, the web left empty, and she is gone.

    A web is left to hang empty only if both its plants still stand: the frost that ends her season can be the one
    that lays a fern's fronds down, and then the web comes down with them."""
    if st.sac_season != ctx.date.year:
        _lay(garden, ctx, st, web, beds, sac_thing, lines)
    down = ""
    if thing is not None and web is not None and not web.empty:
        down = _down(garden, web, beds)
        if down:
            garden.unmake(thing.bed, WEB, "a plant it hung from is gone")
        else:
            web.empty = ctx.date
            garden.make(thing.bed, WEB, web_text(web))
    st.status = "gone"
    if why:
        lines.append("%s: the spider is gone%s" % (
            why, "" if thing is None else ", and her web in the %s is down: %s" % (thing.bed, down) if down
            else ", and her web in the %s hangs empty" % thing.bed))


def _her_day(garden, ctx, st, thing, web, beds, lines) -> None:
    """A day of her season: the web stands, catches, beads and bellies; or tears; or is spun again."""
    sky, rng, today = ctx.sky, ctx.rng, ctx.date
    fell_from = None
    if web is not None:
        down = _down(garden, web, beds)
        if down:
            fell_from = web.bed
            garden.unmake(web.bed, WEB, "a plant it hung from is gone")
            lines.append("the spider's web in the %s came down: %s" % (web.bed, down))
            web = thing = None
    if web is not None and not web.torn and not web.empty:
        bed = beds[web.bed]
        wind = _wind_in(sky, bed)
        if wind >= TEAR:
            web.torn, web.torn_by, web.wind, web.dew = today, "by the wind, force %.1f" % wind, round(wind, 1), None
            garden.make(web.bed, WEB, web_text(web))
            st.status = "without"
            lines.append("the wind tore the spider's web in the %s" % web.bed)
            return
        for when, what, how, by in _catches(garden, ctx, web):
            web.caught.append((when, what, how))
            st.caught[by] = st.caught.get(by, 0) + 1
        web.caught = web.caught[-CAUGHT_KEPT:]
        web.wind = round(wind, 1)
        dew = _dew(sky, bed)
        web.dew, web.rime = (today if dew else None), dew == "rime"
        if web.spun and (today - web.spun).days >= 3 and wind < STILL and sky.rain < 6 and rng.random() < 0.22:
            if rng.random() < MOVES:
                new = _spin(garden, ctx, st, beds, home=web.bed, avoid=(web.a, web.b))
            else:
                new = _spin(garden, ctx, st, beds, home=web.bed, keep=(web.a, web.b))
            if new is not None and (new.bed == web.bed or garden.unmake(web.bed, WEB, "she spun elsewhere")):
                if garden.make(new.bed, WEB, web_text(new)):
                    st.webs, st.status = new.nth, "in"
                    return
        garden.make(web.bed, WEB, web_text(web))
        st.status = "in"
        return
    if web is not None:                             # torn: she spins again where it hung, if she can
        new = _spin(garden, ctx, st, beds, home=web.bed, keep=(web.a, web.b))
    else:
        new = _spin(garden, ctx, st, beds, home=fell_from)
    if new is None:
        st.status = "without"
        return
    if web is not None and new.bed != web.bed:
        garden.unmake(web.bed, WEB, "she spun elsewhere")
    if garden.make(new.bed, WEB, web_text(new)):
        st.webs, st.status = new.nth, "in"
        if new.nth == 1:
            lines.append("a garden spider has spun her web in the %s, between %s and %s" % (new.bed, new.a, new.b))
    else:
        st.status = "without"


def day(garden, ctx):
    st = State(ctx.state)
    today, sky, rng = ctx.date, ctx.sky, ctx.rng
    lines = []
    beds = {bed.name: bed for bed in garden.beds()}
    mine = sorted((thing for thing in garden.things() if thing.maker == NAME), key=lambda thing: thing.where)
    thing = next((each for each in mine if each.name == WEB), None)
    sac_thing = next((each for each in mine if each.name == SAC), None)
    web = read_web(thing.text, thing.bed) if thing is not None else None
    if sac_thing is not None:
        _tend_sac(garden, ctx, st, sac_thing, lines)
    in_season = (today.month == 8 and today.day >= 20) or today.month >= 9
    if st.status in ("waiting", "gone") and in_season and st.season != today.year:
        if sky.rain < 4 and sky.wind < 5 and rng.random() < 0.3:
            st.status, st.season, st.webs, st.caught = "without", today.year, 0, {}
    if st.status in ("in", "without"):
        bed = beds.get(thing.bed) if thing is not None else None
        low = _low_in(sky, bed)
        if not in_season or st.season != today.year:
            _season_ends(garden, ctx, st, thing, web, beds, sac_thing, lines, "")
        elif low <= HARD:
            _season_ends(garden, ctx, st, thing, web, beds, sac_thing, lines, "the first hard frost")
        elif today.month == 11 and today.day >= 20 and low < 0:
            _season_ends(garden, ctx, st, thing, web, beds, sac_thing, lines, "a frost this late in the year")
        elif today.month == 12 and today.day >= 15:
            _season_ends(garden, ctx, st, thing, web, beds, sac_thing, lines, "her season is over")
        else:
            _her_day(garden, ctx, st, thing, web, beds, lines)
            if st.sac_season != today.year and today.month >= 10 and (rng.random() < 0.04 or sky.tmin < 0):
                mine_now = [each for each in garden.things() if each.maker == NAME]
                web_now = next((each for each in mine_now if each.name == WEB), None)
                _lay(garden, ctx, st, read_web(web_now.text, web_now.bed) if web_now else None, beds,
                     next((each for each in mine_now if each.name == SAC), None), lines)
    elif st.status == "gone" and thing is not None:
        bed = beds.get(thing.bed)
        if bed is None or web.empty is None or _wind_in(sky, bed) >= TAKEN_DOWN or (today - web.empty).days >= 21:
            garden.unmake(thing.bed, WEB, "the empty web came down in the wind")
        elif _down(garden, web, beds):              # a plant it hung from went down (a fern's fronds, to the frost)
            garden.unmake(thing.bed, WEB, "the empty web came down with a plant it hung from")
        else:                                       # it hangs on, and the day's wind and dew are on it still
            web.wind = round(_wind_in(sky, bed), 1)
            dew = _dew(sky, bed)
            web.dew, web.rime = (today if dew else None), dew == "rime"
            garden.make(thing.bed, WEB, web_text(web))
    standing = [each for each in garden.things() if each.maker == NAME and each.name == WEB]
    st.web = standing[0].where if standing else ""
    if st.status == "in" and not standing:
        st.status = "without"
    ctx.save(st.text())
    return lines


# ------------------------------------------------------------ at the gate

def present(garden, ctx):
    """While her web stands: dew on it in the morning, the wind in it, or herself at the hub in the dark.
    After her season, an empty web with the morning's dew or rime on it."""
    st = State(ctx.state)
    thing = next((each for each in garden.things() if each.maker == NAME and each.name == WEB), None)
    if thing is None:
        return None
    web = read_web(thing.text, thing.bed)
    hour = ctx.hour if isinstance(ctx.hour, int) else 12
    dark = _dark(ctx.sky, hour)
    wet = web.dew == ctx.date and not dark and hour <= 10
    wet_words = "white with rime" if web.rime else "beaded with dew"
    if web.empty and not web.torn:
        return "An empty web in the %s is %s" % (thing.bed, wet_words) if wet else None
    if st.status != "in" or web.torn or web.empty:
        return None
    if wet:
        return "The web between %s and %s in the %s is %s" % (web.a, web.b, thing.bed, wet_words)
    if dark:
        return "The spider waits at the hub of her web in the %s" % thing.bed
    if web.wind >= 3:
        return "A spider's web between %s and %s in the %s bellies in the wind" % (web.a, web.b, thing.bed)
    return "A spider's web hangs between %s and %s in the %s" % (web.a, web.b, thing.bed)


# ------------------------------------------------------------ the drawings

SILK, SPIRAL, PLANT = "#3d3d3d", "#77716a", "#8a8070"
DEW_INK, SAC_INK = "#5f9fd0", "#b8954a"
CAUGHT_INKS = {"bee": "#d9a400", "moth": "brown", "hoverfly": "orange"}


def draw(text, ctx, pen):
    """Her web face on, or her egg sac, as the text says it."""
    head = str(text or "").lstrip().lower()
    if head.startswith("an egg sac") or (_LAID.search(str(text or "")) and "spokes" not in head):
        _draw_sac(read_sac(text), ctx, pen)
    else:
        _draw_web(read_web(text), ctx, pen)


def _ray(frame, cx, cy, angle) -> float:
    """How far from the hub, along `angle`, the frame lies."""
    dx, dy = math.cos(angle), math.sin(angle)
    best = None
    for i, (x1, y1) in enumerate(frame):
        x2, y2 = frame[(i + 1) % len(frame)]
        ex, ey = x2 - x1, y2 - y1
        den = dx * ey - dy * ex
        if abs(den) < 1e-12:
            continue
        t = ((x1 - cx) * ey - (y1 - cy) * ex) / den
        s = ((x1 - cx) * dy - (y1 - cy) * dx) / den
        if t > 0 and -1e-9 <= s <= 1 + 1e-9:
            best = t if best is None else min(best, t)
    return best if best else 1.0


def _draw_web(web, ctx, pen):
    pen.unit_name = "cm"
    pen.ground(0)
    hour = ctx.hour if isinstance(getattr(ctx, "hour", None), int) else None
    today = getattr(ctx, "date", None)
    width = float(web.across)
    tall, cx, cy, radius = _frame(width)
    seed = "%s|%s|%s" % (web.a, web.b, web.spun)
    shape = ((-0.92, 0.80), (0.94, 0.74), (1.02, -0.30), (0.12, -1.06), (-1.00, -0.42))
    frame = []
    for k, (fx, fy) in enumerate(shape):
        jx = (_crc(seed, k, "x") % 120) / 1000.0 - 0.06
        jy = (_crc(seed, k, "y") % 120) / 1000.0 - 0.06
        frame.append((cx + (fx + jx) * radius, cy + (fy + jy) * radius))
    silk = "dead" if web.empty else SILK
    sticky = "dead" if web.empty else SPIRAL
    ties = [(0.0, frame[0][1] + 0.12 * radius), (width, frame[1][1] + 0.12 * radius),
            (width, frame[2][1] - 0.05 * radius), (cx + 0.25 * radius, 0.0), (0.0, frame[4][1] - 0.08 * radius)]
    tops = {}
    for x, height in ((0.0, web.heights[0]), (width, web.heights[1])):    # the two plants, standing on the ground:
        tied = max(y for tx, y in ties if tx == x)                       # as tall as they are, if the web knows it;
        tops[x] = height if height is not None else tied + 3.0           # else a little above the highest thread
        pen.line(x, 0, x, tops[x], 7, PLANT)
    below = -0.045 * max(list(tops.values()) + [y for _, y in frame])     # the names just under the ground, at any size
    pen.label(0, below, web.a or "?", 16, "ink", "middle")
    pen.label(width, below, web.b or "?", 16, "ink", "middle")
    anchors = [((x, min(y, tops.get(x, y))), frame[k]) for k, (x, y) in enumerate(ties)]   # none above its plant
    try:
        dark = hour is not None and _dark(ctx.sky, hour)
    except Exception:
        dark = False
    if web.torn:
        _draw_torn(pen, frame, anchors, radius, silk)
    else:
        _draw_orb(pen, web, frame, anchors, cx, cy, radius, silk, sticky, seed, hour, today, dark)
    _web_notes(pen, web, hour, today)


def _draw_torn(pen, frame, anchors, radius, silk):
    """What is left after the wind: the anchor threads, and a few threads hanging from where the frame was."""
    for (x0, y0), (x1, y1) in anchors:
        pen.line(x0, y0, x1, y1, 3, silk)
    hangs = ((0, 0.10, -0.70), (1, -0.15, -0.55), (2, -0.20, -0.45), (4, 0.15, -0.35), (3, -0.10, 0.30))
    for k, dx, dy in hangs:
        x, y = frame[k]
        pen.polyline([(x, y), (x + dx * radius * 0.5, y + dy * radius * 0.6), (x + dx * radius, y + dy * radius)], 2, silk)
    for k in (0, 1):                                # spokes broken off near the top corners
        x, y = frame[k]
        pen.polyline([(x, y), (x + (0.3 if k == 0 else -0.3) * radius, y - 0.25 * radius),
                      (x + (0.32 if k == 0 else -0.34) * radius, y - 0.55 * radius)], 2, silk)


def _draw_orb(pen, web, frame, anchors, cx, cy, radius, silk, sticky, seed, hour, today, dark=False):
    spokes, turns = max(5, web.spokes), max(3, web.turns)
    bow = min(0.34, web.wind * 0.055) * radius     # the day's wind bows the web to one side
    bx, by = bow, -0.25 * bow

    def bent(x, y, f):
        """A point of the orb, moved by the wind: the hub most, the frame (tied to the plants) not at all."""
        lift = max(0.0, 1.0 - f * f)
        return x + bx * lift, y + by * lift

    for (x0, y0), (x1, y1) in anchors:
        pen.line(x0, y0, x1, y1, 3, silk)
    for i, (x1, y1) in enumerate(frame):           # the frame, each thread bowed by the wind
        x2, y2 = frame[(i + 1) % len(frame)]
        points = []
        for s in range(9):
            t = s / 8.0
            lift = 4.0 * t * (1.0 - t) * 0.35
            points.append((x1 + (x2 - x1) * t + bx * lift, y1 + (y2 - y1) * t + by * lift))
        pen.polyline(points, 3, silk)
    turn = (_crc(seed, "turn") % 360) * math.pi / 180.0
    angles = [turn + 2.0 * math.pi * k / spokes for k in range(spokes)]
    reach = [_ray(frame, cx, cy, angle) for angle in angles]
    hub = bent(cx, cy, 0.0)
    for angle, far in zip(angles, reach):           # the spokes, from the hub to the frame
        pen.polyline([bent(cx + f * far * math.cos(angle), cy + f * far * math.sin(angle), f)
                      for f in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)], 2, silk)
    for f in (0.035, 0.06, 0.09):                   # the hub's few rings
        pen.polyline([bent(cx + f * far * math.cos(angle), cy + f * far * math.sin(angle), f)
                      for angle, far in zip(angles, reach)], 2, silk, True)
    inner, outer = 0.17, 0.93
    steps = turns * spokes
    spiral = []
    for j in range(steps + 1):                      # the sticky spiral, a straight run between each two spokes
        k = j % spokes
        f = inner + (outer - inner) * j / steps
        spiral.append(bent(cx + f * reach[k] * math.cos(angles[k]), cy + f * reach[k] * math.sin(angles[k]), f))
    pen.polyline(spiral, 2, sticky)
    if web.dew and web.dew == today and (hour is None or hour <= 10):
        step = max(1, len(spiral) // 380)
        for j in range(0, len(spiral) - 1, step):   # beads hang on the threads between the spokes, not where they cross,
            if _crc(seed, j, "bead") % 5 == 0:      # each where it happened to gather, and some threads bare
                continue
            along = 0.15 + 0.7 * (_crc(seed, j, "along") % 1000) / 1000.0
            (x1, y1), (x2, y2) = spiral[j], spiral[j + 1]
            pen.dot(x1 + (x2 - x1) * along, y1 + (y2 - y1) * along, 3.4, "white" if web.rime else DEW_INK)
    for when, what, how in web.caught[-CAUGHT_KEPT:]:
        at = int(len(spiral) * (0.2 + 0.75 * ((_crc(when, what, how) % 1000) / 1000.0)))
        x, y = spiral[min(len(spiral) - 1, at)]
        ink = "dead" if web.empty else CAUGHT_INKS.get(what.split()[-1] if what.split() else "", "ink")
        pen.dot(x, y, 6, ink)
        pen.dot(x, y, 9, "grey", False, 2)
    if not web.empty:
        if hour is not None and hour >= 10 and not dark:   # through the day she waits in her retreat, at the top corner
            x, y = frame[0][0] + 0.06 * radius, frame[0][1] - 0.05 * radius
        else:
            x, y = hub
        _draw_her(pen, x, y)


def _draw_her(pen, x, y):
    """Her, head down: the abdomen above with the pale cross garden spiders carry, the head below, four legs a side."""
    for angle in (15, 45, 135, 165, 195, 228, 312, 345):
        rad = math.radians(angle)
        bend = 0.5 if angle < 180 else -0.5            # the legs bow a little, as hers do
        knee = (x + 1.1 * math.cos(rad), y - 0.35 + 1.1 * math.sin(rad) + bend * 0.35)
        pen.polyline([(x, y - 0.35), knee, (x + 2.1 * math.cos(rad), y - 0.35 + 2.1 * math.sin(rad))], 3, "brown")
    pen.dot(x, y + 0.55, 12, "brown")
    pen.dot(x, y - 0.4, 7, "brown")
    pen.line(x, y + 0.25, x, y + 0.9, 2, "white")
    pen.line(x - 0.25, y + 0.62, x + 0.25, y + 0.62, 2, "white")


def _many(word, n) -> str:
    """'1 bee', '2 bees', '3 hoverflies'."""
    if n == 1:
        return "1 %s" % word
    if word.endswith("y") and word[-2:-1] not in ("a", "e", "o", "u"):
        return "%d %sies" % (n, word[:-1])
    return "%d %s%s" % (n, word, "es" if word.endswith(("s", "sh", "ch", "x")) else "s")


def _web_notes(pen, web, hour, today):
    """Three lines under the drawing: what web this is, what it caught, and the morning's dew and the day's wind."""
    built = "%d spokes, %d turns of the spiral · spun %s, her %s web this season" % (
        web.spokes, web.turns, _said(web.spun) or "on a day not written", _nth(web.nth))
    if web.torn:
        pen.note("torn %s on %s" % (web.torn_by or "by the wind", _said(web.torn)))
        pen.note("she is gone, and her season with her (since %s)" % _said(web.empty) if web.empty
                 else "she will spin again on a still night")
        pen.note(built)
        return
    tally = {}
    for _, what, _ in web.caught[-CAUGHT_KEPT:]:
        word = what.split()[-1] if what.split() else "something"
        tally[word] = tally.get(word, 0) + 1
    if tally:
        colours = {"bee": "yellow", "moth": "brown", "hoverfly": "orange"}
        caught = "caught since it was spun: " + ", ".join(
            "%s (%s)" % (_many(word, n), colours.get(word, "black")) for word, n in sorted(tally.items()))
    else:
        caught = "nothing caught since it was spun"
    if web.dew and web.dew == today:
        wet = ("white with rime at dawn" if web.rime else "beaded with dew at dawn") + (
            ", dried by now" if hour is not None and hour > 10 else "")
    else:
        wet = "no dew this morning"
    if web.empty:
        pen.note("empty since %s: she is gone, and her season with her" % _said(web.empty))
        pen.note(built)
        pen.note("wind %.1f in the bed: %s · %s%s" % (
            web.wind, _bellies(web.wind), wet,
            " · it holds %s, grey now" % ", ".join(_many(word, n) for word, n in sorted(tally.items())) if tally else ""))
        return
    pen.note(built)
    pen.note(caught)
    pen.note("wind %.1f in the bed: %s · %s" % (web.wind, _bellies(web.wind), wet))


def _draw_sac(sac, ctx, pen):
    pen.unit_name = "mm"
    pen.ground(0)
    cx, cy, r = 8.0, 28.0, 8.0
    if sac.on:
        pen.line(0, 0, 0, 60, 7, PLANT)
        pen.label(0, -6, sac.on, 16, "ink", "middle")
        for dy in (-5.0, 0.0, 5.0):
            pen.line(0, cy + dy, cx - r * 0.9, cy + dy * 0.7, 2, SAC_INK)
    else:
        cy = r + 1.0
    opened = sac.gone is not None
    for k in range(26):                             # the tuft of silk: strands wound round and round, each its own way
        ring = 2.5 + (_crc(sac.laid, k, "r") % 60) / 10.0
        sweep = 90 + _crc(sac.laid, k, "s") % 160
        ox = ((_crc(sac.laid, k, "ox") % 40) / 10.0 - 2.0) * (1.0 - ring / 10.0)
        oy = ((_crc(sac.laid, k, "oy") % 40) / 10.0 - 2.0) * (1.0 - ring / 10.0)
        if opened:                                  # torn open at the top: every arc keeps clear of 60..120 degrees
            start = 120 + _crc(sac.laid, k, "a") % max(1, 300 - sweep)
        else:
            start = _crc(sac.laid, k, "a") % 360
        pen.arc(cx + ox, cy + oy, ring, start, start + sweep, 2 if k % 3 else 3, SAC_INK)
    for k in range(6):                              # loose threads, to the stem and the air (never into the ground)
        angle = math.radians(_crc(sac.laid, k, "loose") % (360 if sac.on else 160) + (0 if sac.on else 10))
        far = r + 2.0 + (_crc(sac.laid, k, "len") % 40) / 10.0
        pen.line(cx + r * 0.8 * math.cos(angle), cy + r * 0.8 * math.sin(angle),
                 cx + far * math.cos(angle), cy + far * math.sin(angle), 2, SAC_INK)
    if sac.hatched and not opened:                  # the gold ball of spiderlings
        for k in range(30):
            angle = math.radians(_crc(sac.laid, k, "ball") % 360)
            far = (_crc(sac.laid, k, "far") % 100) / 100.0 * (r + 3.0)
            pen.dot(cx + far * math.cos(angle), cy + far * math.sin(angle), 3, "yellow")
    if opened:                                      # the threads they went out on, drifting off on the air
        for k in range(5):
            far_x = 12.0 + (_crc(sac.gone, k, "x") % 22)
            far_y = 16.0 + (_crc(sac.gone, k, "y") % 18)
            pen.polyline([(cx, cy + r * 0.8), (cx + far_x * 0.2, cy + r + far_y * 0.45),
                          (cx + far_x * 0.6, cy + r + far_y * 0.8), (cx + far_x, cy + r + far_y)], 2, "grey")
    pen.note("laid %s%s" % (_said(sac.laid) or "on a day not written",
                            ", on a stem of %s" % sac.on if sac.on else ", in the shelter of the bed"))
    if opened:
        pen.note("hatched %s; they went out on the wind on %s: gossamer" % (_said(sac.hatched) or "unseen", _said(sac.gone)))
    elif sac.hatched:
        pen.note("hatched %s: a ball of spiderlings, gold, waiting for a light wind" % _said(sac.hatched))
    else:
        pen.note("about %d eggs, through the winter" % sac.eggs)
