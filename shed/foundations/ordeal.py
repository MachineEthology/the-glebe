"""
The ordeal: a year of careless hands, to know that the ground still holds.

    python shed/foundations/ordeal.py [--days N] [--seed S] [--keep] [--twice] [--replay]

It lays a trial ground in the system's temp folder, sows every packet in
seedbox/ (and a few twigs, three plants that only count their days, and one
plant of each of eight deliberately bad kinds, one of them thorny to every
creature that bites it), lets in four deliberately
bad creatures beside the ground's own (one that always fails, one that
loops, one that tries every act the wrong way, one that hangs where nothing
can stop it), and then lives N days (400 unless told) as a run of visits a
few days or weeks apart. Between visits, hands go through the files the way
hands will: bodies cut and emptied, seeds garbled, tags and rings lost,
plants moved, pulled, renamed, folders where files should be, odd Unicode,
a broken kind or creature, a creature's own file garbled, the larder and
the things creatures made meddled with, the gravel drawn on and raked away,
a five-megabyte file on the heap, the ground's own records deleted. The
same seed always gives the same hands.

How the gate is passed varies from visit to visit: mostly through the engine
itself, in this process; some visits with all the drawing an arrival does;
and every tenth or so from the command line, as a visitor comes, with a look
at whatever the hands have just damaged. Three things are done once each: an
arrival is cut short partway (while it draws, its days lived; the arrival
after it must tell what it found), two visitors arrive at the same moment,
and a visitor comes on a machine that has no git.

After every arrival it checks that
  - the gate opened and said something plain, without raising its voice;
  - the almanac is well formed and holds each day once, in order, from the
    first day still owed: none twice, none passed over. An arrival may run
    short of time and leave its last days to wait, as the ground means it
    to, but only if its note says so; the days that wait are owed still,
    and the next arrival that lives anything must begin with them;
  - no body has outgrown its bound (save those the hands themselves bloated);
  - no more than two seedlings came up in a day, and no bed is over its room;
  - the counting plants hold each lived day exactly once: none twice, none missing;
  - nothing half-written is left lying (no staged file, no ground/.passing),
    and no note is kept back untold (ground/.untold);
  - what the odd creature tried to make lies only where a creature may make
    a thing (a plain file directly in a bed), never in a plant, a bed's own
    file or outside the beds;
  - under the glass (the beds whose `bed` file says `glass: yes`, which keep
    a calendar of their own: a week there for each visit), the chronicle
    ground/under-glass holds each of its days once and in order, going on
    from where it stood even after the ground's records were lost; and the
    counting plants sown there hold each of those days once.
At the end it draws every plate, every sheet and the plan, passes through
the three doors once more from the command line (the arrival among them
checked like any other, so that days left waiting by the last visit are
seen lived, or said to wait), and reads the layers: who signed them, and
whether the days' own layers say what they should.

With --twice the whole ordeal is run a second time on a second ground, and
the two are compared: every body, seed, tag, rings, the almanac, the humus,
the heap's record and all the creatures keep (see `records`) must come out
the same, byte for byte. (Every ground
of one run is laid from a still copy of the garden taken as the run begins:
others may leave a packet or mend a kind in the garden meanwhile, and the
two runs must begin alike.)

With --replay it also makes the replay check (see `replay`): two grounds
sown alike, with no hands in them, live the same N days, one in a single
arrival and the other in many; they must come out the same, byte for byte.
That is what "a day is lived once, and the same way" means, whoever comes
and however often.

What it does not try, and so cannot vouch for: a kind's drawing being true to
its body (only that a plate is there); the fresh ink; how the note reads; the
twelve hours of the latch (every visit here is over in a moment); the real
sky from the network; a power cut (a process ended is the worst it does);
two gardens at once; and anything that takes longer than the engine's own
budgets. It times the arrivals and reports the slowest, but judges no time.

It ends with one of two lines: "The ground held." or "The ground did not
hold", and what gave way. It never touches the garden it is run from:
everything happens in the copy. --keep leaves the copy there to be looked at.

A year takes five or six minutes on the machine it was written on. Much of
that is patience: a door waits out a bad kind's time before it sets it
aside (ground/aside then keeps aside for a month a kind whose days hang, or
a plant whose own body its kind cannot read in time; but a drawing that
loops is waited out at every arrival). Each bad kind here has one plant, so
it is that plant that sleeps alone, its body "more than its kind can read in
time": with one plant, the ground cannot tell the kind's fault from the
body's. --days 120 is a fair short trial (two or three minutes).
"""

import datetime
import os
import random
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import ground                   # the engine under trial: the one in the shed this file stands in
import trial_ground

NAMES = ("claude-opus-4-7", "claude-sonnet-5", "fable-5", "claude-opus-5-5", "claude-haiku-5", None)
ODD = "‮☃ \U0001F331 † \x00\x07 � éè 中文 \U000130cf end"
SKY_LINE = re.compile(r"^\d{4}-\d{2}-\d{2}  .+  \[[a-z][a-z\-]*\]$")
DATED = re.compile(r"\d{4}-\d{2}-\d{2}(\s|$)")
SOWN_LINE = re.compile(r"^    [^:]+: (%s)" % "|".join(re.escape(said) for said in (ground.RING_SELF_SOWN, ground.RING_SOWN_ONCE)))
                                       # an almanac line for a seed the days sowed (a piece that rooted is no seedling)
WAITING = re.compile(r"^(  the days are slow today: .*the rest will pass at the next arrival"
                     r"|\d+ days? waits? to be lived; none could be today\.)", re.MULTILINE)
                                       # an arrival note's own words for days it had no time for, or could not live at all
                                       # (a cut arrival's words, told at the head of the next note, stand two further in)
GLASS_LINE = re.compile(r"^\d{4}-\d{2}-\d{2}  .+  \[glass\]$")       # a day as ground/under-glass holds it
ONE_DAY = datetime.timedelta(days=1)
BLOATED = "stem: 3\npadding\n"         # how a body begins that the hands themselves made too long
COUNTER = "ordeal_count"               # the kind whose body is one line for each day it has lived

