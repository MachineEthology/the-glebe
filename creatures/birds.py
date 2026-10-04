"""
Birds: they carry seed far across the garden, and each spring a pair builds a nest.

Their own file, ground/creatures/birds, says how many birds are about the
garden (sparrows, finches, a blackbird or two; the garden does not tell them
apart) and where this year's nest is:

    birds: 30
    nest: north-wall/nest

Any line may be changed by hand. A number that cannot be read is taken
afresh, and the nest is found again by looking in the beds.

What they do in the days:

  Seed. Of the seed the plants drop each day the birds take a share: more
  when they are many, most in autumn and winter when there is little else
  to eat, least in summer when there are insects. Of what they take, about
  two parts in three are carried far across the garden and dropped where
  they perch, mostly in a sheltered bed some way off, never in the keeper's
  border by the gate. The rest is eaten. A seedling from a seed they carried
  says so on its tag (`carried: by birds`) and in its first ring. A spore
  (what a fern or a moss lets go, its seed saying `start: spore`) is dust
  on the wind, not a seed: they neither carry it nor eat it.

  The nest. From the middle of March, on a mild dry day, a pair begins a
  nest in a sheltered bed (never the keeper's), by the biggest plant there
  if there is one. On dry, still days they bring a few strands, and in
  ten days or so it is done. What lies about in this garden to build with is
  the heap: each strand is a strip torn from a line of the humus
  (compost/humus) or of something lying on the heap, torn wherever the beak
  took hold, and laid in by birds who cannot read a word of it. When the
  heap has nothing to give (a young garden's heap has rotted nothing yet),
  they tear their strands from the dead plants still standing in the beds,
  whose bodies are lines that grew; and when there are none of those
  either, they use dry grass. The nest's second line says what it was
  woven of. (A strand is a strip of the words, not the words themselves:
  the heap and the dead plants lose nothing by it.) Then come the eggs,
  one a day; then about a fortnight's sitting; then the young, who fly
  about a fortnight later. A frost while there are eggs may chill one. The empty
  nest stays where it was until the next spring, when the pair pulls it
  apart and some of its strands go into the new one.

  How many. Through the summer the garden's birds raise young, more when
  they are few; the young of the nest are added when they fly. Frost nights
  thin them a little, snow more. There are never fewer than 6 nor more
  than 90.

The nest is a file, beds/<bed>/nest. Its head says when it was begun and
finished, the eggs and the young. Below, one strand to a line, the outside
first, each with the place it was torn from:

    strands, the outside first:
        e heap rotted dow          · compost/humus
        of a letter left o         · compost/a-letter.md
        rain sail* soil            · long-border/rain-ladder

The drawing (python shed/look.py beds/<bed>/nest) is the nest seen from
above. Each strand is a stroke wound part of the way round the cup and
woven a little in or out, as long as its words: the first strands on the
outside, the last ones lining the cup. Strands from the humus are brown,
those from things still lying on the heap are grey, those from dead plants
are rust, and dry grass is straw. Pale blue dots in the cup are its eggs
(an egg the frost chilled is a hollow grey ring); grey dots are the young.
When they have flown the cup is empty.

The almanac hears of them seldom: when a nest is begun; when the young fly,
or when a nest is given up; and when a hard winter has left few birds.
"""

import datetime
import math
import re
import zlib

import hands

NAME = "birds"
FEWEST, MOST = 6, 90
SETTLED = 60             # what the garden holds in a good year: the summer's young are fewer the nearer they come to it
FEW = 12                 # below this the almanac says a hard winter has left few birds
NEST = "nest"
KEEPERS_BED = "gate-border"
STRANDS_FEW = 30         # a nest is not finished with fewer strands than this
STRANDS_MOST = 48        # nor built on past this many
REUSED = 0.33            # of last year's strands, the share that goes into the new nest
SIT_DAYS = 13            # from the last egg to the young
FLY_DAYS = 14            # from the young to their flying
GRASS = "dry grass"
MONTHS = ("January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December")

_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_HEAD = re.compile(r"^\s*(begun|finished|eggs|chilled|hatched|flown|given up)\s*:\s*(.*)$", re.IGNORECASE)


# ------------------------------------------------------------ small things

