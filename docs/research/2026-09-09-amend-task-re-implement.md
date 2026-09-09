# Amending a Task After Implementation, and Re-Implementing

Research date: 2026-09-09. Method: two-perspective panel (`/at:panel`) merged with `/at:synthesize`. Codex was unavailable, so the line-up was two independent Claude panelists rather than the usual cross-family pair — a single-family panel, which is this doc's main methodological limitation (see § Panel Limitations). Every quote below was verified against the skill text in this repo, not against the released plugin cache.

## Problem Anchor (Verbatim)

> Work out how auto-task should support changing a task's intent after implementation has finished — amend the task, extend its plan, re-run implementation.
>
> Trigger: the human reviews the finished code and concludes the implementation itself needs to change, not just be fixed.

This is a design-level answer. It recommends; it does not implement. No skill, README, or config file is touched by this task — the follow-up work is a separate task.

## Bottom Line

1. **Not supported today.** Nothing in the repo names the scenario. Three affordances come close — impl-task Step 6 "Integrate Feedback", auto-task Step 9's open-the-worktree hand-off, and the `[further user instructions]` argument most pipeline skills accept — and none of them writes the task file, which goes on asserting an intent the code no longer implements. Only Step 6 acts on the change itself; the Step 9 hand-off passes the worktree to the human, and `[further user instructions]` only *speaks* the amendment into a step.
2. **The pipeline actively resists it, by design.** The review loop treats the task as an immutable reference frame, enforced at four independent sites. That is what makes auto-task's autonomy safe, and it must stay. Amendment therefore has to sit *outside* the autonomous loop and produce a new fixed anchor before the loop restarts.
3. **Recommended: `/at:amend-task`, a new human-only skill, plus about a dozen sentence-level edits to existing skills.** The skill owns intake and the AC/amendment delta; everything downstream — planning, implementing, re-verifying, shipping — is existing machinery that needs scoping clauses, not replacements.
4. **One new status value, `amended`**, with a single backwards edge `ready-for-signoff → amended → in-dev`. It costs zero config files: `settings.task_store.status` owns *how* status is written, not which values exist, so CLAUDE.md's four-file rule is not triggered. `amended` declares the intent; the guards key on the plan's shape, which is what survives impl-task's unconditional `in-dev` write. **One amendment at a time** — amend-task refuses while the plan still carries an unimplemented one.
5. **Retracted ACs leave the AC list and land in an append-only `## Amendments` log**, each retraction paying for itself with a positive cleanup AC. Plan steps and Implementation Notes are append-and-supersede, never rewritten. Every amendment write rides the task branch, so ensuring the workspace is `/at:amend-task`'s first act, not auto-task's.
6. **Already-shipped tasks are out of scope**; the substitute is a new task that references the superseded one.

**Honesty check, volunteered independently by both panelists:** the new skill is the *small* half of this recommendation. A `/at:amend-task` that could not relax auto-task Step 1's branch guard and could not teach impl-task Step 3 about deltas would produce an amended task nothing can run. If the constraint were genuinely "one lever, no edits elsewhere", the correct answer is alternative 1 below — close it and file a new task — not a new skill.

---

## 1. Where the Current Workflow Blocks

### Closest existing affordances

- **impl-task Step 6** — the only step that takes open-ended human feedback about the finished implementation *and acts on it*: "Wait for the user to provide feedback. Once provided, address it, commit, respond." (review-task Step 4 also waits unbounded on the finished implementation — "present a summary of your findings and wait for user input" — but its Guidance forbids fixing anything; auto-task Step 9, create-task Step 4 and clarify-task Step 3 wait on bounded questions.) Free-text and unbounded, but it writes no task file, moves no status, and triggers no re-review.
- **auto-task Step 9's hand-off** — "Open the worktree in their editor (e.g. VS Code)". This is the live path today: the human takes the worktree by hand.
- **`[further user instructions]`** — on the Usage line of create-task, clarify-task, plan-task, impl-task, review-task and auto-task (ship-task takes no free-text argument at all; review-code's is the differently-worded `[further instructions]`, review-design's `[the change + its design intent]`), so an amendment can be *spoken* into most steps. It is never persisted.

