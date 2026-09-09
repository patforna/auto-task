---
title: Amend a Task Mid-Flight and Re-Implement
date: 2026-09-09
status: in-dev
type: research
---

## Amend a Task Mid-Flight and Re-Implement

Work out how auto-task should support changing a task's intent after implementation has finished — amend the task, extend its plan, re-run implementation.

Trigger: the human reviews the finished code and concludes the implementation itself needs to change, not just be fixed.

### Acceptance Criteria

- The report says whether the current workflow supports this, naming the closest existing affordances and exactly where they block.
- It separates this case from the existing review-feedback loop: here the human changes the task, not just the code.
- It covers both entry points — inside an auto-task run once implementation is done and before ship, and later in a fresh session against a task at ready-for-signoff. It says whether an already-shipped task is in scope.
- It covers intent changes that contradict an already-implemented AC, not just additive ones, and says how a retracted or replaced AC is recorded.
- It recommends one option — new skill, extending existing skills, or a named combination of both — and says how status transitions and plan/AC deltas are handled. Design-level: enough that a follow-up task needs no further research, but no drafted skill body.
- Alternatives considered are named with a one-line reason for rejecting them.
- Ends at the report.
- Findings land as a dated research doc in the repo's research folder, listed under an existing group in its index.

### Notes

- Run the research as a panel plus synthesis, like the existing proposal docs. Internal design analysis — reach for external prior art only where it would change the recommendation.

## Implementation Plan

### TLDR

Answer the question from the pipeline skills' own step text, run as a two-perspective panel plus synthesis, and land it as a dated research doc under the existing Skills/meta group in the research index. Ends at the report.

### Steps

1. **Build the block map first.** Read the actual step text (not summaries) of create-task, clarify-task, plan-task, impl-task, review-code, review-task, ship-task and auto-task in this worktree — the worktree is the source of truth; the installed plugin cache is release 0.1.0 and may be stale. Per skill, record what it reads and writes on the task file, what status it requires and sets, and what it does when the task changes under it. Quote the deciding sentence at each site rather than paraphrasing.

   Anchors the report cannot omit without failing AC1:

   - auto-task Step 1 — refuses to start unless an existing branch/worktree is a provable dead leftover, so a plain re-run cannot proceed.
   - auto-task Step 6.1 — two reject rows deflect exactly this class of change ("would significantly change scope/goal"; "recommends restoring behaviour an AC or locked decision deliberately removed").
   - impl-task Step 1 (stops only on a *missing* plan, else bumps to in-dev) and Step 3 (walks the whole plan — no delta concept, so a re-run re-executes done steps).
   - plan-task Step 1 (ready-for-dev gate) and Step 6 (writes *the* Implementation Plan section — no append or supersede); it reads prior Implementation Notes only for epic sub-tasks.
   - clarify-task Step 4 (minimal edits) and Step 6 (unconditional bump to ready-for-dev — for an amended task a backwards move nothing downstream expects).
   - review-task Step 2 and Step 5, auto-task Step 8.3 — nothing anywhere moves status backwards, and a retracted AC left in place gets re-verified and fails.
   - ship-task Step 5 — branch deleted, worktree removed; the only step that destroys the workspace.
   - create-task § Task states, and § Acceptance Criteria's third exception (a task removing existing behaviour must carry the cleanup).

   Closest existing affordances to name: impl-task Step 6 "Integrate Feedback", auto-task Step 9's open-the-worktree hand-off, and the `[further user instructions]` argument every skill takes. Nothing in the repo names this scenario — that absence is itself a finding; don't keep hunting.

2. **Run the analysis as a panel plus synthesis, not a single pass.** Frame the panel prompt as the questions in steps 3–6, let each panelist inventory cold, then merge without forcing consensus. Record the line-up and where perspectives diverged in the doc's method line — the existing proposal docs carry that provenance. Panel runs on the main thread (its own precondition); if Codex is unavailable, substitute a second independent Claude panelist and note the degradation rather than dropping the second perspective. Internal design analysis: reach for external prior art only where it would change the recommendation — adjacent corpus material is 2026-03-06-beads-yegge.md (task state machines) and 2026-03-13-task-sizing-for-agents.md.

3. **State the loop separation in mechanism terms** → AC2. The review-feedback loop treats the task as the fixed anchor and is designed to reject anything that moves it; amendment moves the anchor. Cite the Step 6.1 rows. "One changes code, one changes the task" alone doesn't show where the current design actively resists this.