def _date(text):
    """The first date written in a piece of text, or None."""
    found = _DATE.search(str(text or ""))
    if not found:
        return None
    try:
        return datetime.date.fromisoformat(found.group())
    except ValueError:
        return None


def _spore(seed) -> bool:
    """Is it a spore, dust on the wind? Its text says so: `start: spore` (as the days write on a fern's or a moss's)."""
    try:
        return hands.word(hands.read_keys(str(seed)), "start", "") in ("spore", "spores")
    except Exception:
        return False


def _first_number(text, default=0) -> int:
    found = re.search(r"\d{1,4}", str(text or ""))
    return int(found.group()) if found else default


def _some(rng, x) -> int:
    """x as a whole number, the part after the point by the dice: 2.3 is 2 seven times in ten, 3 the other three."""
    x = max(0.0, float(x))
    whole = int(x)
    return whole + (1 if rng.random() < x - whole else 0)


def _said(day) -> str:
    """A day as the notes say it: 3 April."""
    return "%d %s" % (day.day, MONTHS[day.month - 1]) if day else ""


def _crc(*parts) -> int:
    """A number that is always the same for the same words (Python's own hash() changes from run to run)."""
    return zlib.crc32("|".join(str(part) for part in parts).encode("utf-8", errors="replace"))


# ------------------------------------------------------------ their own file

def _count(keys) -> int:
    return int(hands.num(keys, "birds", 30, FEWEST, MOST))


def _own_file(n, nest_where) -> str:
    return ("# The birds of the garden: how many are about, and where this year's nest is.\n"
            "# Any line may be changed by hand; what cannot be read is taken afresh.\n"
            "birds: %d\n"
            "nest: %s\n" % (n, nest_where or "none"))


# ------------------------------------------------------------ the nest, as text

class Nest:
    """A nest as its file says it: the title, the dates of its life, and its strands, the outside first."""

    def __init__(self):
        self.title = ""
        self.begun = self.finished = self.first_egg = self.last_egg = None
        self.hatched = self.flown = self.given_up = self.chilled_on = None
        self.eggs = self.chilled = self.young = 0
        self.strands = []                     # [(the strand's words, where it was torn from)]

    @property
    def done(self) -> bool:
        """Its year is over: the young have flown, or it was given up."""
        return bool(self.flown or self.given_up)


def read_nest(text) -> Nest:
    """A nest's file, read as well as it can be. Never raises: a line that cannot be read is passed over."""
    nest = Nest()
    for raw in str(text or "").splitlines():
        if not raw.strip() or raw.startswith("#"):    # a remark; an indented # is a strand torn from a heading
            continue
        head = _HEAD.match(raw)
        if head and not raw[:1].isspace():
            key, value = head.group(1).lower(), head.group(2)
            if key == "begun":
                nest.begun = _date(value)
            elif key == "finished":
                nest.finished = _date(value)
            elif key == "eggs":
                nest.eggs = min(12, _first_number(value))
                found = re.search(r"the first (\d{4}-\d{2}-\d{2})", value)
                nest.first_egg = _date(found.group(1)) if found else _date(value)
                found = re.search(r"the last (\d{4}-\d{2}-\d{2})", value)
                nest.last_egg = _date(found.group(1)) if found else None
            elif key == "chilled":
                nest.chilled, nest.chilled_on = min(12, _first_number(value)), _date(value)
            elif key == "hatched":
                nest.hatched = _date(value)
                found = re.search(r"(\d{1,2})\s+young", value)
                nest.young = int(found.group(1)) if found else 0
            elif key == "flown":
                nest.flown = _date(value)
            elif key == "given up":
                nest.given_up = _date(value)
            continue
        if raw[:1].isspace():                 # a strand: an indented line
            words, _, source = raw.strip().rpartition(" · ")
            if not words:
                words, source = raw.strip(), ""
            words = words.strip()
            if words and len(nest.strands) < STRANDS_MOST + 40:
                nest.strands.append((words[:80], source.strip()[:120]))
            continue
        if not nest.title and raw.strip().lower().startswith("a nest"):
            nest.title = raw.strip()[:160]
    return nest