### Hard blocks

| Site | Deciding sentence | Why it blocks |
| --- | --- | --- |
| auto-task Step 1 | "If the branch or worktree path already exists but is provably a dead leftover … delete both … **Otherwise refuse to start: real work could be lost.**" | After implementation the branch is many commits ahead, so it is not provably dead and a plain `/at:auto-task NNN` re-run refuses. The hardest block — and a correct guard. |
| auto-task Step 2 | "Unless there are major flags, write the plan to the task file." | The write that actually blocks: it consults neither status nor an existing plan, so any re-entry reaching Step 2 replaces *the* `## Implementation Plan` section wholesale — no append, no supersede — destroying the record of what was built. plan-task Step 6 is the mechanism, not the block: it is opt-in ("If the user instructed you to do so"). |
| impl-task Step 3 | "Work through the implementation plan step by step." | No delta concept. A re-run re-walks committed steps, and `/at:tdd` finds no RED because everything is already green — a re-executed done step *is* the "unexpected green" impl-task's own Guidance says to distrust. |
| clarify-task Step 6 | "Finally, set the task status to `ready-for-dev`" | Unconditional. Running clarify on an implemented task drags it back to `ready-for-dev`, erasing that it was ever built — and auto-task Step 0.3 runs clarify on every run. |
| review-task Step 2 | "For each acceptance criterion, determine: **pass**, **fail**, or **unclear**." | A retracted-but-still-listed AC gets re-verified: it fails, or worse, passes against code that should be gone. |
| create-task § Task states | "`new` → `ready-for-dev` (end of clarify) → `in-dev` (start of impl) → `ready-for-signoff` (end of task review) → `done` (ship). Off-ramp states: `rejected` (investigated and declined), `later` (consciously postponed)" | The sole status vocabulary source. Strictly monotone, no reopen edge, no state meaning "implemented, intent has since moved", and no defined edge out of either off-ramp. |

### Softer sites — gaps, not blocks

- **plan-task Step 1** — "If the task's status is not `ready-for-dev` … flag it to the user and ask how to proceed." Flags; does not refuse. Not the blocker (the panel initially split on this; the text settles it).
- **plan-task Step 2** — "For an epic sub-task, also read the epic file's `Locked Decisions` section and the `Implementation Notes` of already-done sibling sub-tasks." A context gap, not a block: reading prior Implementation Notes is scoped to epic sub-tasks only, so re-planning an amended standalone task plans blind to its own first pass.
- **impl-task Step 1** — gates on plan *presence* only, never on status, then writes `in-dev` unconditionally. The *designed* state machine has no reverse edge at all. None of the status writes is a designed reopen: four fire without looking at where the task already is (this one, clarify-task Step 6, review-task Step 5, auto-task Step 8.3), and two of those are backwards in effect — this one and clarify-task Step 6's `ready-for-dev` above.
- **impl-task Steps 4 and 5** — the diff baseline is "from your first commit to HEAD" and Step 5 says "**Add** an `## Implementation Notes` section". Both are written once-per-run and need per-amendment scoping.
- **ship-task Step 1** — "Branch must be `task/NNN-...` with no uncommitted tracked changes." A missing guard rather than a block: no status or plan precondition, so a task whose intent changed but was never re-implemented can still be shipped. § 5 adds the clause.
- **ship-task Step 5** — `worktree remove --force` and `branch -D`, after Step 3 squashes the branch. The point of no return.

### The one affordance that already fits

create-task § Acceptance Criteria, third exception: "When the task replaces, migrates, or removes existing behaviour, include cleanup in the task if stale code or obsolete affordances would otherwise remain ambiguous."

