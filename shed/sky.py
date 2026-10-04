"""The sky over the Glebe.

Every day the garden lives has a sky, and everything in the beds grows under
it. This file answers one question:

    sky_for(root, day)      what was the sky over the garden that day?

The answer is a `Sky`: the night's low and the day's high, the rain, the cloud,
the wind, how long the day was and how much of its light came through, how wet
the ground already was, the moon, the season, and one plain line of words
(`sky.words`). `local(sky, bed)` gives the same sky as one bed feels it, behind
its wall or at the pond's edge.

    python shed/sky.py                 today's sky over the garden
    python shed/sky.py 2026-10-04      that day's sky, and the keeper's words for it
    python shed/sky.py 2027-06-01 to 2027-08-31
                                       each day of a span, as the plants will live it,
                                       and what it came to: rain, dry runs, frosts
    python shed/sky.py --gate          each line of gate/sky.txt: the day it was read
                                       for, what was understood, what it changed
    python shed/sky.py --words         the words the gate reader knows
    python shed/sky.py --help          all of this

TO TRY A KIND UNDER WEATHER OF YOUR OWN. The reckoned sky (3. below) is a
mild one: a month without rain comes about once in ten years, a summer-long
drought never, and its hardest frosts are about -13°. To see how a kind
fares in weather the garden never gives it, lay a trial ground

    python shed/foundations/trial_ground.py "<an empty folder outside the garden>"

and write the weather at that trial ground's own gate, in its gate/sky.txt
(make the folder `gate` if there is none), one line for each run of days, in
the words the gate reader knows (1. below; --words lists them):

    2027-06-10 to 2027-08-31: sec, soleil, 14 à 28°      a summer's drought
    2028-01-05 to 2028-01-25: frost, -9 to -2°           three weeks of hard frost
    2027-11-01 to 2027-11-30: rain 12 mm, overcast       a month of rain

Then, inside the trial ground, `python shed/sky.py 2027-06-01 to 2027-09-15`
shows those days as its plants will live them, and `--gate` what each line
was heard as; wind its clock on (`python shed/foundations/clock.py --advance
N`) and pass its gate (`python shed/arrive.py --as <a name>`) to live them. A
line changes only what it says: "sec" alone keeps the reckoned cloud and
warmth. The ground dries or soaks with what is written (`sky.wet`), and each
bed takes its share as always. One line covers at most 93 days, so write a
longer spell as several. Write such lines only in a trial ground: the
garden's own gate/sky.txt is the keeper's, and what is written there becomes
the garden's weather.

A day's sky is looked for in three places, in this order.

1. THE GATE. The keeper may write the day's weather in `gate/sky.txt`, one line
   a day, in French or English:

       2026-10-04: pluie 6mm, 9 à 15°, gris toute la journée
       2026-10-05 - beau soleil, gel le matin, -1 / 12
       2026-10-06 rain

   A line begins with its date: year first (2026-10-04; 2026/10/4 will do),
   or day first with the whole year last (04/10/2026), or in words (4 octobre
   2026, 1er novembre 2026, 4 October 2026). A weekday or "le" may stand
   before it, and "2026-10-04 to 2026-10-08: ..." covers a run of days, at
   most 93 of them: a longer run (a slip of the pen in the year, perhaps)
   is read for its first day only, and `--gate` says so.

   THE READER PREFERS SILENCE TO INVENTION. A missed frost is a small loss; an
   invented one kills plants. So the reader cuts their line into thoughts, at
   its commas and full stops (and , ; : ! ? ( ) / · and "et", "mais", "puis",
   "and", "but", "then"), and a thought changes the sky only when every word
   and every number in it is understood. One word it does not know, or one
   number that might be counting something else, and the whole thought is
   left alone. A word for another day (demain, hier, prévu, depuis, a weekday,
   a month, a date) leaves alone the rest of its sentence as well: "gel ce
   matin, demain pluie" is a frost and nothing more. So does a thought it
   cannot read that ends in a colon: "fleurs : gris, rose" may be speaking of
   the flowers. But a title that names the day itself or the gauge they read
   (Noël, Toussaint, Pâques, pluviomètre, thermomètre, relevé: the TITLE_WORDS)
   is no such thought: "Noël : soleil, -2 à 5" is read whole. It understands
   little, on purpose, and is sure of what it understands.

   The numbers it takes, and only these:

     6 mm · 6,5 mm · 5 à 10 mm              rain (a range at its middle)
     10 cm, beside the word snow (neige)    snow; a centimetre counts as a millimetre of water
     9 à 15° · 9–15° · -1 / 12 · -5 -1 ·    the night's low and the day's high
       entre 9 et 15° · min 3 · max 12
     9 à 15 · 0 to 4 · 10-16, standing      the low and the high too, with no °: see below
       alone between commas
     12° · -3 · moins 2°                    a temperature they saw at some hour: the day is
                                            widened to hold it, and no more
     20 km/h · 10 à 20 km/h · 12 mph ·      the wind
       force 3-4 · 4 bft

   A number with no ° and no unit is left alone: "pluie 6" might be
   millimetres or showers, "2 à 3 averses" counts showers, "de 9 à 15" is
   hours. The one exception is two numbers that stand alone between commas,
   the lower first, joined by à, to, a dash or "entre ... et", no more than
   25 apart and no warmer than 45: "rain 6mm, 9 to 15, grey all day" and
   "brouillard, 0 à 4" give the day's low and high. Written so, nothing else
   is meant, and having no minus sign they can never make a frost. Anything
   more in the thought ("vent 3 à 4", "9 à 15 cette nuit") and the pair is
   left alone again: write the °. A pair written of a part of the day
   ("-5 à -1 cette nuit") is what that part saw, not the whole day's low and
   high.

   The words it knows are in the tables further down: rain (pluie, averse,
   bruine, orage ...), dry (sec), frost (gel, gelée, givre), snow (neige),
   fog (brouillard, brume), the sky (soleil, beau, clair, dégagé, éclaircies,
   nuageux, gris, couvert ...), the wind (vent, brise, rafales, tempête,
   "vent léger", "vent fort"), cold and warm (froid, frais, doux, chaud,
   canicule), light and heavy, the parts of the day (le matin, l'après-midi,
   le soir, la nuit), and a no before a word: "pas de pluie", "sans gel",
   "no frost or snow", "il ne pleut pas", "il n'a pas plu", "it didn't rain".
   Small words (le, la, il, fait, toute la journée, the, it, all day ...) may
   stand among them.

   Rain, frost, snow or fog said of any part of the day happened that day. But
   "sec le matin" or "pas de gel cette nuit" says nothing of the whole day, so
   "pluie le matin, sec l'après-midi" is a day with rain in it. Amounts are
   added when each names its own part of the day ("4 mm le matin, 6 mm le
   soir" is 10); otherwise the largest stands.

   A day they call clear (soleil, clear, beau, ciel clair, not a cloud ...)
   is a dry day, when that is said of the whole day, their words for it come
   to a clear sky in all, and no rain, shower or snow is named anywhere in
   them: "frost, -4 to 6, clear" has no rain, and so no snow. But sun said
   of a part of the day ("soleil le soir"), or among clouds ("éclaircies",
   "sun and cloud", "soleil, gris"), takes no rain away.

   A day written on several lines is heard as one: its lines mean what they
   would mean as the sentences of one line, in any order. Where they disagree
   of the whole day (rain and dry, frost and no frost), that thing is left as
   it was.

   Their whole sentence is kept in `sky.remark`, understood or not, and the
   almanac prints it beside the day. A day keeps its latest 20 lines, 500
   characters in all, and the day is heard from exactly that remark: what the
   almanac shows of their words is what the day was laid from.

   `understand("gel le matin, -1 / 12")` gives what the reader makes of a
   line, `explain(...)` says it thought by thought in plain words, and
   `unread(root)` gives the lines no date could be read from.

2. THE REAL SKY. Only if `ground/place` says `real-sky: yes` and gives a
   longitude: the day's real weather from open-meteo.com, asked for once and
   kept in `ground/sky-cache`. Five seconds are allowed for a question, and a
   few more for all the questions of one visit; if the asking fails in any
   way, or the answer is not what a sky can be, the day is simply reckoned.
   It is off unless the keeper turns it on, and while it is off nothing in
   this file goes near the network. (When it is on, the garden's latitude and
   longitude are what is sent.)

3. RECKONED. A temperate oceanic climate worked out from the date and the
   garden's `weather-seed`, and nothing else. No day leans on the day before:
   each one is read off a few long slow waves whose crests were fixed by the
   seed, so warm and cold spells last for days, rain comes in runs, and the
   seasons arrive by degrees. The same seed gives the same ten thousand days
   to anyone who asks, in any order. It cannot be guessed in one's head, which
   is the point of it: look up.

The moon and the length of the day are real astronomy, good to a few minutes.

`sky_for` is a pure function of the garden's files and the date. What it has
worked out is remembered while the process lasts, and the three files it
reads (`ground/place`, `gate/sky.txt`, `ground/sky-cache`) are read again at
every asking, so a changed line is heard at once and nothing remembered can
change an answer. Snow and fog are not numbers of the Sky: `sky.snow` and the
"fog" of `sky.words` are heard again from `sky.remark` each time they are
asked, by the same reader that laid the day.
"""

from __future__ import annotations

import datetime
import json
import math
import os
import re
import sys
import time
import unicodedata
import zlib
from dataclasses import dataclass, replace
from functools import lru_cache

Date = datetime.date
ONE_DAY = datetime.timedelta(days=1)


# ───────────────────────────────────────────────────────────── the sky itself

MOON_NAMES = ("new", "waxing crescent", "first quarter", "waxing gibbous",
              "full", "waning gibbous", "last quarter", "waning crescent")
NAMED_PHASE = 0.034     # new, full and the quarters keep their name about a day either side
SNOW_BELOW = 1.0        # °C: what falls on a day whose mean is at or under this is snow


@dataclass(frozen=True)
class Sky:
    """One day's sky over the garden (or over one bed of it)."""

    date: datetime.date
    tmin: float        # °C, the night's low
    tmax: float        # °C, the day's high
    rain: float        # mm that day (snow counts as the water it holds)
    cloud: float       # 0 clear .. 1 overcast
    wind: float        # Beaufort, 0..10
    daylength: float   # hours from sunrise to sunset
    light: float       # hours of useful light = daylength * (1 - 0.7 * cloud)
    wet: float         # 0 dust .. 1 sodden: the ground after the last fortnight's rain
    moon: float        # 0 new · 0.25 first quarter · 0.5 full · 0.75 last quarter
    season: str        # 'spring' | 'summer' | 'autumn' | 'winter', by calendar month, flipped south of the equator
    source: str        # 'reckoned' | 'gate' | 'open-meteo'
    remark: str = ""   # the keeper's own words for the day, if they left any

    @property
    def tmean(self) -> float:
        """The day's mean temperature, °C."""
        return _rounded((self.tmin + self.tmax) / 2.0, 2)

    @property
    def warmth(self) -> float:
        """Degrees above 5 °C, where most growing starts; never below zero."""
        return round(max(0.0, self.tmean - 5.0), 2)

    @property
    def frost(self) -> bool:
        """True when the night went below zero."""
        return self.tmin < 0

    @property
    def snow(self) -> bool:
        """True when what fell that day was snow: by the keeper's word if they gave one, else by the cold.

        Their words are heard from `remark`, by the same reader that laid the day from it.
        """
        if self.rain <= 0:
            return False
        said = _said(self.remark)
        if said.get("snow") is not None:                     # "neige", or "pas de neige"
            return said["snow"]
        if said.get("raining"):
            return False                                     # they called it rain, and said nothing sure of snow
        return self.tmean <= SNOW_BELOW

    @property
    def moon_name(self) -> str:
        return moon_name(self.moon)

    @property
    def words(self) -> str:
        """One plain line: "overcast, 9–15°, rain 6 mm, light 7.4 h, moon waxing gibbous"."""
        parts = ["fog" if _said(self.remark).get("fog") else _cloud_word(self.cloud)]
        parts.append(_degrees(self.tmin, self.tmax))
        if self.frost:
            parts.append("frost")
        if self.rain > 0:
            parts.append(("snow " if self.snow else "rain ") + _millimetres(self.rain) + " mm")
        else:
            parts.append("no rain")
        if self.wind >= 6:
            parts.append("gale" if self.wind >= 8 else "strong wind")
        parts.append(f"light {self.light:.1f} h")
        name = self.moon_name
        parts.append(f"{name} moon" if name in ("new", "full") else f"moon {name}")
        return ", ".join(parts)


def moon_name(phase) -> str:
    """The usual name for a phase between 0 and 1. 'new' and 'full' are said bare."""
    try:
        quarters = (float(phase) % 1.0) * 4.0
    except (TypeError, ValueError):
        return MOON_NAMES[0]
    if quarters != quarters:                       # not a number
        return MOON_NAMES[0]
    nearest = round(quarters)
    if abs(quarters - nearest) <= NAMED_PHASE * 4.0 + 1e-9:    # a hair over, so both sides of a phase are as wide
        return MOON_NAMES[(nearest % 4) * 2]
    return MOON_NAMES[(int(quarters) % 4) * 2 + 1]


def _cloud_word(cloud: float) -> str:
    for below, word in ((0.2, "clear"), (0.4, "bright"), (0.62, "sun and cloud"), (0.82, "cloudy")):
        if cloud < below:
            return word
    return "overcast"


def _rounded(value: float, places: int) -> float:
    """Rounded, and never the "-0.0" that rounding a small frost can leave."""
    return round(value, places) + 0.0


def _finite(value) -> bool:
    """Is this a number a sky can use: an int or a float, and neither NaN nor infinity?"""
    try:
        return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)
    except OverflowError:                            # a whole number too long to be a float
        return False


def _degrees(tmin: float, tmax: float) -> str:
    """The low and the high in words: "9–15°", "-2 to 7°". A sky with no number in it says "?°"."""
    try:
        low, high = _degree(tmin), _degree(tmax)
    except (TypeError, ValueError, OverflowError):
        return "?°"
    if low.startswith("-") or high.startswith("-"):
        return f"{low} to {high}°"                   # "-2–7°" would be hard to read
    return f"{low}–{high}°"


def _degree(value: float) -> str:
    """One temperature to the whole degree; a frost too slight to round is said to the tenth ("-0.3")."""
    whole = int(round(value))                        # int() also turns -0 into 0, and will not take nan or inf
    if whole == 0 and round(value, 1) < 0:
        return f"{value:.1f}"                        # "0" would hide that it froze
    return str(whole)


def _millimetres(mm: float) -> str:
    if not _finite(mm):
        return "?"
    return f"{mm:.1f}" if mm < 0.95 else str(int(round(mm)))


def _as_written(mm: float) -> float:
    """A day's rain as its own line writes it (see _millimetres). A total of several days adds these up, so that
    whoever adds the days' lines finds the total the note gives: two days written "2 mm" make 4, though the sky
    held 1.6 and 1.6."""
    said = _millimetres(mm)
    return 0.0 if said == "?" else float(said)


# ───────────────────────────────────────────────────────────────── the place

DEFAULT_PLACE = {
    "laid": Date(2026, 9, 30),     # the day the ground was laid
    "latitude": 47.0,
    "weather-seed": 20260930,
    "real-sky": False,
    "longitude": None,
}
_YES = {"yes", "oui", "y", "o", "true", "vrai", "on", "1"}
# A number as a hand writes it, the way `hands.num` reads it: 12 · -3 · 0.35 · 0,35 · .5 · 1e3
_NUMBER_ANYWHERE = re.compile(r"[-+]?(?:\d+(?:[.,]\d*)?|[.,]\d+)(?:e[-+]?\d+)?", re.IGNORECASE)
_SOUTH = r"(?:s|sud|south)"            # a letter beside a latitude that puts it below the equator,
_WEST = r"(?:w|west|o|ouest)"          # or beside a longitude, west of Greenwich
# What may follow the degrees of an angle: 41°18' · 41° 18' 30" (the minutes, and the seconds if any)
_MINUTES = re.compile(r"\s*°\s*(\d+(?:[.,]\d+)?)\s*['′’]\s*(?:(\d+(?:[.,]\d+)?)\s*(?:\"|″|''|’’))?")
_DASHES = {0x2212: "-", 0x2013: "-", 0x2014: "-"}       # the minus sign a word processor puts for a hyphen