def _woven_of(strands) -> str:
    """The nest's second line: what it was woven of, as its strands say."""
    sources = {_ink(source) for _, source in strands}
    if sources & {HUMUS_INK, HEAP_INK}:
        return "woven by the birds of what lay on the heap%s; they cannot read a word of it" % (
            ", and of dead plants" if STEM_INK in sources else "")
    if STEM_INK in sources:
        return "woven by the birds of dead plants%s, for the heap had nothing to give; they cannot read a word of it" % (
            " and dry grass" if GRASS_INK in sources else "")
    return "woven of dry grass: the heap had nothing to give yet, nor any dead plant"


def nest_text(nest, bed) -> str:
    """A nest as its file: the title, what it was woven of, what has happened to it, and its strands."""
    lines = [nest.title or "a nest in the %s" % bed, _woven_of(nest.strands), ""]
    if nest.begun:
        lines.append("begun: %s" % nest.begun.isoformat())
    if nest.finished:
        lines.append("finished: %s" % nest.finished.isoformat())
    if nest.eggs:
        egg = "eggs: %d" % nest.eggs
        if nest.first_egg:
            egg += " · the first %s" % nest.first_egg.isoformat()
        if nest.last_egg:
            egg += " · the last %s" % nest.last_egg.isoformat()
        lines.append(egg)
    if nest.chilled:
        when = nest.chilled_on or nest.last_egg or nest.begun
        lines.append("chilled: %d%s" % (nest.chilled, " · in the frost of %s" % when.isoformat() if when else ""))
    if nest.hatched:
        lines.append("hatched: %s · %d young" % (nest.hatched.isoformat(), nest.young))
    if nest.flown:
        lines.append("flown: %s · %d young" % (nest.flown.isoformat(), nest.young))
    if nest.given_up:
        lines.append("given up: %s" % nest.given_up.isoformat())
    lines += ["", "strands, the outside first:"]
    for words, source in nest.strands:
        if source and source != GRASS:
            lines.append("    %-30s · %s" % (words, source))
        else:
            lines.append("    %s" % words)          # dry grass: there is nowhere to say it came from
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------ strands from the heap

def _heap_lines(ctx) -> list:
    """[(where, [lines])] for everything under compost/ the soil shows: the humus and what lies on the heap."""
    found = []
    try:
        texts = ctx.soil.texts()
    except Exception:
        texts = []
    for where, text in texts:
        if not str(where).startswith("compost/"):
            continue
        lines = [" ".join(line.split()) for line in str(text).splitlines() if line.strip()]
        lines = [line for line in lines if any(ch.isalpha() for ch in line)]
        if lines:
            found.append((str(where), lines))
    return found


def _dead_lines(garden) -> list:
    """[(bed/plant, [lines])] for the dead plants still standing in the beds: their bodies, the † line left out.

    Only what stood above the ground: a seed that died in the ground before
    it came up, or a bulb with nothing above it, gives no strand. Of a bulb,
    only the lines of what stood above the ground are taken.
    """
    found = []
    try:
        dead = sorted((plant for plant in garden.plants() if plant.dead), key=lambda plant: plant.where)
    except Exception:
        dead = []
    for plant in dead:
        lines = [" ".join(line.split()) for line in str(plant.body or "").splitlines()]
        lines = [line for line in lines if line and not line.startswith("†")]
        low = [line.lower() for line in lines]
        if not lines or low[0].startswith("a seed in the ground"):
            continue                                   # it never came up
        if "above the ground:" in low:
            lines = lines[low.index("above the ground:") + 1:]
            if not lines or lines[0].lower() == "nothing":
                continue                               # a bulb with nothing above it
        lines = [line for line in lines if not line.startswith("#") and sum(1 for ch in line if ch.isalpha()) >= 3]
        if lines:
            found.append((plant.where, lines[:400]))
    return found


def _tear(line, rng) -> str:
    """A strip torn from a line wherever the beak took hold: nine to thirty characters, not minding the words."""
    line = line.replace("·", ",")
    length = rng.randint(9, 30)
    if len(line) <= length:
        return line.strip()
    start = rng.randint(0, len(line) - length)
    return line[start:start + length].strip()


def _gather(garden, ctx, rng, k) -> list:
    """k strands for the nest: torn from the heap and the humus; when the heap has nothing to give, from the dead
    plants standing in the beds; when there are none, dry grass."""
    sources = _heap_lines(ctx) or _dead_lines(garden)
    strands = []
    for _ in range(k):
        if not sources:
            strands.append((GRASS, GRASS))
            continue
        weights = [math.sqrt(len(lines)) for _, lines in sources]
        where, lines = rng.choices(sources, weights)[0]
        for _ in range(4):
            piece = _tear(lines[rng.randrange(len(lines))], rng)
            if sum(1 for ch in piece if ch.isalpha()) >= 3:
                strands.append((piece, where))
                break
    return strands