A retracting amendment *is* a task removing existing behaviour. The convention that makes contradiction implementable already exists at task-authoring level; what is missing is a mode that reaches for it *after* implementation. Reuse it rather than inventing a convention.

## 2. Why This Is Not the Review-Feedback Loop

Stated as mechanism: **review feedback moves code within a fixed frame; amendment moves the frame.** They are not neighbours on a spectrum. The frame is held fixed at four independent sites:

1. **Triage loads the task as the frame.** auto-task Step 6.1 instruction 1: "Read the task — this is the original intent of the change." Every disposition compares *against* it; no row's outcome is "the task is wrong."
2. **review-code may not infer intent from code.** "Recover intent from the task file and the tests before judging — never infer intent from the code alone. The task file is the spec." Its Lane Discipline adds: "Do not re-check acceptance criteria or task completion — that is `/at:review-task`."
3. **review-task compares one-directionally and cannot write.** Step 2 judges code against ACs; its Guidance says "Flag issues — do not attempt to fix them; let the user decide." The one skill positioned to notice a wrong AC may not touch the spec it is grading; its only write is Step 5's status bump to `ready-for-signoff`.
4. **The status machine has no designed reverse edge** — only unconditional writes that move a task backwards by accident (§ 1).

Why built that way: auto-task spends its autonomy budget on a *fixed* target — "assume there is no human available to help you complete the task … use your own best judgement, make a note of it, proceed and flag it to the user at the end." That is only safe while the target cannot drift. If a subagent could amend the ACs, review-task's evidence standard ("A criterion passes when you can point to specific evidence") becomes circular. Step 6.1's "Never auto-reject a Critical or Major finding … surface it in the Step 9 decisions report instead and let the human decide" is the same policy from the other side: an agent may *report* that the frame is wrong; it may not *resolve* it.

Two Step 6.1 reject rows read like blocks and are not: "Would significantly change scope/goal → Reject (cite the anchor)" and "Recommends restoring behaviour an Acceptance Criterion or locked decision deliberately removed → Reject (cite the AC/decision)". They block *agent-initiated* amendment, which is correct and must stay; they say nothing about a human-initiated one. Reading them as obstacles leads to building the wrong thing — an amend disposition inside triage (alternative 4).

The row that *is* the current pressure valve: "Real issue but probably out of scope → Reject (capture as a follow-up note in the task's `## Implementation Notes`)". An intent change arriving as a review finding is recorded and dropped, and a rejected finding the human later decides to pull in-scope is the commonest amendment there is.

## 3. Entry Points

**(a) Mid-run, implementation finished, before ship — in scope, no special path.** Worktree and branch live; status `in-dev` (Step 8.3 not yet run) or `ready-for-signoff`; review and triage output possibly in flight. The rule that matters: **amend only a quiesced task.** Let the run reach the Step 9 gate — 8.1 has confirmed all changes are committed, 8.3 has bumped status — then amend. Nothing durable is lost by waiting: accepted findings are already commits, rejected ones are already on the task file. Amending while Step 4's reviews are in flight is explicitly out; it races the same task file two subagents are reading as their anchor. `--ship` does not always remove the gate: Step 9 auto-ships only "With `--ship`, and no Critical/Major finding left for a human call", and otherwise falls through to "Do not proceed without explicit user approval." So the gate survives whenever a Critical/Major was surfaced for a human call. With none, the task ships and becomes case (c).

**(b) Fresh session at `ready-for-signoff` — in scope, needs a re-attach rule**, which § 5 makes amend-task's first act, since the amendment has to be written on the branch. The branch exists; the worktree may or may not, since auto-task Step 9 only *offers* to open it and ship-task Step 5 is what removes it. Worktree present at the expected path → adopt it. Branch present, worktree gone → `git worktree add <path> task/NNN-<slug>` (no `-b`, and not from `main`, which is what Step 1's current command does), then re-run worktree-init, since a fresh worktree shares no installed deps with the primary checkout. After re-attach, (a) and (b) share one path.

