"""
Hoverflies: a trial creature, the one that carries pollen.

It lives in the trials of shed/foundations/: trial_ground.py brings it into a
trial ground that has no creatures of its own, so that the ground's side of
creatures can be tried before the garden has any. It is also a short, honest
example of a creature: read it before writing bees or moths.

Its own file, ground/creatures/hoverflies, says how many there are and what
they did last:

    hoverflies: 40
    last out: 2026-07-12, 9 grains carried

On a warm, dry, still day (a top of 14° or more, less than a millimetre of
rain, wind under 5) they go from open flower to open flower, and carry
pollen from a plant to another plant of the same kind with flowers open:
nine flights in ten stay in the bed, the tenth goes to another bed. A cross
can come only of such a flight. Flowers feed them and they grow in number;
cold days thin them; a few always overwinter. They are never fewer than 3
nor more than 300, and the almanac hears of them only when they are many,
or when they have gone quiet.

At an arrival on a warm afternoon, while flowers are open, they are there,
standing in the air over the bed with the most flowers.
"""

import re

NAME = "hoverflies"
FEWEST, MOST = 3, 300


def _count(state) -> int:
    found = re.search(r"hoverflies\s*:\s*(\d{1,6})", state or "")
    return min(MOST, max(FEWEST, int(found.group(1)))) if found else 20


def _out(sky) -> bool:
    """Is it a day for hoverflies? Warm, dry and still."""
    return sky.tmax >= 14 and sky.rain < 1 and sky.wind < 5


def day(garden, ctx):
    n, before = _count(ctx.state), _count(ctx.state)
    rng = ctx.rng
    carried = 0
    if _out(ctx.sky):
        open_flowers = [plant for plant in garden.plants() if not plant.dead and plant.flowers > 0]
        by_kind = {}
        for plant in open_flowers:
            by_kind.setdefault(plant.kind, []).append(plant)
        for _ in range(min(len(open_flowers) * 2, n // 4)):
            giver = rng.choice(open_flowers)
            kin = [plant for plant in by_kind[giver.kind] if plant.where != giver.where]
            if not kin:
                continue
            near = [plant for plant in kin if plant.bed == giver.bed]
            receiver = rng.choice(near) if near and rng.random() < 0.9 else rng.choice(kin)
            carried += 1 if garden.pollen(giver, receiver) else 0
        if open_flowers:                                   # fed, they breed; fewer as the air fills
            n += max(0, round(min(20, 1 + len(open_flowers) // 3) * (1 - n / MOST)))
    elif ctx.sky.tmean < 6:
        n -= max(1, n // 12)
    n = min(MOST, max(FEWEST, n))
    last = [line for line in (ctx.state or "").splitlines() if line.startswith("last out:")]
    if carried:
        last = ["last out: %s, %d grain%s carried" % (ctx.date.isoformat(), carried, "" if carried == 1 else "s")]
    ctx.save("hoverflies: %d\n%s" % (n, "".join(line + "\n" for line in last[-1:])))
    if before < 150 <= n:
        return ["the hoverflies are thick over the flowers"]
    if n < 10 <= before:
        return ["the hoverflies have gone quiet"]
    return []


def present(garden, ctx):
    if not (12 <= (ctx.hour or 0) <= 17 and _out(ctx.sky) and _count(ctx.state) >= 10):
        return None
    beds = {}
    for plant in garden.plants():
        if not plant.dead and plant.flowers > 0:
            beds[plant.bed] = beds.get(plant.bed, 0) + plant.flowers
    if not beds:
        return None
    return "Hoverflies stand in the air over the %s" % max(sorted(beds), key=lambda bed: beds[bed])
