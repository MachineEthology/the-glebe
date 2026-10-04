"""
Tally: a plant that counts.

A tally is one of two things, and its seed says which.

A COUNTER keeps count of something that really happens in the garden: wet
days, frosts, full moons, the days the keeper wrote. It lays one stroke for
each, in fives, a line for each month, and over the years its plate becomes
a calendar of the garden's weather and life.

A RECURRENCE grows a row of numbers. Each new number is made from the ones
before it by a small rule written in its seed, and the plant lays one on the
days its temperament allows, when it has gathered the sap for it. Its plate
draws the numbers so that the rule can be guessed by looking. Guess first;
then open the seed.


THE SEED, LINE BY LINE

    kind: tally
    counts: wet days          a counter: what it keeps count of (see WHAT A COUNTER CAN COUNT)

or

    kind: tally
    rule: a + b               a recurrence: how the next number is made (see THE RULE)
    start: 1, 1               the numbers it starts from, oldest first (at most eight; 1 if none)
    steps: wet days           the days it may lay a number: anything a counter can count,
                              or "when it can" (the default: any day it has the sap)

and for either:

    flowers: spring, summer   the seasons it may flower in (spring and summer if not said)
    colour: violet            the ink of its flowers: a plate ink (blue, pink, dark-red...) or #rrggbb,
                              read loosely ("pale pink, like an astrance" is pale-pink); violet if none
    leaf: waxy                or downy; stem: brittle, or thorny; scent: dusk, or night (see TRAITS)
    variety: <a name>         a name a visitor gave it; seed it sets without a cross carries it on

A seed with a rule: line is a recurrence; any other is a counter. A seed that
says nothing but its kind counts days.

Once a tally has grown, its body says which of the two it is, and the body
wins. If its seed loses its rule (emptied, or the key misspelt), a
recurrence does not turn into a counter and forget its numbers: it sleeps,
and its body says why, until the seed is mended. A counter whose seed gains
a rule sleeps the same way. To turn a tally from one way to the other,
change its seed and cut its body to the ground.


WHAT A COUNTER CAN COUNT

The counts: line is read word by word, in English or French: "rainy days",
"nights of frost", "jours de pluie". Plurals and the small words between
are let pass. It does not guess: a word it does not know ("thunder",
"beautiful"), two things at once ("frost and snow"), or a not, no or
without ("days without frost", "frost-free") and the counter sleeps, and
its body says what it could not count. (One such phrase it does know:
"days without rain" are dry days.) A steps: line it cannot read is taken
as "when it can".

Everything but the moon is measured as its own bed feels the day: a
sheltered bed counts fewer frosts, a dry one fewer wet days, and a north
wall hardly any sunny ones.

    wet days       at least 1 mm of rain (or of snow's water) reached its bed
    dry days       none did
    frosts         the night went below 0 °C in its bed
    hard frosts    below -5 °C
    snow days      what fell was snow
    warm days      the day reached 20 °C
    sunny days     at least 5 hours of useful light reached its bed
    windy days     the wind in its bed reached force 5
    bee days       warm (13 °C), dry and still: days bees can fly. It reads the sky, not the bees.
    full moons     the night the moon came full (one a month)
    new moons      the night of the new moon
    keeper's days  days the keeper wrote: a line for that day in gate/sky.txt,
                   or a note at the gate whose name carries the date
    days the keeper says <word>
                   days their line at the gate names it: "days the keeper says hedgehog"
    book pages     pages that appeared in the visitors' book, a stroke for each, on the
                   first day the days find it. (A visit leaves no other trace a plant can see.)
    days           every day

A counter speaks to the almanac only when its own record says something
new: the first of its thing after two months with none ("counted its first
frost since March"); a month with none where every earlier year (two at
least) had some ("counted no wet days in July, the first July without"); a
month with more than any month before it, once it has a year of record;
and for the moon, a month with two of its moons, or none. Days, and months
of one moon, it does not mention: the calendar knows them already. Where
two counters of the same thing share a bed, only the elder speaks: they
counted the same days.

A counter keeps count for about six years. In a winter after its sixth
year of counting it dies back, and in time the days carry its record to
the heap, where the months rot into the soil.


THE RULE

A recurrence's rule is a small sum, read by the kind itself word by word.
Nothing in it is ever run as a program. It may use:

    a              the newest number; b the one before; c and d the ones before those
                   (a number before the first is 0)
    n              how many numbers it has already (so after a start of one number,
                   the first new one is made with n = 1)
    m              the newest number of the nearest other tally in its bed: a
                   recurrence's newest number, or a counter's count for the month so far
    whole numbers, + - * / % **     (/ is whole division, rounded down; ^ is read as **)
    < <= > >= == !=, and, or, not   (a single = is read as ==; a test is true when not 0)
    x if <test> else y
    gcd(x, y)  lcm(x, y)  isprime(x)  digitsum(x)  digits(x)  rev(x)  isqrt(x)
    abs(x)  min(x, y, ...)  max(x, y, ...)
    seen(x)        1 if x is already one of its numbers, else 0
    term(k)        its number at place k, counting from 0 (0 if there is none)

"3a" is read as 3 * a, and "mod" as %. A number may have at most six digits.
A number written with commas, as the almanac writes it (1,242), is one
number, in the body and in start: alike.

A recurrence stops growing, and is complete, when:
    its next number would have more than six digits (it has reached its height);
    it comes round: its newest numbers are ones it has had before, in the same order,
        so it would only go round again (this is known only for rules that use
        nothing but a, b, c, d);
    its rule gives no number (it divided by nothing);
    or it has 1,000 numbers (it is full grown).
A complete recurrence stands, and flowers in its seasons, for about a year
after; then it dies back, and in time the days carry it to the heap.

A recurrence tells the almanac when it first flowers each year (and on which
numbers), its 100th, 250th, 500th and 750th numbers, and how it came to be
complete.


THE BODY

A counter's body:

    a tally of wet days
    counting since 2026-10-01
    2026-10  ||||/ ||||/ ||:
    2026-11  ||||/ ||
    2026-12
    last flowered: 2027

Each month has a line. | is a stroke; / is the fifth stroke, drawn through the
four before it, and closes a gate of five; : is a stroke that was bitten or
snapped (it still counts); x is a stroke a hand struck out (it does not). A
month's line with nothing after it was counted and came to nought. A record
of more than twenty years (a counter does not live so long, but a hand may
write one) folds its oldest year into one line: "2026: 148".

A recurrence's body:

    sap: 2.41
    2026-10  0 1 3 6 2 7 13
    2026-11  20 12 21 11 22 10
    last flowered: 2027
    complete: 2029-06-02, full grown, at 1000 numbers, ending 1995 3014 1994 3015

Its numbers, oldest first, run on from line to line; each is laid on the line
of the month it came. sap is the growth it has gathered and not yet spent.
The complete line keeps how many numbers it had and the newest of them, so
that it knows when a hand has changed them.

In both, a line beginning with # is a remark and is kept; any other line the
kind cannot read is let go when the plant next grows. Other lines it writes:
"pages seen" (how many pages of the book it has counted), "moon" (the moon's
phase when it last looked, so it can tell the night it turned), "asleep"
(why it is not growing).


CUTTING IT

A counter is soft to the hand: its lines part anywhere. Cut a month's line and
that month is gone from the record, and from the plate; the count goes on
from today. Take strokes off a line and the month counts fewer. To strike a
stroke and still show that it was there, write x in its place.

A recurrence is brittle in another way: every number leans on the ones
before. Cut the newest numbers and it grows them again, the same ones, as a
clipped hedge grows its shape (unless its rule listens to a neighbour, m).
Change its newest number and the numbers still to come change with it.
Change or cut one from the middle and the numbers already laid stay as they
are; only those still to come may change, and only if its rule remembers
(with n, seen or term). To strike a number and keep it on the plate, write
x before it: x13. The rule then passes over it as if it had never been. A
complete plant cut back, or with its newest numbers changed, begins to grow
again. Delete the "complete" line and it tries again from where it stands.

An empty body comes up again from the seed: a counter begins its count again,
a recurrence begins again from its start. So does a recurrence left with no
numbers at all.


GROWTH, AND THE BED

A counter's growth is its record, so it answers the sky exactly as its bed
feels it. A recurrence gathers sap each day it is not frozen, more with
warmth (to 15 °C), light (to 8 hours in its bed), and ground that is not dry,
and more on ground made rich; sap runs to eight at most. On a day its
temperament allows, it lays one number, which costs 1 sap for a number of
one digit and 0.2 more for each digit after. So a recurrence in the open
border grows most days of a summer, one under the north wall one day in
three, and none grows in the cold of winter. Big numbers come slowly.


TRAITS

Each shows on the line the plant stands on: a recurrence's number line, or the
ground under each month a counter has counted.

    leaf: waxy      holds out in drought: dry ground slows neither its sap nor its flowers.
                    On the plate its line is doubled.
    leaf: downy     takes frost better: its sap runs and its flowers stay open down to -4 °C.
                    Its line is stippled.
    stem: brittle   wind of force 5 or more in its bed may snap off its newest number (a
                    recurrence, which grows it again on another day), or break its newest
                    stroke (a counter): one day in seven at force 5, more as it blows
                    harder. Its line is broken.
    stem: thorny    a bite takes a third of what it would. Its line has thorns, pointing down.
    scent: dusk     (or night) moths come to its flowers. Scent is not drawn.


FLOWERS, SEED AND CROSSES

A recurrence flowers on its primes: in its seasons, each prime among its five
newest numbers is an open flower. A counter flowers on its closed gates: in
its seasons, each gate of five closed this month, not bitten, is a flower.
Neither opens a flower on a frozen night or on dry ground (unless downy or
waxy), nor before it is two months old. A rule that makes no primes never
flowers, and spreads only by hand.

With flowers open, a tally now and then sows itself, from four months old,
whether or not pollen came that day. A recurrence's seedling starts from the
number it flowered on (with the numbers before it that its rule needs) and
is named for it; a counter's seedling counts what its parent counts.

When bees or moths have carried pollen from another tally, a seed may also
be a cross. It takes the rule of the parent that has one (the seed-bearer's
first); it starts from the numbers of the other parent: its newest numbers
if it grows in the same bed, else the start: written in its seed, for
pollen from another bed brings the seed's words and not the body. A counter
gives the counts of its newest whole months, so the weather sows the
numbers (a counter in another bed gives none, and the cross starts from the
seed-bearer's own flower). Its temperament, seasons and traits come from
either parent; its colour is the two blended; and it carries no variety
name.

Bites (slugs, and other mouths) take what is soft. From a recurrence, a share
of its sap, and a hard bite takes its newest number too, which it grows
again. On a counter, a bite breaks strokes of this month: they still count,
but a bitten gate does not flower. Only a bite that costs something to see
is told in the almanac: a number lost, or a gate in flower broken.


THE PLATE

A counter is drawn as a calendar: a band for each year, the newest at the
top, its year at the left and its count for the year at the right (the plate
has room for its six newest years; a note says how many earlier ones are not
drawn); a column for each month, January to December, lettered along the
foot. Under each month it counted runs a short stretch of ground in the
planter's ink; a month with no ground was not counted (before it was sown,
or cut from the body), while a month with bare ground was counted and came
to nought. The strokes stand on that ground in gates of five, one gate
above another, so a tall column is a month with much of what it counts. A
stroke with a gap in it was bitten or snapped; a grey cross was struck out
by a hand; a dot of its colour, ringed, at the head of a gate is a flower.
The scale bar measures months. The plate does not say what it counts: the
shape of the years says it, for those who look (strokes only in the cold
months, strokes in every month, one a month), and the seed says it plainly.

A recurrence is drawn on its number line, in the planter's ink, from 0 to its
highest number, both lettered at the ends. (When its numbers all lie far
from 0, in a narrow band, the line starts at its lowest number instead
(or, below 0, ends at its highest), and a small break of two slants at
that end says the line was cut short of 0; a line that runs across 0 has a
tick at 0.) From each number to the next an arc is drawn, the
first above the line, the next below, and so on in turn, each as wide as
the step it makes: so the size and the rhythm of the steps can be read
(once it has more than 400 numbers, only its newest 400 steps have arcs).
Where many arcs lie close together they draw as one heavy band. A small
ring on the line is a step that stayed where it was. Beneath, the numbers
fall as tally strokes: a short upright stroke for each number, at its place
on the line above, each a little lower than the one before, so the column
reads the numbers in the order they came, the oldest at the top. The column
falls in order, one tread for each number, not in numbers or days: a dry
spell leaves no gap. Once there are many numbers the strokes shrink to
dots, still one for each. Only the line and the arcs are drawn to the scale
bar. At the head of the plate its first eight numbers are written out, and
its newest is written under the last stroke. A bar under the last stroke:
it is complete. A ringed dot of its colour on a short stalk above the line
is an open flower, at its number. A small grey cross on the line is a
number a hand struck out.

In both, what has grown since the last visitor left is in the fresh green,
and a dead plant is grey. The texture marks of a trait are spaced unevenly
on purpose: they are not a scale.
"""