*The panel split immaterially on which is primary:* one panelist argued (a) (workspace intact, cheapest), the other (b) (it survives closing the terminal, which is the actual reason to build anything). Both are in scope; the split does not change the design.

**(c) Already shipped — out of scope.** ship-task Step 5 deleted the branch and removed the worktree, and Step 3 squashed the commits into one on `main`. No plan-step-to-commit mapping survives, so the amendment's only real question — what already-built work does this invalidate — can only be answered by reading `main`, which is the normal starting state of every new task. An amendment path here is a new task wearing an old number, and it would break the one-squash-per-task trace ship-task Step 3 deliberately creates.

**Named substitute:** `/at:create-task` a follow-up that references the superseded task number and, because retraction removes existing behaviour, carries the cleanup criterion create-task's third exception already mandates. Optional convention to keep the trail readable: one line in the shipped task's Implementation Notes — "AC 3 superseded by task NNN".

**Prior art checked, not load-bearing.** `2026-03-06-beads-yegge.md` offers a `supersedes` link type and the queryable-state argument, but neither models nor motivates a reopen edge, and its own verdict ("markdown is fine at this scale") applies here too. `2026-03-13-task-sizing-for-agents.md` bears on when to amend versus split, not on the mechanism. Neither changes the recommendation.

## 4. Recording a Contradicting Amendment

**Form: in-place edit of the live AC list, plus an append-only `## Amendments` log.**

- **The live AC list is edited in place** — retracted ACs deleted, replaced ones rewritten, new ones appended. This is non-negotiable: review-task Step 2 iterates "each acceptance criterion", so anything left in that section (struck through, tagged `[superseded]`, or parked under a sub-heading) gets re-verified. Keeping retracted text in the verification surface *is* the bug.
- **`## Amendments`** carries what the in-place edit destroys: one dated entry per amendment, saying what changed, one line of why, and the **verbatim text of every retracted or replaced AC**. It is the only place a retracted AC survives, and the only thing that explains code in `main`'s history. It is also what review-task Step 3's two bullets — "Check that the implementation truly matches the *why* in the description" and "If there were deviations from the plan, check that they are justified" — need in order to stay meaningful.
- **Every retraction carries a positive cleanup AC** in the live list — the direct instantiation of create-task's third exception. Retracting "X happens" yields "no X remains" or "behaviour is now Y", which is what makes the delta implementable and re-verifiable. Nothing downstream needs a concept of a negative AC.
- **Who writes it:** `/at:amend-task` drafts, the human confirms. Never triage, never a step running unattended.

The cleanup AC also supplies **the authority to delete the tests that covered the retracted behaviour**, which vendored `/at:tdd` otherwise denies: "When to delete tests: Only when a test is redundant with another test and removing it does not reduce confidence or clarity." A test for deliberately-removed behaviour is not redundant, it is obsolete, and `/at:tdd` has no such category. Routing that authority through a task AC keeps the fix out of the vendored file — no core-skills round trip.

**Implemented code: forward-only.** The cleanup AC drives removal or replacement as new commits on the same branch. Do not `git revert` the implementing commits as policy and never rewrite history: ship-task squashes anyway, so intermediate churn is invisible on `main`, and revert expresses retraction but not replacement. Revert stays available as an implementation choice inside a cleanup step when the retracted code is cleanly isolated and nothing replaces it; the plan delta says which.

**Plan steps: kept verbatim.** The amendment's plan sub-section opens by naming the original step numbers it supersedes. Deleting them makes the branch unreadable — impl-task Step 2 reads the plan to build context, and a reviewer reconstructs from it why committed code looks as it does. Delete only steps whose code never landed.

**Implementation Notes: append, never rewrite.** They are the historical record review-task Step 3 checks deviations against, and a note recording a deviation for now-retracted behaviour remains true *as history*. The re-run appends a dated block opening with a pointer to the amendment it implements. A note that reads as *current* state and is now false gets a correcting line in the new block, not an edit to the old one.