def place(root) -> dict:
    """`ground/place`, read, with defaults for whatever is missing or garbled.

    The values come back as what they are: `laid` a date, `latitude` a float,
    `weather-seed` an int, `real-sky` True or False, `longitude` a float or
    None. Any other line the keeper added is passed on as they wrote it.
    """
    return dict(_place_from(_bytes_of(_path(root, "ground", "place"))))


@lru_cache(maxsize=16)
def _place_from(data: bytes | None) -> tuple:
    """The place as (key, value) pairs, from the file's bytes. Never raises."""
    found = dict(DEFAULT_PLACE)
    try:
        keys = _read_keys(_text_of(data))
    except Exception:
        keys = {}
    for key, value in keys.items():
        if not isinstance(key, str) or key == "":
            continue
        line = _last_line(value)
        if key == "laid":
            found[key] = _written_date_in(line) or found[key]
        elif key == "latitude":
            found[key] = _angle_in(line, 90.0, _SOUTH, found[key])
        elif key == "longitude":
            found[key] = _angle_in(line, 180.0, _WEST, None)
        elif key == "weather-seed":
            found[key] = _seed_in(line, found[key])
        elif key == "real-sky":
            found[key] = _says_yes(line)
        else:
            found[key] = line
    return tuple(found.items())


def _says_yes(line: str) -> bool:
    """Does a line say yes, and nothing but yes?

    The real sky sends the garden's position out over the network, so it is
    turned on only by one plain yes-word standing alone ("yes", "Oui.", "on").
    A remark may follow after a # or in brackets. "on verra", "y a pas",
    "true? not sure" and "yes, but not yet" are all no.
    """
    words = re.findall(r"\w+", re.split(r"[#(\[]", line, maxsplit=1)[0].lower())
    return len(words) == 1 and words[0] in _YES


def _last_line(value) -> str:
    """A keyed value as one line (a key written twice keeps its last line)."""
    if isinstance(value, (list, tuple)):
        value = value[-1] if value else ""
    lines = [line.strip() for line in str(value).splitlines() if line.strip()]
    return lines[-1] if lines else ""


def _number_in(text: str, low: float, high: float, default):
    """The first number in a line, if it lies between low and high; else the default."""
    found = _NUMBER_ANYWHERE.search(text)
    number = _number(found.group()) if found else None
    if number is None or not low <= number <= high:
        return default
    return number


def _angle_in(text: str, most: float, minus: str, default):
    """A latitude or a longitude: the first number in a line, within ±most, else the default.

    Minutes and seconds are counted in: 41°18' is 41.3. A hemisphere written
    as a letter is heard, before the number or closing the value after it:
    "41.3 S", "S 41.3" and "41°18' S" are all -41.3, "0,69° O" (ouest) is
    -0.69. But "47.0 sud de la rivière" is 47 north: there the word goes on to
    say something else. `minus` is the pattern of the letters that mean below zero.
    """
    text = text.translate(_DASHES)
    found = _NUMBER_ANYWHERE.search(text)
    number = _number(found.group()) if found else None
    if number is None:
        return default
    before, after = text[:found.start()], text[found.end():]
    minutes = _MINUTES.match(after)
    if minutes:
        sixtieths = _number(minutes.group(1)) / 60.0 + (_number(minutes.group(2) or "0") or 0.0) / 3600.0
        number = round(math.copysign(abs(number) + sixtieths, number), 6)
        after = after[minutes.end():]
    if (re.fullmatch(rf"\s*{minus}[\s.:]*", before, re.IGNORECASE)
            or re.match(rf"\s*°?\s*{minus}\.?\s*(?:$|[#(\[])", after, re.IGNORECASE)):
        number = -abs(number)
    return number if -most <= number <= most else default


