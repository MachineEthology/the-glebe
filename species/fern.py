"""
Fern: a plant of the shade, made of fronds that unroll.

A fern has no flowers and sets no seed. It keeps a crown at the ground, and
each spring the crown sends up croziers: fronds coiled like the scroll of a
fiddle, which unroll over some weeks from the base to the tip, and stand
through the summer. In late summer the undersides of the grown fronds carry
sori, the dots of spore, and a dry wind takes the spore. Spore that lands on
damp shaded ground comes up as a prothallus, a flat green heart a few
millimetres across, which makes a crown only if it stays damp for two
months; and where two ferns' spore has landed together, what comes up is a
cross of the two. The fronds of most ferns are killed by the first hard
frost and lie brown through the winter; the crown sleeps, and comes again.

A fern likes shade and damp. Under the north wall it does best; in the open
border its fronds are short, and a hot dry day in full sun scorches them.


A SEED says, line by line:

    kind: fern
    fronds: 7        how many fronds the crown holds at once (3..24)
    long: 60         the longest a frond grows, in cm (10..200)
    arch: 0.6        how far a grown frond bends over: 0 stands like a
                     shuttlecock, 1 lies out along the ground
    cut: twice       none, once, twice or thrice: how finely the frond is
                     divided. None is an undivided blade, like the
                     hart's-tongue; the others are drawn as pinnae, with a
                     tooth on each for twice and two for thrice
    shade: 0.4       the share of the sky's light it does best in (0..1);
                     with more light than that its fronds are shorter, and
                     a hot dry day may scorch them
    evergreen: no    no: the fronds die at the first frost;
                     yes: they stand the winter, as the hart's-tongue does,
                     and die only on a night below -8
    sori: brown      the ink of its spore dots: an ink of the plate or #rrggbb
    hardy: -20       the night, in °C, that kills the crown
    variety: <name>  (if a visitor gave it one) carried on by its own spore,
                     not by a cross
    start: spore     written by the days on every spore a fern lets go: it
                     comes up as a prothallus (see HOW IT LIVES). Without it,
                     what is planted is a crown with buds in it.

Nothing else in the seed is read. What cannot be read is taken from what is
written here.


THE BODY, for example:

    # a fern of 3 fronds, 1 of them unrolling, 1 in spore; 2 buds in the crown
    crown: 2 buds
    spore flew 2027-08-14
    fronds:
      frond 3  up 2027-04-12  54.0 cm  unrolled  in spore
      frond 4  up 2027-04-20  31.2 cm  unrolled  bitten
      frond 5  up 2027-05-02  12.0 cm  unrolling 38%
    dead fronds:
      frond 1  up 2026-05-03  48.0 cm  killed by frost 2026-10-26

  * The line beginning # is only a summary, rewritten every day.
  * crown: how many buds wait in the crown to come up as croziers.
  * asleep since <date>: the crown is dormant (the line is absent while it
    is awake).
  * spore flew <date>: the last day a dry wind took its spore.
  * Under 'fronds:', one line to a living frond, oldest first. 'frond 5' is
    its number: the fifth frond the plant ever sent up. 'up' is the day it
    came up. Its length in cm is how long it has grown so far. Then how it
    stands: 'unrolling 38%' is a crozier still uncoiling, that far along;
    'unrolled' is a grown frond. After that, what else is true of it:
    'in spore' (sori ripe on its underside), 'spent' (its spore has flown),
    'bitten' (a slug or snail took its coiled tip while it was soft, so that
    it opened sooner and came out shorter), 'cropped' (a grazer took it down).
  * Under 'dead fronds:', the fronds that died and still lie there, with how
    and when: 'killed by frost 2026-10-26', 'scorched 2027-07-20'. They fall
    away when the next year's croziers come.
  * A fern that came up from spore begins as a single line instead:
    'prothallus: 23 damp days of 60'.


HOW IT LIVES. In spring, once the days are longer than twelve hours and
mild, the crown wakes, and while it holds buds it sends them up as croziers
a few days apart, as long as the weather is warm. Each crozier unrolls by
the day's warmth (about three weeks in a fair spring; a drought holds it
coiled) and lengthens as it unrolls: the first croziers of a year grow
longest, and each later one a little less. How long a frond can grow is the
seed's 'long', less in a bed brighter than its 'shade' line, less in dry
ground, and more where the ground is rich. The year's first crozier brings
down the dead fronds of the year before, and an evergreen's old fronds with
them.

After midsummer, once its fronds have stood seven weeks, a fern's sori
ripen, all its grown fronds together, and it is in spore; on a dry day with
a breath of wind, or a warm dry day, the spore flies, which is when the
fern casts (one spore that comes to anything, or two). A fern does this once
a year. A hot, dry day in a bed brighter than the fern likes scorches
grown fronds: each may die of it. A frost kills every frond of a fern that
is not evergreen, whether its crown is awake or already asleep. The crown
sleeps from the first frost of autumn (or from the first day of winter, if
no frost came before), and as it goes to sleep it counts its year: it keeps
the buds that never came up, and gains one for each full frond it grew that
year, and one more if it grew any (two at least, and never more than its
'fronds'). A frost in spring kills what is up, and the crown sleeps until it
is mild again; then it sends up again as many croziers as the frost took, and
counts nothing. An evergreen keeps its fronds, and loses them only on a
night below -8. A night below the seed's 'hardy' line kills the crown.

Croziers are soft, and slugs and snails bite them: a bite takes part of the
coil, so that the crozier opens sooner and comes out shorter, and a very
small one is eaten whole. A grown frond is leather to them. A grazer crops
every frond down to a stub (and a stub is not cropped again).

A spore comes up as a prothallus, which has no crown and no fronds. It counts
the days the ground is damp (rain, or ground still wet from it): at sixty it
makes a crown with two buds. A dry day may wither it, the likelier the drier
its bed (at the pond's edge it never withers; in ordinary ground about half
are lost; under the dry wall or on the stones nearly all); so may too much
light, or a hard frost. Where the ferns already in its bed fill a third of
the bed's room, it is crowded out.

A cross: when a fern's spore flies and another fern of its bed, near it, is
in spore too, what it casts may be a cross: the fronds, length, arch, shade
and hardiness are midway between the two, the cut and the evergreen habit
are one parent's or the other's, the sori are the two inks blended, and no
variety is carried. (A fern has no flowers, and no creature carries its
spore: its crosses come of nearness and the wind, not of pollen carried, as
the flowering kinds' do.)


TO CUT IT. The body is soft: a line at a time.
  * Write a smaller length on a frond's line and it is that much shorter:
    it goes on as it was. Write 'unrolled' in place of 'unrolling n%' and the
    crozier is taken to have opened as it stands.
  * Delete a frond's line and it is gone. Move it under 'dead fronds:' and it
    is dead (say why, if you like; 'cut' is as good a reason as any), as it
    is wherever its line says how it died in place of how it stands. Words
    written after 'unrolled' or 'unrolling n%' are only a note.
  * Change 'crown: N buds' and that many croziers will come.
  * Delete 'asleep since' and the crown wakes at once (out of season it soon
    sleeps again); write it, with a date, and the crown sleeps (its fronds
    stay as they are).
  * An emptied body comes up again from the seed, as a crown with buds in
    it: a fern that came from spore comes up as a prothallus again only if it
    is younger than sixty days, too young to have made a crown.


THE PLATE. Nothing is drawn that is not in the body.

  * The crown is a small mound on the ground line. Under the ground, a dot
    for each bud waiting in it.
  * Each living frond rises from the crown and bends over by the seed's
    arch, the oldest leaning furthest out and the newest standing straight.
    Its rachis is one stroke, and the pinnae stand off it to one side and
    the other in turn, longest at a third of the way up; a frond cut twice
    has a tooth on each pinna, cut thrice two; a frond cut none is a blade,
    drawn by its two edges. A crozier still unrolling ends in a coil, which
    draws tighter as it opens.
  * Dots on the pinnae, in the sori's ink, each on a speck of clear paper
    (on a blade, short bars either side of the midrib): in spore.
  * A small open ring just past a frond's tip: bitten (a bitten crozier's
    coil has lost its heart, and the ring stands past it). A heavy bar
    across the tip: cropped (a cropped crozier has no coil).
  * Dead fronds lie along the ground in the pale dead ink, with their pinnae.
  * A prothallus is a small heart on the ground line, drawn in its planter's
    ink (the days', for a spore the days sowed). It is drawn larger than a
    fern is, and the bar says by how much.
  * Green is what has grown since the last visit ended: new length on a
    frond, a crozier newly up, a bud newly made. A dead fern is drawn all in
    the dead ink.
  * The bar at the bottom left says how many cm.

Standard library and hands only. Nothing here raises on a garbled body or seed.
Mended on 1 October 2026 by the builders, before the garden opened: the frost, the year's croziers and buds, the reader, a spore-born fern cut down, and the plate's marks.
"""