Net task-file change: one new section (`## Amendments`); `## Implementation Plan` and `## Implementation Notes` move from single-write to append-with-supersede.

## 5. Recommendation

**`/at:amend-task` — a new skill, the human entry point and sole author of the AC and amendment delta — plus a small set of sentence-level edits to existing skills.** A named combination, not a pure option either way.

Why neither pure option: no existing skill owns "change the intent of an already-implemented task". create-task mints new files via `settings.task_store.create` and its machinery is whole-task shaped; clarify-task is a consistency *gate*, not an intake, and its minimal-edit rule forbids exactly this edit. So intake needs a new home. But everything downstream — planning the delta, executing it, re-verifying, shipping — is existing machinery that needs scoping clauses.

**First act: ensure the workspace. The amendment is written on the task branch.** With the default in-repo task store the task file lives *inside* the worktree, and "task-file edits (plan, status bumps) ride the task branch" (auto-task Step 1) — so the copy in the primary checkout, on `main`, is the *pre-implementation* task file. Verified on this very task: `git show main:tasks/002-amend-task-re-implement.md` carries no `## Implementation Plan`; the branch copy does. An `/at:amend-task` run against the checkout would therefore find no plan to append `### Amendment N` to, and no view of the built work a cleanup AC has to target. So amend-task ensures the workspace *before* it reads or writes anything, by the same three-way rule the Step 1 resume block below applies (adopt / re-attach with `git worktree add` / refuse if the task shipped). The AC edit, the `## Amendments` entry, the plan delta and the `amended` bump then all land on the task branch, and auto-task Step 1 later simply adopts a worktree that already exists. If config routes tasks to a separate repo the task file is "**not** in the worktree" (same step): the amendment commits at its external path instead — but ensuring the workspace still stands, since the built code is what the cleanup AC must target.

**One amendment at a time.** `/at:amend-task` refuses while the plan already carries an unimplemented amendment block — the same plan-shape signal the guards use — and tells the human to implement or abandon it first. Stacked blocks cannot work: impl-task Step 3 executes only the newest, ship-task Step 1 refuses while any is unimplemented, and auto-task invokes `/at:impl-task` exactly once per run (Step 3). So blocks N and N+1 could not both complete in one re-entry, and N+1 would execute before N — wrong precisely when N+1 supersedes N's steps.

### Status: one new value, `amended`

Semantics: *implemented, intent changed, a delta needs implementing.* Single new edge: `ready-for-signoff → amended → in-dev`, then `ready-for-signoff` → `done` unchanged. Written only by `/at:amend-task`. `ready-for-signoff` is the only source state § 3 produces: (a)'s quiesced rule makes every in-scope amendment wait for the Step 9 gate, reached only after Step 8.3's bump, and (b) starts there. No `in-dev → amended` edge is needed — a task at `in-dev` is either mid-run, which § 3(a) excludes, or mid-amendment, which the one-amendment-at-a-time rule forbids amending again. A finished *standalone* impl-task run also rests at `in-dev`; letting review-task Step 5 bump it first keeps the vocabulary to one edge.

**The operative test is plan shape, not status.** `status: amended` declares the intent, but impl-task Step 1 writes `in-dev` the moment the re-run starts — so an amendment abandoned mid-flight is, by status alone, indistinguishable from ordinary in-progress work, and every guard keyed on `amended` would silently stop firing. The durable signal is the plan: **an `### Amendment N` block with no matching per-amendment Implementation Notes block is an amendment not yet implemented.** Only `/at:amend-task` (via plan-task) writes the first half; impl-task Step 5's append-per-amendment convention writes the second. The guards below key on that; `amended` rides alongside as the declared, human-readable intent.

