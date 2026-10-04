"""
The plate's trial.

Run it after changing shed/plate.py:

    python shed/foundations/plate_trial.py [folder]

It writes into the folder it is given, which must lie outside the garden:
the sheets are a megabyte and a half, and they are not the garden's. Given
no folder, it makes one in the system's temp folder and says where.

It draws these sheets there, each as PNG and as SVG:

    lettering    every character the face has, at sizes 14, 18, 24 and 34:
                 first in order, then scrambled, then the look-alikes
                 (the three dashes, I l 1 |, 0 O o, ' `, ( ) [ ], the
                 accented i and e, , . : ;) shuffled into a row of their
                 own, then side by side, then a line as the garden would
                 write it. lettering.txt holds the same lines as text.
    stress       a full-grown plate: 4,000 lengths, 300 dots, 12 lines of
                 lettering, laid out as the ground lays out a plant's plate
    scatter      the same load thrown anywhere: long strokes, all the inks
    crowded      the scatter again with an ink of its own for each stroke,
                 so the plate goes over to full colour
    specimen     a small branching figure in a large box with its scale
                 bar, and the same figure in small boxes
    textures     stipple from dots, a doubled stroke from two lines, a
                 broken line from short strokes, at the finest pens a kind
                 has: on a plate, and on a bed sheet
    inks         every named ink, with its name
    marks        what the other sheets leave out: arcs by quadrant, each
                 with a dot at its start, and arcs asked for oddly; cells in
                 a solid field, in a chequerboard and as hairlines lying and
                 standing; the three anchors against a guide line; three
                 hundred inks on one plate; white flowers and a white shoot
                 drawn a length at a time; scale bars in narrow boxes;
                 fruit kept apart, and the dark eyes of flowers of round
                 petals left alone; a seed alone, and a row of lettered
                 months, both with no bar

Then it checks what can be checked by counting, and prints one verdict line
for each check.

What it cannot check is whether the plates are good to look at. That part is
yours: open the PNGs. Read the scrambled lines and the row of look-alikes of
lettering.png from the picture alone, at the size it is drawn, before you
open lettering.txt; then compare. A character you misread is a fault in the
face, and plate.py says how to mend a letter. (Read so on 30 September:
every row right at 24 and 34; at 14 and 18 an en dash standing alone was
read as an em dash, though between letters all three dashes were read
right, and a shorter en dash only traded that for en read as hyphen.)
"""

import math
import os
import random
import re
import struct
import sys
import tempfile
import time
import xml.etree.ElementTree as ElementTree
import zlib

sys.dont_write_bytecode = True                    # a trial leaves nothing in the shed
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import plate                                      # noqa: E402
from plate import Canvas                          # noqa: E402

BUDGET = 2.5                                      # seconds, for a full plate drawn and saved
SIZES = (14, 18, 24, 34)
SAID = {                                          # a line at each size, as the garden would write it
    14: "The Glebe \u00b7 Wednesday 30 September 2026 \u00b7 17:42 \u00b7 overcast, 9\u201315\u00b0, no rain, moon waxing gibbous",
    18: "long-border/quince came into flower on the 24th; 2 came up by themselves",
    24: "planted 2026-10-03 by claude-opus-4-7 \u00b7 212 days",
    34: "quince \u00b7 214 lengths, in flower",
}
# The look-alikes, side by side: the pairs of the face that are nearest to one another.
TWINS = "\u00ea\u00eb \u00ee\u00ef \u00e9\u00e8 \u00e2\u00e0  - \u2013 \u2014  a-b 9\u201315  hn co Il1| O0o '` () [] (1) [0] :; ,. rn m"
# The look-alikes again, each twice, shuffled into a row of their own among the scrambled lines: side by side the
# face can lean on comparison, and alone it cannot. Read this row blind before anything else.
LOOKALIKES = "- \u2013 \u2014 I l 1 | 0 O o ' ` ( ) [ ] \u00ea \u00eb \u00ee \u00ef , . : ;".split() * 2
# Four arcs, one to a quadrant, each in an ink of its own.
QUADRANTS = ((0, 90, "red"), (90, 180, "blue"), (180, 270, "fresh"), (270, 360, "orange"))


class Thorn:
    """A thing that raises whatever is asked of it."""

    def __float__(self):
        raise RuntimeError("a thorn is not a number")

    def __str__(self):
        raise RuntimeError("a thorn has nothing to say")

    def __bool__(self):
        raise RuntimeError("a thorn is neither yes nor no")

    def __eq__(self, other):
        raise RuntimeError("a thorn is like nothing else")

    def __hash__(self):
        raise RuntimeError("a thorn cannot be looked up")


ODD = [float("nan"), float("inf"), float("-inf"), 1e300, -1e300, None, "seven", [], {}, object(), Thorn()]

verdicts = []


def verdict(name, holds, detail=""):
    """Keep one verdict and print its line."""
    verdicts.append(bool(holds))
    print("%s  %s%s" % ("ok  " if holds else "FAIL", name, (" - " + detail) if detail else ""))


def save(canvas, folder, name):
    """Save a sheet as PNG and SVG."""
    png = canvas.save_png(os.path.join(folder, name + ".png"))
    svg = canvas.save_svg(os.path.join(folder, name + ".svg"))
    return png and svg


# ------------------------------------------------------------------ sheets

def wrapped(canvas, characters, size, room, group=0):
    """Characters set out in lines no wider than room. group > 0 puts a space after every so many."""
    lines, line = [], ""
    for i, ch in enumerate(characters):
        piece = ch + (" " if group and i % group == group - 1 else "")
        if line and canvas.text_width((line + piece).rstrip(), size) > room:
            lines.append(line.rstrip())
            line = ""
        line += piece
    if line.strip():
        lines.append(line.rstrip())
    return lines


def in_groups(canvas, line, size, room):
    """A line whose groups are set apart by two spaces, in lines no wider than room, never breaking a group."""
    lines = []
    for group in line.split("  "):
        if lines and canvas.text_width(lines[-1] + "  " + group, size) <= room:
            lines[-1] += "  " + group
        else:
            lines.append(group)
    return lines