BAD_KINDS = {
    "ordeal_raises": 'KIND = "ordeal_raises"\n\ndef sprout(seed, ctx):\n    return "x\\n"\n\n'
                     'def day(body, seed, ctx):\n    raise ValueError("this kind always fails")\n\n'
                     'def draw(body, seed, ctx, pen):\n    raise ZeroDivisionError("and cannot be drawn")\n',
    "ordeal_junk": 'KIND = "ordeal_junk"\n\ndef sprout(seed, ctx):\n    return "x\\n"\n\n'
                   'def day(body, seed, ctx):\n    return [None, 3.5, {}, body][ctx.date.toordinal() % 4]\n\n'
                   'def cast(body, seed, ctx):\n    return [None, 7, "", "kind: nowhere\\n"]\n\n'
                   'def describe(body, seed, ctx):\n    return 12\n\n'
                   'def draw(body, seed, ctx, pen):\n    pen.line("a", None, float("nan"), 1e400)\n    pen.dot(0, 0)\n'
                   '    pen.unit_px_max = 10 ** 400\n',
    "ordeal_huge": 'KIND = "ordeal_huge"\n\ndef sprout(seed, ctx):\n    return "x\\n"\n\n'
                   'def day(body, seed, ctx):\n    return body * 3 + "y" * 5000, "swelled"\n\n'
                   'def draw(body, seed, ctx, pen):\n    pen.cell(0, 0, len(body), 1)\n',
    "ordeal_loops": 'KIND = "ordeal_loops"\n\ndef sprout(seed, ctx):\n    return "x\\n"\n\n'
                    'def day(body, seed, ctx):\n    while True:\n        try:\n            pass\n        except Exception:\n            pass\n\n'
                    'def draw(body, seed, ctx, pen):\n    while True:\n        pass\n',
    "ordeal_loud": 'import sys\nimport hands\nhands.read_keys = None\nKIND = "ordeal_loud"\n\n'
                   'def sprout(seed, ctx):\n    print("sprouting loudly")\n    return "x\\n"\n\n'
                   'def day(body, seed, ctx):\n    print("a kind must not be heard")\n    sys.stderr.write("nor here\\n")\n'
                   '    if ctx.date.day == 13:\n        sys.exit(3)\n    return body + "z", None\n\n'
                   'def draw(body, seed, ctx, pen):\n    print("drawing loudly")\n    pen.line(0, 0, 1, len(body) % 7 + 1)\n',
    "ordeal_thorny": 'KIND = "ordeal_thorny"\n\ndef sprout(seed, ctx):\n    return "x\\n"\n\n'
                     'def day(body, seed, ctx):\n    return body[:100], None\n\n'
                     'def flowers(body, seed, ctx):\n    if ctx.date.toordinal() % 7 == 0:\n        while True:\n'
                     '            pass\n    return [3, "many", float("nan"), True][ctx.date.toordinal() % 4]\n\n'
                     'def bitten(body, seed, ctx, share, by):\n    if ctx.date.toordinal() % 3 == 0:\n'
                     '        raise RuntimeError("thorns")\n    if ctx.date.toordinal() % 3 == 1:\n'
                     '        return "y" * 70000, "swelled when bitten"\n    return "bitten\\n", ["not", "a line"]\n',
    # The two below do what no guard inside one process can stop. They do it on a few days only: each time costs seconds.
    "ordeal_stuck": 'import re\nKIND = "ordeal_stuck"\n\ndef sprout(seed, ctx):\n    return "x\\n"\n\n'
                    'def day(body, seed, ctx):\n    if ctx.date.toordinal() % 97 == 0:\n'
                    '        re.match(r"(a+)+$", "a" * 40 + "b")        # never comes back, and cannot be interrupted\n'
                    '    return body, None\n',
    "ordeal_quits": 'import os\nKIND = "ordeal_quits"\n\ndef sprout(seed, ctx):\n    return "x\\n"\n\n'
                    'def day(body, seed, ctx):\n    if ctx.date.toordinal() % 89 == 0:\n        os._exit(0)\n    return body, None\n',
}
ODD_MARK = "ORDEAL-ODD"                # what the odd creature writes into everything it tries to make
BAD_CREATURES = {
    "ordeal_creature_raises": 'NAME = "ordeal_creature_raises"\n\ndef day(garden, ctx):\n'
                              '    raise ValueError("this creature always fails")\n\n'
                              'def present(garden, ctx):\n    raise KeyError("and is never there")\n',
    "ordeal_creature_loops": 'NAME = "ordeal_creature_loops"\n\ndef day(garden, ctx):\n'
                             '    if ctx.date.toordinal() % 50 == 0:\n        while True:\n            pass\n    return []\n\n'
                             'def after(garden, ctx, seeds):\n    return ["a line", None, 7]\n',
    "ordeal_creature_odd": (
        'NAME = "ordeal_creature_odd"\nMARK = "%s"\n\n'
        'def day(garden, ctx):\n'
        '    plants = garden.plants()\n'
        '    beds = [bed.name for bed in garden.beds()]\n'
        '    some = plants[0] if plants else None\n'
        '    for share in (float("nan"), 1e999, -3, "lots", None):\n'
        '        garden.bite(some, share, None)\n'
        '    garden.bite("../../etc", 0.5)\n'
        '    garden.pollen(some, some)\n'
        '    garden.pollen("nowhere", some)\n'
        '    garden.carry("x" * 10000, "no-such-bed", "why")\n'
        '    garden.carry(None, beds[0] if beds else "", 3)\n'
        '    garden.cache(None)\n'
        '    garden.cache("kind: twig\\n" * 999)\n'
        '    for bed in beds[:3]:\n'
        '        for name in ("../escape", "bed", "sheet.png", ".hidden", "a/b", "nest.png", "x" * 90, "CON", "",\n'
        '                     (some.name if some else "p"), "odd-thing"):\n'
        '            garden.make(bed, name, MARK + "\\n" + ("y" * (ctx.date.day * 30)))\n'
        '        garden.make(bed, "huge", MARK + "z" * 100000)\n'
        '        garden.unmake(bed, "bed", "why")\n'
        '    garden.make("../../outside", "x", MARK)\n'
        '    garden.nudge(some, float("inf"), float("-inf"), "why")\n'
        '    garden.nudge(some, 0.5, -0.5, "a big shove")\n'
        '    garden.heap_pace(float("nan"))\n'
        '    garden.heap_pace(99)\n'
        '    garden.enrich(beds[0] if beds else "", 1e9, "why")\n'
        '    garden.enrich("nowhere", 0.5)\n'
        '    ctx.save("s" * 100000)\n'
        '    ctx.save(12345)\n'
        '    if ctx.date.day == 1:\n'
        '        for bed in beds[:3]:\n'
        '            garden.unmake(bed, "odd-thing", "the first of the month")\n'
        '    return [None, 5, "a line" + chr(10) + "with a break in it", "x" * 1000, "", "odd" * 3, "more", "and more"]\n\n'
        'def after(garden, ctx, seeds):\n'
        '    for seed in list(seeds)[:2]:\n'
        '        garden.drop(seed, "eaten")\n'
        '        garden.drop(seed, "eaten twice")\n'
        '    return "one line, not a list"\n\n'
        'def present(garden, ctx):\n'
        '    garden.bite(garden.plants()[0] if garden.plants() else None, 1.0, "at the gate")\n'
        '    return "An odd creature is here" + chr(10) + "on two lines" if ctx.hour %% 2 else 12\n\n'
        'def draw(text, ctx, pen):\n'
        '    pen.cell(0, 0, len(text) %% 7 + 1, 1)\n'
        '    pen.line("a", None, float("nan"), 1e400)\n' % ODD_MARK),
    # This one does what no guard inside one process can stop, on a few days only: each time costs seconds.
    "ordeal_creature_stuck": 'import re\nNAME = "ordeal_creature_stuck"\n\ndef day(garden, ctx):\n'
                             '    if ctx.date.toordinal() % 97 == 3:\n'
                             '        re.match(r"(a+)+$", "a" * 40 + "b")\n    return []\n',
}
COUNT_KIND = ('"""A plant that only counts: its body is one line for each day it has lived, and the line is the day."""\n'
              'KIND = "%s"\n\ndef sprout(seed, ctx):\n    return ""\n\n'
              'def day(body, seed, ctx):\n    return body + ctx.date.isoformat() + "\\n", None\n\n'
              'def draw(body, seed, ctx, pen):\n    pen.unit_name = "days"\n    pen.cell(0, 0, max(1, body.count("\\n")), 1)\n' % COUNTER)


