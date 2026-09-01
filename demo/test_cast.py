#!/usr/bin/env python3
"""Check the compiled cast frame by frame: cell contents and per-cell colour.

    python3 test_cast.py        # borrows pyte through uv if it isn't installed

Escape codes lie. The only thing that proves a label starts at col 3, that a gloss
kept its grey, or that a highlight bar really spans the frame is the screen the
terminal ends up with — so every check here replays a fixture screenplay into a
pyte screen and asserts against cells.

Add a check by writing a fixture and a function decorated with @check. Then break
the thing it checks and watch it fail: an assertion never seen to fail is not
known to work.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import pyte
except ModuleNotFoundError:      # pyte is no more a system package than Pillow is
    if os.environ.get("BORROWED_PYTE"):          # uv ran us and pyte still isn't there
        sys.exit("uv could not supply pyte")
    os.environ["BORROWED_PYTE"] = "1"
    try:    # "python", not sys.executable: it has to be uv's interpreter, not ours
        os.execvp("uv", ["uv", "run", "--quiet", "--with", "pyte", "python",
                         os.path.abspath(__file__), *sys.argv[1:]])
    except FileNotFoundError:
        sys.exit("needs pyte: pip install pyte, or install uv and let it fetch one")

import cast
from cast import COLS, ROWS

cast.apply_theme("ghostty")

# The palette the design spec pins, as pyte reports it: lowercase hex, no "#".
FG, GLOSS, PENDING, CLOCK, SEP = "default", "a9afb8", "5f656e", "7b818a", "6b7178"
TINT, ACCENT = "2e323c", "ff875f"

PHASES = "Preflight|Planning|Implementing|Reviewing|Verifying"

# The two screens of the demo, cut down to what a check needs. Column numbers in
# the checks are 1-indexed like the grammar; pyte's are 0-indexed.
CREATE = """\
@prompt /at:create-task build a hello-world cli
@step! 0.4 Clarifying|read the repo · find the ambiguities
@ask How is the name passed?
@select 2 Positional; error if missing|Positional; default "World"
@resolve 0.2
@step 0.4 Creating task|write ACs · commit

@row {green}✓{/} Task 001 ready for dev
@detail tasks/001-hello-world-cli.md · {bold}4{/} ACs
"""

AUTO = """\
@prompt /at:auto-task 001
@checklist """ + PHASES + """
@run 1.2 Preflight|task · tooling · worktree · deps|0:14
@run 1.2 Planning|panel of models · synthesise|1:07
@run 1.2 Implementing|tests first · {bold}6{/} commits|2:31
@run 1.2 Reviewing|{bold}3{/} issues found · fixing 2 of 3|{bold}3{/} issues found · {bold}3{/} fixed|3:52
@run 1.2 Verifying|run CLI · validate ACs|4:12

@row 🎉 Shipped|squash-merged · build green · worktree removed
"""


# ---------------------------------------------------------------- the harness

def screens(script):
    """Replay a screenplay, yielding (cast, screen) after every event it emits."""
    c = cast.render(script)
    screen = pyte.Screen(COLS, ROWS)
    stream = pyte.Stream(screen)
    for _, _, data in c.events:
        stream.feed(data)
        yield c, screen


def final(script):
    for c, s in screens(script):
        pass
    return c, s


def until(script, pred):
    """The first screen the predicate accepts — for a state that doesn't last."""
    for c, s in screens(script):
        if pred(s):
            return c, s
    raise AssertionError("no frame matched")


def cell(s, y, col):
    """The cell at 1-indexed column `col` of row `y`."""
    return s.buffer[y][col - 1]


def text(s, y, col=1, n=None):
    """`n` cells from 1-indexed column `col`. Cell-exact, so wide glyphs don't shift it."""
    n = COLS - col + 1 if n is None else n
    return "".join(s.buffer[y][col - 1 + i].data for i in range(n))


def row_of(s, label):
    for y in range(ROWS):
        if text(s, y).lstrip().startswith(label):
            return y
    raise AssertionError(f"no row starting {label!r} in:\n" + dump(s))


def dump(s):
    return "\n".join(f"{y:2d}|{line.rstrip()}" for y, line in enumerate(s.display))


def raises(script, fragment):
    try:
        cast.render(script)
    except SystemExit as e:
        assert fragment in str(e), f"wrong error: {e}"
        return
    raise AssertionError(f"expected SystemExit containing {fragment!r}")


CHECKS = []


def check(fn):
    CHECKS.append(fn)
    return fn


# ---------------------------------------------------------------- row grammar

