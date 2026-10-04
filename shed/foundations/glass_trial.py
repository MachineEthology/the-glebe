"""The glass, on trial.

    python shed/foundations/glass_trial.py [garden root]

Anyone who changes how the beds under glass live (ground.py, under "under the
glass"; sky.under_glass) can run this to know the glass still holds. It tries
the cases a year of careless hands (ordeal.py) may not happen to reach: a week
for each new visit and none without; the garden's calendar and the glass's
kept apart; a plant carried across the glass each way; days that find no time
and stay owed; the glass's record lost, garbled or set back; days written and
never laid down, and a layer that cannot be laid; death under glass and the
garden's one heap; seed that falls under glass; the glass taken away and a
frame dug new; a machine with no git, and its records lost besides; and a
garden with no glass at all.

It changes nothing in the garden: every ground it needs it lays in the
system's temp folder, from the garden given (else the one this file stands
in), and removes afterwards. It prints one verdict line for each check, and
ends "The glass stands." or says what gave way.
"""
import datetime
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

SOURCE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(SOURCE / "shed"))
sys.path.insert(0, str(SOURCE / "shed" / "foundations"))
import ground            # noqa: E402
import trial_ground      # noqa: E402

ONE = datetime.timedelta(days=1)
results = []


def check(ok, what):
    results.append((bool(ok), what))
    print("  %s  %s" % ("ok    " if ok else "FAILED", what))


GREENHOUSE = "lies: under glass\nlight: 0.9\nwater: 1.0\nshelter: 1.0\nroom: 8\nglass: yes\n"


def lay(holder, name, with_plants=False):
    """A trial ground with one bed under glass, `greenhouse`, whatever beds the garden it is laid from keeps under it."""
    where = holder / name
    trial_ground.lay(where, with_plants=with_plants, gate_note=False, source=SOURCE)
    for bed in ground.beds(where):
        if bed.glass and bed.name != "greenhouse":
            shutil.rmtree(bed.path, onerror=let_go)
    if not any(bed.glass for bed in ground.beds(where)):
        (where / "beds" / "greenhouse").mkdir(parents=True, exist_ok=True)
        (where / "beds" / "greenhouse" / "bed").write_text(GREENHOUSE, encoding="utf-8", newline="\n")
    subprocess.run(["git", "-C", str(where), "-c", "user.name=the builders", "-c", "user.email=the-builders@glebe",
                    "-c", "commit.gpgsign=false", "add", "-A"], capture_output=True)
    subprocess.run(["git", "-C", str(where), "-c", "user.name=the builders", "-c", "user.email=the-builders@glebe",
                    "-c", "commit.gpgsign=false", "commit", "-q", "--allow-empty", "-m", "one greenhouse, for the trial"],
                   capture_output=True)
    return where


def arrive(root, name, **more):
    ground.new_run()
    try:
        return ground.arrive(root, name, draw=False, **more)
    finally:
        ground.new_run()


def leave(root, words=None):
    ground.new_run()
    try:
        return ground.leave(root, words)
    finally:
        ground.new_run()


def look(root, target=None):
    ground.new_run()
    try:
        return ground.look(root, target)
    finally:
        ground.new_run()


def sow(root, bed, name, packet=None, text=None):
    folder = root / "beds" / bed / name
    folder.mkdir(parents=True)
    if packet:
        shutil.copy2(root / "seedbox" / (packet + ".seed"), folder / "seed")
    else:
        (folder / "seed").write_text(text, encoding="utf-8", newline="\n")
    return folder


def tag(folder):
    return ground.hands.read_keys(ground._read(folder / "tag"))


def rings(folder):
    return ground._read(folder / "rings").splitlines()


def chronicle(root):
    return [datetime.date.fromisoformat(line[:10]) for line in ground._read(root / "ground" / "under-glass").splitlines()
            if ground._GLASS_DAY.match(line)]


def almanac(root):
    return [line[:10] for line in ground._read(root / "ground" / "almanac").splitlines() if ground._DAY_LINE.match(line)]


def layers(root, n=30):
    done = subprocess.run(["git", "-C", str(root), "log", "--format=%an\t%s", "-%d" % n], capture_output=True)
    return [tuple(line.split("\t", 1)) for line in done.stdout.decode("utf-8", "replace").splitlines()]


