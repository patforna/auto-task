#!/usr/bin/env python3
"""Render a demo screenplay to an asciicast.

Directives, all starting at column 0. Note what each number means — they are not
all durations:

  @prompt <text>          a human types <text> at the prompt, then hits enter.
                          Takes NO number. A leading /command is bolded, its
                          arguments are not.
  @pause <secs>           wait, showing nothing new
  @clear                  wipe the screen and start again at the top

  @step  <secs> <l>|<g>   a phase row that spins for <secs> — the WHOLE row, give
                          or take HOLD_JITTER so the beats don't tick like a
                          metronome — then ticks over to done in place. The gloss
                          is there from the first frame; the spinner and the tick
                          carry the motion, so there is nothing to reveal in parts.
  @step! <secs> <l>|<g>   the same, but the row is left SPINNING. It keeps turning
                          through whatever is printed below it until an @resolve
                          finishes it. Use when the step is genuinely blocked on
                          the human, e.g. clarify waiting on an answer.
  @resolve <secs>         finish the pending @step! in place, however many rows
                          have been printed since. <secs> is the beat before the
                          tick lands. One pending step at a time.

  @checklist <a>|<b>|<c>  print every phase up front, all pending, so the viewer
                          sees the shape of the run before any of it happens.
  @run <secs> <l>|<g>|<clock>
  @run <secs> <l>|<running g>|<done g>|<clock>
                          tick one checklist row over: <l> spins for <secs> with
                          its running gloss, then lands done. Four fields give it
                          a second gloss for the landed row ("fixing 2 of 3" ->
                          "3 fixed"). Rows must be run in the order they were
                          listed. Every frame repaints the whole block, so rows
                          above stay done and rows below stay pending.
                          <clock> is how long THIS row took. Each row is its own
                          stopwatch: it runs from 0:00 and lands exactly on
                          <clock>, so the column adds up to the run's total. That
                          ticking is what stops a block of five rows reading as a
                          slow typewriter.

  @row <glyph> <l>|<g>    one finished phase row, printed as-is: no spinner, no
                          tick, no "...". Takes NO number. For a row that never
                          runs, e.g. the 🎉 signoff line. An optional third field
                          adds a clock.

  @ask <text>             a question handed back to you, marked with ASK_MARK
  @select <n> <a>|<b>     a TUI picker. <n> is the 1-BASED OPTION that ends up
                          chosen — not a duration. The highlight lands on the
                          first option, walks down to <n>, then pulses to confirm.
                          Timings come from the SELECT_* constants below.

  anything else           printed verbatim (blank lines and indentation included)
  # at column 0           a comment; indented "#" lines are content, not comments

Every phase row — @step, @step!, @checklist, @run, @row — is laid out on one grid,
so a stack of them reads as a column rather than a zigzag (columns are 1-indexed):

  cols 1-2    status glyph, padded to two DISPLAY cells: ✓ · ⠋ take a trailing
              space, 🎉 is already two cells wide and takes none
  cols 3-19   label, bold in the default foreground. "..." means still running:
              the renderer appends it while the row spins and drops it when the
              row lands, so screenplays write the bare label
  cols 20-55  gloss, in the gloss grey; "·" separators are tinted automatically.
              With no clock beside it a gloss may run on to col 78
  col 56      clock, 4 characters ("0:14"), in its own grey. Never emphasised —
              it is read positionally, and competing with it flattens both

A pending row is the exception: pending grey throughout, not bold, and no gloss
and no clock, because it has nothing to report yet.

Blank lines never double up: consecutive blanks collapse to one.

Inline styling: {bold} {dim} {orange} {green} {cyan} {yellow} {red}, the phase-row
greys {pending} {clock} {sep}, and {n}, each closed by {/}. {n} is a count —
bold in the default foreground, because the numbers are the evidence and their
labels are not ("{n}6{/} commits"). {/} pops back to the enclosing tag, so inside
a gloss it returns to the gloss grey instead of resetting the whole field.
Use {green}✓{/} explicitly for a tick; there is no implicit marker on plain lines.

Everything scrolls naturally: content never uses absolute cursor addressing, so
the prompt moves up the screen like a real terminal and nothing leaves ghosts.
The three in-place effects — @select's highlight, @resolve and the @checklist
block — are laid down once and afterwards move relative to the cursor and back,
so they scroll with the transcript like any other content.
"""
import argparse, json, random, re, unicodedata