@check
def done_row_holds_the_grid():
    """a done row: glyph col 1, label col 3, gloss col 20, clock col 56"""
    _, s = final(AUTO)
    y = row_of(s, "✓ Preflight")
    assert cell(s, y, 1).data == "✓", text(s, y)
    assert cell(s, y, 2).data == " ", "the tick needs a trailing space to fill 2 cells"
    assert text(s, y, 3, 17).rstrip() == "Preflight", repr(text(s, y))
    assert text(s, y, 20, 32) == "task · tooling · worktree · deps", text(s, y)
    assert text(s, y, 56, 4) == "0:14", repr(text(s, y))


@check
def a_wide_glyph_still_leaves_the_label_at_col_3():
    """🎉 fills cols 1-2, so Shipped starts at col 3 like every other label"""
    _, s = final(AUTO)
    y = row_of(s, "🎉")
    assert cell(s, y, 1).data == "🎉", repr(text(s, y))
    assert cell(s, y, 2).data == "", "a 2-cell glyph must not take a trailing space"
    assert text(s, y, 3, 17).rstrip() == "Shipped", repr(text(s, y))
    assert text(s, y, 20, 13) == "squash-merged", repr(text(s, y))


@check
def ellipsis_means_still_running():
    """a running row carries "...", a done row does not"""
    _, s = until(AUTO, lambda s: s.buffer[3][0].data in cast.STEP_SPINNER)
    assert text(s, 3, 3, 17).rstrip() == "Implementing...", repr(text(s, 3))
    assert text(s, 2, 3, 17).rstrip() == "Planning", "a done row kept the dots: " + repr(text(s, 2))
    assert text(s, 4, 3, 17).rstrip() == "Reviewing", "a pending row has dots: " + repr(text(s, 4))


@check
def a_running_row_starts_its_gloss_at_col_20_too():
    """the "..." eats into the label column, not the gloss column"""
    _, s = until(AUTO, lambda s: s.buffer[3][0].data in cast.STEP_SPINNER)
    assert text(s, 3, 20, 11) == "tests first", repr(text(s, 3))


@check
def a_pending_row_shows_a_dot_and_nothing_else():
    """a pending row: · glyph, pending grey, no gloss, no clock"""
    _, s = until(AUTO, lambda s: s.buffer[1][0].data in cast.STEP_SPINNER)
    y = row_of(s, "· Verifying")
    assert cell(s, y, 1).data == cast.STEP_PENDING_MARK
    assert text(s, y, 3, 17).rstrip() == "Verifying", repr(text(s, y))
    assert text(s, y, 20).strip() == "", "a pending row has nothing to report: " + repr(text(s, y))
    assert cell(s, y, 3).fg == PENDING, cell(s, y, 3).fg
    assert not cell(s, y, 3).bold, "a pending label is not bold"


@check
def a_gloss_with_no_clock_may_run_past_col_56():
    """the Shipped gloss is 46 cells wide and keeps going"""
    _, s = final(AUTO)
    y = row_of(s, "🎉")
    assert text(s, y, 20, 46) == "squash-merged · build green · worktree removed", repr(text(s, y))
    assert cast.GLOSS_MAX == 59, "cols 20-78"


# ------------------------------------------------------------------- colour

@check
def the_row_colours_are_the_ones_the_spec_pins():
    """label bold in the default fg, gloss #a9afb8, clock #7b818a and never bold"""
    _, s = final(AUTO)
    y = row_of(s, "✓ Preflight")
    label, gloss, clock = cell(s, y, 3), cell(s, y, 20), cell(s, y, 56)
    assert label.bold and label.fg == FG, (label.bold, label.fg)
    assert not gloss.bold and gloss.fg == GLOSS, (gloss.bold, gloss.fg)
    assert not clock.bold and clock.fg == CLOCK, (clock.bold, clock.fg)


@check
def separators_are_dimmer_than_the_gloss_around_them():
    """a bare · inside a gloss is tinted #6b7178 without the screenplay asking"""
    _, s = final(AUTO)
    y = row_of(s, "✓ Preflight")
    col = 20 + text(s, y, 20, 36).index("·")
    assert cell(s, y, col).data == "·"
    assert cell(s, y, col).fg == SEP, cell(s, y, col).fg
    assert int(SEP, 16) < int(GLOSS, 16), "the separator has to be the dimmer of the two"
    assert cell(s, y, col + 1).fg == GLOSS, "the gloss picks its grey back up after the ·"


