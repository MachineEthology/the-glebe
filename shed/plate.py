"""
The plate: the garden's only way of drawing.

Everything a visitor is shown (a plant's plate, a bed's sheet, the plan of the
garden) is drawn through this file, and the visitor who opens those pictures is
a Claude model looking with its own eyes. So the drawings are made for that
eye: bold strokes, smooth edges, plain paper, lettering that reads at a glance.

There are two pens.

    Canvas     draws in pixels, origin top-left, y down. The ground uses it
               for captions, sheets and the plan.
    Specimen   draws in a plant's own units, x to the right, y UP. A kind
               draws its plant with it and never thinks about pixels: when
               the drawing is finished, settle() fits it into its box and
               adds a scale bar, so the picture stays honest about size.

A kind is not handed the Specimen itself. Its draw() gets a pen that only
remembers the same marks, and the ground replays them on a Specimen of its
own, on the plate and again on the bed's sheet (GROUND.md, Run apart). Of
what a kind sets on that pen, only unit_name, unit_px_max, align and the
notes come through; the bar, pens and labels are the ground's to choose.

A plant drawn, from beginning to end:

    from plate import Canvas
    canvas = Canvas(900, 1200)
    pen = canvas.specimen((60, 50, 840, 930))       # the box the plant may fill
    pen.unit_name = "lengths"
    pen.ground()                                    # a faint line at height 0
    pen.line(0, 0, 0, 3, weight=8)                  # a stem three lengths high
    pen.line(0, 3, 1, 4, weight=4, ink="fresh")     # a shoot, new since the last visit
    pen.dot(1, 4, 6, "dark-red")                    # a fruit at its tip
    pen.label(1, 4.4, "first fruit")
    pen.settle()                                    # now it is on the plate, with its scale bar
    canvas.text(60, 978, "quince", 34)              # y is the baseline
    canvas.save_png("plate.png")
    canvas.save_svg("plate.svg")

How the ink is laid (for whoever wants to change it):

  * Every pixel is a small square of SUB x SUB samples, and each sample holds
    the number of one ink (0 is the paper). A stroke is laid as runs of
    samples, sub-row by sub-row, by slice assignment on bytearrays, which is
    the one thing pure Python does quickly. Later ink simply covers earlier
    ink, as on a real plate.
  * The sub-rows are kept in SUB separate bytearrays ("lanes"), one for each
    height within the pixel, so that every SUB-th sample of a lane is one
    whole picture of the plate as seen from one sample position.
  * Saving averages those SUB x SUB pictures. The shares are chosen so that a
    pixel wholly of one ink comes out as exactly that ink, to the last bit
    (see _shares). The averaging is done on whole planes at once with
    bytes.translate and one long integer, never pixel by pixel, and only
    over the rows that were drawn on.
  * Each sub-row's samples sit a little to one side (SHIFT), a different side
    for each sub-row, so an upright edge is measured at SUB x SUB places
    across the pixel and comes out smooth.
  * One byte numbers 256 inks, and few plates want more. One that does (a
    plant coloured by age in three hundred shades) goes over to full colour
    at the 257th: each sample then holds red, green and blue themselves,
    three bytes side by side where there was one, and every ink is exactly
    itself however many there are. Such a plate takes three times the
    memory and about a fifth longer to draw, and other plates pay next to
    nothing for it (see _full_colour and _paint).
  * A stroke costs by its height, not its length, since it is laid sub-row
    by sub-row: about half a microsecond for each. Four thousand strokes the
    size of a plant's lengths take a third of a second; four thousand
    strokes each the whole height of the plate would take ten seconds.

The lettering is a stroke face drawn with the same round pen as everything
else. Its letters are written further down in a small notation (see FACE),
and can be mended there by hand. After mending one, run
foundations/plate_trial.py and read its lettering sheet with your own eyes.
A letter is drawn stroke by stroke only the first time it is wanted at a
size; after that it is pressed from a stamp of its own runs (see _stamp).

Nothing here raises on odd input. A line with a NaN in it, a box of no size,
a list with nothing in it: such marks are skipped and the rest is drawn.

A few things are here beyond what GROUND.md asks. All can be left alone:

    canvas.text(..., halo=True)      clears a little paper round the letters,
                                     for words laid over a drawing
    canvas.pixel(x, y), .pixels()    read the plate back
    canvas.save_png, .save_svg       return True, or False with the reason
                                     left in canvas.trouble
    canvas.remarks                   what was drawn otherwise than asked, in
                                     a few plain lines: a mark left out, an
                                     ink not known, a weight kept to its
                                     range, no room for a bar. Print it when
                                     a plate is not what you wrote.
    pen.pens, pen.labels             finer pens, and no labels, for a plant
                                     drawn small in the cell of a sheet
    pen.box, pen.scale, pen.bar      where the pen draws, and what settle()
                                     decided
    pen.measured                     after settle(): whether anything drawn
                                     has a length, for a bar to measure (a
                                     sheet that draws its own small bars
                                     can ask it)
    pen.unit_name = "length, lengths"    the unit's name for a bar of exactly
                                     one, then its name for any other number
    pen.scale_bar = False            no bar, for a drawing that letters its
                                     own units (months along its foot, say);
                                     set any time before settle(). Only for
                                     whoever holds the Specimen itself: a
                                     kind's pen does not pass it on, and a
                                     plant's plate keeps its bar. A kind
                                     that letters its own measure can still
                                     give the bar an honest unit_name.

Standard library only.
"""

import math
import os
import re
import string
import struct
import unicodedata
import zlib
from math import ceil, floor, sqrt

__all__ = ["Canvas", "Specimen", "INKS", "PAPER", "SUPPORTED"]

# ---------------------------------------------------------------- the inks

PAPER = "#fbf8f1"

INKS = {
    "ink": "#1a1a1a",        # lettering and plain marks
    "wood": "#5a4632",       # the planter's ink; the ground sets it for each plant
    "fresh": "#2e9e3f",      # reserved: what has grown since the last visit
    "faint": "#c9c4b8",      # guides, the ground line
    "dead": "#9a948a",
    "red": "#d1342b",
    "dark-red": "#7a1428",
    "pink": "#e0608f",
    "pale-pink": "#f0b6c8",
    "orange": "#e07b12",
    "yellow": "#e2b100",
    "blue": "#2563c0",
    "violet": "#7b3fb0",
    "brown": "#7a4a21",
    "white": "#ffffff",
    "black": "#000000",
    "grey": "#808080",
}

# ------------------------------------------------------------ the sampling

SUB = 4              # samples along each side of a pixel
LIMIT = 1.0e6        # a pixel coordinate beyond this is not a coordinate
LARGEST = 4096       # the longest side a plate may have, in pixels
MOST = 6_000_000     # the most pixels a plate may have (each costs SUB x SUB bytes)
REMARKS = 12         # the most lines canvas.remarks keeps
HALO = 3.0           # the paper cleared round haloed lettering, in pixels: at 2, words laid over heavy strokes
                     # at size 14 could be read, but had to be worked at
NUMBERED = 256       # the inks one byte can number; a plate asked for more goes over to full colour
PALE = 48            # an ink whose red, green and blue differ from the paper's by less than this, taken
                     # together, would hardly show on it


def _shifts(count):
    """Where each sub-row's samples sit within their cell: spread out, never twice the same."""
    order = sorted(range(count), key=lambda k: ((k + 1) * 0.6180339887) % 1.0)
    shifts = [0.0] * count
    for rank, k in enumerate(order):
        shifts[k] = (rank + 0.5) / count
    return tuple(shifts)


SHIFT = _shifts(SUB)
NUDGE = tuple(1.0 - shift for shift in SHIFT)    # int(x + nudge) is the first sample at or right of x
COLUMN = 1.0 / SUB   # taken together, the sub-rows' samples stand in columns this far apart (in samples)


def _floats(*values):
    """The values as floats, or None if any of them is not a usable number."""
    try:
        numbers = [float(v) for v in values]
    except Exception:                        # not numbers at all
        return None
    for number in numbers:
        if not -LIMIT < number < LIMIT:      # a NaN fails this too
            return None
    return numbers


def _points(pts):
    """A list of (x, y) pairs as floats, or None if anything in it is odd."""
    try:
        points = [(float(x), float(y)) for x, y in pts]
    except Exception:
        return None
    for x, y in points:
        if not (-LIMIT < x < LIMIT and -LIMIT < y < LIMIT):
            return None
    return points


def _yes(value):
    """Whether something given as a yes-or-no means yes. What cannot be asked means no."""
    try:
        return bool(value)
    except Exception:
        return False


def _rgb(colour):
    """'#rrggbb' (or '#rgb') -> (r, g, b), or None if it is not a colour."""
    if not isinstance(colour, str) or not colour.startswith("#"):
        return None
    digits = colour[1:]
    if len(digits) == 3:
        digits = "".join(d + d for d in digits)
    if len(digits) != 6 or not all(d in string.hexdigits for d in digits):      # int() alone would take '-12345'
        return None
    value = int(digits, 16)
    return (value >> 16) & 255, (value >> 8) & 255, value & 255


def _hex(rgb):
    """(r, g, b) -> '#rrggbb'."""
    return "#%02x%02x%02x" % rgb


def _said(thing):
    """Something a visitor passed in, as a remark can safely quote it: short, and never raising."""
    try:
        words = repr(thing)
    except Exception:
        return "one that cannot be named"
    return words if len(words) <= 40 else words[:39] + "..."


# ------------------------------------------------------------ the lettering
#
# The face. Each character is (left, width, right, strokes), in face units:
#
#     the baseline is y = 0, small letters reach y = 5, capitals and figures
#     y = 7, tall small letters (b d f h k l) y = 7.5, tails go down to -2.2.
#     x runs from 0 to width; left and right are the room kept on each side.
#
# These are heights of the face, not pixels. At each size the baseline, the
# top of the small letters and the top of the capitals are set on whole
# pixels, so that those edges come out crisp, and what lies between is
# stretched to fit (see _Measure).
#
# Strokes are separated by "|". A stroke is the points the pen goes through:
#
#     x,y      the pen goes to this point
#     (x,y)    the pen turns round this corner without touching it;
#              between two such corners it passes midway between them
#     z        the stroke closes on itself
#
# A stroke of one point is a dot. So "o" is a square with four turned
# corners, which the pen rounds into a ring, and "i" is a stem and a dot.
# The coordinates are the middle of the pen's line; the pen's width is added
# around them when the letter is written.

_S = 1.45      # room beside a straight stem
_R = 1.15      # room beside a round side
_O = 0.9       # room beside an open or slanting side

_BOWL_RIGHT = "0,3.5 (0.5,5) 1.9,5 (3.6,5) (3.6,0) 1.9,0 (0.5,0) 0,1.5"
_BOWL_LEFT = "3.6,3.5 (3.1,5) 1.7,5 (0,5) (0,0) 1.7,0 (3.1,0) 3.6,1.5"
_RING = "(0,0) (0,7) (5.4,7) (5.4,0) z"
_COMMA = "0.5,0.15 | 0.5,0.1 0.5,-0.5 0,-1.5"

