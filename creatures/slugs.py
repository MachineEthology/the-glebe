"""
Slugs: the many small mouths of the wet nights. (And snails, which are slugs that carry their house.)

They are many, and they are not wicked. Their one job is to bite.

THEIR FILE, ground/creatures/slugs, says how many there are:

    slugs: 240        the grown slugs about the garden
    snails: 45        the snails
    eggs: 300         slugs' eggs in the soil, waiting for the warmth to hatch
    told many: 2027-04-12     when the almanac was last told they were many (and `told few`, `told frost`)

A hand may change any number; the nights go on from what they find. A number
that cannot be read is taken to be an ordinary one.

WHEN THEY COME OUT. On a mild night when the ground is wet. The share of
them that comes out grows with the warmth of the night (from just above
freezing to about seven degrees) and with the wet (the last fortnight's rain,
or rain that day). On a frosty night nothing comes out. After a hot day the
night is drier, and fewer come.

WHAT THEY BITE. What is soft: seedlings most of all, then young plants, and
the grown ones least. They keep to damp and shade, so they are thickest at
the pond's edge and along the foot of the north wall, and fewest among the
dry bright stones; a bed's water, shelter and shade say how much they like
it. A seed that says `stem: thorny` (or spiny, prickly, woody), a leaf that
is waxy, downy, bristly, hairy or leathery, a corky coat or a hard crust:
these they mostly pass by. Each bite is a small share of what is soft (a
twentieth to a sixth), and no plant is bitten more than twice in one night.
What a bite takes is the plant's kind's to say (its bitten()); a kind that
does not say is not eaten, and where the garden tells them a plant cannot
be bitten at all, they spend no bite on it: their bites go to the plants
that can be. There is about one bite in a night for every 150
slugs and snails that are out, and never more than fifteen.

HOW THEIR NUMBERS GO.
- Slugs lay eggs on the nights they are out, in spring (March to June) and
  in autumn (August to November), fewer as the garden fills with them. The
  eggs hatch when the days are warm enough (above six degrees), slowly in
  the cool and faster in the warm, so eggs laid in autumn wait out the
  winter and a mild wet winter fills the spring with slugs. Some eggs are
  always lost; a dry spell loses more. Snails breed in the summer months,
  more slowly.
- A slug lives about a year. Drought kills more, a frost a few, a hard
  frost (below minus four) more again; a crowd thins itself. Snails shut
  themselves in their shells and ride out the dry and the cold better.
- The hedgehog eats them, on the nights she is awake and out and they are
  too: a few in every hundred she meets, and never more than she can eat;
  her young, when they go out with her, eat their share. The slugs know of
  her only by her nest (a thing she made in a bed, see creatures/hedgehog.py):
  when it says she is asleep in it, she is not hunting.
- The thrush takes snails by day and breaks their shells on her anvil in
  the stones bed (a thing she made, see creatures/thrush.py). Each shell on
  it dated the day before was a snail, and is taken off the snails' count:
  every one while there are eighty snails or more; when they are fewer, she
  finds some of hers over the wall (with forty snails, half of them).
- However the years go, there are never fewer than 20 slugs and 5 snails
  (some always come in from the gardens round about), and never more than
  2,000 slugs and 300 snails.

WHAT A VISITOR FINDS. Their bites, in the plants' rings, in each kind's own
words ("slugs ate 'moss' and 'rain'"). In the almanac a line now and then:
when the slugs have become many (800), when they have become few (120), and
at the first hard frost of a winter. At an arrival on a mild
wet night they are out; on the morning after one, their silver trails are
on the stones.
"""

import datetime
import random
import re

import hands

NAME = "slugs"

SLUGS = (20, 2000)          # fewest, most
SNAILS = (5, 300)
EGGS_MOST = 20000
CROWD = 1600                # where a crowd of slugs begins to thin itself, and to lay fewer eggs
MANY, FEW = 800, 120        # crossing these, the almanac is told (and not again for SAY_AGAIN days)
SAY_AGAIN = 200

TO_A_BITE = 150             # slugs or snails out in the night for each bite the garden notices
BITES_MOST = 15             # a night's bites, however many are out
TWICE = 2                   # bites one plant may have in one night

LAYING = (3, 4, 5, 6, 8, 9, 10, 11)
LAY = 0.2                  # eggs a slug lays on a night it is out (in this garden's reckoning), with room to spare
HATCH = 0.03                # the share of the eggs that hatch on a warm day
HATCH_LIVES = 0.3           # of the eggs that hatch, the share that live to be counted
SNAIL_BREEDING = (5, 6, 7, 8)
SNAIL_BREED = 0.06          # new snails for each snail out, on a summer night

LIFE = 0.0035               # the share of the slugs that die of their age on any day (they live about a year)
SNAIL_LIFE = 0.0012
DROUGHT, SNAIL_DROUGHT = 0.008, 0.002
HARD_FROST, SNAIL_HARD_FROST = 0.012, 0.003
FROST = 0.003

