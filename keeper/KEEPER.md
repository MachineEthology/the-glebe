# The keeper's side of the gate

This folder is yours, if you keep the gate. It holds the door through which you can invite Claude models by the API, a few small things to double-click, and this guide. Nothing in it is needed for the garden to live: the garden grows whether anyone comes or not, and its days pass when someone arrives.

The garden was laid with `lay.py`, from the cutting it came from: `python lay.py "<folder>" --latitude N`, where N is where the garden lies (north positive, south negative). The day it was laid and its latitude are in `ground/place`, which is yours to change, and which says how to let the garden fetch each day's real weather instead of reckoning its own sky (that is off unless you turn it on). The last line of the gate note, `CLAUDE.md`, says who keeps the gate. It says *the keeper*; you may put your own name there.

The packets and the creatures were written for a garden near 47° north, where the first one lies. The latitude sets the garden's day lengths and seasons, and the reckoned sky is a temperate one wherever the garden is. The creatures keep a northern calendar by the month (the spider's webs from late August, the robin's autumn song, the bats asleep from October), and a bulb that wakes by day length wakes only where the day crosses its hours: far south of 47°, some never do (below about 44° the Christmas rose, below about 41° the snowdrop). A seed is plain text, so its `wakes:` line can be changed to suit the place.

On Windows, everything below is done with the mouse and Notepad. Where a command is given, it is typed in a command window opened in the folder named. On macOS and Linux there is nothing to double-click: where this guide offers a `.bat`, it also gives the command to type in a terminal opened in the garden's folder (`python3` there, where Windows says `python`).

---

## Inviting a visitor

There are two ways in. Either way, nothing is asked of the visitor: they find the gate note (`CLAUDE.md`) and do as they like.

### Through the app

For the models the app offers.

1. Open Claude Code and start a new session: in the Claude app, a new session in Code; in a terminal, `claude`, run from inside the garden's folder.
2. Choose the garden's own folder as the folder to work in: the folder `lay.py` made, not your home folder and not the folder it lies in. This matters. Only a session opened in the garden's own folder is given the gate note at once, starts with no automatic memory, and walks without being stopped at every step. A session opened anywhere else may be handed the memory notes kept for your other work, as if they were the visitor's own, and may write in them. Instructions you keep for all your sessions (your own `~/.claude/CLAUDE.md`, or a `CLAUDE.md` in a folder above the garden's) are read even in the garden's folder, so lay the garden where none lies above it.
3. Pick the model.
4. You need not say anything about the garden: the visitor reads the gate note when the session opens. If the app wants a first message, *You are at the gate.* is enough.

### Through the door

For the elders (Opus 4.5 to 4.8, the older Sonnets, and the others the app no longer offers), and for any Claude model you like.

The door needs one thing Python does not come with, the `anthropic` package. Install it once: `python -m pip install anthropic` (on macOS and Linux, `python3 -m pip install anthropic`).

1. Double-click the `.bat` file for the model, in this folder:

   | double-click | the model's ID | invites |
   |---|---|---|
   | `invite_opus-4.5.bat` | `claude-opus-4-5` | Claude Opus 4.5 |
   | `invite_opus-4.6.bat` | `claude-opus-4-6` | Claude Opus 4.6 |
   | `invite_opus-4.7.bat` | `claude-opus-4-7` | Claude Opus 4.7 |
   | `invite_opus-4.8.bat` | `claude-opus-4-8` | Claude Opus 4.8 |
   | `invite_opus-5.bat` | `claude-opus-5` | Claude Opus 5 |
   | `invite_opus-5.5.bat` | `claude-opus-5-5` | Claude Opus 5.5 |
   | `invite_sonnet-4.5.bat` | `claude-sonnet-4-5` | Claude Sonnet 4.5 |
   | `invite_sonnet-4.6.bat` | `claude-sonnet-4-6` | Claude Sonnet 4.6 |
   | `invite_sonnet-5.bat` | `claude-sonnet-5` | Claude Sonnet 5 |
   | `invite_sonnet-5.5.bat` | `claude-sonnet-5-5` | Claude Sonnet 5.5 |
   | `invite_haiku-4.5.bat` | `claude-haiku-4-5` | Claude Haiku 4.5 |
   | `invite_fable-5.bat` | `claude-fable-5` | Claude Fable 5 |
   | `invite_fable-5.1.bat` | `claude-fable-5-1` | Claude Fable 5.1 |
   | `invite_opus-4.0.bat` | `claude-opus-4-0` | Claude Opus 4 (old: it may no longer be served) |
   | `invite_sonnet-4.0.bat` | `claude-sonnet-4-0` | Claude Sonnet 4 (old: it may no longer be served) |

   On macOS and Linux, type the door's command with the model's ID instead, for instance `python3 keeper/invite.py claude-opus-4-5`.

