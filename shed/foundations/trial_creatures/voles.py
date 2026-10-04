"""
Voles: a trial creature, the one that grazes.

It lives in the trials of shed/foundations/: trial_ground.py brings it into a
trial ground that has no creatures of its own, so that the ground's side of
creatures can be tried before the garden has any. It is also a short, honest
example of a creature that bites, hides seed and moves plants: read it
before writing slugs, mice or the mole.

Its own file, ground/creatures/voles, says how many there are:

    voles: 12

On mild nights (the lowest above 2°) they come out along their runs and
bite soft growth: a few plants a night, a small bite each, most often in
beds with shelter, since they keep to cover. What a bite takes is the
plant's kind's to say (its bitten()); a kind that does not say is not
eaten, and they pass it by (a plant's view says so: `.edible`), so no
bite is spent on it. A bite that finds something feeds them, and fed
voles breed in spring and summer. Frost thins them, and a crowd of them
thins itself: never fewer than 2 nor more than 120.

In autumn, of the seed that falls, they hide some in their runs (the
larder, ground/larder: the forgotten ones come up in spring) and eat some.
Now and then a run passes under a plant and shifts it a little.

At an arrival in the dusk of the warm months, if they are many, one is seen
running along the edge of a bed.
"""

import re

NAME = "voles"
FEWEST, MOST = 2, 120


def _count(state) -> int:
    found = re.search(r"voles\s*:\s*(\d{1,6})", state or "")
    return min(MOST, max(FEWEST, int(found.group(1)))) if found else 12


def day(garden, ctx):
    n = before = _count(ctx.state)
    rng, sky = ctx.rng, ctx.sky
    fed = 0
    growing = [plant for plant in garden.plants() if not plant.dead]
    edible = [plant for plant in growing if plant.edible]      # what a bite can take something from
    if sky.tmin > 2 and growing:
        cover = {bed.name: 0.3 + bed.shelter for bed in garden.beds()}
        weights = [cover.get(plant.bed, 0.8) for plant in edible]
        for _ in range(max(1, min(n // 8, 6)) if edible else 0):
            plant = rng.choices(edible, weights)[0]
            if garden.bite(plant, rng.uniform(0.05, 0.15), "in the night"):
                fed += 1
        if rng.random() < 0.03:
            plant = rng.choice(growing)
            garden.nudge(plant, rng.uniform(-0.06, 0.06), rng.uniform(-0.06, 0.06), "a vole's run passed under it")
    if sky.season in ("spring", "summer") and fed and rng.random() < 0.3:
        n += max(1, round(n * 0.1 * (1 - n / MOST)))       # a litter; fewer as the runs fill up
    if sky.tmin < -2:
        n -= max(1, n // 6)
    elif not fed and rng.random() < 0.05:
        n -= max(1, n // 10)                               # a lean night: some move on, or are taken
    if n > 80:
        n -= n // 5
    n = min(MOST, max(FEWEST, n))
    ctx.save("voles: %d\n" % n)
    if before < 60 <= n:
        return ["voles are many this year"]
    return []


def after(garden, ctx, seeds):
    """In autumn: some of the fallen seed is hidden in the runs, some is eaten."""
    if ctx.sky.season != "autumn" or not seeds:
        return []
    rng = ctx.rng
    for seed in list(seeds):
        roll = rng.random()
        if roll < 0.3:
            garden.cache(seed, "in a run under the grass")
        elif roll < 0.45:
            garden.drop(seed, "eaten")
    return []


def present(garden, ctx):
    if not (19 <= (ctx.hour or 0) <= 21 and ctx.sky.tmin > 2 and _count(ctx.state) >= 20):
        return None
    beds = sorted(bed.name for bed in garden.beds() if bed.shelter >= 0.5)
    if not beds:
        return None
    return "A vole runs along the edge of the %s" % beds[ctx.rng.randrange(len(beds))]