COLS, ROWS = 80, 16   # peak height is 14 rows either side of the @clear

# The phase-row grid: glyph at cols 1-2, label 3-19, gloss 20-55, clock at 56.
# Every directive that prints a row pads to these, so the columns hold whatever
# is in them. A gloss with no clock after it gets the rest of the row instead,
# stopping two columns short of the edge.
GLYPH_W, LABEL_W, GLOSS_W = 2, 17, 36
GLOSS_MAX = COLS - GLYPH_W - LABEL_W - 2

R = "\x1b[0m"
WEIGHT_OFF = "\x1b[22m"       # weight only — a full reset would drop the colour too
EMPHASIS = "\x1b[1m\x1b[39m"  # bold in the default foreground: a label, and {n}


# "dim" is an explicit grey, not SGR 2. SGR 2 darkens toward the background, which
# on a lifted charcoal collapses the detail text into mush; a fixed value keeps a
# readable contrast ratio whatever the ground.
def rgb(hexcode):
    h = hexcode.lstrip("#")
    return "\x1b[38;2;%d;%d;%dm" % tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# {n} is a count inside a gloss: numbers read as evidence, so they take the weight
# and their labels stay grey. The five theme-driven entries are placeholders here —
# apply_theme() points them at the running theme's own greys.
C = {"bold": "\x1b[1m", "dim": "\x1b[2m", "red": "\x1b[31m", "green": "\x1b[32m",
     "yellow": "\x1b[33m", "cyan": "\x1b[36m", "orange": "\x1b[38;5;209m",
     "pending": "\x1b[2m", "clock": "\x1b[2m", "sep": "\x1b[2m",
     "n": EMPHASIS, "/": R}


def apply_theme(name):
    """Point the colour table and the prompt tint at one of THEMES."""
    global THEME_NAME, PROMPT_BG
    THEME_NAME = name
    t = THEMES[name]
    C["orange"] = rgb(t["accent"])     # "orange" is the accent slot, whatever its hue
    for role in ("dim", "pending", "clock", "sep"):
        C[role] = rgb(t[role])
    h = t["tint"].lstrip("#")
    PROMPT_BG = "\x1b[48;2;%d;%d;%dm" % tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
TAG = re.compile(r"\{(" + "|".join(re.escape(k) for k in C) + r")\}")
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


# Inline per-step spinner (@step, @run): braille dots cycling in a block.
STEP_SPINNER = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
STEP_COLOUR = "orange"   # same as the pinned spinner
STEP_DONE = "green"
STEP_DONE_MARK = "✓"     # a plain tick; "◇" for clack's "submitted step"
STEP_PENDING_MARK = "·"  # a phase that hasn't run yet
RUNNING_MARK = "..."     # appended to a label while its row runs, dropped when it lands
SEP = "·"                # tinted automatically wherever it turns up inside a gloss

# "❯" marks everything the human typed — the command at a @prompt and the answer
# they pick in a @select alike, so the eye finds their turns in the transcript.
HUMAN_MARK = "❯"

# How often the clock on a running @run row moves. Two spinner frames: often
# enough to read as counting, slow enough not to strobe.
CLOCK_TICK = 0.22

# @select — a TUI-style picker. The highlight starts on the first option, walks
# down to the chosen one, then pulses to confirm. Times are seconds.
SELECT_INTRO = 0.55      # options on screen, nothing highlighted yet
SELECT_LEAD = 0.90       # beat on the first option, while the human reads
SELECT_STEP = 0.75       # beat on each row the highlight passes through
SELECT_SETTLE = 0.85     # beat on the chosen row before it confirms
SELECT_FILL = True       # True: the bar spans the frame, fzf-style
SELECT_FLASH = 0.22      # how long the confirm flash is held
SELECT_PULSES = 1        # how many times the chosen row flashes
SELECT_REST = 0.25       # beat after the flash, before the run continues
SELECT_PAD = 5           # "  ❯ " in front of an option and a space behind it, so a
                         # filled bar runs to exactly COLS