import ast
import math
import re
import unicodedata
from datetime import date as Date, timedelta

import hands

KIND = "tally"

CAP = 999_999            # the largest a number may be: six digits
BIGGEST = 10 ** 24       # the largest a rule may reach on the way to a number
MOST_NUMBERS = 1000      # a recurrence with this many is full grown
START_MOST = 8           # numbers a start may give
SAP_MOST = 8.0           # sap a recurrence can hold
SPENT_AFTER = 400        # days a complete recurrence stands before it dies back
COUNT_YEARS = 6          # years a counter keeps count before it may die back, in a winter
WINTER_END = 1 / 45      # its chance on each winter day after that (most go in the first winter, some in the next)
KEPT_YEARS = 20          # years a counter keeps month by month; older ones fold into a line each (a hand may make
                         # a counter's record older than it lives)
DRAWN_YEARS = 6          # years a counter's plate shows
ARCS_MOST = 400          # steps a recurrence's plate draws arcs for (the newest); its strokes show every number
REMARKS_MOST = 12        # remark lines kept in a body
RULE_LONGEST = 240       # characters of a rule it will read
MILESTONES = (100, 250, 500, 750)
FLOWERS_FROM = 60        # days old before a tally flowers
SEEDS_FROM = 120         # days old before it sets seed
OWN_SEED = 0.0015        # chance a day, for each open flower, that it sows itself (no pollen came)
CROSSED = 0.01           # the same, when pollen was carried to it
SEASONS = ("spring", "summer", "autumn", "winter")
MONTHS = ("January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December")
DEFAULT_COLOUR = "violet"
KEPT = ("kind", "counts", "rule", "start", "steps", "flowers", "colour", "leaf", "stem", "scent", "variety")

DAGGER = "†"
ELLIPSIS = "…"
CROSS = "×"


# ================================================================= the sky, read as things to count

def _plain(text) -> str:
    """Lower case, accents taken off, for loose matching: 'Gelée' -> 'gelee'."""
    text = unicodedata.normalize("NFKD", str(text or "").lower())
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def _num(value, default=0.0) -> float:
    try:
        value = float(value)
    except Exception:
        return default
    return value if value == value else default


def _soil_texts(ctx) -> list:
    try:
        return list(ctx.soil.texts())
    except Exception:
        return []


def _pages(ctx) -> int:
    """How many pages the visitors' book holds today."""
    return sum(1 for where, _ in _soil_texts(ctx) if str(where).replace("\\", "/").startswith("book/"))


def _moon_turned(led, sky, at) -> bool:
    """Did the moon pass `at` (0.5 full, 0 or 1 new) since the phase the body last wrote down?"""
    now = _num(getattr(sky, "moon", 0.0)) % 1.0
    was = led.moon
    if was is None:
        return False
    if at == 0.5:
        return was < 0.5 <= now or (now < was and was < 0.5)      # (a whole cycle in one day cannot happen)
    return now < was                                             # the phase wrapped round through new


class Thing:
    """Something a counter can count, or a recurrence can step on."""

    def __init__(self, name, one, many, test):
        self.name, self.one, self.many, self.test = name, one, many, test

    def words(self, count) -> str:
        return "%d %s" % (count, self.one if count == 1 else self.many)


def _keeper_wrote(sky, ctx, led) -> int:
    if str(getattr(sky, "remark", "") or "").strip():
        return 1
    day = ctx.date.isoformat()
    return int(any(str(where).replace("\\", "/").startswith("gate/") and day in str(where)
                   for where, _ in _soil_texts(ctx)))


def _new_pages(sky, ctx, led) -> int:
    now = _pages(ctx)
    if led.pages is None:
        led.pages = now
        return 0
    new = max(0, now - led.pages)
    led.pages = now
    return new


def _moon_count(at):
    def test(sky, ctx, led):
        return int(_moon_turned(led, sky, at))
    return test


# what it can count: its name -> one, several, the test (sky, ctx, ledger) -> strokes to lay today
_THINGS = {
    "hard frosts": ("hard frost", "hard frosts", lambda s, c, l: int(s.tmin <= -5)),
    "frosts": ("frost", "frosts", lambda s, c, l: int(s.tmin < 0)),
    "snow days": ("snow day", "snow days", lambda s, c, l: int(bool(s.snow))),
    "wet days": ("wet day", "wet days", lambda s, c, l: int(s.rain >= 1.0)),
    "dry days": ("dry day", "dry days", lambda s, c, l: int(s.rain < 0.2)),
    "new moons": ("new moon", "new moons", _moon_count(0.0)),
    "full moons": ("full moon", "full moons", _moon_count(0.5)),
    "warm days": ("warm day", "warm days", lambda s, c, l: int(s.tmax >= 20)),
    "sunny days": ("sunny day", "sunny days", lambda s, c, l: int(s.light >= 5.0)),
    "windy days": ("windy day", "windy days", lambda s, c, l: int(s.wind >= 5)),
    "bee days": ("bee day", "bee days", lambda s, c, l: int(s.tmax >= 13 and s.rain < 0.5 and s.wind <= 4)),
    "keeper's days": ("day the keeper wrote", "days the keeper wrote", _keeper_wrote),
    "book pages": ("page in the book", "pages in the book", _new_pages),
    "days": ("day", "days", lambda s, c, l: 1),
}

# The words that name each thing. A word must be one of these whole (a plural s, x or es is let pass),
# so "sundays" is not sun, nor "angels" frost, nor "trains" rain.
_WORDS = {}
for _name, _said in (
        ("frosts", "frost frosty frozen froze freeze freezes freezing gel gele gelee gelees"),
        ("snow days", "snow snowy snowed snowing snowfall neige neigeux neigeuse neigeuses enneige"),
        ("wet days", "wet rain rainy rained raining rainfall shower showers drizzle pluie pluvieux pluvieuse "
                     "pluvieuses humide averse bruine"),
        ("dry days", "dry sec seche"),
        ("full moons", "moon lune"),
        ("warm days", "warm hot heat chaud chaude chaleur"),
        ("sunny days", "sun sunny sunshine sunlight sunlit clear bright soleil ensoleille ensoleillee"),
        ("windy days", "wind windy gale storm stormy blustery breezy vent venteux venteuse tempete"),
        ("bee days", "bee abeille"),
        ("keeper's days", "keeper gardien gardienne gate"),
        ("book pages", "book page visit visitor livre visite visiteur"),
        ("days", "day daily jour journee every each all chaque tous toutes")):
    for _w in _said.split():
        _WORDS[_w] = _name

# Words that turn the thing beside them: a hard frost, a new moon, a full moon.
_TURNS = {"hard": "hard", "heavy": "hard", "severe": "hard", "fort": "hard", "forte": "hard", "grand": "hard",
          "new": "new", "nouvelle": "new", "full": "full", "pleine": "full"}
# Words that say not: a phrase with one of them is not guessed at (but for "without rain", which is dry days).
_NOT = {"not", "no", "non", "without", "sans", "never", "jamais", "pas", "free", "nor", "none", "ni", "except",
        "sauf", "aucun", "aucune", "hardly", "barely"}
# The small words between, let pass.
_FILLER = set("""
    the a an of on in at to with when which where that it its s there was were is are be been this these those by
    for from as and or than then i we you my our your her his their them they one some any
    came come comes fell fall falls blew blow blows shone shine shines flew fly flies flying could can wrote write
    writes written left leave leaves said say says reached reach reaches went go goes turned turn got get had has
    have did do does
    night nights time times weather morning mornings evening evenings count counts counting number how many much
    note notes line lines garden bed
    de des du d la le les l un une en et ou au aux quand il elle y avec par sur dans qu que qui est sont nuit nuits
    temps matin matins soir soirs fois jardin
""".split())
_KEEPER_SAYS = re.compile(r"keeper\S*\s+(?:says|said|names|named|writes|wrote|mentions|mentioned|calls)\s+(.+)$")
_ANY_DAY = re.compile(r"^\s*(?:when it can|whenever|any ?day|always|every ?day|daily|tous les jours)?\s*$")


def _named(word):
    """The thing a single word names ('rainy' -> wet days, 'frosts' -> frosts), or None."""
    for form in (word, word[:-1] if word[-1:] in "sx" else "", word[:-2] if word.endswith("es") else ""):
        if form and form in _WORDS:
            return _WORDS[form]
    return None


