#!/usr/bin/env python3
"""Render a demo screenplay to an asciicast.

Directives, all starting at column 0. Note what each number means — they are not
all durations:

  @prompt <text>         a human types <text> at the prompt, then hits enter.
                         Takes NO number. A leading /command is bolded, its
                         arguments are not. Stops the spinner first.
  @pause <secs>          wait, showing nothing new
  @clear                 wipe the screen and start again at the top

  @step <secs> <a>|<b>   a line with its own braille spinner in front. <secs> is
                         PER CHUNK, not total — three chunks at 0.45 is ~1.35s,
                         give or take CHUNK_JITTER so it doesn't tick like a
                         metronome.
                         The chunks appear one after another, then the line
                         resolves to STEP_DONE_MARK.
  @step! <secs> <a>|<b>  the same, but the line is left SPINNING. It keeps
                         turning through whatever is printed below it until an
                         @resolve finishes it. Use when the step is genuinely
                         blocked on the human, e.g. clarify waiting on an answer.
  @resolve <secs>        finish the pending @step! in place, however many lines
                         have been printed since. <secs> is the beat before the
                         tick lands. One pending step at a time.

  @ask <text>            a question handed back to you, marked with ASK_MARK
  @select <n> <a>|<b>    a TUI picker. <n> is the 1-BASED OPTION that ends up
                         chosen — not a duration. The highlight lands on the
                         first option, walks down to <n>, then pulses to confirm.
                         Timings come from the SELECT_* constants below.

  anything else          printed verbatim (blank lines and indentation included)
  # at column 0          a comment; indented "#" lines are content, not comments

Blank lines never double up: consecutive blanks collapse to one, and @prompt
adds a separating blank only if there isn't one already.

Inline styling: {bold} {dim} {orange} {green} {cyan} {yellow}, closed by {/}.
Use {green}✓{/} explicitly for a tick; there is no implicit marker on plain lines.

Everything scrolls naturally: content never uses absolute cursor addressing, so
the prompt moves up the screen like a real terminal and nothing leaves ghosts.
The two in-place effects — @select's highlight and @resolve — move relative to
the cursor and return to it, so they scroll with the transcript like any other
content. The pinned status line is the sole exception: it owns the row below the
scroll region (DECSTBM) and never participates in scrolling.
"""
import argparse, json, random, re

COLS, ROWS = 80, 15   # peak height is 13 rows either side of the @clear


R = "\x1b[0m"
# "dim" is an explicit grey, not SGR 2. SGR 2 darkens toward the background, which
# on a lifted charcoal collapses the detail text into mush; a fixed value keeps a
# readable contrast ratio whatever the ground.
def rgb(hexcode):
    h = hexcode.lstrip("#")
    return "\x1b[38;2;%d;%d;%dm" % tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


C = {"bold": "\x1b[1m", "dim": "\x1b[2m", "red": "\x1b[31m", "green": "\x1b[32m",
     "yellow": "\x1b[33m", "cyan": "\x1b[36m", "orange": "\x1b[38;5;209m", "/": R}


def apply_theme(name):
    """Point the colour table and the prompt tint at one of THEMES."""
    global THEME_NAME, PROMPT_BG
    THEME_NAME = name
    t = THEMES[name]
    C["orange"] = rgb(t["accent"])     # "orange" is the accent slot, whatever its hue
    C["dim"] = rgb(t["dim"])
    h = t["tint"].lstrip("#")
    PROMPT_BG = "\x1b[48;2;%d;%d;%dm" % tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
TAG = re.compile(r"\{(" + "|".join(re.escape(k) for k in C) + r")\}")
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


# Inline per-step spinner (@step): braille dots cycling in a block.
STEP_SPINNER = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
STEP_COLOUR = "orange"   # same as the pinned spinner
STEP_DONE = "green"
STEP_DONE_MARK = "✓"     # a plain tick; "◇" for clack's "submitted step"

# @select — a TUI-style picker. The highlight starts on the first option, walks
# down to the chosen one, then pulses to confirm. Times are seconds.
SELECT_CURSOR = "❯"     # gutter marker on the highlighted row; JetBrains Mono has it
SELECT_INTRO = 0.55      # options on screen, nothing highlighted yet
SELECT_LEAD = 0.90       # beat on the first option, while the human reads
SELECT_STEP = 0.75       # beat on each row the highlight passes through
SELECT_SETTLE = 0.85     # beat on the chosen row before it confirms
SELECT_FILL = False      # True: the bar spans the frame, fzf-style
SELECT_FLASH = 0.22      # how long the confirm flash is held
SELECT_PULSES = 1        # how many times the chosen row flashes
SELECT_REST = 0.25       # beat after the flash, before the run continues

# Marker for a question handed back to the human (@ask). "" for no marker.
ASK_MARK = ""            # no marker; the question stands on its own
ASK_COLOUR = "orange"

# Minimum hold on the final frame before the recording loops.
END_PAUSE = 3.0