4. **Walk each entry point from its concrete starting state** → AC3.

   - Mid-run, implementation finished, before ship: worktree and branch live, status in-dev or ready-for-signoff, review/triage output possibly in flight.
   - Fresh session at ready-for-signoff: branch exists; the worktree may or may not still be there (auto-task Step 9 leaves it, nothing guarantees it).
   - Already shipped: branch deleted, history squashed onto main, worktree gone, status done. Return a verdict with a reason — in scope, or out with "file a new task" named as the substitute. Leaving it open fails AC3.

5. **Decide how a contradicting amendment is recorded, and what happens to the work it invalidates** → AC4. Name one recording form (in-place edit plus amendment log, superseded-AC list, strike-through) and who writes it. Cover the consequence: retracting an AC usually leaves implemented code behind, so the amendment carries an explicit cleanup criterion. Say what becomes of the plan steps and Implementation Notes covering the retracted behaviour.

6. **Pick one option and specify it design-level** → AC5. Whichever wins (new skill, extend existing, named combination), answer:

   - Status transitions — a new state or a defined backwards move, plus every site that writes status: create-task Step 2's task-states line (the vocabulary source), clarify-task Step 6, impl-task Step 1, review-task Step 5, auto-task Step 8.3, ship-task Step 2, and settings.task_store.status in auto-task.config.defaults.md. Name the cost of the obvious hack (bump back to ready-for-dev): it erases that the task was ever implemented.
   - Plan delta — append, supersede or rewrite, and how impl-task executes only the delta instead of re-walking the whole plan.
   - AC delta — per step 5.
   - Re-entry into auto-task — which step it resumes at, and what it does about the branch/worktree guard in Step 1.
   - Whether amendment is human-initiated only.

   Constraints that price the options: panel, synthesize and tdd are vendored, so a recommendation touching them routes through core-skills plus a re-vendor, not an edit here; a new config setting drags four files along (CLAUDE.md), so prefer none.

7. **Name the alternatives with a one-line rejection each** → AC6, including the two live defaults today: "use impl-task Step 6 feedback" and "close it and file a new task". The latter is the yardstick every other option must beat.

8. **Write the doc and index it** → AC7, AC8. `docs/research/2026-09-09-amend-task-re-implement.md`, in the corpus shape: H1, a one-line date/method line, the problem anchor, the bottom line, then analysis, alternatives and provenance. No frontmatter — research docs have none. Calibrate length and register against 2026-04-09-skill-improvements-proposal.md and 2026-06-03-agentic-design-review-sota.md (~150–200 lines), not the long survey docs. Add one row under the existing Skills/meta group in docs/research/README.md, in that table's existing form.

### Notes

- For a research task the conclusions are the deliverable, so this plan fixes method, evidence base, output shape and scope fence — not the recommendation.
- No test harness and no verification command in this repo; don't invent one for a markdown deliverable. The checks that matter: `git status` shows exactly two changed files (the new doc and the research README), and each of the eight ACs maps to a named section of the doc.
- Dominant failure mode is the report sliding into drafting the skill. If a section starts reading like a SKILL.md, cut it back.

## Implementation Notes

Delivered: `docs/research/2026-09-09-amend-task-re-implement.md` (183 lines) plus one index entry. Exactly two files changed besides this one.

**Deviations from the plan and from impl-task, both deliberate.**

- **No TDD, no verification command.** The deliverable is a markdown document and this repo has no test harness, so `/at:tdd` and impl-task Step 3's failing-test rule do not apply and nothing was invented to stand in for them. Each plan step's check was the AC it satisfies, verified by reading the draft against the eight ACs; the plan's own two checks (two changed files, every AC mapped to a named section) both hold.
- **Index entry is a cell extension, not a new table row.** The plan said "add one row under the existing Skills/meta group", but that table is one row *per group* with the docs listed inside the cell — a second row labelled `Skills/meta` would have looked like a defect. The doc is appended to the existing Skills/meta cell, which is what "listed under an existing group" (AC8) asks for and keeps the table's form. Cell padding was left at the table's existing 184-char width, so the rest of the table is untouched.

**AC → section map** (all against the delivered doc):

| AC | Where |
| --- | --- |
| 1 support verdict, closest affordances, exactly where they block | Bottom Line 1 · § 1 (affordances, hard-blocks table, softer sites) |
| 2 separation from the review-feedback loop | § 2 |
| 3 both entry points, plus the shipped verdict | § 3 (a), (b), (c) with the named substitute |
| 4 contradicting amendments and how a retraction is recorded | § 4 |
| 5 one option, status transitions, plan/AC deltas | § 5 (status table, plan delta, AC delta, re-entry, human-only) |
| 6 alternatives with a one-line rejection each | § 6 (17 entries) |
| 7 ends at the report | Scope line under the Problem Anchor; `git status` shows no skill, README or config change |
| 8 dated doc in the research folder, listed under an existing group | The doc itself · `docs/research/README.md` Skills/meta row |