FACE = {
    " ": (0, 3.0, 0, ""),

    "a": (_R, 3.4, _S, "0.3,4.0 (0.8,5) 1.8,5 (3.4,5) 3.4,3.5 3.4,0 | 3.4,2.8 1.6,2.8 (0,2.8) (0,0) 1.5,0 (2.8,0) 3.4,1.1"),
    "b": (_S, 3.6, _R, "0,7.5 0,0 | " + _BOWL_RIGHT),
    "c": (_R, 3.3, _O, "3.3,4.0 (2.9,5) 1.9,5 (0,5) (0,0) 1.9,0 (2.9,0) 3.3,1.0"),
    "d": (_R, 3.6, _S, "3.6,7.5 3.6,0 | " + _BOWL_LEFT),
    "e": (_R, 3.7, _R, "0,2.6 3.7,2.6 (3.7,5) (0,5) (0,0) 1.9,0 (3.1,0) 3.6,0.9"),
    "f": (_O, 2.4, 0.5, "2.5,7.3 (2.2,7.5) 1.9,7.5 (0.9,7.5) 0.9,6.3 0.9,0 | 0,5 2.3,5"),
    "g": (_R, 3.6, _S, "3.6,5 3.6,-0.6 (3.6,-2.2) 1.8,-2.2 (0.8,-2.2) 0.3,-1.6 | " + _BOWL_LEFT),
    "h": (_S, 3.4, _S, "0,7.5 0,0 | 0,3.5 (0.5,5) 1.8,5 (3.4,5) 3.4,3.3 3.4,0"),
    "i": (_S, 0, _S, "0,5 0,0 | 0,7.2"),
    "j": (_O, 1.3, _S, "1.3,5 1.3,-0.8 (1.3,-2.2) -0.1,-2.2 | 1.3,7.2"),
    "k": (_S, 3.3, _O, "0,7.5 0,0 | 3.2,5 0,2.0 | 1.2,3.1 3.4,0"),
    "l": (_S, 1.4, _O, "0,7.5 0,1.3 (0,0) 1.4,0"),
    "m": (_S, 5.8, _S, "0,5 0,0 | 0,3.6 (0.4,5) 1.6,5 (2.9,5) 2.9,3.4 2.9,0 | 2.9,3.6 (3.3,5) 4.5,5 (5.8,5) 5.8,3.4 5.8,0"),
    "n": (_S, 3.4, _S, "0,5 0,0 | 0,3.5 (0.5,5) 1.8,5 (3.4,5) 3.4,3.3 3.4,0"),
    "o": (_R, 3.8, _R, "(0,0) (0,5) (3.8,5) (3.8,0) z"),
    "p": (_S, 3.6, _R, "0,5 0,-2.2 | " + _BOWL_RIGHT),
    "q": (_R, 3.6, _S, "3.6,5 3.6,-2.2 | " + _BOWL_LEFT),
    "r": (_S, 2.3, 0.6, "0,5 0,0 | 0,3.4 (0.5,5) 1.7,5 (2.1,5) 2.4,4.7"),
    "s": (_R, 3.2, _R, "3.0,4.1 (2.7,5) 1.6,5 (0.1,5) 0.1,3.7 (0.1,2.6) 1.6,2.5 (3.2,2.4) 3.2,1.3 (3.2,0) 1.6,0 (0.4,0) 0,0.9"),
    "t": (_O, 2.4, _O, "0.9,6.7 0.9,1.2 (0.9,0) 2.4,0 | 0,5 2.4,5"),
    "u": (_S, 3.4, _S, "0,5 0,1.7 (0,0) 1.6,0 (2.9,0) 3.4,1.5 | 3.4,5 3.4,0"),
    "v": (_O, 3.6, _O, "0,5 1.8,0 3.6,5"),
    "w": (_O, 5.6, _O, "0,5 1.4,0 2.8,4.6 4.2,0 5.6,5"),
    "x": (_O, 3.4, _O, "0,5 3.4,0 | 3.4,5 0,0"),
    "y": (_O, 3.6, _O, "3.6,5 1.1,-1.6 (0.9,-2.2) 0.1,-2.2 | 0,5 1.8,0.25"),
    "z": (_O, 3.3, _O, "0,5 3.3,5 0,0 3.3,0"),
    "\u0131": (_S, 0, _S, "0,5 0,0"),                       # an i without its dot, for î and ï

    "A": (_O, 5.0, _O, "0,0 2.5,7 5.0,0 | 0.85,2.4 4.15,2.4"),
    "B": (_S, 4.1, _R, "0,0 0,7 2.1,7 (3.8,7) (3.8,3.7) 2.1,3.7 0,3.7 | 2.1,3.7 (4.1,3.7) (4.1,0) 2.1,0 0,0"),
    "C": (_R, 4.6, _O, "4.6,5.5 (4.1,7) 2.7,7 (0,7) (0,0) 2.7,0 (4.1,0) 4.6,1.5"),
    "D": (_S, 4.6, _R, "0,0 0,7 1.8,7 (4.6,7) (4.6,0) 1.8,0 0,0"),
    "E": (_S, 3.7, _O, "3.7,7 0,7 0,0 3.7,0 | 0,3.7 3.2,3.7"),
    "F": (_S, 3.5, _O, "3.5,7 0,7 0,0 | 0,3.6 3.0,3.6"),
    "G": (_R, 4.9, _S, "4.6,5.6 (4.1,7) 2.7,7 (0,7) (0,0) 2.6,0 (4.9,0) 4.9,2.0 4.9,3.3 2.8,3.3"),
    "H": (_S, 4.6, _S, "0,7 0,0 | 4.6,7 4.6,0 | 0,3.7 4.6,3.7"),
    "I": (1.1, 2.2, 1.1, "1.1,7 1.1,0 | 0,7 2.2,7 | 0,0 2.2,0"),
    "J": (_O, 3.0, _S, "3.0,7 3.0,1.8 (3.0,0) 1.5,0 (0.3,0) 0,1.4"),
    "K": (_S, 4.4, _O, "0,7 0,0 | 4.2,7 0,2.7 | 1.55,4.25 4.4,0"),
    "L": (_S, 3.4, _O, "0,7 0,0 3.4,0"),
    "M": (_S, 5.8, _S, "0,0 0,7 2.9,1.8 5.8,7 5.8,0"),
    "N": (_S, 4.8, _S, "0,0 0,7 4.8,0 4.8,7"),
    "O": (_R, 5.4, _R, _RING),
    "P": (_S, 4.0, _R, "0,0 0,7 2.1,7 (4.0,7) (4.0,3.2) 2.1,3.2 0,3.2"),
    "Q": (_R, 5.4, _R, _RING + " | 3.3,1.7 5.6,-0.7"),
    "R": (_S, 4.2, _O, "0,0 0,7 2.1,7 (4.0,7) (4.0,3.4) 2.1,3.4 0,3.4 | 2.1,3.4 4.2,0"),
    "S": (_R, 4.2, _R, "4.0,5.8 (3.6,7) 2.1,7 (0.1,7) 0.1,5.2 (0.1,3.7) 2.1,3.55 (4.2,3.4) 4.2,1.8 (4.2,0) 2.1,0 (0.4,0) 0,1.3"),
    "T": (_O, 4.6, _O, "0,7 4.6,7 | 2.3,7 2.3,0"),
    "U": (_S, 4.6, _S, "0,7 0,2.2 (0,0) 2.3,0 (4.6,0) 4.6,2.2 4.6,7"),
    "V": (_O, 5.0, _O, "0,7 2.5,0 5.0,7"),
    "W": (_O, 7.2, _O, "0,7 1.8,0 3.6,6.0 5.4,0 7.2,7"),
    "X": (_O, 4.6, _O, "0,7 4.6,0 | 4.6,7 0,0"),
    "Y": (_O, 4.6, _O, "0,7 2.3,3.1 4.6,7 | 2.3,3.1 2.3,0"),
    "Z": (_O, 4.2, _O, "0,7 4.2,7 0,0 4.2,0"),

    "0": (_R, 3.8, _R, "(0,0) (0,7) (3.8,7) (3.8,0) z | 2.75,5.4 1.05,1.6"),      # slashed inside: never an O
    "1": (_R, 2.0, _S, "0,5.5 2.0,7 2.0,0"),
    "2": (_R, 3.8, _R, "0.2,5.5 (0.5,7) 1.9,7 (3.8,7) 3.8,5.3 (3.8,4.0) 2.5,2.7 0,0 3.8,0"),
    "3": (_R, 3.8, _R, "0.2,5.8 (0.6,7) 1.9,7 (3.6,7) 3.6,5.3 (3.6,3.7) 1.7,3.7 | 1.7,3.7 (3.8,3.7) 3.8,1.9 (3.8,0) 1.9,0 (0.4,0) 0,1.4"),
    "4": (_O, 4.0, _R, "3.1,0 3.1,7 0,2.1 4.0,2.1"),
    "5": (_R, 3.8, _R, "3.5,7 0.5,7 0.2,3.8 (0.9,4.5) 2.0,4.5 (3.8,4.5) 3.8,2.2 (3.8,0) 1.9,0 (0.4,0) 0,1.3"),
    "6": (_R, 3.8, _R, "3.4,6.1 (3.0,7) 2.0,7 (0,7) 0,3.6 0,2.2 (0,0) 1.9,0 (3.8,0) 3.8,2.2 (3.8,4.4) 1.9,4.4 (0.6,4.4) 0,3.0"),
    "7": (_O, 3.6, _O, "0,7 3.6,7 1.2,0"),
    "8": (_R, 3.8, _R, "(0.25,3.7) (0.25,7) (3.55,7) (3.55,3.7) z | (0,0) (0,3.7) (3.8,3.7) (3.8,0) z"),
    "9": (_R, 3.8, _R, "0.4,0.9 (0.8,0) 1.8,0 (3.8,0) 3.8,3.4 3.8,4.8 (3.8,7) 1.9,7 (0,7) 0,4.8 (0,2.6) 1.9,2.6 (3.2,2.6) 3.8,4.0"),

    "!": (_S, 0, _S, "0,7 0,2.9 | 0,0.15"),
    '"': (_O, 1.6, _O, "0,7.4 0,5.4 | 1.6,7.4 1.6,5.4"),
    "#": (_O, 4.6, _O, "1.7,7 0.9,0 | 3.7,7 2.9,0 | 0.3,4.7 4.6,4.7 | 0,2.3 4.3,2.3"),
    "$": (_R, 4.0, _R, "3.8,5.6 (3.4,6.6) 2.0,6.6 (0.1,6.6) 0.1,5.0 (0.1,3.6) 2.0,3.45 (4.0,3.3) 4.0,1.8 (4.0,0.4) 2.0,0.4 (0.4,0.4) 0,1.5 | 2.0,7.9 2.0,-0.9"),
    "%": (_R, 6.0, _R, "(0,4.0) (0,7) (2.4,7) (2.4,4.0) z | (3.6,0) (3.6,3.0) (6.0,3.0) (6.0,0) z | 5.0,7 1.0,0"),
    "&": (_R, 5.0, _O, "5.0,0 1.2,4.6 (0.5,5.5) (0.8,7) 2.0,7 (3.2,7) (3.4,5.4) 2.3,4.4 1.0,3.4 (0,2.6) (0,0) 1.9,0 (3.4,0) 4.7,2.9"),
    "'": (_O, 0, _O, "0,7.4 0,5.4"),
    "(": (_O, 1.5, 1.1, "1.5,7.9 (0,5.6) 0,3.0 (0,0.4) 1.5,-1.9"),              # room inside, or () closes into a 0
    ")": (1.1, 1.5, _O, "0,7.9 (1.5,5.6) 1.5,3.0 (1.5,0.4) 0,-1.9"),
    "*": (_O, 3.0, _O, "1.5,7.2 1.5,4.0 | 0.1,6.4 2.9,4.8 | 2.9,6.4 0.1,4.8"),
    "+": (_R, 3.8, _R, "1.9,5.4 1.9,1.6 | 0,3.5 3.8,3.5"),
    ",": (_O, 0.6, _O, _COMMA),
    "-": (_O, 2.0, _O, "0,2.8 2.0,2.8"),
    ".": (1.3, 0, 1.3, "0,0.15"),
    "/": (0.5, 2.8, 0.5, "2.8,7.6 0,-1.2"),
    ":": (_S, 0, _S, "0,4.3 | 0,0.15"),
    ";": (_O, 0.6, _O, "0.5,4.3 | " + _COMMA),
    "<": (_R, 3.6, _R, "3.6,5.7 0,3.5 3.6,1.3"),
    "=": (_R, 3.8, _R, "0,4.5 3.8,4.5 | 0,2.5 3.8,2.5"),
    ">": (_R, 3.6, _R, "0,5.7 3.6,3.5 0,1.3"),
    "?": (_R, 3.4, _R, "0.1,5.6 (0.4,7) 1.8,7 (3.4,7) 3.4,5.5 (3.4,4.5) 2.5,4.0 (1.7,3.5) 1.7,2.8 | 1.7,0.15"),
    "@": (_R, 6.6, _R, "(2.0,1.1) (2.0,4.6) (4.6,4.6) (4.6,1.1) z | 4.6,4.6 4.6,2.0 (4.6,1.1) 5.5,1.1 (6.6,1.1) 6.6,3.0 (6.6,6.6) 3.3,6.6 (0,6.6) 0,2.6 (0,-1.4) 3.3,-1.4 (4.6,-1.4) 5.4,-0.9"),
    "[": (_S, 1.5, 1.1, "1.5,7.9 0,7.9 0,-1.9 1.5,-1.9"),                         # and [] into a box
    "\\": (0.5, 2.8, 0.5, "0,7.6 2.8,-1.2"),
    "]": (1.1, 1.5, _S, "0,7.9 1.5,7.9 1.5,-1.9 0,-1.9"),
    "^": (_O, 3.4, _O, "0,4.6 1.7,7.2 3.4,4.6"),
    "_": (0.4, 4.2, 0.4, "0,-1.3 4.2,-1.3"),
    "`": (_O, 1.2, _O, "0,7.6 1.2,6.2"),
    "{": (_O, 2.2, 0.5, "2.2,7.9 (1.1,7.9) 1.1,6.7 1.1,4.2 (1.1,3.0) 0,3.0 (1.1,3.0) 1.1,1.8 1.1,-0.7 (1.1,-1.9) 2.2,-1.9"),
    "|": (_S, 0, _S, "0,7.9 0,-2.2"),
    "}": (0.5, 2.2, _O, "0,7.9 (1.1,7.9) 1.1,6.7 1.1,4.2 (1.1,3.0) 2.2,3.0 (1.1,3.0) 1.1,1.8 1.1,-0.7 (1.1,-1.9) 0,-1.9"),
    "~": (_R, 4.2, _R, "0,3.0 (0.4,4.1) 1.2,4.1 (1.9,4.1) 2.1,3.5 (2.3,2.9) 3.0,2.9 (3.8,2.9) 4.2,4.0"),

    "\u00b7": (1.6, 0, 1.6, "0,2.9"),                                                       # · the garden's separator
    "\u00b0": (_O, 2.2, _O, "(0,4.8) (0,7.2) (2.2,7.2) (2.2,4.8) z"),                       # °
    "\u2013": (_O, 5.4, _O, "0,2.8 5.4,2.8"),                                               # – en dash
    "\u2014": (0.5, 9.0, 0.5, "0,2.8 9.0,2.8"),                                             # — em dash
    "\u00d7": (_R, 3.4, _R, "0,5.0 3.4,1.6 | 3.4,5.0 0,1.6"),                               # ×
    "\u2020": (_R, 3.2, _R, "1.6,7.5 1.6,-2.2 | 0,5.2 3.2,5.2"),                            # † the mark of a dead plant
    "\u2026": (1.3, 5.0, 1.3, "0,0.15 | 2.5,0.15 | 5.0,0.15"),                              # …
    "\u00ab": (_O, 3.4, _O, "1.6,4.5 0,2.7 1.6,0.9 | 3.4,4.5 1.8,2.7 3.4,0.9"),             # «
    "\u00bb": (_O, 3.4, _O, "0,4.5 1.6,2.7 0,0.9 | 1.8,4.5 3.4,2.7 1.8,0.9"),               # »
    "\u2192": (_O, 5.4, _O, "0,2.8 5.4,2.8 | 3.0,5.0 5.4,2.8 3.0,0.6"),                     # →
    "\u2190": (_O, 5.4, _O, "5.4,2.8 0,2.8 | 2.4,5.0 0,2.8 2.4,0.6"),                       # ←
    "\u2191": (_O, 4.4, _O, "2.2,0 2.2,7.0 | 0,4.6 2.2,7.0 4.4,4.6"),                       # ↑
    "\u2193": (_O, 4.4, _O, "2.2,7.0 2.2,0 | 0,2.4 2.2,0 4.4,2.4"),                         # ↓
}

# Accents. Those above are written from the top of the letter (0,0 is the
# middle of the letter, on its top line); the cedilla hangs from the baseline.
# They stand well clear of the letter and are drawn wide, because at size 14 a
# unit is hardly more than a pixel: a low roof and two close dots both come
# out as a small dark bar. The two marks of the diaeresis are short upright
# strokes, not dots (a dot is drawn fatter than the pen), so that paper shows
# between them.
ACCENTS = {
    "\u0301": ("above", "-0.7,2.2 0.9,4.0"),                                                                          # acute   é
    "\u0300": ("above", "0.7,2.2 -0.9,4.0"),                                                                          # grave   è à ù
    "\u0302": ("above", "-1.7,2.0 0,4.0 1.7,2.0"),                                                                    # circumflex  ê â î ô û
    "\u0308": ("above", "-1.35,2.9 -1.35,3.0 | 1.35,2.9 1.35,3.0"),                                                   # diaeresis   ë ï
    "\u0303": ("above", "-1.7,2.5 (-1.3,3.5) -0.75,3.5 (-0.2,3.5) 0,3.0 (0.2,2.5) 0.75,2.5 (1.3,2.5) 1.7,3.5"),       # tilde
    "\u030a": ("above", "(-0.95,2.0) (-0.95,3.9) (0.95,3.9) (0.95,2.0) z"),                                           # ring
    "\u030c": ("above", "-1.7,4.0 0,2.0 1.7,4.0"),                                                                    # caron
    "\u0327": ("below", "0.1,-0.2 -0.2,-1.0 (1.0,-1.1) (0.9,-2.4) -0.7,-2.3"),                                        # cedilla  ç
}

