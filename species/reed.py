"""
Reed: a stand of hollow stems from one rootstock. A dry reed is a pipe, and
the wind plays it.

A reed is made of notes. Each stem is written in its body as the note it
sounds. A stem is a pipe closed at its foot by a node and open at the top,
and such a pipe sounds at 8,575 / (its length in cm) hertz: a stem of
116.8 cm is a D2, one of 58.4 cm is a D3, an octave higher. So the note is
the stem, and its length follows from it. As a green stem grows, its note
falls; a stem that is cut rises.


A SEED says, line by line:

    kind: reed
    ear: D F A C    the notes it listens for, in any octave: letter names
                    (C, F#, Bb) or do re mi fa sol la si (ré, sib, fa#).
                    An octave number (C4) may be written; it is not heard.
                    'any' as the first word is all twelve notes; 'none'
                    makes a deaf reed. Words after the notes are a remark.
                    Set it off with a comma, a bracket or a dash: past
                    such a mark the reading goes on only if every word up
                    to the next mark is a note, so 'mi sol si re, a chord
                    for the pond' hears no A. A remark run straight on
                    from the notes is read until two words running are
                    not notes, and its first word is heard if it is a
                    note's name (a, la, si, do).
    wall: thin      thin or thick:
                      thin   sounds in the lightest air (a wind of 2.5),
                             but a gale may break it;
                      thick  sounds only in a wind of 4, grows a little
                             slower, and stands up to gales.
    root: clumping  clumping or running. A running rootstock sends up a new
                    reed nearby now and then in summer.
    plume: violet   the colour of its flowering plumes: an ink of the plate
                    (violet, brown, orange...) or a #rrggbb
    scent: dusk     (if it is there) the plumes smell at dusk: moths come
    hardy: -18      the night, in °C, that kills the rootstock (-1 at the
                    mildest: a reed does not die of a cool night)
    variety: <name> (if a visitor gave it one) carried on by seed that was
                    not crossed, and by runners
    start: seed     written by the days on every seed a reed lets go (a hand
                    may write it too): it comes up as a seedling, which has
                    still to take root (see HOW IT LIVES). Without it, what
                    is planted is a piece of rootstock, rooted from the
                    first day. A runner is always rootstock.

Nothing else in the seed is read. What cannot be read is taken from what is
written here (an unreadable ear is C D E G A).


THE BODY, for example:

    # a reed of 6 stems, 3 of them green; 5 buds in the rootstock
    heard: D2 A2 E3 on 2027-01-14
    dry stems:
      stem 2    D2        (116.8 cm)   topped, in seed
      stem 1    A2        (78.0 cm)    topped
      stem 3    F3 -38    (50.2 cm)    broken by a gale
    green stems:
      stem 7    E2        (104.1 cm)   topped, in plume
      stem 8    F#2 +12   (92.1 cm)    growing to D2
      stem 9    A#3 -20   (37.2 cm)    growing
    rootstock: 5 buds

  * The line beginning # is only a summary, rewritten every day.
  * heard: the chord the wind last played on it, and the day it did.
  * Under 'dry stems:' and 'green stems:', one line to a stem, from the
    lowest note to the highest. 'stem 8' is its number: the eighth shoot
    it ever sent up. Then its note: a letter, # for a sharp, the octave (C4
    is middle C), and how far off that note it is in cents (hundredths of
    a semitone). Only the note is the stem. The length in brackets is
    written out for you, and is read only as a witness to how long the
    stem was when the days last wrote it (see TO CUT IT).
  * Then how it stands:
      growing               still lengthening (to <note>, once it knows
                            where it will stop);
      topped                it stopped at the note it chose;
      cut                   a hand cut it;
      cropped by <who>      something ate its top;
      broken by a gale;
      stopped by the cold   the autumn came before it found its note;
      stopped by a hand     a hand moved it among the dry stems while it
                            was still growing, or wrote it there.
    in plume: in flower. in seed: the plume has gone to seed.
  * rootstock: how many buds wait in the ground for the spring.
  * seedling: not yet rooted. Only on a reed come up from seed that has
    not yet taken root; the summary line then calls it a seedling. Delete
    the line (or write 'seedling: no') and it is taken to have rooted.


HOW IT LIVES. In spring, once the days are longer than twelve and a half
hours and mild, the buds come up as shoots, a few at a time, over some
weeks. Each green stem grows by the day's warmth, light and the wetness of
the ground, faster where the ground is rich; the first shoots of a spring
are the strongest, and each later one is a little weaker. Reeds like wet
feet: the pond edge suits them; dry stones and deep shade keep them short,
and so high in the voice.

After midsummer, once the days are shorter than fifteen and a half hours,
a growing stem that is at least 20 cm tall listens. Of the notes of its ear
at or below it, no further down than a fifth, it takes the nearest whose
letter no stem of this year's stand has taken; if every one has been taken,
the one the fewest stems stand on (and if its ear has no note within a
fifth, the nearest note of its ear). It counts the stems of every reed in
its bed. It grows to that note, stops there exactly, and comes into plume. So a
stand fills out its chord before it doubles a note, and two reeds in one
bed share a chord between them. A stem may not get there: the first cold
of autumn (a frost, or a day colder than 6° on average) dries every green
stem, and one still growing stops where it is, out of tune. As the new
stems dry, last year's fall. So the stand the wind plays through a winter
is the one that grew that summer.

The wind plays the dry stems. Shelter takes the wind away: at the foot of
the north wall a reed is never heard. Once every stem is dry, the almanac
hears the reed on a day the wind plays a chord it has not played since it
was last heard. A gale (a wind of 5) may break a dry stem, which is then
shorter, and higher. A late frost can take young shoots.

Mouths find little to eat in a reed. Slugs, snails, voles and most small
creatures find only the young shoots soft, under 25 cm, and eat them whole,
the smallest first; a taller stem is cane to them. The bud of a shoot eaten
goes back into the rootstock, to come up again later and weaker (or, after
midsummer, next spring). A grazer (a pony, a horse, a deer) crops the
green stems flat, and a cropped stem grows no more.

What the rootstock has for next spring comes from the stems it grew: a
stem that topped out feeds it best, one stopped by the cold less, one cut,
cropped or broken while green hardly at all. A rootstock with no buds left
makes one on a frosty night of autumn or winter. A rooted reed is hard to
kill: only a frost past its hardy line does it.

Its plumes, when bees or moths have brought another reed's pollen, may
drop a crossed seed; seed heads let a little seed go on the winter wind;
a running rootstock sends up a new reed nearby, now and then in summer.
All of these come more rarely as the other reeds of its bed grow in
number, and not at all once they fill a third of the bed's room. So a
stand leaves the rest of its bed to other kinds.

A seed comes up as a seedling: one bud in the ground, and no rootstock
yet. It takes root on the first cold day of an autumn once it has stood
a stem through the summer, and until then it is easily lost. On each day
of spring and summer it may dry out, the likelier the drier its bed (the
water: line of the bed's file) and the drier the day: at the pond edge
it never does; in ordinary ground (water 1) about two in three are lost
before they root; in a drier bed most are, and at the foot of the north
wall (water 0.7) nearly all. And wherever the rooted reeds of
its bed, not counting itself, already fill a third of the bed's room,
it is crowded out. So the wild corner, where so much seed lands, is not
filled with reeds. A seedling sets no seed until it has rooted.

A cross takes the notes both parents' ears share, and the first note each
has that the other has not; its plume is the two colours blended; its wall
and root are one parent's or the other's. A crossed seed carries no
variety.


TO CUT IT. A reed is the easiest thing in the garden to cut, and the most
exacting to tune. Each stem is one line, and to cut a stem is to raise its
note:
  * write a higher note on its line, or write 'to <note>' after it: it is
    cut to that note (never shorter than 1 cm). A cut stem grows no more,
    green or dry: it holds that note. The days know a higher note for a
    cut by the bracket beside it, which still gives the old length; if you
    rewrite the bracket as well, they take it that the stem always stood
    so, and it goes on as it was.
  * write 'to <note>' after a green stem that is still growing, lower than
    it now stands, and it grows to that note and stops there;
  * write a lower note and the stem is longer. No knife could do that, but
    a hand in this garden can. It goes on as it was.
  * delete its line and it is gone. Delete the rootstock line and it is
    read as one bud.
A cut is on the plate at once. The stems still growing seek the notes that
are left. Cutting dry stems in winter costs the reed nothing: it is the
harvest. Cutting green stems in summer takes from next year's buds. Move a
line from 'green stems:' to 'dry stems:' to dry it at once, or the other way
to make it green again.


THE PLATE. Nothing is drawn that is not in the body.

  * Each stem stands on the faint ground line, as tall as it is: the dry
    stems on the left, the green on the right, each group from the lowest
    note (the longest) to the highest. Only the heights are to scale: the
    stems are spaced for reading.
  * A green stem is one solid stroke: full of sap, it cannot sound. A dot
    at its tip: it is still growing.
  * A dry stem is drawn as a tube: two walls with the paper between,
    closed at the foot by a bar (the node) and open at the top. A thin
    wall is one fine line; a thick wall is a doubled line.
  * The top of a stem says how it stopped. Bare: it topped out at its
    note (and has let its seed go, or never flowered). A flat bar across
    the top (on a tube, a flat rim on each wall, the bore left open): cut,
    or cropped. Ragged, the walls ending at two heights: broken by a gale.
    A small ring: stopped before it found its note, by the cold or by a
    hand.
  * A fan of bold strokes standing up from the top, in the plume's
    colour: in plume. A finer, paler plume nodding over to one side: gone
    to seed. (A plume too pale to show on the paper is drawn a shade
    deeper.)
  * Over each stem, its note. In brackets, (E2), if the stem is green and
    silent; plain if it is dry and the wind can play it. A + or - after the
    note: more than 15 cents sharp or flat. Where a stand is so crowded
    that a note cannot be lettered over its own stem, it is left out; the
    body has every note.
  * Under the ground, the rootstock, with a dot for each bud waiting for
    spring (its depth and length are not to scale). A clumping rootstock
    ends square beyond its outermost stems. A running one reaches on past
    the stand and turns up at each end, where it will send up a new reed.
    A seedling not yet rooted has no rootstock: only a thread of root, a
    fine broken line, with its bud on it.
  * Green ink is what has grown since the last visit ended (new stems, new
    length, new buds): it says when a stem grew, not whether it is green.
    A dead reed is drawn all in the pale dead ink, its lettering too.
  * The bar at the bottom left says how many cm. Scent is not drawn.
"""