**Surprises and judgement calls.**

- The panel's two panelists disagreed on whether auto-task Step 6.1's two reject rows are blocks. They are not: they block *agent*-initiated amendment, which must stay. Reading them as blocks is what leads to building an amend disposition inside triage — the wrong thing. The report puts them in the mechanism section, not the block list.
- The pricing fact that makes the recommendation cheap: `settings.task_store.status` in `auto-task.config.defaults.md` says only "Edit the task file's `status:` frontmatter field in place" — it owns *how* status is written, not which values exist. Adding `amended` therefore touches zero config files and does not trigger CLAUDE.md's four-file rule.
- Two questions the plan left open were closed in the report rather than deferred: the amendment step-numbering scheme (`A<N>.1, A<N>.2, …`) and re-entry mechanism (`status: amended`, not a `--resume <step>` flag).
- Every quoted deciding sentence was re-grepped against the skills in this worktree after drafting; all matched.

**Follow-up not yet captured** (both flagged in the doc's Panel Limitations, neither in scope here): amending an *epic sub-task*, where locked decisions are shared across siblings; and whether the README and demo text need to name the amendment path once it exists. The follow-up implementation task should also expect to touch about a dozen skill files, since the new skill is the small half of the recommendation.

**Environment note:** the bash sandbox denies writes outside the primary checkout, so worktree edits went through the Edit/Write tools; the one padding-sensitive table edit ran with the sandbox disabled.

### 2026-09-09 — review findings applied

Review of the delivered doc found three design holes in § 5's recommendation, all fixed in the doc only (187 lines, still inside the 150–200 target):

- **Re-entry passed through auto-task Step 2.** Step 2 is unconditional — it consults neither status nor an existing plan — so resuming at Step 3 still re-plans via plan-task Step 6 and overwrites the amendment. § 5 now carries an `auto-task Step 2` skip row.
- **`status: amended` is not a durable marker.** impl-task Step 1 writes `in-dev` unconditionally, and runs before Step 3, so an amendment interrupted mid-flight loses the marker. The auto-task Step 1 bypass, the ship-task Step 1 refusal and the impl-task Step 3 scope clause now key on **plan shape** — an `### Amendment N` block with no matching per-amendment Implementation Notes block. `amended` stays as the declared intent.
- **`--ship` does not always bypass the gate.** auto-task Step 9 auto-ships only with no Critical/Major finding left for a human call; when one was surfaced, the gate still stops. With none, the task ships and becomes the already-shipped case.

Eight minor findings and five nits also applied (block-table rows reclassified, quote elisions restored, the "every skill" claims scoped to the skills that actually carry the text, ship-task Step 2 added to the status table, `in-dev → amended` reconciled with § 3(a)'s quiesced rule). Two proposed findings were rejected as non-defects and left alone. Every fix was re-verified against the skill text in this worktree.

### 2026-09-09 — second review round applied

The re-keying above left status-based arguments standing next to plan-shape guards. Three majors, nine minors/nits fixed in the doc (190 lines, still inside 150–200); this file's `--ship` line qualified.

- **The plan-shape signal is amendment-granular; interruption is commit-granular.** impl-task Step 5 writes the notes block at the end of a run (`skills/impl-task/SKILL.md:75`), after Step 3 has committed — so a run interrupted between them re-selects an amendment whose steps are partly built. Stated honestly in § 5 rather than papered over: the reconciliation is the branch (Step 2 reads the code; `A<N>.k` ids match steps to landed commits), no new marker was invented, the "stays in step across sessions" claim is gone, and the residual is now an open question in Panel Limitations. Step 3's clause also gained the all-blocks-noted case (the fix-lane state auto-task Step 6.2 runs in).
- **One authoritative re-entry mechanism.** Step 1's resume jump is the mechanism; the `auto-task Step 2` skip is defence-in-depth for a run arriving by another path. It is no longer described as load-bearing.
- **The warrant for `amended` re-argued narrowly.** Plan shape now covers impl-task Step 3 and auto-task Step 1, so `amended` earns its place as plan-task Step 1's gate discriminator, the declared intent a human or status scan reads, and ship-task's human-facing signal. "Cost of the obvious hack", alternative 5's rejection and the clarify-task Step 6 row's rationale were rewritten to the cost that actually remains.

Minors: the wholesale plan write re-attributed from plan-task Step 6 (opt-in, `skills/plan-task/SKILL.md:97-99`) to auto-task Step 2's own last line (`skills/auto-task/SKILL.md:113`) in both places, "unconditionally" dropped for the accurate sense; the backwards-write enumeration opened up to all four unconditional status writes; `in-dev` narrowed off the mid-Step-4 state § 3(a) excludes; the bypass no longer claims amend-task exclusivity; the impl-task Step 6 parenthetical fixed (review-task Step 4 also waits unbounded, `skills/review-task/SKILL.md:55`). Nits: quote capitalisation, review-design's argument variant added, the `--ship` ranking dropped, three § 5 cells trimmed.

One finding cited its evidence imprecisely: m4 attributed "Unless there are major flags, write the plan to the task file" to § 1's neighbouring cell, where the quote is plan-task Step 6's "If the user instructed you to do so…". The defect it names is real either way — both quotes are conditional, so "unconditionally" over-claimed — and was fixed.

### 2026-09-09 — third review round applied

An adversarial gap-check found three majors and five minors/nits; all were real and all are fixed in the doc (194 lines, still inside 150–200 — the six added lines were paid for by collapsing the Step 1 resume bullets, which § 3(b) and the new workspace paragraph already state). Every claim was re-verified against the skill text in this worktree before editing.

- **Where the amendment is written was unspecified, and the ordering was wrong.** With the default in-repo store the task file lives in the worktree and "task-file edits (plan, status bumps) ride the task branch" (`skills/auto-task/SKILL.md:103`) — verified empirically: `git show main:tasks/002-amend-task-re-implement.md` carries no `## Implementation Plan` and reads `status: ready-for-dev`, while the branch copy carries both. So an amend-task run against the primary checkout would see the pre-implementation task file. § 5 now makes ensuring the workspace amend-task's *first* act (adopt / re-attach / refuse if shipped), states that every amendment write rides the task branch, leaves auto-task Step 1 merely adopting a worktree that already exists, and carries one clause for the external-task-store case. The "What `amended` earns" passage no longer claims frontmatter-scan visibility — a status committed on the task branch is invisible to a scan of the checkout where `main` lives; the same over-claim was narrowed in "Cost of the obvious hack" and in alternative 5.
- **Stacked unimplemented amendments dead-ended the pipeline.** impl-task Step 3 executes only the newest block, ship-task Step 1 refuses while any is unimplemented, and auto-task invokes `/at:impl-task` exactly once per run (`skills/auto-task/SKILL.md:115-119`), so N and N+1 cannot both complete in one re-entry and N+1 would run before N. § 5 gains a **one-amendment-at-a-time** rule (amend-task refuses while the plan carries an unimplemented block), and the `in-dev → amended` edge's "abandoned amendment re-run" justification — which that rule forbids — is gone. Per m7 the edge is narrowed to `ready-for-signoff → amended → in-dev`, the only source state § 3 produces.
- **§ 5 described the impl-task Step 3 clause two contradictory ways.** The commit-matching version in the change table is now the single reading: the clause matches `A<N>.k` steps against landed commits so a resume skips committed work. The prose passage was rewritten to match (it no longer says the clause re-selects already-committed steps, nor files the remedy as open), and Panel Limitations now asks only how prescriptively impl-task should spell the matching out.

Minors: § 1's hard-block row relabelled from plan-task Step 6 (opt-in, `skills/plan-task/SKILL.md:97-99`) to **auto-task Step 2**, the site that actually blocks; the impl-task Step 1 change row marked **unchanged** (readiness gates on the section's presence only, `skills/impl-task/SKILL.md:45`); the clarify-task Step 6 conditional re-gated on plan shape so it covers the reachable `in-dev` case too — plus the wrinkle that Step 0.3 runs before Step 1's worktree, so the block must be read off the task branch; a **review-task Step 3** row added (superseded plan steps are not deviations, `## Amendments` is the justification, `skills/review-task/SKILL.md:51`). Nits: the six skills carrying the "task file plus repo state" sentence named instead of "all"; an **auto-task Step 1** row added to the § 5 change table; Bottom Line 1 no longer claims all three near-affordances change code.

§ 5 was re-read end to end as one piece afterwards: it tells one story — the amendment is written on the task branch after amend-task ensures the workspace, plan shape is the operative signal, one amendment at a time, and the change table lists every site including auto-task Steps 1 and 2.