def lettering_sheet(folder):
    """Every character of the face at four sizes, in order and scrambled, and a line as the garden would write it."""
    visible = [ch for ch in plate.SUPPORTED if ch != " "]
    probe = Canvas(10, 10)
    blocks, height = [], 40
    for size in SIZES:
        scrambled, alike = list(visible), list(LOOKALIKES)
        random.Random("scrambled %d" % size).shuffle(scrambled)     # a different order at each size, so none can
        random.Random("alike %d" % size).shuffle(alike)             # be read from another
        lines = (wrapped(probe, visible, size, 900) + wrapped(probe, scrambled, size, 900, group=5)
                 + wrapped(probe, "  ".join(alike), size, 900) + in_groups(probe, TWINS, size, 900) + [SAID[size]])
        blocks.append((size, lines))
        height += int(len(lines) * size * 1.7) + 50
    canvas = Canvas(1000, height)
    as_text = []
    y = 30
    for size, lines in blocks:
        canvas.text(970, y + 6, "size %d" % size, 14, "grey", "end")
        as_text.append("size %d" % size)
        for line in lines:
            y += size * 1.7
            canvas.text(40, y, line, size)
            as_text.append(line)
        as_text.append("")
        y += 50
    with open(os.path.join(folder, "lettering.txt"), "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(as_text) + "\n")
    return save(canvas, folder, "lettering")


def grow(pen, rng, lengths, fresh=0, trunk=14.0):
    """Draw a branching figure of so many lengths, one unit to a length. The last `fresh` of them are new growth.

    Returns the tips: [(x, y)].
    """
    shoots = [(0.0, 0.0, 90.0, trunk)]            # where, heading in degrees, weight
    drawn = 0
    while drawn < lengths and shoots:
        x, y, heading, weight = shoots.pop(0)
        heading += rng.uniform(-14, 14) + (90 - heading) * 0.06     # it wanders, and leans back toward the light
        nx = x + math.cos(math.radians(heading))
        ny = y + math.sin(math.radians(heading))
        pen.line(x, y, nx, ny, weight, "fresh" if drawn >= lengths - fresh else "wood")
        drawn += 1
        shoots.append((nx, ny, heading, weight * 0.985))
        if rng.random() < 0.12:
            shoots.append((nx, ny, heading + rng.choice((-1, 1)) * rng.uniform(25, 50), weight * 0.7))
    return [(x, y) for x, y, _, _ in shoots]


def caption(canvas, name, lines, notes, planter="claude-opus-5-5"):
    """The words under a plant's box, laid out as the ground lays them out."""
    canvas.text(60, 978, name, 34)
    y = 978
    for line in list(lines) + list(notes):
        y += 27
        canvas.text(60, y, line, 18)
    canvas.rect(60, 1148, 26, 12, "wood")
    width = canvas.text(94, 1160, planter, 14)
    canvas.rect(94 + width + 24, 1148, 26, 12, "fresh")
    canvas.text(94 + width + 58, 1160, "grown since 2026-09-18", 14)
    canvas.text(840, 1160, "drawn 2026-09-30 17:42", 14, "ink", "end")


def stress_plate(folder):
    """A full-grown plant's plate: 4,000 lengths, 300 dots, 12 lines of lettering. Returns seconds."""
    began = time.perf_counter()
    rng = random.Random(4000)
    canvas = Canvas(900, 1200)
    canvas.inks["wood"] = "#1f4e9c"
    pen = canvas.specimen((60, 50, 840, 930))
    pen.unit_name = "lengths"
    pen.ground(0.0)
    tips = grow(pen, rng, 4000, fresh=900)
    for x, y in tips[:300]:
        pen.dot(x, y, rng.choice((4.0, 5.0, 6.0)), rng.choice(("red", "dark-red", "pale-pink")))
    top = max(tips, key=lambda tip: tip[1])
    east = max(tips, key=lambda tip: tip[0])
    west = min(tips, key=lambda tip: tip[0])
    pen.label(top[0], top[1] + 0.8, "the leader", 14)
    pen.label(east[0] + 0.6, east[1], "east", 14, "ink", "start")
    pen.label(west[0] - 0.6, west[1], "west", 14, "ink", "end")
    pen.note("4000 lengths, 300 in fruit")
    pen.note("forked 480 times; the leader stands 61 lengths high")
    pen.note("900 lengths are new since the last visit")
    pen.settle()
    caption(canvas, "stress", ["bough \u00b7 trial-bed", "planted 2026-03-02 by claude-opus-5-5 \u00b7 212 days"], pen.notes)
    canvas.save_png(os.path.join(folder, "stress.png"))
    seconds = time.perf_counter() - began
    canvas.save_svg(os.path.join(folder, "stress.svg"))
    return seconds


def scatter_plate(folder, crowded=False):
    """The same load with no plant in it: 4,000 strokes of any length and ink, thrown anywhere.

    crowded gives each stroke an ink of its own: far more than one byte can
    number, so the plate goes over to full colour, the slowest way it has.
    Returns (seconds, bytes to a sample): 3 says it really went over.
    """
    began = time.perf_counter()
    rng = random.Random(300)
    canvas = Canvas(900, 1200)
    names = [name for name in canvas.inks if name not in ("paper", "white")]
    for k in range(4000):
        x, y = rng.uniform(0, 900), rng.uniform(0, 1000)
        angle, reach = rng.uniform(0, math.tau), rng.uniform(20, 200)
        width, ink = rng.uniform(2, 6), rng.choice(names)
        canvas.line(x, y, x + reach * math.cos(angle), y + reach * math.sin(angle), width, shade(k) if crowded else ink)
    for _ in range(300):
        canvas.dot(rng.uniform(0, 900), rng.uniform(0, 1000), rng.uniform(3, 12), rng.choice(names), rng.random() < 0.7)
    canvas.rect(0, 960, 900, 240, "paper")
    for i in range(12):
        canvas.text(40, 985 + i * 18, "line %d of twelve \u00b7 4000 strokes of 20 to 200 px, 300 dots, thrown anywhere" % (i + 1), 14)
    name = "crowded" if crowded else "scatter"
    canvas.save_png(os.path.join(folder, name + ".png"))
    seconds = time.perf_counter() - began
    canvas.save_svg(os.path.join(folder, name + ".svg"))
    return seconds, canvas._deep


def twig(pen):
    """A small branching figure: three weights, three inks, a ground line, labels and notes."""
    rng = random.Random(7)
    pen.unit_name = "lengths"
    pen.ground(0.0)
    tips = grow(pen, rng, 46, fresh=12, trunk=9.0)
    for i, (x, y) in enumerate(tips):
        if i % 3 == 0:
            pen.dot(x, y, 6.0, "dark-red")
        elif i % 3 == 1:
            pen.dot(x, y, 7.0, "pink", filled=False, weight=3.0)
    top = max(tips, key=lambda tip: tip[1])
    pen.label(top[0], top[1] + 0.7, "leader", 14)
    pen.label(0.5, 0.35, "sown here", 14, "ink", "start")
    pen.note("46 lengths, %d tips" % len(tips))
    pen.note("12 lengths are new since the last visit")
    pen.note("a filled dot is a fruit, a ring is a bud")
    return pen


def specimen_sheet(folder):
    """The same figure in a large box with its scale bar, and in small boxes."""
    canvas = Canvas(900, 1200)
    canvas.inks["wood"] = "#6a2c91"
    boxes = [
        ((60, 60, 600, 900), {}, {}, ""),
        ((640, 60, 840, 230), {"scale_bar": False}, {}, "scale_bar=False"),
        ((640, 280, 840, 450), {"scale_bar": False}, {"pens": 0.5, "labels": False}, "pens=0.5, labels=False"),
        ((640, 500, 840, 670), {"scale_bar": False, "align": "center", "unit_px_max": 8.0}, {}, 'align="center", 8 px'),
        ((640, 720, 840, 900), {"unit_px_max": 10.0}, {}, "unit_px_max=10"),
    ]
    pens = []
    for box, asked, settings, words in boxes:
        x0, y0, x1, y1 = box
        canvas.rect(x0, y0, x1 - x0, y1 - y0, "faint", filled=False, width=1.0)
        pen = twig(canvas.specimen(box, **asked))
        for name, value in settings.items():
            setattr(pen, name, value)
        pen.settle()
        pens.append(pen)
        if words:
            canvas.text(x0, y1 + 20, words, 14, "grey")
    caption(canvas, "twig", ["trial \u00b7 foundations", "planted 2026-09-12 by claude-opus-5-5 \u00b7 18 days"], pens[0].notes)
    save(canvas, folder, "specimen")
    return canvas, pens


def ink_chart(folder):
    """Every named ink: a swatch, a bold and a fine stroke, a dot, a ring, and its name in ink and in itself."""
    probe = Canvas(10, 10)
    names = list(probe.inks)
    canvas = Canvas(900, 110 + 58 * len(names))
    canvas.text(40, 44, "the inks", 24)
    y = 70
    for name in names:
        y += 58
        canvas.rect(38, y - 24, 64, 32, "faint", filled=False, width=1.0)
        canvas.rect(40, y - 22, 60, 28, name)
        canvas.line(124, y - 8, 204, y - 8, 8.0, name)
        canvas.line(224, y - 8, 304, y - 8, 2.0, name)
        canvas.dot(336, y - 8, 9.0, name)
        canvas.dot(372, y - 8, 9.0, name, filled=False, width=2.5)
        canvas.text(410, y, name, 18)
        canvas.text(540, y, canvas.inks[name], 14, "grey")
        canvas.text(640, y, name + " 0123 lengths", 18, name)
    save(canvas, folder, "inks")
    return names


def _shade_run(count):
    """count inks, every one different from every other, from the paper, and from the named inks, and none too pale.

    Multiplying by an odd number shuffles all 2**24 colours without
    putting two on one place, so n -> n * 0x9e3779 mod 2**24 never repeats.
    The few that would be the paper, a named ink, or so pale that the
    plate would give them a rim are passed over.
    """
    paper = plate._rgb(plate.PAPER)
    taken = {plate._rgb(colour) for colour in plate.INKS.values()} | {paper}
    run, n = [], 0
    while len(run) < count:
        n += 1
        value = n * 0x9E3779 % (1 << 24)
        rgb = (value >> 16, (value >> 8) & 255, value & 255)
        if rgb not in taken and sum(abs(a - b) for a, b in zip(rgb, paper)) >= plate.PALE:
            run.append("#%06x" % value)
    return run


SHADES = _shade_run(4096)


def shade(i):
    """The i-th of 4,096 inks that are all different: far more than one byte can number."""
    return SHADES[i % len(SHADES)]


def cross(canvas, cx, cy, reach):
    """Two faint axes through a point."""
    canvas.line(cx - reach, cy, cx + reach, cy, 1.5, "faint")
    canvas.line(cx, cy - reach, cx, cy + reach, 1.5, "faint")


def canvas_arcs(canvas, cx, cy):
    """Four arcs on the canvas, one to a quadrant: a dot at each start, its angles written inside it."""
    cross(canvas, cx, cy, 115)
    for start, end, ink in QUADRANTS:
        canvas.arc(cx, cy, 90, start, end, 6.0, ink)
        a, m = math.radians(start), math.radians((start + end) / 2)
        canvas.dot(cx + 90 * math.cos(a), cy - 90 * math.sin(a), 6.0, "ink")
        canvas.text(cx + 50 * math.cos(m), cy - 50 * math.sin(m) + 5, "%d..%d" % (start, end), 14, ink, "middle")


def turned_arcs(canvas, cx, cy):
    """Arcs asked for the other way round, across 0, more than once round, all but once round, and not at all."""
    cross(canvas, cx, cy, 115)
    asked = ((100, 90, 0, "red", "90..0 runs clockwise"), (80, 350, 10, "blue", "350..10 is the long way round"),
             (60, 350, 370, "fresh", "350..370 crosses 0"), (40, 0, 1000, "orange", "0..1000 is a circle"),
             (30, 45, 404.99, "brown", "45..404.99 stops just short"), (20, 30, 30, "violet", "30..30 is a dot"))
    for row, (r, start, end, ink, words) in enumerate(asked):
        canvas.arc(cx, cy, r, start, end, 5.0, ink)
        a = math.radians(start)
        if end != start:                           # the arc that goes nowhere is its own dot
            canvas.dot(cx + r * math.cos(a), cy - r * math.sin(a), 4.0, "ink")
        canvas.text(cx - 110, cy + 138 + 18 * row, words, 14, ink)


def specimen_arcs(canvas, box):
    """The same four arcs drawn by a Specimen, where y runs up: on the page they must lie as the canvas's do."""
    pen = canvas.specimen(box, unit_px_max=200.0)
    pen.unit_name = "unit, units"
    pen.line(-1.25, 0, 1.25, 0, 2.0, "faint")
    pen.line(0, -1.25, 0, 1.25, 2.0, "faint")
    for start, end, ink in QUADRANTS:
        pen.arc(0, 0, 1, start, end, 6.0, ink)
        a, m = math.radians(start), math.radians((start + end) / 2)
        pen.dot(math.cos(a), math.sin(a), 6.0, "ink")
        pen.label(0.56 * math.cos(m), 0.56 * math.sin(m) - 0.06, "%d..%d" % (start, end), 14, ink)
    pen.settle()


def cell_fields(canvas, box):
    """Cells in a solid field, in a chequerboard, and as hairlines a two-hundredth of a cell thick, lying and standing."""
    pen = canvas.specimen(box)
    pen.unit_name = "cell, cells"
    for i in range(12):
        for j in range(12):
            pen.cell(i, j)
            if (i + j) % 2 == 0:
                pen.cell(14 + i, j, 1, 1, "blue")
        pen.cell(28, i + 0.5, 6, 0.005, "ink")
        pen.cell(35.5 + i / 2, 0, 0.005, 12, "ink")
    pen.settle()


def anchored_words(canvas, x, y):
    """The three anchors, each holding its words to the same red guide line."""
    canvas.line(x, y - 26, x, y + 70, 1.5, "red")
    for row, anchor in enumerate(("start", "middle", "end")):
        canvas.text(x, y + 30 * row, 'anchor "%s"' % anchor, 18, "ink", anchor)


def many_inks(canvas, box, count=300):
    """A plant of three hundred strokes, each in an ink of its own, and one dot in yet another."""
    pen = canvas.specimen(box, scale_bar=False)
    for i in range(count):
        pen.line(i, 0, i, 14 + 5 * math.sin(i / 15.0), 3.0, shade(i))
    pen.dot(count / 2, 26, 8.0, "#ff00ff")
    pen.settle()


def white_flowers(canvas, box, pens=1.0):
    """A stem with white flowers: white on cream, which would not show without its rim.

    The flower at the top is five white petals drawn from one centre, and
    a white shoot runs off to the right a length at a time: each must come
    out as one white figure with one grey edge, not as pieces rimmed apart.
    """
    pen = canvas.specimen(box, scale_bar=False)
    pen.pens = pens
    pen.ground(0.0)
    pen.line(0, 0, 0, 8, 6.0)
    tips = []
    for at, lean in ((3, -1), (4, 1), (6, -1)):
        pen.line(0, at, 2.2 * lean, at + 2.2, 4.0)
        tips.append((2.2 * lean, at + 2.2))
    for x, y in tips:
        pen.dot(x, y, 8.0, "white")
    for k in range(5):
        a = math.radians(90 + 72 * k)
        pen.line(0, 8, 1.3 * math.cos(a), 8 + 1.3 * math.sin(a), 7.0, "white")
    pen.dot(0, 8, 4.0, "yellow")
    x, y = 0.0, 1.5
    for rise in (0.5, 0.35, 0.2, 0.05):
        pen.line(x, y, x + 0.9, y + rise, 5.0, "white")
        x, y = x + 0.9, y + rise
    pen.settle()


def narrow_boxes(canvas, x, y):
    """A figure in boxes of 96 to 240 px: each must have its scale bar, however little room there is."""
    for width, reach in ((96, 40), (120, 1.2), (150, 99), (200, 7), (240, 5000)):
        canvas.rect(x, y, width, 150, "faint", filled=False, width=1.0)
        pen = canvas.specimen((x, y, x + width, y + 150))
        pen.unit_name = "length, lengths"
        pen.line(0, 0, reach, reach * 0.6, 4.0)
        pen.settle()
        canvas.text(x, y + 168, "%d px" % width, 14, "grey")
        x += width + 12


def flowers_and_fruit(canvas, x, y):
    """Fruit that cross, kept apart; a fruit over a canopy's edge; flowers of 5, 4 and 3 round petals, and a dead one.

    Drawn one unit to the pixel, at the sizes a stray draws its flowers. A
    dark eye lies on its petals with no ring round it; the grey eye of the
    dead flower, among grey petals, has its line of paper, which is all
    that shows it.
    """
    pen = canvas.specimen((x, y, x + 180, y + 110), unit_px_max=1.0, scale_bar=False, align="center")
    for fx, fy in ((-80, 4), (-70, 6), (-75, -4), (-64, -3), (-58, 7), (-86, -6)):
        pen.dot(fx, fy, 6.0, "red")
    pen.dot(20, 0, 30.0, "brown")
    pen.dot(52, 6, 6.0, "brown")
    pen.dot(46, -18, 5.0, "red")
    pen.settle()
    for k, (n, petal, eye) in enumerate(((5, "#d8321f", "#56140c"), (4, "#d8321f", "#56140c"), (3, "blue", "#0f2850"),
                                         (5, "dead", "dead"))):
        left = x + 190 + 72 * k
        pen = canvas.specimen((left, y, left + 72, y + 110), unit_px_max=1.0, scale_bar=False, align="center")
        for j in range(n):
            a = math.radians(90.0 + 180.0 / n + 360.0 * j / n)
            pen.dot(17.36 * math.cos(a), 17.36 * math.sin(a), 20.0 - n, petal)
        pen.dot(0, 0, 6.0, eye)
        pen.settle()


def no_bars(canvas, x, y):
    """A seed alone, which has nothing for a bar to measure, and a calendar of lettered months that declines its bar."""
    canvas.rect(x, y, 120, 110, "faint", filled=False, width=1.0)
    pen = canvas.specimen((x, y, x + 120, y + 110))
    pen.unit_name = "length, lengths"
    pen.ground(0)
    pen.dot(0, -0.3, 6.0, "blue")
    pen.settle()
    canvas.rect(x + 135, y, 200, 110, "faint", filled=False, width=1.0)
    pen = canvas.specimen((x + 135, y, x + 335, y + 110), unit_px_max=14.0)
    pen.unit_name = "month, months"
    pen.scale_bar = False                          # the letters are its measure
    pen.ground(0)
    for m, tall in enumerate((5, 3, 4, 2, 1, 1, 0, 1, 2, 4, 5, 6)):
        if tall:
            pen.cell(m + 0.2, 0, 0.6, tall * 0.5, "blue")
        pen.label(m + 0.5, -1.4, "JFMAMJJASOND"[m], 14)
    pen.settle()


def marks_sheet(folder):
    """What the other sheets leave out. Every part of it is a thing that once went wrong without being seen."""
    canvas = Canvas(900, 1220)
    canvas.inks["wood"] = "#00808a"
    canvas.text(30, 34, "arcs by quadrant: on the canvas, turned, and by a specimen \u00b7 a dot marks each start", 14, "grey")
    canvas_arcs(canvas, 150, 170)
    turned_arcs(canvas, 440, 170)
    specimen_arcs(canvas, (600, 50, 870, 330))
    canvas.text(30, 436, "cells: a solid field, a chequerboard, hairlines lying and standing \u00b7 the three anchors", 14, "grey")
    cell_fields(canvas, (30, 450, 560, 660))
    anchored_words(canvas, 740, 510)
    canvas.text(30, 696, "three hundred inks on one plate, and a magenta dot \u00b7 white flowers and a white shoot", 14, "grey")
    many_inks(canvas, (30, 710, 560, 800))
    white_flowers(canvas, (600, 670, 760, 800))
    white_flowers(canvas, (790, 720, 860, 800), pens=0.4)
    canvas.text(30, 834, "scale bars in narrow boxes", 14, "grey")
    narrow_boxes(canvas, 30, 846)
    canvas.text(30, 1046, "dots: fruit kept apart, and one over a canopy's edge \u00b7 dark eyes on round petals, "
                "left alone \u00b7 a dead flower's grey eye, parted", 14, "grey")
    flowers_and_fruit(canvas, 30, 1058)
    canvas.text(530, 1196, "no bars: a seed alone \u00b7 months lettered", 14, "grey")
    no_bars(canvas, 530, 1066)
    save(canvas, folder, "marks")


def stipple(pen, x, y, width, height, apart, rng):
    """Dots of the smallest size scattered over a patch, never closer than `apart` pixels (one unit is one pixel)."""
    placed = []
    for _ in range(width * height // (apart * apart) * 3):
        px, py = x + rng.uniform(0, width), y + rng.uniform(0, height)
        if all((px - qx) ** 2 + (py - qy) ** 2 >= apart * apart for qx, qy in placed):
            placed.append((px, py))
            pen.dot(px, py, 3.0)
    return len(placed)


def doubled(pen, points, apart, weight=2.0):
    """A doubled stroke: the same path twice, `apart` pixels between the two middle lines, as a kind draws cork or wax."""
    for side in (-0.5, 0.5):
        shifted = []
        for i, (x, y) in enumerate(points):
            (ax, ay), (bx, by) = points[max(0, i - 1)], points[min(len(points) - 1, i + 1)]
            length = math.hypot(bx - ax, by - ay) or 1.0
            shifted.append((x - side * apart * (by - ay) / length, y + side * apart * (bx - ax) / length))
        pen.polyline(shifted, weight)


def broken(pen, x0, y0, x1, y1, piece, gap, weight=2.0):
    """A broken line: short strokes `piece` pixels long with `gap` pixels between their ends, as a kind draws what is brittle."""
    length = math.hypot(x1 - x0, y1 - y0)
    at = 0.0
    while at < length:
        end = min(length, at + piece)
        pen.line(x0 + (x1 - x0) * at / length, y0 + (y1 - y0) * at / length,
                 x0 + (x1 - x0) * end / length, y0 + (y1 - y0) * end / length, weight)
        at = end + gap


def texture_rows(pen, rng):
    """The three textures of GROUND.md at their finest, drawn with one unit to the pixel (y up, as a kind draws)."""
    for row, apart in enumerate((7, 9, 12)):                   # stipple, in a row and scattered
        for k in range(12):
            pen.dot(k * apart, 150 - 12 * row, 3.0)
    stipple(pen, 160, 118, 120, 36, 8, rng)
    stipple(pen, 300, 118, 120, 36, 11, rng)
    for column, phase in enumerate((0.0, 0.25, 0.5, 0.75)):      # doubled, at four places within the pixel
        x = column * 110 + phase
        doubled(pen, [(x, 92 + phase), (x + 90, 92 + phase)], 3.0)
        doubled(pen, [(x, 74 + phase), (x + 90, 74 + phase)], 5.0)
        doubled(pen, [(x + 5, 4), (x + 5, 60)], 3.0)
        doubled(pen, [(x + 22, 4), (x + 22, 60)], 5.0)
        doubled(pen, [(x + 40 + 22 * math.sin(a / 12.0), 4 + a * 56 / 36.0) for a in range(37)], 3.0)
        doubled(pen, [(x + 65, 4), (x + 95, 60)], 3.0)
    for row, (piece, gap) in enumerate(((6, 4), (4, 4), (8, 6))):    # broken, level and slanting
        broken(pen, 460, 150 - 18 * row, 700, 150 - 18 * row, piece, gap)
        broken(pen, 460 + 90 * row, 4, 520 + 90 * row, 90, piece, gap)


def texture_sheet(folder):
    """Stipple, a doubled stroke and a broken line, drawn with the finest pens a kind has: do they read as textures?

    Top: at the plate's own pens (2 px strokes, dots of r 3). Below: the
    same at the pens of a bed sheet (0.3), where strokes are 1.25 px and
    dots r 1.5. Each doubled stroke is drawn at four places within the
    pixel (0, 1/4, 1/2, 3/4 of a pixel off), since two lines 3 px apart
    leave a single pixel of paper between them, and whether that pixel is
    clear depends on where the lines fall (the plate sets level and
    upright strokes on the pixels for this; see plate._on_pixels).

    A kind draws its texture in plant units, so the spacing shrinks with
    the fit while the pens do not: a doubled stroke drawn 0.05 units apart
    is 3 px apart at 60 px a unit and merges into one line at 20. On a bed
    sheet, where every plant is drawn small, textures are mostly lost; the
    plate is where they are read.
    """
    canvas = Canvas(900, 560)
    canvas.inks["wood"] = "#5a4632"
    for pens, top, stroke, dot in ((1.0, 20, "2 px", "3"), (0.3, 300, "1.25 px", "1.5")):
        canvas.text(20, top + 14, "pens %g%s \u00b7 stipple: dots of r %s in rows 7, 9 and 12 px apart; scattered 8 and 11 px apart"
                    % (pens, "" if pens == 1 else ", as on a bed sheet", dot), 14, "grey")
        canvas.text(20, top + 32, "doubled: two %s strokes 3 px apart (and 5 px), level, upright, curved and slanting, "
                    "at 0, 1/4, 1/2, 3/4 px" % stroke, 14, "grey")
        canvas.text(20, top + 50, "broken: %s strokes 6, 4 and 8 px long, gaps of 4, 4 and 6 px between their ends" % stroke,
                    14, "grey")
        pen = canvas.specimen((20, top + 60, 880, top + 240), unit_px_max=1.0, scale_bar=False, align="center")
        pen.pens = pens
        texture_rows(pen, random.Random(5))
        pen.settle()
    save(canvas, folder, "textures")
    return canvas


# ------------------------------------------------------------------ checks

def dark(pixels, width, x, y):
    """How much black ink is on one pixel of a plate of default paper: 0 none .. 1 full."""
    return (251 - pixels[(y * width + x) * 3]) / 251.0


def inked_box(canvas):
    """(x0, y0, x1, y1) of everything that is not paper, or None."""
    pixels = canvas.pixels()
    paper = bytes(plate._rgb(canvas.inks["paper"]))
    row = canvas.width * 3
    rows = [y for y in range(canvas.height) if pixels[y * row:(y + 1) * row] != paper * canvas.width]
    if not rows:
        return None
    columns = []
    for y in rows:
        line = pixels[y * row:(y + 1) * row]
        marked = [x for x in range(canvas.width) if line[x * 3:x * 3 + 3] != paper]
        columns += [marked[0], marked[-1]]
    return min(columns), rows[0], max(columns) + 1, rows[-1] + 1


def check_every_letter():
    """Each character leaves a mark, and no two leave the same one."""
    seen, blank, twins = {}, [], []
    for ch in plate.SUPPORTED:
        if ch == " ":
            continue
        canvas = Canvas(60, 60)
        canvas.text(30, 40, ch, 34, "black", "middle")
        mark = bytes(canvas.pixels())
        if inked_box(canvas) is None:
            blank.append(ch)
        if mark in seen:
            twins.append(seen[mark] + ch)
        seen[mark] = ch
    detail = "%d characters" % len(seen)
    if blank:
        detail += "; blank: " + " ".join(blank)
    if twins:
        detail += "; the same mark: " + " ".join(twins)
    verdict("lettering: every character leaves a mark of its own", not blank and not twins, detail)


def check_widths_and_anchors():
    """text() returns text_width(), and the three anchors put the words where they say."""
    words = "quince \u00b7 9\u201315\u00b0 \u00e9t\u00e9"
    worst = 0.0
    for size in SIZES:
        told = Canvas(10, 10).text_width(words, size)
        boxes = []
        for anchor in ("start", "middle", "end"):
            sheet = Canvas(900, 70)
            returned = sheet.text(450, 45, words, size, "black", anchor)
            worst = max(worst, abs(returned - told))
            boxes.append(inked_box(sheet))
        start, middle, end = boxes
        slack = 0.12 * size + 1                    # the room the face keeps beside a letter
        worst = max(worst, abs(start[0] - 450) - slack, abs(end[2] - 450) - slack,
                    abs((middle[0] + middle[2]) / 2 - 450) - slack, abs((start[2] - start[0]) - told) - 2 * slack)
    verdict("lettering: text() returns text_width(), and the anchors hold", worst <= 0.0,
            "worst miss %.2f px" % max(worst, 0.0))


def check_stamps():
    """A letter pressed from its stamp is, pixel for pixel, the letter drawn stroke by stroke."""
    rng = random.Random(64)
    differ = 0
    for _ in range(40):
        size = rng.choice((10, 14, 18, 24, 34, 64))
        x, y = rng.uniform(-40, 380), rng.uniform(-10, 130)
        words = rng.choice(("quince, 214 lengths", "Wjg|_^ 2026", plate.SUPPORTED))
        anchor, halo = rng.choice(("start", "middle", "end")), rng.random() < 0.4
        pictures = []
        for stamped in (plate.STAMPED, 0):         # 0: nothing is pressed, every letter is drawn
            kept, plate.STAMPED = plate.STAMPED, stamped
            canvas = Canvas(360, 120)
            canvas.rect(0, 0, 360, 120, "pale-pink")
            canvas.text(x, y, words, size, "ink", anchor, halo=halo)
            pictures.append(bytes(canvas.pixels()))
            plate.STAMPED = kept
        differ += pictures[0] != pictures[1]
    verdict("lettering: a pressed letter is exactly a drawn one", not differ,
            "%d of 40 lines differ" % differ if differ else "40 lines, on and off the plate's edge")


def ink_width(ch, size):
    """How many pixels wide the ink of one character is."""
    canvas = Canvas(120, 80)
    canvas.text(20, 50, ch, size, "black")
    box = inked_box(canvas)
    return box[2] - box[0]


def check_dashes():
    """The hyphen, the en dash and the em dash are of three lengths that cannot be taken for one another."""
    faults, said = [], ""
    for size in SIZES:
        hyphen, en, em = (ink_width(ch, size) for ch in "-\u2013\u2014")
        said = said or "at size %d they are %d, %d and %d px" % (size, hyphen, en, em)
        if en < 1.7 * hyphen or em < en + 0.25 * size:
            faults.append("at size %d they are %d, %d and %d px" % (size, hyphen, en, em))
    verdict("lettering: the en dash is nearly twice the hyphen, the em dash longer again", not faults,
            "; ".join(faults) or said)


def check_stand_ins():
    """Characters the face lacks fall back to a base letter, a stand-in or '?', and none raises."""
    canvas = Canvas(300, 80)
    width = canvas.text_width
    pairs = [("\u00c9", "E"), ("\u00f1", "n"), ("\u0153", "oe"), ("\u2019", "'"), ("\u201c", '"'),
             ("\u2212", "-"), ("\u4e2d", "?"), ("\U0001f331", "?"), ("a\nb", "a b"), ("\ufb01", "fi"), ("\u00bd", "1/2")]
    wrong = [a for a, b in pairs if abs(width(a, 20) - width(b, 20)) > 1e-9]
    marks = []
    for words in ("e\u0301te\u0301 nai\u0308ve c\u0327a", "\u00e9t\u00e9 na\u00efve \u00e7a"):     # in two pieces, and whole
        sheet = Canvas(200, 50)
        sheet.text(10, 35, words, 20)
        marks.append(bytes(sheet.pixels()))
    if marks[0] != marks[1]:
        wrong.append("a letter followed by its accent")
    try:
        canvas.text(10, 40, "".join(a for a, _ in pairs) + "\x00\x07\u200b\u0301", 20)
        raised = ""
    except Exception as error:
        raised = repr(error)
    detail = "%d fallbacks, and an accent that arrives after its letter" % len(pairs)
    verdict("lettering: what the face lacks falls back, and never raises", not wrong and not raised,
            raised or ("wrong: " + " ".join(map(repr, wrong)) if wrong else detail))


def check_inks(names):
    """In the middle of a stroke, a named ink is exactly itself; an unknown ink is 'ink'."""
    canvas = Canvas(200, 40 * len(names) + 120)
    wrong = []
    for i, name in enumerate(names):
        y = 30 + 40 * i
        canvas.line(20, y, 180, y, 9.0, name)
        if canvas.pixel(100, y) != canvas.inks[name]:
            wrong.append(name)
    y = 30 + 40 * len(names)
    canvas.line(20, y, 180, y, 9.0, "#4a7bd0")
    canvas.line(20, y + 40, 180, y + 40, 9.0, "no-such-ink")
    canvas.line(20, y + 80, 180, y + 80, 9.0, ["not", "an", "ink"])
    if canvas.pixel(100, y) != "#4a7bd0":
        wrong.append("#4a7bd0")
    if canvas.pixel(100, y + 40) != canvas.inks["ink"] or canvas.pixel(100, y + 80) != canvas.inks["ink"]:
        wrong.append("an unknown ink")
    if canvas.pixel(100, 10) != canvas.inks["paper"]:
        wrong.append("the ground is not plain paper")
    verdict("inks: each named ink is exactly itself in the middle of a stroke", not wrong,
            "wrong: " + ", ".join(wrong) if wrong else "%d inks, a #rrggbb, and an unknown one drawn in 'ink'" % len(names))


def check_many_inks():
    """More inks than one byte can number are each exactly themselves, and the plate is none the worse for them."""
    wrong = []
    crowded = Canvas(320, 120)
    twig(crowded.specimen((10, 40, 110, 110), scale_bar=False)).settle()      # drawn while the inks are still numbered
    for i in range(300):
        crowded.rect(10 + i, 5, 1, 20, shade(i))
    crowded.inks["wood"] = "#1f4e9c"
    crowded.line(130, 60, 300, 60, 9.0, "wood")
    crowded.line(130, 80, 300, 80, 9.0, "fresh")
    crowded.dot(215, 100, 8.0, "#ff00ff")
    off = sum(1 for i in range(300) if crowded.pixel(10 + i, 15) != shade(i))
    if off:
        wrong.append("%d of 300 inks are not themselves" % off)
    if crowded.pixel(215, 60) != "#1f4e9c" or crowded.pixel(215, 80) != crowded.inks["fresh"]:
        wrong.append("a named ink on a crowded plate")
    if crowded.pixel(215, 100) != "#ff00ff" or "#ff00ff" in SHADES[:300]:
        wrong.append("the 301st ink drew as %s" % crowded.pixel(215, 100))
    if len(set(SHADES)) != len(SHADES):
        wrong.append("the trial's inks are not all different")
    if crowded._deep != 3:                         # else this check has quietly stopped trying full colour
        wrong.append("the crowded plate never went over to full colour")
    pictures = []
    for crowd in (0, 300):                         # the same drawing on a plate of few inks, and on one that held many
        canvas = Canvas(200, 200)
        for i in range(crowd):
            canvas.rect(i % 200, 0, 1, 200, shade(i))
        if canvas._deep != (3 if crowd else 1):
            wrong.append("a plate of %d inks is %s" % (crowd + 1, "numbered" if canvas._deep == 1 else "in full colour"))
        canvas.rect(0, 0, 200, 200, "paper")
        twig(canvas.specimen((10, 10, 190, 190))).settle()
        canvas.text(100, 30, "quince \u00e9t\u00e9", 18, "blue", "middle", halo=True)
        pictures.append(bytes(canvas.pixels()))
    if pictures[0] != pictures[1]:
        wrong.append("a drawing differs on a plate that has held many inks")
    verdict("inks: three hundred on one plate are each exactly themselves", not wrong,
            "; ".join(wrong) if wrong else "300 different inks and a 301st, the named inks among them, in full colour; "
            "the drawing unchanged")


def check_wood():
    """'wood' is the ink it was when the mark was made: on one plate, two planters' plants each keep their own."""
    canvas = Canvas(200, 100)
    canvas.inks["wood"] = "#1f4e9c"
    first = canvas.specimen((0, 0, 100, 100), scale_bar=False)
    first.line(0, 0, 0, 1, 18.0)
    canvas.inks["wood"] = "#c25e00"
    second = canvas.specimen((100, 0, 200, 100), scale_bar=False)
    second.line(0, 0, 0, 1, 18.0)
    first.settle()
    second.settle()
    drawn = (canvas.pixel(50, 50), canvas.pixel(150, 50))
    verdict("inks: a plant keeps the 'wood' it was drawn with, whenever it is settled", drawn == ("#1f4e9c", "#c25e00"),
            "the first drew %s, the second %s" % drawn)


def grey_pixels(canvas, pixels, box):
    """How many pixels of box = (x0, y0, x1, y1) are grey: the colour of a rim, half way from the paper to black."""
    x0, y0, x1, y1 = box
    return sum(1 for x in range(x0, x1) for y in range(y0, y1) if 0.3 < dark(pixels, canvas.width, x, y) < 0.7)


def white_stem(beside=None):
    """Five white lengths drawn one at a time, 50 px each, and at each joint whatever `beside` draws there.

    Returns how many grey pixels lie down the middle of the stem: 2, its
    two ends, when it is one white figure with one edge.
    """
    stem = Canvas(200, 300)
    pen = stem.specimen((10, 10, 190, 290), scale_bar=False, unit_px_max=50.0)
    for k in range(5):
        pen.line(0, k, 0, k + 1, 14.0, "white")
        if beside:
            beside(pen, k + 1)
    pen.settle()
    pixels = stem.pixels()
    white = b"\xff\xff\xff"
    whites = [sum(pixels[(y * 200 + x) * 3:(y * 200 + x + 1) * 3] == white for y in range(300)) for x in range(200)]
    inside = [x for x in range(200) if whites[x] > max(whites) / 2]             # the stem stands wherever the paper drawn
    middle = (inside[0] + inside[-1]) // 2                                      # beside it has pushed it
    return grey_pixels(stem, pixels, (middle, 0, middle + 1, 300))


def check_white():
    """A white mark on the cream paper is given a rim and can be seen. A mark in the paper's own ink has none.

    The rim goes round the white figure, not round each stroke of it: a
    stem of white lengths drawn one at a time has grey only at its two
    ends, whatever is drawn at its joints: a red bud on each, a dot of
    clear paper well to one side (which cut the stem into sausages once),
    or a halo of clear paper round a bud beside each joint, biting into
    the stem's edge (the plan's way of keeping two dots apart). And a white
    flower drawn on a patch of paper-coloured ink keeps its rim.
    """
    rims, centres = {}, {}
    for ink in ("white", "paper", "yellow"):
        canvas = Canvas(60, 60)
        pen = canvas.specimen((0, 0, 60, 60), scale_bar=False, align="center")
        pen.dot(0, 0, 10.0, ink)
        pen.settle()
        rims[ink] = grey_pixels(canvas, canvas.pixels(), (0, 0, 60, 60))
        centres[ink] = canvas.pixel(30, 30)
    joints = [white_stem(lambda pen, y: pen.dot(0, y, 4.0, "red")),
              white_stem(lambda pen, y: pen.dot(1.2, y - 0.5, 4.0, "paper")),
              white_stem(lambda pen, y: (pen.dot(0.2, y, 7.0, "paper"), pen.dot(0.2, y, 4.0, "red")))]
    patch = Canvas(80, 80)
    pen = patch.specimen((0, 0, 80, 80), scale_bar=False, align="center")
    pen.dot(0, 0, 30.0, "black")
    pen.dot(0, 0, 20.0, "paper")
    pen.dot(0, 0, 10.0, "white")
    pen.settle()
    patched = grey_pixels(patch, patch.pixels(), (27, 27, 53, 53))            # inside the cleared patch
    holds = (rims["white"] >= 40 and centres["white"] == "#ffffff" and not rims["paper"] and not rims["yellow"]
             and joints == [2, 2, 2] and patched >= 40)
    verdict("inks: a white figure has a grey rim round it and can be seen; no other has one", holds,
            "grey pixels round a dot of r 10: white %d, paper %d, yellow %d; down a stem of five white lengths "
            "with buds, paper dots or halos at its joints %s (2: its ends); round a white dot on cleared paper %d"
            % (rims["white"], rims["paper"], rims["yellow"], "/".join(map(str, joints)), patched))


def measured_width(width, how):
    """Draw one black stroke and measure its thickness by the ink on a cut across it."""
    canvas = Canvas(200, 200)
    if how == "level":
        canvas.line(-30, 100.3, 230, 100.3, width, "black")
        slant = 1.0
    elif how == "upright":
        canvas.line(100.3, -30, 100.3, 230, width, "black")
        slant = 1.0
    else:
        canvas.line(-30, 40.0, 230, 150.0, width, "black")
        slant = math.cos(math.atan2(110.0, 260.0))
    pixels = canvas.pixels()
    if how == "upright":
        return sum(dark(pixels, 200, x, 100) for x in range(200))
    return sum(dark(pixels, 200, 100, y) for y in range(200)) * slant


def check_sizes():
    """A stroke is as wide as it is told, and a dot as large."""
    worst = 0.0
    for width in (1.0, 2.0, 3.0, 5.5, 12.0, 18.0):
        for how in ("level", "upright", "slanting"):
            worst = max(worst, abs(measured_width(width, how) - width))
    canvas = Canvas(100, 100)
    canvas.dot(50.2, 49.7, 7.0, "black")
    pixels = canvas.pixels()
    area = sum(dark(pixels, 100, x, y) for x in range(100) for y in range(100))
    off = abs(area - math.pi * 49.0) / (math.pi * 49.0)
    verdict("sizes: a stroke is as wide as it is told, a dot as large", worst <= 0.26 and off <= 0.02,
            "widths within %.2f px, a dot's area within %.1f%%" % (worst, off * 100))


def check_edges():
    """A slanting edge passes through many tones, and the paper beside it stays plain."""
    canvas = Canvas(200, 200)
    canvas.line(10, 30, 190, 170, 6.0, "black")
    pixels = canvas.pixels()
    tones = {pixels[i] for i in range(0, len(pixels), 3)}
    corner = canvas.pixel(190, 10)
    verdict("edges: smooth, on plain paper", len(tones) >= 12 and corner == canvas.inks["paper"],
            "%d tones along a slanting stroke" % len(tones))


def quadrants(draw):
    """Which quarters of a 200 x 200 plate hold ink once `draw` has drawn on it: 'NE', 'NW', 'SW', 'SE' as seen on the page."""
    canvas = Canvas(200, 200)
    draw(canvas)
    pixels = canvas.pixels()
    near, far = range(0, 94, 2), range(106, 200, 2)            # a band along each axis belongs to no quarter
    found = set()
    for name, xs, ys in (("NE", far, near), ("NW", near, near), ("SW", near, far), ("SE", far, far)):
        if any(dark(pixels, 200, x, y) > 0.5 for x in xs for y in ys):
            found.add(name)
    return found


def check_arcs():
    """An arc lies in the quadrants its angles name, on the canvas and on a specimen, whichever way it is asked for."""
    def on_canvas(start, end):
        return quadrants(lambda canvas: canvas.arc(100, 100, 70, start, end, 4.0, "black"))

    def on_specimen(start, end):
        def draw(canvas):
            pen = canvas.specimen((0, 0, 200, 200), scale_bar=False, align="center")
            pen.dot(-1.3, -1.3, 3.0, "paper")                  # two unseen corners, so that (0, 0) is the middle
            pen.dot(1.3, 1.3, 3.0, "paper")
            pen.arc(0, 0, 1, start, end, 4.0, "black")
            pen.settle()
        return quadrants(draw)

    everywhere = {"NE", "NW", "SW", "SE"}
    wanted = [((5, 85), {"NE"}), ((95, 175), {"NW"}), ((185, 265), {"SW"}), ((275, 355), {"SE"}),
              ((85, 5), {"NE"}), ((-85, -5), {"SE"}), ((350, 370), {"NE", "SE"}), ((350, 10), everywhere),
              ((0, 1000), everywhere), ((0, -360), everywhere)]
    faults = []
    for (start, end), where in wanted:
        for name, lies in (("canvas", on_canvas(start, end)), ("specimen", on_specimen(start, end))):
            if lies != where:
                faults.append("%s arc %d..%d lies %s" % (name, start, end, "+".join(sorted(lies)) or "nowhere"))
    verdict("arcs: counter-clockwise from +x with 90 up, on the canvas and on a specimen alike", not faults,
            "; ".join(faults[:3]) if faults else "%d arcs on each, some asked for clockwise, some across 0" % len(wanted))


def flaws(canvas, ink):
    """How many pixels inside a solid field of one ink are not exactly that ink (all, if there is no field to be seen).

    The field is found by its ink: the box round every pixel that is exactly the ink.
    """
    width, height = canvas.width, canvas.height
    pixels = bytes(canvas.pixels())
    ink = plate._rgb(canvas.inks.get(ink, ink))
    same = -1                                      # a bit for each pixel: set where all three of its parts are the ink's
    for part in range(3):
        table = bytes(1 if value == ink[part] else 0 for value in range(256))
        same &= int.from_bytes(pixels[part::3].translate(table), "big")
    same = same.to_bytes(width * height, "big")
    rows = [y for y in range(height) if 1 in same[y * width:(y + 1) * width]]
    if not rows:
        return width * height
    lefts = [same.index(1, y * width, (y + 1) * width) - y * width for y in rows]
    rights = [same.rindex(1, y * width, (y + 1) * width) - y * width for y in rows]
    x0, x1 = min(lefts), max(rights) + 1
    return sum((x1 - x0) - same[y * width + x0:y * width + x1].count(1) for y in range(rows[0], rows[-1] + 1))


def check_cells():
    """Cells laid side by side leave no seam, a chequerboard is half ink, and nothing is too thin to show.

    Besides fields at scales picked at random, which seldom put a cell's
    edge on a line of samples, three fields that once did, and showed a line
    of lighter pixels right through: 16 x 48 cells in a box of 373 x 440,
    9 x 80 in the box of a plant's plate, and 1 x 32 cells of 0.7 in the
    cell of a bed's sheet.
    """
    rng = random.Random(12)
    seams = 0
    for _ in range(20):
        canvas = Canvas(160, 160)
        pen = canvas.specimen((8, 8, 152, 152), unit_px_max=rng.uniform(0.7, 30.0), scale_bar=False)
        side = rng.randint(3, 30)
        for i in range(side):
            for j in range(side):
                pen.cell(i, j, 1, 1, "black")
        pen.settle()
        x0, y0, x1, y1 = inked_box(canvas)
        pixels = canvas.pixels()
        seams += sum(1 for y in range(y0 + 1, y1 - 1) for x in range(x0 + 1, x1 - 1) if pixels[(y * 160 + x) * 3])
    for size, box, wide, tall, side, ink, bar in (((393, 460), (10, 10, 383, 450), 16, 48, 1.0, "black", False),
                                                  ((900, 1200), (60, 50, 840, 930), 9, 80, 1.0, "#1f4e9c", True),
                                                  ((450, 600), (50.0, 160.0, 403.33, 522.0), 1, 32, 0.7, "black", False)):
        canvas = Canvas(*size)
        pen = canvas.specimen(box, scale_bar=bar)
        for i in range(wide):
            for j in range(tall):
                pen.cell(i * side, j * side, side, side, ink)
        pen.settle()
        seams += flaws(canvas, ink)
    canvas = Canvas(200, 200)
    pen = canvas.specimen((0, 0, 200, 200), scale_bar=False)
    for i in range(10):
        for j in range(10):
            if (i + j) % 2:
                pen.cell(i, j, 1, 1, "black")
    scale = pen.settle()
    pixels = canvas.pixels()
    share = sum(dark(pixels, 200, x, y) for x in range(200) for y in range(200)) / (10 * scale) ** 2
    lying, standing = Canvas(120, 400), Canvas(400, 120)
    lying_pen = lying.specimen((0, 0, 120, 400), scale_bar=False)
    standing_pen = standing.specimen((0, 0, 400, 120), scale_bar=False)
    for k in range(40):                            # forty cells each a twenty-fifth of a pixel thick, and forty more standing
        lying_pen.cell(0, k, 10, 0.004, "black")
        standing_pen.cell(k, 0, 0.004, 10, "black")
    lying_pen.settle()
    standing_pen.settle()
    down, across = lying.pixels(), standing.pixels()
    shown = sum(1 for y in range(1, 400) if down[(y * 120 + 60) * 3] != 251 and down[((y - 1) * 120 + 60) * 3] == 251)
    shown += sum(1 for x in range(1, 400) if across[(60 * 400 + x) * 3] != 251 and across[(60 * 400 + x - 1) * 3] == 251)
    lost = 0
    for k in range(40):                            # and on the bare canvas, a hairline at every place in the pixel
        level, upright = Canvas(60, 20), Canvas(20, 60)
        level.rect(10, 5 + k / 40.0, 40, 0.1, "black")                      # lying: somewhere in rows 0..7
        level.line(10, 12 + k / 40.0, 50, 12 + k / 40.0, 0.1, "black")      # and in rows 8..19
        upright.rect(5 + k / 40.0, 10, 0.03, 40, "black")                   # standing, finer than the samples' columns
        upright.line(12 + k / 40.0, 10, 12 + k / 40.0, 50, 0.03, "black")
        down, across = level.pixels(), upright.pixels()
        for places in (range(0, 8), range(8, 20)):
            lost += not any(down[(y * 60 + 30) * 3] != 251 for y in places)
            lost += not any(across[(30 * 20 + x) * 3] != 251 for x in places)
    holds = not seams and abs(share - 0.5) < 0.01 and shown == 80 and not lost
    verdict("cells: no seam in a solid field, a chequerboard half ink, no hairline lost", holds,
            "%d pixels of seam in 23 fields, %.1f%% ink, %d of 80 thin cells shown, %d of 160 hairlines lost"
            % (seams, share * 100, shown, lost))


def check_specimen_fit(pens):
    """Each figure stays inside its box and stands where it should, no larger than unit_px_max."""
    faults = []
    for pen in pens:
        if not 0 < pen.scale <= float(pen.unit_px_max) + 1e-9:
            faults.append("scale %.2f" % pen.scale)
    sheet = Canvas(400, 400)
    pen = twig(sheet.specimen((50, 60, 350, 340)))
    pen.settle()
    box = inked_box(sheet)
    if box[0] < 50 or box[1] < 60 or box[2] > 350 or box[3] > 340:
        faults.append("ink outside the box: %s" % (box,))
    small = Canvas(400, 400)
    pen = small.specimen((50, 60, 350, 340), scale_bar=False)
    pen.line(0, 0, 0, 1, 4.0, "black")
    scale = pen.settle()
    box = inked_box(small)
    if scale != 60.0:
        faults.append("a plant one unit high was drawn at %.2f px per unit" % scale)
    if abs((box[3] - box[1]) - 64) > 1 or abs(box[3] - 337) > 1:
        faults.append("a plant one unit high is %d px high, its foot at %d" % (box[3] - box[1], box[3]))
    tall = Canvas(400, 400)
    pen = tall.specimen((50, 60, 350, 340))
    pen.line(0, 0, 0, 5, 4.0)
    pen.label(0, 5, "\u00c9\u00c2|{[", 34)          # accented capitals and tall brackets, at the very top
    pen.settle()
    box = inked_box(tall)
    if box[1] < 60:
        faults.append("a label of tall letters stands %d px above its box" % (60 - box[1]))
    verdict("specimen: fits its box, stands on its floor, never above unit_px_max", not faults,
            "; ".join(faults) if faults else "scales " + ", ".join("%.1f" % pen.scale for pen in pens))


def check_scale_bar():
    """The bar is a round number of units, 80 to 200 px long, and measures exactly that on the plate."""
    faults = []
    worst = 0.0
    sizes = [0.3, 1, 2.5, 7, 13, 40, 99, 250, 1234, 56789, 3.0e6]
    for reach in sizes:
        canvas = Canvas(700, 500)
        pen = canvas.specimen((40, 40, 660, 460), unit_px_max=300.0)
        pen.line(0, 0, reach, reach * 0.5, 3.0, "black")
        scale = pen.settle()
        if pen.bar is None:
            faults.append("no bar for a plant %g wide" % reach)
            continue
        units, left, right, y = pen.bar
        lead = units / 10 ** math.floor(math.log10(units) + 1e-9)
        if min(abs(lead - r) for r in (1, 2, 5)) > 1e-6 or not 80 - 1e-6 <= units * scale <= 200 + 1e-6:
            faults.append("%g units make %.1f px" % (units, units * scale))
        pixels = canvas.pixels()
        row = int(y - 0.5)
        ink = sum((251 - pixels[(row * 700 + x) * 3]) / 225.0 for x in range(int(left) - 3, int(right) + 4))
        worst = max(worst, abs((ink - 2.0) - units * scale))       # the two end ticks add a pixel each
    narrow = 0
    for width in range(96, 400, 19):               # a narrow box still has its bar: shorter, round, and inside the box
        for reach in (0.3, 7, 40, 5000):
            canvas = Canvas(440, 200)
            pen = canvas.specimen((20, 20, 20 + width, 180))
            pen.unit_name = "a long name for one unit"
            pen.line(0, 0, reach, reach * 0.4, 3.0, "black")
            scale = pen.settle()
            narrow += 1
            if pen.bar is None:
                faults.append("no bar in a box %d px wide" % width)
                continue
            lead = pen.bar[0] / 10 ** math.floor(math.log10(pen.bar[0]) + 1e-9)
            if min(abs(lead - r) for r in (1, 2, 5)) > 1e-6 or pen.bar[0] * scale > 200 + 1e-6:
                faults.append("in a box %d px wide, %g units make %.1f px" % (width, pen.bar[0], pen.bar[0] * scale))
            if inked_box(canvas)[2] > 20 + width:
                faults.append("in a box %d px wide the bar or its words stand outside" % width)
    words = []
    for unit_px, name in ((100.0, "length, lengths"), (60.0, "length, lengths"), (100.0, "lengths")):
        canvas = Canvas(300, 300)
        pen = canvas.specimen((10, 10, 290, 290), unit_px_max=unit_px)
        pen.unit_name = name
        pen.line(0, 0, 1, 1)
        pen.settle()
        words.append(ElementTree.fromstring(canvas._svg()).findall("{*}g/{*}text")[-1].text)      # the bar's own words
    if words != ["1 length", "2 lengths", "1 lengths"]:
        faults.append("the bar's words were %s" % ", ".join(words))
    verdict("specimen: the scale bar is a round number of units and measures true", not faults and worst <= 0.3,
            "; ".join(faults[:3]) if faults else "%d plants, the bar within %.2f px; %d narrow boxes, each with its bar"
            % (len(sizes), worst, narrow))


def check_clamps():
    """Weights are kept to 2..18 px and dots to 3 px and up, whatever the scale.

    However far a weight runs away (a million, infinity, less than
    nothing), it is drawn at the nearest end of the range, never at some
    default: a trunk grown absurdly thick is drawn at its thickest. Only
    what is no number at all (NaN) is drawn at the default, 3 px.
    """
    measured = []
    asked = ((0.2, 60.0), (6.0, 60.0), (6.0, 3.0), (90.0, 60.0), (1e7, 60.0), (float("inf"), 60.0), (-1e7, 60.0),
             (float("nan"), 60.0))
    for weight, scale_max in asked:
        canvas = Canvas(300, 300)
        pen = canvas.specimen((0, 0, 300, 300), unit_px_max=scale_max, scale_bar=False, align="center")
        pen.line(-2, 0, 2, 0, weight, "black")
        pen.settle()
        pixels = canvas.pixels()
        measured.append(sum(dark(pixels, 300, 150, y) for y in range(300)))
    canvas = Canvas(100, 100)
    pen = canvas.specimen((0, 0, 100, 100), scale_bar=False, align="center")
    pen.dot(0, 0, 0.5, "black")
    pen.settle()
    pixels = canvas.pixels()
    area = sum(dark(pixels, 100, x, y) for x in range(100) for y in range(100))
    wanted = [2.0, 6.0, 6.0, 18.0, 18.0, 18.0, 2.0, 3.0]
    covered = []
    for r in (1e7, float("inf")):                  # a dot grown past all reason covers its whole box
        canvas = Canvas(100, 100)
        pen = canvas.specimen((0, 0, 100, 100), scale_bar=False, align="center")
        pen.dot(0, 0, r, "black")
        pen.settle()
        pixels = canvas.pixels()
        covered.append(sum(dark(pixels, 100, x, y) for x in range(100) for y in range(100)) / 10000.0)
    holds = (all(abs(a - b) <= 0.26 for a, b in zip(measured, wanted)) and abs(area - math.pi * 9) < 0.6
             and min(covered) > 0.99)
    verdict("specimen: sizes in pixels stay as told; weights kept to 2..18, dots to 3 and up", holds,
            "weights 0.2, 6, 6, 90, 1e7, inf, -1e7, nan drawn %s px; a dot of 0.5 drawn r %.2f; dots of 1e7 and inf "
            "cover %s of their box" % (", ".join("%.2f" % m for m in measured), math.sqrt(area / math.pi),
                                       " and ".join("%d%%" % round(100 * c) for c in covered)))


def check_fine_pens():
    """A sheet may ask for finer pens and no labels: pens = 0.5 halves the weights, down to 1.25 px."""
    measured, heights = [], []
    for weight in (6.0, 2.0):
        canvas = Canvas(300, 300)
        pen = canvas.specimen((0, 0, 300, 300), scale_bar=False, align="center")
        pen.pens = 0.5
        pen.labels = False
        pen.line(-2, 0, 2, 0, weight, "black")
        pen.label(0, 1, "left out")
        pen.settle()
        pixels = canvas.pixels()
        measured.append(sum(dark(pixels, 300, 150, y) for y in range(300)))
        box = inked_box(canvas)
        heights.append(box[3] - box[1])
    holds = abs(measured[0] - 3.0) <= 0.26 and abs(measured[1] - 1.25) <= 0.26 and max(heights) <= 4
    verdict("specimen: pens = 0.5 draws with finer pens, labels = False leaves the labels out", holds,
            "weights 6 and 2 drawn %.2f and %.2f px" % tuple(measured))


def check_no_bar():
    """scale_bar=False draws no bar and gives the drawing the whole box; so does a drawing with nothing to measure.

    The bar may be declined on the pen itself, pen.scale_bar = False before
    settle(), as well as when the pen is made: a calendar that letters its
    months has no use for a bar of months. (That is for whoever holds the
    Specimen: the ground, a trial. A kind's pen passes no scale_bar on, and
    a plant's plate keeps its bar; see GROUND.md, Run apart.) And a drawing
    in which nothing has a length
    (a seed alone: one dot, sized in pixels, under a ground line) has no
    bar, since the bar would measure only where the dot was put. Two dots
    apart are a length, and have their bar.
    """
    faults = []
    with_bar, without, declined = Canvas(300, 300), Canvas(300, 300), Canvas(300, 300)
    boxes = []
    for canvas, asked in ((with_bar, True), (without, False), (declined, None)):
        pen = canvas.specimen((10, 10, 290, 290), scale_bar=asked is not False)
        if asked is None:
            pen.scale_bar = False                  # declined on the pen once it is made, not when it is asked for
        pen.line(0, 0, 0, 30, 4.0, "black")
        pen.settle()
        boxes.append((pen.bar, inked_box(canvas), pen.scale))
    if not (boxes[0][0] is not None and boxes[1][0] is None and boxes[1][2] > boxes[0][2] and boxes[1][1][3] >= 286):
        faults.append("scale_bar=False: %.2f px per unit with the bar, %.2f without" % (boxes[0][2], boxes[1][2]))
    if boxes[2][0] is not None or bytes(declined.pixels()) != bytes(without.pixels()):
        faults.append("pen.scale_bar = False, set after the pen was made, is not as scale_bar=False")
    measures = []
    for words, draw in (("a seed alone", lambda pen: (pen.ground(0), pen.dot(0, -0.3, 6.0, "blue"))),
                        ("a dot and its words", lambda pen: (pen.dot(0, 0, 6.0), pen.label(0, 0.5, "a seed"))),
                        ("a stroke that goes nowhere", lambda pen: (pen.line(1, 1, 1, 1, 6.0), pen.dot(1, 1, 3.0))),
                        ("two dots apart", lambda pen: (pen.dot(0, 0, 6.0), pen.dot(1, 0, 6.0))),
                        ("a stroke", lambda pen: pen.line(0, 0, 0.5, 0, 4.0))):
        canvas = Canvas(300, 300)
        pen = canvas.specimen((10, 10, 290, 290))
        pen.unit_name = "length, lengths"
        draw(pen)
        pen.settle()
        measures.append(pen.bar is not None)
        if pen.measured != measures[-1]:
            faults.append("%s: pen.measured is %s" % (words, pen.measured))
        said = any("nothing drawn has a length" in line for line in canvas.remarks)
        if said == measures[-1]:
            faults.append("%s: %s, and the remarks %s" % (words, "a bar" if measures[-1] else "no bar",
                                                           "say there was nothing to measure" if said else "say nothing"))
    if measures != [False, False, False, True, True]:
        faults.append("bars for a seed alone, a dot and its words, a stroke that goes nowhere, two dots apart, a stroke: %s"
                      % ", ".join("yes" if bar else "no" for bar in measures))
    verdict("specimen: no bar when declined, or when nothing has a length; the drawing then has the whole box", not faults,
            "; ".join(faults) if faults else "%.2f px per unit with the bar, %.2f without; declined on the pen, the "
            "same; no bar for a seed alone, a dot with its words, a stroke that goes nowhere; a bar for two dots apart"
            % (boxes[0][2], boxes[1][2]))


def flower(n, petal, eye, D=17.36):
    """A flower as a stray draws one, on a plate of 120 x 120 with its eye at (60, 60): n round petals, a dark eye.

    The petals are dots of radius 20 - n (larger than APART_MOST: shapes),
    their centres D px from the eye; the eye is a dot of radius 6.
    Returns the canvas.
    """
    canvas = Canvas(120, 120)
    pen = canvas.specimen((0, 0, 120, 120), unit_px_max=1.0, scale_bar=False, align="center")
    pen.dot(-55, -55, 3.0, "paper")                # two unseen corners, so that (0, 0) is the middle
    pen.dot(55, 55, 3.0, "paper")
    for j in range(n):
        a = math.radians(90.0 + 180.0 / n + 360.0 * j / n)
        pen.dot(D * math.cos(a), D * math.sin(a), 20.0 - n, petal)
    pen.dot(0, 0, 6.0, eye)
    pen.settle()
    return canvas


def paler_round(canvas, cx, cy, inner, outer, than):
    """How many pixels between two radii round (cx, cy) are clearly paler than the ink `than`: a ring of paper."""
    pixels = canvas.pixels()
    floor_green = plate._rgb(canvas.inks.get(than, than))[1] + 40
    found = 0
    for y in range(int(cy - outer) - 1, int(cy + outer) + 2):
        for x in range(int(cx - outer) - 1, int(cx + outer) + 2):
            if inner <= math.hypot(x + 0.5 - cx, y + 0.5 - cy) <= outer and pixels[(y * canvas.width + x) * 3 + 1] > floor_green:
                found += 1
    return found


def check_apart():
    """Small dots that cross are kept apart by a line of paper; the dark eye of a flower of round petals is not.

    Fruit in a crowded crown are parted so that they can be counted, and
    so is a fruit hanging over the edge of a canopy of its own ink. But the
    eye in the middle of four or five round petals crosses every petal and
    lies inside none: parted, it wore a pale halo the flower does not have
    (seen on the scarlet and the bluebottle, 30 September). Its own ink
    tells it from the petals, so it is left alone. The grey eye of a dead
    flower, among petals of the same grey, is still parted: there the ring
    is all that shows it.
    """
    faults = []
    for n, petal, eye in ((5, "#d8321f", "#56140c"), (4, "#d8321f", "#56140c"), (3, "blue", "#0f2850")):
        halo = paler_round(flower(n, petal, eye), 60, 60, 6.3, 7.7, petal)
        if halo:
            faults.append("the eye of a flower of %d petals wears a halo of %d pale pixels" % (n, halo))
    dead = paler_round(flower(5, "dead", "dead"), 60, 60, 6.3, 7.7, "dead")
    if dead < 10:
        faults.append("the grey eye of a dead flower is lost among its grey petals (%d pale pixels round it)" % dead)
    canvas = Canvas(200, 100)                      # two fruit, crossing, and a fruit over a canopy's edge, all one ink
    pen = canvas.specimen((0, 0, 200, 100), unit_px_max=1.0, scale_bar=False, align="center")
    pen.dot(-60, 0, 6.0, "red")
    pen.dot(-50, 0, 6.0, "red")
    pen.dot(30, 0, 30.0, "red")
    pen.dot(62, 0, 6.0, "red")
    pen.settle()
    pixels = canvas.pixels()
    pale = plate._rgb(canvas.inks["red"])[1] + 40      # along the middle, a pixel greener than this is partly paper
    inked = [pixels[(50 * 200 + x) * 3 + 1] <= pale for x in range(200)]
    shown = sum(1 for x in range(200) if inked[x] and (x == 0 or not inked[x - 1]))
    if shown != 4:
        faults.append("two crossing fruit, a canopy and a fruit over its edge make %d runs of ink, not 4" % shown)
    verdict("dots: fruit that cross are parted; a dark eye on its round petals is not, a grey one on grey is",
            not faults, "; ".join(faults) if faults else "no pale pixel round the eyes of flowers of 5, 4 and 3 petals; "
            "%d round the eye of a dead one; crossing fruit and a fruit over a canopy's edge each stand apart" % dead)


def runs_of_ink(pixels, width, points):
    """How many separate runs of ink lie along a row or column of pixels, [(x, y), ...] in order."""
    paper = bytes(plate._rgb(plate.PAPER))
    runs, inked = 0, False
    for x, y in points:
        here = pixels[(y * width + x) * 3:(y * width + x) * 3 + 3] != paper
        runs += here and not inked
        inked = here
    return runs


def check_textures():
    """The textures of GROUND.md survive the finest pens: a doubled stroke stays two, a broken line keeps its gaps,
    a row of dots keeps its dots apart.

    A doubled stroke of two 2 px lines 3 px apart leaves one pixel of
    paper between them; it must be clear paper wherever the pair falls
    within the pixel, lying or standing. A broken line of 6 px strokes 4
    px apart must show every stroke, and a row of dots of r 3 8 px apart
    every dot. Each is drawn at four places within the pixel.
    """
    faults = []
    for phase in (0.0, 0.25, 0.5, 0.75):
        for standing in (False, True):
            canvas = Canvas(80, 80)
            pen = canvas.specimen((0, 0, 80, 80), unit_px_max=1.0, scale_bar=False)
            for side in (0.0, 3.0):
                a, b = (side + phase, 10), (side + phase, 60)
                pen.line(*(a + b) if standing else (a[1], a[0], b[1], b[0]), 2.0)
            pen.settle()
            pixels = canvas.pixels()
            across = [(x, 40) for x in range(80)] if standing else [(40, y) for y in range(80)]
            if runs_of_ink(pixels, 80, across) != 2:
                faults.append("a doubled stroke %s at %g px is one band" % ("standing" if standing else "lying", phase))
        canvas = Canvas(200, 60)
        pen = canvas.specimen((0, 0, 200, 60), unit_px_max=1.0, scale_bar=False)
        for k in range(12):
            pen.line(k * 10 + phase, 20 + phase, k * 10 + 6 + phase, 20 + phase, 2.0)
            pen.dot(k * 8 + phase, 40 + phase, 3.0)
        pen.settle()
        pixels = canvas.pixels()
        rows = {}
        for y in range(60):
            rows[y] = runs_of_ink(pixels, 200, [(x, y) for x in range(200)])
        if max(rows.values()) != 12:
            faults.append("at %g px a broken line or a row of dots has run together (%d runs)" % (phase, max(rows.values())))
    verdict("textures: a doubled stroke stays two, a broken line keeps its gaps, a row of dots its dots", not faults,
            "; ".join(faults[:3]) if faults else "2 px strokes 3 px apart, 6 px strokes 4 px apart and dots 8 px apart, "
            "each at four places in the pixel")


def check_remarks():
    """canvas.remarks says in a few plain lines what was drawn otherwise than asked; a plain drawing leaves it empty."""
    plain = Canvas(300, 300)
    twig(plain.specimen((10, 10, 290, 290))).settle()
    odd = Canvas(300, 300)
    pen = odd.specimen((10, 10, 70, 290))           # too narrow for a scale bar
    pen.line(0, 0, 0, 1, 90.0, "no-such-ink")
    pen.line(float("nan"), 0, 0, 1)
    pen.dot(0, 1, 1.0)
    pen.align = "left"
    pen.settle()
    pen.line(0, 0, 1, 1)
    for k in range(40):                             # forty inks not known: the remarks stay short
        odd.line(0, 0, 10, 10, 3.0, "ink number %d" % k)
    wanted = ("no-such-ink", "a line was left out", "weight over 18", "radius under 3", "no room for a scale bar",
              "align 'left'", "after settle()")
    missing = [words for words in wanted if not any(words in line for line in odd.remarks)]
    holds = not plain.remarks and not missing and len(odd.remarks) <= plate.REMARKS
    verdict("remarks: what was drawn otherwise than asked is said, briefly; a plain drawing says nothing", holds,
            "a plain twig: %s; missing: %s" % (plain.remarks or "nothing", ", ".join(missing)) if not holds else
            "%d lines for seven odd things and forty unknown inks, e.g. %r" % (len(odd.remarks), odd.remarks[0]))


def check_odd_input():
    """Odd numbers, empty lists and boxes of no size raise nothing and draw nothing."""
    canvas = Canvas(120, 120)
    raised = []

    def attempt(what, *args, **more):
        try:
            return what(*args, **more)
        except Exception as error:
            raised.append("%s%r: %r" % (getattr(what, "__name__", "?"), args, error))

    for odd in ODD:
        attempt(canvas.line, odd, 10, 50, 50)
        attempt(canvas.line, 10, 10, 50, odd)
        attempt(canvas.line, 10, 10, 50, 50, odd)
        attempt(canvas.polyline, odd)
        attempt(canvas.polyline, [(10, 10), (odd, 20)])
        attempt(canvas.polyline, [(10, 10), (30, 20)], odd)
        attempt(canvas.rect, odd, 10, 20, 20)
        attempt(canvas.rect, 10, 10, odd, 20)
        attempt(canvas.dot, 50, odd, 5)
        attempt(canvas.dot, 50, 50, odd)
        attempt(canvas.arc, 50, 50, odd, 0, 90)
        attempt(canvas.arc, 50, 50, 20, odd, 90)
        attempt(canvas.text, odd, 50, "words")
        attempt(canvas.text, 10, 50, "words", odd)
        attempt(canvas.text_width, "words", odd)
        attempt(canvas.text_width, odd)
        attempt(canvas.pixel, odd, odd)
        for box in (odd, (odd, 0, 50, 50), (10, 10, 10, 10), (0, 0, 50)):
            pen = attempt(canvas.specimen, box, odd, odd, odd)
            if pen is not None:
                attempt(pen.line, 0, 0, 1, 1)
                attempt(pen.settle)
        pen = canvas.specimen((10, 10, 110, 110), scale_bar=False)
        attempt(pen.line, odd, 0, 1, 1)
        attempt(pen.polyline, odd)
        attempt(pen.polyline, [(0, 0), (1, odd)])
        attempt(pen.dot, 0, odd)
        attempt(pen.arc, 0, 0, odd, 0, 90)
        attempt(pen.arc, 0, 0, 1, odd, 90)
        attempt(pen.cell, odd, 0)
        attempt(pen.cell, 0, 0, odd, 1)
        attempt(pen.label, 0, odd, "words")
        attempt(pen.label, 0, 0, odd, odd)
        attempt(pen.ground, odd)
        attempt(pen.note, odd)
        attempt(pen.settle)
    attempt(canvas.polyline, [])
    attempt(canvas.text, 10, 50, "")
    attempt(canvas.specimen((10, 10, 110, 110)).settle)
    drawn = inked_box(canvas)
    for odd in ODD:                                # these may draw; they must only not raise
        attempt(canvas.line, 10, 10, 50, 50, 3, odd)
        attempt(canvas.text, 10, 50, odd, 14, odd, odd)
        attempt(canvas.rect, 10, 10, 20, 20, odd, odd, odd)
        attempt(canvas.dot, 50, 50, 5, odd, odd, odd)
        attempt(Canvas, odd, odd, odd)
        pen = canvas.specimen((10, 10, 110, 110), odd, odd, odd)
        pen.unit_name = odd
        attempt(pen.line, 0, 0, 1, 1, odd, odd)
        attempt(pen.dot, 0, 0, odd, odd, odd, odd)
        attempt(pen.label, 0, 0, "words", 14, odd, odd)
        attempt(pen.settle)
    attempt(Canvas(0, 0).pixels)
    verdict("odd input: nothing raises, and what is skipped leaves the paper clean", not raised and drawn is None,
            raised[0] if raised else ("ink was laid at %s" % (drawn,) if drawn else "%d odd values in every place" % len(ODD)))


def read_png(path):
    """A PNG written by the plate -> (width, height, r g b bytes), checking every chunk's sum."""
    with open(path, "rb") as handle:
        data = handle.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    at, chunks = 8, {}
    while at < len(data):
        length, kind = struct.unpack(">I4s", data[at:at + 8])
        body = data[at + 8:at + 8 + length]
        if struct.unpack(">I", data[at + 8 + length:at + 12 + length])[0] != zlib.crc32(kind + body) & 0xffffffff:
            raise ValueError("a chunk's sum is wrong")
        chunks[kind] = chunks.get(kind, b"") + body
        at += 12 + length
    width, height, depth, colour = struct.unpack(">IIBB", chunks[b"IHDR"][:10])
    if (depth, colour) != (8, 2):
        raise ValueError("not 8-bit RGB")
    raw = zlib.decompress(chunks[b"IDAT"])
    row = width * 3 + 1
    if any(raw[y * row] for y in range(height)):
        raise ValueError("a filtered row")
    return width, height, b"".join(raw[y * row + 1:(y + 1) * row] for y in range(height))


def check_png(folder, canvas):
    """The PNG on disk holds exactly the plate's pixels."""
    try:
        width, height, pixels = read_png(os.path.join(folder, "specimen.png"))
        holds = (width, height) == (canvas.width, canvas.height) and pixels == bytes(canvas.pixels())
        detail = "%d x %d, %d KB" % (width, height, os.path.getsize(os.path.join(folder, "specimen.png")) // 1024)
    except Exception as error:
        holds, detail = False, repr(error)
    verdict("PNG: reads back as the plate's own pixels", holds, detail)


SVG = "{http://www.w3.org/2000/svg}"


def arc_pieces(path):
    """An SVG path of arcs, as the plate writes one -> [(x1, y1, r, large, sweep, x2, y2)], a tuple for each piece."""
    numbers = [float(n) for n in path.get("d").replace("M", " ").replace("A", " ").split()]
    x, y, pieces = numbers[0], numbers[1], []
    for at in range(2, len(numbers) - 6, 7):
        r, _, _, large, sweep, x2, y2 = numbers[at:at + 7]
        pieces.append((x, y, r, large, sweep, x2, y2))
        x, y = x2, y2
    return pieces


def svg_centre(x1, y1, r, large, sweep, x2, y2):
    """Where a viewer of the SVG puts the centre of an arc of a circle, from its two ends (the SVG rule), or None."""
    hx, hy = (x1 - x2) / 2, (y1 - y2) / 2
    half = hx * hx + hy * hy
    if half == 0:
        return None                                # an arc that ends where it began is left out altogether
    k = math.sqrt(max(0.0, r * r - half) / half) * (1 if large != sweep else -1)
    return (x1 + x2) / 2 + k * hy, (y1 + y2) / 2 - k * hx


def shares_centre(arc, others):
    """Whether each piece of an arc (a list of centres, as svg_centre gives them) is drawn round a centre another arc has."""
    theirs = [centre for other in others for centre in other if centre is not None]
    return all(mine is not None and any(math.dist(mine, centre) < 0.5 for centre in theirs) for mine in arc)


def field_pieces(path):
    """An SVG path of rects, as the plate writes a field of cells -> [(left, top, right, bottom)], or None if it is not one."""
    found = re.findall(r"M([-\d.]+) ([-\d.]+)H([-\d.]+)V([-\d.]+)H([-\d.]+)z", path.get("d", ""))
    if not found or "".join("M%s %sH%sV%sH%sz" % piece for piece in found) != path.get("d"):
        return None
    return [(float(a), float(b), float(c), float(d)) for a, b, c, d, _ in found]


def field_faults(pieces, wanted, words):
    """Why the rects of one field would not show as one solid field in the SVG: a list, empty if they would."""
    if pieces is None or len(pieces) != wanted:
        return ["%s: the cells are not written as one shape of %d pieces" % (words, wanted)]
    left, top = min(p[0] for p in pieces), min(p[1] for p in pieces)
    right, bottom = max(p[2] for p in pieces), max(p[3] for p in pieces)
    area = sum((r - l) * (b - t) for l, t, r, b in pieces)
    rows = {}
    for l, t, r, b in pieces:
        rows.setdefault((t, b), []).append((l, r))
    gaps = sum(1 for row in rows.values() for a, b in zip(sorted(row), sorted(row)[1:]) if a[1] != b[0])
    if gaps or abs(area - (right - left) * (bottom - top)) > 1e-6 * area:
        return ["%s: the cells do not meet edge to edge (%d gaps)" % (words, gaps)]
    return []


def svg_faults(canvas):
    """What a viewer of this plate's SVG would draw differently from the plate: a list of faults, empty if none.

    The plate holds a stroke of one point, an arc that stops a hundredth of
    a degree short of a whole turn, a field of cells, a field of cells
    finer than a pixel, and a hairline cell; each once went missing,
    astray, or pale in the SVG while the plate was right. A field must be
    one shape: written as a rect for each cell, every joint lets a hairline
    of paper through wherever the SVG is shown, and a field of cells
    finer than a pixel has a joint in every pixel and comes out pale.
    """
    canvas.polyline([(50, 60)], 16.0, "red")
    canvas.arc(250, 150, 30, 45, 404.99, 5.0, "orange")
    pen = canvas.specimen((20, 200, 220, 300), scale_bar=False)
    for i in range(7):
        for j in range(3):
            pen.cell(i, j, 1, 1, "brown")
    pen.cell(8, 0, 1, 0.001, "ink")
    pen.settle()
    fine = canvas.specimen((230, 200, 264.5, 234.5), unit_px_max=0.7, scale_bar=False)
    for i in range(40):
        for j in range(40):
            fine.cell(i, j, 1, 1, "#1f4e9c")
    fine.settle()
    root = ElementTree.fromstring(canvas._svg())
    faults = []
    dots = [c for c in root.iter(SVG + "circle") if (c.get("cx"), c.get("cy"), c.get("r")) == ("50", "60", "8")]
    if not dots or dots[0].get("fill") != canvas.inks["red"]:
        faults.append("a stroke of one point is not a dot")
    for piece in [piece for path in root.iter(SVG + "path") if "A" in path.get("d") for piece in arc_pieces(path)]:
        centre = svg_centre(*piece)
        if centre is None or math.hypot(centre[0] - 250, centre[1] - 150) > 0.5:
            faults.append("an arc all but once round is drawn round %s, not round (250, 150)" % (centre,))
            break
    for ink, wanted, words in ((canvas.inks["brown"], 21, "a field of cells"), ("#1f4e9c", 1600, "a field of 0.7 px cells")):
        paths = [path for path in root.iter(SVG + "path") if path.get("fill") == ink]
        faults += field_faults(field_pieces(paths[0]) if len(paths) == 1 else None, wanted, words)
    rects = [[float(rect.get(key)) for key in ("x", "y", "width", "height")]
             for rect in root.iter(SVG + "rect") if rect.get("x") is not None]        # (not the paper under it all)
    if not any(h >= 0.25 and w > 1 for x, y, w, h in rects if h < 1):
        faults.append("a hairline cell is thinner in the SVG than on the plate, or gone")
    return faults


def check_svg(folder, names):
    """Every SVG is well-formed, carries its lettering as real text, and draws what the plate draws."""
    faults, texts = [], 0
    for name in ("lettering", "stress", "scatter", "crowded", "specimen", "inks", "marks", "textures"):
        try:
            root = ElementTree.parse(os.path.join(folder, name + ".svg")).getroot()
        except Exception as error:
            faults.append("%s: %r" % (name, error))
            continue
        found = ["".join(element.itertext()) for element in root.iter(SVG + "text")]
        texts += len(found)
        if name == "inks" and not all(ink in found for ink in names):
            faults.append("inks.svg does not name every ink")
        if name == "stress":
            if "stress" not in found or not any(text.endswith("lengths") for text in found):
                faults.append("stress.svg lacks its name or its scale")
            if len(list(root.iter(SVG + "line"))) < 4000 or len(list(root.iter(SVG + "circle"))) < 300:
                faults.append("stress.svg lacks strokes")
        if name == "marks":                        # twelve arcs that go somewhere, each round a centre it shares with others
            arcs = [[svg_centre(*piece) for piece in arc_pieces(path)] for path in root.iter(SVG + "path") if "A" in path.get("d")]
            alone = sum(1 for i, arc in enumerate(arcs) if not shares_centre(arc, arcs[:i] + arcs[i + 1:]))
            if len(arcs) != 12 or alone:
                faults.append("marks.svg has %d arcs, %d of them round a centre of their own" % (len(arcs), alone))
    faults += svg_faults(Canvas(300, 320))
    verdict("SVG: well-formed, with real text, drawing what the plate draws", not faults,
            "; ".join(faults) if faults else "8 drawings, %d pieces of text; a stroke of one point, an arc all but once "
            "round, fields of cells (one finer than a pixel) and a hairline come out as on the plate" % texts)


def check_saving(folder):
    """A save that cannot be made says so and does not raise."""
    canvas = Canvas(20, 20)
    try:
        holds = canvas.save_png(os.path.join(folder, "lettering.png", "under-a-file.png")) is False and bool(canvas.trouble)
        detail = "it said: " + canvas.trouble[:60]
        holds = holds and canvas.save_svg(None) is False
    except Exception as error:
        holds, detail = False, repr(error)
    verdict("saving: a save that cannot be made returns False and raises nothing", holds, detail)


def tall_strokes():
    """How long a hundred strokes the whole height of a plate take to lay. Returns seconds."""
    began = time.perf_counter()
    canvas = Canvas(900, 1200)
    for i in range(100):
        canvas.line(9 * i, 0, 9 * i, 1200, 18.0)
    return time.perf_counter() - began


def trial_folder(given):
    """The folder the sheets go into: the one given, or a new one in the temp folder. None if it lies in the garden."""
    if not given:
        return tempfile.mkdtemp(prefix="glebe-plate-")
    garden = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    garden, folder = (os.path.normcase(os.path.realpath(path)) for path in (garden, given[0]))
    try:
        inside = os.path.commonpath([garden, folder]) == garden
    except ValueError:                             # on another drive altogether
        inside = False
    return None if inside else os.path.abspath(given[0])


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) > 2:
        print("One folder to write into, or none:  python plate_trial.py [folder]")
        return 2
    folder = trial_folder(sys.argv[1:])
    if folder is None:
        print("That folder lies inside the garden, and the trial's sheets are not the garden's.")
        print("Give a folder outside it, or none: the trial then makes one in the system's temp folder.")
        return 2
    os.makedirs(folder, exist_ok=True)

    began = time.perf_counter()
    lettering_sheet(folder)
    stress = stress_plate(folder)
    scatter, _ = scatter_plate(folder)
    crowded, deep = scatter_plate(folder, crowded=True)
    canvas, pens = specimen_sheet(folder)
    names = ink_chart(folder)
    marks_sheet(folder)
    texture_sheet(folder)
    print("stress plate (a full-grown plant: 4000 lengths, 300 dots, 12 lines): %.2f s to draw and save" % stress)
    print("scatter plate (4000 strokes of 20 to 200 px, 300 dots, 12 lines):    %.2f s to draw and save" % scatter)
    print("crowded plate (the scatter, each stroke in an ink of its own):       %.2f s, %s"
          % (crowded, "in full colour" if deep == 3 else "NOT in full colour"))
    print("a stroke costs by its height: 100 strokes the whole height of a plate took %.2f s to lay" % tall_strokes())
    print()

    check_every_letter()
    check_widths_and_anchors()
    check_stamps()
    check_dashes()
    check_stand_ins()
    check_inks(names)
    check_many_inks()
    check_wood()
    check_white()
    check_sizes()
    check_edges()
    check_arcs()
    check_cells()
    check_specimen_fit(pens)
    check_scale_bar()
    check_clamps()
    check_fine_pens()
    check_no_bar()
    check_apart()
    check_textures()
    check_remarks()
    check_odd_input()
    check_png(folder, canvas)
    check_svg(folder, names)
    check_saving(folder)
    verdict("speed: a full plate is drawn and saved within %.1f s" % BUDGET, max(stress, scatter, crowded) < BUDGET and deep == 3,
            "%.2f s, %.2f s, and %.2f s %s" % (stress, scatter, crowded,
                                               "in full colour" if deep == 3 else "for a crowded plate that never went over"))

    print()
    failed = verdicts.count(False)
    print("%d checks, %s. The whole trial took %.1f s. The sheets are in %s"
          % (len(verdicts), "all hold" if not failed else "%d FAILED" % failed, time.perf_counter() - began, folder))
    print("Now open the PNGs and look: that is the check this trial cannot make for you.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