# Marker for a question handed back to the human (@ask). "" for no marker.
ASK_MARK = ""            # no marker; the question stands on its own
ASK_COLOUR = "orange"

# Minimum hold on the final frame before the recording loops.
END_PAUSE = 3.0

# Background tint behind a @prompt line, so the human's input reads as theirs.
# "" for none; PROMPT_FILL extends the tint to the full width of the row.
PROMPT_BG = "\x1b[48;2;46;50;60m"   # one step up from the background
PROMPT_FILL = False

FRAME = 0.11
# Typing rhythm. A fixed table cycles and reads as uniform, so this is drawn from
# a seeded RNG instead: fast within a word, a beat at word boundaries, and the
# occasional hesitation. Seeded, so a rebuild is still byte-identical.
TYPING_SEED = 7
KEY = (0.016, 0.052)      # per-character range
WORD_PAUSE = (0.05, 0.11)  # extra after a space...
WORD_PAUSE_CHANCE = 0.45   # ...this often
HESITATE = (0.16, 0.30)    # an occasional longer think
HESITATE_CHANCE = 0.05

# A spinning row holds for `secs` give or take this fraction, so a run of rows
# doesn't tick like a metronome. Symmetric, so the average duration is unchanged.
HOLD_JITTER = 0.40

# Named themes. Each carries its own accent (used for every in-progress state and
# the human's mark), prompt tint and the three phase-row greys, because all of
# them have to hold a contrast relationship with the background. The greys are one
# ladder from the ground up to `dim`: pending ~0.47 of the way, sep ~0.55, clock
# ~0.67. kiro and catppuccin redraw that ladder on their own grounds rather than
# borrowing ghostty's hexes.
THEMES = {
    "ghostty": {           # Ghostty's default, dropped a notch: still a charcoal
        "fg": "#e6e8ea", "bg": "#21242b",   # rather than a near-black, but with
        "accent": "#ff875f", "dim": "#a9afb8", "tint": "#2e323c",  # more contrast
        "pending": "#5f656e", "clock": "#7b818a", "sep": "#6b7178",
        "win": "#21242b", "bar": "#2e323b", "outer": "#131519",
        "palette": ["#1d1f21", "#cc6666", "#b5bd68", "#f0c674", "#81a2be", "#b294bb",
                    "#8abeb7", "#c5c8c6", "#666666", "#d54e53", "#b9ca4a", "#e7c547",
                    "#7aa6da", "#c397d8", "#70c0b1", "#eaeaea"],
    },
    "kiro": {              # near-black, one vivid violet accent, near-white text
        "fg": "#f2f2f7", "bg": "#0e0e13",
        "accent": "#b48cff", "dim": "#8b8fa3", "tint": "#1b1b24",
        "pending": "#484a56", "clock": "#626473", "sep": "#535562",
        "win": "#0e0e13", "bar": "#22222c", "outer": "#050508",
        "palette": ["#2a2a35", "#ff6b81", "#3fd07f", "#e6c07b", "#7aa2f7", "#b48cff",
                    "#63d5e0", "#d8d8e0", "#4a4a58", "#ff8fa0", "#66e0a0", "#f0d49a",
                    "#9ab8ff", "#c9a8ff", "#8ce6ee", "#ffffff"],
    },
    "catppuccin": {        # Catppuccin Mocha
        "fg": "#cdd6f4", "bg": "#1e1e2e",
        "accent": "#fab387", "dim": "#9399b2", "tint": "#282a3c",
        "pending": "#55576c", "clock": "#6c7086", "sep": "#5e6176",
        "win": "#1e1e2e", "bar": "#313244", "outer": "#11111b",
        "palette": ["#45475a", "#f38ba8", "#a6e3a1", "#f9e2af", "#89b4fa", "#f5c2e7",
                    "#94e2d5", "#bac2de", "#585b70", "#f38ba8", "#a6e3a1", "#f9e2af",
                    "#89b4fa", "#f5c2e7", "#94e2d5", "#a6adc8"],
    },
}
THEME_NAME = "ghostty"
apply_theme(THEME_NAME)   # so an import is never left holding the placeholders