@check
def counts_carry_the_emphasis_and_their_labels_do_not():
    """{bold}6{/} commits: 6 lifts out of the grey, commits drops back into it"""
    _, s = final(AUTO)
    y = row_of(s, "✓ Implementing")
    col = 20 + text(s, y, 20, 36).index("6")
    six, word = cell(s, y, col), cell(s, y, col + 2)
    assert six.data == "6" and six.bold and six.fg == FG, (six.data, six.bold, six.fg)
    assert word.data == "c" and not word.bold and word.fg == GLOSS, (word.data, word.bold, word.fg)


@check
def a_gloss_without_counts_has_no_emphasis_at_all():
    """write ACs · commit is gloss grey end to end"""
    _, s = final(CREATE)
    y = row_of(s, "✓ Creating task")
    assert text(s, y, 20, 18) == "write ACs · commit", repr(text(s, y))
    assert not any(cell(s, y, c).bold for c in range(20, 38)), "nothing here is a count"


@check
def a_count_on_a_detail_line_returns_to_the_grey_it_came_from():
    """@detail … {bold}4{/} ACs — the 4 is emphasised, ACs is not, both stay in the line"""
    _, s = final(CREATE)
    y = row_of(s, "tasks/001")
    col = text(s, y).index("4") + 1
    four, word = cell(s, y, col), cell(s, y, col + 2)
    assert four.data == "4" and four.bold and four.fg == FG, (four.data, four.bold, four.fg)
    assert word.data == "A" and not word.bold and word.fg == GLOSS, (word.data, word.bold, word.fg)


@check
def a_heading_row_lets_its_label_run_past_the_column():
    """the label column only exists to line a gloss up, so a heading ignores it"""
    long = "Task 001 ready for signoff"          # 26 cells, well past LABEL_W
    c = cast.render("@row {green}\u2713{/} " + long + "\n")
    assert c.warn == [], f"nothing follows the label, so nothing is misaligned: {c.warn}"
    _, s = final("@row {green}\u2713{/} " + long + "\n")
    assert text(s, 0, 3, len(long)) == long, repr(text(s, 0))
    # ...but the moment a gloss follows, the column is load-bearing again
    c = cast.render("@row {green}\u2713{/} " + long + "|x\n")
    assert any("label >" in w for w in c.warn), c.warn


@check
def a_detail_line_gets_the_gloss_treatment_without_asking():
    """@detail indents to col 3, greys the words and tints the separators itself"""
    _, s = final(CREATE)
    y = row_of(s, "tasks/001")
    assert text(s, y, 1, 2) == "  ", repr(text(s, y, 1, 6))
    assert cell(s, y, 3).fg == GLOSS, cell(s, y, 3).fg
    col = text(s, y).index("\u00b7") + 1
    assert cell(s, y, col).fg == SEP, f"the separator tints itself: {cell(s, y, col).fg}"


@check
def a_tag_that_is_not_a_tag_is_caught_before_it_reaches_the_gif():
    """an unknown {tag} prints as literal text, which is invisible until rendered"""
    assert any("unknown tag {nope}" in w for w in cast.render("{nope}x{/}\n").warn)
    assert cast.render("{bold}x{/}\n").warn == [], "a real tag is not a typo"
    assert cast.render(CREATE).warn == [] and cast.render(AUTO).warn == []


@check
def every_theme_keeps_the_grey_ladder():
    """dim > clock > sep > pending, on each theme's own ground"""
    for name, t in cast.THEMES.items():
        ladder = [int(t[k].lstrip("#"), 16) for k in ("dim", "clock", "sep", "pending")]
        assert ladder == sorted(ladder, reverse=True), (name, ladder)
        assert len(set(ladder)) == 4, f"{name} reuses a grey"
    assert len({t["pending"] for t in cast.THEMES.values()}) == 3, "themes share a pending grey"


# ------------------------------------------------------- prompt and the picker

@check
def one_glyph_marks_everything_the_human_typed():
    """❯ at col 1 of a @prompt, and at col 3 of the option they chose"""
    _, s = final(CREATE)
    y = row_of(s, "❯ /at:create-task")
    assert cell(s, y, 1).data == "❯" and cell(s, y, 1).fg == ACCENT
    chosen = row_of(s, "❯ Positional; default")
    assert cell(s, chosen, 3).data == "❯" and cell(s, chosen, 3).fg == ACCENT


@check
def the_prompt_tint_stops_at_the_typed_text():
    """PROMPT_FILL stays False: the tint shrink-wraps what was typed"""
    _, s = final(CREATE)
    y = row_of(s, "❯ /at:create-task")
    assert cell(s, y, 1).bg == TINT, cell(s, y, 1).bg
    assert cell(s, y, COLS).bg == "default", "the prompt tint must not run to the edge"