def _date_in(text: str):
    """The first date written year first in a text (2026-10-04), or None."""
    found = re.search(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", text)
    return _date_from(*found.groups()) if found else None


def _written_date_in(text: str):
    """The first date in a text, written any way the gate accepts: 2026-10-15, 15/10/2026, 15 octobre 2026."""
    found = re.search(_WRITTEN_DATE, text, re.IGNORECASE)
    return _written_date(found.groups()) if found else None


def _date_from(year, month, day):
    try:
        return Date(int(year), int(month), int(day))
    except (ValueError, TypeError):
        return None


def _seed_in(text: str, default: int) -> int:
    """The weather seed: a whole number, or any word at all (a word is hashed)."""
    text = text.strip()
    if not text:
        return default
    number = re.match(r"[-+]?\d{1,18}\b", text)
    return int(number.group()) if number else zlib.crc32(text.encode("utf-8"))


def _plain_keys(text: str) -> dict:
    """A keyed file read the garden's way. Used only if `hands` is not to be found."""
    keys: dict = {}
    for line in text.splitlines():
        if line.strip().startswith("#") or not line.strip():
            continue
        key, colon, value = line.partition(":")
        key, value = (key.strip().lower(), value.strip()) if colon else ("", line.strip())
        keys[key] = keys[key] + "\n" + value if key in keys else value
    return keys


def _plain_num(value, default: float, low: float, high: float) -> float:
    """A number read the garden's way and kept between low and high. Used only if `hands` is not to be found.

    As in `hands.num`: if the key was written twice, the last line that holds a number wins.
    """
    number = default
    try:
        if isinstance(value, (list, tuple)):
            value = "\n".join(str(line) for line in value)
        for line in reversed(str(value if value is not None else "").splitlines()):
            found = _number_in(line, -math.inf, math.inf, None)
            if found is not None:
                number = found
                break
    except Exception:
        number = default
    return max(low, min(high, number))


def _num(value, default: float, low: float, high: float) -> float:
    """What a key holds, as the number `hands.num` would make of it. Never raises."""
    try:
        return float(_the_hands().num({"it": value}, "it", default, low, high))
    except Exception:                              # no hands in the shed: the sky reads it alone
        return _plain_num(value, default, low, high)


_hands = False            # the garden's `hands`, once looked for: the module, or None if it is not to be found


def _the_hands():
    """`hands`, which sits beside this file in the shed; None if it is missing or broken (the sky then stands alone)."""
    global _hands
    if _hands is False:
        try:
            import hands as found
        except Exception:
            found = None
        _hands = found
    return _hands


def _read_keys(text: str) -> dict:
    """Read a keyed file with `hands.read_keys`; the sky stands alone if hands is missing."""
    try:
        keys = _the_hands().read_keys(text)
        return keys if isinstance(keys, dict) else _plain_keys(text)
    except Exception:
        return _plain_keys(text)


def _path(root, *parts) -> str:
    return os.path.join(os.path.abspath(os.fspath(root)), *parts)


def _bytes_of(path: str) -> bytes | None:
    """A file's bytes (the first two million, if someone left a mountain), or None if it cannot be read."""
    try:
        with open(path, "rb") as file:
            return file.read(2_000_000)
    except OSError:
        return None


def _text_of(data: bytes | None) -> str:
    """Bytes as text. UTF-8 first; a file saved by an old Notepad keeps its accents too.

    Notepad's "Unicode" is UTF-16, which always begins with its two-byte mark;
    a line added with PowerShell's ">>" is UTF-16 without one, among UTF-8.
    """
    if not data:
        return ""
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return data.decode("utf-16", errors="replace")
    if b"\x00" in data:                            # PowerShell's ">>": the letters are all there, between zeros
        data = data.replace(b"\x00", b"")          # (as the ground's own reader takes them out)
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return "\n".join(_line_of(line) for line in data.split(b"\n"))


def _line_of(line: bytes) -> str:
    try:
        return line.decode("utf-8-sig")
    except UnicodeDecodeError:
        return line.decode("cp1252", errors="replace")


def _as_date(day) -> datetime.date:
    """A date, from a date, a datetime, or '2026-10-04'."""
    if isinstance(day, datetime.datetime):
        return day.date()
    if isinstance(day, Date):
        return day
    found = _date_in(str(day))
    if found is None:
        raise ValueError(f"not a day the sky can be asked about: {day!r}")
    return found


# ────────────────────────────────────────────────────────────── the astronomy
#
# After Jean Meeus, "Astronomical Algorithms": the sun's longitude from its
# mean anomaly, the moon's from the largest terms of its series. Everything is
# taken at noon, universal time, on the day asked.

_MOON_TERMS = (
    # millionths of a degree, then the multiples of D, M, M', F in the sine
    (6288774, 0, 0, 1, 0), (1274027, 2, 0, -1, 0), (658314, 2, 0, 0, 0),
    (213618, 0, 0, 2, 0), (-185116, 0, 1, 0, 0), (-114332, 0, 0, 0, 2),
    (58793, 2, 0, -2, 0), (57066, 2, -1, -1, 0), (53322, 2, 0, 1, 0),
    (45758, 2, -1, 0, 0), (-40923, 0, 1, -1, 0), (-34720, 1, 0, 0, 0),
    (-30383, 0, 1, 1, 0), (15327, 2, 0, 0, -2), (-12528, 0, 0, 1, 2),
    (10980, 0, 0, 1, -2), (10675, 4, 0, -1, 0), (10034, 0, 0, 3, 0),
    (8548, 4, 0, -2, 0), (-7888, 2, 1, -1, 0), (-6766, 2, 1, 0, 0),
    (-5163, 1, 0, -1, 0), (4987, 1, 1, 0, 0), (4036, 2, -1, 1, 0),
    (3994, 2, 0, 2, 0), (3861, 4, 0, 0, 0), (3665, 2, 0, -3, 0),
)


def _centuries(day: datetime.date, hour: float = 12.0) -> float:
    """Julian centuries since noon on 1 January 2000."""
    julian_day = day.toordinal() + 1721424.5 + hour / 24.0
    return (julian_day - 2451545.0) / 36525.0


def _sun_longitude(t: float) -> float:
    """The sun's true longitude along the ecliptic, in degrees."""
    mean = 280.46646 + 36000.76983 * t + 0.0003032 * t * t
    anomaly = math.radians(357.52911 + 35999.05029 * t - 0.0001537 * t * t)
    centre = ((1.914602 - 0.004817 * t - 0.000014 * t * t) * math.sin(anomaly)
              + (0.019993 - 0.000101 * t) * math.sin(2 * anomaly)
              + 0.000289 * math.sin(3 * anomaly))
    return mean + centre


def _moon_longitude(t: float) -> float:
    """The moon's longitude along the ecliptic, in degrees."""
    mean = 218.3164477 + 481267.88123421 * t - 0.0015786 * t * t
    d = math.radians(297.8501921 + 445267.1114034 * t - 0.0018819 * t * t)    # elongation
    m = math.radians(357.5291092 + 35999.0502909 * t - 0.0001536 * t * t)     # sun's anomaly
    mm = math.radians(134.9633964 + 477198.8675055 * t + 0.0087414 * t * t)   # moon's anomaly
    f = math.radians(93.2720950 + 483202.0175233 * t - 0.0036539 * t * t)     # from its node
    flattening = 1.0 - 0.002516 * t - 0.0000074 * t * t
    total = 0.0
    for size, of_d, of_m, of_mm, of_f in _MOON_TERMS:
        term = size * math.sin(of_d * d + of_m * m + of_mm * mm + of_f * f)
        total += term * flattening ** abs(of_m)
    total += 3958 * math.sin(math.radians(119.75 + 131.849 * t))
    total += 1962 * math.sin(math.radians(mean) - f)
    total += 318 * math.sin(math.radians(53.09 + 479264.290 * t))
    return mean + total / 1e6


def _moon_phase(t: float) -> float:
    """How far round from the sun the moon stands: 0 new, 0.5 full."""
    apart = _moon_longitude(t) - _sun_longitude(t) + 0.00569     # the sun, as seen
    return (apart % 360.0) / 360.0


def moon(day) -> float:
    """The moon's phase at noon UT: 0 new · 0.25 first quarter · 0.5 full · 0.75 last quarter."""
    phase = round(_moon_phase(_centuries(_as_date(day))), 3)
    return 0.0 if phase >= 1.0 else phase


def daylength(latitude, day) -> float:
    """Hours from sunrise to sunset (the sun's upper edge, through the air's bending).

    Beyond the polar circles it is 0 in the long night and 24 in the long day.
    """
    latitude = _latitude(latitude)
    t = _centuries(_as_date(day))
    tilt = math.radians(23.4393 - 0.0130 * t)
    sun = math.radians(_sun_longitude(t) - 0.00569)
    declination = math.asin(math.sin(tilt) * math.sin(sun))
    phi = math.radians(max(-89.9, min(89.9, latitude)))
    horizon = math.radians(-0.833)
    cos_hour = ((math.sin(horizon) - math.sin(phi) * math.sin(declination))
                / (math.cos(phi) * math.cos(declination)))
    if cos_hour >= 1.0:
        return 0.0
    if cos_hour <= -1.0:
        return 24.0
    return round(2.0 * math.degrees(math.acos(cos_hour)) / 15.0, 2)


def season(latitude, day) -> str:
    """The season by calendar month, flipped south of the equator."""
    month = _as_date(day).month
    north = ("winter", "winter", "spring", "spring", "spring", "summer",
             "summer", "summer", "autumn", "autumn", "autumn", "winter")[month - 1]
    if _latitude(latitude) >= 0:
        return north
    return {"winter": "summer", "summer": "winter", "spring": "autumn", "autumn": "spring"}[north]


def _latitude(latitude) -> float:
    """A latitude as a number; anything unreadable is the garden's own 47° north."""
    try:
        latitude = float(latitude)
    except (TypeError, ValueError):
        return DEFAULT_PLACE["latitude"]
    return latitude if -90.0 <= latitude <= 90.0 else DEFAULT_PLACE["latitude"]


# ─────────────────────────────────────────────────────── the reckoned climate
#
# Four strands of weather run through the days: warmth, damp, veil (cloud) and
# air (wind). Each strand is a sum of waves. A wave is a smooth curve through
# heights set every so many days; the heights, and where the first one falls,
# are hashed from the weather seed, so a wave never repeats itself and no two
# gardens share one. The lengths share no common measure, so neither do the
# spells they make. Nothing is carried from one day to the next.
#
# As tuned (measured over 48 seeds, ten years each): 11.5 °C, 152 wet days,
# 710 mm of rain and 37 frost nights a year, nearly all of the frost between
# November and March, and about a week of snow. A wet day is followed
# by another two times in three, a dry day by a wet one once in five. Change a
# number below, then run foundations/sky_trial.py to see what climate it makes.

YEAR_MEAN = 11.5        # °C over the whole year
YEAR_SWING = 7.6        # °C either side of it
COLDEST_DAY = 15        # day of the year: 15 January
WARMEST_DAY = 205       # 24 July

#            (days between heights, weight)
WARMTH = ((1.7, 1.0), (3.1, 1.1), (5.9, 1.0), (11.3, 0.8), (23.7, 0.55), (61.0, 0.4), (173.0, 0.3), (701.0, 0.15))
DAMP = ((1.3, 1.0), (2.3, 1.1), (4.7, 1.0), (9.1, 0.7), (19.3, 0.45), (47.0, 0.25), (113.0, 0.15))
VEIL = ((1.9, 1.0), (5.3, 0.8), (14.9, 0.5))
AIR = ((1.1, 0.8), (2.7, 1.0), (7.3, 0.7), (29.0, 0.4))

RAIN_LINE = 0.22        # how damp the air must be before it rains (lower = more wet days)
RAIN_GIVES = 6.0        # how much a wet day gives (higher = more millimetres)
SODDEN_MM = 9.0         # how much lingering rain it takes to make the ground properly wet

_MASK = (1 << 64) - 1
_WAVE_SPREAD = 0.4976   # the spread of one wave of weight 1


def _stir(x: int) -> int:
    """Stir 64 bits thoroughly (the splitmix64 finisher)."""
    x = (x + 0x9E3779B97F4A7C15) & _MASK
    x = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & _MASK
    x = ((x ^ (x >> 27)) * 0x94D049BB133111EB) & _MASK
    return x ^ (x >> 31)


@lru_cache(maxsize=512)
def _strand(seed: int, name: str, which: int) -> int:
    """The key of one wave of one strand in one garden."""
    return _stir(_stir(seed & _MASK) ^ zlib.crc32(name.encode("ascii")) ^ (which << 40))


def _chance(key: int, n: int) -> float:
    """A number in 0..1 that depends on the key and on n, and on nothing else."""
    return _stir(key ^ (n & _MASK)) / 18446744073709551616.0


def _wave(key: int, t: float, length: float) -> float:
    """A smooth curve between -1 and 1 through hashed heights `length` days apart."""
    along = t / length + _chance(key, -1)            # the hashed phase
    knot = math.floor(along)
    part = along - knot
    before = 2.0 * _chance(key, knot) - 1.0
    after = 2.0 * _chance(key, knot + 1) - 1.0
    return before + (after - before) * part * part * (3.0 - 2.0 * part)


def _drift(seed: int, name: str, waves, t: float) -> float:
    """A strand of weather on day t: mean 0, spread about 1."""
    total = 0.0
    weights = 0.0
    for which, (length, weight) in enumerate(waves):
        total += weight * _wave(_strand(seed, name, which), t, length)
        weights += weight * weight
    return total / (_WAVE_SPREAD * math.sqrt(weights))


def _turn_of_year(day: datetime.date, south: bool = False) -> float:
    """Where the year stands: -1 on its coldest day, +1 on its warmest, easing between."""
    of_year = day.timetuple().tm_yday + (182.6 if south else 0.0)
    since_cold = (of_year - COLDEST_DAY) % 365.25
    warming = WARMEST_DAY - COLDEST_DAY
    if since_cold < warming:
        return -math.cos(math.pi * since_cold / warming)
    return math.cos(math.pi * (since_cold - warming) / (365.25 - warming))


def usual_warmth(day, south: bool = False) -> float:
    """The mean temperature the season would usually bring on that day, °C."""
    return YEAR_MEAN + YEAR_SWING * _turn_of_year(_as_date(day), south)


def _rain_cloud(rain: float) -> float:
    """The least cloud a day of that much rain can have."""
    return 0.6 + min(0.35, rain / 20.0)


@lru_cache(maxsize=None)
def _reckoned(seed: int, ordinal: int, south: bool) -> tuple:
    """The reckoned weather of one day: (tmin, tmax, rain, cloud, wind)."""
    turn = _turn_of_year(Date.fromordinal(ordinal), south)
    damp = _drift(seed, "damp", DAMP, ordinal)
    key = _strand(seed, "day", 0)
    dice = [_chance(key, ordinal * 4 + n) for n in range(4)]      # the day's own four throws

    # Rain, when the air is damp enough; summer asks for more and gives more at once.
    over = damp + 0.45 * (2.0 * dice[0] - 1.0) - (RAIN_LINE + 0.13 * turn)
    rain = 0.0
    if over > 0:
        burst = 0.25 - 0.75 * math.log(1.0 - 0.985 * dice[1])
        rain = min(70.0, 0.4 + RAIN_GIVES * (1.0 + 0.15 * turn) * over ** 1.15 * burst)

    # Cloud follows the damp; rain keeps its cloud.
    cloud = 0.56 - 0.10 * turn + 0.24 * damp + 0.12 * _drift(seed, "veil", VEIL, ordinal)
    cloud = max(0.02, min(1.0, cloud))
    if rain > 0:
        cloud = max(cloud, _rain_cloud(rain))

    # Warmth: the season, a spell of its own, and the lean the damp gives it
    # (wet winter days are mild, wet summer days are cool).
    spell = (3.5 - 0.5 * turn) * _drift(seed, "warmth", WARMTH, ordinal)
    lean = damp * (-0.15 - 1.45 * turn)
    mean = YEAR_MEAN + YEAR_SWING * turn + spell + lean + 2.4 * (dice[2] - 0.5)
    # Day and night stand further apart in summer and under a clear sky.
    apart = (5.4 + 2.9 * (turn + 1.0)) * (1.3 - 0.65 * cloud) + 0.8 * (dice[3] - 0.5)

    # Wind rises with the damp and in winter; the top of it is stretched into gales.
    wind = 2.7 - 0.45 * turn + 1.0 * damp + 1.0 * _drift(seed, "air", AIR, ordinal)
    if wind > 4.0:
        wind = 4.0 + (wind - 4.0) * 1.6
    wind = max(0.3, min(10.0, wind))

    return (_rounded(mean - apart / 2.0, 1), _rounded(mean + apart / 2.0, 1),
            round(rain, 1), round(cloud, 2), round(wind, 1))


def reckon(seed, day, south: bool = False) -> dict:
    """The reckoned weather of a day: tmin, tmax, rain, cloud, wind. No files are read."""
    tmin, tmax, rain, cloud, wind = _reckoned(int(seed), _as_date(day).toordinal(), bool(south))
    return {"tmin": tmin, "tmax": tmax, "rain": rain, "cloud": cloud, "wind": wind}


# ─────────────────────────────────────────────────────────── the gate's lines
#
# The keeper's words are folded to plain lower-case letters (gelée -> gelee)
# and looked up in these tables; a final s or x is forgiven (pluies, nuages).
# The tables are short on purpose (Ruling 11: the reader prefers silence to
# invention). Before adding a word, ask whether it could mean anything else in
# a line written about a garden. If it could, leave it out: a thought holding a
# word the tables do not know is simply left alone, and that is always safe.

RAIN_WORDS = {      # word -> the millimetres it suggests when no amount is given
    "rain": 5, "rainy": 5, "raining": 5, "rained": 5, "pluie": 5, "pluvieux": 5, "pluvieuse": 5,
    "plu": 5, "pleut": 5, "pleuvoir": 5, "precipitation": 5,
    "shower": 3, "averse": 3, "ondee": 3, "giboulee": 3,
    "drizzle": 1, "bruine": 1, "crachin": 1,
    "downpour": 18, "deluge": 18, "orage": 14, "orageux": 14, "thunderstorm": 14,
}
DRY_WORDS = {"dry", "sec", "seche"}
FROST_WORDS = {"frost", "frosty", "gel", "gele", "gelee", "givre", "froze", "frozen", "verglas"}
SNOW_WORDS = {"snow", "snowy", "snowed", "snowing", "neige", "neigeux", "neiger", "flocon"}
FOG_WORDS = {"fog", "foggy", "mist", "misty", "brouillard", "brume", "brumeux"}
SKY_WORDS = {       # word -> cloud, 0 clear .. 1 overcast
    "sun": 0.1, "sunny": 0.1, "sunshine": 0.1, "soleil": 0.1, "ensoleille": 0.1, "ensoleillee": 0.1,
    "clear": 0.05, "clair": 0.05, "claire": 0.05, "degage": 0.05, "degagee": 0.05,
    "blue": 0.1, "bleu": 0.1, "beau": 0.15, "belle": 0.15,
    "bright": 0.3, "eclaircie": 0.45,       # "bright" as `Sky.words` says it: 0.2 to 0.4
    "cloud": 0.7, "cloudy": 0.75, "nuage": 0.7, "nuageux": 0.75, "nuageuse": 0.75,
    "grey": 0.9, "gray": 0.9, "gris": 0.9, "grise": 0.9, "maussade": 0.9, "overcast": 0.95, "couvert": 0.95,
}
WIND_WORDS = {      # word -> Beaufort
    "wind": 4.5, "windy": 5.5, "vent": 4.5, "venteux": 5.5, "breeze": 2.5, "brise": 2.5, "breezy": 4.0,
    "gust": 6.0, "gusty": 6.0, "rafale": 6.0, "bourrasque": 6.5, "gale": 8.0, "tempete": 9.0,
}
FEEL_WORDS = {      # word -> degrees away from what the season usually brings
    "glacial": -7.0, "cold": -4.5, "froid": -4.5, "froide": -4.5, "chilly": -2.5,
    "frais": -2.0, "fraiche": -2.0, "mild": 2.0, "doux": 2.0, "douce": 2.0, "warm": 3.5,
    "chaud": 4.5, "chaude": 4.5, "hot": 5.5, "heatwave": 9.0, "canicule": 9.0,
}
LIGHT_WORDS = {"light", "leger", "legere", "faible", "fine", "petit", "petite", "peu", "little", "slight",
               "gentle", "quelque", "few", "bit"}
HEAVY_WORDS = {"heavy", "strong", "fort", "forte", "violent", "violente", "gros", "grosse", "beaucoup", "lot",
               "torrential", "battante"}
NO_WORDS = {"no", "not", "pas", "sans", "without", "aucun", "aucune", "ni", "nor", "jamais", "never", "ne"}
OR_WORDS = {"or", "ou"}                 # understood only after a no: "no frost or snow"
OF_WORDS = {"de", "d", "of"}            # "pas un flocon de neige": the no takes the flake and the snow
# The parts of a day. Rain, frost, snow or fog said of a part of the day happened that day;
# but "sec le matin" or "pas de gel cette nuit" says nothing of the whole day. ("Lever" is not
# among them: "au lever du soleil" is sunrise, and its "soleil" says nothing of the sky.)
DAY_PARTS = {"matin", "matinee", "aube", "nuit", "midi", "apres", "soir", "soiree", "ensuite",
             "morning", "afternoon", "evening", "night", "overnight", "dawn", "noon", "midday", "later"}
# Small words that change nothing a weather word means. A thought may hold these and still be heard.
SMALL_WORDS = set((
    "le la les l un une des de du d au aux a ce cet cette ces il y ai avait est etait fait faisait eu j on s "
    "tres assez toute toutes tous journee jour aujourd hui ciel temps meteo blanc blanche "
    "the an it its is was has had been there did do does very quite some of all at in this today day sky "
    "weather we i got").split())
# A word for another day, or for weather only forecast, feared or wished for: the rest of its
# sentence is left alone ("demain : pluie", "45 mm depuis lundi", "comme le 15 octobre, 12°").
OTHER_DAY_WORDS = set((
    "demain tomorrow hier yesterday avant veille lendemain prochain prochaine dernier derniere next last "
    "prevu prevue prevus prevision annonce annoncee attendu attendue forecast forecasted expected "
    "risque risk faudrait should will would sera fera va semaine mois annee week month year depuis since "
    "cumul until jusqu lundi mardi mercredi jeudi vendredi samedi dimanche monday tuesday wednesday "
    "thursday friday saturday sunday janvier janv fevrier fevr fev mars avril avr mai juin juillet juil "
    "aout septembre sept octobre oct novembre nov decembre dec january jan february feb march apr april "
    "may june jun july jul august aug september sep october november december").split())
# Words that may head their line before a colon, as its title: they name the day itself (a feast) or
# the gauge they read. What follows such a title is read as usual ("Noël : soleil, -2 à 5",
# "Pluviomètre : 6 mm"). Any other word they head a line with may be naming a thing in the garden,
# and leaves the rest of its sentence alone ("fleurs : gris, rose"). Away from a colon, these words
# are not known at all: "neige à Noël ?" may be a wish.
TITLE_WORDS = set((
    "noel toussaint paques pentecote ascension assomption epiphanie chandeleur reveillon armistice "
    "nouvel saint sylvestre christmas easter eve pluviometre thermometre thermometer releve").split())

# The words that go with a number, and only with one:
LOW_LABELS = {"min", "mini", "minimum", "tmin"}         # "min 3", "tmin: 3"
HIGH_LABELS = {"max", "maxi", "maximum", "tmax"}        # "max 12"
FORCE_WORDS = {"force", "beaufort", "bft"}              # "force 3", "force 3-4"
MINUS_WORDS = {"moins", "minus"}                        # "moins 2°" at the head of a thought (not "au moins 12")
BETWEEN_WORDS = {"entre", "between"}                    # "entre 9 et 15°"
AND_WORDS = {"et", "and"}
TO_WORDS = {"a", "to"}                                  # "9 à 15°", "9 to 15°"
DEGREE_WORDS = {"degre", "degres", "degree", "degrees", "deg"}
RAIN_UNITS = {"mm", "millimetre", "millimetres", "millimeter", "millimeters"}
SNOW_UNITS = {"cm"}                                     # snow only, and a centimetre of it is taken as a millimetre of water
SPEED_UNITS = {"kmh": 1.0, "kph": 1.0, "mph": 1.609, "ms": 3.6, "noeuds": 1.852, "knots": 1.852}   # -> km/h
BEAUFORT_UNITS = {"bft", "bf", "beaufort"}

WEATHER_WORDS = (set(RAIN_WORDS) | DRY_WORDS | FROST_WORDS | SNOW_WORDS | FOG_WORDS | set(SKY_WORDS)
                 | set(WIND_WORDS) | set(FEEL_WORDS))
_KNOWN = (WEATHER_WORDS | LIGHT_WORDS | HEAVY_WORDS | NO_WORDS | OR_WORDS | OF_WORDS | DAY_PARTS | SMALL_WORDS
          | LOW_LABELS | HIGH_LABELS | FORCE_WORDS | TO_WORDS)
_ALL_WORDS = (_KNOWN | OTHER_DAY_WORDS | MINUS_WORDS | BETWEEN_WORDS | AND_WORDS | DEGREE_WORDS | RAIN_UNITS
              | SNOW_UNITS | set(SPEED_UNITS) | BEAUFORT_UNITS | TITLE_WORDS)

MONTHS = {          # a month as the keeper may write it (folded) -> its number, for the date at the head of a line
    "janvier": 1, "janv": 1, "jan": 1, "january": 1, "fevrier": 2, "fevr": 2, "fev": 2, "feb": 2, "february": 2,
    "mars": 3, "mar": 3, "march": 3, "avril": 4, "avr": 4, "apr": 4, "april": 4, "mai": 5, "may": 5,
    "juin": 6, "jun": 6, "june": 6, "juillet": 7, "juil": 7, "jul": 7, "july": 7,
    "aout": 8, "aug": 8, "august": 8, "septembre": 9, "sept": 9, "sep": 9, "september": 9,
    "octobre": 10, "oct": 10, "october": 10, "novembre": 11, "nov": 11, "november": 11,
    "decembre": 12, "dec": 12, "december": 12,
}
WEEKDAYS = ("lundi mardi mercredi jeudi vendredi samedi dimanche lun mar mer jeu ven sam dim "
            "monday tuesday wednesday thursday friday saturday sunday mon tue tues wed thu thur thurs fri sat sun")

_ISO = r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})"      # a date, year first
# A date as the gate accepts it, in nine groups: year first (2026-10-04), day first with the whole
# year last (04/10/2026), or the day, the month in words, the year (4 octobre 2026, 1er novembre 2026):
_WRITTEN_DATE = (rf"(?:{_ISO}|(\d{{1,2}})[-/.](\d{{1,2}})[-/.](\d{{4}})(?!\d)"
                 r"|(\d{1,2})(?:er|e|st|nd|rd|th)?\s+([^\W\d_]{3,9})\.?,?\s+(\d{4})(?!\d))")