def _tags(text, close):
    """Substitute inline tags. {/} pops back to the enclosing tag, or to `close`."""
    stack = [close]

    def sub(m):
        if m.group(1) == "/":
            if len(stack) > 1:
                stack.pop()
            return WEIGHT_OFF + stack[-1]   # weight only; the colour comes back with it
        stack.append(stack[-1] + C[m.group(1)])
        return C[m.group(1)]

    return TAG.sub(sub, text)


def style(s):
    """Inline tags on their own: an unmatched {/} resets."""
    return _tags(s, R)


def span(text, base):
    """Inline tags inside a field that already carries a colour — a gloss.

    {/} returns to `base` rather than resetting: a reset would drop the gloss grey
    and leave the rest of the field in the default foreground.
    """
    return base + _tags(text, base)


def visible(s):
    return ANSI.sub("", s)


def cells(s):
    """Display width. Wide glyphs (emoji, CJK) take two cells, everything else one."""
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in s)


def pad(s, width):
    """Pad styled text to `width` display cells."""
    return s + " " * max(0, width - cells(visible(s)))


def spinner(i):
    return STEP_SPINNER[i % len(STEP_SPINNER)]


def row(glyph, label, gloss="", clock="", muted=False):
    """One phase row on the shared grid (see the module docstring).

    `glyph` arrives already coloured, and is padded by display width rather than
    character count — 🎉 is two cells and takes no trailing space, ✓ is one and
    does, and either way the label lands on col 3. `muted` is a row that hasn't
    run: pending grey throughout, with neither gloss nor clock to show yet.
    """
    if muted:
        return C["pending"] + pad(glyph, GLYPH_W) + style(label) + R
    out = pad(glyph, GLYPH_W) + EMPHASIS + pad(style(label), LABEL_W) + WEIGHT_OFF
    if gloss:
        body = span(gloss.replace(SEP, "{sep}" + SEP + "{/}"), C["dim"])
        out += pad(body, GLOSS_W) if clock else body
    elif clock:
        out += " " * GLOSS_W
    return out + (C["clock"] + clock if clock else "") + R


def clock_secs(s):
    """"1:07" -> 67. A running row counts up to its clock, so it has to do arithmetic."""
    m, _, sec = s.partition(":")
    if not (m.isdigit() and sec.isdigit()):
        raise SystemExit(f"clock must be M:SS, not {s!r}")
    return int(m) * 60 + int(sec)


def fmt_clock(secs):
    m, s = divmod(round(secs), 60)
    return f"{m}:{s:02d}"


