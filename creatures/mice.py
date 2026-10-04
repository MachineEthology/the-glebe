"""
Mice: in autumn they hide seed for the winter, and forget some of it.

Their own file, ground/creatures/mice, says how many live in the garden's
edges (under the stones, in the long grass, at the foot of the walls), how
much fallen seed they have found since the autumn began, and how much of
it they hid:

    mice: 24
    found this autumn: 40
    hidden this autumn: 31

Any line may be changed by hand; a number that cannot be read is taken
afresh.

What they do in the days:

  Seed. From September to November, of the seed that falls each day, the
  mice hide a share in the larder (ground/larder): more when they are many.
  A little they eat where it fell. Through the winter they live on what they
  hid, and the ground keeps the rest of the story: in spring most of the
  hidden seed is found again and eaten, but some is forgotten, and a
  forgotten seed comes up somewhere, in any bed with room but the keeper's.
  Such a seedling says so on its tag (`hidden: by mice on <day>, and
  forgotten`) and in its first ring. In winter the mice also eat what little
  seed falls. In spring and summer they leave the seed alone. A spore (what
  a fern or a moss lets go, its seed saying `start: spore`) is dust on the
  wind, not a seed: they neither find it nor hide it nor eat it.

  How many. From March to October they breed, faster when they are few and
  fed. Frost nights thin them through the winter, and snow more; the more
  seed they hid in the autumn, the better they come through. There are
  never fewer than 4 (a few always come in from the hedges) nor more
  than 60.

  A young garden. The first autumns of a new garden let fall very little
  seed, and the mice cannot hide what does not fall: they live on what the
  hedges give, and the larder stays empty or nearly. They come into their
  own as the garden fills and its plants seed freely. (Seed still held in
  the seed heads is the plants' own business; the mice take only what has
  fallen.)

The almanac hears of them once a year, on the last day of November: how
many of the seeds they found that autumn went into the larder, or that
they found none to hide. And when they are very many, or very few.
"""

import hands

NAME = "mice"
FEWEST, MOST = 4, 60
MANY = 45                # crossing this upwards, the almanac hears of it
FEW = 6                  # and this downwards


def _some(rng, x) -> int:
    """x as a whole number, the part after the point by the dice."""
    x = max(0.0, float(x))
    whole = int(x)
    return whole + (1 if rng.random() < x - whole else 0)


def _read(state) -> tuple:
    """(how many mice, seeds found this autumn, seeds hidden this autumn), from their file."""
    keys = hands.read_keys(state)
    hidden = int(hands.num(keys, "hidden this autumn", 0, 0, 100_000))
    return (int(hands.num(keys, "mice", 20, FEWEST, MOST)),
            max(hidden, int(hands.num(keys, "found this autumn", hidden, 0, 100_000))),
            hidden)


def _own_file(n, found, hidden) -> str:
    return ("# The mice: how many live in the garden's edges, and since September how much fallen seed they found\n"
            "# and how much of it they hid. The seed itself is in ground/larder. Any line may be changed by hand.\n"
            "mice: %d\n"
            "found this autumn: %d\n"
            "hidden this autumn: %d\n" % (n, found, hidden))


def _seeds(n) -> str:
    return "%d seed%s" % (n, "" if n == 1 else "s")


def _spore(seed) -> bool:
    """Is it a spore, dust on the wind? Its text says so: `start: spore` (as the days write on a fern's or a moss's)."""
    try:
        return hands.word(hands.read_keys(str(seed)), "start", "") in ("spore", "spores")
    except Exception:
        return False


def day(garden, ctx):
    n, found, hidden = _read(ctx.state)
    before = n
    sky, rng, today = ctx.sky, ctx.rng, ctx.date
    lines = []
    if today.month == 9 and today.day == 1:
        found = hidden = 0                          # a new autumn: last year's store is eaten or come up by now
    if 3 <= today.month <= 10 and sky.tmean >= 6:
        fed = 1.0 + min(1.0, hidden / max(1.0, n * 4.0))
        n += _some(rng, n * 0.006 * fed * max(0.0, 1.0 - n / 50.0))
    if sky.tmin < 0 or sky.snow:
        store = min(0.6, hidden / max(1.0, n * 5.0))   # what they hid carries them through
        n -= _some(rng, n * (0.03 if sky.snow else 0.012) * (1.0 - store))
    n = min(MOST, max(FEWEST, n))
    if today.month == 11 and today.day == 30:
        if hidden:
            lines.append("mice: of the %s they found fallen this autumn, they hid %d" % (_seeds(found), hidden)
                         if found > hidden else "mice: they hid %s this autumn" % _seeds(hidden))
        elif found:
            lines.append("mice: they found %s fallen this autumn, and hid none" % _seeds(found))
        else:
            lines.append("mice: they found no fallen seed to hide this autumn")
    if before < MANY <= n:
        lines.append("mice are many in the garden this year")
    elif n <= FEW < before:
        lines.append("mice are few in the garden now")
    ctx.save(_own_file(n, found, hidden))
    return lines


def after(garden, ctx, seeds):
    """Autumn: a share of the fallen seed hidden in the larder, a little eaten. Winter: what falls is eaten.
    Spores are passed by: they are not counted as found, hidden or eaten."""
    seeds = [seed for seed in (seeds or []) if not _spore(seed)]
    if not seeds:
        return []
    n, found, hidden = _read(ctx.state)
    rng, month = ctx.rng, ctx.date.month
    if 9 <= month <= 11:
        hide = max(0.06, min(0.55, n / 70.0))
        found += len(seeds)                         # what lay fallen when they came by (the birds have had theirs)
        for seed in list(seeds):
            roll = rng.random()
            if roll < hide:
                if garden.cache(seed, "for the winter"):
                    hidden += 1
            elif roll < hide * 1.15:
                garden.drop(seed, "eaten by a mouse")
        ctx.save(_own_file(n, found, hidden))
    elif month in (12, 1, 2):
        eat = max(0.05, min(0.4, n / 80.0))
        for seed in list(seeds):
            if rng.random() < eat:
                garden.drop(seed, "eaten by a mouse, in the cold")
    return []