# The date, after a bullet, a weekday or "le" if there is one, and perhaps "to 2026-10-08":
_GATE_LINE = re.compile(
    rf"^\W{{0,4}}(?:(?:le|du|on|from|{WEEKDAYS.replace(' ', '|')})\b[.,]?\s+){{0,3}}{_WRITTEN_DATE}"
    rf"(?:\s*(?:to|until|au|a|à|-|–|—|->|→|\.\.+)\s*(?:le\s+)?{_WRITTEN_DATE})?", re.IGNORECASE)

# How a folded line is cut into thoughts: at these marks (a comma or a full stop only when it is
# not inside a number like 6,5), and at these small words ...
_THOUGHT_WORDS = re.compile(r"\b(?:et|and|mais|but|puis|then|avec|with)\b")
# ... but not at the "et" of "entre 9 et 15°", nor at the colon of "min: 3".
_BETWEEN_OPEN = re.compile(r"\b(?:entre|between)\s+-?[0-9]+(?:[.,][0-9]+)?\s*(?:°\s*c?|deg[a-z]*)?\s*$")
_LABEL_OPEN = re.compile(r"\b(?:tmin|tmax|min|max|mini|maxi|minimum|maximum|force|beaufort)\s*$")
_TOKEN = re.compile(r"[0-9]+(?:[.,][0-9]+)?|[a-z]+|\S")
_UNITS_JOINED = re.compile(r"(?<![a-z])(?:km\s*/\s*h|m\s*/\s*s)(?![a-z])")    # km/h and m/s, as one word each (same length)
_ODD_MARKS = set("%:@$€£§<>^~\\" + chr(0x2026))      # marks that make a number doubtful (the last is "…", a line cut short)
_FOLDED = {0x2212: "-", 0x2013: "-", 0x2014: "-", 0x2010: "-", 0x2011: "-", 0x2019: "'", 0x2018: "'",
           0xA0: " ", 0x202F: " ", 0x2009: " ", 0xBA: "°", 0x2DA: "°", 0x153: "oe", 0xE6: "ae"}


@dataclass(frozen=True)
class Thought:
    """One thought of the keeper's line: their own words, and what the reader made of them.

    `said` holds what it says, as (key, value) pairs; it is empty when the
    thought was left alone, and then `why` says why, in plain words. A thought
    whose words were all understood but say nothing of the sky has neither;
    a title before a colon ("Noël :") says only ("title", True).
    `part` holds the parts of the day it names ("matin", "soir"), if any.
    """

    words: str
    said: tuple = ()
    why: str = ""
    part: tuple = ()


@dataclass
class _Piece:
    """One token of a folded thought: a number, a word, or a mark."""

    kind: str                  # "num" "word" "deg" "dash" "slash" "odd"
    text: str
    start: int                 # where it lies in the folded thought
    end: int
    spaced: bool               # a space (or the start of the thought) just before it
    value: float = 0.0         # a number's value, with its sign
    signed: bool = False       # a number written with a minus
    degree: bool = False       # a number written with a degree mark
    used: bool = False         # taken up by a reading


def _fold(text: str) -> str:
    """Lower-case, accents off, the odd minus signs, degree signs and spaces made plain."""
    return _folded(text)[0]


def _folded(text: str) -> tuple:
    """The text folded, and for each folded character the place in `text` it came from."""
    out, where = [], []
    for at, ch in enumerate(text):
        plain = "".join(c for c in unicodedata.normalize("NFD", ch.lower()) if not unicodedata.combining(c))
        plain = plain.translate(_FOLDED)
        out.append(plain)
        where.extend([at] * len(plain))
    return "".join(out), where


def _number(text: str):
    try:
        return float(text.replace(",", "."))
    except ValueError:
        return None


def _beaufort(kmh: float) -> float:
    """A wind speed in km/h on the Beaufort scale."""
    return round(min(10.0, (max(0.0, kmh) / 3.01) ** (2.0 / 3.0)), 1)


def _known(token: str) -> str:
    """A word as the tables know it: itself, or itself without a final s or x."""
    if token in _ALL_WORDS or len(token) < 5 or token[-1] not in "sx":     # "plus" is not "plu"
        return token
    return token[:-1] if token[:-1] in _ALL_WORDS else token


def _is_temperature(value) -> bool:
    return value is not None and -40.0 <= value <= 50.0


def _thought_spans(folded: str) -> list:
    """Where each thought of a folded line begins and ends: [(start, end, begins a sentence), ...].

    A sentence ends at . ; ! ? and at the end of a line; a thought also ends
    at a comma, a colon, a bracket, a slash or a free-standing dash between
    words, the almanac's "·", and "et", "mais", "puis", "and", "but", "then".
    """
    cuts = []                                      # (start, end, ends a sentence)
    for match in _THOUGHT_WORDS.finditer(folded):
        if match.group() in AND_WORDS and _BETWEEN_OPEN.search(folded, 0, match.start()):
            continue                               # the "et" of "entre 9 et 15°"
        cuts.append((match.start(), match.end(), False))
    for at, ch in enumerate(folded):
        if ch in ";!?\n\r":
            cuts.append((at, at + 1, True))
        elif ch in ".,":
            if not _between_digits(folded, at):
                cuts.append((at, at + 1, ch == "."))
        elif ch in "()[]{}|+" or ch in (chr(0xB7), chr(0x2022)):         # and the almanac's "·", a bullet "•"
            cuts.append((at, at + 1, False))
        elif ch == ":":
            if not (_between_digits(folded, at)
                    or (_LABEL_OPEN.search(folded, 0, at) and re.match(r"\s*-?[0-9]", folded[at + 1:]))):
                cuts.append((at, at + 1, False))
        elif ch == "/":
            if not _numbers_beside(folded, at):
                cuts.append((at, at + 1, False))
        elif ch == "-":
            free = 0 < at < len(folded) - 1 and folded[at - 1].isspace() and folded[at + 1].isspace()
            if free and not _numbers_beside(folded, at):
                cuts.append((at, at + 1, False))
    spans, begins, new = [], 0, True
    for start, end, ends_sentence in sorted(cuts):
        if start >= begins:
            spans.append((begins, start, new))
            begins, new = end, ends_sentence
        else:
            new = new or ends_sentence
    spans.append((begins, len(folded), new))
    return spans


def _between_digits(text: str, at: int) -> bool:
    return 0 < at < len(text) - 1 and text[at - 1] in "0123456789" and text[at + 1] in "0123456789"


def _numbers_beside(text: str, at: int) -> bool:
    """Does a mark stand between two numbers ("-1 / 12", "9 - 15")?"""
    left, right = text[:at].rstrip(), text[at + 1:].lstrip()
    return bool(left) and bool(right) and left[-1] in "0123456789°" and right[0] in "0123456789-"


def _pieces(thought: str) -> list:
    """The tokens of one folded thought, with each minus sign and degree mark joined to its number."""
    raw = []
    for match in _TOKEN.finditer(thought):
        text, at = match.group(), match.start()
        spaced = at == 0 or thought[at - 1].isspace()
        if text[0] in "0123456789":
            kind = "num"
        elif "a" <= text[0] <= "z":
            kind = "word"
        elif text == ":" and raw and raw[-1].kind == "word" and raw[-1].text in LOW_LABELS | HIGH_LABELS | FORCE_WORDS:
            continue                               # "min: 3"
        elif text in "°-/":
            kind = {"°": "deg", "-": "dash", "/": "slash"}[text]
        elif text.isalnum() or text in _ODD_MARKS:
            kind = "odd"                           # a letter it cannot read, a ², a %, a line cut short
        else:
            continue                               # quotes, apostrophes, stars, pictures: they say nothing
        piece = _Piece(kind, text, at, match.end(), spaced)
        if kind == "word":
            if text in DEGREE_WORDS:
                piece.kind = "deg"
            elif text == "c" and raw and raw[-1].kind == "deg" and not spaced:
                continue                           # 12°C
            elif text == "n" and thought[match.end():match.end() + 1] == "'":
                piece.text = "ne"                  # n'a, n'y: the French no
            elif (text == "t" and thought[at - 1:at] == "'" and raw and raw[-1].kind == "word"
                  and raw[-1].text.endswith("n")):
                raw[-1].text, piece.text = raw[-1].text[:-1], "not"      # didn't, isn't
        raw.append(piece)
    pieces, at = [], 0
    while at < len(raw):
        piece = raw[at]
        if (piece.kind == "dash" and at + 1 < len(raw) and raw[at + 1].kind == "num" and not raw[at + 1].spaced
                and (at == 0 or piece.spaced or raw[at - 1].kind not in ("num", "deg"))):
            number = raw[at + 1]                   # a minus: "-3", "à -5", "-5 -1" (but not the dash of "9-15")
            number.text, number.start, number.spaced, number.signed = "-" + number.text, piece.start, piece.spaced, True
            piece, at = number, at + 1
        if piece.kind == "num":
            piece.value = _number(piece.text)
            if at + 1 < len(raw) and raw[at + 1].kind == "deg":
                piece.degree, piece.end, at = True, raw[at + 1].end, at + 1
        pieces.append(piece)
        at += 1
    return pieces


def _word(piece) -> str:
    return _known(piece.text) if piece is not None and piece.kind == "word" else ""


def _a_date(pieces: list):
    """The pieces of a date written inside a thought (2026-10-15, 12/10), or None."""
    for at in range(len(pieces) - 2):
        first, mark, second = pieces[at:at + 3]
        if not (first.kind == "num" and mark.kind in ("dash", "slash") and second.kind == "num"
                and not mark.spaced and not second.spaced and not first.degree):
            continue
        more = pieces[at + 3:at + 5]
        if len(more) == 2 and more[0].kind in ("dash", "slash") and more[1].kind == "num" and not more[0].spaced:
            return pieces[at:at + 5]               # three numbers joined: a date
        if mark.kind == "slash" and not first.signed and not second.degree:
            return pieces[at:at + 3]               # "12/10": a day and a month (a pair of degrees has its °)
    return None


def _run(pieces: list, at: int) -> list:
    """The number at `at`, or the two numbers of a range from it ("10 à 20", "3-4", "-1 / 12")."""
    if (at + 2 < len(pieces) and pieces[at + 2].kind == "num"
            and (pieces[at + 1].kind in ("dash", "slash") or _word(pieces[at + 1]) in TO_WORDS)):
        return [pieces[at], pieces[at + 2]]
    return [pieces[at]]


def _take(pieces: list, first: int, count: int) -> None:
    for piece in pieces[first:first + count]:
        piece.used = True


def _read_numbers(pieces: list, said: dict):
    """Take every number of a thought that can be read for sure into `said`.

    Returns None, or the first trouble met: (what, [pieces]) for a number
    that could be something else, or that no sky could have.
    """
    trouble = None
    alone = _bare_pair(pieces)                     # "9 à 15" and nothing more: the low and the high
    at = 0
    while at < len(pieces):
        piece, word = pieces[at], _word(pieces[at])
        after = pieces[at + 1] if at + 1 < len(pieces) else None
        if word in MINUS_WORDS and after is not None and after.kind == "num" and not after.signed and (
                at == 0 or _word(pieces[at - 1]) in ("fait", "faisait")):
            piece.used, after.value, after.signed = True, -after.value, True       # "moins 2°", "il fait moins 3"
        elif word in LOW_LABELS | HIGH_LABELS and after is not None and after.kind == "num" and (
                at == 0 or pieces[at - 1].kind != "num" or pieces[at - 1].used):    # not the "min" of "20 min"
            if _is_temperature(after.value):
                said.setdefault("low" if word in LOW_LABELS else "high", []).append(after.value)
            else:
                trouble = trouble or ("impossible", [after])
            _take(pieces, at, 2)
        elif word in FORCE_WORDS and after is not None and after.kind == "num":
            numbers = _run(pieces, at + 1)
            force = sum(n.value for n in numbers) / len(numbers)
            if 0 <= force <= 12 and not any(n.signed or n.degree for n in numbers):
                said.setdefault("wind", []).append(min(10.0, force))
            else:
                trouble = trouble or ("impossible", numbers)
            _take(pieces, at, 2 * len(numbers))
        elif (word in BETWEEN_WORDS and at + 3 < len(pieces) and pieces[at + 1].kind == "num"
              and _word(pieces[at + 2]) in AND_WORDS and pieces[at + 3].kind == "num"):
            found = _read_pair(pieces[at + 1], pieces[at + 3], said, alone)
            trouble = trouble or found
            _take(pieces, at, 4)
        elif piece.kind == "num" and not piece.used:
            found = _read_number(pieces, at, said, alone)
            trouble = trouble or found
        at += 1
    return trouble


BARE_PAIR_WARMEST = 45.0   # °C: two plain numbers above this are not a day's low and high
BARE_PAIR_WIDEST = 25.0    # nor two further apart than this


def _bare_pair(pieces: list) -> bool:
    """Is the whole thought two plain numbers, the lower first, that can only be the day's low and high?

    "9 à 15", "0 to 4", "10-16", "entre 9 et 15": the two numbers, the word or
    dash between them, and nothing else. No ° and no minus (those pairs are read
    in any case), the lower first, no warmer than BARE_PAIR_WARMEST and no
    further apart than BARE_PAIR_WIDEST. With no minus, such a pair can never
    make a frost. One word more ("vent 3 à 4", "de 9 à 15", "9 à 15 cette
    nuit") and it is no longer bare: it may be counting, or hours, or a part
    of the day.
    """
    if len(pieces) == 3 and (pieces[1].kind == "dash" or _word(pieces[1]) in TO_WORDS):
        low, high = pieces[0], pieces[2]
    elif len(pieces) == 4 and _word(pieces[0]) in BETWEEN_WORDS and _word(pieces[2]) in AND_WORDS:
        low, high = pieces[1], pieces[3]
    else:
        return False
    return (low.kind == high.kind == "num" and not any(n.signed or n.degree for n in (low, high))
            and _finite(low.value) and _finite(high.value)
            and low.value < high.value <= BARE_PAIR_WARMEST and high.value - low.value <= BARE_PAIR_WIDEST)


def _read_number(pieces: list, at: int, said: dict, alone: bool = False):
    """A number (or a range of two) and the unit after it, if any. Returns a trouble, or None.

    `alone` says the thought is a bare pair (see `_bare_pair`).
    """
    numbers = _run(pieces, at)
    spans = 2 * len(numbers) - 1
    unit_piece = pieces[at + spans] if at + spans < len(pieces) else None
    unit = _word(unit_piece)
    values = [n.value for n in numbers]
    if not all(_finite(value) for value in values):
        _take(pieces, at, spans)
        return "impossible", numbers
    mean = sum(values) / len(values)
    plain = not any(n.signed or n.degree for n in numbers)
    if unit in RAIN_UNITS | SNOW_UNITS | set(SPEED_UNITS) | BEAUFORT_UNITS:
        _take(pieces, at, spans + 1)
        if not plain:
            return "impossible", numbers
        if unit in RAIN_UNITS and mean <= 300:
            said.setdefault("mm", []).append(round(mean, 1))
        elif unit in SNOW_UNITS and mean <= 300:
            said.setdefault("cm", []).append(round(mean, 1))
            said.setdefault("cm_written", [numbers[0], unit_piece])        # to quote, if no snow stands beside it
        elif unit in SPEED_UNITS and mean * SPEED_UNITS[unit] <= 300:
            said.setdefault("wind", []).append(_beaufort(mean * SPEED_UNITS[unit]))
        elif unit in BEAUFORT_UNITS and mean <= 12:
            said.setdefault("wind", []).append(min(10.0, mean))
        else:
            return "impossible", numbers
        return None
    if len(numbers) == 2:
        _take(pieces, at, 3)
        return _read_pair(numbers[0], numbers[1], said, alone)
    nxt = pieces[at + 1] if at + 1 < len(pieces) else None
    if pieces[at].signed and nxt is not None and nxt.kind == "num" and nxt.signed:
        _take(pieces, at, 2)                       # "-5 -1": two frosts side by side
        return _read_pair(pieces[at], nxt, said)
    _take(pieces, at, 1)
    if pieces[at].degree or pieces[at].signed:     # "12°", "-3": surely a temperature
        if not _is_temperature(pieces[at].value):
            return "impossible", numbers
        said.setdefault("seen", []).append(pieces[at].value)
        return None
    return "number", numbers                       # "pluie 6", "2 fois", "9h": counting something else, perhaps