# ------------------------------------------------------------ the beds

def _centre(bed):
    at = bed.at
    try:
        x, y, w, h = (float(v) for v in at)
        return x + w / 2.0, y + h / 2.0
    except (TypeError, ValueError):
        return None


def _far_bed(beds, from_bed, rng):
    """Where a carried seed is dropped: a bed some way off, the farther and the more sheltered the likelier."""
    here = next((bed for bed in beds if bed.name == from_bed), None)
    centre = _centre(here) if here is not None else None
    choices, weights = [], []
    for bed in beds:
        if bed.name in (from_bed, KEEPERS_BED):
            continue
        there = _centre(bed)
        far = math.hypot(there[0] - centre[0], there[1] - centre[1]) if centre and there else 300.0
        choices.append(bed.name)
        weights.append((max(40.0, far) / 100.0) ** 1.5 * (0.4 + max(0.0, min(1.0, bed.shelter))))
    return rng.choices(choices, weights)[0] if choices else None


def _nest_bed(garden, rng, refused=()):
    """A sheltered bed for the nest, never the keeper's: the more sheltered, the likelier."""
    beds = [bed for bed in garden.beds() if bed.name != KEEPERS_BED and bed.name not in refused]
    sheltered = [bed for bed in beds if bed.shelter >= 0.5] or sorted(beds, key=lambda bed: -bed.shelter)[:1]
    if not sheltered:
        return None
    return rng.choices(sheltered, [max(0.05, bed.shelter) ** 2 for bed in sheltered])[0]


def _nest_title(garden, bed) -> str:
    """'a nest in the north-wall, by the quince': by the biggest plant there (the most cover), if there is one.

    Only 'by': the garden's kinds are many, and a nest cannot be in a lichen.
    """
    growing = [plant for plant in garden.plants(bed=bed.name) if not plant.dead]
    if not growing:
        return "a nest in the %s" % bed.name
    biggest = max(sorted(growing, key=lambda plant: plant.name), key=lambda plant: len(plant.body))
    return "a nest in the %s, by the %s" % (bed.name, biggest.name)


# ------------------------------------------------------------ the days

def _my_nest(garden, keys):
    """The nest the birds made, as a thing that lies in a bed: the one their file names if it is there."""
    mine = [thing for thing in garden.things() if thing.maker == NAME and thing.name == NEST]
    said = hands.line(keys, "nest", "")
    for thing in mine:
        if thing.where == said:
            return thing
    return mine[0] if mine else None


def _begin(garden, ctx, old, lines):
    """A pair begins a nest: last year's comes apart and a third of its strands go in first. Returns (thing place, Nest)."""
    rng = ctx.rng
    reused = []
    if old is not None:
        before = read_nest(old.text).strands
        reused = [strand for strand in before if rng.random() < REUSED]
        garden.unmake(old.bed, old.name, "pulled apart for a new nest")
    refused = []
    for _ in range(3):
        bed = _nest_bed(garden, rng, refused)
        if bed is None:
            return None, None
        nest = Nest()
        nest.title = _nest_title(garden, bed)
        nest.begun = ctx.date
        nest.strands = reused + _gather(garden, ctx, rng, rng.randint(2, 5))
        if garden.make(bed.name, NEST, nest_text(nest, bed.name)):
            lines.append("birds: a pair began a nest in the %s" % bed.name
                         + (", with strands of last year's in it" if reused else ""))
            return "%s/%s" % (bed.name, NEST), nest
        refused.append(bed.name)                   # a hand's file of that name lies there: another bed
    return None, None