import datetime
import math
import re

import hands

KIND = "reed"
SPEED = 8575.0             # 34,300 cm/s over 4: a pipe closed at its foot sounds at SPEED / length (cm) hertz
NAMES = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
LETTERS = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}
SOLFEGE = {"do": 0, "ut": 0, "re": 2, "ré": 2, "mi": 4, "fa": 5, "sol": 7, "so": 7, "la": 9, "si": 11, "ti": 11}
DEFAULT_EAR = [0, 2, 4, 7, 9]      # C D E G A
LOWEST, HIGHEST = 16.69, 120.41    # the notes of a stem 400 cm long and of one 1 cm long
SHOOT = 3.0                # cm, a shoot on the day it comes up
MOST_BUDS = 12
MOST_STEMS = 40            # stem lines read; a reed grows at most 2 x MOST_BUDS
SOUNDS_AT = {"thin": 2.5, "thick": 4.0}
BREAKS = {"thin": 0.20, "thick": 0.04}      # the chance, on a gale day, that one dry stem breaks
GALE = 5.0
REACH = 7                  # semitones: a stem listens for a free note no further below it than a fifth
LISTENS = 20.0             # cm: a shoot shorter than this does not listen yet
RIPE = 15.5                # hours: after midsummer, once the days are shorter than this, the stems listen
FEEDS = {"topped": 2.0, "stopped": 1.2}     # buds a green stem gives the rootstock as it dries; anything else 0.4
SOFT = 25.0                # cm: a growing shoot shorter than this is soft right through; a taller stem is cane
CROSSES = 0.02             # the chance, on a day reed pollen was carried to it, that each open plume (up to three)
                           # sets a crossed seed. A rooted reed lives for ever unless a hard frost takes it, so every
                           # cross that roots is a lasting neighbour: at 0.06 a reed in a garden of hoverflies set
                           # several a summer.
HEADS = 0.0015             # the chance, on a windy day of autumn or winter, that each seed head lets a seed go
RUNS = 0.006               # the chance, on a summer day, that a running rootstock of 4 buds and stems or more runs
                           # (all three are held back as the other reeds of the bed fill their third: see _room_left)
WITHERS = 0.025            # a seedling's chance of drying out, on a spring or summer day, in the driest bed and the
                           # driest day; less by the square of how much drier than THIRSTY its bed is (see _withers)
THIRSTY = 1.5              # the water of a bed (the pond edge is 1.7) at which a seedling never dries out
TUNED = 15.0               # cents: a note further off than this is out of tune (and a bracket that far out, a cut)
KEPT = ("kind", "ear", "wall", "root", "plume", "scent", "hardy", "variety")     # a cast seed's own lines; not
                                                                                 # 'start', which cast() decides
GRAZERS = ("pony", "poney", "horse", "cheval", "chevaux", "jument", "mare", "donkey", "âne",
           "deer", "cerf", "chevreuil", "roe", "cow", "vache", "sheep", "mouton", "brebis", "goat", "chèvre")

_PITCH = r"(do|ut|ré|re|mi|fa|sol|la|si|ti|[a-g])([#♯b♭]?)(-?\d)(?![\d.])"
_NOTE = re.compile(r"(?<![^\W\d_])" + _PITCH, re.I)
_TO = re.compile(r"\bto\s+" + _PITCH, re.I)
_CENTS = re.compile(r"\s*([+\-−–])\s*(\d{1,2})(?![\d.])")
_NUMBER = re.compile(r"\bstem\s*(\d{1,4})", re.I)
_LEADING = re.compile(r"^\s*(\d{1,4})\b")
_BRACKET = re.compile(r"\(\s*(\d{1,3}(?:[.,]\d{1,3})?)\s*cm\s*\)", re.I)
_EAR_WORD = re.compile(r"(do|ut|ré|re|mi|fa|sol|so|la|si|ti|[a-g])([#♯b♭]*)(-?\d)?$")
_EAR_TURNS = {"flat": -1, "bémol": -1, "bemol": -1, "sharp": 1, "dièse": 1, "diese": 1,
              "natural": 0, "naturel": 0, "bécarre": 0, "becarre": 0}
_EAR_JOINS = ("and", "et", "or", "ou", "then", "puis", "&")
_EAR_MARKS = re.compile(r"[,;:/()\[\]{}·+…—–\-.!?|]+")      # clause marks: what follows one may be a remark
_EAR_OCTAVE = re.compile(r"\d{1,2}$")                       # an octave number written apart from its note
_DATE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
_BY = re.compile(r"\bby\s+([^,;()]{1,40})", re.I)


# ------------------------------------------------------------------ notes

def _length(m) -> float:
    """The length in cm of a stem that sounds midi note m."""
    return SPEED / (440.0 * 2.0 ** ((m - 69.0) / 12.0))