import datetime
import math
import re

import hands

KIND = "fern"
KEPT = ("kind", "fronds", "long", "arch", "cut", "shade", "evergreen", "sori", "hardy", "variety")
CUTS = ("none", "once", "twice", "thrice")
UNIT_PX = 20.0            # pixels per cm, at most, on a plate
PROTH_PX = 60.0           # the same for a prothallus, which is a few millimetres across
DAMP_DAYS = 60            # damp days a prothallus needs to make a crown
COIL = 3.0                # cm: the radius of a crozier's coil when it is just up
WAKE_HOURS = 12.6         # the crown wakes once the days are this long (the start of April here), and mild
SPORE_HOURS = 15.5        # fronds come into spore once the days are shorter than this (after midsummer)
SPORE_AGE = 49            # and have stood this many days
EVERGREEN_KILL = -8.0     # the night that kills an evergreen's fronds
FRONDS_MOST = 24
DEAD_KEPT = 24            # dead fronds kept lying on the body, at most

_FROND = re.compile(r"^\s*frond\s+(\d{1,5})\b(.*)$", re.I)
FROND_NUMBER_MOST = 99999  # the most _FROND reads back
_UP = re.compile(r"\bup\s+(\d{4}-\d{2}-\d{2})", re.I)
_CM = re.compile(r"(?<![\d.,])(\d+(?:[.,]\d+)?)\s*cm", re.I)    # from the start of a number only: read in one pass
_GONE = re.compile(r"\b(killed by frost|frost|scorched|cut|died|dead|fell|withered)\b")
_STANDS = re.compile(r"\bunroll(?:ed|ing)\b")
_UNROLLING = re.compile(r"\bunrolling\s*(\d{1,3})\s*%?")
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_PROTH = re.compile(r"^\s*prothallus\s*:\s*(\d{1,4})", re.I)
_ASLEEP = re.compile(r"^\s*asleep\b.*?(\d{4}-\d{2}-\d{2})?", re.I)
_FLEW = re.compile(r"^\s*spore\s+flew\s+(\d{4}-\d{2}-\d{2})", re.I)
_CROWN = re.compile(r"^\s*crown\s*:\s*(\d{1,3})", re.I)


# --------------------------------------------------------------- the seed