@check
def the_selection_bar_spans_the_frame():
    """SELECT_FILL: the chosen option's highlight runs col 1 to col 80"""
    _, s = final(CREATE)
    y = row_of(s, "❯ Positional; default")
    bg = [cell(s, y, c).bg for c in range(1, COLS + 1)]
    assert set(bg) == {TINT}, f"bar covers {bg.count(TINT)}/{COLS} cells"
    assert cast.SELECT_FILL is True


@check
def the_picker_sits_on_its_own_columns():
    """question at col 3, options at col 5, chosen option's ❯ at col 3"""
    _, s = final(CREATE)
    q = row_of(s, "How is the name passed?")
    assert text(s, q, 3, 23) == "How is the name passed?", repr(text(s, q))
    assert cell(s, q, 1).data == " " and cell(s, q, 2).data == " "
    other = row_of(s, "Positional; error")
    assert text(s, other, 5, 25) == "Positional; error if missing"[:25], repr(text(s, other))
    chosen = row_of(s, "❯ Positional; default")
    assert text(s, chosen, 5, 10) == "Positional", repr(text(s, chosen))


# ---------------------------------------------------------------- checklist

@check
def the_checklist_prints_every_phase_up_front():
    """all five rows land at once, all pending, before anything runs"""
    _, s = until(AUTO, lambda s: s.buffer[1][0].data == cast.STEP_PENDING_MARK)
    for y, label in enumerate(PHASES.split("|"), start=1):
        assert cell(s, y, 1).data == cast.STEP_PENDING_MARK, dump(s)
        assert text(s, y, 3, len(label)) == label, dump(s)
        assert cell(s, y, 3).fg == PENDING, dump(s)


@check
def running_a_row_leaves_the_rest_of_the_block_alone():
    """rows above stay done, rows below stay pending, all in place"""
    _, s = until(AUTO, lambda s: s.buffer[3][0].data in cast.STEP_SPINNER)
    assert [cell(s, y, 1).data for y in (1, 2, 4, 5)] == ["✓", "✓", "·", "·"], dump(s)
    assert text(s, 1, 56, 4) == "0:14" and text(s, 2, 56, 4) == "1:07", dump(s)
    assert text(s, 5, 20).strip() == "", "a pending row must not have run: " + dump(s)


@check
def the_gloss_can_change_when_the_row_lands():
    """4 fields: fixing 2 of 3 while it runs, 3 fixed once it has"""
    _, s = until(AUTO, lambda s: s.buffer[4][0].data in cast.STEP_SPINNER)
    assert text(s, 4, 20, 30) == "3 issues found · fixing 2 of 3", repr(text(s, 4))
    _, s = final(AUTO)
    assert text(s, 4, 20, 22) == "3 issues found · 3 fix", repr(text(s, 4))


@check
def the_clock_counts_up_and_lands_exactly():
    """Reviewing is its own stopwatch: it starts at 0:00 and lands on 3:52"""
    seen = []
    for c, s in screens(AUTO):
        if s.buffer[4][0].data in cast.STEP_SPINNER + "✓" and text(s, 4, 3, 9) == "Reviewing":
            v = text(s, 4, 56, 4).strip()
            if v and (not seen or seen[-1] != v):
                seen.append(v)
    secs = [cast.clock_secs(v) for v in seen]
    assert seen[0] == "0:00", f"each row times itself from zero, not from {seen[0]}"
    assert seen[-1] == "3:52", f"lands exactly, not on {seen[-1]}"
    assert secs == sorted(secs), seen
    assert len(seen) >= 4, f"barely ticks: {seen}"
    assert "3:52" not in seen[:-1], f"reached its target before it landed: {seen}"


@check
def the_block_closes_when_something_else_prints():
    """the cursor drops below the block; the block keeps its state"""
    _, s = final(AUTO)
    assert [cell(s, y, 1).data for y in range(1, 6)] == ["✓"] * 5, dump(s)
    assert text(s, 6).strip() == "", "a blank row should follow the block: " + dump(s)
    assert text(s, 7, 3, 7) == "Shipped", dump(s)


@check
def pause_does_not_close_the_block():
    """a @run after a @pause still finds its checklist"""
    _, s = final("@checklist A|B\n@run 0.2 A|first|0:05\n@pause 0.3\n@run 0.2 B|second|0:09\n")
    assert [cell(s, y, 1).data for y in (0, 1)] == ["✓", "✓"], dump(s)
    assert text(s, 1, 20, 6) == "second", dump(s)