**The signal is amendment-granular; the interruption it must survive is commit-granular.** Step 5 writes the notes block at the *end* of a run, after Step 3 has already committed work, so a run interrupted between the two leaves an `### Amendment N` block with no notes block — marked unimplemented while in fact partly built. No extra marker closes that: one written before the work lies if the run dies, one written after has the identical hole. What closes it is the branch, and it is part of Step 3's scope clause (table below), not a separate mechanism: impl-task Step 2 already reads the code before Step 3 runs, and the `A<N>.k` step ids let Step 3 match the amendment's steps against landed commits and start at the first with none — so a resume skips committed work instead of re-walking it. What remains open is only how much of that matching procedure impl-task should spell out versus leave to the implementer (§ Panel Limitations).

| Site | Change |
| --- | --- |
| create-task § Task states (vocabulary source) | Add `amended` and the one backwards edge |
| clarify-task Step 6 | One conditional keyed on plan shape, not status: skip the `ready-for-dev` bump while the plan carries an unimplemented amendment block. It must cover the `in-dev` case too — impl-task Step 1 writes `in-dev`, so every later auto-task re-entry runs Step 0.3 clarify on a mid-amendment task and would otherwise perform § 1's block verbatim. Step 0.3 runs *before* Step 1's worktree, so read the block off the task branch (`git show task/NNN-<slug>:<task-path>`), not the checkout's `main` copy |
| plan-task Step 1 | Accept `amended`, with the delta-only mode attached to that case |
| plan-task Step 2 | Extend the read-prior-Implementation-Notes rule from epic sub-tasks to amended tasks |
| plan-task Step 6 | Append/supersede variant for the delta |
| impl-task Step 1 | Unchanged — readiness gates on the `Implementation plan` section's *presence*, which an `### Amendment N` sub-section does not disturb; the `in-dev` write stands, being the correct forward move from `amended` |
| impl-task Step 3 | Scope clause: execute only the newest `### Amendment N` block with no Implementation Notes block, matching its `A<N>.k` steps against landed commits so a resume skips committed work; earlier steps are given state, still read in Step 2. Inert once every block is noted — the fix-lane state (auto-task Step 6.2), where Step 3 runs as today |
| impl-task Step 4 | Diff baseline becomes the first commit *of this amendment*; the AC sweep stays whole-task, which is correct now the list is the amended list |
| impl-task Step 5 | Append a per-amendment notes block instead of creating the section |
| review-task Step 3 | One clause: superseded plan steps are not deviations — `## Amendments` is the justification. Without it, "If there were deviations from the plan, check that they are justified" reads deliberately-deleted code against a step § 4 keeps verbatim |
| review-task Step 5, auto-task Step 8.3 | Unchanged — both write `ready-for-signoff`, where the re-run correctly lands |
| auto-task Step 1 | An explicit "resuming an amended task" block: adopt the worktree amend-task ensured (or re-attach it), skip the dead-leftover check, continue at Step 3. § 1's hardest block, and the authoritative re-entry mechanism (below) |
| auto-task Step 2 | Skip the re-plan when the plan already carries an unimplemented amendment block. Defence-in-depth, not the mechanism: Step 1's resume block jumps to Step 3, so an amend-task hand-off never reaches Step 2. This catches a run that arrives by another path |
| ship-task Step 1 | One clause: refuse while the plan carries an unimplemented amendment block — keyed on plan shape, since `status: amended` alone misses a run abandoned after impl-task Step 1 bumped it to `in-dev` |
| ship-task Step 2 | Unchanged — still writes `done`; unreachable while Step 1 refuses an unimplemented amendment |
| `settings.task_store.status` | Unchanged. It owns *how* status is written, not which values exist, so no config file changes and CLAUDE.md's four-file rule is not triggered |

**What `amended` earns, now the guards read plan shape.** Not the operative test. Three narrower jobs: (i) plan-task Step 1's gate discriminator — the one site that must branch on status ("If the task's status is not `ready-for-dev` … flag it to the user"); (ii) the declared, human-readable intent in the task file itself, *read on the branch* — a status committed there is invisible to a scan of the checkout where `main` lives, so no frontmatter-scan visibility is claimed for it; (iii) ship-task's cheap human-facing signal beside the plan-shape refusal. **Cost of the obvious hack** (reuse `ready-for-dev`): plan-task Step 1 takes it as clearance to write *the* plan from scratch against a half-built repo, and every reader of the task file sees a task queued for a first build that was in fact already built.