class Cast:
    def __init__(self):
        self.t, self.events, self.warn = 0.0, [], []
        self.rng = random.Random(TYPING_SEED)
        self.last_blank = True
        self.frame = 0
        self.pending = None      # (label, gloss) of a @step! left unresolved
        self.pending_dist = 0    # rows between it and the cursor
        self.rows = []           # the open @checklist block, if there is one
        self.last_visible = 0.0

    def out(self, data, dt=0.0):
        self.t += dt
        self.events.append([round(self.t, 3), "o", data])
        if data:
            self.last_visible = self.t

    def wait(self, s):
        self.t += s

    def line(self, text="", dt=0.12):
        styled = style(text)
        shown = visible(styled)
        blank = not shown.strip()
        if blank and self.last_blank:     # collapse runs of blank lines to one
            return
        if cells(shown) > COLS:
            self.warn.append(f">{COLS} cols: {shown[:60]}")
        self.out(styled + "\r\n", dt)
        self.advance()
        self.last_blank = blank

    def check_row(self, label, *glosses, clock=""):
        """Warn when a field outgrows its column.

        A row that overflows pushes everything after it sideways, and a column of
        rows going ragged is invisible until the GIF is rendered.
        """
        if cells(visible(style(label))) > LABEL_W:
            self.warn.append(f"label >{LABEL_W} cols: {label}")
        # A gloss beside a clock gets one column fewer than it owns: filling the
        # column leaves no gap, and "commit2:10" reads as one word.
        limit = GLOSS_W - 1 if clock else GLOSS_MAX
        for g in glosses:
            if cells(visible(style(g))) > limit:
                self.warn.append(f"gloss >{limit} cols: {g}")

    def beats(self, secs):
        """Spinner frames spanning `secs` ± HOLD_JITTER: [(index, delay)], and the hold.

        Frames sit a fixed FRAME apart, so the leftover rides on the last one —
        otherwise the hold snaps to multiples of FRAME and the jitter quantises
        away. Frame i is shown at i * FRAME, which never reaches the hold: a clock
        interpolated off it stops just short of its target, and lands exactly on it
        only when the row does.
        """
        hold = secs * self.rng.uniform(1 - HOLD_JITTER, 1 + HOLD_JITTER)
        n = max(1, int(hold / FRAME))
        slack = max(0.0, hold - n * FRAME)
        return [(i, 0.0 if i == 0 else FRAME + (slack if i == n - 1 else 0.0))
                for i in range(n)], hold

    def type(self, chars):
        for i, ch in enumerate(chars):
            dt = self.rng.uniform(*KEY)
            if i and chars[i - 1] == " " and self.rng.random() < WORD_PAUSE_CHANCE:
                dt += self.rng.uniform(*WORD_PAUSE)     # a beat between words
            elif self.rng.random() < HESITATE_CHANCE:
                dt += self.rng.uniform(*HESITATE)       # an occasional hesitation
            self.out(ch, dt)

    def prompt(self, text):
        bg, fg_off = PROMPT_BG, "\x1b[39m"
        self.out(f"{bg}{C['orange']}{HUMAN_MARK}{fg_off} ", 0.25)
        head, sep, tail = text.partition(" ")
        if head.startswith("/"):          # the command carries the emphasis,
            self.out(C["bold"])           # its arguments don't
            self.type(head)
            self.out(WEIGHT_OFF)
            self.type(sep + tail)
        else:                             # a bare answer: emphasise the whole thing
            self.out(C["bold"])
            self.type(text)
            self.out(WEIGHT_OFF)
        self.wait(0.45)
        self.out((" \x1b[K" if (bg and PROMPT_FILL) else " ") + R + "\r\n")
        self.advance()
        self.last_blank = False

    def step(self, secs, label, gloss="", pending=False):
        """A phase row that spins for `secs`, then ticks over to done in place."""
        self.check_row(label + RUNNING_MARK, gloss)
        frames, _ = self.beats(secs)
        for i, dt in frames:
            self.out("\r\x1b[2K" + row(C[STEP_COLOUR] + spinner(i),
                                       label + RUNNING_MARK, gloss), dt)
        if pending:                   # leave it spinning; @resolve finishes it later
            self.out("\r\x1b[2K" + row(C[STEP_COLOUR] + spinner(len(frames)),
                                       label + RUNNING_MARK, gloss) + "\r\n", FRAME)
            self.pending, self.pending_dist = (label, gloss), 1   # cursor one row below
        else:
            self.out("\r\x1b[2K" + row(C[STEP_DONE] + STEP_DONE_MARK, label, gloss)
                     + "\r\n", FRAME)
            self.advance()
        self.last_blank = False

    def static_row(self, glyph, label, gloss="", clock=""):
        """A phase row that never ran: printed finished, in one go."""
        self.check_row(label, gloss, clock=clock)
        self.out("\r\x1b[2K" + row(style(glyph), label, gloss, clock) + "\r\n", 0.12)
        self.advance()
        self.last_blank = False

    def _select_row(self, text, width, on, flash=False):
        """One picker row, padded to `width` so the highlight bar can't jitter."""
        body = pad(style(text), width)
        if not on:
            return f"\r\x1b[2K    {C['dim']}{body}{R}"
        # The human's choice wears the human's colour: the same tint as a @prompt
        # line, plus the accent cursor. The cursor takes col 3 and the text col 5,
        # so a chosen option sits on the same columns as an unchosen one. Flashing
        # swaps the tint for reverse video, which paints the whole bar in the accent.
        tint = "\x1b[7m" if flash else PROMPT_BG
        fg_off = "" if flash else "\x1b[39m"   # back to default fg, keeping the tint
        return (f"\r\x1b[2K{tint}  {C['orange']}{HUMAN_MARK}{fg_off} "
                f"{C['bold']}{body}{WEIGHT_OFF} {R}")

    def advance(self, n=1):
        """The cursor moved down n rows; a pending step is now n rows further up."""
        if self.pending is not None:
            self.pending_dist += n

    def repaint_pending(self, done=False, dt=0.0):
        """Redraw a @step! left pending, n rows above, without moving the cursor."""
        if self.pending is None:
            return
        self.frame += 1
        label, gloss = self.pending
        glyph = (C[STEP_DONE] + STEP_DONE_MARK if done
                 else C[STEP_COLOUR] + spinner(self.frame))
        n = self.pending_dist
        up, down = (f"\x1b[{n}A" if n else ""), (f"\x1b[{n}B" if n else "")
        self.out(up + "\r\x1b[2K"
                 + row(glyph, label + ("" if done else RUNNING_MARK), gloss)
                 + down + "\r", dt)
        if done:
            self.pending, self.pending_dist = None, 0

    def checklist(self, labels):
        """Print every phase up front, all pending, cursor left on the last row.

        Laid down once and repainted in place from then on, exactly like @select's
        highlight, so the block scrolls with the transcript instead of pinning
        itself to a screen row.
        """
        if self.pending is not None:
            raise SystemExit("@checklist while a @step! is still pending: both would "
                             "repaint above the cursor. @resolve it first")
        for label in labels:
            self.check_row(label + RUNNING_MARK)
        self.rows = [{"label": label, "state": "pending", "gloss": "", "clock": "",
                      "frame": 0} for label in labels]
        self.paint_rows(0.12, first=True)
        self.last_blank = False

    def row_text(self, r):
        if r["state"] == "pending":
            return "\r\x1b[2K" + row(STEP_PENDING_MARK, r["label"], muted=True)
        if r["state"] == "running":
            return "\r\x1b[2K" + row(C[STEP_COLOUR] + spinner(r["frame"]),
                                     r["label"] + RUNNING_MARK, r["gloss"], r["clock"])
        return "\r\x1b[2K" + row(C[STEP_DONE] + STEP_DONE_MARK,
                                 r["label"], r["gloss"], r["clock"])

    def paint_rows(self, dt=0.0, first=False):
        """Repaint the whole block: up to its first row, rewrite it, end on its last.

        Net cursor movement is zero, so nothing outside the block has to know it
        happened — and a row that finished stays finished, because every frame
        redraws all of them from state rather than touching one in isolation.
        """
        n = len(self.rows)
        up = f"\x1b[{n - 1}A" if n > 1 else ""
        body = "\r\n".join(self.row_text(r) for r in self.rows)
        self.out(("" if first else up) + body, dt)
        if first:
            self.advance(n - 1)   # the block laid itself down; cursor is on its last row

    def next_row(self, label):
        """Index of `label` in the open checklist, refusing anything out of order.

        A screenplay typo here is worth catching at compile time rather than in
        the GIF, where it looks like a rendering bug.
        """
        if not self.rows:
            raise SystemExit(f"@run {label}: no @checklist is open")
        labels = [r["label"] for r in self.rows]
        if label not in labels:
            raise SystemExit(f"@run {label}: not in the checklist ({' | '.join(labels)})")
        i, nxt = labels.index(label), sum(r["state"] == "done" for r in self.rows)
        if i != nxt:
            expected = labels[nxt] if nxt < len(labels) else "nothing, the block is done"
            raise SystemExit(f"@run {label}: out of order — {expected} is next")
        return i

    def run(self, secs, label, gloss, done_gloss, clock=""):
        """Tick one checklist row over: spin for `secs`, then land it done.

        Each row's clock is its own stopwatch: it runs from 0:00 up to `clock`
        while the row spins, and is set exactly rather than interpolated once it
        lands. Rows time themselves, so the column adds up to the run's total.
        """
        r = self.rows[self.next_row(label)]
        self.check_row(label + RUNNING_MARK, gloss, done_gloss, clock=clock)
        target = clock_secs(clock) if clock else 0
        r.update(state="running", gloss=gloss, clock=fmt_clock(0) if clock else "")
        frames, hold = self.beats(secs)
        for j, dt in frames:
            r["frame"] = j
            if clock:   # the clock only moves every CLOCK_TICK, whatever the frame rate
                held = int(j * FRAME / CLOCK_TICK) * CLOCK_TICK
                r["clock"] = fmt_clock(target * (held / hold if hold else 0.0))
            self.paint_rows(dt)
        r.update(state="done", gloss=done_gloss, clock=clock)
        self.paint_rows(FRAME)

    def close_rows(self):
        """Drop the cursor below an open checklist, so the next thing starts clean."""
        if not self.rows:
            return
        self.out("\r\n")
        self.advance()
        self.rows = []

    def select(self, chosen, options):
        """A picker: the highlight lands on option 1, walks to `chosen`, confirms.

        Painted as a plain stream — the block is laid down once and every repaint
        is a relative move up and back, never leaving a trailing newline, so the
        block scrolls with the transcript like any other content.
        """
        n = len(options)
        longest = max(cells(visible(style(o))) for o in options)
        width = COLS - SELECT_PAD if SELECT_FILL else longest
        if longest + SELECT_PAD > COLS:
            self.warn.append(f">{COLS} cols: {visible(style(options[0]))[:60]}")
        up, first = (f"\x1b[{n - 1}A" if n > 1 else ""), True

        def paint(cur, dt, flash=False):
            nonlocal first
            rows = "\r\n".join(self._select_row(o, width, i == cur, flash)
                               for i, o in enumerate(options))
            was_first = first
            self.out(("" if first else up) + rows, dt)
            first = False
            if was_first:
                self.advance(n - 1)     # the block laid itself down; cursor is on its last row
            self.repaint_pending()      # the step above keeps turning while you choose

        paint(-1, 0.12)              # the options land first, unhighlighted
        paint(0, SELECT_INTRO)       # then the highlight arrives on the first one
        hold = SELECT_LEAD
        for i in range(1, chosen):        # walk the highlight down to the answer
            paint(i, hold)
            hold = SELECT_STEP
        chosen -= 1
        if chosen:
            hold = SELECT_SETTLE
        for _ in range(SELECT_PULSES):    # confirm
            paint(chosen, hold, flash=True)
            paint(chosen, SELECT_FLASH)
            hold = SELECT_FLASH
        self.out("\r\n", SELECT_REST)
        self.advance()
        self.last_blank = False


