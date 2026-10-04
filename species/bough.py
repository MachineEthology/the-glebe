"""
Bough: a plant made of wood and buds. Trees, shrubs, climbers and herbs.

A bough grows by one small rule: what a bud becomes when it breaks. Everything
else about it (what warmth a length of wood costs, how it takes shade, drought
and frost, when and how it flowers) is its temperament, written in the seed
beside the rule. What it has grown is its body: wood that stays where it was
laid, and buds that act.


THE SEED, LINE BY LINE

    kind: bough
    rule: F[+b]F[-b]b     what a bud becomes when it breaks (the grammar is below)
    angle: 30             degrees of one turn
    habit: tree           tree, shrub, climber or herb: how it carries itself
    growth: woody         woody; or herbaceous, which dies back to its crown each winter
    cost: 60              the warmth one length of wood costs (degree-days above 5 °C)
    sun: 0.6              the light it wants: 1 an open bed, 0.35 the foot of the north wall
    thirst: 0.5           how moist it wants the ground: 0 dust will do, 1 never dry
    hardy: -20            the coldest night its buds bear, °C
    tall: 20              the most lengths from the ground to a tip
    most: 300             the most lengths it will ever carry
    leader: 0.4           how far the leading bud outgrows the buds below it (0 not at all)
    reach: 0.12           how its wood bends up towards the sky as it lengthens (below 0: it droops)
    flowers: may to june  when it flowers: months, or a season
    form: umbel           single, spike or umbel: how a flower head is made
    colour: white         the flowers' colour: an ink's name, or #rrggbb
    fruit: dark-red       the colour of its fruit or seed heads, once ripe
    bloom: 16             days a flower stays open
    scent: dusk           none, day, dusk or night. Moths come to dusk and night.
    stem: thorny          (optional) Slugs and ponies leave thorny wood alone,
                          and other mouths take little of it.
    bracts: papery        (optional) A collar of papery bracts round each head. It
                          holds through heavy rain, and stays on the seed head.
    variety: <a name>     (optional) Carried on by its own seed; lost in a cross.

Any line may be missing or garbled: each has a default and a bound.


THE RULE

    F    a length of wood          +  -   a turn, left or right, by `angle`
    b    a bud                     [  ]   a branch: what is inside grows off to the side
    .    a sleeping bud

When a bud breaks it becomes a sleeping bud and the rule. With the rule
F[+b]F[-b]b, a bud `b` becomes `.F[+b]F[-b]b`: a sleeping bud at the foot of
the new shoot, a length, a side bud to the left, a length, a side bud to the
right, and a new bud at the tip. A rule with no bud of its own at the end
(F[+b][-b], say) spends its tip, which is written `x`, and the stem goes on
from its side buds. A branch of the rule with no bud of its own (the [+F] of
F[+F][-F]b) is spent the same way as it is laid: a spur of dead wood with an
`x` at its tip. Branches on branches go at most forty deep; a bud that deep
grows on as if its rule had no branches.

Buds break on warm days in the growing season (spring; and summer too for
climbers and herbs, while trees and shrubs stop once the days shorten below
fourteen hours), as many as the day's warmth can pay for, the leading buds
first. Light, water, the richness of the bed and the plant's own size all
change what a day pays. In shade a bough grows long and sparse: a length may be
laid twice, and side shoots stay asleep as buds. Near its `most`, side shoots
sleep too.


THE BODY

The body is the rule, grown out. A young tree might read:

    .F.F[-b].F
      [+.F[+b]F[-b]b]
    F[-b].F[+b]F[-b]b

    F  a length of wood                  b  a bud, which will break
    +  -  a turn, left or right          .  a sleeping bud
    [ ]  a branch                        *  an open flower (one whole head)
    [27  a branch that broke in 2027     o  a seed head, or a fruit
    ^  where a climber took hold of its  x  a dead tip, or the scar of a fallen fruit
       support: what grows on from it climbs

Only buds act. What has been laid is never changed: a bud is replaced by new
wood, or opens as a flower; a flower becomes a seed head; nothing moves. So
the plate can put exactly the new lengths in the fresh ink.

The `.`s at the very start, before any wood, are the crown: buds at ground
level that shoots come up from. Wood written without brackets is the trunk;
each bracket at the start is a stem from the crown. A herb has only such
stems. It dies back each autumn (at the first hard frost, or when the days are
shorter than about nine and a half hours): its stems stand dead through the
winter and fall when it comes up again from its crown in spring, a stem more
each good year. A crown of two buds or more always keeps one back.

The first line of the body is a key to all this; while the plant is in flower
and scented, a second line says so (scent cannot be drawn). A line that begins
`# remembered:` is what the plant keeps in mind: the year it last came into
flower, the most it has grown past, and what it climbs. Cut that line and it
forgets them. How the text is set out on lines means nothing: the plant writes
itself out tidily whenever it changes, a short branch on its parent's line and
a long one on lines of its own. A # begins a remark, which stays with the wood
written before it. Words written without a # become a remark too: notation is
written in its own case (F; b, o and x in small letters), so a note that
begins "Bob" or "off" stays a note, and so does any line with no wood or
bracket before its words. Whatever else it cannot read, it leaves out. A body
too long to read (some eight thousand marks) loses its end, and says so.


CUTTING IT

Pruning is deleting text. Delete a bracketed branch, from its `[` to its
matching `]`, and the branch is gone. Delete the end of a stem and it is headed
back. Delete a flower or a seed head and it is deadheaded. A herb's stems are
short lines that part anywhere. A thorny, twiggy tree is nested deep and is
slow to cut without taking more than you meant.

The plant answers a cut as real ones do. A stem that has lost its tip (to a
cut, a bite, the frost or the drought) wakes its highest sleeping bud below the
loss, and sometimes the one under it, and each grows out as a branch dated
with the year it broke. But if a living side branch already stands at or above
that bud, the branch simply takes the lead and nothing wakes. The plant answers
all its losses together on one growing day, so a hard pruning is answered in
one line of the almanac.

Sleeping buds face left and right in turn up a stem: left where an even number
of lengths lie below them on that stem, right where an odd number do. A woken
bud grows out on its own side, so to turn a stem outwards, cut just above a
bud that faces out. Cut well above the last sleeping bud and the stub dies back
to a grey snag, which falls in time. Cut down to the crown and it comes again
from the crown. Deadhead a herb in early summer and it may flower again. Wood
with no bud left anywhere on the plant is dead; an empty body comes up again
from the seed.


THE PLATE

    a stroke for each length   in the planter's ink. Its weight is what it
                               carries: a stem is as thick as the branches above
                               it together (the pipe rule), so the trunk is
                               heaviest and every twig is fine, up to the
                               plate's heaviest line.
    fresh green                lengths laid since the last visitor left.
    grey                       dead wood: above a dead tip, a snag above the last
                               living bud, a branch with nothing living on it, a
                               herb's stems in winter, all of a dead plant.
    a dot                      a bud, in the ink of the wood under it: at a tip,
                               or on a stem where a side bud is awake.
    a small ring beside a stem a sleeping bud, on the side it faces. On a plant
                               of more than 400 lengths only the highest on each
                               stem is drawn: the one a loss above it would wake.
    two short slanting strokes a cut: an end that was taken off.
      across an end
    a thick bar on the ground  the crown, with a pale dot for each sleeping crown
                               bud; stems from the crown stand in a row along
                               it, those that lean left to the left.
    filled dots in a colour    open flowers. single: one round dot. spike: a
                               column of dots. umbel: five florets on short
                               rays. Each is one head, one * in the body.
    rings                      seed heads and fruit: one ring, a column of rings,
                               or three on a small fork. Each is one head, one o
                               in the body (a fork of three is one bunch). Pale
                               while they ripen, from the first flowers until
                               August; then in the fruit's colour.
    a starry collar            papery bracts, in the flowers' colour; faded
                               round a seed head.
    small barbs                thorns, on the fine wood of a thorny bough.

Heads are drawn a little smaller on a plant drawn small. Where a flower's or a
fruit's colour is close to the ink of the wood it grows on (the planter's, the
fresh green or the grey), each floret and fruit stands on a rim of clear paper,
so that it can be told from the wood.

The bar in the corner says how long a length is drawn. A climber with something
to climb (a wall, fence, trellis, hedge or tree named in its bed's `lies:`
line, a `support:` line in its tag, or a woody bough close by in the same bed)
takes hold of it: a `^` goes in before each growing tip, and what grows on from
there goes up. What it laid before it took hold stays where it lay. With
nothing to climb it arches over and runs along the ground, and grows weaker;
if its support goes, it lets go and falls. The caption says which, and says
when a bed is shady enough to stretch it.


A LIFE

A night colder than `hardy` kills buds; one eight degrees colder kills the
plant (five degrees, for a herb's crown). A late frost, once the buds are out,
takes young tips, the less so the hardier the plant. A long drought takes tips
from a thirsty one. Flowers open in their months, and in the fortnight before,
on days warm enough for the time of year: early in a warm spring, late in a
cold one, and not all on one morning. On a herb they come from its second
summer, at the top of its stems; on a shrub or climber of some size from its
second season; on a tree only after its first year and a half, and only on its
side branches, never on the leader. A flower ends the growth of its stem; the
sleeping buds below it carry on. Heavy rain knocks open flowers over, unless
they have papery bracts. From August until the frosts the seed heads sow a
seed now and then, about one a year, true to type and keeping their variety.
Birds take most of a woody bough's fruit through the autumn and winter, and
what is left falls in spring, before the new flowers.

When bees or moths bring pollen from another bough of the same growth and the
same form of flower to one in flower, it may set a crossed seed that day, about
one in a flowering season at the most: its colour a blend of both parents',
every other trait taken from one parent or the other, and no variety name. Its
tag will say whose it is. Slugs take the lowest soft buds and flowers, and a
herb's young stems whole, though its crown keeps a bud back to come again
from; a pony takes the tops off in one clean cut, flat across. Thorns keep
both of them off, and other mouths take only a little of a thorny bough.

What the almanac hears from a bough: that it came into flower (once a season),
went down for the winter, came up again from its crown, woke sleeping buds
below a cut, took hold of a support or lost its hold, lost young tips to a
late frost or to drought, grew past a hundred, two hundred and fifty or five
hundred lengths (once in its life), lost the end of a body too long to read,
or died.


Written by the builder of bough, 30 September 2026. Mended on 1 October 2026,
after an ordeal and a blind eye had been over it.
"""