# Background tint behind a @prompt line, so the human's input reads as theirs.
# "" for none; PROMPT_FILL extends the tint to the full width of the row.
PROMPT_BG = "\x1b[48;2;49;54;64m"   # one step up from the background
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

# @step chunks hold for `secs` give or take this fraction, so the reveal doesn't
# tick like a metronome. Symmetric, so the average duration is unchanged.
CHUNK_JITTER = 0.40

# Named themes. Each carries its own accent (used for every in-progress state and
# the prompt marker), dim (explicit, never SGR 2) and prompt tint, because those
# three have to hold a contrast relationship with the background.
THEMES = {
    "ghostty": {           # Ghostty's default, dropped a notch: still a charcoal
        "fg": "#e6e8ea", "bg": "#21242b",   # rather than a near-black, but with
        "accent": "#ff875f", "dim": "#9aa4b5", "tint": "#2b2f37",  # more contrast
        "win": "#21242b", "bar": "#2e323b", "outer": "#131519",
        "palette": ["#1d1f21", "#cc6666", "#b5bd68", "#f0c674", "#81a2be", "#b294bb",
                    "#8abeb7", "#c5c8c6", "#666666", "#d54e53", "#b9ca4a", "#e7c547",
                    "#7aa6da", "#c397d8", "#70c0b1", "#eaeaea"],
    },
    "kiro": {              # near-black, one vivid violet accent, near-white text
        "fg": "#f2f2f7", "bg": "#0e0e13",
        "accent": "#b48cff", "dim": "#8b8fa3", "tint": "#1b1b24",
        "win": "#0e0e13", "bar": "#22222c", "outer": "#050508",
        "palette": ["#2a2a35", "#ff6b81", "#3fd07f", "#e6c07b", "#7aa2f7", "#b48cff",
                    "#63d5e0", "#d8d8e0", "#4a4a58", "#ff8fa0", "#66e0a0", "#f0d49a",
                    "#9ab8ff", "#c9a8ff", "#8ce6ee", "#ffffff"],
    },
    "catppuccin": {        # Catppuccin Mocha
        "fg": "#cdd6f4", "bg": "#1e1e2e",
        "accent": "#fab387", "dim": "#9399b2", "tint": "#282a3c",
        "win": "#1e1e2e", "bar": "#313244", "outer": "#11111b",
        "palette": ["#45475a", "#f38ba8", "#a6e3a1", "#f9e2af", "#89b4fa", "#f5c2e7",
                    "#94e2d5", "#bac2de", "#585b70", "#f38ba8", "#a6e3a1", "#f9e2af",
                    "#89b4fa", "#f5c2e7", "#94e2d5", "#a6adc8"],
    },
}
THEME_NAME = "ghostty"


def style(s):
    return TAG.sub(lambda m: C[m.group(1)], s)


def visible(s):
    return ANSI.sub("", s)