def _read_phrase(plain):
    """The name of the one thing a plain phrase asks for, word by word; None if it is not sure.

    Every word must be known: a thing, a word that turns it (hard, new, full),
    a small word between, or a not. Two things, or any not, and it will not
    guess; except that "without rain", "no rain", "sans pluie" and "rainless"
    are dry days. ("Not a wet day" is not: a day of half a millimetre is
    neither wet nor dry.)
    """
    words = re.findall(r"[a-z]+", plain)
    things, turns, negated, rainless = set(), set(), False, False
    for i, w in enumerate(words):
        if w in _NOT:
            negated = True
            rainless = rainless or (w in ("without", "sans", "no") and
                                    any(x in ("rain", "rains", "pluie", "pluies") for x in words[i + 1:i + 3]))
        elif w.endswith("less") and _named(w[:-4]):          # rainless, moonless, sunless
            negated = True
            rainless = rainless or w == "rainless"
            things.add(_named(w[:-4]))
        elif _named(w):
            things.add(_named(w))
        elif _TURNS.get(w) or _TURNS.get(w[:-1] if w[-1:] == "s" else ""):
            turns.add(_TURNS.get(w) or _TURNS.get(w[:-1]))
        elif w in ("froid", "froids") and any(x in ("grand", "grands") for x in words):
            things.add("frosts")                             # le grand froid: hard frosts, with its "grand"
        elif w not in _FILLER and not (w[-1:] == "s" and w[:-1] in _FILLER):
            return None                                      # a word it does not know
    if len(things) > 1:
        things.discard("days")                               # "every wet day" is wet days
    if len(things) != 1:
        return None
    name = things.pop()
    if negated:                                          # only "without rain", "no rain", "sans pluie", "rainless"
        return "dry days" if rainless and name == "wet days" and not turns else None
    if not turns:
        return name
    if turns == {"hard"} and name == "frosts":
        return "hard frosts"
    if turns == {"new"} and name == "full moons":
        return "new moons"
    if turns == {"full"} and name == "full moons":
        return name
    return None


def _thing(phrase):
    """The Thing a phrase names ('wet days', 'days the keeper says hedgehog'), or None if it is not sure."""
    plain = _plain(phrase).strip()
    said = _KEEPER_SAYS.search(plain)
    if said:
        word = said.group(1).strip(" .,;:!?\"'()")[:40]
        if word:
            pattern = re.compile(r"(?<![a-z])%s(?![a-z])" % re.escape(word))
            written = re.search(_KEEPER_SAYS.pattern, " ".join(str(phrase).split()), re.I)
            shown = written.group(1).strip(" .,;:!?\"'()")[:40] if written else word     # as the seed wrote it

            def names(sky, ctx, led, pattern=pattern):
                return int(bool(pattern.search(_plain(getattr(sky, "remark", "")))))
            return Thing("keeper says " + word, "day the keeper named " + shown,
                         "days the keeper named " + shown, names)
    if not plain:
        return None
    name = _read_phrase(plain)
    if name is None:
        return None
    one, many, test = _THINGS[name]
    return Thing(name, one, many, test)


def _counts(seed):
    """What a counter's seed asks it to count: (Thing or None, the words the seed used)."""
    phrase = hands.line(seed, "counts", "") or hands.line(seed, "count", "")
    if not phrase:
        return _thing("days"), "days"
    return _thing(phrase), phrase[:60]


def _steps(seed):
    """What a recurrence's temperament lets it step on: a Thing, or None for 'when it can'."""
    phrase = hands.line(seed, "steps", "") or hands.line(seed, "steps on", "") or hands.line(seed, "on", "")
    if _ANY_DAY.match(_plain(phrase)):
        return None
    found = _thing(phrase)
    return None if found is None or found.name == "days" else found


def _needs_moon(thing) -> bool:
    return thing is not None and thing.name in ("full moons", "new moons")


# ================================================================= the rule

class _Unreadable(Exception):
    """The rule cannot be read; the message says why, in plain words."""


class _NoNumber(Exception):
    """The rule gave no number this time (it divided by nothing)."""


class _TooBig(Exception):
    """The rule reached past what a tally can hold."""


def _held(v):
    if isinstance(v, bool):
        return int(v)
    if not isinstance(v, int):
        raise _NoNumber("it made something that is not a whole number")
    if v > BIGGEST or v < -BIGGEST:
        raise _TooBig()
    return v


def _whole(x):
    return int(x) if isinstance(x, bool) else x