import datetime
import math
import re

import hands

KIND = "bough"

HABITS = ("tree", "shrub", "climber", "herb")
FORMS = ("single", "spike", "umbel")
SCENTS = ("none", "day", "dusk", "night")
DEFAULT_RULE = ("F", "[", "+", "b", "]", "F", "[", "-", "b", "]", "b")
KEPT = ("kind", "rule", "angle", "habit", "growth", "cost", "sun", "thirst", "hardy", "tall", "most",
        "leader", "reach", "flowers", "form", "colour", "fruit", "bloom", "scent", "stem", "bracts")
WORDS = ("rule", "habit", "growth", "flowers", "form", "scent", "stem", "bracts")
NUMBERS = {"angle": 0, "cost": 0, "sun": 2, "thirst": 2, "hardy": 0, "tall": 0, "most": 0,
           "leader": 2, "reach": 2, "bloom": 0}                 # the numbers a cross blends, and to how many places
SUPPORTS = ("wall", "fence", "trellis", "hedge", "arch", "pergola", "post", "stake", "pole", "tree",
            "mur", "treillis", "haie", "arbre", "tuteur", "palissade", "grille", "arceau")
SPRAWL = -0.12            # how a climber with nothing to climb bends: down, and along the ground
TAKE_HOLD = (0.3, 12)     # a woody bough is taken hold of within this distance, with at least this many lengths;
KEEP_HOLD = (0.4, 8)      # and kept hold of within this one (a nudge across the line must not drop the plant)
PONIES = ("pony", "poney", "horse", "cheval", "jument", "deer")
SLUGS = ("slug", "snail", "limace", "escargot")
HEADER = ("# a bough's body: F a length of wood · + - a turn · [ ] a branch ([27 broke in 2027)"
          " · b a bud · . a sleeping bud · * a flower · o a seed head · x a dead tip")
HOLD_KEY = " · ^ it took hold of a support here"
MIND = "remembered:"
OWN_REMARKS = ("a bough's body", "in flower and scented", MIND)
SCENT_WORDS = {"day": "by day", "dusk": "at dusk", "night": "at night"}
MOST_TOKENS = 8_000       # what a body is read to; growth stops short of it (see ROOM) and long before (see `most`)
ROOM = 200                # the marks growth always leaves unwritten below MOST_TOKENS
MOST_DEPTH = 40           # branches on branches deeper than this are read as part of their parent; growth stops short
MOST_INDENT = 30          # the deepest a branch's line is set in, in spaces
BODY_MOST = 50_000        # a body laid out longer than this is written close, without its indents
WRAP = 72                 # a line of body is broken after about this many characters
INLINE = 30               # a branch with no branches of its own and no longer than this stays on its parent's line
DAGGER = hands.DAGGER
MILESTONES = (100, 250, 500)
LEAD = 14                 # days before its first flowering month in which a warm spell may open the first flowers
RIPE = 8                  # the month seed and fruit are ripe from (August)
CROSS_MOST = 0.012        # the most a day's pollen can do: about one crossed seed in a flowering season, at the most
UNIT_PX_MAX = 100.0       # a length is never drawn longer than this: a seedling fills a good part of its plate
ROW = 0.5                 # lengths between the feet of two stems that come up from the crown side by side
MANY_RINGS = 400          # above this many lengths, only the highest sleeping bud on each stem is drawn
PAPER = "#fbf8f1"


# ============================================================ the temperament

MONTHS = {"jan": 1, "feb": 2, "fev": 2, "mar": 3, "apr": 4, "avr": 4, "may": 5, "mai": 5, "jun": 6,
          "jui": 7, "jul": 7, "aug": 8, "aou": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}
SEASON_MONTHS = {"spring": (3, 5), "printemps": (3, 5), "summer": (6, 8), "ete": (6, 8), "autumn": (9, 11),
                 "fall": (9, 11), "automne": (9, 11), "winter": (12, 2), "hiver": (12, 2)}
_PLAIN = str.maketrans("éèêëàâäîïôöûüùç", "eeeeaaaiioouuuc")


def months_of(said) -> frozenset:
    """The months a `flowers:` line names: 'may', 'june to august', 'summer', 'juin-août'. Default: summer."""
    found = []
    for word in re.findall(r"[^\W\d_]+", str(said or "").lower().translate(_PLAIN)):
        if word in SEASON_MONTHS:
            found += list(SEASON_MONTHS[word])
        elif word[:4] == "juil":
            found.append(7)
        elif word[:4] == "juin":
            found.append(6)
        elif word[:3] in MONTHS and not (word[:3] == "mar" and word.startswith("mardi")):
            found.append(MONTHS[word[:3]])
    if not found:
        return frozenset((6, 7, 8))
    first, last = found[0], found[-1]
    months, month = [first], first
    while month != last and len(months) < 12:
        month = month % 12 + 1
        months.append(month)
    return frozenset(months)


def rule_of(said) -> list:
    """A `rule:` line as tokens: F + - [ ] b and . only, brackets balanced, at most about forty."""
    tokens, depth = [], 0
    for c in str(said or "")[:400]:
        if c in "Ff":
            tokens.append("F")
        elif c in "+-.":
            tokens.append(c)
        elif c in "bB":
            tokens.append("b")
        elif c == "[":
            tokens.append("[")
            depth += 1
        elif c == "]" and depth:
            tokens.append("]")
            depth -= 1
        if len(tokens) >= 40:
            break
    tokens += ["]"] * depth
    if "F" not in tokens and "b" not in tokens:
        tokens = list(DEFAULT_RULE)
    return tokens


def _spent(rule) -> list:
    """The rule as a bud lays it: a branch with no bud of its own ends in a spent tip, x.

    Without the x, the bare end of such a branch would read as a cut (and be
    drawn and answered as one) although nothing was taken off.
    """
    out, own = [], []
    for tok in rule:
        if tok == "[":
            own.append(False)
        elif tok == "]":
            if own and not own.pop():
                out.append("x")
        elif tok == "b" and own:
            own[-1] = True
        out.append(tok)
    return out


def _ink(said, otherwise) -> str:
    """An ink as a seed names it ('dark-red', '#f0b6c8'), or `otherwise` if it names none the plate knows."""
    said = str(said or "").strip().split()
    said = said[0].lower() if said else ""
    if not said:
        return otherwise
    return said if hands.mix(said, said) != "#1a1a1a" or said == "#1a1a1a" else otherwise


class Temper:
    """A seed's temperament, read forgivingly: every value has a default and a bound."""

    def __init__(self, seed):
        seed = seed if isinstance(seed, dict) else {}
        self.habit = hands.word(seed, "habit", "shrub", HABITS)
        herb = self.habit == "herb"
        self.growth = hands.word(seed, "growth", "herbaceous" if herb else "woody", ("woody", "herbaceous"))
        self.woody = self.growth == "woody"
        self.rule = rule_of(hands.line(seed, "rule", ""))
        self.rule_wood = max(1, self.rule.count("F"))
        depth, self.apex, self.rule_depth, flat = 0, False, 0, []   # does the rule carry the stem on with a bud of its own?
        for tok in self.rule:
            depth += 1 if tok == "[" else -1 if tok == "]" else 0
            self.rule_depth = max(self.rule_depth, depth)
            self.apex = self.apex or (tok == "b" and depth == 0)
            if depth == 0 and tok != "]":
                flat.append(tok)
        self.lays = _spent(self.rule)                    # what a bud becomes
        self.lays_flat = flat                            # ...when it is too deep for the rule's branches
        self.angle = hands.num(seed, "angle", 28, 3, 90)
        self.cost = hands.num(seed, "cost", 60 if self.woody else 25, 2, 400)
        self.sun = hands.num(seed, "sun", 0.6, 0.05, 1)
        self.thirst = hands.num(seed, "thirst", 0.5, 0, 1)
        self.hardy = hands.num(seed, "hardy", -15, -40, 10)
        self.tall = hands.num(seed, "tall", 20 if self.woody else 6, 1, 60)
        self.most = hands.num(seed, "most", 300 if self.woody else 120, 5, 900)
        self.leader = hands.num(seed, "leader", 0.4 if self.woody else 0.0, 0, 0.95)
        self.reach = hands.num(seed, "reach", 0.12, -0.5, 0.6)
        self.months = months_of(hands.line(seed, "flowers", "summer"))
        self.first_month = next((m for m in range(1, 13) if m in self.months and (m - 2) % 12 + 1 not in self.months),
                                min(self.months))
        self.form = hands.word(seed, "form", "single", FORMS)
        self.colour = _ink(hands.line(seed, "colour", "") or hands.line(seed, "color", ""), "white")
        self.fruit = _ink(hands.line(seed, "fruit", ""), "brown")
        self.bloom = hands.num(seed, "bloom", 18, 2, 90)
        self.scent = hands.word(seed, "scent", "none", SCENTS)
        self.thorny = hands.word(seed, "stem", "", ("thorny",)) == "thorny"
        self.papery = hands.word(seed, "bracts", "", ("papery",)) == "papery"
        self.stops_midsummer = self.woody and self.habit in ("tree", "shrub")


