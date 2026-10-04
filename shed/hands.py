"""
Hands: the few small things every kind of plant needs, and any visitor may use.

The garden is files, and hands of every sort will have been in them. So the
first thing here is a forgiving way to read the garden's keyed files (`seed`,
`tag`, `bed`, `place`):

    kind: twig
    flowers: summer
    # a line beginning with # is a remark
    a line with no colon is kept too, under the key ""

    seed = hands.read_keys(text)              {"kind": "twig", "flowers": "summer", "": "a line with ..."}
    hands.num(seed, "tall", 40, 3, 200)       a number, whatever was written there: never raises, always in 3..200
                                              (0,35 is 0.35; −30, –30 and - 30 are all minus thirty)
    hands.word(seed, "flowers", "spring", ("spring", "summer", "autumn", "winter"))
    hands.line(seed, "says", "")              what a key says, as one line

The rest is for bodies and for drawing:

    hands.is_dead(body)                       does its first line begin with † ?
    hands.fresh_lines(body, left)             which lines were not there when the last visitor left
    hands.mix("#1f4e9c", "#ffffff", 0.3)      two inks blended
    hands.roman(2)                            'ii'

Nothing here raises, whatever it is given. Nothing here touches a file.
Standard library only.
"""

import re

__all__ = ["read_keys", "write_keys", "num", "word", "line", "is_dead", "fresh_lines", "mix", "roman"]

DAGGER = "\u2020"      # † the mark of a dead plant