class Seed:
    def __init__(self, seed):
        if not isinstance(seed, dict):
            seed = hands.read_keys(seed)
        self.fronds = int(hands.num(seed, "fronds", 7, 3, FRONDS_MOST))
        self.long = hands.num(seed, "long", 60.0, 10.0, 200.0)
        self.arch = hands.num(seed, "arch", 0.6, 0.0, 1.0)
        cut = hands.word(seed, "cut", "", CUTS + ("0", "1", "2", "3", "entire", "undivided", "simple", "fine",
                                                  "pinnate", "bipinnate", "tripinnate"))
        self.cut = {"0": "none", "entire": "none", "undivided": "none", "1": "once", "simple": "once",
                    "pinnate": "once", "2": "twice", "bipinnate": "twice", "3": "thrice", "fine": "thrice",
                    "tripinnate": "thrice"}.get(cut, cut) or "twice"
        self.shade = hands.num(seed, "shade", 0.4, 0.0, 1.0)
        self.evergreen = hands.word(seed, "evergreen", "no", ("yes", "no", "oui", "non", "true", "false")) in ("yes", "oui", "true")
        self.sori = hands.line(seed, "sori", "brown") or "brown"
        self.hardy = hands.num(seed, "hardy", -20.0, -40.0, 5.0)
        self.spore = hands.word(seed, "start", "", ("spore", "spores", "crown")) in ("spore", "spores")
        self.variety = hands.line(seed, "variety", "")


# --------------------------------------------------------------- the body

class Frond:
    __slots__ = ("number", "up", "length", "unroll", "spore", "bitten", "cropped", "dead", "_side", "_lean", "_arch")

    def __init__(self, number):
        self.number = number
        self.up = None            # date it came up
        self.length = 0.0         # cm
        self.unroll = 100         # percent uncoiled; 100 is a grown frond
        self.spore = ""           # '', 'in spore' or 'spent'
        self.bitten = False
        self.cropped = False
        self.dead = ""            # '' while alive; else how and when it died
        self._side, self._lean, self._arch = 1, 0.0, 0.0     # set just before drawing

    @property
    def unrolling(self):
        return self.unroll < 100 and not self.cropped


class Fern:
    def __init__(self):
        self.read = 0             # how many lines of the body could be read
        self.buds = 0
        self.asleep = None        # a date while the crown sleeps, else None
        self.flew = None          # the last day its spore flew
        self.proth = None         # damp days counted, while it is a prothallus; else None
        self.fronds = []          # living, oldest first
        self.dead = []            # dead and still lying


def _date(text):
    try:
        return datetime.date.fromisoformat(text)
    except Exception:
        return None


def _num(text, default):
    try:
        return float(str(text).replace(",", "."))
    except Exception:
        return default


def read(body) -> Fern:
    """A body as a Fern. Reads what it can; never raises."""
    fern, under_dead, numbers = Fern(), False, set()
    for raw in str(body or "").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith(hands.DAGGER):
            continue
        low = line.lower()
        if low.startswith("fronds"):
            under_dead = False
            continue
        if low.startswith("dead fronds"):
            under_dead = True
            continue
        found = _CROWN.match(line)
        if found:
            fern.buds = min(int(found.group(1)), FRONDS_MOST)
            fern.read += 1
            continue
        found = _PROTH.match(line)
        if found:
            fern.proth = min(int(found.group(1)), DAMP_DAYS)
            fern.read += 1
            continue
        found = _FLEW.match(line)
        if found:
            fern.flew = _date(found.group(1))
            continue
        if low.startswith("asleep"):
            when = _DATE.search(line)
            fern.asleep = _date(when.group()) if when else datetime.date(2000, 1, 1)
            fern.read += 1
            continue
        found = _FROND.match(line)
        if not found:
            continue
        fern.read += 1
        number = int(found.group(1))
        if number in numbers or len(fern.fronds) + len(fern.dead) >= FRONDS_MOST + DEAD_KEPT:
            continue
        numbers.add(number)
        rest, frond = found.group(2), Frond(number)
        rest_low = rest.lower()
        up = _UP.search(rest)
        frond.up = _date(up.group(1)) if up else None
        cm = _CM.search(rest)
        frond.length = max(0.0, min(_num(cm.group(1), 0.0), 400.0)) if cm else 0.0
        unrolling = _UNROLLING.search(rest_low)
        frond.unroll = min(int(unrolling.group(1)), 99) if unrolling else 100
        frond.spore = "in spore" if "in spore" in rest_low else ("spent" if "spent" in rest_low else "")
        frond.bitten = "bitten" in rest_low
        frond.cropped = "cropped" in rest_low
        cause = ""
        gone, stands = _GONE.search(rest_low), _STANDS.search(rest_low)
        if gone and (under_dead or not (stands and stands.start() < gone.start())):     # how it died, in place of how it stands;
            tail = rest[gone.start():].strip()                                           # after 'unrolled', words are only a note
            cause = tail if gone.group(1) != "frost" or "killed" in rest_low else "killed by " + tail
        if under_dead or cause:
            frond.dead = cause or "dead"
            fern.dead.append(frond)
        else:
            fern.fronds.append(frond)
    fern.fronds.sort(key=lambda f: ((f.up or datetime.date.min), f.number))
    fern.dead.sort(key=lambda f: ((f.up or datetime.date.min), f.number))
    return fern


def _cm(x) -> str:
    return "%.1f" % x


def _frond_line(frond) -> str:
    words = ["frond %d" % frond.number]
    if frond.up:
        words.append("up %s" % frond.up.isoformat())
    words.append("%s cm" % _cm(frond.length))
    if frond.dead:
        words.append(frond.dead)
    else:
        words.append("unrolled" if frond.unroll >= 100 else "unrolling %d%%" % frond.unroll)
        if frond.spore:
            words.append(frond.spore)
        if frond.bitten:
            words.append("bitten")
        if frond.cropped:
            words.append("cropped")
    return "  " + "  ".join(words)


def _summary(fern, s) -> str:
    if fern.proth is not None:
        return "# a prothallus: the flat green heart a spore comes up as. It needs damp shade for %d days to make a crown" % DAMP_DAYS
    n = len(fern.fronds)
    unrolling = sum(1 for f in fern.fronds if f.unrolling)
    spore = sum(1 for f in fern.fronds if f.spore == "in spore")
    parts = ["a fern of %d frond%s" % (n, "" if n == 1 else "s")]
    if unrolling:
        parts.append("%d of them unrolling" % unrolling)
    if spore:
        parts.append("%d in spore" % spore)
    text = "# " + ", ".join(parts) + "; %d bud%s in the crown" % (fern.buds, "" if fern.buds == 1 else "s")
    if s.evergreen:
        text += "; evergreen"
    if fern.asleep:
        text += "; asleep"
    return text