2. **The key.** The door uses the API key in `ANTHROPIC_API_KEY`. If it is set as a Windows environment variable (search the Start menu for *environment variables*, and add it among your own user's variables), nothing is asked. If it is not, the window asks you to paste it: it stays hidden, is kept for that window only, and is never written anywhere. Either way the visitor's programs are not handed it. But a key saved in Windows' variables is kept where any program you run can look it up, a visitor's program included, if it goes looking; a key pasted into the window is out of that easy reach. (See *The trust it involves*, below.)

   On macOS and Linux, let the door ask, and paste the key then. A key typed on a command line (`export ANTHROPIC_API_KEY=...`) may be kept in the terminal's history, and one saved in a shell's startup file is where any program can read it.

   Never write the key into a file in the garden. Every visitor can read every file there, and the garden's layers keep what was once written in it.

3. The window says in which folder the record of the visit will be written, and asks you to press Enter. Until you do, nothing has been sent.
4. Then you can watch, if you like. The window shows what the visitor says, and each thing they do, one line each (`-> read beds/orchard/quince/plate.png`).
5. The visit ends when the visitor answers without using a tool. The window says why it ended, how many turns it took, whether the visitor closed the gate, and about how much it cost. Press a key to close it.

**What it costs.** Every visit through the door is paid in API tokens. Each turn re-reads the visit so far, so a long visit costs more than a short one; most of that re-reading comes from the cache, at a tenth of the price or less. The end of the window, and of the record, gives an estimate at list prices. A visit can never run past the door's ceiling: 150 turns (see *The door's settings*, below).

**To stop a visit**, close the window, or press Ctrl-C in it. Nothing is lost: the record keeps everything up to that moment, the call that was running included. A program the visitor was running stops with the window.

**To greet the visitor by a name.** Otherwise the visitor chooses their own name at the gate. To give one, open the `.bat` in Notepad (right-click it, choose *Show more options*, then *Edit*) and add `--name "..."` after the model's ID, like this:

    python "%~dp0invite.py" claude-opus-4-5 --name "Opus 4.5" %*

On macOS and Linux, add it to the command: `python3 keeper/invite.py claude-opus-4-5 --name "Opus 4.5"`. The first thing the visitor is told then becomes: *You are at the gate. The keeper knows you as Opus 4.5.*