def _div(x, y):
    if y == 0:
        raise _NoNumber("it divided by nothing")
    return _held(x // y)


def _mod(x, y):
    if y == 0:
        raise _NoNumber("it divided by nothing")
    return _held(x % y)


def _pow(x, y):
    x, y = _whole(x), _whole(y)
    if y < 0:
        raise _NoNumber("it raised a number to a power below nothing")
    if abs(x) > 1 and y * math.log10(abs(x)) > 25:
        raise _TooBig()
    if abs(x) <= 1 and y > 2:
        y = 2 + y % 2                     # 0, 1 and -1 go round in twos; no need to multiply a billion times
    return _held(x ** y)


_ARITH = {
    ast.Add: lambda x, y: _held(x + y),
    ast.Sub: lambda x, y: _held(x - y),
    ast.Mult: lambda x, y: _held(x * y),
    ast.Div: _div,
    ast.FloorDiv: _div,
    ast.Mod: _mod,
    ast.Pow: _pow,
}
_COMPARE = {
    ast.Lt: lambda x, y: x < y, ast.LtE: lambda x, y: x <= y,
    ast.Gt: lambda x, y: x > y, ast.GtE: lambda x, y: x >= y,
    ast.Eq: lambda x, y: x == y, ast.NotEq: lambda x, y: x != y,
}
_SIGNS = {ast.BitXor: "^", ast.BitAnd: "&", ast.BitOr: "|", ast.LShift: "<<", ast.RShift: ">>", ast.MatMult: "@"}


def _isprime(n) -> bool:
    """Is n prime? Exact for every number a rule can reach (Miller-Rabin with enough witnesses)."""
    n = _whole(n)
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _digitsum(x):
    return sum(int(ch) for ch in str(abs(_whole(x))))


def _rev(x):
    x = _whole(x)
    value = int(str(abs(x))[::-1])
    return -value if x < 0 else value


def _isqrt(x):
    if x < 0:
        raise _NoNumber("it took the root of a number below nothing")
    return math.isqrt(_whole(x))


def _gcd(*xs):
    return math.gcd(*[_whole(x) for x in xs])


def _lcm(*xs):
    return _held(math.lcm(*[_whole(x) for x in xs]))


# name -> (fewest arguments, most arguments, what it does: f(env, *values))
_FUNCTIONS = {
    "gcd": (2, 8, lambda env, *xs: _gcd(*xs)),
    "lcm": (2, 8, lambda env, *xs: _lcm(*xs)),
    "isprime": (1, 1, lambda env, x: int(_isprime(x))),
    "digitsum": (1, 1, lambda env, x: _digitsum(x)),
    "ds": (1, 1, lambda env, x: _digitsum(x)),
    "digits": (1, 1, lambda env, x: len(str(abs(_whole(x))))),
    "rev": (1, 1, lambda env, x: _rev(x)),
    "isqrt": (1, 1, lambda env, x: _isqrt(x)),
    "abs": (1, 1, lambda env, x: abs(_whole(x))),
    "min": (1, 8, lambda env, *xs: min(_whole(x) for x in xs)),
    "max": (1, 8, lambda env, *xs: max(_whole(x) for x in xs)),
    "seen": (1, 1, lambda env, x: int(_whole(x) in env["seen"])),
    "term": (1, 1, lambda env, k: _term_at(env["terms"], k)),
}
_VARIABLES = ("a", "b", "c", "d", "n", "m")


def _term_at(terms, k):
    k = _whole(k)
    return terms[k] if 0 <= k < len(terms) else 0


def _build(node, used, depth=0):
    """A piece of the rule's tree, checked against the whitelist, as a function of the numbers so far."""
    if depth > 40:
        raise _Unreadable("its rule is nested too deep to read")
    kind = type(node)
    if kind is ast.Constant:
        value = node.value
        if isinstance(value, bool):
            value = int(value)
        if not isinstance(value, int):
            raise _Unreadable("it counts only in whole numbers")
        if abs(value) > BIGGEST:
            raise _Unreadable("its rule holds a number too big to read")
        return lambda env: value
    if kind is ast.Name:
        name = node.id
        if name not in _VARIABLES:
            raise _Unreadable("it does not know the name %s" % name[:20])
        used.add(name)
        return lambda env: env[name]
    if kind is ast.UnaryOp:
        inner = _build(node.operand, used, depth + 1)
        if isinstance(node.op, ast.USub):
            return lambda env: _held(-inner(env))
        if isinstance(node.op, ast.UAdd):
            return inner
        if isinstance(node.op, ast.Not):
            return lambda env: 0 if inner(env) else 1
        raise _Unreadable("it does not know the sign ~")
    if kind is ast.BinOp:
        op = _ARITH.get(type(node.op))
        if op is None:
            raise _Unreadable("it does not know the sign %s" % _SIGNS.get(type(node.op), "there"))
        left, right = _build(node.left, used, depth + 1), _build(node.right, used, depth + 1)
        return lambda env: op(left(env), right(env))
    if kind is ast.BoolOp:
        parts = [_build(v, used, depth + 1) for v in node.values]
        if isinstance(node.op, ast.And):
            def both(env):
                value = 1
                for part in parts:
                    value = part(env)
                    if not value:
                        return value
                return value
            return both

        def either(env):
            value = 0
            for part in parts:
                value = part(env)
                if value:
                    return value
            return value
        return either
    if kind is ast.Compare:
        first = _build(node.left, used, depth + 1)
        ops = []
        for op, right in zip(node.ops, node.comparators):
            test = _COMPARE.get(type(op))
            if test is None:
                raise _Unreadable("it does not know 'in' or 'is'")
            ops.append((test, _build(right, used, depth + 1)))

        def compare(env):
            x = first(env)
            for test, right in ops:
                y = right(env)
                if not test(x, y):
                    return 0
                x = y
            return 1
        return compare
    if kind is ast.IfExp:
        test, yes, no = (_build(node.test, used, depth + 1), _build(node.body, used, depth + 1),
                         _build(node.orelse, used, depth + 1))
        return lambda env: yes(env) if test(env) else no(env)
    if kind is ast.Call:
        if not isinstance(node.func, ast.Name) or node.keywords:
            raise _Unreadable("it can only call its own few words, like gcd(a, b)")
        name = node.func.id
        if name not in _FUNCTIONS:
            raise _Unreadable("it does not know what %s() does" % name[:20])
        fewest, most, does = _FUNCTIONS[name]
        if not fewest <= len(node.args) <= most:
            raise _Unreadable("%s() is given the wrong number of things" % name)
        args = [_build(arg, used, depth + 1) for arg in node.args]
        used.add(name)
        return lambda env: does(env, *[arg(env) for arg in args])
    raise _Unreadable("it cannot read everything in its rule")


class Rule:
    """A rule that has been read: `make(env)` gives the next number."""

    def __init__(self, make, used):
        self.make = make
        self.used = used
        letters = [i + 1 for i, v in enumerate("abcd") if v in used]
        self.reach = max(letters) if letters else 0           # how many of the newest numbers it reads
        self.closed = not (used & {"n", "m", "seen", "term"})  # does its next number hang on its newest ones alone?


def _tidy(text) -> str:
    """A rule as a hand wrote it, made readable: '3a' -> 3*a, '^' -> **, a lone = -> ==, 'next = ' dropped."""
    text = str(text or "").strip().rstrip(".;")
    for this, that in (("×", "*"), ("·", "*"), ("÷", "/"), ("−", "-"), ("–", "-"),
                       ("≤", "<="), ("≥", ">="), ("≠", "!="), ("^", "**")):
        text = text.replace(this, that)
    text = re.sub(r"^\s*(?:the\s+)?(?:next(?:\s+number)?|new|term|x|an|a_n|a\s*\(\s*n\s*\))\s*(?:is|=)(?!=)\s*", "",
                  text, flags=re.I)
    text = re.sub(r"(?<![=!<>])=(?!=)", "==", text)
    text = re.sub(r"\bmod\b", "%", text)
    text = re.sub(r"(\d)\s*([abcdnm])(?![A-Za-z_])", r"\1*\2", text)
    text = re.sub(r"(\d)\s*\(", r"\1*(", text)
    return text.strip()


_rules = {}


def _rule(seed):
    """The seed's rule, read: (Rule, "") or (None, why it cannot be read)."""
    text = hands.line(seed, "rule", "")
    if text in _rules:
        return _rules[text]
    try:
        tidy = _tidy(text)
        if not tidy:
            raise _Unreadable("it has no rule")
        if len(tidy) > RULE_LONGEST:
            raise _Unreadable("its rule is too long to read")
        tree = ast.parse(tidy, mode="eval")
        if sum(1 for _ in ast.walk(tree)) > 160:
            raise _Unreadable("its rule is too long to read")
        used = set()
        found = (Rule(_build(tree.body, used), used), "")
    except _Unreadable as why:
        found = (None, str(why))
    except Exception:
        found = (None, "its rule is not written in a way it can read")
    if len(_rules) > 256:
        _rules.clear()
    _rules[text] = found
    return found


def _start(seed) -> list:
    """The numbers a recurrence starts from, as its seed gives them."""
    numbers = []
    for said in re.findall(r"[+-]?\d{1,7}", _ungrouped(hands.line(seed, "start", "")), re.ASCII):
        value = int(said)
        if abs(value) <= CAP:
            numbers.append(value)
        if len(numbers) >= START_MOST:
            break
    return numbers or [1]


def _next_number(rule, terms, ctx):
    """The rule's next number, or raises _TooBig / _NoNumber."""
    env = {"n": len(terms), "terms": terms, "m": 0}
    for i, name in enumerate("abcd"):
        env[name] = terms[-1 - i] if len(terms) > i else 0
    if "seen" in rule.used:
        env["seen"] = set(terms)
    if "m" in rule.used:
        env["m"] = _neighbour_number(ctx)
    try:
        value = rule.make(env)
    except (_TooBig, _NoNumber):
        raise
    except (RecursionError, MemoryError, OverflowError):
        raise _TooBig()
    except Exception:
        raise _NoNumber("its rule gave no number")
    return _held(value)


def _neighbour_number(ctx) -> int:
    """m: the newest number of the nearest other tally in the bed."""
    try:
        others = [nb for nb in ctx.neighbours if getattr(nb, "kind", "") == KIND]
    except Exception:
        return 0
    if not others:
        return 0
    nearest = min(others, key=lambda nb: (_num(getattr(nb, "distance", 9), 9), str(getattr(nb, "name", ""))))
    numbers = _numbers_of(getattr(nearest, "body", ""), getattr(nearest, "seed", {}), 1)
    return numbers[-1] if numbers else 0


def _numbers_of(body, seed, count, before=None) -> list:
    """A tally's newest `count` numbers, oldest first: a recurrence's newest numbers, a counter's newest months' counts.

    With `before` (a day), a counter gives only months it counted whole and that ended before that day,
    not the month still being counted (m, the neighbour's number, is given the month so far: it listens
    to the present; a cross's start is given whole months).
    """
    if not isinstance(seed, dict):
        seed = hands.read_keys(seed)
    way = _way_of(body, seed)
    led = _read(body, way)
    if way == "rule":
        return led.terms()[-count:] if count else []
    keys = led.month_keys()
    if before is not None:
        keys = [key for key in keys if key < _month_key(before) and _counted_whole(led, key)]
    return [led.month_count(month) for month in keys[-count:]] if count else []


# ================================================================= the body

_MONTH_LINE = re.compile(r"^(\d{4})-(\d{1,2})(?![\d-]):?\s*(.*)$", re.ASCII)    # a colon right after the month is a hand's
                                                                      # separator; one after a space is a broken stroke
_YEAR_LINE = re.compile(r"^(\d{4})\s*:\s*(\d{1,7})\b(.*)$", re.ASCII)
_GROUPED = re.compile(r"(?<![\d,])([+-]?\d{1,3}(?:,\d{3})+)(?![\d,])", re.ASCII)   # 1,242 as the almanac writes it


def _ungrouped(text) -> str:
    """Numbers written with commas between their thousands made whole: 'x1,242 9' -> 'x1242 9'."""
    return _GROUPED.sub(lambda found: found.group(1).replace(",", ""), str(text or ""))
_KEYED = re.compile(r"^(sap|last flowered|pages seen|moon|complete|asleep|counting since)\b\s*:?\s*(.*)$", re.I)
_TERM = re.compile(r"^[+-]?\d{1,7}$", re.ASCII)            # only the digits 0-9: int() would take others
_STRUCK = re.compile(r"^(?:[xX]+|~+)([+-]?\d{1,7})~*$", re.ASCII)
_ISO = re.compile(r"(\d{4})-(\d{1,2})-(\d{1,2})", re.ASCII)
MARKS = "|/\\:xX"


def _date_in(text):
    found = _ISO.search(str(text or ""))
    if not found:
        return None
    try:
        return Date(int(found.group(1)), int(found.group(2)), int(found.group(3)))
    except ValueError:
        return None


class Ledger:
    """A body, read. Months are [key 'YYYY-MM', [tokens]] in the order the body gives them."""

    def __init__(self):
        self.dead = ""
        self.months = []
        self.years = []          # [(year, total)] folded years of a counter
        self.sap = 0.0
        self.flowered = None
        self.pages = None
        self.moon = None
        self.complete = ""
        self.asleep = ""
        self.since = None
        self.remarks = []
        self.lines = 0           # lines it could read (a body with none is a plant cut to the ground)

    # ---- a recurrence

    def tokens(self):
        """(line index, token index, token) for every token of every month line, in order."""
        for i, (_, tokens) in enumerate(self.months):
            for j, token in enumerate(tokens):
                yield i, j, token

    def terms(self) -> list:
        return [int(token) for _, _, token in self.tokens() if _TERM.match(token) and abs(int(token)) <= CAP]

    def struck(self) -> list:
        found = []
        for _, _, token in self.tokens():
            hit = _STRUCK.match(token)
            if hit and abs(int(hit.group(1))) <= CAP:
                found.append(int(hit.group(1)))
        return found

    def lay(self, month, value) -> None:
        if not self.months or self.months[-1][0] != month:
            self.months.append([month, []])
        self.months[-1][1].append(str(value))

    def drop_newest(self):
        """Take the newest number off; returns it, or None if there was none."""
        for i in range(len(self.months) - 1, -1, -1):
            tokens = self.months[i][1]
            for j in range(len(tokens) - 1, -1, -1):
                if _TERM.match(tokens[j]):
                    value = tokens.pop(j)
                    if not tokens:
                        self.months.pop(i)
                    return int(value)
        return None

    # ---- a counter

    def month_keys(self) -> list:
        seen, keys = set(), []
        for key, _ in self.months:
            if key not in seen:
                seen.add(key)
                keys.append(key)
        return keys

    def month_groups(self, key) -> list:
        return [group for k, groups in self.months if k == key for group in groups]

    def month_count(self, key) -> int:
        return sum(_strokes(group) for group in self.month_groups(key))

    def line_for(self, key) -> list:
        """The groups of this month's last line, made if there is none (at the end)."""
        for k, groups in reversed(self.months):
            if k == key:
                return groups
        self.months.append([key, []])
        return self.months[-1][1]


def _strokes(group) -> int:
    """Strokes a group counts: | and : and the closing / (a struck x counts nothing)."""
    return sum(1 for ch in group if ch in "|:/\\")


def _bars(group) -> int:
    return sum(1 for ch in group if ch in "|:xX")


def _closed(group) -> bool:
    return "/" in group or "\\" in group or _bars(group) >= 5


def _read(body, way) -> Ledger:
    """A body as a Ledger. Reads what it can and never raises."""
    led = Ledger()
    try:
        text = str(body or "")
    except Exception:
        text = ""
    for raw in text.splitlines()[:6000]:
        line = raw.strip()
        if not line:
            continue
        if line.startswith(DAGGER):
            led.dead = led.dead or line[:200]
            continue
        if line.startswith("#"):
            if len(led.remarks) < REMARKS_MOST:
                led.remarks.append(line[:200])
            continue
        month = _MONTH_LINE.match(line)
        if month and 1 <= int(month.group(2)) <= 12:
            key = "%s-%02d" % (month.group(1), int(month.group(2)))
            rest = month.group(3)
            if way == "rule":
                tokens = [t for t in re.split(r"[\s,;]+", _ungrouped(rest)) if t][:MOST_NUMBERS + 50]
            else:
                tokens = ["".join(ch for ch in group if ch in MARKS)[:40] for group in rest.split()]
                tokens = [t for t in tokens if t][:40]
            led.months.append([key, tokens])
            led.lines += 1
            continue
        year = _YEAR_LINE.match(line)
        if year and way == "count":
            led.years.append((int(year.group(1)), int(year.group(2))))
            led.lines += 1
            continue
        keyed = _KEYED.match(line)
        if keyed:
            key, value = keyed.group(1).lower(), keyed.group(2).strip()
            led.lines += 1
            if key == "sap":
                led.sap = hands.num({"sap": value}, "sap", 0.0, 0.0, SAP_MOST)
            elif key == "last flowered":
                found = re.search(r"\d{4}", value, re.ASCII)
                led.flowered = int(found.group()) if found else None
            elif key == "pages seen":
                led.pages = int(hands.num({"p": value}, "p", 0, 0, 100000))
            elif key == "moon":
                led.moon = hands.num({"m": value}, "m", 0.0, 0.0, 1.0)
            elif key == "complete":
                led.complete = value[:200]
            elif key == "asleep":
                led.asleep = value[:200]
            elif key == "counting since":
                led.since = _date_in(value)
            continue
        if line.lower().startswith("a tally of"):
            led.lines += 1
    return led


def _write(led, way, seed) -> str:
    lines = [led.dead] if led.dead else []
    if way == "count":
        thing, phrase = _counts(seed)
        lines.append("a tally of %s" % (thing.many if thing else phrase))
        if led.since:
            lines.append("counting since %s" % led.since.isoformat())
        lines += ["%d: %d" % year for year in led.years]
        lines += [("%s  %s" % (key, " ".join(groups))).rstrip() for key, groups in led.months]
    else:
        lines.append("sap: %.2f" % led.sap)
        lines += [("%s  %s" % (key, " ".join(tokens))).rstrip() for key, tokens in led.months]
    if led.flowered:
        lines.append("last flowered: %d" % led.flowered)
    if led.pages is not None:
        lines.append("pages seen: %d" % led.pages)
    if led.moon is not None:
        lines.append("moon: %.3f" % led.moon)
    if led.complete:
        lines.append("complete: %s" % led.complete)
    if led.asleep:
        lines.append("asleep: %s" % led.asleep)
    lines += led.remarks
    return "\n".join(lines) + "\n"


def _way(seed) -> str:
    """What the seed asks for: 'rule' for a recurrence, 'count' for a counter."""
    return "rule" if hands.line(seed, "rule", "").strip() else "count"


_SAP_LINE = re.compile(r"^sap\b\s*:?", re.I)


def _body_way(body):
    """What a body has grown as: 'rule' (a row of numbers), 'count' (strokes), or None if it cannot tell.

    A 'sap' line says a recurrence and 'a tally of', 'counting since' or a folded year say a counter, whichever
    comes first; else the month lines are weighed, digits against strokes. An empty body tells nothing.
    """
    digits = strokes = 0
    try:
        lines = str(body or "").splitlines()[:6000]
    except Exception:
        return None
    for raw in lines:
        line = raw.strip()
        low = line.lower()
        if not line or line.startswith(("#", DAGGER)):
            continue
        if _SAP_LINE.match(line):
            return "rule"
        if low.startswith(("a tally of", "counting since")) or _YEAR_LINE.match(line):
            return "count"
        month = _MONTH_LINE.match(line)
        if month:
            rest = month.group(3)
            digits += sum(1 for ch in rest if "0" <= ch <= "9")
            strokes += sum(1 for ch in rest if ch in "|/\\")
    if digits > strokes:
        return "rule"
    if strokes > digits:
        return "count"
    return None


def _way_of(body, seed) -> str:
    """The way a grown tally is read: as its body has grown, else as its seed asks."""
    return _body_way(body) or _way(seed)


def _month_key(day) -> str:
    return "%04d-%02d" % (day.year, day.month)


ENDING = 4                 # newest numbers a complete line keeps, to know a hand's change
_ENDING = re.compile(r"ending\s+((?:[+-]?\d{1,7}\s*)+)$", re.ASCII)


def _completion(led):
    """(the day it came, how many numbers it had then, its newest numbers then or None) if the body says it is
    complete, else None."""
    if not led.complete:
        return None
    when = _date_in(led.complete)
    count = re.search(r"at (\d+) numbers?", led.complete, re.ASCII)
    if when is None or count is None:
        return None
    ending = _ENDING.search(led.complete.strip())
    return when, int(count.group(1)), tuple(int(v) for v in ending.group(1).split()) if ending else None


def _complete_still(led, terms):
    """The completion, if it still holds: the body has the numbers it had when it came (else a hand has cut or
    changed it, and it grows again)."""
    done = _completion(led)
    if done is None or done[1] != len(terms):
        return None
    if done[2] is not None and tuple(terms[-len(done[2]):]) != done[2]:
        return None
    return done


def _complete_line(day, why, terms) -> str:
    return "%s, %s, at %d numbers, ending %s" % (day.isoformat(), why, len(terms),
                                                 " ".join(str(v) for v in terms[-ENDING:]))


def _ordinal(n) -> str:
    return "%d%s" % (n, "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


def _spoken(value) -> str:
    """A number as the almanac writes it: 1,242."""
    return "{:,}".format(value)


# ================================================================= growth

def _trait(seed, key, choices) -> str:
    return hands.word(seed, key, "", choices)


def _seasons(seed) -> set:
    said = _plain(hands.line(seed, "flowers", ""))
    if "all" in said or "year" in said:
        return set(SEASONS)
    found = {s for s in SEASONS if s in said}
    for french, english in (("printemps", "spring"), ("ete", "summer"), ("automne", "autumn"), ("hiver", "winter")):
        if french in said:
            found.add(english)
    return found or {"spring", "summer"}


def _flower_weather(seed, sky) -> bool:
    """Is it a day a tally can hold flowers open: not frozen, and not dry ground (unless its leaf is made for it)?"""
    leaf = _trait(seed, "leaf", ("waxy", "downy"))
    if sky.tmin < (-4.0 if leaf == "downy" else 0.0):
        return False
    return leaf == "waxy" or _num(sky.wet) >= 0.1


def _sap_today(sky, seed, bed) -> float:
    """What a recurrence gathers today from its bed's sky."""
    leaf = _trait(seed, "leaf", ("waxy", "downy"))
    if sky.tmin < (-4.0 if leaf == "downy" else 0.0):
        return 0.0
    warm = min(1.0, max(0.0, _num(sky.warmth)) / 10.0)
    light = min(1.0, max(0.0, _num(sky.light)) / 8.0)
    water = 0.25 + 0.75 * min(1.0, max(0.0, _num(sky.wet)) / 0.4)
    if leaf == "waxy":
        water = max(water, 0.9)
    rich = hands.num(bed or {}, "rich", 0.0, 0.0, 1.0)
    return 1.3 * warm * light * water * (1.0 + 0.6 * rich)


def _snaps(seed, sky, ctx) -> bool:
    """Does the wind snap a brittle tally today? One chance in seven at force 5 in its bed, a fifth more for each force above."""
    if _trait(seed, "stem", ("brittle", "thorny")) != "brittle" or _num(sky.wind) < 5:
        return False
    return ctx.rng.random() < min(1.0, 0.15 + 0.2 * (_num(sky.wind) - 5))


def _cost(value) -> float:
    return 0.8 + 0.2 * len(str(abs(value)))


def _open_flowers(led, seed, ctx, way) -> list:
    """What is in flower today: a recurrence's prime numbers among its newest five; a counter's closed, unbitten gates this month."""
    try:
        sky = ctx.sky
        if led.dead or led.asleep or sky.season not in _seasons(seed) or not _flower_weather(seed, sky):
            return []                                     # (a plant asleep over a rule it cannot read does not flower)
        if _num(getattr(ctx, "age", FLOWERS_FROM), FLOWERS_FROM) < FLOWERS_FROM:
            return []                                     # a seedling does not flower in its first two months
    except Exception:
        return []
    if way == "rule":
        found = []
        for value in led.terms()[-5:]:
            if value not in found and _isprime(value):
                found.append(value)
        return found
    return [g for g in led.month_groups(_month_key(ctx.date)) if _closed(g) and ":" not in g and "x" not in g.lower()]


def _came_round(terms, reach):
    """If the newest `reach` numbers stood in that order before, the numbers of the round; else None."""
    reach = max(1, reach)
    if len(terms) <= reach:
        return None
    newest = tuple(terms[-reach:])
    for i in range(len(terms) - reach - 1, -1, -1):
        if tuple(terms[i:i + reach]) == newest:
            return terms[i + reach - 1:len(terms) - 1] if reach == 1 else terms[i:len(terms) - reach]
    return None


def _grow_rule(led, seed, ctx) -> list:
    """One day of a recurrence. Returns its events."""
    events, day, sky = [], ctx.date, ctx.sky
    rule, why = _rule(seed)
    stepping = _steps(seed)
    moon_before = led.moon
    turned = stepping.test(sky, ctx, led) if stepping is not None else 1
    if _needs_moon(stepping) or moon_before is not None:
        led.moon = _num(getattr(sky, "moon", 0.0)) % 1.0
    if rule is None:
        if led.asleep != why:
            led.asleep = why
            events.append("sleeps: " + why)
        return events
    if led.asleep:
        led.asleep = ""
        events.append("woke: its rule can be read")
    terms = led.terms()
    if not terms:                                         # every number cut or struck: it comes up from its start
        for value in _start(seed):
            led.lay(_month_key(day), value)
        led.complete = ""
        return events + ["came up again from its start"]
    done = _complete_still(led, terms)
    if led.complete and done is None:
        led.complete = ""                                 # a hand cut it back, or changed it: it grows again
    led.sap = min(SAP_MOST, led.sap + _sap_today(sky, seed, getattr(ctx, "bed", {})))
    if done:
        if (day - done[0]).days >= SPENT_AFTER:
            led.dead = "%s %s, spent, after %d numbers" % (DAGGER, day.isoformat(), len(terms))
            return events + ["died back, spent, after %d numbers" % len(terms)]
        return events
    if _snaps(seed, sky, ctx) and len(terms) > len(_start(seed)):
        lost = led.drop_newest()                          # a windy day is a lost day: what snaps grows again later
        if lost is not None:
            events.append("the wind snapped off its newest number, %s" % _spoken(lost))
            return events
    if turned and led.sap >= 1.0:
        _step(led, rule, terms, ctx, events)
    return events


def _step(led, rule, terms, ctx, events) -> None:
    """Try to lay one number."""
    day = ctx.date
    try:
        value = _next_number(rule, terms, ctx)
    except _TooBig:
        value = None
        why = "reached its height"
    except _NoNumber as error:
        value = None
        why = "its rule gave no number: %s" % error
    else:
        why = "reached its height" if abs(value) > CAP else ""
    if why:
        led.complete = _complete_line(day, why, terms)
        events.append(why if why != "reached its height" else
                      "reached its height: the next number would have more than six digits")
        return
    cost = _cost(value)
    if led.sap < cost:
        return
    led.sap -= cost
    led.lay(_month_key(day), value)
    terms.append(value)
    if len(terms) in MILESTONES:
        events.append("its %s number: %s" % (_ordinal(len(terms)), _spoken(value)))
    round_ = _came_round(terms, rule.reach) if rule.closed else None
    if round_:
        shown = ", ".join(_spoken(v) for v in round_) if len(round_) <= 6 else "a round of %d numbers" % len(round_)
        led.complete = _complete_line(day, "came round: %s" % shown, terms)
        events.append("came round: %s" % shown)
    elif len(terms) >= MOST_NUMBERS:
        led.complete = _complete_line(day, "full grown", terms)
        events.append("full grown, at %s numbers" % _spoken(len(terms)))


def _grow_count(led, seed, ctx) -> list:
    """One day of a counter. Returns its events."""
    events, day, sky = [], ctx.date, ctx.sky
    ended = _count_ends(led, ctx)
    if ended:
        return [ended]
    thing, phrase = _counts(seed)
    if thing is None:
        why = "it does not know how to count %s" % phrase
        if led.asleep != why:
            led.asleep = why
            events.append("sleeps: " + why)
        return events
    if led.asleep:
        led.asleep = ""
        events.append("woke: it knows what to count")
    said = [_month_said(led, thing, day)] if day.day == 1 else []
    groups = led.line_for(_month_key(day))
    strokes = max(0, min(int(thing.test(sky, ctx, led)), 31))
    if _needs_moon(thing):
        led.moon = _num(getattr(sky, "moon", 0.0)) % 1.0
    for _ in range(strokes):
        if groups and not _closed(groups[-1]):
            groups[-1] += "/" if _bars(groups[-1]) >= 4 else "|"
        else:
            groups.append("|")
    said.append(_first_since(led, thing, day, strokes))
    said = [line for line in said if line]
    if said and not _elder_in_bed(led, thing, ctx):
        events += said
    if _snaps(seed, sky, ctx):
        if _break(groups, 1):
            events.append("the wind broke one of its strokes")
    _fold(led)
    return events


def _month_start(key):
    """The first day of a month key 'YYYY-MM', or None for one no calendar has (a hand may write year 0000)."""
    try:
        return Date(int(key[:4]), int(key[5:7]), 1)
    except (ValueError, TypeError):
        return None


def _record_begun(led):
    """The first day of a counter's record: its 'counting since', else its oldest month or folded year."""
    if led.since:
        return led.since
    found = [start for start in (_month_start(key) for key, _ in led.months) if start]
    found += [Date(year, 1, 1) for year, _ in led.years if 1 <= year <= 9999]
    return min(found) if found else None


def _count_ends(led, ctx) -> str:
    """A counter's end: in a winter after its sixth year of counting, now and then, it dies back. Its event, or ''."""
    begun = _record_begun(led)
    if begun is None or getattr(ctx.sky, "season", "") != "winter":
        return ""
    years = (ctx.date - begun).days // 365
    if years < COUNT_YEARS or ctx.rng.random() >= WINTER_END:
        return ""
    total = sum(led.month_count(key) for key in led.month_keys()) + sum(t for _, t in led.years)
    led.dead = "%s %s, done counting, after %d years and %s strokes" % (DAGGER, ctx.date.isoformat(), years,
                                                                        _spoken(total))
    return "died back, done counting, after %d years" % years


def _counted_whole(led, key) -> bool:
    """Was this month counted from its first day? (The month a counter was sown in may not have been.)"""
    start = _month_start(key)
    return start is not None and (led.since is None or led.since <= start)


def _month_said(led, thing, day):
    """What a counter tells the almanac on the first of a month about the month gone, if it is worth telling; else None.

    Only what its own record makes new: a month with none where every earlier year's same month had some (two
    earlier years at least); a month with more than any before it, once it has a year of record; for the moon, a
    month without one, or with two.
    """
    gone = day - timedelta(days=1)
    key = _month_key(gone)
    if thing.name == "days" or key not in led.month_keys() or not _counted_whole(led, key):
        return None
    total, month = led.month_count(key), MONTHS[gone.month - 1]
    if thing.name in ("full moons", "new moons"):
        if total == 1:
            return None
        return "counted %s in %s" % (thing.words(total) if total else "no " + thing.one, month)
    earlier = [k for k in led.month_keys() if k < key and _counted_whole(led, k)]
    same = [led.month_count(k) for k in earlier if k[5:] == key[5:]]
    if total == 0 and len(same) >= 2 and min(same) > 0:
        return "counted no %s in %s, the first %s without" % (thing.many, month, month)
    if total and len(earlier) >= 12 and total > max(led.month_count(k) for k in earlier):
        return "counted %s in %s, more than in any month before" % (thing.words(total), month)
    return None


def _first_since(led, thing, day, laid):
    """'counted its first frost since March', when today's strokes are the first after two whole months of none."""
    if laid <= 0 or thing.name in ("days", "full moons", "new moons"):
        return None
    key = _month_key(day)
    if led.month_count(key) != laid:
        return None                                       # not the first of this month
    first = day.replace(day=1)
    prev1 = _month_key(first - timedelta(days=1))
    prev2 = _month_key((first - timedelta(days=1)).replace(day=1) - timedelta(days=1))
    keys = led.month_keys()
    if prev1 not in keys or prev2 not in keys or led.month_count(prev1) or led.month_count(prev2):
        return None
    last = max((k for k in keys if k < prev2 and led.month_count(k) > 0), default=None)
    if last is None:
        return "counted its first %s" % thing.one
    year, month = int(last[:4]), int(last[5:])
    ago = (day.year - year) * 12 + day.month - month
    return "counted its first %s since %s" % (thing.one, MONTHS[month - 1] if ago < 12 else
                                               "%s %d" % (MONTHS[month - 1], year))


def _elder_in_bed(led, thing, ctx) -> bool:
    """Is there an older counter of the same thing in this bed? Then it speaks for the bed's month, and this one keeps quiet.

    Two counters of wet days in one bed count the same days; the almanac
    needs to hear it once.
    """
    mine = (led.since or Date(9999, 1, 1), str(getattr(ctx, "name", "")))
    try:
        others = list(ctx.neighbours)
    except Exception:
        return False
    for other in others:
        if getattr(other, "kind", "") != KIND:
            continue
        seed = other.seed if isinstance(getattr(other, "seed", None), dict) else hands.read_keys(getattr(other, "seed", ""))
        if _way_of(getattr(other, "body", ""), seed) != "count" or hands.is_dead(getattr(other, "body", "")):
            continue
        theirs, _ = _counts(seed)
        if theirs is None or theirs.name != thing.name:
            continue
        since = _read(getattr(other, "body", ""), "count").since or Date(9999, 1, 1)
        if (since, str(getattr(other, "name", ""))) < mine:
            return True
    return False


def _break(groups, count) -> int:
    """Break the newest whole strokes of a month into bitten ones (:). Returns how many."""
    broken = 0
    for g in range(len(groups) - 1, -1, -1):
        chars = list(groups[g])
        for i in range(len(chars) - 1, -1, -1):
            if broken >= count:
                break
            if chars[i] == "|":
                chars[i] = ":"
                broken += 1
        groups[g] = "".join(chars)
        if broken >= count:
            break
    return broken


def _fold(led) -> None:
    """Fold the oldest years of a counter into one line each, keeping KEPT_YEARS month by month."""
    years = sorted({int(key[:4]) for key, _ in led.months})
    while len(years) > KEPT_YEARS:
        oldest = years.pop(0)
        total = sum(_strokes(g) for key, groups in led.months if int(key[:4]) == oldest for g in groups)
        led.years.append((oldest, total))
        led.months = [m for m in led.months if int(m[0][:4]) != oldest]


# ================================================================= what the ground calls

def sprout(seed, ctx) -> str:
    """The body on the day it is sown."""
    way = _way(seed)
    led = Ledger()
    if way == "count":
        led.since = ctx.date + timedelta(days=1)
        thing, _ = _counts(seed)
        if thing is not None and thing.name == "book pages":
            led.pages = _pages(ctx)
        if _needs_moon(thing):
            led.moon = _num(getattr(ctx.sky, "moon", 0.0)) % 1.0
    else:
        led.months.append([_month_key(ctx.date), [str(v) for v in _start(seed)]])
        stepping = _steps(seed)
        if stepping is not None and stepping.name == "book pages":
            led.pages = _pages(ctx)
        if _needs_moon(stepping):
            led.moon = _num(getattr(ctx.sky, "moon", 0.0)) % 1.0
    return _write(led, way, seed)


_ASLEEP_LINE = re.compile(r"^\s*asleep\b", re.I)


def _asleep_as_it_stands(body, grown, seed):
    """A tally whose seed asks for the other way than its body has grown: it sleeps, and its body stays as it stands.

    (Before this, a recurrence whose seed lost its rule was rewritten as a counter the same day and every number
    was lost. Now nothing is lost: mend the seed and it wakes.)
    """
    if grown == "rule":
        asks_count = hands.line(seed, "counts", "") or hands.line(seed, "count", "")
        why = ("its seed asks it to count, but it has grown as a row of numbers" if asks_count
               else "its seed has lost its rule")
    else:
        why = "its seed has a rule, but it has grown as a count"
    if _read(body, grown).asleep == why:
        return body, None
    kept = [line for line in str(body).splitlines() if not _ASLEEP_LINE.match(line)]
    while kept and not kept[-1].strip():
        kept.pop()
    return "\n".join(kept + ["asleep: " + why]) + "\n", "sleeps: " + why


def day(body, seed, ctx):
    """One day: the new body, and an event line or None."""
    if hands.is_dead(body):
        return body, None
    way = _way_of(body, seed)
    if way != _way(seed):
        return _asleep_as_it_stands(body, way, seed)
    led = _read(body, way)
    if not str(body or "").strip() or led.lines == 0:
        again = sprout(seed, ctx) + "".join(remark + "\n" for remark in led.remarks)    # a visitor's remarks stay
        return again, ("came up again from the seed" if way == "rule" else "came up again: the count begins again")
    events = _grow_rule(led, seed, ctx) if way == "rule" else _grow_count(led, seed, ctx)
    if not led.dead:
        opened = _open_flowers(led, seed, ctx, way)
        if opened and led.flowered != ctx.date.year:
            led.flowered = ctx.date.year
            if way == "rule":
                events.append("came into flower on %s" % ", ".join(_spoken(v) for v in opened[:4]))
            else:
                events.append("came into flower")
    return _write(led, way, seed), ("; ".join(events) if events else None)


def flowers(body, seed, ctx) -> int:
    """How many flowers are open today."""
    if hands.is_dead(body):
        return 0
    way = _way_of(body, seed)
    return len(_open_flowers(_read(body, way), seed, ctx, way))


def bitten(body, seed, ctx, share, by):
    """The body after a bite of `share` of what is soft, and an event line.

    Only a bite that costs something a visitor can see is told: a recurrence's newest number lost, or a counter's
    gate in flower broken. A bite of sap alone, or of strokes that were not in flower, changes the body quietly
    (the sap line, the : marks), so that the almanac does not become a log of nibbles.
    """
    if hands.is_dead(body):
        return body, None
    share = hands.num({"s": share}, "s", 0.0, 0.0, 1.0)
    if _trait(seed, "stem", ("brittle", "thorny")) == "thorny":
        share /= 3.0
    by = " ".join(str(by or "something").split())[:40] or "something"
    way = _way_of(body, seed)
    if way != _way(seed):
        return body, None                                 # asleep over its seed: nothing soft to take
    led = _read(body, way)
    if way == "count":
        was_open = len(_open_flowers(led, seed, ctx, way))
        groups = led.line_for(_month_key(ctx.date))
        whole = sum(g.count("|") for g in groups)
        broken = _break(groups, int(round(share * whole)))
        if not broken:
            return body, None
        spoiled = was_open - len(_open_flowers(led, seed, ctx, way))
        said = None
        if spoiled > 0:
            said = "bitten by %s: %s in flower broken" % (by, "a gate" if spoiled == 1 else "%d gates" % spoiled)
        return _write(led, way, seed), said
    taken = led.sap * share
    led.sap -= taken
    tip = None
    if share >= 0.3 and not led.complete and len(led.terms()) > len(_start(seed)):
        tip = led.drop_newest()
    if tip is None:
        return (body, None) if taken < 0.005 else (_write(led, way, seed), None)
    return _write(led, way, seed), "bitten by %s: it lost its newest number, %s" % (by, _spoken(tip))


def cast(body, seed, ctx) -> list:
    """Seed dropped today: now and then a cross, if pollen was carried to it; else, now and then, its own."""
    if hands.is_dead(body):
        return []
    way = _way_of(body, seed)
    if way != _way(seed):
        return []
    led = _read(body, way)
    opened = _open_flowers(led, seed, ctx, way)
    if not opened or _num(getattr(ctx, "age", SEEDS_FROM), SEEDS_FROM) < SEEDS_FROM:
        return []
    rng = ctx.rng
    pollen = []
    for grain in list(getattr(ctx, "pollen", None) or [])[:40]:
        donor = getattr(grain, "seed", None)
        donor = donor if isinstance(donor, dict) else hands.read_keys(donor)
        if hands.word(donor, "kind", "") == KIND and getattr(grain, "where", "") != getattr(ctx, "where", ""):
            pollen.append((grain, donor))
    if pollen and rng.random() < min(0.1, CROSSED * len(opened)):
        grain, donor = pollen[rng.randrange(len(pollen))]
        return [_crossed(led, seed, ctx, way, opened, grain, donor)]
    if rng.random() >= min(0.02, OWN_SEED * len(opened)):     # a flower that was visited still sets some of its own
        return []
    return [_own_seed(led, seed, ctx, way, opened)]


def _kept(seed) -> dict:
    return {key: hands.line(seed, key, "") for key in KEPT if hands.line(seed, key, "")}


def _flower_start(led, seed, flower) -> list:
    """The numbers a seed set on `flower` starts from: that number, and the ones before it that the rule reads."""
    terms = led.terms()
    rule, _ = _rule(seed)
    reach = max(1, rule.reach if rule else 1)
    if flower not in terms:
        return _start(seed)
    at = len(terms) - 1 - terms[::-1].index(flower)
    return terms[max(0, at - reach + 1):at + 1]


def _own_seed(led, seed, ctx, way, opened) -> str:
    child = _kept(seed)
    child["kind"] = KIND
    if way == "rule":
        flower = opened[ctx.rng.randrange(len(opened))]
        child["start"] = ", ".join(str(v) for v in _flower_start(led, seed, flower))
        stem = re.sub(r"(-(\d+|[ivxlc]+|seedling))+$", "", str(getattr(ctx, "name", "") or "tally")) or "tally"
        child["name"] = "%s-%d" % (stem[:40], flower)
    return hands.write_keys(child)


def _crossed(led, seed, ctx, way, opened, grain, donor) -> str:
    """A cross of this tally (the seed-bearer) with the one whose pollen was carried."""
    rng = ctx.rng
    mine, theirs = _kept(seed), _kept(donor)
    child = {"kind": KIND}
    their_where = str(getattr(grain, "where", "") or "another tally")
    their_body = None
    their_bed, _, their_name = their_where.replace("\\", "/").rpartition("/")
    my_bed = str(getattr(ctx, "where", "") or "").replace("\\", "/").rpartition("/")[0]
    if their_bed and their_bed == my_bed:                 # only a neighbour's body can be read; pollen from another
        try:                                              # bed brings the seed's words and not the body
            for nb in ctx.neighbours:
                if getattr(nb, "name", None) == their_name and getattr(nb, "kind", "") == KIND:
                    their_body = getattr(nb, "body", None)
        except Exception:
            pass
    if mine.get("rule") or theirs.get("rule"):
        mother_rules = bool(mine.get("rule"))
        child["rule"] = mine["rule"] if mother_rules else theirs["rule"]
        rule, _ = _rule(child)
        reach = max(1, rule.reach if rule else 1)
        if mother_rules:                                   # the numbers come from the other parent
            if their_body is not None:
                numbers = _numbers_of(their_body, donor, reach, before=ctx.date)
            elif theirs.get("rule"):
                numbers = _start(donor)
            else:
                numbers = []                               # a counter in another bed: its months are not to be read
            numbers = numbers or _flower_start(led, seed, opened[0])
        else:                                              # this counter's newest whole months give the numbers
            whole = [key for key in led.month_keys() if key < _month_key(ctx.date) and _counted_whole(led, key)]
            numbers = [led.month_count(key) for key in whole[-reach:]] or [1]
        child["start"] = ", ".join(str(v) for v in numbers[-START_MOST:])
        temperaments = [x for x in (mine.get("steps") or mine.get("counts"), theirs.get("steps") or theirs.get("counts")) if x]
        if temperaments:
            child["steps"] = temperaments[rng.randrange(len(temperaments))]
    else:
        choices = [x for x in (mine.get("counts"), theirs.get("counts")) if x]
        if choices:
            child["counts"] = choices[rng.randrange(len(choices))]
    for key in ("flowers", "leaf", "stem", "scent"):
        choices = [x for x in (mine.get(key), theirs.get(key)) if x is not None]
        pick = (mine.get(key), theirs.get(key))[rng.randrange(2)]
        if pick:
            child[key] = pick
        elif choices and key == "flowers":
            child[key] = choices[0]
    child["colour"] = hands.mix(_colour(seed), _colour(donor), 0.5)
    child["from"] = "cross of %s %s %s" % (getattr(ctx, "where", "a tally"), CROSS, their_where)
    return hands.write_keys(child)


INK_NAMES = ("red", "dark-red", "pink", "pale-pink", "orange", "yellow", "blue", "violet", "brown", "white", "black", "grey")
INK_WORDS = {"gray": "grey", "purple": "violet", "rouge": "red", "rose": "pink", "bleu": "blue", "jaune": "yellow",
             "blanc": "white", "blanche": "white", "brun": "brown", "marron": "brown", "noir": "black", "gris": "grey"}


def _colour(seed) -> str:
    """The ink of its flowers, read loosely: '#b03060', 'dark red', 'pale pink, like an astrance', 'rose'."""
    said = _plain(hands.line(seed, "colour", "") or hands.line(seed, "color", ""))
    found = re.search(r"#[0-9a-f]{6}\b", said)
    if found:
        return found.group()
    words = [INK_WORDS.get(w, w) for w in re.findall(r"[a-z]+", said)]
    for first, second in zip(words, words[1:]):
        if first + "-" + second in INK_NAMES:
            return first + "-" + second
    for w in words:
        if w in INK_NAMES:
            return w
    return DEFAULT_COLOUR


def describe(body, seed, ctx) -> str:
    """One short line. Like the plate, it does not say what a counter counts, nor a recurrence's rule: the seed does."""
    way = _way_of(body, seed)
    led = _read(body, way)
    if led.dead:
        return led.dead.lstrip(DAGGER).strip()
    if led.asleep:
        return "asleep: " + led.asleep
    if way == "count":
        total = sum(led.month_count(k) for k in led.month_keys()) + sum(t for _, t in led.years)
        now = led.month_count(_month_key(ctx.date)) if _month_key(ctx.date) in led.month_keys() else 0
        text = "%s counted, %d this month" % (_spoken(total), now)
    else:
        terms = led.terms()
        text = "%d number%s, the newest %s" % (len(terms), "" if len(terms) == 1 else "s",
                                             _spoken(terms[-1]) if terms else "none")
        if _complete_still(led, terms):
            text += "; complete"
    if _open_flowers(led, seed, ctx, way):
        text += "; in flower"
    return text


def size(body, seed) -> float:
    """For its dot on the plan: its numbers, or its strokes, six to a unit (about a line of them)."""
    way = _way_of(body, seed)
    led = _read(body, way)
    if way == "count":
        return (sum(led.month_count(k) for k in led.month_keys()) + sum(t for _, t in led.years)) / 6.0
    return len(led.terms()) / 6.0


# ================================================================= the plate

def draw(body, seed, ctx, pen) -> None:
    """The plate: a counter's calendar, or a recurrence's number line with its arcs and its stair."""
    way = _way_of(body, seed)
    led = _read(body, way)
    dead = bool(led.dead) or hands.is_dead(body)
    left = None if ctx.left is None else _read(ctx.left, way)
    if way == "rule":
        _draw_rule(led, seed, ctx, pen, dead, left)
    else:
        _draw_count(led, seed, ctx, pen, dead, left)


_RHYTHM = (1.0, 0.62, 1.38, 0.8, 1.2, 0.7, 1.3)    # uneven, so that texture marks are not read as a scale


def _uneven(x1, x2, count) -> list:
    """`count` stretches of x1..x2, of uneven lengths in a fixed rhythm: [(start, end), ...]."""
    gaps = [_RHYTHM[i % len(_RHYTHM)] for i in range(count)]
    total, at, out = sum(gaps), 0.0, []
    for gap in gaps:
        out.append((x1 + at / total * (x2 - x1), x1 + (at + gap) / total * (x2 - x1)))
        at += gap
    return out


def _texture(pen, seed, x1, x2, y, size, ink, weight=3.0) -> None:
    """The line a tally stands on, from x1 to x2 at height y, with the texture of its traits.

    waxy: doubled · downy: stippled beneath · brittle: broken · thorny: thorns, pointing down.
    `size` is a small length in plant units, about 9 px on the plate (a thorn's reach, the doubling's gap).
    The marks come in an uneven rhythm, so that no one takes them for the ticks of a scale.
    """
    leaf = _trait(seed, "leaf", ("waxy", "downy"))
    stem = _trait(seed, "stem", ("brittle", "thorny"))
    length = x2 - x1
    if length <= 0 or not size > 0:
        return
    if stem == "brittle":
        for a, b in _uneven(x1, x2, max(2, min(40, int(length / (size * 5)) or 2))):
            pen.line(a, y, a + 0.72 * (b - a), y, weight, ink)
    else:
        pen.line(x1, y, x2, y, weight, ink)
    if leaf == "waxy":
        pen.line(x1, y - size * 0.7, x2, y - size * 0.7, max(2.0, weight - 1), ink)
    if leaf == "downy":
        for i, (a, b) in enumerate(_uneven(x1, x2, max(3, min(60, int(length / (size * 2.5)))))):
            pen.dot((a + b) / 2, y - size * (0.8 if i % 2 else 1.4), 3, ink)
    if stem == "thorny":                                  # a thorn: a short spike, broad at the line, leaning
        for a, b in _uneven(x1, x2, max(2, min(40, int(length / (size * 4))))):
            x = (a + b) / 2
            pen.polyline([(x - size * 0.35, y), (x + size * 0.3, y - size * 1.25), (x + size * 0.35, y)], 2.0, ink,
                         closed=True)


# ---- a recurrence

def _draw_rule(led, seed, ctx, pen, dead, left) -> None:
    pen.unit_name = "along the line"
    terms, struck = led.terms(), led.struck()
    wood = "dead" if dead else "wood"
    if not terms:
        pen.dot(0, 0, 6, wood, filled=False)
        pen.note("no numbers: " + (led.asleep or "it has been cut to the ground"))
        return
    was = left.terms() if left is not None else []
    same = 0
    while same < min(len(was), len(terms)) and was[same] == terms[same]:
        same += 1
    fresh_from = same if left is not None else 0          # numbers from this place on are new since the last visit
    ink = lambda i: wood if dead or i < fresh_from else "fresh"

    low, high = min(terms + struck), max(terms + struck)
    lo, hi = min(0, low), max(0, high)
    cut = ""                                              # a line that does not reach 0: which end was cut
    if 0 < low < high and high - low < high / 3:
        lo, cut = low, "left"                             # numbers in a narrow band far above 0
    elif low < high < 0 and high - low < -low / 3:
        hi, cut = high, "right"                           # ... or far below it
    span = max(1, hi - lo)
    above = below = 0.0
    arc_weight = 3.0 if len(terms) <= 40 else 2.5 if len(terms) <= 150 else 2.0
    first_arc = max(1, len(terms) - ARCS_MOST)             # older steps are left to the strokes below
    for i in range(first_arc, len(terms)):
        x1, x2 = terms[i - 1], terms[i]
        r = abs(x2 - x1) / 2.0
        if r == 0:
            pen.dot(x1, 0, 7, ink(i), filled=False, weight=2.5)
        elif i % 2:
            pen.arc((x1 + x2) / 2.0, 0, r, 0, 180, arc_weight, ink(i))
            above = max(above, r)
        else:
            pen.arc((x1 + x2) / 2.0, 0, r, 180, 360, arc_weight, ink(i))
            below = max(below, r)

    small = span * 0.012                                  # a small length on this plate, in numbers
    old_lo, old_hi = (min(0, min(was)), max(0, max(was))) if was and not dead else (lo, hi)
    old_lo, old_hi = max(lo, old_lo), min(hi, old_hi)
    if left is None and not dead:
        old_lo = old_hi = max(lo, min(hi, 0))
    if old_lo < old_hi:
        _texture(pen, seed, old_lo, old_hi, 0, small, wood)
    if lo < old_lo:
        _texture(pen, seed, lo, old_lo, 0, small, "fresh")
    if old_hi < hi:
        _texture(pen, seed, old_hi, hi, 0, small, "fresh")
    gap = small * 3.2 if cut == "left" else small           # room for the break before the lowest number
    pen.label(lo - gap, -small * 1.2, _spoken(lo), 14, "ink", "end")
    pen.label(hi + (small * 3.2 if cut == "right" else small), -small * 1.2, _spoken(hi), 14, "ink", "start")
    if cut:                                               # the break: two short slants, the line does not reach 0
        end, away = (lo, -1) if cut == "left" else (hi, 1)
        for step in (1.0, 2.1):
            x = end + away * small * step
            pen.line(x - small * 0.45, -small * 1.3, x + small * 0.45, small * 1.3, 2.5, wood)
    if lo < 0 < hi:
        pen.line(0, -small * 1.5, 0, small * 1.5, 2.5, wood)

    for value in struck:
        pen.line(value - small, -small, value + small, small, 2.5, "dead")
        pen.line(value - small, small, value + small, -small, 2.5, "dead")

    count = len(terms)
    top = -(below + span * 0.08)
    fall = min(0.5 * span, count * span / 12.0)           # how far the column of strokes falls, in plate units
    tread = fall / count
    # About how many pixels a unit will be once the plate is fitted into its box (774 x 844 px inside the inset,
    # less room for the end labels, the heading and the newest number): for sizing the strokes only.
    guess = min(60.0, 684.0 / span, 794.0 / (above + below + span * 0.195 + fall))
    tread_px = tread * guess
    weight = 2.5 if tread_px >= 6 else 2.0
    # A stroke is 0.8 of its tread, but short enough that it and the next one do not touch (a pen's round ends
    # reach half its weight beyond); once the treads are small it shrinks to a dot, one for each number still.
    stroke = max(0.0, min(0.8 * tread_px, tread_px - weight - 1.0)) / guess
    for i, value in enumerate(terms):
        y = top - i * tread
        pen.line(value, y, value, y - stroke, weight, ink(i))
    foot = top - (count - 1) * tread - stroke - 4.0 / guess
    done = _complete_still(led, terms)                    # a complete plant a hand has since cut is growing again
    if done:
        pen.line(terms[-1] - span * 0.03, foot, terms[-1] + span * 0.03, foot, 5, wood)
    pen.label(terms[-1], foot - span * 0.045, _spoken(terms[-1]), 16, "ink", "middle")

    heading = " ".join(str(v) for v in terms[:8]) + (" " + ELLIPSIS if count > 8 else "")
    pen.label(lo, above + span * 0.07, heading, 18, "ink", "start")

    opened = [] if dead else _open_flowers(led, seed, ctx, "rule")
    for value in opened:                                  # a flower on a short stalk above its number, ringed, so
        pen.line(value, small * 0.4, value, small * 2.6, 2.0, wood)   # that it hides no arc and a white one is
        pen.dot(value, small * 2.6, 7.5, _colour(seed))               # not taken for a ring on the line
        pen.dot(value, small * 2.6, 7.5, wood, filled=False, weight=2.0)

    pen.note("%d number%s%s; the newest %s, the highest %s" % (
        count, "" if count == 1 else "s", " (arcs for the newest %d steps)" % ARCS_MOST if first_arc > 1 else "",
        _spoken(terms[-1]), _spoken(max(terms))))
    if led.dead:
        pass                                              # the ground letters the death line in the caption itself
    elif led.asleep:
        pen.note("asleep: " + led.asleep)
    elif done:
        pen.note("complete since %s: %s" % (done[0].isoformat(), led.complete.split(",", 1)[-1].rsplit(", at", 1)[0].strip()))
    if opened:
        pen.note("in flower on %s" % ", ".join(_spoken(v) for v in opened))


# ---- a counter

GROUP_PITCH = 0.8          # height of one gate of five and the room above it, in months
BAR_H = 0.6                # a stroke's height
BAR_STEP = 0.15            # between strokes of a gate
GROUP_X = 0.2              # where a gate begins inside its month


def _draw_count(led, seed, ctx, pen, dead, left) -> None:
    pen.unit_name = "month, months"
    wood = "dead" if dead else "wood"
    by_month = {}
    for key, groups in led.months:
        by_month.setdefault(key, []).extend(groups)
    before = {}
    if left is not None:
        for key, groups in left.months:
            before[key] = before.get(key, 0) + sum(sum(1 for ch in g if ch in MARKS) for g in groups)
    years = sorted({int(key[:4]) for key in by_month})[-DRAWN_YEARS:]
    if not years:
        pen.ground(0)
        pen.label(6, 0.4, "nothing counted yet", 16, "ink", "middle")
        pen.note("counting since %s" % (led.since.isoformat() if led.since else "it came up"))
        if led.asleep:
            pen.note("asleep: " + led.asleep)
        return
    tallest = max(1, max((len(by_month.get("%d-%02d" % (y, m), [])) for y in years for m in range(1, 13)), default=1))
    band = tallest * GROUP_PITCH + 0.35
    height = len(years) * band + 0.6
    scale = min(60.0, 860.0 / height, 700.0 / 13.5)      # about how many pixels a month will be: for spacing letters
    # stroke weight, flower size and pixels per month, to the scale
    pens = (max(2.0, min(3.0, scale * 0.06)), max(4.5, min(8.0, scale * 0.16)), scale)
    now = _month_key(ctx.date)
    flowering = [] if dead else _open_flowers(led, seed, ctx, "count")
    colour = _colour(seed)
    for row, year in enumerate(years):
        base = row * band
        pen.ground(base)
        pen.label(-0.12, base + 0.1, str(year), 16, "ink", "end")
        total = sum(led.month_count("%d-%02d" % (year, m)) for m in range(1, 13) if "%d-%02d" % (year, m) in by_month)
        pen.label(12.1, base + 0.1, _spoken(total), 16, "ink", "start")
        for m in range(12):
            key = "%d-%02d" % (year, m + 1)
            if key not in by_month:
                continue
            fresh_ground = left is not None and key not in before or left is None
            _texture(pen, seed, m + 0.06, m + 0.94, base, 9.0 / scale,             # a trait's marks about 9 px
                     "fresh" if fresh_ground and not dead else wood, 3.0)
            old = before.get(key, 0) if left is not None else 0
            mark = 0
            for g, group in enumerate(by_month[key]):
                y = base + 0.1 + g * GROUP_PITCH
                mark = _draw_gate(pen, m + GROUP_X, y, group, mark, old, wood, dead,
                                  colour if key == now and group in flowering else None, pens)
    for m in range(12):                                   # below the marks a trait makes under the ground
        pen.label(m + 0.5, -32.0 / scale, MONTHS[m][0], 14, "ink", "middle")
    total = sum(led.month_count(k) for k in led.month_keys()) + sum(t for _, t in led.years)
    # What it counts is its rule, and the caption never prints the rule: the years show it, and the seed says it.
    pen.note("%s counted since %s" % (_spoken(total), led.since.isoformat() if led.since else "it came up"))
    detail = []
    if flowering:
        detail.append("%d gate%s in flower" % (len(flowering), "" if len(flowering) == 1 else "s"))
    broken = sum(g.count(":") for groups in by_month.values() for g in groups)
    if broken:
        detail.append("%d stroke%s broken" % (broken, "" if broken == 1 else "s"))
    hidden = sorted({int(k[:4]) for k in by_month} - set(years)) + [y for y, _ in led.years]
    if hidden:
        detail.append("%d earlier year%s not drawn" % (len(hidden), "" if len(hidden) == 1 else "s"))
    if led.asleep and not led.dead:                       # (a death is lettered by the ground in the caption)
        detail.insert(0, "asleep: " + led.asleep)
    if detail:
        pen.note("; ".join(detail))


def _draw_gate(pen, x0, y, group, mark, old, wood, dead, flower, pens=(3.0, 8.0, 30.0)) -> int:
    """One gate of strokes, from its lower-left corner. Returns the month's mark count so far."""
    weight, bloom, px = pens
    bars = sum(1 for ch in group if ch in "|:xX")
    step = BAR_STEP if bars <= 5 else 0.6 / max(1, bars - 1)
    width = step * max(0, min(bars, 4) - 1) if bars <= 5 else step * (bars - 1)
    slash = ("/" in group or "\\" in group) and bars <= 5
    lo, hi = (x0 - 0.07, y + 0.1), (x0 + width + 0.07, y + BAR_H - 0.08)     # the fifth stroke, drawn through
    half = min(0.16 * BAR_H, max(0.1 * BAR_H, (weight + 3.0) / (2.0 * px)))  # half a bite's gap: about 3 px clear
    j = 0
    for ch in group:
        ink = wood if dead or mark < old else "fresh"
        mark += 1
        if ch in "/\\":
            pen.line(lo[0], lo[1], hi[0], hi[1], weight, ink)
            if flower:
                pen.dot(hi[0], hi[1], bloom, flower)
                pen.dot(hi[0], hi[1], bloom, wood, filled=False, weight=2.0)    # ringed: a white flower shows too
            continue
        x = x0 + j * step
        j += 1
        if ch == "|":
            pen.line(x, y, x, y + BAR_H, weight, ink)
        elif ch == ":":
            middle = 0.5 * BAR_H                          # the gap in a bitten stroke; in a closed gate it keeps clear
            if slash:                                     # of the fifth stroke, above it or below it
                crossing = lo[1] + (x - lo[0]) / max(1e-9, hi[0] - lo[0]) * (hi[1] - lo[1]) - y
                middle = 0.72 * BAR_H if crossing < 0.5 * BAR_H else 0.26 * BAR_H
            pen.line(x, y, x, y + middle - half, weight, ink)
            pen.line(x, y + middle + half, x, y + BAR_H, weight, ink)
        else:                                             # struck out by a hand: a grey cross, the size of a stroke's middle
            reach = min(0.07, max(0.05, 4.0 / px))
            pen.line(x - reach, y + 0.12, x + reach, y + 0.48, 3.0, "dead")
            pen.line(x - reach, y + 0.48, x + reach, y + 0.12, 3.0, "dead")
    return mark