# What is written in place of a character the face does not have.
STAND_INS = {
    "\u2018": "'", "\u2019": "'", "\u201a": ",", "\u2032": "'",                             # ‘ ’ ‚ ′   curled quotes and primes
    "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u2033": '"',                             # “ ” „ ″
    "\u2212": "-", "\u2010": "-", "\u2011": "-", "\u2012": "\u2013", "\u2015": "\u2014",    # − ‐ ‑ ‒ ―   the minus sign and the other dashes
    "\u2022": "\u00b7", "\u2219": "\u00b7", "\u22c5": "\u00b7",                             # • ∙ ⋅   bullets
    "\u0153": "oe", "\u0152": "OE", "\u00e6": "ae", "\u00c6": "AE", "\u00df": "ss",         # œ Œ æ Æ ß
    "\u00f8": "o", "\u00d8": "O", "\u0142": "l", "\u0141": "L",                             # ø Ø ł Ł
    "\u2715": "\u00d7", "\u2716": "\u00d7", "\u2717": "\u00d7",                             # ✕ ✖ ✗
    "\u00ba": "\u00b0", "\u2021": "\u2020",                                                 # º ‡
    "\u2044": "/", "\u2215": "/",                                                           # ⁄ ∕   the stroke inside ½
}

# Every character the face is sure of. Others are written by STAND_INS, by
# their base letter with whatever ACCENTS are known, or as "?".
SUPPORTED = ("".join(chr(c) for c in range(32, 127))
             + "\u00b7\u00b0\u2013\u2014\u00d7\u2020\u2026"                                 # · ° – — × † …
             + "\u00e9\u00e8\u00ea\u00e0\u00e7\u00f9\u00e2\u00ee\u00f4\u00fb\u00eb\u00ef"   # é è ê à ç ù â î ô û ë ï
             + "\u00ab\u00bb\u2192\u2190\u2191\u2193")                                      # « » → ← ↑ ↓

ROUND = 0.80          # how round a turned corner is: 0.707 is a true circle, 1.0 squarer
DOT = 0.72            # a dot's radius, in pen widths
TALL_SMALL = "bdfhklt"

STAMPED = 64          # lettering up to this size is pressed from stamps; larger is drawn stroke by stroke

_spellings = {}       # character -> the keys it is written with
_shapes = {}          # (key, steps) -> the traced letter, in face units
_writings = {}        # (key, size) -> the letter as it is written at that size, in samples
_stamps = {}          # (key, size, pen radius) -> the same letter as runs of samples, ready to be pressed
_stamp_load = [0]     # how many runs the stamps hold between them


def _bend(start, corner, finish, steps):
    """The points of a turn from start to finish, round the corner (the start itself is left out)."""
    points = []
    for step in range(1, steps + 1):
        t = step / steps
        a = (1 - t) * (1 - t)
        b = 2 * ROUND * t * (1 - t)
        c = t * t
        total = a + b + c
        points.append(((a * start[0] + b * corner[0] + c * finish[0]) / total,
                       (a * start[1] + b * corner[1] + c * finish[1]) / total))
    return points


def _knots(stroke):
    """A stroke as written in the face -> ([(x, y, turned)], closed)."""
    knots, closed = [], False
    for token in stroke.split():
        if token == "z":
            closed = True
            continue
        x, y = token.strip("()").split(",")
        knots.append((float(x), float(y), token.startswith("(")))
    return knots, closed


def _trace(stroke, steps):
    """A stroke as written in the face -> the points the pen passes through."""
    knots, closed = _knots(stroke)
    if not knots:
        return []
    path = []
    for i, knot in enumerate(knots):
        path.append(knot)
        after = knots[(i + 1) % len(knots)]
        if knot[2] and after[2] and (closed or i + 1 < len(knots)):
            path.append(((knot[0] + after[0]) / 2, (knot[1] + after[1]) / 2, False))
    if closed:
        touched = [i for i, knot in enumerate(path) if not knot[2]]
        if not touched:
            return []
        first = touched[0]
        path = path[first:] + path[:first] + [path[first]]
    points = [path[0][:2]]
    i = 1
    while i < len(path):
        x, y, turned = path[i]
        if turned and i + 1 < len(path):
            points += _bend(points[-1], (x, y), path[i + 1][:2], steps)
            i += 2
        else:
            points.append((x, y))
            i += 1
    return points


def _spell(text):
    """A text -> the keys of the letters it is written with. A key is a character of the face, or (letter, accents)."""
    keys = []
    for ch in text:
        found = _spellings.get(ch)
        if found is None:
            found = _spellings[ch] = _spell_one(ch)
        keys.extend(found)
    return keys


def _spell_one(ch, depth=0):
    """One character -> its keys: itself, a stand-in, its base letter with accents, or '?'."""
    if ch in FACE:
        return (ch,)
    if ch in STAND_INS:
        return tuple(STAND_INS[ch])
    parts = unicodedata.normalize("NFD", ch)
    base = parts[0]
    if base in FACE and len(parts) > 1:
        accents = "".join(a for a in parts[1:] if a in ACCENTS)
        if base == "i" and any(ACCENTS[a][0] == "above" for a in accents):
            base = "\u0131"
        return ((base, accents),) if accents else (base,)
    if ch.isspace():
        return (" ",)
    if unicodedata.category(ch) in ("Cc", "Cf", "Mn", "Me", "Cs", "Co", "Cn"):
        return ()
    wider = unicodedata.normalize("NFKD", ch)
    if wider != ch and depth < 2:
        keys = []
        for part in wider:
            keys.extend(_spell_one(part, depth + 1))
        return tuple(keys)
    return ("?",)


def _shape(key, steps):
    """A letter traced in face units: (advance, strokes, accents, zone).

    strokes and accents are lists of point lists; accents are measured from the
    letter's top line (or from the baseline, for the cedilla) and carry that
    line's height with them: (height, points). zone says how its heights
    are to be read: "cap", "small", or "tall" for a small letter with an ascender.
    """
    shape = _shapes.get((key, steps))
    if shape is not None:
        return shape
    base, accents = (key, "") if isinstance(key, str) else key
    left, width, right, written = FACE[base]
    strokes = []
    for stroke in written.split("|"):
        points = _trace(stroke, steps)
        if points:
            strokes.append([(x + left, y) for x, y in points])
    zone = "cap" if not base.islower() else ("tall" if base in TALL_SMALL else "small")
    top = {"cap": 7.0, "tall": 7.5, "small": 5.0}[zone]
    middle = left + width / 2
    marks = []
    for accent in accents:
        where, written = ACCENTS[accent]
        for stroke in written.split("|"):
            points = _trace(stroke, steps)
            if points:
                marks.append((top if where == "above" else 0.0, [(x + middle, y) for x, y in points]))
    shape = (left + width + right, strokes, marks, zone)
    if len(_shapes) > 4000:
        _shapes.clear()
    _shapes[(key, steps)] = shape
    return shape


class _Measure:
    """How the face is written at one size: the pen's width, the unit, and the heights, all in pixels."""

    def __init__(self, size):
        pen = max(size * 0.105, min(1.5, size * 0.125))
        self.pen = max(0.5, round(pen * 4) / 4)                  # in quarter pixels, so its edges fall on sub-rows
        x_top = max(round(size * 0.55), ceil(self.pen) + 1)      # whole pixels: the tops and the baseline are crisp
        cap_top = max(round(size * 0.73), x_top + 1)
        tall_top = cap_top + round(size * 0.035)
        self.unit = (x_top - self.pen) / 5.0
        self.foot = self.pen / 2.0
        self.waist = x_top - self.pen / 2.0
        self.head = tall_top - self.pen / 2.0
        self.cap_unit = (cap_top - self.pen) / 7.0
        self.steps = 4 if size <= 16 else (6 if size <= 40 else 10)
        self.room = max(0.0, (20.0 - size) * 0.05)               # small lettering is set a little looser

    def rise(self, y, zone):
        """How far above the baseline (in pixels) a height of the face is written."""
        if zone == "cap":
            return self.foot + y * self.cap_unit
        if y <= 5.0:
            return self.foot + y * self.unit
        if zone == "small":                                      # the dot of an i floats clear of its stem
            return self.waist + (y - 5.0) * self.unit
        if y <= 7.5:
            return self.waist + (y - 5.0) * (self.head - self.waist) / 2.5
        return self.head + (y - 7.5) * self.unit


_measures = {}


def _measure(size):
    """The measures of one size, worked out once and kept."""
    measure = _measures.get(size)
    if measure is None:
        if len(_measures) > 500:
            _measures.clear()
        measure = _measures[size] = _Measure(size)
    return measure


def _writing(key, size):
    """A letter as it is written at one size: (advance in px, lines, dots), in samples from the pen's place, y down."""
    writing = _writings.get((key, size))
    if writing is not None:
        return writing
    measure = _measure(size)
    advance, strokes, marks, zone = _shape(key, measure.steps)
    lines, dots = [], []

    def place(points, height_of):
        placed = [(x * measure.unit * SUB, -height_of(y) * SUB) for x, y in points]
        (dots if len(placed) == 1 else lines).append(placed)

    for points in strokes:
        place(points, lambda y: measure.rise(y, zone))
    for line_height, points in marks:
        line = measure.rise(line_height, zone)
        place(points, lambda y: line + y * measure.unit)
    writing = (advance * measure.unit + measure.room, lines, [dot[0] for dot in dots])
    if len(_writings) > 6000:
        _writings.clear()
    _writings[(key, size)] = writing
    return writing