# ============================================================== the body read

_WORD = re.compile(r"[^\W\d_]+")
_GRAMMAR = frozenset("Fbox")          # notation is written in its own case: F, and b o x in small letters
_TOKENS = re.compile(r"\[\s*\d{0,4}|[F+\-\]b.*ox^]")
_MIND = re.compile(r"#\s*remembered\s*:(.*)", re.IGNORECASE)


def _split(line):
    """A line of body as (its notation, its remark). Words that are not notation begin a remark.

    If nothing but a mark or two (no wood, no bracket) stands before the
    words, the whole line is a remark: '- cut in May' and 'x marks the old
    leader' are notes, not a turn and a dead tip.
    """
    at = line.find("#")
    code, remark = (line[:at], line[at + 1:].strip()) if at >= 0 else (line, "")
    for word in _WORD.finditer(code):
        if not _GRAMMAR.issuperset(word.group()):
            head = code[:word.start()]
            if not any(c in head for c in "F[]"):
                head = ""
            prose = code[len(head):].strip()
            code = head
            remark = prose + ("  " + remark if remark else "")
            break
    return code, remark.strip()


def read(body):
    """A body as (its † line or '', its tokens). Reads what it can; never raises.

    Tokens are 'F' '+' '-' ']' 'b' '.' '*' 'o' 'x' '^', '[' or '[27' (a
    branch, with the year it broke), and '#words' (a remark). Brackets always
    balance.
    """
    dead, tokens, _ = _read(body)
    return dead, tokens


def _read(body):
    """read(), and whether the body was too long to read to its end (then its end is lost)."""
    text = _text(body)[:200_000]
    dead, tokens, first, remarks, depth, lost = "", [], True, 0, 0, False
    kept = []                                            # for each open [: was it kept? (deeper than MOST_DEPTH is not)
    for raw in text.split("\n"):                         # only a newline ends a line: not \x0b, \x85, U+2028 ...
        line = raw.strip()
        if not line:
            continue
        if first:
            first = False
            if line.startswith(DAGGER):
                dead = line
                continue
        code, remark = _split(line)
        found = _TOKENS.findall(code)
        if "[" not in code and "]" not in code:
            room = MOST_TOKENS - len(tokens)
            if len(found) > room:
                found, lost = found[:max(0, room)], True
            tokens += found
        else:
            for said in found:
                if len(tokens) >= MOST_TOKENS:
                    lost = True
                    break
                if said[0] == "[":
                    keep = depth < MOST_DEPTH
                    kept.append(keep)
                    if keep:
                        depth += 1
                        year = said[1:].strip()
                        tokens.append("[" + ("%02d" % (int(year) % 100) if year else ""))
                elif said == "]":
                    if kept and kept.pop():
                        depth -= 1
                        tokens.append("]")
                else:
                    tokens.append(said)
        if remark and not remark.lower().startswith(OWN_REMARKS) and remarks < 200:
            if len(tokens) >= MOST_TOKENS:
                lost = True
            else:
                tokens.append("#" + remark[:300])
                remarks += 1
        if lost:
            break
    return dead, tokens + ["]"] * depth, lost


def _trim(tokens, most) -> list:
    """The first `most` tokens, with every branch left open closed again."""
    kept, depth = tokens[:max(0, most)], 0
    for tok in kept:
        depth += 1 if tok[0] == "[" else -1 if tok == "]" else 0
    return kept + ["]"] * max(0, depth)


def _text(body) -> str:
    """Whatever a body file gave, as text."""
    if isinstance(body, (bytes, bytearray)):
        return bytes(body).decode("utf-8", errors="replace")
    return body if isinstance(body, str) else ("" if body is None else str(body))


def _memory(body) -> dict:
    """What the body's `# remembered:` line keeps: the year it last came into flower, the most it grew past, its support."""
    mind = {"flowered": 0, "past": 0, "climbing": ""}
    text = _text(body)[:200_000]
    if "emembered" not in text and "EMEMBERED" not in text:
        return mind
    for line in text.split("\n"):
        found = _MIND.search(line)
        if not found:
            continue
        for part in found.group(1).split("·"):
            part = part.strip()
            said = re.match(r"in flower in (\d{1,4})\b", part)
            if said:
                mind["flowered"] = int(said.group(1))
            said = re.match(r"past (\d{1,6}) lengths?\b", part)
            if said:
                mind["past"] = int(said.group(1))
            if part.startswith("climbing "):
                mind["climbing"] = part[9:].strip()[:40]
        break
    return mind


def _mind_line(mind) -> str:
    """The `# remembered:` line for what a plant keeps in mind, or '' if there is nothing."""
    mind = mind or {}
    parts = []
    if mind.get("flowered"):
        parts.append("in flower in %d" % mind["flowered"])
    if mind.get("past"):
        parts.append("past %d lengths" % mind["past"])
    support = re.sub(r"[·#\s]+", " ", str(mind.get("climbing") or "")).strip()[:40]
    if support:
        parts.append("climbing " + support)
    return "# %s %s" % (MIND, " · ".join(parts)) if parts else ""


class Axis:
    """One stem or branch: the trunk (written without brackets) or what lies between a [ and its ]."""

    __slots__ = ("open", "close", "parent", "pos", "year", "turns", "items", "children", "nF", "depth",
                 "key", "base", "alive", "last_live", "tips", "started", "fs")

    def __init__(self, open_, parent, pos, year):
        self.open, self.close, self.parent, self.pos, self.year = open_, open_, parent, pos, year
        self.turns, self.items, self.children, self.nF = "", [], [], 0
        self.depth = parent.depth + 1 if parent else 0
        self.base = parent.base + pos if parent else 0       # lengths from the ground to where it starts
        self.key, self.alive, self.last_live, self.tips, self.started, self.fs = (), False, -1, 1, False, []


class Anatomy:
    """The body's tokens laid out as axes. `node[i]` is how many lengths of its own axis lie below token i."""

    def __init__(self, tokens, feel=True):
        self.tokens = tokens
        self.named = False
        self.top = Axis(-1, None, 0, "")
        self.axes = [self.top]
        self.axis = [self.top] * len(tokens)
        self.node = [0] * len(tokens)
        here = self.top
        for i, tok in enumerate(tokens):
            head = tok[0]
            if head == "[":
                child = Axis(i, here, here.nF, tok[1:])
                self.axis[i], self.node[i] = here, here.nF
                here.items.append(child)
                here.children.append(child)
                self.axes.append(child)
                here = child
                continue
            self.axis[i], self.node[i] = here, here.nF
            if head == "]":
                here.close = i
                here = here.parent or self.top
                continue
            here.items.append(i)
            if head == "F":
                here.fs.append(i)
                here.nF += 1
            if head in "+-" and not here.started:
                here.turns += head
            elif head != "#":
                here.started = True
        self.top.close = len(tokens)
        if feel:
            self.feel()

    def _name(self):
        """Give each axis a key that stays the same while the plant grows: where it leaves its parent, and how."""
        self.named = True
        seen = {}
        for axis in self.axes[1:]:
            mark = (id(axis.parent), axis.pos, axis.year, axis.turns)
            seen[mark] = seen.get(mark, -1) + 1
            axis.key = axis.parent.key + ((axis.pos, axis.year, axis.turns, seen[mark]),)

    def feel(self):
        """Find what is alive: each axis's highest living node, and how many tips it carries (the pipe rule).

        Buds, sleeping buds, flowers and ripening seed heads or fruit are
        living; wood above the highest of them on its axis is dead.
        """
        living = ("b", ".", "*", "o")
        tokens, node = self.tokens, self.node
        for axis in reversed(self.axes):
            last, tips = -1, 1
            for item in axis.items:
                if isinstance(item, Axis):
                    tips += item.tips
                    if item.alive:
                        last = max(last, item.pos)
                elif tokens[item] in living:
                    last = max(last, node[item])
            axis.last_live, axis.alive, axis.tips = last, last >= 0, tips

    def end(self, axis):
        """The token that ends an axis (F, b, ., *, o or x), as (index, token); (None, '') if it has none."""
        for item in reversed(axis.items):
            if not isinstance(item, Axis) and self.tokens[item] in "Fb.*ox":
                return item, self.tokens[item]
        return None, ""

    def height(self, i) -> int:
        """Lengths from the ground to token i."""
        return self.axis[i].base + self.node[i]

    def wood(self) -> set:
        """Every length, by a name that growth never changes: (its axis's key, its place along that axis)."""
        if not self.named:
            self._name()
        return {(axis.key, j) for axis in self.axes for j in range(axis.nF)}


def _anything(tokens) -> bool:
    """Is there anything here at all: wood, or a bud of any sort?"""
    return any(tok in ("F", "b", ".", "*") for tok in tokens)


def _alive(tokens) -> bool:
    """Is anything living left: a bud, a sleeping bud, a flower, a ripening seed head or fruit?"""
    return any(tok in ("b", ".", "*", "o") for tok in tokens)


# ============================================================== the body laid

def lay(tokens, dead="", scent="", mind=None) -> str:
    """Tokens as the text of a body: a key, what it remembers, then the plant, one branch of any size to a line."""
    shape = Anatomy(tokens, feel=False)
    lines = [dead] if dead else []
    lines.append(HEADER + (HOLD_KEY if "^" in tokens else ""))
    if scent:
        lines.append("# in flower and scented %s" % scent)
    remembered = _mind_line(mind)
    if remembered:
        lines.append(remembered)
    grown = []
    _lay_axis(shape.top, tokens, 0, 0, "", grown)
    text = "\n".join(lines + grown) + "\n"
    if len(text) <= BODY_MOST:
        return text
    close, line = [], ""                                 # too long set out: written close, a remark to a line
    for tok in tokens:
        if tok[0] == "#" or len(line) >= WRAP:
            close.append(line)
            line = ""
        if tok[0] == "#":
            close.append("# " + tok[1:])
        else:
            line += tok
    return "\n".join(lines + [c for c in close + [line] if c]) + "\n"