### Plan delta

A new `### Amendment N` sub-section under the existing `## Implementation Plan`, opening with one line naming what already-built work it invalidates and which original step numbers it supersedes. plan-task's Guidance applies unchanged, and `/at:amend-task` delegates the drafting to plan-task rather than duplicating planning judgement. Two constraints: the heading must not break impl-task Step 1's `Implementation plan` section check, and step numbering must stay unambiguous — **the scheme to adopt is `A<N>.1, A<N>.2, …`**, so a step id names its amendment and can never collide with an original step number or with a later amendment's.

### AC delta

Per § 4, authored by `/at:amend-task` alone, which then re-gates the amended task via clarify-task. Apply create-task Step 4's decomposition triggers as a size fence: if the amendment runs to "More than ~10 ACs", or clusters into distinct themes, hand back to create-task instead of amending.

### Re-entry into auto-task: Step 3, plan-shape-driven, guard preserved

Steps 4–9 then run normally — the branch changed, so every review and gate must re-run. Step 0's preflight still runs (cheap, and the roster may have moved). Step 2 is bypassed by the jump out of Step 1 — that jump is the authoritative mechanism, and the Step 2 skip in the table above is defence-in-depth for a run reaching Step 2 by another path (a human invoking auto-task without amend-task's hand-off). Either way, what must not fire on an amended plan is Step 2's own last line, "Unless there are major flags, write the plan to the task file": it writes the plan wholesale and overwrites the amendment — the hard block of § 1, reached on the way in. auto-task Step 1 gains one explicit "resuming an amended task" block rather than scattered conditionals:

worktree present at the expected path with the task branch checked out (the normal case, since amend-task ensured it) → adopt it, skip the dead-leftover check, continue at Step 3; branch present, worktree gone → re-attach with § 3(b)'s command; no branch → the task shipped → refuse, and point at the file-a-new-task substitute.

**The guard is not weakened.** The refusal exists because "real work could be lost", and the amended re-entry is precisely the case that *wants* that work. The bypass keys on two conjoined facts — a plan carrying an unimplemented `### Amendment N` block **and** a branch matching this task's number and slug — a combination no stale or abandoned branch carries, since the block exists only if someone authored an amendment (normally `/at:amend-task`; a direct `/at:plan-task` run on a hand-set `amended` task can author one too, which the guard neither needs nor forbids). Keying it on `status: amended` would fail precisely where it is needed: impl-task Step 1 writes `in-dev` as soon as the re-run starts, so an amendment interrupted mid-flight and resumed in a later session would meet the original refusal again, on a branch many commits ahead. Every other stale-branch case still refuses.

Invocation: `/at:amend-task <task-path> [what changed]`, ending in a hand-off; `/at:auto-task NNN` then picks up the unimplemented amendment and resumes. Neither panelist wanted an in-run interrupt hook.

### Human-initiated only: yes

An agent may **propose** an amendment — the natural producers are Step 6.1's reject rows and review-task Step 2 failures — but only through the channel that already exists for frame problems: surface it in the Step 9 decisions report for a human call. `/at:amend-task` requires explicit human invocation and human confirmation before it writes anything, and `--ship` must never reach it. If an agent could invoke it, triage would gain a route to legalise scope creep by rewriting the AC a finding violates, and "Reject (cite the anchor)" would stop meaning anything.

## 6. Alternatives Considered

