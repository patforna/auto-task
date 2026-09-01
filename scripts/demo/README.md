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
```

```
demo.txt ──cast.py──> demo.cast ──agg──> demo-raw.gif ──chrome.py──> demo.gif
                          └────────mkpreview.py────────────────────> demo.html
```

| file           | what it is                                       | committed |
| -------------- | ------------------------------------------------ | --------- |
| `demo.cast`    | asciicast v2 — the source of truth for timing    | yes       |
| `demo.gif`     | the deliverable, framed, ~320 KB                 | yes       |
| `demo-raw.gif` | agg's bare output, before chrome                 | no        |
| `demo.html`    | scrubbing preview, player inlined, works offline | no        |
| `demo-<theme>.*` | output of `variants.sh`                        | no        |
| `assets/`      | asciinema player, fetched on first preview       | no        |

Needs `python3`, [`agg`](https://github.com/asciinema/agg) (`brew install agg`) and `uv`
(for Pillow, which draws the chrome). If Pillow is unreachable, `render.sh` warns and falls
back to the unframed GIF. `curl` is used once, to fetch the player.

**Watch `demo.html` while iterating** — it has a scrubber. But judge the *GIF*: it renders
at 2× and is meant to display at half width, which supersamples the text and comes out
sharper than the player at 100%.

## The screenplay language

Plain lines print verbatim, blank lines and indentation included. Directives and `#`
comments start at column 0 — an indented `#` is content, so markdown headings survive.

The numbers are not all durations:

| directive              | what it does                                                          |
| ---------------------- | --------------------------------------------------------------------- |
| `@prompt <text>`       | a human types it, then enter. **No number.** A leading `/command` is bolded, its arguments are not |
| `@step <secs> a\|b\|c` | a line with a braille spinner, revealed chunk by chunk. `<secs>` is **per chunk**, not total, ±`CHUNK_JITTER`. Resolves to a green tick |
| `@step! <secs> a\|b`   | the same, but left **spinning** until an `@resolve`. For a step genuinely blocked on the human |
| `@resolve <secs>`      | finish the pending `@step!` in place, however many lines have been printed since. One pending step at a time |
| `@ask <text>`          | a question handed back to you, prefixed with `ASK_MARK` (currently none) |
| `@select <n> a\|b`     | a TUI picker. `<n>` is the **1-based option chosen**, not a duration. The highlight lands on the first option, walks to `<n>`, then flashes to confirm |
| `@pause <secs>`        | wait, showing nothing new                                              |
| `@clear`               | wipe the screen and start again at the top                             |

Inline styling: `{bold}` `{dim}` `{orange}` `{green}` `{cyan}` `{yellow}` `{red}`, each
closed by `{/}`. No implicit styling — use `{green}✓{/}` explicitly.

Two invariants so layout can't drift as you edit: consecutive blank lines collapse to one,
and the final frame is held for at least `END_PAUSE` before the loop restarts.

## Tuning

Constants at the top of `cast.py`:

| constant                                    | default        | effect                                        |
| ------------------------------------------- | -------------- | ---------------------------------------------- |
| `COLS`, `ROWS`                              | `80`, `15`     | frame size. Lines wider than `COLS` warn on render |
| `THEMES`, `THEME_NAME`                       | `ghostty`      | palette, accent, dim, prompt tint and chrome colours, per theme. Also `--theme` |
| `STEP_SPINNER`, `STEP_COLOUR`               | braille, accent | the per-step inline spinner                    |
| `STEP_DONE_MARK`, `STEP_DONE`               | `✓`, green     | what a finished `@step` resolves to            |
| `CHUNK_JITTER`                              | `0.40`         | ± on each chunk's hold, so the reveal isn't metronomic |
| `SELECT_*`                                  | see file       | picker intro, walk, settle, flash, rest         |
| `SELECT_FILL`                               | `False`        | `True` spans the bar across the frame, fzf-style |
| `ASK_MARK`, `ASK_COLOUR`                    | `""`           | marker before an `@ask`. Also `--ask-mark`      |
| `PROMPT_BG`, `PROMPT_FILL`                  | tint, `False`  | background behind `@prompt` lines and the picker highlight |
| `TYPING_SEED`, `KEY`, `WORD_PAUSE*`, `HESITATE*` | seeded    | typing rhythm — fast within words, a beat between them, occasional hesitation. Seeded, so rebuilds are identical |
| `END_PAUSE`                                 | `3.0`          | minimum hold on the last frame before looping   |