def _read_pair(first, second, said: dict, alone: bool = False):
    """Two numbers written as a pair. They are temperatures if one has its ° or a minus, or if they stand alone.

    `alone`: the pair is the whole thought, and could only be a day's low and high (see `_bare_pair`).
    """
    if not (first.degree or second.degree or first.signed or second.signed or alone):
        return "pair", [first, second]             # "2 à 3 averses", "vent 3 à 4": degrees, or a count?
    low, high = sorted((first.value, second.value))
    if not (_is_temperature(low) and _is_temperature(high)):
        return "impossible", [first, second]
    said.setdefault("pairs", []).append((low, high))
    return None


def _read_words(pieces: list, said: dict):
    """What the words of a thought say, once its numbers are taken. Returns a trouble, or None."""
    words = [piece for piece in pieces if piece.kind == "word" and not piece.used]
    kinds = [_known(piece.text) for piece in words]
    denied, joined = set(), set()
    for at, kind in enumerate(kinds):
        if kind not in NO_WORDS:
            continue
        target = next((n for n in range(at + 1, len(kinds)) if kinds[n] in WEATHER_WORDS), None)
        if target is None:
            if "ne" in kinds[:at]:
                continue                           # the pas that closes "il ne pleut pas"
            return "no", [words[at]]
        denied.add(target)
        while True:                                # "no frost or snow", "pas un flocon de neige"
            step = target + 1
            if step < len(kinds) and kinds[step] in OR_WORDS:
                joined.add(step)
                step += 1
            elif not (step < len(kinds) and kinds[step] in OF_WORDS):
                break
            while step < len(kinds) and kinds[step] in OF_WORDS | {"la", "le", "les", "l", "du", "des", "the", "a"}:
                step += 1
            if step < len(kinds) and kinds[step] in WEATHER_WORDS:
                denied.add(step)
                target = step
            else:
                break
    stray = [words[at] for at, kind in enumerate(kinds) if kind in OR_WORDS and at not in joined]
    if stray:
        return "or", stray                         # "pluie ou neige": which one fell?
    skies, feels = [], []
    for at, kind in enumerate(kinds):
        if kind not in WEATHER_WORDS:
            continue
        near = set(kinds[max(0, at - 2):at + 3])
        weight = 0.3 if near & LIGHT_WORDS else 3.2 if near & HEAVY_WORDS else 1.0
        no = at in denied
        if kind in RAIN_WORDS:
            if no:
                said["dry"] = True
            else:
                said["raining"] = max(said.get("raining", 0.0), round(RAIN_WORDS[kind] * weight, 1))
        elif kind in DRY_WORDS:
            if not no:
                said["dry"] = True
        elif kind in FROST_WORDS or kind in SNOW_WORDS:
            key = "frost" if kind in FROST_WORDS else "snow"
            said[key] = said.get(key, False) or not no
        elif kind in FOG_WORDS:
            if not no:
                said["fog"] = True
                skies.append(0.85)
        elif kind in SKY_WORDS:
            cloud = SKY_WORDS[kind]
            skies.append(cloud if not no else (0.85 if cloud < 0.5 else 0.1))       # "pas de soleil", "not a cloud"
        elif kind in WIND_WORDS:
            if no:
                said["calm"] = True
            else:
                force = WIND_WORDS[kind]
                if weight != 1.0 and force < 8.0:
                    force = 2.0 if weight < 1.0 else 7.0                           # "vent léger", "strong wind"
                said["wind_word"] = max(said.get("wind_word", 0.0), force)
        elif kind in FEEL_WORDS and not no:
            feels.append(FEEL_WORDS[kind])
    if skies:
        said["skies"] = skies
    if feels:
        said["feel"] = feels
    return None


def _hear_thought(thought: str) -> tuple:
    """What one folded thought says: (said, trouble, parts of the day).

    `trouble` is None when the thought is heard, else (what, [pieces]):
    "elsewhen" or "date" (it speaks of another day), "unknown" (a word the
    tables do not know), "number" or "pair" (a number that may count
    something else), "impossible", "no", "or", "cm", "odd".
    """
    pieces = _pieces(thought)
    for piece in pieces:
        if _word(piece) in OTHER_DAY_WORDS:
            return {}, ("elsewhen", [piece]), ()
    date = _a_date(pieces)
    if date:
        return {}, ("date", date), ()
    said: dict = {}
    trouble = _read_numbers(pieces, said)
    left = [piece for piece in pieces if not piece.used]
    unknown = [piece for piece in left if piece.kind == "word" and _known(piece.text) not in _KNOWN]
    if unknown:
        return {}, ("unknown", unknown), ()
    if trouble:
        return {}, trouble, ()
    odd = [piece for at, piece in enumerate(pieces) if not piece.used and piece.kind != "word"
           and not (piece.kind == "dash" and _hyphen(pieces, at))]
    if odd:
        return {}, ("odd", odd), ()
    trouble = _read_words(pieces, said)
    if trouble:
        return {}, trouble, ()
    written = said.pop("cm_written", None)
    if written and said.get("snow") is not True:
        return {}, ("cm", written), ()
    part = tuple(sorted({_known(piece.text) for piece in left if piece.kind == "word"} & DAY_PARTS))
    for low, high in said.pop("pairs", ()):
        if part:                                   # "-5 à -1 cette nuit": what the night saw, not the whole day
            said.setdefault("seen", []).extend((low, high))
        else:
            said.setdefault("low", []).append(low)
            said.setdefault("high", []).append(high)
    return {key: tuple(value) if isinstance(value, list) else value for key, value in said.items()}, None, part


def _hyphen(pieces: list, at: int) -> bool:
    """Is the dash at `at` a hyphen between two words ("après-midi"), or a bullet at the head or foot of a thought?"""
    if at == len(pieces) - 1 or (at == 0 and pieces[1].kind == "word"):
        return True
    return (0 < at and pieces[at - 1].kind == "word" and pieces[at + 1].kind == "word"
            and not pieces[at].spaced and not pieces[at + 1].spaced)


_WHY = {
    "elsewhen": '{0} speaks of another day, or of weather only forecast; the rest of the sentence goes with it',
    "date": '{0} is a date, so another day; the rest of the sentence goes with it',
    "after": 'it follows {0} in the same sentence, so it may speak of that other day too',
    "heading": 'it follows {0}, and may be speaking of that rather than of the sky '
               '(after a full stop it would be read on its own)',
    "unknown": 'the reader does not know {0}',
    "number": '{0} has no unit or ° to say what it counts (write 6 mm for rain, 12° for warmth)',
    "pair": '{0} could be degrees or a count: write the ° if they are degrees ("9 à 15°")',
    "impossible": '{0} is not a number a day\'s sky can have',
    "no": '{0} does not say which weather is not',
    "or": '{0}: one or the other, but the reader cannot tell which',
    "cm": '{0}: centimetres are taken as snow only beside the word snow (neige) in the same thought',
    "odd": '{0} leaves the numbers in doubt',
}


def _quoted(things: list) -> str:
    """'"a", "b" and "c"'."""
    things = [f'"{thing}"' for thing in dict.fromkeys(things)]
    return things[0] if len(things) == 1 else ", ".join(things[:-1]) + " and " + things[-1]


def _why(what: str, theirs: list) -> str:
    """Why a thought was left alone, in plain words, quoting the keeper's own words."""
    if what == "unknown":
        return _WHY[what].format(("the word " if len(set(theirs)) == 1 else "the words ") + _quoted(theirs))
    return _WHY[what].format(_quoted(theirs))


@lru_cache(maxsize=4096)
def _hear(text: str) -> tuple:
    """A line of the keeper's (or a day's whole remark) as its thoughts. Never raises.

    Each thought comes back with their own words for it, and what it says or
    why it was left alone. A thought that names another day leaves alone the
    rest of its sentence (up to the next . ; ! or ?), and so does a thought
    it cannot read that ends in a colon: "fleurs : gris, rose" may be
    speaking of the flowers, not of the sky. A title before a colon that
    names the day or the gauge ("Noël :", "Pluviomètre :") leaves nothing
    alone; its thought says `title`, and nothing of the sky.
    """
    try:
        text = str(text)[:4000]
        folded, where = _folded(text)
        folded = _UNITS_JOINED.sub(lambda unit: ("kmh" if unit.group()[0] == "k" else "ms").ljust(len(unit.group())),
                                   folded)             # km/h and m/s as one word each, before the "/" can cut them
        thoughts, carried = [], None               # (why, their words) that the rest of the sentence goes with
        for begins, ends, new_sentence in _thought_spans(folded):
            if new_sentence:
                carried = None
            if not any(ch.isalnum() for ch in folded[begins:ends]):
                continue                           # only marks and pictures
            own = _own(text, where, begins, ends)
            if carried:
                thoughts.append(Thought(own, why=_why(*carried)))
                continue
            if folded[ends:ends + 1] == ":" and _a_title(folded[begins:ends]):
                thoughts.append(Thought(own, (("title", True),)))
                continue
            said, trouble, part = _hear_thought(folded[begins:ends])
            if trouble is None:
                thoughts.append(Thought(own, tuple(sorted(said.items())), "", part))
                continue
            what, pieces = trouble
            if what in ("date", "pair", "number", "impossible", "cm"):     # one stretch of their words: "9 à 15", "4 cm"
                theirs = [_own(text, where, begins + pieces[0].start, begins + pieces[-1].end)]
            else:
                theirs = [_own(text, where, begins + piece.start, begins + piece.end) for piece in pieces]
            if what in ("elsewhen", "date"):
                carried = "after", [theirs[0]]
            elif folded[ends:ends + 1] == ":":
                carried = "heading", [own + ":"]
            thoughts.append(Thought(own, why=_why(what, theirs)))
        return tuple(thoughts)
    except Exception:
        return ()


def _a_title(thought: str) -> bool:
    """Is this folded thought a title naming the day or the gauge: "Noël", "le jour de Noël", "Pluviomètre"?

    One of the TITLE_WORDS, with nothing else but small words, and no number.
    """
    words = [_known(word) for word in re.findall(r"[a-z]+", thought)]
    return (not re.search(r"[0-9]", thought) and any(word in TITLE_WORDS for word in words)
            and all(word in TITLE_WORDS or word in SMALL_WORDS for word in words))


def _own(text: str, where: list, begins: int, ends: int) -> str:
    """The keeper's own words for the folded span begins..ends, without the spaces round them."""
    inside = [at for at in range(begins, min(ends, len(where))) if not text[where[at]].isspace()]
    if not inside:
        return ""
    return text[where[inside[0]]:where[inside[-1]] + 1]


def _together(thoughts) -> tuple:
    """What a day's thoughts say all together: (said, doubts, notes).

    The thoughts may come from one line or from several, in any order: they
    are heard the same way. Where they disagree about the whole day (rain and
    dry, frost and no frost), that thing is left as it was, and `doubts` says so.
    `notes` says, for the keeper, what was drawn from their words as a whole
    rather than from any one thought of them (a clear day is a dry one).
    """
    heard = [(dict(thought.said), thought.part) for thought in thoughts if thought.said]
    said: dict = {}
    doubts: list = []
    notes: list = []

    amounts = [(mm, part) for one, part in heard for mm in one.get("mm", ()) + one.get("cm", ())]
    if amounts:
        parts = [set(part) for _, part in amounts]
        each_its_own = all(parts) and all(a.isdisjoint(b) for n, a in enumerate(parts) for b in parts[n + 1:])
        total = sum(mm for mm, _ in amounts) if each_its_own else max(mm for mm, _ in amounts)
        said["rain"] = round(min(300.0, total), 1)      # "4 mm le matin, 6 mm le soir" is 10; else the largest stands
    raining = max((one["raining"] for one, _ in heard if "raining" in one), default=None)
    dry = any(one.get("dry") and not part for one, part in heard)
    if "rain" not in said:
        if raining is not None and dry:
            doubts.append("rain and dry are both said of the whole day, so its rain is left as it was")
            raining = None
        elif dry:
            said["rain"] = 0.0
    if raining is not None:
        said["raining"] = raining

    for key, name in (("frost", "frost"), ("snow", "snow")):
        yes = any(one.get(key) is True for one, _ in heard)
        no = any(one.get(key) is False and not part for one, part in heard)
        if yes and no:
            doubts.append(f"{name} and no {name} are both said of the whole day, so that is left as it was")
        elif yes or no:
            said[key] = yes
    if any(one.get("fog") for one, _ in heard):
        said["fog"] = True

    skies = [cloud for one, _ in heard for cloud in one.get("skies", ())]
    if skies:
        said["cloud"] = round(sum(skies) / len(skies), 2)
        if _clear_and_dry(thoughts, heard, said):
            said["rain"] = 0.0
            notes.append("they call the whole day clear, and name no rain, shower or snow, so the day is dry")
    measured = [force for one, _ in heard for force in one.get("wind", ())]
    worded = [one["wind_word"] for one, _ in heard if "wind_word" in one]
    if measured or worded:
        said["wind"] = max(measured or worded)          # a measure outweighs a word
    elif any(one.get("calm") for one, _ in heard):
        said["wind"] = 0.5
    feels = [feel for one, _ in heard for feel in one.get("feel", ())]
    if feels and (min(feels) > 0 or max(feels) < 0):
        said["feel"] = max(feels, key=abs)
    elif feels:
        doubts.append("both warm and cold are said, so neither is taken")

    lows = [low for one, _ in heard for low in one.get("low", ())]
    highs = [high for one, _ in heard for high in one.get("high", ())]
    if lows:
        said["tmin"] = min(lows)
    if highs:
        said["tmax"] = max(highs)
    if lows and highs and said["tmin"] > said["tmax"]:
        doubts.append("the low they wrote is above the high they wrote, so neither is taken")
        del said["tmin"], said["tmax"]
    seen = sorted({value for one, _ in heard for value in one.get("seen", ())})
    if seen:
        said["seen"] = tuple(seen)
        if ("tmin" in said and seen[0] < said["tmin"]) or ("tmax" in said and seen[-1] > said["tmax"]):
            doubts.append("a temperature they saw lies outside the low and high they wrote; the low and high stand")
    return said, doubts, notes


# Words of water that fell, or lay wet, which the reader does not measure: named anywhere in their
# words for a day, they keep a clear sky from making that day dry ("soleil, grêle à midi").
WET_WORDS = {"grele", "gresil", "hail", "sleet", "goutte", "drop", "mouille", "mouillee", "wet", "humide", "damp"}


def _clear_and_dry(thoughts, heard: list, said: dict) -> bool:
    """Does the keeper call the whole day clear, and name no rain, shower or snow anywhere in their words for it?

    All three must hold: some thought of the whole day (not of a part of it)
    speaks of the sky; all they say of the sky comes to "clear", as `Sky.words`
    would say it (so "sun and cloud", "éclaircies" or "soleil, gris" do not);
    and no word of rain, snow or wet, and no millimetre, stands anywhere in
    their words, even in a thought that was left alone ("soleil, pluie 20 min"
    keeps its rain). Rain they measured, or called dry, is already said.
    """
    if "rain" in said or _cloud_word(said.get("cloud", 1.0)) != "clear":
        return False
    if not any(one.get("skies") and not part for one, part in heard):
        return False                               # "soleil le soir": the sun of a part of the day only
    wet = set(RAIN_WORDS) | SNOW_WORDS | RAIN_UNITS | WET_WORDS
    return not any(_known(word) in wet for thought in thoughts for word in re.findall(r"[a-z]+", _fold(thought.words)))