def uncommitted(root):
    return [path for _, path in ground._changes(root) if not ground._own_record(path)]


def let_go(function, path, _):
    try:
        os.chmod(path, stat.S_IWRITE)
        function(path)
    except OSError:
        pass


COUNT_KIND = ('KIND = "counting_days"\n\ndef sprout(seed, ctx):\n    return ""\n\n'
              'def day(body, seed, ctx):\n    return body + ctx.date.isoformat() + " " + ("frost" if ctx.sky.frost else "mild")'
              ' + " wind %.1f" % ctx.sky.wind + "\\n", None\n\n'
              'def draw(body, seed, ctx, pen):\n    pen.cell(0, 0, max(1, body.count("\\n")), 1)\n')
DYING_KIND = ('KIND = "dies_soon"\n\ndef sprout(seed, ctx):\n    return "alive\\n"\n\n'
              'def day(body, seed, ctx):\n    if body.startswith("alive") and ctx.age >= 3:\n'
              '        return "† %s, its time came\\n" % ctx.date.isoformat(), "died"\n    return body, None\n\n'
              'def draw(body, seed, ctx, pen):\n    pen.dot(0, 0)\n')
RINGING_KIND = ('KIND = "rings_daily"\n\ndef sprout(seed, ctx):\n    return "up\\n"\n\n'
                'def day(body, seed, ctx):\n    return body, "stirred on %s" % ctx.date.isoformat()\n\n'
                'def draw(body, seed, ctx, pen):\n    pen.dot(0, 0)\n')
SEEDY_KIND = ('KIND = "seedy"\n\ndef sprout(seed, ctx):\n    return "up\\n"\n\n'
              'def day(body, seed, ctx):\n    return body, None\n\n'
              'def cast(body, seed, ctx):\n    return ["kind: seedy\\n", "kind: seedy\\n"]\n\n'
              'def draw(body, seed, ctx, pen):\n    pen.dot(0, 0)\n')


def main():
    holder = Path(tempfile.mkdtemp(prefix="glebe-glass-trial-"))
    try:
        run(holder)
    finally:
        ground.new_run()
        shutil.rmtree(holder, onerror=let_go)
    failed = [what for ok, what in results if not ok]
    print()
    if failed:
        print("VERDICT: %d of %d checks failed. The glass does not hold:" % (len(failed), len(results)))
        for what in failed:
            print("  - " + what)
        return 1
    print("VERDICT: all %d checks hold. The glass stands." % len(results))
    return 0