def fields(text, lo, hi, form):
    """Split a directive's "|" fields, and say so plainly if there are the wrong number."""
    parts = [p.strip() for p in text.split("|")]
    if not lo <= len(parts) <= hi:
        raise SystemExit(f"{form}: expected {lo}-{hi} fields, got {len(parts)}: {text}")
    return parts + [""] * (hi - len(parts))


def render(script):
    c = Cast()
    c.out("\x1b[2J\x1b[H\x1b[?25l")
    c.wait(0.4)
    lines = script.split("\n")
    if lines and lines[-1] == "":   # the file's closing newline, not a blank row: it
        lines.pop()                 # would cost a row, and every row is spoken for
    for raw in lines:
        if raw.startswith("#"):        # comment: only at column 0, so indented
            continue                   # markdown headings in content still print
        if not raw.startswith("@"):
            c.close_rows()
            c.line(raw)
            continue
        cmd, _, rest = raw[1:].partition(" ")
        rest = rest.strip()
        if cmd not in ("pause", "checklist", "run", "clear"):
            c.close_rows()             # anything that writes elsewhere ends the block
        if cmd == "prompt":
            c.prompt(rest)
        elif cmd == "pause":          # wait
            c.wait(float(rest))
        elif cmd == "clear":          # wipe and start again at the top
            c.out("\x1b[2J\x1b[H")
            c.pending, c.pending_dist, c.rows = None, 0, []   # nothing above to repaint
            c.last_blank = True
        elif cmd == "resolve":        # finish a @step! that was left pending
            c.repaint_pending(done=True, dt=float(rest or 0.2))
        elif cmd == "ask":            # a question handed back to the human, at col 3
            mark = f"{C[ASK_COLOUR]}{ASK_MARK}{R} " if ASK_MARK else ""
            c.out("  " + mark + style("{bold}" + rest + "{/}") + "\r\n", 0.12)
            c.advance()
            c.last_blank = False
        elif cmd in ("step", "step!"):   # a phase row that spins, then ticks over
            secs, _, text = rest.partition(" ")
            label, gloss = fields(text, 1, 2, f"@{cmd} <secs> <label>|<gloss>")
            c.step(float(secs), label, gloss, pending=(cmd == "step!"))
        elif cmd == "checklist":      # every phase up front, all pending
            c.checklist([p.strip() for p in rest.split("|")])
        elif cmd == "run":            # tick one checklist row over
            secs, _, text = rest.partition(" ")
            label, gloss, third, fourth = fields(
                text, 2, 4, "@run <secs> <label>|<gloss>[|<done gloss>]|<clock>")
            # 4 fields split the gloss either side of the tick; 3 is one gloss and a clock
            done_gloss, clock = (third, fourth) if fourth else (gloss, third)
            c.run(float(secs), label, gloss, done_gloss, clock)
        elif cmd == "row":            # a finished phase row, printed as-is
            glyph, _, text = rest.partition(" ")
            label, gloss, clock = fields(text, 1, 3, "@row <glyph> <label>|<gloss>")
            c.static_row(glyph, label, gloss, clock)
        elif cmd == "select":         # a picker; "|" splits the options
            idx, _, text = rest.partition(" ")
            c.select(int(idx), [p.strip() for p in text.split("|")])
        else:
            raise SystemExit(f"unknown directive @{cmd}")
    c.wait(max(0.0, END_PAUSE - (c.t - c.last_visible)))   # hold before the loop
    c.out("\x1b[?25h")
    return c


def cast_theme():
    t = THEMES[THEME_NAME]
    return {"fg": t["fg"], "bg": t["bg"], "palette": ":".join(t["palette"])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("-o", "--out", default="demo.cast")
    ap.add_argument("--theme", default="ghostty", choices=sorted(THEMES),
                    help="colour theme (default: ghostty)")
    ap.add_argument("--ask-mark", default=None,
                    help='marker before an @ask question; "" for none')
    a = ap.parse_args()
    apply_theme(a.theme)
    if a.ask_mark is not None:
        globals()["ASK_MARK"] = a.ask_mark
    c = render(open(a.script).read())
    hdr = {"version": 2, "width": COLS, "height": ROWS, "theme": cast_theme(),
           "title": "auto-task", "env": {"TERM": "xterm-256color", "SHELL": "/bin/zsh"}}
    with open(a.out, "w") as f:
        f.write(json.dumps(hdr) + "\n")
        for e in c.events:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"{a.out}: {c.t:.1f}s, {len(c.events)} events, {COLS}x{ROWS}")
    for w in c.warn:
        print(f"  WARN {w}")


if __name__ == "__main__":
    main()