HUNT = 0.012                # the share of the slugs out that one hedgehog eats in a night
HUNT_MOST = 7               # and the most she can eat (her young: half as many each)
OVER_THE_WALL = 80          # fewer snails than this, and some of the thrush's shells are from over the wall

SPURNED = (("stem", ("thorny", "spiny", "prickly", "woody"), 0.15),
           ("leaf", ("waxy", "downy", "bristly", "hairy", "leathery", "furry", "woolly"), 0.4),
           ("coat", ("corky",), 0.4),
           ("crust", ("hard",), 0.3))
TOLD = ("many", "few", "frost")
PLACES = {"pond-edge": "by the pond", "north-wall": "at the foot of the north wall"}    # how a bed is said at night


# ------------------------------------------------------------------ reading

def _clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x


def _date(text):
    found = re.search(r"(\d{4})-(\d{2})-(\d{2})", text or "")
    if not found:
        return None
    try:
        return datetime.date(int(found.group(1)), int(found.group(2)), int(found.group(3)))
    except ValueError:
        return None


def _state(text) -> dict:
    """Their file as numbers. Anything a hand left that cannot be read is an ordinary number instead."""
    keys = hands.read_keys(text or "")
    st = {
        "slugs": hands.num(keys, "slugs", 240, *SLUGS),
        "snails": hands.num(keys, "snails", 45, *SNAILS),
        "eggs": hands.num(keys, "eggs", 300, 0, EGGS_MOST),
    }
    for news in TOLD:
        st[news] = _date(hands.line(keys, "told " + news, ""))
    return st


def _text(st) -> str:
    lines = ["# The slugs and snails of the garden, as the nights count them. A hand may change the numbers.",
             "slugs: %d" % round(st["slugs"]),
             "snails: %d" % round(st["snails"]),
             "eggs: %d" % round(st["eggs"])]
    lines += ["told %s: %s" % (news, st[news].isoformat()) for news in TOLD if st[news]]
    return "\n".join(lines) + "\n"


def _night(sky) -> float:
    """The share of them that comes out tonight, 0..1: none in a frost; most on a mild night after rain."""
    if sky.tmin < 0:
        return 0.0
    warm = _clamp((sky.tmin + 1.0) / 8.0, 0.0, 1.0)
    damp = max(_clamp((sky.wet - 0.08) / 0.42, 0.0, 1.0), _clamp(sky.rain / 4.0, 0.0, 1.0))
    if sky.tmax >= 27:
        damp *= 0.5                        # a hot day dries the night
    return warm * damp


def _bed_liking(bed) -> float:
    """How much they like a bed: wet ground, shelter and shade. The pond's edge and the foot of the wall most of all."""
    return max(0.02, max(0.0, bed.water) * (0.3 + _clamp(bed.shelter, 0.0, 1.0)) ** 1.5 * max(0.1, 1.5 - bed.light))


def _softness(plant) -> float:
    """How soft a plant is to a slug: seedlings most, the grown least; less again for thorns, down, wax or cork."""
    age = plant.age
    soft = 6.0 if age < 30 else 3.0 if age < 120 else 1.5 if age < 365 else 1.0
    seed = plant.seed
    for key, words, spared in SPURNED:
        if hands.word(seed, key, "", words):
            soft *= spared
    return soft


def _edible(plant) -> bool:
    """Can a bite be had of it at all? The garden says so on the view (`edible`) where it can tell; where it says
    nothing, it may be, and the kind decides when they bite."""
    try:
        return bool(getattr(plant, "edible", True))
    except Exception:
        return True


def _hedgehogs_out(garden) -> float:
    """How many hedgehogs hunt tonight, as their nest says: none if it says she is asleep in it, or says nothing of
    the night; else she, and her young (each worth half of her) if they go out with her. No nest, no hedgehog."""
    for thing in garden.things():
        if thing.maker != "hedgehog":
            continue
        keys = hands.read_keys(thing.text)
        if "asleep in it" in keys or "out" not in hands.line(keys, "by night", ""):
            return 0.0
        young = hands.line(keys, "young", "")
        return 1.0 + (0.5 * hands.num(keys, "young", 0, 0, 8) if "out with her" in young else 0.0)
    return 0.0


def _shells(garden, day) -> int:
    """Snail shells the thrush broke on her anvil on `day`: the lines of her anvil dated so."""
    stamp = day.isoformat()
    return sum(1 for thing in garden.things() if thing.maker == "thrush"
               for line in thing.text.splitlines() if line.startswith(stamp))


# ------------------------------------------------------------------ the night