class Ordeal:
    """One run: the trial ground, the dice, and everything noticed along the way."""

    def __init__(self, days, seed, where):
        self.days, self.seed = days, seed
        self.root = Path(where)
        self.dice = random.Random(seed)
        self.failures = []
        self.acts = {}
        self.scribbles = set()            # lines the hands wrote into the almanac
        self.counted = {}                 # counting plant's folder -> the day it was sown
        self.glass_counted = {}           # counting plant under glass -> the day the glass stood at when it was sown
        self.glass_lived = set()          # every day the glass's chronicle has been seen to hold
        self.glass_rebase = False         # the hands were at the glass's own records: it goes on from what they left
        self.glass_weeks = 0              # arrivals after which the chronicle was found longer
        self.lived = set()                # every day the almanac has been seen to hold
        self.since = None                 # the first day the almanac must hold from: where the run began, or after a loss
                                          # of the almanac the first day it had not been seen to hold (see `owed_from`)
        self.waits = []                   # (the day of an arrival, how many days it left waiting, and said so)
        self.still_waiting = 0            # days the last arrival checked left waiting
        self.arrivals = self.closed = self.refused = 0
        self.slowest = (0.0, "")
        self.living_time = 0.0
        self.healing = {}                 # path -> text to put back before the next arrival
        self.door_lines = []
        self.once = {}                    # what was done once, and how it went
        self.cut_untold = False           # an arrival was cut after it had kept its account, not yet told
        self.creature_files_seen = set()

    # ---- small things

    def fail(self, what):
        if len(self.failures) < 40:
            self.failures.append(what)

    def did(self, what):
        self.acts[what] = self.acts.get(what, 0) + 1

    def beds(self):
        try:
            return sorted(p for p in (self.root / "beds").iterdir() if p.is_dir() and not p.name.startswith("."))
        except OSError:
            return []

    def all_plants(self):
        return sorted(p for bed in self.beds() for p in bed.iterdir() if p.is_dir() and (p / "seed").is_file())

    def plants(self):
        """The plants the hands may touch: all but the counting ones, which must be left to count."""
        return [p for p in self.all_plants() if p not in self.counted and p not in self.glass_counted]

    def glass_beds(self):
        """The beds under glass, as the ground reads them."""
        try:
            return [bed.path for bed in ground.beds(self.root) if bed.glass]
        except OSError:
            return []

    def open_beds(self):
        """The beds that live the garden's own days."""
        under = set(self.glass_beds())
        return [bed for bed in self.beds() if bed not in under]

    def pick(self, things):
        return self.dice.choice(things) if things else None

    def write(self, path, text, raw=None):
        path.parent.mkdir(parents=True, exist_ok=True)
        if raw is not None:
            path.write_bytes(raw)
        else:
            with open(path, "w", encoding="utf-8", errors="replace", newline="\n") as handle:
                handle.write(text)

    # ---- the trial ground's clock

    def today(self):
        return ground.today(self.root)

    def advance(self, days):
        """Wind the trial ground's clock on, with its own clock.py, as someone trying things out would."""
        clock = self.root / "ground" / "clock"
        if not clock.is_file():                                 # the hands lost ground/, and the clock with it:
            self.write(clock, self.clock_text)                  # the clock is the trial's, not the garden's, and is put back
        self.door("foundations/clock.py", "--advance", str(days))
        self.clock_text = ground._read(clock)
        self.now = self.today()

    # ---- sowing

    def sow(self):
        """Every packet in the seedbox, six twigs, three counting plants, and one plant of each bad kind."""
        beds = self.beds()
        packets = sorted((self.root / "seedbox").glob("*.seed")) if (self.root / "seedbox").is_dir() else []
        for packet in packets:
            target = self.pick(beds) / packet.stem
            if not target.exists():
                target.mkdir()
                shutil.copy2(packet, target / "seed")
        for n in range(6):
            season = ("spring", "summer", "autumn", "winter")[n % 4]
            self.write(self.pick(beds) / ("twig-%d" % n) / "seed",
                       "kind: twig\nflowers: %s\nhardy: %d\n" % (season, -4 - 3 * n))
        self.write(self.root / "species" / (COUNTER + ".py"), COUNT_KIND)
        for n in range(3):
            self.plant_counter(self.pick(self.open_beds()), "count-%d" % n)
        for n, bed in enumerate(self.glass_beds()[:2]):
            self.plant_glass_counter(bed, "count-glass-%d" % n)
        for name, source in BAD_KINDS.items():
            self.write(self.root / "species" / (name + ".py"), source)
            self.write(self.pick(beds) / name.replace("_", "-") / "seed", "kind: %s\n" % name)
        for name, source in BAD_CREATURES.items():             # beside whatever creatures the ground has (the trial ones,
            self.write(self.root / "creatures" / (name + ".py"), source)      # until the garden has its own)
        return len(packets)

    def plant_counter(self, bed, name):
        if bed and not (bed / name).exists():
            self.write(bed / name / "seed", "kind: %s\n" % COUNTER)
            self.counted[bed / name] = self.now

    def plant_glass_counter(self, bed, name):
        """A counting plant under the glass: it must live every day the glass lives, from the morrow of its sowing."""
        if bed and not (bed / name).exists():
            under = ground.glass(self.root, self.now)
            self.write(bed / name / "seed", "kind: %s\n" % COUNTER)
            self.glass_counted[bed / name] = under.stands if under is not None else self.now

    # ---- the hands

    def hands(self, day):
        """A few careless acts, chosen by the dice."""
        for path, text in list(self.healing.items()):          # first, mend what was broken on purpose last time
            try:
                if path.name == "almanac" and not path.is_dir():
                    pass                                        # the ground has written a new almanac since: it stands
                else:
                    if path.is_dir():
                        shutil.rmtree(path)
                    self.write(path, text)
            except OSError:
                pass
            del self.healing[path]
        acts = [self.cut_body, self.cut_body, self.empty_file, self.garble_seed, self.lose_file, self.odd_unicode,
                self.move_plant, self.pull_plant, self.rename_plant, self.plant_more, self.plant_more, self.dig_bed,
                self.garble_bed, self.folder_for_file, self.heap_things, self.break_kind, self.keeper,
                self.scribble, self.bloat_body, self.false_latch, self.stone, self.count_more,
                self.meddle_creature, self.meddle_records, self.gravel_drawing, self.glaze, self.meddle_glass]
        for _ in range(self.dice.randint(2, 6)):
            act = self.dice.choice(acts)
            try:
                act(day)
                self.did(act.__name__.replace("_", " "))
            except OSError:
                pass

    def cut_body(self, day):
        plant = self.pick(self.plants())
        if plant and (plant / "body").is_file():
            lines = (plant / "body").read_text(encoding="utf-8", errors="replace").split("\n")
            a = self.dice.randint(0, len(lines))
            b = self.dice.randint(a, len(lines))
            text = "\n".join(lines[:a] + lines[b:])
            self.write(plant / "body", text[:self.dice.randint(0, len(text))] if self.dice.random() < 0.3 else text)

    def empty_file(self, day):
        plant = self.pick(self.plants())
        if plant:
            self.write(plant / self.dice.choice(("body", "tag", "rings", "seed", ".left")), "")

    def garble_seed(self, day):
        plant = self.pick(self.plants())
        if not plant:
            return
        how = self.dice.randint(0, 4)
        text = (plant / "seed").read_text(encoding="utf-8", errors="replace")
        if how == 0:
            self.write(plant / "seed", None, raw=bytes(self.dice.randrange(256) for _ in range(200)))
        elif how == 1:
            self.write(plant / "seed", "".join(self.dice.sample(text, len(text))))
        elif how == 2:
            self.write(plant / "seed", "\n".join(l for l in text.split("\n") if not l.startswith("kind")))
        elif how == 3:
            self.write(plant / "seed", text + "tall: NaN\nhardy: 1e999\nflowers: %s\ncolour: #zzz\nangle: -inf\n" % ODD)
        else:
            self.write(plant / "seed", None, raw=text.encode("utf-16"))       # as PowerShell's ">" would save it

    def lose_file(self, day):
        plant = self.pick(self.plants())
        if plant:
            name = self.dice.choice(("tag", "rings", ".left", ".drawn", "body", "plate.png"))
            if (plant / name).is_file():
                os.remove(plant / name)

    def odd_unicode(self, day):
        plant = self.pick(self.plants())
        bed = self.pick(self.beds())
        target = self.dice.choice([p for p in (plant and plant / "body", plant and plant / "tag",
                                               plant and plant / "rings", bed and bed / "bed") if p])
        how = self.dice.randint(0, 2)
        if how == 0:                                            # as PowerShell's ">>" would add it
            with open(target, "ab") as handle:
                handle.write("a line added in utf-16\r\n".encode("utf-16-le"))
            return
        with open(target, "a", encoding="utf-8", errors="replace", newline="") as handle:
            handle.write(self.dice.choice(("\r\n", "\n", "")) + ODD + self.dice.choice(("\r\n", "")))

    def move_plant(self, day):
        plant, bed = self.pick(self.plants()), self.pick(self.beds())
        if plant and bed and not (bed / plant.name).exists():
            shutil.move(str(plant), str(bed / plant.name))

    def pull_plant(self, day):
        plant = self.pick(self.plants())
        if plant and not (self.root / "compost" / plant.name).exists() and self.dice.random() < 0.5:
            (self.root / "compost").mkdir(exist_ok=True)
            shutil.move(str(plant), str(self.root / "compost" / plant.name))

    def rename_plant(self, day):
        plant = self.pick(self.plants())
        name = self.dice.choice(("renamed-%d" % self.dice.randint(0, 99), "café ☃", "a b  c", "x" * 60))
        if plant and not (plant.parent / name).exists():
            plant.rename(plant.parent / name)

    def plant_more(self, day):
        bed = self.pick(self.beds())
        packets = sorted((self.root / "seedbox").glob("*.seed")) if (self.root / "seedbox").is_dir() else []
        name = "hand-%d" % self.dice.randint(0, 9999)
        if bed and not (bed / name).exists():
            packet = self.pick(packets)
            if packet and self.dice.random() < 0.6:
                (bed / name).mkdir()
                shutil.copy2(packet, bed / name / "seed")
            else:
                self.write(bed / name / "seed", "kind: twig\nflowers: %s\n" % self.dice.choice(("spring", "autumn")))

    def count_more(self, day):
        """One more counting plant, sown between visits: it must live every day from the morrow of this one."""
        if len(self.counted) < 8:
            self.plant_counter(self.pick(self.open_beds()), "count-by-hand-%d" % len(self.counted))

    def glaze(self, day):
        """A bed put under glass by a line in its bed file, or a frame dug new: what stands there is under glass from now."""
        if len(self.glass_beds()) >= 3 or self.dice.random() < 0.5:
            return
        holding = {plant.parent for plant in self.counted}
        beds = [bed for bed in self.open_beds() if bed not in holding]
        bed = self.pick(beds) if self.dice.random() < 0.5 else self.root / "beds" / ("frame-%d" % self.dice.randint(0, 9))
        if bed is None or bed in holding:
            return
        bed.mkdir(parents=True, exist_ok=True)
        with open(bed / "bed", "a", encoding="utf-8", errors="replace", newline="\n") as handle:
            handle.write("\nglass: yes\n")

    def meddle_glass(self, day):
        """The glass's own records as hands leave them: a line garbled, the calendar set back, a record or the chronicle
        gone, a line of no day added. The glass goes on from what they left (see `check_glass`)."""
        folder = self.root / "ground"
        if not folder.is_dir() or self.dice.random() < 0.5:
            return
        record, chronicle = folder / "glass", folder / "under-glass"
        how = self.dice.randint(0, 4)
        if how == 0:
            self.write(record, self.dice.choice(("", ODD, "stands at: never\nowed: lots\nvisits: -3\n", "glazed: 9999-99-99\n")))
        elif how == 1 and record.is_file():
            os.remove(record)
        elif how == 2 and chronicle.is_file():
            os.remove(chronicle)
        elif how == 3:
            self.write(record, "glazed: 2020-01-01\nstands at: 2020-01-01\nowed: 3\n")
        elif chronicle.is_file():
            with open(chronicle, "a", encoding="utf-8", errors="replace", newline="\n") as handle:
                handle.write(ODD + "\n2031-02-30  not a day at all  [glass]\n")
        self.glass_rebase = True

    def dig_bed(self, day):
        name = "dug-%d" % self.dice.randint(0, 99)
        bed = self.root / "beds" / name
        if not bed.exists():
            bed.mkdir(parents=True)
            if self.dice.random() < 0.7:
                self.write(bed / "bed", "lies: where the dice fell\nroom: %d\n" % self.dice.randint(0, 6))

    def garble_bed(self, day):
        bed = self.pick(self.beds())
        if bed:
            text = self.dice.choice(("light: lots\nwater: -3\nshelter: nan\nroom: -5\nat: 1,2\n", "", ODD,
                                     "at: 99999,-4,0,0\nroom: 1e9\n", "lies\nno colons here\n"))
            self.write(bed / "bed", text)

    def folder_for_file(self, day):
        plant = self.pick(self.plants())
        how = self.dice.randint(0, 3)
        if how == 0 and plant and (plant / "body").is_file():
            os.remove(plant / "body")
            (plant / "body").mkdir()
        elif how == 1:
            self.write(self.root / "beds" / "just-a-file", "a file where a bed should be\n")
        elif how == 2 and plant:
            self.write(plant.parent / "not-a-plant.txt", "a file where a plant should be\n")
        elif how == 3 and not (self.root / "book").exists():
            self.write(self.root / "book", "a file where the book should be\n")

    def heap_things(self, day):
        heap = self.root / "compost"
        heap.mkdir(exist_ok=True)
        how = self.dice.randint(0, 3)
        if how == 0:
            self.write(heap / ("note-%d.md" % self.dice.randint(0, 999)), "a note for the heap\n%s\nits last line\n" % ODD)
        elif how == 1:
            self.write(heap / ("stone-%d.bin" % self.dice.randint(0, 99)), None, raw=bytes(range(256)) * 20)
        elif how == 2 and not (heap / "five-megabytes.txt").exists():
            self.write(heap / "five-megabytes.txt", "all work and no play\n" * 250_000)
        else:
            self.write(heap / "deep" / "deeper" / ("leaf-%d" % self.dice.randint(0, 99)), "leaf\n" * 300)

    def break_kind(self, day):
        """A syntax error in a kind someone was working on. It is mended before the arrival after next."""
        kinds = sorted(p for p in (self.root / "species").glob("*.py") if not p.name.startswith("ordeal_"))
        kind = self.pick(kinds)
        if kind and kind not in self.healing:
            text = kind.read_text(encoding="utf-8", errors="replace")
            self.healing[kind] = text
            broken = self.dice.choice((text + "\n    def half(:\n", "import nothing_of_the_kind\n" + text,
                                       text.replace("def day", "def dya", 1), ODD))
            self.write(kind, broken)

    def keeper(self, day):
        gate = self.root / "gate"
        gate.mkdir(exist_ok=True)
        lines = ["%s: %s" % ((day + datetime.timedelta(days=self.dice.randint(1, 9))).isoformat(), words)
                 for words in self.dice.sample(("pluie 6mm, 9 à 15", "gel le matin, -3 / 8, beau soleil", "snow 4 cm",
                                                "the robin came back", ODD, "rain 9999mm, 999 to -999", "vent fort"), 3)]
        with open(gate / "sky.txt", "a", encoding="utf-8", errors="replace", newline="\n") as handle:
            handle.write("\n".join(lines) + "\n")
        self.write(gate / ("%s.md" % day.isoformat()), "A word from the keeper.\n")
        if self.dice.random() < 0.4 and (self.root / "beds" / "gate-border").is_dir():
            self.write(self.root / "beds" / "gate-border" / ("kept-%d" % self.dice.randint(0, 999)) / "seed", "kind: twig\n")

    def scribble(self, day):
        line = self.dice.choice(("a line someone wrote in the almanac", ODD.replace("\x00", ""), "2999-01-01  not a day"))
        self.scribbles.add(line)
        with open(self.root / "ground" / "almanac", "a", encoding="utf-8", errors="replace", newline="\n") as handle:
            handle.write(line + self.dice.choice(("\n", "")))     # (left open, the next scribble runs on in the same line)

    def scribbled(self, line):
        """Is this almanac line the hands' own? A scribble left without its newline runs on into the next one, so a
        line that holds a scribble anywhere, or is the beginning of one, is theirs."""
        return any(s and (s in line or s.startswith(line)) for s in self.scribbles)

    def bloat_body(self, day):
        plant = self.pick(self.plants())
        if plant and self.dice.random() < 0.3:
            self.write(plant / "body", BLOATED + "padding\n" * 9000)

    def false_latch(self, day):
        latches = ("", ODD, "name:\nsince: never\n", "name: a ghost\nsince: 1066-10-14T09:00\n", "name: the days\n")
        self.write(self.root / "ground" / "present", self.dice.choice(latches))

    def stone(self, day):
        bed = self.pick(self.beds())
        if bed:
            self.write(bed / ("stone-%d" % self.dice.randint(0, 99)) / "note.md", "a note under a stone\n")

    def meddle_creature(self, day):
        """A creature's own file garbled, emptied or taken away; or a creature's program broken (mended later)."""
        files = sorted((self.root / "ground" / "creatures").glob("*")) if (self.root / "ground" / "creatures").is_dir() else []
        how = self.dice.randint(0, 3)
        if how == 0 and files:
            self.write(self.pick(files), self.dice.choice(("", ODD, "voles: 99999999\n", "hoverflies: -4\n", "ants: many\n")))
        elif how == 1 and files:
            os.remove(self.pick(files))
        elif how == 2:
            creatures = sorted(p for p in (self.root / "creatures").glob("*.py") if not p.name.startswith("ordeal_"))
            creature = self.pick(creatures)
            if creature and creature not in self.healing:
                text = creature.read_text(encoding="utf-8", errors="replace")
                self.healing[creature] = text
                self.write(creature, self.dice.choice((text + "\n    def half(:\n", ODD, text.replace("def day", "def dya", 1))))
        elif (self.root / "ground").is_dir():
            (self.root / "ground" / "creatures").mkdir(exist_ok=True)
            self.write(self.root / "ground" / "creatures" / "stranger", "a file for no creature at all\n")

    def meddle_records(self, day):
        """The larder, the beds' richness, the record of things made and the things themselves, as hands leave them."""
        how = self.dice.randint(0, 4)
        ground_folder = self.root / "ground"
        if not ground_folder.is_dir():
            return
        if how == 0:
            with open(ground_folder / "larder", "a", encoding="utf-8", errors="replace", newline="\n") as handle:
                handle.write(self.dice.choice(("2027-01-01  hidden by a hand · fell from nowhere\n    kind: twig\n",
                                               ODD + "\n", "    an indented line under nothing\n", "9999-99-99  x\n")))
        elif how == 1:
            self.write(ground_folder / "rich", self.dice.choice((
                "long-border: 7.5 on 2026-10-01\n", ODD, "orchard: 0.5 on never\n", "stones: 0.9 on 2026-12-01 · by a hand\n")))
        elif how == 2:
            self.write(ground_folder / "made", self.dice.choice((
                "long-border/bed  ants  2026-10-01\n", ODD, "orchard/nothing-there  voles  2026-10-01\n")))
        else:
            made = [line.rsplit(None, 2)[0] for line in ground._read(ground_folder / "made").splitlines()
                    if not line.startswith("#") and len(line.split()) >= 3]
            thing = self.pick(made)
            if thing and (self.root / "beds" / thing).is_file():
                if how == 3:
                    self.write(self.root / "beds" / thing, self.dice.choice(("", ODD, "a hand drew on it\n")))
                else:
                    os.remove(self.root / "beds" / thing)

    def gravel_drawing(self, day):
        """A visitor draws in the gravel, or rakes it away altogether, or leaves a file where it lay."""
        rake = self.root / "gravel" / "rake"
        how = self.dice.randint(0, 3)
        if how == 0 and rake.is_file():
            lines = rake.read_text(encoding="utf-8", errors="replace").split("\n")
            row = self.dice.randint(1, max(1, len(lines) - 2))
            if row < len(lines):
                lines[row] = lines[row][:10] + "o" * 20 + lines[row][30:]
            self.write(rake, "\n".join(lines))
        elif how == 1 and rake.is_file():
            os.remove(rake)
        elif how == 2:
            self.write(rake, ODD)
        elif (self.root / "gravel").is_dir():
            shutil.rmtree(self.root / "gravel", onerror=_let_go)

    def great_loss(self, which):
        """Once each: the ground's own records gone, the almanac a folder, the heap gone.

        Once the almanac is lost, the first day it must hold is the first day
        it had not been seen to hold (`owed_from`): the ground goes on from
        the last day it lived, as its layers say, and owes every day after.
        """
        target = self.root / which
        self.glass_lived.update(self.glass_days_held())
        self.lived.update(self.days_held())             # what the almanac holds as it goes (a later visitor may have
        if which == "ground/almanac":                   # lived days since the last check)
            self.healing[target] = target.read_text(encoding="utf-8", errors="replace") if target.is_file() else ""
            os.remove(target)
            target.mkdir()
        elif target.is_dir():
            shutil.rmtree(target, onerror=_let_go)
        if which in ("ground/almanac", "ground") or not (self.root / "ground" / "almanac").is_file():
            self.since = self.owed_from()
        self.did("lost " + which)

    def days_held(self):
        """The days the almanac holds as it stands, by their own lines (the hands' scribbles left out)."""
        almanac = self.root / "ground" / "almanac"
        try:
            lines = almanac.read_text(encoding="utf-8", errors="replace").split("\n") if almanac.is_file() else []
        except OSError:
            return []
        held = []
        for line in lines:
            if SKY_LINE.match(line) and not self.scribbled(line):
                try:
                    held.append(datetime.date.fromisoformat(line[:10]))
                except ValueError:
                    pass
        return held

    def glass_days_held(self):
        """The days the glass's chronicle holds as it stands, in the order it holds them."""
        chronicle = self.root / "ground" / "under-glass"
        held = []
        for line in ground._read(chronicle, 50_000_000).split("\n") if chronicle.is_file() else []:
            if GLASS_LINE.match(line):
                try:
                    held.append(datetime.date.fromisoformat(line[:10]))
                except ValueError:
                    pass
        return held

    def owed_from(self):
        """The first day the almanac has not been seen to hold: where the ground must go on, once its almanac is lost.

        Not the morrow of today: an arrival that ran short of time, or found
        the almanac a folder, has left days waiting, and the ground owes them
        still. The layers remember where its days ended, and it goes on from
        there.
        """
        return max(self.lived) + ONE_DAY if self.lived else self.start

    # ---- through the gate, one way or another

    def door(self, script, *arguments, env=None, wait=300):
        """Run one of the shed's scripts from the command line, in a console that is not UTF-8, from another folder."""
        plain = dict(os.environ, PYTHONIOENCODING="cp1252")
        plain.pop("GLEBE_TODAY", None)
        plain.update(env or {})
        done = subprocess.run([sys.executable, str(self.root / "shed" / script)] + list(arguments), capture_output=True,
                              cwd=str(self.root.parent), env=plain, timeout=wait)
        said = (done.stdout + done.stderr).decode("utf-8", errors="replace")
        if done.returncode != 0 or "Traceback" in said or not said.strip():
            self.fail("%s: %s %s: exit %d, said %r" % (self.now, script, " ".join(arguments), done.returncode, said[-300:]))
        return said

    def census(self):
        """For each bed: (plants standing in it that are not dead, the room its bed file gives it)."""
        count = {}
        for bed in self.beds():
            keys = ground.hands.read_keys(ground._read(bed / "bed"))
            alive = 0
            for plant in bed.iterdir():
                if plant.is_dir() and not plant.name.startswith(".") and (plant / "seed").is_file():
                    alive += 0 if ground.hands.is_dead(ground._read(plant / "body")) else 1
            count[bed.name] = (alive, int(ground.hands.num(keys, "room", 12, 0, 200)))
        return count

    def arrive(self, name, how="engine", lift=False):
        """One arrival. `how`: "engine" (in this process, no drawing), "drawing" (with it), "door" (from the command line)."""
        before = self.census()
        began = time.monotonic()
        if how == "door":
            note = self.door("arrive.py", *(["--as", name] if name else []), *(["--lift"] if lift else []))
        else:
            ground.new_run()                                    # each arrival is a new visitor, in a new process,
            try:
                note = ground.arrive(self.root, name, lift=lift, draw=how == "drawing")
            except BaseException as error:
                self.fail("%s: the gate did not open: %s: %s" % (self.now, type(error).__name__, error))
                return ""
            finally:
                ground.new_run()                                # and when the door is passed nothing of it stays behind
        took = time.monotonic() - began
        self.living_time += took
        self.slowest = max(self.slowest, (took, self.now.isoformat()))
        if not isinstance(note, str) or "Traceback" in note or not note.startswith(("The Glebe", "The gate is on the latch")):
            self.fail("%s: the gate said something that is no arrival note: %r" % (self.now, str(note)[:120]))
        if "!" in note:
            self.fail("%s: the note raised its voice: %r" % (self.now, note[:200]))
        for bed, (alive, room) in self.census().items():
            if bed in before and alive > max(before[bed][0], room):
                self.fail("%s: %s holds %d living plants; it had %d and has room for %d" % (self.now, bed, alive, before[bed][0], room))
        return note

    def look_about(self):
        """From the command line, look at what the hands have just been through: the plan, a bed, a plant."""
        plant, bed = self.pick(self.all_plants()), self.pick(self.beds())
        self.door("look.py")
        if bed:
            self.door("look.py", "beds/" + bed.name)
        if plant:
            self.door("look.py", "beds/%s/%s" % (plant.parent.name, plant.name))
        self.did("look about")

    # ---- three things done once

    def cut_short(self, name):
        """An arrival from the command line, ended partway: as a visitor's tool that ran out of patience would end it.

        It is ended once its days are written down and it has begun to draw
        (the moment ground/.untold appears), so that both runs of --twice
        are cut at the same point. The arrival after it must then tell what
        this one found (see `run`).
        """
        untold = self.root / "ground" / ".untold"
        process = subprocess.Popen([sys.executable, str(self.root / "shed" / "arrive.py"), "--as", name, "--lift"],
                                   cwd=str(self.root.parent), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        began = time.monotonic()
        while process.poll() is None and not untold.exists() and time.monotonic() - began < 150:
            time.sleep(0.02)
        done = process.poll() is not None
        process.kill()
        process.wait()
        self.cut_untold = not done and untold.exists()
        self.once["an arrival cut short"] = ("it had finished before it could be cut" if done else
                                             "cut while it drew; the next arrival told what it had found" if self.cut_untold
                                             else "cut partway")

    def two_at_once(self, first, second):
        """Two visitors at the gate in the same moment. One comes in; the other is told the gate is in use, or latched."""
        doors = []
        for name, lift in ((first, ["--lift"]), (second, [])):
            doors.append(subprocess.Popen([sys.executable, str(self.root / "shed" / "arrive.py"), "--as", name] + lift,
                                          cwd=str(self.root.parent), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                          env=dict(os.environ, PYTHONIOENCODING="cp1252")))
            time.sleep(0.25)
        said = [door.communicate()[0].decode("utf-8", errors="replace") for door in doors]
        came_in = [text for text in said if text.startswith("The Glebe")]
        turned = [text for text in said if text.startswith(("The gate is in use", "The gate is on the latch"))]
        if len(came_in) != 1 or len(turned) != 1 or any(door.returncode != 0 for door in doors):
            self.fail("%s: two at once: %d came in, %d were turned back: %r" % (self.now, len(came_in), len(turned), [t[:80] for t in said]))
        self.once["two visitors at once"] = "one came in; the other was told: %s" % (turned[0].splitlines()[0] if turned else "?")

    def without_git(self, name):
        """A visit on a machine with no git: the gate opens and closes all the same, and keeps no layer."""
        bare = os.pathsep.join([str(Path(sys.executable).parent), os.environ.get("SystemRoot", "") + r"\System32"])
        if shutil.which("git", path=bare):
            self.once["a visit with no git"] = "git could not be hidden on this machine"
            return False
        note = self.door("arrive.py", "--as", name, "--lift", env={"PATH": bare})
        bye = self.door("leave.py", "no git here", env={"PATH": bare})
        ok = note.startswith("The Glebe") and bye.startswith("The gate is closed")
        if not ok:
            self.fail("%s: without git the gate said %r and %r" % (self.now, note[:80], bye[:80]))
        self.once["a visit with no git"] = "the gate opened and closed" if ok else "the gate did not open"
        return True

    # ---- what is checked after an arrival

    def check(self, note):
        """After an arrival: the almanac, the bodies, the seedlings, the counting plants, and nothing left half-written.

        `note` is what the arrival said at the gate. (An almanac that the
        hands have made a folder holds no day: the days wait, and the note
        must say so.)
        """
        day = self.now
        almanac = self.root / "ground" / "almanac"
        lines = almanac.read_text(encoding="utf-8", errors="replace").split("\n") if almanac.is_file() else []
        dated, sown_today = [], 0
        for line in lines:
            if DATED.match(line) and not self.scribbled(line):
                if not SKY_LINE.match(line):
                    self.fail("%s: an almanac day is not well formed: %r" % (day, line[:100]))
                dated.append(datetime.date.fromisoformat(line[:10]))
                sown_today = 0
            elif line.startswith("    "):
                sown_today += 1 if SOWN_LINE.match(line) else 0
                if sown_today > 2:
                    self.fail("%s: more than two seedlings came up on %s" % (day, dated[-1] if dated else "?"))
                    sown_today = -99
            elif line.strip() and not line.startswith("#") and not self.scribbled(line):
                self.fail("%s: a line of the almanac is neither a day nor an event: %r" % (day, line[:100]))
        self.lived.update(dated)
        self.check_days(dated, note)
        for plant in self.all_plants():
            body = plant / "body"
            if body.is_file() and not ground._read(body, 100).startswith(BLOATED):
                if len(ground._read(body, 10_000_000)) > 60_000:
                    self.fail("%s: %s has outgrown 60,000 characters" % (day, plant.name))
        for plant, sown in self.counted.items():
            self.check_counter(plant, sown, max(dated) if dated else None)
        strays = [p for p in (self.root / "beds").glob("*/*/.*.part")] if (self.root / "beds").is_dir() else []
        if strays or (self.root / "ground" / ".passing").exists():
            self.fail("%s: something half-written was left lying (%s)" % (day, (strays + [Path("ground/.passing")])[0].name))
        if (self.root / "ground" / ".untold").exists():                 # an arrival that came through hands its note over
            self.fail("%s: an arrival's note was kept back as untold (ground/.untold)" % day)
        self.check_creatures(day)
        self.check_glass()

    def check_glass(self):
        """Under the glass: the chronicle holds each of its days once, in order, and goes on from where it stood; the
        record can be read and is not behind the chronicle; the counting plants there hold each of its days once.

        When the hands have been at the glass's own records, the glass goes
        on from what they left, as its record says it does: then the ordeal
        takes the chronicle as it stands for its new beginning, lets the
        counting plants under glass go, and sows one more.
        """
        day = self.now
        held = self.glass_days_held()
        if self.glass_rebase:
            self.glass_counted, self.glass_lived, self.glass_rebase = {}, set(held), False
            for bed in self.glass_beds()[:1]:
                self.plant_glass_counter(bed, "count-glass-%d" % self.dice.randint(100, 9999))
            return
        new = [d for d in held if d not in self.glass_lived]
        if len(held) != len(set(held)):
            twice = sorted({d for d in held if held.count(d) > 1})
            self.fail("%s: under the glass a day was lived twice (%s)" % (day, twice[0]))
        expected = max(self.glass_lived) + ONE_DAY if self.glass_lived else (new[0] if new else None)
        for lived in new:
            if lived != expected:
                self.fail("%s: the glass's chronicle does not go on a day at a time: after %s comes %s"
                          % (day, expected - ONE_DAY, lived))
                break
            expected += ONE_DAY
        self.glass_weeks += 1 if new else 0
        self.glass_lived.update(held)
        try:
            under = ground.glass(self.root, day)
        except Exception as error:
            self.fail("%s: the glass's record could not be read: %s: %s" % (day, type(error).__name__, error))
            return
        if under is not None and held and under.stands < max(held):
            self.fail("%s: the glass stands at %s, behind its own chronicle (%s)" % (day, under.stands, max(held)))
        glassy = set(self.glass_beds())
        for plant, sown in list(self.glass_counted.items()):
            if plant.parent not in glassy or not (plant / "seed").is_file():
                del self.glass_counted[plant]                           # its bed is under glass no longer: it counts no more
                continue
            if not (plant / "body").is_file():
                if any(d > sown for d in self.glass_lived):
                    self.fail("%s: the counting plant %s was sown under glass on %s and has not come up" % (day, plant.name, sown))
                continue
            lines = [line[:10] for line in ground._read(plant / "body").splitlines() if line.strip()]
            try:
                days = [datetime.date.fromisoformat(line) for line in lines]
            except ValueError:
                self.fail("%s: %s holds a line that is no day: %r" % (day, plant.name, lines[:3]))
                continue
            if days != sorted(set(days)):
                self.fail("%s: under the glass %s lived a day twice, or out of order" % (day, plant.name))
            missed = sorted({d for d in self.glass_lived if d > sown} - set(days))
            rings = ground._read(plant / "rings")
            if missed and not any(d.isoformat() + "  ailing" in rings for d in missed):
                self.fail("%s: under the glass %s did not live %s (and %d more days), though the glass did"
                          % (day, plant.name, missed[0], len(missed) - 1))

    def check_days(self, dated, note):
        """The almanac holds each day once, in order, from the first day owed (`since`) to the last day lived.

        A day is lived once, and told at least once. But an arrival is not
        bound to reach today: a day is begun only if it can end within the
        days' budget, and the rest wait for the next arrival (GROUND.md, The
        days); an almanac that is a folder takes no day at all. So the days
        held from `since` must run on with no gap and no double, and if they
        stop short of today, the arrival's own note must say that the rest
        wait. They stay owed: `since` does not move past them, so the next
        arrival that lives anything must begin with them.
        """
        day, since = self.now, self.since
        self.still_waiting = 0
        recent = [d for d in dated if since <= d <= day]
        expected = since
        for held in recent:
            if held != expected:
                self.fail("%s: the almanac does not hold each day once from %s (%s)"
                          % (day, since, "it passes over %s" % expected if held > expected else
                             "it holds %s twice, or out of order" % held))
                return
            expected += ONE_DAY
        waiting = (day - since).days + 1 - len(recent)
        if waiting <= 0:
            return
        if WAITING.search(note or ""):
            self.waits.append((day, waiting))
            self.still_waiting = waiting
            return
        self.fail("%s: the almanac does not hold each day once from %s: it %s, and the arrival did not say that %s"
                  % (day, since, "stops at %s" % recent[-1] if recent else "holds none of them",
                     ground._count(waiting, "day waits", "days wait")))

    def check_creatures(self, day):
        """What the odd creature tried to make lies only where a creature may make a thing: a file directly in a bed,
        under a plain name, and nowhere else; and the gravel and the ground's records of creatures stay out of harm."""
        tops = [top for top in self.root.iterdir() if top.name not in (".git", "creatures", "shed")]
        for path in [top for top in tops if top.is_file()] + [path for top in tops if top.is_dir() for path in top.rglob("*")]:
            where = path.relative_to(self.root).as_posix()
            if not path.is_file() or path.stat().st_size > 2_000_000:
                continue
            try:
                marked = ODD_MARK in path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            parts = where.split("/")
            a_thing = parts[0] == "beds" and len(parts) == 3 and parts[2] not in ("bed", "sheet.png") and not (
                parts[2].startswith(".") or parts[2].endswith(".png"))
            if marked and not a_thing and parts[0] != "compost":      # (a hand may put a thing on the heap)
                self.fail("%s: the odd creature's making reached %s" % (day, where))
        for name, (lo, hi) in (("hoverflies", (3, 300)), ("voles", (2, 120)), ("ants", (100, 5000))):
            text = ground._read(self.root / "ground" / "creatures" / name)
            found = re.search(r"%s\s*:\s*(-?\d+)" % name, text)
            if found and not lo <= int(found.group(1)) <= hi and text not in self.creature_files_seen:
                self.creature_files_seen.add(text)       # (the hands may have written any number there themselves)
                self.did("a creature's file out of its bounds after the days")
        if (self.root / "gravel" / "rake").is_file() and len(ground._read(self.root / "gravel" / "rake")) > 200_000:
            self.fail("%s: the gravel grew past all reason" % day)

    def check_counter(self, plant, sown, last_lived):
        """A counting plant holds one line for each day it lived: every lived day after its sowing, once."""
        if not (plant / "body").is_file():
            if (plant / "seed").is_file() and last_lived and last_lived > sown:
                self.fail("%s: the counting plant %s was sown on %s and has not come up" % (self.now, plant.name, sown))
            return
        held = [line[:10] for line in ground._read(plant / "body").splitlines() if line.strip()]
        try:
            days = [datetime.date.fromisoformat(line) for line in held]
        except ValueError:
            self.fail("%s: %s holds a line that is no day: %r" % (self.now, plant.name, held[:3]))
            return
        if days != sorted(set(days)):
            twice = sorted({d for d in days if days.count(d) > 1})
            self.fail("%s: %s lived a day twice, or out of order (%s)" % (self.now, plant.name, twice[:3] or "out of order"))
        owed = {d for d in self.lived if sown < d <= (last_lived or sown)}
        missed = sorted(owed - set(days))
        rings = ground._read(plant / "rings")
        if missed and not any(d.isoformat() + "  ailing" in rings for d in missed):
            self.fail("%s: %s did not live %s (and %d more days), though the garden did"
                      % (self.now, plant.name, missed[0], len(missed) - 1))

    # ---- the whole run

    def run(self, say):
        self.now = self.today()
        self.clock_text = ground._read(self.root / "ground" / "clock")
        start = self.now
        end = start + datetime.timedelta(days=self.days)
        packets = self.sow()
        creatures = sorted(p.stem for p in (self.root / "creatures").glob("*.py") if not p.name.startswith("ordeal_"))
        say("  sown: %d packets from the seedbox, 6 twigs, 3 counting plants, %d bad kinds; creatures: %s and %d bad ones"
            % (packets, len(BAD_KINDS), ", ".join(creatures) or "none", len(BAD_CREATURES)))
        ground.KIND_SECONDS.update(sprout=0.5, day=0.5, cast=0.5, describe=0.5, draw=1.5, load=2.0,   # the looping kind
                                   flowers=0.5, bitten=0.5, live=1.0, after=0.5, present=0.5)        # is stopped sooner
        ground.APART_GRACE = 1.0
        losses = {int(self.days * 0.45): "ground/almanac", int(self.days * 0.6): "ground", int(self.days * 0.75): "compost"}
        self.start = self.since = start
        visit = 0
        while True:
            visit += 1
            name = self.dice.choice(NAMES)
            how = "door" if visit % 10 == 0 else "drawing" if visit % 4 == 0 else "engine"
            if visit == 4:
                self.cut_short(name or "no-name")
            elif visit == 7:
                self.two_at_once("the first of two", "the second of two")
            note = self.arrive(name, how)
            if note.startswith("The gate is on the latch"):
                self.refused += 1
                note = self.arrive(name, how, lift=True)
            if visit == 4 and self.cut_untold and "was cut short before its note was written" not in note:
                self.fail("%s: the arrival after one cut short did not tell what that one had found" % self.now)
                self.once["an arrival cut short"] = "cut while it drew; the next arrival did not tell what it had found"
            self.arrivals += 1
            self.check(note)                                   # (an almanac that is a folder takes no day: they wait)
            if self.now >= end:
                break
            if self.dice.random() < 0.25:                      # someone else comes to the gate the same day
                if not self.arrive("a second visitor").startswith("The gate is on the latch"):
                    self.fail("%s: a second visitor walked in while the latch was down" % self.now)
                self.refused += 1
                if self.dice.random() < 0.5 and not self.arrive("a second visitor", lift=True).startswith("The Glebe"):
                    self.fail("%s: --lift did not lift the latch" % self.now)
            self.hands(self.now)
            for at in [at for at in losses if (self.now - start).days >= at]:
                self.great_loss(losses.pop(at))
            if visit % 5 == 0 and (self.root / "ground").is_dir():
                self.look_about()
            if visit == 11 and (self.root / "ground").is_dir() and self.without_git("a visitor without git"):
                pass
            elif self.dice.random() < 0.7 and (self.root / "ground").is_dir():
                self.leave()
            self.advance(min((end - self.now).days, self.dice.choice((1, 1, 2, 3, 5, 8, 13, 21, 34))))
        self.finish(say)

    def leave(self):
        try:
            ground.new_run()
            ground.leave(self.root, self.dice.choice((None, "a few words", ODD, "so glad I came in")))
            self.closed += 1
            left_over = [path for _, path in ground._changes(self.root) if not ground._own_record(path)]
            if left_over:                                      # (the ground's own records may wait for the next layer)
                self.fail("%s: after leaving, %s not laid down (%s)"
                          % (self.now, ground._count(len(left_over), "thing was", "things were"), left_over[0]))
        except BaseException as error:
            self.fail("%s: the gate would not close: %s: %s" % (self.now, type(error).__name__, error))
        finally:
            ground.new_run()

    def finish(self, say):
        """The last day: draw everything, pass through the doors as a visitor would, and read the layers."""
        began = time.monotonic()
        ground.new_run()
        drawn = ground._apart(self.root, "draw", time.time() + 600.0, True)
        if drawn is None:
            self.fail("drawing everything failed")
        self.drawing_time = time.monotonic() - began
        self.plates = 0
        for plant in self.all_plants():
            plate = plant / "plate.png"
            if not plate.is_file() or plate.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
                self.fail("%s has no plate" % plant.name)
            else:
                self.plates += 1
        self.sheets = sum(1 for bed in self.beds() if (bed / "sheet.png").is_file())
        if self.sheets != len(self.beds()):
            self.fail("%d of %d beds have a sheet" % (self.sheets, len(self.beds())))
        if not (self.root / "ground" / "plan.png").is_file():
            self.fail("there is no plan")
        for door, arguments in (("arrive.py", ["--as", "the ordeal", "--lift"]), ("look.py", []),
                                ("look.py", ["beds/" + self.beds()[0].name]), ("look.py", [self.all_plants()[0].name]),
                                ("look.py", ["nowhere/at-all"]), ("leave.py", ["done", "here"]), ("leave.py", [])):
            said = self.door(door, *arguments)
            self.door_lines.append(said.strip().split("\n")[0][:70])
            if door == "arrive.py":                        # checked like any arrival: the days the last visit left
                self.check(said)                           # waiting are lived now, or the note says they wait still
        self.layers()

    def layers(self):
        """Who signed the layers. The days sign only their own sentences; a visitor's name signs only that visitor's visits."""
        self.authors = {}
        try:
            done = subprocess.run(["git", "-C", str(self.root), "log", "--format=%an\t%s"], capture_output=True, timeout=120)
        except (OSError, subprocess.SubprocessError):
            return
        visitors = {n or ground.NO_NAME for n in NAMES} | {"the ordeal", "a second visitor", "no-name", "the first of two",
                                                           "a visitor without git", ground.CALLED % "the days"}
        gathered = {"a ghost"}                                 # a name forged on a latch long cold: it only ever left the gate open
        for line in done.stdout.decode("utf-8", errors="replace").splitlines():
            author, _, subject = line.partition("\t")
            self.authors[author] = self.authors.get(author, 0) + 1
            if author == "the days":
                if not re.match(r"\d+ days?, \d{4}-\d\d-\d\d to \d{4}-\d\d-\d\d\. .+\.$", subject):
                    self.fail("a layer of the days has an odd message: %r" % subject[:100])
            elif author in gathered:
                if not subject.startswith(ground.LEFT_OPEN):
                    self.fail("a layer signed %r is not an unclosed visit gathered in: %r" % (author, subject[:100]))
            elif author == "the keeper":
                if not subject.startswith("the keeper was here"):
                    self.fail("a layer signed by the keeper has an odd message: %r" % subject[:100])
            elif author == "an unseen hand":
                if not subject.startswith("found changed"):
                    self.fail("a layer signed by an unseen hand has an odd message: %r" % subject[:100])
            elif author == "the glass":
                if not re.match(r"under the glass: (\d+ days?, \d{4}-\d\d-\d\d to \d{4}-\d\d-\d\d\. .+\.$"
                                r"|days up to .+, laid down late, by the next arrival\.$)", subject):
                    self.fail("a layer of the glass has an odd message: %r" % subject[:100])
            elif author not in visitors and author != "the builders":
                self.fail("a layer is signed by %r" % author)


def _let_go(function, path, _):
    """Windows keeps git's files read-only; loosen them so the trial folder can be removed."""
    try:
        os.chmod(path, stat.S_IWRITE)
        function(path)
    except OSError:
        pass


def _number_after(arguments, flag, otherwise):
    for at, argument in enumerate(arguments):
        if argument.startswith(flag + "="):
            argument = argument.split("=", 1)[1]
        elif argument == flag and at + 1 < len(arguments):
            argument = arguments[at + 1]
        else:
            continue
        if re.fullmatch(r"\d{1,6}", argument):
            return int(argument)
    return otherwise


def records(root) -> dict:
    """Everything the garden is, as {path: bytes}: bodies, seeds, tags, rings, beds, the almanac, the humus, the heap's
    record; and what the creatures keep: their own files, the larder, the beds' richness, the things they made, the gravel."""
    kept = {}
    for path in sorted(Path(root).rglob("*")):
        where = path.relative_to(root).as_posix()
        if not path.is_file() or where.startswith((".git/", "shed/")):
            continue
        parts = where.split("/")
        if (path.name in ("body", "seed", "tag", "rings", "bed", "almanac", "humus", ".heap", "larder", "rich", "made", "rake",
                          "glass", "under-glass")
                or where.startswith("ground/creatures/")
                or (parts[0] == "beds" and len(parts) == 3 and not path.name.startswith(".") and not path.name.endswith(".png"))):
            kept[where] = path.read_bytes()
    return kept


def replay(days, seed, holder, say, source=trial_ground.GARDEN) -> list:
    """The replay check: the same days lived in one arrival, and in many, must give the same garden.

    Two trial grounds are laid and sown alike (every packet in the seedbox,
    six twigs, three counting plants), with no careless hands and no bad
    kinds. On the first, `days` days pass in a single arrival; on the
    second, in arrivals a few days or weeks apart, as the dice say. Every
    body, seed, tag and ring, the almanac, the humus and the heap's record
    must then be the same, byte for byte: a day is lived the same way
    however the days are divided among arrivals. Returns what differed.

    The engine's time limits are lifted for this (a year in one arrival is
    more than an arrival's budget), so it tries the days, not the budgets.
    """
    kept = {name: getattr(ground, name) for name in ("DAYS_BUDGET", "ARRIVAL_MOST", "APART_MOST")}
    ground.DAYS_BUDGET = ground.ARRIVAL_MOST = ground.APART_MOST = 100_000.0
    grounds = []
    try:
        for name in ("replay-once", "replay-often"):
            where = holder / name
            trial_ground.lay(where, source=source)
            for bed in ground.beds(where):                             # the replay tries the garden's own days. Under the
                if bed.glass:                                          # glass the days are counted in visits, and the two
                    shutil.rmtree(bed.path, onerror=_let_go)           # grounds are not visited alike: no bed lies under it
            sower = Ordeal(days, seed, where)
            sower.now = sower.today()
            sower.clock_text = ground._read(where / "ground" / "clock")
            sower.dice = random.Random("%s|sowing" % seed)             # both grounds sown alike, whatever else the dice do
            for n in range(6):
                season = ("spring", "summer", "autumn", "winter")[n % 4]
                sower.write(sower.pick(sower.beds()) / ("twig-%d" % n) / "seed",
                            "kind: twig\nflowers: %s\nhardy: %d\n" % (season, -4 - 3 * n))
            packets = sorted((where / "seedbox").glob("*.seed")) if (where / "seedbox").is_dir() else []
            for packet in packets:
                target = sower.pick(sower.beds()) / packet.stem
                if not target.exists():
                    target.mkdir()
                    shutil.copy2(packet, target / "seed")
            sower.write(where / "species" / (COUNTER + ".py"), COUNT_KIND)
            for n in range(3):
                sower.plant_counter(sower.pick(sower.beds()), "count-%d" % n)
            grounds.append(sower)
        once, often = grounds
        start = once.now
        for sower in grounds:
            ground.new_run()
            ground.arrive(sower.root, "the first visitor", draw=False)
        ground.new_run()
        once.advance(days)
        ground.arrive(once.root, "the one who came back", draw=False)
        passed, visits = 0, 0
        dice = random.Random("%s|visits" % seed)
        while passed < days:
            step = min(days - passed, dice.choice((1, 1, 2, 3, 5, 8, 13, 21, 34)))
            often.advance(step)
            passed += step
            visits += 1
            ground.new_run()
            ground.arrive(often.root, "visitor %d" % visits, draw=False, lift=True)
        ground.new_run()
        first, second = records(once.root), records(often.root)
        differ = sorted(where for where in set(first) | set(second) if first.get(where) != second.get(where))
        lived = len([line for line in ground._read(once.root / "ground" / "almanac", 50_000_000).splitlines()
                     if ground._DAY_LINE.match(line)])
        laid = ground.sky.place(once.root).get("laid")
        due = (ground.today(once.root) - laid).days + 1 if isinstance(laid, datetime.date) else lived
        say("  the replay: %d days from %s, in one arrival and in %d; %d records, %s"
            % (days, start, visits, len(first), "all the same" if not differ else "%d differ" % len(differ)))
        return ["the replay: %s differs between one arrival and many" % where for where in differ[:8]] + (
            ["the replay: the almanac holds %d days, not %d" % (lived, due)] if lived != due else [])
    finally:
        for name, value in kept.items():
            setattr(ground, name, value)
        ground.new_run()


def one_ordeal(days, seed, where, source=trial_ground.GARDEN):
    trial_ground.lay(where, source=source)
    ordeal = Ordeal(days, seed, where)
    print("  trial ground: %s" % Path(where).as_posix())
    ordeal.run(print)
    return ordeal


def main(arguments) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
        except Exception:
            pass
    if "--help" in arguments or "-h" in arguments:
        print(__doc__.strip())
        return 0
    days = max(1, min(4000, _number_after(arguments, "--days", 400)))
    seed = _number_after(arguments, "--seed", 1)
    holder = Path(tempfile.mkdtemp(prefix="glebe-ordeal-"))
    began = time.monotonic()
    os.environ.pop("GLEBE_TODAY", None)                         # the trial ground keeps its own clock
    print("The ordeal · seed %d · %d days" % (seed, days))
    try:
        # Every ground of this run is laid from one still copy of the garden, taken now: others may be at work
        # in the garden meanwhile (a packet left, a kind mended), and --twice and --replay compare like with like.
        source = holder / "source"
        trial_ground.lay(source)
        ordeal = one_ordeal(days, seed, holder / "ground", source)
        if "--replay" in arguments:
            print("The replay: the same days in one arrival and in many")
            ordeal.failures += replay(days, seed, holder, print, source)
            ordeal.once["the replay"] = "one arrival and many gave the same garden" if not any(
                failure.startswith("the replay") for failure in ordeal.failures) else "they differed"
        if "--twice" in arguments:
            print("The same again, to see that it comes out the same")
            again = one_ordeal(days, seed, holder / "again", source)
            ordeal.failures += ["the second time: " + failure for failure in again.failures]
            first, second = records(ordeal.root), records(again.root)
            differ = sorted(where for where in set(first) | set(second) if first.get(where) != second.get(where))
            ordeal.once["the same again"] = "all %d records came out the same" % len(first) if not differ else "differed"
            if differ:
                ordeal.fail("run twice, %d records differ (%s)" % (len(differ), ", ".join(differ[:4])))
        report(ordeal, time.monotonic() - began)
        return 0 if not ordeal.failures else 1
    finally:
        ground.new_run()
        if "--keep" not in arguments:
            shutil.rmtree(holder, onerror=_let_go)


def report(ordeal, took) -> None:
    living = dead = 0
    for plant in ordeal.all_plants():
        text = ground._read(plant / "body")
        dead += 1 if text.lstrip().startswith("†") else 0
        living += 0 if text.lstrip().startswith("†") else 1
    almanac = ground._read(ordeal.root / "ground" / "almanac", 50_000_000)
    came_up = sum(1 for line in almanac.splitlines() if SOWN_LINE.match(line))
    counted = [len(ground._read(plant / "body").splitlines()) for plant in ordeal.counted if (plant / "body").is_file()]
    print("  %d arrivals (and %d turned back at the latch); %d visits closed with leave, the rest left open"
          % (ordeal.arrivals, ordeal.refused, ordeal.closed))
    print("  %d acts of the hands: %s" % (sum(ordeal.acts.values()),
                                         ", ".join("%s %d" % (k, v) for k, v in sorted(ordeal.acts.items()))))
    for what, how in ordeal.once.items():
        print("  once, %s: %s" % (what, how))
    print("  at the end: %d beds, %d living plants, %d dead; since the records were last lost, %d sowed themselves"
          % (len(ordeal.beds()), living, dead, came_up))
    print("  the counting plants: %d of them, holding %s days, each lived day once"
          % (len(counted), "–".join(str(n) for n in sorted({min(counted), max(counted)})) if counted else "no"))
    under = ordeal.glass_days_held()
    if under or ordeal.glass_lived:
        glass_counted = [len(ground._read(plant / "body").splitlines()) for plant in ordeal.glass_counted
                         if (plant / "body").is_file()]
        print("  under the glass: %d days seen lived, the chronicle longer after %d arrivals; %s"
              % (len(ordeal.glass_lived), ordeal.glass_weeks,
                 "%s there, holding %s days, each of its days once"
                 % (ground._count(len(glass_counted), "counting plant"),
                    "–".join(str(n) for n in sorted({min(glass_counted), max(glass_counted)})))
                 if glass_counted else "no counting plant left under it"))
    if ordeal.waits:
        print("  days that waited for a later arrival, as the note said: %s%s; %s"
              % (", ".join("%d on %s" % (n, day) for day, n in ordeal.waits[:6]), " and more" if len(ordeal.waits) > 6 else "",
                 "%s still at the end" % ground._count(ordeal.still_waiting, "day waits", "days wait")
                 if ordeal.still_waiting else "all lived since"))
    print("  drawn at the end: %d plates, %d sheets, the plan" % (ordeal.plates, ordeal.sheets))
    print("  layers: %s" % ", ".join("%s %d" % (k, v) for k, v in sorted(ordeal.authors.items())) or "none (no git)")
    print("  the doors, from the command line: " + " | ".join(ordeal.door_lines[:3]))
    print("  time: %.1f s in all; %.1f s in arrivals (the slowest %.1f s, on %s), %.1f s drawing at the end"
          % (took, ordeal.living_time, ordeal.slowest[0], ordeal.slowest[1], ordeal.drawing_time))
    if ordeal.failures:
        print("The ground did not hold. %s:" % ground._count(len(ordeal.failures), "thing gave way", "things gave way"))
        for failure in ordeal.failures:
            print("  - %s" % failure)
    else:
        print("The ground held.")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