def _stamp(key, size, r):
    """A letter as the runs of samples a pen of radius r (in samples) leaves behind: (reach, lanes).

    lanes[k] lists (row, first, count) for lane k: a pixel row, a first sample
    and a number of samples, all counted from the letter's place on the
    baseline. reach = (left, top, right, bottom) bounds them. The letter is
    drawn once, stroke by stroke, on a slip of its own and read back from it,
    so a pressed letter is exactly a drawn one; pressing is only quicker.
    """
    stamp = _stamps.get((key, size, r))
    if stamp is not None:
        return stamp
    _, lines, dots = _writing(key, size)
    points = [point for line in lines for point in line] + list(dots)
    stamp = ((0, 0, 0, 0), [[] for _ in range(SUB)])
    if points:
        margin = int(r + DOT * _measure(size).pen * SUB) + 3
        ox = margin - floor(min(x for x, _ in points))                  # the letter's place on the slip, in samples
        oy = SUB * ceil((margin - min(y for _, y in points)) / SUB)     # a whole number of pixels down
        slip = Canvas((ox + ceil(max(x for x, _ in points)) + margin) // SUB + 2,
                      (oy + ceil(max(y for _, y in points)) + margin) // SUB + 2)
        slip._letter(key, size, ox, oy, r, slip._fill((0, 0, 0)))       # the slip's first ink: number 1
        stride = slip._stride
        lanes = [[(run.start() // stride - oy // SUB, run.start() % stride - ox, run.end() - run.start())
                  for run in re.finditer(b"\x01+", lane)] for lane in slip._lanes]
        runs = [run for lane in lanes for run in lane]
        if runs:
            stamp = ((min(a for _, a, _ in runs), min(row for row, _, _ in runs),
                      max(a + n for _, a, n in runs), max(row for row, _, _ in runs) + 1), lanes)
    load = sum(len(lane) for lane in stamp[1])
    if _stamp_load[0] + load > 400_000:           # the stamps have outgrown their drawer: empty it
        _stamps.clear()
        _stamp_load[0] = 0
    _stamp_load[0] += load
    _stamps[(key, size, r)] = stamp
    return stamp


def _size(size):
    """A lettering size as a usable number, or None."""
    numbers = _floats(size)
    if numbers is None or not 1.0 <= numbers[0] <= 2000.0:
        return None
    return round(numbers[0], 2)


def _text(s):
    """Whatever was given as a text, as a single line of text.

    A letter that arrives in two pieces, an e followed by its accent, is put
    together again, so that it is written as the one letter it is.
    """
    if s is None:
        return ""
    try:
        s = str(s).replace("\r", " ").replace("\n", " ").replace("\t", " ")
        return unicodedata.normalize("NFC", s)
    except Exception:
        return ""


def _anchor(anchor, otherwise="start"):
    """Which part of a text sits at its x: 'start', 'middle' or 'end'. Anything else is read as otherwise."""
    return anchor if isinstance(anchor, str) and anchor in ("start", "middle", "end") else otherwise


_heights = {}         # (key, size) -> how far the letter's ink reaches above and below the baseline, in pixels


def _height(key, size):
    """How far one letter's ink reaches above its baseline and below it, in pixels, at one size."""
    height = _heights.get((key, size))
    if height is None:
        _, lines, dots = _writing(key, size)
        pen = _measure(size).pen
        ys = [(y / SUB, pen / 2) for line in lines for _, y in line] + [(y / SUB, DOT * pen) for _, y in dots]
        height = (max([r - y for y, r in ys], default=0.0), max([r + y for y, r in ys], default=0.0))
        if len(_heights) > 6000:
            _heights.clear()
        _heights[(key, size)] = height
    return height


# --------------------------------------------------------------- the canvas

class Canvas:
    """A plate of paper, drawn on in pixels. Origin top-left, y down.

    inks maps the names of the inks to '#rrggbb', and may be changed: the
    ground sets inks['wood'] to the planter's ink. Wherever an ink is asked
    for, give one of those names or a '#rrggbb' of your own, as many
    different ones as you like: each is drawn exactly as asked. An ink the
    plate does not know is drawn in 'ink'. A name is looked up when the mark
    is made, so changing inks['wood'] changes only what is drawn afterwards.

    Strokes have round ends and round joints. Widths, radii and sizes are
    in pixels and are drawn as told, with one exception: a level stroke or
    rectangle finer than a quarter of a pixel is drawn a quarter of a pixel
    thick, and an upright one finer than a sixteenth of a pixel is drawn a
    sixteenth wide, so that neither is lost between two lines of samples.

    A plate is at most 4096 pixels a side and six million pixels in all
    (LARGEST, MOST). Asked for more, it is made narrower, then shorter:
    width and height say what it became, and trouble says that it was cut
    down, until a save leaves its own word there.
    """

    def __init__(self, width, height, paper=PAPER):
        self.width = _side_length(width, 900)
        self.height = min(_side_length(height, 1200), max(1, MOST // self.width))
        paper_rgb = _rgb(paper) or _rgb(PAPER)
        self.inks = dict(INKS)
        self.inks["paper"] = _hex(paper_rgb)
        # What went wrong last, in a sentence: the plate was cut down to size, a plant could not be drawn, a save failed.
        self.trouble = _cut_down(width, height, self.width, self.height)
        self._stride = self.width * SUB           # samples in one sub-row
        self._sub_rows = self.height * SUB
        self._paper = paper_rgb
        self._lanes = [bytearray(self._stride * self.height) for _ in range(SUB)]
        self._deep = 1                            # bytes to a sample: 1, an ink's number; 3 once in full colour
        self._palette = [paper_rgb]               # ink number -> (r, g, b); 0 is the paper. None in full colour.
        self._numbers = {paper_rgb: 0}            # (r, g, b) -> ink number
        self._dipped = {}                         # a colour as given -> (what lays it, its '#rrggbb')
        self._marks = []                          # everything drawn, in order, for the SVG
        self._touched = [self.height, 0]          # the pixel rows that may hold ink: first, and one past the last
        self._special = None                      # ("trace", runs) or ("within", runs) while a Specimen restores rims
                                                  # (see _paint_special); None for all ordinary drawing
        # What was drawn otherwise than asked, in plain words, one line for each sort of thing: a mark left out,
        # an ink not known, a weight kept to the range, a bar with no room. For whoever wonders why a plate is
        # not what they wrote. At most REMARKS lines; the plate draws on regardless.
        self.remarks = []

    # ---- the pens a visitor may use

    def line(self, x1, y1, x2, y2, width=3.0, ink="ink"):
        """A straight stroke with round ends."""
        given = _floats(x1, y1, x2, y2, width)
        if given is None or given[4] <= 0:
            self._remark("a line was left out: its ends or its width were no usable number")
            return
        x1, y1, x2, y2, width = given
        fill, colour = self._dip(ink)
        self._capsule(x1 * SUB, y1 * SUB, x2 * SUB, y2 * SUB, width * SUB / 2, fill)
        self._marks.append(("line", x1, y1, x2, y2, width, colour))

    def polyline(self, pts, width=3.0, ink="ink", closed=False):
        """A stroke through several points, with round joints. closed joins the last point to the first."""
        points = _points(pts)
        given = _floats(width)
        if not points or given is None or given[0] <= 0:
            self._remark("a polyline was left out: it had no points, or a point or its width was no usable number")
            return
        width = given[0]
        fill, colour = self._dip(ink)
        closed = _yes(closed) and len(points) > 2
        self._stroke([(x * SUB, y * SUB) for x, y in points], width * SUB / 2, fill, closed)
        self._marks.append(("polyline", points, width, colour, closed))

    def rect(self, x, y, w, h, ink="ink", filled=True, width=2.0):
        """A rectangle with its top-left corner at (x, y). Not filled: an outline, drawn inside the edge."""
        given = _floats(x, y, w, h, width)
        if given is None:
            self._remark("a rectangle was left out: its place or size was no usable number")
            return
        x, y, w, h, width = given
        filled = _yes(filled)
        if w < 0:
            x, w = x + w, -w
        if h < 0:
            y, h = y + h, -h
        if w == 0 or h == 0 or (not filled and width <= 0):
            return
        fill, colour = self._dip(ink)
        if filled or width * 2 >= min(w, h):
            self._block(x * SUB, y * SUB, w * SUB, h * SUB, fill)
            self._marks.append(("rect", x, y, w, h, colour))
            return
        for bx, by, bw, bh in ((x, y, w, width), (x, y + h - width, w, width),
                               (x, y + width, width, h - 2 * width), (x + w - width, y + width, width, h - 2 * width)):
            self._block(bx * SUB, by * SUB, bw * SUB, bh * SUB, fill)
        self._marks.append(("frame", x, y, w, h, width, colour))

    def dot(self, x, y, r, ink="ink", filled=True, width=2.0):
        """A round dot of radius r. Not filled: a ring whose outer edge is at r."""
        given = _floats(x, y, r, width)
        if given is None or given[2] <= 0:
            self._remark("a dot was left out: its place or radius was no usable number")
            return
        x, y, r, width = given
        filled = _yes(filled)
        if not filled and width <= 0:
            return
        fill, colour = self._dip(ink)
        if filled or width >= r:
            self._disc(x * SUB, y * SUB, r * SUB, fill)
            self._marks.append(("dot", x, y, r, colour))
        else:
            self._ring(x * SUB, y * SUB, r * SUB, (r - width) * SUB, fill)
            self._marks.append(("ring", x, y, r, width, colour))

    def arc(self, cx, cy, r, start_deg, end_deg, width=3.0, ink="ink"):
        """Part of a circle round (cx, cy), from start_deg to end_deg.

        Angles are measured counter-clockwise as seen on the page: 0 points
        right, 90 up. The arc passes through every angle between the two, so
        it runs counter-clockwise if end_deg is the larger and clockwise if
        it is the smaller: arc(.., 350, 10) is the long way round. To cross
        0 write 350 to 370, or -10 to 10. More than a whole turn is a circle;
        no turn at all is a dot of the pen's width.
        """
        given = _floats(cx, cy, r, start_deg, end_deg, width)
        if given is None or given[2] <= 0 or given[5] <= 0:
            self._remark("an arc was left out: its centre, radius, angles or width were no usable number")
            return
        cx, cy, r, start, end, width = given
        sweep = max(-360.0, min(360.0, end - start))
        fill, colour = self._dip(ink)
        points = _arc_points(cx, cy, r, start, sweep)
        self._stroke([(x * SUB, y * SUB) for x, y in points], width * SUB / 2, fill, False)
        self._marks.append(("arc", cx, cy, r, start, sweep, width, colour))

    def text(self, x, y, s, size=20, ink="ink", anchor="start", *, halo=False):
        """Lettering. y is the baseline; anchor is start, middle or end. Returns the width in pixels.

        halo=True clears a little paper round the letters first, so that a
        label laid over a drawing can still be read.
        """
        given = _floats(x, y)
        size = _size(size)
        s = _text(s)
        if given is None or size is None or not s:
            if s and (given is None or size is None):
                self._remark("lettering was left out: its place was no usable number, or its size not between 1 and 2000")
            return 0.0
        x, y = given
        halo = _yes(halo)
        anchor = _anchor(anchor)
        keys = _spell(s)
        width = sum(_writing(key, size)[0] for key in keys)
        start = x - width / 2 if anchor == "middle" else (x - width if anchor == "end" else x)
        fill, colour = self._dip(ink)
        pen = _measure(size).pen * SUB / 2
        if halo:
            self._write(keys, size, start, round(y), pen + HALO * SUB, self._fill(self._paper))
        self._write(keys, size, start, round(y), pen, fill)
        self._marks.append(("text", x, y, s, size, colour, anchor, width, halo))
        return width

    def text_width(self, s, size=20):
        """How wide text() would write s, in pixels."""
        size = _size(size)
        if size is None:
            return 0.0
        return sum(_writing(key, size)[0] for key in _spell(_text(s)))

    def specimen(self, box, unit_px_max=60.0, align="ground", scale_bar=True):
        """A pen that draws in plant units inside box = (x0, y0, x1, y1). See Specimen."""
        return Specimen(self, box, unit_px_max, align, scale_bar)

    def pixel(self, x, y):
        """The colour of one pixel as '#rrggbb' (None outside the plate). For trials and the curious."""
        try:
            x, y = int(x), int(y)
        except Exception:
            return None
        if not (0 <= x < self.width and 0 <= y < self.height):
            return None
        deep = self._deep
        at = (y * self._stride + x * SUB) * deep
        held = [tuple(lane[at + i:at + i + deep]) for lane in self._lanes for i in range(0, SUB * deep, deep)]
        if self._palette is None:
            colours = held                        # in full colour a sample is its own red, green and blue
        else:
            colours = [self._palette[sample[0]] for sample in held]
        return _hex(_blend(colours))

    def save_png(self, path):
        """Write the plate as a PNG. Returns True, or False with the reason in self.trouble."""
        try:
            data = _png(self.width, self.height, self.pixels())
        except Exception as error:                # a plate must never stop the day
            self.trouble = "%s: %s" % (type(error).__name__, error)
            return False
        return self._put(path, data)

    def save_svg(self, path):
        """Write the same drawing as SVG: strokes as strokes, lettering as real text."""
        try:
            data = self._svg().encode("utf-8")
        except Exception as error:
            self.trouble = "%s: %s" % (type(error).__name__, error)
            return False
        return self._put(path, data)

    def _remark(self, words):
        """Note, once, something drawn otherwise than asked (see remarks)."""
        if isinstance(self.remarks, list) and words not in self.remarks and len(self.remarks) < REMARKS:
            self.remarks.append(words)

    # ---- inks

    def _dip(self, ink):
        """An ink as asked for -> (what lays it, its '#rrggbb'). An unknown ink comes out as 'ink'."""
        try:
            colour = self.inks.get(ink, ink)
            known = self._dipped.get(colour)
        except Exception:                         # an ink that cannot be looked up, or inks is no longer a dict
            colour, known = None, None
        if known is not None:
            return known
        rgb = _rgb(colour)
        if rgb is None:                           # not an ink at all: it is drawn in 'ink'
            self._remark("an ink not known, %s, was drawn in 'ink'" % _said(ink))
            try:
                rgb = _rgb(self.inks.get("ink"))
            except Exception:
                rgb = None
            rgb = rgb or _rgb(INKS["ink"])
            return self._fill(rgb), _hex(rgb)
        if len(self._dipped) >= NUMBERED:          # kept small: each holds a whole sub-row (see _fill)
            self._dipped.clear()
        known = self._dipped[colour] = (self._fill(rgb), _hex(rgb))
        return known

    def _fill(self, rgb):
        """What lays a colour: a whole sub-row of it, of which each run laid is a piece.

        A plate begins with numbered inks, the next number going to each
        colour new to it, and a sample is one byte: the ink's number. When
        the numbers run out the plate goes over to full colour, and a sample
        is three bytes: the ink's red, its green, its blue.
        """
        if self._palette is not None:
            number = self._numbers.get(rgb)
            if number is None and len(self._palette) < NUMBERED:
                number = self._numbers[rgb] = len(self._palette)
                self._palette.append(rgb)
            if number is not None:
                return bytes((number,)) * self._stride
            self._full_colour()
        return bytes(rgb) * self._stride

    def _pale(self, ink):
        """Whether a mark in this ink would hardly show on this paper: white on cream. The paper itself is not pale."""
        rgb = _rgb(self._dip(ink)[1])
        return rgb != self._paper and sum(abs(a - b) for a, b in zip(rgb, self._paper)) < PALE

    def _clears(self, ink):
        """Whether this ink is the paper's own: a mark in it is a patch of cleared paper."""
        return _rgb(self._dip(ink)[1]) == self._paper

    def _full_colour(self):
        """Turn a plate of numbered inks into a plate in full colour, so that it can hold any number of them.

        Each sample, one byte that held an ink's number, becomes three bytes
        side by side in the same lane: the red, the green and the blue of
        the ink that lay there. A run of samples is still laid in one piece,
        only three times as long. Only a plate asked for more than 256 inks
        comes to this, and it alone pays: three times the memory, and a
        little more time to draw.
        """
        tables = [bytes(rgb[part] for rgb in self._palette).ljust(NUMBERED, b"\0") for part in range(3)]
        for index, lane in enumerate(self._lanes):
            coloured = bytearray(3 * len(lane))
            for part, table in enumerate(tables):
                coloured[part::3] = lane.translate(table)
            self._lanes[index] = coloured
        self._deep = 3
        self._palette = self._numbers = None
        self._dipped.clear()                      # what laid each colour on the numbered plate lays it no longer

    # ---- laying ink. Everything below works in samples: pixels times SUB.

    def _paint(self, top, lefts, rights, fill):
        """Lay runs of one ink: sub-row top + i is inked from lefts[i] to rights[i]. The rows must be on the plate.

        This is the innermost loop of the plate. A run is laid in one piece
        whether a sample is one byte or three; the two are written out side
        by side because one line with a multiplier in it cost every plate a
        tenth of its time.
        """
        if self._special is not None:
            self._paint_special(top, lefts, rights, fill)
            return
        stride = self._stride
        touched = self._touched
        if top // SUB < touched[0]:
            touched[0] = top // SUB
        if (top + len(lefts) - 1) // SUB >= touched[1]:
            touched[1] = (top + len(lefts) - 1) // SUB + 1
        numbered = self._deep == 1
        for phase, lane in enumerate(self._lanes):
            first = (phase - top) % SUB
            base = (top + first) // SUB * stride
            nudge = NUDGE[phase]
            for left, right in zip(lefts[first::SUB], rights[first::SUB]):
                a = int(left + nudge)
                b = int(right + nudge)
                if a < 0:
                    a = 0
                if b > stride:
                    b = stride
                if a < b:
                    if numbered:                  # one byte to a sample
                        lane[base + a:base + b] = fill[:b - a]
                    else:                         # three: red, green, blue
                        lane[3 * (base + a):3 * (base + b)] = fill[:3 * (b - a)]
                base += stride

    def _paint_special(self, top, lefts, rights, fill):
        """_paint, for the two moments a Specimen needs more than laying ink (see Specimen._draw).

        ("trace", runs): the ink is laid as usual, and every run of samples
        it covers is noted in runs, {sub-row: [(first, end), ...]}. This is
        how the footprint of a mark in the paper's own ink is known.
        ("within", runs): the ink is laid only where it falls inside those
        runs. This is how a rim is laid again on exactly the paper that such
        a mark cleared, and nowhere else.
        Slower than _paint, and used only for those few marks.
        """
        how, runs = self._special
        stride = self._stride
        if how == "trace":
            self._special = None
            try:
                self._paint(top, lefts, rights, fill)
            finally:
                self._special = (how, runs)
        deep = self._deep
        touched = self._touched
        for i, (left, right) in enumerate(zip(lefts, rights)):
            row = top + i
            nudge = NUDGE[row % SUB]
            a, b = max(0, int(left + nudge)), min(stride, int(right + nudge))
            if a >= b:
                continue
            if how == "trace":
                runs.setdefault(row, []).append((a, b))
                continue
            lane, base = self._lanes[row % SUB], row // SUB * stride
            for c, d in runs.get(row, ()):
                c, d = max(a, c), min(b, d)
                if c < d:
                    lane[deep * (base + c):deep * (base + d)] = fill[:deep * (d - c)]
                    touched[0] = min(touched[0], row // SUB)
                    touched[1] = max(touched[1], row // SUB + 1)

    def _rows(self, y_top, y_bottom):
        """The first sub-row and the one past the last whose sample line lies between two heights, kept to the plate."""
        first = max(0, ceil(y_top - 0.5))
        end = min(self._sub_rows, ceil(y_bottom - 0.5))
        return first, end

    def _capsule(self, x1, y1, x2, y2, r, fill):
        """Ink everything within r of the segment: a stroke with round ends."""
        if y2 < y1:
            x1, y1, x2, y2 = x2, y2, x1, y1
        if max(x1, x2) + r < 0 or min(x1, x2) - r > self._stride:
            return
        first, end = self._rows(y1 - r, y2 + r)
        # So fine and so level that it lies between two sample lines, or so fine and so upright that it may
        # lie between the sample columns: it is laid as a block, which sees that it is not lost.
        if end <= first or abs(x2 - x1) + 2 * r < COLUMN:
            self._block(min(x1, x2) - r, y1 - r, abs(x2 - x1) + 2 * r, y2 - y1 + 2 * r, fill)
            return
        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy)
        if length < 1e-9:
            self._disc(x1, y1, r, fill)
            return
        # The two long edges stand off the middle line by (ox, -oy) on the right and (-ox, oy) on the left.
        ox, oy = r * dy / length, r * dx / length
        slope = dx / dy if dy > 1e-9 else 0.0
        rights = _side(first, end, x1, y1, x2, y2, r, ox, -oy, slope, 1.0)
        lefts = _side(first, end, x1, y1, x2, y2, r, -ox, oy, slope, -1.0)
        self._paint(first, lefts, rights, fill)

    def _stroke(self, points, r, fill, closed):
        """A stroke through points (in samples), round at every joint."""
        if len(points) == 1:
            self._disc(points[0][0], points[0][1], r, fill)
            return
        if closed:
            points = points + [points[0]]
        x1, y1 = points[0]
        for x2, y2 in points[1:]:
            self._capsule(x1, y1, x2, y2, r, fill)
            x1, y1 = x2, y2

    def _disc(self, cx, cy, r, fill):
        """A filled circle."""
        first, end = self._rows(cy - r, cy + r)
        if end <= first or cx + r < 0 or cx - r > self._stride:
            return
        halves = _chords(first, end, cy, r)
        self._paint(first, [cx - half for half in halves], [cx + half for half in halves], fill)

    def _ring(self, cx, cy, r, inner, fill):
        """A circle with a round hole of radius inner: two runs in each sub-row, one either side of the hole."""
        first, end = self._rows(cy - r, cy + r)
        if end <= first or cx + r < 0 or cx - r > self._stride:
            return
        outer = _chords(first, end, cy, r)
        hole_first, hole_end = self._rows(cy - inner, cy + inner)
        hole = [0.0] * (end - first)
        if hole_end > hole_first:
            hole[hole_first - first:hole_end - first] = _chords(hole_first, hole_end, cy, inner)
        self._paint(first, [cx - half for half in outer], [cx - half for half in hole], fill)
        self._paint(first, [cx + half for half in hole], [cx + half for half in outer], fill)

    def _block(self, x, y, w, h, fill):
        """A filled rectangle with level and upright sides.

        However thin it is, it is not lost. A level block that lies between
        two sample lines is laid on the one nearest its middle, a quarter of
        a pixel thick. An upright block finer than the sample columns stand
        apart (a sixteenth of a pixel: see SHIFT) might stand between two of
        them, so it is laid on the one nearest its middle, a sixteenth wide.
        """
        first, end = self._rows(y, y + h)
        if end <= first:
            first = floor(y + h / 2)
            end = first + 1
            if h <= 0 or not 0 <= first < self._sub_rows:
                return
        if w < COLUMN:
            column = (floor((x + w / 2) / COLUMN) + 0.5) * COLUMN
            x, w = column - COLUMN / 4, COLUMN / 2            # a little either side of that one column
        self._paint(first, [x] * (end - first), [x + w] * (end - first), fill)

    def _write(self, keys, size, x, baseline, r, fill):
        """Write letters from x along a baseline (both in pixels) with a pen of radius r (in samples).

        Each letter is pressed from its stamp where it lies wholly on the
        plate, and drawn stroke by stroke where it does not, or is very large.
        """
        stride, touched, deep = self._stride, self._touched, self._deep
        for key in keys:
            left = round(x * SUB)
            x += _writing(key, size)[0]
            if size > STAMPED:
                self._letter(key, size, left, baseline * SUB, r, fill)
                continue
            (x0, y0, x1, y1), lanes = _stamp(key, size, r)
            if x0 == x1:                                                    # a space: nothing to press
                continue
            if left + x0 < 0 or left + x1 > stride or baseline + y0 < 0 or baseline + y1 > self.height:
                self._letter(key, size, left, baseline * SUB, r, fill)      # it crosses the edge: drawn, and clipped
                continue
            touched[0] = min(touched[0], baseline + y0)
            touched[1] = max(touched[1], baseline + y1)
            for lane, runs in zip(self._lanes, lanes):
                for row, first, count in runs:
                    at = ((baseline + row) * stride + left + first) * deep
                    lane[at:at + count * deep] = fill[:count * deep]

    def _letter(self, key, size, left, bottom, r, fill):
        """One letter drawn stroke by stroke, its place on the baseline at (left, bottom), in samples."""
        _, lines, dots = _writing(key, size)
        dot_r = r + (DOT - 0.5) * _measure(size).pen * SUB
        for points in lines:
            x1, y1 = points[0]
            for x2, y2 in points[1:]:
                self._capsule(left + x1, bottom + y1, left + x2, bottom + y2, r, fill)
                x1, y1 = x2, y2
        for dx, dy in dots:
            self._disc(left + dx, bottom + dy, dot_r, fill)

    # ---- developing the plate

    def _shares(self):
        """For each sample position, three tables: what a sample holds -> its share of red, of green, of blue.

        The k-th of n samples contributes (v + k) // n. Added over k = 0..n-1
        that comes to exactly v, so a pixel wholly of one ink is exactly that ink.

        On a plate of numbered inks a sample holds a number, and the tables
        look up that ink's red, green and blue. In full colour a sample
        holds the red, the green and the blue themselves, and the three
        tables are one and the same.
        """
        count = SUB * SUB
        if self._palette is None:
            parts = [range(NUMBERED)] * 3
        else:
            parts = [[rgb[part] for rgb in self._palette] for part in range(3)]
        return [[bytes((value + k) // count for value in values).ljust(NUMBERED, b"\0") for values in parts]
                for k in range(count)]

    def pixels(self):
        """The plate as it stands: r, g, b for every pixel, row by row. The samples are averaged down here."""
        paper = bytes(self._paper)
        first, end = self._touched
        if end <= first:
            return bytearray(paper * (self.width * self.height))
        shares = self._shares()
        count = self.width * (end - first)
        deep = self._deep
        total = 0
        k = 0
        for lane in self._lanes:
            for offset in range(SUB):
                # the touched rows of the plate, as seen from one sample position: one view, or one for each
                # of a sample's three bytes
                begin, stop = (first * self._stride + offset) * deep, end * self._stride * deep
                views = [bytes(lane[begin + part:stop:SUB * deep]) for part in range(deep)]
                if deep == 1:
                    views *= 3
                seen = [view.translate(table) for view, table in zip(views, shares[k])]
                total += int.from_bytes(b"".join(seen), "little")
                k += 1
        flat = total.to_bytes(3 * count, "little")
        pixels = bytearray(3 * count)
        pixels[0::3] = flat[:count]
        pixels[1::3] = flat[count:2 * count]
        pixels[2::3] = flat[2 * count:]
        return bytearray(paper * (self.width * first)) + pixels + paper * (self.width * (self.height - end))

    def _put(self, path, data):
        """Write a file whole or not at all: a half-written plate is never on show."""
        halfway = None
        try:
            path = os.fspath(path)
            folder, name = os.path.split(path)
            if folder:
                os.makedirs(folder, exist_ok=True)
            halfway = os.path.join(folder, "." + name + ".part")
            with open(halfway, "wb") as handle:
                handle.write(data)
            os.replace(halfway, path)
        except Exception as error:
            self.trouble = "%s: %s" % (type(error).__name__, error)
            try:
                if halfway and os.path.exists(halfway):
                    os.remove(halfway)
            except OSError:
                pass
            return False
        self.trouble = ""
        return True

    # ---- the same drawing as text

    def _svg(self):
        """Every mark made on the plate, in order, as one SVG document."""
        lines = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
                 % (self.width, self.height, self.width, self.height),
                 '<rect width="100%%" height="100%%" fill="%s"/>' % _hex(self._paper),
                 '<g fill="none" stroke-linecap="round" stroke-linejoin="round" '
                 'font-family="Verdana, \'DejaVu Sans\', sans-serif" xml:space="preserve">']
        paper = _hex(self._paper)
        masks = 0
        marks, at = self._marks, 0
        while at < len(marks):
            mark = marks[at]
            if mark[0] == "mask":                 # what follows is seen only inside this mark (see Specimen._draw)
                masks += 1
                lines += ['<mask id="m%d" maskUnits="userSpaceOnUse" x="0" y="0" width="%d" height="%d">'
                          % (masks, self.width, self.height),
                          _svg_mark(_recoloured(mark[1], "#ffffff"), paper), '</mask>', '<g mask="url(#m%d)">' % masks]
            elif mark[0] == "unmask":
                lines.append("</g>")
            elif mark[0] == "rect":               # a field of cells is written as one shape for each ink
                end = at + 1
                while end < len(marks) and marks[end][0] == "rect":
                    end += 1
                lines += _svg_rects(marks[at:end])
                at = end
                continue
            else:
                lines.append(_svg_mark(mark, paper))
            at += 1
        lines.append("</g>")
        lines.append("</svg>")
        return "\n".join(lines) + "\n"


def _side_length(value, otherwise):
    """A plate's width or height as a whole number of pixels, at least 1."""
    numbers = _floats(value)
    if numbers is None:
        return otherwise
    return int(min(max(numbers[0], 1), LARGEST))


def _cut_down(width, height, made_width, made_height):
    """What a plate says of itself when it was made smaller than it was asked for; nothing if it was not."""
    asked = _floats(width, height)
    if asked is None or (asked[0] < made_width + 1 and asked[1] < made_height + 1):
        return ""
    return ("asked for %g x %g, made %d x %d: a plate is at most %d pixels a side and %s in all"
            % (asked[0], asked[1], made_width, made_height, LARGEST, format(MOST, ",")))


def _chords(first, end, cy, r):
    """Half the width of a circle at each sub-row's sample line."""
    rr = r * r
    offset = 0.5 - cy
    return [sqrt(abs(rr - d * d)) for d in [j + offset for j in range(first, end)]]


def _side(first, end, x1, y1, x2, y2, r, ox, oy, slope, sign):
    """One side of a capsule, sub-row by sub-row: round the upper end, down the straight edge, round the lower end.

    The straight edge runs from (x1 + ox, y1 + oy) to (x2 + ox, y2 + oy).
    """
    a = min(max(ceil(y1 + oy - 0.5), first), end)
    b = min(max(ceil(y2 + oy - 0.5), a), end)
    rr = r * r
    upper = [j + (0.5 - y1) for j in range(first, a)]
    lower = [j + (0.5 - y2) for j in range(b, end)]
    start = x1 + ox + (0.5 - y1 - oy) * slope          # where the edge would cross sub-row 0's sample line
    return ([x1 + sign * sqrt(abs(rr - d * d)) for d in upper]
            + [start + j * slope for j in range(a, b)]
            + [x2 + sign * sqrt(abs(rr - d * d)) for d in lower])


def _arc_points(cx, cy, r, start, sweep):
    """Points along an arc, close enough together that the chords cannot be told from the curve."""
    step = 2 * math.acos(max(-1.0, 1 - 0.04 / r)) if r > 0.04 else math.pi
    count = int(min(2000, max(2, ceil(abs(math.radians(sweep)) / step))))
    points = []
    for i in range(count + 1):
        angle = math.radians(start + sweep * i / count)
        points.append((cx + r * math.cos(angle), cy - r * math.sin(angle)))
    return points


def _blend(colours):
    """The average of some (r, g, b) colours, with the same shares as pixels()."""
    count = len(colours)
    return tuple(sum((rgb[channel] + k) // count for k, rgb in enumerate(colours)) for channel in range(3))


# ------------------------------------------------------------------ the PNG

def _png(width, height, pixels):
    """An 8-bit RGB PNG from r, g, b bytes."""
    row = 3 * width
    raw = bytearray((row + 1) * height)               # each row begins with a 0: no filter
    for y in range(height):
        at = y * (row + 1) + 1
        raw[at:at + row] = pixels[y * row:(y + 1) * row]
    return b"".join([
        b"\x89PNG\r\n\x1a\n",
        _chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)),
        _chunk(b"IDAT", zlib.compress(raw, 6)),
        _chunk(b"IEND", b""),
    ])


def _chunk(kind, data):
    """One chunk of a PNG: its length, its kind, its data, and their checksum."""
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)


# ------------------------------------------------------------------ the SVG

def _n(value):
    """A number as SVG wants it: two decimals at most, no trailing zeros."""
    text = "%.2f" % value
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return "0" if text in ("-0", "") else text


def _xml(text):
    """A text made safe to sit inside an SVG element."""
    kept = []
    for ch in text:
        code = ord(ch)
        if code < 32 or 0xd800 <= code <= 0xdfff or code in (0xfffe, 0xffff):
            ch = " "
        kept.append(ch)
    return "".join(kept).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _svg_mark(mark, paper):
    """One mark of the drawing as one SVG element."""
    kind = mark[0]
    if kind == "line":
        _, x1, y1, x2, y2, width, colour = mark
        return '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"/>' % (
            _n(x1), _n(y1), _n(x2), _n(y2), colour, _n(width))
    if kind == "polyline":
        _, points, width, colour, closed = mark
        if len(points) == 1:                      # SVG draws nothing for a stroke of one point; on the plate it is a dot
            (x, y), = points
            return '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (_n(x), _n(y), _n(width / 2), colour)
        return '<%s points="%s" stroke="%s" stroke-width="%s"/>' % (
            "polygon" if closed else "polyline",
            " ".join("%s,%s" % (_n(x), _n(y)) for x, y in points), colour, _n(width))
    if kind == "rect":
        return _svg_rect(mark)
    if kind == "frame":
        _, x, y, w, h, width, colour = mark
        return '<rect x="%s" y="%s" width="%s" height="%s" stroke="%s" stroke-width="%s" stroke-linejoin="miter"/>' % (
            _n(x + width / 2), _n(y + width / 2), _n(w - width), _n(h - width), colour, _n(width))
    if kind == "dot":
        _, x, y, r, colour = mark
        return '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (_n(x), _n(y), _n(r), colour)
    if kind == "ring":
        _, x, y, r, width, colour = mark
        return '<circle cx="%s" cy="%s" r="%s" stroke="%s" stroke-width="%s"/>' % (
            _n(x), _n(y), _n(r - width / 2), colour, _n(width))
    if kind == "arc":
        return _svg_arc(mark)
    _, x, y, s, size, colour, anchor, width, halo = mark
    around = ' stroke="%s" stroke-width="%s" paint-order="stroke"' % (paper, _n(2 * HALO)) if halo else ""
    place = ' text-anchor="%s"' % anchor if anchor in ("middle", "end") else ""
    length = ' textLength="%s" lengthAdjust="spacingAndGlyphs"' % _n(width) if len(s.strip()) > 1 else ""
    return '<text x="%s" y="%s" font-size="%s" fill="%s"%s%s%s>%s</text>' % (
        _n(x), _n(y), _n(size), colour, place, length, around, _xml(s))


def _rect_edges(mark):
    """A filled rectangle's edges as the SVG writes them: (left, top, right, bottom), and whether they may be crisp.

    It is written no finer than the plate lays it (see Canvas._block): a
    quarter of a pixel lying, a sixteenth standing. The edges are rounded,
    not the sizes, so that two rects that share an edge on the plate share
    it here. A rect of a pixel or more each way may have crisp edges; a
    finer one keeps smooth ones, since crisp edges could drop it between
    two pixels.
    """
    _, x, y, w, h, colour = mark
    lying, standing = 1.0 / SUB, COLUMN / SUB     # the finest of each, in pixels
    if h < lying:
        y, h = y + (h - lying) / 2, lying
    if w < standing:
        x, w = x + (w - standing) / 2, standing
    return (round(x, 2), round(y, 2), round(x + w, 2), round(y + h, 2)), (w >= 1 and h >= 1)


def _svg_rect(mark):
    """A filled rectangle standing alone, as an SVG rect."""
    (left, top, right, bottom), crisp = _rect_edges(mark)
    return '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"%s/>' % (
        _n(left), _n(top), _n(right - left), _n(bottom - top), mark[5],
        ' shape-rendering="crispEdges"' if crisp else "")


def _svg_rects(marks):
    """Filled rectangles drawn one after another (a field of cells, perhaps in several inks) -> SVG elements.

    Where no two of them in different inks overlap, the order they were
    drawn in cannot matter, and each ink's rects are gathered into one
    shape. Where some do overlap, only rects of one ink drawn one after
    another are joined, so that what was drawn over stays over.
    """
    groups = _ink_groups(marks)
    if groups is None:
        groups = []
        for mark in marks:
            if groups and groups[-1][-1][5] == mark[5]:
                groups[-1].append(mark)
            else:
                groups.append([mark])
    return [_svg_rect(group[0]) if len(group) == 1 else _svg_field(group) for group in groups]


def _ink_groups(marks):
    """The rects gathered by ink, in the order each ink first came; None if two of different inks overlap.

    Rects that only touch along an edge do not overlap. They are found by
    filing each in squares about the size of a typical rect, so a field of
    thousands costs about as many comparisons as it has cells. A rect far
    larger than the others (one laid under a field, say) is not filed:
    the rects are then simply taken to overlap.
    """
    edged = [(_rect_edges(mark)[0], mark[5]) for mark in marks]
    sizes = sorted(max(right - left, bottom - top) for (left, top, right, bottom), _ in edged)
    square = sizes[len(sizes) // 2] or 1.0
    filed, groups = {}, {}
    for index, ((left, top, right, bottom), ink) in enumerate(edged):
        columns = range(floor(left / square), floor(right / square - 1e-9) + 1)
        rows = range(floor(top / square), floor(bottom / square - 1e-9) + 1)
        if len(columns) * len(rows) > 64:
            return None
        for place in [(i, j) for i in columns for j in rows]:
            for other in filed.setdefault(place, []):
                (l, t, r, b), other_ink = edged[other]
                if other_ink != ink and left < r and l < right and top < b and t < bottom:
                    return None
            filed[place].append(index)
        groups.setdefault(ink, []).append(marks[index])
    return list(groups.values())


def _svg_field(marks):
    """Several filled rectangles in one ink (a field of cells) as one SVG path.

    Written as separate rects, a field shows a hairline of paper at every
    joint wherever the SVG is shown: each rect's edge is smoothed on its
    own, and two half-covered pixels laid one over the other let paper
    through. Crisp edges do not cure it everywhere (a renderer may ignore
    them), and at cells finer than a pixel there is a joint in every pixel
    and the whole field comes out pale and mottled. One path is filled as
    one shape, so its inner joints are not edges at all. Each rect is one
    sub-path, all turning the same way, so where they overlap they add up
    and never cancel.
    """
    pieces, crisp = [], True
    for mark in marks:
        (left, top, right, bottom), fine = _rect_edges(mark)
        crisp = crisp and fine
        pieces.append("M%s %sH%sV%sH%sz" % (_n(left), _n(top), _n(right), _n(bottom), _n(left)))
    return '<path d="%s" fill="%s"%s/>' % ("".join(pieces), marks[0][5], ' shape-rendering="crispEdges"' if crisp else "")


_COLOUR_AT = {"line": 6, "polyline": 3, "rect": 5, "frame": 6, "dot": 4, "ring": 5, "arc": 7, "text": 5}


def _recoloured(mark, colour):
    """The same canvas mark in another colour (for the white shape of an SVG mask)."""
    at = _COLOUR_AT[mark[0]]
    return mark[:at] + (colour,) + mark[at + 1:]


def _svg_arc(mark):
    """An arc as an SVG path (or a whole circle). SVG's y runs down, so counter-clockwise on the page is sweep 0.

    SVG is told an arc's two ends and finds the centre for itself. Written
    to two decimals, two ends that lie close together hardly say where the
    centre is, nor do two that face each other across the circle, and an
    arc between such ends may be drawn in another place. So an arc is
    written in pieces of a third of a turn at most, each the short way
    between two ends that pin it well.
    """
    _, cx, cy, r, start, sweep, width, colour = mark
    if abs(sweep) >= 360:                         # all the way round: a circle
        return '<circle cx="%s" cy="%s" r="%s" stroke="%s" stroke-width="%s"/>' % (
            _n(cx), _n(cy), _n(r), colour, _n(width))
    pieces = max(1, ceil(abs(sweep) / 120.0))
    angles = [math.radians(start + sweep * i / pieces) for i in range(pieces + 1)]
    points = [(_n(cx + r * math.cos(a)), _n(cy - r * math.sin(a))) for a in angles]
    if len(set(points)) == 1:                     # SVG leaves out a path that goes nowhere; on the plate it is a dot
        return '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (points[0] + (_n(width / 2), colour))
    turn = " A%s %s 0 0 %d " % (_n(r), _n(r), 0 if sweep > 0 else 1)
    path = turn.join("%s %s" % point for point in points)
    return '<path d="M%s" stroke="%s" stroke-width="%s"/>' % (path, colour, _n(width))


# ------------------------------------------------------------- the specimen

# The clamps are for the eye, not for taste. Below 2 px a stroke on a 900 x 1200 plate is a hairline that a
# vision model reads as a scratch or loses altogether; above 18 px a trunk swallows the branches beside it and
# the drawing becomes a blot. A dot under 3 px in radius cannot be told from a stroke's end or a speck of dust.
WEIGHTS = (2.0, 18.0)     # a stroke is never thinner or thicker than this, in pixels
SMALLEST_DOT = 3.0        # a dot is never smaller than this, in pixels
LARGEST_DOT = float(LARGEST)      # nor larger than the longest side a plate can have
FINEST = 1.25             # ...unless finer pens were asked for (Specimen.pens); then this is the floor
FINEST_DOT = 1.5
BAR = (80.0, 200.0)       # the scale bar is between these lengths, in pixels (shorter only in a narrow box)
RIM = 1.0                 # the rim drawn round a mark whose ink would not show on the paper, in pixels
RIM_INK = "grey"
APART = 1.0               # the clear paper kept between two small dots whose edges cross, in pixels (see _apart)
APART_MOST = 12.0         # dots of a larger radius are shapes, not things to count: they are left to merge
APART_SQUARE = 32.0       # the squares small dots are filed in; more than twice APART_MOST, and then some
INK_AT = {"line": 3, "polyline": 3, "dot": 3, "arc": 5, "cell": 2, "label": 4}     # where each kind of mark keeps its ink
INSET = 3.0               # clear paper kept inside the box's edge
GRAIN = 2.0 ** 20         # the edges of a cell are set on a grain of this many to the pixel (see _edges)
UNIT_LIMIT = 1.0e12       # a plant coordinate beyond this is not a coordinate


def _units(*values):
    """Plant coordinates as floats, or None if any is not a usable number."""
    try:
        numbers = [float(v) for v in values]
    except Exception:
        return None
    for number in numbers:
        if not -UNIT_LIMIT < number < UNIT_LIMIT:
            return None
    return numbers


def _clamped(value, low, high, otherwise):
    """A size kept between low and high; otherwise, if it is not a number at all (NaN included).

    Every number is clamped, however large: a weight of a million, or of
    infinity, is drawn at the heaviest, never at some default.
    """
    try:
        number = float(value)
    except Exception:
        return otherwise
    if number != number:                      # NaN is the one float not equal to itself
        return otherwise
    return min(high, max(low, number))


class Specimen:
    """The pen a plant is drawn with. Plant units, x to the right, y UP.

    A kind draws the same marks on a pen that only remembers them, and the
    ground replays them here (GROUND.md, Run apart): what follows holds for
    the plant's drawing all the same. Of the settings, only unit_name,
    unit_px_max, align and the notes come through from a kind.

    Positions and lengths (x, y, radius, w, h) are in the plant's own units
    and are scaled to fit the box. Sizes (weight, r, size) are in pixels and
    are not: strokes stay bold however large the plant grows. Weights are
    kept between 2 and 18 px, and dots to a radius of 3 px and up (see
    WEIGHTS for why). A size beyond the range, however far beyond, even
    infinite, is drawn at the nearest end of it; a size that is no number
    at all (NaN, None, a word) is drawn at the default. A position that is
    no number leaves its mark out.

    Nothing reaches the plate until settle() is called, and nothing drawn
    after it does: the plant is settled once. settle() fits the whole
    drawing into the box with one scale, never more than unit_px_max
    pixels to a unit (float("inf") for no limit), and draws it standing on
    the bottom of the box (align "ground") or in its middle ("center", or
    "centre"). Labels are drawn last, each on a little cleared paper, so
    that they can be read over the plant.

    The limit is what lets a plate show age. A seedling two units high is
    drawn 120 px high at the default 60, small in its tall box, and that is
    on purpose: it is small. Only a plant too large for the box at 60 px a
    unit is shrunk to fit, and the scale bar then says how far.

    Because the fit changes as a plant grows, settle() also draws a scale
    bar in the bottom-left corner of the box: a round number of units, 80 to
    200 px long, named with unit_name. The bar is what keeps the picture
    honest about size. A box less than about 200 px wide may not have room
    for such a bar; there the bar is shorter, but still a round number. A
    box less than 96 px wide, or too low to spare the strip, has no bar.

    Nor has a drawing in which nothing has a length: a seed alone, say,
    which is a dot (sized in pixels) under a ground line (a guide). There
    the bar would measure only where the dot was put. A stroke, an arc or a
    cell has a length, and so have two dots at different places; a dot
    alone, lettering and ground lines have none. And a drawing that
    carries its own measure, lettered (months along its foot, say), may
    decline the bar: scale_bar=False, or pen.scale_bar = False set any time
    before settle(). Either way the drawing then has the whole box.

    Declining is for whoever holds the Specimen itself: the ground (a bed's
    sheet draws small bars of its own), a trial. A kind cannot: its pen
    passes no scale_bar on, so a plant's plate keeps its bar wherever there
    is room and something to measure. A kind whose drawing letters its own
    measure can still make the bar honest by naming what one unit is
    (unit_name = "damp day, damp days").

    The ink a kind is given by default is 'wood', the planter's own. 'fresh'
    is kept for what has grown since the last visit. A named ink is looked
    up when the mark is made, not when the drawing is settled: a plant keeps
    the 'wood' it was drawn with, even on a sheet that goes on to the plant
    of another planter.

    A mark in an ink that would hardly show on the paper (white, on this
    cream) is drawn with a fine grey rim, so that a white flower can be
    seen. The rim goes round the pale figure, not round each stroke of it:
    white lengths that meet are one white stem, as they would be in any
    other ink, whatever is drawn between them. A mark in 'paper' clears
    what lies under it; a white mark drawn on it later still has its rim.
    Lettering has no rim: write in an ink that shows.

    Two things are done for the eye without being asked. Small dots whose
    edges cross (fruit in a crowded crown) are kept apart by a line of
    clear paper, so that they can be counted; a dot inside another, a dot
    lying on large ones of other inks (the dark eye of a flower of round
    petals), and a dot more than 12 px in radius, are left alone (see
    _apart). And a
    stroke that lies level or stands upright is moved, by less than half a
    pixel, so that its edges fall between pixels: textures made of fine
    strokes (a doubled stroke for cork or wax, a broken line for what is
    brittle) then stay crisp wherever they fall (see _on_pixels). Stipple
    is dots of the smallest size, at least 8 px apart to stay clear.
    Remember that a texture drawn in plant units shrinks with the fit
    while the pens do not: what is 3 px apart at 60 px a unit runs
    together at 20.
    """

    unit_name = "units"       # what one unit is called on the scale bar ("lengths", "cells", "words"). Written
                              # "length, lengths", a bar of exactly one says "1 length" and not "1 lengths".
    pens = 1.0                # 1: weights and dots as told. A sheet that draws plants small may ask for
                              # finer pens, down to 0.25; then the floors are 1.25 px and 1.5 px instead.
    labels = True             # False: the labels are left out (for a drawing too small to carry them)

    def __init__(self, canvas, box, unit_px_max=60.0, align="ground", scale_bar=True):
        self.canvas = canvas
        self.box = _box(box)                  # (x0, y0, x1, y1) in pixels, or None if it was no box
        self.unit_px_max = unit_px_max
        self.align = align
        self.scale_bar = scale_bar
        self.notes = []
        self.scale = 0.0                      # pixels per unit, once settled
        self.bar = None                       # (units, x_left, x_right, y) of the scale bar, once settled
        self.measured = False                 # once settled: whether anything drawn has a length (see _has_length)
        self._marks = []                      # what was drawn, in plant units, in order
        self._grounds = []                    # heights of ground lines
        self._settled = False

    # ---- drawing

    def line(self, x1, y1, x2, y2, weight=3.0, ink="wood"):
        """A straight stroke from (x1, y1) to (x2, y2)."""
        given = _units(x1, y1, x2, y2)
        if self._refused("a line", given is not None, "an end of it was no usable number"):
            return
        self._marks.append(("line", given, self._weight(weight, 3.0), self._held(ink)))

    def polyline(self, pts, weight=3.0, ink="wood", closed=False):
        """A stroke through several points [(x, y), ...]. closed joins the last point to the first."""
        try:
            points = [_units(x, y) for x, y in pts]
        except Exception:
            points = []
        if self._refused("a polyline", points and None not in points, "it had no points, or a point was no usable number"):
            return
        self._marks.append(("polyline", points, self._weight(weight, 3.0), self._held(ink), _yes(closed)))

    def dot(self, x, y, r=5.0, ink="wood", filled=True, weight=2.0):
        """A round dot at (x, y), r pixels in radius. Not filled: a ring, its outer edge at r."""
        given = _units(x, y)
        if self._refused("a dot", given is not None, "its place was no usable number"):
            return
        self._marks.append(("dot", given, self._radius(r), self._held(ink), _yes(filled), self._weight(weight, 2.0)))

    def arc(self, cx, cy, radius, start_deg, end_deg, weight=3.0, ink="wood"):
        """Part of a circle round (cx, cy), from start_deg to end_deg.

        Angles are measured counter-clockwise: 0 points right, 90 up. The arc
        passes through every angle between the two, so it runs
        counter-clockwise if end_deg is the larger and clockwise if it is the
        smaller: arc(.., 350, 10) is the long way round. To cross 0 write 350
        to 370, or -10 to 10.
        """
        given = _units(cx, cy, radius)
        angles = _floats(start_deg, end_deg)
        if self._refused("an arc", given is not None and angles is not None and given[2] > 0,
                         "its centre, radius or angles were no usable number, or its radius was not above 0"):
            return
        sweep = max(-360.0, min(360.0, angles[1] - angles[0]))
        self._marks.append(("arc", given, angles[0], sweep, self._weight(weight, 3.0), self._held(ink)))

    def cell(self, x, y, w=1.0, h=1.0, ink="wood"):
        """A filled rectangle; (x, y) is its lower-left corner."""
        given = _units(x, y, w, h)
        if self._refused("a cell", given is not None and given[2] != 0 and given[3] != 0,
                         "its place or size was no usable number, or it had no width or no height"):
            return
        x, y, w, h = given
        self._marks.append(("cell", (min(x, x + w), min(y, y + h), abs(w), abs(h)), self._held(ink)))

    def label(self, x, y, s, size=14, ink="ink", anchor="middle"):
        """Words at (x, y), which is their baseline. anchor says which part of them sits at x: start, middle or end.

        Letter in an ink that stands out from the paper: 'ink', 'wood', or a
        dark or strong colour. Lettering has no rim, and in 'faint',
        'pale-pink', 'yellow' or 'white' it cannot be read on this paper at
        size 14, however tempting it is to name a flower in its own colour.
        """
        given = _units(x, y)
        size = _size(size)
        s = _text(s)
        if not s.strip() or self._refused("a label", given is not None and size is not None,
                                          "its place was no usable number, or its size not between 1 and 2000"):
            return
        self._marks.append(("label", given, s, size, self._held(ink), _anchor(anchor, "middle")))

    def _remark(self, words):
        """A word in canvas.remarks. Never raises: noting a thing must not stop a drawing."""
        try:
            self.canvas._remark(words)
        except Exception:
            pass

    def _refused(self, what, usable, why):
        """Whether a mark is left out: asked for after settle(), or not usable. Either way, a word in the remarks."""
        if self._settled:
            self._remark("%s drawn after settle() was left out: the plant was already on the plate" % what)
            return True
        if not usable:
            self._remark("%s was left out: %s" % (what, why))
            return True
        return False

    def _weight(self, weight, otherwise):
        """A stroke's weight kept to WEIGHTS, and a word in the remarks when it had to be."""
        kept = _clamped(weight, *WEIGHTS, otherwise)
        asked = _clamped(weight, -math.inf, math.inf, None)
        if asked is None:
            self._remark("a weight that was no number was drawn at the default, %g px" % otherwise)
        elif asked != kept:
            self._remark("a weight %s %g px was drawn at %g px" % ("under" if asked < kept else "over", kept, kept))
        return kept

    def _radius(self, r):
        """A dot's radius kept to SMALLEST_DOT and up, and a word in the remarks when it had to be."""
        kept = _clamped(r, SMALLEST_DOT, LARGEST_DOT, 5.0)
        asked = _clamped(r, -math.inf, math.inf, None)
        if asked is None:
            self._remark("a dot's radius that was no number was drawn at the default, 5 px")
        elif asked != kept:
            self._remark("a dot's radius %s %g px was drawn at %g px" % ("under" if asked < kept else "over", kept, kept))
        return kept

    def _held(self, ink):
        """An ink as it stands at this moment: a name is looked up when the mark is made, not when it is settled.

        So on a plate that carries the plants of several planters, a plant's
        'wood' is whatever 'wood' was while that plant was being drawn.
        """
        try:
            colour = self.canvas.inks.get(ink, ink)
        except Exception:                     # an ink that cannot be looked up: the plate will draw it in 'ink'
            return ink
        return colour if _rgb(colour) is not None else ink

    def ground(self, y=0.0):
        """A faint ground line across the box at plant height y."""
        given = _units(y)
        if given is not None:
            self._grounds.append(given[0])

    def note(self, s):
        """A line for the caption. At most three are kept."""
        s = _text(s).strip()
        if not isinstance(self.notes, list):
            self.notes = []
        if s and len(self.notes) < 3:
            self.notes.append(s)

    # ---- settling

    def settle(self):
        """Fit the drawing into the box and draw it. Returns pixels per unit (0 if nothing was drawn)."""
        if self._settled:
            return self.scale
        self._settled = True
        try:
            self.scale = self._settle()
        except Exception as error:            # a plant that cannot be drawn leaves its box empty, and says why
            self.scale = 0.0
            self.canvas.trouble = "%s: %s" % (type(error).__name__, error)
            self._remark("the plant could not be drawn: " + self.canvas.trouble)
        return self.scale

    def _settle(self):
        """Find the room, the scale and the place, then draw the marks and the bar."""
        if self.box is None or not (self._marks or self._grounds):
            return 0.0
        x0, y0, x1, y1 = self.box
        marks = self._sized()
        self.measured = _has_length(marks)
        bar = _yes(self.scale_bar)
        if bar and not self.measured:
            bar = False
            self._remark("nothing drawn has a length (a dot alone, lettering, ground lines): no scale bar was drawn")
        strip = self._strip(x1 - x0) if bar else 0.0
        if y1 - y0 - strip < 8:
            strip = 0.0
        if bar and not strip:
            self._remark("the box, %d x %d px, has no room for a scale bar: none was drawn" % (x1 - x0, y1 - y0))
        floor = y1 - strip if strip else y1 - INSET
        room_w = (x1 - x0) - 2 * INSET
        room_h = floor - (y0 + INSET)
        if room_w <= 0 or room_h <= 0:
            return 0.0
        reach = self._reach(marks)
        scale = _fit(reach, room_w, room_h, _clamped(self.unit_px_max, 1e-9, LIMIT, 60.0))
        left, right, bottom, top = _spread(reach, scale)
        if right - left > room_w + 0.5 or top - bottom > room_h + 0.5:
            self._remark("the pens or the labels alone are wider than the box: the drawing overhangs it")
        ox = (x0 + x1) / 2 - (left + right) / 2
        align = self.align.strip().lower() if isinstance(self.align, str) else None
        if align in ("center", "centre"):
            oy = (y0 + INSET + floor) / 2 + (top + bottom) / 2
        else:
            oy = floor + bottom
            if align != "ground":
                self._remark("align %s is not known: the drawing stands on the ground" % _said(self.align))
        self._draw(marks, scale, ox, oy)
        if strip:
            self._draw_bar(scale, strip)
        return scale

    def _strip(self, width):
        """The height kept clear at the bottom of a box this wide for a scale bar that is wanted (0 if there is no room).

        Whenever a strip is kept, a bar is drawn in it. A narrow box keeps a
        higher strip, because there the bar's words stand above it.
        """
        if width < BAR[0] + 16:
            return 0.0
        return 30.0 if width >= 330 else 46.0

    def _sized(self):
        """The marks as they will be drawn: with finer pens if self.pens asks, without labels if self.labels is off."""
        marks = self._marks if _yes(self.labels) else [mark for mark in self._marks if mark[0] != "label"]
        fine = _clamped(self.pens, 0.25, 1.0, 1.0)
        if fine >= 1.0:
            return marks
        sized = []
        for mark in marks:
            kind = mark[0]
            if kind in ("line", "polyline"):
                mark = mark[:2] + (max(FINEST, mark[2] * fine),) + mark[3:]
            elif kind == "dot":
                mark = mark[:2] + (max(FINEST_DOT, mark[2] * fine), mark[3], mark[4], max(FINEST, mark[5] * fine))
            elif kind == "arc":
                mark = mark[:4] + (max(FINEST, mark[4] * fine),) + mark[5:]
            sized.append(mark)
        return sized

    def _reach(self, marks):
        """Everything drawn, gathered by how far its ink reaches past its points.

        {(left, right, down, up) in pixels: [xmin, xmax, ymin, ymax] in plant units}
        The reaches are counted in half pixels, rounded up, so that a plant
        of a thousand weights makes a few dozen entries, not a thousand.
        """
        reach = {}

        def gather(pads, xs, ys):
            box = reach.get(pads)
            if box is None:
                box = reach[pads] = [math.inf, -math.inf, math.inf, -math.inf]
            if xs:
                box[0] = min(box[0], min(xs))
                box[1] = max(box[1], max(xs))
            box[2] = min(box[2], min(ys))
            box[3] = max(box[3], max(ys))

        text_width = self.canvas.text_width
        for mark in marks:
            kind = mark[0]
            if kind == "line":
                half = ceil(mark[2]) / 2
                x1, y1, x2, y2 = mark[1]
                gather((half, half, half, half), (x1, x2), (y1, y2))
            elif kind == "polyline":
                half = ceil(mark[2]) / 2
                gather((half, half, half, half), [p[0] for p in mark[1]], [p[1] for p in mark[1]])
            elif kind == "dot":
                r = ceil(mark[2] * 2) / 2
                gather((r, r, r, r), mark[1][:1], mark[1][1:])
            elif kind == "arc":
                half = ceil(mark[4]) / 2
                xs, ys = _arc_box(mark[1], mark[2], mark[3])
                gather((half, half, half, half), xs, ys)
            elif kind == "cell":
                x, y, w, h = mark[1]
                gather((0.0, 0.0, 0.0, 0.0), (x, x + w), (y, y + h))
            elif kind == "label":
                _, (x, y), s, size, _, anchor = mark
                width = text_width(s, size) + 2 * HALO
                before = {"start": HALO, "middle": width / 2, "end": width - HALO}[anchor]
                heights = [_height(key, size) for key in _spell(s)]
                up = max([0.78 * size] + [above for above, _ in heights])      # tall brackets and accented capitals
                down = max([0.3 * size] + [below for _, below in heights])     # reach further than plain words do
                gather((before, width - before, down + HALO, up + HALO), (x,), (y,))
        if self._grounds:
            gather((0.0, 0.0, 1.0, 1.0), (), self._grounds)
        return reach

    def _draw(self, marks, scale, ox, oy):
        """Draw everything at one scale, with plant (0, 0) at pixel (ox, oy).

        The rims of the pale marks all go down first, under the whole plant,
        and the plant is drawn over them, so that a rim shows only where it
        lies on the paper. Pale strokes that meet are then one figure with
        one edge, however many pieces the figure was drawn in and whatever
        was drawn in between. (Laid one by one, each just before its own
        mark, the rims cut every earlier pale mark they touched: a white
        stem came out as a string of sausages.)

        A mark in the paper's own ink (a halo of clear paper round a bud, a
        patch cleared for a flower) clears what lies under it, the rims
        laid for later marks included. So the rims of the pale marks drawn
        after it, and only of those that reach it, are laid again: only on
        the paper it cleared, and nowhere else. A white flower on a cleared
        patch keeps its edge, and a white stem with a halo beside every
        node is still one stem.
        """
        canvas = self.canvas
        x0, y0, x1, y1 = self.box
        for height in self._grounds:
            canvas.line(x0 + 1, oy - height * scale, x1 - 1, oy - height * scale, 2.0, "faint")
        rim = RIM * _clamped(self.pens, 0.5, 1.0, 1.0)         # finer where the pens are finer, as on a sheet
        body = self._apart([mark for mark in marks if mark[0] != "label"], scale, ox, oy)
        pale = [canvas._pale(mark[INK_AT[mark[0]]]) for mark in body]
        for mark, is_pale in zip(body, pale):
            if is_pale:
                self._make(mark, scale, ox, oy, rim)
        clears = [canvas._clears(mark[INK_AT[mark[0]]]) for mark in body] if any(pale) else [False] * len(body)
        reaching = _Reaching([(j, self._bounds(body[j], scale, ox, oy, rim + 1.0)) for j in range(len(body)) if pale[j]]
                             if any(clears) else [])
        for i, mark in enumerate(body):
            if not clears[i]:
                self._make(mark, scale, ox, oy)
                continue
            later = reaching.after(i, self._bounds(mark, scale, ox, oy, 1.0))
            if not later:
                self._make(mark, scale, ox, oy)
                continue
            runs, count = {}, len(canvas._marks)
            canvas._special = ("trace", runs)
            try:
                self._make(mark, scale, ox, oy)
            finally:
                canvas._special = None
            if not runs or len(canvas._marks) == count:
                continue
            canvas._marks.append(("mask", canvas._marks[-1]))            # the SVG does the same with a mask
            canvas._special = ("within", runs)
            try:
                for j in later:
                    self._make(body[j], scale, ox, oy, rim)
            finally:
                canvas._special = None
            canvas._marks.append(("unmask",))
        for mark in marks:
            if mark[0] == "label":
                _, (x, y), s, size, ink, anchor = mark
                canvas.text(ox + x * scale, oy - y * scale, s, size, ink, anchor, halo=True)

    def _apart(self, body, scale, ox, oy):
        """The marks, with a thin ring of clear paper laid just before each small dot whose edge crosses an earlier dot's.

        In a crown full of fruit, dots of one ink that touch run together
        into one mass that cannot be counted; a line of paper between them
        keeps each one itself, as the plan keeps its plants apart. Only
        dots whose edges cross are parted. A dot that lies wholly inside an
        earlier one is a detail on it and is never parted, even where it
        also crosses a neighbour. Dots larger than APART_MOST are shapes (a
        cushion, a canopy, a round petal) rather than things to count, and
        are meant to merge: they are never parted, though a small dot
        crossing one is.

        A small dot whose ring would lie wholly on such shapes, all of
        other inks than its own, is a detail on them too, though no one of
        them holds it: the dark eye in the middle of four or five round
        petals, which crosses every petal and lies inside none. Its own
        ink already tells it from them; parted, it would wear a pale halo
        that the flower does not have. Only filled shapes count, as only
        they are ink all through. A dot in the same ink as a shape it lies
        on (the grey eye of a dead flower among grey petals) is still
        parted: there the ring is all that shows it.

        The ring is a mark in the paper's own ink, so a white dot parted
        from another keeps its rim (see _draw).
        """
        gap = APART * _clamped(self.pens, 0.5, 1.0, 1.0)
        paper = self._held("paper")
        small, large, shapes, parted = {}, [], [], []
        for mark in body:
            if mark[0] != "dot" or self.canvas._clears(mark[3]):
                parted.append(mark)
                continue
            x, y, r = ox + mark[1][0] * scale, oy - mark[1][1] * scale, mark[2]
            i, j = floor(x / APART_SQUARE), floor(y / APART_SQUARE)
            if r <= APART_MOST:
                near = large + [dot for di in (-1, 0, 1) for dj in (-1, 0, 1) for dot in small.get((i + di, j + dj), ())]
                between = [(math.hypot(x - u, y - v), s) for u, v, s in near]      # centre to centre, and its radius
                inside = any(d + r <= s for d, s in between)
                crosses = any(abs(r - s) < d < r + s + gap for d, s in between)
                if crosses and not inside and not _on_shapes(x, y, r + gap, shapes, self.canvas._dip(mark[3])[1]):
                    parted.append(("dot", mark[1], r + gap, paper, False, gap + 1.0))
                small.setdefault((i, j), []).append((x, y, r))
            else:
                large.append((x, y, r))
                if mark[4] or mark[5] >= r:                  # filled, or a ring so heavy it is drawn as a disc
                    shapes.append((x, y, r, self.canvas._dip(mark[3])[1]))
            parted.append(mark)
        return parted

    def _bounds(self, mark, scale, ox, oy, pad):
        """(x0, y0, x1, y1): the pixels a mark's ink may reach, pad pixels more all round."""
        kind = mark[0]
        if kind == "dot":
            (x, y), reach = mark[1], mark[2] + pad
            xs, ys = (x,), (y,)
        elif kind == "cell":
            x, y, w, h = mark[1]
            xs, ys, reach = (x, x + w), (y, y + h), pad
        elif kind == "arc":
            xs, ys = _arc_box(mark[1], mark[2], mark[3])
            reach = mark[4] / 2 + pad
        else:                                                           # a line or a polyline
            points = mark[1] if kind == "polyline" else (mark[1][:2], mark[1][2:])
            xs, ys = [p[0] for p in points], [p[1] for p in points]
            reach = mark[2] / 2 + pad
        return (ox + min(xs) * scale - reach, oy - max(ys) * scale - reach,
                ox + max(xs) * scale + reach, oy - min(ys) * scale + reach)

    def _make(self, mark, scale, ox, oy, rim=0.0):
        """Draw one mark on the plate.

        rim > 0 draws its rim instead: the same mark in grey, that many
        pixels larger all round. The mark itself is drawn over it later
        (see _draw). This is how a mark in an ink too pale for the paper
        (white, on this cream) is given an edge and can be seen. The rim is
        not counted in the fit: it lies on the clear paper kept inside the
        box's edge (INSET).
        """
        canvas = self.canvas
        kind = mark[0]
        ink = RIM_INK if rim else mark[INK_AT[kind]]
        if kind == "line":
            ax, ay, bx, by = mark[1]
            (x1, y1), (x2, y2) = _on_pixels([(ox + ax * scale, oy - ay * scale), (ox + bx * scale, oy - by * scale)], mark[2])
            canvas.line(x1, y1, x2, y2, mark[2] + 2 * rim, ink)
        elif kind == "polyline":
            points = _on_pixels([(ox + x * scale, oy - y * scale) for x, y in mark[1]], mark[2])
            canvas.polyline(points, mark[2] + 2 * rim, ink, mark[4])
        elif kind == "dot":
            x, y = mark[1]
            canvas.dot(ox + x * scale, oy - y * scale, mark[2] + rim, ink, mark[4], mark[5] + 2 * rim)
        elif kind == "arc":
            cx, cy, radius = mark[1]
            canvas.arc(ox + cx * scale, oy - cy * scale, radius * scale, mark[2], mark[2] + mark[3], mark[4] + 2 * rim, ink)
        elif kind == "cell":
            x, y, w, h = mark[1]
            left, width = _edges(ox + x * scale, ox + (x + w) * scale)
            top, height = _edges(oy - (y + h) * scale, oy - y * scale)
            canvas.rect(left - rim, top - rim, width + 2 * rim, height + 2 * rim, ink)

    def _draw_bar(self, scale, strip):
        """The scale bar, in the bottom-left corner of the box: a round number of units, 80 to 200 px long.

        In a box too narrow for such a bar it is shorter: the most units,
        still a round number, that the box has room for. Its words stand
        beside the bar in a wide box and above it in a narrow one, and the
        unit's name is cut short where there is no room for all of it.
        """
        canvas = self.canvas
        x0, _, x1, y1 = self.box
        left = x0 + 6.0
        right = x1 - INSET - 1.0              # the last tick and the words stay clear of the box's edge
        y = y1 - 9.0
        units = _round_units(scale, right - left)
        length = units * scale
        canvas.line(left, y, left + length, y, 2.0, "ink")
        canvas.line(left, y - 5, left, y + 5, 2.0, "ink")
        canvas.line(left + length, y - 5, left + length, y + 5, 2.0, "ink")
        one, several = _unit_names(self.unit_name)
        count = "%d" % units if 1 <= units < 1e6 else "%g" % units
        if strip < 40:
            words, baseline = left + length + 10, y + 5
        else:
            words, baseline = left, y - 12
        name = _cut(canvas, one if units == 1 else several, 14, right - words - canvas.text_width(count + " ", 14))
        canvas.text(words, baseline, (count + " " + name).rstrip(), 14, "ink")
        self.bar = (units, left, left + length, y)


class _Reaching:
    """Where the pale marks of a drawing lie, so that a mark in the paper's ink can ask which later ones it touches.

    The marks' bounds are filed in squares of REACH_SQUARE pixels; a mark
    that spans very many squares is kept aside and always asked. Bounds
    are generous (a slanting line's are its whole box), which costs only
    a little drawing that falls outside the cleared paper and is not laid.
    """

    def __init__(self, bounded):
        self.squares, self.wide = {}, []
        for index, bounds in bounded:
            squares = _squares(bounds)
            if squares is None:
                self.wide.append((index, bounds))
                continue
            for square in squares:
                self.squares.setdefault(square, []).append((index, bounds))

    def after(self, index, bounds):
        """The indices of the pale marks after `index` whose bounds meet `bounds`, in order."""
        if not self.squares and not self.wide:
            return []
        found = set()
        near = [self.wide] + [self.squares.get(square, ()) for square in (_squares(bounds) or self.squares)]
        x0, y0, x1, y1 = bounds
        for filed in near:
            for other, (a0, b0, a1, b1) in filed:
                if other > index and a0 <= x1 and x0 <= a1 and b0 <= y1 and y0 <= b1:
                    found.add(other)
        return sorted(found)


REACH_SQUARE = 64.0


def _squares(bounds):
    """The squares of REACH_SQUARE pixels that bounds cover, or None if they are too many to file."""
    x0, y0, x1, y1 = (floor(v / REACH_SQUARE) for v in bounds)
    if (x1 - x0 + 1) * (y1 - y0 + 1) > 256:
        return None
    return [(i, j) for i in range(x0, x1 + 1) for j in range(y0, y1 + 1)]


def _has_length(marks):
    """Whether anything in a drawing has a length in plant units: something for a scale bar to measure.

    A stroke, an arc or a cell has one. A dot has only a place (its size
    is in pixels), and so has a stroke that goes nowhere: a line from a
    point to itself, a polyline of one point, an arc of no sweep. Two such
    places apart are a length. Labels and ground lines are left out: one
    is lettering, the other a guide drawn across the whole box.
    """
    place = None
    for mark in marks:
        kind = mark[0]
        if kind == "cell":
            return True
        if kind == "line":
            x1, y1, x2, y2 = mark[1]
            if (x1, y1) != (x2, y2):
                return True
            here = (x1, y1)
        elif kind == "polyline":
            here = tuple(mark[1][0])
            if any(tuple(point) != here for point in mark[1]):
                return True
        elif kind == "arc":
            if mark[3] != 0:
                return True
            (cx, cy, radius), angle = mark[1], math.radians(mark[2])
            here = (cx + radius * math.cos(angle), cy + radius * math.sin(angle))
        elif kind == "dot":
            here = tuple(mark[1])
        else:
            continue
        if place is None:
            place = here
        elif here != place:
            return True
    return False


def _on_shapes(x, y, reach, shapes, colour):
    """Whether the circle of radius `reach` round (x, y) lies wholly on shapes none of which is in `colour`.

    shapes are filled dots, [(x, y, r, '#rrggbb')], in pixels. The circle
    is looked at a point to every pixel of its length, so a sliver of
    paper finer than a pixel between two shapes may pass unseen; a ring
    laid there would hardly show either.
    """
    touching = [(u, v, s, ink) for u, v, s, ink in shapes if math.hypot(x - u, y - v) < reach + s]
    if not touching or any(ink == colour for _, _, _, ink in touching):
        return False
    count = max(16, ceil(2 * math.pi * reach))
    for k in range(count):
        angle = 2 * math.pi * k / count
        px, py = x + reach * math.cos(angle), y + reach * math.sin(angle)
        if not any((px - u) ** 2 + (py - v) ** 2 <= s * s for u, v, s, _ in touching):
            return False
    return True


def _box(box):
    """(x0, y0, x1, y1) in pixels with x0 < x1 and y0 < y1, or None if it is no box."""
    try:
        given = _floats(*box)
    except Exception:
        return None
    if given is None or len(given) != 4:
        return None
    x0, x1 = sorted((given[0], given[2]))
    y0, y1 = sorted((given[1], given[3]))
    if x1 - x0 < 1 or y1 - y0 < 1:
        return None
    return x0, y0, x1, y1


def _on_pixels(points, weight):
    """A stroke that lies level or stands upright, moved (by less than half a pixel) so that its edges fall between pixels.

    Two fine strokes side by side are a texture: a doubled stroke for
    cork or wax is two lines of 2 px with a pixel or two of paper between
    them. Where their edges fall inside a pixel, that pixel is half ink
    from each side, the paper between them is lost, and the pair reads as
    one pale band. Set on the pixels, each stroke is solid and the paper
    between them is clear, wherever the drawing happens to fall. Only a
    stroke wholly level or wholly upright can be set so; a slanting or
    curving one is drawn where it lies. A rim is set by the weight of its
    own mark, so that it stays round it evenly.
    """
    xs, ys = [x for x, _ in points], [y for _, y in points]
    if max(ys) - min(ys) < 0.01:
        y = floor((max(ys) + min(ys)) / 2 - weight / 2 + 0.5) + weight / 2
        return [(x, y) for x in xs]
    if max(xs) - min(xs) < 0.01:
        x = floor((max(xs) + min(xs)) / 2 - weight / 2 + 0.5) + weight / 2
        return [(x, y) for y in ys]
    return points


def _edges(low, high):
    """Two facing edges of a cell, in pixels -> (where the cell begins, how far it goes), both on the grain.

    Two cells that touch must share their edge to the last bit, or a line
    of samples lying exactly on it may belong to neither of them and show
    as a seam. Worked out twice, from one cell and from its neighbour, an
    edge can differ in that last bit: so each edge is set on a grain far
    finer than the samples (GRAIN), where the two agree. A cell too thin to
    span one grain is left as it was, so that it is not closed up.
    """
    if not (-LIMIT < low < LIMIT and -LIMIT < high < LIMIT):
        return low, high - low
    start, end = round(low * GRAIN) / GRAIN, round(high * GRAIN) / GRAIN
    return (start, end - start) if end > start else (low, high - low)


def _spread(reach, scale):
    """How far the drawing reaches at one scale: (left, right, bottom, top) in pixels from plant (0, 0), y up."""
    lefts, rights, bottoms, tops = [], [], [], []
    for (pad_l, pad_r, pad_d, pad_u), (xmin, xmax, ymin, ymax) in reach.items():
        if xmin <= xmax:
            lefts.append(scale * xmin - pad_l)
            rights.append(scale * xmax + pad_r)
        if ymin <= ymax:
            bottoms.append(scale * ymin - pad_d)
            tops.append(scale * ymax + pad_u)
    return min(lefts, default=0.0), max(rights, default=0.0), min(bottoms, default=0.0), max(tops, default=0.0)


def _fit(reach, room_w, room_h, limit):
    """The largest scale, never above limit, at which the whole drawing fits in room_w by room_h pixels."""
    def fits(scale):
        left, right, bottom, top = _spread(reach, scale)
        return right - left <= room_w and top - bottom <= room_h

    if fits(limit):
        return limit
    low, high = 0.0, limit
    if not fits(limit * 1e-12):
        # The pens alone are wider than the box. Fit the points and let the ink overhang.
        left, right, bottom, top = _spread({(0, 0, 0, 0): box for box in _merged(reach)}, 1.0)
        wide, tall = max(right - left, 1e-12), max(top - bottom, 1e-12)
        return min(limit, room_w / wide, room_h / tall)
    for _ in range(60):
        middle = (low + high) / 2
        if fits(middle):
            low = middle
        else:
            high = middle
    return low


def _merged(reach):
    """All the boxes of a reach as one."""
    boxes = list(reach.values())
    return [[min(b[0] for b in boxes), max(b[1] for b in boxes), min(b[2] for b in boxes), max(b[3] for b in boxes)]]


def _arc_box(centre, start, sweep):
    """The xs and ys that bound an arc: its two ends, and wherever it passes due east, north, west or south."""
    cx, cy, radius = centre
    low, high = (start, start + sweep) if sweep >= 0 else (start + sweep, start)
    angles = [low, high]
    quarter = ceil(low / 90.0)
    while quarter * 90.0 < high:
        angles.append(quarter * 90.0)
        quarter += 1
    xs = [cx + radius * math.cos(math.radians(a)) for a in angles]
    ys = [cy + radius * math.sin(math.radians(a)) for a in angles]
    return xs, ys


def _round_units(scale, room=BAR[1]):
    """The round number of units (1, 2, 5, 10, 20, 50, ...) that a scale bar is to show.

    It is the smallest whose bar is at least 80 px long. Where there is not
    room pixels for that one, it is the largest whose bar does fit.
    """
    power = math.floor(math.log10(BAR[0] / scale)) - 1         # begin with a bar of a few pixels, and lengthen it
    fitting = None
    while True:
        for lead in (1, 2, 5):
            units = lead * 10.0 ** power
            if units * scale > room and fitting is not None:
                return fitting
            if units * scale >= BAR[0] * (1 - 1e-9):
                return units
            fitting = units
        power += 1


def _unit_names(unit_name):
    """What one unit is called, and what several are called, from a Specimen's unit_name.

    "lengths" is used for any number of them. Written with a comma, "length,
    lengths", the first is the name for a bar of exactly one.
    """
    one, comma, several = _text(unit_name).partition(",")
    one, several = one.strip(), several.strip()
    if comma and one and several:
        return one, several
    return (one or several,) * 2


def _cut(canvas, s, size, room):
    """A text, or as much of it as room pixels can hold at this size, ending in an ellipsis."""
    if canvas.text_width(s, size) <= room:
        return s
    width = canvas.text_width("\u2026", size)
    kept = ""
    for ch in s:
        width += canvas.text_width(ch, size)
        if width > room:
            break
        kept += ch
    return kept.rstrip() + "\u2026" if kept.strip() else ""