1. **Close it and file a new task** *(the yardstick, and the right answer for shipped work)* — wrong pre-ship: it splits one unshipped change across two tasks and branches, forces shipping code the human just called wrong, and discards the plan and Implementation Notes the new task must then reconstruct.
2. **impl-task Step 6 "Integrate Feedback"** *(the live default)* — absorbs the change as code only: no AC edit, no plan record, no status move, no re-review, so the task file ends up asserting an intent the code no longer implements and review-task keeps grading the stale rubric.
3. **Do nothing; document the manual workaround** *(the most honest rival)* — open the worktree at Step 9 and drive Step 6 by hand. Genuinely suffices for a small in-session tweak, and it is what happens today; loses on durability across sessions and on review-task verifying a disowned spec.
4. **Extend Step 6.1 triage with an "amend the task" disposition** — puts anchor-moving inside the autonomous loop and destroys the property that makes triage's rejections trustworthy.
5. **Bump status back to `ready-for-dev` and re-run** — erases that the task was implemented: plan-task Step 1 reads it as clearance to plan from scratch against a half-built repo, and any reader of the task file sees a task that was never built. The branch guard is no longer the objection — keyed on plan shape, it adopts the branch either way.
6. **Make clarify-task the amendment intake** — right gate, wrong intake: its goal is internal consistency, Step 4 forbids edits beyond the strictly necessary, Step 6 drags status backwards, and auto-task Step 0.3 invokes it unattended.
7. **Let plan-task rewrite the plan on re-run** — Step 6 writes the section wholesale, so the record of what was built is lost and the re-run cannot distinguish new work from done work.
8. **Keep retracted ACs inside the AC list** (strike-through or a "superseded" sub-heading) — review-task Step 2 iterates every AC and re-verifies them.
9. **Track the amendment outside the task file** — the Context sections of create-, clarify-, plan-, impl-, review- and ship-task all rest on "the task file plus repo state carry everything the next agent needs"; a second artefact breaks that invariant.
10. **Model the amendment as an epic sub-task** — the machinery is for splitting planned work, not correcting intent, and each sub-task gets its own branch, worktree and ship, which is what the unshipped case is trying to avoid.
11. **A real task state machine with a reopen transition and audit trail** (beads-shaped) — buys queryable history that git already carries for a markdown file, at the cost of a state machine in a plugin whose whole state store is one frontmatter line.
12. **`git revert` the invalidated commits, then re-plan from a clean base** — expresses retraction but not replacement, and ship squashes anyway; keep revert as a choice *inside* a cleanup step.
13. **A `--resume <step>` flag on auto-task** — a second resume mechanism competing with the status field, and it needs the human to know auto-task's step numbering.
14. **A new config setting** (amendment policy, state name, log location) — nothing varies per project, and CLAUDE.md prices any setting at four files.
15. **Edit `/at:tdd` to sanction deleting tests for retracted behaviour** — vendored, so it needs a core-skills change plus a re-vendor; the authority belongs in the task's cleanup AC, where it is per-case and auditable.
16. **A dedicated `/at:re-impl` that only re-runs implementation** — the cheap-looking half; leaves the AC and plan deltas unrecorded, which is the part that makes the re-run reviewable.
17. **Allow agent-initiated amendment when review-code surfaces a genuine design flaw** — duplicates the Critical/Major-surfaced-for-a-human-call route Step 9 already owns, and unbounds scope.

## Panel Limitations

- **Single model family.** Codex was unavailable, so the two perspectives are not independent across families and the strongest signal — cross-family disagreement — is missing. The two panelists converged on the recommendation's shape, which under a single family is weaker evidence than it looks.
- **Two divergences, both recorded above rather than resolved away:** whether plan-task Step 1 is a gate or a flag (settled on the text: a flag), and which entry point is primary (immaterial — both are in scope and share one path).
- **Not addressed by either panelist:** amending an *epic sub-task*, where locked decisions are shared across siblings; and whether the README and demo text need to name the amendment path once it exists.
- **Left open by this doc:** how much of the commit-matching procedure impl-task Step 3 should spell out versus leave to the implementer (§ 5). *That* a resume matches its `A<N>.k` steps against landed commits is settled; how prescriptively to write it is not. All three are open questions for the follow-up task.
