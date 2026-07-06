# Sample Run

The verbatim final report of a real `/at:auto-task` run (full mode, no config — pure defaults) on a small TypeScript library the workflow had never seen. The task: add a stats CLI (`count`/`median`/`p90`) with behavioural acceptance criteria.

Worth noticing:

- The Codex adversarial pass caught a real numeric bug the Claude reviewer had passed — and the review of the *fix* then caught a second bug the fix introduced.
- One finding was **rejected** with cited evidence (an artefact of the reviewer's own sandbox), instead of being obediently "fixed".
- The workflow stopped at the ship gate; `/at:ship-task` was invoked separately and squash-merged the branch after re-verifying the integrated tree.

---

> Task 001 is done and `ready-for-signoff` on branch `task/001-stats-command` (worktree: `../wordwise.worktrees/001-stats-command`, 8 commits, nothing uncommitted).
>
> ## What Was Achieved
>
> - **Planned** via a Codex + Claude panel (raw responses saved to `/tmp`); the plans agreed on the shape, the synthesis was written to the task file.
> - **Implemented**: `src/stats.ts` (pure `parseNumbers` + `computeStats`), thin `src/cli.ts`, `stats` script in `package.json`, 20 tests — mirroring the existing pattern (pure logic throws, CLI maps to stderr + exit 1).
> - **Reviewed**: `/at:review-code` (clean) + Codex adversarial review, synthesised, fixed, re-reviewed until Codex approved.
> - **Task review**: independent agent exercised every AC live against the CLI — all pass; `bun run check` green (tsc clean, 20/20 tests).
>
> ## Triage Decisions (the Bit Worth Your Eyes)
>
> - **2 findings fixed**, both accepted with reproduced evidence, no Critical/Major left to a human call:
>   1. *Minor* — even-count median `(a+b)/2` overflowed to `Infinity` for inputs near `Number.MAX_VALUE` (Codex found it; the Claude reviewer had missed it). First fix `a/2 + b/2`…
>   2. …which the fix-review caught as introducing subnormal underflow (`[5e-324, 5e-324]` → median `0`). Final form is a hybrid: `(a+b)/2` with the half-sum only as overflow fallback — proven correct at both extremes, regression tests for both.
> - **1 finding rejected**: Codex's "CLI tests aren't hermetic" (`mkdtempSync` at module load failed with EPERM *in Codex's own sandbox*). Rejected as environment-specific — the suite passes in the real environment, and no restructuring would make subprocess-spawning tests runnable in a tmp-unwritable sandbox. Codex's "no-ship" verdicts were both severity-inflated; the substance survived triage, the framing didn't.
> - **Deferred (follow-up note, not fixed)**: Codex's optional suggestion to also pin the overflow fallback for large *negative* even-count medians with a test.
>
> ## How Do You Want to Proceed?
>
> 1. Open the worktree in your editor (e.g. VS Code)
> 2. Open the worktree in a new tmux pane
> 3. Both
> 4. Run `/at:ship-task`
>
> I'll wait for your call.

---

And the subsequent `/at:ship-task` output:

> Task 001 shipped: status set to done, branch squash-merged into `main` as `ce9d72b`, verified green on the merged tree (`tsc` clean, 20/20 tests pass), and the task worktree and branch removed — no remote configured, so there was nothing to push.
