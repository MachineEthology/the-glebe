"""
Twig: the plainest plant there is.

It exists for the trials in shed/foundations/ and is not one of the garden's
own kinds, though it would grow there. It is also the shortest honest example
of what a kind is: read it before writing one.

A seed says:

    kind: twig
    flowers: summer      the season it flowers in (spring, summer, autumn, winter)
    colour: pink         the ink of its flowers
    tall: 30             the most lengths its stem will reach (3..80)
    hardy: -6            the night, in °C, that kills it
    variety: Pale Moon   (if a visitor named it) carried on by its own seed, never by a cross

The body is one line for the stem and one for each side shoot:

    stem: 7
    left shoot at 3: 2 *
    right shoot at 5: 1

"stem: 7" is a stem seven lengths high. "left shoot at 3: 2" leaves the stem
at height 3, to the left, and is two lengths long. A * at the end of a line
is a flower at that tip. Cut a line and the shoot is gone; lower a number and
it is pruned. An empty body comes up again from the seed. It is soft all
through: any line parts cleanly.

It adds a length on warm days (more often where the bed's ground is rich),
branches now and then, flowers in its season, and dies of a hard frost.

What creatures meet in it: its open flowers (flowers() counts them), and its
soft shoots, which a bite shortens from the tips, flowers first (bitten()).
It sets seed two ways. Now and then a flower sets its own seed, true to the
parent and carrying its variety. And when pollen of another twig has been
carried to it that day (ctx.pollen), a flower may set a crossed seed: its
colour halfway between the two parents', its height and hardiness between
theirs, and no variety. Nearness alone crosses nothing.

On the plate: stem and shoots in the planter's ink; what has grown since the
last visit in the fresh green; a dot at each flowering tip, in its colour; a
dead twig grey.
"""

import re

import hands

KIND = "twig"
SEASONS = ("spring", "summer", "autumn", "winter")
KEPT = ("kind", "flowers", "colour", "tall", "hardy", "variety")     # what a twig's own seed carries on
_STEM = re.compile(r"^\s*stem\s*:\s*(\d{1,6})\s*(\*?)")
_SHOOT = re.compile(r"^\s*(left|right) shoot at (\d{1,6})\s*:\s*(\d{1,6})\s*(\*?)")


def read(body):
    """A body as (stem, stem in flower, [[side, at, length, in flower], ...]). Reads what it can; never raises."""
    stem, flower, shoots = 0, False, []
    for line in str(body or "").splitlines():
        found = _STEM.match(line)
        if found:
            stem, flower = min(int(found.group(1)), 80), bool(found.group(2))
        found = _SHOOT.match(line)
        if found and len(shoots) < 16:
            shoots.append([found.group(1), min(int(found.group(2)), 80), min(int(found.group(3)), 12), bool(found.group(4))])
    return stem, flower, shoots


def write(stem, flower, shoots) -> str:
    lines = ["stem: %d%s" % (stem, " *" if flower else "")]
    lines += ["%s shoot at %d: %d%s" % (side, at, length, " *" if f else "") for side, at, length, f in shoots]
    return "\n".join(lines) + "\n"


def sprout(seed, ctx) -> str:
    return write(1, False, [])


def day(body, seed, ctx):
    if hands.is_dead(body):
        return body, None
    stem, flower, shoots = read(body)
    if stem < 1:                                            # cut to the ground, or never readable
        return sprout(seed, ctx), "came up again from the seed"
    if ctx.sky.tmin < hands.num(seed, "hardy", -6, -30, 5):
        return "† %s, frost\n%s" % (ctx.date.isoformat(), write(stem, flower, shoots)), "died of frost"
    rng, event = ctx.rng, None
    rich = hands.num(getattr(ctx, "bed", None) or {}, "rich", 0.0, 0.0, 1.0)
    chance = min(0.9, ctx.sky.warmth / 12.0) * (0.4 + 0.6 * min(1.0, ctx.sky.light / 8.0)) * (1.0 + 0.5 * rich)
    if stem < hands.num(seed, "tall", 30, 3, 80) and rng.random() < chance:
        stem += 1
        if stem >= 3 and len(shoots) < 12 and rng.random() < 0.15:
            shoots.append([rng.choice(("left", "right")), rng.randint(1, stem - 1), 1, False])
            event = "branched"
    for shoot in shoots:
        if shoot[2] < 12 and rng.random() < chance / 2:
            shoot[2] += 1
    had = flower or any(shoot[3] for shoot in shoots)
    if ctx.sky.season != hands.word(seed, "flowers", "summer", SEASONS):
        if had:
            flower, event = False, "dropped its flowers"
            for shoot in shoots:
                shoot[3] = False
    elif stem >= 4:
        flower = flower or rng.random() < 0.2
        for shoot in shoots:
            shoot[3] = shoot[3] or rng.random() < 0.2
        if not had and (flower or any(shoot[3] for shoot in shoots)):
            event = "came into flower"
    return write(stem, flower, shoots), event


# ---- what creatures meet

def flowers(body, seed, ctx) -> int:
    """How many flowers are open today: one at each flowering tip."""
    if hands.is_dead(body):
        return 0
    stem, flower, shoots = read(body)
    return int(flower) + sum(1 for shoot in shoots if shoot[3])