class Cast:
    def __init__(self):
        self.t, self.events, self.warn = 0.0, [], []
        self.rng = random.Random(TYPING_SEED)
        self.last_blank = True
        self.frame = 0
        self.pending = None      # (text, width) of a @step left unresolved
        self.pending_dist = 0    # rows between it and the cursor
        self.last_visible = 0.0

    def out(self, data, dt=0.0):
        self.t += dt
        self.events.append([round(self.t, 3), "o", data])
        if data:
            self.last_visible = self.t

    def wait(self, s):
        self.t += s

    def line(self, text="", dt=0.12):
        blank = not visible(style(text)).strip()
        if blank and self.last_blank:     # collapse runs of blank lines to one
            return
        if len(visible(style(text))) > COLS:
            self.warn.append(visible(style(text))[:70])
        self.out(style(text) + "\r\n", dt)
        self.advance()
        self.last_blank = not visible(style(text)).strip()

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
        self.out(f"{bg}{C['orange']}>{fg_off} ", 0.25)
        head, sep, tail = text.partition(" ")
        bold_off = "\x1b[22m"            # weight only — a full reset would drop the tint
        if head.startswith("/"):          # the command carries the emphasis,
            self.out(C["bold"])           # its arguments don't
            self.type(head)
            self.out(bold_off)
            self.type(sep + tail)
        else:                             # a bare answer: emphasise the whole thing
            self.out(C["bold"])
            self.type(text)
            self.out(bold_off)
        self.wait(0.45)
        self.out((" \x1b[K" if (bg and PROMPT_FILL) else " ") + R + "\r\n")
        self.last_blank = False

    def step(self, secs, parts, pending=False):
        """A line that spins in place, revealing `parts` one at a time, then ticks.

        `secs` is per part, so the line grows chunk by chunk while it works.
        """
        shown, f = "", 0
        for part in parts:
            shown += part
            hold = secs * self.rng.uniform(1 - CHUNK_JITTER, 1 + CHUNK_JITTER)
            n = max(1, int(hold / FRAME))
            # Spinner frames are a fixed FRAME apart, so without this the hold
            # snaps to multiples of FRAME and the jitter quantises away.
            slack = max(0.0, hold - n * FRAME)
            for i in range(n):
                glyph = STEP_SPINNER[f % len(STEP_SPINNER)]
                f += 1
                self.out(f"\r\x1b[2K{C[STEP_COLOUR]}{glyph}{R} {style(shown)}",
                         0.0 if f == 1 else FRAME + (slack if i == n - 1 else 0.0))
        if pending:                   # leave it spinning; @resolve finishes it later
            self.out(f"\r\x1b[2K{C[STEP_COLOUR]}"
                     f"{STEP_SPINNER[f % len(STEP_SPINNER)]}{R} {style(shown)}\r\n", FRAME)
            self.pending, self.pending_dist = shown, 1   # cursor is one row below it
        else:
            self.out(f"\r\x1b[2K{C[STEP_DONE]}{STEP_DONE_MARK}{R} {style(shown)}\r\n", FRAME)
            self.advance()
        self.last_blank = False

    def _select_row(self, text, width, on, flash=False):
        """One picker row, padded to `width` so the highlight bar can't jitter."""
        body = style(text) + " " * (width - len(visible(style(text))))
        if not on:
            return f"\r\x1b[2K  {C['dim']}{body}{R}"
        # The human's choice wears the human's colour: the same tint as a @prompt
        # line, plus the accent cursor. Flashing swaps the tint for reverse video,
        # which paints the whole bar in the accent.
        tint = "\x1b[7m" if flash else PROMPT_BG
        fg_off = "" if flash else "\x1b[39m"   # back to default fg, keeping the tint
        bold, bold_off = C["bold"], "\x1b[22m"  # weight only — a reset drops the tint
        return (f"\r\x1b[2K{tint}{C['orange']}{SELECT_CURSOR}{fg_off} "
                f"{bold}{body}{bold_off} {R}")

    def _step_line(self, text, done):
        mark = (f"{C[STEP_DONE]}{STEP_DONE_MARK}" if done
                else f"{C[STEP_COLOUR]}{STEP_SPINNER[self.frame % len(STEP_SPINNER)]}")
        return f"\r\x1b[2K{mark}{R} {style(text)}"

    def advance(self, n=1):
        """The cursor moved down n rows; a pending step is now n rows further up."""
        if self.pending is not None:
            self.pending_dist += n

    def repaint_pending(self, done=False, dt=0.0):
        """Redraw a @step left pending, n rows above, without moving the cursor."""
        if self.pending is None:
            return
        self.frame += 1
        n = self.pending_dist
        up, down = (f"\x1b[{n}A" if n else ""), (f"\x1b[{n}B" if n else "")
        self.out(up + self._step_line(self.pending, done) + down + "\r", dt)
        if done:
            self.pending, self.pending_dist = None, 0

    def select(self, chosen, options):
        """A picker: the highlight lands on option 1, walks to `chosen`, confirms.

        Painted as a plain stream — the block is laid down once and every repaint
        is a relative move up and back, never leaving a trailing newline, so the
        block scrolls with the transcript like any other content.
        """
        n = len(options)
        width = COLS - 4 if SELECT_FILL else max(len(visible(style(o))) for o in options)
        if width + 4 > COLS:
            self.warn.append(visible(style(options[0]))[:70])
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


def render(script):
    c = Cast()
    c.out("\x1b[2J\x1b[H\x1b[?25l")
    c.wait(0.4)
    for raw in script.split("\n"):
        if raw.startswith("#"):        # comment: only at column 0, so indented
            continue                   # markdown headings in content still print
        if not raw.startswith("@"):
            c.line(raw)
            continue
        cmd, _, rest = raw[1:].partition(" ")
        if cmd.endswith("!") and cmd[:-1] == "step":
            pass
        rest = rest.strip()
        if cmd == "prompt":
            c.prompt(rest)
        elif cmd == "pause":          # wait
            c.wait(float(rest))
        elif cmd == "clear":          # wipe and start again at the top
            c.out("\x1b[2J\x1b[H")
            c.pending, c.pending_dist = None, 0   # nothing above to resolve now
            c.last_blank = True
        elif cmd == "resolve":        # finish a @step! that was left pending
            c.repaint_pending(done=True, dt=float(rest or 0.2))
        elif cmd == "ask":            # a question handed back to the human
            mark = f"{C[ASK_COLOUR]}{ASK_MARK}{R} " if ASK_MARK else ""
            c.out(mark + style("{bold}" + rest + "{/}") + "\r\n", 0.12)
            c.advance()
            c.last_blank = False
        elif cmd in ("step", "step!"):  # inline spinner; "|" splits reveal chunks
            secs, _, text = rest.partition(" ")
            c.step(float(secs), [p for p in text.split("|")], pending=(cmd == "step!"))
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
        print(f"  WARN >{COLS} cols: {w}")


if __name__ == "__main__":
    main()
