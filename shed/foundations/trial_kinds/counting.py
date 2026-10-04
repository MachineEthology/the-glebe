"""
Counting: a plant that only counts the days it lives. A trial kind, for the trials in shed/foundations/.

Its body is one line for each day it has lived, and the line is that day:

    2026-10-01
    2026-10-02
    2026-10-03

So "a day is lived once" can be read straight off the body: every day the
garden lived since it was sown is there, once, in order. A day
missing, twice, or out of order shows a fault in the ground, not in the
plant. A seed says only `kind: counting`.

It never flowers, never casts a seed, never dies. Cut its body and it forgets
those days; empty it and it begins counting again from the next day.

On the plate: one cell for each day counted, laid in rows of thirty (a
month), the days counted since the last visit in the fresh ink.
"""

KIND = "counting"


def sprout(seed, ctx) -> str:
    return ""


def day(body, seed, ctx):
    return str(body or "") + ctx.date.isoformat() + "\n", None


def describe(body, seed, ctx) -> str:
    days = [line for line in str(body or "").splitlines() if line.strip()]
    return "%d day%s counted" % (len(days), "" if len(days) == 1 else "s")


def draw(body, seed, ctx, pen) -> None:
    days = [line for line in str(body or "").splitlines() if line.strip()]
    before = len([line for line in str(ctx.left or "").splitlines() if line.strip()]) if ctx.left is not None else 0
    pen.unit_name = "day, days"
    pen.ground(0)
    for n in range(min(len(days), 3000)):
        pen.cell(n % 30, n // 30, 0.8, 0.8, "wood" if n < before else "fresh")
    pen.note(describe(body, seed, ctx))