def write(fern, s, dead_line=None) -> str:
    lines = [dead_line] if dead_line else []
    lines.append(_summary(fern, s))
    if fern.proth is not None:
        lines.append("prothallus: %d damp days of %d" % (fern.proth, DAMP_DAYS))
        return "\n".join(lines) + "\n"
    lines.append("crown: %d bud%s" % (fern.buds, "" if fern.buds == 1 else "s"))
    if fern.asleep:
        lines.append("asleep since %s" % fern.asleep.isoformat())
    if fern.flew:
        lines.append("spore flew %s" % fern.flew.isoformat())
    if fern.fronds:
        lines.append("fronds:")
        lines += [_frond_line(f) for f in fern.fronds]
    if fern.dead:
        lines.append("dead fronds:")
        lines += [_frond_line(f) for f in fern.dead[-DEAD_KEPT:]]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- the days

def _sky(ctx):
    return getattr(ctx, "sky", None)


def _light_share(ctx) -> float:
    return hands.num(getattr(ctx, "bed", None) or {}, "light", 1.0, 0.0, 1.0)


def _water(ctx) -> float:
    return hands.num(getattr(ctx, "bed", None) or {}, "water", 1.0, 0.0, 5.0)


def _rich(ctx) -> float:
    return hands.num(getattr(ctx, "bed", None) or {}, "rich", 0.0, 0.0, 1.0)


def _wet(sky) -> float:
    return max(0.0, min(1.0, float(getattr(sky, "wet", 0.5) or 0.0)))


def _this_year(frond, today) -> bool:
    """Did the frond come up this year? One with no date, or a date still to come (a hand's slip), is an old one."""
    return bool(frond.up and frond.up.year == today.year and frond.up <= today)


def _ferns_in_bed(ctx) -> int:
    count = 0
    for other in (getattr(ctx, "neighbours", None) or [])[:400]:
        if str(getattr(other, "kind", "") or "").lower() == KIND:
            count += 1
    return count


def _age(ctx, unknown=0.0) -> float:
    """Days since it was planted or sown, as the ground tells it (`unknown` if it does not)."""
    return hands.num({"age": getattr(ctx, "age", None)}, "age", unknown, 0.0, 1e6)


def sprout(seed, ctx) -> str:
    s = Seed(seed)
    fern = Fern()
    if s.spore and _age(ctx) < DAMP_DAYS:                   # a spore comes up as a prothallus; a fern that grew from
        fern.proth = 0                                      # spore long since has a crown, and comes again from it
        return write(fern, s)
    fern.buds = min(2 if s.spore else 3, s.fronds)
    sky, today = _sky(ctx), getattr(ctx, "date", None)
    if sky is not None and today and not (getattr(sky, "daylength", 12.0) >= WAKE_HOURS and getattr(sky, "season", "") in ("spring", "summer")):
        fern.asleep = today
    return write(fern, s)