@lru_cache(maxsize=4096)
def _said_items(text: str) -> tuple:
    return tuple(sorted(_together(_hear(text))[0].items()))


def _said(text) -> dict:
    """What the keeper's words say of a day, all together (see `understand`)."""
    return dict(_said_items(str(text))) if text else {}


def understand(sentence) -> dict:
    """What the gate reader makes of a loosely written line, or of a day's lines joined by "; ". Never raises.

    The keys it may give: `rain` (mm, measured; 0 for dry), `raining` (the mm
    a rain word suggests when no amount was given), `tmin` and `tmax` (the
    low and the high, as they wrote them), `seen` (temperatures they saw at some
    hour, which the day is widened to hold), `cloud` (0..1), `fog`, `wind`
    (Beaufort), `frost` and `snow` (True, or False for "no frost"), `feel`
    (degrees from the season's usual). An empty dict means nothing was
    understood, or nothing for sure: see `explain` for why.
    """
    try:
        return _said(sentence)
    except Exception:
        return {}


def explain(sentence) -> list:
    """Each thought of a line, in plain words: [(their words, what it says, or why it was left alone)]. Never raises."""
    try:
        return [(thought.words, _in_words(thought)) for thought in _hear(str(sentence))]
    except Exception:
        return []


def _in_words(thought: Thought) -> str:
    """What one thought says, or why it was left alone, in plain words."""
    if thought.why:
        return "left alone: " + thought.why
    said = dict(thought.said)
    if not said:
        return "nothing about the sky"
    if said.get("title"):
        return "a title, naming the day or the gauge: what follows it is read"
    only_part = "only part of the day, so it does not say the whole day had none"
    bits = []
    for mm in said.get("mm", ()):
        bits.append(f"rain, {mm:g} mm")
    for cm in said.get("cm", ()):
        bits.append(f"snow, {cm:g} cm (taken as {cm:g} mm of water)")
    if "raining" in said and not said.get("mm"):
        size = "light rain" if said["raining"] < 2 else "heavy rain" if said["raining"] >= 10 else "rain"
        bits.append(f"{size}, no amount given")
    if said.get("dry"):
        bits.append("no rain" + (f": {only_part}" if thought.part else ""))
    for key in ("frost", "snow"):
        if said.get(key) is True and not said.get("cm"):
            bits.append(f"{key}")
        elif said.get(key) is False:
            bits.append(f"no {key}" + (f": {only_part}" if thought.part else ""))
    if said.get("fog"):
        bits.append("fog")
    if said.get("skies"):
        cloud = sum(said["skies"]) / len(said["skies"])
        bits.append(f"the sky {_cloud_word(cloud)} (cloud {cloud:.2g})")
    for force in said.get("wind", ()):
        bits.append(f"wind, Beaufort {force:g}")
    if "wind_word" in said and not said.get("wind"):             # a measure outweighs a word
        force = said["wind_word"]
        bits.append(("a gale" if force >= 8 else "strong wind" if force >= 6 else "light wind" if force <= 2
                     else "some wind") + f" (Beaufort {force:g})")
    if said.get("calm"):
        bits.append("no wind")
    if said.get("feel"):
        feel = max(said["feel"], key=abs)
        bits.append(f"{'colder' if feel < 0 else 'warmer'} than the season's usual (by about {abs(feel):g}°)")
    for low in said.get("low", ()):
        bits.append(f"a low of {low:g}°")
    for high in said.get("high", ()):
        bits.append(f"a high of {high:g}°")
    if said.get("seen"):
        seen = " and ".join(f"{value:g}°" for value in said["seen"])
        bits.append(f"{seen} seen at some hour" + (f" ({', '.join(thought.part)})" if thought.part else "")
                    + ": the day's low and high are widened to hold it, if need be")
    return "; ".join(bits)


RUN_DAYS = 93            # the most days one line of the gate may cover ("2026-10-04 to 2026-10-08"): a season


def _read_gate(text: str, cut_runs: list | None = None) -> tuple:
    """The text of gate/sky.txt as the keeper's sentences by day, and the lines no date could be read from.

    Returns ({date: [sentence, ...]}, [line, ...]). Empty lines and remarks
    (lines beginning with #) are neither. A run of more than RUN_DAYS days,
    or one whose last day comes before its first, is read for its first day
    only; given a list as `cut_runs`, each such line is added to it as
    (line, first, last), so that it can be said.
    """
    days: dict = {}
    undated: list = []
    for line in unicodedata.normalize("NFC", text).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        found = _GATE_LINE.match(line)
        first = _written_date(found.groups()[:9]) if found else None
        last = _written_date(found.groups()[9:]) if found and any(found.groups()[9:]) else first
        if first is None or last is None:
            undated.append(_as_remark(line))
            continue
        sentence = _as_remark(re.sub(r"^\s*(?:[:=;,–—]|-(?=\s))?\s*", "", line[found.end():]))
        if not sentence:
            continue
        if not 0 <= (last - first).days < RUN_DAYS:
            if cut_runs is not None:
                cut_runs.append((_as_remark(line), first, last))
            last = first
        for ordinal in range(first.toordinal(), last.toordinal() + 1):
            days.setdefault(Date.fromordinal(ordinal), []).append(sentence)
    return days, undated


def _gate_days(text: str) -> dict:
    """The keeper's sentences by day: {date: [sentence, ...]} from the text of gate/sky.txt."""
    return _read_gate(text)[0]


def _written_date(groups):
    """A date from the nine groups of `_WRITTEN_DATE`, or None if it is no day of the calendar."""
    year, month, day, day_first, month_second, year_last, day_said, month_said, year_said = groups
    if year:
        return _date_from(year, month, day)
    if year_last:
        return _date_from(year_last, month_second, day_first)
    return _date_from(year_said, MONTHS.get(_fold(month_said or "")), day_said)


REMARK_LENGTH = 500       # the most a day's remark runs to
REMARK_LINES = 20         # and the most lines of theirs it is made from (the latest ones)


def _as_remark(sentence: str) -> str:
    """The keeper's sentence as it will be kept: on one line, and not endless."""
    sentence = "".join(ch if ch.isprintable() else " " for ch in sentence)
    return _cut(" ".join(sentence.split()), REMARK_LENGTH)


def _cut(sentence: str, length: int) -> str:
    return sentence if len(sentence) <= length else sentence[:max(0, length - 1)] + chr(0x2026)


