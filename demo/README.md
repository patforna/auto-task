# Demo screencast

The looping terminal demo of the auto-task workflow. A screenplay (`demo.txt`) is compiled
to an [asciicast](https://docs.asciinema.org/manual/asciicast/v2/), rendered to a GIF and
framed in window chrome.

Nothing here is recorded from a live terminal — the clip is *constructed*. Its content
comes from a real run, so the artefacts and counts are true (see [Provenance](#provenance)).

## Rendering

```sh
./render.sh                 # demo.txt -> demo.gif + demo.html
./render.sh other.txt       # a different screenplay
FONT_SIZE=15 ./render.sh    # half-resolution GIF (smaller file, softer on retina)
./variants.sh               # render every theme, for comparison
./variants.sh kiro          # just one
python3 test_cast.py        # check the compiler against a real terminal screen
```

```
demo.txt ──cast.py──> demo.cast ──agg──> demo-raw.gif ──chrome.py──> demo.gif
                          └────────mkpreview.py────────────────────> demo.html
```

| file                       | what it is                                                               | committed |
| -------------------------- | ------------------------------------------------------------------------ | --------- |
| `demo.txt`                 | the screenplay — the file you edit                                       | yes       |
| `cast.py`                  | screenplay -> asciicast. Its docstring is the language reference         | yes       |
| `test_cast.py`             | 31 checks: fixtures replayed into a `pyte.Screen`, asserted cell by cell | yes       |
| `chrome.py`                | frames agg's GIF in a window — corners, title bar, traffic lights        | yes       |
| `mkpreview.py`             | wraps a cast in a self-contained HTML player                             | yes       |
| `render.sh`, `variants.sh` | the two entry points                                                     | yes       |
| `demo.cast`                | asciicast v2 — the source of truth for timing                            | yes       |
| `demo.gif`                 | the deliverable, framed, ~300 KB                                         | yes       |
| `demo-raw.gif`             | agg's bare output, before chrome                                         | no        |
| `demo.html`                | scrubbing preview, player inlined, works offline                         | no        |
| `demo-<theme>.*`           | output of `variants.sh`                                                  | no        |
| `assets/`                  | asciinema player, fetched on first preview                               | no        |
| `transcripts/`             | session transcripts behind Provenance, kept out of the repo              | no        |

Needs `python3`, [`agg`](https://github.com/asciinema/agg) (`brew install agg`) and `uv`
(for Pillow, which draws the chrome). If Pillow is unreachable, `render.sh` warns and falls
back to the unframed GIF. `curl` is used once, to fetch the player. `test_cast.py` needs
`pyte`, and borrows one through `uv` if it isn't installed. The font chain `render.sh` pins —
JetBrains Mono, Menlo, Apple Color Emoji — is macOS-only as configured: install JetBrains Mono
(`brew install --cask font-jetbrains-mono`), and on another OS repoint `FONT` at a monospace
face, a text fallback that has the braille spinner and `✓`, and an emoji font.

**Watch `demo.html` while iterating** — it has a scrubber. But judge the *GIF*: it renders
at 2× and is meant to display at half width, which supersamples the text and comes out
sharper than the player at 100%.

## The screenplay language

Plain lines print verbatim, blank lines and indentation included. Directives and `#`
comments start at column 0 — an indented `#` is content, so markdown headings survive.

The numbers are not all durations:

| directive                                     | what it does                                                         |
| --------------------------------------------- | -------------------------------------------------------------------- |
| `@prompt <text>`                              | a human types it, then enter. **No number.** A leading `/command` is bolded and its arguments are not; a bare answer is bolded whole |
| `@step <secs> <l>\|<g>`                       | a phase row that spins for `<secs>` — the **whole row**, ±`HOLD_JITTER` — then ticks over to done in place |
| `@step! <secs> <l>\|<g>`                      | the same, but left **spinning** until an `@resolve`. For a step genuinely blocked on the human |
| `@resolve <secs>`                             | finish the pending `@step!` in place, however far the cursor has moved on. `<secs>` is the beat before the tick lands. One pending step at a time |
| `@checklist <a>\|<b>\|<c>`                    | print every phase up front, all pending, so the shape of the run is on screen before any of it happens |
| `@run <secs> <l>\|<g>\|<clock>`               | tick one checklist row over: it spins for `<secs>`, then lands. Rows must run in the order they were listed. `<clock>` is **how long that row took**, `M:SS` |
| `@run <secs> <l>\|<running>\|<done>\|<clock>` | four fields swap the gloss when the row lands — `fixing 2 of 3` becomes `3 fixed` |
| `@row <glyph> <l>\|<g>[\|<clock>]`            | one finished phase row, printed as-is: no spinner, no tick, no `...`. **No number.** For a phase that never runs, e.g. the signoff. With neither gloss nor clock it is a heading, and its label runs free |
| `@detail <text>`                              | an indented line under a heading: col 3, in the gloss grey, its `·` separators tinted for you. **No number.** |
| `@ask <text>`                                 | a question handed back to you: col 3, bold, prefixed with `ASK_MARK` (currently none) |
| `@select <n> <a>\|<b>`                        | a TUI picker. `<n>` is the **1-based option chosen**, not a duration. The options land unhighlighted, the highlight arrives on the first, walks to `<n>`, then flashes to confirm |
| `@pause <secs>`                               | wait, showing nothing new |
| `@clear`                                      | wipe the screen and start again at the top |

Each row's clock is its own stopwatch: a running row counts *up* from `0:00` and lands
exactly on its `<clock>`, so the column adds up to the run's total. That ticking is what
stops a block of five rows reading as a slow typewriter.

### Phase rows

`@step`, `@step!`, `@checklist`, `@run` and `@row` all print on one grid, so a stack of
them reads as a column rather than a zigzag (columns are 1-indexed):

| cols  | what                                                                 |
| ----- | -------------------------------------------------------------------- |
| 1-2   | status glyph, padded by **display width**: `✓ · ⠋` take a trailing space, `🎉` is already two cells wide and takes none |
| 3-19  | label, bold in the default foreground. The width is only there to line a gloss up, so a row with neither gloss nor clock lets its label run on |
| 20-55 | gloss, in the gloss grey. A `·` inside it is tinted automatically |
| 56-59 | clock, `M:SS`, in its own grey. Never emphasised — it is read positionally, and competing with it flattens both |

A gloss with no clock beside it gets the rest of the row instead, running on to col 78. A
row with neither is a heading: nothing follows the label, so nothing has to line up, and it
is neither padded nor width-checked.

```
@row {green}✓{/} Task 001 ready for signoff
@detail task/001-hello-world-cli
```

The moment a gloss or a clock follows, the column is load-bearing again and an over-long
label warns as before. `@detail` is the line that belongs under such a heading: it starts
at col 3, on the label column, in the gloss grey.

`...` means "still running", and the renderer owns it: it appends the dots while a row
spins and drops them when the row lands, so screenplays write bare labels. A pending row
is the exception to all of the above — pending grey throughout, not bold, and neither
gloss nor clock, because it has nothing to report yet.

An open `@checklist` survives a `@pause`; anything else that prints closes the block and
drops the cursor below it, and `@clear` forgets it. A `@run` naming a row that isn't in the
checklist, or one that is out of order, fails the compile — in the GIF it would look like a
rendering bug. So does a `@checklist` opened while a `@step!` is still pending — both
repaint above the cursor. A gloss, a line past `COLS`, or a label with a gloss or clock
after it warns on render, because a column going ragged is invisible until then.

### Inline styling

`{bold}` `{dim}` `{orange}` `{green}` `{cyan}` `{yellow}` `{red}` and the three phase-row
greys `{pending}` `{clock}` `{sep}` — each closed by `{/}`. That is the whole set.
`{orange}` is the accent slot, whatever hue the theme gives it.

`{bold}` sets the weight **and** returns to the default foreground, which is what lifts a
count out of the grey around it: in `{bold}6{/} commits`, weight alone would only give you
a heavier grey. So one tag marks every count — the numbers are the evidence, their labels
are not.

`{/}` pops back to the *enclosing* tag rather than resetting, which is what lets
`{dim}… {bold}4{/} ACs{/}` leave `ACs` grey instead of dropping it to the default
foreground; inside a gloss or an `@detail` it returns to the gloss grey. No implicit
styling otherwise — write `{green}✓{/}` for a tick. A `·` tints itself inside a gloss and
inside an `@detail`, which between them cover every separator the screenplay writes, so
`{sep}` is never spelled out by hand; it stays available for a `·` on any other line.

A brace-wrapped word that isn't a tag — a typo, or one that was renamed away — warns on
render. Otherwise it prints as literal text in the GIF, and nothing catches that until you
watch it.

Two invariants so layout can't drift as you edit: consecutive blank lines collapse to one,
and the final frame is held for at least `END_PAUSE` before the loop restarts.

## Tuning

Constants at the top of `cast.py`:

| constant                                         | default         | effect                                         |
| ------------------------------------------------ | --------------- | ---------------------------------------------- |
| `COLS`, `ROWS`                                   | `80`, `16`      | frame size. Lines wider than `COLS` warn on render |
| `GLYPH_W`, `LABEL_W`, `GLOSS_W`                  | `2`, `17`, `36` | the phase-row columns. `GLOSS_MAX` (`59`) is what a gloss gets instead when no clock follows it |
| `THEMES`, `THEME_NAME`                           | `ghostty`       | palette, accent, the greys, prompt tint and chrome colours, per theme. Also `--theme` |
| `STEP_SPINNER`, `STEP_COLOUR`                    | braille, accent | the per-row spinner |
| `STEP_DONE_MARK`, `STEP_DONE`                    | `✓`, green      | what a finished row lands on |
| `STEP_PENDING_MARK`                              | `·`             | a phase that hasn't run yet |
| `RUNNING_MARK`                                   | `...`           | appended to a label while its row spins, dropped when it lands |
| `SEP`                                            | `·`             | tinted automatically wherever it turns up in a gloss or an `@detail` |
| `HOLD_JITTER`                                    | `0.40`          | ± on a row's hold, so a stack of rows isn't metronomic |
| `FRAME`, `CLOCK_TICK`                            | `0.11`, `0.22`  | spinner frame interval, and how often a running clock moves — two frames: often enough to read as counting, slow enough not to strobe |
| `SELECT_*`                                       | see file        | picker intro, walk, settle, flash, rest |
| `SELECT_FILL`, `SELECT_PAD`                      | `True`, `5`     | the highlight bar spans the frame, fzf-style; the pad is `"  ❯ "` in front of an option and a space behind it, so a filled bar ends exactly on `COLS` |
| `HUMAN_MARK`                                     | `❯`             | one glyph for everything the human typed — the command at a `@prompt` and the option they pick in a `@select`, both in the accent |
| `ASK_MARK`, `ASK_COLOUR`                         | `""`, accent    | marker before an `@ask`. Also `--ask-mark` |
| `PROMPT_BG`, `PROMPT_FILL`                       | tint, `False`   | background behind a `@prompt` line and under the picker highlight; the confirm flash paints `ACCENT_BG` instead |
| `TYPING_SEED`, `KEY`, `WORD_PAUSE*`, `HESITATE*` | seeded          | typing rhythm — fast within words, a beat between them, occasional hesitation. Seeded, so rebuilds are identical |
| `END_PAUSE`                                      | `3.0`           | minimum hold on the last frame before looping |

The two fill flags disagree deliberately. `SELECT_FILL` is on because a picker is a list:
in the cast this replaced, bars shrink-wrapped to their own text measured 107, 359 and
557 px and read as three different things rather than three options. `PROMPT_FILL` is off
because a prompt is a transcript: the tint marks what the human typed, and running it to
col 80 marks the row instead.

`mkpreview.py` takes `--font-size` (18), `--line-height` (1.45) and `--font-family`
(JetBrains Mono). Preview only — the GIF's size comes from `agg --font-size` in
`render.sh`. `chrome.py` takes a title plus `--scale`, `--win`, `--bar`, `--outer`; its own
constants (`BAR`, `RADIUS`, `TITLE_SIZE`, …) are 1× values that `--scale` multiplies, so
`TITLE_SIZE = 10` draws at 20 px on the 2× render. It sets the title in JetBrains Mono —
the terminal's own face — and falls back to the macOS system sans on a machine without it.

That title is derived, not written down twice. `cast.title()` returns `auto-task · 80×16`;
`cast.py` puts it in the cast header and `render.sh` hands the same string to `chrome.py`,
so the window has one name instead of two that drift apart. It carries the grid on purpose —
the frame is a fixed raster, so anyone reproducing the render needs the size, and the title
bar is the one place it can't go stale.

### On colour

Background, foreground and the ANSI tags (`{green}` `{cyan}` `{red}` `{yellow}`) are
palette-driven. Everything else is pinned per theme, because it has to hold a contrast
relationship with the ground that a palette swap must never silently break:

- the **accent** — every in-progress state, `HUMAN_MARK`, and the picker's confirm flash
  (ground-on-accent, via `ACCENT_BG`)
- the **prompt tint** — behind a `@prompt` line, and under the picker highlight
- the **greys** — `dim`, which is every gloss, and the three phase-row greys stepped below
  it: `clock` ~0.67 of the way from the ground up to `dim`, `sep` ~0.55, `pending` ~0.47.
  Each theme redraws that ladder on its own ground rather than borrowing ghostty's hexes

`dim` is an explicit grey rather than SGR 2, which darkens *towards the background* and on
a lifted charcoal collapses the detail text into mush.

ghostty's `dim` and `tint` were both lifted a step — `#9aa4b5` → `#a9afb8` and
`#2b2f37` → `#2e323c`. They are the first two things GIF quantisation eats, and nothing
else carries what they carry: the gloss holds every detail on screen, and the tint is the
only mark that input was typed. Don't darken them back.

## Provenance

Content comes from a real `/at:auto-task` run against a scratch repo (`~/github/hello-world`,
task 001 — a hello-world CLI on Bun + TypeScript), session `6718d57a`, 31 Aug 2026 — bar
the signoff, answered the next morning. Every count on screen is from that run bar one: 4 acceptance criteria, 3 lines cut by the
tightening pass, two plans with one panel disagreement resolved, two reviewers with nothing
blocking, 8 commits on `task/001-hello-world-cli`, `3/3 tests pass` (the run printed
`3 pass / 0 fail`), and a squash-merge whose build was re-verified on main afterwards.

**The clocks are derived, not quoted.** `/at:auto-task` prints no duration string at all:
the per-phase figures and the `9m 20s` total are computed from the session's own message
timestamps, one boundary per phase, with the demo's five phases folding the run's steps a
little (preflight absorbs the worktree setup, verifying absorbs the summarise). The phase
column sums to the signoff total, so editing one figure means editing two.

Three things are illustrative rather than true of that run. **`1 flag`** — the run flagged
five degradations and deviations, only one of which (a justified plan deviation) actually
wanted a human; the demo shows what the flag column is *for* rather than that run's tally.
**`deps`** — the repo was empty at preflight, so there was nothing to install. And
the phase glosses generally, which summarise a stage rather than an instance. Deliberate:
the clip illustrates the workflow, it is not a recording.

The clarify question is the run's, cut to its second half: it asked how the name is passed
*and* what happens when it's missing, offering a `--name` flag, a positional that errors when
the name is missing, and a positional defaulting to `World` — the answer. The demo keeps the
missing-name fork, the half two agents would genuinely split on, and drops the flag. The
question came from `/at:create-task`'s own ambiguity pass; the later `/at:clarify-task`
round asked about test level and the bin entry, and is not shown.

The signoff prompt is compressed the same way: the run offered four options (ship, open the
worktree in an editor, in a tmux pane, or both) and `Ship it` was chosen; the demo asks
`Ship?`.

## Gotchas

Each of these cost real time to find.

- **Never use absolute cursor addressing for content.** An earlier approach was abandoned
  entirely because its chrome repainted at fixed rows inside the scrolling area: the prompt
  didn't scroll, the spinner left ghosts, rules landed on text. The three in-place effects
  here (`@select`'s highlight, `@resolve`, the `@checklist` block) are laid down once and
  afterwards move *relative* to the cursor and back, so they scroll with the transcript.
- **Track net cursor movement, not newlines.** `@resolve` has to know how many rows above
  the cursor the pending line sits. Counting `\n` in the output stream is wrong — the
  picker repaints in place, moving up before writing — and the line reprints progressively
  further up, duplicating itself. Only operations that genuinely advance a row call
  `advance()`.
- **`@prompt` advances the cursor, so `@resolve` has to count it.** `prompt()` didn't call
  `advance()`, so a `@prompt` between a `@step!` and its `@resolve` finished the wrong row.
  Same class as the one above: consuming a row and saying so are two different things.
- **A screenplay's trailing newline must not become a blank row.** The file ends with `\n`,
  which compiled to a real blank line and cost a row the design had already spent — enough
  to scroll the prompt off a final frame that fills the frame to its last line. `render()` drops it; a blank line the
  screenplay actually asks for still prints.
- **Reset weight with `\x1b[22m`, not `\x1b[0m`** — a full reset also clears the prompt
  tint, and inside a gloss it clears the gloss grey.
- **`--font-family` disables agg's fallback chain**, so every font you need must be named.
  JetBrains Mono has neither the braille spinner nor `🎉`: drop `Menlo` from the list and
  the braille falls through to Apple Color Emoji, so the spinner renders in colour; drop
  `Apple Color Emoji` and the party popper vanishes.
- **The GIF is a fixed raster.** It renders at 2× and is displayed at half width. Font
  choice does not fix sharpness; pixels do.
- **Don't give the framed GIF transparent corners.** GIF transparency forces a per-frame
  palette and full frames — around 20× the bytes, for a detail nobody sees on a dark page.
  `chrome.py` backs the corners with `OUTER` instead.
- **Build the GIF palette from a spread of composed frames.** Sampling frame 1 (nearly
  blank), or the bare terminal without its chrome, starves it of the shades text
  antialiasing needs and the glyphs come out chunky.
- **Don't compare finished GIFs to prove chrome pixels are unchanged.** The 256-colour
  palette is quantised from the composed frames, so touching anything at all shifts the
  palette and perturbs every pixel by up to 1/255. Compare the composed frames *before*
  quantisation.
- **`chrome.py` must scale with the render.** Its constants are 1× values; `render.sh`
  passes `--scale` derived from the font size.
- **`mkpreview.py`'s HTML is a `%`-format template** — a literal `%` in its CSS must be `%%`.
- **asciinema-player hardcodes its font in CSS**, so `terminalFontFamily` alone is ignored.
  `mkpreview.py` overrides `.ap-terminal` at higher specificity.
- **asciicast v3 stores relative intervals**, v2 absolute. `cast.py` emits v2; `mkpreview.py`
  handles both.
- **Verify frames; don't read escape codes.** For anything structural — a column, a colour,
  whether an effect actually applied — the only proof is the screen the terminal ends up
  with, and that discipline lives in `test_cast.py`: it compiles fixture screenplays,
  replays them into a `pyte.Screen` and asserts on cell contents and per-cell colour. For
  anything visual — weight, contrast, spacing, chrome — screenshot the preview with
  `shot-scraper <file>.html -o /tmp/x.png --width 1100 --wait <ms>` and look at the PNG
  (~60-90s; pass a bare path, not a `file://` URL). Neither judges **motion**: flicker,
  pacing and reveal rhythm need a human.