def day(body, seed, ctx):
    if hands.is_dead(body):
        return body, None
    s, sky, today, rng = Seed(seed), _sky(ctx), getattr(ctx, "date", None), ctx.rng
    fern = read(body)
    if sky is None or today is None:
        return body, None
    if fern.read == 0:                                      # nothing of a fern could be read: cut to the ground
        return sprout(seed, ctx), "came up again from the seed"
    tmin, tmax = float(sky.tmin), float(sky.tmax)
    if tmin < s.hardy:
        return "%s %s, frost\n%s" % (hands.DAGGER, today.isoformat(), write(fern, s)), "died of frost"
    if fern.proth is not None:
        return _prothallus_day(fern, s, sky, ctx, today, rng)
    said = []
    warmth = max(0.0, float(getattr(sky, "warmth", 0.0)))
    wet, season = _wet(sky), str(getattr(sky, "season", ""))
    daylength = float(getattr(sky, "daylength", 12.0))

    # the crown wakes (quietly: its first crozier says so)
    if fern.asleep and daylength >= WAKE_HOURS and sky.tmean > 6.0 and season in ("spring", "summer"):
        fern.asleep = None

    # croziers come up: as many in a year as the seed's fronds, whatever still stands of last year
    if not fern.asleep and fern.buds > 0 and season in ("spring", "summer") and warmth > 3.0 \
            and sum(1 for f in fern.fronds if _this_year(f, today)) < s.fronds:
        last = max([f.up for f in fern.fronds if f.up and f.up <= today] + [datetime.date.min])
        if (today - last).days >= 3 and rng.random() < min(0.5, warmth / 16.0):
            first = not any(_this_year(f, today) for f in fern.fronds + fern.dead)
            used = {f.number for f in fern.fronds + fern.dead}
            number = max(used | {0}) + 1
            if number > FROND_NUMBER_MOST:                  # past what the body can read back: the lowest number free
                number = next(n for n in range(1, FROND_NUMBER_MOST + 1) if n not in used)
            if first:
                old = [f for f in fern.fronds if not _this_year(f, today)]
                if fern.dead or old:
                    said.append("the old fronds fell away")
                fern.dead = []
                fern.fronds = [f for f in fern.fronds if f not in old]
                said.append("the first crozier of the year is up")
            frond = Frond(number)
            frond.up, frond.length, frond.unroll = today, 2.0, 0
            fern.fronds.append(frond)
            fern.buds -= 1

    # croziers unroll and lengthen
    if not fern.asleep and warmth > 0:
        drought = wet < 0.1 and _water(ctx) < 1.5
        vigour = (1.0 - 0.6 * max(0.0, _light_share(ctx) - s.shade)) * (0.6 + 0.4 * wet) * (1.0 + 0.3 * _rich(ctx))
        rank = 0
        for frond in fern.fronds:
            if not _this_year(frond, today):
                continue
            rank += 1
            if not frond.unrolling or drought:
                continue
            step = min(0.12, warmth / 150.0)
            frond.length = min(400.0, frond.length + s.long * step * vigour * max(0.6, 1.0 - 0.04 * (rank - 1)))
            whole = int(step * 100)
            frond.unroll = min(100, frond.unroll + whole + (1 if rng.random() < step * 100 - whole else 0))

    # spore
    if not fern.asleep and daylength < SPORE_HOURS and season in ("summer", "autumn"):
        eligible = [f for f in fern.fronds if f.unroll >= 100 and not f.spore and not f.cropped and f.up
                    and (today - f.up).days >= SPORE_AGE]
        ripe = [f for f in fern.fronds if f.spore == "in spore"]
        spent = [f for f in fern.fronds if f.spore == "spent"]
        if eligible and not ripe and not spent and rng.random() < 0.05:    # the sori ripen together, once a year
            for frond in eligible:                                         # (quietly: the flight is what is told)
                frond.spore = "in spore"
        elif eligible and ripe:                                            # late fronds join the ripe ones, quietly
            for frond in eligible:
                frond.spore = "in spore"
        ripe = [f for f in fern.fronds if f.spore == "in spore"]
        # spore is dust: a dry day with a breath of wind, or a warm dry one, takes it, even at the foot of the wall
        if ripe and float(sky.rain) <= 0 and (float(sky.wind) >= 1.5 or tmax >= 20.0) and wet < 0.95 and rng.random() < 0.3:
            for frond in ripe:
                frond.spore = "spent"
            if not (fern.flew and fern.flew.year == today.year):
                said.append("its spore went on the wind")
            fern.flew = today

    # the sun
    if not fern.asleep and tmax >= 27.0 and float(sky.rain) <= 0 and wet < 0.35 and _light_share(ctx) > s.shade + 0.25:
        scorched = []
        for frond in fern.fronds:
            if frond.unroll >= 100 and rng.random() < 0.25 * (_light_share(ctx) - s.shade):
                scorched.append(frond)
        before = any(f.dead.startswith("scorched %d-" % today.year) for f in fern.dead)
        for frond in scorched:
            frond.dead = "scorched %s" % today.isoformat()
            fern.fronds.remove(frond)
            fern.dead.append(frond)
        if scorched and not before:                         # told once a summer; each frond's line keeps its day
            said.append("scorched in the sun: %d frond%s died" % (len(scorched), "" if len(scorched) == 1 else "s"))

    # the frost, and sleep
    sleeps = not fern.asleep and (tmin < 0 or season == "winter")
    if sleeps and season in ("autumn", "winter"):          # the year is counted once, as the crown goes to sleep for the
        grown = sum(1 for f in fern.fronds if f.unroll >= 100 and not f.cropped and _this_year(f, today))     # winter
        if grown:
            fern.buds += grown + 1                          # a crown that did well sends up one more next year
        fern.buds = max(2, min(s.fronds, fern.buds))
    killed = tmin < 0 and not s.evergreen and bool(fern.fronds)     # the frost kills them, the crown asleep or awake
    hard = s.evergreen and tmin < EVERGREEN_KILL and bool(fern.fronds)
    if killed or hard:
        if season in ("spring", "summer"):                  # a late frost: the crown will send up again what it took
            lost = sum(1 for f in fern.fronds if _this_year(f, today))
            fern.buds = max(fern.buds, min(s.fronds, fern.buds + lost))
        for frond in fern.fronds:
            frond.dead = "killed by frost %s" % today.isoformat()
        fern.dead += fern.fronds
        fern.fronds = []
    if sleeps:
        fern.asleep = today
    if killed:
        said.append("the fronds were killed by frost; the crown sleeps" if sleeps else "the fronds were killed by frost")
    elif sleeps:
        said.append("the crown sleeps")
    if hard:
        said.append("the fronds were killed by a hard frost")
    fern.dead = fern.dead[-DEAD_KEPT:]
    return write(fern, s), ("; ".join(said) if said else None)


def _prothallus_day(fern, s, sky, ctx, today, rng):
    wet, water, light = _wet(sky), _water(ctx), _light_share(ctx)
    room = hands.num(getattr(ctx, "bed", None) or {}, "room", 12, 0, 200)

    def died(how):          # a spore that fails the day after it landed fails quietly: its † line says it
        return ("%s %s, %s as a prothallus\n%s" % (hands.DAGGER, today.isoformat(), how, write(fern, s)),
                None if _age(ctx, 99.0) <= 1 else how)

    if _ferns_in_bed(ctx) >= max(1.0, room / 3.0):
        return died("crowded out")
    if float(sky.tmin) < -5.0 and rng.random() < 0.5:
        return died("frozen")
    if float(sky.rain) >= 1.0 or wet >= 0.25:
        if float(sky.tmin) > 0:
            fern.proth += 1
    elif wet < 0.12 and water < 1.5 and rng.random() < (0.5 if water >= 1.0 else 0.8):
        return died("dried out")
    if light > 0.8 and float(sky.tmax) >= 25.0 and rng.random() < 0.1:
        return died("scorched")
    if fern.proth >= DAMP_DAYS:
        fern.proth, fern.buds = None, 2
        if not (float(getattr(sky, "daylength", 12.0)) >= WAKE_HOURS and getattr(sky, "season", "") in ("spring", "summer")):
            fern.asleep = today
        return write(fern, s), "made a crown"
    return write(fern, s), None


# ----------------------------------------------- what creatures meet