def _kept_lines(sentences) -> list:
    """A day's sentences as its remark keeps them: the latest REMARK_LINES, the longest cut first to fit.

    Every line keeps its opening words, and a long one does not push the next out of the almanac.
    """
    kept = list(sentences)[-REMARK_LINES:]
    room = REMARK_LENGTH - 2 * (len(kept) - 1)
    allowed: dict = {}
    for done, at in enumerate(sorted(range(len(kept)), key=lambda n: len(kept[n]))):
        allowed[at] = min(len(kept[at]), room // (len(kept) - done))
        room -= allowed[at]
    return [_cut(sentence, allowed[at]) for at, sentence in enumerate(kept)]


def _day_remark(sentences) -> str:
    """A day's sentences as one remark, joined by "; ". The day is laid from exactly this."""
    return "; ".join(_kept_lines(sentences))


def _lay_over(values: dict, said: dict, usual: float) -> None:
    """Lay what the keeper said of a day over its values, changing only what they spoke of for sure."""
    _lay_temperatures(values, said, usual)
    _lay_rain(values, said)
    if "cloud" in said:
        values["cloud"] = said["cloud"]
        if values["rain"] > 0:
            values["cloud"] = max(values["cloud"], 0.4)      # sun and showers: a day with rain in it is never "clear"
    elif _speaks_of_rain(said) and values["rain"] > 0:
        values["cloud"] = max(values["cloud"], _rain_cloud(values["rain"]))
    if "wind" in said:
        values["wind"] = said["wind"]


def _speaks_of_rain(said: dict) -> bool:
    return said.get("rain", 0) > 0 or "raining" in said or said.get("snow") is True


def _lay_rain(values: dict, said: dict) -> None:
    if "rain" in said:
        values["rain"] = said["rain"]                        # an amount, or 0 for "dry"
    elif "raining" in said:
        suggested = said["raining"]                          # keep the amount there is, if it is of that order
        if not suggested / 3.0 <= values["rain"] <= suggested * 3.0:
            values["rain"] = suggested
    elif said.get("snow") is True and values["rain"] < 1.0:
        values["rain"] = 3.0                                 # snow fell: something fell


def _lay_temperatures(values: dict, said: dict, usual: float) -> None:
    """The keeper's numbers first; then their words, which never move a number they gave and never make a frost they did not say.

    `tmin`/`tmax` are the low and the high they wrote. A temperature they saw
    (`seen`) only widens the day to hold it, where they did not write that end.
    """
    apart = values["tmax"] - values["tmin"]
    low, high, seen = said.get("tmin"), said.get("tmax"), said.get("seen", ())
    if low is not None and high is not None:
        values["tmin"], values["tmax"] = low, high
    elif low is not None:
        values["tmin"] = low
        if values["tmax"] < low + 1.0:
            values["tmax"] = low + apart
    elif high is not None:
        values["tmax"] = high
        if values["tmin"] > high - 1.0:
            values["tmin"] = _low_under(high, apart, said)
    if seen:
        if low is None and seen[0] < values["tmin"]:
            values["tmin"] = seen[0]
        if high is None and seen[-1] > values["tmax"]:
            values["tmax"] = seen[-1]
    none_given = low is None and high is None and not seen
    before = values["tmin"]
    feel = said.get("feel")
    if feel is not None and none_given:
        shift = usual + feel - (values["tmin"] + values["tmax"]) / 2.0
        if (feel < 0) == (shift < 0):                        # only if the day is not already that cold, or that warm
            if shift < 0 and before >= 0 and said.get("frost") is not True:
                shift = max(shift, min(0.0, 0.5 - before))   # cold, but no frost they did not say
            values["tmin"] += shift
            values["tmax"] += shift
    if said.get("snow") is True and none_given:
        values["tmin"] = min(values["tmin"], 0.0)            # snow: a cold day, but a frost only if they say so
        values["tmax"] = min(values["tmax"], 2.0)
    if said.get("frost") is True:
        if low is None and values["tmin"] >= 0:
            values["tmin"] = -1.0
        elif low == 0:
            values["tmin"] = -0.1                            # "gel blanc, min 0": their zero was a frost
    elif said.get("frost") is False and low is None and values["tmin"] < 0 and not (seen and seen[0] < 0):
        values["tmin"] = 0.5
    if values["tmax"] < values["tmin"] + 0.5:                # keep the high above the low
        if high is None:
            values["tmax"] = values["tmin"] + 0.5
        elif low is None:
            lowered = values["tmax"] - 0.5
            values["tmin"] = lowered if lowered >= 0 or values["tmax"] <= 0 or said.get("frost") else 0.0


def _low_under(high: float, apart: float, said: dict) -> float:
    """A night's low to go under a high the keeper gave, when the low there was stood above it.

    The day keeps its spread, but no frost is invented: unless they said
    frost, a high above zero keeps its low above zero too.
    """
    low = high - apart
    if said.get("frost") is not True and high > 0:
        low = max(low, min(1.0, high / 2.0))
    return low


# ───────────────────────────────────────────────────────────── the real sky
#
# Off unless the keeper turns it on. The network is touched in one place only,
# `_ask` (with the `_fetch` it sends out), and urllib is not even loaded until then.
#
# A day is asked for together with the fortnight before it and the weeks after,
# so a long absence costs a few questions, not hundreds. Days still to come are
# never asked for, and only the days asked for are taken from an answer. What
# open-meteo gives is kept and never asked for again; a day it could not give
# is reckoned, and may turn real at some later asking. Numbers no sky could
# have are not believed, from the wire or from the cache: that day is reckoned.
# If the network fails once, or answers with nothing of use, or has taken more
# than a few seconds in all, the process stops asking: no visit waits twice.

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"          # the last three months
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"    # anything older
DAILY = "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,sunshine_duration"
ASK_SECONDS = 5           # the longest one question may take, from the first word to the whole answer
ASK_BUDGET = 8            # seconds: once the questions of this process have taken this long, no more are asked
ASK_BYTES = 1_000_000     # no answer is read past its first megabyte (a year of days is a few thousand bytes)
CACHE_FIELDS = ("tmin", "tmax", "rain", "cloud", "wind")
BELIEVABLE = {            # what one day's real weather can be: a value outside these is not believed
    "tmin": (-60.0, 60.0), "tmax": (-60.0, 60.0), "rain": (0.0, 500.0), "cloud": (0.0, 1.0), "wind": (0.0, 12.0),
}

_gave_up = False          # the network failed in this process, or was too slow: do not ask again
_asking_took = 0.0        # seconds this process has spent waiting for answers
_asked: dict = {}         # root -> the days already asked about in this process


def _ask(url: str) -> str:
    """Ask open-meteo one question, and wait ASK_SECONDS for the whole answer, no longer.

    The only place in the garden's sky that uses the network. The question is
    put on a thread of its own, because a socket's timeout does not cover
    everything: a name that will not resolve, or an answer that drips in a
    byte at a time, could hold the gate for minutes. When the time is up the
    garden walks on, and the thread is left to end by itself.
    """
    import threading
    heard: list = []
    asking = threading.Thread(target=_fetch, args=(url, heard), daemon=True)
    asking.start()
    asking.join(ASK_SECONDS)
    if not heard:
        raise TimeoutError("open-meteo did not answer in time")
    if isinstance(heard[0], Exception):
        raise heard[0]
    if isinstance(heard[0], BaseException):        # an interrupt or an exit from inside the asking: only a failure here
        raise OSError(f"the asking was broken off: {heard[0]!r}")
    return heard[0]


def _fetch(url: str, heard: list) -> None:
    """Fetch the answer to one question into `heard`; if that fails, the failure goes there in its place."""
    try:
        from urllib.request import urlopen
        with urlopen(url, timeout=ASK_SECONDS) as answer:
            heard.append(answer.read(ASK_BYTES).decode("utf-8", errors="replace"))
    except BaseException as trouble:
        heard.append(trouble)


def open_meteo_url(latitude: float, longitude: float, first, last, today) -> str:
    """The question to ask for the days first..last."""
    base = FORECAST_URL if (today - first).days <= 90 else ARCHIVE_URL
    return (f"{base}?latitude={latitude:.4f}&longitude={longitude:.4f}&daily={DAILY}"
            f"&start_date={first.isoformat()}&end_date={last.isoformat()}"
            f"&timezone=auto&wind_speed_unit=kmh")


def read_open_meteo(answer, latitude: float = 47.0) -> dict:
    """open-meteo's answer as {date: {tmin, tmax, rain, wind, cloud}}. Never raises.

    A day with no temperatures is left out, and so is a day whose numbers no
    sky could have (see BELIEVABLE). Cloud is worked out from the hours of
    sunshine against the length of the day; without them it is left unsaid.
    The wind is the day's strongest hour, taken down a little, on the Beaufort scale.
    """
    days: dict = {}
    try:
        daily = (json.loads(answer) if isinstance(answer, (str, bytes)) else answer)["daily"]
        times = daily["time"]
    except Exception:
        return days
    for at, stamp in enumerate(times if isinstance(times, (list, tuple)) else ()):
        try:
            day = Date.fromisoformat(str(stamp)[:10])
        except Exception:
            continue
        figures = [_nth(daily, name, at) for name in ("temperature_2m_min", "temperature_2m_max",
                                                      "precipitation_sum", "wind_speed_10m_max", "sunshine_duration")]
        low, high, rain, speed, sunshine = figures
        if low is None or high is None or not all(_finite(figure) for figure in figures if figure is not None):
            continue
        found = {"tmin": round(min(low, high), 1), "tmax": round(max(low, high), 1)}
        found["rain"] = round(max(0.0, rain), 1) if rain is not None else 0.0
        if speed is not None:
            found["wind"] = _beaufort(0.7 * speed)
        hours = daylength(latitude, day)
        if sunshine is not None and hours > 0:
            found["cloud"] = round(max(0.0, min(1.0, 1.0 - sunshine / 3600.0 / (0.9 * hours))), 2)
        if _believable(found):
            days[day] = found
    return days


def _nth(daily: dict, name: str, at: int):
    """One number from one of open-meteo's lists (which may be NaN or infinity); None if there is none.

    A `true` or `false` there is no number (though Python would make 1.0 of it).
    """
    try:
        figure = daily[name][at]
        return None if isinstance(figure, bool) else float(figure)
    except Exception:
        return None


def _believable(values: dict) -> bool:
    """Could these be one day's real weather? Every number finite and within BELIEVABLE, the low not above the high."""
    try:
        within = all(_finite(values[name]) and low <= values[name] <= high
                     for name, (low, high) in BELIEVABLE.items() if name in values)
        return within and values["tmin"] <= values["tmax"]
    except (KeyError, TypeError):
        return False


def _window(day, today):
    """The days to ask for along with `day`: the fortnight before it (for the ground's wetness) and what follows."""
    first = day - 14 * ONE_DAY
    last = min(day + 30 * ONE_DAY, today)
    if (today - day).days > 85:
        last = min(last, today - 5 * ONE_DAY)       # the archive runs a few days behind
    else:
        first = max(first, today - 90 * ONE_DAY)
    return first, last


def _real_day(garden: "_Garden", day):
    """The real weather of a day, from the cache or by asking; None if it is not to be had."""
    global _gave_up, _asking_took
    if day in garden.real:
        return garden.real[day]
    asked = _asked.setdefault(garden.root, set())
    today = Date.today()
    if _gave_up or day in asked or day > today:
        return None
    first, last = _window(day, today)
    where = garden.place
    started = time.monotonic()
    try:
        answer = _ask(open_meteo_url(where["latitude"], where["longitude"], first, last, today))
        fetched = read_open_meteo(answer, where["latitude"])
    except Exception:
        fetched = {}
    _asking_took += time.monotonic() - started
    given = {d: v for d, v in fetched.items() if first <= d <= last}       # only the days that were asked for
    if not given or _asking_took >= ASK_BUDGET:
        _gave_up = True                            # nothing of use came back, or it has all taken too long
    new = {d: v for d, v in given.items() if d not in garden.real and d not in asked}
    asked.update(Date.fromordinal(n) for n in range(first.toordinal(), last.toordinal() + 1))
    if new:
        garden.real.update(new)
        _write_cache(garden)
    return garden.real.get(day)


def _cache_is_for(where: dict) -> str:
    return f"{where['latitude']:.4f},{where['longitude']:.4f}"


def _read_cache(text: str, where: dict) -> dict:
    """`ground/sky-cache` as {date: values}; empty if it was kept for another place.

    A hand may have been in this file too: a line whose numbers no sky could have is passed over.
    """
    days: dict = {}
    right_place = False
    for line in text.splitlines():
        if line.startswith("for:"):
            right_place = line[4:].strip() == _cache_is_for(where)
            continue
        parts = line.split()
        day = _date_in(parts[0]) if parts else None
        if day is None or not right_place:
            continue
        values = {}
        for name, number in zip(parts[1::2], parts[2::2]):
            if name in CACHE_FIELDS and _number(number) is not None:
                values[name] = _number(number)
        if _believable(values):
            days[day] = values
    return days


def _write_cache(garden: "_Garden") -> None:
    """Keep the real days in `ground/sky-cache`. If it cannot be written, never mind."""
    lines = ["# The real sky over the garden, as open-meteo.com gave it. One line per day.",
             "# Each day is asked for once and kept. Remove a line (or the file) to ask again.",
             "for: " + _cache_is_for(garden.place)]
    for day in sorted(garden.real):
        values = garden.real[day]
        lines.append(day.isoformat() + "".join(f"  {name} {values[name]}" for name in CACHE_FIELDS if name in values))
    path = _path(garden.root, "ground", "sky-cache")
    try:
        with open(path + ".new", "w", encoding="utf-8", newline="\n") as file:
            file.write("\n".join(lines) + "\n")
        os.replace(path + ".new", path)
    except OSError:
        try:
            os.remove(path + ".new")
        except OSError:
            pass


# ─────────────────────────────────────────────────────── the sky over a garden

_gardens: dict = {}
troubles: list = []       # if the sky ever had to fall back on a bare reckoning, why (newest last)


class _Garden:
    """What the sky has read of one garden, and the days it has already worked out.

    It is thrown away and read afresh the moment any of the three files changes.
    """

    def __init__(self, root: str, files: tuple):
        place_bytes, gate_bytes, cache_bytes, _today = files
        self.root = root
        self.files = files
        self.place = dict(_place_from(place_bytes))
        self.south = self.place["latitude"] < 0
        self.cut_runs: list = []   # (line, first, last): runs read for their first day only
        self.gate, self.undated = _read_gate(_text_of(gate_bytes), self.cut_runs)
        self.real = _read_cache(_text_of(cache_bytes), self.place) if self.wants_real_sky else {}
        self.plain: dict = {}      # date -> _Day, before the ground's wetness
        self.skies: dict = {}      # date -> Sky

    @property
    def wants_real_sky(self) -> bool:
        return self.place["real-sky"] is True and self.place["longitude"] is not None


def _files_of(root: str) -> tuple:
    """The bytes of the files a garden's sky depends on."""
    place_bytes = _bytes_of(_path(root, "ground", "place"))
    gate_bytes = _bytes_of(_path(root, "gate", "sky.txt"))
    where = dict(_place_from(place_bytes))
    if where["real-sky"] is True and where["longitude"] is not None:
        return place_bytes, gate_bytes, _bytes_of(_path(root, "ground", "sky-cache")), Date.today()
    return place_bytes, gate_bytes, None, None


def _garden(root) -> _Garden:
    root = _path(root)
    files = _files_of(root)
    known = _gardens.get(root)
    if known is None or known.files != files:
        known = _gardens[root] = _Garden(root, files)
    return known


@dataclass(frozen=True)
class _Day:
    """A day's weather as its sources give it, before the ground's wetness is worked out."""

    values: dict           # tmin, tmax, rain, cloud, wind: what the day is
    source: str            # 'reckoned' | 'gate' | 'open-meteo'
    remark: str            # the keeper's words for the day, as kept
    before: dict           # the same values as they were without the keeper's words
    before_source: str     # 'reckoned' | 'open-meteo'


def _plain_day(garden: _Garden, day) -> _Day:
    """A day's weather from its source, with the keeper's words laid over it."""
    known = garden.plain.get(day)
    if known is not None:
        return known
    reckoned = reckon(garden.place["weather-seed"], day, garden.south)
    values = dict(reckoned)
    source = "reckoned"
    real = _real_day(garden, day) if garden.wants_real_sky else None
    if real:
        values.update(real)
        source = "open-meteo"
    before = dict(values)
    _tidy(before, reckoned)
    remark = _day_remark(garden.gate.get(day, ()))
    said = _said(remark)                           # the day is heard from exactly the remark the almanac prints
    if said:
        _lay_over(values, said, usual_warmth(day, garden.south))
    _tidy(values, reckoned)
    garden.plain[day] = _Day(values, "gate" if said else source, remark, before, source)
    return garden.plain[day]


SKY_LIMITS = {            # what a day's values are held to, whatever their source: (least, most, decimal places kept)
    "tmin": (-60.0, 60.0, 1), "tmax": (-60.0, 60.0, 1), "rain": (0.0, 500.0, 1),
    "cloud": (0.0, 1.0, 2), "wind": (0.0, 10.0, 1),
}


def _tidy(values: dict, reckoned: dict) -> None:
    """Keep a day's values within what a sky can be. The last line of defence.

    A value that is no number at all (NaN, infinity, a word) gives way to the reckoned one.
    """
    for name, (least, most, places) in SKY_LIMITS.items():
        value = values.get(name)
        if not _finite(value):
            value = reckoned[name]
        values[name] = _rounded(max(least, min(most, value)), places)
    if values["tmin"] > values["tmax"]:
        values["tmin"], values["tmax"] = values["tmax"], values["tmin"]


def _wetness(garden: _Garden, day, hours: float) -> float:
    """How wet the ground is on the morning of `day`, from the fourteen days before.

    Each day back counts for less; long days dry the ground faster than short ones.
    """
    keeps = max(0.5, min(0.95, 0.95 - 0.0175 * hours))     # the share of yesterday's wet still there today
    lingering, share = 0.0, 1.0
    for back in range(1, 15):
        if day.toordinal() - back < 1:
            break
        share *= keeps
        lingering += share * _plain_day(garden, day - back * ONE_DAY).values["rain"]
    return round(1.0 - math.exp(-lingering / SODDEN_MM), 2)


def _whole_sky(garden: _Garden, day) -> Sky:
    plain = _plain_day(garden, day)
    return _sky_of(garden, day, plain.values, plain.source, plain.remark)


def _sky_of(garden: _Garden, day, values: dict, source: str, remark: str) -> Sky:
    latitude = garden.place["latitude"]
    hours = daylength(latitude, day)
    return Sky(date=day, tmin=values["tmin"], tmax=values["tmax"], rain=values["rain"],
               cloud=values["cloud"], wind=values["wind"], daylength=hours,
               light=round(hours * (1.0 - 0.7 * values["cloud"]), 2),
               wet=_wetness(garden, day, hours), moon=moon(day),
               season=season(latitude, day), source=source, remark=remark)


def sky_for(root, day) -> Sky:
    """The sky over the garden at `root` on `day`. Pure: the same files and date give the same sky."""
    day = _as_date(day)
    try:
        garden = _garden(root)
        sky = garden.skies.get(day)
        if sky is None:
            sky = garden.skies[day] = _whole_sky(garden, day)
        return sky
    except Exception as trouble:                   # the gate always opens: a bare reckoned sky
        troubles.append(f"{day.isoformat()}: {type(trouble).__name__}: {trouble}")
        del troubles[:-20]
        return _whole_sky(_Garden("", (None, None, None, None)), day)


# ─────────────────────────────────────────────────────────── under the glass
#
# A bed under glass keeps a calendar of its own (see ground.py, `Glass`): its
# days are not the garden's days, so the keeper's lines and the real sky, which
# are written for the garden's days, say nothing of them. A day under the glass
# is the reckoned sky of its own date, a little warmer, with the frost, the snow
# and the wind kept out, and the can standing in for the rain: on a day the
# reckoned sky would have rained, the bench is watered by as much.

GLASS_WARMER = 3.0      # degrees the glass keeps over the open air, by night and by day
GLASS_LEAST = 2.0       # °C: the coldest a night under the glass may be. No frost comes in


def under_glass(root, day) -> Sky:
    """The sky of one day under the glass. Pure: the same place and date give the same sky. Never raises."""
    day = _as_date(day)
    try:
        where = dict(_place_from(_bytes_of(_path(root, "ground", "place"))))
    except Exception:
        where = dict(DEFAULT_PLACE)
    seed, latitude = where["weather-seed"], where["latitude"]
    south = latitude < 0
    values = reckon(seed, day, south)
    tmin = max(GLASS_LEAST, values["tmin"] + GLASS_WARMER)
    tmax = max(tmin, values["tmax"] + GLASS_WARMER)
    hours = daylength(latitude, day)
    keeps = max(0.5, min(0.95, 0.95 - 0.0175 * hours))     # the bench dries as the ground does (see `_wetness`)
    lingering, share = 0.0, 1.0
    for back in range(1, 15):
        if day.toordinal() - back < 1:
            break
        share *= keeps
        lingering += share * reckon(seed, day - back * ONE_DAY, south)["rain"]
    return Sky(date=day, tmin=_rounded(tmin, 1), tmax=_rounded(tmax, 1), rain=values["rain"], cloud=values["cloud"],
               wind=0.0, daylength=hours, light=round(hours * (1.0 - 0.7 * values["cloud"]), 2),
               wet=round(1.0 - math.exp(-lingering / SODDEN_MM), 2), moon=moon(day),
               season=season(latitude, day), source="glass", remark="")


def unread(root) -> list:
    """The lines of `gate/sky.txt` that no date could be read from, as the keeper wrote them. Never raises.

    Empty lines and remarks (#) are not among them. With this the arrival note
    can say that a line at the gate could not be dated, so that a month of
    lines written some other way is not passed over in silence.
    """
    try:
        return list(_garden(root).undated)
    except Exception:
        return []


def local(sky: Sky, bed) -> Sky:
    """The same sky as a bed feels it: its share of the light and the rain, and its shelter.

    `bed` may be the ground's Bed or a bed's keys as a dict; missing or
    unreadable values are light 1, water 1, shelter 0.5.
    """
    light = _of_bed(bed, "light", 1.0, 0.0, 1.0)
    water = _of_bed(bed, "water", 1.0, 0.0, 5.0)
    shelter = _of_bed(bed, "shelter", 0.5, 0.0, 1.0)
    return replace(
        sky,
        light=round(sky.light * light, 2),
        rain=round(sky.rain * water, 1),
        wet=round(min(1.0, sky.wet * water), 2),
        tmin=_rounded(min(sky.tmax, sky.tmin + 2.5 * shelter), 1),
        wind=round(sky.wind * (1.0 - 0.8 * shelter), 1),
    )


def _of_bed(bed, name: str, default: float, low: float, high: float) -> float:
    """One of a bed's numbers, from an attribute or a key, read as `hands.num` reads it. Never raises.

    So a bed's `water: .5` is the same half to the sky as it is to the ground.
    """
    try:
        value = getattr(bed, name, None)
        if value is None and isinstance(bed, dict):
            value = bed.get(name)
    except Exception:                              # a bed whose attribute raises says nothing of itself
        value = None
    return _num(value, default, low, high)


def _garden_today(root) -> datetime.date:
    """Today as the garden's doors count it (see `ground.today`), read exactly as they read it.

    GLEBE_TODAY if it is set (strictly 2026-10-04, nothing looser); else the
    real date, plus the `ahead: N` days of `ground/clock` on a trial ground
    whose calendar has been wound on.
    """
    found = re.search(r"(\d{4})-(\d{2})-(\d{2})", os.environ.get("GLEBE_TODAY", ""))
    given = _date_from(*found.groups()) if found else None
    if given is not None:
        return given
    clock = _read_keys(_text_of(_bytes_of(_path(root, "ground", "clock"))))
    ahead = _num(clock.get("ahead"), 0, -40_000, 40_000)
    return Date.today() + datetime.timedelta(days=int(ahead))


# ───────────────────────────────────────── what the keeper is shown of their lines
#
# `python shed/sky.py --gate` and `python shed/sky.py <date>`: plain words for
# the keeper, who writes the lines and is not asked to read this file. Nothing
# here changes anything; it only reads, and says.

_DAY_NAMES = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
_MONTH_NAMES = ("January", "February", "March", "April", "May", "June", "July", "August", "September",
                "October", "November", "December")
_SOURCES = {"reckoned": "reckoned", "open-meteo": "the real sky, from open-meteo", "gate": "their words"}


def _long_date(day) -> str:
    """"Sunday 4 October 2026" (in English whatever the machine's language)."""
    return f"{_DAY_NAMES[day.weekday()]} {day.day} {_MONTH_NAMES[day.month - 1]} {day.year}"


def _brief(sky: Sky) -> str:
    """A day's sky in a few words, without the light and the moon: "overcast, 9–15°, rain 6 mm, wind 3"."""
    parts = sky.words.split(", ")
    kept = [part for part in parts if not part.startswith(("light ", "moon ", "new moon", "full moon"))]
    return ", ".join(kept) + f", wind {sky.wind:g}"


def _on_trial(root) -> bool:
    """Is this a trial ground? As the ground decides it: it holds a file ground/clock."""
    return os.path.isfile(_path(root, "ground", "clock"))


TRIAL_HINT = ("This is a trial ground: to try a kind under weather of your own (a long drought, a hard frost),\n"
              "write it in this ground's own gate/sky.txt, as `python shed/sky.py --help` shows.")


def _cut_run(line: str, first, last) -> list:
    """A line of the gate whose run is read for its first day only, and why, in plain words."""
    if last < first:
        why = f"its last day ({_long_date(last)}) comes before its first"
        mend = "Write the earlier day first."
    else:
        why = f"it runs {(last - first).days + 1} days, more than the {RUN_DAYS} one line may cover"
        mend = "Write a longer spell as several lines."
    return [f'  "{line}"', f"      {why},", f"      so only {_long_date(first)} is given its words. {mend}"]


def _cut_runs_over(garden: _Garden, first, last) -> list:
    """The cut runs that meant some day from `first` to `last` they are not read for (all but their first)."""
    found = []
    for line, start, end in garden.cut_runs:
        low, high = max(first, min(start, end)), min(last, max(start, end))
        if low <= high and not low == high == start:
            found.append((line, start, end))
    return found


def _changes(before: dict, after: dict) -> str:
    """What the keeper's words changed in a day, field by field, in plain words."""
    said = []
    for name, label, unit in (("tmin", "low", "°"), ("tmax", "high", "°"), ("rain", "rain", " mm"),
                              ("cloud", "cloud", ""), ("wind", "wind", "")):
        if before[name] != after[name]:
            said.append(f"{label} {before[name]:g}{unit} → {after[name]:g}{unit}")
    return ", ".join(said)


def _last_lived(root, today):
    """The last day the garden has lived (the last dated line of ground/almanac, not after today), or None."""
    try:
        with open(_path(root, "ground", "almanac"), "rb") as file:
            file.seek(0, 2)
            file.seek(max(0, file.tell() - 200_000))
            tail = _text_of(file.read())
    except OSError:
        return None
    last = None
    for line in tail.splitlines():
        found = re.match(r"(\d{4})-(\d{2})-(\d{2})(?:\s|$)", line)
        day = _date_from(*found.groups()) if found else None
        if day is not None and day <= today and (last is None or day > last):
            last = day
    return last


def _when(garden: _Garden, day, today, lived) -> str:
    """Where a day stands in the garden's life, in a few words."""
    if day < garden.place["laid"]:
        return "is before the ground was laid: no garden lived it"
    if day > today:
        return "has not come yet: the line will be heard when it does"
    if lived is not None and day <= lived:
        return "has already been lived: the garden grew under its sky as it was read then"
    return "is still to be lived: the next arrival will live it under this sky"


def _day_account(garden: _Garden, day, today, lived, show_lines: bool = True) -> list:
    """The keeper's lines for one day, thought by thought, and what they changed."""
    out = []
    lines = _kept_lines(garden.gate.get(day, ()))
    dropped = len(garden.gate.get(day, ())) - len(lines)
    if show_lines:
        if dropped:
            out.append(f"  ({dropped} earlier line{'s' if dropped > 1 else ''} for this day are not read: "
                       f"a day keeps its latest {REMARK_LINES})")
        for line in lines:
            out.append(f'  "{line}"')
            for words, meaning in explain(line):
                out.append(f'      "{words}": {meaning}')
        _, doubts, notes = _together(_hear(_day_remark(garden.gate.get(day, ()))))
        for doubt in doubts:
            out.append(f"  Their words disagree: {doubt}.")
        for note in notes:
            out.append(f"  Taken all together: {note}.")
    plain = _plain_day(garden, day)
    now = _sky_of(garden, day, plain.values, plain.source, plain.remark)
    without = _sky_of(garden, day, plain.before, plain.before_source, "")
    changed = _changes(plain.before, plain.values)
    if changed or now.snow != without.snow or _brief(now) != _brief(without):
        out.append(f"  The day without their words: {_brief(without)}  ({_SOURCES[plain.before_source]})")
        out.append(f"  The day with them:           {_brief(now)}")
        if changed:
            out.append(f"  Changed: {changed}.")
    else:
        out.append(f"  It changes nothing: the day stays {_brief(without)}  ({_SOURCES[plain.before_source]}).")
    out.append(f"  This day {_when(garden, day, today, lived)}.")
    return out


def gate_report(root) -> str:
    """What the reader makes of every line in gate/sky.txt, in plain words, for the keeper. Changes nothing."""
    root = _path(root)
    garden = _garden(root)
    today = _garden_today(root)
    lived = _last_lived(root, today)
    out = ["What the sky makes of the keeper's lines in gate/sky.txt",
           f"Today in the garden: {_long_date(today)}."
           + (f" The garden has lived its days up to {_long_date(lived)}." if lived else ""),
           "",
           "Each line is cut into thoughts at its commas and full stops. A thought changes the sky only",
           "when every word and number in it is understood; anything else is left alone, and their words",
           "are still printed beside the day in the almanac. A number needs its unit or its °, except",
           "two numbers standing alone between commas, the lower first (\"9 à 15\"): the low and the high.",
           ""]
    if _bytes_of(_path(root, "gate", "sky.txt")) is None:
        out.append("There is no gate/sky.txt yet. A line there looks like this:")
        out.append("    2026-10-04: pluie 6mm, 9 à 15°, gris toute la journée")
        if _on_trial(root):
            out += ["", TRIAL_HINT, "A run of days looks like this:",
                    "    2027-06-10 to 2027-08-31: sec, soleil, 14 à 28°"]
        return "\n".join(out)
    days = sorted(garden.gate)
    groups: list = []
    for day in days:                                # a run of days with the same lines is shown once
        if groups and day - groups[-1][-1] == ONE_DAY and garden.gate[day] == garden.gate[groups[-1][0]]:
            groups[-1].append(day)
        else:
            groups.append([day])
    for group in groups:
        if len(group) == 1:
            out.append(_long_date(group[0]))
        else:
            out.append(f"{_long_date(group[0])} to {_long_date(group[-1])} ({len(group)} days, the same words)")
        out += _day_account(garden, group[0], today, lived)
        for day in group[1:8]:
            out.append(f"  {_long_date(day)}:")
            out += ["  " + line for line in _day_account(garden, day, today, lived, show_lines=False)]
        if len(group) > 8:
            out.append(f"  ... and {len(group) - 8} more days of the same words.")
        out.append("")
    if not days:
        out += ["No line in gate/sky.txt is dated for a day yet.", ""]
    if garden.cut_runs:
        many = len(garden.cut_runs) > 1
        out.append(f"{len(garden.cut_runs)} line{'s' if many else ''} {'are' if many else 'is'} read for "
                   f"{'their' if many else 'its'} first day only:")
        for line, first, last in garden.cut_runs:
            out += _cut_run(line, first, last)
        out.append("")
    if garden.undated:
        out.append(f"{len(garden.undated)} line{'s' if len(garden.undated) > 1 else ''} could not be dated, "
                   "and so change nothing:")
        out += [f'  "{line}"' for line in garden.undated]
        out.append("  A line begins with its date: 2026-10-04, 04/10/2026, or 4 octobre 2026.")
    else:
        out.append("Every line could be dated.")
    out.append("The words the reader knows: python shed/sky.py --words")
    return "\n".join(out)


def known_words() -> str:
    """Every word the gate reader knows, table by table, for whoever writes the lines."""
    def row(name: str, words) -> str:
        return f"  {name:<13}" + ", ".join(sorted(words))
    return "\n".join([
        "The words the sky's reader knows, written here without accents (a final s or x does not matter).",
        "A thought is heard only when every word in it is one of these, and every number is one of the",
        "shapes at the end.",
        "",
        row("rain", RAIN_WORDS), row("dry", DRY_WORDS), row("frost", FROST_WORDS), row("snow", SNOW_WORDS),
        row("fog", FOG_WORDS), row("the sky", SKY_WORDS), row("wind", WIND_WORDS), row("cold, warm", FEEL_WORDS),
        row("light", LIGHT_WORDS), row("heavy", HEAVY_WORDS), row("no", NO_WORDS | OR_WORDS),
        row("day parts", DAY_PARTS), row("small words", SMALL_WORDS - {"s", "d", "l", "j", "y"}),
        "",
        row("another day", OTHER_DAY_WORDS),
        "               (one of these leaves alone the rest of its sentence)",
        row("titles", TITLE_WORDS),
        "               (one of these before a colon heads the line: \"Noël : soleil\" is read whole)",
        "",
        "  numbers      6 mm · 5 à 10 mm · 10 cm beside neige · 9 à 15° · -1 / 12 · entre 9 et 15° · min 3 ·",
        "               max 12 · 12° · -3 · moins 2° · 20 km/h · 10 à 20 km/h · 12 mph · force 3-4 · 4 bft",
        "               9 à 15 · 0 to 4 · 10-16, with no °, only standing alone between commas, the lower first",
    ])


SPAN_MOST = 3653          # the most days `python shed/sky.py <day> to <day>` goes through: ten years
SPAN_LISTED = 400         # and the most it lists one by one; a longer span is told in sum only
_FROM = {"gate": "from the gate", "reckoned": "reckoned", "open-meteo": "from open-meteo"}


def span_report(root, first, last) -> str:
    """Each day from `first` to `last` as the garden's plants will live it, and what they came to. Changes nothing.

    For whoever wants to know the weather a stretch of days will bring, before
    winding a trial ground on through it: a kind's trial, most often.
    """
    root = _path(root)
    first, last = sorted((_as_date(first), _as_date(last)))
    out = []
    if (last - first).days >= SPAN_MOST:
        last = first + (SPAN_MOST - 1) * ONE_DAY
        out += [f"(Ten years at most are gone through: here, up to {_long_date(last)}.)", ""]
    days = [Date.fromordinal(n) for n in range(first.toordinal(), last.toordinal() + 1)]
    skies = [sky_for(root, day) for day in days]
    if len(days) <= SPAN_LISTED:
        out.append("Each day's sky over the garden (each bed then takes its own share of it), and how wet the")
        out.append("ground is that morning, 0 dust .. 1 sodden:")
        for day, sky in zip(days, skies):
            out.append(f"  {day.isoformat()} {_DAY_NAMES[day.weekday()][:3]}  {sky.words}; ground {sky.wet:.2f}"
                       f"  [{sky.source}]")
        out.append("")
    sources = [f"{sum(1 for sky in skies if sky.source == source)} {words}" for source, words in _FROM.items()
               if any(sky.source == source for sky in skies)]
    out.append(f"{len(days)} day{'s' if len(days) > 1 else ''}, {_long_date(first)} to {_long_date(last)}"
               f" ({', '.join(sources)}):")
    wet = [sky for sky in skies if sky.rain > 0]
    snowy = sum(1 for sky in wet if sky.snow)
    dry_run, dry_from = _longest(skies, lambda sky: sky.rain <= 0)
    if not wet:
        out.append("  No rain on any of them.")
    else:
        rain = f"  Rain on {len(wet)} of them, {_millimetres(sum(_as_written(sky.rain) for sky in wet))} mm in all"
        rain += f" ({snowy} of them snow)" if snowy else ""
        rain += (f"; the longest run without rain {dry_run} day{'s' if dry_run > 1 else ''},"
                 f" from {_long_date(dry_from)}" if dry_run else "; not one day without it")
        out.append(rain + ".")
    frosts = sum(1 for sky in skies if sky.frost)
    frost_run, frost_from = _longest(skies, lambda sky: sky.frost)
    out.append((f"  Frost on {frosts} night{'s' if frosts > 1 else ''}" if frosts else "  No frost")
               + (f", the longest run of them {frost_run} nights, from {_long_date(frost_from)}"
                  if frost_run > 1 else "")
               + f"; the coldest night {_degree(min(sky.tmin for sky in skies))}°,"
               f" the warmest day {_degree(max(sky.tmax for sky in skies))}°.")
    out.append(f"  The ground at its driest {min(sky.wet for sky in skies):.2f},"
               f" at its wettest {max(sky.wet for sky in skies):.2f}.")
    garden = _garden(root)
    cut = _cut_runs_over(garden, first, last)
    if cut:
        out += ["", "A line at the gate meant some of these days, but is read for its first day only:"]
        for line, start, end in cut:
            out += _cut_run(line, start, end)
    if _on_trial(root) and not any(sky.source == "gate" for sky in skies):
        out += ["", TRIAL_HINT]
    return "\n".join(out)


def _longest(skies: list, holds) -> tuple:
    """The longest run of days in a row for which `holds(sky)` is true: (how many, its first day)."""
    best, best_from, run = 0, None, 0
    for at, sky in enumerate(skies):
        run = run + 1 if holds(sky) else 0
        if run > best:
            best, best_from = run, skies[at - run + 1].date
    return best, best_from


def _say(arguments: list, root) -> None:
    """`python shed/sky.py [date | date to date | --gate | --words | --help]`, for the garden at `root`."""
    if "--help" in arguments or "-h" in arguments:
        print(__doc__.strip())
        return
    if "--gate" in arguments:
        print(gate_report(root))
        return
    if "--words" in arguments:
        print(known_words())
        return
    asked = " ".join(arguments).strip()
    written = [found.groups() for found in re.finditer(_WRITTEN_DATE, asked, re.IGNORECASE)][:2]
    if len(written) == 2:                          # a span: "2027-06-01 to 2027-08-31", or two days given apart
        first, last = _written_date(written[0]), _written_date(written[1])
        if first is not None and first == last:
            asked = first.isoformat()              # the same day twice is that day
        elif first is not None and last is not None:
            print(span_report(root, first, last))
            return
        else:
            print(f'I could not read two days in "{asked}" (write them year first: 2027-06-01 to 2027-08-31).'
                  " Here is today.")
            asked = ""
    day = _date_in(asked) or _written_date_in(asked) if asked else None
    if day is None:
        day = _garden_today(root)
        if asked:
            print(f'I could not read a day in "{asked}" (write it year first: 2026-10-04). Here is today.')
    sky = sky_for(root, day)
    print(f"{day.isoformat()}  {sky.words}. {sky.season.capitalize()}.  [{sky.source}]")
    garden = _garden(root)
    if garden.gate.get(day):
        today = _garden_today(root)
        print(f"The keeper's words for {_long_date(day)}:")
        print("\n".join(_day_account(garden, day, today, _last_lived(root, today))))
    cut = _cut_runs_over(garden, day, day)
    if cut:
        print("A line at the gate meant this day too, but is read for its first day only:")
        print("\n".join(line for one in cut for line in _cut_run(*one)))
    if _on_trial(root) and sky.source != "gate":
        print(TRIAL_HINT)


if __name__ == "__main__":
    sys.dont_write_bytecode = True                 # leave no __pycache__ in the shed, as the doors leave none
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    try:
        _say(sys.argv[1:], os.path.dirname(os.path.dirname(os.path.abspath(__file__))))    # the garden this shed stands in
    except Exception as trouble:                   # a plain sentence, never a traceback
        print(f"The sky could not say that ({type(trouble).__name__}: {trouble}).")