@check
def clear_resets_the_checklist():
    """@clear wipes the block state, so nothing tries to repaint above the cursor"""
    _, s = final("@checklist A|B\n@run 0.2 A|first|0:05\n@clear\nplain line\n")
    assert text(s, 0, 1, 10) == "plain line", dump(s)


@check
def a_pending_step_survives_whatever_is_printed_under_it():
    """@step! keeps spinning through an @ask and a @select, then @resolve ticks it"""
    _, s = until(CREATE, lambda s: s.buffer[3][2].data == "❯")   # the picker is on screen
    assert s.buffer[1][0].data in cast.STEP_SPINNER, dump(s)
    assert text(s, 1, 3, 13) == "Clarifying...", dump(s)
    _, s = final(CREATE)
    assert cell(s, 1, 1).data == "✓", dump(s)
    assert text(s, 1, 3, 17).rstrip() == "Clarifying", dump(s)
    assert text(s, 1, 20, 15) == "read the repo ·", dump(s)


@check
def a_screenplays_closing_newline_is_not_a_blank_row():
    """every row in the frame is spoken for — the file's own newline can't take one"""
    _, s = final("one\ntwo\n")
    assert (text(s, 0, 1, 3), text(s, 1, 1, 3)) == ("one", "two"), dump(s)
    assert s.cursor.y == 2, f"row {s.cursor.y}: a blank row was printed under it"
    _, s = final("one\ntwo\n\n")
    assert s.cursor.y == 3, "a blank row the screenplay asked for still prints"


@check
def a_prompt_under_a_pending_step_counts_as_a_row():
    """@prompt advances the cursor, so @resolve has to count it too"""
    _, s = final("@step! 0.3 Working|on it\n@prompt yes\n@resolve 0.2\n")
    assert cell(s, 0, 1).data == "✓", dump(s)
    assert text(s, 0, 3, 17).rstrip() == "Working", dump(s)
    assert cell(s, 1, 1).data == "❯", "the prompt is a row of its own: " + dump(s)


# ------------------------------------------------------- compile-time refusals

@check
def a_screenplay_typo_fails_the_compile():
    """the errors that would otherwise look like a rendering bug in the GIF"""
    raises("@checklist A|B\n@run 0.2 C|x|0:05\n", "not in the checklist")
    raises("@checklist A|B\n@run 0.2 B|x|0:05\n", "out of order")
    raises("@run 0.2 A|x|0:05\n", "no @checklist is open")
    raises("@step! 0.2 A|x\n@checklist A|B\n", "still pending")
    raises("@step 0.2 A|one|two|three\n", "expected 1-2 fields")
    raises("@checklist A\n@run 0.2 A|x|nine\n", "clock must be M:SS")


@check
def a_field_that_outgrows_its_column_warns():
    """a ragged column is invisible until the GIF renders, so say it at compile time"""
    c = cast.render("@step 0.2 A much too long label|x\n")
    assert any("label >17" in w for w in c.warn), c.warn
    c = cast.render("@checklist A\n@run 0.2 A|" + "x" * 40 + "|0:05\n")
    assert any("gloss >35" in w for w in c.warn), c.warn
    # A gloss beside a clock has one column fewer than it owns: filling all 36
    # leaves no gap and "commit2:10" reads as one word. The boundary is the bug.
    c = cast.render("@checklist A\n@run 0.2 A|" + "x" * cast.GLOSS_W + "|0:05\n")
    assert c.warn, "a gloss that fills the column butts against the clock"
    c = cast.render("@checklist A\n@run 0.2 A|" + "x" * (cast.GLOSS_W - 1) + "|0:05\n")
    assert c.warn == [], f"one short of the column is the widest that fits: {c.warn}"
    c = cast.render("@row X A|" + "x" * 60 + "\n")
    assert any("gloss >59" in w for w in c.warn), c.warn
    assert cast.render(AUTO).warn == [], "the real screenplay should be clean"


# --------------------------------------------------------------------- runner

def main():
    failed = 0
    for fn in CHECKS:
        name = (fn.__doc__ or fn.__name__).strip()
        try:
            fn()
            print(f"PASS  {name}")
        except (Exception, SystemExit) as e:
            failed += 1
            first = str(e).split("\n")[0][:200]
            print(f"FAIL  {name}\n      {type(e).__name__}: {first}")
    print(f"\n{len(CHECKS) - failed}/{len(CHECKS)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