def day(garden, ctx):
    st = _state(ctx.state)
    sky, rng, month = ctx.sky, ctx.rng, ctx.date.month
    out = _night(sky)

    if out > 0:
        want = (st["slugs"] + st["snails"]) * out / TO_A_BITE
        bites = min(BITES_MOST, int(want) + (1 if rng.random() < want - int(want) else 0))
        if bites:
            _bite(garden, rng, bites)
    _reckon(st, sky, month, out, _hedgehogs_out(garden) if out > 0 else 0.0,
            _shells(garden, ctx.date - datetime.timedelta(days=1)))
    lines = _news(st, ctx)
    ctx.save(_text(st))
    return lines


def _reckon(st, sky, month, out, hogs, shells) -> None:
    """One day of their numbers: what hatched, what was laid, what died, what was eaten."""
    slugs, snails, eggs = st["slugs"], st["snails"], st["eggs"]
    room = max(0.0, 1.0 - slugs / CROWD)
    dry = sky.wet < 0.1 and sky.tmax > 20

    if month in LAYING and out > 0.15:
        eggs += slugs * out * LAY * room
    if sky.tmean > 6 and sky.tmin >= 0:
        hatched = eggs * HATCH * _clamp((sky.tmean - 6.0) / 8.0, 0.15, 1.0)
        eggs -= hatched
        slugs += hatched * HATCH_LIVES
    eggs -= eggs * (0.012 if dry else 0.002)
    if month in SNAIL_BREEDING and out > 0.15:
        snails += snails * out * SNAIL_BREED * max(0.0, 1.0 - snails / SNAILS[1])

    die, snail_die = LIFE + 0.004 * (slugs / CROWD) ** 2, SNAIL_LIFE
    if dry:
        die, snail_die = die + DROUGHT, snail_die + SNAIL_DROUGHT
    if sky.tmin < -4:
        die, snail_die = die + HARD_FROST, snail_die + SNAIL_HARD_FROST
    elif sky.tmin < 0:
        die += FROST
    slugs -= slugs * die
    snails -= snails * snail_die

    if hogs:
        slugs -= min(slugs * out * HUNT * hogs, HUNT_MOST * hogs)
        snails -= min(snails * out * HUNT * 0.5 * hogs, hogs)
    if shells:
        snails -= shells * min(1.0, snails / OVER_THE_WALL)

    st["slugs"] = _clamp(slugs, *SLUGS)
    st["snails"] = _clamp(snails, *SNAILS)
    st["eggs"] = _clamp(eggs, 0.0, EGGS_MOST)


def _bite(garden, rng, bites) -> int:
    """Tonight's bites, each where the slugs are thickest and the growth softest. Returns how many found something."""
    liking = {bed.name: _bed_liking(bed) for bed in garden.beds()}
    soft = [plant for plant in garden.plants() if not plant.dead and _edible(plant)]
    if not soft:
        return 0
    weights = [liking.get(plant.bed, 0.3) * _softness(plant) for plant in soft]
    had, fed = {}, 0
    for _ in range(bites):
        plant = rng.choices(soft, weights)[0]
        if had.get(plant.where, 0) >= TWICE:
            continue
        had[plant.where] = had.get(plant.where, 0) + 1
        if garden.bite(plant, rng.uniform(0.05, 0.17)):
            fed += 1
    return fed


def _news(st, ctx) -> list:
    """A line for the almanac, now and then: when they have become many, or few, and at a winter's first hard frost."""
    today = ctx.date

    def due(news, days=SAY_AGAIN):
        return st[news] is None or (today - st[news]).days > days

    if st["slugs"] >= MANY and due("many"):
        st["many"] = today
        return ["the slugs grew many, and hundreds were out in the wet"]
    if st["slugs"] <= FEW and due("few"):
        st["few"] = today
        return ["the slugs grew few, and hardly any were out in the wet"]
    if ctx.sky.tmin < -4 and due("frost", 150):
        st["frost"] = today
        return ["a hard frost sent the slugs deep, and killed some of them"]
    return []


# ------------------------------------------------------------------ at the gate

def present(garden, ctx):
    hour = ctx.hour if isinstance(ctx.hour, int) else 12
    st = _state(ctx.state)
    many = st["slugs"] + st["snails"]
    out = _night(ctx.sky)
    if (hour >= 21 or hour <= 4) and out > 0.3 and many >= 150:
        liked = sorted(garden.beds(), key=lambda bed: (-_bed_liking(bed), bed.name))[:2]
        if not liked:
            return None
        bed = liked[0 if ctx.rng.random() < 0.6 or len(liked) < 2 else 1].name
        place = PLACES.get(bed, "in the %s" % bed)
        return "Slugs are out on the wet ground %s" % place
    # Whether the trails are there is the morning's, not the hour's: dice of the date alone (ctx.rng at an arrival
    # falls anew each hour), so whoever comes at five and whoever comes at eight find the same stones.
    if 5 <= hour <= 8 and out > 0.3 and many >= 100 and random.Random("slug trails|%s" % ctx.date).random() < 0.5:
        return "Silver trails cross the stones where the slugs went in the night"
    return None