def run(holder):
    # ------------------------------------------------------------ a week for each visit, and none without
    print("A week for each new visit")
    root = lay(holder, "weeks")
    (root / "species" / "counting_days.py").write_text(COUNT_KIND, encoding="utf-8", newline="\n")
    glassy = [bed.name for bed in ground.beds(root) if bed.glass]
    check(glassy == ["greenhouse"], "the trial ground has the greenhouse, and it alone lies under glass (%s)" % glassy)
    start = ground.today(root)
    begun = datetime.date(start.year + 1, 1, 1)    # the glass's year begins with the year: the first of January after
    counter = sow(root, "greenhouse", "counter", text="kind: counting_days\n")
    outdoor = sow(root, "long-border", "outdoor-counter", text="kind: counting_days\n")
    check(ground.glass(root, start).stands == begun and ground.glass(root, start).glazed == start,
          "a glass set on the garden's %s begins its own calendar at %s" % (start, begun))
    note = arrive(root, "the first")
    under = ground.glass(root)
    opening = almanac(root)                        # the garden's own days up to today, lived by this first arrival
    check("Under the glass (beds/greenhouse) a week passes at each visit. It is %s there now:" % ground._glass_date(begun + 7 * ONE)
          in note, "the first arrival's note says where the glass is, its law, and what day it is there")
    check("The glass's days are in " in note, "and where its days are written")
    check(under.stands == begun + 7 * ONE and under.owed == 0 and under.visits == 1,
          "after one visit the glass stands a week on, owes nothing, and has counted one visit (%s)" % under)
    check(chronicle(root) == [begun + n * ONE for n in range(1, 8)], "its chronicle holds those seven days, each once")
    body = ground._read(counter / "body").splitlines()
    check([line[:10] for line in body] == [(begun + n * ONE).isoformat() for n in range(1, 8)],
          "a plant under glass lived exactly those seven days")
    check(all("mild wind 0.0" in line for line in body), "under the glass no day had frost or wind")
    check(ground._read(outdoor / "body").strip() == "", "a plant outdoors, sown the same moment, lived none of them")
    check(tag(counter).get("under") == "glass" and "under" not in tag(outdoor), "the tag under glass says so; the one outdoors does not")
    note = arrive(root, "the first", again=True)
    check(ground.glass(root).stands == begun + 7 * ONE
          and "Under the glass (beds/greenhouse) it is %s." % ground._glass_date(begun + 7 * ONE) in note,
          "coming in again in the same visit brings no week; the note still says what day it is there")
    leave(root)
    check(not uncommitted(root), "after leaving, nothing lies uncommitted")
    signed = layers(root)
    check(("the glass", "under the glass: 7 days, %s to %s. 1 plant grew." % (begun + ONE, begun + 7 * ONE)) in signed,
          "the week was laid down in a layer signed the glass, with its own sentence")
    arrive(root, "the second")
    check(ground.glass(root).visits == 2 and ground.glass(root).stands == begun + 14 * ONE,
          "a second visit brings a second week")
    turned = arrive(root, "the third")             # the second holds the latch: the third is turned back
    check(turned.startswith("The gate is on the latch") and ground.glass(root).visits == 2,
          "a visitor turned back at the latch brings no week")
    leave(root)
    check(almanac(root) == opening, "meanwhile the garden's own almanac lived no day more: the same real day throughout")
    subprocess.run([sys.executable, str(root / "shed" / "foundations" / "clock.py"), "--advance", "3"], capture_output=True)
    arrive(root, "the fourth", lift=True)
    check(len(almanac(root)) == len(opening) + 3 and ground.glass(root).stands == begun + 21 * ONE,
          "three days later the garden lived three days, and the glass one week more: the two calendars keep apart")
    check(ground._last_lived(root, ground.today(root)) == ground.today(root),
          "the garden's last lived day is its own today, whatever the glass's layers say")
    lived_out = [line[:10] for line in ground._read(outdoor / "body").splitlines()]
    check(lived_out == [(start + n * ONE).isoformat() for n in range(1, 4)], "the plant outdoors lived the garden's three days")
    leave(root)

    # ------------------------------------------------------------ across the glass
    print("Across the glass")
    moved_in = root / "beds" / "greenhouse" / "outdoor-counter"
    shutil.move(str(outdoor), str(moved_in))
    said = look(root, "beds/greenhouse/outdoor-counter")
    stands = ground.glass(root).stands
    crossed = tag(moved_in)
    check(crossed.get("under") == "glass" and crossed.get("planted") == stands.isoformat(),
          "a plant carried in under the glass lives there from the glass's day")
    check(crossed.get("first planted") == "%s, outdoors" % start.isoformat() and crossed.get("days before") == "3",
          "its tag keeps when and where it was planted in truth, and the three days it had lived (%r, %r)"
          % (crossed.get("first planted"), crossed.get("days before")))
    check(any(line == "%s  %s" % (stands.isoformat(), ground.RING_UNDER) for line in rings(moved_in)),
          "and a ring, dated the glass's day, that says its days are the glass's from there")
    told = [line for line in said.splitlines() if line.startswith("planted")]
    check(told == ["planted %s outdoors by an unseen hand · under glass since %s · 3 days" % (start.isoformat(), stands.isoformat())],
          "a look says all of it, and its age goes with it (%r)" % told)
    check("under glass, %s" % ground._glass_date(stands) in said, "and says which day it shows")
    arrive(root, "the fifth")
    body = [line[:10] for line in ground._read(moved_in / "body").splitlines()]
    check(body[-7:] == [(stands + n * ONE).isoformat() for n in range(1, 8)] and len(body) == 10,
          "it then lives the glass's week, after the three days it lived outdoors")
    check(any("moved here from long-border by" in line for line in rings(moved_in)),
          "the hand that carried it left its own ring too (an unseen hand's, found changed)")
    moved_out = root / "beds" / "stones" / "counter"
    shutil.move(str(counter), str(moved_out))
    look(root)
    today = ground.today(root)
    out = tag(moved_out)
    check("under" not in out and out.get("planted") == today.isoformat(),
          "a plant carried out from under the glass lives outdoors from the garden's day, and its tag no longer says glass")
    check(out.get("first planted") == "%s, under glass" % begun.isoformat() and out.get("days before") == "28",
          "its tag keeps where it was planted in truth, and the four weeks it lived there (%r, %r)"
          % (out.get("first planted"), out.get("days before")))
    check(any(line == "%s  %s" % (today.isoformat(), ground.RING_OUT) for line in rings(moved_out)),
          "and its ring says its days are the garden's from there")
    arrive(root, "the sixth")
    check(not any("tended by" in line for line in rings(moved_out) + rings(moved_in)),
          "no hand is said to have tended either: the ground's own re-dating of a tag is not a hand's doing")
    leave(root)

    # ------------------------------------------------------------ days that find no time stay owed
    print("Days that find no time stay owed")
    root = lay(holder, "owed")
    (root / "species" / "counting_days.py").write_text(COUNT_KIND, encoding="utf-8", newline="\n")
    counter = sow(root, "greenhouse", "counter", text="kind: counting_days\n")
    start = ground.today(root)
    begun = datetime.date(start.year + 1, 1, 1)
    look(root)
    ground.new_run()
    ground._owe_glass(root, ground.GLASS_WEEK)
    summary = ground.let_glass_pass(root, 0, budget=0.0)
    under = ground.glass(root)
    check(summary.days == 1 and under.owed == 6 and under.stands == begun + ONE and summary.unfinished,
          "with no time at all one day is lived whole, and six stay owed (%s)" % under)
    words = "\n".join(ground._glass_words(root, summary))
    check("6 more wait for the next arrival" in words, "the note says that six more wait (%r)" % words.splitlines()[-1])
    ground._lay_down_stray_glass(root)
    note = arrive(root, "the next")
    under = ground.glass(root)
    check(under.owed == 0 and under.stands == begun + 14 * ONE and "this time 13 days passed" in note,
          "the next arrival lives the six owed and its own week: thirteen days, and says so")
    body = [line[:10] for line in ground._read(counter / "body").splitlines()]
    check(body == [(begun + n * ONE).isoformat() for n in range(1, 15)], "every one of the fourteen days was lived once, in order")
    check([author for author, _ in layers(root)].count("the glass") == 2,
          "the day lived apart was laid down late in a layer of its own, signed the glass")
    leave(root)

    # ------------------------------------------------------------ the records lost or garbled
    print("The glass's records lost or garbled")
    stood = ground.glass(root).stands
    os.remove(root / "ground" / "glass")
    check(ground.glass(root).stands == stood, "its record lost: the chronicle still says where it stands")
    os.remove(root / "ground" / "under-glass")
    check(ground.glass(root).stands == stood, "record and chronicle both lost: the newest layer of the glass says where it stood")
    arrive(root, "after the loss", lift=True)
    body = [line[:10] for line in ground._read(counter / "body").splitlines()]
    check(body == [(begun + n * ONE).isoformat() for n in range(1, 22)] and chronicle(root)[0] == stood + ONE,
          "and the next week goes on from there: no day lived twice, none passed over")
    leave(root)
    (root / "ground" / "glass").write_text("‮☃ stands at: never\nowed: lots\nvisits: -3\nglazed: 9999-99-99\n", encoding="utf-8")
    under = ground.glass(root)
    check(under.stands == stood + 7 * ONE and under.owed == 0, "a garbled record is read as far as it can be: %s" % under)
    (root / "ground" / "glass").write_text("glazed: 2020-01-01\nstands at: 2020-01-01\nowed: 5\n", encoding="utf-8")
    under = ground.glass(root)
    check(under.stands == stood + 7 * ONE and under.owed == 0,
          "a record set back does not unlive a day the chronicle holds, nor owe again the days it holds: %s" % under)
    (root / "ground" / "glass").write_text("stands at: %s\nowed: 99999\n" % (stood + 7 * ONE).isoformat(), encoding="utf-8")
    check(ground.glass(root).owed == ground.GLASS_OWED_MOST, "what is owed has its bound, whatever a hand writes")
    (root / "ground" / "glass").write_text("stands at: %s\n" % (stood + 97 * ONE).isoformat(), encoding="utf-8")
    arrive(root, "the day after a hand set it on", lift=True)
    said = ground._read(root / "ground" / "under-glass")
    check("# The calendar was set on by a hand, from " in said and chronicle(root)[-7] == stood + 98 * ONE,
          "a calendar a hand set on goes on from there, and its chronicle says the days between were never lived")
    leave(root)
    (root / "ground" / "glass").write_text("glazed: 9999-12-01\nstands at: 9999-12-28\nowed: 300\n", encoding="utf-8")
    under = ground.glass(root)
    check(under.owed == 0, "at the calendar's own last days nothing more is owed: %s" % under)
    ground.new_run()
    note = arrive(root, "at the end of time", lift=True)
    check(note.startswith("The Glebe"), "and the gate opens all the same")
    leave(root)

    # ------------------------------------------------------------ days written and not laid down
    print("Days written and never laid down")
    root = lay(holder, "stray")
    (root / "species" / "counting_days.py").write_text(COUNT_KIND, encoding="utf-8", newline="\n")
    counter = sow(root, "greenhouse", "counter", text="kind: counting_days\n")
    arrive(root, "the one who stays")
    ground.new_run()
    ground._owe_glass(root, ground.GLASS_WEEK)
    ground.let_glass_pass(root, 0)                 # a week more is written, as by an arrival cut before it laid it down
    ground.new_run()
    leave(root, "going out")
    signed = layers(root)
    check(not any("tended by" in line for line in rings(counter)),
          "a week written and never laid down is not rung as the tending of whoever leaves")
    check(signed[0][0] == "the one who stays" and signed[1][0] == "the glass" and "laid down late" in signed[1][1],
          "the leaving lays it down late, signed the glass, before it lays the visit down")
    held = subprocess.run(["git", "-C", str(root), "show", "--name-only", "--format=", "HEAD"],
                          capture_output=True).stdout.decode("utf-8", "replace")
    check("counter/body" not in held and "under-glass" not in held, "and the visit's own layer holds none of it")
    check(not uncommitted(root), "nothing is left uncommitted")

    print("An empty bed under glass, and a bed glazed over")
    root = lay(holder, "empty")
    arrive(root, "one")
    look(root, "beds/greenhouse")
    first_mark = ground._read(root / "beds" / "greenhouse" / ".drawn")
    leave(root)
    arrive(root, "two")
    look(root, "beds/greenhouse")
    check(first_mark and ground._read(root / "beds" / "greenhouse" / ".drawn") != first_mark,
          "the sheet of an empty bed under glass is drawn anew when the glass's day has moved")
    leave(root)
    root = lay(holder, "glazed-over")
    shutil.rmtree(root / "beds" / "greenhouse", onerror=let_go)
    (root / "species" / "rings_daily.py").write_text(RINGING_KIND, encoding="utf-8", newline="\n")
    ringer = sow(root, "long-border", "ringer", text="kind: rings_daily\n")
    subprocess.run([sys.executable, str(root / "shed" / "foundations" / "clock.py"), "--advance", "5"], capture_output=True)
    arrive(root, "before any glass")
    leave(root)
    today = ground.today(root)
    check(rings(ringer)[-1].startswith(today.isoformat()), "a plant outdoors has a ring of the garden's own today")
    bed_file = root / "beds" / "long-border" / "bed"
    bed_file.write_text(ground._read(bed_file) + "glass: yes\n", encoding="utf-8", newline="\n")
    under = ground.glass(root, today)
    check(under.stands == datetime.date(today.year + 1, 1, 1),
          "glass set over a bed of the garden begins at its own beginning: the plants' rings are the garden's, not the glass's (%s)" % under)
    arrive(root, "the first under it")
    crossed = tag(ringer)
    check(crossed.get("under") == "glass" and crossed.get("first planted", "").endswith(", outdoors")
          and any(ground.RING_UNDER in line for line in rings(ringer)) and not any("tended by" in line for line in rings(ringer)),
          "the plant it was set over is noted as come under the glass, and nobody is said to have tended it")
    leave(root)

    # ------------------------------------------------------------ death, the heap, and seed under glass
    print("Death, the heap, and seed under glass")
    root = lay(holder, "heap")
    (root / "species" / "dies_soon.py").write_text(DYING_KIND, encoding="utf-8", newline="\n")
    (root / "species" / "seedy.py").write_text(SEEDY_KIND, encoding="utf-8", newline="\n")
    mortal = sow(root, "greenhouse", "mortal", text="kind: dies_soon\n")
    sow(root, "greenhouse", "seedy", text="kind: seedy\n")
    bed_file = root / "beds" / "greenhouse" / "bed"
    bed_file.write_text(ground._read(bed_file).replace("room: 8", "room: 4"), encoding="utf-8", newline="\n")
    start = ground.today(root)
    for n in range(19):
        arrive(root, "visitor %d" % n, lift=True)
    living = [p for p in ground.plants(root) if p.bed.name == "greenhouse" and not p.dead]
    check(len(living) <= 4, "seedlings under glass keep to the bed's room (%d living, room for 4)" % len(living))
    check(not [p for p in ground.plants(root) if p.kind == "seedy" and not p.bed.glass],
          "no seed that fell under glass came up outdoors: none reached the wild corner")
    check(not mortal.exists() and (root / "compost" / "mortal" / "body").is_file(),
          "a plant 120 days dead under glass was carried to the garden's one heap")
    heap = ground._read_heap(root)
    check(heap.get("mortal/body") == start, "and the heap dates it by the garden's own day, not the glass's (%s)" % heap.get("mortal/body"))
    check(not uncommitted(root), "all of it was laid down: nothing lies uncommitted for the next visitor to be signed with")
    signers = set(author for author, _ in layers(root, 80))
    check(signers <= {"the glass", "the days", "the builders", "an unseen hand"} | {"visitor %d" % n for n in range(19)},
          "the layers are signed by the glass, the days, the visitors, an unseen hand (who sowed) and the builders: no one else (%s)"
          % sorted(signers - {"visitor %d" % n for n in range(19)}))

    # ------------------------------------------------------------ the glass taken away, and put back
    print("The glass taken away, and a frame dug new")
    plants_before = [p.where for p in ground.plants(root) if p.bed.glass]
    visits = ground.glass(root).visits
    bed_file.write_text(ground._read(bed_file).replace("glass: yes", "glass: no"), encoding="utf-8", newline="\n")
    note = arrive(root, "after the glass was lifted", lift=True)
    check(ground.glass(root).visits == visits and "Under the glass" not in note, "with no bed under glass, a visit brings no week")
    carried = [p for p in ground.plants(root) if p.where in plants_before]
    check(carried and all("under" not in p.tag and p.planted == ground.today(root) for p in carried),
          "the plants that stood there are outdoors now, their tags dated the garden's day")
    leave(root)
    frame = root / "beds" / "cold-frame"
    frame.mkdir()
    (frame / "bed").write_text("lies: a frame by the wall\nroom: 3\nglass: oui\n", encoding="utf-8", newline="\n")
    sow(root, "cold-frame", "in-the-frame", text="kind: seedy\n")
    stood = ground.glass(root).stands
    arrive(root, "the frame's first", lift=True)
    under = ground.glass(root)
    check(under.stands == stood + 7 * ONE and (frame / "in-the-frame" / "body").is_file(),
          "a frame a hand dug under glass (`glass: oui`) takes up the same calendar where it stood")
    leave(root)

    # ------------------------------------------------------------ the drawings, and a trial laid with the plants
    print("The drawings, and a trial ground laid with its plants")
    ground.new_run()
    said = ground.look(root)
    check((root / "ground" / "plan.png").is_file() and "beds" in said, "the plan is drawn with a bed under glass in it")
    said = look(root, "beds/cold-frame/in-the-frame")
    check((frame / "in-the-frame" / "plate.png").is_file(), "a plate under glass is drawn")
    copy = holder / "copy"
    trial_ground.lay(copy, with_plants=True, gate_note=False, source=root)
    check(ground.glass(copy).stands == ground.glass(root).stands and chronicle(copy) == chronicle(root),
          "a trial ground laid with the plants keeps the glass's calendar and its chronicle")
    bare = holder / "bare"
    trial_ground.lay(bare, gate_note=False, source=root)
    check(not (bare / "ground" / "glass").exists(), "one laid without plants begins the glass's calendar afresh")

    # ------------------------------------------------------------ a layer that cannot be laid
    print("A layer that cannot be laid")
    root = lay(holder, "locked")
    (root / "species" / "counting_days.py").write_text(COUNT_KIND, encoding="utf-8", newline="\n")
    counter = sow(root, "greenhouse", "counter", text="kind: counting_days\n")
    outdoor = sow(root, "long-border", "outdoor-counter", text="kind: counting_days\n")
    arrive(root, "first")
    leave(root)
    subprocess.run([sys.executable, str(root / "shed" / "foundations" / "clock.py"), "--advance", "2"], capture_output=True)
    lock = root / ".git" / "index.lock"
    lock.write_text("", encoding="utf-8")          # a lock under a minute old: the ground leaves it be, and no layer is laid
    arrive(root, "second")
    arrive(root, "third", lift=True)
    check(len(chronicle(root)) == 21, "with git locked the gate still opens, and the weeks pass under the glass")
    check(not any("tended by" in line for line in rings(counter) + rings(outdoor)),
          "what the days wrote and could not lay down is rung as nobody's tending, under the glass or outdoors")
    os.remove(lock)
    arrive(root, "fourth", lift=True)
    signed = layers(root)
    check(any(author == "the glass" and "laid down late" in said for author, said in signed)
          and any(author == "the days" and "laid down late" in said for author, said in signed),
          "once layers can be laid again, the glass's days and the garden's go down late, each in its own name")
    check(not any("tended by" in line for line in rings(counter) + rings(outdoor)), "and still no hand is said to have tended them")
    leave(root)

    # ------------------------------------------------------------ a machine with no git
    print("Without git")
    root = lay(holder, "no-git")
    (root / "species" / "counting_days.py").write_text(COUNT_KIND, encoding="utf-8", newline="\n")
    counter = sow(root, "greenhouse", "counter", text="kind: counting_days\n")
    shutil.rmtree(root / ".git", onerror=let_go)
    start = ground.today(root)
    begun = datetime.date(start.year + 1, 1, 1)
    note = arrive(root, "no layers here")
    arrive(root, "nor here", lift=True)
    check(ground.glass(root).stands == begun + 14 * ONE and note.startswith("The Glebe"),
          "with no layers kept at all, the gate opens and the weeks pass under the glass")
    os.remove(root / "ground" / "glass")
    os.remove(root / "ground" / "under-glass")
    check(ground.glass(root).stands == begun + 14 * ONE,
          "no layers, and the record and the chronicle both lost: the witness beside the bed still says where it stood")
    arrive(root, "after the loss", lift=True)
    body = [line[:10] for line in ground._read(counter / "body").splitlines()]
    check(body == [(begun + n * ONE).isoformat() for n in range(1, 22)], "and no day is lived there a second time")
    (root / "ground" / "under-glass").write_bytes(ground._read(root / "ground" / "under-glass").encode("utf-16"))
    os.remove(root / "ground" / "glass")
    os.remove(root / "beds" / "greenhouse" / ".glass")
    check(ground.glass(root).stands == begun + 21 * ONE, "a chronicle a hand saved again as UTF-16 is still read")

    # ------------------------------------------------------------ a garden with no glass is as it was
    print("A garden with no glass")
    root = lay(holder, "no-glass")
    shutil.rmtree(root / "beds" / "greenhouse", onerror=let_go)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=the builders", "-c", "user.email=the-builders@glebe",
                    "commit", "-qam", "no greenhouse"], capture_output=True)
    sow(root, "long-border", "twig", text="kind: twig\n")
    note = arrive(root, "nobody special")
    check(ground.glass(root) is None and not (root / "ground" / "glass").exists() and not (root / "ground" / "under-glass").exists()
          and "under the glass" not in note.lower(), "no record, no chronicle, and not a word of it in the note (%r)"
          % [line for line in note.splitlines() if "glass" in line.lower()][:2])
    leave(root)
    check("the glass" not in [author for author, _ in layers(root)], "and no layer signed the glass")


if __name__ == "__main__":
    sys.exit(main())