# A number as a hand writes it: 12 · -3 · 0.35 · 0,35 · .5 · 1e3
_NUMBER = re.compile(r"[-+]?(?:\d+(?:[.,]\d+)?|\.\d+)(?:[eE][-+]?\d+)?")
# The minus as typography and word processors set it, read as the plain one: − (the minus sign), – and — (the
# en and em dashes), ‐ ‑ ‒ (hyphens and the figure dash), ﹣ and － (the small and the fullwidth hyphen-minus).
_MINUS = str.maketrans(dict.fromkeys("\u2212\u2013\u2014\u2010\u2011\u2012\ufe63\uff0d", "-"))
# A minus set apart from its number, as French typography sets it ('- 30', '− 30'): it is still the number's
# sign when nothing but space, an opening bracket or the key's colon stands before it.
_SPACED_MINUS = re.compile(r"(?<![^\s(\[:=~\u2248])-\s+(?=[.,]?\d)")
_ROMAN = ((1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"),
          (50, "l"), (40, "xl"), (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i"))


def _text(value) -> str:
    """Whatever was given, as text. Bytes are read as UTF-8; None is nothing."""
    if value is None:
        return ""
    if isinstance(value, (bytes, bytearray)):
        return bytes(value).decode("utf-8", errors="replace")
    try:
        return str(value)
    except Exception:
        return ""


# ------------------------------------------------------------- keyed files

def read_keys(text) -> dict:
    """A keyed file as a dict. Never raises.

    Each line is `key: value`. Keys are lower-cased and stripped. A key
    written twice keeps both values, one to a line. Lines beginning with #
    are remarks and are skipped, as are empty lines. Lines with no colon are
    kept, in order, under the key "".
    """
    keys = {}
    for raw in _text(text).lstrip("\ufeff").splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        key, colon, value = stripped.partition(":")
        if colon:
            key, value = key.strip().lower(), value.strip()
        else:
            key, value = "", stripped
        keys[key] = keys[key] + "\n" + value if key in keys else value
    return keys


def write_keys(d) -> str:
    """A dict as the text of a keyed file: the other way round from read_keys.

    A value of several lines is written as the key repeated. Remarks are not
    in a dict, so a file read and written back loses them: to add one line to
    a file someone else wrote, append to it instead.
    """
    lines = []
    try:
        items = list(d.items())
    except Exception:
        return ""
    for key, value in items:
        key = _text(key).strip()
        parts = value if isinstance(value, (list, tuple)) else _text(value).split("\n")
        for part in parts:
            part = _text(part).strip()
            lines.append("%s: %s" % (key, part) if key else part)
    return "\n".join(lines) + "\n" if lines else ""


def line(d, key, default="") -> str:
    """What a key says, as one line. If the key was written twice, the last line wins."""
    try:
        value = d.get(key)
    except Exception:
        return default
    for said in reversed(_text(value).splitlines()):
        if said.strip():
            return said.strip()
    return default


def num(d, key, default, lo=None, hi=None):
    """The number a key holds, kept between lo and hi. Never raises.

    The first number on the line is taken, so `light: 0.35   in the wall's
    shade` reads as 0.35, and a French `0,35` does too. A minus is a minus
    however it was typeset: `hardy: −30` (the minus sign), `–30` (a dash),
    `－30` (a fullwidth one) and `- 30` all read as -30. (If the key was
    written twice, the last line that holds a number wins.) If there is no
    number, or no such key, the default comes back (clamped as well, if it
    is a number). An endless number with no bound to hold it is no number.
    """
    value = default
    try:
        text = _text(d.get(key))
    except Exception:
        text = ""
    for said in reversed(text.splitlines()):
        found = _NUMBER.search(_signed(said))
        if found:
            try:
                value = float(found.group().replace(",", "."))
            except ValueError:
                value = default
            break
    return _clamp(value, default, lo, hi)


def _signed(text) -> str:
    """A line with every way of typesetting a minus made the plain '-', set close to its number: '− 30' -> '-30'."""
    return _SPACED_MINUS.sub("-", _text(text).translate(_MINUS))


def _clamp(value, default, lo, hi):
    """A number kept between lo and hi; what is not a number at all becomes the default."""
    lo, hi = _bound(lo), _bound(hi)
    try:
        value = float(value)
    except Exception:
        return default
    endless = value in (float("inf"), float("-inf")) and (hi if value > 0 else lo) is None
    if value != value or endless:            # not a number, or one with no end and nothing to hold it
        try:
            value = float(default)
        except Exception:
            return default
        if value != value:
            return default
    if lo is not None and value < lo:
        value = lo
    if hi is not None and value > hi:
        value = hi
    return value


def _bound(limit):
    """A bound as a number, or None if it is none."""
    try:
        limit = float(limit)
    except Exception:
        return None
    return limit if limit == limit else None


def word(d, key, default, choices=None) -> str:
    """The word a key holds, lower-cased. Never raises.

    With choices: the first word on the line that is one of them, else the
    default. Without: the first word on the line, whatever it is. (For a
    whole sentence, use line().)
    """
    words = [w.strip(",;.!?\"'()").lower() for w in line(d, key, "").split()]
    words = [w for w in words if w]
    if choices is None:
        return words[0] if words else default
    try:
        allowed = {_text(c).lower() for c in choices}
    except Exception:
        allowed = set()
    for candidate in words:
        if candidate in allowed:
            return candidate
    return default


# ------------------------------------------------------------------ bodies

def is_dead(body) -> bool:
    """A body is dead when its first line that is not empty begins with †."""
    for said in _text(body).splitlines():
        if said.strip():
            return said.lstrip().startswith(DAGGER)
    return False


def fresh_lines(body, left) -> set:
    """The indices of the lines of body that were not in left.

    left is the body as the last visitor left it. Every line of left accounts
    for one equal line of body, so a line that appears twice now and appeared
    once then has one fresh copy (the later one). Empty lines are never
    fresh. If left is None the plant is new since then, and every line is.
    """
    lines = _text(body).splitlines()
    if left is None:
        return {i for i, said in enumerate(lines) if said.strip()}
    before = {}
    for said in _text(left).splitlines():
        said = said.rstrip()
        before[said] = before.get(said, 0) + 1
    fresh = set()
    for i, said in enumerate(lines):
        said = said.rstrip()
        if not said.strip():
            continue
        if before.get(said, 0) > 0:
            before[said] -= 1
        else:
            fresh.add(i)
    return fresh


# ------------------------------------------------------------------- small

def _rgb(colour):
    """'#rrggbb', '#rgb' or the name of one of the plate's inks -> (r, g, b), or None."""
    colour = _text(colour).strip().lower()
    if colour and not colour.startswith("#"):
        try:
            import plate
            colour = plate.INKS.get(colour, "")
        except Exception:
            colour = ""
    digits = colour[1:]
    if len(digits) == 3:
        digits = "".join(c + c for c in digits)
    if len(digits) != 6 or any(c not in "0123456789abcdef" for c in digits):
        return None                          # (int() alone would take "0x12ab", "1_2345" and other scripts' digits)
    try:
        value = int(digits, 16)
    except ValueError:
        return None
    return (value >> 16) & 255, (value >> 8) & 255, value & 255


def mix(hex_a, hex_b, t=0.5) -> str:
    """Two inks blended: t = 0 is all hex_a, t = 1 is all hex_b. Returns '#rrggbb'.

    An ink that cannot be read gives way to the other; if neither can, the
    answer is the plate's near-black.
    """
    a, b = _rgb(hex_a), _rgb(hex_b)
    if a is None and b is None:
        return "#1a1a1a"
    a, b = a or b, b or a
    t = _clamp(t, 0.5, 0.0, 1.0)
    return "#%02x%02x%02x" % tuple(int(round(x + (y - x) * t)) for x, y in zip(a, b))


def roman(n) -> str:
    """A small number in lower-case roman numerals: 2 -> 'ii'. Nothing for zero or less."""
    try:
        n = int(n)
    except Exception:
        return ""
    n = min(n, 3999)
    out = []
    for value, letters in _ROMAN:
        while n >= value:
            out.append(letters)
            n -= value
    return "".join(out)
