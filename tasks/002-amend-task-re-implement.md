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