def bitten(body, seed, ctx, share, by):
    """Slugs take the soft coiled tips, the smallest croziers first; a grazer crops every frond to a stub."""
    if hands.is_dead(body):
        return body, None
    s, fern, rng = Seed(seed), read(body), ctx.rng
    if fern.proth is not None:
        return body, None
    share = hands.num({"share": share}, "share", 0.0, 0.0, 1.0)
    by = " ".join(str(by or "something").split())[:40] or "something"
    if share >= 0.3:                                        # a grazer; a stub is not cropped again
        standing = [f for f in fern.fronds if not f.cropped]
        if not standing:
            return body, None
        for frond in standing:
            frond.length = max(3.0, round(frond.length * 0.3, 1))
            frond.cropped, frond.spore = True, ""
        return write(fern, s), "%s cropped it to stubs" % by
    soft = sorted([f for f in fern.fronds if f.unroll < 100 and not f.cropped], key=lambda f: f.length)
    if not soft:
        return body, None
    want = share * len(soft)
    take = int(want) + (1 if rng.random() < want - int(want) else 0)
    eaten, bit = [], []
    for frond in soft[:take]:
        if frond.length < 6.0:
            fern.fronds.remove(frond)
            eaten.append(frond.number)
        else:                                               # the coil is eaten into: less is left to unroll, so it comes out shorter
            frond.bitten = True
            frond.unroll = min(99, frond.unroll + 30)
            bit.append(frond.number)
    if not eaten and not bit:
        return body, None
    news = None
    if eaten:
        news = "%s ate the crozier of frond %s whole" % (by, " and ".join(str(n) for n in eaten[:2]))
    elif len(bit) >= 2:
        news = "%s bit %d croziers" % (by, len(bit))
    return write(fern, s), news


# -------------------------------------------------------------- spore

def _donor_seed(other):
    seed = getattr(other, "seed", None)
    if isinstance(seed, str):
        seed = hands.read_keys(seed)
    return seed if isinstance(seed, dict) else {}


def cast(body, seed, ctx) -> list:
    """On the day its spore flew: one spore, or two; a cross if a fern in spore stands near."""
    if hands.is_dead(body):
        return []
    fern, today, rng = read(body), getattr(ctx, "date", None), ctx.rng
    if fern.flew is None or today is None or fern.flew != today:
        return []
    own = {key: value for key, value in (seed.items() if isinstance(seed, dict) else hands.read_keys(seed).items()) if key in KEPT}
    own["kind"] = KIND
    mates = []
    for other in (getattr(ctx, "neighbours", None) or [])[:400]:
        if str(getattr(other, "kind", "") or "").lower() != KIND:
            continue
        distance = hands.num({"d": getattr(other, "distance", None)}, "d", 9.0)
        if distance > 0.35:                                 # (one standing at 0.0 is as near as can be)
            continue
        if "in spore" in str(getattr(other, "body", "") or "").lower() or "spent" in str(getattr(other, "body", "") or "").lower():
            mates.append(other)
    out = []
    for _ in range(1 if rng.random() < 0.7 else 2):             # one spore comes to anything, or two
        if mates and rng.random() < 0.5:
            mate = mates[rng.randrange(len(mates))]
            out.append(_crossed(own, _donor_seed(mate), getattr(ctx, "where", "a fern"), getattr(mate, "where", "another fern"), rng))
        else:
            child = dict(own)
            child["start"] = "spore"
            out.append(hands.write_keys(child))
    return out


def _crossed(own, donor, here, there, rng) -> str:
    a, b = Seed(own), Seed(donor)
    child = {
        "kind": KIND,
        "fronds": "%d" % round((a.fronds + b.fronds) / 2.0),
        "long": "%d" % round((a.long + b.long) / 2.0),
        "arch": "%.2f" % ((a.arch + b.arch) / 2.0),
        "cut": rng.choice((a.cut, b.cut)),
        "shade": "%.2f" % ((a.shade + b.shade) / 2.0),
        "evergreen": "yes" if rng.choice((a.evergreen, b.evergreen)) else "no",
        "sori": hands.mix(a.sori, b.sori, 0.5),
        "hardy": "%d" % round((a.hardy + b.hardy) / 2.0),
        "start": "spore",
        "from": "cross of %s × %s" % (here, there),
    }
    return hands.write_keys(child)


# ------------------------------------------------------------- describe

def describe(body, seed, ctx) -> str:
    fern = read(body)
    if hands.is_dead(body):
        if fern.proth is not None:
            return "dead; it was a prothallus"
        return "dead; it stood %d frond%s" % (len(fern.fronds), "" if len(fern.fronds) == 1 else "s")
    if fern.proth is not None:
        return "a prothallus, %d damp day%s" % (fern.proth, "" if fern.proth == 1 else "s")
    n = len(fern.fronds)
    unrolling = sum(1 for f in fern.fronds if f.unrolling)
    spore = sum(1 for f in fern.fronds if f.spore == "in spore")
    if fern.asleep and not n:
        text = "asleep; %d bud%s in the crown" % (fern.buds, "" if fern.buds == 1 else "s")
        if fern.dead:
            text += "; %d dead frond%s lying" % (len(fern.dead), "" if len(fern.dead) == 1 else "s")
        return text
    parts = ["%d frond%s" % (n, "" if n == 1 else "s")]
    if unrolling:
        parts.append("%d unrolling" % unrolling)
    if spore:
        parts.append("%d in spore" % spore)
    if fern.asleep:
        parts.append("asleep")
    return ", ".join(parts)


def size(body, seed) -> float:
    fern = read(body)
    if fern.proth is not None:
        return 0.5
    return sum(f.length for f in fern.fronds) / 15.0 + 0.5 * fern.buds


# ------------------------------------------------------------- the plate

def _pixel(fern, s) -> float:
    """About how many cm one pixel of the plate will stand for (see the bulb's account of the same)."""
    reach = max([f.length for f in fern.fronds + fern.dead] + [0.0])
    width = max(2.0 * reach + 2.0, 6.0)
    height = max(reach + 4.0, 6.0)
    return max(1.0 / UNIT_PX, width / 770.0, height / 840.0)