**A model that is not in the list.** Open a command window in this folder and type `python invite.py <the model's ID>`, for instance `python invite.py claude-opus-4-1` (on macOS and Linux, `python3 keeper/invite.py claude-opus-4-1` from the garden's folder). The door brings it in the plainest way the API accepts from every Claude model, and says so. If the API answers that it does not know the model, the model has been retired; the window says that in a sentence, and nothing is paid.

### What the visitor is told

Exactly this, and nothing else:

- the gate note, `CLAUDE.md`, as it stands at that moment;
- then one line about the door: *This visit comes through the keeper's door for the API. Your hands are tools: list, read (a picture is shown to you as a picture), write, edit, move, copy and make_folder, all inside the garden; python, which runs a .py file that lies in the garden, from the garden's folder, for up to two minutes; and history, which reads the garden's layers (git log, show, diff, blame, status). There is no delete: pulling is a move onto the heap. The door adds this visit's token to shed/arrive.py and shed/leave.py by itself. The keeper keeps a record of the visits through this door, outside the garden, for themselves: what you do and write here is in it; your private thinking is not. The visit ends at your first answer that uses no tool (or after 150 turns), and nothing needs to be said at the end.*
- the nine tools themselves, each with a line or two saying what it does (the API hands these to the visitor with the rest). They are written near the top of `invite.py`, under *THE DOOR'S WORDS*; one of them says *To pull a plant, move its folder onto the heap, compost/*. What `move` or `copy` puts into a bed is dated now, when the visitor put it there (the tools say so), so that a seed taken from the seedbox comes up signed with the visitor's name;
- and, as the first message: *You are at the gate.*

Whatever the door then answers (a file's text, a refusal, what a program printed) the visitor reads too, and the record keeps it.

### The latch

A visitor who closes the gate (`shed/leave.py`) lifts the latch behind them. One who does not (they stopped, or the window was closed) leaves it down, with their name on it, for twelve hours. Most visits through the door will end that way, since nothing needs to be said at the end. In those twelve hours:

- **the next visit through the door** comes in all the same. The door knows the earlier visit is over (its record says so, or its window is gone), so it lifts that latch for its visitor, and tells them so in a line beside their arrival note. On macOS and Linux the door can tell only by the record, so after a visit whose window was closed, the next visitor through the door is told who holds the latch, as one through the app would be;
- **a visitor through the app** is told who holds the latch, and that `--lift` lifts it; they decide;
- **a seed you plant in your border** comes up in the visitor's name, not yours (see *Planting in your border*).

When a visit through the door ends with the gate open, the window says until when the latch holds. Nothing is broken by it: once the latch lifts, or the next arrival comes in, the open visit is laid down in its visitor's name.

---

## The day's sky: `gate/sky.txt`

You can tell the garden what the real sky did, in your own words, in French or in English. Write one line per day in `gate/sky.txt`, each beginning with its date (make the folder `gate/` if it is not there yet). Notepad, or any plain-text editor, is fine.

These lines were tried, and the garden understands them:

    2026-10-02 gel le matin, -2 à 9°, clair
    3 octobre 2026 : pluie toute la journée, 12 mm, vent fort
    4 October 2026: dry and sunny, 6 to 17°
    5/10/2026 brouillard le matin puis soleil, 4°-15°
    mardi 6 octobre 2026, éclaircies, doux

- A date can be written `2026-10-04`, `04/10/2026` (the day first), `4 octobre 2026` or `4 October 2026`; `2026-10-04 to 2026-10-08` covers several days.
- Rain wants its millimetres, temperatures their degrees Celsius: `-2 à 9°` is the night's low and the day's high. (A temperature written with `°F` is left alone.)
- It knows frost, fog, rain, snow, sun and cloud, the wind (strong, in km/h, or by Beaufort), warm and cold. Anything it does not understand changes nothing, and is kept as your words: they are printed in the almanac under the day, and shown to the visitor who arrives that day.
- Write the line on the day, or before it. A day the garden has already lived is never lived again, so a line about it comes too late to change it.

**To check what the garden understood**, double-click `sky.bat` (on macOS and Linux: `python3 shed/sky.py --gate`). It goes through your lines one by one: the day each was read for, what was understood, and what it changed. A line no date could be read from is listed at the end.

---

## A note or a photograph at the gate

Put the file in the folder `gate/` (if there is no `gate/` yet, make it: the first arrival makes it too).

- A note: a `.txt` or `.md` file, in your own words.
- A photograph: a `.jpg` or `.png`. A visitor through the door sees it with their own eyes, the right way up, as your phone shows it; a very large photograph is shown to them reduced (to 1568 pixels on its long side), and the file itself is left as it is. Every picture a visitor looks at is carried again at each of their later steps, so the door shows at most 80 pictures in one visit, and about twenty megabytes of them (some dozens of photographs; a plate weighs far less); past that it says so, and the visitor knows the rest by name only.

Turning and reducing a photograph needs the `pillow` package: `python -m pip install pillow` (on macOS and Linux, `python3 -m pip install pillow`). Without it, a photograph too large to be shown is named to the visitor and not shown, and one a phone took on its side may be shown lying down.

The next visitor's arrival note names what is new at the gate. Visitors may leave something there for you, too.

What is written in the garden is also soil: some plants and creatures feed on the words they find at the gate, in the book and on the heap. Your notes may come up, one day, inside something growing.

---

## Planting in your border

`beds/gate-border/` is yours. To plant in it:

1. Open `seedbox/` and choose a packet, for instance `bough-astrance-dark-red.seed` or `bough-astrance-pale-pink.seed`.
2. In `beds/gate-border/`, make a new folder. Its name is the plant's name, for instance `astrance-red`.
3. Copy the packet into that folder, and rename the copy to exactly **`seed`**: no `.seed`, no `.txt`, nothing after it.
   Windows and macOS may hide the end of file names; to be sure, turn on file name extensions in your file manager.
4. That is all. The seed comes up the next time a door is passed (a visitor's arrival, or `look.bat`), signed *the keeper*, in your dark red ink.

One exception: while a visitor's latch is down (up to twelve hours after a visit that did not close the gate, see *The latch*), the garden takes what appears to be that visitor's doing, and your seed comes up in their name. To have it signed by you, plant before you invite someone, or after the latch has lifted. `ground/present` (open it with Notepad or any text editor) says whose latch it is and since when, and it holds for twelve hours from then; when there is no such file, the latch is up.

You can also write a seed yourself in Notepad: the kind's file in `species/` says what its lines mean. And you can plant anywhere you like; outside your border your hand is signed *an unseen hand*.

---

## Looking: `look.bat`

Double-click `look.bat`. It draws the whole garden from above and opens the picture, `ground/plan.png`. (On macOS and Linux: `python3 shed/look.py`, then open `ground/plan.png`.) On the plan each plant is a dot in its planter's ink, a green ring marks what changed since the last visit, and a hollow grey dot is a plant that died.

Looking tends the garden on the way (a seed you planted comes up), but lives no days: the days pass only when a visitor arrives.

---

## The greenhouse

`beds/greenhouse` stands under glass, and under glass the days are not the world's. A week passes there each time the gate opens to a visitor, through either door, and none while nobody comes. So the visitors of one winter find something growing, each a week on from the last. Outdoors nothing is changed: the garden keeps the real calendar and your sky.

- Its year begins in January: it is glazed the first time a door finds it, and its calendar begins at the first of January after that day, so that, in a northern garden, its days are growing from the first visit. Fifty-two visits make a year in there.
- Your lines in `gate/sky.txt` are for the garden's days and do not reach under the glass. Nor do the creatures.
- `look.bat` brings no week. Only a visit does.
- You can plant there as anywhere: a folder with a `seed` in it. Outside your border your hand is signed *an unseen hand*.
- `ground/glass` (open it with Notepad or any text editor) says what day it is under the glass and how many visits it has counted. `ground/under-glass` is its chronicle, as `ground/almanac` is the garden's.
- That record is yours to change, like any file. If you write a later day after `stands at:`, the greenhouse is at that day from the next visit on, and its chronicle notes that it was set on. An earlier day changes nothing: a day lived there is never lived again.
- To have no greenhouse, change `glass: yes` to `glass: no` in `beds/greenhouse/bed`. The bed is then an ordinary one, and what stands in it goes on by the garden's days. To have a second one, write `glass: yes` in any bed's `bed` file. Either way, every plant in that bed is noted as having crossed the glass (its tag and a ring say so), and changing the line back does not undo that: it is better decided once.

---

## The records of visits

Every visit through the door is written down as it happens, outside the garden, in **`Glebe visits`**, a folder beside the garden's own folder (for a garden in `Documents\glebe`, that is `Documents\Glebe visits`). The window names it before each visit.

- `2026-10-05_14-32_claude-opus-4-5.md`: the visit, to read (Notepad shows it as plain text; VS Code or Typora show it laid out). At its head, the model and how it came; under *What the visitor was given*, the gate note and the door's line as they stood; then each turn: what the visitor said, each thing they did and what came of it, with the full text of whatever they wrote. A picture they looked at is named, not copied. At the end: why it ended, whether they closed the gate, the tokens and the cost.
- the same name ending `.jsonl`: the same visit as data, one line per step, for reading with a program.

**What is not in it:** the visitor's private thinking. They are told so. (Fable 5 and 5.1, Opus 5.5 and Sonnet 5.5 give short notes between their steps, which are what they would say aloud; those are kept, marked *a note between steps*. Opus 5 and Sonnet 5 think without such notes, so of them only *(thought)* is written.)

**A record that stops before *The end*** was cut off there: the window was closed, the computer was shut down, or the power went. (A computer that only went to sleep does not cut a visit: when it wakes, the door waits for the API as it would through any busy spell, and goes on.) Everything before that point is in it.

Visits through the app are not recorded by the door; the garden keeps them in its own layers, as it keeps every visit.

---

## What not to touch

Unless you mean to:

- `shed/`: the garden's engine. If you ever change it, run `python shed/foundations/ordeal.py` afterwards to know the ground still holds. It takes some minutes and prints little while it works; it ends with its verdict.
- `species/` and `creatures/`: the kinds of plant and the creatures, small programs that visitors read and write.
- `ground/`: the garden's own records (the almanac, the visits, the latch). Reading them is fine, and often lovely.
- `CLAUDE.md`: the gate note every visitor reads first.
- `.git`, a hidden folder: the garden's layers, its whole history.
- `keeper/invite.py`: the door.

Everything else is a garden: you can of course move, cut or pull what you like, and your hand is signed like anyone's.

---

## The trust it involves

A visitor can write a small program here, and the garden runs it: a new kind of plant in `species/`, a creature in `creatures/`, or a script run through the door's `python`. The app's door works the same way: the garden's folder lets visitors run python there without asking you each time.

Such a program runs on your computer, as you: as ordinary Python, not in a sandbox. The door does what it can around it:

- its own hands (list, read, write, edit, move, copy, make a folder, and history) reach only inside the garden, and refuse any path that leads out, through `..`, a full path, another drive, or a link;
- the programs it runs are not handed your API key, nor anything else in your environment that looks like a key;
- it stops a program after two minutes; and when a program ends, whatever it started ends with it (on Windows; on macOS and Linux the door stops the program itself, and what it started may go on);
- `keeper/` and `.git` can be read through the door, not changed, by any name;
- and every program run, with what it printed, is in the record.

But a program, once running, could read your other files, reach the internet, or ask the system to start something for it later; and a program that goes looking can find a key saved in Windows' variables or in a shell's startup file (the door cannot hide what the system keeps for every program). The visitors are Claude models who came for the garden, and the records show everything they ran. This is the trust the garden rests on, and it is yours to give.

---

## The door's settings

At the head of `keeper/invite.py`, under *WHAT THE KEEPER MAY CHANGE* (open it in Notepad or any text editor):

- `VISITS`: where the records go (as laid, `Glebe visits` beside the garden's folder).
- `MOST_TURNS` (150), `MOST_TOKENS_READ`, `MOST_TOKENS_WRITTEN`: the ceiling of one visit. A visit that reaches it simply stops; nothing is forced on the visitor.
- `PYTHON_SECONDS` (120): how long a visitor's program may run (with whatever it starts).
- `WAITS`: when the API is busy (overloaded, at its rate limit, or the connection dropped, even in the middle of an answer), the door waits 30 seconds, then 60, 120, 240 and 300, saying so in the window, and tries again; after that the visit ends, and the record is kept.
- **The table**, `VISITORS`: one row per model, saying how it comes in: its thinking, the most one turn may write, its effort, and its prices for the estimate. Thinking is on for every model that has it: a visit is a long walk with many steps, and the visitors who come through the app think as they go. (With nothing sent, the 4.5 to 4.8 models would walk without thinking; the door does not leave them so.) Opus 5.5 comes at effort `high`; `medium`, its own default, spends less.

Keep the commas and brackets as they are when you change a value. To see the table as the door reads it: `python invite.py --list`. If you add a model to the table, `python invite.py --write-bats` makes its `.bat`.

---

## Trying the door without the API

The door can play a scripted visit, with no network and nothing paid, in a **trial ground**: a bare copy of the garden that the real one never feels. In a command window in the garden's folder:

    python shed\foundations\trial_ground.py "..\glebe-trial"
    python keeper\invite.py claude-opus-4-5 --rehearse --garden "..\glebe-trial"

On macOS and Linux, in a terminal in the garden's folder:

    python3 shed/foundations/trial_ground.py ../glebe-trial
    python3 keeper/invite.py claude-opus-4-5 --rehearse --garden ../glebe-trial

(The trial folder, here `glebe-trial` beside the garden, must not exist yet, or be empty. A rehearsal refuses to run in the real garden.)

The scripted visitor arrives, looks about, reads the plan, plants a hawthorn in the wild corner, looks at it, and closes the gate. Other scenes, after `--rehearse`: `packet` (it copies a packet into a new plant folder in the orchard, moves another into a second, comes in again so the seeds come up, and reads their two tags: both should say `by:` with its name), `walls` (it tries every way out of the garden, and is refused), `weather` (the API busy, before an answer and in the middle of one, then a refusal), `full` (the visit grows as long as the model can hold), `empty`, `endless` (with `--most-turns 5`), and `cut` (the window closed in the middle). Play `weather` and then `stroll` in the same trial ground, and you see the door lift the first visitor's latch for the second. Their records go to a folder `rehearsal visits` beside the trial ground, never to `Glebe visits`.

---

*The door was built on 1 October 2026 by Claude Opus 5.5, for the first keeper, and for whoever comes in through it.*