`mkpreview.py` takes `--font-size` (18), `--line-height` (1.45) and `--font-family`
(JetBrains Mono). Preview only — the GIF's size comes from `agg --font-size` in
`render.sh`. `chrome.py` takes `--scale`, `--win`, `--bar`, `--outer`.

### On colour

Only background, foreground, green and cyan are palette-driven. The **accent** (every
in-progress state, the `>` and `❯` markers) and the **prompt tint** are pinned per theme,
because both must hold a contrast relationship with the ground — a palette swap must never
silently recolour them.

## Provenance

Content comes from a real `/at:auto-task` run against a scratch repo (`~/github/hello-world`,
task 001 — a hello-world CLI on Bun + TypeScript). The task file, the clarify question and
its options, the commit count and the ship result are from that run.

The step wording is written for a viewer rather than quoted. Two things are true of the
workflow rather than of that run: `install deps` (the repo was empty at preflight, so there
was nothing to install) and the step descriptions generally, which summarise a stage rather
than an instance. Deliberate: the clip illustrates the workflow, it is not a recording.

## Gotchas

Each of these cost real time to find.

- **Never use absolute cursor addressing for content.** An earlier approach was abandoned
  entirely because its chrome repainted at fixed rows inside the scrolling area: the prompt
  didn't scroll, the spinner left ghosts, rules landed on text. The two in-place effects
  here (`@select`'s highlight, `@resolve`) move *relative* to the cursor and return to it.
- **Track net cursor movement, not newlines.** `@resolve` has to know how many rows above
  the cursor the pending line sits. Counting `\n` in the output stream is wrong — the
  picker repaints in place, moving up before writing — and the line reprints progressively
  further up, duplicating itself. Only operations that genuinely advance a row call
  `advance()`.
- **Reset weight with `\x1b[22m`, not `\x1b[0m`** — a full reset also clears the prompt tint.
- **`--font-family` disables agg's fallback chain**, so every font you need must be named.
  JetBrains Mono has none of the braille or dingbat glyphs; without `Menlo` in the list they
  resolve to Apple Color Emoji and the spinner renders in colour.
- **The GIF is a fixed raster.** It renders at 2× and is displayed at half width. Font
  choice does not fix sharpness; pixels do.
- **Don't give the framed GIF transparent corners.** GIF transparency forces a per-frame
  palette and full frames — 6.4 MB versus 264 KB. `chrome.py` backs the corners with `OUTER`.
- **Build the GIF palette from a spread of composed frames.** Sampling frame 1 (nearly
  blank) starves it of the shades text antialiasing needs and the glyphs come out chunky.
- **`chrome.py` must scale with the render.** Its constants are 1× values; `render.sh`
  passes `--scale` derived from the font size.
- **`mkpreview.py`'s HTML is a `%`-format template** — a literal `%` in its CSS must be `%%`.
- **asciinema-player hardcodes its font in CSS**, so `terminalFontFamily` alone is ignored.
  `mkpreview.py` overrides `.ap-terminal` at higher specificity.
- **asciicast v3 stores relative intervals**, v2 absolute. `cast.py` emits v2; `mkpreview.py`
  handles both.
- **Verify frames with a terminal emulator, not by reading escape codes.**
  `uv run --with pyte python …` feeding the cast into a `pyte.Screen` shows exactly what
  lands on screen, including per-cell colours and reverse video.