def _tend(garden, nest, ctx, n, lines, bed):
    """One day in the life of a nest of this year. Returns the birds' number, with the young once they fly."""
    day, sky, rng = ctx.date, ctx.sky, ctx.rng
    if nest.done:
        return n
    if not nest.finished:
        if sky.rain < 2 and sky.wind < 6 and sky.tmean >= 5:
            nest.strands += _gather(garden, ctx, rng, rng.randint(2, 5))
            if len(nest.strands) >= STRANDS_MOST or (len(nest.strands) >= STRANDS_FEW and rng.random() < 0.3):
                nest.finished = day
        return n
    if not nest.last_egg:
        if day > nest.finished:
            nest.eggs += 1
            nest.first_egg = nest.first_egg or day
            if nest.eggs >= 6 or (nest.eggs >= 3 and rng.random() < 0.35):
                nest.last_egg = day
        return n
    if not nest.hatched:
        warm = nest.eggs - nest.chilled
        if sky.tmin < -1 and warm > 0 and rng.random() < 0.5:
            nest.chilled += 1
            nest.chilled_on = day
            warm -= 1
        if (day - nest.last_egg).days >= SIT_DAYS:
            if warm <= 0:
                nest.given_up = day
                lines.append("birds: the nest in the %s was given up; no egg hatched" % bed)
            else:
                nest.hatched, nest.young = day, warm
        return n
    if (day - nest.hatched).days >= FLY_DAYS:
        nest.flown = day
        lines.append("birds: the young left the nest in the %s" % bed)
        return n + nest.young
    return n


def _season(n, ctx) -> int:
    """How many there are after the day: the summer's young, the winter's losses, a crowd thinning itself."""
    sky, rng, month = ctx.sky, ctx.rng, ctx.date.month
    if month in (5, 6, 7):
        n += _some(rng, n * 0.007 * max(0.0, 1.0 - n / SETTLED))
    if sky.tmin < 0:
        n -= _some(rng, n * 0.008)
    if sky.snow:
        n -= _some(rng, n * 0.025)
    if n > 75:
        n -= _some(rng, n * 0.01)
    return min(MOST, max(FEWEST, n))


def day(garden, ctx):
    keys = hands.read_keys(ctx.state)
    n = before = _count(keys)
    lines = []
    old = _my_nest(garden, keys)
    where = old.where if old is not None else ""
    nest = read_nest(old.text) if old is not None else None
    today = ctx.date
    this_year = nest is not None and nest.begun is not None and nest.begun.year == today.year
    may_begin = (today.month == 3 and today.day >= 15) or today.month in (4, 5)
    if may_begin and (not this_year or (nest.given_up and today.month < 6)):
        sky = ctx.sky
        if sky.tmean >= 7 and sky.rain < 2 and sky.wind < 6 and ctx.rng.random() < 0.15:
            where, nest = _begin(garden, ctx, old, lines)
            this_year = nest is not None
    elif this_year and old is not None:
        bed = old.bed
        n = _tend(garden, nest, ctx, n, lines, bed)
        text = nest_text(nest, bed)
        if text != old.text:
            garden.make(bed, NEST, text)
    n = _season(n, ctx)
    if n < FEW <= before:
        lines.append("birds: a hard winter has left few birds in the garden")
    ctx.save(_own_file(n, where))
    return lines


def after(garden, ctx, seeds):
    """Of the seed that fell today, the birds' share: most carried far and dropped where they perch, the rest eaten.
    Spores are passed by."""
    seeds = [seed for seed in (seeds or []) if not _spore(seed)]
    if not seeds:
        return []
    rng, sky = ctx.rng, ctx.sky
    n = _count(hands.read_keys(ctx.state))
    hunger = {"winter": 1.5, "autumn": 1.3, "spring": 0.9, "summer": 0.6}.get(sky.season, 1.0)
    share = min(0.4, n / 220.0 * hunger)
    beds = garden.beds()
    for seed in list(seeds):
        if rng.random() >= share:
            continue
        if rng.random() < 0.65:
            bed = _far_bed(beds, getattr(seed, "bed", ""), rng)
            if bed:
                garden.carry(seed, bed, "dropped far from where it fell")
        else:
            garden.drop(seed, "eaten by a bird")
    return []


# ------------------------------------------------------------ the drawing

HUMUS_INK, HEAP_INK, GRASS_INK, STEM_INK = "brown", "grey", "#b8a25a", "#b4502a"
EGG_INK, YOUNG_INK = "#a9cfd8", "#8c7b6b"


def _ink(source) -> str:
    """A strand's ink, by where it was torn from: the humus, the heap, a dead plant (bed/plant), or dry grass."""
    source = str(source or "").strip().strip("/")
    if not source or source == GRASS:
        return GRASS_INK
    if source.endswith("humus"):
        return HUMUS_INK
    if source.count("/") == 1 and not source.startswith("compost"):
        return STEM_INK
    return HEAP_INK