def _inline(axis, tokens):
    """A short branch with no branches of its own, as one piece of text; None if it deserves its own line."""
    if axis.children:
        return None
    own = [tokens[i] for i in axis.items]
    if any(tok[0] == "#" for tok in own):
        return None
    text = "[" + axis.year + "".join(own) + "]"
    return text if len(text) <= INLINE else None


def _lay_axis(axis, tokens, open_col, col, opener, lines):
    """Lay one axis: its own tokens along a line, short branches inline, long ones on lines of their own.

    Each branch on a line of its own is set in a little further than its
    parent, but never past MOST_INDENT: the indents are for the eye only.
    """
    at, text = open_col, opener
    for item in axis.items:
        if isinstance(item, Axis):
            short = _inline(item, tokens)
            if short is not None:
                if len(text) + len(short) > WRAP and text:
                    lines.append(" " * at + text)
                    at, text = col, ""
                text += short
                continue
            if text:
                lines.append(" " * at + text)
            _lay_axis(item, tokens, min(col + 2, MOST_INDENT), min(col + 3, MOST_INDENT + 1), "[" + item.year, lines)
            at, text = col, ""
            continue
        tok = tokens[item]
        if tok[0] == "#":
            lines.append(" " * at + (text + "  " if text else "") + "# " + tok[1:])
            at, text = col, ""
            continue
        if len(text) >= WRAP:
            lines.append(" " * at + text)
            at, text = col, ""
        text += tok
    if axis.parent is None:
        if text:
            lines.append(" " * at + text)
    elif text:
        lines.append(" " * at + text + "]")
    elif lines and "#" not in lines[-1]:
        lines[-1] += "]"
    else:
        lines.append(" " * col + "]")


# ================================================================ the weather

class Day:
    """What one day's sky means to this bough in its bed."""

    def __init__(self, t, ctx):
        s = ctx.sky
        self.warm = _f(getattr(s, "warmth", 0.0), 0.0, 0.0, 40.0)
        self.tmin = _f(getattr(s, "tmin", 5.0), 5.0, -60.0, 60.0)
        self.rain = _f(getattr(s, "rain", 0.0), 0.0, 0.0, 500.0)
        daylength = _f(getattr(s, "daylength", 12.0), 12.0, 0.0, 24.0)
        self.daylength = daylength
        share = _f(getattr(s, "light", 6.0), 6.0, 0.0, 24.0) / max(1.0, daylength) / 0.6
        self.shade = max(0.0, min(1.0, 1.0 - share / t.sun))
        self.f_light = max(0.15, min(1.0, share / t.sun)) ** 0.6
        wet = _f(getattr(s, "wet", 0.5), 0.5, 0.0, 1.0)
        need = 0.35 * t.thirst
        self.f_water = 1.0 if wet >= need else max(0.0, wet / need) ** 0.7
        self.drought = 1.0 - self.f_water
        self.rich = hands.num(getattr(ctx, "bed", None) or {}, "rich", 0.0, 0.0, 1.0)
        season = str(getattr(s, "season", "") or "")
        self.season = season
        self.month = getattr(getattr(ctx, "date", None), "month", 6)
        self.grows = self.warm > 0 and (season == "spring" or (
            season == "summer" and (daylength >= 14.0 or not t.stops_midsummer)))


def _f(value, otherwise, lo, hi) -> float:
    try:
        value = float(value)
    except Exception:
        return otherwise
    if value != value:
        return otherwise
    return min(hi, max(lo, value))


def _flower_time(t, date):
    """(the year this flowering season began, days since its first flowers could open), or None out of season.

    The season opens LEAD days before the first of its first month, and runs
    to the end of its last month.
    """
    try:
        for year in (date.year + 1, date.year, date.year - 1):
            opens = datetime.date(year, t.first_month, 1) - datetime.timedelta(days=LEAD)
            since = (date - opens).days
            if since >= 0:
                break
        else:
            return None
    except Exception:
        return None
    if since < LEAD or date.month in t.months:
        return (opens + datetime.timedelta(days=LEAD)).year, since
    return None


def _opening(t, d, since) -> float:
    """The chance that a bud ready to flower opens today: none until the days are warm enough for the time of year.

    In the fortnight before its months only an unusually warm day opens a
    flower; a week or so into them (longer, for a long flowering) an
    ordinary one does. So the first flowers come early in a warm spring and
    late in a cold one, and a bed of boughs does not come into flower on
    one morning.
    """
    ramp = LEAD + 7.0 * len(t.months)
    needed = 16.0 - 12.0 * min(1.0, since / ramp)
    return 0.07 * max(0.0, min(1.5, (d.warm - needed) / 6.0))


def _fruit_falls(t, d) -> float:
    """The chance that one fruit of a woody bough is taken by birds or falls today (a herb keeps its seed heads)."""
    if not t.woody:
        return 0.0
    if d.season == "autumn":
        return 0.012 + (0.02 if d.tmin < 2.0 else 0.0)
    if d.season == "winter":
        return 0.015
    if d.season == "spring":
        return 0.06                                      # what the birds left falls before the new flowers
    return 0.0


def _ripening(t, month) -> bool:
    """Is a seed head or fruit still ripening in this month? From the plant's first flowers until August it is."""
    return isinstance(month, int) and t.first_month <= month < RIPE


def climbing(t, ctx, holding=False):
    """What a climber has to climb, in a few words; None if it has nothing (or is no climber).

    A plant already holding on keeps hold of a woody neighbour a little
    further off, and a little smaller, than one it would take hold of anew,
    so that a nudge across the line does not drop it.
    """
    if t.habit != "climber":
        return None
    for keys in (getattr(ctx, "tag", None) or {}, getattr(ctx, "seed", None) or {}):
        said = hands.line(keys, "support", "")
        if said:
            return said[:40]
    lies = hands.line(getattr(ctx, "bed", None) or {}, "lies", "").lower()
    for word in re.findall(r"[^\W\d_]+", lies):
        if word.rstrip("s") in SUPPORTS or word in SUPPORTS:
            return "the " + word
    near_most, wood_least = KEEP_HOLD if holding else TAKE_HOLD
    try:
        near = sorted(getattr(ctx, "neighbours", None) or [], key=lambda n: n.distance)
    except Exception:
        near = []
    for other in near[:6]:
        try:
            if other.kind != KIND or other.distance > near_most:
                continue
            them = Temper(other.seed)
            if them.woody and them.habit in ("tree", "shrub") and read(other.body)[1].count("F") >= wood_least:
                return str(other.name)[:40]
        except Exception:
            continue
    return None


# ================================================================== the days

def sprout(seed, ctx) -> str:
    """A seedling: one crown bud and a first length with a bud on it (a herb's in brackets, since it will die back).

    A climber sown where it has something to climb has hold of it from the start.
    """
    t = Temper(seed)
    year = "%02d" % (getattr(getattr(ctx, "date", None), "year", 2026) % 100)
    support = climbing(t, ctx)
    hold = ["^"] if support else []
    tokens = [".", *hold, "F", "b"] if t.woody else [".", "[" + year, *hold, "F", "b", "]"]
    return lay(tokens, mind={"climbing": support or ""})