def bitten(body, seed, ctx, share, by):
    """A bite of `share` of what is soft: lengths taken from the tips of the shoots (flowers go with them), then from
    the top of the stem. Eaten to the ground, it dies."""
    if hands.is_dead(body):
        return body, None
    stem, flower, shoots = read(body)
    share = hands.num({"share": share}, "share", 0.0, 0.0, 1.0)
    soft = stem + sum(shoot[2] for shoot in shoots)
    want = share * soft
    take = int(want) + (1 if ctx.rng.random() < want - int(want) else 0)
    by = " ".join(str(by or "something").split())[:40] or "something"
    taken = 0
    for shoot in sorted(shoots, key=lambda s: -s[2]):
        while take > 0 and shoot[2] > 0:
            shoot[2] -= 1
            shoot[3] = False
            take -= 1
            taken += 1
    shoots = [shoot for shoot in shoots if shoot[2] > 0]
    while take > 0 and stem > 0:
        stem -= 1
        flower = False
        take -= 1
        taken += 1
    shoots = [shoot for shoot in shoots if shoot[1] < stem]
    if taken == 0:
        return body, None
    if stem < 1:
        return "† %s, eaten by %s\nstem: 0\n" % (ctx.date.isoformat(), by), "eaten to the ground by %s" % by
    news = taken >= max(4, soft // 4)                       # a nibble is not news; a quarter of the plant is
    return write(stem, flower, shoots), ("%s took %d lengths" % (by, taken) if news else None)


# ---- seed

def cast(body, seed, ctx):
    """Seed dropped today: a cross, only from pollen of another twig really carried here; else, now and then, its own."""
    stem, flower, shoots = read(body)
    open_ = int(flower) + sum(1 for shoot in shoots if shoot[3])
    if not open_ or hands.is_dead(body):
        return []
    rng = ctx.rng
    grains = [grain for grain in (getattr(ctx, "pollen", None) or [])
              if hands.word(_donor(grain), "kind", "") == KIND and getattr(grain, "where", "") != ctx.where]
    if grains and rng.random() < min(0.5, 0.1 * open_):
        return [_crossed(seed, grains[rng.randrange(len(grains))], ctx)]
    if rng.random() < min(0.1, 0.01 * open_):
        return [hands.write_keys({key: value for key, value in seed.items() if key in KEPT})]
    return []


def _donor(grain) -> dict:
    donor = getattr(grain, "seed", None)
    if isinstance(donor, str):
        donor = hands.read_keys(donor)
    return donor if isinstance(donor, dict) else {}


def _crossed(seed, grain, ctx) -> str:
    """A seed of this twig crossed with the twig whose pollen was carried here: halfway between them, with no variety."""
    donor = _donor(grain)
    child = {
        "kind": KIND,
        "flowers": ctx.rng.choice((hands.word(seed, "flowers", "summer", SEASONS), hands.word(donor, "flowers", "summer", SEASONS))),
        "colour": hands.mix(hands.line(seed, "colour", "pink"), hands.line(donor, "colour", "pink"), 0.5),
        "tall": "%d" % round((hands.num(seed, "tall", 30, 3, 80) + hands.num(donor, "tall", 30, 3, 80)) / 2),
        "hardy": "%d" % round((hands.num(seed, "hardy", -6, -30, 5) + hands.num(donor, "hardy", -6, -30, 5)) / 2),
        "from": "cross of %s × %s" % (ctx.where, getattr(grain, "where", "") or "another twig"),
    }
    return hands.write_keys(child)


def describe(body, seed, ctx) -> str:
    stem, flower, shoots = read(body)
    text = "%d length%s, %d shoot%s" % (stem, "" if stem == 1 else "s", len(shoots), "" if len(shoots) == 1 else "s")
    if hands.is_dead(body):
        return "dead; it stood " + text
    return text + (", in flower" if flower or any(shoot[3] for shoot in shoots) else "")


def draw(body, seed, ctx, pen) -> None:
    stem, flower, shoots = read(body)
    dead = hands.is_dead(body)
    was_stem, _, was_shoots = read(ctx.left)                # None reads as nothing: a new plant is all fresh
    was = {(side, at): length for side, at, length, _ in was_shoots}
    wood = "dead" if dead else "wood"
    pen.unit_name = "length, lengths"                       # what the scale bar calls one of them, and several
    pen.ground(0)

    def stroke(x, y, dx, dy, length, old, weight):
        """`length` lengths from (x, y): the first `old` of them as they were, the rest in the fresh ink."""
        old = length if dead else min(old, length)
        if old > 0:
            pen.line(x, y, x + dx * old, y + dy * old, weight, wood)
        if length > old:
            pen.line(x + dx * old, y + dy * old, x + dx * length, y + dy * length, weight, "fresh")
        return x + dx * length, y + dy * length

    tips = [(stroke(0, 0, 0, 1, stem, was_stem, 7), flower)]
    for side, at, length, in_flower in shoots:
        lean = -0.7 if side == "left" else 0.7
        tips.append((stroke(0, min(at, stem), lean, 0.7, length, was.get((side, at), 0), 4), in_flower))
    for (x, y), in_flower in tips:
        if in_flower:
            pen.dot(x, y, 8, "dead" if dead else hands.line(seed, "colour", "pink"))
    pen.note(describe(body, seed, ctx))