def _midi(length) -> float:
    """The note (midi, with its fraction) a stem of this many cm sounds; kept to the cent."""
    length = min(400.0, max(1.0, length))
    return round(69.0 + 12.0 * math.log2(SPEED / length / 440.0), 2)


def _name(m) -> str:
    k = int(round(m))
    return NAMES[k % 12] + str(k // 12 - 1)


def _cents(m) -> int:
    return int(round((m - round(m)) * 100))


def _note(m) -> str:
    """A note as the body writes it: 'F#2 +12', or 'D2' when it is true."""
    cents = _cents(m)
    return _name(m) + (" %+d" % cents if cents else "")


def _heard_name(m, dry) -> str:
    """A note as the plate letters it: + or - if more than 15 cents off; in brackets if the stem is silent."""
    cents = _cents(m)
    said = _name(m) + ("+" if cents > TUNED else "-" if cents < -TUNED else "")
    return said if dry else "(%s)" % said


def _pitch_class(word, accidental) -> int:
    word = word.lower()
    pc = SOLFEGE[word] if word in SOLFEGE else LETTERS.get(word[:1], 0)
    for mark in accidental or "":
        pc += 1 if mark in "#♯" else -1
    return pc


def _pitch(found, start=1) -> float:
    """A midi note from a match of _PITCH (its groups from `start`), kept between LOWEST and HIGHEST."""
    pc = _pitch_class(found.group(start), found.group(start + 1))
    octave = int(found.group(start + 2))
    return float(min(HIGHEST, max(LOWEST, (octave + 1) * 12 + pc)))


# ------------------------------------------------------------------ the seed

def _ear_remark(word) -> bool:
    """Whether a word of the ear line is none of: a note, a sharp or flat, an 'and', a bare octave number."""
    return not (_EAR_WORD.match(word) or word in _EAR_TURNS or word in _EAR_JOINS or _EAR_OCTAVE.match(word))


def _ear(seed) -> list:
    """The pitch classes it listens for, in the order written. [] for a deaf reed.

    The first word may say 'any' (all twelve) or 'none' (deaf). Otherwise
    each word that is a note is taken, with any octave number dropped;
    'flat' and 'sharp' (bémol, dièse) turn the note before them; 'and' is
    passed over. Two words running that are none of these end the reading:
    what follows is a remark, like the gloss beside the ear in the docstring.
    A clause mark (a comma, a bracket, a dash...) once a note has been read
    ends it too, unless every word up to the next mark is a note: so in
    'mi sol si re, a chord for the pond' the remark's 'a' is not an A.
    """
    text = hands.line(seed, "ear", "").lower()
    pieces = [[w.strip("'\"!?") for w in piece.split()] for piece in _EAR_MARKS.split(text)]
    pieces = [[w for w in piece if w] for piece in pieces]
    pieces = [piece for piece in pieces if piece]
    if not pieces:
        return list(DEFAULT_EAR)
    if pieces[0][0] in ("none", "deaf", "nothing", "rien", "sourd"):
        return []
    if pieces[0][0] in ("any", "all", "every", "chromatic", "tout", "toutes"):
        return list(range(12))
    raw, unread = [], 0
    for piece in pieces:
        if raw and any(_ear_remark(word) for word in piece):
            break                       # past a clause mark, a stretch with a word that is no note is a remark
        for word in piece:
            found = _EAR_WORD.match(word)
            if found:
                raw.append(_pitch_class(found.group(1), found.group(2)))
                unread = 0
            elif word in _EAR_TURNS:
                if raw:
                    raw[-1] += _EAR_TURNS[word]
                unread = 0
            elif _ear_remark(word):
                unread += 1
                if unread >= 2:
                    break
        if unread >= 2:
            break
    ear = []
    for pc in raw:
        if pc % 12 not in ear:
            ear.append(pc % 12)
    return ear[:12] or list(DEFAULT_EAR)


def _wall(seed) -> str:
    return hands.word(seed, "wall", "thin", ("thin", "thick"))


def _running(seed) -> bool:
    said = hands.word(seed, "root", "clumping", ("clumping", "clump", "running", "runs", "runner", "runners"))
    return said.startswith("run")


def _plume(seed) -> str:
    said = "-".join(hands.line(seed, "plume", "").lower().split())
    said = re.sub(r"[^a-z0-9#\-]", "", said)[:24]
    return said or "violet"


def _hardy(seed) -> float:
    return hands.num(seed, "hardy", -18, -40, -1)


def _from_seed(seed) -> bool:
    """Whether what was planted is a seed (it comes up as a seedling), not a piece of rootstock."""
    return hands.word(seed, "start", "rootstock", ("seed", "seeds", "graine", "rootstock", "root")) in (
        "seed", "seeds", "graine")


# ------------------------------------------------------------------ the body

class _Stem:
    __slots__ = ("num", "m", "dry", "end", "why", "plume", "to")

    def __init__(self, num, m, dry=False, end="growing", why="", plume="", to=None):
        self.num, self.m, self.dry, self.end, self.why, self.plume, self.to = num, m, dry, end, why, plume, to

    @property
    def length(self) -> float:
        return _length(self.m)


class _Reed:
    def __init__(self):
        self.stems = []
        self.buds = 1
        self.heard = []           # note names, low to high
        self.heard_on = None
        self.rooted = True        # False for a seedling that has not yet taken root

    def green(self) -> list:
        return [s for s in self.stems if not s.dry]

    def dry(self) -> list:
        return [s for s in self.stems if s.dry]

    def next_number(self) -> int:
        return max([0] + [s.num for s in self.stems if s.num is not None]) + 1


_ENDS = ("growing", "topped", "cut", "cropped", "broken", "stopped")


def _read(body):
    """A body as a _Reed, reading what it can. None if nothing in it can be read. Never raises."""
    try:
        return _read_carefully(body)
    except Exception:
        return None


def _read_carefully(body):
    reed = _Reed()
    found_any, buds_said = False, False
    state = False                                  # the group being read: False green, True dry
    for raw in str(body or "").splitlines()[:400]:
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("†"):
            continue
        key, colon, value = line.partition(":")
        key = " ".join(key.lower().split())
        if colon and key in ("dry", "dry stems", "green", "green stems"):
            state = key.startswith("dry")
            found_any = True
            if not value.strip():
                continue
            line = value
        elif colon and key == "rootstock":
            number = re.search(r"\d+", value)
            reed.buds = int(min(MOST_BUDS, int(number.group()))) if number else 1
            found_any = buds_said = True
            continue
        elif colon and key == "seedling":                # 'seedling: not yet rooted' (a hand's 'no' or 'rooted' roots it)
            said = value.lower()
            reed.rooted = bool(re.search(r"\b(no|rooted)\b", said)) and not re.search(r"\bnot\b", said)
            found_any = True
            continue
        elif colon and key == "heard":
            reed.heard = [_name(_pitch(n)) for n in _NOTE.finditer(value)][:40]
            dated = _DATE.search(value)
            if dated:
                try:
                    reed.heard_on = datetime.date(int(dated.group(1)), int(dated.group(2)), int(dated.group(3)))
                except ValueError:
                    reed.heard_on = None
            found_any = True
            continue
        if len(reed.stems) < MOST_STEMS:
            stem = _read_stem(line, state)
            if stem is not None:
                reed.stems.append(stem)
                found_any = True
    if not found_any:
        return None
    if not buds_said:
        reed.buds = 1
    seen = set()                                   # a line copied by hand is a stem of its own, with a new number
    for stem in reed.stems:
        if stem.num is None or stem.num in seen:
            stem.num = None
        else:
            seen.add(stem.num)
    for stem in reed.stems:
        if stem.num is None:
            stem.num = reed.next_number()
    return reed


def _read_stem(line, dry):
    """One stem line as a _Stem, or None if it holds no note.

    A hand's cut is read here, so that every reader of the body (the days,
    the plate, the creatures) sees it at once, and sees it the same: a note
    written higher than the bracket beside it says, or 'to <note>' higher
    than the stem stands. Either way the stem is 'cut' and grows no more.
    """
    to = None
    wish = _TO.search(line)
    if wish:
        to = _pitch(wish, 1)
        line = line[:wish.start()] + " " + line[wish.end():]
    note = _NOTE.search(line)
    if not note:
        return None
    m = _pitch(note)
    cents = _CENTS.match(line, note.end())
    if cents:
        m += (-1 if cents.group(1) in "-−–" else 1) * min(50, int(cents.group(2))) / 100.0
    m = min(HIGHEST, max(LOWEST, m))
    number = _NUMBER.search(line) or _LEADING.match(line)
    num = int(number.group(1)) if number else None
    lower = line.lower()
    if re.search(r"\bdry\b", lower):
        dry = True
    elif re.search(r"\bgreen\b", lower):
        dry = False
    end, at = None, len(lower) + 1
    for word in _ENDS:
        found = re.search(r"\b%s\b" % word, lower)
        if found and found.start() < at:
            end, at = word, found.start()
    why = ""
    if end in ("cropped", "broken", "stopped"):
        said = _BY.search(line, at)
        why = " ".join(said.group(1).split()) if said else ""
    if end is None:                               # a line with no word for how it stands was written by a hand
        end, why = ("stopped", "a hand") if dry else ("growing", "")
    if dry and end == "growing":                  # a growing line a hand moved among the dry stems
        end, why = "stopped", "a hand"
    plume = "plume" if re.search(r"\bin\s+plume\b", lower) else "seed" if re.search(r"\bin\s+seed\b", lower) else ""
    if _cut_since(line, m):                       # a higher note written over the old one
        end, why, plume = "cut", "", ""
    if to is not None and to > m + 0.02:          # 'to <note>' higher than it stands
        m, end, why, plume = to, "cut", "", ""
    if end != "growing":                          # only a growing stem can still grow to a note
        to = None
    return _Stem(num, m, dry, end, why, plume, to)


def _cut_since(line, m) -> bool:
    """Whether the bracket on a stem's line says it was longer when the days last wrote it, by more than a
    rounding: then a hand has written a higher note since, and that is a cut. No bracket, no witness."""
    said = _BRACKET.search(line)
    if not said:
        return False
    try:
        was = float(said.group(1).replace(",", "."))
    except ValueError:
        return False
    now = _length(m)
    return was > now + 0.15 and 1200.0 * math.log2(was / now) > TUNED


def _order(stems) -> list:
    return sorted(stems, key=lambda s: (s.m, s.num))


def _stem_line(s) -> str:
    if s.end == "growing":
        how = "growing" + (" to %s" % _name(s.to) if s.to is not None else "")
    elif s.end == "cropped":
        how = "cropped by %s" % (s.why or "something")
    elif s.end == "broken":
        how = "broken by %s" % (s.why or "a gale")
    elif s.end == "stopped":
        how = "stopped by %s" % (s.why or "the cold")
    else:
        how = s.end
    if s.plume:
        how += ", in %s" % s.plume
    return "  stem %-4d %-9s %-12s %s" % (s.num, _note(s.m), "(%.1f cm)" % s.length, how)


def _write(reed) -> str:
    green, dry = reed.green(), reed.dry()
    n = len(reed.stems)
    a = "# a reed" if reed.rooted else "# a reed seedling"
    head = "%s of %d stem%s" % (a, n, "" if n == 1 else "s")
    if n:
        head += ", %d of them green" % len(green) if len(green) != n else ", all green"
        if not green:
            head = "%s of %d dry stem%s" % (a, n, "" if n == 1 else "s")
    head += "; %d bud%s in the %s" % (reed.buds, "" if reed.buds == 1 else "s",
                                      "rootstock" if reed.rooted else "ground, not yet rooted")
    lines = [head]
    if reed.heard:
        lines.append("heard: %s%s" % (" ".join(reed.heard),
                                     " on %s" % reed.heard_on.isoformat() if reed.heard_on else ""))
    if dry:
        lines.append("dry stems:")
        lines += [_stem_line(s) for s in _order(dry)]
    if green:
        lines.append("green stems:")
        lines += [_stem_line(s) for s in _order(green)]
    lines.append("rootstock: %d bud%s" % (reed.buds, "" if reed.buds == 1 else "s"))
    if not reed.rooted:
        lines.append("seedling: not yet rooted")
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ the sky, read safely

class _Air:
    """The day's local sky as plain numbers, whatever was handed in."""

    def __init__(self, sky):
        def get(name, default):
            try:
                value = float(getattr(sky, name, default))
                return value if value == value else default
            except Exception:
                return default
        self.tmin, self.tmax = get("tmin", 5.0), get("tmax", 12.0)
        self.tmean = get("tmean", (self.tmin + self.tmax) / 2.0)
        self.light, self.wet, self.wind = get("light", 6.0), get("wet", 0.5), get("wind", 2.0)
        self.daylength = get("daylength", 12.0)
        self.season = str(getattr(sky, "season", "") or "")
        self.frost = self.tmin < 0.0


def _ripe(air) -> bool:
    """After midsummer: the stems listen for their notes and plume."""
    return air.season in ("summer", "autumn") and air.daylength < RIPE


def _growth(air, seed, bed) -> float:
    """How many cm a green stem puts on today, before its own share of luck."""
    if air.frost:
        return 0.0
    warm = min(1.0, max(0.0, (air.tmean - 6.0) / 11.0))
    light = 0.3 + 0.7 * min(1.0, max(0.0, air.light / 9.0))
    water = min(1.0, max(0.15, 0.15 + 1.1 * air.wet))
    rich = 1.0 + 0.5 * hands.num(bed or {}, "rich", 0, 0, 1)
    wall = 0.85 if _wall(seed) == "thick" else 1.0
    return 1.8 * warm * light * water * rich * wall


# ------------------------------------------------------------------ the days

def sprout(seed, ctx) -> str:
    """A piece of rootstock with three buds; or, from a seed, a seedling with one bud. (A reed whose body was taken
    away comes again by this too: after its first year, from a seed or not, it comes again from its rootstock.)"""
    reed = _Reed()
    reed.buds = 3
    try:
        young = float(getattr(ctx, "age", 0) or 0) < 365
    except (TypeError, ValueError):
        young = True
    if _from_seed(seed) and young:
        reed.buds, reed.rooted = 1, False
    return _write(reed)


def _third(ctx) -> float:
    """A third of the bed's room: as many reeds as a bed bears before they hold back (the stray keeps the same)."""
    return max(2.0, hands.num(getattr(ctx, "bed", None) or {}, "room", 12, 1, 400) / 3.0)


def _other_reeds(ctx) -> list:
    """The other living reeds of the bed: for each, True if it has rooted, False if it is a seedling."""
    found = []
    for other in (getattr(ctx, "neighbours", None) or [])[:400]:
        if str(getattr(other, "kind", "")) != KIND:
            continue
        body = getattr(other, "body", "")
        if hands.is_dead(body):
            continue
        theirs = _read(body)
        found.append(theirs is None or theirs.rooted)          # a body no one can read still holds its place
    return found


def _room_left(ctx) -> float:
    """How freely a reed may still sow or run: 1 alone in its bed, falling as the other reeds of the bed (rooted or
    seedlings, each holds a place) grow in number, and 0 once they fill a third of its room."""
    return max(0.0, 1.0 - len(_other_reeds(ctx)) / _third(ctx))


def _withers(air, ctx) -> float:
    """A seedling's chance of drying out today (a day of spring or summer): none in a bed as wet as the pond edge,
    more the drier its bed (by the square of how much less water it keeps than THIRSTY), and more on a dry day than
    a wet one. At water 1 about two seedlings in three are lost in a summer; at 0.7, nineteen in twenty."""
    water = hands.num(getattr(ctx, "bed", None) or {}, "water", 1, 0, 5)
    thirst = min(1.0, max(0.0, THIRSTY - water))
    return WITHERS * thirst * thirst * (1.2 - min(1.0, max(0.0, air.wet)))


def _taken(reed) -> dict:
    """The notes this year's stand has taken, and how many stems hold each: green stems that have stopped, and the
    notes growing ones are growing to. {midi note: how many}"""
    taken = {}
    for s in reed.green():
        note = int(round(s.m)) if s.end != "growing" else int(round(s.to)) if s.to is not None else None
        if note is not None:
            taken[note] = taken.get(note, 0) + 1
    return taken


def _taken_by_neighbours(ctx) -> dict:
    """What the other reeds of the bed have taken: a reed hears every reed in its bed."""
    taken = {}
    for other in (getattr(ctx, "neighbours", None) or [])[:40]:
        if str(getattr(other, "kind", "")) != KIND:
            continue
        theirs = _read(getattr(other, "body", ""))
        if theirs is not None:
            for note, count in _taken(theirs).items():
                taken[note] = taken.get(note, 0) + count
    return taken


def _seek(m, ear, taken):
    """Where a stem at m will stop. Of the notes of its ear at or below it, within a fifth: the nearest whose letter
    no stem has taken; else the one the fewest stems stand on (the nearer, if two tie). With none within a fifth,
    the nearest note of its ear. None for a deaf reed."""
    top = int(math.floor(m + 0.02))
    notes = [k for k in range(top, max(math.ceil(LOWEST), top - 48) - 1, -1) if k % 12 in ear]
    near = [k for k in notes if top - k <= REACH]
    letters = {note % 12 for note in taken}
    for k in near:
        if k % 12 not in letters:
            return k
    if near:
        return min(near, key=lambda k: (taken.get(k, 0), top - k))
    return notes[0] if notes else None


def day(body, seed, ctx):
    """One day of a reed. The almanac hears only what is worth a line: its first shoots, its first plumes, the
    cold coming before stems found their notes, a late frost that took half its shoots or more, a gale, a new
    chord in the wind, and its death. What every reed does every year (plume in July, dry in autumn) is left
    to the body and the plate."""
    if hands.is_dead(body):
        return body, None
    reed = _read(body)
    if reed is None:
        again = sprout(seed, ctx)
        rooted = getattr(_read(again), "rooted", True)
        return again, "came up again from the rootstock" if rooted else "came up again from its seed"
    air, rng, date = _Air(ctx.sky), ctx.rng, ctx.date
    wall, ear = _wall(seed), set(_ear(seed))
    events = []                                   # (weight, words): the day keeps the weightiest

    if air.tmin < _hardy(seed):
        frost = "a frost of %d°" % round(air.tmin)
        return "† %s, %s\n" % (date.isoformat(), frost) + _write(reed), "killed by " + frost

    # a seedling not yet rooted is easily lost: among too many reeds, or in dry ground
    if not reed.rooted:
        if sum(_other_reeds(ctx)) >= _third(ctx):
            return ("† %s, crowded out among the reeds\n" % date.isoformat() + _write(reed),
                    "crowded out among the reeds before it took root")
        if air.season in ("spring", "summer") and rng.random() < _withers(air, ctx):
            return ("† %s, dried out before it took root\n" % date.isoformat() + _write(reed),
                    "dried out before it took root")

    ripe = _ripe(air)

    # a late frost takes young shoots
    if air.tmin < -1.0:
        young = [s for s in reed.green() if s.end == "growing" and s.length < SOFT]
        lost = [s for s in young if rng.random() < 0.5]
        if lost:
            reed.stems = [s for s in reed.stems if s not in lost]
            if len(lost) == len(young):
                events.append((5, "a late frost took its only shoot" if len(lost) == 1 else
                               "a late frost took all %d of its shoots" % len(lost)))
            elif 2 * len(lost) >= len(young):
                events.append((5, "a late frost took %d of its %d shoots" % (len(lost), len(young))))

    # shoots, in spring
    if (reed.buds and air.season in ("spring", "summer") and not ripe and air.daylength >= 12.5
            and air.tmean >= 8.0 and not air.frost):
        came = sum(1 for _ in range(reed.buds) if rng.random() < 0.05)
        first = not reed.stems                    # never a stem before (or cut to the ground since)
        for _ in range(came):
            reed.stems.append(_Stem(reed.next_number(), _midi(SHOOT)))
            reed.buds -= 1
        if came and first:
            events.append((3, "its first shoot is up" if came == 1 else "its first shoots are up"))

    # after midsummer the growing stems listen, and choose where they will stop
    if ripe and ear:
        taken = _taken(reed)
        for note, count in _taken_by_neighbours(ctx).items():
            taken[note] = taken.get(note, 0) + count
        for s in _order(reed.green()):
            if s.end == "growing" and s.to is None and s.length >= LISTENS:
                s.to = _seek(s.m, ear, taken)
                if s.to is not None:
                    taken[s.to] = taken.get(s.to, 0) + 1

    # growth
    grow = _growth(air, seed, ctx.bed)
    if grow > 0:
        for rank, s in enumerate(sorted(reed.green(), key=lambda s: s.num)):
            if s.end != "growing":
                continue
            vigour = max(0.5, 1.25 - 0.08 * rank)       # the first shoots of a spring are the strongest
            longer = min(400.0, s.length + grow * vigour * (0.8 + 0.4 * rng.random()))
            if s.to is not None and longer >= _length(s.to) - 1e-6:
                s.m, s.end, s.to = float(s.to), "topped", None
            else:
                s.m = _midi(longer)

    # plumes
    plumed = False
    was_flowering = any(s.plume for s in reed.green())
    for s in reed.stems:
        if s.plume == "plume" and rng.random() < 0.05:
            s.plume = "seed"
        elif s.plume == "seed" and s.dry and air.season in ("winter", "spring") and rng.random() < 0.015:
            s.plume = ""
        elif not s.dry and s.end == "topped" and not s.plume and ripe:
            s.plume, plumed = "plume", True
    if plumed and not was_flowering and not reed.dry():     # its first plumes (no older stand stands by them);
        events.append((5, "came into plume"))                # later summers are for the plate

    # a seedling that has stood a stem through the summer takes root with the first cold of autumn
    cold = air.season in ("autumn", "winter") and (air.frost or air.tmean < 6.0 or air.daylength < 9.5)
    if not reed.rooted and reed.stems and cold:
        reed.rooted = True
        events.append((6.5, "it has taken root"))

    # the first cold of autumn dries the green stems, and last year's fall
    if reed.green() and cold:
        old = reed.dry()
        gain, short = 0.0, 0
        for s in reed.green():
            if s.end == "growing":
                s.end, s.why, s.to = "stopped", "the cold", None
                short += 1
            gain += FEEDS.get(s.end, 0.4)
            s.dry = True
            if s.plume == "plume":
                s.plume = "seed"
        reed.stems = [s for s in reed.stems if s not in old]
        reed.buds = int(min(MOST_BUDS, reed.buds + max(1, round(gain))))
        if short and ear:
            events.append((6, "the cold came before one stem found its note" if short == 1 else
                           "the cold came before %d stems found their notes" % short))
        elif not old:                                           # its first stand to dry
            events.append((6, "its stems have dried"))

    if not reed.buds and not reed.green() and air.season in ("autumn", "winter") and air.frost:
        reed.buds = 1

    # a gale breaks a dry stem
    broke = False
    if air.wind >= GALE and reed.dry() and rng.random() < BREAKS[wall]:
        s = rng.choice(reed.dry())
        shorter = s.length * (1.0 - rng.uniform(0.15, 0.45))
        if shorter < 5.0:
            reed.stems.remove(s)
        else:
            s.m, s.end, s.why, s.plume = _midi(shorter), "broken", "a gale", ""
        broke = True

    # the wind plays the dry stand
    chord = []
    if reed.dry() and not reed.green() and air.wind >= SOUNDS_AT[wall]:
        chord = _chord(reed)
    if broke:
        if chord and chord != reed.heard:
            reed.heard, reed.heard_on = chord, date
            events.append((5.5, "a gale broke a stem; the wind played %s" % " ".join(chord)))
        else:
            events.append((4, "a gale broke a stem"))
    elif chord and chord != reed.heard and not any(w >= 5 for w, _ in events):
        reed.heard, reed.heard_on = chord, date
        events.append((5, "the wind played %s" % " ".join(chord)))

    body = _write(reed)
    return body, (max(events)[1] if events else None)


def _chord(reed) -> list:
    """The notes the dry stems sound, low to high, each once."""
    names, seen = [], set()
    for s in _order(reed.dry()):
        name = _name(s.m)
        if name not in seen:
            seen.add(name)
            names.append(name)
    return names


def _count(n, word) -> str:
    return "%d %s%s" % (n, word, "" if n == 1 else "s")


# ------------------------------------------------------------------ what creatures meet

def flowers(body, seed, ctx) -> int:
    """How many plumes are open today."""
    if hands.is_dead(body):
        return 0
    reed = _read(body)
    return sum(1 for s in reed.stems if s.plume == "plume") if reed else 0


def _grazer(who) -> bool:
    """Whether a biter is a grazer that crops flat (a pony, a horse, a deer), by its name. Any other mouth, known
    or not, is taken for a small one: it can do a reed far less harm."""
    for word in re.findall(r"[^\W\d_]+", str(who).lower()):
        if word in GRAZERS or (word.endswith("s") and word[:-1] in GRAZERS):
            return True
    return False


def bitten(body, seed, ctx, share, by):
    """A bite of this share of what is soft.

    Most mouths find only the young shoots soft (growing, under 25 cm): they
    eat that share of them whole, the smallest first, and leave the rest of
    the stand alone. Each shoot eaten gives its bud back to the rootstock, so
    a bite costs the reed time, not a stem. A grazer crops the green stems
    flat, at the one height that takes this share of all their length, and a
    cropped stem grows no more.
    """
    if hands.is_dead(body):
        return body, None
    reed = _read(body)
    if reed is None:
        return body, None
    try:
        share = min(1.0, max(0.0, float(share)))
    except (TypeError, ValueError):
        return body, None
    who = " ".join(str(by or "something").split())[:40] or "something"
    rng = getattr(ctx, "rng", None)
    roll = rng.random() if rng is not None else 0.5
    green = reed.green()
    if not green or share <= 0:
        return body, None
    if not _grazer(who):
        young = sorted((s for s in green if s.end == "growing" and s.length < SOFT), key=lambda s: (s.length, s.num))
        want = share * len(young)
        k = int(want) + (1 if roll < want - int(want) else 0)
        if not k:
            return body, None
        eaten = young[:k]
        reed.stems = [s for s in reed.stems if s not in eaten]
        reed.buds = int(min(MOST_BUDS, reed.buds + len(eaten)))        # the rootstock will send another in its place
        return _write(reed), "%s ate %s" % (who, _count(len(eaten), "shoot"))
    lengths = [s.length for s in green]
    want = share * sum(lengths)
    low, high = 0.0, max(lengths)
    for _ in range(40):                               # the height of a flat crop that takes `want` cm in all
        middle = (low + high) / 2.0
        if sum(max(0.0, x - middle) for x in lengths) > want:
            low = middle
        else:
            high = middle
    height = high
    cropped = 0
    for s in list(green):
        if s.length > height + 0.5:
            cropped += 1
            if height < 3.0:
                reed.stems.remove(s)
            else:
                s.m, s.end, s.why, s.plume, s.to = _midi(height), "cropped", who, "", None
    if not cropped:
        return body, None
    return _write(reed), "%s cropped %s to %d cm" % (who, _count(cropped, "stem"), round(height))


# ------------------------------------------------------------------ seed

def _own_seed(seed) -> dict:
    kept = {key: value for key, value in seed.items() if key in KEPT}
    kept["kind"] = KIND
    return kept


def _donor(item):
    donor = getattr(item, "seed", None)
    if isinstance(donor, str):
        donor = hands.read_keys(donor)
    if not isinstance(donor, dict):
        donor = {}
    return donor, str(getattr(item, "where", "") or "another reed")


def _reed_pollen(item) -> bool:
    """Whether a grain is a reed's: by the kind the ground grows its giver as, else by its giver's seed."""
    kind = str(getattr(item, "kind", "") or "").strip().lower()
    if kind:
        return kind == KIND
    return hands.word(_donor(item)[0], "kind", "") == KIND


def _ear_words(ear) -> str:
    return " ".join(NAMES[pc] for pc in ear)


def _crossed(seed, ctx, item) -> str:
    donor, where = _donor(item)
    rng = ctx.rng
    mine, theirs = _ear(seed), _ear(donor)
    ear = [pc for pc in mine if pc in theirs]
    ear += [pc for pc in mine if pc not in theirs][:1] + [pc for pc in theirs if pc not in mine][:1]
    child = {"kind": KIND, "ear": _ear_words(ear) if ear else "none",
             "wall": rng.choice((_wall(seed), _wall(donor))),
             "root": rng.choice(("running" if _running(seed) else "clumping",
                                 "running" if _running(donor) else "clumping")),
             "plume": hands.mix(_plume(seed), _plume(donor), 0.5)}
    scent = rng.choice((hands.line(seed, "scent", ""), hands.line(donor, "scent", "")))
    if scent:
        child["scent"] = scent
    child["hardy"] = "%d" % round((_hardy(seed) + _hardy(donor)) / 2)
    child["start"] = "seed"
    child["from"] = "cross of %s × %s" % (ctx.where, where)
    return hands.write_keys(child)


def cast(body, seed, ctx):
    """What a rooted reed lets go today: a crossed seed from a plume pollen came to, a seed from a seed head on the
    wind, a runner from a running rootstock. Each comes the more rarely the more reeds its bed holds already, and
    none once the others fill a third of the bed's room (_room_left). A seedling lets nothing go."""
    if hands.is_dead(body):
        return []
    reed = _read(body)
    if reed is None or not reed.rooted:
        return []
    rng, air = ctx.rng, _Air(ctx.sky)
    open_plumes = sum(1 for s in reed.stems if s.plume == "plume")
    pollen = [item for item in (getattr(ctx, "pollen", None) or [])
              if _reed_pollen(item) and _donor(item)[1] != ctx.where] if open_plumes else []
    heads = sum(1 for s in reed.stems if s.plume == "seed")
    if air.season not in ("autumn", "winter") or air.wind < 2.5:
        heads = 0                                   # seed heads let go only on the windy days of autumn and winter
    runs = _running(seed) and air.season == "summer" and reed.buds + len(reed.green()) >= 4
    if not (pollen or heads or runs):
        return []
    room = _room_left(ctx)                          # (read only on a day something could fall: it reads the bed)
    if room <= 0.0:
        return []
    dropped = []
    if pollen and rng.random() < CROSSES * min(3, open_plumes) * room:
        dropped.append(_crossed(seed, ctx, pollen[rng.randrange(len(pollen))]))
    if heads and rng.random() < HEADS * heads * room:
        own = _own_seed(seed)
        own["start"] = "seed"
        dropped.append(hands.write_keys(own))
    if runs and rng.random() < RUNS * room:
        runner = _own_seed(seed)
        base = re.sub(r"(-runner|-seedling)(-[ivxlcdm]+)?$", "", str(getattr(ctx, "name", "") or "reed")) or "reed"
        runner["name"] = base[:40] + "-runner"
        runner["from"] = "ran from %s by the root" % ctx.where
        dropped.append(hands.write_keys(runner))
    return dropped[:2]


def describe(body, seed, ctx) -> str:
    reed = _read(body)
    if reed is None:
        return "nothing to be read in its body"
    n, green = len(reed.stems), len(reed.green())
    if hands.is_dead(body):
        if not reed.rooted:
            return "a seedling, dead before it took root"
        return "dead; it stood %s" % _count(n, "stem")
    if not n:
        said = "%s waiting in the ground" % _count(reed.buds, "bud")
        return said if reed.rooted else "a seedling, not yet rooted: " + said
    said = _count(n, "stem") + (", %d green" % green if green and green != n else ", all green" if green else ", all dry")
    if any(s.plume == "plume" for s in reed.stems):
        said += ", in plume"
    elif any(s.end == "growing" for s in reed.stems):
        said += ", growing"
    return said if reed.rooted else "a seedling of " + said + "; not yet rooted"


def size(body, seed) -> float:
    """For its dot on the plan: its stems by their length (15 cm to a unit), and half a unit for every bud
    waiting in the ground."""
    reed = _read(body)
    if reed is None:
        return 0.0
    return sum(s.length for s in reed.stems) / 15.0 + 0.5 * reed.buds


# ------------------------------------------------------------------ the plate
#
# The pen is told positions in cm, but the paper inside a tube, the walls, the
# plumes and the lettering are sized in pixels, and so is the spacing of the
# stems. So draw() first reckons the scale the pen will choose when it settles
# (the tallest stem decides it) and works out those pixel sizes in cm from it.

PAPER = "#fbf8f1"
INK = "#1a1a1a"
BORE = 5.0                  # px of paper inside a dry stem
WALL = 2.2                  # px: one stroke of a wall
GAP = 2.4                   # px of paper between the two strokes of a thick wall
STALK = 5.0                 # px: a green stem's stroke
DEPTH = 22.0                # px under the ground line to the rootstock (not to scale)
LIFTS = 2                   # a label may be lifted this many lines to clear the others; past that it is left out
SHOWS = 2.0                 # the least contrast, against the paper, that a plume is drawn at
MONTHS = ("January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December")


def draw(body, seed, ctx, pen) -> None:
    pen.unit_name = "cm"
    pen.ground(0)
    dead = hands.is_dead(body)
    reed = _read(body)
    if reed is None:
        pen.note("nothing to be read in its body")
        return
    left = getattr(ctx, "left", None)
    before = _read(left) if left is not None else None
    was = {s.num: s.length for s in before.stems} if before is not None else {}
    new_buds = reed.buds if before is None else max(0, reed.buds - before.buds)

    def ink(fresh):
        return "dead" if dead else "fresh" if fresh else "wood"

    wall, running = _wall(seed), _running(seed)
    plume = "dead" if dead else _shown(_plume(seed))
    seedhead = "dead" if dead else _shown(_plume(seed), fade=0.4)
    dry, green = _order(reed.dry()), _order(reed.green())
    stems = dry + green
    slots = len(stems) + (1 if dry and green else 0)
    tallest = max([s.length for s in stems] + [0.0])
    wide, high = _room(pen)
    most = getattr(pen, "unit_px_max", 60.0)
    most = min(60.0, max(0.5, most)) if isinstance(most, (int, float)) and most == most else 60.0
    scale = min(most, (high - 80.0) / max(tallest, 1e-6))
    pitch = min(64.0, (wide - 34.0) / max(1, slots + (4 if running else 1)))
    step = pitch / scale
    fan = min(26.0, 0.5 * pitch)                         # a plume's reach, in px: never wider than its share of room
    xs, slot = [], 0
    for i in range(len(stems)):
        if i == len(dry) and dry and green:
            slot += 1                                   # a gap between the dry stand and the green one
        xs.append(slot * step)
        slot += 1

    placed = []                                         # the labels lettered so far: (left, right, baseline), in px
    for i, s in enumerate(stems):
        x, top = xs[i], s.length
        old = top if dead else min(top, was.get(s.num, 0.0))
        grew = top > old + 0.05
        new = old <= 0.0 and not dead                   # the whole stem came up since the last visit
        if s.dry:
            rim = _tube(pen, s, x, top, old, scale, wall, ink, new)
        else:
            rim = STALK / 2
            if old > 0:
                pen.line(x, 0, x, old, STALK, ink(False))
            if grew:
                pen.line(x, old, x, top, STALK, ink(True))
        pen.line(x, 0, x, -DEPTH / scale, 2.2, ink(new))            # its foot, down to the rootstock
        above = _crown(pen, s, x, top, scale, rim, ink, grew)
        if s.plume == "plume":
            _plume_fan(pen, x, top, scale, fan, plume)
            above = max(above, fan + 8.0)
        elif s.plume == "seed":
            _seed_head(pen, x, top, scale, fan, seedhead)
            above = max(above, 0.92 * fan + 8.0)
        said = _heard_name(s.m, s.dry)
        lift = _clear_of(placed, x * scale, top * scale + above, _width(pen, said))
        if lift is not None:
            pen.label(x, lift / scale, said, 14, "dead" if dead else "ink")

    _rootstock(pen, [x * scale for x in xs], reed.buds, new_buds, running and reed.rooted, pitch, scale, ink,
               reed.rooted)

    pen.note(describe(body, seed, ctx))
    if reed.heard:
        when = reed.heard_on
        pen.note("the wind last played %s%s" % (" ".join(reed.heard), ", on %d %s %d" % (
            when.day, MONTHS[when.month - 1], when.year) if when else ""))


def _room(pen):
    """The width and height (px) the drawing has in the pen's box, less the strip kept for the scale bar; the
    plate's own, if the pen cannot say."""
    try:
        x0, y0, x1, y1 = (float(v) for v in pen.box)
        if x1 - x0 > 60 and y1 - y0 > 60:
            return x1 - x0 - 6.0, y1 - y0 - 36.0
    except Exception:
        pass
    return 774.0, 844.0


def _tube(pen, s, x, top, old, scale, wall, ink, new) -> float:
    """A dry stem: two walls with the bore between (a thick wall doubled), closed at the foot by the node. A stem
    broken by a gale has walls ending at two heights. Returns how far (px) the outside of a wall is from the middle."""
    inner = BORE / 2 + WALL / 2
    offsets = [inner] if wall == "thin" else [inner, inner + WALL + GAP]
    rim = offsets[-1] + WALL / 2
    for side in (-1, 1):
        end = top
        if s.end == "broken" and side > 0:
            end = max(0.0, top - 9.0 / scale)                     # the break is ragged: one wall is shorter
        for offset in offsets:
            wx = x + side * offset / scale
            if old > 0:
                pen.line(wx, 0, wx, min(old, end), WALL, ink(False))
            if end > old + 0.05:
                pen.line(wx, old, wx, end, WALL, ink(True))
        if s.end == "broken":                                       # each wall ends in a jag, off to its own side
            wx = x + side * offsets[-1] / scale
            pen.polyline([(wx, end), (wx + side * 3.5 / scale, end + 4.0 / scale), (wx + side * 1.0 / scale, end + 5.5 / scale),
                          (wx + side * 4.5 / scale, end + 10.0 / scale)], 2.0, ink(False))
    pen.line(x - rim / scale, 0, x + rim / scale, 0, 2.6, ink(new))           # the node that closes its foot
    return rim


def _crown(pen, s, x, top, scale, rim, ink, grew) -> float:
    """The mark at the top of a stem that says how it stopped. Returns the height (px) to letter its note at."""
    px = 1.0 / scale
    if s.end in ("cut", "cropped"):
        if s.dry:                                   # a flat rim on each wall, the bore left open
            for side in (-1, 1):
                pen.line(x + side * (BORE / 2) * px, top, x + side * (rim + 4.0) * px, top, 3.0, ink(False))
        else:
            pen.line(x - (rim + 5.0) * px, top, x + (rim + 5.0) * px, top, 3.0, ink(False))
        return 10.0
    if s.end == "broken":
        if not s.dry:                               # (only a hand can write a green stem broken)
            pen.polyline([(x - 6 * px, top - 3 * px), (x - 2 * px, top + 3 * px), (x + 2 * px, top - 3 * px),
                          (x + 6 * px, top + 3 * px)], 2.4, ink(False))
        return 12.0
    if s.end == "stopped":
        pen.dot(x, top + 6.0 * px, 4.0, ink(False), filled=False, weight=2.0)
        return 16.0
    if s.end == "growing":
        pen.dot(x, top, 4.5, ink(grew))
        return 12.0
    return 10.0


def _plume_fan(pen, x, top, scale, fan, colour):
    """A plume in flower: a fan of bold strokes standing up from the top of the stem."""
    weight = max(2.5, min(4.0, fan / 6.0))
    for j in range(5):
        angle = math.radians(-40.0 + 80.0 * j / 4)
        pen.line(x, top, x + math.sin(angle) * fan / scale, top + math.cos(angle) * fan / scale, weight, colour)


def _seed_head(pen, x, top, scale, fan, colour):
    """A plume gone to seed: it has nodded over to one side, and its seeds hang from it in short strokes."""
    u = fan / scale
    arch = [(x, top), (x + 0.12 * u, top + 0.62 * u), (x + 0.42 * u, top + 0.92 * u), (x + 0.78 * u, top + 0.82 * u),
            (x + 1.0 * u, top + 0.48 * u)]
    pen.polyline(arch, 2.4, colour)
    for px_, py_ in arch[1:]:
        pen.line(px_, py_, px_ + 0.08 * u, py_ - 0.5 * u, 2.0, colour)


def _rootstock(pen, feet, buds, new_buds, running, pitch, scale, ink, rooted=True):
    """The rootstock under the stand (px along it, turned into cm for the pen), with its buds between the feet.
    A running one reaches on past the stand and turns up at each end. A seedling not yet rooted has only a thread
    of root: a fine broken line."""
    reach = 10.0 if rooted else 26.0                              # px past the outermost feet: a thread wanders
    if feet:
        a, b = feet[0] - reach, feet[-1] + reach
    else:
        a, b = (-40.0, 40.0) if rooted else (-24.0, 24.0)
    if running:
        a, b = a - 2.0 * pitch, b + 2.0 * pitch
    a, b, spots = _bud_places(feet, a, b, buds, pitch)
    depth = DEPTH / scale
    if not rooted:
        dash, gap = 7.0, 5.0                                        # px
        x = a
        while x < b - 0.5:
            pen.line(x / scale, -depth, min(b, x + dash) / scale, -depth, 2.0, ink(False))
            x += dash + gap
    else:
        pen.line(a / scale, -depth, b / scale, -depth, 4, ink(False))
    if running:
        for end, side in ((a, -1), (b, 1)):
            pen.line(end / scale, -depth, (end + side * 7.0) / scale, -depth + 10.0 / scale, 4, ink(False))
    for j, spot in enumerate(spots):
        pen.dot(spot / scale, -depth, 4.5, ink(j >= buds - new_buds))


def _bud_places(feet, a, b, n, pitch):
    """Where n buds sit along a rootstock from a to b (px): spread evenly over it, but clear of the stems' feet, so
    that a bud is not taken for the joint of a stem. The rootstock is lengthened at both ends if they need room.
    Returns (a, b, places)."""
    if n <= 0:
        return a, b, []
    clear, apart = max(5.0, min(8.0, pitch / 2.0 - 3.0)), 13.0
    free = []
    for _ in range(6):
        free, low = [], a + 6.0
        for foot in feet:
            if foot - clear > low:
                free.append((low, foot - clear))
            low = max(low, foot + clear)
        if b - 6.0 > low:
            free.append((low, b - 6.0))
        room = sum(hi - lo for lo, hi in free)
        if room >= n * apart:
            break
        grow = (n * apart - room) / 2.0 + 2.0
        a, b = a - grow, b + grow
    room = sum(hi - lo for lo, hi in free)
    places = []
    for j in range(n):
        along = (j + 0.5) * room / n
        for lo, hi in free:
            if along <= hi - lo:
                places.append(lo + along)
                break
            along -= hi - lo
    return a, b, places


def _width(pen, said) -> float:
    """How wide a label is lettered at size 14, in px."""
    try:
        return float(pen.canvas.text_width(said, 14))
    except Exception:
        return 8.6 * len(said)


def _clear_of(placed, x, baseline, width):
    """The lowest baseline, at or above the one asked for, where a label of this width at x clears every label
    already placed (all in px, y up); at most LIFTS lines up, so that a label stays over its own stem. Records it
    and returns it, or returns None: in a crowded stand that note is not lettered."""
    left, right = x - width / 2 - 3, x + width / 2 + 3
    for _ in range(LIFTS + 1):
        clash = [b for l, r, b in placed if l < right and left < r and abs(b - baseline) < 16]
        if not clash:
            placed.append((left, right, baseline))
            return baseline
        baseline = max(clash) + 16
    return None


def _rgb(colour):
    """(r, g, b) of an ink, through hands.mix, which reads names and #rrggbb alike (near-black if neither)."""
    said = hands.mix(colour, colour, 0.0)
    return tuple(int(said[i:i + 2], 16) for i in (1, 3, 5))


def _contrast(a, b) -> float:
    """How far apart two colours stand to the eye, as the web measures it: 1 (the same) to 21 (black on white)."""
    def lum(rgb):
        lin = [c / 3294.6 if c <= 10.0 else ((c / 255.0 + 0.055) / 1.055) ** 2.4 for c in rgb]
        return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
    la, lb = lum(_rgb(a)), lum(_rgb(b))
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def _shown(colour, fade=0.0) -> str:
    """The plume's colour as the plate draws it: faded toward the paper by `fade` (a seed head is paler), but only
    so far as it still stands SHOWS to one against the paper. A colour too pale for that even at full strength
    (pale pink, white, a pale cross) is deepened toward the ink just enough."""
    full = hands.mix(colour, colour, 0.0)
    t = fade
    while t > 0.0 and _contrast(hands.mix(full, PAPER, t), PAPER) < SHOWS:
        t -= 0.05
    if t > 0.0:
        return hands.mix(full, PAPER, t)
    deep = 0.0
    while deep < 0.9 and _contrast(hands.mix(full, INK, deep), PAPER) < SHOWS:
        deep += 0.05
    return hands.mix(full, INK, deep)