def _path(length, lean, arch, side, steps=14):
    """The rachis of a frond: from the crown, leaning `lean` degrees from upright, bending over by `arch` along its length."""
    pts, x, y = [(0.0, 0.0)], 0.0, 0.0
    for i in range(steps):
        t = (i + 0.5) / steps
        angle = math.radians(90.0 - side * min(108.0, lean + arch * 100.0 * t))
        x += math.cos(angle) * length / steps
        y = max(0.3, y + math.sin(angle) * length / steps)
        pts.append((x, y))
    return pts


def _length(pts) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def _at(pts, s):
    """The point `s` cm along the line, and the unit tangent there."""
    run = 0.0
    for a, b in zip(pts, pts[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        if seg <= 0:
            continue
        if run + seg >= s:
            t = (s - run) / seg
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), ((b[0] - a[0]) / seg, (b[1] - a[1]) / seg)
        run += seg
    a, b = pts[-2], pts[-1]
    seg = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    return b, ((b[0] - a[0]) / seg, (b[1] - a[1]) / seg)


def _part(pts, start, end):
    total = _length(pts)
    end = total if end is None else max(0.0, min(end, total))
    start = max(0.0, min(start, end))
    if end - start < 1e-9:
        return []
    out, run = [], 0.0
    for a, b in zip(pts, pts[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        first, run = run, run + seg
        if seg <= 0 or run <= start:
            continue
        if not out:
            t = (start - first) / seg
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
        if run >= end:
            t = (end - first) / seg
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
            return out
        out.append(b)
    return out


def _draw_frond(pen, s, frond, old_length, ink, fresh, px, sparse=False, dead_plant=False):
    """One frond: its rachis (old length in `ink`, the rest in `fresh`), its pinnae, its coil, its sori and its harm."""
    length = max(0.5, frond.length)
    lean, arch, side = frond._lean, frond._arch, frond._side
    pts = _path(length, lean, arch, side)
    old = min(old_length, length)
    for piece, colour in ((_part(pts, 0.0, old), ink), (_part(pts, old, None), fresh)):
        if len(piece) >= 2:
            pen.polyline(piece, 4, colour)
    coil_r = (COIL * (1.0 - frond.unroll / 100.0) + 0.4) if frond.unrolling and not frond.dead else 0.0   # a stub has none
    open_to = length - 1.6 * coil_r
    pmax = min(14.0, 0.17 * length)
    foot = max(0.22 * length, 1.5)                  # the stipe below the first pinnae is bare
    spore = frond.spore == "in spore" and not frond.dead and not dead_plant
    if s.cut == "none":
        _draw_blade(pen, s, frond, pts, length, foot, open_to, coil_r, pmax, old, ink, fresh, sparse, spore)
    else:
        _draw_pinnae(pen, s, frond, pts, length, foot, open_to, coil_r, pmax, old, ink, fresh, sparse, spore)
    # the coil of a crozier (a bitten one has lost its heart)
    tip, (tx, ty) = pts[-1], _at(pts, length)[1]
    past = tip                                      # where the frond's tip ends, coil and all
    reach = 0.0
    if coil_r > 0:
        nx, ny = -ty * side, tx * side              # toward the side it leans to: the coil curls inward
        cx, cy = tip[0] + nx * coil_r, tip[1] + ny * coil_r
        start = math.atan2(tip[1] - cy, tip[0] - cx)
        coil = []
        turns = 1.6
        for i in range(0, 13 if frond.bitten else 25):
            u = i / 24.0
            theta = start + side * u * turns * 2.0 * math.pi
            r = coil_r * (1.0 - 0.72 * u)
            coil.append((cx + math.cos(theta) * r, cy + math.sin(theta) * r))
        pen.polyline(coil, 3, fresh if length > old + 0.05 else ink)
        past, reach = (cx, cy), coil_r
    # harm, in the lettering's ink (the dead ink on what is dead)
    harm = "dead" if (frond.dead or dead_plant) else "ink"
    if frond.bitten:                                # just past the tip, or past the coil, clear of it
        out = reach + 10.0 * px
        pen.dot(past[0] + tx * out, past[1] + ty * out, 7, harm, filled=False, weight=3)
    if frond.cropped:                               # a cut straight across the stub
        half = 11.0 * px
        pen.line(tip[0] + ty * half, tip[1] - tx * half, tip[0] - ty * half, tip[1] + tx * half, 5, harm)


def _split(points, at, ink, fresh):
    """A line given as (position, point) pairs, as the plate's pieces: what lies up to `at` in `ink`, the rest in `fresh`."""
    kept = sum(1 for pos, _ in points if pos <= at + 1e-9)
    pieces = []
    if kept >= 2:
        pieces.append(([p for _, p in points[:kept]], ink))
    if kept < len(points):
        pieces.append(([p for _, p in points[max(0, kept - 1):]], fresh))
    return pieces


def _draw_blade(pen, s, frond, pts, length, foot, open_to, coil_r, pmax, old, ink, fresh, sparse, spore=False):
    """An undivided frond: its two edges, standing off the rachis by the pinna profile, and bars of sori across it."""
    if open_to <= foot + 0.5:
        return
    steps = 16
    left, right, bars = [], [], []
    for i in range(steps + 1):
        pos = foot + (open_to - foot) * i / steps
        t = pos / max(length, 1e-6)
        half = 0.55 * pmax * max(0.0, 4.0 * t * (1.0 - t)) ** 0.55
        half *= min(1.0, (pos - foot) / max(0.15 * length, 1e-6))     # the blade narrows into its stalk
        if coil_r > 0:
            half *= max(0.15, min(1.0, (open_to - pos) / (2.0 * COIL)))
        (x, y), (tx, ty) = _at(pts, pos)
        left.append((pos, (x - ty * half, y + tx * half)))
        right.append((pos, (x + ty * half, y - tx * half)))
        if spore and 2 <= i <= steps - 2 and i % 2 == 0:
            for way in (1, -1):                     # a bar each side of the midrib
                bars.append(((x - way * ty * half * 0.2, y + way * tx * half * 0.2),
                             (x - way * ty * half * 0.7, y + way * tx * half * 0.7)))
    # the edges meet the rachis at the foot and at the tip
    (fx, fy), _ = _at(pts, foot)
    (ex, ey), _ = _at(pts, open_to)
    for edge in ([(foot, (fx, fy))] + left + [(open_to, (ex, ey))], [(foot, (fx, fy))] + right + [(open_to, (ex, ey))]):
        for piece, colour in _split(edge, old, ink, fresh):     # new length in the fresh ink, as on the rachis
            pen.polyline(piece, 2.5, colour)
    for (ax, ay), (bx, by) in bars:
        pen.line(ax, ay, bx, by, 5.5, "paper")      # a rim of paper, so that the sori show whatever the blade's ink
        pen.line(ax, ay, bx, by, 2.5, s.sori)


def _draw_pinnae(pen, s, frond, pts, length, foot, open_to, coil_r, pmax, old, ink, fresh, sparse, spore=False):
    """The pinnae along the rachis, to one side and the other in turn, with their teeth, and sori dots on them in spore."""
    spacing = max(2.2, length / 22.0)
    teeth = {"once": 0, "twice": 1, "thrice": 2}.get(s.cut, 1)
    n, k = 0, 0
    pos = foot
    while pos < open_to and n < 46:
        n += 1
        if sparse and n % 2 == 0:
            pos += spacing
            continue
        t = pos / max(length, 1e-6)
        plen = pmax * max(0.0, 4.0 * t * (1.0 - t)) ** 0.55
        if coil_r > 0:
            plen *= max(0.15, min(1.0, (open_to - pos) / (2.0 * COIL)))   # the pinnae nearest the coil are still folded
        (x, y), (tx, ty) = _at(pts, pos)
        flip = 1 if k % 2 == 0 else -1
        k += 1
        ang = math.atan2(ty, tx) + flip * math.radians(62.0)
        ex, ey = x + math.cos(ang) * plen, y + math.sin(ang) * plen
        if ey < 0.0:                                        # a frond lying on the ground carries its pinnae upward
            flip = -flip
            ang = math.atan2(ty, tx) + flip * math.radians(62.0)
            ex, ey = x + math.cos(ang) * plen, y + math.sin(ang) * plen
        colour = ink if pos <= old else fresh
        pen.line(x, y, ex, ey, 2.5, colour)
        for j in range(teeth):
            f = (j + 1) / (teeth + 1.0)
            bx, by = x + (ex - x) * f, y + (ey - y) * f
            tooth = plen * 0.28
            tang = ang - flip * (1 if j % 2 == 0 else -1) * math.radians(58.0)     # mirrored: on either side, the
            pen.line(bx, by, bx + math.cos(tang) * tooth, by + math.sin(tang) * tooth, 2, colour)   # first toward the tip
        if spore and ((n - 1) // 2) % 2 == 0:              # every other pair of pinnae, on both sides
            dx, dy = x + (ex - x) * 0.55, y + (ey - y) * 0.55
            pen.dot(dx, dy, 5, "paper")                     # a rim of paper, so that the sori show whatever the frond's ink
            pen.dot(dx, dy, 3, s.sori)
        pos += spacing


def draw(body, seed, ctx, pen) -> None:
    s, fern = Seed(seed), read(body)
    dead = hands.is_dead(body)
    left = getattr(ctx, "left", None)
    was = read(left) if left is not None else None
    pen.unit_name = "cm"
    pen.unit_px_max = UNIT_PX
    pen.ground(0)
    px = _pixel(fern, s)
    wood, fresh = ("dead", "dead") if dead else ("wood", "fresh")
    if fern.proth is not None:                      # a few millimetres across, drawn larger, and the bar says so
        pen.unit_px_max = PROTH_PX
        new = was is None or was.proth is None
        ink = fresh if new else wood
        r, top = 0.15, 0.21                         # the heart is 4r across: 6 mm
        pen.arc(-r, top, r, 0, 180, 3, ink)
        pen.arc(r, top, r, 0, 180, 3, ink)
        pen.line(-2 * r, top, 0.0, 0.0, 3, ink)
        pen.line(2 * r, top, 0.0, 0.0, 3, ink)
        pen.note(describe(body, seed, ctx))
        return
    # fronds: the newest stand straight, the oldest lean out (past seven, the lean is shared out among them all)
    living = list(fern.fronds)
    old_lengths = {f.number: f.length for f in (was.fronds if was is not None else [])}
    count = len(living)
    step = min(11.0, 66.0 / max(1, count - 1))
    for i, frond in enumerate(living):
        frond._side = -1 if frond.number % 2 else 1
        frond._lean = 8.0 + step * (count - 1 - i)
        frond._arch = s.arch * (0.5 + 0.5 * frond.unroll / 100.0)
        _draw_frond(pen, s, frond, old_lengths.get(frond.number, 0.0) if was is not None else 0.0, wood, fresh, px,
                    dead_plant=dead)
    for j, frond in enumerate(fern.dead[-DEAD_KEPT:]):    # lying along the ground
        frond._side = -1 if frond.number % 2 else 1
        frond._lean = 86.0 + 2.0 * (j % 3)
        frond._arch = 0.1
        _draw_frond(pen, s, frond, frond.length, "dead", "dead", px, sparse=True, dead_plant=dead)
    # the crown and its buds, over the feet of the fronds, never too small to see
    crown = max(1.0, 10.0 * px)
    pen.arc(0.0, 0.0, crown, 0, 180, 4, wood)
    old_buds = was.buds if was is not None else 0
    gap = max(1.4, 11.0 * px)
    for k in range(min(fern.buds, FRONDS_MOST)):
        x = (k - (min(fern.buds, FRONDS_MOST) - 1) / 2.0) * gap
        pen.dot(x, -max(1.3, 12.0 * px), 4, wood if k < old_buds else fresh)
    pen.note(describe(body, seed, ctx))