def day(body, seed, ctx):
    """One day of a bough's life. Returns (the new body, an event line or None)."""
    body = _text(body)
    dead, tokens, lost = _read(body)
    if dead or hands.is_dead(body):
        return body, None
    if not _anything(tokens):
        return sprout(seed, ctx), "came up again from the seed"
    t = Temper(seed)
    rng = ctx.rng
    d = Day(t, ctx)
    date = getattr(ctx, "date", None)
    year = "%02d" % (getattr(date, "year", 2026) % 100)
    mind = _memory(body)
    minded = dict(mind)
    events = []
    if lost:
        tokens = _trim(tokens, MOST_TOKENS - ROOM)       # so that it is read to its end from now on
        events.append("the end of its body could not be read, and was lost")
    before = list(tokens)
    wood_before = tokens.count("F")

    # -- a climber takes hold of what it can climb (at its growing tips; new shoots find it too), or lets go
    held = "^" in tokens
    support = climbing(t, ctx, held)
    if support and not held:
        tokens = _take_hold(tokens)
    elif held and not support:
        tokens = [tok for tok in tokens if tok != "^"]
    vigour = 0.6 if t.habit == "climber" and "^" not in tokens else 1.0

    # -- the cold that kills
    killing = t.hardy - (8.0 if t.woody else 5.0)
    if d.tmin < killing:
        return _dead(tokens, ctx, "frost", mind), "died of frost"
    shape = None                                         # the body's anatomy, worked out only on days that need it

    # -- a herb's year: down in autumn (and up again in spring, below)
    if not t.woody and d.season in ("autumn", "winter") and (d.tmin < -1.0 or d.daylength < 9.6):
        shape = Anatomy(tokens)
        if any(a.alive for a in shape.top.children):
            tokens = _die_back(tokens, shape, t, d)
            events.append("went down for the winter")
        shape = None

    # -- frost and drought take buds (one token for one: nothing moves)
    lost_frost = lost_drought = 0
    for i, tok in enumerate(tokens):
        if tok != "b":
            continue
        if d.tmin < t.hardy and rng.random() < min(0.9, (t.hardy - d.tmin) / 8.0):
            tokens[i], lost_frost = "x", lost_frost + 1
        elif d.season == "spring" and d.daylength >= 12.5 and d.tmin < -1.0 and rng.random() < (      # a late frost, once buds are out
                min(0.6, 0.12 * (-1.0 - d.tmin)) * max(0.1, min(1.0, (t.hardy + 35.0) / 25.0))):
            tokens[i], lost_frost = "x", lost_frost + 1
        elif d.drought > 0.6 and d.warm > 6 and rng.random() < (0.012 if t.woody else 0.03) * d.drought:
            tokens[i], lost_drought = "x", lost_drought + 1
    buds = max(1, tokens.count("b") + lost_frost + lost_drought)
    if lost_frost >= max(2, buds // 10):
        events.append("the frost took %d young tips" % lost_frost)
    if lost_drought >= max(3, buds // 6):
        events.append("the drought took %d tips" % lost_drought)

    # -- flowers open and fade; fruit falls
    season = _flower_time(t, date)
    knock = 0.0 if t.papery or d.rain < 12 else 0.25
    ready, opening = None, 0.0
    if season is not None and "b" in tokens:
        opening = _opening(t, d, season[1])
        if opening > 0:
            shape = Anatomy(tokens, feel=False)
            ready = _ready_to_flower(t, shape, tokens, ctx)
    falls = _fruit_falls(t, d)
    opened = 0
    for i, tok in enumerate(tokens):
        if tok == "*":
            if rng.random() < 1.0 / t.bloom + knock:
                tokens[i] = "o"
        elif tok == "b" and ready is not None and ready(i) and rng.random() < opening:
            tokens[i] = "*"
            opened += 1
        elif tok == "o" and falls and rng.random() < falls:
            tokens[i] = "x"                              # the fruit is gone; a scar where it hung
    if opened and mind["flowered"] != season[0]:
        events.append("came into flower")                # once a season, and the plant remembers which
        mind["flowered"] = season[0]

    # -- the growing: buds break, sleeping buds wake, a herb comes up
    edits = {}
    room = [MOST_TOKENS - ROOM - len(tokens)]            # what growth may still write today, in marks
    shed = rng.random() < 0.03
    if d.grows or shed:
        if shape is None:
            shape = Anatomy(tokens)
        else:
            shape.feel()                                 # the same shape; what is alive in it may have changed
    if d.grows:
        woken = _wake(tokens, shape, t, d, rng, year, edits, room, bool(support))
        if woken:
            events.append("woke %s below the cut" % ("a sleeping bud" if woken == 1 else "%d sleeping buds" % woken))
        if not t.woody:
            came = _crown_wakes(tokens, shape, t, d, rng, year, edits, room, bool(support))
            if came:
                events.append("came up again from its crown")
        _grow(tokens, shape, t, d, rng, vigour, edits, room)
    if shed:
        _shed(tokens, shape, t, rng, edits)
    if edits:
        grown = []
        for i, tok in enumerate(tokens):
            grown.extend(edits[i]) if i in edits else grown.append(tok)
        tokens = grown
    holds = "^" in tokens
    if holds and not held:
        events.append("took hold of %s" % (support or "its support"))
    elif held and not holds and not support:
        events.append("lost its hold and fell")
    mind["climbing"] = (support or mind["climbing"]) if holds else ""

    # -- is anything left alive?
    if not _alive(tokens):
        why = "frost" if lost_frost else "drought" if lost_drought else "no bud left"
        return (_dead(tokens, ctx, why, mind),
                "died: " + ("the %s took its last buds" % why if why != "no bud left" else why))

    wood_now = tokens.count("F")
    for mark in MILESTONES:
        if mind["past"] < mark <= wood_now:              # once in its life: the plant remembers
            if wood_before < mark:
                events.append("grew past %d lengths" % mark)
            mind["past"] = mark
    if tokens == before and mind == minded and not lost and len(body) <= BODY_MOST:
        return body, None
    return lay(tokens, scent=_scent(t, tokens), mind=mind), "; ".join(events[:3]) or None


def _dead(tokens, ctx, why, mind=None) -> str:
    date = getattr(getattr(ctx, "date", None), "isoformat", lambda: "")()
    return lay(tokens, dead="%s %s, %s" % (DAGGER, date, why), mind=mind)


def _scent(t, tokens) -> str:
    return SCENT_WORDS.get(t.scent, "") if "*" in tokens else ""


def _take_hold(tokens) -> list:
    """A climber takes hold: a ^ goes in before the bud at each growing tip, so what grows on from there climbs.

    Nothing already laid moves. A plant with no wood at all takes hold from
    its foot. One with wood but no growing tip (a herb resting on its crown)
    cannot take hold today; its new stems will.
    """
    shape = Anatomy(tokens, feel=False)
    tips = set()
    for axis in shape.axes:
        at, end = shape.end(axis)
        if end == "b":
            tips.add(at)
    if not tips:
        return ["^"] + tokens if "F" not in tokens else tokens
    if len(tokens) + len(tips) > MOST_TOKENS - ROOM:
        return tokens
    out = []
    for i, tok in enumerate(tokens):
        if i in tips:
            out.append("^")
        out.append(tok)
    return out


def _die_back(tokens, shape, t, d):
    """A herb goes down: its stems die where they stand, and the crown sets buds for next year's stems."""
    stems = [a for a in shape.top.children if a.alive]
    flowered = sum(1 for a in stems if any(tokens[i] in "*o" for i in range(a.open, a.close)))
    crown = sum(1 for i in shape.top.items if not isinstance(i, Axis) and tokens[i] == "." and shape.node[i] == 0)
    grow_by = 1 + (1 if flowered >= 2 else 0) + (1 if d.rich > 0.3 else 0)
    crown = max(1, min(14, crown + len(stems) + grow_by))
    out, placed = [], False
    for i, tok in enumerate(tokens):
        at_crown = shape.axis[i] is shape.top and shape.node[i] == 0
        if at_crown and tok == ".":
            continue                                     # the old crown buds: written again below
        if not placed and not tok.startswith("#"):
            out += ["."] * crown
            placed = True
        out.append("x" if tok in ("b", ".", "*", "o") and not at_crown else tok)
    if not placed:
        out += ["."] * crown
    return out


def _ready_to_flower(t, shape, tokens, ctx):
    """Which buds may open as flowers today: a test on a token's index, or None if none may."""
    wood = tokens.count("F")
    age = getattr(ctx, "age", 0) or 0
    if t.woody and (wood < 15 or age < (400 if t.habit == "tree" else 240)):
        return None                                      # too young: a tree waits for its second spring
    if not t.woody:
        if age < 200:
            return None                                  # a herb's first flowers come in its second summer
        least = max(2, int(t.tall * 0.5))
        return lambda i: shape.height(i) >= least
    if t.habit == "tree":
        return lambda i: shape.axis[i].depth >= 1 and shape.height(i) >= 3
    return lambda i: shape.height(i) >= 3


def _grow(tokens, shape, t, d, rng, vigour, edits, room):
    """Break as many buds as the day's warmth pays for, the leading ones first, and no more than there is room for."""
    wood = tokens.count("F")
    if wood >= t.most or room[0] <= 0:
        return
    buds = [i for i, tok in enumerate(tokens) if tok == "b" and i not in edits]
    if not buds:
        return
    active = len(buds) + tokens.count("*")
    capacity = 1.0 + math.sqrt(active)
    if not t.woody:
        capacity += 0.7 * sum(1 for a in shape.top.children if a.alive)
    fill = (1.0 - wood / t.most) ** 0.7
    sap = d.warm * d.f_light * d.f_water * (1.0 + 0.5 * d.rich) * fill * capacity * vigour
    count = min(_poisson(rng, sap / (t.cost * (t.rule_wood + 0.5))), 24)
    choice = [(i, (1.0 - t.leader) ** shape.axis[i].depth) for i in buds if shape.height(i) < t.tall]
    maturity = wood / t.most
    asleep = max(0.0, min(0.9, 0.25 * t.leader + 0.7 * d.shade + 0.5 * maturity))
    for _ in range(count):
        total = sum(w for _, w in choice)
        if total <= 0:
            break
        pick = rng.random() * total
        for k, (i, w) in enumerate(choice):
            pick -= w
            if pick <= 0:
                break
        i = choice.pop(k)[0]
        grown = _break(tokens, shape, i, t, d, rng, asleep)
        if len(grown) - 1 > room[0]:
            break                                        # the body is as long as it can be read: no more today
        room[0] -= len(grown) - 1
        edits[i] = grown


def _break(tokens, shape, i, t, d, rng, asleep) -> list:
    """What one bud becomes: a sleeping bud and the rule, stretched in shade, some side shoots asleep.

    A side shoot of the rule that does not break is written as what it is:
    a sleeping bud at its node, on the stem it would have left. A bud so deep
    among branches that the rule's own would go past MOST_DEPTH grows on as if
    the rule had none.
    """
    axis = shape.axis[i]
    sideways = shape.node[i] < axis.nF                   # a bud part way up a stem: it grows out to the side
    depth = axis.depth + (1 if sideways else 0)
    if depth > MOST_DEPTH:
        return ["b"]
    rule = t.lays if depth + t.rule_depth <= MOST_DEPTH else t.lays_flat
    grown, depth, k = ["."], 0, 0
    while k < len(rule):
        tok = rule[k]
        if tok == "[" and depth == 0 and rng.random() < asleep:
            inner = 0
            while k < len(rule):
                inner += 1 if rule[k] == "[" else -1 if rule[k] == "]" else 0
                k += 1
                if inner == 0:
                    break
            grown.append(".")
            continue
        if tok == "F":
            grown.append("F")
            if rng.random() < 0.8 * d.shade:
                grown.append("F")
        else:
            depth += 1 if tok == "[" else -1 if tok == "]" else 0
            grown.append(tok)
        k += 1
    if not t.apex:
        grown.append("x")                                # a rule that does not carry the stem on: its tip is spent
    if sideways:
        side = "+" if shape.node[i] % 2 == 0 else "-"
        grown = ["[", side] + grown + ["]"]
    return grown


def _wake(tokens, shape, t, d, rng, year, edits, room, climbs=False) -> int:
    """Wake sleeping buds below every stem that has lost its tip. Returns how many woke below a cut.

    The plant answers all its losses together, on one growing day, not one
    stem at a time: so a hard pruning is answered in one line of the almanac.
    A stem that ends in bare wood, or in a sleeping bud, was cut; one that
    ends in x lost its tip to the weather, a mouth or its own rule, and wakes
    its buds without a word. When the plant `climbs` (a climber with
    something to climb), a woken shoot takes hold of it: it is written with a ^.
    """
    below_cut = 0
    if rng.random() > 0.25:
        return 0
    for axis in shape.axes:
        if axis is shape.top and not t.woody:
            continue                                     # a herb's crown wakes by the season (_crown_wakes)
        if axis.depth + 1 > MOST_DEPTH:
            continue
        at, end = shape.end(axis)
        if at is None or end in ("b", "*", "o"):
            continue                                     # a living tip, a fruit, a seed head: nothing lost
        sleeping = [i for i in axis.items if not isinstance(i, Axis) and tokens[i] == "."]
        if not sleeping:
            continue
        highest = shape.node[sleeping[-1]]
        if any(isinstance(item, Axis) and item.alive and item.pos >= highest for item in axis.items):
            continue                                     # a living branch above has taken the lead
        if any(not isinstance(i, Axis) and tokens[i] in "b*" and shape.node[i] >= highest for i in axis.items):
            continue
        woke = [sleeping[-1]] + ([sleeping[-2]] if len(sleeping) > 1 and rng.random() < 0.35 else [])
        woke = [i for i in woke if i not in edits]
        for i in woke:
            if room[0] < 5:
                return below_cut
            side = "+" if shape.node[i] % 2 == 0 else "-"
            edits[i] = ["[" + year, side] + (["^"] if climbs else []) + ["b", "]"]
            room[0] -= len(edits[i]) - 1
        if end in "F.":
            below_cut += len(woke)
    return below_cut


def _crown_wakes(tokens, shape, t, d, rng, year, edits, room, climbs=False) -> bool:
    """A herb in spring: its crown buds wake into stems, and last year's dead stems fall. True on the first day.

    New stems are always written after the ones already standing, so that
    old stems keep their names and nothing but the new is in the fresh ink.
    Where a stem stands along the crown is set by the way it leans (see
    _row): left-leaning stems to the left, right-leaning ones to the right,
    so the clump fans out and nothing crosses. A crown of two buds or more
    keeps one back; a crown of one sends up a stem only when nothing else
    stands, and keeps its bud. When the plant `climbs`, its new stems take
    hold (^) from the start.
    """
    if d.season != "spring":
        return False
    top = shape.top
    crown = [i for i in top.items if not isinstance(i, Axis) and tokens[i] == "." and shape.node[i] == 0]
    basal = [a for a in top.children if a.pos == 0]
    living = [a for a in basal if a.alive]
    if not crown or (len(crown) == 1 and living):
        return False
    waking = crown if len(crown) == 1 else crown[1:]    # the first crown bud is kept back
    leaning = {"+": 0, "-": 0}
    for axis in living:
        if axis.turns[:1] in leaning:
            leaning[axis.turns[:1]] += 1
    hold = ["^"] if climbs else []
    new = []
    for i in waking:
        if i in edits or rng.random() >= 0.08 * min(1.0, d.warm / 6.0):
            continue
        if room[0] - len(new) < 6:
            break
        if len(crown) > 1:
            edits[i] = []
        if not living and not new:
            new += ["[" + year] + hold + ["b", "]"]      # the first stem of the year stands upright
        elif leaning["+"] < leaning["-"] or (leaning["+"] == leaning["-"] and rng.random() < 0.5):
            new += ["[" + year, "+"] + hold + ["b", "]"]
            leaning["+"] += 1
        else:
            new += ["[" + year, "-"] + hold + ["b", "]"]
            leaning["-"] += 1
    if not new:
        return False
    room[0] -= len(new)
    first = not living
    if first:
        for axis in basal:                               # last year's stems fall
            for i in range(axis.open, axis.close + 1):
                edits.setdefault(i, [])
    last = basal[-1].close if basal else crown[-1]
    edits[last] = edits.get(last, [tokens[last]]) + new
    return first


def _shed(tokens, shape, t, rng, edits):
    """Now and then a dead twig falls off, or a snag breaks away (leaving a scar, x, where it was)."""
    dead = []
    for axis in shape.axes[1:]:
        if not axis.alive and (t.woody or axis.parent is not shape.top):
            dead.append((axis.open, axis.close, False))
    for axis in shape.axes:
        if t.woody and axis.alive and 0 <= axis.last_live < axis.nF:
            start = axis.fs[axis.last_live]
            dead.append((start, axis.close - 1 if axis.parent else len(tokens) - 1, True))
    if not dead:
        return
    start, end, scar = dead[rng.randrange(len(dead))]
    if any(i in edits for i in range(start, end + 1)):
        return
    for i in range(start, end + 1):
        if tokens[i][0] != "#":
            edits[i] = []
    if scar:
        edits[start] = ["x"]


def _poisson(rng, mean) -> int:
    if mean <= 0:
        return 0
    if mean > 30:
        return max(0, int(round(rng.gauss(mean, math.sqrt(mean)))))
    limit, k, p = math.exp(-mean), 0, 1.0
    while True:
        p *= rng.random()
        if p <= limit:
            return k
        k += 1


# ============================================================ what others ask

def flowers(body, seed, ctx) -> int:
    """How many flower heads are open today."""
    dead, tokens = read(body)
    return 0 if dead or hands.is_dead(body) else tokens.count("*")


def bitten(body, seed, ctx, share, by):
    """A bite of `share` of what is soft. Slugs take the lowest soft tips; a pony crops flat across the top.

    Thorns keep a pony and the slugs off altogether; any other mouth takes
    a fifth of what it would from a smooth bough.
    """
    body = _text(body)
    dead, tokens = read(body)
    if dead or hands.is_dead(body):
        return body, None
    t = Temper(seed)
    who = str(by or "something")
    pony = any(word in who.lower() for word in PONIES)
    if t.thorny and (pony or any(word in who.lower() for word in SLUGS)):
        return body, None
    share = _f(share, 0.0, 0.0, 1.0) * (0.2 if t.thorny else 1.0)
    if share <= 0:
        return body, None
    mind = _memory(body)
    rng = ctx.rng
    if pony:
        return _crop(body, tokens, t, ctx, share, who, mind)
    shape = Anatomy(tokens)
    soft = [i for i, tok in enumerate(tokens) if tok in "b*"]
    young = [] if t.woody else [a for a in shape.top.children if a.alive and a.nF <= 2]
    items = [(shape.height(i), "tip", i) for i in soft] + [(0, "stem", a) for a in young]
    if not items:
        return body, None
    take = int(share * len(items)) + (1 if rng.random() < (share * len(items)) % 1 else 0)
    if take <= 0:
        return body, None
    items.sort(key=lambda item: (item[0], rng.random()))
    edits, tips, stems = {}, 0, 0
    for _, what, item in items[:take]:
        if what == "tip":
            if item not in edits:
                edits[item] = ["x"]
                tips += 1
        else:
            for i in range(item.open, item.close + 1):
                edits[i] = []
            stems += 1
    grown = []
    for i, tok in enumerate(tokens):
        grown.extend(edits[i]) if i in edits else grown.append(tok)
    if not _alive(grown):
        return _dead(grown, ctx, "eaten by %s" % who, mind), "eaten to the ground by %s" % who
    said = None
    if stems:
        said = "%s ate %d young stem%s" % (who, stems, "" if stems == 1 else "s")
    elif tips >= 3:
        said = "%s ate %d soft tips" % (who, tips)
    return lay(grown, scent=_scent(t, grown), mind=mind), said


def _crop(body, tokens, t, ctx, share, who, mind=None):
    """A clean flat cut across the top: every stem that reaches above a height is cut there."""
    shape = Anatomy(tokens)
    seg, _ = walk(tokens, shape, t)
    tops = sorted((seg[a.fs[-1]][3] for a in shape.axes if a.fs), reverse=True)
    if not tops:
        return body, None
    k = max(1, min(len(tops), int(round(share * len(tops)))))
    level = max(0.5, tops[k - 1] - 0.5)
    cuts = []
    for axis in shape.axes:
        for j, i in enumerate(axis.fs):
            if seg[i][3] > level:
                cuts.append((i, axis.close if axis.parent else len(tokens)))
                break
    if not cuts:
        return body, None
    drop = set()
    for start, end in cuts:
        drop.update(i for i in range(start, end) if tokens[i][0] != "#")
    grown = [tok for i, tok in enumerate(tokens) if i not in drop]
    if not _alive(grown):
        return _dead(grown, ctx, "cropped by %s" % who, mind), "cropped to nothing by %s" % who
    return lay(grown, scent=_scent(t, grown), mind=mind), "cropped flat by %s" % who


def cast(body, seed, ctx):
    """Seed dropped today: a cross, if pollen of a like bough was carried to open flowers; else now and then its own.

    However many grains were brought, a day's pollen sets at most one
    crossed seed, and seldom: about one in a flowering season at the most,
    so that a plant's own seed, true to its variety, still comes up as often.
    """
    dead, tokens = read(body)
    if dead or hands.is_dead(body):
        return []
    t = Temper(seed)
    rng = ctx.rng
    birds = 0.25 if t.woody else 1.0                     # birds take most of a woody bough's fruit
    open_ = tokens.count("*")
    if open_:
        fathers = []
        for grain in list(getattr(ctx, "pollen", None) or [])[:24]:
            donor = getattr(grain, "seed", None)
            if isinstance(donor, str):
                donor = hands.read_keys(donor)
            if not isinstance(donor, dict) or hands.word(donor, "kind", "") != KIND:
                continue
            where = str(getattr(grain, "where", "") or "")
            if where and where == getattr(ctx, "where", None):
                continue
            them = Temper(donor)
            if them.growth != t.growth or them.form != t.form:
                continue                                 # too unlike to set seed
            fathers.append((donor, where))
        if fathers and rng.random() < min(CROSS_MOST, 0.001 * open_) * birds:
            donor, where = fathers[rng.randrange(len(fathers))]
            return [_crossed(seed, donor, rng, getattr(ctx, "where", "") or "", where or "another bough")]
    heads = tokens.count("o")
    month = getattr(getattr(ctx, "date", None), "month", 9)
    if heads and RIPE <= month <= 11:                    # the seed is ripe from August until the frosts
        chance = min(0.005, 0.00025 * heads) * birds     # a seed a year or so
        if rng.random() < chance:
            return [_own_seed(seed)]
    return []


def _own_seed(seed) -> str:
    """A seed true to its parent: the same rule, the same temperament, the same variety."""
    keys = {}
    for key in KEPT + ("variety",):
        said = hands.line(seed, key, "") or (hands.line(seed, "color", "") if key == "colour" else "")
        if said:
            keys[key] = said
    keys["kind"] = KIND
    return hands.write_keys(keys)


def _crossed(mother, father, rng, mother_at, father_at) -> str:
    """A crossed seed: numbers blended, colours mixed, each word from one parent or the other, no variety."""
    tm, tf = Temper(mother), Temper(father)
    blend = rng.uniform(0.3, 0.7)
    keys = {"kind": KIND}
    for key in KEPT[1:]:
        if key in NUMBERS:
            a, b = getattr(tm, key), getattr(tf, key)
            value = round(a + (b - a) * blend, NUMBERS[key])
            keys[key] = ("%d" % value) if NUMBERS[key] == 0 else ("%g" % value)
        elif key == "colour":
            keys[key] = hands.mix(tm.colour, tf.colour, blend)
        elif key == "fruit":
            keys[key] = hands.mix(tm.fruit, tf.fruit, blend)
        elif key in WORDS:
            said = hands.line(mother if rng.random() < 0.5 else father, key, "")
            if said:
                keys[key] = said
    keys["from"] = "cross of %s × %s" % (mother_at, father_at)
    return hands.write_keys(keys)


def describe(body, seed, ctx) -> str:
    """One short line: '84 lengths, 6 in flower'; 'a crown of 5 sleeping buds'; 'dead: frost'."""
    dead, tokens = read(body)
    if dead or hands.is_dead(body):
        said = (dead or "").lstrip(DAGGER + " ")
        return "dead" + (": " + said[10:].strip(" ,") if len(said) > 10 else "")
    t = Temper(seed)
    shape = Anatomy(tokens)
    wood, open_, heads = tokens.count("F"), tokens.count("*"), tokens.count("o")
    crown = sum(1 for i in shape.top.items if not isinstance(i, Axis) and tokens[i] == "." and shape.node[i] == 0)
    if not t.woody and not any(a.alive for a in shape.top.children):
        return "a crown of %d sleeping bud%s, resting" % (crown, "" if crown == 1 else "s")
    parts = ["%d length%s" % (wood, "" if wood == 1 else "s")]
    if not t.woody:
        stems = sum(1 for a in shape.top.children if a.alive)
        parts[0] += " on %d stem%s" % (stems, "" if stems == 1 else "s")
    if open_:
        parts.append("%d in flower" % open_)
    if heads:
        one = heads == 1
        if not t.woody:
            what = "seed head" if one else "seed heads"
        elif t.form == "umbel":
            what = "bunch of fruit" if one else "bunches of fruit"
        elif t.form == "spike":
            what = "spike of fruit" if one else "spikes of fruit"
        else:
            what = "fruit"
        parts.append("%d %s" % (heads, what))
    return ", ".join(parts)


def size(body, seed) -> float:
    """For its dot on the plan: its lengths, and half a length for the crown they grow from."""
    dead, tokens = read(body)
    return tokens.count("F") + 0.5


# ================================================================ the drawing

def _bend(h, reach) -> float:
    """A heading bent a little towards the sky (reach > 0) or the ground (reach < 0)."""
    if not reach:
        return h
    target = 90.0 if reach > 0 else -90.0
    turn = (target - h + 180.0) % 360.0 - 180.0
    return h + turn * abs(reach)


def _row(shape) -> dict:
    """Where each stem from the crown stands along it, in lengths from the middle, by the index of its '['.

    Left-leaning stems stand to the left in the order they are written,
    right-leaning ones to the right, upright ones about the middle. A stem's
    place depends only on the stems written before it, and new stems are
    written last, so a stem that comes up never moves one that stood.
    """
    x, count = {}, {"+": 0, "-": 0, "": 0}
    for axis in shape.top.children:
        if axis.pos != 0:
            continue
        lean = axis.turns[:1] if axis.turns[:1] in ("+", "-") else ""
        k = count[lean]
        count[lean] += 1
        if lean == "+":
            x[axis.open] = -(k + 1) * ROW
        elif lean == "-":
            x[axis.open] = (k + 1) * ROW
        else:
            x[axis.open] = ((k + 1) // 2) * (ROW / 3.0) * (1 if k % 2 else -1)
    return x


def walk(tokens, shape, t):
    """Lay the body out in plant units, as a turtle would. Returns ({F index: (x1, y1, x2, y2)}, {other: (x, y, heading)}).

    A climber's wood lies down (it bends towards the ground, then runs along
    it) except what grew on from a ^, where it took hold of its support.
    """
    row = _row(shape)
    up = t.habit != "climber"
    seg, at, stack = {}, {}, []
    x = y = 0.0
    h = 90.0
    for i, tok in enumerate(tokens):
        head = tok[0]
        if head == "F":
            r = math.radians(h)
            nx, ny = x + math.cos(r), y + math.sin(r)
            if ny < 0.0:                                 # it meets the ground and runs along it
                ny = 0.0
                h = 0.0 if math.cos(r) >= 0 else 180.0
                nx = x + (1.0 if h == 0.0 else -1.0)
            else:
                h = _bend(h, t.reach if up else SPRAWL)
            seg[i] = (x, y, nx, ny)
            x, y = nx, ny
        elif head == "+":
            h += t.angle
        elif head == "-":
            h -= t.angle
        elif head == "^":
            up = True
        elif head == "[":
            stack.append((x, y, h, up))
            if i in row:
                x = row[i]
        elif head == "]":
            if stack:
                x, y, h, up = stack.pop()
        else:
            at[i] = (x, y, h)
    return seg, at


def _hex(ink):
    """An ink as (r, g, b), through hands.mix; None if it cannot be read."""
    said = hands.mix(ink, ink)
    try:
        return int(said[1:3], 16), int(said[3:5], 16), int(said[5:7], 16)
    except Exception:
        return None


def _close(a, b, within=60) -> bool:
    """Are two inks so close that one would not show on the other?"""
    a, b = _hex(a), _hex(b)
    return a is not None and b is not None and sum(abs(p - q) for p, q in zip(a, b)) < within


def _faded(colour) -> str:
    """The collar of a seed head: the flowers' colour faded. A pale colour fades to grey, so it still shows."""
    if _close(colour, PAPER, 150):
        return hands.mix(colour, "#9a948a", 0.45)
    return hands.mix(colour, PAPER, 0.5)


def draw(body, seed, ctx, pen) -> None:
    """The plate: wood by the pipe rule, fresh wood in the fresh ink, flowers in their colour. See the docstring."""
    t = Temper(seed)
    dead_line, tokens = read(body)
    gone = bool(dead_line) or hands.is_dead(body)
    mind = _memory(body)
    shape = Anatomy(tokens)
    seg, at = walk(tokens, shape, t)
    row = _row(shape)
    pen.unit_name = "length, lengths"
    pen.ground(0)

    left = getattr(ctx, "left", None)
    before = None if left is None else Anatomy(read(left)[1], feel=False).wood()
    shape.wood()                                         # (names this body's wood the same way, to compare)

    # how big a pixel is in plant units, so that heads and barbs keep their size on the page
    xs = [p for s in seg.values() for p in (s[0], s[2])] + [p[0] for p in at.values()] + [0.0]
    ys = [p for s in seg.values() for p in (s[1], s[3])] + [p[1] for p in at.values()] + [0.0]
    width, height = max(xs) - min(xs), max(ys) - min(ys)
    pen.unit_px_max = UNIT_PX_MAX
    scale = min(UNIT_PX_MAX, 700.0 / max(width, 0.3), 780.0 / max(height, 0.3))
    px = 1.0 / scale
    small = max(0.6, min(1.0, scale / 60.0))            # heads are drawn smaller on a plant drawn small

    ink_of = {}
    for axis in shape.axes:
        carried = [0] * (axis.nF + 1)
        for child in axis.children:
            carried[min(child.pos, axis.nF)] += child.tips
        above = 1
        for j in range(axis.nF - 1, -1, -1):
            above += carried[j + 1]
            i = axis.fs[j]
            if gone or not axis.alive or j >= axis.last_live:
                ink = "dead"
            elif before is None or (axis.key, j) not in before:
                ink = "fresh"
            else:
                ink = "wood"
            weight = min(18.0, max(2.0, (2.4 if t.woody else 2.1) * math.sqrt(above)))
            ink_of[i] = (ink, weight)

    def below(axis, node):
        """The ink of the wood just under a node."""
        while axis is not None:
            if node > 0 and axis.fs:
                return ink_of[axis.fs[min(node, axis.nF) - 1]][0]
            node, axis = axis.pos, axis.parent
        return "dead" if gone else "wood"

    def weight_at(axis, node):
        """How heavy the stroke is where a node sits: the wood above and below it, and at a branch's foot its parent."""
        w = 2.0
        while axis is not None:
            if axis.fs:
                if node < axis.nF:
                    w = max(w, ink_of[axis.fs[node]][1])
                if node > 0:
                    w = max(w, ink_of[axis.fs[min(node, axis.nF) - 1]][1])
            if node > 0 or axis.parent is None:
                return w
            node, axis = axis.pos, axis.parent
        return w

    # the wood, heaviest first so the fine twigs lie on top
    for i in sorted(ink_of, key=lambda i: -ink_of[i][1]):
        ink, weight = ink_of[i]
        x1, y1, x2, y2 = seg[i]
        if y1 <= 0.0 < y2:                               # a foot on the ground: its round end kept above the ground
            span = math.hypot(x2 - x1, y2 - y1)
            lift = min(0.5 * span, 0.5 * weight * px) / max(span, 1e-9)
            x1, y1 = x1 + (x2 - x1) * lift, y1 + (y2 - y1) * lift
        pen.line(x1, y1, x2, y2, weight, ink)
        if t.thorny and weight <= 6.5:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            h = math.degrees(math.atan2(y2 - y1, x2 - x1)) + (55 if shape.node[i] % 2 else -55)
            r = math.radians(h)
            pen.line(mx, my, mx + math.cos(r) * 8 * px, my + math.sin(r) * 8 * px, 2, ink)

    # the crown, over the feet of its stems, with its sleeping buds in the gaps between them
    basal = [a for a in shape.top.children if a.pos == 0]
    crown = [i for i in shape.top.items if not isinstance(i, Axis) and tokens[i] == "." and shape.node[i] == 0]
    if crown or basal:
        feet = [(row.get(a.open, 0.0), ink_of[a.fs[0]][1] if a.fs else 2.0) for a in basal]
        if shape.top.fs:
            feet.append((0.0, ink_of[shape.top.fs[0]][1]))
        spread = [f for f, _ in feet] or [0.0]
        low, high = min(spread) - 0.3, max(spread) + 0.3
        spots, x = [], low + 6 * px
        for _ in range(4000):
            if len(spots) >= len(crown):
                break
            clear = all(abs(x - f) >= (w / 2 + 6) * px for f, w in feet)
            if clear and (not spots or x - spots[-1] >= 12 * px):
                spots.append(x)
                x += 12 * px
            else:
                x += 2 * px
        if spots:
            high = max(high, spots[-1] + 6 * px)
        pen.line(low, 0, high, 0, 8, "dead" if gone else "wood")
        for x in spots:
            pen.dot(x, 0, 3.2, "dead" if gone else "white")

    # cut ends: two short slanting strokes across the end that was taken off (a thorn is one, from the side)
    for axis in shape.axes:
        at_end, end = shape.end(axis)
        if end == "." and axis.fs and shape.node[at_end] == axis.nF:
            at_end, end = axis.fs[-1], "F"                   # cut just above a sleeping bud: the cut is at the wood's end
        if end == "F" and at_end in seg:
            x1, y1, x2, y2 = seg[at_end]
            ink, weight = ink_of[at_end]
            along = math.atan2(y2 - y1, x2 - x1)
            r = along + math.radians(45)
            reach = (weight / 2 + 5) * px
            for back in (0.0, 5.0 * px):
                cx, cy = x2 - math.cos(along) * back, y2 - math.sin(along) * back
                pen.line(cx - math.cos(r) * reach, cy - math.sin(r) * reach,
                         cx + math.cos(r) * reach, cy + math.sin(r) * reach, 2.0, ink)

    # sleeping buds (rings beside the stem, clear of its stroke) and buds (dots)
    thin = tokens.count("F") > MANY_RINGS
    highest = {}
    if thin:
        for i, tok in enumerate(tokens):
            if tok == "." and not (shape.axis[i] is shape.top and shape.node[i] == 0):
                highest[id(shape.axis[i])] = i           # written in order up the stem: the last is the highest
    for i, (x, y, h) in at.items():
        tok = tokens[i]
        axis = shape.axis[i]
        if tok == ".":
            if axis is shape.top and shape.node[i] == 0:
                continue                                 # a crown bud: drawn on the crown
            if thin and highest.get(id(axis)) != i:
                continue
            node = shape.node[i]
            if y <= 1e-9:                                # at the ground: lifted clear of the crown, up its own stem
                a = math.radians(h)
                x, y = x + math.cos(a) * 9 * px, y + max(0.0, math.sin(a)) * 9 * px
            off = (weight_at(axis, node) / 2 + 3 + 1.5) * px
            r = math.radians(h + (90 if node % 2 == 0 else -90))
            pen.dot(x + math.cos(r) * off, max(7 * px, y + math.sin(r) * off), 3.0, below(axis, node),
                    filled=False, weight=1.6)
        elif tok == "b":
            pen.dot(x, y, 3.6, below(axis, shape.node[i]))

    # flowers and seed heads
    inks = {"wood": None, "fresh": "#2e9e3f", "dead": "#9a948a"}
    try:
        inks = {name: pen.canvas.inks.get(name, said) for name, said in inks.items()}
    except Exception:
        pass
    month = getattr(getattr(ctx, "date", None), "month", None)
    fruit = t.fruit if not _ripening(t, month) else hands.mix(t.fruit, PAPER, 0.55)
    for i, (x, y, h) in at.items():
        tok = tokens[i]
        if tok in "*o" and not gone:
            ink = t.colour if tok == "*" else fruit
            halo = _close(ink, inks.get(below(shape.axis[i], shape.node[i])))   # it would not show on its own wood
            _head(pen, x, y, h, t, px, ink, tok == "*", gone, small, halo)
        elif tok in "*o":
            _head(pen, x, y, h, t, px, "dead", tok == "*", gone, small, False)

    pen.note(describe(body, seed, ctx))
    if not gone:
        if t.habit == "climber":
            if "^" in tokens:
                pen.note("climbing %s" % (mind["climbing"] or "its support"))
            else:
                near = climbing(t, ctx)
                pen.note("it sprawls, but will take hold of %s" % near if near else "nothing to climb here: it sprawls")
        elif 1.0 - hands.num(getattr(ctx, "bed", None) or {}, "light", 1.0, 0.0, 1.0) / t.sun > 0.25:
            pen.note("in shade here: it grows long and sparse")
        scent = _scent(t, tokens)
        if scent:
            pen.note("in flower and scented %s" % scent)


def _head(pen, x, y, h, t, px, ink, open_, gone, small=1.0, halo=False):
    """One flower head (open_) or seed head, in its form, at a tip heading h.

    Open flowers are filled dots; seed heads and fruit are rings, smaller and
    set apart, so the two are never mistaken for each other. `small` shrinks
    the figure (not its dots) on a plant drawn small; `halo` sets each dot on
    a rim of clear paper, for a colour that would not show on the wood.
    """
    r = math.radians(h)
    ux, uy = math.cos(r), math.sin(r)
    cx, cy = x + ux * 4 * px, y + uy * 4 * px
    dots = []                                            # (x, y, radius, filled, weight): drawn last, over their halos

    def spoke(angle, inner, outer, weight, colour):
        a = math.radians(angle)
        pen.line(cx + math.cos(a) * inner * px, cy + math.sin(a) * inner * px,
                 cx + math.cos(a) * outer * px, cy + math.sin(a) * outer * px, weight, colour)

    def around(angle, distance):
        a = math.radians(angle)
        return cx + math.cos(a) * distance * px, cy + math.sin(a) * distance * px

    if t.form == "single":
        dots.append((x + ux * 7 * px, y + uy * 7 * px, 7.0 if open_ else 6.0, open_, 2.5))
        extent = 10.0
    elif t.form == "spike":
        extent = 40.0 * small
        pen.line(x, y, x + ux * extent * px, y + uy * extent * px, 2, ink)
        for k in range(5 if open_ else 3):
            d = (8 + (8 if open_ else 13) * k) * small * px
            dots.append((x + ux * d, y + uy * d, 4.4 - 0.3 * k if open_ else 4.0, open_, 2.0))
        extent = 12.0
    elif open_:                                          # an umbel in flower: five florets on short rays, clear of each other
        reach = 14.5                                     # (9 px between florets: room for the rim a pale one is given)
        for k in range(5):
            a = h - 72 + 36 * k
            spoke(a, 0, reach, 1.5, ink)
            dots.append(around(a, reach) + (3.0, True, 2.0))
        extent = reach + 3.0
    else:                                                # three seeds or fruit on a small fork
        reach = max(9.0, 11.0 * small)
        for a in (h - 38, h, h + 38):
            spoke(a, 0, reach - 3.0, 1.8, ink)
            dots.append(around(a, reach) + (3.4, False, 2.0))
        extent = reach + 3.4

    if t.papery:                                         # the starry collar of bracts, round the head
        ruff = "dead" if gone else (t.colour if open_ else _faded(t.colour))
        inner = extent + 2.5
        outer = inner + max(5.0, 8.0 * small)
        for k in range(13):
            if t.form != "spike" or abs(18 * k - 108) > 30:        # (not across a spike's own stalk)
                spoke(h - 108 + 18 * k, inner, outer, 2.2, ruff)
    if halo:
        for dx, dy, radius, _, _ in dots:
            pen.dot(dx, dy, radius + 1.8, "paper")
    for dx, dy, radius, filled, weight in dots:
        pen.dot(dx, dy, radius, ink, filled=filled, weight=weight)