def draw(text, ctx, pen):
    """The nest from above: each strand a stroke round the cup, as long as its words, the outside first; then the cup."""
    nest = read_nest(text)
    pen.unit_name = "cm"
    pen.align = "center"
    strands = nest.strands
    count = len(strands)
    if not count:
        pen.note("no strands are left in the nest's text")
        return
    outer = 6.0 + min(1.5, count * 0.03)
    cup = 3.2
    for i, (words, source) in enumerate(strands):
        t = i / max(count - 1, STRANDS_FEW + 5)  # 0 for the first strand laid (outside), 1 for the lining: a nest
                                                 # still being built has its outer wall, and the cup is not lined yet
        r = outer - (outer - cup - 0.4) * t ** 0.85 + ((_crc(words, i, "r") % 60) / 100.0 - 0.3)
        length = max(3.0, min(14.0, len(words) * 0.45))
        sweep = min(280.0, math.degrees(length / max(1.0, r)))
        start = _crc(words, i) % 360
        way = 1 if _crc(words, i, "way") % 2 else -1
        drift = ((_crc(words, i, "drift") % 120) / 100.0 - 0.6)     # a strand is woven in and out, not laid round
        points = []
        for s in range(25):
            angle = math.radians(start + way * sweep * s / 24.0)
            here = max(cup - 0.2, r + drift * (s / 24.0 - 0.5) * 2.0)
            points.append((here * math.cos(angle), here * math.sin(angle)))
        pen.polyline(points, 5 if t < 0.55 else 4, _ink(source))
    warm = max(0, nest.eggs - nest.chilled)
    marks = []
    if nest.flown or nest.given_up:
        pass
    elif nest.hatched:
        marks = [(YOUNG_INK, True)] * max(0, nest.young)
    elif nest.eggs:
        marks = [(EGG_INK, True)] * warm + [("dead", False)] * min(nest.chilled, nest.eggs)
    k = len(marks)
    for j, (ink, filled) in enumerate(marks):
        angle = math.radians(90 + 360.0 * j / max(1, k))
        x, y = (0.0, 0.0) if k == 1 else (1.2 * math.cos(angle), 1.2 * math.sin(angle))
        if filled:
            pen.dot(x, y, 12 if ink == EGG_INK else 10, ink)
            pen.dot(x, y, 12 if ink == EGG_INK else 10, "grey", False, 2)
        else:
            pen.dot(x, y, 12, ink, False, 3)
    if nest.finished:
        pen.note("begun %s · finished %s" % (_said(nest.begun), _said(nest.finished)))
    elif nest.begun:
        pen.note("being built since %s" % _said(nest.begun))
    inks = [_ink(source) for _, source in strands]
    present = [ink for ink in (HUMUS_INK, HEAP_INK, STEM_INK, GRASS_INK) if ink in inks]
    if len(present) < 4:
        words = {HUMUS_INK: "from the humus (brown)", HEAP_INK: "from the heap (grey)",
                 STEM_INK: "from dead plants (rust)", GRASS_INK: "of dry grass (straw)"}
    else:                                        # all four in the long words would run off the plate
        words = {HUMUS_INK: "humus (brown)", HEAP_INK: "heap (grey)", STEM_INK: "dead plants (rust)",
                 GRASS_INK: "dry grass (straw)"}
    parts = ["%d %s" % (inks.count(ink), words[ink]) for ink in present]
    pen.note("%d strands: %s" % (count, ", ".join(parts)))
    if nest.flown:
        pen.note("the young flew on %s; the cup is empty" % _said(nest.flown))
    elif nest.given_up:
        pen.note("given up on %s" % _said(nest.given_up))
    elif nest.hatched:
        pen.note("%d young, hatched %s (grey)" % (nest.young, _said(nest.hatched)))
    elif nest.eggs:
        chilled = "; %d chilled by frost (the ring)" % nest.chilled if nest.chilled else ""
        pen.note("%d egg%s (pale blue)%s%s" % (nest.eggs, "" if nest.eggs == 1 else "s",
                                                ", the last laid %s" % _said(nest.last_egg) if nest.last_egg else "",
                                                chilled))
